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
| — | Henüz yayımlanan video yok | — |

## Kurallar

- **Kaynak her satırda.** Her dosyanın kaynağı `sozluk.json`'da ya da README'sinde; plan hedefleri plan metninden alıntıyla verilir.
- **Nitelik açık.** Planlardaki bir sayının *hedef* mi *tahmin* mi olduğu tablo başlığından okunur ve yazılır.
- **Geçmiş silinmez.** Düzeltilen bir rakamın eski hali `DUZELTMELER.md`'de kalır; her video yayını bir etikettir (`04-v1.0`), o gün gösterilen veri o etikette durur.
- **Girmeyenler:** Ham PDF'ler ve üçüncü tarafların tam veri setleri (yalnız bağlantısı verilir), ses dosyaları, kişisel veri.

## Hata mı buldunuz?

[Düzeltme bildirin](../../issues/new?template=duzeltme.yml) ya da [siteden yazın](https://kokneden.org/iletisim/?tur=duzeltme). Doğrulanan her düzeltme adınızla (isterseniz) `DUZELTMELER.md`'ye ve videonun sayfasına işlenir. Katkı yolu: [KATKI.md](KATKI.md).

## Lisans ve atıf

- Veri ve metinler: [CC BY 4.0](LICENSE). Kaynak göstererek her amaçla kullanabilirsiniz: `Kök Neden, "<video başlığı>", kokneden.org, <yıl>. github.com/KokNeden/veri`
- Kod: [MIT](LICENSE-KOD).
- Üçüncü taraf verilerin (TÜİK, Dünya Bankası, V-Dem, OECD…) kendi lisansları geçerlidir; her dosyanın kaynağında belirtilir.
