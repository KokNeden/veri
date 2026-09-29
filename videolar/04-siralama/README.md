# 04 · Türkiye'nin 24 kronik sorunundan hangisi kök neden? İlk sıralama

Video ve sayfası yakında yayında. · Sürüm: v1.0 (sıralama v0.2) · Güncelleme: 27 Eylül 2026

## Özet

Türkiye'nin 24 kronik sorununu aynı anda konuşamayız; nereden başlayacağımızı seçmek zorundayız. Bu videoda sezgi yerine bir yöntem kullanıyoruz: DEMATEL. Her sorun çiftine "bu sorun düzelseydi, şu sorun ne kadar düzelirdi?" diye sorup puan veriyor, dolaylı etkileri de hesaba katarak hangi sorunların "neden", hangilerinin "sonuç" olduğunu çıkarıyoruz. Kök olmanın yanına iki ölçü daha ekliyoruz: Türkiye'nin kendi plan hedeflerine göre açık ve sorunun etki alanı.

Sıralamanın ilk dördü hukuk ve yargı, kurallı ve tarafsız kamu yönetimi, medya ve kutuplaşma; on bin senaryonun yüzde 96'sından fazlasında ilk beşte kalıyorlar. Beşinci sıra (plan-uygulama kopukluğu) sınırda. Enflasyon, dış finansman ve kayıt dışılık "sonuç" grubunda. İlk sezonun konusu Kurallar ve kurumlar. Bu bir ön sonuç (sürüm 0.2): matrisin ilk taslağı yapay zekâ desteğiyle hazırlandı, her bağlantı gerekçesi ve kaynağıyla bu sayfada.

## Veri dosyaları

- [etki-matrisi-v0.2.csv](veri/etki-matrisi-v0.2.csv): 24×24 etki matrisi (0–4).
- [baglanti-gerekceleri-v0.2.csv](veri/baglanti-gerekceleri-v0.2.csv): 162 bağlantının puanı, durumu (güçlü, zayıf, tartışmalı, yargı), gerekçesi ve kaynağı.
- [kaynakca.csv](veri/kaynakca.csv): Gerekçelerde kullanılan kaynaklar, DOI ya da bağlantıyla.
- [plan-hedefleri-v0.2.csv](veri/plan-hedefleri-v0.2.csv): Açık skorunda kullanılan 23 plan hedefi, başlangıç ve gerçekleşme.
- [sonuclar-v0.2.csv](veri/sonuclar-v0.2.csv), [duyarlilik-v0.2.csv](veri/duyarlilik-v0.2.csv), [acik-skorlari-v0.2.csv](veri/acik-skorlari-v0.2.csv), [baglanti-etkisi-v0.2.csv](veri/baglanti-etkisi-v0.2.csv), [senaryolar-v0.2.txt](veri/senaryolar-v0.2.txt): Sonuç, duyarlılık ve senaryo çıktıları.

## Kod

- [`kod/siralama-motoru/`](kod/siralama-motoru/)
- [`kod/hesaplama/`](kod/hesaplama/)

Kod, Kök Neden'in çalışma klasörü düzenine göre yazıldı; ham verileri kaynak adreslerinden kendisi indirir ya da README'sinde nereden indirileceğini söyler.

## Kaynaklar

