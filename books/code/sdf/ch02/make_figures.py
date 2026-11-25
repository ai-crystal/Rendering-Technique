import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np


def sd_circle(p, c, r):
    return np.linalg.norm(p - c, axis=-1) - r


def sd_box(p, c, b):
    q = np.abs(p - c) - b
    outside = np.linalg.norm(np.maximum(q, 0.0), axis=-1)
    inside = np.minimum(np.maximum(q[..., 0], q[..., 1]), 0.0)
    return outside + inside


C1 = np.array([-0.30, 0.0])
C2 = np.array([1.02, 0.0])
R = 0.90
BC = np.array([0.62, 0.0])
BH = np.array([0.68, 0.50])

# ---------------------------------------------------------------- 图 2-1
def fig2_1():
    c1 = np.array([-1.02, 0.0])
    c2 = np.array([1.02, 0.0])
    r = 0.56
    n = 700
    xs = np.linspace(-2.2, 2.2, n)
    ys = np.linspace(-1.6, 1.6, n)
    X, Y = np.meshgrid(xs, ys)
    P = np.stack([X, Y], axis=-1)
    d1 = sd_circle(P, c1, r)
    d2 = sd_circle(P, c2, r)
    d = np.minimum(d1, d2)

    # 中轴：两个不同最近点距离相等，位于两圆之间的对称面上

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.3))
    ax = axes[0]
    ax.contour(X, Y, d, levels=[-0.45, -0.25, 0.0, 0.15, 0.30, 0.45, 0.60],
               colors="#4a4a4a", linewidths=0.75)
    ax.contour(X, Y, d, levels=[0.0], colors="black", linewidths=1.8)
    ax.plot([0.0, 0.0], [-1.55, 1.55], color=RED, lw=1.0, ls=(0, (4, 2)))
    ax.annotate("中轴", (0.0, 1.30), xytext=(0.12, 1.42), fontsize=8, color=RED)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    panel_label(ax, "(a)", x=-0.20, y=1.06)

    ax = axes[1]
    xx = np.linspace(-1.9, 1.9, 900)
    p = np.stack([xx, np.zeros_like(xx)], axis=-1)
    a = sd_circle(p, c1, r)
    b = sd_circle(p, c2, r)
    ax.plot(xx, a, color=BLUE, lw=1.0, ls="--", label=r"$d_1$（左圆）")
    ax.plot(xx, b, color=TEAL, lw=1.0, ls="--", label=r"$d_2$（右圆）")
    ax.plot(xx, np.minimum(a, b), color=INK, lw=1.9, label=r"$\min(d_1,d_2)$")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.plot([0.0], [1.02 - r], "o", ms=5, color=RED)
    ax.annotate("中轴：梯度由 +1 跳到 -1", (0.02, 1.02 - r + 0.03), xytext=(-1.55, 1.30),
                fontsize=8, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
    ax.set_xlabel("沿 x 轴的位置")
    ax.set_ylabel("距离值")
    ax.set_ylim(-1.0, 1.95)
    ax.legend(loc="upper center", ncol=3, fontsize=7.5, bbox_to_anchor=(0.5, -0.2))
    panel_label(ax, "(b)", x=-0.16, y=1.06)
    fig.tight_layout()
    save(fig, "fig2-1-medial-axis.png")


# ---------------------------------------------------------------- 图 2-2
def true_union_distance(P):
    # 圆与盒子并集的边界采样点
    th = np.linspace(0, 2 * np.pi, 2400, endpoint=False)
    circ = np.stack([np.cos(th) * R, np.sin(th) * R], -1)
    circ = np.stack([circ[:, 0] + C1[0], circ[:, 1] + C1[1]], -1)
    keep1 = sd_box(circ, BC, BH) > 0
    keep2 = np.zeros(0, bool)
    circ2 = np.zeros((0, 2))

    s = np.linspace(-BH[0], BH[0], 900)
    sy = np.linspace(-BH[1], BH[1], 600)
    box_pts = [
        np.stack([BC[0] + s, np.full_like(s, BC[1] - BH[1])], -1),
        np.stack([BC[0] + s, np.full_like(s, BC[1] + BH[1])], -1),
        np.stack([np.full_like(sy, BC[0] - BH[0]), BC[1] + sy], -1),
        np.stack([np.full_like(sy, BC[0] + BH[0]), BC[1] + sy], -1),
    ]
    box_pts = np.concatenate(box_pts)
    keep = sd_circle(box_pts, C1, R) > 0

    pts = np.concatenate([circ[keep1], circ2[keep2], box_pts[keep]])
    flat = P.reshape(-1, 2)
    dmin = np.full(flat.shape[0], 1e9)
    for k in range(0, pts.shape[0], 200):
        blk = pts[k:k + 200]
        dist = np.linalg.norm(flat[:, None, :] - blk[None, :, :], axis=-1).min(axis=1)
        dmin = np.minimum(dmin, dist)
    sgn = np.where(np.minimum(sd_circle(P, C1, R), sd_box(P, BC, BH)) < 0, -1.0, 1.0)
    return (sgn.reshape(-1) * dmin).reshape(P.shape[:-1])


def fig2_2():
    n = 360
    xs = np.linspace(-1.9, 2.0, n)
    ys = np.linspace(-1.35, 1.35, n)
    X, Y = np.meshgrid(xs, ys)
    P = np.stack([X, Y], axis=-1)
    f = np.minimum(sd_circle(P, C1, R), sd_box(P, BC, BH))
    dtrue = true_union_distance(P)
    err = f - dtrue

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))
    ax = axes[0]
    lim = 0.42
    im = ax.pcolormesh(X, Y, np.clip(err, -lim, lim), cmap="PuOr_r",
                       shading="auto", vmin=-lim, vmax=lim)
    ax.contour(X, Y, f, levels=[0.0], colors="black", linewidths=1.2)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    cb = fig.colorbar(im, ax=ax, fraction=0.042, pad=0.02)
    cb.set_label("场值减真实距离", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    panel_label(ax, "(a)", x=-0.18, y=1.05)

    ax = axes[1]
    yy = 0.0
    xx = np.linspace(-1.9, 2.0, 800)
    P1 = np.stack([xx, np.full_like(xx, yy)], axis=-1)
    f1 = np.minimum(sd_circle(P1, C1, R), sd_box(P1, BC, BH))
    t1 = true_union_distance(P1)
    ax.plot(xx, t1, color=INK, lw=1.6, label="真实距离")
    ax.plot(xx, f1, color=ACCENT, lw=1.6, ls="--", label=r"$\min(d_1,d_2)$")
    ax.fill_between(xx, f1, t1, where=(f1 < t1 - 1e-4), color=ACCENT, alpha=0.18)
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel("沿 y = 0 的位置 x")
    ax.set_ylabel("距离值")
    ax.legend(loc="upper right", fontsize=7.5)
    ax.set_ylim(-0.95, 1.3)
    panel_label(ax, "(b)", x=-0.14, y=1.05)
    fig.tight_layout()
    save(fig, "fig2-2-union-error.png")


# ---------------------------------------------------------------- 图 2-3
def fig2_3():
    y0 = 0.35
    def dist(x):
        return np.sqrt(x * x + y0 * y0) - 1.0

    def trace(scale, eps=1e-3, maxit=64):
        x, pts = -3.0, [-3.0]
        for _ in range(maxit):
            v = scale * dist(x)
            if v < eps:
                break
            x = x + v
            pts.append(x)
            if x > 3.0:
                break
        return np.array(pts), dist(x) < 0

    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    rows = [(r"精确场 $d$", 1.0, BLUE, 2.0),
            (r"保守场 $0.7d$", 0.7, TEAL, 1.0),
            (r"放大场 $1.6d$", 1.6, RED, 0.0)]
    for label, s, col, ypos in rows:
        pts, crossed = trace(s)
        ax.plot(pts, np.full_like(pts, ypos), "|", ms=12, mew=1.5, color=col)
        txt = f"{label}，{len(pts)} 步"
        if crossed:
            txt += "，已穿过表面"
        ax.text(-3.5, ypos + 0.22, txt, fontsize=8, color=col, va="bottom")

    for xv in (-1.0, 1.0):
        ax.axvline(xv, color=GREY, ls=":", lw=0.9)
    ax.text(-1.0, -0.42, "表面", fontsize=8, color=GREY, ha="center")
    ax.text(1.0, -0.42, "表面", fontsize=8, color=GREY, ha="center")
    ax.set_xlim(-3.6, 3.4)
    ax.set_ylim(-0.6, 2.8)
    ax.set_yticks([])
    ax.set_xlabel("沿光线的位置 x（竖条为每步落点）")
    fig.tight_layout()
    save(fig, "fig2-3-step-scaling.png")


if __name__ == "__main__":
    fig2_1()
    fig2_2()
    fig2_3()
