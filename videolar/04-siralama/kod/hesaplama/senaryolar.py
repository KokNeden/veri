"""V4 ek duyarlılık senaryoları ve sezon takvimi görseli.

Çalıştır (05-siralama-sonucu/ içinden):  PYTHONPATH=../04-siralama-yontemi/kod python kod/senaryolar.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from kokneden_siralama import dematel, esik, katmanlar, kok_skoru, oncelik, sirala  # noqa: E402
from kokneden_siralama.calistir import aciklar, matris_oku  # noqa: E402
from kokneden_siralama.skorlar import etki_skoru  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
V, C = KOK / "veri", KOK / "cikti"


def hazirla(sorunlar, A):
    gost = pd.read_csv(V / "gostergeler.csv")
    liste = pd.read_csv(V / "gosterge_listesi.csv")
    ac = aciklar(sorunlar, gost, liste)
    Aphi = ac.A_phi.to_numpy(dtype=float)
    E = np.array([etki_skoru(int(x)) for x in sorunlar.etki_duzey])
    return Aphi, E


def ilk5(ids, P):
    s = sirala(P)
    return [ids[i] for i in np.argsort(s)[:5]]


def main():
    sorunlar = pd.read_csv(V / "sorunlar.csv")
    ids = sorunlar.sorun_id.tolist()
    A = matris_oku(V / "etki_matrisi.csv", ids)
    Aphi, E = hazirla(sorunlar, A)
    Ab = np.where(np.isnan(Aphi), 0.5, Aphi)
    d = dematel(A)
    K = kok_skoru(d)
    satir = []

    def ekle(ad, P, aciklama, idler=ids):
        satir.append({"senaryo": ad, "ilk5": " > ".join(ilk5(idler, P)), "aciklama": aciklama})

    ekle("taban", oncelik(K, Ab, E), "wK=0.5, wA=0.25, wE=0.25, geometrik, λ=0.5, eksik A=0.5")
    ekle("esit_agirlik", oncelik(K, Ab, E, (1, 1, 1)), "Üç bileşen eşit ağırlıklı")
    ekle("yalniz_kok", oncelik(K, Ab, E, (1, 0, 0)), "Yalnız kök skoru (açık ve etki yok)")
    ekle("aritmetik", oncelik(K, Ab, E, tur="aritmetik"), "Ağırlıklı toplam")
    ekle("lam_0.3", oncelik(kok_skoru(d, 0.3), Ab, E), "Kök skorunda D ağırlıklı")
    ekle("lam_0.7", oncelik(kok_skoru(d, 0.7), Ab, E), "Kök skorunda D−R ağırlıklı")
    ekle("eksik_A_1", oncelik(K, np.where(np.isnan(Aphi), 1.0, Aphi), E), "Verisi olmayan sorunlarda açık = en kötü")
    ekle("eksik_A_0", oncelik(K, np.where(np.isnan(Aphi), 0.05, Aphi), E), "Verisi olmayan sorunlarda açık = yok")
    # S22'yi cari dengeyle ölç
    s2 = sorunlar.copy()
    s2.loc[s2.sorun_id == "S22", ["ana_gosterge", "yedek_gosterge"]] = ["G045", ""]
    Aphi2, _ = hazirla(s2, A)
    ekle("S22_cari_denge", oncelik(K, np.where(np.isnan(Aphi2), 0.5, Aphi2), E),
         f"S22 açığı cari dengeyle ölçülürse (A = {Aphi2[ids.index('S22')]:.2f})")
    # S12 (aday) çıkarılırsa
    keep = [i for i, x in enumerate(ids) if x != "S12"]
    A3 = A[np.ix_(keep, keep)]
    d3 = dematel(A3)
    ekle("S12_cikarilirsa", oncelik(kok_skoru(d3), Ab[keep], E[keep]), "Aday madde listeden çıkarılırsa",
         [ids[i] for i in keep])
    # Tartışmalı bağlantılar sıfırlanırsa / S09→S07 = 2
    g = pd.read_csv(V / "baglanti_gerekceleri.csv")
    A4 = A.copy()
    for r in g[g.durum.isin(["tartismali", "zayif"])].itertuples():
        A4[ids.index(r.kaynak), ids.index(r.hedef)] = 0
    n_tz = int(g.durum.isin(["tartismali", "zayif"]).sum())
    ekle("tartismalilar_sifir", oncelik(kok_skoru(dematel(A4)), Ab, E), f"Tartışmalı ve zayıf {n_tz} bağlantı 0")
    A5 = A.copy()
    A5[ids.index("S09"), ids.index("S07")] = 2
    ekle("S09_S07_2", oncelik(kok_skoru(dematel(A5)), Ab, E), "S09→S07 bağlantısı 4 yerine 2")
    # Yalnız 3-4 puanlı (kaynaklı) bağlantılar
    A6 = np.where(A >= 3, A, 0)
    ekle("yalniz_kaynakli", oncelik(kok_skoru(dematel(A6)), Ab, E), "Yalnız kaynaklı 3-4 puanlı bağlantılar (1-2'ler 0)")
    # Tüm 1-2 puanlar 1 azaltılırsa (taslak yargısı abartılı ise)
    A7 = np.where((A > 0) & (A < 3), A - 1, A)
    ekle("yargilar_eksi1", oncelik(kok_skoru(dematel(A7)), Ab, E), "Kaynaksız 1-2 puanlık yargılar 1 düşürülürse")
    # Karşı tez: "önce eğitim" (Glaeser vd. 2004) — eğitimden kurumlara bağlar eklenirse
    A8 = A.copy()
    for j, p in [("S06", 3), ("S09", 3), ("S11", 2), ("S12", 2)]:
        A8[ids.index("S01"), ids.index(j)] = p
    ekle("egitim_once", oncelik(kok_skoru(dematel(A8)), Ab, E),
         "Glaeser vd. (2004) karşı tezi: S01→S06=3, S01→S09=3, S01→S11=2, S01→S12=2 eklenirse")
    # S08'e hiç gelen bağlantı yok: eksik olabilir
    A9 = A.copy()
    for i in ["S11", "S09", "S07"]:
        A9[ids.index(i), ids.index("S08")] = 2
    ekle("S08_girdi", oncelik(kok_skoru(dematel(A9)), Ab, E), "S08'e S11, S09, S07'den 2 puanlık bağ eklenirse")
    # Denetim (21.09) önerileri birlikte: puan düşürmeleri + eksik bağlar
    A10 = A.copy()
    for (i, j), p in {("S16", "S17"): 3, ("S21", "S22"): 2, ("S18", "S21"): 2, ("S13", "S19"): 2, ("S12", "S09"): 2,
                      ("S09", "S06"): 2, ("S01", "S05"): 2, ("S21", "S14"): 1, ("S19", "S17"): 1, ("S11", "S09"): 1}.items():
        A10[ids.index(i), ids.index(j)] = p
    ekle("denetim_onerileri", oncelik(kok_skoru(dematel(A10)), Ab, E),
         "Denetim önerileri birlikte: 5 puan düşürme + 5 eksik bağ (01-berke-sorular.md B9-B10)")
    # v0.2 riski: S23 sonuç göstergesine taşınır ve S12 sıralamadan çıkarsa
    keep2 = [i for i, x in enumerate(ids) if x not in ("S12", "S23")]
    ekle("S12_S23_cikarilirsa", oncelik(kok_skoru(dematel(A[np.ix_(keep2, keep2)])), Ab[keep2], E[keep2]),
         "S23 sonuç göstergesine taşınır ve S12 çıkarsa", [ids[i] for i in keep2])
    pd.DataFrame(satir).to_csv(C / "senaryolar_v0.1.csv", index=False)
    print(pd.DataFrame(satir).to_string(index=False))

    # ISM eşik duyarlılığı
    rows = []
    for k in [0.5, 1.0, 1.5, 2.0, 2.5]:
        th = esik(d.T, "ortalama+kss", k)
        kat = katmanlar(d.T, th)
        derin = [ids[i] for i in np.where(kat == kat.max())[0]]
        rows.append({"k": k, "esik": round(th, 4), "bag_sayisi": int((d.T > th).sum()),
                     "katman_sayisi": int(kat.max()), "en_derin_katman": ";".join(derin)})
    pd.DataFrame(rows).to_csv(C / "ism_esik_duyarliligi_v0.1.csv", index=False)
    print(pd.DataFrame(rows).to_string(index=False))

    sezon_takvimi(C / "sezon_takvimi_v0.1.png")


def sezon_takvimi(dosya):
    sezonlar = [
        ("Sezon 1", "Kamuda liyakat ve\nkurumsal kapasite (S09)", "#B5452B", "Sıra 1 · ilk-5: %100"),
        ("Sezon 2", "Hukukun üstünlüğü ve\nyargı (S06)", "#C9713D", "Sıra 2 · ilk-5: %100"),
        ("Sezon 3", "Plan-uygulama kopukluğu\n(S07)", "#D89A55", "Sıra 3 · ilk-5: %99"),
        ("Sezon 4", "Eğitimin niteliği\n(S01)", "#8A8F5A", "Sıra 5 · ilk-5: %48"),
    ]
    fig, ax = plt.subplots(figsize=(12, 4.2), dpi=150)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for i, (s, konu, renk, not_) in enumerate(sezonlar):
        x = i + 0.05
        ax.add_patch(plt.Rectangle((x, 0.28), 0.9, 0.55, color=renk, alpha=0.92))
        ax.text(x + 0.45, 0.76, s, ha="center", va="center", color="white", fontsize=12, fontweight="bold")
        ax.text(x + 0.45, 0.55, konu, ha="center", va="center", color="white", fontsize=10.5)
        ax.text(x + 0.45, 0.36, "3 analiz + 1 ulusal çözüm\n+ bölgesel çözümler", ha="center", va="center",
                color="white", fontsize=8)
        ax.text(x + 0.45, 0.2, not_, ha="center", va="center", fontsize=8.5, color="#333")
    ax.text(0.05, 0.95, "Kök Neden · Taslak sezon takvimi (sıralama v0.1'den türetildi)", fontsize=13,
            fontweight="bold", va="top")
    ax.text(0.05, 0.06, "Sezon 4 için aday: S01 (ilk-5 olasılığı %48). S12 Medya ekosistemi (sıra 4) aday madde ve vekil "
            "gösterge ile ölçüldüğü için sezona alınmadı; v0.2'de yeniden değerlendirilecek.", fontsize=8, color="#555")
    fig.savefig(dosya, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
