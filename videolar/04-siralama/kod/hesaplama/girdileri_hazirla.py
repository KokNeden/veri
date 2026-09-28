"""V4 girdilerini üretir: sorunlar.csv, baglanti_gerekceleri.csv, etki_matrisi_v0.1.csv,
kaynakca.csv, gostergeler.csv (V2 verisi + elle eklenenler), gosterge_listesi.csv.

Tek doğruluk kaynağı: aşağıdaki BAGLANTILAR listesi. Matris bu listeden türetilir.
Durum kodları:
    guclu      3-4 puan, en az bir akademik/kurumsal kaynak
    zayif      3-4 puan ama kaynak kuramsal/dolaylı → "gerekçesi zayıf"
    tartismali Berk'e soru olarak sunuldu (bkz. 05-siralama-sonucu/01-berke-sorular.md)
    yargi      1-2 puan, Kök Neden taslak yargısı (kaynak zorunlu değil)
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from kaynakca import KAYNAK

KOK = Path(__file__).resolve().parents[1]
VERI = KOK / "veri"
V2_VERI = KOK.parent / "03-kronik-sorunlar" / "veri"
V2_KOD = KOK.parent / "03-kronik-sorunlar" / "kod"
SURUM = "v0.2"

SORUNLAR = [
    # id, sütun, ad, kısa ad, ana gösterge, yedek, etki düzeyi, etki gerekçesi
    # v0.2 (27.09.2026): 03'ün 24 maddelik kronik listesi. S03 (kronik testini geçmedi) ve S23 (sonuç göstergesi) çıktı;
    # S09 ve S22 yeniden adlandırıldı; S11 Toplum ve kültür sütununa taşındı; S24–S26 eklendi.
    ("S01", "İnsan", "Eğitimin niteliği", "Eğitim niteliği", "G001", "", 3, "Tüm öğrenciler, dolayısıyla gelecekteki tüm işgücü"),
    ("S02", "İnsan", "Beceri uyumsuzluğu ve mesleki eğitim", "Beceri uyumsuzluğu", "G004", "G005", 2, "Gençler ve yeni mezunlar: geniş bir kesim, ama tüm nüfus değil"),
    ("S04", "İnsan", "Kadınların iş gücüne düşük katılımı", "Kadın istihdamı", "G007", "G008", 2, "Çalışma çağındaki kadınlar: nüfusun geniş bir kesimi"),
    ("S05", "İnsan", "Demografik dönüşüm", "Demografik dönüşüm", "G009", "", 3, "Yaş yapısı tüm nüfusu ve kamu maliyesini etkiler"),
    ("S06", "Kurumlar", "Hukukun üstünlüğü ve yargının güvenilirliği ile hızı", "Hukuk ve yargı", "G013", "G012", 3, "Kurumsal çerçeve: tüm yurttaşlar ve firmalar"),
    ("S07", "Kurumlar", "Plan-uygulama kopukluğu ve politika sürekliliği", "Plan-uygulama kopukluğu", "G015", "", 3, "Tüm kamu politikaları"),
    ("S08", "Kurumlar", "Aşırı merkeziyetçilik ve yerel kapasite", "Merkeziyetçilik", "G017", "", 3, "Tüm yerel hizmetler"),
    ("S09", "Kurumlar", "Kurallı ve tarafsız kamu yönetimi", "Kurallı ve tarafsız kamu yönetimi", "G018", "G019", 3, "Tüm kamu hizmetleri"),
    ("S10", "Kurumlar", "Kayıt dışılık", "Kayıt dışılık", "G020", "G021", 2, "Kayıt dışı çalışanlar ve vergi tabanı: geniş kesim"),
    ("S12", "Kurumlar", "Medya ve bilgi ekosistemi (aday)", "Medya ekosistemi", "G024", "G059", 3, "Tüm kamusal tartışma"),
    ("S13", "Üretim", "Tarımda verimlilik ve parçalı arazi", "Tarım verimliliği", "G026", "", 2, "Tarım çalışanları, kırsal nüfus ve gıda fiyatları"),
    ("S14", "Üretim", "Sanayinin teknoloji düzeyi ve ithal ara malı bağımlılığı", "Sanayi teknolojisi", "G060", "G031", 2, "İmalat sanayi: büyük ama tek bir sektör"),
    ("S15", "Teknoloji", "Ar-Ge'yi ürüne dönüştürme kapasitesi", "Ar-Ge'yi ürüne dönüştürme", "G032", "G034", 1, "Doğrudan: Ar-Ge yapan firmalar ve araştırmacılar"),
    ("S16", "Mekân ve kaynak", "Plansız kentleşme", "Plansız kentleşme", "G035", "", 2, "Kentli nüfusun ruhsatsız/plansız alanlarda yaşayan kesimi"),
    ("S17", "Mekân ve kaynak", "Deprem ve afet riski yönetimi", "Afet riski", "G037", "", 3, "Büyük nüfus merkezleri yüksek deprem tehlikesi altında"),
    ("S18", "Mekân ve kaynak", "Enerjide dışa bağımlılık", "Enerji bağımlılığı", "G038", "", 3, "Makro: fiyatlar ve cari denge üzerinden tüm ekonomi"),
    ("S19", "Mekân ve kaynak", "Su yönetimi ve kuraklık", "Su ve kuraklık", "G039", "G040", 2, "Tarım ve kuraklık riski taşıyan havzalar"),
    ("S20", "Mekân ve kaynak", "Bölgesel eşitsizlik", "Bölgesel eşitsizlik", "G041", "", 2, "Geride kalan bölgelerde yaşayanlar"),
    ("S21", "Ekonomi", "Kronik enflasyon ve makroekonomik istikrarsızlık", "Enflasyon ve istikrarsızlık", "G042", "G043", 3, "Tüm nüfus"),
    ("S22", "Ekonomi", "Dış finansman bağımlılığı", "Dış finansman bağımlılığı", "G045", "", 3, "Makro: tüm ekonomi"),
    ("S11", "Toplum ve kültür", "Toplumsal güven", "Toplumsal güven", "G023", "", 3, "Tüm toplumsal ve ekonomik ilişkiler"),
    ("S24", "Toplum ve kültür", "Siyasi kutuplaşma", "Siyasi kutuplaşma", "G061", "", 3, "Tüm seçmenler ve kamusal karar alma"),
    ("S25", "Toplum ve kültür", "Din, dil ve etnik köken ekseninde ayrışma", "Kimlik temelli ayrışma", "G062", "", 2, "Dışlanan gruplar ve toplumsal barış: geniş bir kesim"),
    ("S26", "Toplum ve kültür", "Okuma, düşünme ve tartışma kültürünün zayıflığı (aday)", "Tartışma kültürü", "G063", "", 3, "Tüm kamusal tartışma ve karar alma"),
]

# (kaynak, hedef, puan, durum, [kaynak anahtarları], gerekçe)
BAGLANTILAR = [
    # S01 Eğitimin niteliği
    ("S01", "S02", 3, "guclu", ["WB13", "HSWZ17"], "Temel becerileri zayıf mezunun işgücü piyasasına uyumu düşük; mesleki eğitimin getirisi genel becerilere bağlı ve yaşam boyu azalıyor."),
    ("S01", "S15", 3, "guclu", ["CL90", "GRV04"], "Ar-Ge'yi ürüne dönüştürmek soğurma kapasitesi ister; bu kapasitenin temeli çalışanların bilgi ve becerisi."),
    ("S01", "S23", 3, "guclu", ["HW12"], "Bilişsel beceriler (test puanları) uzun dönem büyümeyi okullaşma süresinden daha güçlü açıklıyor."),
    ("S01", "S14", 2, "yargi", [], "Nitelikli işgücü teknoloji yoğun sanayinin ön koşulu; etki büyük ölçüde S02 ve S15 üzerinden dolaylı."),
    ("S01", "S04", 2, "yargi", ["IL12"], "Kadın katılımı eğitim düzeyiyle güçlü ilişkili; kaynak niteliği değil düzeyi ölçtüğü için 2."),
    ("S01", "S03", 1, "yargi", [], "Nitelikli eğitim arayışı yurt dışına yönelmede bir etken."),
    ("S01", "S20", 1, "yargi", [], "Okul niteliğindeki bölgesel farklar eşitsizliği yeniden üretir."),
    ("S01", "S11", 1, "yargi", [], "Eğitim düzeyi ve niteliği genelleşmiş güvenle ilişkili."),
    ("S01", "S12", 1, "yargi", [], "Medya okuryazarlığı bilgi ekosisteminin talep tarafı."),
    # S02 Beceri uyumsuzluğu
    ("S02", "S23", 2, "yargi", [], "Beceri-iş uyumsuzluğu emeğin yanlış dağılımı yoluyla verimliliği düşürür."),
    ("S02", "S14", 2, "yargi", [], "Ara eleman eksikliği teknoloji yükseltmeyi yavaşlatır."),
    ("S02", "S03", 1, "yargi", [], "Nitelikli gençlerin işsizliği ve eksik istihdamı göç niyetini artırır."),
    ("S02", "S10", 1, "yargi", [], "Kayıtlı işe giremeyen gençler kayıt dışına yönelir."),
    ("S02", "S04", 1, "yargi", [], "Genç kadınlar için okul-iş geçişi daha zayıf."),
    # S03 Beyin göçü
    ("S03", "S15", 2, "yargi", ["DR12"], "Nitelikli göç araştırma kapasitesini azaltır; diaspora ve geri dönüş kanalları nedeniyle net etki literatürde tartışmalı."),
    ("S03", "S01", 1, "yargi", [], "Akademisyen ve nitelikli öğretmen kaybı."),
    ("S03", "S09", 1, "yargi", [], "Kamudan nitelikli personel kaybı."),
    ("S03", "S23", 1, "yargi", [], "Nitelikli emek kaybı."),
    # S04 Kadın istihdamı
    ("S04", "S23", 2, "yargi", ["CT16"], "Cinsiyet açıkları kişi başı geliri düşürüyor; etki verimlilikten çok işgücü miktarı kanalından."),
    ("S04", "S05", 2, "yargi", ["BCFF09"], "Kadın katılımı ve doğurganlık karşılıklı ilişkili."),
    ("S04", "S10", 1, "yargi", [], "Ücretsiz aile işçiliği ve ev eksenli kayıt dışı çalışma."),
    ("S04", "S22", 1, "yargi", [], "Tek gelirli hanede tasarruf kapasitesi düşük."),
    ("S04", "S20", 1, "yargi", [], "Kadın katılımındaki bölgesel farklar."),
    # S05 Demografik dönüşüm
    ("S05", "S22", 2, "yargi", ["HIG98"], "Yaş yapısı tasarruf oranını etkiler (yaşam döngüsü); demografik pencere daralıyor."),
    ("S05", "S23", 1, "yargi", [], "Yaşlanan işgücü."),
    ("S05", "S02", 1, "yargi", [], "Genç nüfusun büyüklüğü eğitim-iş uyumunu zorlar."),
    # S06 Hukuk ve yargı
    ("S06", "S23", 3, "guclu", ["AJR01", "RST04", "DJ03"], "Mülkiyet hakları ve sözleşmelerin uygulanması yatırım ve verimliliğin en güçlü belirleyicileri arasında; mahkemelerin hızı ve biçimselliği uyuşmazlık maliyetini belirliyor."),
    ("S06", "S10", 3, "guclu", ["TS09"], "Kurumsal kaliteye ve hukukun uygulanmasına güven kayıt dışı ekonomiyi küçültüyor."),
    ("S06", "S11", 3, "guclu", ["RS08"], "Tarafsız hukuk ve düzen kurumları genelleşmiş güvenin başlıca kaynağı."),
    ("S06", "S03", 2, "yargi", ["GT14"], "Geri dönüş niyetinde siyasi ve ekonomik istikrar etkili; hukuk güvencesinin payı ayrıştırılamıyor."),
    ("S06", "S22", 2, "yargi", [], "Hukuki öngörülebilirlik uzun vadeli yatırımı ve dış finansmanın bileşimini (doğrudan yatırım / sıcak para) etkiler."),
    ("S06", "S09", 2, "yargi", [], "İdari yargı denetimi kamu yönetiminin kurallılığını etkiler."),
    ("S06", "S12", 2, "yargi", [], "Yargı bağımsızlığı basın özgürlüğünün güvencesi."),
    ("S06", "S15", 2, "yargi", [], "Fikri mülkiyet korumasının uygulanması."),
    ("S06", "S07", 2, "yargi", [], "Kural temelli yönetim politika sürekliliğini destekler."),
    ("S06", "S16", 2, "yargi", [], "İmar kurallarının yaptırımı."),
    ("S06", "S17", 2, "yargi", [], "Yapı denetimi ihlallerine yaptırım."),
    ("S06", "S21", 1, "yargi", [], "Sözleşme güvencesi ve finansal derinlik."),
    # S07 Plan-uygulama kopukluğu
    ("S07", "S21", 3, "tartismali", ["CWN92"], "Gelişmekte olan ülkelerde yasal bağımsızlıktan çok merkez bankası başkanlarının değişim sıklığı (fiili süreklilik) yüksek enflasyonla ilişkili. Kaynak S07'nin yalnız politika sürekliliği bileşenini ölçüyor."),
    ("S07", "S23", 2, "yargi", ["BBD16"], "Politika belirsizliği yatırımı ve istihdamı azaltıyor."),
    ("S07", "S22", 2, "yargi", ["BBD16"], "Belirsizlik uzun vadeli tasarrufu ve yatırımı caydırır."),
    ("S07", "S01", 2, "yargi", [], "Sık sistem değişikliği (sınav, kademe) eğitimde sürekliliği bozar."),
    ("S07", "S13", 2, "yargi", [], "Destek ve arazi politikalarında süreksizlik."),
    ("S07", "S15", 2, "yargi", [], "Ar-Ge teşviklerinde süreksizlik."),
    ("S07", "S16", 2, "yargi", [], "İmar planlarının uygulanmaması."),
    ("S07", "S17", 2, "yargi", [], "Afet planlarının uygulamaya geçmemesi."),
    ("S07", "S19", 2, "yargi", [], "Havza planlarının uygulanmaması."),
    ("S07", "S20", 2, "yargi", [], "Bölgesel planların uygulanmaması."),
    ("S07", "S14", 1, "yargi", [], "Sanayi politikasında süreksizlik."),
    ("S07", "S18", 1, "yargi", [], "Enerji politikasında süreksizlik."),
    # S08 Merkeziyetçilik
    ("S08", "S07", 2, "yargi", [], "Uygulama yerelde olur; yerel kapasite zayıfsa plan uygulamaya geçmez."),
    ("S08", "S16", 2, "yargi", [], "Planlama yetkisinin merkezde toplanması ve yerel kapasitenin zayıflığı."),
    ("S08", "S17", 2, "yargi", ["OECD23EQ"], "Afet hazırlığı ve müdahalede yerel kapasite belirleyici."),
    ("S08", "S20", 1, "tartismali", ["RPE10"], "Literatür ters yönlü: mali ademi merkeziyetçilik düşük/orta gelirli ülkelerde bölgesel eşitsizliği ARTIRMAKLA ilişkili bulunmuş. Bu yüzden 1."),
    ("S08", "S19", 1, "yargi", [], "Su hizmetlerinde yerel kapasite."),
    ("S08", "S09", 1, "yargi", [], "Yerel yönetimlerde kurumsal kapasite."),
    ("S08", "S11", 1, "yargi", [], "Yerel katılım ve güven."),
    # S09 Kamuda liyakat
    ("S09", "S07", 4, "guclu", ["PWA13", "ER99"], "Planın kâğıtta kalıp kalmayacağını belirleyen ana etken uygulama kapasitesi: liyakatle seçilmiş, kurallı bürokrasi. 'Devlet gibi görünme' (isomorphic mimicry) literatürü."),
    ("S09", "S23", 3, "guclu", ["ER99", "RE00"], "Weberyen bürokrasi (liyakatle işe alım, kariyer) büyüme ve kamu performansıyla ilişkili."),
    ("S09", "S17", 3, "guclu", ["ESC07", "AB11"], "Kamu kesimindeki yolsuzluk büyük depremlerde ölüm sayısını artırıyor (yapı denetimi)."),
    ("S09", "S11", 3, "guclu", ["RS08"], "Kamu hizmetinin tarafsızlığı genelleşmiş güvenin kaynağı."),
    ("S09", "S10", 2, "yargi", ["BP09"], "Vergi idaresi kapasitesi kayıt dışılıkla birlikte gelişir."),
    ("S09", "S03", 2, "yargi", [], "Liyakatsizlik algısı nitelikli göçü iter."),
    ("S09", "S01", 2, "yargi", [], "Eğitim yönetiminin kapasitesi."),
    ("S09", "S15", 2, "yargi", [], "Ar-Ge destek programlarının yönetimi."),
    ("S09", "S16", 2, "yargi", [], "İmar ve ruhsat süreçleri."),
    ("S09", "S19", 2, "yargi", [], "Su yönetimi kurumlarının kapasitesi."),
    ("S09", "S21", 2, "yargi", [], "Ekonomi yönetimi kurumlarının kapasitesi."),
    ("S09", "S13", 1, "yargi", [], "Tarım destek yönetimi."),
    ("S09", "S20", 1, "yargi", [], "Bölgesel kalkınma ajanslarının kapasitesi."),
    ("S09", "S12", 1, "yargi", [], "Kamu bilgisinin açıklığı."),
    # S10 Kayıt dışılık
    ("S10", "S23", 3, "guclu", ["LPS14", "WB10"], "Kayıt dışı firmalar çok daha düşük verimli ve büyümüyor; kayıt dışılık kaynakları verimsiz firmalarda tutuyor."),
    ("S10", "S22", 2, "yargi", ["WB10"], "Dar vergi tabanı kamu tasarrufunu düşürür."),
    ("S10", "S11", 1, "yargi", [], "Kurala uymayanın kazandığı algısı."),
    ("S10", "S02", 1, "yargi", [], "Kayıt dışı işlerde eğitim ve beceri yatırımı düşük."),
    ("S10", "S21", 1, "yargi", [], "Vergi tabanı dar → maliye politikası kırılgan."),
    ("S10", "S04", 1, "yargi", [], "Kayıt dışı iş kadınlar için güvencesiz."),
    # S11 Toplumsal güven
    ("S11", "S23", 3, "guclu", ["KK97"], "Genelleşmiş güven büyüme ve yatırımla ilişkili (sözleşme ve izleme maliyetleri). Kaynak büyümeyi ölçüyor; verimliliğe eşlendi."),
    ("S11", "S10", 2, "yargi", ["TS09"], "Vergi ahlakı ve kurumlara güven kayıt dışılığı etkiliyor."),
    ("S11", "S06", 1, "yargi", [], "Kurallara uyum kültürü."),
    ("S11", "S12", 1, "yargi", [], "Kutuplaşma ve bilgi kaynaklarına güven."),
    ("S11", "S07", 1, "yargi", [], "Uzlaşı kapasitesi ve politika sürekliliği."),
    ("S11", "S22", 1, "yargi", [], "Finansal sisteme güven ve tasarruf."),
    # S12 Medya ekosistemi
    ("S12", "S09", 3, "guclu", ["BW03"], "Basın özgürlüğü yolsuzluğu azaltıyor. Yolsuzluk S09'un bir bileşeni; liyakate doğrudan kanıt değil."),
    ("S12", "S07", 2, "yargi", ["BB02"], "Bilgili kamuoyu hükümetin duyarlılığını ve hesap verebilirliğini artırıyor."),
    ("S12", "S11", 2, "yargi", [], "Bilgi kirliliği ve kutuplaşma güveni aşındırır."),
    ("S12", "S06", 2, "yargi", [], "Hesap verebilirlik ve yargı üzerinde kamuoyu denetimi."),
    ("S12", "S21", 1, "yargi", [], "Beklenti yönetimi ve bilgiye güven."),
    # S13 Tarım
    ("S13", "S19", 3, "tartismali", ["OECD16AG", "WBCCDR22"], "Tarım en büyük su kullanıcısı; verimsiz sulama su stresini artırıyor. Ama bağ düşük verimlilikten değil sulama yönetiminden geliyor; verimlilik artışı su kullanımını artırabilir de (geri tepme etkisi). S13↔S19 karşılıklı 3-3 döngüsü S13'ü neden grubuna taşıyor."),
    ("S13", "S10", 3, "tartismali", ["WB10"], "Kayıt dışı istihdamın büyük kısmı tarımda. Ama bu büyük ölçüde bileşim etkisi olabilir (tarım küçüldükçe kayıt dışılık azalır): nedensellik mi, sayım mı?"),
    ("S13", "S16", 2, "yargi", ["HT70"], "Tarımda düşük gelir kırdan kente göçü iter."),
    ("S13", "S20", 2, "yargi", [], "Tarıma bağımlı bölgelerde düşük gelir."),
    ("S13", "S21", 2, "yargi", [], "Gıda fiyatları enflasyonun oynak bileşeni."),
    ("S13", "S04", 2, "yargi", ["IL12"], "Tarımdan çıkış (ücretsiz aile işçiliğinin çözülmesi) kadın katılımını düşürdü."),
    ("S13", "S23", 2, "yargi", [], "Düşük verimli sektörde yüksek istihdam payı toplam verimliliği düşürür."),
    # S14 Sanayi teknolojisi
    ("S14", "S23", 3, "guclu", ["HHR07"], "İhraç sepetinin teknoloji/karmaşıklık düzeyi sonraki büyümeyi öngörüyor."),
    ("S14", "S22", 3, "guclu", ["SAY10"], "İmalatın ithal ara malı bağımlılığı büyüme dönemlerinde ithalatı ve cari açığı artırıyor."),
    ("S14", "S15", 2, "yargi", [], "Düşük teknolojili sanayinin Ar-Ge talebi düşük."),
    ("S14", "S02", 1, "yargi", [], "Beceri talebinin yapısı."),
    ("S14", "S18", 1, "yargi", [], "Enerji yoğun üretim."),
    ("S14", "S21", 1, "yargi", [], "İthal girdi → kur geçişkenliği."),
    # S15 Ar-Ge
    ("S15", "S14", 3, "guclu", ["GRV04"], "Ar-Ge hem yenilik hem teknoloji soğurma yoluyla sanayinin teknoloji düzeyini yükseltiyor."),
    ("S15", "S23", 3, "guclu", ["GRV04"], "Ar-Ge verimlilik artışının doğrudan kaynağı."),
    ("S15", "S03", 1, "yargi", [], "Araştırmacı istihdamı az → göç."),
    ("S15", "S18", 1, "yargi", [], "Yerli enerji teknolojileri."),
    ("S15", "S02", 1, "yargi", [], "Nitelikli iş talebi."),
    # S16 Plansız kentleşme
    ("S16", "S17", 4, "guclu", ["GUN15", "SBB23"], "Eski yönetmelikle yapılmış, denetimsiz ve imar aflarıyla kayda geçmiş yapı stoku deprem kayıplarının ana nedenlerinden. (Denetim ve yolsuzluk kanalı S09>S17'de ayrıca sayılıyor.)"),
    ("S16", "S19", 1, "yargi", [], "Havza koruma alanlarında yapılaşma."),
    ("S16", "S11", 1, "yargi", [], "Kentsel bütünleşme."),
    ("S16", "S20", 1, "yargi", [], "Kent içi eşitsizlik."),
    ("S16", "S23", 1, "yargi", [], "Altyapı ve ulaşım maliyetleri."),
    ("S16", "S21", 1, "yargi", [], "Konut fiyatları."),
    # S17 Afet
    ("S17", "S22", 2, "yargi", ["GRADE23", "SBB23"], "Büyük depremler kamu maliyesine ve dış finansman ihtiyacına büyük yük bindiriyor."),
    ("S17", "S20", 2, "yargi", ["OECD23EQ"], "Depremden etkilenen bölgelerin geri kalması."),
    ("S17", "S16", 1, "yargi", [], "Afet sonrası aceleci yapılaşma."),
    ("S17", "S21", 1, "yargi", [], "Yeniden yapım harcamaları."),
    ("S17", "S23", 1, "yargi", [], "Sermaye stoku kaybı."),
    ("S17", "S03", 1, "yargi", [], "Güvenlik kaygısıyla göç."),
    # S18 Enerji
    ("S18", "S22", 3, "guclu", ["EREN25"], "Enerji ithalatı cari açığın ana kalemi; TCMB analizine göre petrol fiyatındaki 10 dolarlık artış 12 ayda yaklaşık 2,6 milyar dolar ek cari açık yaratıyor (ihracat ve ithalat esnekliği sıfır varsayımıyla)."),
    ("S18", "S21", 3, "tartismali", ["DK14", "EREN25"], "Petrol fiyatları iç fiyatlara geçiyor; TCMB analizine göre yüzde 10'luk artış TÜFE'yi yaklaşık 1 puan yükseltiyor. Ama bu bir fiyat düzeyi şoku; kronik enflasyonu tek başına açıklamıyor (setteki enerji ithalatçılarının çoğu düşük enflasyonlu)."),
    ("S18", "S14", 1, "yargi", [], "Enerji maliyeti ve rekabet gücü."),
    ("S18", "S23", 1, "yargi", [], "Enerji fiyat şokları."),
    # S19 Su
    ("S19", "S13", 3, "guclu", ["WBCCDR22"], "Kuraklık ve su kıtlığı tarım üretimini doğrudan etkiliyor."),
    ("S19", "S20", 1, "yargi", [], "Kuraklığa açık bölgeler."),
    ("S19", "S21", 1, "yargi", [], "Gıda fiyatları."),
    ("S19", "S18", 1, "yargi", [], "Hidroelektrik üretimi."),
    # S20 Bölgesel eşitsizlik
    ("S20", "S16", 3, "zayif", ["HT70"], "Bölgeler arası gelir farkı göçü, göç plansız kentleşmeyi besliyor. Kaynak kuramsal; Türkiye'ye özgü ampirik kaynak eklenmeli."),
    ("S20", "S01", 2, "yargi", [], "Okul niteliğinde bölgesel farklar."),
    ("S20", "S10", 2, "yargi", [], "Kayıt dışılığın bölgesel yoğunlaşması."),
    ("S20", "S04", 1, "yargi", [], "Kadın katılımında bölgesel fark."),
    ("S20", "S11", 1, "yargi", [], "Bölgesel kopukluk."),
    ("S20", "S23", 1, "yargi", [], "Kaynakların verimsiz mekânsal dağılımı."),
    # S21 Enflasyon
    ("S21", "S22", 3, "zayif", ["WB11", "VR10"], "Yüksek ve oynak enflasyon tasarrufu dövize, altına ve kısa vadeye kaydırıyor. Kaynaklar 2000'lerdeki tasarruf düşüşünü daha çok mali konsolidasyon ve kredi derinleşmesine bağlıyor; toplam tasarrufa etkisi belirsiz. Gerekçesi zayıf: Türkiye'ye özgü, bu yönü doğrudan gösteren kaynak eklenmeli ya da puan düşürülmeli."),
    ("S21", "S23", 3, "guclu", ["FIS93"], "Enflasyon büyüme ve verimlilik artışıyla negatif ilişkili (belirsizlik, kaynak dağılımı)."),
    ("S21", "S07", 2, "yargi", [], "Kriz dönemleri plan ve programların rafa kalkmasına yol açar."),
    ("S21", "S03", 2, "yargi", [], "Ekonomik istikrarsızlık nitelikli göçü iter."),
    ("S21", "S15", 2, "yargi", [], "Uzun vadeli yatırım ufku kısalır."),
    ("S21", "S11", 1, "yargi", [], "Paraya ve kurumlara güven."),
    ("S21", "S10", 1, "yargi", [], "Kayıt dışına kaçış."),
    # S22 Tasarruf ve dış finansman
    ("S22", "S21", 3, "guclu", ["KR99"], "Dış finansmana bağımlılık ani duruş ve kur krizlerine açıklık yaratıyor; kur şokları enflasyona geçiyor. (Kaynak ikiz krizleri kapsıyor; kur geçişkenliği için Türkiye'ye özgü kaynak eklenmeli.)"),
    ("S22", "S23", 1, "yargi", [], "Yatırımın finansman maliyeti."),
    ("S22", "S15", 1, "yargi", [], "Uzun vadeli finansman eksikliği."),
    ("S22", "S07", 1, "yargi", [], "Dış şoklar programları bozar."),
    ("S22", "S14", 1, "yargi", [], "Sanayi yatırımının finansmanı."),
    # S23 Verimlilik
    ("S23", "S22", 2, "yargi", [], "Düşük gelir artışı tasarrufu sınırlar."),
    ("S23", "S03", 2, "yargi", [], "Düşük ücretler nitelikli göçü iter."),
    ("S23", "S21", 1, "yargi", [], "Birim maliyet baskısı."),
    ("S23", "S10", 1, "yargi", [], "Düşük verimli firmalar kayıt dışında kalır."),
    ("S23", "S20", 1, "yargi", [], "Verimlilik farkının bölgesel yansıması."),
]

CIKAN = {"S03", "S23"}  # v0.2: 03'te listeden çıkanlar
BAGLANTILAR = [b for b in BAGLANTILAR if b[0] not in CIKAN and b[1] not in CIKAN]
try:  # S24–S26 bağlantı taslağı (veri/yeni_baglantilar_s24_s26.py)
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("yeni", VERI / "yeni_baglantilar_s24_s26.py")
    _m = _iu.module_from_spec(_sp); _sp.loader.exec_module(_m)
    KAYNAK.update(_m.YENI_KAYNAK)
    BAGLANTILAR += _m.YENI_BAGLANTILAR
except FileNotFoundError:
    pass

# v0.2 kararları (Berk, 27.09.2026: 01-berke-sorular.md B1–B10 önerileriyle toplu kabul; S09 yeni tanımı).
# (kaynak, hedef) → yeni satır; puan 0 ise bağlantı silinir.
DUZELTME = {
    ("S09", "S07"): (3, "guclu", ["PWA13", "RT08"], "Planın uygulanması, kurallara bağlı ve tarafsız işleyen bir yönetime dayanır; keyfi ve kişiye göre işleyen yönetimde program 'devlet gibi görünür' ama uygulanmaz (isomorphic mimicry). B1: 4→3; ER99 çıktı (işe alımda liyakati ölçüyor, S09'un yeni tanımı değil)."),
    ("S12", "S09"): (3, "guclu", ["BW03"], "Basın özgürlüğü yolsuzluğu azaltıyor; yolsuzluk tarafsız ve kurallı yönetimin tam karşıtı."),
    ("S13", "S10"): (2, "yargi", ["WB10"], "Kayıt dışı istihdamın büyük kısmı tarımda; bağın bir kısmı bileşim (sayım) etkisi olduğu için 2 (B3)."),
    ("S16", "S17"): (3, "guclu", ["GUN15", "SBB23"], "Eski yönetmelikle yapılmış, denetimsiz ve imar aflarıyla kayda geçmiş yapı stoku deprem kayıplarının ana nedenlerinden. Denetim kanalı S09>S17'de sayıldığı için 3 (B9)."),
    ("S21", "S22"): (2, "yargi", ["WB11", "VR10"], "Yüksek ve oynak enflasyon tasarrufu dövize ve kısa vadeye kaydırıyor; toplam etkisi belirsiz, 2 (B9)."),
    ("S18", "S21"): (2, "yargi", ["DK14", "EREN25"], "Petrol fiyatları iç fiyatlara geçiyor; ama bu bir fiyat düzeyi şoku, kronik enflasyonu tek başına açıklamıyor, 2 (B9)."),
    ("S13", "S19"): (2, "yargi", ["OECD16AG", "WBCCDR22"], "Tarım en büyük su kullanıcısı; bağ verimlilikten çok sulama yönetiminden geliyor, 2 (B9)."),
    ("S01", "S06"): (1, "yargi", [], "Eğitim düzeyi ve kurumlar (Glaeser vd. 2004 tezi; tartışmalı ama sıfır değil, B8)."),
    ("S01", "S09"): (1, "yargi", [], "Kamu personelinin eğitimi ve yurttaşın talebi (B8)."),
    ("S09", "S06"): (2, "yargi", [], "Yargı personeli ve mahkeme yönetiminin kurallı ve tarafsız işleyişi (B10)."),
    ("S01", "S05"): (2, "yargi", ["BCFF09"], "Kadın eğitimi doğurganlıkla ilişkili (B10)."),
    ("S21", "S14"): (1, "yargi", [], "Oynaklık uzun vadeli sanayi yatırımını caydırır (B10)."),
    ("S19", "S17"): (1, "yargi", [], "Kuraklık ve sel afet riskinin parçası (B10)."),
    ("S11", "S09"): (1, "yargi", [], "Güven düşük toplumda kayırmacılık beklentisi (B10)."),
    ("S09", "S01"): (1, "yargi", [], "Eğitim yönetiminin kurallı ve tarafsız işleyişi (S09 yeni tanımı)."),
    ("S09", "S15"): (1, "yargi", [], "Ar-Ge destek programlarının tarafsız ve kurallı yönetimi (S09 yeni tanımı)."),
    ("S09", "S19"): (1, "yargi", [], "Su tahsisinin kurallı ve tarafsız yönetimi (S09 yeni tanımı)."),
    ("S09", "S21"): (2, "yargi", [], "Kurallara bağlı ekonomi yönetimi ve öngörülebilirlik (S09 yeni tanımı)."),
    ("S12", "S11"): (2, "yargi", [], "Bilgi kirliliği güveni aşındırır (kutuplaşma kanalı artık S24'te)."),
    ("S11", "S12"): (1, "yargi", [], "Bilgi kaynaklarına güven (kutuplaşma kanalı artık S24'te)."),
    ("S11", "S07"): (1, "yargi", [], "Uzlaşı kapasitesi (siyasi kutuplaşma kanalı S24>S07'de ayrıca sayılıyor)."),
}
_eski = {(b[0], b[1]): i for i, b in enumerate(BAGLANTILAR)}
for (a_, b_), (p_, d_, k_, g_) in DUZELTME.items():
    satir = (a_, b_, p_, d_, k_, g_)
    if (a_, b_) in _eski:
        BAGLANTILAR[_eski[(a_, b_)]] = satir
    else:
        BAGLANTILAR.append(satir)
BAGLANTILAR = [b for b in BAGLANTILAR if b[2] > 0]

# V2'de eksik kalan ana göstergeler için elle eklenen değerler (hepsi 2026-09-21'de çekildi)
WGI_2023 = {  # World Bank WGI 2023 tahminleri; API kodu GOV_WGI_*.EST (kaynak 3)
    "G012": {"AUS": 1.5031839, "AUT": 1.6577235, "BEL": 1.2719977, "CAN": 1.4361681, "CHL": 0.6647803, "COL": -0.5648803, "CRI": 0.6431263, "CZE": 1.1605869, "DEU": 1.5855645, "DNK": 2.0143499, "EST": 1.482125, "FIN": 2.0200539, "FRA": 0.9946177, "GRC": 0.3963788, "HUN": 0.1894005, "IRL": 1.5980444, "ISL": 1.59027, "ISR": 0.6642378, "ITA": 0.6505552, "CHE": 1.7920906, "ESP": 0.9304606, "GBR": 1.2703547, "JPN": 1.5084872, "KOR": 1.1844569, "LTU": 1.3288838, "LUX": 1.7286548, "LVA": 1.0727082, "MEX": -1.0777054, "MYS": 0.3016843, "NLD": 1.7174805, "NOR": 1.9859646, "NZL": 1.7075544, "POL": 0.3564347, "PRT": 1.0824285, "SVK": 0.5534478, "SVN": 0.9707915, "SWE": 1.6947293, "TUR": -0.7992335, "USA": 0.9606912},
    "G015": {"AUS": 1.7818134, "AUT": 1.5790569, "BEL": 1.1646047, "CAN": 1.7452669, "CHL": 0.9969509, "COL": -0.0421246, "CRI": 0.3340948, "CZE": 1.2354239, "DEU": 1.5613864, "DNK": 1.9559634, "EST": 1.2678954, "FIN": 1.787685, "FRA": 1.3517693, "GRC": 0.2578486, "HUN": 0.5461907, "IRL": 1.6609005, "ISL": 1.6402729, "ISR": 1.3569151, "ITA": 0.8533467, "CHE": 2.0409373, "ESP": 1.0779914, "GBR": 1.1378943, "JPN": 1.9883877, "KOR": 1.4955907, "LTU": 0.9448653, "LUX": 2.1455984, "LVA": 0.6374221, "MEX": -0.0748652, "MYS": 0.7474758, "NLD": 1.7511282, "NOR": 1.7870167, "NZL": 1.7271046, "POL": 0.6341038, "PRT": 0.9658494, "SVK": 0.5846525, "SVN": 1.1624609, "SWE": 1.6930218, "TUR": -0.114085, "USA": 1.3585237},
    "G019": {"AUS": 1.8057703, "AUT": 1.3200882, "BEL": 1.467016, "CAN": 1.6263584, "CHL": 1.0318341, "COL": -0.3090049, "CRI": 0.6775627, "CZE": 0.8499213, "DEU": 1.699403, "DNK": 2.3171626, "EST": 1.6727855, "FIN": 2.193956, "FRA": 1.2672713, "GRC": 0.3292978, "HUN": 0.083173, "IRL": 1.5859129, "ISL": 1.6623764, "ISR": 0.8712956, "ITA": 0.571449, "CHE": 2.0972439, "ESP": 0.7395223, "GBR": 1.4745753, "JPN": 1.3377896, "KOR": 0.8788564, "LTU": 0.8884764, "LUX": 2.0124074, "LVA": 0.7759204, "MEX": -0.9321625, "MYS": 0.380697, "NLD": 1.8837073, "NOR": 2.0745237, "NZL": 2.0156067, "POL": 0.7534838, "PRT": 0.7848198, "SVK": 0.3846188, "SVN": 0.6814999, "SWE": 1.9804259, "TUR": -0.4374572, "USA": 1.1951066},
    "G059": {"AUS": 1.5142943, "AUT": 1.4328609, "BEL": 1.5152567, "CAN": 1.5113422, "CHL": 1.0282277, "COL": 0.0303931, "CRI": 1.0983992, "CZE": 1.139348, "DEU": 1.5915479, "DNK": 1.9213047, "EST": 1.3973248, "FIN": 1.8446784, "FRA": 1.1742965, "GRC": 0.830097, "HUN": -0.0468028, "IRL": 1.6268782, "ISL": 1.4096588, "ISR": 0.4202063, "ITA": 1.0865677, "CHE": 1.625069, "ESP": 1.1523041, "GBR": 1.2519674, "JPN": 1.1289319, "KOR": 0.9190605, "LTU": 1.1887714, "LUX": 1.6677685, "LVA": 1.1124815, "MEX": -0.2517507, "MYS": -0.1658995, "NLD": 1.7002227, "NOR": 1.9331357, "NZL": 1.7161747, "POL": 0.4100224, "PRT": 1.3110945, "SVK": 0.972897, "SVN": 1.0261192, "SWE": 1.7304193, "TUR": -1.0826785, "USA": 0.8636176},
}
WGI_KOD = {"G012": "GOV_WGI_RL.EST", "G015": "GOV_WGI_GE.EST", "G019": "GOV_WGI_CC.EST", "G059": "GOV_WGI_VA.EST"}
# Not: WGI 2024 verisi API'de var; burada 2023 kullanıldı (çekim anında erişilebilen sürüm)
# PISA 2022 (mat, okuma, fen) — OECD (2023) PISA 2022 Results Vol. I, Tablo I.1. OECD satırı = OECD ortalaması
PISA_2022 = {"TUR": (453, 456, 476), "KOR": (527, 515, 528), "ESP": (473, 474, 485), "PRT": (472, 477, 484),
             "GRC": (430, 438, 441), "POL": (489, 489, 499), "MEX": (395, 415, 410), "MYS": (409, 388, 416),
             "OECD_MED": (472, 476, 485)}
# "İnsanların çoğuna güvenilir" (%) — Integrated Values Surveys (WVS+EVS) 2024, OWID; 2022 = 7. dalga
WVS_2022 = {"TUR": 13.99586, "KOR": 32.93173, "ESP": 40.96439, "PRT": 16.91347, "GRC": 8.447196,
            "POL": 24.11202, "MEX": 10.48835, "MYS": 19.5735}
KARSI = ["TUR", "KOR", "ESP", "PRT", "GRC", "POL", "MEX", "MYS"]
OECD = ["AUS", "AUT", "BEL", "CAN", "CHL", "COL", "CRI", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC",
        "HUN", "ISL", "IRL", "ISR", "ITA", "JPN", "KOR", "LVA", "LTU", "LUX", "MEX", "NLD", "NZL", "NOR",
        "POL", "PRT", "SVK", "SVN", "ESP", "SWE", "CHE", "TUR", "GBR", "USA"]


def manuel_satirlar() -> pd.DataFrame:
    s = []
    for g, d in WGI_2023.items():
        for u in KARSI:
            s.append((u, g, WGI_KOD[g], 2023, d[u], f"World Bank WGI, 2023 verisi ({WGI_KOD[g]}); 2024 verisi yayımlandı, V2 yeniden çekimde güncellenecek"))
        med = float(pd.Series([d[u] for u in OECD]).median())
        s.append(("OECD_MED", g, WGI_KOD[g], 2023, med, "Kök Neden hesaplaması: 38 OECD üyesinin ortancası"))
    for u, (m, o, f) in PISA_2022.items():
        kaynak = "OECD (2023) PISA 2022 Results Vol. I, Tablo I.1" + (" — OECD ortalaması" if u == "OECD_MED" else "")
        s.append((u, "G001", "PISA_MEAN", 2022, (m + o + f) / 3, kaynak))
    for u, v in WVS_2022.items():
        s.append((u, "G023", "WVS_TRUST", 2022, v, "Integrated Values Surveys (2024) via Our World in Data; 7. dalga (2017-2022; OWID yılı dalga bitişi, TR saha çalışması 2018)"))
    return pd.DataFrame(s, columns=["ulke", "gosterge_id", "kod", "yil", "deger", "kaynak"])


def main() -> None:
    VERI.mkdir(parents=True, exist_ok=True)
    ids = [s[0] for s in SORUNLAR]
    pd.DataFrame(SORUNLAR, columns=["sorun_id", "sutun", "ad", "kisa_ad", "ana_gosterge", "yedek_gosterge",
                                    "etki_duzey", "etki_gerekce"]).assign(
        # Konuya göre karşılaştırma seti (kararlar.md): deprem için depreme maruz OECD ülkeleri
        karsilastirma_seti=lambda d: d.sorun_id.map({"S17": "JPN;CHL;ITA;GRC;MEX;NZL;USA"}).fillna("")
    ).to_csv(VERI / "sorunlar.csv", index=False)
    g = pd.DataFrame(BAGLANTILAR, columns=["kaynak", "hedef", "puan", "durum", "anahtar", "gerekce"])
    assert not g.duplicated(["kaynak", "hedef"]).any(), "Tekrarlanan bağlantı"
    assert set(g.kaynak) | set(g.hedef) <= set(ids)
    assert (g.kaynak != g.hedef).all()
    eksik = {k for a in g.anahtar for k in a} - set(KAYNAK)
    assert not eksik, eksik
    guclu_kaynaksiz = g[(g.puan >= 3) & (g.anahtar.str.len() == 0)]
    assert guclu_kaynaksiz.empty, "3-4 puanlı bağlantının kaynağı yok"
    g["kaynakca"] = g.anahtar.apply(lambda a: " | ".join(KAYNAK[k][0] for k in a))
    g["doi_url"] = g.anahtar.apply(lambda a: " | ".join(KAYNAK[k][1] for k in a if KAYNAK[k][1]))
    g["anahtar"] = g.anahtar.apply(";".join)
    g.insert(0, "baglanti_id", [f"{a}>{b}" for a, b in zip(g.kaynak, g.hedef)])
    g["surum"] = SURUM
    g.to_csv(VERI / "baglanti_gerekceleri.csv", index=False)

    M = pd.DataFrame(0, index=pd.Index(ids, name="etkileyen"), columns=ids)
    for r in g.itertuples():
        M.loc[r.kaynak, r.hedef] = r.puan
    M.to_csv(VERI / f"etki_matrisi_{SURUM}.csv")
    M.to_csv(VERI / "etki_matrisi.csv")  # çalıştırıcının beklediği ad

    pd.DataFrame([(k, v[0], v[1]) for k, v in KAYNAK.items()],
                 columns=["anahtar", "kunye", "doi_url"]).to_csv(VERI / "kaynakca.csv", index=False)

    man = manuel_satirlar()
    man.to_csv(VERI / "manuel_ek.csv", index=False)
    v2 = pd.read_csv(V2_VERI / "gostergeler_zaman_serisi.csv")
    vdem = pd.read_csv(V2_VERI / "vdem_secilmis.csv")  # 03: V-Dem v16, OECD ortancası Türkiye hariç
    deprem = pd.read_csv(V2_VERI / "deprem_olum_ulke.csv")  # 03: EM-DAT, 2002–2025, deprem ülkeleri
    pd.concat([v2, man, vdem, deprem], ignore_index=True).to_csv(VERI / "gostergeler.csv", index=False)
    liste = pd.read_csv(V2_KOD / "gosterge_listesi.csv")
    ek = pd.DataFrame([
        {"gosterge_id": "G061", "sorun_id": "S24", "rol": "ana", "ad": "Siyasi kutuplaşma (V-Dem)", "kaynak": "vdem", "kod": "v2cacamps", "birim": "z", "yon": -1, "not": "v0.2"},
        {"gosterge_id": "G062", "sorun_id": "S25", "rol": "ana", "ad": "Sosyal gruba göre dışlanma (V-Dem)", "kaynak": "vdem", "kod": "v2xpe_exlsocgr", "birim": "0..1", "yon": -1, "not": "v0.2"},
        {"gosterge_id": "G063", "sorun_id": "S26", "rol": "ana", "ad": "Karşı argümana saygı (V-Dem)", "kaynak": "vdem", "kod": "v2dlcountr", "birim": "z", "yon": 1, "not": "v0.2"},
    ])
    liste = pd.concat([liste[~liste.gosterge_id.isin(ek.gosterge_id)], ek], ignore_index=True)
    liste.loc[liste.gosterge_id.isin(["G013", "G018", "G024"]), "yon"] = 1
    liste.loc[liste.kaynak == "wgi", "kod"] = liste.loc[liste.kaynak == "wgi", "kod"].str.replace(
        r"^(?!GOV_WGI_)", "GOV_WGI_", regex=True)
    liste.to_csv(VERI / "gosterge_listesi.csv", index=False)
    print(f"{len(ids)} sorun, {len(g)} bağlantı ({(g.puan >= 3).sum()} güçlü), "
          f"durum: {g.durum.value_counts().to_dict()}")


if __name__ == "__main__":
    main()
