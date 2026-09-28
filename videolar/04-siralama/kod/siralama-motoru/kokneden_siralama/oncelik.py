"""Öncelik skoru.

Varsayılan: ağırlıklı geometrik ortalama  P = K^wK · A^wA · E^wE,  (wK, wA, wE) = (0.5, 0.25, 0.25).

Neden çarpım (geometrik) ve neden bu ağırlıklar — bkz. 04-siralama-yontemi/01-yontem.md §4:
- Çarpım, 'kök ama açığı yok' ya da 'açık büyük ama kimseyi etkilemiyor' sorunların
  tek bir güçlü bileşenle üste çıkmasını engeller (kısmi telafi).
- Saf çarpım (K·A·E) ağırlık taşımaz ve bir bileşen 0 ise sonucu sıfırlar;
  bu yüzden bileşenlere taban (ε = 0.05) konur ve ağırlıklı geometrik ortalama alınır.
- Kök skoru projenin temel fikri olduğu için yarı ağırlıktadır.
Duyarlılık analizinde ağırlıklar ve toplama türü (geometrik/aritmetik) değiştirilir.
"""
from __future__ import annotations

import numpy as np

VARSAYILAN_AGIRLIK = (0.5, 0.25, 0.25)
TABAN = 0.05


def oncelik(K, A, E, agirlik=VARSAYILAN_AGIRLIK, tur: str = "geometrik") -> np.ndarray:
    K, A, E = (np.clip(np.asarray(x, dtype=float), TABAN, 1.0) for x in (K, A, E))
    w = np.asarray(agirlik, dtype=float)
    if (w < 0).any() or w.sum() <= 0:
        raise ValueError("Ağırlıklar negatif olamaz ve toplamı 0'dan büyük olmalı")
    w = w / w.sum()
    if tur == "geometrik":
        return np.exp(w[0] * np.log(K) + w[1] * np.log(A) + w[2] * np.log(E))
    if tur == "aritmetik":
        return w[0] * K + w[1] * A + w[2] * E
    raise ValueError(tur)


def sirala(skor: np.ndarray) -> np.ndarray:
    """1 = en yüksek öncelik. Eşitlikte küçük indeks önce."""
    sira = np.empty(len(skor), dtype=int)
    sira[np.argsort(-np.asarray(skor), kind="stable")] = np.arange(1, len(skor) + 1)
    return sira
