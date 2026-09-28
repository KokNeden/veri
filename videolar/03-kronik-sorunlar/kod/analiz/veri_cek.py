"""Kök Neden V2 — gösterge verilerini çeker ve tek bir uzun formatlı CSV üretir.

Kullanım:
    pip install -r requirements.txt
    python veri_cek.py                 # API kaynakları (WDI, WGI) + ham/ klasöründeki dosyalar
    python veri_cek.py --sadece-api    # yalnızca API

Çıktı: ../veri/gostergeler_zaman_serisi.csv  (ulke, gosterge_id, kod, yil, deger, kaynak)
       ../veri/eksikler.csv                  (çekilemeyen gösterge/ülke kombinasyonları)

Elle indirilecek dosyalar (../veri/ham/ altına, adları aynen):
    mpd2023_web.xlsx     Maddison Project Database 2023   https://doi.org/10.34894/INZBF2
    pwt1001.xlsx         Penn World Table 10.01           https://doi.org/10.34894/QT5BCC
    vdem_core.csv        V-Dem Country-Year Core (v15+)   https://v-dem.net/data/the-v-dem-dataset/
    manuel.csv           Diğer elle derlenen seriler (ulke,kod,yil,deger,kaynak)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd
import requests

KOK = Path(__file__).resolve().parent
VERI = KOK.parent / "veri"
HAM = VERI / "ham"

KARSILASTIRMA = ["TUR", "KOR", "ESP", "PRT", "GRC", "POL", "MEX", "MYS"]
# OECD üyeleri (2026). Ortanca, bugünkü üyelikle tüm yıllar için hesaplanır (bileşim etkisi: sınırlılık).
OECD = ["AUS", "AUT", "BEL", "CAN", "CHL", "COL", "CRI", "CZE", "DNK", "EST", "FIN", "FRA",
        "DEU", "GRC", "HUN", "ISL", "IRL", "ISR", "ITA", "JPN", "KOR", "LVA", "LTU", "LUX",
        "MEX", "NLD", "NZL", "NOR", "POL", "PRT", "SVK", "SVN", "ESP", "SWE", "CHE", "TUR",
        "GBR", "USA"]
ULKELER = sorted(set(KARSILASTIRMA) | set(OECD))
OECD_MIN_ULKE = 20  # ortanca için o yıl en az bu kadar üyede veri olmalı

WB_KAYNAK = {"wdi": 2, "wgi": 3}
WB_URL = "https://api.worldbank.org/v2/country/{ulkeler}/indicator/{kod}"


def wb_cek(kod: str, kaynak: str, oturum: requests.Session) -> pd.DataFrame:
    """Dünya Bankası API'sinden (WDI/WGI) tüm ülkeler için seriyi çeker. Ham JSON önbelleğe yazılır."""
    onbellek = HAM / "api" / f"{kaynak}_{kod}.json"
    if onbellek.exists():
        kayitlar = json.loads(onbellek.read_text())
    else:
        kayitlar, sayfa = [], 1
        while True:
            params = {"format": "json", "per_page": 20000, "page": sayfa, "source": WB_KAYNAK[kaynak]}
            url = WB_URL.format(ulkeler=";".join(ULKELER), kod=kod)
            for deneme in range(4):
                try:
                    r = oturum.get(url, params=params, timeout=60)
                    r.raise_for_status()
                    veri = r.json()
                    break
                except (requests.RequestException, ValueError) as e:
                    if deneme == 3:
                        raise RuntimeError(f"{kod}: {e}") from e
                    time.sleep(2 ** deneme)
            if len(veri) < 2 or veri[1] is None:
                mesaj = veri[0].get("message") if veri and isinstance(veri[0], dict) else veri
                raise RuntimeError(f"{kod}: boş yanıt {mesaj}")
            kayitlar += veri[1]
            if sayfa >= veri[0]["pages"]:
                break
            sayfa += 1
        onbellek.parent.mkdir(parents=True, exist_ok=True)
        onbellek.write_text(json.dumps(kayitlar))
    satirlar = [
        {"ulke": k["countryiso3code"], "yil": int(k["date"]), "deger": k["value"]}
        for k in kayitlar if k["value"] is not None and k.get("countryiso3code")
    ]
    df = pd.DataFrame(satirlar, columns=["ulke", "yil", "deger"])
    df["kaynak"] = f"World Bank {'WDI' if kaynak == 'wdi' else 'WGI'} ({kod})"
    return df


def maddison_oku(kod: str) -> pd.DataFrame:
    df = pd.read_excel(HAM / "mpd2023_web.xlsx", sheet_name="Full data")
    df = df.rename(columns={"countrycode": "ulke", "year": "yil", kod: "deger"})
    df = df[df.ulke.isin(ULKELER)][["ulke", "yil", "deger"]].dropna()
    df["kaynak"] = "Maddison Project Database 2023"
    return df


