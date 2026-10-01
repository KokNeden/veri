"""Plan hedeflerine gerçekleşme değeri ekler (yalnız aynı ya da yakın ölçü bulunanlar).

Kullanım (03-kronik-sorunlar/ içinden):
    python3 kod/plan_gerceklesme.py

Girdi:  site/veri/plan-hedefleri.csv, veri/gostergeler_zaman_serisi.csv (Dünya Bankası WDI, Türkiye),
        site/veri/enflasyon-hedef-gerceklesme.csv
        veri/gerceklesme_arastirma_*.csv (plan metinleri, DSİ, SBB, TÜİK'ten elle derlenen satırlar)
Çıktı:  site/veri/plan-hedef-gerceklesme.csv

Kural: Gerçekleşme ancak hedefle aynı şeyi ölçen bir seriden yazılır.
  ayni_olcu  = tanım ve kapsam hedefle aynı
  yakin_olcu = aynı kavram, küçük tanım ya da kaynak farkı var (not sütununda yazılı)
Ölçüsü uymayan hedefler (ör. Türkiye'deki "ortaöğretim" ile Dünya Bankası "secondary") dosyaya alınmaz.
"""
import csv
import math

HEDEF = "site/veri/plan-hedefleri.csv"
WDI = "veri/gostergeler_zaman_serisi.csv"
ENF = "site/veri/enflasyon-hedef-gerceklesme.csv"
CIKTI = "site/veri/plan-hedef-gerceklesme.csv"

wdi = {}
for r in csv.DictReader(open(WDI, encoding="utf-8-sig")):
    if r["ulke"] == "TUR":
        wdi.setdefault(r["kod"], {})[int(r["yil"])] = float(r["deger"])

KAYNAK = {
    "SP.DYN.TFRT.IN": "Dünya Bankası WDI, SP.DYN.TFRT.IN",
    "SL.TLF.CACT.FE.ZS": "Dünya Bankası WDI, SL.TLF.CACT.FE.ZS (ILO modellenmiş tahmin)",
    "SL.UEM.1524.ZS": "Dünya Bankası WDI, SL.UEM.1524.ZS (ILO modellenmiş tahmin)",
    "GB.XPD.RSDV.GD.ZS": "Dünya Bankası WDI, GB.XPD.RSDV.GD.ZS (UNESCO/TÜİK)",
    "IP.PAT.RESD": "Dünya Bankası WDI, IP.PAT.RESD (WIPO)",
    "NV.IND.MANF.ZS": "Dünya Bankası WDI, NV.IND.MANF.ZS (TÜİK ulusal hesaplar)",
    "BN.CAB.XOKA.GD.ZS": "Dünya Bankası WDI, BN.CAB.XOKA.GD.ZS",
    "FP.CPI.TOTL.ZG": "Dünya Bankası WDI, FP.CPI.TOTL.ZG (TÜİK TÜFE)",
}

AR_GE_NOT = ("Dünya Bankası serisi, hedef yazıldıktan sonra revize edilen TÜİK değerlerini veriyor "
             "(ör. XI. Plan'ın 2017 başlangıcı 0,96, revize seride 1,18); sonuç değişmiyor.")

