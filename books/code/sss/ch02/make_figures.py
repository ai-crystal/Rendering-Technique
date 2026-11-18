#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 2 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403
from matplotlib.patches import Arc


def fig2_1():
    """辐亮度定义里的两个投影。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.9))

    # ---------------- (a) 光束与表面
    ax = axes[0]
    th = np.deg2rad(36.0)
    u = np.array([-np.sin(th), -np.cos(th)])       # 入射方向（向下）
    up = -u
    w = 0.46
    A = np.array([-w / 2, 0.0])
    B = np.array([w / 2, 0.0])
    ax.plot([-0.78, 0.78], [0, 0], color=INK, lw=1.6, zorder=3)
    for P in (A, B):
        Q = P + 1.55 * up
        ax.plot([P[0], Q[0]], [P[1], Q[1]], color=SKY, lw=1.0, zorder=2)
    ax.add_patch(plt.Polygon([A, B, B + 1.55 * up, A + 1.55 * up],
                             closed=True, facecolor=SKY, alpha=0.14,
                             edgecolor="none", zorder=1))
    ax.plot([0, 0], [0, 0.75], color=GREY, lw=0.9, ls=(0, (4, 3)), zorder=3)
    ax.add_patch(Arc((0, 0), 0.62, 0.62, theta1=90,
                     theta2=90 + np.rad2deg(th), color=INK, lw=0.9))
    ax.text(-0.19, 0.30, r"$\theta$", fontsize=9.5)
    M = A + 1.02 * up
    t = float(np.dot(M - B, u))
    N = B + t * u
    ax.plot([M[0], N[0]], [M[1], N[1]], color=BLUE, lw=1.2, zorder=4)
    ax.plot([M[0], N[0]], [M[1], N[1]], "o", ms=2.6, color=BLUE, zorder=5)
    ax.annotate(r"$dA\cos\theta$", xy=(0.5 * (M[0] + N[0]), 0.5 * (M[1] + N[1])),
                xytext=(0.16, 1.30), fontsize=8.5, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.7))
    ax.annotate("", xy=A, xytext=B,
                arrowprops=dict(arrowstyle="<|-|>", color=ACCENT, lw=1.0,
                                mutation_scale=7))
    ax.text(0.0, -0.13, r"$dA$", color=ACCENT, fontsize=9, ha="center")
    ax.text(-0.72, 1.40, "入射光", fontsize=8.5, color=SKY)
    ax.text(-0.74, 0.60, "法线", fontsize=8, color=GREY)
    ax.set_xlim(-0.80, 0.80)
    ax.set_ylim(-0.22, 1.55)
    ax.set_aspect("equal")
    ax.axis("off")
    panel_label(ax, "(a)", x=-0.08, y=1.06)

    # ---------------- (b) 同一立体角在两个屏上的脚印
    ax = axes[1]
    o = np.array([-0.92, 0.0])
    Lp = 0.92
    tilt = np.deg2rad(38.0)
    h = Lp * np.tan(np.deg2rad(16.0))
    c = np.array([o[0] + Lp, 0.0])
    top = c + np.array([0.0, h])
    bot = c - np.array([0.0, h])
    for P in (top, bot):
        k = 1.42
        ax.plot([o[0], o[0] + k * (P[0] - o[0])],
                [o[1], o[1] + k * (P[1] - o[1])],
                color=SKY, lw=0.9, zorder=2)
    ax.add_patch(Arc(o, 0.52, 0.52, theta1=-16, theta2=16, color=GREY, lw=0.8))
    ax.text(o[0] + 0.40, -0.075, r"$d\omega$", fontsize=8.5, color=GREY)
    ax.plot([top[0], bot[0]], [top[1], bot[1]], color=BLUE, lw=1.6, zorder=3)
    ax.text(c[0] - 0.03, h + 0.05, r"$A_\perp$", fontsize=8.5, color=BLUE,
            ha="right")
    e = np.array([np.sin(tilt), np.cos(tilt)])
    s2 = h / np.cos(tilt)
    ax.plot([c[0] - e[0] * s2, c[0] + e[0] * s2],
            [c[1] - e[1] * s2, c[1] + e[1] * s2], color=ACCENT, lw=1.6,
            zorder=3)
    ax.add_patch(Arc(c, 0.30, 0.30, theta1=90,
                     theta2=90 + np.rad2deg(tilt), color=INK, lw=0.9))
    ax.text(c[0] + 0.055, 0.135, r"$\theta$", fontsize=9)
    ax.text(c[0] + 0.06, -h - 0.30, r"$A=A_\perp/\cos\theta$", fontsize=8.5,
            color=ACCENT, ha="center")
    ax.set_xlim(-1.05, 1.55)
    ax.set_ylim(-0.72, 0.55)
    ax.set_aspect("equal")
    ax.axis("off")
    panel_label(ax, "(b)", x=-0.02, y=1.16)

    fig.subplots_adjust(wspace=0.03)
    save(fig, "fig2-1-solid-angle.png")


def fig2_2():
    """P1 近似的极坐标形状。"""
    fig = plt.figure(figsize=(3.9, 3.9))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_position([0.12, 0.14, 0.76, 0.76])
    th = np.linspace(0, 2 * np.pi, 400)
    for k, c, lab in ((0.0, GREY, "各向同性"),
                      (0.5, TEAL, "轻微漂移"),
                      (0.92, RED, "强漂移")):
        ax.plot(th, (1.0 + k * np.cos(th)) / (4 * np.pi), color=c, lw=1.6,
                label=lab)
    ax.set_rlim(0, 0.20)
    ax.set_rticks([])
    ax.set_thetagrids([0, 90, 180, 270], ["漂移方向", "90°", "180°", "270°"],
                      fontsize=8)
    ax.grid(alpha=0.25)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=3,
              fontsize=8, handlelength=1.4, columnspacing=0.9)
    ax.set_title(r"$L=\dfrac{1}{4\pi}(\phi+3E\cos\theta)$", fontsize=9, pad=10)
    save(fig, "fig2-2-p1-polar.png")


if __name__ == "__main__":
    fig2_1()
    fig2_2()
