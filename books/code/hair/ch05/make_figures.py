#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 5 章插图：能量阶梯、高阶路径的旋转、多次散射填谷。"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import *
import hairlib as H


def fig_ladder():
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ps = np.arange(0, 9)
    for fb, c in [(0.05, GREY), (0.2, BLUE), (0.4, ACCENT)]:
        e = [H.mean_energy(p, fbar=fb) for p in ps]
        ax.plot(ps, e, "o-", color=c, lw=1.5, ms=3.5,
                label=f"平均内反射率 {fb}")
    ax.set_yscale("log")
    ax.set_ylim(1e-5, 1.2)
    ax.set_xlabel("路径阶数 $p$（$p=0$ 为 $R$，$p=1$ 为 $TT$，$p=2$ 为 $TRT$）")
    ax.set_ylabel("该阶携带的能量份额")
    ax.axvspan(1.6, 2.4, color=LIGHT, alpha=0.35, lw=0)
    ax.text(2.0, 0.55, "单次\n散射\n边界", fontsize=7.5, ha="center", color=INK)
    ax.legend(loc="lower left", fontsize=8, handlelength=1.4)
    fig.tight_layout()
    save(fig, "fig5-1-ladder.png")


def fig_rotation():
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    hs = np.linspace(0.02, 0.99, 400)
    cols = [ACCENT, BLUE, TEAL, RED, PURPLE, GREEN]
    for k, c in zip(range(2, 8), cols):
        phi, L, w = H.phi_of_h(k, hs)
        dev = np.degrees(np.unwrap(H.specular_deviation(phi, k)))
        ax.plot(hs, dev, color=c, lw=1.5, label=f"$p={k}$")
    ax.set_xlim(0, 1)
    ax.set_ylim(-160, 400)
    ax.set_yticks([0, 90, 180, 270, 360])
    ax.set_xlabel("入射偏移 $h$（相对半径）")
    ax.set_ylabel("相对镜面方向的方位角（度）")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=6,
              handlelength=1.2, fontsize=8, columnspacing=0.9)
    fig.tight_layout()
    save(fig, "fig5-2-rotation.png")


def fig_fill():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
    ax = axes[0]
    k = np.exp(-0.5 * (np.arange(-10, 11) / 3.0) ** 2)
    k = k / k.sum()
    curves = {}
    for kmax, c, ls in [(2, BLUE, (0, (4, 3))), (8, ACCENT, "-")]:
        cc, d, e = H.total_azimuth(kmax, fbar=0.3, bins=241, n=9000)
        d = np.convolve(d, k, mode="same")
        curves[kmax] = d
        ax.plot(np.degrees(cc), d, color=c, lw=1.6, ls=ls,
                label=f"阶数不超过 {kmax}，能量 {e:.2f}")
    ax.fill_between(np.degrees(cc), curves[2], curves[8],
                    where=curves[8] > curves[2], color=ACCENT, alpha=0.20, lw=0)
    ax.set_xlim(-120, 120)
    ax.set_yscale("log")
    ax.set_ylim(2e-3, 2)
    ax.set_xticks([-120, -60, 0, 60, 120])
    ax.set_xlabel("相对理想方向的方位角（度）")
    ax.set_ylabel("方位角密度（每弧度）")
    ax.legend(loc="lower center", fontsize=7.5, handlelength=1.8)
    ax.text(-116, 0.9, "阴影是高阶路径补上的部分", fontsize=7.5, color=ACCENT)
    panel_label(ax, "（a）", x=-0.15, y=1.02)

    ax = axes[1]
    for mel, c in [(0.08, GOLD), (0.35, ACCENT), (0.9, INK)]:
        sa = float(H.sigma_a(mel)[1])
        cc, d, e = H.total_azimuth(8, fbar=0.3, sigma_a=sa, bins=241, n=8000)
        d = np.convolve(d, k, mode="same")
        ax.plot(np.degrees(cc), d / d.max(), color=c, lw=1.6,
                label=f"黑色素 {mel}：总反射 {e:.2f}")
    ax.set_xlim(-120, 120)
    ax.set_xticks([-120, -60, 0, 60, 120])
    ax.set_xlabel("相对理想方向的方位角（度）")
    ax.set_ylabel("归一化强度")
    ax.legend(loc="upper left", fontsize=7.5, handlelength=1.8)
    panel_label(ax, "（b）", x=-0.15, y=1.02)
    fig.tight_layout()
    save(fig, "fig5-3-fill.png")


if __name__ == "__main__":
    fig_ladder()
    fig_rotation()
    fig_fill()