# (plan, sorun, göstergenin başı, seri, yıllar, eşleşme, not)
# Birden çok yıl verilirse gerçekleşme o yılların ortalamasıdır.
# Notu "AÇIK " ile başlayan satırlarda gerçekleşmenin işareti çevrilir (plan açığı artı sayıyla yazmış).
ESLEME = [
    (4, "S05", "Toplam doğurganlık oranı (uzun dönem)", "SP.DYN.TFRT.IN", range(1995, 2001), "yakin_olcu", "1995–2000 ortalaması."),
    (7, "S05", "Toplam doğurganlık hızı", "SP.DYN.TFRT.IN", [2000], "ayni_olcu", ""),
    (8, "S05", "Toplam doğurganlık hızı (tahmin)", "SP.DYN.TFRT.IN", [2005], "ayni_olcu", "Planda tahmin olarak yazılmış."),
    (9, "S05", "Total fertility rate", "SP.DYN.TFRT.IN", [2013], "ayni_olcu", ""),
    (10, "S05", "Toplam doğurganlık hızı", "SP.DYN.TFRT.IN", [2018], "ayni_olcu", ""),
    (11, "S05", "Toplam doğurganlık hızı", "SP.DYN.TFRT.IN", [2023], "ayni_olcu", ""),
    (9, "S04", "Female labor force participation rate", "SL.TLF.CACT.FE.ZS", [2013], "yakin_olcu", "ILO modellenmiş tahmin; TÜİK hane halkı işgücü değeri biraz farklı olabilir."),
    (10, "S04", "Kadın işgücüne katılma oranı", "SL.TLF.CACT.FE.ZS", [2018], "yakin_olcu", "ILO modellenmiş tahmin; TÜİK değeri biraz farklı olabilir."),
    (11, "S04", "İşgücüne katılma oranı, kadın", "SL.TLF.CACT.FE.ZS", [2023], "yakin_olcu", "ILO modellenmiş tahmin; TÜİK değeri biraz farklı olabilir."),
    (10, "S02", "Gençlerde işsizlik oranı", "SL.UEM.1524.ZS", [2018], "yakin_olcu", "15–24 yaş, ILO modellenmiş tahmin."),
    (11, "S02", "İşsizlik oranı, genç nüfus", "SL.UEM.1524.ZS", [2023], "yakin_olcu", "15–24 yaş, ILO modellenmiş tahmin."),
    (8, "S15", "Ar-Ge harcaması / GSYİH", "GB.XPD.RSDV.GD.ZS", [2005], "yakin_olcu", AR_GE_NOT),
    (9, "S15", "Ar-Ge harcaması / GSYH", "GB.XPD.RSDV.GD.ZS", [2013], "yakin_olcu", AR_GE_NOT),
    (10, "S15", "Ar-Ge harcaması / GSYH", "GB.XPD.RSDV.GD.ZS", [2018], "yakin_olcu", AR_GE_NOT),
    (11, "S15", "Ar-Ge harcaması / GSYH", "GB.XPD.RSDV.GD.ZS", [2023], "yakin_olcu", AR_GE_NOT),
    (10, "S15", "Yerli patent başvuru sayısı", "IP.PAT.RESD", [2018], "ayni_olcu", ""),
    (10, "S14", "İmalat sanayii / GSYH (cari)", "NV.IND.MANF.ZS", [2018], "ayni_olcu", ""),
    (11, "S14", "İmalat sanayii / GSYH (cari)", "NV.IND.MANF.ZS", [2023], "ayni_olcu", ""),
    (8, "S22", "Cari işlemler açığı / GSMH", "BN.CAB.XOKA.GD.ZS", [2005], "yakin_olcu", "AÇIK Plan açığı GSMH'ya oranlar, seri GSYH'ya. Gerçekleşme açık olarak yazıldı (artı = açık)."),
    (9, "S22", "Cari işlemler dengesi / GSYH", "BN.CAB.XOKA.GD.ZS", [2013], "ayni_olcu", ""),
    (9, "S22", "Cari işlemler açığı / GSYH", "BN.CAB.XOKA.GD.ZS", [2013], "ayni_olcu", "AÇIK Plan açığı artı sayıyla yazmış; gerçekleşme de açık olarak yazıldı (artı = açık)."),
    (10, "S22", "Cari işlemler dengesi / GSYH", "BN.CAB.XOKA.GD.ZS", [2018], "ayni_olcu", ""),
    (11, "S22", "Cari işlemler dengesi / GSYH", "BN.CAB.XOKA.GD.ZS", [2023], "ayni_olcu", ""),
    (10, "S21", "TÜFE yıllık artış hızı", "FP.CPI.TOTL.ZG", [2018], "ayni_olcu", "Yıllık ortalama TÜFE artışı."),
]

# Enflasyon: 03'te elle derlenen hedef–gerçekleşme tablosu (TÜİK, TCMB). Plan satırı → enflasyon satırı.
ENF_ESLEME = [
    (5, "Fiyat artışları (enflasyon)", "1989"),
    (6, "GSMH zımni deflatörü artış hızı", "1994"),
    (7, "GSMH deflatörü artışı (aralık alt ucu)", "2000"),
    (7, "GSMH deflatörü artışı (aralık üst ucu)", "2000"),
    (8, "TEFE yıllık artışı (2001 yılı sonu)", "2001"),
    (8, "TEFE yıllık artışı (2002 yılı sonu)", "2002"),
    (9, "TÜFE artışı (yıl sonu)", "2013"),
    (10, "TÜFE yıllık artışı (yıl sonu)", "2018"),
    (11, "TÜFE (yıl sonu)", "2023"),
]