def pwt_oku(kod: str) -> pd.DataFrame:
    df = pd.read_excel(HAM / "pwt1001.xlsx", sheet_name="Data")
    df = df.rename(columns={"countrycode": "ulke", "year": "yil", kod: "deger"})
    df = df[df.ulke.isin(ULKELER)][["ulke", "yil", "deger"]].dropna()
    df["kaynak"] = "Penn World Table 10.01"
    return df


_VDEM: pd.DataFrame | None = None


def vdem_oku(kod: str) -> pd.DataFrame:
    global _VDEM
    if _VDEM is None:
        _VDEM = pd.read_csv(HAM / "vdem_core.csv", low_memory=False)
        _VDEM = _VDEM[_VDEM.country_text_id.isin(ULKELER)]
    df = _VDEM.rename(columns={"country_text_id": "ulke", "year": "yil", kod: "deger"})
    df = df[["ulke", "yil", "deger"]].dropna()
    df["kaynak"] = "V-Dem Country-Year Core"
    return df


def manuel_oku(kod: str) -> pd.DataFrame:
    yol = HAM / "manuel.csv"
    if not yol.exists():
        raise FileNotFoundError("manuel.csv yok")
    df = pd.read_csv(yol)
    df = df[df.kod == kod][["ulke", "yil", "deger", "kaynak"]]
    if df.empty:
        raise LookupError(f"manuel.csv içinde {kod} yok")
    return df


def oecd_ortanca(df: pd.DataFrame) -> pd.DataFrame:
    """Her gösterge-yıl için OECD üyelerinin ortancası (en az OECD_MIN_ULKE ülke varsa)."""
    # Türkiye kendi referansına girmez; NaN değerler eşiği şişirmesin diye sayılmaz
    uye = df[df.ulke.isin(OECD) & (df.ulke != "TUR") & df.deger.notna()]
    g = uye.groupby(["gosterge_id", "kod", "yil"]).agg(deger=("deger", "median"), n=("deger", "count"))
    g = g[g.n >= OECD_MIN_ULKE].reset_index().drop(columns="n")
    g["ulke"] = "OECD_MED"
    g["kaynak"] = "Kök Neden hesaplaması: OECD üyeleri ortancası (TUR hariç)"
    return g


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sadece-api", action="store_true")
    args = ap.parse_args()

    liste = pd.read_csv(KOK / "gosterge_listesi.csv")
    oturum = requests.Session()
    parcalar, eksikler = [], []
    okuyucular = {"maddison": maddison_oku, "pwt": pwt_oku, "vdem": vdem_oku}

    for g in liste.itertuples():
        try:
            if g.kaynak in WB_KAYNAK:
                try:
                    df = wb_cek(g.kod, g.kaynak, oturum)
                except RuntimeError:
                    if g.kaynak != "wgi":
                        raise
                    # WGI 2023 revizyonundan sonra API kimlikleri GOV_WGI_ önekiyle geliyor
                    df = wb_cek(f"GOV_WGI_{g.kod}", g.kaynak, oturum)
            elif args.sadece_api:
                continue
            elif g.kaynak in okuyucular:
                df = okuyucular[g.kaynak](g.kod)
            else:  # manuel_*
                df = manuel_oku(g.kod)
        except Exception as e:  # noqa: BLE001 — eksik veri raporlanır, akış durmaz
            eksikler.append({"gosterge_id": g.gosterge_id, "kod": g.kod, "kaynak": g.kaynak, "hata": str(e)[:200]})
            print(f"  ! {g.gosterge_id} {g.kod}: {e}", file=sys.stderr)
            continue
        df.insert(1, "gosterge_id", g.gosterge_id)
        df.insert(2, "kod", g.kod)
        parcalar.append(df)
        tr = df[df.ulke == "TUR"].yil
        print(f"  ✓ {g.gosterge_id} {g.kod}: {len(df)} satır, TUR {tr.min() if len(tr) else '-'}–{tr.max() if len(tr) else '-'}")

    if not parcalar:
        print("Hiç gösterge çekilemedi; bkz. veri/eksikler.csv", file=sys.stderr)
        return 1
    tum = pd.concat(parcalar, ignore_index=True)
    tum = pd.concat([tum, oecd_ortanca(tum)], ignore_index=True)
    # Çıktıda karşılaştırma seti + OECD ortancası kalır; ham tüm OECD verisi önbellekte.
    tum = tum[tum.ulke.isin(KARSILASTIRMA + ["OECD_MED"])]
    tum = tum.sort_values(["gosterge_id", "ulke", "yil"])
    VERI.mkdir(exist_ok=True)
    tum.to_csv(VERI / "gostergeler_zaman_serisi.csv", index=False)
    pd.DataFrame(eksikler, columns=["gosterge_id", "kod", "kaynak", "hata"]).to_csv(VERI / "eksikler.csv", index=False)
    print(f"\n{len(tum)} satır yazıldı; {len(eksikler)} gösterge eksik (bkz. veri/eksikler.csv)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
