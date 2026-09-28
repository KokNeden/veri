"""Açık skoru (A) ve etki alanı skoru (E).

A iki ölçütten oluşur (Kök Neden temel kararı, 21.09.2026):
  1. BİRİNCİL — plan açığı: Türkiye'nin kendi planında koyduğu hedefe ne kadar uzak kaldığı.
     A_plan = 1 − ilerleme,  ilerleme = (x_son − x_başlangıç) / (hedef − x_başlangıç), [0, 1]'e kırpılır.
  2. İKİNCİL — ülke açığı: aşağıdaki sağlam z-skoru.
  İkisi de varsa A = 0,7 · A_plan + 0,3 · A_ülke. Yalnız biri varsa o kullanılır.

Ülke açığı: Türkiye'nin ana göstergesinin karşılaştırma setinin ortancasından standart uzaklığı.
   Sağlam z = yön · (ortanca − x_TUR) / (1.4826 · MAD).  z > 0 → Türkiye daha kötü.
   A = Φ(z) ∈ (0, 1). Alternatif (duyarlılık için): yüzdelik = setin kaçta kaçından kötü.
E: Etki alanı düzeyi 1-3 → 1/3, 2/3, 1.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

KARSILASTIRMA = ["KOR", "ESP", "PRT", "GRC", "POL", "MEX", "MYS"]
REFERANS = "OECD_MED"
ULKE = "TUR"
PENCERE = 3  # karşılaştırma değeri TR yılından en çok bu kadar yıl eski olabilir


@dataclass
class Acik:
    gosterge_id: str | None
    yil: int | None
    tur: float | None
    ortanca: float | None
    n_set: int
    z: float | None
    A_phi: float | None       # Φ(z)
    A_yuzdelik: float | None  # setin kaçta kaçından kötü
    not_: str


def _phi(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def son_deger(seri: pd.DataFrame, ulke: str, en_gec: int | None = None,
              en_erken: int | None = None) -> tuple[int, float] | None:
    s = seri[seri.ulke == ulke].dropna(subset=["deger"])
    if en_gec is not None:
        s = s[s.yil <= en_gec]
    if en_erken is not None:
        s = s[s.yil >= en_erken]
    if s.empty:
        return None
    r = s.sort_values("yil").iloc[-1]
    return int(r.yil), float(r.deger)


def acik_skoru(seri: pd.DataFrame, yon: int, gosterge_id: str | None = None,
               min_set: int = 5, karsilastirma: list[str] | None = None) -> Acik:
    """seri: ulke, yil, deger sütunları (tek gösterge).

    karsilastirma: konuya göre seçilen ülke seti (kararlar: set konuya göre seçilir).
    Verilmezse varsayılan set (KARSILASTIRMA) + OECD ortancası kullanılır. Not: OECD ortancası
    sete bir 'ülke' gibi girer; set içindeki OECD üyeleri böylece iki kez temsil edilir.
    """
    if yon == 0:
        return Acik(gosterge_id, None, None, None, 0, None, None, None,
                    "yön normatif değil → açık hesaplanmaz (bilmiyoruz)")
    tr = son_deger(seri, ULKE)
    if tr is None:
        return Acik(gosterge_id, None, None, None, 0, None, None, None, "Türkiye verisi yok")
    yil, x = tr
    degerler = []
    for u in (karsilastirma or KARSILASTIRMA) + [REFERANS]:
        d = son_deger(seri, u, en_gec=yil, en_erken=yil - PENCERE)
        if d is not None:
            degerler.append(d[1])
    v = np.array(degerler)
    if len(v) < min_set:
        return Acik(gosterge_id, yil, x, None, len(v), None, None, None,
                    f"karşılaştırma setinde yalnız {len(v)} değer")
    med = float(np.median(v))
    mad = float(np.median(np.abs(v - med))) * 1.4826
    if mad > 0:
        z = yon * (med - x) / mad
    else:  # setin çoğu aynı değerde: standart sapmaya, o da 0 ise yalnız yöne bak (birimden bağımsız)
        sd = float(v.std())
        z = yon * (med - x) / sd if sd > 0 else (0.0 if x == med else 4.0 * float(np.sign(yon * (med - x))))
    z = float(np.clip(z, -4, 4))
    kotu_oldugu = float(np.mean(yon * (v - x) > 0))  # set üyelerinin kaçı TR'den iyi
    return Acik(gosterge_id, yil, x, med, len(v), z, _phi(z), kotu_oldugu, "")


PLAN_AGIRLIK = 0.7


def plan_acigi(baslangic: float, hedef: float, gerceklesen: float,
               baslangic_yil: float | None = None, hedef_yil: float | None = None,
               gerceklesen_yil: float | None = None) -> float | None:
    """Plan hedefine kalan mesafe ∈ [0, 1]. 0 = hedef tuttu (ya da takvimin önünde), 1 = hiç ilerleme yok ya da geriledi.

    Yıllar verilirse ilerleme, takvime göre beklenen ilerlemeye oranlanır: süresi dolmamış bir
    hedefte ilk yıl %10 ilerleme, beş yıllık planın 1/5'i geçtiyse "geride" değil "biraz geride" sayılır.
    """
    if any(v is None or pd.isna(v) for v in (baslangic, hedef, gerceklesen)) or hedef == baslangic:
        return None
    ilerleme = (gerceklesen - baslangic) / (hedef - baslangic)
    yillar = (baslangic_yil, hedef_yil, gerceklesen_yil)
    if not any(v is None or pd.isna(v) for v in yillar) and hedef_yil > baslangic_yil:
        beklenen = min(max((gerceklesen_yil - baslangic_yil) / (hedef_yil - baslangic_yil), 1e-9), 1.0)
        ilerleme = ilerleme / beklenen
    return float(np.clip(1 - ilerleme, 0.0, 1.0))


def birlesik_acik(A_plan: float | None, A_ulke: float | None) -> float | None:
    if A_plan is not None and A_ulke is not None and not np.isnan(A_ulke):
        return PLAN_AGIRLIK * A_plan + (1 - PLAN_AGIRLIK) * A_ulke
    if A_plan is not None:
        return A_plan
    return A_ulke


ETKI_DUZEY = {1: 1 / 3, 2: 2 / 3, 3: 1.0}


def etki_skoru(duzey: int) -> float:
    if duzey not in ETKI_DUZEY:
        raise ValueError("Etki düzeyi 1, 2 veya 3 olmalı")
    return ETKI_DUZEY[duzey]
