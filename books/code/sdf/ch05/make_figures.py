import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np


def sd_circle(p, c, r):
    return np.linalg.norm(p - c, axis=-1) - r


def sd_box(p, c, b):
    q = np.abs(p - c) - b
    out = np.linalg.norm(np.maximum(q, 0.0), axis=-1)
    ins = np.minimum(np.maximum(q[..., 0], q[..., 1]), 0.0)
    return out + ins


CA, RA = np.array([-0.25, 0.0]), 0.90
CB, BHB = np.array([0.72, 0.0]), np.array([0.62, 0.50])


def grid(x0, x1, y0, y1, n=420):
    xs = np.linspace(x0, x1, n)
    ys = np.linspace(y0, y1, n)
    X, Y = np.meshgrid(xs, ys)
    return X, Y, np.stack([X, Y], -1)


# ---------------------------------------------------------------- 图 5-1
def fig5_1():
    X, Y, P = grid(-1.7, 1.7, -1.35, 1.35, 400)
    a = sd_circle(P, CA, RA)
    b = sd_box(P, CB, BHB)

    fig, axes = plt.subplots(1, 3, figsize=(7.8, 2.9))
    for ax, (d, name) in zip(axes, [(np.minimum(a, b), "并集  min(a, b)"),
                                    (np.maximum(a, b), "交集  max(a, b)"),
                                    (np.maximum(a, -b), "差集  max(a, −b)")]):
        ax.pcolormesh(X, Y, np.clip(d, -0.45, 0.45), cmap="RdBu_r", shading="auto",
                      vmin=-0.45, vmax=0.45)
        ax.contour(X, Y, d, levels=[0.0], colors="black", linewidths=1.7)
        ax.contour(X, Y, d, levels=[-0.25, 0.12, 0.25], colors="#3d3d3d",
                   linewidths=0.55)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.03, 0.96, name, transform=ax.transAxes, va="top", fontsize=8.4,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.82))
    axes[1].set_xlabel("x")
    fig.tight_layout()
    save(fig, "fig5-1-booleans.png")


# ---------------------------------------------------------------- 图 5-2
def true_diff_distance(P):
    th = np.linspace(0, 2 * np.pi, 2400, endpoint=False)
    circ = np.stack([CA[0] + RA * np.cos(th), CA[1] + RA * np.sin(th)], -1)
    keep_c = sd_box(circ, CB, BHB) > 0

    s = np.linspace(-BHB[0], BHB[0], 900)
    sy = np.linspace(-BHB[1], BHB[1], 700)
    boxp = np.concatenate([
        np.stack([CB[0] + s, np.full_like(s, CB[1] - BHB[1])], -1),
        np.stack([CB[0] + s, np.full_like(s, CB[1] + BHB[1])], -1),
        np.stack([np.full_like(sy, CB[0] - BHB[0]), CB[1] + sy], -1),
        np.stack([np.full_like(sy, CB[0] + BHB[0]), CB[1] + sy], -1)])
    keep_b = sd_circle(boxp, CA, RA) < 0

    pts = np.concatenate([circ[keep_c], boxp[keep_b]])
    flat = P.reshape(-1, 2)
    dmin = np.full(flat.shape[0], 1e9)
    for k in range(0, pts.shape[0], 200):
        blk = pts[k:k + 200]
        dmin = np.minimum(dmin, np.linalg.norm(flat[:, None, :] - blk[None], axis=-1).min(1))
    inside = (sd_circle(P, CA, RA) < 0) & (sd_box(P, CB, BHB) > 0)
    sgn = np.where(inside.reshape(-1), -1.0, 1.0)
    return (sgn * dmin).reshape(P.shape[:-1])


def fig5_2():
    X, Y, P = grid(-1.6, 1.6, -1.25, 1.25, 340)
    a = sd_circle(P, CA, RA)
    b = sd_box(P, CB, BHB)
    f = np.maximum(a, -b)
    tr = true_diff_distance(P)
    err = f - tr

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.9))
    ax = axes[0]
    im = ax.pcolormesh(X, Y, np.clip(err, -0.4, 0.4), cmap="PuOr_r", shading="auto",
                       vmin=-0.4, vmax=0.4)
    ax.contour(X, Y, f, levels=[0.0], colors="black", linewidths=1.3)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label("场值减真实距离", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    panel_label(ax, "(a)", x=-0.16, y=1.06)

    ax = axes[1]
    xx = np.linspace(-1.6, 1.6, 800)
    P1 = np.stack([xx, np.zeros_like(xx)], -1)
    f1 = np.maximum(sd_circle(P1, CA, RA), -sd_box(P1, CB, BHB))
    t1 = true_diff_distance(P1)
    ax.plot(xx, t1, color=INK, lw=1.7, label="真实距离")
    ax.plot(xx, f1, color=ACCENT, lw=1.6, ls="--", label=r"$\max(a,-b)$")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel("沿 y = 0 的位置 x")
    ax.set_ylabel("距离值")
    ax.set_ylim(-1.0, 1.1)
    ax.legend(loc="upper right", fontsize=7.5)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig5-2-difference.png")


# ---------------------------------------------------------------- 图 5-3
def fig5_3():
    X, Y, P = grid(-1.5, 1.5, -1.2, 1.2, 380)
    d = sd_circle(P, np.zeros(2), 0.85)
    t = 0.13
    shell = np.abs(d) - t

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.9))
    ax = axes[0]
    ax.pcolormesh(X, Y, np.clip(shell, -0.2, 0.2), cmap="RdBu_r", shading="auto",
                  vmin=-0.2, vmax=0.2)
    ax.contour(X, Y, shell, levels=[0.0], colors="black", linewidths=1.6)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.text(0.03, 0.96, "壳体  |d| − 0.13", transform=ax.transAxes, va="top",
            fontsize=8.4,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.82))
    panel_label(ax, "(a)", x=-0.16, y=1.06)

    ax = axes[1]
    xx = np.linspace(-1.35, 1.35, 700)
    dd = np.abs(xx) - 0.85
    ax.plot(xx, dd, color=BLUE, lw=1.5, label=r"$d$")
    ax.plot(xx, np.abs(dd), color=TEAL, lw=1.5, ls="--", label=r"$|d|$")
    ax.plot(xx, np.abs(dd) - t, color=ACCENT, lw=1.7, label=r"$|d|-t$")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel("沿 y = 0 的位置 x")
    ax.set_ylabel("距离值")
    ax.set_ylim(-1.1, 0.8)
    ax.legend(loc="upper center", ncol=3, fontsize=7.5)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig5-3-shell.png")


if __name__ == "__main__":
    fig5_1()
    fig5_2()
    fig5_3()
