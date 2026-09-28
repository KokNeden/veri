"""DEMATEL: doğrudan etki matrisinden toplam etki, D, R, D+R, D−R.

Gabus & Fontela (1972, 1973) Battelle Cenevre; normalizasyon için Lee vd. (2013).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

OLCEK_MIN, OLCEK_MAX = 0, 4


@dataclass
class DematelSonucu:
    X: np.ndarray        # normalize doğrudan etki matrisi
    T: np.ndarray        # toplam etki matrisi  T = X (I − X)^−1
    D: np.ndarray        # satır toplamı: verdiği toplam etki
    R: np.ndarray        # sütun toplamı: aldığı toplam etki
    s: float             # normalizasyon katsayısı

    @property
    def onem(self) -> np.ndarray:  # D + R
        return self.D + self.R

    @property
    def net(self) -> np.ndarray:  # D − R  (> 0: neden grubu)
        return self.D - self.R


def dogrula(A: np.ndarray) -> np.ndarray:
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("Etki matrisi kare olmalı")
    if np.isnan(A).any():
        raise ValueError("Matriste boş hücre var")
    if (A < OLCEK_MIN).any() or (A > OLCEK_MAX).any():
        raise ValueError(f"Puanlar {OLCEK_MIN}-{OLCEK_MAX} arasında olmalı")
    if np.any(np.diag(A) != 0):
        raise ValueError("Köşegen 0 olmalı (bir sorun kendini etkilemez)")
    return A


def normalize(A: np.ndarray) -> tuple[np.ndarray, float]:
    """s = max(en büyük satır toplamı, en büyük sütun toplamı).

    Bu seçim X'in hem satır hem sütun toplamlarını ≤ 1 yapar. Satır ya da sütun toplamı s'ye
    eşit olan kapalı bir etki bloğu varsa spektral yarıçap 1 olur ve (I − X) tersinir değildir
    (Lee vd. 2013'ün "uygulanamazlık" durumu). Bu durumda s %1 büyütülür (X ← 0,99·X) ve uyarı
    verilir: T'nin ölçeği büyür, sonuç ayrıca raporlanmalıdır. (Lee vd. 2013 başka bir düzeltme
    önerir: s = max(en büyük satır toplamı, ε + en büyük sütun toplamı).)
    """
    s = max(A.sum(axis=1).max(), A.sum(axis=0).max())
    if s == 0:
        raise ValueError("Matris tamamen sıfır")
    X = A / s
    if max(abs(np.linalg.eigvals(X))) >= 1 - 1e-9:
        import warnings
        warnings.warn("ρ(X) = 1: kapalı etki bloğu; s %1 büyütüldü, T ölçeği büyür", RuntimeWarning)
        s = s / 0.99
        X = A / s
    return X, float(s)


def dematel(A: np.ndarray) -> DematelSonucu:
    A = dogrula(A)
    X, s = normalize(A)
    n = len(A)
    T = X @ np.linalg.inv(np.eye(n) - X)
    return DematelSonucu(X=X, T=T, D=T.sum(axis=1), R=T.sum(axis=0), s=s)


def esik(T: np.ndarray, yontem: str = "ortalama", k: float = 1.5) -> float:
    """Haritada gösterilecek / ISM'e girecek bağlantılar için eşik.

    'ortalama'     : T'nin ortalaması (literatürde en yaygın; harita okları için)
    'ortalama+kss' : ortalama + k standart sapma (ISM için; varsayılan k = 1.5)
    T dolaylı etkileri de içerdiği için yoğundur; ortalama eşiğinde neredeyse her düğüm
    birbirine ulaşır ve ISM tek katmana çöker. Bu yüzden ISM daha seçici eşik kullanır.
    """
    if yontem == "ortalama":
        return float(T.mean())
    if yontem == "ortalama+kss":
        return float(T.mean() + k * T.std())
    raise ValueError(yontem)


def kok_skoru(sonuc: DematelSonucu, lam: float = 0.5) -> np.ndarray:
    """Kök skoru K ∈ [0, 1] = λ·ñ(D−R) + (1−λ)·ñ(D), ñ: min-max normalizasyon.

    D  : sorunun sisteme verdiği toplam (doğrudan + dolaylı) etki → "ne kadar çok şeyi sürüklüyor?"
    D−R: net veren mi, net alan mı → "kendisi başka bir şeyin sonucu mu?"
    D+R (toplam önem) bilinçli olarak dışarıda: çok etki ALAN sonuç sorunlarını da ödüllendirir.
    (Rutubetli ev örneğinde D+R kullanılsaydı 'duvarda nem', 'tesisat kaçağı'nın önüne geçerdi.)
    λ = 0.5; duyarlılık analizinde λ ∈ [0.3, 0.7].
    """
    return lam * minmax(sonuc.net) + (1 - lam) * minmax(sonuc.D)


def minmax(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    aralik = v.max() - v.min()
    if aralik == 0:
        return np.full_like(v, 0.5)
    return (v - v.min()) / aralik