# Elle derlenen araştırma satırlarından gözden geçirmede çıkarılanlar ve eşleşmesi düşürülenler.
# Anahtar: (plan, sorun, göstergenin başı). Gerekçe yanında.
ARASTIRMA_DISI = {
    (1, "S13", "Yeni sulanacak alan"): "değer üst sınır tahmini ('200 bin hektarı aşmadığı'), gerçekleşme değil",
    (1, "S19", "sulamaya yeni açılacak alan"): "değer üst sınır tahmini",
    (2, "S13", "Plan döneminde sulanacak alan"): "kaynaklar çelişiyor (DİE farkı 501, III. Plan tabanıyla 399 bin ha)",
    (2, "S19", "sulanacak ek alan"): "kaynaklar çelişiyor (501 / 399 bin ha)",
    (3, "S13", "Ek sulanan alan"): "başlangıç değeri iki kaynakta farklı (1 939 / 2 041); toplam alan satırı (III. Plan, S19) yeterli",
    (1, "S13", "Sulanan alan / tarım alanı"): "payda planlar arasında farklı; seçilen paydaya göre sonuç tersine dönüyor (%6,6 / %6,0)",
    (1, "S19", "sulanan alanın tarım alanına oranı"): "payda farkı (%6,6 / %6,0)",
    (2, "S13", "Sulanan alan / işlenen tarım arazisi"): "payda farkı; sonuç tersine dönüyor (%7,1 / %8,3)",
    (2, "S19", "sulanan alanın işlenen tarım arazisine oranı"): "payda farkı (%7,1 / %8,3)",
    (4, "S13", "Sulanan alan"): "hedef yılı 1983, bulunan değer 1984",
    (9, "S13", "DSİ sulama alanı"): "kaynak tablosunun 2012 sonunu mu 2013 sonunu mu gösterdiği belirsiz",
    (9, "S19", "DSİ sulama alanı"): "yıl belirsiz",
    (9, "S13", "Arazi toplulaştırma"): "2013 değeri tahmin ve seri tanımı (faaliyet / tescil) hedefle aynı olmayabilir",
    (11, "S13", "Sulamaya açılan net tarımsal alan"): "değer iki kaynaktan hesaplanmış (3,34 + 0,42); XII. Plan yalnız brüt veriyor",
    (11, "S19", "sulamaya açılan net tarımsal alan"): "iki kaynaktan hesaplanmış",
    (10, "S19", "kanalizasyon şebekesiyle"): "resmî kaynak yerine TBB yayını (ikincil)",
    (1, "S19", "köy içme suyu yatırımı"): "hedefin fiyat bazı belirsiz; cari TL tutarı karşılaştırılamaz",
    (5, "S19", "sulama alanı"): "plan tablosunda birim '100 Ha' yazıyor ama değerler bin hektar; fark hesabı yanıltıcı olur",
    (7, "S01", "Yükseköğretim okullaşma oranı"): "açıköğretim sayımı değişmiş (plan başlangıcı 26,7, sonraki kaynaklarda 22,1); gerçekleşme hedefle aynı tabanda değil",
    (7, "S18", "Birincil enerji üretimi"): "hidrolik dönüşüm yöntemi değişmiş (1 GWh = 250 → 86 TEP); gerçekleşme hedefle aynı tabanda değil",
    (10, "S18", "Birincil enerji üretiminde yerli kaynak payı"): "kaynak payı doğrudan vermiyor (100 − 'yüzde 72' ithalat oranı) ve hedef tanımı TPAO'nun yurt dışı üretimini de sayıyor",
    (10, "S10", "Vergi yükü"): "hedef 1998 bazlı, gerçekleşme 2009 bazlı GSYH ile; 4,9 puanlık farkın yaklaşık 2,9 puanı seri revizyonundan geliyor",
    (6, "S16", "plan dönemi toplam yeni konut ihtiyacı"): "hedef üretim değil ihtiyaç tahmini (yalnız 20 bin+ nüfuslu yerler); toplam bizim hesabımız ve ruhsat serisiyle sonuç tersine dönüyor",
    (7, "S16", "plan dönemi toplam yeni konut ihtiyacı"): "hedef üretim değil ihtiyaç tahmini; sonraki plan dönemi üretimiyle karşılaştırmıyor, toplam bizim hesabımız",
    (8, "S16", "plan dönemi toplam konut ihtiyacı"): "hedef üretim değil ihtiyaç tahmini (20 bin+ nüfuslu yerler); kapsam kullanım izni serisinden farklı, toplam bizim hesabımız",
    (6, "S14", "İmalat sanayii ihracatının toplam ihracat içindeki payı"): "sonuç sınıflamaya göre tersine dönüyor (DPT 92,9 hedef üstü, TÜİK ISIC Rev.3 85,7 hedef altı)",
    (10, "S22", "Cari işlemler dengesi"): "dolar değeri revizyon öncesi seriden (−27,0; revize seride −14,6); panodaki oran satırı (WDI) revize seriyle aynı olguyu veriyor",
    (10, "S05", "Nüfus artış hızı"): "plan tanım yazmıyor; göç dahil artış (binde 14,7) hedefin üstünde, doğal artış (yaklaşık binde 10) altında: sonuç tanıma göre tersine dönüyor",
    (10, "S17", "bütünleşik afet tehlike haritası"): "tamamlanan haritalar yalnız heyelan, kaya düşmesi ve çığı kapsıyor; 'bütünleşik' tüm afet türleri diye okunursa hedef tutmamış, sonuç okumaya göre tersine dönüyor",
    (11, "S26", "Gezici kütüphane sayısı"): "2023 değeri sayım tarihine göre değişiyor (2024 Programı 75, KYGM bülteni Şubat 2024'te gönderilen 10 aracı da sayarak 85); sonuç tersine dönüyor",
}
YAKINA_DUSUR = {
    (3, "S13", "Tarım sektörü katma değeri büyümesi"): "revize seri (SBB) aynı dönem için %1,2 veriyor",
    (5, "S13", "Tarım üretimi yıllık ortalama artış"): "1989 değeri tahmin",
    (11, "S13", "Tescili tamamlanan arazi toplulaştırma"): "2023 değeri gerçekleşme tahmini",
    (11, "S19", "sulama oranı"): "2023 değeri gerçekleşme tahmini",
    (7, "S10", "Vergi gelirlerinin GSMH"): "oran tablodan servet vergileri çıkarılarak hesaplandı; 2002 Programı aynı yıl için 24,4 veriyor",
}


