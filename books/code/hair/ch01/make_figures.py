#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 1 章插图：纤维的同心结构、内部路径长度、角向散射。"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from figstyle import *
import hairlib as H


def fig_structure():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6),
                             gridspec_kw={"width_ratios": [1.0, 1.0]})
    ax = axes[0]
    ax.set_aspect("equal")
    for r, c in [(1.00, "#efe9df"), (0.90, "#e6d9c8"), (0.34, "#cdbda4")]:
        ax.add_patch(Circle((0, 0), r, facecolor=c, edgecolor="#6b6472", lw=0.9, zorder=1))
    for r in (0.90, 0.34):
        ax.add_patch(Circle((0, 0), r, facecolor="none", edgecolor="#9a9186",
                            lw=0.8, ls=(0, (3, 2)), zorder=2))

    pts = H.path_points(0.82, 2, back=0.62)
    ax.plot(pts[:, 0], pts[:, 1], "-", color=ACCENT, lw=1.3, zorder=4)
    mid = 0.5 * (pts[0] + pts[1])
    ax.annotate("", xy=pts[1] - 0.10 * (pts[1] - pts[0]), xytext=mid,
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.1))
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.1))

    ax.text(0, 0.0, "髓质", ha="center", va="center", fontsize=8, color="#4a4237")
    ax.text(0, 0.60, "皮层", ha="center", va="center", fontsize=8, color="#4a4237")
    ax.annotate("角质层", xy=(0.72, -0.72), xytext=(0.92, -1.30), fontsize=8,
                color="#4a4237", ha="left", arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.annotate("一次内反射点", xy=(pts[2][0], pts[2][1]), xytext=(0.30, 1.30), fontsize=8,
                color="#3c4654", arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.text(pts[0][0] - 0.02, pts[0][1] - 0.09, "入射", fontsize=8, color=ACCENT,
            ha="left", va="top")
    ax.text(pts[-1][0] + 0.02, pts[-1][1] - 0.06, "出射", fontsize=8, color=ACCENT,
            ha="left", va="top")
    ax.set_xlim(-1.75, 1.62)
    ax.set_ylim(-1.52, 1.55)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("横截面，半径归一化为 1", fontsize=8.5)
    panel_label(ax, "（a）", x=-0.06, y=1.02)

    ax = axes[1]
    r = np.linspace(0, 1, 600)
    n = np.where(r < 0.34, 1.33, 1.55)
    ax.axvspan(0, 0.34, color="#cdbda4", alpha=0.22, lw=0)
    ax.axvspan(0.90, 1.0, color="#e6d9c8", alpha=0.45, lw=0)
    ax.plot(r, n, color=BLUE, lw=1.8)
    ax.set_xlim(0, 1)
    ax.set_ylim(1.0, 1.72)
    ax.set_xlabel("到轴心的距离（归一化）")
    ax.set_ylabel("折射率 n")
    ax.text(0.17, 1.345, "髓质（含空腔）", ha="center", va="bottom", fontsize=8, color="#4a4237")
    ax.text(0.60, 1.565, "皮层", ha="center", va="bottom", fontsize=8, color=INK)
    ax.text(0.95, 1.565, "角质层", ha="center", va="bottom", fontsize=8, color="#4a4237")
    ax.annotate("", xy=(0.905, 1.10), xytext=(0.995, 1.10),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=0.8))
    ax.text(0.99, 1.075, "厚度约 0.1R", ha="right", va="top", fontsize=7.5, color=GREY)
    panel_label(ax, "（b）", x=-0.24, y=1.03)
    fig.tight_layout()
    save(fig, "fig1-1-structure.png")


def fig_path_length():
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    hs = np.linspace(0, 1, 300)
    cols = [ACCENT, BLUE, TEAL, PURPLE]
    tags = ["$p=1$ TT", "$p=2$ TRT", "$p=3$ TRRT", "$p=4$ TRRRT"]
    for i, p in enumerate([1, 2, 3, 4]):
        L = H.path_length(p, hs) / 2.0
        ax.plot(hs, L, color=cols[i], lw=1.7)
        ax.text(1.012, L[-1], tags[i], color=cols[i], va="center", fontsize=8)
    for k in range(1, 5):
        ax.axhline(k, color=LIGHT, lw=0.7, ls=(0, (4, 3)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0.68, 4.22)
    ax.set_xlabel("入射偏移 $|h|$（相对半径）")
    ax.set_ylabel("内部路径长度（以直径为 1）")
    fig.tight_layout()
    save(fig, "fig1-2-pathlength.png")


def fig_scattering():
    c, d, e = H.total_azimuth(6, bins=361, n=14000)
    k = np.exp(-0.5 * (np.arange(-12, 13) / 4.0) ** 2)
    d = np.convolve(d, k / k.sum(), mode="same")
    d = d / d.max()
    fig = plt.figure(figsize=(4.6, 4.3))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_theta_zero_location("E")
    ax.plot(c, d, color=ACCENT, lw=1.8, label="纤维（数值计算）")
    ax.plot(c, 0.5 * np.ones_like(c), color=BLUE, lw=1.2, ls=(0, (4, 3)),
            label="各向同性参考")
    ax.set_rlim(0, 1.0)
    ax.set_rticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0.25", "0.50", "0.75", "1.00"], fontsize=7)
    ax.set_rlabel_position(112)
    ax.set_thetagrids([0, 45, 90, 135, 180, 225, 270, 315],
                      ["0° 入射", "45°", "90°", "135°", "180°", "225°", "270°", "315°"],
                      fontsize=7.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.10), ncol=1,
              handlelength=1.8, fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig1-3-scattering.png")


if __name__ == "__main__":
    fig_structure()
    fig_path_length()
    fig_scattering()
