#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 13 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403
from matplotlib.patches import FancyArrowPatch


def fig13_1():
    """偶极子的几何。"""
    fig, ax = plt.subplots(figsize=(5.8, 3.1))
    ax.add_patch(plt.Rectangle((-0.2, -2.6), 8.4, 2.6, facecolor="#f0e6da",
                               edgecolor="none", zorder=0))
    ax.plot([-0.2, 8.2], [0, 0], color=INK, lw=1.5, zorder=3)
    ax.plot([-0.2, 8.2], [1.08, 1.08], color=RED, lw=0.9, ls=(0, (5, 3)),
            zorder=3)
    ax.text(8.1, 1.18, r"$d=-z_b$（外推平面，$\varphi=0$）", fontsize=8,
            color=RED, ha="right")
    xs = 2.6
    ax.plot([xs], [-0.5], "o", ms=8, color=BLUE, zorder=4)
    ax.plot([xs], [-2.16], "o", ms=8, color=ACCENT, zorder=4)
    ax.text(xs + 0.18, -0.52, r"正源  $+\alpha'P$，深度 $z_r$", fontsize=8.5,
            color=BLUE, va="top")
    ax.text(xs + 0.18, -2.14, r"负源  $-\alpha'P$，深度 $z_v=z_r+2z_b$",
            fontsize=8.5, color=ACCENT, va="top")
    # 到外推平面上一点的距离
    xq = 6.2
    ax.plot([xq], [1.08], "o", ms=4, color=INK, zorder=5)
    for ys, c in ((-0.5, BLUE), (-2.16, ACCENT)):
        ax.plot([xq, xs], [1.08, ys], color=c, lw=0.9, ls=(0, (2, 2)), zorder=2)
    ax.text(4.55, 0.42, r"$d_r$", fontsize=9, color=BLUE)
    ax.text(4.20, -0.95, r"$d_v$", fontsize=9, color=ACCENT)
    ax.text(xq + 0.12, 1.20, "同一点", fontsize=8, color=INK)
    ax.annotate("", xy=(xs - 0.35, 0), xytext=(xs - 0.35, -0.5),
                arrowprops=dict(arrowstyle="<|-|>", color=GREY, lw=0.8,
                                mutation_scale=5))
    ax.annotate("", xy=(xs - 0.35, 1.08), xytext=(xs - 0.35, 0),
                arrowprops=dict(arrowstyle="<|-|>", color=GREY, lw=0.8,
                                mutation_scale=5))
    ax.text(xs - 0.45, -0.28, r"$z_r$", fontsize=8.5, ha="right", color=GREY)
    ax.text(xs - 0.45, 0.55, r"$z_b$", fontsize=8.5, ha="right", color=GREY)
    ax.text(0.0, -2.45, "介质", fontsize=9, color="#8a7a66")
    ax.text(0.0, 0.55, "外部", fontsize=9, color="#8a93a0")
    ax.set_xlim(-0.2, 8.2)
    ax.set_ylim(-2.6, 1.6)
    ax.set_xlabel("横向位置 r")
    ax.set_ylabel("深度 d")
    ax.set_yticks([-2.5, -2, -1, 0, 1])
    ax.set_yticklabels(["", "", "", "0", r"$-z_b$"])
    ax.grid(False)
    save(fig, "fig13-1-geometry.png")


def term(r, ma, ms, g, eta, which):
    st = sigma_tr(ma, ms, g)
    m = mu_eff(ma, ms, g)
    zb = zb_extrapolation(ma, ms, g, eta)
    zr = 1.0 / st
    zv = -(zr + 2 * zb)          # 有符号
    z = zr if which == 0 else zv
    d = np.sqrt(r * r + z * z)
    return np.sign(z) * z * (m * d + 1) * np.exp(-m * d) / d ** 3


def fig13_2():
    """两项的分解。"""
    ma, ms, g, eta = 0.02, 10.0, 0.8, 1.4
    r = np.linspace(0.0, 5.0, 400)
    ap = albedo_prime(ma, ms, g)
    t1 = ap / (4 * np.pi) * term(r, ma, ms, g, eta, 0)
    t2 = ap / (4 * np.pi) * term(r, ma, ms, g, eta, 1)
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.plot(r, t1, color=ACCENT, ls=(0, (5, 2)), label="第一项（正源）")
    ax.plot(r, np.abs(t2), color=BLUE, ls=(0, (1, 2)),
            label="第二项（虚源）")
    ax.plot(r, t1 + t2, color=INK, lw=2.0, label="两项之和")
    ax.set_yscale("log")
    ax.set_xlim(0, 5)
    ax.set_ylim(1e-5, 2)
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$R_d$ 的构成  (mm$^{-2}$)")
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig13-2-terms.png")


def fig13_3():
    """偶极子与蒙特卡洛。"""
    ma, ms, g = 0.002, 10.0, 0.8
    rng = np.random.default_rng(5)
    re, kind, ev = mc_slab(ma, ms, g, n_photons=150000, max_events=20000, rng=rng)
    ok = np.isfinite(re)
    edges = np.linspace(0, 8, 90)
    area = np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
    rc = 0.5 * (edges[:-1] + edges[1:])
    cnt, _ = np.histogram(re[ok], bins=edges)
    n_tot = re.size
    mc = cnt / (n_tot * area)
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.semilogy(rc, mc, color=BLUE, label="蒙特卡洛")
    ax.semilogy(rc, rd_dipole(rc, ma, ms, g, 1.0), color=ACCENT, label="偶极子")
    print("MC R", round(float(np.mean(kind == 0)), 3),
          "dipole", round(rd_total(lambda x: rd_dipole(x, ma, ms, g, 1.0), 40, 30000), 3))
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$R_d(r)$  (mm$^{-2}$)")
    ax.set_xlim(0, 8)
    ax.set_ylim(1e-5, 3)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.16)
    ax.annotate("近源处偏低", xy=(0.1, 0.55), xytext=(1.4, 1.7), fontsize=8,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    save(fig, "fig13-3-vs-mc.png")


if __name__ == "__main__":
    fig13_1()
    fig13_2()
    fig13_3()
