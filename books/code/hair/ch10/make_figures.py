#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 10 章插图：白炉测试、路径长度分布、参数敏感性。"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import *
import hairlib as H

ETA = 1.55


def fig_white_furnace():
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    fbars = np.linspace(0.02, 0.55, 60)
    for kmax, c, lab in [(2, BLUE, "只算 $R$、$TT$、$TRT$"),
                         (4, TEAL, "补到 $p=4$"),
                         (12, ACCENT, "补到 $p=12$")]:
        e = [sum(H.mean_energy(p, fbar=fb) for p in range(0, kmax + 1))
             for fb in fbars]
        ax.plot(fbars, e, color=c, lw=1.7, label=lab)
    ax.axhline(1.0, color=INK, lw=1.0, ls=(0, (5, 3)))
    ax.text(0.02, 1.005, "能量守恒：1.00", fontsize=8, color=INK)
    ax.set_xlim(0.02, 0.55)
    ax.set_ylim(0.55, 1.06)
    ax.set_xlabel("平均内反射率")
    ax.set_ylabel("积分得到的总能量")
    ax.legend(loc="lower left", fontsize=8, handlelength=1.8)
    ax.annotate("", xy=(0.5, 0.86), xytext=(0.5, 0.985),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.0))
    ax.text(0.44, 0.90, "缺口", fontsize=7.5, color=RED, ha="right")
    fig.tight_layout()
    save(fig, "fig10-1-white.png")


def fig_length_dist():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
    ax = axes[0]
    hs = np.linspace(0, 1, 4000)
    for p, c in [(1, BLUE), (2, RED)]:
        L = H.path_length(p, hs) / 2.0
        ax.hist(L, bins=80, density=True, color=c, alpha=0.45, lw=0,
                label=f"$p={p}$")
        ax.axvline(L.mean(), color=c, lw=1.2, ls=(0, (4, 3)))
    ax.set_xlim(0.6, 2.2)
    ax.set_xlabel("内部路径长度（以直径为 1）")
    ax.set_ylabel("概率密度")
    ax.legend(loc="upper left", fontsize=8, handlelength=1.4)
    ax.text(1.75, 3.2, "虚线：平均值", fontsize=7.5, color=GREY)
    panel_label(ax, "（a）", x=-0.16, y=1.10)

    ax = axes[1]
    mel = np.linspace(0, 1.2, 200)
    for p, c in [(1, BLUE), (2, RED)]:
        L = H.path_length(p, hs) / 2.0
        exact = np.array([np.mean(np.exp(-H.SIGMA_EU[1] * m * L)) for m in mel])
        approx = np.exp(-H.SIGMA_EU[1] * mel * L.mean())
        ax.plot(mel, (approx - exact) / exact * 100, color=c, lw=1.7,
                label=f"$p={p}$")
    ax.axhline(0, color=LIGHT, lw=0.8)
    ax.set_xlim(0, 1.2)
    ax.set_xlabel("黑色素浓度")
    ax.set_ylabel("用平均长度代替分布的误差（%）")
    ax.legend(loc="upper left", fontsize=8, handlelength=1.4)
    panel_label(ax, "（b）", x=-0.16, y=1.10)
    fig.tight_layout()
    save(fig, "fig10-2-length.png")


def fig_sensitivity():
    names, peak, pos, energy = [], [], [], []
    base_beta = 0.18
    ti = -0.5
    to = np.linspace(-1.6, 1.6, 2000)

    def n_peak(beta, p=2):
        return H.n_p(ti, to, p, beta=beta, spread=0.06).max()

    def n_pos(beta, p=2):
        return np.degrees(to[np.argmax(H.n_p(ti, to, p, beta=beta, spread=0.06))])

    def total_e(fbar, sa=0.0):
        return sum(H.mean_energy(p, fbar=fbar, sigma_a=sa) for p in range(0, 3))

    # 粗糙度
    names.append("粗糙度")
    peak.append(abs(n_peak(base_beta * 1.1) / n_peak(base_beta) - 1))
    pos.append(abs(n_pos(base_beta * 1.1) - n_pos(base_beta)) / 40.0)
    energy.append(0.0)
    # 黑色素
    names.append("黑色素")
    peak.append(0.0)
    pos.append(0.0)
    e0 = total_e(0.3, H.SIGMA_EU[1] * 0.35)
    e1 = total_e(0.3, H.SIGMA_EU[1] * 0.35 * 1.1)
    energy.append(abs(e1 / e0 - 1))
    # 平均内反射率
    names.append("内反射率")
    peak.append(0.0)
    pos.append(0.0)
    energy.append(abs(total_e(0.33) / total_e(0.3) - 1))
    # 折射率（用 TRT 折返点的位置变化表示）
    names.append("折射率")
    peak.append(0.0)
    p0 = 18.0

    def trt_fold(eta):
        h = np.linspace(0.01, 0.999, 4000)
        phi, L, w = H.phi_of_h(2, h, eta)
        dev = np.degrees(H.specular_deviation(phi, 2))
        return dev[np.argmax(dev)]

    pos.append(abs(trt_fold(ETA * 1.1) - trt_fold(ETA)) / 40.0)
    energy.append(0.0)

    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    x = np.arange(len(names))
    w = 0.27
    ax.bar(x - w, np.array(peak) * 100, width=w, color=ACCENT, label="高光峰值强度")
    ax.bar(x, np.array(pos) * 100, width=w, color=BLUE, label="高光角度位置")
    ax.bar(x + w, np.array(energy) * 100, width=w, color=TEAL, label="总能量")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel("该量变化的百分比（参数 +10%）")
    ax.set_ylim(0, 26)
    ax.legend(loc="upper left", fontsize=8, handlelength=1.4)
    ax.text(0.30, 0.94, "角度位置的百分比以 40 度为基准", transform=ax.transAxes,
            fontsize=7.5, color=GREY)
    fig.tight_layout()
    save(fig, "fig10-3-sensitivity.png")


if __name__ == "__main__":
    fig_white_furnace()
    fig_length_dist()
    fig_sensitivity()
