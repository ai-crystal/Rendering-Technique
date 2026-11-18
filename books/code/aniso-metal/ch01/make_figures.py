#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 1 章插图：金属的光学常数。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from anisocommon import *       # noqa: F401,F403


def fig1_1():
    """趋肤深度 δ = λ/(4πk)，λ = 0.65 μm。"""
    names = list(METALS.keys())
    vals = [float(skin_depth_nm(0.65, METALS[m][0][1])) for m in names]
    ks = [METALS[m][0][1] for m in names]
    order = np.argsort(vals)
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    y = np.arange(len(names))
    ax.barh(y, [vals[i] for i in order], height=0.58,
            color=[COLORS[i] for i in order], edgecolor="white", lw=0.8)
    for j, i in enumerate(order):
        ax.text(vals[i] + 0.4, j, f"{vals[i]:.0f} nm", va="center", fontsize=8.5)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{names[i]}（k = {ks[i]:.2f}）" for i in order], fontsize=9)
    ax.set_xlabel("趋肤深度 $\\delta=\\lambda/4\\pi k$  (nm)，$\\lambda = 0.65\\,\\mu$m")
    ax.set_xlim(0, 21)
    ax.grid(axis="y", visible=False)
    save(fig, "fig1-1-skin-depth.png")


def fig1_2():
    """五种金属在三个波长上的垂直入射反射率。"""
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    names = list(METALS.keys())
    x = np.arange(len(names))
    w = 0.26
    for j in range(3):
        vals = [float(f0_from_nk(*METALS[m][j])) for m in names]
        ax.bar(x + (j - 1) * w, vals, w, label=WL_NAME[j],
               color=[ACCENT, TEAL, BLUE][j], edgecolor="white", lw=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=10)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("$F_0$")
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.legend(loc="lower center", ncol=3, bbox_to_anchor=(0.5, 1.0))
    ax.grid(axis="x", visible=False)
    note(ax, "银与铝三条柱几乎等高（中性）\n金与铜在蓝端塌陷（有色）", 0.02, 0.86)
    save(fig, "fig1-2-f0-bars.png")


def fig1_3():
    """F0 在 (n, k) 平面上的等值线。"""
    fig, ax = plt.subplots(figsize=(5.6, 4.1))
    n = np.linspace(0.01, 3.6, 320)
    k = np.linspace(0.01, 8.2, 360)
    N, K = np.meshgrid(n, k)
    F = f0_from_nk(N, K)
    cs = ax.contourf(N, K, F, levels=np.linspace(0, 1, 21), cmap="Blues", alpha=0.85)
    cl = ax.contour(N, K, F, levels=[0.2, 0.4, 0.6, 0.8, 0.9, 0.95],
                    colors="#2b3540", linewidths=0.7)
    ax.clabel(cl, fmt="%.2f", fontsize=7)
    off = {"金": (9, -14), "铜": (9, 6), "银": (10, -3), "铝": (9, 6), "铁": (9, 6)}
    for (name, nk), c in zip(METALS.items(), COLORS):
        nn, kk = nk[0]
        ax.plot([nn], [kk], "o", ms=7, mfc="white", mec=INK, mew=1.1, zorder=6)
        ax.annotate(name, (nn, kk), textcoords="offset points", xytext=off[name],
                    fontsize=8.5, color=INK, zorder=7)
    ax.set_xlabel("折射率实部 $n$")
    ax.set_ylabel("消光系数 $k$")
    fig.colorbar(cs, ax=ax, label="$F_0$", pad=0.02)
    ax.grid(False)
    save(fig, "fig1-3-f0-contour.png")


if __name__ == "__main__":
    fig1_1()
    fig1_2()
    fig1_3()
