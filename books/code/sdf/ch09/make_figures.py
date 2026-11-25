import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

AA, BB = 1.0, 0.30
TH = np.linspace(0, 2 * np.pi, 4000, endpoint=False)
BOUND = np.stack([AA * np.cos(TH), BB * np.sin(TH)], -1)


def cheap(p):
    """|p/(a,b)| - 1，短轴方向把距离放大约 1/b 倍。"""
    return np.hypot(p[..., 0] / AA, p[..., 1] / BB) - 1.0


def true_d(P):
    flat = P.reshape(-1, 2)
    d = np.full(flat.shape[0], 1e9)
    for k in range(0, BOUND.shape[0], 500):
        blk = BOUND[k:k + 500]
        d = np.minimum(d, np.linalg.norm(flat[:, None, :] - blk[None], axis=-1).min(1))
    inside = (flat[:, 0] / AA) ** 2 + (flat[:, 1] / BB) ** 2 < 1.0
    return np.where(inside, -d, d).reshape(P.shape[:-1])


# ---------------------------------------------------------------- 图 9-1
def fig9_1():
    x0 = 0.82
    ys = np.linspace(-0.9, 0.9, 900)
    P = np.stack([np.full_like(ys, x0), ys], -1)
    f = cheap(P)
    tr = true_d(P)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))
    ax = axes[0]
    ax.plot(ys, tr, color=INK, lw=1.9, label="真实距离")
    ax.plot(ys, f, color=RED, lw=1.6, ls="--", label="椭球公式")
    ax.axhline(0.0, color=GREY, lw=0.8)
    ax.set_xlabel("沿 x = 0.82 的位置 y")
    ax.set_ylabel("距离值")
    ax.set_ylim(-0.75, 1.0)
    ax.set_xlim(-0.9, 0.9)
    ax.legend(loc="upper center", fontsize=7.5)
    panel_label(ax, "(a)", x=-0.15, y=1.06)

    ax = axes[1]
    ax.plot(ys, f, color=RED, lw=1.5, ls="--", label="椭球公式")
    ax.plot(ys, tr, color=INK, lw=1.1, label="真实距离")
    ax.axhline(0.0, color=GREY, lw=0.8)
    t, pts, crossed = -0.35, [-0.35], False
    for _ in range(6):
        v = cheap(np.array([x0, t]))
        if v < 1e-3:
            break
        t = t + v
        pts.append(t)
        if cheap(np.array([x0, t])) < 0:
            crossed = True
            break
    for i, py in enumerate(pts):
        pv = cheap(np.array([x0, py]))
        ax.plot([py], [pv], "o", ms=4.4, color=ACCENT)
        ax.annotate(str(i), (py, pv), textcoords="offset points", xytext=(3, 6),
                    fontsize=7.5, color=ACCENT)
    if crossed:
        ax.annotate("第二步落到表面另一侧", (pts[-1], cheap(np.array([x0, pts[-1]]))),
                    xytext=(-0.45, -0.28), fontsize=8, color=ACCENT,
                    arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.9))
    ax.set_xlim(-0.6, 0.35)
    ax.set_ylim(-0.4, 0.75)
    ax.set_xlabel("沿光线的位置 y")
    ax.set_ylabel("场值")
    ax.legend(loc="upper right", fontsize=7.3)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig9-1-overshoot.png")


# ---------------------------------------------------------------- 图 9-2
def march(o, u, c, tmax=3.0, eps=2e-3, maxit=400):
    t = 0.0
    for i in range(maxit):
        v = cheap(o + t * u)
        if v < eps:
            return t, True, i + 1
        if v < 0:
            return t, False, i + 1
        t += c * v
        if t > tmax:
            break
    return t, False, maxit


def fig9_2():
    xs = np.linspace(-0.95, 0.95, 61)
    cs = np.linspace(0.10, 1.10, 51)
    miss, steps = [], []
    for c in cs:
        nm, st = 0, []
        for xv in xs:
            t, hit, n = march(np.array([xv, -0.9]), np.array([0.0, 1.0]), c)
            if abs(xv) < AA and not hit:
                nm += 1
            if hit:
                st.append(n)
        miss.append(100.0 * nm / len(xs))
        steps.append(np.mean(st) if st else np.nan)

    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(cs, miss, color=RED, lw=1.9, label="漏检率")
    ax.set_xlabel("步长系数 c（步长 = c × 场值）")
    ax.set_ylabel("漏检率（%）", color=RED)
    ax.tick_params(axis="y", colors=RED)
    ax.set_ylim(-3, 105)
    ax.axvline(1.0 / (1.0 / BB), color=GREY, ls=":", lw=1.1)
    ax.text(0.34, 92, "理论上界 1/L = 0.30", fontsize=7.5, color="#3c4654")
    ax2 = ax.twinx()
    ax2.plot(cs, steps, color=BLUE, lw=1.8, ls="--", label="平均步数")
    ax2.set_ylabel("命中光线的平均步数", color=BLUE)
    ax2.set_ylim(0, 40)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(BLUE)
    ax2.tick_params(axis="y", colors=BLUE)
    l1, n1 = ax.get_legend_handles_labels()
    l2, n2 = ax2.get_legend_handles_labels()
    ax.legend(l1 + l2, n1 + n2, loc="center right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig9-2-miss-rate.png")


# ---------------------------------------------------------------- 图 9-3
def fig9_3():
    n = np.arange(0, 26)
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.semilogy(n, 0.5 * 0.5 ** n, color=BLUE, lw=1.7, marker="o", ms=3,
                label="二分回退，区间每次减半")
    ax.semilogy(n, 0.5 * np.exp(-0.35 * n), color=ACCENT, lw=1.7, ls="--",
                label="保守步进 c = 1/L，收敛近似线性")
    ax.set_xlabel("额外迭代次数")
    ax.set_ylabel("剩余区间长度")
    ax.set_ylim(1e-8, 1.0)
    ax.legend(loc="upper right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig9-3-bisection.png")


if __name__ == "__main__":
    fig9_1()
    fig9_2()
    fig9_3()
