import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np


def sd_box(p, b):
    q = np.abs(p) - b
    return np.linalg.norm(np.maximum(q, 0.0), axis=-1) + np.minimum(np.max(q, -1), 0.0)


def sd_poly(P, verts):
    d = np.full(P.shape[:-1], 1e9)
    inside = np.zeros(P.shape[:-1], bool)
    v = [np.array(x, float) for x in verts]
    for i in range(len(v)):
        a, b = v[i], v[(i + 1) % len(v)]
        ba = b - a
        t = np.clip(((P - a) @ ba) / (ba @ ba), 0.0, 1.0)
        d = np.minimum(d, np.linalg.norm(P - a - t[..., None] * ba, axis=-1))
        cond = (a[1] > P[..., 1]) != (b[1] > P[..., 1])
        xint = a[0] + (b[0] - a[0]) * (P[..., 1] - a[1]) / (b[1] - a[1] + 1e-12)
        inside ^= cond & (P[..., 0] < xint)
    return np.where(inside, -d, d)


def panel(ax, X, Y, f, title, lim=0.42):
    ax.pcolormesh(X, Y, np.clip(f, -lim, lim), cmap="RdBu_r", shading="auto",
                  vmin=-lim, vmax=lim)
    ax.contour(X, Y, f, levels=[0.0], colors="black", linewidths=1.7)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.03, 0.96, title, transform=ax.transAxes, va="top", fontsize=8.3,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.82))


# ---------------------------------------------------------------- 图 8-1
def fig8_1():
    n = 400
    X, Y = np.meshgrid(np.linspace(-1.4, 1.4, n), np.linspace(-1.0, 1.0, n))
    P = np.stack([X, Y], -1)
    d = sd_box(P, np.array([0.62, 0.36]))

    fig, axes = plt.subplots(1, 3, figsize=(7.8, 2.55))
    panel(axes[0], X, Y, d - 0.22, "圆角  d − 0.22")
    panel(axes[1], X, Y, np.abs(d) - 0.09, "壳体  |d| − 0.09", lim=0.25)

    # 伸长：把坐标沿 x 夹取，再求值
    r = 0.55
    qx = X - np.clip(X, -r, r)
    q = np.stack([qx, Y], -1)
    el = sd_box(q, np.array([0.62, 0.30]))
    panel(axes[2], X, Y, el, "伸长  沿 x")
    fig.tight_layout()
    save(fig, "fig8-1-operators.png")


# ---------------------------------------------------------------- 图 8-2
L = [(-0.85, -0.80), (0.85, -0.80), (0.85, -0.20), (-0.25, -0.20),
     (-0.25, 0.80), (-0.85, 0.80)]


def fig8_2():
    n = 420
    X, Y = np.meshgrid(np.linspace(-1.2, 1.2, n), np.linspace(-1.1, 1.1, n))
    P = np.stack([X, Y], -1)
    d = sd_poly(P, L)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))
    ax = axes[0]
    for r, ls in ((0.0, "-"), (0.26, "--")):
        ax.contour(X, Y, d + r, levels=[0.0], colors="black" if r == 0 else ACCENT,
                   linewidths=1.6, linestyles=ls)
    r = 0.26
    bad = (d + r < 0)
    ax.contourf(X, Y, bad.astype(float), levels=[0.5, 1.5], colors=[RED], alpha=0.18)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.plot([], [], color="black", lw=1.6, label="原形状")
    ax.plot([], [], color=ACCENT, lw=1.6, ls="--", label="向内偏移 0.26")
    ax.fill_between([], [], color=RED, alpha=0.18, label="场判为内部、实际为空")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=3, fontsize=7.0)
    panel_label(ax, "(a)", x=-0.16, y=1.06)

    ax = axes[1]
    yy = 0.45
    xx = np.linspace(-1.15, 1.15, 800)
    P1 = np.stack([xx, np.full_like(xx, yy)], -1)
    d1 = sd_poly(P1, L)
    ax.plot(xx, d1, color=INK, lw=1.7, label="原距离场")
    ax.plot(xx, d1 + r, color=ACCENT, lw=1.7, ls="--", label="偏移 0.26")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel("沿 y = 0.45 的位置 x")
    ax.set_ylabel("距离值")
    ax.set_ylim(-0.7, 0.9)
    ax.legend(loc="upper right", fontsize=7.4)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig8-2-shrink.png")


# ---------------------------------------------------------------- 图 8-3
def curvature_at(r, h=2e-3):
    """半径 1 的圆收缩 r 之后，在零等值面上估曲率。"""
    R = 1.0 - r
    p = np.array([R, 0.0])

    def f(x, y):
        return np.hypot(x, y) - 1.0 + r

    fxx = (f(p[0] + h, 0.0) - 2 * f(p[0], 0.0) + f(p[0] - h, 0.0)) / h ** 2
    fyy = (f(0.0, p[1] + h) - 2 * f(0.0, p[1]) + f(0.0, p[1] - h)) / h ** 2
    return fyy if R < 0.3 else fyy


def fig8_3():
    rs = np.linspace(0.0, 0.94, 120)
    kappa, gmax = [], []
    for r in rs:
        R = 1.0 - r
        kappa.append(1.0 / R)
        X, Y = np.meshgrid(np.linspace(-1.2, 1.2, 200), np.linspace(-1.2, 1.2, 200))
        f = np.hypot(X, Y) - 1.0 + r
        h = 0.02
        gx = (np.hypot(X + h, Y) - np.hypot(X - h, Y)) / (2 * h)
        gy = (np.hypot(X, Y + h) - np.hypot(X, Y - h)) / (2 * h)
        gmax.append(np.hypot(gx, gy).max())

    fig, ax = plt.subplots(figsize=(6.3, 3.2))
    ax.semilogy(rs, kappa, color=RED, lw=1.8, label="零等值面的曲率 $1/(1-r)$")
    ax.semilogy(rs, gmax, color=BLUE, lw=1.6, label=r"场梯度长度最大值")
    ax.axvline(1.0, color=GREY, ls=":", lw=1.0)
    ax.text(0.96, 2.0, "r = 1：形状消失", fontsize=8, color="#3c4654", ha="right")
    ax.set_xlabel("向内偏移量 r")
    ax.set_ylabel("值（对数尺度）")
    ax.set_ylim(0.5, 100)
    ax.legend(loc="upper left", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig8-3-shrink-curvature.png")


if __name__ == "__main__":
    fig8_1()
    fig8_2()
    fig8_3()
