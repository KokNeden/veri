"""Neden-sonuç haritası (D+R yatay, D−R dikey) ve ilk-k olasılığı grafiği."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

RENK_NEDEN = "#B5452B"
RENK_SONUC = "#2B5F8A"
GRI = "#9AA0A6"


def neden_sonuc_haritasi(sonuc, etiketler, dosya, esik=None, baslik="Neden-sonuç haritası",
                         en_fazla_ok=30, alt_not=None):
    D_R, DmR = sonuc.onem, sonuc.net
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=150)
    if esik is not None:
        T = sonuc.T.copy()
        np.fill_diagonal(T, 0)
        idx = np.argwhere(T > esik)
        idx = sorted(idx, key=lambda ij: -T[ij[0], ij[1]])[:en_fazla_ok]
        tmax = T.max()
        for i, j in idx:
            ax.annotate("", xy=(D_R[j], DmR[j]), xytext=(D_R[i], DmR[i]),
                        arrowprops=dict(arrowstyle="-|>", color=GRI, lw=0.4 + 1.6 * T[i, j] / tmax,
                                        alpha=0.55, shrinkA=6, shrinkB=6,
                                        connectionstyle="arc3,rad=0.12"))
    renk = [RENK_NEDEN if v > 0 else RENK_SONUC for v in DmR]
    ax.scatter(D_R, DmR, s=90, c=renk, zorder=3, edgecolor="white", linewidth=1)
    metinler = [ax.text(x, y, e, fontsize=8.5, zorder=4) for x, y, e in zip(D_R, DmR, etiketler)]
    try:  # isteğe bağlı: etiket çakışmalarını çözer (pip install adjustText)
        from adjustText import adjust_text
        adjust_text(metinler, x=list(D_R), y=list(DmR), ax=ax, expand=(1.3, 1.6),
                    arrowprops=dict(arrowstyle="-", color="#777", lw=0.5))
    except ImportError:
        for t in metinler:
            t.set_position((t.get_position()[0] + 0.01, t.get_position()[1] + 0.01))
    ax.axhline(0, color="#444", lw=0.8)
    ax.axvline(np.mean(D_R), color="#444", lw=0.6, ls=":")
    ax.set_xlabel("D + R  (toplam önem: verdiği + aldığı etki)")
    ax.set_ylabel("D − R  (> 0 neden grubu, < 0 sonuç grubu)")
    ax.set_title(baslik, loc="left", fontsize=13, fontweight="bold")
    ax.text(0.99, 0.98, "NEDEN GRUBU", transform=ax.transAxes, ha="right", va="top",
            color=RENK_NEDEN, fontsize=9, fontweight="bold")
    ax.text(0.99, 0.02, "SONUÇ GRUBU", transform=ax.transAxes, ha="right", va="bottom",
            color=RENK_SONUC, fontsize=9, fontweight="bold")
    if alt_not:
        fig.text(0.01, 0.005, alt_not, fontsize=7.5, color="#555")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(dosya)
    plt.close(fig)


def ilk_k_grafigi(ozet, etiketler, dosya, k=5, baslik=None, alt_not=None):
    kol = f"ilk{k}_olasilik"
    o = ozet.assign(etiket=etiketler).sort_values(kol, ascending=True)
    o = o[o[kol] > 0.005].tail(15)
    fig, ax = plt.subplots(figsize=(9, 0.42 * len(o) + 1.4), dpi=150)
    ax.barh(o.etiket, o[kol] * 100, color=[RENK_NEDEN if v >= 0.5 else GRI for v in o[kol]])
    for y, v in enumerate(o[kol]):
        ax.text(v * 100 + 1, y, f"%{v * 100:.0f}", va="center", fontsize=8.5)
    ax.set_xlim(0, 105)
    ax.set_xlabel(f"İlk {k}'te kalma olasılığı (%)")
    ax.set_title(baslik or f"İlk {k}'te kalma olasılığı", loc="left", fontsize=12, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    if alt_not:
        fig.text(0.01, 0.005, alt_not, fontsize=7.5, color="#555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(dosya)
    plt.close(fig)
