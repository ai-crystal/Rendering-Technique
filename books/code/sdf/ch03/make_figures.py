import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np


def sd_box(p, b):
    q = np.abs(p) - b
    outside = np.linalg.norm(np.maximum(q, 0.0), axis=-1)
    inside = np.minimum(np.maximum(q[..., 0], q[..., 1]), 0.0)
    return outside + inside


def sd_capsule(p, a, b, r):
    pa = p - a
    ba = b - a
    h = np.clip(np.sum(pa * ba, -1) / np.dot(ba, ba), 0.0, 1.0)
    return np.linalg.norm(pa - h[..., None] * ba, axis=-1) - r


def sd_capped_cone(p, h, r1, r2):
    q = np.stack([np.linalg.norm(p[:, :1], axis=-1), p[:, 1]], -1)
    k1 = np.array([r2, h])
    k2 = np.array([r2 - r1, 2.0 * h])
    sel = np.where(q[:, 1:2] < 0.0, r1, r2)
    ca = np.stack([q[:, 0] - np.minimum(q[:, 0], sel[:, 0]), np.abs(q[:, 1]) - h], -1)
    t = np.clip(np.sum((k1 - q) * k2, -1) / np.dot(k2, k2), 0.0, 1.0)
    cb = q - k1 + t[:, None] * k2
    s = np.where((cb[:, 0] < 0.0) & (ca[:, 1] < 0.0), -1.0, 1.0)
    return s * np.sqrt(np.minimum(np.sum(ca * ca, -1), np.sum(cb * cb, -1)))


def sd_cone(p, H, r1, r2):
    """底半径 r1 在 y=0，顶半径 r2 在 y=H。iq 的公式以 y=0 为中面，这里平移。"""
    h = 0.5 * H
    q = np.array(p, dtype=float, copy=True)
    q[:, 1] -= h
    return sd_capped_cone(q, h, r1, r2)


def grid(x0, x1, y0, y1, n=420):
    xs = np.linspace(x0, x1, n)
    ys = np.linspace(y0, y1, n)
    X, Y = np.meshgrid(xs, ys)
    return X, Y, np.stack([X, Y], -1)


def shape_panel(ax, X, Y, d, title):
    lim = 0.5
    ax.pcolormesh(X, Y, np.clip(d, -lim, lim), cmap="RdBu_r", shading="auto",
                  vmin=-lim, vmax=lim)
    ax.contour(X, Y, d, levels=[-0.3, -0.15, 0.08, 0.16, 0.3, 0.45],
               colors="#3a3a3a", linewidths=0.6)
    ax.contour(X, Y, d, levels=[0.0], colors="black", linewidths=1.7)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.03, 0.96, title, transform=ax.transAxes, ha="left", va="top",
            fontsize=8.5, color="#1f2430",
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none", alpha=0.8))


# ---------------------------------------------------------------- 图 3-1
def fig3_1():
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.8))
    X, Y, P = grid(-1.25, 1.25, -1.25, 1.25, 360)

    ax = axes[0]
    d = sd_box(P, np.array([0.70, 0.45]))
    shape_panel(ax, X, Y, d, "盒（圆角为零）")

    ax = axes[1]
    d = sd_capsule(P, np.array([-0.72, 0.0]), np.array([0.72, 0.0]), 0.34)
    shape_panel(ax, X, Y, d, "胶囊")

    ax = axes[2]
    flat = P.reshape(-1, 2)
    d = sd_cone(np.stack([flat[:, 0], flat[:, 1]], -1), 0.75, 0.62, 0.12)
    shape_panel(ax, X, Y, d.reshape(X.shape), "圆台（底 0.62，顶 0.12，高 0.75）")

    fig.tight_layout()
    save(fig, "fig3-1-shapes.png")


# ---------------------------------------------------------------- 图 3-2
def cone_truth(p, h, r1, r2):
    """圆台边界的真实距离，用两条圆（上下底）与侧线采样求最小。"""
    th = np.linspace(0, 2 * np.pi, 720, endpoint=False)
    pts = []
    for rr, yy in ((r1, 0.0), (r2, h)):
        pts.append(np.stack([rr * np.cos(th), np.full_like(th, yy)], -1))
    s = np.linspace(0, 1, 400)
    pts.append(np.stack([(r1 + (r2 - r1) * s) + 0 * s, s * h], -1))
    pts = np.concatenate(pts)
    flat = p.reshape(-1, 2)
    far = np.min(np.linalg.norm(flat[:, None, :] - pts[None, ::4, :], axis=-1), axis=1)
    sgn = np.where(sd_cone(np.stack([flat[:, 0], flat[:, 1]], -1), h, r1, r2) < 0,
                   -1.0, 1.0)
    return (sgn * far).reshape(p.shape[:-1])