# Planın hedef değil tahmin, beklenti, projeksiyon ya da ihtiyaç tespiti olarak yazdığı satırlar (X ve XI dışı planlar).
# Çıktıda nitelik = "tahmin"; sitede ayrı etiketle gösterilir (fark "hedef tuttu/tutmadı" diye okunmasın).
TAHMIN = {
    (4, "S05", "Toplam doğurganlık oranı (uzun dönem)"): "uzun dönem projeksiyon varsayımı",
    (8, "S05", "Toplam doğurganlık hızı (tahmin)"): "planda tahmin",
    (6, "S05", "Nüfus artış hızı (beklenen)"): "planda beklenti",
    (8, "S05", "Yıllık nüfus artış hızı (tahmin)"): "planda tahmin",
    (9, "S05", "Annual natural increase"): "plan projeksiyonu",
    (9, "S08", "mahalli idare sabit sermaye yatırımı"): "plan projeksiyonu",
    (3, "S12", "televizyon yayın alanındaki nüfus oranı"): "planda tahmin",
    (2, "S16", "şehir konutu ihtiyacı"): "ihtiyaç tahmini, üretim hedefi değil",
    (2, "S18", "Ham petrol talebi"): "talep tahmini",
    (6, "S18", "Birincil enerji talebi"): "talep tahmini",
    (8, "S18", "Birincil enerji tüketimi"): "tüketim projeksiyonu",
    (10, "S18", "Enerji ithalatı"): "ithalat projeksiyonu",
    # X cari (−5,2) buradan çıkarıldı: md. 476 "hedeflenmektedir" (01.10.2026). X ve XI satırları NITELIK_X_XI'den okunur.
}


