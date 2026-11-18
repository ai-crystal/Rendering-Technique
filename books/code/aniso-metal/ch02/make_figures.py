#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 2 章插图：导体 Fresnel 与 Schlick 近似的误差。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from anisocommon import *       # noqa: F401,F403

TH = np.linspace(0.0, np.pi / 2 - 1e-3, 720)
C = np.cos(TH)
DEG = np.degrees(TH)


def fig2_1():
    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    cols = [ACCENT, TEAL, BLUE]
    for j in range(3):
        n, k = METALS["金"][j]
        R = fresnel_conductor(C, n, k)
        ax.plot(DEG, R, color=cols[j], label=f"精确，{WL_NAME[j]}")
    n, k = METALS["金"][0]
    ax.plot(DEG, fresnel_schlick(C, f0_from_nk(n, k)), "--", color=GREY, lw=1.6,
            label="Schlick，0.65 μm")
    ax.set_xlabel("入射角 (度)")
    ax.set_ylabel("反射率 $R$")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="lower right")
    save(fig, "fig2-1-gold-fresnel.png")


def fig2_2():
    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    txt = []
    for (name, nk), c in zip(METALS.items(), COLORS):
        n, k = nk[0]
        f0 = float(f0_from_nk(n, k))
        err = fresnel_conductor(C, n, k) - fresnel_schlick(C, f0)
        ax.plot(DEG, err, color=c, label=f"{name}（$F_0$ = {f0:.2f}）")
        i = int(np.argmax(np.abs(err)))
        txt.append((name, DEG[i], float(err[i])))
        ax.plot([DEG[i]], [err[i]], "o", ms=4, color=c)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xlabel("入射角 (度)")
    ax.set_ylabel("精确值减 Schlick 近似")
    ax.set_xlim(0, 90)
    ax.legend(loc="upper left", ncol=2)
    save(fig, "fig2-2-schlick-error.png")


def fig2_3():
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    n, k = METALS["金"][0]
    s2 = 1.0 - C ** 2
    a2 = n ** 2 - k ** 2 - s2
    b2 = 2 * n * k
    t = np.sqrt(a2 ** 2 + b2 ** 2)
    a = np.sqrt(np.maximum(0.5 * (t + a2), 0))
    b = np.sqrt(np.maximum(0.5 * (t - a2), 0))
    rs = ((C - a) ** 2 + b ** 2) / ((C + a) ** 2 + b ** 2)
    rp = (((n ** 2 - k ** 2) * C - a) ** 2 + (2 * n * k * C - b) ** 2) / \
         (((n ** 2 - k ** 2) * C + a) ** 2 + (2 * n * k * C + b) ** 2)
    ax.plot(DEG, rs, color=ACCENT, label="金，s 偏振")
    ax.plot(DEG, rp, color=ACCENT, ls="--", label="金，p 偏振")
    eg = np.arccos(np.clip(np.sqrt(1 - (np.sin(TH) / 1.5) ** 2), 0, 1))
    ct = np.sqrt(1 - (np.sin(TH) / 1.5) ** 2)
    g_s = ((C - 1.5 * ct) / (C + 1.5 * ct)) ** 2
    g_p = ((1.5 * C - ct) / (1.5 * C + ct)) ** 2
    ax.plot(DEG, g_s, color=BLUE, lw=1.2, label="玻璃，s 偏振")
    ax.plot(DEG, g_p, color=BLUE, lw=1.2, ls="--", label="玻璃，p 偏振")
    ax.set_xlabel("入射角 (度)")
    ax.set_ylabel("反射率")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="center right", fontsize=7.6)
    ax.annotate("p 分量在布儒斯特角降到零", (56.3, 0.02), xytext=(40, 0.22),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.7, color=GREY))
    save(fig, "fig2-3-rs-rp.png")


if __name__ == "__main__":
    fig2_1()
    fig2_2()
    fig2_3()
