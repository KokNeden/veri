"""V-Dem değişkenleri için dört dönemlik kronik testi.

Kullanım (03-kronik-sorunlar/ içinden):  python3 kod/vdem_donem.py
Girdi : veri/ham/V-Dem-CY-FullOthers-v16_csv.zip
Çıktı : veri/vdem_kronik.csv (sorun, değişken, dönem, Türkiye, set ve OECD ortancası, sorun yönünde ayrışma)

Kural (kararlar.md, 26.09.2026): dört dönemin en az üçünde Türkiye'nin OECD ortancasından
sorun yönünde ayrışması. OECD ortancası bugünkü üyelerle (Türkiye hariç) geriye doğru hesaplanır.
"""
import csv
import io
import statistics as st
import zipfile

# (sorun, değişken, yön, kısa ad) · yön +1: yüksek değer iyi, -1: yüksek değer sorun
DEGISKENLER = [
    ("S06", "v2x_rule", 1, "Hukukun üstünlüğü endeksi"),
    ("S06", "v2juhcind", 1, "Yüksek mahkeme bağımsızlığı"),
    ("S08", "v2ellocpwr", 1, "Yerel seçilmiş organların gücü"),
    ("S09", "v2stcritrecadm", 1, "Kamuya atamada liyakat"),
    ("S09", "v2clrspct", 1, "Tarafsız ve kurallı kamu yönetimi"),
    ("S09", "v2x_corr", -1, "Siyasi yolsuzluk endeksi"),
    ("S12", "v2x_freexp_altinf", 1, "İfade özgürlüğü ve alternatif bilgi kaynakları"),
    ("S12", "v2mecenefm", 1, "Medyada hükümet sansürü çabası (yüksek = az sansür)"),
    ("S24", "v2cacamps", -1, "Siyasi kutuplaşma"),
    ("S25", "v2xpe_exlsocgr", -1, "Sosyal gruba göre dışlanma"),
    ("S26", "v2dlcountr", 1, "Karşı argümana saygı"),
]
SET = ["KOR", "ESP", "PRT", "GRC", "POL", "MEX", "MYS"]
OECD = ["AUS", "AUT", "BEL", "CAN", "CHL", "COL", "CRI", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "ISL",
        "IRL", "ISR", "ITA", "JPN", "KOR", "LVA", "LTU", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT", "SVK", "SVN",
        "ESP", "SWE", "CHE", "GBR", "USA"]
DONEMLER = [(1923, 1949, "1923–1950"), (1950, 1979, "1950–1980"), (1980, 2001, "1980–2002"), (2002, 2025, "2002–2025")]

z = zipfile.ZipFile("veri/ham/V-Dem-CY-FullOthers-v16_csv.zip")
f = io.TextIOWrapper(z.open("V-Dem-CY-Full+Others-v16.csv"), encoding="utf-8")
r = csv.reader(f)
bas = next(r)
eksik = [v for _, v, _, _ in DEGISKENLER if v not in bas]
if eksik:
    raise SystemExit(f"Veri setinde yok: {eksik}")
ci, yi = bas.index("country_text_id"), bas.index("year")
vi = {v: bas.index(v) for _, v, _, _ in DEGISKENLER}
veri = {}
ulkeler = set(SET) | set(OECD) | {"TUR"}
for row in r:
    c = row[ci]
    if c not in ulkeler:
        continue
    y = int(row[yi])
    if y < 1923:
        continue
    for v, i in vi.items():
        if row[i] != "":
            veri.setdefault((v, c), {})[y] = float(row[i])


def ort(v, c, a, b):
    d = veri.get((v, c), {})
    xs = [d[y] for y in range(a, b + 1) if y in d]
    return st.mean(xs) if xs else None


satirlar = []
for sorun, v, yon, ad in DEGISKENLER:
    kotu = 0
    olculen = 0
    print(f"\n{sorun} · {ad} ({v}) · yön {'+' if yon > 0 else '−'}")
    for a, b, dad in DONEMLER:
        tr = ort(v, "TUR", a, b)
        s = [x for x in (ort(v, c, a, b) for c in SET) if x is not None]
        o = [x for x in (ort(v, c, a, b) for c in OECD) if x is not None]
        so, oo = (st.median(s) if s else None), (st.median(o) if o else None)
        ayrisma = None
        if tr is not None and oo is not None:
            olculen += 1
            ayrisma = (tr - oo) * yon < 0
            kotu += ayrisma
        fm = lambda x: "—" if x is None else f"{x:.2f}"
        print(f"  {dad}: TR {fm(tr)} | set {fm(so)} | OECD {fm(oo)} | {'KÖTÜ' if ayrisma else ('iyi' if ayrisma is False else '—')}")
        satirlar.append([sorun, v, ad, dad, fm(tr), fm(so), fm(oo), "" if ayrisma is None else int(ayrisma)])
    print(f"  → {kotu}/{olculen} dönemde OECD ortancasından sorun yönünde · {'KRONİK' if kotu >= 3 else 'kronik değil'}")

with open("veri/vdem_kronik.csv", "w", newline="") as g:
    w = csv.writer(g)
    w.writerow(["sorun", "degisken", "ad", "donem", "turkiye", "set_ortancasi", "oecd_ortancasi", "sorun_yonunde"])
    w.writerows(satirlar)