def fig3_2():
    H, r1, r2 = 0.75, 0.62, 0.18
    # 侧面所在的平面，法向朝外
    n = np.array([H, r1 - r2], float)
    n = n / np.linalg.norm(n)
    a = np.array([r1, 0.0])

    X, Y, P = grid(-0.9, 1.0, -0.15, 0.9, 420)
    flat = P.reshape(-1, 2)
    ex = sd_cone(np.stack([flat[:, 0], flat[:, 1]], -1), H, r1, r2).reshape(X.shape)
    lin = (X - a[0]) * n[0] + (Y - a[1]) * n[1]

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.1))
    ax = axes[0]
    lv = [0.06, 0.12, 0.2, 0.3, 0.42]
    ax.contour(X, Y, ex, levels=lv, colors=BLUE, linewidths=0.9)
    ax.contour(X, Y, lin, levels=lv, colors=RED, linewidths=0.9, linestyles="--")
    ax.contour(X, Y, ex, levels=[0.0], colors="black", linewidths=1.8)
    ax.set_aspect("equal")
    ax.set_xlabel("半径方向 r")
    ax.set_ylabel("高度 y")
    ax.plot([], [], color=BLUE, lw=1.2, label="精确圆台公式")
    ax.plot([], [], color=RED, lw=1.2, ls="--", label="侧面平面式")
    ax.legend(loc="upper right", fontsize=7.5)
    panel_label(ax, "(a)", x=-0.16, y=1.06)

    ax = axes[1]
    xx = np.linspace(-1.0, 1.0, 700)
    pp = np.stack([xx, np.full_like(xx, 0.30)], -1)
    d_ex = sd_cone(pp, H, r1, r2)
    d_lin = (xx - a[0]) * n[0] + (0.30 - a[1]) * n[1]
    ax.plot(xx, d_ex, color=BLUE, lw=1.7, label="精确圆台公式")
    ax.plot(xx, d_lin, color=RED, lw=1.5, ls="--", label="侧面平面式")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.text(-0.95, -0.72, "顶面附近精确式取平，平面式继续线性增长", fontsize=8,
            color="#3c4654", va="bottom")
    ax.set_xlabel("沿 y = 0.30 的位置 r")
    ax.set_ylabel("距离值")
    ax.set_ylim(-0.8, 0.6)
    ax.legend(loc="upper left", fontsize=7.5)
    panel_label(ax, "(b)", x=-0.14, y=1.06)
    fig.tight_layout()
    save(fig, "fig3-2-cone-error.png")


# ---------------------------------------------------------------- 图 3-3
def poly_edges(verts):
    return [(verts[i], verts[(i + 1) % len(verts)]) for i in range(len(verts))]


def seg_dist(p, a, b):
    pa = p - a
    ba = b - a
    t = np.clip(np.sum(pa * ba, -1) / np.dot(ba, ba), 0.0, 1.0)
    return np.linalg.norm(pa - t[..., None] * ba, axis=-1)


def sd_polygon_true(P, verts):
    e = poly_edges(verts)
    d = np.full(P.shape[:-1], 1e9)
    for a, b in e:
        d = np.minimum(d, seg_dist(P, np.array(a), np.array(b)))
    # 奇偶判断符号
    inside = np.zeros(P.shape[:-1], bool)
    x, y = P[..., 0], P[..., 1]
    for a, b in e:
        cond = ((a[1] > y) != (b[1] > y))
        xint = (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1] + 1e-12) + a[0]
        inside ^= cond & (x < xint)
    return np.where(inside, -d, d)


def sd_polygon_halfplanes(P, verts):
    """凸多边形的 max 形式；对非凸多边形照用会出错。"""
    vals = []
    cx, cy = np.mean(np.array(verts), axis=0)
    for a, b in poly_edges(verts):
        a = np.array(a, float)
        b = np.array(b, float)
        e = b - a
        nrm = np.array([e[1], -e[0]])
        nrm = nrm / np.linalg.norm(nrm)
        if np.dot(nrm, np.array([cx, cy]) - a) > 0:
            nrm = -nrm
        vals.append((P[..., 0] - a[0]) * nrm[0] + (P[..., 1] - a[1]) * nrm[1])
    return np.max(np.stack(vals, -1), -1)


def fig3_3():
    L = [(-0.75, -0.75), (0.75, -0.75), (0.75, -0.15), (-0.15, -0.15),
         (-0.15, 0.75), (-0.75, 0.75)]
    X, Y, P = grid(-1.3, 1.3, -1.3, 1.3, 420)
    dtrue = sd_polygon_true(P, L)
    dhp = sd_polygon_halfplanes(P, L)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))
    ax = axes[0]
    ax.contour(X, Y, dtrue, levels=[0.0, 0.15, 0.3, 0.45, 0.6],
               colors="#3a3a3a", linewidths=0.7)
    ax.contour(X, Y, dtrue, levels=[0.0], colors="black", linewidths=1.7)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    note(ax, "L 形多边形与真实距离等值线", 0.02, 0.97, size=8.5)
    panel_label(ax, "(a)", x=-0.16, y=1.06)

    ax = axes[1]
    xx = np.linspace(-1.3, 1.3, 700)
    pp = np.stack([xx, np.full_like(xx, 0.35)], -1)
    t = sd_polygon_true(pp, L)
    hp = sd_polygon_halfplanes(pp, L)
    ax.plot(xx, t, color=INK, lw=1.7, label="真实距离")
    ax.plot(xx, hp, color=RED, lw=1.5, ls="--", label="六个半平面取最大")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel("沿 y = 0.35 的位置 x")
    ax.set_ylabel("距离值")
    ax.legend(loc="lower right", fontsize=7.5)
    ax.set_ylim(-0.85, 1.0)
    panel_label(ax, "(b)", x=-0.14, y=1.06)
    fig.tight_layout()
    save(fig, "fig3-3-polygon.png")


if __name__ == "__main__":
    fig3_1()
    fig3_2()
    fig3_3()
