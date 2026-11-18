#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 9 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig9_1():
    """同一 φ 下，真实角分布与 P1 重建的差别。"""
    th = np.deg2rad(np.linspace(0, 180, 600))
    c = np.cos(th)
    g = 0.8
    p = hg_phase(c, g)                       # 总能量为 1 的角分布
    p1 = (1 + 3 * g * c) / (4 * np.pi)       # 同样的 φ 与 E
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.plot(np.rad2deg(th), p, color=RED, label=r"真实分布 HG，$g=0.8$")
    ax.plot(np.rad2deg(th), p1, color=BLUE, ls=(0, (5, 2)),
            label=r"P1 重建（同一个 $\phi$ 与 $\mathbf{E}$）")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_yscale("symlog", linthresh=1e-3)
    ax.set_ylim(-0.3, 10)
    ax.set_xlim(0, 180)
    ax.set_xticks([0, 45, 90, 135, 180])
    ax.set_xlabel(r"散射角 $\theta$ (度)")
    ax.set_ylabel(r"$L(\theta)$")
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.16)
    ax.annotate("P1 在这里穿过零", xy=(126, 0.0), xytext=(96, 0.10),
                fontsize=8, color=BLUE, ha="left",
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.7))
    save(fig, "fig9-1-p1-limit.png")


def fig9_2():
    """HG 的 Legendre 矩。"""
    l = np.arange(0, 8)
    fig, ax = plt.subplots(figsize=(5.0, 2.7))
    for g, c in ((0.3, BLUE), (0.5, TEAL), (0.8, ACCENT), (0.9, RED)):
        ax.plot(l, g ** l.astype(float), "o-", ms=3.5, color=c,
                label=rf"$g={g}$")
    ax.set_xlabel("阶数 l")
    ax.set_ylabel(r"$a_l=g^l$")
    ax.set_xticks(l)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=8, ncol=2, loc="lower left")
    ax.grid(alpha=0.2)
    ax.axvspan(-0.3, 1.3, color=GREY, alpha=0.10)
    ax.text(0.0, 0.96, "P1 保留", fontsize=8, color=GREY, ha="center")
    save(fig, "fig9-2-moments.png")


if __name__ == "__main__":
    fig9_1()
    fig9_2()
