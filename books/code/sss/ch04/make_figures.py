#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 4 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403
from matplotlib.patches import Arc, FancyArrowPatch


def fig4_1():
    """Beer–Lambert：三种材料的直线衰减。"""
    d = np.linspace(0, 2.0, 400)
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    for st, c, lab in ((12.0, RED, r"皮肤  $\sigma_t=12$"),
                       (25.0, ACCENT, r"牛奶  $\sigma_t=25$"),
                       (1e-4, BLUE, r"清水  $\sigma_t=10^{-4}$")):
        ax.semilogy(d, np.exp(-st * d), color=c, label=lab)
    ax.axhline(np.exp(-1), color=GREY, lw=0.8, ls=(0, (4, 3)))
    ax.text(0.03, np.exp(-1) * 1.35, r"$1/e$", fontsize=8, color=GREY)
    ax.set_xlabel("深度 d (mm)")
    ax.set_ylabel(r"$e^{-\sigma_t d}$")
    ax.set_xlim(0, 2.0)
    ax.set_ylim(1e-6, 1.6)
    ax.legend(loc="lower left", fontsize=8)
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig4-1-beer.png")


def fig4_2():
    """微分体元的能量账本：光进入一体积元后的四个去向。"""
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    # 体积元
    x0, y0, w, h = 1.15, 0.55, 1.5, 1.25
    ax.add_patch(plt.Rectangle((x0, y0), w, h, facecolor="#eaf1f6",
                               edgecolor=BLUE, lw=1.2, alpha=0.85, zorder=2))
    ax.text(x0 + w / 2, y0 + h / 2 - 0.05, r"$dV$", fontsize=11, ha="center",
            va="center", zorder=3)
    ax.text(x0 + w / 2, y0 + h / 2 - 0.32, r"$\sigma_t,\ \alpha,\ p(\omega,\omega')$",
            fontsize=7.5, ha="center", va="center", zorder=3, color="#3c4654")
    # 入射与出射
    ax.annotate("", xy=(x0, y0 + h * 0.62), xytext=(x0 - 0.75, y0 + h * 0.62),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.4,
                                mutation_scale=10))
    ax.text(x0 - 0.80, y0 + h * 0.72, r"$L(x,\omega)$", fontsize=9, color=ACCENT)
    ax.annotate("", xy=(x0 + w + 0.75, y0 + h * 0.62),
                xytext=(x0 + w, y0 + h * 0.62),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.4,
                                mutation_scale=10))
    ax.text(x0 + w + 0.18, y0 + h * 0.72,
            r"$L+\dfrac{\partial L}{\partial s}ds$", fontsize=9, color=ACCENT)
    # 四个去向
    lab = [(x0 + w * 0.5, y0 + h + 0.78, "吸收  $\\sigma_a L\\,ds$", RED),
           (x0 + w * 0.5, y0 + h + 0.30, "散射出去  $\\sigma_s L\\,ds$", TEAL),
           (x0 + w * 0.5, y0 - 0.42, "从别处散进来  $\\sigma_s\\!\\int p L\\,d\\omega'$", PURPLE)]
    for (tx, ty, s, c) in lab:
        ax.annotate(s, xy=(tx, ty + (0.06 if ty > y0 else -0.02)),
                    xytext=(tx, ty), fontsize=8.5, color=c, ha="center",
                    arrowprops=dict(arrowstyle="-", color=c, lw=0.7,
                                    shrinkA=0, shrinkB=2))
    ax.set_xlim(0.1, 4.1)
    ax.set_ylim(-0.75, 3.25)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "fig4-2-balance.png")


def fig4_3():
    """平均自由程的指数分布。"""
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    s = np.linspace(0, 4, 400)
    for st, c, lab in ((0.5, BLUE, r"$\sigma_t=0.5$"),
                       (1.0, TEAL, r"$\sigma_t=1.0$"),
                       (2.0, RED, r"$\sigma_t=2.0$")):
        ax.plot(s, st * np.exp(-st * s), color=c, label=lab)
        ax.plot([1 / st], [st * np.exp(-1)], "o", ms=3.5, color=c)
    ax.set_xlabel("步长 s (mm)")
    ax.set_ylabel(r"$p(s)=\sigma_t e^{-\sigma_t s}$")
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 0.85)
    ax.legend(fontsize=8, loc="upper right")
    ax.annotate("圆点：平均自由程处", xy=(1.0, 0.368), xytext=(1.6, 0.55),
                fontsize=8, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    save(fig, "fig4-3-mfp.png")


if __name__ == "__main__":
    fig4_1()
    fig4_2()
    fig4_3()
