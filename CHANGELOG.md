# Değişiklik günlüğü

Her değişiklik burada. Biçim: tarih ve etiket başlığı, altında video klasörü başına bir satır. Veri düzeltmeleri ayrıca [DUZELTMELER.md](DUZELTMELER.md)'de.

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
