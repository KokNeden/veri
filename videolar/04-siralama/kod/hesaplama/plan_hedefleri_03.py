"""Sıralamanın birincil ölçütü: plan açığı. Kaynak: 03-kronik-sorunlar araştırması ve kaynak testi.

Yalnız planın kendi sözüyle "hedef" olan sayılar alınır (03'teki ders: "tahmin" hedef sayılmaz). Nitelik tablo başlığından
okunur ("Hedefler", "Gelişmeler ve Hedefler"). 04 kaynak testinden sonra (27.09.2026) çıkarılanlar: S07 Tablo 30 (%100 hedefi
bizim varsayımımızdı), S05 X (tablo "Nüfus Gelişmeleri ve Tahminleri"). Ar-Ge satırlarında başlangıç ve gerçekleşme aynı seriden.
Başlangıç değeri planın kendi tablosundan (icerik/03-kronik-sorunlar/veri/plan_hedefleri_*.csv),
gerçekleşme bir sonraki planın tablosundan ya da ham veriden (TÜİK, TCMB, Dünya Bankası).
Gerçekleşme bir tahminse 'not' sütununda yazılır.
Nitelik (01.10.2026, yonetim/raporlar/hedef-tahmin-taramasi-2026-10-01.md Ek A): X. ve XI. Planların
"Hedefler" başlıklı tablolarının dipnotu son yıl sütununu "Plan tahminleri" diye tanımlar. Sayılar ve sıralama
değişmedi; 'nitelik' sütunu planın kendi sözünü yazar (hedef / tahmin / ongoru / beklenen).
Çıktı: veri/plan_hedefleri.csv  (kokneden_siralama.calistir biçimi)
"""
from pathlib import Path

import pandas as pd

VERI = Path(__file__).resolve().parents[1] / "veri"

# sorun, plan, gösterge, baş. yıl, baş., hedef yıl, hedef, gerç. yıl, gerç., kaynak, not
SATIRLAR = [
    ("S21", "V", "Fiyat artışları (%)", 1984, 48.4, 1989, 10, 1989, 63.3, "V. Plan md. 139; TÜİK T.17.15", "TÜFE yıllık ortalama"),
    ("S21", "VI", "GSMH deflatörü artışı (%)", 1989, 75.5, 1994, 13.5, 1994, 107.3, "VI. Plan md. 182; TÜİK T.17.15", ""),
    ("S21", "X", "TÜFE yıl sonu (%)", 2012, 6.16, 2018, 4.5, 2018, 20.30, "X. Plan md. 493 (PDF 81); TCMB", ""),
    # Başlangıç ve gerçekleşme aynı seriden (Dünya Bankası, güncel TÜİK serisi); planın kendi başlangıç değeri eski seriden.
    ("S15", "IX", "Ar-Ge / GSYH (%)", 2006, 0.55, 2013, 2.0, 2013, 0.81, "IX. Plan s. 71 (hedef); WDI", "Başlangıç WDI (planın tablosu 0,80)"),
    ("S15", "X", "Ar-Ge / GSYH (%)", 2011, 0.79, 2018, 1.8, 2018, 1.27, "X. Plan s. 98 Tablo 19; WDI", "Başlangıç WDI (planın tablosu 0,86); o dönem açıklanan TÜİK 2018 değeri %1,03"),
    ("S15", "XI", "Ar-Ge / GSYH (%)", 2017, 1.18, 2023, 1.8, 2023, 1.42, "XI. Plan s. 108 Tablo 23; WDI", "Başlangıç WDI (planın tablosu 0,96)"),
    ("S14", "X", "İmalat / GSYH (%)", 2012, 15.9, 2018, 16.5, 2018, 18.9, "X. Plan s. 101 Tablo 20; WDI", "Başlangıç WDI (planın tablosu 15,6); hedef eski GSYH serisinde, gerçekleşme revize seride"),
    ("S14", "XI", "İmalat / GSYH (%)", 2018, 18.9, 2023, 21.0, 2023, 19.5, "XI. Plan Tablo 12 'İmalat Sanayiinde Hedefler'; WDI", "Başlangıç WDI (planın tablosu 19,1)"),
    ("S13", "X", "DSİ sulamaya açılan net alan (milyon ha)", 2012, 2.81, 2018, 3.75, 2018, 3.34, "X. Plan s. 112; XI. Plan", ""),
    ("S18", "X", "Birincil enerjide yerli kaynak payı (%)", 2011, 28, 2018, 35, 2018, 24.2, "X. Plan s. 186; WDI (100 − net ithalat)", "Tanım farkı: X yurt dışı çıkarımları da sayar"),
    ("S22", "X", "Cari denge / GSYH (%)", 2012, -6.0, 2018, -5.2, 2018, -1.9, "X. Plan s. 79; WDI", "Hedef tuttu (daralma yılı)"),
    ("S22", "XI", "Cari denge / GSYH (%)", 2018, -3.5, 2023, -0.9, 2023, -3.6, "XI. Plan s. 48; WDI", ""),
    ("S17", "X", "Zorunlu deprem sigortalı yapı (milyon)", 2012, 4.8, 2018, 9.5, 2018, 8.9, "X. Plan s. 152; XI. Plan s. 178", ""),
    ("S17", "XI", "Zorunlu deprem sigortalı yapı (milyon)", 2018, 8.9, 2023, 12.1, 2023, 11.7, "XI. Plan s. 178; XII. Plan", "Gerçekleşme XII. Plan tahmini"),
    ("S19", "XI", "İçme suyu kayıp kaçak oranı (%)", 2018, 36, 2023, 25, 2023, 31, "XI. Plan s. 172; XII. Plan s. 227", "Gerçekleşme XII. Plan tahmini"),
    ("S20", "X", "En zengin / en yoksul bölge geliri (kat)", 2012, 4.3, 2018, 3.99, 2017, 4.28, "X. Plan s. 135; XI. Plan s. 164", "Hedef '<4'"),
    ("S20", "XI", "En zengin / en yoksul bölge geliri (kat)", 2017, 4.28, 2023, 3.85, 2023, 4.30, "XI. Plan s. 164; XII. Plan", "Gerçekleşme XII. Plan tahmini"),
    ("S01", "VIII", "Okul öncesi okullaşma (%)", 2000, 9.8, 2005, 25.0, 2006, 19.9, "VIII. Plan s. 92; IX. Plan", ""),
    ("S01", "IX", "Okul öncesi okullaşma (%)", 2006, 19.9, 2013, 50.0, 2012, 44.0, "IX. Plan s. 74; X. Plan", ""),
    ("S02", "VII", "Mesleki-teknik okullaşma (%)", 1995, 22.4, 2001, 34.5, 2000, 22.8, "VII. Plan s. 41; VIII. Plan s. 92",
     "VII'nin tablosu 'beklenen'; VIII bunları 'Plan hedefleri' diye anıyor (s. 91–92)"),
    ("S04", "X", "Kadın iş gücüne katılım (%)", 2012, 29.5, 2018, 34.9, 2018, 34.2, "X. Plan s. 58; XI. Plan s. 140", ""),
    ("S05", "XI", "Toplam doğurganlık hızı", 2018, 1.99, 2023, 2.15, 2023, 1.51, "XI. Plan Tablo 41 'Nüfus Hedefleri'; WDI", ""),
    ("S10", "X", "Kayıt dışı istihdam (%)", 2012, 39.0, 2018, 30.0, 2018, 33.4, "X. Plan s. 58; XI. Plan s. 140", ""),
]


