"""05 videosunun grafik verisi: ham CSV'lerden video/src/videolar/05-kurallar-tarih/veri/veriler.ts üretir.
Rakamlar elle yazılmaz (VIDEO-YAPIM §3). Kullanım: python3 icerik/05-kurallar-tarih/kod/video_verisi.py
"""
import csv
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
HEDEF = KOK.parents[1] / "video" / "src" / "videolar" / "05-kurallar-tarih" / "veri" / "veriler.ts"


def seri(degisken):
    satirlar = [s for s in csv.DictReader(open(KOK / "veri" / "vdem_yargi_kamu_yillik.csv")) if s["degisken"] == degisken]
    tr = [(int(s["yil"]), round(float(s["turkiye"]), 3)) for s in satirlar if int(s["yil"]) >= 1923 and s["turkiye"]]
    oecd = [(int(s["yil"]), round(float(s["oecd_ortancasi"]), 3)) for s in satirlar if int(s["yil"]) >= 1923 and s["oecd_ortancasi"]]
    return tr, oecd


def ts(liste):
    return "[" + ", ".join(f"[{a}, {b}]" for a, b in liste) + "]"


kural_tr, kural_oecd = seri("v2x_rule")
kamu_tr, kamu_oecd = seri("v2clrspct")
dava = [
    (int(s["yil"]), int(s["gelen_dava"]), int(s["gelecek_yila_devreden"]))
    for s in csv.DictReader(open(KOK / "veri" / "ham" / "tuik_mahkeme_dava_1967_2010.csv"))
]
oranlar = [d / g for _, g, d in dava]
aihm = [
    (int(s["donem_sonu"][-4:]), int(s["kumulatif_toplam_karar"]))
    for s in csv.DictReader(open(KOK / "veri" / "ham" / "aihm_turkiye_kumulatif.csv"))
]

HEDEF.parent.mkdir(parents=True, exist_ok=True)
HEDEF.write_text(
    f"""// Üretildi: icerik/05-kurallar-tarih/kod/video_verisi.py — elle düzenlenmez.
// V-Dem v16 (Türkiye ve bugünkü OECD üyelerinin ortancası, Türkiye hariç), 1923–2025.
export const kuralTR = {ts(kural_tr)} as const;
export const kuralOECD = {ts(kural_oecd)} as const;
export const kamuTR = {ts(kamu_tr)} as const;
export const kamuOECD = {ts(kamu_oecd)} as const;

// TÜİK İstatistik Göstergeler 1923–2011, Tablo 6.2: [yıl, mahkemelerin önündeki dava (devir dahil), ertesi yıla devreden]
export const dava = {ts([(y, f"{g}, {d}") for y, g, d in dava]).replace("'", "")} as const;
// AİHM, Türkiye hakkında kümülatif karar sayısı (1959'dan dönem sonuna): [yıl, karar]
export const aihmKumulatif = {ts(aihm)} as const;
export const devirOrani = {{en_dusuk: {min(oranlar):.3f}, en_yuksek: {max(oranlar):.3f}, ortalama: {sum(oranlar) / len(oranlar):.3f}}} as const;
""",
    encoding="utf-8",
)
print(HEDEF, len(kural_tr), "yıl V-Dem,", len(dava), "yıl dava")