1. Gabus, A. & Fontela, E. (1972). *World Problems, an Invitation to Further Thought within the Framework of DEMATEL*. Battelle Geneva Research Centre; Gabus & Fontela (1973), DEMATEL Report No. 1.
2. Kök Neden, *Etki matrisi v0.2* ve bağlantı gerekçeleri (24 sorun, 162 bağlantı, 21 güçlü ve kaynaklı). Kaynakça: `veri/kaynakca.csv`.
3. Kök Neden, *Sıralama yöntemi* (21.09.2026): DEMATEL, açık skoru, etki alanı, ağırlıklı geometrik ortalama, Monte Carlo duyarlılık; "sağlam / sınırda" eşikleri.
4. DPT / SBB, Beş Yıllık Kalkınma Planları I–XII: plan hedefleri (23 eşleşme, `veri/plan-hedefleri-v0.2.csv`).
5. Dünya Bankası, World Development Indicators; V-Dem v16; EM-DAT (CRED / UCLouvain).
6. Escaleras, M., Anbarci, N. & Register, C.A. (2007). Public sector corruption and major earthquakes. *Public Choice* 132:209–230; Ambraseys, N. & Bilham, R. (2011). Corruption kills. *Nature* 469:153–155.
7. McCoy, J., Rahman, T. & Somer, M. (2018). Polarization and the Global Crisis of Democracy. *American Behavioral Scientist* 62(1); Somer, M. (2019), Türkiye vaka incelemesi; Frye, T. (2002). The Perils of Polarization. *World Politics* 54(3); Azzimonti, M. (2011). Barriers to Investment in Polarized Societies. *American Economic Review* 101(5).
8. Brunetti, A. & Weder, B. (2003). A free press is bad news for corruption. *Journal of Public Economics* 87(7–8).
9. Cukierman, A., Webb, S.B. & Neyapti, B. (1992). Measuring the Independence of Central Banks and Its Effect on Policy Outcomes. *World Bank Economic Review* 6(3).

Erişim tarihi: 27.09.2026.

## Sınırlılıklar

- **Nasıl yapıldı:** Kaynak tarama, veri işleme ve görsellerin kodu yapay zekâ araçları desteğiyle yapıldı. Metindeki her iddia, yazarın notlarını görmeden, ayrı bir yapay zekâ denetimiyle ham kaynağa karşı sınandı (kaynak testi); bulguları Berk Can inceledi. Seslendirme, Berk Can'ın sesinden (ses örneği) yapay zekâyla üretildi. Uzman okuması: henüz yok. Ayrıntı: Nerede duruyoruz?
- **Puanlar yargıdır.** Matrisin ilk taslağı yapay zekâ destekli bir literatür taramasıyla hazırlandı ve Berk Can tarafından gözden geçirildi. 162 bağlantının 141'i 1–2 puanlı yargıdır; 21 güçlü bağlantının her biri için kaynak gösterildi, ikisi "tartışmalı" ya da "zayıf" işaretli. Uzman paneli henüz kurulmadı; kurulduğunda (ilk tur 6–8 kişi) bu tabloyu bağımsız olarak dolduracak.
- **Sıra yargılara duyarlı, ilk dört değil.** Yalnız güçlü bağlarla sıra değişiyor, ilk dörtteki dört sorun değişmiyor. Beşinci sıra sınırda.
- **Kutuplaşma kanıtı** karşılaştırmalı çalışmalar, bir Türkiye vaka incelemesi ve kuramsal bir modele dayanır; Türkiye'ye özgü nedensel tahmin değildir.
- **Açık skoru:** Plan hedefi varsa %70 plan, %30 ülke karşılaştırması; yoksa yalnız ülke karşılaştırması. Bazı plan tablolarının başlığı "hedef", dipnotu "tahmin" der; nitelik tablo başlığından okundu. Ar-Ge ve imalat satırlarında başlangıç ve gerçekleşme aynı seriden (Dünya Bankası).
- **Aday maddeler** (medya, tartışma kültürü) sıralamada kalır, sezon konusu olmaz.
- **DEMATEL doğrusal bir yapısal modeldir:** eşik etkileri, zamanlama ve etkileşimler yoktur; sıralama "yapısal konum"dur, dinamik bir tahmin değildir.
- Videoda "ilk turu başlatıyoruz" deniyor; uzman paneli henüz kurulmadı, başvurular açık. Kurulduğunda bu sayfada duyurulacak. Durum: Nerede duruyoruz?

## Düzeltmeler

Henüz düzeltme yok. Her düzeltme bu bölüme tarihiyle, neyin değiştiğiyle ve (izin verilirse) bildirenin adıyla eklenir.

---
Veri: [CC BY 4.0](../../LICENSE) · Kod: [MIT](../../LICENSE-KOD) · Bu klasör `node yonetim/acik-veri.mjs 04` ile üretilir; elle düzenlenmez.
