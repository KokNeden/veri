# V4 · Sıralama v0.1: sonuçlar, duyarlılık, karşı-kontrol ve yorum

Durum: **ön sonuç** · 21 Eylül 2026 · Matris: Kök Neden taslağı v0.1 (Berk incelemesi bekliyor, bkz. `01-berke-sorular.md`)
Bu dosya `kod/rapor_tablolari.py` ile üretildi. Tablolar `cikti/` altındaki CSV'lerden otomatik doluyor; elle rakam girilmedi.

## 1. Ne yaptık?

1. **Matris:** 23 × 23, 149 dolu hücre. 28 hücre 3-4 puan (güçlü); her birinin en az bir akademik veya kurumsal kaynağı var (`veri/baglanti_gerekceleri.csv`). Bunların 4'ü "tartışmalı", 2'si "gerekçesi zayıf" işaretli (21.09 denetiminden sonra). Ayrıca 1 puanlık bir bağlantı (S08>S20) tartışmalı. 120 hücre 1-2 puanlık taslak yargı.
2. **Açık skorları (yalnız ikincil ölçüt):** Birincil ölçüt olan plan hedefleri henüz derlenmedi (`01-berke-sorular.md` A4); bu sürümde açık yalnız ülke setine göre. V2 verisi (WDI, 13.437 satır) + elle eklenenler: WGI 2023, PISA 2022, WVS 7. dalga (`veri/manuel_ek.csv`). 23 sorunun 17'sinde skor var; 3'ü vekil gösterge; 6'sı "bilmiyoruz".
3. **Etki düzeyleri:** `veri/sorunlar.csv`, her biri tek cümlelik gerekçeyle.
4. **V3 kodu:** DEMATEL, öncelik skoru, 10.000 senaryolu Monte Carlo, bağlantı sıfırlama testi, 17 ek senaryo, liste bağımlılığı testi (her sorun sırayla çıkarılır), otomatik tutarlılık kontrolleri, ISM.

## 2. Sonuç tablosu

{{TABLO_SONUC}}

*K = 0,5·ñ(D−R) + 0,5·ñ(D). Öncelik = K^0,5 · A^0,25 · E^0,25. "Bilmiyoruz" olan açık skorları tabanda 0,5. Yorum kuralı önceden ilan edildi: ≥ %80 sağlam · %50-80 büyük olasılıkla · %20-50 sınırda · < %20 ilk 5'te değil.*

![Neden-sonuç haritası](cikti/neden_sonuc_haritasi_v0.1.png)

**Neden grubu (D−R > 0):** S09, S06, S07, S12, S01, S13, S08, S18, S05.
**Sonuç grubu:** geri kalan 14 sorun. En güçlü sonuçlar: S23 verimlilik, S22 tasarruf/dış finansman, S21 enflasyon, S15 Ar-Ge, S03 beyin göçü.

## 3. Açık skorları

{{TABLO_ACIK}}