# X. ve XI. Plan satırlarının niteliği, planın kendi sözüyle (hedef/tahmin düzeltmesi, 01.10.2026;
# yonetim/raporlar/hedef-tahmin-taramasi-2026-10-01.md). X'in "Gelişmeler ve Hedefler" ve XI'in "… Hedefleri"
# tablolarının dipnotu son yıl sütununu "Plan tahminleri" diye tanımlar; bu yüzden bir sayı ancak plan metninde
# ("hedeflenmektedir", "üretilecektir") ya da X'in Öncelikli Dönüşüm Programlarının "Program Hedefleri" listesinde
# geçiyorsa hedef sayılır. Metin "öngörülmektedir/beklenmektedir" diyorsa ongoru. Dipnotunda tahmin olmayan
# "Hedefler" tablosu satırı hedef (başlık) sayılır. Sayfalar PDF sayfasıdır.
D_X = "dipnot: '2013 ve 2018 yılı verileri Onuncu Kalkınma Planı tahminleridir'"
D_XI = "dipnot: '2023 yılı verileri On Birinci Kalkınma Planı tahminleridir'"
NITELIK_X_XI = {
    (10, "S01", "Okul öncesi (4-5 yaş) brüt okullaşma oranı"): ("tahmin", f"X Tablo 2 (PDF 44), {D_X}"),
    (10, "S02", "Gençlerde işsizlik oranı"): ("tahmin", f"X Tablo 6 (PDF 58), {D_X}"),
    (10, "S04", "Kadın işgücüne katılma oranı"): ("hedef", "X Öncelikli Dönüşüm Programı, Program Hedefleri (PDF 176): 'yüzde 34,9 … yükseltilmesi'; Tablo 6 dipnotu tahmin"),
    (10, "S05", "Toplam doğurganlık hızı"): ("tahmin", f"X Tablo 8 'Nüfus Gelişmeleri ve Tahminleri' (PDF 62), {D_X}; md. 350 yalnız nitel hedef ('yükseltilmesi hedeflenmektedir')"),
    (10, "S08", "mahalli idare harcamalarının GSYH'ya oranı"): ("tahmin", f"X Tablo 36 (PDF 145), {D_X}"),
    (10, "S08", "mahalli idare gelirlerinin GSYH'ya oranı"): ("tahmin", f"X Tablo 36 (PDF 145), {D_X}"),
    (10, "S10", "Kayıt dışı istihdam oranı"): ("tahmin", f"X Tablo 6 (PDF 58), {D_X}. X'in kayıt dışılık hedefi başka ölçüde: 'Tarım dışı sektörlerde kayıt dışı istihdam oranının beş puan azaltılması' (Program Hedefleri, PDF 178); eylem planı (YPK 2015/3) %22 → 2018 %17; 2018 gerçekleşme %22,28 (TÜİK HİA, SGK derlemesi)"),
    (10, "S13", "Arazi toplulaştırma (kümülatif)"): ("hedef", "X Tablo 24 'Gelişmeler ve Hedefler' (PDF 112); bu satırda tahmin dipnotu yok (dipnot 4 ve 5 başka satırlara bağlı)"),
    (10, "S13", "İşletmeye açılan sulama alanı (net kümülatif, DSİ)"): ("hedef", "X Tablo 24 'Gelişmeler ve Hedefler' (PDF 112); bu satırda tahmin dipnotu yok"),
    (10, "S14", "İmalat sanayii / GSYH (cari)"): ("tahmin", f"X Tablo 20 (PDF 101), {D_X}"),
    (10, "S14", "Yüksek teknoloji sektörlerinin imalat ihracatındaki payı"): ("tahmin", f"X Tablo 20 (PDF 101), {D_X}"),
    (10, "S14", "Ortanın üstü teknoloji sektörlerinin imalat ihracatındaki payı"): ("tahmin", f"X Tablo 20 (PDF 101), {D_X}"),
    (10, "S15", "Ar-Ge harcaması / GSYH"): ("tahmin", f"X Tablo 19 (PDF 98), {D_X}"),
    (10, "S15", "Yerli patent başvuru sayısı"): ("hedef", "X Tablo 22 'Patent Başvurularında Gelişmeler ve Hedefler' (PDF 107); dipnotta tahmin yok"),
    (10, "S15", "TZE araştırmacı sayısı"): ("tahmin", f"X Tablo 19 (PDF 98), {D_X}"),
    (10, "S17", "zorunlu deprem sigortasına dâhil konut ve işyeri sayısı"): ("tahmin", f"X Tablo 37 (PDF 152), {D_X}"),
    (10, "S18", "Yenilenebilir kaynakların elektrik üretimindeki payı"): ("tahmin", f"X Tablo 25 (PDF 115), {D_X}"),
    (10, "S18", "Enerji ithalatı"): ("tahmin", f"X Tablo 12 (PDF 79), {D_X}"),
    (10, "S19", "işletmeye açılan sulama alanı (net kümülatif)"): ("hedef", "X Tablo 24 'Gelişmeler ve Hedefler' (PDF 112); bu satırda tahmin dipnotu yok"),
    (10, "S19", "DSİ sulamalarında sulama oranı"): ("hedef", "X Öncelikli Dönüşüm Programı, Program Hedefleri (PDF 190): 'yüzde 68'e … çıkarılması'"),
    (10, "S19", "DSİ sulamalarında sulama randımanı"): ("hedef", "X Öncelikli Dönüşüm Programı, Program Hedefleri (PDF 190): 'yüzde 50'ye çıkarılması'"),
    (10, "S20", "en yüksek / en düşük gelirli bölge kişi başı gelir oranı"): ("tahmin", f"X Tablo 31 (PDF 135), {D_X}"),
    (10, "S20", "5. ve 6. bölge illerinde teşvik belgeli yatırımın payı"): ("tahmin", f"X Tablo 31 (PDF 135), {D_X}"),
    (10, "S21", "TÜFE yıllık artış hızı"): ("hedef", "X md. 493 (PDF 81): 'yüzde 4,5'e indirilmesi hedeflenmektedir'"),
    (10, "S21", "TÜFE yıllık artışı (yıl sonu)"): ("hedef", "X md. 493 (PDF 81): 'yüzde 4,5'e indirilmesi hedeflenmektedir'; Tablo 13 'Enflasyon Gelişmeleri ve Tahminleri' dipnotu tahmin"),
    (10, "S22", "Cari işlemler dengesi / GSYH"): ("hedef", "X md. 476 (PDF 79): 'yüzde 5,2'ye gerilemesi hedeflenmektedir'; Tablo 12 dipnotu tahmin"),
    (11, "S01", "5 yaş net okullaşma oranı"): ("tahmin", f"XI Tablo 33 (PDF 137), {D_XI}"),
    (11, "S01", "Okullaşma oranı, kadın (yükseköğrenim)"): ("tahmin", f"XI Tablo 36 (PDF 147), {D_XI}"),
    (11, "S02", "İşsizlik oranı, genç nüfus"): ("tahmin", f"XI Tablo 34 (PDF 140), {D_XI}"),
    (11, "S02", "Genç istihdam oranı (15-24 yaş)"): ("tahmin", f"XI Tablo 37 (PDF 153), {D_XI}"),
    (11, "S04", "İşgücüne katılma oranı, kadın"): ("tahmin", f"XI Tablo 34 (PDF 140), {D_XI}"),
    (11, "S04", "Kadın istihdam oranı"): ("tahmin", f"XI Tablo 36 (PDF 147), {D_XI}"),
    (11, "S05", "Toplam doğurganlık hızı"): ("tahmin", f"XI Tablo 41 'Nüfus Hedefleri' (PDF 161), {D_XI}"),
    (11, "S05", "Yaşlı nüfusun işgücüne katılma oranı"): ("tahmin", f"XI Tablo 41 (PDF 161), {D_XI}"),
    (11, "S10", "Kayıt dışı istihdam oranı"): ("tahmin", f"XI Tablo 34 (PDF 140), {D_XI}; 28,5 metinde geçmiyor"),
    (11, "S10", "Genel devlet gelirleri"): ("tahmin", f"XI Tablo 9 'Kamu Maliyesine İlişkin Hedefler' (PDF 56), {D_XI}"),
    (11, "S13", "Tarım sektörü büyüme hızı"): ("ongoru", "XI md. 218 (PDF 41): 'yüzde 3,1 oranında büyümesi … beklenmektedir'"),
    (11, "S13", "Tescili tamamlanan arazi toplulaştırma alanı"): ("tahmin", f"XI Tablo 19 (PDF 98), {D_XI}"),
    (11, "S14", "İmalat sanayii / GSYH (cari)"): ("tahmin", f"XI Tablo 12 'İmalat Sanayiinde Hedefler' (PDF 63), {D_XI}"),
    (11, "S14", "Orta-yüksek teknolojili sanayilerin imalat ihracatındaki payı"): ("tahmin", f"XI Tablo 12 (PDF 63), {D_XI}"),
    (11, "S14", "Yüksek teknolojili sanayilerin imalat ihracatındaki payı"): ("tahmin", f"XI Tablo 12 (PDF 63), {D_XI}"),
    (11, "S15", "Ar-Ge harcaması / GSYH"): ("tahmin", f"XI Tablo 23 'Bilim, Teknoloji ve Yenilik Hedefleri' (PDF 108), {D_XI}"),
    (11, "S15", "TZE Ar-Ge personeli sayısı"): ("tahmin", f"XI Tablo 23 (PDF 108), {D_XI}"),
    (11, "S15", "Yerli patent başvurularının toplam içindeki payı"): ("tahmin", f"XI Tablo 25 (PDF 113), {D_XI}"),
    (11, "S16", "sosyal konut üretimi (plan dönemi)"): ("hedef", "XI md. 686.2 (PDF 167): '250 bin sosyal konut üretilecektir'"),
    (11, "S16", "kentsel dönüşüm strateji belgesi hazırlanan il sayısı"): ("tahmin", f"XI Tablo 45 (PDF 169), {D_XI}"),
    (11, "S17", "zorunlu deprem sigortasına dâhil konut ve işyeri sayısı"): ("tahmin", f"XI Tablo 49 (PDF 178), {D_XI}"),
    (11, "S17", "risk azaltma planı hazırlanacak il sayısı"): ("tahmin", f"XI Tablo 49 (PDF 178), {D_XI}"),
    (11, "S18", "Yerli kaynaklardan üretilen elektrik"): ("tahmin", f"XI Tablo 27 (PDF 120), {D_XI}"),
    (11, "S18", "Yenilenebilir kaynakların elektrik üretimindeki payı"): ("tahmin", f"XI Tablo 27 (PDF 120), {D_XI}"),
    (11, "S19", "sulama oranı"): ("tahmin", f"XI Tablo 19 (PDF 98), {D_XI}"),
    (11, "S19", "içme suyu kayıp kaçak oranı"): ("tahmin", f"XI Tablo 46 (PDF 172), {D_XI}"),
    (11, "S20", "en yüksek/en düşük gelirli bölge kişi başı gelir oranı"): ("tahmin", f"XI Tablo 42 'Bölgesel Gelişme Hedefleri' (PDF 164), {D_XI}; XII aynı 3,85'i 2028 hedefi olarak yazar"),
    (11, "S21", "TÜFE (yıl sonu)"): ("hedef", "XI md. 179 (PDF 38): 'enflasyon yüzde 5 hedefine kademeli bir şekilde yakınsayacaktır'; Tablo 7 'Enflasyon Tahminleri' dipnotu: '2023 yılı verisi On Birinci Kalkınma Planı tahminidir'"),
    (11, "S22", "Cari işlemler dengesi / GSYH"): ("ongoru", "XI md. 178 (PDF 38): 'yüzde 0,9 olarak gerçekleşmesi öngörülmektedir'; Tablo 6 dipnotu tahmin"),
    (11, "S22", "Cari işlemler dengesi"): ("tahmin", f"XI Tablo 6 'Ödemeler Dengesine İlişkin Hedefler' (PDF 48), {D_XI}"),
}
ESKI_NITELIK = "X/XI dışı: 03-v1.2 sınıflaması (tablo başlığı ve cümle); 01.10.2026 düzeltmesinde yeniden sınanmadı"


