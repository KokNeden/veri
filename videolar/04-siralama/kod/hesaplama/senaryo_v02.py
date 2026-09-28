"""v0.2 karar senaryoları: her kararın ilk 5'i değiştirip değiştirmediği (n=2000)."""
import shutil, subprocess, sys, tempfile
from pathlib import Path
import pandas as pd

KOK = Path(__file__).resolve().parents[1]
PY = sys.executable
SENARYO = {
    "taban (v0.2)": [],
    "(karar sonrası) S09→S07 3→4": [("S09", "S07", 4)],
    "B9 denetim (5 bağ bir puan aşağı)": [("S16", "S17", 3), ("S21", "S22", 2), ("S18", "S21", 2), ("S13", "S19", 2), ("S12", "S09", 2)],
    "B10 eksik bağlar": [("S09", "S06", 2), ("S01", "S05", 2), ("S21", "S14", 1), ("S19", "S17", 1), ("S11", "S09", 1)],
    "B8 eğitim→kurumlar": [("S01", "S06", 1), ("S01", "S09", 1)],
    "S12→S24 3→2 (ABD kanıtı)": [("S12", "S24", 2)],
    "S25→S11 3→2": [("S25", "S11", 2)],
    "yalnız kaynaklı (1–2 sil)": "yalniz_kaynakli",
}

def calistir(degisim):
    with tempfile.TemporaryDirectory() as d:
        g = Path(d) / "veri"; shutil.copytree(KOK / "veri", g)
        M = pd.read_csv(g / "etki_matrisi.csv", index_col=0)
        if degisim == "yalniz_kaynakli":
            M[M < 3] = 0
        else:
            for a, b, p in degisim:
                M.loc[a, b] = p
        M.to_csv(g / "etki_matrisi.csv")
        c = Path(d) / "c"
        (g / "baglanti_gerekceleri.csv").unlink(missing_ok=True)  # senaryoda gerekçe tablosu matrisle eşleşmez
        r = subprocess.run([PY, "-m", "kokneden_siralama.calistir", "--girdi", g, "--cikti", c, "--n", "2000", "--etiket", "s"],
                           capture_output=True, text=True, env={"PYTHONPATH": str(KOK.parent / "04-siralama-yontemi/kod"), "PATH": "/usr/bin:/bin"})
        if r.returncode:
            return [r.stderr.strip().splitlines()[-1][:120]]
        s = pd.read_csv(c / "sonuclar_s.csv").sort_values("sira")
        return list(s.sorun_id.head(7))

for ad, dg in SENARYO.items():
    print(f"{ad:38} {' '.join(calistir(dg))}")
