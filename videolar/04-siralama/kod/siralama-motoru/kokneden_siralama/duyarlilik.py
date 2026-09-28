"""Monte Carlo duyarlılık analizi.

Her turda şu belirsizlikler aynı anda örneklenir:
1. Matris puanları: dolu hücre p_dolu olasılıkla ±1; 'gerekçesi zayıf' hücre p_zayif ile ±1;
   boş hücre p_bos olasılıkla 1 olur. Puanlar 0-4'e kırpılır.
2. λ (kök skorundaki D−R / D dengesi) ~ U(0.3, 0.7)
3. Ağırlıklar ~ Dirichlet(c · w0)
4. Açık skoru yöntemi: Φ(z) ya da yüzdelik (yarı yarıya); verisi olmayan A ~ U(0, 1)
5. Etki düzeyi: p_etki olasılıkla ±1 düzey
(Not: 0-4 ve 1-3 sınırlarında kırpma nedeniyle sınırdaki hücrelerin etkili oynama olasılığı yaklaşık yarıdır.)
6. Toplama türü: geometrik ya da aritmetik (yarı yarıya)

Çıktı: her sorun için sıra dağılımı, ilk-5'te ve 1. sırada olma olasılığı, neden grubunda
olma olasılığı; tur başına Kendall tau (taban sıralamaya göre).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from .dematel import dematel, kok_skoru
from .oncelik import VARSAYILAN_AGIRLIK, oncelik, sirala
from .skorlar import ETKI_DUZEY


@dataclass
class DuyarlilikAyari:
    n: int = 10_000
    tohum: int = 20260921
    p_dolu: float = 0.30
    p_zayif: float = 0.50
    p_bos: float = 0.05
    lam_aralik: tuple[float, float] = (0.3, 0.7)
    dirichlet_c: float = 20.0
    p_etki: float = 0.25
    matris: bool = True
    agirlik: bool = True
    acik: bool = True
    etki: bool = True
    toplama: bool = True
    ilk_k: int = 5


@dataclass
class DuyarlilikSonucu:
    siralar: np.ndarray          # (n_tur, n_sorun)
    tau: np.ndarray              # (n_tur,)
    neden_mi: np.ndarray         # (n_tur, n_sorun) bool
    ayar: DuyarlilikAyari = field(repr=False)

    def ozet(self, idler: list[str]) -> pd.DataFrame:
        k = self.ayar.ilk_k
        s = self.siralar
        return pd.DataFrame({
            "sorun_id": idler,
            "sira_ortanca": np.median(s, axis=0),
            "sira_p05": np.percentile(s, 5, axis=0),
            "sira_p95": np.percentile(s, 95, axis=0),
            f"ilk{k}_olasilik": (s <= k).mean(axis=0),
            "birinci_olasilik": (s == 1).mean(axis=0),
            "neden_grubu_olasilik": self.neden_mi.mean(axis=0),
        })


def _bozuk_matris(A, zayif, ayar, rng):
    B = A.copy()
    n = len(A)
    dolu = A > 0
    p = np.where(dolu, np.where(zayif, ayar.p_zayif, ayar.p_dolu), 0.0)
    oynat = rng.random((n, n)) < p
    B = B + oynat * rng.choice([-1, 1], size=(n, n))
    yeni = (~dolu) & (rng.random((n, n)) < ayar.p_bos)
    B = np.where(yeni, 1, B)
    B = np.clip(B, 0, 4)
    np.fill_diagonal(B, 0)
    return B


def monte_carlo(A, A_phi, A_yuzde, etki_duzey, zayif=None,
                ayar: DuyarlilikAyari | None = None, taban_sira=None) -> DuyarlilikSonucu:
    """A_phi / A_yuzde: NaN = veri yok. etki_duzey: 1-3 tamsayı."""
    ayar = ayar or DuyarlilikAyari()
    rng = np.random.default_rng(ayar.tohum)
    A = np.asarray(A, dtype=float)
    n = len(A)
    zayif = np.zeros_like(A, dtype=bool) if zayif is None else np.asarray(zayif, dtype=bool)
    A_phi = np.asarray(A_phi, dtype=float)
    A_yuzde = np.asarray(A_yuzde, dtype=float)
    eksik = np.isnan(A_phi)
    etki_duzey = np.asarray(etki_duzey, dtype=int)
    w0 = np.asarray(VARSAYILAN_AGIRLIK)

    if taban_sira is None:
        taban = dematel(A)
        taban_sira = sirala(oncelik(kok_skoru(taban), np.where(eksik, 0.5, A_phi),
                                    [ETKI_DUZEY[d] for d in etki_duzey]))

    siralar = np.empty((ayar.n, n), dtype=int)
    neden = np.empty((ayar.n, n), dtype=bool)
    tau = np.empty(ayar.n)
    for t in range(ayar.n):
        M = _bozuk_matris(A, zayif, ayar, rng) if ayar.matris else A
        if M.sum() == 0:
            M = A
        d = dematel(M)
        lam = rng.uniform(*ayar.lam_aralik) if ayar.agirlik else 0.5
        K = kok_skoru(d, lam)
        if ayar.acik:
            Av = A_phi if rng.random() < 0.5 else A_yuzde
            Av = np.where(eksik, rng.random(n), Av)
        else:
            Av = np.where(eksik, 0.5, A_phi)
        if ayar.etki:
            kay = (rng.random(n) < ayar.p_etki) * rng.choice([-1, 1], size=n)
            dz = np.clip(etki_duzey + kay, 1, 3)
        else:
            dz = etki_duzey
        E = np.array([ETKI_DUZEY[x] for x in dz])
        w = rng.dirichlet(ayar.dirichlet_c * w0) if ayar.agirlik else w0
        tur = ("geometrik" if rng.random() < 0.5 else "aritmetik") if ayar.toplama else "geometrik"
        s = sirala(oncelik(K, Av, E, w, tur))
        siralar[t] = s
        neden[t] = d.net > 0
        tau[t] = kendalltau(taban_sira, s).statistic
    return DuyarlilikSonucu(siralar, tau, neden, ayar)


def baglanti_etkisi(A, idler, K_fn, P_fn, esik_puan: int = 3, ilk_k: int = 5) -> pd.DataFrame:
    """Her güçlü bağlantıyı (≥ esik_puan) tek tek sıfırlayıp ilk-k listesinin nasıl değiştiğini ölçer.

    K_fn(A) → kök skoru; P_fn(K) → öncelik skoru.
    """
    taban = sirala(P_fn(K_fn(A)))
    taban_ilk = set(np.where(taban <= ilk_k)[0])
    satirlar = []
    for i, j in zip(*np.where(A >= esik_puan)):
        B = A.copy()
        B[i, j] = 0
        s = sirala(P_fn(K_fn(B)))
        yeni_ilk = set(np.where(s <= ilk_k)[0])
        satirlar.append({
            "kaynak": idler[i], "hedef": idler[j], "puan": int(A[i, j]),
            f"ilk{ilk_k}_degisti": taban_ilk != yeni_ilk,
            "cikan": ";".join(idler[x] for x in sorted(taban_ilk - yeni_ilk)),
            "giren": ";".join(idler[x] for x in sorted(yeni_ilk - taban_ilk)),
            "kaynak_sira_once": int(taban[i]), "kaynak_sira_sonra": int(s[i]),
            "tau": float(kendalltau(taban, s).statistic),
        })
    return pd.DataFrame(satirlar)


def liste_bagimliligi(A, A_taban, E, idler, K_lam: float = 0.5, ilk_k: int = 5) -> pd.DataFrame:
    """Her sorunu sırayla listeden çıkarıp kalanları yeniden sıralar: ilk-k nasıl değişiyor?"""
    A = np.asarray(A, dtype=float)
    n = len(A)
    taban = sirala(oncelik(kok_skoru(dematel(A), K_lam), A_taban, E))
    taban_ilk = [idler[i] for i in np.argsort(taban)[:ilk_k]]
    satir = []
    for k in range(n):
        m = np.arange(n) != k
        B = A[np.ix_(m, m)]
        if B.sum() == 0:
            continue
        kalan = [idler[i] for i in range(n) if m[i]]
        s = sirala(oncelik(kok_skoru(dematel(B), K_lam), np.asarray(A_taban)[m], np.asarray(E)[m]))
        yeni = [kalan[i] for i in np.argsort(s)[:ilk_k]]
        beklenen = [x for x in taban_ilk if x != idler[k]]
        satir.append({"cikarilan": idler[k], f"yeni_ilk{ilk_k}": ";".join(yeni),
                      "ilk_kume_degisti": set(yeni[:len(beklenen)]) != set(beklenen),
                      "giren": ";".join(x for x in yeni if x not in taban_ilk)})
    return pd.DataFrame(satir)
