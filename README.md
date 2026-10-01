# Kök Neden · Açık veri

[Kök Neden](https://kokneden.org) videolarında ve sitesinde kullanılan bütün rakamların verisi, kodu ve kaynakları. Her videoda söylenen her sayı buradaki bir dosyaya, oradan da kaynağına götürülebilmeli.

## Düzen

```
videolar/
  NN-ad/
    README.md        videonun sorusu, dosyalar, kaynaklar, sınırlılıklar, düzeltmeler
    veri/            CSV dosyaları (UTF-8) ve sözlük (sutunlar, kaynak)
    kod/             veriyi çeken ve hesaplayan kod (varsa)
CHANGELOG.md         her değişiklik, tarihiyle
DUZELTMELER.md       yayından sonra düzeltilen her rakam, eski ve yeni haliyle
```

| No | Video | Klasör |
|---|---|---|
<!-- videolar -->
| 01 | Manifesto: Plan var, saha? | [`videolar/01-manifesto/`](videolar/01-manifesto/) |
| 02 | Yalnız ekonomi değil: güven, kutuplaşma, okuma kültürü | [`videolar/02-kapsam/`](videolar/02-kapsam/) |
| 03 | Türkiye'nin 24 kronik sorunu: 12 kalkınma planı ne hedefledi, ne oldu? | [`videolar/03-kronik-sorunlar/`](videolar/03-kronik-sorunlar/) |
| 04 | Türkiye'nin 24 kronik sorunundan hangisi kök neden? İlk sıralama | [`videolar/04-siralama/`](videolar/04-siralama/) |

## Kurallar

- **Kaynak her satırda.** Her dosyanın kaynağı `sozluk.json`'da ya da README'sinde; plan hedefleri plan metninden alıntıyla verilir.
- **Nitelik açık.** Planlardaki bir sayının *hedef* mi *tahmin* mi olduğu tablo başlığından okunur ve yazılır.
- **Geçmiş silinmez.** Düzeltilen bir rakamın eski hali `DUZELTMELER.md`'de kalır; her video yayını bir etikettir (`04-v1.0`), o gün gösterilen veri o etikette durur.
- **Girmeyenler:** Ham PDF'ler ve üçüncü tarafların tam veri setleri (yalnız bağlantısı verilir), ses dosyaları, kişisel veri.

## Hata mı buldunuz?

[Düzeltme bildirin](../../issues/new?template=duzeltme.yml) ya da [siteden yazın](https://kokneden.org/iletisim/?tur=duzeltme). Doğrulanan her düzeltme adınızla (isterseniz) `DUZELTMELER.md`'ye ve videonun sayfasına işlenir. Katkı yolu: [KATKI.md](KATKI.md).

## Lisans ve atıf

- Veri: [CC BY 4.0](LICENSE). Kaynak göstererek her amaçla kullanabilirsiniz: `Kök Neden, "<video başlığı>", kokneden.org, <yıl>. github.com/KokNeden/veri`
- Kod: [MIT](LICENSE-KOD).
- Metinler (README'ler, kaynak listeleri, sitedeki sayfalar ve transkriptler): [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/deed.tr). Kaynak göstererek olduğu gibi paylaşabilirsiniz; değiştirilmiş hâli yayımlanmaz. Ayrıntı: [kokneden.org/lisans](https://kokneden.org/lisans/).
- Üçüncü taraf verilerin (TÜİK, Dünya Bankası, V-Dem, OECD…) kendi lisansları geçerlidir; her dosyanın kaynağında belirtilir.