*Set (v0.1'de bütün sorunlar için varsayılan; kararlar gereği konuya göre değişebilir, ikincil ölçüt): KOR, ESP, PRT, GRC, POL, MEX, MYS + OECD ortancası; her ülke için Türkiye yılından en çok 3 yıl eski son değer. z > 0: Türkiye daha kötü. PISA'da OECD satırı ortanca değil OECD ortalaması (OECD yalnız ortalamayı yayımlıyor). WVS'de OECD değeri yok.*

## 4. Sıralama ne kadar sağlam?

### 4.1 Monte Carlo (10.000 senaryo)

{{TABLO_DUYARLILIK}}

![İlk 5 olasılığı](cikti/ilk5_olasiligi_v0.1.png)

- **Tüm sıralama:** taban sıralamayla Kendall tau ortancası {{TAU_ORTANCA}}, en kötü %5'lik dilimde {{TAU_P05}}. Yani genel sıra orta düzeyde oynak, ama tepe sabit.
- **Oynaklık nereden geliyor?** Yalnız matris puanları oynatılınca tau {{TAU_MATRIS}}; yalnız ağırlık, açık yöntemi, etki ve toplama türü oynatılınca {{TAU_AGIRLIK}}. **Ağırlık ve yöntem seçimleri, matris puanlarından daha fazla oynaklık yaratıyor.**
- **Sabit olanlar:** S09, S06, S07 (ilk 5 olasılığı ≥ %99). S12 %87 ile "sağlam".
- **Oynak olan:** 5. sıra. S01 (%48) ve S21 (%31) "sınırda". S08 (%16) ve S13 (%13) arada bir giriyor.
- **S21 neden oynak?** Yalnız matris oynatılınca ilk 5 olasılığı düşük; ağırlık ve yöntem oynatılınca yükseliyor. Çünkü S21 kök değil (sonuç grubunda) ama açığı en büyük sorunlardan (A = 1,00). Açığa ağırlık veren senaryolarda üste çıkıyor.

### 4.2 Tek bağlantı testi

{{BE_N}} güçlü bağlantının her biri tek tek sıfırlandı. İlk 5'in değiştiği bağlantı sayısı: **{{BE_DEGISEN}}**. En düşük Kendall tau: {{BE_MIN_TAU}}. **İlk 5 kümesi hiçbir tek silmede değişmiyor.** Ama sıralama içinde bir istisna önemli: **S09→S07 silinirse 1. ve 2. yer değişiyor** (S06 1., S09 2.). Monte Carlo'da da S09'un 1. olma olasılığı %76, S06'nın %23. Sezon 1 kararı büyük ölçüde bu tek bağa dayanıyor (`cikti/baglanti_etkisi_v0.1.csv`, `01-berke-sorular.md` B1).

**Liste bağımlılığı:** her sorun sırayla listeden çıkarılıp kalanlar yeniden sıralandı. Çıkarılan sorunun kendisi dışında ilk 5 kümesi yalnız bir durumda değişiyor: S09 çıkarılınca S21 ilk 5'e giriyor (`cikti/liste_bagimliligi_v0.1.csv`).

### 4.3 Senaryolar

{{TABLO_SENARYO}}

Okuma:

- **İlk 2 (S09, S06) 18 senaryonun hepsinde aynı.**
- **S07 bir senaryo dışında hep 3.** İstisna önemli: yalnız kaynaklı 3-4'lük bağlantılar bırakılınca S07 8. sıraya düşüyor. S07'nin yüksek sırası çoğunlukla kaynaksız 2 puanlık yargılardan geliyor (S07'den çıkan 9 tane 2'lik bağ). Uzman paneli bu hücrelere özellikle bakmalı.
- **"Önce eğitim" karşı tezi** (Glaeser vd. 2004) matrise eklenince S01 4. sıraya çıkıyor, ilk 3 değişmiyor.
- **Aday madde S12 çıkarılınca** S01 4. sıraya çıkıyor, S21 ilk 5'e giriyor.
- **Denetim önerileri birlikte uygulanınca** (5 puan düşürme + 5 eksik bağ, B9-B10) ilk 3 değişmiyor; S01 ile S12 yer değiştiriyor.
- **v0.2 riski:** S23 sonuç göstergesine taşınır ve S12 çıkarsa **S08 4. sıraya çıkıyor**, oysa S08'in açık verisi yok ve ona gelen bağlantı yok (B6). Bu karardan önce S08 çözülmeli.

### 4.4 Katmanlı harita (ISM)

Taban eşikte (ortalama + 1,5 ss) katmanlar, en derinden en üste: {{ISM_KATMAN}}.

{{TABLO_ISM}}

ISM eşiğe çok duyarlı. Bu yüzden sıralamaya girmiyor. Ama eşikler arasında tutarlı bir şey var: **en derin katman hep kurumlar sütunundan** (S06, S12, S09).

## 5. Karşı-kontrol: uluslararası kurumlar ve literatür ne diyor?

| Kaynak | Öne çıkardığı öncelikler | Bizim sıralamada |
|---|---|---|
| **OECD Economic Surveys: Türkiye 2025** (Nisan 2025) | Dezenflasyon ve ihtiyatlı makro politika; vergi tabanı ve sosyal yardım; kadınların işgücüne katılımı (okul öncesi bakım); beceri, yenilik ve düzenleme yoluyla verimlilik; karbon fiyatlama | S21: 6 · S10: 16 · S04: 13 · S01: 5, S02: 12, S23: 23 (sonuç) · S18: 10 |
| **Dünya Bankası, Türkiye CEM: Jobs for Prosperity** (Eylül 2025) | Fiyat istikrarı; iş ortamı ve rekabet; işgücü piyasası reformu (vergi kaması, kıdem); beceri uyumsuzluğu; kadın istihdamı | S21: 6 · S06/S09: 1-2 (kısmen) · S10: 16 · S02: 12 · S04: 13 |
| **IMF 2025 Article IV** (Ülke Raporu 26/43, Şubat 2026) | Dezenflasyon ve mali sıkılaştırma; yapısal: verimlilik, beceri, KOBİ'ler, **hukuki ve yönetişim çerçeveleri**, dış şoklara kırılganlık | S21: 6 · S01: 5 · **S06/S09: 1-2** · S22: 22 |
| **Literatür:** Acemoglu & Üçer (2015); Dünya Bankası (2014) *Turkey's Transitions* | Türkiye'de büyüme yavaşlamasını kurumsal kalitedeki gerilemeyle açıklıyor; "kurumlar" üç ana geçişten biri | S06, S09 ilk 2 |

*İlk üç satır yayınların özetlerinden derlendi; tam metinler video çekiminden önce okunmalı ve bu tablo güncellenmeli.*

### Nerede örtüşüyor?

- **Kurumlar.** IMF'nin "hukuki ve yönetişim çerçeveleri", Dünya Bankası'nın "iş ortamı ve rekabet" başlığı ve Türkiye'ye özgü literatür, bizim ilk 2'mizle aynı yönü gösteriyor.
- **Eğitim ve beceri.** Üç kurum da beceriyi yapısal öncelik sayıyor. S01 bizde sınırda 5. Kadın istihdamı ve işgücü piyasasını OECD ve Dünya Bankası öne çıkarıyor, IMF özetinde yok.
- **Enflasyon.** Üç kurumda da ilk sırada. Bizde 6. ve sonuç grubunda. Ama açığı en büyük sorun (A = 1,00).

### Nerede ayrışıyor ve neden?

1. **Enflasyon (S21) bizde neden 1 değil?** Kurumlar *acil* olanı söylüyor, biz *kök* olanı arıyoruz. Matrise göre kronik enflasyon büyük ölçüde başka sorunlardan besleniyor: politika sürekliliği (S07), enerji bağımlılığı (S18) ve dış finansman (S22). Bu iki cevap çelişmiyor. Evinizde yangın varsa önce yangını söndürürsünüz, sonra kablolamaya bakarsınız. **Bu sıralama "enflasyonla mücadele beklesin" demek değil.**
2. **İşgücü piyasası (S02, S04, S10) bizde düşük.** Kurumlar bunları öne çıkarıyor çünkü uygulanabilir, ölçülebilir ve getirisi hesaplanabilir kaldıraçlar. Bizim yöntemimizde **"çözülebilirlik" diye bir boyut yok.** Bu, yöntemin gerçek bir boşluğu. Sıralama "nereden başlamalı?" sorusunu yapısal açıdan cevaplıyor, "en hızlı nerede sonuç alınır?" sorusunu cevaplamıyor.
3. **Kurumlar raporlarında daha az öne çıkıyor.** Uluslararası kurumlar üye hükümetlere yönelik yazıyor ve yönetişim konularını genellikle "çerçeve" gibi genel başlıklarla ele alıyor. Bizim ilk 3'ümüz tam da bu başlıklar. Bu, bizim yöntemimizin farklı bir soruyu sorduğunu da, kurumlar literatürüne yaslanan matrisimizin bir yanlılığını da gösteriyor olabilir. İkisini ayırmanın yolu uzman paneli.

## 6. Yorum

### 6.1 Neden grubunun tepesi: devletin kapasitesi ve kuralların güvenilirliği

- **S09 Kamuda liyakat ve kurumsal kapasite (1.)** Matriste en çok sorunu doğrudan besleyen madde (14 sorun, 4'ü güçlü). Toplam etkisinin en büyük olduğu yerler: verimlilik (S23), plan-uygulama (S07), afet kayıpları (S17), toplumsal güven (S11). Kısacası: *"Doğru planı yapsanız bile, uygulayacak kurumsal kapasite yoksa plan kâğıtta kalır."*
- **S06 Hukukun üstünlüğü ve yargı (2.)** Neredeyse hiçbir sorundan beslenmiyor (R = 0,10), 12 sorunu besliyor. Etkisinin en büyük olduğu yerler: verimlilik (S23), kayıt dışılık (S10), güven (S11), dış finansman (S22).
- **S07 Plan-uygulama kopukluğu (3.)** Hem veren hem alan. Onu en çok besleyen S09. Kendisi en çok enflasyonu (S21), verimliliği ve dış finansmanı etkiliyor.
- **S12 Medya ve bilgi ekosistemi (4., aday).** Liyakati (S09, basın özgürlüğü–yolsuzluk bağı) ve hesap verebilirliği besliyor.
- **S01 Eğitimin niteliği (5., sınırda).** Beceri (S02), Ar-Ge (S15) ve verimlilik (S23) üzerinden etkili. Açığı orta düzeyde (PISA 2022: Türkiye 461,7; set ortancası 477,5).

### 6.2 Sonuç grubu ne anlama geliyor?

Enflasyon, dış finansman, verimlilik, kayıt dışılık, güven, afet kayıpları, plansız kentleşme, beyin göçü. Bunlar **acının hissedildiği yerler.** Gündemde en çok konuşulan sorunların çoğu bu grupta.

Sonuç grubunda olmak "önemsiz" demek değil. İki anlamı var:

1. Bu sorunlar tek başına ele alınırsa tekrar etme eğiliminde. Boyayı yeniden boyamak gibi.
2. Kalıcı çözüm, onları besleyen kök sorunlarla birlikte tasarlanmalı.

**Özel not, S17 Deprem ve afet riski:** sonuç grubunda (onu en çok besleyenler plansız kentleşme ve kamu kapasitesi). Bu, **deprem hazırlığının bekleyebileceği anlamına gelmez.** Hayati risklerde aciliyet ayrı bir ölçüdür. Sıralama yalnız "kök nerede?" sorusunu cevaplıyor.

### 6.3 Sürprizler ve beklentiyle çelişenler

| # | Beklenti | Sonuç | Neden |
|---|---|---|---|
| 1 | Sezon 1 = plan-uygulama kopukluğu (S07) | S07 3. S09 onu besliyor | Planların kâğıtta kalmasının arkasında uygulama kapasitesi var (S09 → S07 = 4) |
| 2 | Enflasyon en tepede | 6., sonuç grubunda | Enflasyonu besleyen üç güçlü bağ var: S07, S18, S22 |
| 3 | "Düşük tasarruf" kronik sorun | Güncel veride Türkiye'nin tasarruf oranı setin üstünde | V2 tanımı gözden geçirilmeli (`01-berke-sorular.md` C1) |
| 4 | Enerji bağımlılığı büyük açık | Setin yalnız biraz üstünde | Karşılaştırma setindeki ülkelerin çoğu da enerji ithalatçısı |
| 5 | Tarım bir "sonuç" sorunu | Neden grubunda | Su stresi ve kayıt dışılık üzerinden (ikincisi tartışmalı, B3) |
| 6 | Aday madde medya geride kalır | 4. ve sağlam | Liyakat ve hesap verebilirliğe güçlü bağ + WGI söz hakkında büyük açık |

## 7. Zayıf noktalar (özet)

1. **Matris tek elden.** 120 yargı hücresi taslak yazarına ait. S07'nin sırası bu hücrelere duyarlı.
2. **Kaynak yanlılığı riski.** Kurumlar literatürü baskın. Karşı tez senaryosu sonucu değiştirmedi, ama uzman paneli farklı kaynaklarla gelebilir.
3. **Açık skorları yalnız ikincil ölçütle (ülke seti) hesaplandı; birincil ölçüt (plan hedefleri) eksik. 6 sorunda veri yok, 3 sorunda vekil gösterge.** Ayrıca: v0.1 verisinde OECD ortancası Türkiye dahil hesaplandı (V2 kodu düzeltildi, yeniden çekimde değişecek); 2025 ILO değerleri modellenmiş tahmin; WGI için 2024 verisi yayımlanmışken 2023 kullanıldı; karşılaştırma seti bütün sorunlarda aynı (kod artık sorun başına set destekliyor, `karsilastirma_seti` sütunu).
4. **Çözülebilirlik boyutu yok.** Kurumların öne çıkardığı işgücü piyasası kaldıraçları bu yüzden düşük kalıyor.
5. **Doğrusal ve statik.** Döngüler (S21 ↔ S22) ve eşik etkileri modellenmiyor.
6. **İlk 3'ün hepsi yönetişim.** Yöntemsel olarak sorun değil, iletişimsel olarak risk.

## Kaynakça (bu dosyada ek olarak kullanılanlar)

- Acemoglu, D. & Üçer, M. (2015). The Ups and Downs of Turkish Growth, 2002–2015: Political Dynamics, the European Union and the Institutional Slide. NBER Working Paper No. 21608.
- Glaeser, E.L., La Porta, R., Lopez-de-Silanes, F. & Shleifer, A. (2004). Do Institutions Cause Growth? *Journal of Economic Growth* 9(3):271–303. doi:10.1023/B:JOEG.0000038933.16398.ed
- IMF (2026). *Republic of Türkiye: 2025 Article IV Consultation*. IMF Country Report No. 26/43. https://www.imf.org/en/publications/cr/issues/2026/02/13/republic-of-trkiye-2025-article-iv-consultation-press-release-staff-report-and-statement-573962
- OECD (2025). *OECD Economic Surveys: Türkiye 2025*. https://www.oecd.org/en/publications/oecd-economic-surveys-turkiye-2025_d01c660f-en.html
- OECD (2023). *PISA 2022 Results (Volume I)*, Tablo I.1.
- Integrated Values Surveys (2024), Our World in Data üzerinden: "Share of people agreeing with the statement 'most people can be trusted'". https://ourworldindata.org/grapher/self-reported-trust-attitudes
- World Bank (2025). *Türkiye Country Economic Memorandum: Jobs for Prosperity*. https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099091725075068918
- World Bank (2014). *Turkey's Transitions: Integration, Inclusion, Institutions*. Report No. 90509-TR.
- World Bank, Worldwide Governance Indicators (2024 sürümü, 2023 verisi), API kodları GOV_WGI_*.EST.
- Matris gerekçelerinin tam kaynakçası: `veri/kaynakca.csv`.
