"""ISM (Interpretive Structural Modeling) katmanları — Warfield (1974).

DEMATEL toplam etki matrisi eşikle ikili hale getirilir, geçişli kapanış alınır,
ardından seviye ayrıştırması yapılır. Sonuç: her sorunun katmanı.
Katman 1 = en üst (en çok 'sonuç'), en büyük katman = en derin kök.
"""
from __future__ import annotations

import numpy as np


def erisim_matrisi(T: np.ndarray, esik: float) -> np.ndarray:
    n = len(T)
    M = (T > esik).astype(int)
    np.fill_diagonal(M, 1)
    # Warshall geçişli kapanış
    for k in range(n):
        M = M | (M[:, [k]] & M[[k], :])
    return M


def katmanlar(T: np.ndarray, esik: float) -> np.ndarray:
    M = erisim_matrisi(T, esik)
    n = len(M)
    kalan = set(range(n))
    seviye = np.zeros(n, dtype=int)
    s = 1
    while kalan:
        bu_tur = []
        for i in kalan:
            erisim = {j for j in kalan if M[i, j]}
            onculler = {j for j in kalan if M[j, i]}
            if erisim <= onculler:  # erişim ∩ öncül = erişim
                bu_tur.append(i)
        if not bu_tur:  # teorik olarak olmaz; güvenlik
            bu_tur = list(kalan)
        for i in bu_tur:
            seviye[i] = s
            kalan.discard(i)
        s += 1
    return seviye
