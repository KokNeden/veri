"""Matris ve gerekçe dosyası için otomatik tutarlılık kontrolleri (04-siralama-yontemi/01-yontem.md §3.3).

Hatalar hesaplamayı durdurur; uyarılar raporlanır.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def kontrol_et(A: np.ndarray, idler: list[str], gerekceler: pd.DataFrame | None = None) -> dict[str, list[str]]:
    A = np.asarray(A, dtype=float)
    hata, uyari = [], []
    if np.any(np.diag(A) != 0):
        hata.append("köşegen 0 değil")
    if ((A < 0) | (A > 4)).any():
        hata.append("0-4 aralığı dışında puan var")
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] == 4 and A[j, i] == 4:
                uyari.append(f"{idler[i]}↔{idler[j]} iki yönde de 4: döngü gerekçesi yazılmalı")
    if gerekceler is not None and len(gerekceler):
        g = gerekceler.set_index(["kaynak", "hedef"])
        for i, j in zip(*np.where(A >= 3)):
            anahtar = (idler[i], idler[j])
            if anahtar not in g.index:
                hata.append(f"{idler[i]}>{idler[j]} = {int(A[i, j])} ama gerekçe satırı yok")
                continue
            r = g.loc[anahtar]
            kaynak = str(r.get("kaynakca", "") if hasattr(r, "get") else "")
            if kaynak in ("", "nan"):
                hata.append(f"{idler[i]}>{idler[j]} = {int(A[i, j])} ama kaynak yok")
            if int(r.get("puan", A[i, j])) != int(A[i, j]):
                hata.append(f"{idler[i]}>{idler[j]}: matris {int(A[i, j])}, gerekçe dosyası {int(r['puan'])}")
    return {"hata": hata, "uyari": uyari}
