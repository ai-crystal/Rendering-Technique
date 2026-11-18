#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 7 章插图：覆盖率、双流近似、LOD 误差。"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import *


def km(KS, tau):
    """Kubelka–Munk 双流解：返回 (反射率, 透射率)，tau = S·d。"""
    a = 1.0 + KS
    b = np.sqrt(max(a * a - 1.0, 1e-12))
    sh = np.sinh(b * tau)
    ch = np.cosh(b * tau)
    den = a * sh + b * ch
    return sh / den, b / den


def fig_coverage():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
    ax = axes[0]
    N = np.linspace(0, 40, 300)
    for a, c in [(0.03, BLUE), (0.10, ACCENT), (0.30, RED)]:
        ax.plot(N, 1 - np.exp(-N * a), color=c, lw=1.6,
                label=f"单根覆盖率 {a}")
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("一个像素覆盖的纤维数 $N$")
    ax.set_ylabel("不透明度 $\\alpha$")
    ax.legend(loc="lower right", fontsize=8, handlelength=1.6)
    panel_label(ax, "（a）", x=-0.20, y=1.10)

    ax = axes[1]
    tau = np.linspace(0.01, 8, 300)
    for KS, c in [(0.05, GOLD), (0.3, ACCENT), (1.2, INK)]:
        R, T = km(KS, tau)
        ax.plot(tau, T, color=c, lw=1.6, label=f"$K/S={KS}$")
        ax.plot(tau, np.exp(-(1 + KS) * tau), color=c, lw=1.0, ls=(0, (3, 2.5)),
                alpha=0.8)
    ax.set_yscale("log")
    ax.set_ylim(1e-4, 1.2)
    ax.set_xlim(0, 8)
    ax.set_xlabel("光学厚度 $\\tau=Sd$")
    ax.set_ylabel("透射率")
    ax.text(4.4, 3e-3, "实线：双流解\\n虚线：只算衰减", fontsize=7.5, color="#3c4654")
    ax.legend(loc="lower left", fontsize=8, handlelength=1.4)
    panel_label(ax, "（b）", x=-0.20, y=1.10)
    fig.tight_layout()
    save(fig, "fig7-1-coverage.png")


def fig_glow():
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    tau = np.linspace(0.02, 6, 300)
    KS = 0.25
    R, T = km(KS, tau)
    ax.plot(tau, R, color=ACCENT, lw=1.7, label="反射（同一侧看到）")
    ax.plot(tau, T, color=BLUE, lw=1.7, label="透射（逆光看到）")
    ax.plot(tau, np.exp(-(1 + KS) * tau), color=GREY, lw=1.1, ls=(0, (3, 2.5)),
            label="无多次散射的透射")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.02, 6)
    ax.set_ylim(1e-4, 1.2)
    ax.set_xlabel("光学厚度 $\\tau$")
    ax.set_ylabel("相对强度")
    ax.legend(loc="lower left", fontsize=8, handlelength=1.8)
    ax.annotate("厚样品的透射被多次散射抬高数倍到十几倍",
                xy=(3.0, float(km(KS, 3.0)[1])), xytext=(0.055, 6e-3),
                fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    fig.tight_layout()
    save(fig, "fig7-2-glow.png")


def fig_lod():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
    ax = axes[0]
    N = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=float)
    a = 0.1
    alpha = 1 - np.exp(-N * a)
    noise = np.sqrt(alpha * (1 - alpha) / N)
    ax.loglog(N, noise, "o-", color=BLUE, lw=1.5, ms=4, label="逐纤维蒙特卡洛")
    ax.set_xlabel("每像素纤维数 $N$")
    ax.set_ylabel("像素值的相对噪声")
    ax.set_ylim(1e-4, 1.0)
    ax.legend(loc="lower left", fontsize=8, handlelength=1.8)
    ax.text(1.4, 5.0e-3, "体积化没有采样噪声，误差变成偏差（右图）", fontsize=7.5, color=INK)
    panel_label(ax, "（a）", x=-0.20, y=1.10)

    ax = axes[1]
    tau = np.linspace(0.05, 5.0, 300)
    for KS, c in [(0.1, GOLD), (0.4, ACCENT), (1.0, INK)]:
        R, T = km(KS, tau)
        R1 = 1 - np.exp(-tau)
        ax.plot(tau, R1 / np.maximum(R, 1e-9) - 1.0, color=c, lw=1.6,
                label=f"$K/S={KS}$")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 2.6)
    ax.set_xlabel("光学厚度（$S d$）")
    ax.set_ylabel("覆盖率模型相对真实反射的偏差")
    ax.legend(loc="upper left", fontsize=8, handlelength=1.4)
    panel_label(ax, "（b）", x=-0.20, y=1.10)
    fig.tight_layout()
    save(fig, "fig7-3-lod.png")


if __name__ == "__main__":
    fig_coverage()
    fig_glow()
    fig_lod()