def anahtar_bul(tablo, plan, sorun, gosterge):
    return next((v for (p, so, bas), v in tablo.items() if p == plan and so == sorun and gosterge.startswith(bas)), None)


hedefler = list(csv.DictReader(open(HEDEF, encoding="utf-8-sig")))
enf = {r["hedef_yili"]: r for r in csv.DictReader(open(ENF, encoding="utf-8-sig"))}


def bul(plan, sorun, bas):
    eslesen = [h for h in hedefler if int(h["plan_no"]) == plan and h["sorun_id"] == sorun and h["gosterge"].startswith(bas)]
    # Birden çok satır göstergenin başıyla eşleşirse ("… (uzun dönem perspektif)" gibi) tam eşleşen seçilir.
    tam = [h for h in eslesen if h["gosterge"] == bas]
    if len(eslesen) > 1 and len(tam) == 1:
        eslesen = tam
    if len(eslesen) != 1:
        raise SystemExit(f"Eşleşme {len(eslesen)} satır: {plan} {sorun} {bas}")
    return eslesen[0]


def yuvarla(x):
    return f"{x:.2f}".rstrip("0").rstrip(".") if abs(x) < 1000 else f"{x:.0f}"


satirlar = []
for plan, sorun, bas, seri, yillar, eslesme, not_ in ESLEME:
    h = bul(plan, sorun, bas)
    degerler = [wdi.get(seri, {}).get(y) for y in yillar]
    if any(d is None or math.isnan(d) for d in degerler):
        raise SystemExit(f"Veri yok: {seri} {list(yillar)}")
    yillar = list(yillar)
    # "Açık" diye yazılmış hedeflerde seri (eksi = açık) açık cinsine çevrilir.
    if not_.startswith("AÇIK "):
        degerler = [-d for d in degerler]
        not_ = not_[5:]
    satirlar.append({
        "plan_no": plan, "sorun_id": sorun, "gosterge": h["gosterge"], "hedef_degeri": h["hedef_degeri"], "birim": h["birim"],
        "hedef_yili": h["hedef_yili"], "gerceklesme": yuvarla(sum(degerler) / len(degerler)),
        "gerceklesme_donemi": str(yillar[0]) if len(yillar) == 1 else f"{yillar[0]}–{yillar[-1]}",
        "eslesme": eslesme, "kaynak": KAYNAK[seri], "not": not_,
    })
