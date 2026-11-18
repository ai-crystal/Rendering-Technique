#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 2 章插图：切线空间、幂次高光、与几何结果的对比。"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Arc
from figstyle import *
import hairlib as H


def fig_tangent_frame():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4),
                             gridspec_kw={"width_ratios": [1.2, 1]})
    ax = axes[0]
    ax.add_patch(Rectangle((-1.45, -0.34), 2.9, 0.60, facecolor="#e6d9c8",
                           edgecolor="#6b6472", lw=0.9, zorder=1))
    ax.add_patch(Ellipse((1.45, -0.04), 0.26, 0.60, facecolor="#efe9df",
                         edgecolor="#6b6472", lw=0.9, zorder=2))
    ax.annotate("", xy=(1.10, -0.04), xytext=(-0.95, -0.04),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1))
    ax.text(1.14, -0.04, r"$T$", fontsize=10, color=INK, va="center")

    P = np.array([0.05, 0.26])
    ti, to = np.radians(110.0), np.radians(70.0)
    li = np.array([np.cos(ti), np.sin(ti)])
    vo = np.array([np.cos(to), np.sin(to)])
    ax.annotate("", xy=P, xytext=P + 1.05 * li,
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.3))
    ax.text(*(P + 1.10 * li), r"$L$", fontsize=10, color=BLUE, ha="center")
    ax.annotate("", xy=P + 1.05 * vo, xytext=P,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.3))
    ax.text(*(P + 1.10 * vo), r"$V$", fontsize=10, color=RED, ha="center")

    ax.add_patch(Arc(P, 1.60, 1.60, theta1=0, theta2=110, color=BLUE, lw=1.0))
    ax.add_patch(Arc(P, 0.95, 0.95, theta1=0, theta2=70, color=RED, lw=1.0))
    ax.text(P[0] + 0.90 * np.cos(np.radians(50)), P[1] + 0.90 * np.sin(np.radians(50)),
            r"$\theta_i$", fontsize=10, color=BLUE, ha="center")
    ax.text(P[0] + 0.56 * np.cos(np.radians(22)), P[1] + 0.56 * np.sin(np.radians(22)),
            r"$\theta_o$", fontsize=10, color=RED, ha="center")
    ax.text(-1.50, 0.56, "两个角都从 $+T$ 量到光线", fontsize=7.5, color="#3c4654")
    ax.set_xlim(-1.55, 1.72)
    ax.set_ylim(-0.62, 1.42)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlabel("侧视：两个角都从切线量起", fontsize=8.5)
    panel_label(ax, "（a）", x=-0.04, y=1.0)

    ax = axes[1]
    ax.add_patch(Ellipse((0, 0), 2.0, 2.0, facecolor="#efe9df",
                         edgecolor="#6b6472", lw=0.9))
    for a in np.linspace(0, 2 * np.pi, 9)[:-1]:
        c, s = np.cos(a), np.sin(a)
        ax.annotate("", xy=(1.17 * c, 1.17 * s), xytext=(0.99 * c, 0.99 * s),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.9))
    ax.plot([0.0, 1.0], [0, 0], color=GREY, lw=0.8, ls=(0, (4, 3)))
    ax.text(1.05, 0.0, r"$L$", fontsize=9.5, color=GREY, va="center")
    ax.text(0.0, -1.44, "横截面：法线绕一圈，$N$ 不唯一",
            fontsize=8, color=INK, ha="center")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.6, 1.42)
    ax.set_aspect("equal")
    ax.axis("off")
    panel_label(ax, "（b）", x=0.02, y=1.0)
    fig.tight_layout()
    save(fig, "fig2-1-tangent.png")


def fig_power_lobes():
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    to = np.linspace(-1.45, 0.85, 800)
    ti = -0.7
    for n, c in zip([8, 30, 120, 600], [GREY, BLUE, ACCENT, PURPLE]):
        val = np.clip(np.cos(ti + to), 0.0, None) ** n
        ax.plot(np.degrees(to), val / val.max(), color=c, lw=1.6,
                label=f"$n={n}$")
    ax.axvline(-np.degrees(ti), color=RED, lw=0.9, ls=(0, (4, 3)))
    ax.text(-np.degrees(ti) + 1.5, 0.90, "镜面方向", fontsize=8, color=RED)
    ax.set_xlim(-85, 62)
    ax.set_xlabel(r"$\theta_o$（度）")
    ax.set_ylabel("归一化高光强度")
    ax.legend(loc="upper left", ncol=2, handlelength=1.5, columnspacing=1.0)
    fig.tight_layout()
    save(fig, "fig2-2-power.png")


def fig_compare():
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    c, d, e = H.total_azimuth(6, bins=241, n=9000)
    k = np.exp(-0.5 * (np.arange(-10, 11) / 3.0) ** 2)
    d = np.convolve(d, k / k.sum(), mode="same")
    ax.plot(np.degrees(c), d, color=ACCENT, lw=1.8,
            label="纤维的真实方位角分布")
    ax.axhline(d.mean(), color=BLUE, lw=1.5, ls=(0, (5, 3)),
               label="Kajiya–Kay 的隐含分布（与方位角无关）")
    ax.axvline(0, color=LIGHT, lw=0.8)
    ax.set_xlim(-180, 180)
    ax.set_xlabel("方位角 $\\varphi$：出射方向相对入射方向（度）")
    ax.set_ylabel("角密度（每弧度）")
    ax.set_xticks([-180, -120, -60, 0, 60, 120, 180])
    ax.legend(loc="upper right", handlelength=1.8, fontsize=7.5)
    ax.annotate("透射峰", xy=(0, d.max()), xytext=(-46, d.max() * 0.88),
                fontsize=8, color=ACCENT,
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.8))
    i95 = int(np.argmin(abs(np.degrees(c) - 95)))
    ax.annotate("侧向几乎无光", xy=(95, d[i95]), xytext=(52, d.max() * 0.45),
                fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    fig.tight_layout()
    save(fig, "fig2-3-compare.png")


if __name__ == "__main__":
    fig_tangent_frame()
    fig_power_lobes()
    fig_compare()
