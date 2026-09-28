"""Uzman matrislerini birleştirme ve anlaşmazlık ölçümü (04-siralama-yontemi/01-yontem.md §3.3).

Boş hücre (NaN) = "emin değilim". Birleşik puan = hücre ortancası (NaN'ler dışarıda).
Hiç puan yoksa 0. Tartışmalı: IQR ≥ 2 ya da puan veren uzman < en_az.
"""
from __future__ import annotations

from itertools import combinations

import numpy as np
from scipy.stats import kendalltau


def birlestir(matrisler: list[np.ndarray], en_az: int = 3, iqr_esik: float = 2.0):
    Y = np.stack([np.asarray(m, dtype=float) for m in matrisler])  # (uzman, n, n)
    n_puan = np.sum(~np.isnan(Y), axis=0)
    with np.errstate(all="ignore"):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            med = np.nanmedian(Y, axis=0)
            q1, q3 = np.nanpercentile(Y, 25, axis=0), np.nanpercentile(Y, 75, axis=0)
    med = np.where(n_puan == 0, 0.0, med)
    iqr = np.where(n_puan == 0, 0.0, q3 - q1)
    tartismali = (iqr >= iqr_esik) | (n_puan < en_az)  # hiç puan almayan hücre de tartışmalı
    np.fill_diagonal(med, 0)
    np.fill_diagonal(tartismali, False)
    return med, iqr, n_puan, tartismali


def uzman_uyumu(matrisler: list[np.ndarray]) -> np.ndarray:
    """Uzman çiftleri arasında, ikisinin de puanladığı köşegen dışı hücrelerde Kendall tau."""
    k = len(matrisler)
    U = np.eye(k)
    maske = ~np.eye(len(matrisler[0]), dtype=bool)
    for a, b in combinations(range(k), 2):
        x, y = np.asarray(matrisler[a], float)[maske], np.asarray(matrisler[b], float)[maske]
        ok = ~np.isnan(x) & ~np.isnan(y)
        U[a, b] = U[b, a] = kendalltau(x[ok], y[ok]).statistic if ok.sum() > 2 else np.nan
    return U
