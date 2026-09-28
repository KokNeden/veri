"""Plan hedefi tablolarını birleştirir ve her alıntıyı plan metnine karşı doğrular.

Kullanım (03-kronik-sorunlar/ içinden):
    python3 kod/plan_hedef_dogrula.py <çıktı.csv> <parça1.csv> [parça2.csv ...]

Her satır için alıntı, belirtilen dosyanın belirtilen sayfasında (± 1 sayfa) aranır.
Karşılaştırma: küçük harf, Türkçe karakterler sadeleştirilmiş, boşluk ve satır sonu tireleri kaldırılmış.
Tam eşleşme yoksa alıntının 6 kelimelik pencerelerinden en az yarısı aranır (OCR ve tablo
satırı birleştirmeleri için). Sütun başlığı eklemeleri (" | " sonrası) arama dışında tutulur.

Çıktıya iki sütun eklenir: dogrulama (tam / kismi / bulunamadi / hedef_yok) ve dogrulama_sayfa.
"""
import csv
import re
import sys
import unicodedata

PLAN_DIR = "veri/ham/planlar"


def sade(s):
    s = s.lower().replace("ı", "i").replace("İ", "i")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"-\s*\n\s*", "", s)
    return re.sub(r"[^a-z0-9%,.]+", "", s)


sayfa_onbellek = {}


def sayfalar(dosya):
    if dosya not in sayfa_onbellek:
        t = open(f"{PLAN_DIR}/{dosya}", encoding="utf-8").read()
        parca = re.split(r"\n=== S(\d+) ===\n", t)
        d = {}
        for i in range(1, len(parca), 2):
            d[int(parca[i])] = sade(parca[i + 1])
        sayfa_onbellek[dosya] = d
    return sayfa_onbellek[dosya]


def dogrula(satir):
    alinti = satir["alinti"]
    if not satir.get("hedef_degeri") and ("bulunamad" in alinti.lower()):
        return "hedef_yok", ""
    dosya = satir["dosya"].split("/")[-1]
    try:
        s0 = int(re.sub(r"\D", "", satir["pdf_sayfa"]) or 0)
    except ValueError:
        s0 = 0
    try:
        sp = sayfalar(dosya)
    except FileNotFoundError:
        return "dosya_yok", ""
    aday = [s0, s0 - 1, s0 + 1] if s0 else list(sp)
    en_iyi = (0.0, "", "")
    # Sütun başlığı " | " ile başa ya da sona eklenmiş olabilir: her parça ayrı denenir.
    for govde in alinti.split(" | "):
        if govde.strip().lower().startswith("sütunlar"):
            continue
        govde = re.sub(r"\(?(belirsiz|not)[:：].*$", "", govde, flags=re.I)
        govde = govde.replace("...", " ").replace("…", " ")
        hedef = sade(govde)
        if len(hedef) >= 12:
            for s_ in aday:
                if s_ in sp and hedef in sp[s_]:
                    return "tam", str(s_)
        kel = [k for k in re.split(r"\s+", govde) if k]
        pencere = [sade(" ".join(kel[i:i + 6])) for i in range(0, max(1, len(kel) - 5), 3)]
        pencere = [p_ for p_ in pencere if len(p_) >= 10]
        # Tablo satırları: sayılar PDF'te sütunlara dağılır; alıntıdaki sayıların sayfada geçme oranı
        sayilar = [sade(x) for x in re.findall(r"\d[\d.,]*\d|\d", govde)]
        sayilar = [x for x in sayilar if len(x) >= 2]
        for s_ in aday:
            if s_ not in sp:
                continue
            if pencere:
                r = sum(1 for p_ in pencere if p_ in sp[s_]) / len(pencere)
                if r > en_iyi[0]:
                    en_iyi = (r, str(s_), "metin")
            if len(sayilar) >= 3:
                r = sum(1 for x in sayilar if x in sp[s_]) / len(sayilar)
                if r > en_iyi[0]:
                    en_iyi = (r, str(s_), "tablo")
    if en_iyi[0] >= 0.8 and en_iyi[2] == "tablo":
        return "tablo_sayilari", en_iyi[1]
    if en_iyi[0] >= 0.5 and en_iyi[2] == "metin":
        return "kismi", en_iyi[1]
    return "bulunamadi", ""


cikti, *parcalar = sys.argv[1:]
satirlar = []
bas = None
for p in parcalar:
    r = list(csv.DictReader(open(p, encoding="utf-8")))
    bas = bas or list(r[0].keys())
    satirlar += r
from collections import Counter

sayac = Counter()
for s in satirlar:
    s["dogrulama"], s["dogrulama_sayfa"] = dogrula(s)
    sayac[s["dogrulama"]] += 1
satirlar.sort(key=lambda s: (s["sorun_id"], int(re.sub(r"\D", "", str(s["plan_no"])) or 0)))
with open(cikti, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=bas + ["dogrulama", "dogrulama_sayfa"], quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    w.writerows(satirlar)
print(len(satirlar), "satır ·", dict(sayac))
for s in satirlar:
    if s["dogrulama"] in ("bulunamadi", "dosya_yok"):
        print("  ✗", s["sorun_id"], "plan", s["plan_no"], "S", s["pdf_sayfa"], "|", s["alinti"][:110])
