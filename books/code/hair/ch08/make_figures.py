#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 8 章插图：求交迭代、切线插值、双散射查找表。"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import *
import hairlib as H


def fig_intersect():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2))
    ax = axes[0]
    R = 1.0
    # 视线与半径为 R 的圆柱求交（二维截面）
    for off, c in [(1.4, BLUE), (0.8, ACCENT), (0.2, RED)]:
        t = 0.0
        res = []
        for _ in range(8):
            p = np.array([-4.0 + t, off])
            f = np.dot(p, p) - R * R
            fp = 2 * (p[0])
            t = t - f / fp
            res.append(abs(f))
        ax.semilogy(range(1, len(res) + 1), np.maximum(res, 1e-17), "o-",
                    color=c, lw=1.4, ms=3.5, label=(f"偏移 {off}" if off < 1 else f"偏移 {off}（未命中）"))
    ax.set_xlabel("牛顿迭代次数")
    ax.set_ylabel("残差 $|\\,|p|^2-R^2\\,|$")
    ax.set_ylim(1e-17, 1e3)
    ax.legend(loc="lower left", fontsize=8, handlelength=1.4)
    panel_label(ax, "（a）", x=-0.20, y=1.10)

    ax = axes[1]
    ds = np.linspace(0.01, 3.0, 400)
    for r, c in [(20, BLUE), (50, ACCENT), (100, GREY)]:
        ax.loglog(ds, np.degrees(ds / r), color=c, lw=1.6, label=f"半径 {r} 微米")
    ax.axhline(1.0, color=RED, lw=1.0, ls=(0, (4, 3)))
    ax.text(0.012, 1.3, "1 度", fontsize=7.5, color=RED)
    ax.set_xlabel("求交得到的位置误差（微米）")
    ax.set_ylabel("法线方向的角误差（度）")
    ax.set_xlim(0.01, 3)
    ax.legend(loc="lower right", fontsize=8, handlelength=1.4)
    panel_label(ax, "（b）", x=-0.20, y=1.10)
    fig.tight_layout()
    save(fig, "fig8-1-intersect.png")


def fig_tangent_error():
    """折线近似的转角误差随细分的变化，以及它对高光方向的影响。"""
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    n = np.array([2, 4, 8, 16, 32, 64, 128, 256], dtype=float)
    theta = np.pi / 2          # 总转角 90 度
    per = np.degrees(theta) / n
    ax.loglog(n, per, "o-", color=BLUE, lw=1.5, ms=4, label="每段转角")
    ax.loglog(n, 2 * per, "s--", color=ACCENT, lw=1.4, ms=4,
              label="高光方向的最大偏差（约两倍）")
    ax.set_xlabel("每根纤维的线段数")
    ax.set_ylabel("角度（度）")
    ax.set_ylim(1e-3, 100)
    ax.legend(loc="lower left", fontsize=8, handlelength=1.8)
    ax.axhline(1.0, color=RED, lw=1.0, ls=(0, (4, 3)))
    ax.text(2.2, 1.2, "1 度：可见的折角", fontsize=7.5, color=RED)
    fig.tight_layout()
    save(fig, "fig8-2-tangent.png")


def fig_lut():
    hs = np.linspace(-1 + 1e-4, 1 - 1e-4, 3000)
    geo = {}
    for p in range(3, 7):
        phi, L, w = H.phi_of_h(p, hs)
        geo[p] = (H.specular_deviation(phi, p), L, w > 0)
    fbars = np.linspace(0.05, 0.5, 24)
    edges = np.linspace(-np.pi, np.pi, 121)
    ctr = np.degrees(0.5 * (edges[1:] + edges[:-1]))
    table = np.zeros((len(fbars), len(edges) - 1))
    for i, fb in enumerate(fbars):
        acc = np.zeros(len(edges) - 1)
        for p in range(3, 7):
            dev, L, ok = geo[p]
            w = H.order_energy(p, hs, fbar=fb) * ok
            idx = np.clip(np.digitize(dev, edges) - 1, 0, len(edges) - 2)
            tmp = np.zeros(len(edges) - 1)
            np.add.at(tmp, idx, w)
            acc += tmp
        table[i] = acc
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    cs = ax.pcolormesh(ctr, fbars, table / table.max(), cmap="YlOrBr",
                       shading="auto")
    ax.set_xlim(-120, 120)
    ax.set_xlabel("相对理想方向的方位角（度）")
    ax.set_ylabel("平均内反射率")
    cb = fig.colorbar(cs, ax=ax, pad=0.02, ticks=[0, 0.5, 1.0])
    cb.ax.set_yticklabels(["0", "0.5", "1"], fontsize=7)
    cb.set_label("相对强度", fontsize=8)
    ax.contour(ctr, fbars, table / table.max(), levels=[0.2, 0.5],
               colors="#3c4654", linewidths=0.6)
    fig.tight_layout()
    save(fig, "fig8-3-lut.png")


if __name__ == "__main__":
    fig_intersect()
    fig_tangent_error()
    fig_lut()
