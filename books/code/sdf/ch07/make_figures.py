import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np


def sd_circle(p, c, r):
    return np.linalg.norm(p - c, axis=-1) - r


def sd_box3(q, b):
    w = np.abs(q) - b
    out = np.linalg.norm(np.maximum(w, 0.0), axis=-1)
    ins = np.minimum(np.max(w, axis=-1), 0.0) if False else np.minimum(w.max(-1), 0.0)
    return out + ins


# ---------------------------------------------------------------- 图 7-1
def fig7_1():
    s = 0.55
    r = 0.80
    xx = np.linspace(-2.2, 2.2, 900)
    f = xx / s - r
    corr = f * s
    tr = xx - r * s

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.1))
    ax = axes[0]
    ax.plot(xx, tr, color=INK, lw=2.0, label="真实距离（沿 x 轴）")
    ax.plot(xx, f, color=RED, lw=1.5, ls="--", label="未修正")
    ax.plot(xx, corr, color=BLUE, lw=1.5, label=r"乘 $s_{\min}=0.55$")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel("沿 x 轴的位置")
    ax.set_ylabel("距离值")
    ax.set_ylim(-1.0, 1.0)
    ax.legend(loc="upper left", fontsize=7.5)
    panel_label(ax, "(a)", x=-0.15, y=1.06)

    ax = axes[1]
    ss = np.logspace(np.log10(0.25), np.log10(3.0), 60)
    X, Y = np.meshgrid(np.linspace(-2.2, 2.2, 240), np.linspace(-1.2, 1.2, 160))
    gmax, gcorr = [], []
    for sv in ss:
        fld = np.sqrt((X / sv) ** 2 + Y ** 2) - r
        gx = np.gradient(fld, X[0, 1] - X[0, 0], axis=1)
        gy = np.gradient(fld, Y[1, 0] - Y[0, 0], axis=0)
        g = np.hypot(gx, gy)
        band = np.abs(fld) < 0.4
        gmax.append(g[band].max())
        gcorr.append(min(sv, 1.0) * g[band].max())
    ax.loglog(ss, gmax, color=RED, lw=1.6, label="未修正：场梯度最大值")
    ax.loglog(ss, gcorr, color=BLUE, lw=1.6, label=r"乘 $s_{\min}$ 之后")
    ax.loglog(ss, 1.0 / ss, color=GREY, ls=":", lw=1.1, label=r"$1/s$")
    ax.axhline(1.0, color=GREY, ls="-.", lw=1.1, label="1（安全边界）")
    ax.set_xlabel("x 方向缩放比 s")
    ax.set_ylabel(r"$\Vert\nabla f\Vert$ 最大值")
    ax.set_xticks([0.25, 0.5, 1.0, 2.0, 3.0])
    ax.set_xticklabels(["0.25", "0.5", "1", "2", "3"])
    ax.legend(loc="lower left", fontsize=7.0)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig7-1-scale.png")


# ---------------------------------------------------------------- 图 7-2
def fig7_2():
    n = 460
    xs = np.linspace(-3.0, 3.0, n)
    ys = np.linspace(-2.2, 2.2, n)
    X, Y = np.meshgrid(xs, ys)
    P = np.stack([X, Y], -1)

    s = np.array([1.2, 1.2])
    q = (P + 0.5 * s) % s - 0.5 * s
    f = sd_circle(q, np.zeros(2), 0.34)

    brute = np.full(X.shape, 1e9)
    for i in range(-3, 4):
        for j in range(-2, 3):
            c = np.array([i * s[0], j * s[1]])
            brute = np.minimum(brute, sd_circle(P - c, np.zeros(2), 0.34))

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))
    ax = axes[0]
    ax.pcolormesh(X, Y, np.clip(f, -0.3, 0.5), cmap="RdBu_r", shading="auto",
                  vmin=-0.3, vmax=0.5)
    ax.contour(X, Y, f, levels=[0.0], colors="black", linewidths=1.5)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.text(0.03, 0.96, "重复（mod）", transform=ax.transAxes, va="top", fontsize=8.4,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.82))
    panel_label(ax, "(a)", x=-0.16, y=1.06)

    ax = axes[1]
    xx = np.linspace(-3.0, 3.0, 900)
    P1 = np.stack([xx, np.zeros_like(xx)], -1)
    q1 = (P1 + 0.5 * s) % s - 0.5 * s
    f1 = sd_circle(q1, np.zeros(2), 0.34)
    b1 = np.full(xx.shape, 1e9)
    for i in range(-3, 4):
        b1 = np.minimum(b1, sd_circle(P1 - np.array([i * s[0], 0.0]), np.zeros(2), 0.34))
    ax.plot(xx, b1, color=INK, lw=2.0, label="对 7 个副本取最小")
    ax.plot(xx, f1, color=ACCENT, lw=1.3, ls="--", label="mod 形式")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel("沿 y = 0 的位置 x")
    ax.set_ylabel("距离值")
    ax.set_ylim(-0.45, 0.75)
    ax.legend(loc="upper center", fontsize=7.5)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig7-2-repeat.png")


