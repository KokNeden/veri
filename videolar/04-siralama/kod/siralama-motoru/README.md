# kokneden-siralama

Kök Neden'in sorun sıralama yöntemi: **DEMATEL + ISM + açık/etki skorları + Monte Carlo duyarlılık analizi.**
Yöntemin tam anlatımı: [kokneden.org/yontem/siralama](https://kokneden.org) · `04-siralama-yontemi/01-yontem.md`

> Matematik öznelliği ortadan kaldırmaz, görünür kılar. Bu depo o görünürlüğün aracı.

## Kurulum

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q          # 19 test
python ornekler/oyuncak.py   # 4 ve 6 düğümlü örnekler → ornekler/cikti/
```

## Kullanım

```bash
python -m kokneden_siralama.calistir --girdi GIRDI/ --cikti CIKTI/ --n 10000 --etiket v0.1
```

`GIRDI/` klasöründe beklenen dosyalar:

| Dosya | İçerik |
|---|---|
| `sorunlar.csv` | `sorun_id, ad, kisa_ad, sutun, ana_gosterge, yedek_gosterge, etki_duzey, etki_gerekce` |
| `etki_matrisi.csv` | İlk sütun `etkileyen`, diğer sütunlar sorun kimlikleri; hücre (i, j) = i'nin j'ye doğrudan etkisi, 0-4 |
| `baglanti_gerekceleri.csv` | `kaynak, hedef, puan, durum, gerekce, kaynakca, doi_url`; `durum` ∈ {guclu, zayif, tartismali, yargi} |
| `gostergeler.csv` | `ulke, gosterge_id, yil, deger` (uzun format) |
| `gosterge_listesi.csv` | `gosterge_id, yon` (1: yüksek iyi, −1: yüksek kötü, 0: normatif değil) |
| `plan_hedefleri.csv` | *(isteğe bağlı, birincil açık ölçütü)* `sorun_id, plan, gosterge, baslangic_yil, baslangic, hedef_yil, hedef, gerceklesen_yil, gerceklesen, kaynak` |

Çıktılar: `sonuclar_*.csv`, `duyarlilik_*.csv`, `acik_skorlari_*.csv`, `toplam_etki_*.csv`, `baglanti_etkisi_*.csv`, `meta_*.json`, `neden_sonuc_haritasi_*.png`, `ilk5_olasiligi_*.png`.

Python'dan:

```python
from kokneden_siralama import dematel, kok_skoru, oncelik, sirala
d = dematel(A)                 # A: n×n, 0-4
K = kok_skoru(d, lam=0.5)      # λ·ñ(D−R) + (1−λ)·ñ(D)
P = oncelik(K, A_skor, E_skor) # K^0.5 · A^0.25 · E^0.25
sira = sirala(P)
```

Uzman matrislerini birleştirmek için: `kokneden_siralama.birlestir.birlestir(liste)` → ortanca, IQR, puan sayısı, tartışmalı maske.

## Yapı

```
kokneden_siralama/
  dematel.py      normalizasyon, T = X(I−X)⁻¹, D, R, kök skoru, eşik
  ism.py          erişim matrisi, katmanlar (Warfield 1974)
  skorlar.py      açık skoru (sağlam z → Φ; yüzdelik), etki skoru
  oncelik.py      ağırlıklı geometrik / aritmetik öncelik, sıralama
  duyarlilik.py   Monte Carlo, bağlantı sıfırlama testi
  birlestir.py    uzman matrislerini birleştirme, uyum
  harita.py       neden-sonuç haritası, ilk-k grafiği
  calistir.py     uçtan uca akış (CLI)
ornekler/oyuncak.py   rutubetli ev (4) ve yolu olmayan kasaba (6)
sablon_uret.py        uzman formu (CSV + XLSX)
tests/                birim testleri
```

## Önerilen GitHub deposu

- **Ad:** `kokneden/kokneden-siralama` (ayrı depo; içerik deposu `kokneden/kokneden-veri` ayrı tutulur)
- **Sürümleme:** kod için anlamsal sürüm (`0.1.0`); matris ve sonuçlar için veri sürümü (`v0.1`, `v0.2`...). Her sonuç dosyası hangi kod sürümüyle üretildiğini `meta_*.json` içinde taşır.
- **CI:** her PR'da `pytest` + oyuncak örnek; `main`'e birleşen her matris değişikliğinde sonuçlar yeniden üretilir ve farkı (hangi sorunun sırası değişti) PR yorumuna yazılır.
- **Katkı:** matris değişikliği önerisi = `baglanti_gerekceleri.csv` üzerinde PR ya da sitedeki itiraz formu. Kod katkısı için test zorunlu.
- **Lisans önerisi:** kod **MIT** (bu klasördeki `LICENSE`); veri, matris ve metinler **CC BY 4.0** (atıf şartıyla serbest kullanım). Gerekçe: en yaygın ve en az sürtünmeli kombinasyon; akademik yeniden kullanımı kolaylaştırır.

## Sınırlılıklar

Etkiler doğrusal ve sabit varsayılıyor. Sıralama bir *yapısal konum* ölçüsü, dinamik bir model değil. Tüm ayrıntı: `04-siralama-yontemi/01-yontem.md` §1 ve §4.
