#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 4 章插图：方位角分布的归一化、纵向分布、二维联合分布。"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import *
import hairlib as H


def fig_norm():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
    cols = {0: ACCENT, 1: BLUE, 2: RED}
    lab = {0: "$M_R$", 1: "$M_{TT}$", 2: "$M_{TRT}$"}
    ax = axes[0]
    k = np.exp(-0.5 * (np.arange(-6, 7) / 1.6) ** 2)
    k = k / k.sum()
    for p in [0, 1, 2]:
        c, d = H.azimuth_density(p, bins=361)
        d = np.convolve(d, k, mode="same")
        ax.plot(np.degrees(c), d, color=cols[p], lw=1.6, label=lab[p])
    ax.set_ylim(0, 2.45)
    ax.set_xlim(-180, 180)
    ax.set_xticks([-180, -90, 0, 90, 180])
    ax.set_xlabel("相对理想方向的方位角（度）")
    ax.set_ylabel("方位角密度（每弧度）")
    ax.legend(loc="upper left", handlelength=1.4, fontsize=8)
    panel_label(ax, "（a）", x=-0.14, y=1.02)

    ax = axes[1]
    hs = np.linspace(1e-4, 1 - 1e-4, 6000)
    phi, L, w = H.phi_of_h(2, hs)
    dev = H.specular_deviation(phi, 2)
    dphidh = np.maximum(np.abs(np.gradient(dev, hs)), 1e-9)
    A = w
    edges = np.linspace(-np.pi, np.pi, 361)
    idx = np.clip(np.digitize(dev, edges) - 1, 0, len(edges) - 2)
    dh = hs[1] - hs[0]
    good = np.zeros(len(edges) - 1)
    bad = np.zeros(len(edges) - 1)
    np.add.at(good, idx, A * dh / dphidh)
    np.add.at(bad, idx, A * dh * dphidh)
    ctr = 0.5 * (edges[1:] + edges[:-1])
    dphi = edges[1] - edges[0]
    good = good / (good.sum() * dphi)
    bad = bad / (bad.sum() * dphi)
    k2 = np.exp(-0.5 * (np.arange(-6, 7) / 1.6) ** 2)
    good = np.convolve(good, k2 / k2.sum(), mode="same")
    bad = np.convolve(bad, k2 / k2.sum(), mode="same")
    ax.plot(np.degrees(ctr), good, color=RED, lw=1.6, label="正确：$A\\,|dh/d\\varphi|$")
    ax.plot(np.degrees(ctr), bad, color=GREY, lw=1.5, ls=(0, (4, 3)),
            label="错误：$A\\,|d\\varphi/dh|$")
    ax.set_xlim(-45, 45)
    ax.set_yscale("log")
    ax.set_ylim(0.02, 24)
    ax.set_xlabel("相对镜面方向的方位角（度）")
    ax.set_ylabel("方位角密度（每弧度）")
    ax.legend(loc="upper center", fontsize=8, handlelength=1.6)
    panel_label(ax, "（b）", x=-0.20, y=1.02)
    fig.tight_layout()
    save(fig, "fig4-1-norm.png")


def fig_longitudinal():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
    ax = axes[0]
    to = np.linspace(-1.3, 1.3, 600)
    ti = -0.6
    for p, c, lab in [(0, ACCENT, "$N_R$"), (1, BLUE, "$N_{TT}$"),
                      (2, RED, "$N_{TRT}$")]:
        ax.plot(np.degrees(to), H.n_p(ti, to, p, beta=0.18, spread=0.06),
                color=c, lw=1.7, label=lab)
    ax.axvline(-np.degrees(ti), color=LIGHT, lw=0.9, ls=(0, (4, 3)))
    ax.set_xlim(-70, 70)
    ax.set_ylim(0, 5.0)
    ax.set_xlabel(r"$\theta_o$（度）")
    ax.set_ylabel("纵向密度")
    ax.legend(loc="upper left", handlelength=1.2, ncol=3, columnspacing=1.2,
              fontsize=8)
    ax.text(-np.degrees(ti) + 2.5, 4.7, r"$-\theta_i$", fontsize=8, color=GREY)
    panel_label(ax, "（a）", x=-0.14, y=1.02)

    ax = axes[1]
    ax.plot(np.degrees(to), H.n_p(ti, to, 0, beta=0.18, spread=1e-4),
            color=GREY, lw=1.5, ls=(0, (4, 3)), label=r"只有粗糙度：$\beta=0.18$")
    ax.plot(np.degrees(to), H.n_p(ti, to, 0, beta=0.02, spread=0.10),
            color=BLUE, lw=1.5, ls=(0, (1, 1.6)), label="只有倾角：标准差 0.10 rad")
    ax.plot(np.degrees(to), H.n_p(ti, to, 0, beta=0.18, spread=0.10),
            color=ACCENT, lw=1.8, label="两者卷积")
    ax.axvline(-np.degrees(ti), color=LIGHT, lw=0.9, ls=(0, (4, 3)))
    ax.set_xlim(-40, 80)
    ax.set_ylim(0, 2.6)
    ax.set_xlabel(r"$\theta_o$（度）")
    ax.set_ylabel("$N_R$ 的密度")
    ax.legend(loc="upper left", fontsize=7.5, handlelength=1.8)
    panel_label(ax, "（b）", x=-0.14, y=1.02)
    fig.tight_layout()
    save(fig, "fig4-2-longitudinal.png")


def fig_joint():
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    phi = np.linspace(-0.9, 0.9, 300)
    tho = np.linspace(-1.2, 1.2, 300)
    P, T = np.meshgrid(phi, tho)
    M = H.pdf_phi(2, P, bins=361)
    Nn = H.n_p(-0.5, T, 2, beta=0.18, spread=0.06)
    Z = M * Nn
    Z = Z / Z.max()
    cs = ax.contourf(np.degrees(P), np.degrees(T), Z,
                     levels=np.linspace(0.05, 1.0, 12), cmap="YlOrBr")
    ax.contour(np.degrees(P), np.degrees(T), Z, levels=[0.1, 0.3, 0.6],
               colors="#5b6472", linewidths=0.6)
    ax.set_xlabel(r"$\varphi$（度）")
    ax.set_ylabel(r"$\theta_o$（度），$\theta_i=-28.6°$")
    ax.set_xlim(-27, 27)
    ax.set_ylim(2, 54)
    cb = fig.colorbar(cs, ax=ax, pad=0.02, ticks=[0, 0.5, 1.0])
    cb.ax.set_yticklabels(["0", "0.5", "1.0"], fontsize=7)
    cb.set_label("相对强度", fontsize=8)
    fig.tight_layout()
    save(fig, "fig4-3-joint.png")


if __name__ == "__main__":
    fig_norm()
    fig_longitudinal()
    fig_joint()
