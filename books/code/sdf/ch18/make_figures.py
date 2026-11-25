import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.ticker import NullFormatter
import numpy as np

R = 0.80


def target(P):
    return np.linalg.norm(P, axis=-1) - R


def train_net(H, iters=1200, seed=0):
    rng = np.random.default_rng(seed)
    W1 = rng.normal(0, 1 / np.sqrt(2), (2, H)); b1 = np.zeros(H)
    W2 = rng.normal(0, 1 / np.sqrt(H), (H, H)); b2 = np.zeros(H)
    W3 = rng.normal(0, 1 / np.sqrt(H), (H, 1)); b3 = np.zeros(1)
    ps = [W1, b1, W2, b2, W3, b3]
    ms = [np.zeros_like(p) for p in ps]
    vs = [np.zeros_like(p) for p in ps]
    lr, be1, be2 = 3e-3, 0.9, 0.999
    for it in range(iters):
        P = rng.uniform(-1.6, 1.6, (512, 2))
        y = target(P)
        z1 = np.tanh(P @ W1 + b1)
        z2 = np.tanh(z1 @ W2 + b2)
        pred = (z2 @ W3 + b3)[:, 0]
        d = pred - y
        g = {}
        g["W3"] = z2.T @ d[:, None] / len(P) * 2
        g["b3"] = np.array([d.sum() / len(P) * 2])
        dz2 = ((d[:, None] * 2 / len(P)) @ W3.T) * (1 - z2 ** 2)
        g["W2"] = z1.T @ dz2
        g["b2"] = dz2.sum(0)
        dz1 = (dz2 @ W2.T) * (1 - z1 ** 2)
        g["W1"] = P.T @ dz1
        g["b1"] = dz1.sum(0)
        gl = [g["W1"], g["b1"], g["W2"], g["b2"], g["W3"], g["b3"]]
        for i, (p, gg) in enumerate(zip(ps, gl)):
            ms[i] = be1 * ms[i] + (1 - be1) * gg
            vs[i] = be2 * vs[i] + (1 - be2) * gg ** 2
            mh = ms[i] / (1 - be1 ** (it + 1))
            vh = vs[i] / (1 - be2 ** (it + 1))
            ps[i] -= lr * mh / (np.sqrt(vh) + 1e-8)
    # 评估
    P = rng.uniform(-1.1, 1.1, (20000, 2))
    y = target(P)
    z1 = np.tanh(P @ W1 + b1)
    z2 = np.tanh(z1 @ W2 + b2)
    pred = (z2 @ W3 + b3)[:, 0]
    rmse = float(np.sqrt(np.mean((pred - y) ** 2)))
    nparam = 2 * H + H * H + H + 1
    return rmse, nparam


HS = [8, 16, 32, 64]
NET = [train_net(H, seed=5) for H in HS]

A = 10.0       # 表面积，平方米


def grid_curve(hs):
    mem = 6 * A / hs ** 2 * 4
    err = hs ** 2 / (8 * 1.0)
    return mem, err


def fig18_1():
    hs = np.logspace(np.log10(0.2), np.log10(0.002), 80)
    mem, err = grid_curve(hs)
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    ax.loglog(mem / 1e6, err, color=BLUE, lw=1.9, label="网格 / 窄带")
    ax.loglog(mem / 1e6 * 2.7, err, color=PURPLE, lw=1.5, ls="--", label="八叉树")
    nm = [n * 4 / 1e6 for _, n in NET]
    ne = [r for r, _ in NET]
    ax.loglog(nm, ne, "o-", color=ACCENT, ms=5, lw=1.5, label="神经场（实测）")
    for h, r, n in zip(HS, ne, nm):
        ax.annotate(f"H={h}", (n, r), textcoords="offset points", xytext=(-16, 8),
                    fontsize=7, color=ACCENT)
    ax.plot([1e-6], [1e-8], "*", color=TEAL, ms=12)
    ax.annotate("解析式", (1e-6, 1e-8), textcoords="offset points", xytext=(8, 4),
                fontsize=8, color=TEAL)
    ax.set_xlabel("内存（MB）")
    ax.set_ylabel("距离的均方根误差")
    ax.set_ylim(1e-9, 1.0)
    ax.legend(loc="upper right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig18-1-accuracy-memory.png")


def fig18_2():
    hs = np.logspace(np.log10(0.2), np.log10(0.002), 80)
    mem, err = grid_curve(hs)
    t_grid = np.full_like(hs, 8 * 30.0)   # 8 次读取 × 每次 30 周期
    t_net = np.array([2 * n for _, n in NET], dtype=float) + 60
    ne = np.array([r for r, _ in NET])

    fig, ax = plt.subplots(figsize=(6.3, 3.2))
    ax.loglog(t_grid, err, color=BLUE, lw=1.9, label="网格三线性")
    ax.loglog(t_net, ne, "o-", color=ACCENT, ms=5, lw=1.5, label="神经场（实测误差）")
    ax.loglog([30.0], [1e-8], "*", color=TEAL, ms=12)
    ax.annotate("解析式", (30.0, 1e-8), textcoords="offset points", xytext=(8, 2),
                fontsize=8, color=TEAL)
    ax.set_xlabel("单次查询的估算周期数")
    ax.set_ylabel("距离的均方根误差")
    ax.set_ylim(1e-9, 1.0)
    ax.legend(loc="lower left", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig18-2-accuracy-time.png")


def fig18_3():
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    ax.loglog(HS, [r for r, _ in NET], "o-", color=ACCENT, ms=5, lw=1.7,
              label="实测均方根误差")
    ax.set_xlabel("隐层单元数 H")
    ax.set_ylabel("距离的均方根误差")
    ax.set_xticks(HS)
    ax.set_xticklabels([str(h) for h in HS])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.legend(loc="upper right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig18-3-capacity.png")


if __name__ == "__main__":
    fig18_1()
    fig18_2()
    fig18_3()
