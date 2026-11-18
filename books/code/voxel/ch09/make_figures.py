import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

rng = np.random.default_rng(9)


# ---------------------------------------------------------------- 图 9-1
def first_hit_offset(d, R, h, conservative):
    t = 1.6 * R
    step = 0.04 * h
    while t > 0.2 * R:
        p = d * t
        c = (np.floor(p / h) + 0.5) * h
        if conservative:
            occ = np.linalg.norm(c) - R < 0.5 * np.sqrt(3) * h
        else:
            occ = np.linalg.norm(c) < R
        if occ:
            return t - R
        t -= step
    return np.nan


def fig9_1():
    R = 1.0
    N = 400
    d = rng.normal(size=(N, 3))
    d /= np.linalg.norm(d, axis=1)[:, None]
    ratios = np.array([8, 12, 16, 24, 32, 48, 64, 96])
    m_cons, m_cent = [], []
    for r in ratios:
        h = R / r
        a = np.array([first_hit_offset(x, R, h, True) for x in d])
        b = np.array([first_hit_offset(x, R, h, False) for x in d])
        m_cons.append(np.nanmean(a) / h)
        m_cent.append(np.nanmean(b) / h)

    fig, ax = plt.subplots(figsize=(6.1, 3.4))
    ax.plot(ratios, m_cons, color=ACCENT, marker="o", ms=3, label="保守体素化")
    ax.plot(ratios, m_cent, color=BLUE, marker="s", ms=3, label="格心采样")
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xlabel("球半径 / 体素边长")
    ax.set_ylabel("首交位置相对球面的偏移（体素边长）")
    ax.set_ylim(-0.4, 1.1)
    ax.legend(loc="center left", fontsize=7.8)
    fig.tight_layout()
    save(fig, "fig9-1-offset.png")


# ---------------------------------------------------------------- 图 9-2
def fig9_2():
    k = np.arange(0, 41)
    rho = 0.8
    fig, ax = plt.subplots(figsize=(6.1, 3.4))
    for s, col, ls in ((1.00, BLUE, "-"), (1.05, RED, "--"), (0.95, GOLD, "-.")):
        ax.semilogy(k, (s * rho) ** k / rho ** k, color=col, ls=ls,
                    label=f"权重和 = {s:.2f}")
    ax.axhline(1.0, color=GREY, ls=":", lw=1.0)
    ax.set_xlabel("弹射次数")
    ax.set_ylabel("总能量 / 精确值")
    ax.set_ylim(0.05, 20)
    ax.legend(loc="upper left", fontsize=7.8)
    note(ax, "反照率 0.8，白炉应为 $0.8^k$", 0.45, 0.06)
    fig.tight_layout()
    save(fig, "fig9-2-furnace.png")


# ---------------------------------------------------------------- 图 9-3
def fig9_3():
    N = np.logspace(0.5, 4.5, 120).astype(int)
    # 一维积分：f(x) = 1 (x<0.5) 否则 0.2，真值 0.6
    p_edge = 0.5
    true = 0.5 * 1.0 + 0.5 * 0.2
    samples = rng.random((4000, N[-1]))
    ys = np.where(samples < p_edge, 1.0, 0.2)
    cs = np.cumsum(ys, axis=1)
    mc = np.array([np.sqrt(np.mean((cs[:, n - 1] / n - true) ** 2)) for n in N])

    bias = 0.05          # 宽度为 0.1 的盒式过滤带来的偏差
    floor = np.full_like(N, bias, dtype=float)
    total = np.sqrt(mc ** 2 + bias ** 2)

    fig, ax = plt.subplots(figsize=(6.1, 3.4))
    ax.loglog(N, mc, color=BLUE, label="纯蒙特卡洛（无偏）")
    ax.loglog(N, floor, color=RED, ls="--", label="体素过滤（有偏，无方差）")
    ax.loglog(N, total, color=TEAL, ls="-.", label="两者结合")
    ax.set_xlabel("样本数")
    ax.set_ylabel("相对真值的均方根误差")
    ax.set_ylim(1e-3, 1.0)
    ax.legend(loc="lower left", fontsize=7.6)
    fig.tight_layout()
    save(fig, "fig9-3-bias-variance.png")


if __name__ == "__main__":
    fig9_1()
    fig9_2()
    fig9_3()
