import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kokneden_siralama import acik_skoru, dematel, esik, katmanlar, kok_skoru, minmax, oncelik, sirala  # noqa: E402
from kokneden_siralama.duyarlilik import DuyarlilikAyari, baglanti_etkisi, monte_carlo  # noqa: E402


def test_iki_dugum_analitik():
    # A = [[0, a], [0, 0]] → X = [[0,1],[0,0]] ; X^2 = 0 → T = X
    A = np.array([[0, 2], [0, 0]])
    d = dematel(A)
    assert d.s == 2
    np.testing.assert_allclose(d.T, [[0, 1], [0, 0]])
    np.testing.assert_allclose(d.net, [1, -1])


def test_seri_toplami_ile_ayni():
    rng = np.random.default_rng(1)
    A = rng.integers(0, 5, (6, 6)).astype(float)
    np.fill_diagonal(A, 0)
    d = dematel(A)
    S, P = np.zeros_like(d.X), np.eye(6)
    for _ in range(400):
        P = P @ d.X
        S += P
    np.testing.assert_allclose(d.T, S, atol=1e-8)


def test_D_toplami_R_toplamina_esit():
    rng = np.random.default_rng(2)
    A = rng.integers(0, 5, (8, 8)).astype(float)
    np.fill_diagonal(A, 0)
    d = dematel(A)
    assert abs(d.D.sum() - d.R.sum()) < 1e-9
    assert abs(d.net.sum()) < 1e-9


def test_gecersiz_girdiler():
    with pytest.raises(ValueError):
        dematel(np.array([[0, 5], [0, 0]]))
    with pytest.raises(ValueError):
        dematel(np.array([[1, 0], [0, 0]]))
    with pytest.raises(ValueError):
        dematel(np.zeros((3, 3)))


def test_tam_dolu_matris_yakinsar():
    # Her satır ve sütun toplamı eşit: klasik normalizasyonda spektral yarıçap = 1 (Lee vd. 2013)
    A = np.full((4, 4), 4.0)
    np.fill_diagonal(A, 0)
    d = dematel(A)
    assert np.isfinite(d.T).all()


def test_zincirde_kok_ustte():
    # 1 → 2 → 3 → 4 zinciri: kök skoru azalan, ISM katmanı: 4 en üst (1), 1 en derin
    A = np.zeros((4, 4))
    A[0, 1] = A[1, 2] = A[2, 3] = 3
    d = dematel(A)
    assert np.argmax(d.net) == 0 and np.argmin(d.net) == 3
    kat = katmanlar(d.T, 0.0)
    assert list(kat) == [4, 3, 2, 1]


def test_kok_skoru_araligi():
    A = np.array([[0, 3, 1], [0, 0, 2], [1, 0, 0]])
    K = kok_skoru(dematel(A))
    assert K.min() >= 0 and K.max() <= 1
    np.testing.assert_allclose(minmax([2, 2, 2]), [0.5, 0.5, 0.5])


def _seri(tr, digerleri):
    ulkeler = ["KOR", "ESP", "PRT", "GRC", "POL", "MEX", "MYS", "OECD_MED"]
    satir = [{"ulke": "TUR", "yil": 2024, "deger": tr}]
    satir += [{"ulke": u, "yil": 2024, "deger": v} for u, v in zip(ulkeler, digerleri)]
    return pd.DataFrame(satir)


def test_acik_yonu():
    s = _seri(10, [20, 21, 19, 22, 18, 20, 20, 20])
    iyi_yuksek = acik_skoru(s, +1)   # yüksek iyi, TR düşük → açık büyük
    kotu_yuksek = acik_skoru(s, -1)  # yüksek kötü, TR düşük → açık küçük
    assert iyi_yuksek.z > 0 and iyi_yuksek.A_phi > 0.9
    assert kotu_yuksek.z < 0 and kotu_yuksek.A_phi < 0.1
    assert iyi_yuksek.A_yuzdelik == 1.0


def test_acik_eksik_ve_normatif():
    s = _seri(10, [20, 21, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]).dropna()
    assert acik_skoru(s, 1).A_phi is None
    assert acik_skoru(_seri(1, [2] * 8), 0).A_phi is None


def test_oncelik_ve_sira():
    P = oncelik([1, 0.5, 0.1], [1, 0.5, 0.1], [1, 1, 1])
    assert list(sirala(P)) == [1, 2, 3]
    # geometrik: bir bileşeni tabanda olan sorun yüksek tek bileşenle kurtulamaz
    g = oncelik([1.0, 0.6], [0.0, 0.6], [1.0, 0.6])
    a = oncelik([1.0, 0.6], [0.0, 0.6], [1.0, 0.6], tur="aritmetik")
    assert g[0] < g[1] and a[0] > a[1]