# ---------------------------------------------------------------- 图 7-3
BQ = np.array([0.55, 0.26, 0.26])


def twisted(X, Y, om, z=0.0):
    th = om * X
    c, s = np.cos(th), np.sin(th)
    qy = c * Y - s * z
    qz = s * Y + c * z
    return sd_box3(np.stack([X, qy, qz], -1), BQ)


def fig7_3():
    n = 420
    xs = np.linspace(-1.5, 1.5, n)
    ys = np.linspace(-1.5, 1.5, n)
    X, Y = np.meshgrid(xs, ys)
    h = xs[1] - xs[0]

    om = 1.6
    f = twisted(X, Y, om)
    gx = (twisted(X + h, Y, om) - twisted(X - h, Y, om)) / (2 * h)
    gy = (twisted(X, Y + h, om) - twisted(X, Y - h, om)) / (2 * h)
    g = np.hypot(gx, gy)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))
    ax = axes[0]
    im = ax.pcolormesh(X, Y, np.clip(g, 0.9, 2.4), cmap="magma", shading="auto",
                       vmin=0.9, vmax=2.4)
    ax.contour(X, Y, f, levels=[0.0], colors="cyan", linewidths=1.4)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label(r"$\Vert\nabla f\Vert$", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    panel_label(ax, "(a)", x=-0.16, y=1.06)

    ax = axes[1]
    oms = np.linspace(0.0, 1.6, 33)
    gmax = []
    for o in oms:
        fg = twisted(X, Y, o)
        gxx = (twisted(X + 3 * h, Y, o) - twisted(X - 3 * h, Y, o)) / (6 * h)
        gyy = (twisted(X, Y + 3 * h, o) - twisted(X, Y - 3 * h, o)) / (6 * h)
        gg = np.hypot(gxx, gyy)
        gmax.append(gg[np.abs(fg) < 0.5].max())
    ax.plot(oms, gmax, color=RED, lw=1.8, marker="o", ms=3,
            label="表面附近梯度长度最大值")
    od = np.linspace(0.001, 1.6, 200)
    ax.plot(od, np.sqrt(1.0 + (od * 0.26) ** 2), color=GREY, ls=":", lw=1.2,
            label=r"$\sqrt{1+(\omega r)^2}$，$r=0.26$")
    ax.axhline(1.0, color=GREY, ls="-.", lw=1.0)
    ax.axvspan(1.5, 1.7, color=GREY, alpha=0.12)
    ax.text(1.45, 1.28, "截面开始互相穿插", fontsize=7.5, color="#3c4654",
            ha="right", va="top")
    ax.set_xlim(0, 1.65)
    ax.set_ylim(0.95, 1.3)
    ax.set_xlabel(r"扭转率 $\omega$")
    ax.set_ylabel(r"$\Vert\nabla f\Vert$ 最大值")
    ax.legend(loc="upper left", fontsize=7.5)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig7-3-twist.png")


if __name__ == "__main__":
    fig7_1()
    fig7_2()
    fig7_3()