for plan, bas, yil in ENF_ESLEME:
    h = bul(plan, "S21", bas)
    e = enf[yil]
    satirlar.append({
        "plan_no": plan, "sorun_id": "S21", "gosterge": h["gosterge"], "hedef_degeri": h["hedef_degeri"], "birim": h["birim"],
        "hedef_yili": h["hedef_yili"], "gerceklesme": e["gerceklesme"], "gerceklesme_donemi": yil,
        "eslesme": "ayni_olcu" if e["not"].startswith("Aynı ölçü") else "yakin_olcu",
        "kaynak": e["kaynak"], "not": f"{e['gerceklesme_olcusu']}. {e['not']}".strip(),
    })

import glob
cikan = []
for dosya in sorted(glob.glob("veri/gerceklesme_arastirma_*.csv")):
    for r in csv.DictReader(open(dosya, encoding="utf-8-sig")):
        plan, sorun = int(r["plan_no"]), r["sorun_id"]
        neden = anahtar_bul(ARASTIRMA_DISI, plan, sorun, r["gosterge"])
        if neden:
            cikan.append(f"{plan} {sorun} {r['gosterge']}: {neden}")
            continue
        h = bul(plan, sorun, r["gosterge"])
        eslesme, not_ = r["eslesme"], r["not"]
        dusur = anahtar_bul(YAKINA_DUSUR, plan, sorun, r["gosterge"])
        if dusur and eslesme == "ayni_olcu":
            eslesme = "yakin_olcu"
            # Gerekçe notta zaten geçiyorsa tekrar yazılmaz.
            if "tahmin" not in not_.lower() and dusur.split(" ")[0].lower() not in not_.lower():
                not_ = f"{dusur[0].upper()}{dusur[1:]}. {not_}".strip()
        satirlar.append({
            "plan_no": plan, "sorun_id": sorun, "gosterge": h["gosterge"], "hedef_degeri": h["hedef_degeri"], "birim": h["birim"],
            "hedef_yili": h["hedef_yili"], "gerceklesme": r["gerceklesme"], "gerceklesme_donemi": r["gerceklesme_donemi"],
            "eslesme": eslesme, "kaynak": r["kaynak"], "not": not_, "alinti": r["alinti"],
        })
