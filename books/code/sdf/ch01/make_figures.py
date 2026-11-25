import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

# ---------------------------------------------------------------- 图 1-1
def fig1_1():
    """求交代价的模型估算，横轴是三角形数。"""
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    N = np.logspace(2, 8, 200)

    brute = 0.5 * N
    bvh = 2.0 * np.log2(N) + 8.0
    analytic = np.full_like(N, 0.35)
    # 网格距离场：三线性采样按 0.5 次三角形测试计，平均 48 步
    grid = np.full_like(N, 0.5 * 48)

    ax.loglog(N, brute, color=RED, label="暴力遍历")
    ax.loglog(N, bvh, color=BLUE, label="BVH")
    ax.loglog(N, analytic, color=TEAL, ls="--", label="解析 SDF")
    ax.loglog(N, grid, color=ACCENT, ls="-.", label="网格 SDF 步进")

    ax.set_xlabel("物体三角形数 N")
    ax.set_ylabel("单次求交代价（归一化）")
    ax.set_ylim(0.1, 1e8)
    ax.legend(loc="upper left", ncol=2)
    ax.annotate("BVH 与网格步进\n在千面量级交叉",
                xy=(2 ** 8, 24), xytext=(3e4, 3.0), fontsize=8,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
    fig.tight_layout()
    save(fig, "fig1-2-cost-model.png")


# ---------------------------------------------------------------- 图 1-2
def sd_circle(p, c, r):
    return np.linalg.norm(p - c, axis=-1) - r


def sd_box(p, c, b):
    q = np.abs(p - c) - b
    outside = np.linalg.norm(np.maximum(q, 0.0), axis=-1)
    inside = np.minimum(np.maximum(q[..., 0], q[..., 1]), 0.0)
    return outside + inside


def fig1_2():
    n = 420
    xs = np.linspace(-1.9, 1.9, n)
    ys = np.linspace(-1.5, 1.5, n)
    X, Y = np.meshgrid(xs, ys)
    P = np.stack([X, Y], axis=-1)
    d1 = sd_circle(P, np.array([-0.55, 0.0]), 0.80)
    d2 = sd_box(P, np.array([0.55, 0.05]), np.array([0.60, 0.45]))
    d = np.minimum(d1, d2)

    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    im = ax.pcolormesh(X, Y, np.clip(d, -0.6, 0.6), cmap="RdBu_r",
                       shading="auto", vmin=-0.6, vmax=0.6)
    cs = ax.contour(X, Y, d, levels=[-0.5, -0.35, -0.2, -0.08, 0.08, 0.2, 0.35, 0.55],
                    colors="#333333", linewidths=0.7)
    ax.contour(X, Y, d, levels=[0.0], colors="black", linewidths=2.0)
    ax.clabel(cs, fmt="%.2f", fontsize=7)
    ax.set_aspect("equal")
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    cb = fig.colorbar(im, ax=ax, fraction=0.036, pad=0.02)
    cb.set_label("距离值", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    fig.tight_layout()
    save(fig, "fig1-3-union-contour.png")


# ---------------------------------------------------------------- 图 1-3
def fig1_3():
    """沿一条偏移光线，距离函数给出的步长与落点。"""
    y0 = 0.35
    def d(x):
        return np.sqrt(x * x + y0 * y0) - 1.0

    xs = np.linspace(-3.2, 3.2, 600)
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    ax.plot(xs, d(xs), color=BLUE, lw=1.6, label=r"沿光线偏移 $y_0=0.35$ 的距离 $d(x)$")
    ax.axhline(0.0, color=INK, lw=0.9)

    pts = []
    x = -3.0
    for _ in range(4):
        v = d(x)
        pts.append((x, v))
        x = x + v
    pts.append((x, 0.0))
    for i, (px, pv) in enumerate(pts):
        ax.plot([px, px], [0, pv], color=ACCENT, lw=1.0, ls=":")
        ax.plot([px], [pv], "o", ms=4.2, color=ACCENT)
        ax.annotate(f"$x_{i}$", (px, pv), textcoords="offset points",
                    xytext=(0, 6), ha="center", fontsize=8, color=ACCENT)
    ax.plot([pts[-1][0]], [0.0], "o", ms=5.5, color=RED)
    ax.annotate("落点", (pts[-1][0], 0.0), textcoords="offset points",
                xytext=(4, -14), fontsize=8, color=RED)

    ax.set_xlabel("沿光线的位置 x")
    ax.set_ylabel("距离场值")
    ax.set_ylim(-0.35, 2.6)
    ax.legend(loc="upper center")
    fig.tight_layout()
    save(fig, "fig1-1-march-profile.png")


if __name__ == "__main__":
    fig1_1()
    fig1_2()
    fig1_3()
