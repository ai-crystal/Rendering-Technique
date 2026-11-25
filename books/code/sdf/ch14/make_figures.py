import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.ticker import NullFormatter
import numpy as np


# ---------------------------------------------------------------- 图 14-1
def chamfer2d(occ, a=1.0, b=np.sqrt(2.0)):
    """两遍扫描的 chamfer 距离变换，occ 为内部掩码。"""
    n, m = occ.shape
    d = np.where(occ, 0.0, np.inf)
    for i in range(n):
        for j in range(m):
            v = d[i, j]
            if i > 0:
                v = min(v, d[i - 1, j] + a)
                if j > 0:
                    v = min(v, d[i - 1, j - 1] + b)
                if j < m - 1:
                    v = min(v, d[i - 1, j + 1] + b)
            if j > 0:
                v = min(v, d[i, j - 1] + a)
            d[i, j] = v
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            v = d[i, j]
            if i < n - 1:
                v = min(v, d[i + 1, j] + a)
                if j > 0:
                    v = min(v, d[i + 1, j - 1] + b)
                if j < m - 1:
                    v = min(v, d[i + 1, j + 1] + b)
            if j < m - 1:
                v = min(v, d[i, j + 1] + a)
            d[i, j] = v
    return d


def fig14_1():
    h = 0.02
    n = 121
    xs = (np.arange(n) - n // 2) * h
    X, Y = np.meshgrid(xs, xs)
    R = 0.85
    occ = X ** 2 + Y ** 2 <= R ** 2
    cham = chamfer2d(occ) * h
    exact = np.abs(np.hypot(X, Y) - R)
    err = cham - exact

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.1))
    ax = axes[0]
    im = ax.pcolormesh(X, Y, err, cmap="PuOr_r", shading="auto", vmin=-0.02, vmax=0.02)
    ax.contour(X, Y, exact, levels=[0.0], colors="black", linewidths=1.2)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label("chamfer 减精确距离", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    panel_label(ax, "(a)", x=-0.16, y=1.06)

    ax = axes[1]
    ax.plot(exact.ravel()[::37], err.ravel()[::37], ".", ms=1.6, color=BLUE, alpha=0.5)
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel("离表面的距离")
    ax.set_ylabel("误差")
    ax.set_ylim(-0.03, 0.03)
    ax.text(0.30, -0.022, "误差随距离增长，约 5% 的相对误差", fontsize=8, color="#3c4654")

    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig14-1-chamfer.png")


# ---------------------------------------------------------------- 图 14-2
def crossing(P, verts):
    inside = np.zeros(P.shape[:-1], bool)
    for i in range(len(verts)):
        a, b = verts[i], verts[(i + 1) % len(verts)]
        cond = (a[1] > P[..., 1]) != (b[1] > P[..., 1])
        xint = a[0] + (b[0] - a[0]) * (P[..., 1] - a[1]) / (b[1] - a[1] + 1e-12)
        inside ^= cond & (P[..., 0] < xint)
    return inside


def winding(P, verts):
    w = np.zeros(P.shape[:-1])
    for i in range(len(verts)):
        a, b = verts[i], verts[(i + 1) % len(verts)]
        cond = (a[1] > P[..., 1]) != (b[1] > P[..., 1])
        xint = a[0] + (b[0] - a[0]) * (P[..., 1] - a[1]) / (b[1] - a[1] + 1e-12)
        up = (b[1] - a[1]) > 0
        w += np.where(cond & (P[..., 0] < xint), np.where(up, 1.0, -1.0), 0.0)
    return w


def fig14_2():
    n = 5
    verts = []
    for k in range(n):
        ang = np.pi / 2 + 2 * np.pi * k * 2 / n
        verts.append((0.9 * np.cos(ang), 0.9 * np.sin(ang)))

    X, Y = np.meshgrid(np.linspace(-1.15, 1.15, 460), np.linspace(-1.15, 1.15, 460))
    P = np.stack([X, Y], -1)
    cr = crossing(P, verts).astype(float)
    wd = winding(P, verts)
    wd_in = (np.abs(wd) > 0.5).astype(float)
    diff = np.abs(cr - wd_in)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.3))
    ax = axes[0]
    ax.contourf(X, Y, cr, levels=[0.5, 1.5], colors=["#c8d7e8"])
    for i in range(n):
        a, b = verts[i], verts[(i + 1) % n]
        ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=1.3)
    ax.set_aspect("equal")
    ax.set_title("交叉奇偶判定的内部", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])

    ax = axes[1]
    ax.contourf(X, Y, wd_in, levels=[0.5, 1.5], colors=["#e8cfc8"])
    ax.contourf(X, Y, diff, levels=[0.5, 1.5], colors=["#b0453c"], alpha=0.55)
    for i in range(n):
        a, b = verts[i], verts[(i + 1) % n]
        ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=1.3)
    ax.set_aspect("equal")
    ax.set_title("绕数判定的内部，差异区填红", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    save(fig, "fig14-2-winding.png")


# ---------------------------------------------------------------- 图 14-3
def fig14_3():
    hs = np.logspace(np.log10(0.16), np.log10(0.012), 24)
    rms, nerr = [], []
    rng = np.random.default_rng(1)
    for h in hs:
        n = int(2.4 / h)
        g = (np.arange(n) + 0.5) * h - 1.2
        X, Y = np.meshgrid(g, g)
        F = np.hypot(X, Y) - 0.8
        # 三线性插值（二维双线性）
        pts = rng.random((4000, 2)) * 2.2 - 1.1
        u = (pts[:, 0] + 1.2) / h - 0.5
        v = (pts[:, 1] + 1.2) / h - 0.5
        i0 = np.clip(np.floor(u).astype(int), 0, n - 2)
        j0 = np.clip(np.floor(v).astype(int), 0, n - 2)
        tu, tv = u - i0, v - j0
        f00 = F[j0, i0]; f10 = F[j0, i0 + 1]
        f01 = F[j0 + 1, i0]; f11 = F[j0 + 1, i0 + 1]
        val = (f00 * (1 - tu) * (1 - tv) + f10 * tu * (1 - tv)
               + f01 * (1 - tu) * tv + f11 * tu * tv)
        ref = np.hypot(pts[:, 0], pts[:, 1]) - 0.8
        rms.append(np.sqrt(np.mean((val - ref) ** 2)))
        # 法线：由插值场的差分得到
        gx = ((f10 - f00) * (1 - tv) + (f11 - f01) * tv) / h
        gy = ((f01 - f00) * (1 - tu) + (f11 - f10) * tu) / h
        ang = np.degrees(np.arccos(np.clip(
            (gx * pts[:, 0] + gy * pts[:, 1]) /
            (np.hypot(gx, gy) * np.hypot(pts[:, 0], pts[:, 1]) + 1e-12), -1, 1)))
        nerr.append(np.sqrt(np.mean(ang ** 2)))

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))
    ax = axes[0]
    ax.loglog(hs, rms, "o-", color=BLUE, ms=3.4, lw=1.5)
    ax.loglog(hs, 0.12 * hs ** 2, color=GREY, ls=":", lw=1.1, label=r"$O(h^2)$")
    ax.set_xlabel("体素边长 h")
    ax.set_ylabel("插值值的均方根误差")
    ax.set_xticks([0.02, 0.05, 0.1])
    ax.set_xticklabels(["0.02", "0.05", "0.1"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.legend(loc="lower right", fontsize=7.5)
    panel_label(ax, "(a)", x=-0.15, y=1.06)

    ax = axes[1]
    ax.loglog(hs, nerr, "s-", color=RED, ms=3.2, lw=1.5)
    ax.loglog(hs, 25.0 * hs, color=GREY, ls=":", lw=1.1, label=r"$O(h)$")
    ax.set_xlabel("体素边长 h")
    ax.set_ylabel("法线夹角的均方根（度）")
    ax.set_xticks([0.02, 0.05, 0.1])
    ax.set_xticklabels(["0.02", "0.05", "0.1"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.legend(loc="lower right", fontsize=7.5)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig14-3-resample.png")


if __name__ == "__main__":
    fig14_1()
    fig14_2()
    fig14_3()
