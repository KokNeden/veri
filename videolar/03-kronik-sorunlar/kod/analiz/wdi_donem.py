"""Dünya Bankası (WDI/WGI) göstergeleri için dört dönemlik kronik testi.

Kullanım (03-kronik-sorunlar/ içinden):  python3 kod/wdi_donem.py
Girdi : veri/gostergeler_zaman_serisi.csv (kod/veri_cek.py), kod/gosterge_listesi.csv (yön: 1 yüksek iyi, -1 yüksek kötü)
Çıktı : veri/wdi_kronik.csv

Kural (kararlar.md): dört dönemin en az üçünde Türkiye'nin OECD ortancasından (Türkiye hariç,
bugünkü üyeler) sorun yönünde ayrışması. WDI 1960'ta başladığı için 1923–1950 dönemi ölçülmez;
1950–1980 dönemi yalnız 1960–1979 yıllarıyla temsil edilir. Ölçülen dönem sayısı üçten azsa
"ölçüm sınırlı" kuralı uygulanır (mevcut dönemlerin hepsinde sorun → listede kalır).
"""
import csv
import statistics as st
from collections import defaultdict

DONEMLER = [(1923, 1949, "1923–1950"), (1950, 1979, "1950–1980"), (1980, 2001, "1980–2002"), (2002, 2026, "2002–2026")]
SET = ["KOR", "ESP", "PRT", "GRC", "POL", "MEX", "MYS"]

gosterge = {r["gosterge_id"]: r for r in csv.DictReader(open("kod/gosterge_listesi.csv"))}
seri = defaultdict(dict)  # (gid, ülke) -> {yıl: değer}
for r in csv.DictReader(open("veri/gostergeler_zaman_serisi.csv")):
    if r["deger"] in ("", None):
        continue
    seri[(r["gosterge_id"], r["ulke"])][int(float(r["yil"]))] = float(r["deger"])


def ort(gid, ulke, a, b):
    d = seri.get((gid, ulke), {})
    xs = [d[y] for y in range(a, b + 1) if y in d]
    return st.mean(xs) if xs else None


satirlar = []
ozet = []
for gid, g in gosterge.items():
    yon = int(g["yon"]) if g["yon"] not in ("", None) else 1
    kotu = olculen = 0
    for a, b, ad in DONEMLER:
        tr, oe = ort(gid, "TUR", a, b), ort(gid, "OECD_MED", a, b)
        s = [x for x in (ort(gid, c, a, b) for c in SET) if x is not None]
        so = st.median(s) if s else None
        ayr = None
        if tr is not None and oe is not None:
            olculen += 1
            ayr = (tr - oe) * yon < 0
            kotu += ayr
        f = lambda x: "" if x is None else f"{x:.4g}"
        satirlar.append([g["sorun_id"], gid, g["rol"], g["ad"], ad, f(tr), f(so), f(oe), "" if ayr is None else int(ayr)])
    if olculen >= 3:
        sonuc = "KRONİK" if kotu >= 3 else "kronik değil"
    elif olculen > 0:
        sonuc = "ölçüm sınırlı · hepsinde sorun" if kotu == olculen else "ölçüm sınırlı · sorun her dönemde yok"
    else:
        sonuc = "veri yok"
    ozet.append((g["sorun_id"], gid, g["rol"], g["ad"], kotu, olculen, sonuc))

with open("veri/wdi_kronik.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["sorun", "gosterge", "rol", "ad", "donem", "turkiye", "set_ortancasi", "oecd_ortancasi", "sorun_yonunde"])
    w.writerows(satirlar)
for s, gid, rol, ad, k, o, sonuc in sorted(ozet):
    print(f"{s:8} {gid} {rol:8} {k}/{o} {sonuc:40} {ad[:60]}")
