"""İki oyuncak örnek. Çalıştır:  python ornekler/oyuncak.py

1) 4 düğüm (video için): rutubetli ev. Bütün sayılar videoda gösterilebilir.
2) 6 düğüm (kod gösterimi): yolu olmayan kasaba; döngü içerir (göç ↔ okul).
Bu örnekler kurgusaldır; Türkiye hakkında bir iddia taşımaz.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kokneden_siralama import dematel, esik, katmanlar, kok_skoru, oncelik, sirala  # noqa: E402
from kokneden_siralama.duyarlilik import DuyarlilikAyari, monte_carlo  # noqa: E402
from kokneden_siralama.harita import neden_sonuc_haritasi  # noqa: E402

CIKTI = Path(__file__).resolve().parent / "cikti"

EV_ID = ["A", "B", "C", "D"]
EV_AD = ["Tesisat kaçağı", "Duvarda nem", "Küf", "Boya dökülmesi"]
EV = np.array([
    #  A  B  C  D
    [0, 4, 1, 1],   # A Tesisat kaçağı
    [0, 0, 3, 3],   # B Duvarda nem
    [0, 1, 0, 2],   # C Küf
    [0, 0, 0, 0],   # D Boya dökülmesi
])

KASABA_ID = ["Y", "P", "G", "M", "O", "N"]
KASABA_AD = ["Yol yok", "Pazara erişim", "Düşük gelir", "Göç", "Okul kapanıyor", "Yaşlanma"]
KASABA = np.array([
    #  Y  P  G  M  O  N
    [0, 4, 1, 0, 1, 0],   # Y
    [0, 0, 3, 1, 0, 0],   # P
    [0, 0, 0, 3, 1, 0],   # G
    [0, 0, 1, 0, 3, 3],   # M
    [0, 0, 0, 2, 0, 0],   # O
    [0, 0, 1, 0, 0, 0],   # N
])
# Kasaba için kurgusal açık (0-1) ve etki düzeyi (1-3)
KASABA_ACIK = np.array([0.9, 0.7, 0.8, 0.6, 0.5, 0.4])
KASABA_ETKI = np.array([3, 2, 3, 2, 2, 2])


def tablo(ad, idler, adlar, A):
    d = dematel(A)
    th = esik(d.T)
    df = pd.DataFrame({"id": idler, "ad": adlar, "D": d.D, "R": d.R, "D+R": d.onem, "D-R": d.net,
                       "grup": np.where(d.net > 0, "neden", "sonuç"), "K": kok_skoru(d),
                       "ISM katman": katmanlar(d.T, th)})  # küçük örnekte ortalama eşiği yeterli
    print(f"\n=== {ad} ===  s = {d.s:g}   eşik (T ortalaması) = {th:.3f}")
    print("X = A / s:\n", pd.DataFrame(d.X, index=idler, columns=idler).round(3))
    print("T = X (I - X)^-1:\n", pd.DataFrame(d.T, index=idler, columns=idler).round(3))
    print(df.round(3).to_string(index=False))
    return d, df, th


def main():
    CIKTI.mkdir(exist_ok=True)
    d, df, th = tablo("Rutubetli ev (4 düğüm)", EV_ID, EV_AD, EV)
    df.round(4).to_csv(CIKTI / "ev_4_sonuc.csv", index=False)
    pd.DataFrame(d.T, index=EV_ID, columns=EV_ID).round(4).to_csv(CIKTI / "ev_4_T.csv")
    neden_sonuc_haritasi(d, [f"{i} {a}" for i, a in zip(EV_ID, EV_AD)], CIKTI / "ev_4_harita.png",
                         esik=th, baslik="Oyuncak örnek: rutubetli ev")

    d, df, th = tablo("Yolu olmayan kasaba (6 düğüm)", KASABA_ID, KASABA_AD, KASABA)
    E = KASABA_ETKI / 3
    P = oncelik(df.K, KASABA_ACIK, E)
    df["A"], df["E"], df["P"], df["sira"] = KASABA_ACIK, E, P, sirala(P)
    mc = monte_carlo(KASABA, KASABA_ACIK, KASABA_ACIK, KASABA_ETKI,
                     ayar=DuyarlilikAyari(n=2000, ilk_k=2), taban_sira=sirala(P))
    oz = mc.ozet(KASABA_ID)
    print("\nÖncelik:\n", df[["id", "ad", "K", "A", "E", "P", "sira"]].round(3).to_string(index=False))
    print("\nDuyarlılık (2000 senaryo, ilk-2):\n", oz.round(3).to_string(index=False))
    print(f"Kendall tau ortanca = {np.median(mc.tau):.3f}")
    df.round(4).to_csv(CIKTI / "kasaba_6_sonuc.csv", index=False)
    oz.round(4).to_csv(CIKTI / "kasaba_6_duyarlilik.csv", index=False)
    neden_sonuc_haritasi(d, [f"{i} {a}" for i, a in zip(KASABA_ID, KASABA_AD)],
                         CIKTI / "kasaba_6_harita.png", esik=th, baslik="Oyuncak örnek: yolu olmayan kasaba")


if __name__ == "__main__":
    main()
