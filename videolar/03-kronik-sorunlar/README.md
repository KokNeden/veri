# 03 · Türkiye'nin 24 kronik sorunu: 12 kalkınma planı ne hedefledi, ne oldu?

Video ve sayfası yakında yayında. · Sürüm: v1.2 · Güncelleme: 1 Ekim 2026

## Özet

Bir soruna ne zaman "kronik" denir? Bu videoda üç koşul koyduk: sorun Cumhuriyet tarihinin dört döneminin en az üçünde görülmeli; devlet bu sorun için bir hedef koymuş ve tutturamamış olmalı; başka ülkelerle karşılaştırma da bunu desteklemeli. Planda hedef yoksa, yıllar boyunca tekrarlanan bağımsız ölçümlere baktık.

1963'ten bu yana yayımlanan on iki kalkınma planını baştan sona taradık ve sorunlarla ilgili her hedefi ve ifadeyi 630 satırlık bir tabloya çıkardık. Sonuç: yedi sütunda 24 kronik sorun. En kronik sorunların bir kısmı için planların hiç ölçülebilir hedef koymadığını, testi geçemeyen bir maddeyi (beyin göçü) ve listeye girmeyen iyi haberleri de açıkça gösteriyoruz.

## Veri dosyaları

- [plan-hedefleri.csv](veri/plan-hedefleri.csv): On iki planda sorunlarla ilgili 630 hedef ve ifade; plan, sayfa, alıntı ve plan metnine karşı otomatik doğrulama sonucu.
- [enflasyon-hedef-gerceklesme.csv](veri/enflasyon-hedef-gerceklesme.csv): Planların enflasyon hedefleri ya da öngörüleri ve aynı ölçüyle gerçekleşmeler; `nitelik` ve dayanağı.
- [plan-hedef-gerceklesme.csv](veri/plan-hedef-gerceklesme.csv): Gerçekleşmesi aynı ya da yakın ölçüyle bulunan 169 plan sayısı; `nitelik` (hedef, tahmin, öngörü) ve dayanağı (`nitelik_kaynagi`).
- [dunya-bankasi-secilmis.csv](veri/dunya-bankasi-secilmis.csv): Videoda kullanılan Dünya Bankası serileri, Türkiye ve OECD ortancası (Türkiye hariç).
- [vdem-donem-karsilastirmasi.csv](veri/vdem-donem-karsilastirmasi.csv): V-Dem göstergelerinin dört dönem ortalaması: Türkiye, karşılaştırma seti ve OECD ortancası.
- [deprem-olumleri.csv](veri/deprem-olumleri.csv): Deprem ölümleri, yılda milyon kişi başına, dört dönem.
- [beyin-gocu.csv](veri/beyin-gocu.csv): Yükseköğrenimli göç oranı ve seçicilik, 1980–2010.
- [sorun-listesi.csv](veri/sorun-listesi.csv): Sorun listesi (sütun, ad, ana ölçüm).

Sütunların anlamı ve her dosyanın kaynağı: [`veri/sozluk.json`](veri/sozluk.json).

## Kod

- [`kod/analiz/`](kod/analiz/)

Kod, Kök Neden'in çalışma klasörü düzenine göre yazıldı; ham verileri kaynak adreslerinden kendisi indirir ya da README'sinde nereden indirileceğini söyler.

## Kaynaklar

