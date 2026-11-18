#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 9 章插图：色度轨迹、粗糙度与高光宽度、沿纤维的颜色渐变。"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import *
import hairlib as H

M_RGB2XYZ = np.array([[0.4124, 0.3576, 0.1805],
                      [0.2126, 0.7152, 0.0722],
                      [0.0193, 0.1192, 0.9505]])


def to_xy(rgb):
    xyz = M_RGB2XYZ @ np.asarray(rgb, dtype=float)
    s = xyz.sum()
    return xyz[0] / max(s, 1e-9), xyz[1] / max(s, 1e-9)


def fig_chroma():
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    tri = np.array([[0.64, 0.33], [0.30, 0.60], [0.15, 0.06], [0.64, 0.33]])
    ax.plot(tri[:, 0], tri[:, 1], color=GREY, lw=1.0, ls=(0, (4, 3)))
    ax.text(0.63, 0.30, "sRGB 原色", fontsize=7.5, color=GREY, ha="right")
    L = 1.86
    for redness, c in [(0.0, INK), (0.5, RED)]:
        xs, ys = [], []
        for mel in np.linspace(0.03, 0.7, 200):
            sa = H.sigma_a(mel, redness)
            rgb = np.exp(-sa * L)
            x, y = to_xy(np.clip(rgb, 0, 1))
            xs.append(x)
            ys.append(y)
        ax.plot(xs, ys, color=c, lw=1.7,
                label=f"褐黑色素比例 {redness}")
        for mel, mk in [(0.08, "o"), (0.3, "s"), (0.6, "^")]:
            sa = H.sigma_a(mel, redness)
            rgb = np.exp(-sa * L)
            x, y = to_xy(np.clip(rgb, 0, 1))
            ax.plot([x], [y], mk, color=c, ms=4.5)
            ax.text(x + 0.012, y - 0.028, f"{mel}", fontsize=7, color=c)
    ax.set_xlabel("色度坐标 $x$")
    ax.set_ylabel("色度坐标 $y$")
    ax.set_xlim(0.1, 0.7)
    ax.set_ylim(0.0, 0.65)
    ax.legend(loc="upper left", fontsize=8, handlelength=1.6)
    fig.tight_layout()
    save(fig, "fig9-1-chroma.png")


def fig_width():
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    betas = np.linspace(0.04, 0.6, 200)
    fwhm = []
    to = np.linspace(-1.6, 1.6, 1200)
    for b in betas:
        val = H.n_p(-0.5, to, 2, beta=b, spread=0.06)
        half = val.max() / 2
        idx = np.where(val >= half)[0]
        fwhm.append(np.degrees(to[idx[-1]] - to[idx[0]]))
    ax.plot(betas, fwhm, color=ACCENT, lw=1.8, label="数值半高宽")
    ax.plot(betas, np.degrees(2.355 * betas), color=BLUE, lw=1.2,
            ls=(0, (4, 3)), label=r"$2.355\beta$（纯高斯）")
    for b, c, t in [(0.15, GREEN, "健康"), (0.30, GOLD, "一般"), (0.50, RED, "受损")]:
        ax.axvline(b, color=c, lw=1.0, ls=(0, (2, 3)))
        ax.text(b + 0.008, 4, t, fontsize=7.5, color=c, rotation=90, va="bottom")
    ax.set_xlabel(r"粗糙度参数 $\beta$（弧度）")
    ax.set_ylabel("纵向高光半高宽（度）")
    ax.set_xlim(0.04, 0.6)
    ax.set_ylim(0, 90)
    ax.legend(loc="upper left", fontsize=8, handlelength=1.8)
    fig.tight_layout()
    save(fig, "fig9-2-width.png")


def fig_gradient():
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    s = np.linspace(0, 1, 300)
    mel = 0.55 - 0.40 * s
    Ltt, Ltrt = 1.9, 3.7
    for i, (name, c) in enumerate([("红", RED), ("绿", GREEN), ("蓝", BLUE)]):
        amp = (1 - H.sigma_a(0.0)[i] * 0)
        tt = np.exp(-H.SIGMA_EU[i] * mel * Ltt)
        trt = np.exp(-H.SIGMA_EU[i] * mel * Ltrt)
        ax.plot(s, 0.65 * tt + 0.35 * trt, color=c, lw=1.6,
                label=f"{name} 通道")
    ax2 = ax.twinx()
    ax2.plot(s, mel, color=GREY, lw=1.0, ls=(0, (4, 3)))
    ax2.set_ylabel("黑色素浓度", color=GREY, fontsize=8.5)
    ax2.tick_params(axis="y", colors=GREY, labelsize=8)
    ax2.set_ylim(0.05, 0.65)
    ax2.grid(False)
    ax.set_xlabel("沿纤维的归一化位置（0 为发根，1 为发梢）")
    ax.set_ylabel("出射强度（TT 与 TRT 加权）")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.85)
    ax.legend(loc="lower right", fontsize=8, handlelength=1.4)
    ax.text(0.02, 0.78, "灰虚线：浓度沿长度线性下降", fontsize=7.5, color=GREY)
    fig.tight_layout()
    save(fig, "fig9-3-gradient.png")


if __name__ == "__main__":
    fig_chroma()
    fig_width()
    fig_gradient()
