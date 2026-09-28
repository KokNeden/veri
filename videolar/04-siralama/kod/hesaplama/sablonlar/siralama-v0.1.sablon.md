# Sıralama v0.1

*Ön sonuç · 21 Eylül 2026 · [Yöntem](https://kokneden.org/yontem/siralama) · [Etki matrisi](etki-matrisi.md) · [Yol haritası](yol-haritasi.md) · [Bu sıralamaya itiraz et](https://kokneden.org/itiraz) · [Değişiklik günlüğü](degisiklik-gunlugu.md)*

> **Bu bir ön sonuç.** Etki matrisinin ilk taslağı Kök Neden tarafından hazırlandı ve henüz uzman panelinden geçmedi. Açık skorları bu sürümde yalnız ikincil ölçütle (benzer ülkeler) hesaplandı; birincil ölçütümüz olan Türkiye'nin kendi plan hedefleri bir sonraki sürümde eklenecek. Sıralama, panelin ilk turundan sonra v0.2 olarak güncellenecek.

## Kısaca

- **Kök nedenlerin en üstünde:** kamuda liyakat ve kurumsal kapasite, hukukun üstünlüğü ve yargı, plan-uygulama kopukluğu. Üçü de 10.000 senaryonun %99'undan fazlasında ilk 5'te.
- **Sonuç grubunda:** enflasyon, verimlilik, dış finansman, kayıt dışılık, toplumsal güven, afet kayıpları. Gündemde en çok konuşulan sorunların çoğu burada.
- **Sınırda:** 5. sıra. Eğitimin niteliği (%48) ve enflasyon (%31).
- **Sezon 1:** Kamuda liyakat ve kurumsal kapasite ([yol haritası](yol-haritasi.md)).

## Sonuç tablosu

{{TABLO_SONUC}}

*D: verdiği toplam etki · R: aldığı toplam etki · D−R > 0: neden grubu · K: kök skoru · A: açık skoru (Türkiye'nin karşılaştırma setine göre açığı; "bilmiyoruz" = veri yok, 0,5 alındı) · E: etki alanı · Öncelik = K^0,5 · A^0,25 · E^0,25 · İlk 5 olasılığı: 10.000 senaryoda.*

## Neden-sonuç haritası

![Neden-sonuç haritası v0.1](neden_sonuc_haritasi_v0.1.png)

Yatay eksen toplam önemi (verdiği + aldığı etki), dikey eksen rolü gösterir. Sıfır çizgisinin üstündekiler **neden**, altındakiler **sonuç** grubunda. Oklar en güçlü 30 dolaylı + doğrudan etkiyi gösterir.

## Sıralama ne kadar sağlam?

{{TABLO_DUYARLILIK}}

![İlk 5'te kalma olasılığı](ilk5_olasiligi_v0.1.png)

- 10.000 senaryoda matris puanları, ağırlıklar, açık ve etki skorları ve hesap türü aynı anda rastgele değiştirildi.
- İlk 3'ün ilk 5'teki yeri sabit. 5. sıra oynak.
- 28 güçlü bağlantının her biri tek tek silindi: **hiçbiri ilk 5 kümesini değiştirmedi.** Ama kamuda liyakat → plan-uygulama bağı silinirse ilk iki yer değişiyor (hukuk ve yargı 1. oluyor).
- **Zayıf nokta:** Yalnız kaynaklı güçlü bağlantılarla hesaplanınca plan-uygulama kopukluğu 8. sıraya düşüyor. Bu maddenin yüksek sırası büyük ölçüde kaynaksız orta düzey yargılara dayanıyor.
- Tüm senaryolar: [senaryolar_v0.1.csv](veri/senaryolar_v0.1.csv).

## Yorum

**Neden grubunun tepesinde devletin kapasitesi ve kuralların güvenilirliği var.** Kamuda liyakat en çok verimliliği, plan-uygulamayı, afet kayıplarını ve güveni besliyor. Hukuk ve yargı en çok verimliliği, kayıt dışılığı ve güveni besliyor. Plan-uygulama kopukluğu hem veren hem alan: onu en çok kamu kapasitesi besliyor.

**Sonuç grubunda olmak önemsiz olmak demek değil.** Bu sorunlar tek başına ele alındığında tekrar etme eğiliminde. Kalıcı çözüm onları besleyen kök sorunlarla birlikte tasarlanmalı. **Deprem ve afet riski sonuç grubunda, ama bu deprem hazırlığının bekleyebileceği anlamına gelmez.** Hayati risklerde aciliyet ayrı bir ölçüdür.

**Uluslararası kurumlarla karşılaştırma.** OECD, Dünya Bankası ve IMF'nin son Türkiye raporları dezenflasyonu ilk sıraya koyuyor. OECD ve Dünya Bankası ardından beceri, kadın istihdamı ve işgücü piyasasını; IMF verimlilik, beceri, KOBİ'ler ve hukuki-yönetişim çerçevelerini öne çıkarıyor. Fark şuradan geliyor: kurumlar *acil ve uygulanabilir* olanı soruyor, biz *kök* olanı. Yöntemimizde "çözülebilirlik" boyutu yok. Bu bilinen bir sınırlılık.

**Sürprizler.** (1) Beklentimiz Sezon 1'in plan-uygulama kopukluğu olmasıydı; sonuç onun bir üst basamağını, kamu kapasitesini gösterdi. (2) "Düşük tasarruf" iddiamız güncel veriyle tutmuyor; madde "dış finansman bağımlılığı" olarak yeniden tanımlanacak. (3) Aday madde "medya ve bilgi ekosistemi" 4. sırada ve sağlam; kronik testini geçene kadar sezon açmıyor.

## Veri dosyaları

| Dosya | İçerik |
|---|---|
| [etki_matrisi_v0.1.csv](veri/etki_matrisi_v0.1.csv) | 23 × 23 doğrudan etki matrisi (0-4) |
| [baglanti_gerekceleri.csv](veri/baglanti_gerekceleri.csv) | 149 bağlantının puanı, durumu, gerekçesi, kaynağı |
| [sonuclar_v0.1.csv](veri/sonuclar_v0.1.csv) | D, R, D±R, K, A, E, öncelik, sıra, ISM katmanı |
| [duyarlilik_v0.1.csv](veri/duyarlilik_v0.1.csv) | Sıra aralığı, ilk 5 / 1. olma / neden grubunda olma olasılığı |
| [acik_skorlari_v0.1.csv](veri/acik_skorlari_v0.1.csv) | Her sorunun göstergesi, yılı, Türkiye değeri, set ortancası, z, A |
| [senaryolar_v0.1.csv](veri/senaryolar_v0.1.csv) | 18 senaryonun ilk 5'i |
| [liste_bagimliligi_v0.1.csv](veri/liste_bagimliligi_v0.1.csv) | Her sorun çıkarılınca ilk 5 |
| [kaynakca.csv](veri/kaynakca.csv) | Tüm kaynaklar, DOI/URL |

Lisans: CC BY 4.0. Kod: github.com/kokneden/kokneden-siralama (MIT). Aynı sonuçları tek komutla üretebilirsiniz.

*İlk taslak, Berk Can tarafından yapay zekâ destekli bir literatür taramasıyla hazırlandı. (⚠️ Berk onayı bekliyor)*