def test_monte_carlo_tekrarlanabilir():
    A = np.array([[0, 4, 1, 0], [0, 0, 3, 1], [0, 1, 0, 2], [0, 0, 0, 0]])
    Aa = np.array([0.8, 0.6, np.nan, 0.3])
    ay = DuyarlilikAyari(n=200, tohum=7, ilk_k=2)
    m1 = monte_carlo(A, Aa, Aa, [3, 2, 2, 1], ayar=ay)
    m2 = monte_carlo(A, Aa, Aa, [3, 2, 2, 1], ayar=ay)
    np.testing.assert_array_equal(m1.siralar, m2.siralar)
    oz = m1.ozet(list("ABCD"))
    assert oz["ilk2_olasilik"].between(0, 1).all()


def test_belirsizlik_kapaliysa_tau_bir():
    A = np.array([[0, 4, 1], [0, 0, 3], [1, 0, 0]])
    Aa = np.array([0.8, 0.6, 0.4])
    ay = DuyarlilikAyari(n=20, matris=False, agirlik=False, acik=False, etki=False, toplama=False)
    m = monte_carlo(A, Aa, Aa, [3, 2, 1], ayar=ay)
    assert np.allclose(m.tau, 1.0)


def test_baglanti_etkisi():
    A = np.array([[0, 4, 0], [0, 0, 3], [0, 0, 0]], dtype=float)
    be = baglanti_etkisi(A, ["a", "b", "c"], lambda M: kok_skoru(dematel(M)),
                         lambda k: oncelik(k, [0.5] * 3, [1] * 3), ilk_k=1)
    assert len(be) == 2 and set(be.puan) == {3, 4}


def test_birlestir_ortanca_ve_tartismali():
    from kokneden_siralama.birlestir import birlestir, uzman_uyumu
    n = np.nan
    m1 = np.array([[0, 4, 0], [1, 0, 2], [0, 0, 0]], float)
    m2 = np.array([[0, 4, 1], [0, 0, 2], [n, 0, 0]], float)
    m3 = np.array([[0, 0, 1], [1, 0, 3], [n, 0, 0]], float)
    med, iqr, npuan, tart = birlestir([m1, m2, m3])
    assert med[0, 1] == 4 and med[1, 2] == 2
    assert tart[0, 1]          # 4, 4, 0 → IQR = 2
    assert tart[2, 0]          # yalnız 1 uzman puan vermiş
    assert npuan[2, 0] == 1
    U = uzman_uyumu([m1, m2, m3])
    assert U.shape == (3, 3) and U[0, 0] == 1


def test_plan_acigi():
    from kokneden_siralama.skorlar import birlesik_acik, plan_acigi
    assert plan_acigi(10, 20, 20) == 0.0          # hedef tuttu
    assert plan_acigi(10, 20, 15) == 0.5          # yarı yol
    assert plan_acigi(10, 20, 8) == 1.0           # geriledi
    assert plan_acigi(10, 5, 5) == 0.0            # azaltma hedefi
    assert plan_acigi(3, 3, 4) is None
    assert abs(birlesik_acik(0.5, 1.0) - 0.65) < 1e-12
    assert birlesik_acik(None, 0.4) == 0.4 and birlesik_acik(0.2, None) == 0.2


def test_plan_acigi_takvim():
    from kokneden_siralama.skorlar import plan_acigi
    # 5 yıllık hedefin 1. yılında %20 ilerleme = takvimde → açık 0
    assert plan_acigi(10, 20, 12, 2023, 2028, 2024) == 0.0
    # 1. yılda %10 ilerleme → beklenenin yarısı → açık 0,5
    assert abs(plan_acigi(10, 20, 11, 2023, 2028, 2024) - 0.5) < 1e-9
    # süresi dolmuş: yıl etkisi yok
    assert plan_acigi(10, 20, 15, 2019, 2023, 2025) == 0.5


def test_mad_sifir_birimden_bagimsiz():
    a = acik_skoru(_seri(19.9, [20] * 8), +1)
    b = acik_skoru(_seri(0.199, [0.2] * 8), +1)
    assert a.z == b.z == 4.0


def test_kapali_blok_T_olcegi_makul():
    A = np.full((4, 4), 4.0)
    np.fill_diagonal(A, 0)
    with pytest.warns(RuntimeWarning):
        d = dematel(A)
    assert d.T.max() < 1e3


def test_kontrol_ve_liste_bagimliligi():
    from kokneden_siralama.duyarlilik import liste_bagimliligi
    from kokneden_siralama.kontrol import kontrol_et
    A = np.array([[0, 4, 0], [4, 0, 3], [0, 0, 0]], float)
    k = kontrol_et(A, ["a", "b", "c"], pd.DataFrame({"kaynak": ["a"], "hedef": ["b"], "puan": [4], "kaynakca": ["X"]}))
    assert any("iki yönde" in u for u in k["uyari"]) and any("b>a" in h for h in k["hata"])
    lb = liste_bagimliligi(A, [0.5] * 3, [1] * 3, ["a", "b", "c"], ilk_k=1)
    assert len(lb) >= 2  # tamamen sıfırlanan alt matrisler atlanır
