"""cikti/ altındaki CSV'lerden markdown tablolar üretir ve şablon dosyalardaki {{...}} yer tutucularını doldurur.

    python kod/rapor_tablolari.py sablon.md hedef.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

KOK = Path(__file__).resolve().parents[1]
C, V = KOK / "cikti", KOK / "veri"


def f(x, n=2):
    if abs(x) < 0.5 * 10 ** -n:
        x = 0.0
    return f"{x:.{n}f}".replace(".", ",")


def yuzde(x):
    return f"%{x * 100:.0f}"


def yorum(p):
    return "sağlam" if p >= .8 else "büyük olasılıkla" if p >= .5 else "sınırda" if p >= .2 else "ilk 5'te değil"


def tablolar() -> dict[str, str]:
    s = pd.read_csv(C / "sonuclar_v0.1.csv")
    d = pd.read_csv(C / "duyarlilik_v0.1.csv").set_index("sorun_id")
    a = pd.read_csv(C / "acik_skorlari_v0.1.csv").set_index("sorun_id")
    so = pd.read_csv(V / "sorunlar.csv").set_index("sorun_id")
    sc = pd.read_csv(C / "senaryolar_v0.1.csv")
    ism = pd.read_csv(C / "ism_esik_duyarliligi_v0.1.csv")
    be = pd.read_csv(C / "baglanti_etkisi_v0.1.csv")
    meta = json.loads((C / "meta_v0.1.json").read_text())
    liste = pd.read_csv(V / "gosterge_listesi.csv").set_index("gosterge_id")
    out = {}

    r = ["| Sıra | Sorun | Grup | D | R | D−R | Kök (K) | Açık (A) | Etki (E) | Öncelik | İlk 5 olasılığı | Yorum |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in s.itertuples():
        dd = d.loc[x.sorun_id]
        acik = f(x.acik_skoru) + ("" if x.acik_veri else " *(bilmiyoruz)*")
        r.append(f"| {x.sira} | {x.sorun_id} {so.loc[x.sorun_id, 'kisa_ad']} | {x.grup} | {f(x.D)} | {f(x.R)} | "
                 f"{f(x.D_eksi_R)} | {f(x.kok_skoru)} | {acik} | {f(x.etki_skoru)} | {f(x.oncelik_skoru)} | "
                 f"{yuzde(dd.ilk5_olasilik)} | {yorum(dd.ilk5_olasilik)} |")
    out["TABLO_SONUC"] = "\n".join(r)

    r = ["| Sorun | Taban sıra | Sıra aralığı (%5-%95) | İlk 5 | 1. olma | Neden grubunda | İlk 5 · yalnız matris | İlk 5 · yalnız ağırlık/yöntem |",
         "|---|---|---|---|---|---|---|---|"]
    for sid, x in d.sort_values("sira").head(10).iterrows():
        r.append(f"| {sid} {so.loc[sid, 'kisa_ad']} | {int(x.sira)} | {x.sira_p05:.0f}–{x.sira_p95:.0f} | {yuzde(x.ilk5_olasilik)} | "
                 f"{yuzde(x.birinci_olasilik)} | {yuzde(x.neden_grubu_olasilik)} | {yuzde(x.ilk5_yalniz_matris)} | "
                 f"{yuzde(x.ilk5_yalniz_agirlik_yontem)} |")
    out["TABLO_DUYARLILIK"] = "\n".join(r)

    r = ["| Sorun | Gösterge | Yıl | Türkiye | Set ortancası | n | z | A = Φ(z) | Not |", "|---|---|---|---|---|---|---|---|---|"]
    for sid, x in a.iterrows():
        if pd.isna(x.A_phi):
            r.append(f"| {sid} {so.loc[sid, 'kisa_ad']} | — | — | — | — | — | — | — | {x['not']} |")
            continue
        ad = liste.loc[x.gosterge_id, "ad"]
        r.append(f"| {sid} {so.loc[sid, 'kisa_ad']} | {x.gosterge_id} {ad} | {x.yil:.0f} | {f(x.tur)} | {f(x.ortanca)} | "
                 f"{x.n_set:.0f} | {f(x.z)} | {f(x.A_phi)} | {'' if pd.isna(x['not']) else 'vekil (yedek gösterge)'} |")
    out["TABLO_ACIK"] = "\n".join(r)

    r = ["| Senaryo | İlk 5 | Açıklama |", "|---|---|---|"]
    for x in sc.itertuples():
        r.append(f"| `{x.senaryo}` | {x.ilk5} | {x.aciklama} |")
    out["TABLO_SENARYO"] = "\n".join(r)

    r = ["| k | Eşik | Bağlantı | Katman sayısı | En derin katman |", "|---|---|---|---|---|"]
    for x in ism.itertuples():
        r.append(f"| {f(x.k, 1)} | {f(x.esik, 4)} | {x.bag_sayisi} | {x.katman_sayisi} | {x.en_derin_katman.replace(';', ', ')} |")
    out["TABLO_ISM"] = "\n".join(r)

    out["TAU_ORTANCA"] = f(meta["tau_ortanca"])
    out["TAU_P05"] = f(meta["tau_p05"])
    out["TAU_MATRIS"] = f(meta["parcalar"]["yalniz_matris"]["tau_ortanca"])
    out["TAU_AGIRLIK"] = f(meta["parcalar"]["yalniz_agirlik_yontem"]["tau_ortanca"])
    out["BE_N"] = str(len(be))
    out["BE_DEGISEN"] = str(int(be.ilk5_degisti.sum()))
    out["BE_MIN_TAU"] = f(be.tau.min())
    M = pd.read_csv(V / "etki_matrisi_v0.1.csv", index_col=0)
    g = pd.read_csv(V / "baglanti_gerekceleri.csv").set_index("baglanti_id")
    isaret = {"tartismali": "◆", "zayif": "○"}
    r = ["| ↓ etkileyen / etkilenen → | " + " | ".join(M.columns) + " |", "|---|" + "---|" * len(M.columns)]
    for i in M.index:
        hucre = []
        for j in M.columns:
            p = int(M.loc[i, j])
            d_ = g.durum.get(f"{i}>{j}", "") if p else ""
            hucre.append("·" if i == j else (f"{p}{isaret.get(d_, '')}" if p else ""))
        r.append(f"| **{i}** {so.loc[i, 'kisa_ad']} | " + " | ".join(hucre) + " |")
    out["TABLO_MATRIS"] = "\n".join(r)
    out["SORUN_KODLARI"] = " · ".join(f"{i} {so.loc[i, 'kisa_ad']}" for i in M.columns)
    kat = s.set_index("sorun_id").ism_katman
    out["ISM_KATMAN"] = "; ".join(f"**{k}**: " + ", ".join(kat[kat == k].index) for k in sorted(kat.unique(), reverse=True))
    return out


def doldur(sablon: Path, hedef: Path) -> None:
    metin = sablon.read_text()
    for k, v in tablolar().items():
        metin = metin.replace("{{" + k + "}}", v)
    assert "{{" not in metin, "doldurulmamış yer tutucu"
    hedef.write_text(metin)


if __name__ == "__main__":
    doldur(Path(sys.argv[1]), Path(sys.argv[2]))