for s_ in satirlar:
    s_.setdefault("alinti", "")
    plan_, sorun_ = int(s_["plan_no"]), s_["sorun_id"]
    if plan_ in (10, 11):
        # Tam eşleşme önce ("Cari işlemler dengesi" ile "Cari işlemler dengesi / GSYH" karışmasın).
        nk = NITELIK_X_XI.get((plan_, sorun_, s_["gosterge"])) or anahtar_bul(NITELIK_X_XI, plan_, sorun_, s_["gosterge"])
        if not nk:
            raise SystemExit(f"X/XI satırının niteliği yazılmamış: {plan_} {sorun_} {s_['gosterge']}")
        s_["nitelik"], s_["nitelik_kaynagi"] = nk
    else:
        neden = anahtar_bul(TAHMIN, plan_, sorun_, s_["gosterge"])
        s_["nitelik"] = "tahmin" if neden else "hedef"
        s_["nitelik_kaynagi"] = f"{ESKI_NITELIK} ({neden})" if neden else ESKI_NITELIK
satirlar.sort(key=lambda r: (r["sorun_id"], int(r["plan_no"])))
with open(CIKTI, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(satirlar[0].keys()))
    w.writeheader()
    w.writerows(satirlar)
print(f"{CIKTI}: {len(satirlar)} satır; araştırmadan çıkarılan {len(cikan)}:")
for c in cikan:
    print("  -", c)