# Planın kendi sözüyle nitelik (Ek A). V md. 139 bir söz: "yüzde 10 civarına inecek şekilde sürdürülecektir".
NITELIK = {
    ("S21", "V"): "hedef", ("S21", "VI"): "hedef", ("S21", "X"): "hedef",
    ("S15", "IX"): "hedef", ("S15", "X"): "tahmin", ("S15", "XI"): "tahmin",
    ("S14", "X"): "tahmin", ("S14", "XI"): "tahmin",
    ("S13", "X"): "hedef",  # X Tablo 24: başlık "Hedefler", bu satırda tahmin dipnotu yok
    ("S18", "X"): "hedef",  # Program Hedefleri
    ("S22", "X"): "hedef", ("S22", "XI"): "ongoru",  # X md. 476 "hedeflenmektedir"; XI md. 178 "öngörülmektedir"
    ("S17", "X"): "tahmin", ("S17", "XI"): "tahmin",
    ("S19", "XI"): "tahmin", ("S20", "X"): "tahmin", ("S20", "XI"): "tahmin",
    ("S01", "VIII"): "hedef", ("S01", "IX"): "hedef",
    ("S02", "VII"): "beklenen",  # VII Tablo 3 "Eğitimde Beklenen Sayısal Gelişmeler"
    ("S04", "X"): "hedef",  # Program Hedefleri
    ("S05", "XI"): "tahmin", ("S10", "X"): "tahmin",
}


def main() -> None:
    df = pd.DataFrame(SATIRLAR, columns=["sorun_id", "plan", "gosterge", "baslangic_yil", "baslangic", "hedef_yil",
                                         "hedef", "gerceklesen_yil", "gerceklesen", "kaynak", "not"])
    df["nitelik"] = [NITELIK[(s, p)] for s, p in zip(df.sorun_id, df.plan)]
    df.to_csv(VERI / "plan_hedefleri.csv", index=False)
    print(f"plan_hedefleri.csv: {len(df)} satır, {df.sorun_id.nunique()} sorun")


if __name__ == "__main__":
    main()
