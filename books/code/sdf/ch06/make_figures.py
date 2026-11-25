import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np


def smin_poly(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b + (a - b) * h - k * h * (1.0 - h)


def smin_exp(a, b, k):
    m = np.minimum(a, b)
    return m - k * np.log1p(np.exp(-np.abs(a - b) / k))


def smin_quart(a, b, k):
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.minimum(a, b) - h * h * k * 0.25


def sd_circle(p, c, r):
    return np.linalg.norm(p - c, axis=-1) - r


# ---------------------------------------------------------------- 图 6-1
def fig6_1():
    a = 0.0
    bb = np.linspace(-0.5, 0.5, 800)
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.1))

    ax = axes[0]
    k = 0.35
    ax.plot(bb, np.minimum(a, bb), color=INK, lw=1.6, label=r"$\min$（硬接缝）")
    ax.plot(bb, smin_poly(a, bb, k), color=BLUE, lw=1.6, label=r"多项式 $k=0.35$")
    ax.plot(bb, smin_exp(a, bb, k), color=TEAL, lw=1.5, ls="--", label=r"指数 $k=0.35$")
    ax.plot(bb, smin_quart(a, bb, k), color=ACCENT, lw=1.5, ls="-.", label=r"四次 $k=0.35$")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel(r"$b$（固定 $a=0$）")
    ax.set_ylabel("平滑最小值")
    ax.set_ylim(-0.45, 0.35)
    ax.legend(loc="upper left", fontsize=7.2)
    panel_label(ax, "(a)", x=-0.15, y=1.06)

    ax = axes[1]
    for k, col in ((0.1, SKY), (0.25, BLUE), (0.5, PURPLE)):
        ax.plot(bb, smin_poly(a, bb, k), color=col, lw=1.5, label=f"多项式 k = {k}")
    ax.plot(bb, np.minimum(a, bb), color=INK, lw=1.4, ls=":", label=r"$\min$")
    ax.set_xlabel(r"$b$（固定 $a=0$）")
    ax.set_ylabel("平滑最小值")
    ax.set_ylim(-0.6, 0.35)
    ax.legend(loc="upper left", fontsize=7.2)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig6-1-smin-curves.png")


# ---------------------------------------------------------------- 图 6-2
def fig6_2():
    n = 400
    xs = np.linspace(-1.9, 1.9, n)
    ys = np.linspace(-1.4, 1.4, n)
    X, Y = np.meshgrid(xs, ys)
    P = np.stack([X, Y], axis=-1)
    d1 = sd_circle(P, np.array([-0.55, 0.0]), 0.75)
    d2 = sd_circle(P, np.array([0.55, 0.0]), 0.75)

    fig, axes = plt.subplots(1, 3, figsize=(7.8, 2.75))
    for ax, k in zip(axes, (0.0, 0.20, 0.55)):
        f = np.minimum(d1, d2) if k == 0 else smin_poly(d1, d2, k)
        ax.pcolormesh(X, Y, np.clip(f, -0.4, 0.4), cmap="RdBu_r", shading="auto",
                      vmin=-0.4, vmax=0.4)
        ax.contour(X, Y, f, levels=[0.0], colors="black", linewidths=1.6)
        ax.contour(X, Y, f, levels=[0.1, 0.22], colors="#3d3d3d", linewidths=0.55)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.03, 0.96, "硬接缝" if k == 0 else f"k = {k}",
                transform=ax.transAxes, va="top", fontsize=8.4,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.82))
    fig.tight_layout()
    save(fig, "fig6-2-smin-2d.png")


# ---------------------------------------------------------------- 图 6-3
def fig6_3():
    n = 600
    xs = np.linspace(-1.9, 1.9, n)
    ys = np.linspace(-1.4, 1.4, n)
    X, Y = np.meshgrid(xs, ys)
    h = xs[1] - xs[0]
    d1 = sd_circle(np.stack([X, Y], -1), np.array([-0.55, 0.0]), 0.75)
    d2 = sd_circle(np.stack([X, Y], -1), np.array([0.55, 0.0]), 0.75)

    ks = np.linspace(0.02, 0.8, 40)
    gmax, gseam = [], []
    for k in ks:
        f = smin_poly(d1, d2, k)
        gx = (smin_poly(sd_circle(np.stack([X + h, Y], -1), np.array([-0.55, 0.0]), 0.75),
                        sd_circle(np.stack([X + h, Y], -1), np.array([0.55, 0.0]), 0.75), k)
              - smin_poly(sd_circle(np.stack([X - h, Y], -1), np.array([-0.55, 0.0]), 0.75),
                          sd_circle(np.stack([X - h, Y], -1), np.array([0.55, 0.0]), 0.75), k)) / (2 * h)
        gy = (smin_poly(sd_circle(np.stack([X, Y + h], -1), np.array([-0.55, 0.0]), 0.75),
                        sd_circle(np.stack([X, Y + h], -1), np.array([0.55, 0.0]), 0.75), k)
              - smin_poly(sd_circle(np.stack([X, Y - h], -1), np.array([-0.55, 0.0]), 0.75),
                          sd_circle(np.stack([X, Y - h], -1), np.array([0.55, 0.0]), 0.75), k)) / (2 * h)
        g = np.hypot(gx, gy)
        near = (np.abs(f) < 0.02) & (np.abs(X) < 0.35)
        gmax.append(g.max())
        gseam.append(g[near].mean())

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.1))
    ax = axes[0]
    ax.plot(ks, gmax, color=RED, lw=1.6, label="区域内最大梯度长度")
    ax.plot(ks, gseam, color=BLUE, lw=1.6, label="接缝附近平均梯度长度")
    ax.axhline(1.0, color=GREY, ls=":", lw=1.1, label="1（精确距离）")
    ax.axhline(1.0 / np.sqrt(2), color=GREY, ls="-.", lw=1.1, label=r"$1/\sqrt{2}$")
    ax.set_xlabel("平滑参数 k")
    ax.set_ylabel(r"$\Vert\nabla f\Vert$")
    ax.set_ylim(0.5, 1.1)
    ax.legend(loc="lower right", fontsize=7.2)
    panel_label(ax, "(a)", x=-0.15, y=1.06)

    ax = axes[1]
    yy = np.linspace(-1.3, 1.3, 700)
    P1 = np.stack([np.zeros_like(yy), yy], -1)
    e1 = sd_circle(P1, np.array([-0.55, 0.0]), 0.75)
    e2 = sd_circle(P1, np.array([0.55, 0.0]), 0.75)
    ax.plot(yy, np.minimum(e1, e2), color=INK, lw=1.5, label="min")
    ax.plot(yy, smin_poly(e1, e2, 0.20), color=BLUE, lw=1.5, label="k = 0.20")
    ax.plot(yy, smin_poly(e1, e2, 0.55), color=PURPLE, lw=1.5, label="k = 0.55")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel("沿 x = 0（两圆对称面）的位置 y")
    ax.set_ylabel("场值")
    ax.set_ylim(-0.4, 0.6)
    ax.legend(loc="lower right", fontsize=7.2)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig6-3-smin-lipschitz.png")


if __name__ == "__main__":
    fig6_1()
    fig6_2()
    fig6_3()
