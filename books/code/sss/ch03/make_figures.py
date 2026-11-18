#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 3 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403
from matplotlib.patches import Arc, FancyArrowPatch
from bsdf import fresnel_dielectric


def fig3_1():
    """两个点、两个半球。"""
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    # 表面（略带透视的带子）
    ax.add_patch(plt.Polygon([(-0.1, 0.0), (7.2, 0.0), (6.9, -0.55), (-0.4, -0.55)],
                             closed=True, facecolor="#f0e6da", edgecolor="none",
                             zorder=0))
    ax.plot([-0.1, 7.2], [0, 0], color=INK, lw=1.4, zorder=2)
    xi = np.array([1.5, 0.0])
    xo = np.array([5.0, 0.0])
    # 半球弧
    for c, col, lab in ((xi, ACCENT, r"$\omega_i$"), (xo, BLUE, r"$\omega_o$")):
        ax.add_patch(Arc(c, 1.5, 1.5, theta1=0, theta2=180, color=col, lw=0.9,
                         ls=(0, (3, 2)), alpha=0.7))
        ax.plot([c[0], c[0]], [0, 0.75], color=GREY, lw=0.8, ls=(0, (2, 2)))
    # 方向箭头
    d_i = np.array([0.42, 0.62])
    d_o = np.array([0.45, 0.58])
    ax.annotate("", xy=xi + d_i, xytext=xi,
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.1,
                                mutation_scale=9))
    ax.annotate("", xy=xo + d_o, xytext=xo,
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.1,
                                mutation_scale=9))
    ax.text(xi[0] + 0.50, 0.68, r"$\omega_i$", color=ACCENT, fontsize=9)
    ax.text(xo[0] + 0.52, 0.64, r"$\omega_o$", color=BLUE, fontsize=9)
    # 内部路径
    th = np.linspace(0, 1, 60)
    px = xi[0] + (xo[0] - xi[0]) * th
    py = -0.30 * np.sin(np.pi * th) - 0.10
    ax.plot(px, py, color=TEAL, lw=1.1, ls=(0, (4, 2)), zorder=3)
    ax.plot(xi[0], -0.06, "o", ms=4, color=ACCENT, zorder=4)
    ax.plot(xo[0], -0.06, "o", ms=4, color=BLUE, zorder=4)
    ax.plot([1.5], [0.0], "o", ms=4.5, color=INK, zorder=5)
    ax.plot([5.0], [0.0], "o", ms=4.5, color=INK, zorder=5)
    ax.text(xi[0] - 0.05, -0.14, r"$x_i$", fontsize=10, ha="right", va="top")
    ax.text(xo[0] + 0.10, -0.14, r"$x_o$", fontsize=10, ha="left", va="top")
    # 距离
    ax.annotate("", xy=(xi[0], -0.80), xytext=(xo[0], -0.80),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=0.9,
                                mutation_scale=7))
    ax.text(3.25, -1.00, r"$r=\|x_i-x_o\|$", fontsize=9.5, ha="center")
    ax.plot([xi[0], xi[0]], [0.0, -0.80], color=GREY, lw=0.6, ls=(0, (2, 2)))
    ax.plot([xo[0], xo[0]], [0.0, -0.80], color=GREY, lw=0.6, ls=(0, (2, 2)))
    # 法线
    ax.text(1.35, 0.82, r"$n_i$", fontsize=9, color=GREY)
    ax.text(4.85, 0.82, r"$n_o$", fontsize=9, color=GREY)
    ax.text(6.35, -0.30, "介质", fontsize=8.5, color="#8a7a66")
    ax.set_xlim(-0.4, 7.3)
    ax.set_ylim(-1.15, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "fig3-1-geometry.png")


def fig3_2():
    """可分离形式的两半。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.7))
    ax = axes[0]
    r = np.linspace(0.0, 6.0, 400)
    for ma, c, lab in ((0.02, RED, r"$\alpha'=0.979$"),
                       (0.20, ACCENT, r"$\alpha'=0.83$"),
                       (0.80, BLUE, r"$\alpha'=0.55$")):
        ax.plot(r, rd_dipole(r, ma, 10.0, 0.8, 1.4), color=c, label=lab)
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$R_d(r)$  (mm$^{-2}$)")
    ax.set_yscale("log")
    ax.set_ylim(1e-5, 1.0)
    ax.set_xlim(0, 6)
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title(r"径向因子：$R_d(r)$", fontsize=9)
    ax.grid(True, which="both", alpha=0.16)

    ax = axes[1]
    th = np.linspace(0, 88, 300)
    Fi = fresnel_dielectric(np.cos(np.deg2rad(th)), 1.4)
    ax.plot(th, 1 - Fi, color=TEAL)
    ax.axhline(1.0, color=GREY, lw=0.8, ls=(0, (4, 3)))
    ax.set_xlabel(r"入射角 $\theta_i$ (度)")
    ax.set_ylabel(r"$F_t(\theta_i)$")
    ax.set_xlim(0, 88)
    ax.set_ylim(0, 1.05)
    ax.set_title("角向因子：界面透射率", fontsize=9)
    ax.annotate(r"$F_t(0)=0.97$", xy=(4, 0.98), xytext=(18, 0.86), fontsize=8,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    ax.annotate(r"掠射时几乎全反射", xy=(84, 0.30), xytext=(46, 0.40), fontsize=8,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    fig.subplots_adjust(wspace=0.30)
    save(fig, "fig3-2-separable.png")


def fig3_3():
    """总反射率随 α' 的变化。"""
    ap = np.linspace(0.30, 0.9995, 70)
    st = 2.0
    tot = []
    for a in ap:
        ms = st / (1 - 0.8)
        ma = ms * (1 - 0.8) * (1 - a) / a
        tot.append(rd_total(lambda r: rd_dipole(r, ma, ms, 0.8, 1.4), 30.0, 8000))
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    ax.plot(ap, tot, color=ACCENT)
    ax.plot([1.0], [tot[-1]], "o", ms=4, color=ACCENT)
    ax.annotate(f"{tot[-1]:.2f}", xy=(1.0, tot[-1]), xytext=(0.86, tot[-1] - 0.16),
                fontsize=8.5, color=ACCENT,
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.7))
    ax.set_xlabel(r"输运反照率 $\alpha'$")
    ax.set_ylabel("总反射率")
    ax.set_xlim(0.3, 1.02)
    ax.set_ylim(0, 1.02)
    ax.axhline(1.0, color=GREY, lw=0.8, ls=(0, (4, 3)))
    ax.text(0.33, 0.94, "物理上界", fontsize=8, color=GREY)
    save(fig, "fig3-3-albedo.png")


if __name__ == "__main__":
    fig3_1()
    fig3_2()
    fig3_3()
