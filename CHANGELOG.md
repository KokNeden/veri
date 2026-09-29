# Değişiklik günlüğü

Her değişiklik burada. Biçim: tarih ve etiket başlığı, altında video klasörü başına bir satır. Veri düzeltmeleri ayrıca [DUZELTMELER.md](DUZELTMELER.md)'de.

## 29.09.2026 · 05-v1.0

- `05-kurallar-tarih`: ilk sürüm. Veri (V-Dem hukukun üstünlüğü ve tarafsız kamu yönetimi 1923–2025, mahkeme dava yükü 1967–2010, hâkim kurulu yapıları, AİHM kararları), sözlük ve kod.
- `01`–`04` README: sitenin henüz yayında olmayan sayfalarına göreli bağlantılar metne çevrildi (GitHub'da kırılıyordu).

## 28.09.2026 · durum notları

- `01`–`04` README: "Nasıl yapıldı" araç beyanı ve "Uzman okuması: henüz yok" durum notları eklendi (sitedeki sayfalarla aynı); henüz yayında olmayan site sayfalarına bağlantı kaldırıldı.

## 28.09.2026 · atıf

- `CITATION.cff` eklendi: GitHub'daki "Cite this repository" düğmesi APA ve BibTeX üretir. Atıf biçimleri README'de.

## 28.09.2026 · 03-v1.3

- `03-kronik-sorunlar`: `veri/plan-hedef-gerceklesme.csv` 169 hedef; planların bütün sayısal hedefleri tarandı. Eklenen: XI. Plan kadın istihdam oranı (%34 hedef, %31,3 gerçekleşme; yakın ölçü, TÜİK 2021 seri revizyonu). Çıkarılan: XI. Plan gezici kütüphane (2023 değeri sayım tarihine göre değişiyor, sonuç tersine dönüyor; gerekçe `kod/analiz/plan_gerceklesme.py` → ARASTIRMA_DISI). `veri/sozluk.json` kayıt sayısı.

## 28.09.2026 · 03-v1.2

- `03-kronik-sorunlar`: `veri/plan-hedef-gerceklesme.csv`'ye `nitelik` sütunu eklendi (hedef / tahmin). 13 kayıt planın hedefi değil tahmini, beklentisi ya da ihtiyaç tespiti; bu satırlarda fark öngörünün isabetini gösterir, "hedef tuttu/tutmadı" diye okunmaz. VIII–XI. Plan Ar-Ge/GSYH satırları `yakin_olcu`ya alındı (WDI serisi revize TÜİK değerlerini veriyor; sonuç değişmiyor). `veri/sozluk.json`: `nitelik` açıklaması.

## 28.09.2026 · 03-v1.1

- `03-kronik-sorunlar`: `veri/plan-hedef-gerceklesme.csv` 154 → 168 hedef (gerçekleşmesi bulunan plan hedefleri; 03-v1.0'da 154, araştırmanın başında 64). Son tur: medya, bölgesel, yerel yönetim, afet ve küçük sorunlar. `kod/analiz/plan_gerceklesme.py`: eşleştirme tam eşleşmeyi tercih ediyor; araştırma dışı bırakılan 29 hedef gerekçeleriyle kodda.

## 28.09.2026 · 01-v1.0 · 02-v1.0 · 03-v1.0 · 04-v1.0

- `01-manifesto`: 3 dosya eklendi.
- `02-kapsam`: 5 dosya eklendi.
- `03-kronik-sorunlar`: 19 dosya eklendi.
- `04-siralama`: 43 dosya eklendi.

## 28.09.2026 · kurulum

- Depo kuruldu: README, lisanslar (veri CC BY 4.0, kod MIT), düzeltme bildirimi şablonu.
