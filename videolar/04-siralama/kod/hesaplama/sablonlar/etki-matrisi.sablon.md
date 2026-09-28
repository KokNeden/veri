# Etki Matrisi v0.1

*Kök Neden taslağı v0.1 · 21 Eylül 2026 · Uzman paneli tarafından güncellenecek*

Bu tablo sıralamanın tek girdisi. Her hücre şu sorunun cevabı: **"Satırdaki sorun kendiliğinden düzelseydi, sütundaki sorun ne kadar düzelirdi?"** (0: yok · 1: zayıf · 2: orta · 3: güçlü · 4: çok güçlü)

- **149** dolu hücre · **28** güçlü (3-4) · her güçlü bağlantının en az bir kaynağı var
- Güçlülerin **4**'ü tartışmalı, **2**'si gerekçesi zayıf · **120** taslak yargı (1-2 puan; kaynak zorunlu değil)
- Hücreye tıklayın: gerekçe, kaynak ve "itiraz et" düğmesi açılır.

[İnteraktif tablo buraya gelir — bkz. şartname aşağıda. JavaScript olmadan okunabilen statik sürüm:]

{{TABLO_MATRIS}}

*Satır = etkileyen, sütun = etkilenen. ◆ tartışmalı, ○ gerekçesi zayıf. Sütun kodları: {{SORUN_KODLARI}}*

İndir: [etki_matrisi_v0.1.csv](veri/etki_matrisi_v0.1.csv) · [baglanti_gerekceleri.csv](veri/baglanti_gerekceleri.csv) · [kaynakca.csv](veri/kaynakca.csv)

---

## Şartname: interaktif etki matrisi sayfası

### Amaç

Ziyaretçi 23 × 23 matrisin tamamını görür. Herhangi bir hücreye tıklayınca o bağlantının puanını, durumunu, gerekçesini ve kaynağını okur. İsterse o hücreye itiraz eder.

### Veri

- `etki_matrisi_v0.1.csv`: satır = etkileyen, sütun = etkilenen.
- `baglanti_gerekceleri.csv`: `baglanti_id, kaynak, hedef, puan, durum, anahtar, gerekce, kaynakca, doi_url, surum`.
- `sorunlar.csv`: `sorun_id, sutun, ad, kisa_ad`.
- Sayfa derleme sırasında üç dosyayı tek bir JSON'a çevirir (`matris_v0.1.json`). Çalışma anında sunucu çağrısı yok.

### Düzen

**Masaüstü (≥ 1024 px)**

- Solda matris ısı haritası. Hücre rengi puana göre (0 boş, 1-4 açıktan koyuya tek renk skalası). Satır ve sütun başlıkları kısa adla, sütunlar (insan, kurumlar…) renkli bantla gruplanır. Başlıklar kaydırmada sabit kalır.
- Sağda **ayrıntı paneli** (genişlik ~360 px). Varsayılan: seçim yoksa kısa kullanım notu.
- Durum işaretleri hücrede küçük simgeyle: tartışmalı (◆), gerekçesi zayıf (○). Renk tek başına anlam taşımaz.

**Mobil (< 1024 px)**

- Matris yerine **satır görünümü**: önce sorun seçilir ("Hangi sorunun etkilerini görmek istiyorsunuz?"). Ardından o sorunun verdiği ve aldığı bağlantılar iki liste halinde, puana göre sıralı. Liste öğesine dokununca ayrıntı alttan açılan panelde.
- Tam matris "Tabloyu göster" düğmesiyle yatay kaydırmalı olarak açılabilir.

### Ayrıntı paneli (hücre seçilince)

```
S16 Plansız kentleşme  →  S17 Deprem ve afet riski yönetimi
Puan: 4 (çok güçlü)          Durum: güçlü (kaynaklı)
Gerekçe: Ruhsatsız ve denetimsiz yapı stoku deprem kayıplarının ana nedeni.
Kaynaklar:
  • Güneş, O. (2015). Turkey's grand challenge… Case Studies in Construction Materials 2:18–34. [DOI]
  • Ambraseys, N. & Bilham, R. (2011). Corruption kills. Nature 469:153–155. [DOI]
  • SBB (2023). 2023 Kahramanmaraş ve Hatay Depremleri Raporu.
Toplam etki (doğrudan + dolaylı): 0,10   ·   Bu bağlantı silinirse ilk 5: değişmiyor
Ters yön (S17 → S16): 1
[ Bu bağlantıya itiraz et ]   [ Bağlantıyı paylaş ]
```

- "Toplam etki" `toplam_etki_v0.1.csv`'den; "silinirse ilk 5" `baglanti_etkisi_v0.1.csv`'den (yalnız 3-4 puanlılarda).
- Boş hücrede: "Bu iki sorun arasında doğrudan etki öngörmedik (0). Katılmıyorsanız → itiraz et."
- "İtiraz et" düğmesi itiraz formunu `kaynak`, `hedef`, `mevcut_puan` alanları dolu olarak açar.
- "Paylaş": URL `…/matris?h=S16-S17` hücreyi seçili açar.

### Filtreler ve görünümler (üst çubuk)

- **Durum filtresi:** tümü / yalnız güçlü / tartışmalı + zayıf / yalnız yargı.
- **Sütun filtresi:** tek bir sütunun (ör. kurumlar) satır ve sütunlarını vurgula.
- **Görünüm:** doğrudan (A) / toplam etki (T). T görünümünde renk skalası T değerine göre, hücrede iki ondalık.
- **Arama:** sorun adı ya da kaynak yazarı ("Acemoglu" → o kaynağı kullanan bağlantılar vurgulanır).
- **Sürüm seçici:** v0.1 / v0.2… Seçilen iki sürüm arasında **fark görünümü**: değişen hücreler çerçeveli, üzerine gelince "2 → 3" gösterilir.

### Erişilebilirlik ve performans

- Klavye: ok tuşlarıyla hücre gezme, Enter ile ayrıntı. Ekran okuyucu için her hücrenin `aria-label`'ı: "Plansız kentleşme, deprem riskini etkiler, puan 4, güçlü".
- 529 hücre SVG ya da CSS grid ile; sanal kaydırma gerekmiyor.
- JSON boyutu < 150 KB. İlk açılış < 1 sn (orta seviye mobil).

### Kabul testleri

1. Her 3-4 puanlı hücrede en az bir kaynak görünüyor (yoksa derleme hata verir).
2. Matristeki puanlar ile gerekçe dosyasındaki puanlar birebir aynı (derleme kontrolü).
3. `?h=S09-S07` bağlantısı doğrudan o hücreyi açıyor.
4. Mobilde satır görünümünde S09 seçilince 14 giden bağlantı listeleniyor.
