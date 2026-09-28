# 03 · Türkiye'nin 24 kronik sorunu: 12 kalkınma planı ne hedefledi, ne oldu?

Video yakında YouTube’da. · [Sitedeki sayfa](https://kokneden.org/videolar/03-kronik-sorunlar/) · Sürüm: v1.1 · Güncelleme: 27 Eylül 2026

## Özet

Bir soruna ne zaman "kronik" denir? Bu videoda üç koşul koyduk: sorun Cumhuriyet tarihinin dört döneminin en az üçünde görülmeli; devlet bu sorun için bir hedef koymuş ve tutturamamış olmalı; başka ülkelerle karşılaştırma da bunu desteklemeli. Planda hedef yoksa, yıllar boyunca tekrarlanan bağımsız ölçümlere baktık.

1963'ten bu yana yayımlanan on iki kalkınma planını baştan sona taradık ve sorunlarla ilgili her hedefi ve ifadeyi 630 satırlık bir tabloya çıkardık. Sonuç: yedi sütunda 24 kronik sorun. En kronik sorunların bir kısmı için planların hiç ölçülebilir hedef koymadığını, testi geçemeyen bir maddeyi (beyin göçü) ve listeye girmeyen iyi haberleri de açıkça gösteriyoruz.

## Veri dosyaları

- [plan-hedefleri.csv](veri/plan-hedefleri.csv): On iki planda sorunlarla ilgili 630 hedef ve ifade; plan, sayfa, alıntı ve plan metnine karşı otomatik doğrulama sonucu.
- [enflasyon-hedef-gerceklesme.csv](veri/enflasyon-hedef-gerceklesme.csv): Planların enflasyon hedefleri ya da öngörüleri ve aynı ölçüyle gerçekleşmeler.
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

Erişim tarihi: 26–27.09.2026.

## Sınırlılıklar

- **Tablo 30** önlemlerin *sayısını* ölçer, ağırlığını değil; IV. Plan bu çekinceyi kendisi yazar.
- **Hedef ve öngörü:** Planlar enflasyon ve bazı başka göstergeler için sayıyı kimi zaman "hedef", kimi zaman "tahmin" diye yazar. Videoda ve tabloda bu ayrım gözetildi; `plan-hedefleri.csv` dosyasında `hedef_degeri` sütunu planın yazdığı sayıdır, niteliği `gosterge` ve `alinti` sütunlarından okunmalıdır.
- **Ölçü farkı:** Hedef ve gerçekleşme her zaman aynı ölçü değildir (VIII. Plan enflasyonu yıl sonu hedeflerken tabloda yalnız yıllık ortalama var; enerji hedefleri Dünya Bankası ölçüsüyle birebir aynı değildir). Aynı ölçünün olmadığı yer tabloda belirtildi.
- **Ülke karşılaştırması** destekleyici bir ölçüttür. V-Dem uzman kodlamasına dayanır; uzun dönemlerde değerler sabit bloklar halinde gelir, dönem ortalaması kaba bir özettir.
- **Toplumsal güven** ölçümü 1990'ların başında başlar; yalnız iki dönem görülebilir ("ölçüm sınırlı 2/2").
- **Sanayi teknolojisi** için plan kanıtı zayıftır (imalat payı hedefleri kimi planda tuttu; III. Plan'ın itirafı ilk iki planın dönemi içindir); listeye çekinceyle alındı.
- **Dış finansman bağımlılığı** listeye çekinceyle alındı: planlar cari denge için çoğunlukla hedef değil öngörü yazdı ve öngörülerin yarısı tuttu; kroniklik daha çok 1974'ten bu yana süren açıklara dayanır.
- **Enerji:** X. Plan'ın "yerli kaynak" tanımı yurt dışındaki çıkarımları da içerir; Dünya Bankası ölçüsü içermez.
- **Deprem:** 2002 sonrası değer, nüfus verisinin bittiği yıla göre 28,9 ile 31,9 arasında değişir.
- **Beyin göçü** verisi 2010'da biter; 2016 sonrası göç dalgası bu veride yoktur.
- Planlardaki OCR hataları alıntılarda olduğu gibi korundu. Seslendirme bir ses üretim aracıyla yapıldı.

## Düzeltmeler

Henüz düzeltme yok. Her düzeltme bu bölüme tarihiyle, neyin değiştiğiyle ve (izin verilirse) bildirenin adıyla eklenir.

---
Veri: [CC BY 4.0](../../LICENSE) · Kod: [MIT](../../LICENSE-KOD) · Bu klasör `node yonetim/acik-veri.mjs 03` ile üretilir; elle düzenlenmez.
