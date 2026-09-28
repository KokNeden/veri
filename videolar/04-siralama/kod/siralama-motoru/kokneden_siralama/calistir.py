"""Uçtan uca çalıştırma.

    python -m kokneden_siralama.calistir --girdi GIRDI/ --cikti CIKTI/ [--n 10000] [--etiket v0.1]

GIRDI klasöründe:
    sorunlar.csv              sorun_id, ad, kisa_ad, sutun, ana_gosterge, yedek_gosterge, etki_duzey, etki_gerekce
    etki_matrisi.csv          ilk sütun 'etkileyen', diğer sütunlar sorun_id; hücre (i, j) = i'nin j'ye doğrudan etkisi (0-4)
    baglanti_gerekceleri.csv  (isteğe bağlı) kaynak, hedef, puan, durum [guclu|zayif|tartismali], ...
    gostergeler.csv           ulke, gosterge_id, yil, deger  (V2 çıktısı + elle eklenenler)
    gosterge_listesi.csv      gosterge_id, yon
    (sorunlar.csv isteğe bağlı sütun: karsilastirma_seti = "KOR;ESP;..." konuya göre ülke seti)
    plan_hedefleri.csv        (isteğe bağlı, BİRİNCİL ölçüt) sorun_id, plan, gosterge, baslangic_yil, baslangic,
                              hedef_yil, hedef, gerceklesen_yil, gerceklesen, kaynak

CIKTI klasörüne: sonuclar_<etiket>.csv, duyarlilik_<etiket>.csv, toplam_etki_<etiket>.csv,
                  acik_skorlari_<etiket>.csv, baglanti_etkisi_<etiket>.csv, harita + grafik PNG.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import __version__
from .dematel import dematel, esik, kok_skoru
from .duyarlilik import DuyarlilikAyari, baglanti_etkisi, liste_bagimliligi, monte_carlo
from .kontrol import kontrol_et
from .harita import ilk_k_grafigi, neden_sonuc_haritasi
from .ism import katmanlar
from .oncelik import oncelik, sirala
from .skorlar import acik_skoru, birlesik_acik, etki_skoru, plan_acigi


def matris_oku(yol: Path, idler: list[str]) -> np.ndarray:
    m = pd.read_csv(yol, index_col=0)
    m.index = m.index.astype(str)
    eksik = set(idler) - set(m.index) | set(idler) - set(m.columns)
    if eksik:
        raise ValueError(f"Matriste eksik sorun: {sorted(eksik)}")
    return m.loc[idler, idler].to_numpy(dtype=float)


def zayif_maske(yol: Path, idler: list[str]) -> np.ndarray:
    n = len(idler)
    M = np.zeros((n, n), dtype=bool)
    if not yol.exists():
        return M
    g = pd.read_csv(yol)
    konum = {s: k for k, s in enumerate(idler)}
    if "durum" not in g.columns:
        return M
    for r in g.itertuples():
        if str(r.durum) in ("zayif", "tartismali") and r.kaynak in konum and r.hedef in konum:
            M[konum[r.kaynak], konum[r.hedef]] = True
    return M


def aciklar(sorunlar: pd.DataFrame, gostergeler: pd.DataFrame, liste: pd.DataFrame) -> pd.DataFrame:
    yon = dict(zip(liste.gosterge_id, liste.yon))
    satirlar = []
    for s in sorunlar.itertuples():
        set_ = getattr(s, "karsilastirma_seti", None)
        set_ = [u.strip() for u in str(set_).split(";") if u.strip()] if isinstance(set_, str) and set_ else None
        adaylar = [g for g in [s.ana_gosterge, *str(s.yedek_gosterge).split(";")]
                   if isinstance(g, str) and g and g != "nan"]
        secilen, not_ = None, "gösterge yok"
        for k, g in enumerate(adaylar):
            seri = gostergeler[gostergeler.gosterge_id == g]
            if g not in yon:
                continue
            a = acik_skoru(seri, int(yon[g]), g, karsilastirma=set_)
            if a.A_phi is not None:
                secilen = a
                if k > 0:
                    a.not_ = f"ana gösterge ({adaylar[0]}) yok/uygun değil → yedek"
                break
            if k == 0:
                not_ = a.not_
                if int(yon[g]) == 0:  # normatif olmayan ana gösterge: yedeğe geçilmez
                    break
        if secilen is None:
            satirlar.append({"sorun_id": s.sorun_id, "gosterge_id": "", "yil": None, "tur": None,
                             "ortanca": None, "n_set": 0, "z": None, "A_phi": np.nan,
                             "A_yuzdelik": np.nan, "not": f"bilmiyoruz: {not_}"})
        else:
            satirlar.append({"sorun_id": s.sorun_id, "gosterge_id": secilen.gosterge_id,
                             "yil": secilen.yil, "tur": secilen.tur, "ortanca": secilen.ortanca,
                             "n_set": secilen.n_set, "z": secilen.z, "A_phi": secilen.A_phi,
                             "A_yuzdelik": secilen.A_yuzdelik, "not": secilen.not_})
    return pd.DataFrame(satirlar)


def plan_aciklari(yol: Path, idler: list[str]) -> dict[str, float]:
    """Her sorun için plan açığı; birden çok plan hedefi varsa ortalaması."""
    if not yol.exists():
        return {}
    p = pd.read_csv(yol)
    p = p[p.sorun_id.isin(idler)]
    p["A_plan"] = [plan_acigi(r.baslangic, r.hedef, r.gerceklesen, getattr(r, "baslangic_yil", None),
                              getattr(r, "hedef_yil", None), getattr(r, "gerceklesen_yil", None))
                   for r in p.itertuples()]
    return p.dropna(subset=["A_plan"]).groupby("sorun_id").A_plan.mean().to_dict()


def calistir(girdi: Path, cikti: Path, n: int = 10_000, etiket: str = "v0.1",
             tohum: int = 20260921) -> dict:
    cikti.mkdir(parents=True, exist_ok=True)
    sorunlar = pd.read_csv(girdi / "sorunlar.csv")
    idler = sorunlar.sorun_id.tolist()
    kisa = sorunlar.get("kisa_ad", sorunlar.ad).tolist()
    A = matris_oku(girdi / "etki_matrisi.csv", idler)
    zayif = zayif_maske(girdi / "baglanti_gerekceleri.csv", idler)
    gost = pd.read_csv(girdi / "gostergeler.csv")
    liste = pd.read_csv(girdi / "gosterge_listesi.csv")

    d = dematel(A)
    th = esik(d.T, "ortalama")
    K = kok_skoru(d, 0.5)
    ac = aciklar(sorunlar, gost, liste)
    ap = plan_aciklari(girdi / "plan_hedefleri.csv", idler)
    ac["A_ulke"] = ac.A_phi
    ac["A_plan"] = [ap.get(i, np.nan) for i in idler]
    for k in ("A_phi", "A_yuzdelik"):  # birincil ölçüt (plan) varsa birleştir
        ac[k] = [birlesik_acik(None if np.isnan(p) else p, u) if not (np.isnan(p) and np.isnan(u)) else np.nan
                 for p, u in zip(ac.A_plan, ac[k].astype(float))]
    ac["olcut"] = np.where(ac.A_plan.notna() & ac.A_ulke.notna(), "plan+ülke",
                           np.where(ac.A_plan.notna(), "plan", np.where(ac.A_ulke.notna(), "yalnız ülke (ikincil)", "yok")))
    A_phi = ac.A_phi.to_numpy(dtype=float)
    A_yuz = ac.A_yuzdelik.to_numpy(dtype=float)
    A_taban = np.where(np.isnan(A_phi), 0.5, A_phi)
    E = np.array([etki_skoru(int(x)) for x in sorunlar.etki_duzey])
    P = oncelik(K, A_taban, E)
    sira = sirala(P)
    th_ism = esik(d.T, "ortalama+kss", 1.5)
    kat = katmanlar(d.T, th_ism)

    sonuc = pd.DataFrame({
        "sorun_id": idler, "ad": sorunlar.ad, "D": d.D, "R": d.R, "D_arti_R": d.onem,
        "D_eksi_R": d.net, "grup": np.where(d.net > 0, "neden", "sonuç"),
        "kok_skoru": K, "acik_skoru": A_taban, "acik_veri": ~np.isnan(A_phi),
        "etki_skoru": E, "oncelik_skoru": P, "sira": sira, "ism_katman": kat,
        "acik_olcut": ac.olcut.to_numpy(), "acik_gosterge": ac.gosterge_id.to_numpy(),
        "acik_not": ac["not"].fillna("").to_numpy(),
        "etki_gerekce": sorunlar.get("etki_gerekce", pd.Series([""] * len(idler))).to_numpy(),
    }).sort_values("sira")

    ayar = DuyarlilikAyari(n=n, tohum=tohum)
    mc = monte_carlo(A, A_phi, A_yuz, sorunlar.etki_duzey.to_numpy(), zayif, ayar, taban_sira=sira)
    ozet = mc.ozet(idler)
    # Kaynak ayrıştırma: yalnız matris / yalnız ağırlık+yöntem belirsizliği
    parca = {}
    for ad, kw in {"yalniz_matris": dict(agirlik=False, acik=False, etki=False, toplama=False),
                   "yalniz_agirlik_yontem": dict(matris=False)}.items():
        a2 = DuyarlilikAyari(n=max(n // 4, 500), tohum=tohum + 1, **kw)
        m2 = monte_carlo(A, A_phi, A_yuz, sorunlar.etki_duzey.to_numpy(), zayif, a2, taban_sira=sira)
        o2 = m2.ozet(idler)
        ozet[f"ilk5_{ad}"] = o2["ilk5_olasilik"].to_numpy()
        parca[ad] = {"tau_ortanca": float(np.median(m2.tau)), "tau_p05": float(np.percentile(m2.tau, 5))}
    ozet = ozet.merge(sonuc[["sorun_id", "sira"]], on="sorun_id").sort_values("sira")

    Kf = lambda M: kok_skoru(dematel(M), 0.5)  # noqa: E731
    Pf = lambda k: oncelik(k, A_taban, E)  # noqa: E731
    be = baglanti_etkisi(A, idler, Kf, Pf)
    lb = liste_bagimliligi(A, A_taban, E, idler)
    ism_k = {str(k): katmanlar(d.T, esik(d.T, "ortalama+kss", k)).tolist() for k in (1.0, 1.5, 2.0)}
    gyol = girdi / "baglanti_gerekceleri.csv"
    kont = kontrol_et(A, idler, pd.read_csv(gyol) if gyol.exists() else None)
    if kont["hata"]:
        raise ValueError("Tutarlılık kontrolü başarısız: " + "; ".join(kont["hata"]))

    sonuc.to_csv(cikti / f"sonuclar_{etiket}.csv", index=False, float_format="%.4f")
    ozet.to_csv(cikti / f"duyarlilik_{etiket}.csv", index=False, float_format="%.4f")
    ac.to_csv(cikti / f"acik_skorlari_{etiket}.csv", index=False, float_format="%.4f")
    pd.DataFrame(d.T, index=idler, columns=idler).to_csv(cikti / f"toplam_etki_{etiket}.csv",
                                                         float_format="%.4f")
    be.to_csv(cikti / f"baglanti_etkisi_{etiket}.csv", index=False, float_format="%.4f")
    lb.to_csv(cikti / f"liste_bagimliligi_{etiket}.csv", index=False)

    etik = [f"{i} {k}" for i, k in zip(idler, kisa)]
    neden_sonuc_haritasi(d, etik, cikti / f"neden_sonuc_haritasi_{etiket}.png", esik=th,
                         baslik=f"Kök Neden · Neden-sonuç haritası ({etiket}, ön sonuç)",
                         alt_not=f"Oklar: toplam etkisi eşiğin (T ortalaması = {th:.3f}) üstündeki en güçlü 30 bağlantı. "
                                 "Kaynak: Kök Neden etki matrisi taslağı " + etiket)
    ilk_k_grafigi(ozet, [f"{i} {k}" for i, k in zip(ozet.sorun_id, [dict(zip(idler, kisa))[x] for x in ozet.sorun_id])],
                  cikti / f"ilk5_olasiligi_{etiket}.png",
                  baslik=f"İlk 5'te kalma olasılığı · {n:,} senaryo ({etiket})".replace(",", "."),
                  alt_not="Matris puanları, ağırlıklar, açık/etki skorları ve toplama türü aynı anda rastgele değiştirildi.")
    meta = {
        "etiket": etiket, "kod_surumu": __version__, "n_senaryo": n, "tohum": tohum, "normalizasyon_s": d.s, "esik_harita": th, "esik_ism": th_ism,
        "tau_ortanca": float(np.median(mc.tau)), "tau_p05": float(np.percentile(mc.tau, 5)),
        "parcalar": parca, "dolu_hucre": int((A > 0).sum()), "guclu_hucre": int((A >= 3).sum()),
        "zayif_isaretli": int(zayif.sum()),
        "plan_hedefli_sorun": int(ac.A_plan.notna().sum()),
        "ism_esik_duyarliligi": {k: dict(zip(idler, v)) for k, v in ism_k.items()},
        "liste_bagimliligi_ilk5_degisen": int(lb.ilk_kume_degisti.sum()) if len(lb) else 0,
        "kontrol_uyarilari": kont["uyari"],
    }
    (cikti / f"meta_{etiket}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    return meta


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--girdi", type=Path, required=True)
    ap.add_argument("--cikti", type=Path, required=True)
    ap.add_argument("--n", type=int, default=10_000)
    ap.add_argument("--etiket", default="v0.1")
    a = ap.parse_args()
    print(json.dumps(calistir(a.girdi, a.cikti, a.n, a.etiket), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
