"""04 videosunun grafik verisini sıralama çıktılarından üretir (elle kopyalama yok).
Çıktı: video/src/videolar/04-siralama/veri/siralama.ts
Kullanım (05-siralama-sonucu/ içinden): ../04-siralama-yontemi/kod/.venv/bin/python kod/video_verisi.py
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parents[1]
HEDEF = KOK.parents[1] / "video" / "src" / "videolar" / "04-siralama" / "veri" / "siralama.ts"
import sys
sys.path.insert(0, str(KOK.parent / "04-siralama-yontemi" / "kod"))
from kokneden_siralama.dematel import dematel  # noqa: E402

s = pd.read_csv(KOK / "cikti/sonuclar_v0.2.csv").sort_values("sira")
d = pd.read_csv(KOK / "cikti/duyarlilik_v0.2.csv").drop(columns=["sira"])
m = s.merge(d, on="sorun_id")
sor = pd.read_csv(KOK / "veri/sorunlar.csv")
kisa = dict(zip(sor.sorun_id, sor.kisa_ad))
sutun = dict(zip(sor.sorun_id, sor.sutun))
g = pd.read_csv(KOK / "veri/baglanti_gerekceleri.csv")
M = pd.read_csv(KOK / "veri/etki_matrisi.csv", index_col=0)

sorunlar = [{"id": r.sorun_id, "ad": kisa[r.sorun_id], "sutun": sutun[r.sorun_id], "sira": int(r.sira), "D": round(r.D, 3),
             "R": round(r.R, 3), "net": round(r.D_eksi_R, 3), "oncelik": round(r.oncelik_skoru, 3),
             "ilk5": round(r.ilk5_olasilik, 3), "birinci": round(r.birinci_olasilik, 3)} for r in m.itertuples()]
baglar = [{"a": r.kaynak, "b": r.hedef, "p": int(r.puan), "d": r.durum} for r in g.itertuples()]

A = np.array([[0, 4, 1, 1], [0, 0, 3, 3], [0, 1, 0, 2], [0, 0, 0, 0]], float)
o = dematel(A)
oyuncak = {"ad": ["Kaçak", "Nem", "Küf", "Boya"], "A": A.astype(int).tolist(), "T": np.round(o.T, 2).tolist(),
           "D": np.round(o.D, 2).tolist(), "R": np.round(o.R, 2).tolist(), "dogrudan": round(A[0, 3] / 6, 2), "toplam": round(float(o.T[0, 3]), 2)}

sen = {}
for satir in (KOK / "cikti/senaryolar_v0.2.txt").read_text().splitlines():
    ad, ids = satir[:38].strip(), satir[38:].split()
    sen[ad] = ids
tek = pd.read_csv(KOK / "cikti/baglanti_etkisi_v0.2.csv")
tek = [{"a": r.kaynak, "b": r.hedef, "degisti": bool(r.ilk5_degisti)} for r in tek.itertuples()]

veri = {"sorunlar": sorunlar, "baglar": baglar, "oyuncak": oyuncak, "hucre": int(M.shape[0] * (M.shape[0] - 1)),
        "dolu": int((M.values > 0).sum()), "guclu": int((g.puan >= 3).sum()),
        "yalnizGuclu": sen.get("yalnız kaynaklı (1–2 sil)", []), "tekBag": tek}
HEDEF.write_text("// Otomatik üretildi: icerik/05-siralama-sonucu/kod/video_verisi.py (sıralama v0.2). Elle düzenleme.\n"
                 f"export const veri = {json.dumps(veri, ensure_ascii=False, indent=1)} as const;\n")
print(HEDEF, len(sorunlar), "sorun", len(baglar), "bağ")
