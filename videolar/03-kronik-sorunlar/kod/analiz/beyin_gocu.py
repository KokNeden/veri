"""S03 Beyin göçü: yükseköğrenimli göç oranı, Türkiye ve karşılaştırma ortancaları.

Kullanım (03-kronik-sorunlar/ içinden):  python3 kod/beyin_gocu.py
Girdi : veri/ham/iab_brain_drain_emigration.csv (IAB Brain Drain Data 1980–2010, Brücker, Capuano, Marfouk 2013;
        25 yaş üstü, 20 OECD varış ülkesi; kaynak .xls'ten düz CSV'ye çevrildi)
Çıktı : veri/beyin_gocu.csv

Ölçü: yükseköğrenimli göç oranı = yurt dışındaki yükseköğrenimli / (yurt içi + yurt dışı yükseköğrenimli).
İkinci ölçü: seçicilik = yükseköğrenimli göç oranı / toplam göç oranı (1'den büyükse göç eğitimlilerde yoğun).
Yön: yüksek kötü. Dönemler: 1980–2002 (1980, 1985, 1990, 1995, 2000), 2002+ (2005, 2010). Önceki dönemler ölçülmez.
"""
import csv
import statistics as st
from collections import defaultdict

SET = ["Korea", "Spain", "Portugal", "Greece", "Poland", "Mexico", "Malaysia"]
# Bugünkü OECD üyeleri, Türkiye hariç (IAB adlarıyla)
OECD = ["Australia", "Austria", "Belgium", "Canada", "Chile", "Colombia", "Costa Rica", "Czech Republic", "Denmark",
        "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Israel", "Italy", "Japan",
        "Korea", "Latvia", "Lithuania", "Luxembourg", "Mexico", "Netherlands", "New Zealand", "Norway", "Poland",
        "Portugal", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "United Kingdom", "United States"]
DONEMLER = [("1980–2002", [1980, 1985, 1990, 1995, 2000]), ("2002–2026", [2005, 2010])]

d = defaultdict(dict)
for r in csv.DictReader(open("veri/ham/iab_brain_drain_emigration.csv")):
    d[(r["ulke"], r["egitim"])][int(r["yil"])] = float(r["goc_orani"])


def olc(ulke, yillar, secicilik=False):
    xs = []
    for y in yillar:
        h = d[(ulke, "High")].get(y)
        t = d[(ulke, "Total")].get(y)
        if h is None or (secicilik and not t):
            continue
        xs.append(h / t if secicilik else h * 100)
    return st.mean(xs) if xs else None


satir = []
for ad, sec in (("Yükseköğrenimli göç oranı (%)", False), ("Seçicilik (yükseköğrenimli / toplam göç oranı)", True)):
    for donem, yillar in DONEMLER:
        tr = olc("Turkey", yillar, sec)
        so = st.median([x for x in (olc(c, yillar, sec) for c in SET) if x is not None])
        oe = st.median([x for x in (olc(c, yillar, sec) for c in OECD) if x is not None])
        satir.append([ad, donem, f"{tr:.3g}", f"{so:.3g}", f"{oe:.3g}", int(tr > oe)])
    for y in sorted(d[("Turkey", "High")]):
        satir.append([ad, str(y), f"{olc('Turkey', [y], sec):.3g}", f"{st.median([olc(c, [y], sec) for c in SET]):.3g}",
                      f"{st.median([olc(c, [y], sec) for c in OECD]):.3g}", ""])
with open("veri/beyin_gocu.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["olcu", "donem_ya_da_yil", "turkiye", "set_ortancasi", "oecd_ortancasi", "sorun_yonunde"])
    w.writerows(satir)
for s in satir:
    print(" | ".join(map(str, s)))
