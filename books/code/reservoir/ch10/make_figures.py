import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *

A, B, L = 0.9, 0.65, 1.5          # sigma(x) = A (1 + B sin(2 pi x / L))
SMAX = A * (1 + B)


def sigma(x):
    return A * (1 + B * np.sin(2 * np.pi * np.asarray(x) / L))


def tau(d):
    d = np.asarray(d, float)
    return A * (d + B * L / (2 * np.pi) * (1 - np.cos(2 * np.pi * d / L)))


def track(d, rng, n, mode="ratio"):
    """非均匀介质的追踪。mode='analog' 在真碰撞处终止并返回 0；
    mode='ratio' 继续前进，每次碰撞乘上 (1 - sigma/SMAX)。"""
    t = np.zeros(n)
    w = np.ones(n)
    alive = np.ones(n, bool)
    steps = np.zeros(n)
    while alive.any():
        step = -np.log(np.maximum(rng.random(n), 1e-300)) / SMAX
        t = np.where(alive, t + step, t)
        alive &= t < d
        s = sigma(t)
        coll = alive & (rng.random(n) < s / SMAX)
        if mode == "analog":
            w[coll] = 0.0
            alive &= ~coll
        else:
            w[alive] *= 1.0 - s[alive] / SMAX
        steps += alive
    return w, steps


def fig10_1():
    ds = np.array([0.15, 0.3, 0.6, 1.0, 1.6, 2.4, 3.2])
    rng = np.random.default_rng(0)
    n = 40000
    truth = np.exp(-tau(ds))
    sa, sr, ba, br = [], [], [], []
    for d in ds:
        a, _ = track(d, rng, n, "analog")
        r, _ = track(d, rng, n, "ratio")
        tr = float(np.exp(-tau(d)))
        sa.append(a.std() / tr)
        sr.append(r.std() / tr)
        ba.append(a.mean() / tr - 1)
        br.append(r.mean() / tr - 1)
        print(f"d={d:.2f} tau={tr and float(tau(d)):.2f} Tr={tr:.3f} "
              f"analog {a.mean():.3f} relstd {sa[-1]:.2f} bias {ba[-1]*100:+.1f}% | "
              f"ratio {r.mean():.3f} relstd {sr[-1]:.3f} bias {br[-1]*100:+.1f}%")

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3))
    ax = axes[0]
    ax.plot(ds, truth, "k-", lw=1.4, label="解析值")
    ax.plot(ds, truth * (1 + np.array(ba)), "s", ms=4.5, color=BLUE, label="模拟追踪")
    ax.plot(ds, truth * (1 + np.array(br)), "o", ms=4.5, color=ACCENT, label="权重式追踪")
    ax.set_xlabel("沿射线的距离")
    ax.set_ylabel("透射率")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title("估计值", fontsize=9)

    ax = axes[1]
    ax.semilogy(ds, sa, "s-", ms=4, color=BLUE, label="模拟追踪")
    ax.semilogy(ds, sr, "o-", ms=4, color=ACCENT, label="权重式追踪")
    ax.set_xlabel("沿射线的距离")
    ax.set_ylabel("相对标准差（对数）")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_title("同样的样本数", fontsize=9)
    fig.tight_layout()
    save(fig, "fig10-2-transmittance.png")


def fig10_2():
    dmax = 4.0
    rng = np.random.default_rng(1)
    n = 400000
    t = np.zeros(n)
    alive = np.ones(n, bool)
    steps = np.zeros(n)
    tcoll = np.full(n, np.inf)
    while alive.any():
        step = -np.log(np.maximum(rng.random(n), 1e-300)) / SMAX
        t = np.where(alive, t + step, t)
        alive &= t < dmax
        hit = alive & (rng.random(n) < sigma(t) / SMAX)
        tcoll[hit] = t[hit]
        alive &= ~hit
        steps += alive

    xs = np.linspace(0.001, dmax, 900)
    pdf = sigma(xs) * np.exp(-tau(xs))
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.hist(tcoll[np.isfinite(tcoll)], bins=90, range=(0, dmax), density=True,
            color=SKY, alpha=0.75, edgecolor="white", linewidth=0.3,
            label="自由飞行距离的直方图")
    ax.plot(xs, pdf / np.trapezoid(pdf, xs), color=ACCENT, lw=1.8,
            label="解析密度 $\\sigma_t e^{-\\tau}$")
    ax.set_xlabel("沿射线的距离")
    ax.set_ylabel("概率密度")
    ax.legend(loc="upper right", fontsize=8)
    print("平均步数", round(float(steps.mean()), 2),
          "穿透比例", round(float(np.mean(~np.isfinite(tcoll))), 3),
          "解析穿透", round(float(np.exp(-tau(dmax))), 3))
    save(fig, "fig10-1-freeflight.png")


def fig10_3():
    """把"便宜的距离采样"和"昂贵的光源可见性查询"分开：
    RIS 用 M 个便宜候选挑一个，只对选中的那一个做一次昂贵查询。"""
    rng = np.random.default_rng(2)
    dmax = 3.0
    L0 = lambda t: 0.3 + 2.5 * np.exp(-((np.asarray(t) - 1.45) / 0.35) ** 2)
    V = lambda t: ((np.asarray(t) < 0.55) | (np.asarray(t) > 0.95)).astype(float)

    xs = np.linspace(1e-4, dmax, 8000)
    tru = np.trapezoid(np.exp(-tau(xs)) * sigma(xs) * L0(xs) * V(xs), xs)

    Ms = [1, 2, 4, 8, 16, 32]
    n = 20000
    rel_plain, rel_ris, rel_strat = [], [], []
    for M in Ms:
        p = 1.0 / dmax
        # 普通单样本：1 次便宜求值 + 1 次昂贵查询
        u = rng.random(n) * dmax
        est_plain = np.exp(-tau(u)) * sigma(u) * L0(u) * V(u) / p
        rel_plain.append(est_plain.std() / tru)

        # 分层：M 个距离等分，只对选中的层做昂贵查询
        k = np.arange(M)[None, :]
        uu = (k + rng.random((n, M))) / M * dmax
        ph = np.exp(-tau(uu)) * sigma(uu) * L0(uu)
        w = ph * dmax
        W = w.sum(axis=1)
        cdf = np.cumsum(w, axis=1) / np.maximum(W[:, None], 1e-300)
        idx = np.minimum((rng.random((n, 1)) > cdf).sum(axis=1), M - 1)
        y = np.take_along_axis(uu, idx[:, None], 1)[:, 0]
        est_ris = (W / M) * V(y)
        rel_ris.append(est_ris.std() / tru)
        print(f"M={M} 普通 {rel_plain[-1]:.3f} RIS {rel_ris[-1]:.3f}")

    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.plot(Ms, rel_plain, "s-", ms=4, color=GREY, label="普通单样本（1 次查询）")
    ax.plot(Ms, rel_ris, "o-", ms=4, color=ACCENT,
            label="RIS：$M$ 个便宜候选 + 1 次查询")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("每帧每像素的便宜求值次数 $M$")
    ax.set_ylabel("相对标准差")
    ax.legend(loc="upper right", fontsize=8)
    save(fig, "fig10-3-volris.png")


fig10_1()
fig10_2()
fig10_3()
