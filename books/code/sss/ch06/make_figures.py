#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 6 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig6_1():
    """微分体元的账本。"""
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    cx, cy, L, r = 2.0, 1.5, 1.5, 0.55
    ang = np.deg2rad(-12)
    ex = np.array([np.cos(ang), np.sin(ang)])
    ey = np.array([-np.sin(ang), np.cos(ang)])
    p0 = np.array([cx, cy]) - ex * L / 2
    corners = [p0 + ey * r, p0 + ex * L + ey * r, p0 + ex * L - ey * r, p0 - ey * r]
    ax.add_patch(plt.Polygon(corners, closed=True, facecolor="#eaf1f6",
                             edgecolor=BLUE, lw=1.2, zorder=2))
    ax.plot([p0[0], p0[0] + ex[0] * L], [p0[1], p0[1] + ex[1] * L],
            color=BLUE, lw=0.7, ls=(0, (3, 2)))
    ax.text(cx - 0.05, cy - 0.02, r"$ds$", fontsize=9.5, color=BLUE)
    ax.annotate("", xy=p0 - ex * 0.02, xytext=p0 - ex * 1.2,
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.3,
                                mutation_scale=10))
    ax.annotate("", xy=p0 + ex * (L + 1.2), xytext=p0 + ex * L,
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.3,
                                mutation_scale=10))
    ax.text(p0[0] - ex[0] * 1.35, p0[1] + 0.30, r"$L(x,\omega)$", fontsize=9,
            color=ACCENT, ha="left")
    ax.text(p0[0] + ex[0] * (L + 0.25), p0[1] + 0.34,
            r"$L+\dfrac{\partial L}{\partial s}ds$", fontsize=9, color=ACCENT)
    out = np.array([cx + 0.55, cy + 0.95])
    ax.annotate("", xy=out, xytext=(cx + 0.15, cy + 0.30),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.0,
                                mutation_scale=8))
    ax.text(out[0] + 0.10, out[1] + 0.02, r"$\sigma_s L\,ds$", fontsize=8.5,
            color=TEAL)
    inc = np.array([cx - 0.85, cy + 1.05])
    ax.annotate("", xy=(cx - 0.30, cy + 0.28), xytext=inc,
                arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1.0,
                                mutation_scale=8))
    ax.text(inc[0] - 0.55, inc[1] + 0.05,
            r"$\sigma_s\!\int p(\omega',\omega)L\,d\omega'$", fontsize=8.5,
            color=PURPLE)
    ax.annotate("", xy=(cx, cy - 1.05), xytext=(cx, cy - 0.35),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.0,
                                mutation_scale=8))
    ax.text(cx + 0.10, cy - 1.02, r"$\sigma_a L\,ds$", fontsize=8.5, color=RED)
    ax.set_xlim(-0.2, 4.6)
    ax.set_ylim(-0.1, 3.2)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "fig6-1-balance.png")


def fig6_2():
    """散射次数分布：高反照率与低反照率。"""
    fig, ax = plt.subplots(figsize=(5.4, 2.9))
    cases = [(0.002, 10.0, ACCENT), (1.40, 3.0, TEAL)]
    for ma, ms, c in cases:
        ap = albedo_prime(ma, ms, 0.8)
        re, kind, ev = mc_slab(ma, ms, 0.8, n_photons=50000, max_events=1200)
        ok = np.isfinite(re)
        e = ev[ok]
        ax.hist(e, bins=np.arange(0, 60, 1.5), color=c, alpha=0.55,
                density=True, label=rf"$\alpha'={ap:.3f}$")
        ax.axvline(np.mean(e), color=c, lw=1.0, ls=(0, (4, 3)))
        print("alpha'", ap, "mean events", np.mean(e), "escape frac", ok.mean())
    ax.set_xlabel("出射光子经历的散射次数")
    ax.set_ylabel("概率密度")
    ax.set_xlim(0, 60)
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=8)
    ax.text(0.62, 0.92, "虚线为均值", transform=ax.transAxes, fontsize=8,
            color=GREY)
    save(fig, "fig6-2-neumann.png")


if __name__ == "__main__":
    fig6_1()
    fig6_2()
