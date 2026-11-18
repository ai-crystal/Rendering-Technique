#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 3 章插图：三条路径的几何、方位角偏折、吸收与颜色。"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from figstyle import *
import hairlib as H


def fig_paths():
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.2))
    names = ["（a）$R$：表面反射", "（b）$TT$：透射", "（c）$TRT$：一次内反射"]
    cols = [ACCENT, BLUE, RED]
    for ax, p, col, name in zip(axes, [0, 1, 2], cols, names):
        ax.add_patch(Circle((0, 0), 1.0, facecolor="#efe9df", edgecolor="#6b6472", lw=0.9))
        pts = H.path_points(0.5, p, back=0.55)
        ax.plot(pts[:, 0], pts[:, 1], "-", color=col, lw=1.3)
        ax.annotate("", xy=pts[1] - 0.06 * (pts[1] - pts[0]), xytext=pts[0],
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0))
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0))
        phi, L, w, ok = H.trace(0.5, p)
        ax.text(0.0, -1.62, f"$L={L:.2f}R$，偏折 {np.degrees(phi):+.0f}°",
                ha="center", fontsize=7.8, color=INK)
        ax.set_xlim(-1.75, 1.75)
        ax.set_ylim(-1.78, 1.30)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(name, fontsize=8.5, pad=1)
    fig.tight_layout()
    save(fig, "fig3-1-paths.png")


def fig_phi_density():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4))
    hs = np.linspace(0, 1, 500)
    cols = {0: ACCENT, 1: BLUE, 2: RED}
    lab = {0: "$R$", 1: "$TT$", 2: "$TRT$"}
    ax = axes[0]
    for p in [0, 1, 2]:
        phi, L, w = H.phi_of_h(p, hs)
        ax.plot(hs, np.degrees(H.specular_deviation(phi, p)), color=cols[p],
                lw=1.7, label=lab[p])
    ax.axhline(0, color=LIGHT, lw=0.8)
    hstar = np.sqrt((4.0 - 1.55 ** 2) / 3.0)
    ax.plot([hstar], [18.0], "o", ms=4, color=RED, zorder=5)
    ax.annotate("$d\\varphi/dh=0$", xy=(hstar, 18.0), xytext=(0.30, 62),
                fontsize=8, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
    ax.set_xlabel("入射偏移 $h$（相对半径）")
    ax.set_ylabel("相对理想方向的偏折（度）")
    ax.set_xlim(0, 1)
    ax.set_ylim(-195, 90)
    ax.legend(loc="lower left", ncol=3, handlelength=1.2, columnspacing=1.2)
    panel_label(ax, "（a）", x=-0.14, y=1.02)

    ax = axes[1]
    for p in [0, 1, 2]:
        c, d = H.azimuth_density(p, bins=361)
        k = np.exp(-0.5 * (np.arange(-14, 15) / 3.4) ** 2)
        d = np.convolve(d, k / k.sum(), mode="same") * H.mean_energy(p)
        ax.plot(np.degrees(c), d, color=cols[p], lw=1.6, label=lab[p])
    ax.set_xlim(-120, 120)
    ax.set_yscale("log")
    ax.set_ylim(2e-3, 2)
    ax.set_xlabel("相对理想方向的方位角（度）")
    ax.set_ylabel("能量加权密度（每弧度）")
    ax.legend(loc="lower center", ncol=3, handlelength=1.2, columnspacing=1.4,
              fontsize=8)
    panel_label(ax, "（b）", x=-0.14, y=1.02)
    fig.tight_layout()
    save(fig, "fig3-2-phi.png")


def fig_color():
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    mel = np.linspace(0, 1.2, 400)
    sa = H.SIGMA_EU
    L = 2 * 0.93
    for name, s, c in [("R 通道", sa[0], RED), ("G 通道", sa[1], GREEN),
                       ("B 通道", sa[2], BLUE)]:
        ax.plot(mel, np.exp(-s * mel * L), color=c, lw=1.7, label=name + "（TRT）")
    ax.axhline(1.0, color=GREY, lw=1.0, ls=(0, (4, 3)))
    ax.text(0.02, 1.02, "$R$ 路径：三个通道都是 1", fontsize=7.5, color=GREY)
    ax.axvspan(0.05, 0.22, color=GOLD, alpha=0.13, lw=0)
    ax.axvspan(0.7, 1.2, color=INK, alpha=0.05, lw=0)
    ax.text(0.135, 0.05, "浅色", fontsize=7.5, color=GOLD, ha="center")
    ax.text(0.95, 0.05, "深色", fontsize=7.5, color=INK, ha="center")
    ax.set_xlim(0, 1.2)
    ax.set_ylim(0, 1.08)
    ax.set_xlabel("黑色素浓度参数（相对值）")
    ax.set_ylabel("TRT 出射的相对强度")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=3,
              handlelength=1.4, fontsize=8, columnspacing=1.6)
    fig.tight_layout()
    save(fig, "fig3-3-color.png")


if __name__ == "__main__":
    fig_paths()
    fig_phi_density()
    fig_color()