1. DPT / SBB, *Beş Yıllık Kalkınma Planları* I–XII (1963–2028). IX. Plan için resmî İngilizce çeviri kullanıldı (Türkçe PDF taranmış görüntü). [sbb.gov.tr](https://www.sbb.gov.tr/kalkinma-planlari/)
2. DPT, *Dördüncü Beş Yıllık Kalkınma Planı 1979–1983*, Yayın No. 1664, Nisan 1979; Tablo 30 "Planlı Dönemde Önlemlerin Uygulama Durumu (1963–1977)" ve md. 104–105.
3. TÜİK, *İstatistik Göstergeler 1923–2011*, Tablo 17.15 (fiyat endeksleri ve değişim oranları).
4. TCMB, Tüketici Fiyatları tablosu (TÜİK verisi; aralık ayı yıllık değişim = yıl sonu enflasyonu). [tcmb.gov.tr](https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Enflasyon+Verileri/Tuketici+Fiyatlari)
5. Dünya Bankası, *World Development Indicators* (Ar-Ge harcaması, cari denge, net enerji ithalatı, bebek ölüm hızı, yükseköğretim okullaşması, doğurganlık). [databank.worldbank.org](https://databank.worldbank.org/source/world-development-indicators)
6. V-Dem Institute, *Varieties of Democracy* veri seti v16 (Country-Year: V-Dem Full+Others), 2026. [v-dem.net](https://www.v-dem.net/data/the-v-dem-dataset/)
7. EM-DAT, CRED / UCLouvain, uluslararası afet veri tabanı; Our World in Data işlemesi. Nüfus: Our World in Data. [emdat.be](https://www.emdat.be/)
8. OECD, PISA matematik ortalama puanları 2003–2022; Our World in Data işlemesi. [oecd.org/pisa](https://www.oecd.org/pisa/)
9. Dünya ve Avrupa Değerler Araştırmaları (WVS / EVS), "İnsanların çoğuna güvenilebilir mi?" sorusu; Our World in Data işlemesi. [ourworldindata.org](https://ourworldindata.org/grapher/self-reported-trust-attitudes)
11. Maddison Project Database, kişi başı gelir; Our World in Data işlemesi. [rug.nl/ggdc](https://www.rug.nl/ggdc/historicaldevelopment/maddison/)
10. Brücker, H., Capuano, S., Marfouk, A. (2013), *Education, gender and international migration: insights from a panel-dataset 1980–2010* (IAB Brain Drain Data). [iab.de](https://iab.de/en/daten/iab-brain-drain/)
12. Kalkınma Bakanlığı, *Onuncu Kalkınma Planı (2014-2018) Kayıt Dışı Ekonominin Azaltılması Programı Eylem Planı*, YPK kararı 16.02.2015, 2015/3; "Performans Göstergeleri" tablosu (s. 2). [sbb.gov.tr](https://www.sbb.gov.tr/wp-content/uploads/2018/10/9Kayitdisi_Ekonominin_Azaltilmasi_Programi.pdf)
13. TÜİK, Hanehalkı İşgücü İstatistikleri: tarım dışı kayıt dışı istihdam oranı (SGK "Kayıtdışı İstihdam Oranları" derlemesi, arşiv kopyaları [2019](https://web.archive.org/web/20191016201830/http://www.sgk.gov.tr/wps/portal/sgk/tr/calisan/kayitdisi_istihdam/kayitdisi_istihdam_oranlari) ve [2024](https://web.archive.org/web/20240720135919/http://eski.sgk.gov.tr/wps/portal/sgk/tr/calisan/kayitdisi_istihdam/kayitdisi_istihdam_oranlari)); TÜİK İşgücü İstatistikleri Aralık 2018 bülteni (Sayı 30681).

Erişim tarihi: 26–27.09.2026 (12 ve 13: 01.10.2026).

## Sınırlılıklar

- **Nasıl yapıldı:** Kaynak tarama, veri işleme ve görsellerin kodu yapay zekâ araçları desteğiyle yapıldı. Metin taslaklarında da yapay zekâ araçlarından destek alındı; her cümleyi Berk Can okuyup onayladı. Metindeki her iddia, yazarın notlarını kanıt saymadan, ayrı bir yapay zekâ denetimiyle ham kaynağa karşı sınandı (kaynak testi); bulguları Berk Can inceledi. Seslendirme, Berk Can'ın sesinden (ses örneği) yapay zekâyla üretildi. Uzman okuması: henüz yok. Ayrıntı: Nerede duruyoruz?
- **Tablo 30** önlemlerin *sayısını* ölçer, ağırlığını değil; IV. Plan bu çekinceyi kendisi yazar.
- **Hedef ve tahmin:** X. ve XI. Planların tabloları başlıkta "hedefler" der, dipnotta aynı sütunu "Plan tahminleri" diye tanımlar; XII. Plan dipnotta "hedefleri" der. Bu yüzden X ve XI'den bir sayıyı ancak plan metninde ("hedeflenmektedir") ya da X'in "Program Hedefleri" listesinde de geçiyorsa hedef diye anıyoruz. Videonun ilk sürümünde bu sayıların bir kısmı "hedef" diye anıldı; düzeltme: 1 Ekim 2026 (aşağıda Düzeltmeler). `plan-hedef-gerceklesme.csv` ve `enflasyon-hedef-gerceklesme.csv` dosyalarındaki `nitelik` sütunu planın sözüne göre güncellendi; dayanağı `nitelik_kaynagi` sütununda. `plan-hedefleri.csv` dosyasında `hedef_degeri` planın yazdığı sayıdır; alıntılarda tablo dipnotu yoktur, niteliği gerçekleşme dosyasından ya da planın kendisinden okunmalıdır.
- **Kayıt dışılık:** X. Plan'ın hedefi toplam oran değil, tarım dışı orandır; yılı ve başlangıcı plan metninde değil, Yüksek Planlama Kurulu kararıyla (2015/3) yürürlüğe giren eylem planındadır. Plan programları kendini "rehber niteliğinde" diye tanımlar (md. 1127). VIII, IX ve XI. Planlarda kayıt dışılık için hedef nitelikli bir sayı yoktur; XI'in %28,5'i (2023) tabloda tahmindir ve oran 2023'te %26,1'e inmiştir. Hedef yılından sonra tarım dışı oran düştü: 2021'de %17,5. Bu düşüş pandemi yıllarına ve TÜİK'in 2021 yöntem değişikliğine denk gelir; nedeni bu çalışmada incelenmedi.
- **Ölçü farkı:** Hedef ve gerçekleşme her zaman aynı ölçü değildir (VIII. Plan enflasyonu yıl sonu hedeflerken tabloda yalnız yıllık ortalama var; enerji hedefleri Dünya Bankası ölçüsüyle birebir aynı değildir). Aynı ölçünün olmadığı yer tabloda belirtildi.
- **Ülke karşılaştırması** destekleyici bir ölçüttür. V-Dem uzman kodlamasına dayanır; uzun dönemlerde değerler sabit bloklar halinde gelir, dönem ortalaması kaba bir özettir.
- **Toplumsal güven** ölçümü 1990'ların başında başlar; yalnız iki dönem görülebilir ("ölçüm sınırlı 2/2").
- **Sanayi teknolojisi** için plan kanıtı zayıftır (imalat payı hedefleri kimi planda tuttu; III. Plan'ın tespiti ilk iki planın dönemi içindir); listeye çekinceyle alındı.
- **Dış finansman bağımlılığı** listeye çekinceyle alındı: planlar cari denge için çoğunlukla hedef değil öngörü yazdı ve öngörülerin yarısı tuttu; kroniklik daha çok 1974'ten bu yana süren açıklara dayanır.
- **Enerji:** X. Plan'ın "yerli kaynak" tanımı yurt dışındaki çıkarımları da içerir; Dünya Bankası ölçüsü içermez.
- **Deprem:** 2002 sonrası değer, nüfus verisinin bittiği yıla göre 28,9 ile 31,9 arasında değişir.
- **Beyin göçü** verisi 2010'da biter; 2016 sonrası göç dalgası bu veride yoktur.
- Planlardaki OCR hataları alıntılarda olduğu gibi korundu.

## Düzeltmeler

**1 Ekim 2026 · hedef mi, tahmin mi?** Kendi denetimimizde (Terazi) bulundu. X. ve XI. Kalkınma Planlarının "Hedefler" başlıklı tabloları, son yıl sütununu dipnotta "Plan tahminleri" diye tanımlıyor[^d1]. Videonun ilk sürümü bu sayıların bir kısmını "hedef" diye andı. Video bu yüzden yeniden seslendiriliyor; yeni sürüm yüklenince bu sayfadaki transkript ve altyazı da yenilenecek. Değişen cümleler:

| Videonun ilk sürümünde | Doğrusu (yeni sürüm) | Kaynak |
|---|---|---|
| "Ar-Ge harcaması için altı plan üst üste hedef koydu … Altısında da tutmadı." | Altı plan bir sayı yazdı: dördü hedef (VI–IX), son ikisi (X ve XI, %1,8) tahmin. Hiçbirine ulaşılmadı. | [^d2] |
| "En yakın gelinen yıl 2023: hedef yüzde 1,8" | XI'in 2023 tahmini yüzde 1,8 | [^d2] |
| "Gelir farkını 2023'te 3,85 kata indirme hedefi … tutmadı; aynı hedef yeniden kondu." | XI 3,85'i 2023 için öngördü (tahmin); XII 2023 farkını 4,30 kat olarak tahmin etti ve 3,85'i 2028 hedefi olarak yazdı. | [^d3] |
| "Kayıp ve kaçak için 2023 hedefi yüzde 25'ti" | XI 2023'te yüzde 25 öngördü (tahmin); XII'nin tahmini yüzde 31. | [^d3] |
| "On Birinci Plan … hedefi 2023'e taşıdı. On İkinci Plan da 2028'e." (kadın iş gücü) | XI 2023 için yüzde 38,5 öngördü; XII 2028 için yüzde 40,1'i hedef olarak koydu. | [^d3] |
| "2023 için hedef kadın başına 2,15 çocuktu." | XI'in 2023 tahmini 2,15 çocuktu. | [^d3] |
| "Onuncu Plan 2018 için kayıt dışı istihdamı yüzde 30'a indirmeyi hedefledi. On Birinci Plan 2018'i yüzde 33,4 olarak yazdı." | %30 tahmindi. X'in hedefi başka bir ölçüde: tarım dışı kayıt dışı istihdamı 2018'e kadar %22'den %17'ye indirmek (program ve eylem planı); 2018'de %22,3. | [^d4] |
| "Yenilenebilir kaynaklardan elektrik üretimi hedefleri son iki planda tuttu." | Yenilenebilir kaynakların elektrik üretimindeki payı son iki planın tahminlerini aştı. | [^d3] |

Yeni sürümde ekranlar da (enflasyon, Ar-Ge, bölgesel ve su kartları, kadın iş gücü, kayıt dışılık) aynı dile çekiliyor; Shorts'taki Ar-Ge cümlesi "altı plan üst üste bir sayı yazdı; hiçbirine ulaşılmadı" oluyor. Listedeki 24 sorun değişmedi. Bu sayfada rakam satırları, "Hedef ve tahmin" sınırlılığı (eski metni: "Videoda ve tabloda bu ayrım gözetildi") ve veri dosyalarının `nitelik` sütunu düzeltildi; `plan-hedef-gerceklesme.csv`'de X cari denge hedef, XI cari denge öngörü olarak düzeltildi (iki satır ters etiketliydi).

[^d1]: X. Plan, örn. Tablo 6 (PDF 58): "2013 ve 2018 yılı verileri Onuncu Kalkınma Planı tahminleridir."; XI. Plan, örn. Tablo 42 (PDF 164): "2023 yılı verileri On Birinci Kalkınma Planı tahminleridir."; XII. Plan, örn. Tablo 52 (PDF 229): "… 2028 yılı verileri On İkinci Kalkınma Planı hedefleridir."
[^d2]: X. Plan Tablo 19 (PDF 98) ve XI. Plan Tablo 23 (PDF 108), dipnot "tahminleridir"; VI–IX için plan metinleri (VI PDF 324, VII PDF 87, VIII PDF 135, IX Table 6.8 "R&D Targets").
[^d3]: XI. Plan Tablo 42 (PDF 164), 46 (PDF 172), 34 (PDF 140), 41 (PDF 161), 27 (PDF 120); X. Plan Tablo 25 (PDF 115): hepsinde dipnot "tahminleridir". XII. Plan Tablo 52 (PDF 229) ve Tablo 36 (PDF 175): 2028 "hedefleridir".
[^d4]: X. Plan Tablo 6 (PDF 58, dipnot "tahminleridir") ve Kayıt Dışı Ekonominin Azaltılması Programı, Program Hedefleri (PDF 178); eylem planı (YPK 2015/3), s. 2; TÜİK HİA (Kaynaklar 12, 13).

---
Veri: [CC BY 4.0](../../LICENSE) · Kod: [MIT](../../LICENSE-KOD) · Bu klasör `node yonetim/acik-veri.mjs 03` ile üretilir; elle düzenlenmez.
