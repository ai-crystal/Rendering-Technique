import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import pathlab as pl

A0 = -0.30
SIGMA = 0.02          # 结果放大用的常数，只为让数字好读


def fig9_0():
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    ax.plot([-0.9, 1.0], [0, 0], color=INK, lw=2.2)
    ax.plot([1.0, 1.0], [0, 2.0], color=INK, lw=2.2)
    ax.add_patch(plt.Rectangle((0.38, 0), 0.20, 0.72, color=GREY, alpha=0.55, lw=0))
    ax.plot([0.30], [2.30], "*", ms=13, color=GOLD)
    ax.text(0.33, 2.34, "光源", fontsize=8, color=INK)
    for a in (-0.5, -0.3, -0.1):
        ax.plot([a], [0], "o", ms=4.5, color=BLUE)
    ax.text(-0.72, -0.16, "主顶点 $A$", fontsize=8, color=BLUE)
    zb = 1.52
    ax.plot([1.0], [zb], "o", ms=4.5, color=RED)
    ax.text(0.55, zb + 0.04, "二次顶点 $B$", fontsize=8, color=RED)
    ax.annotate("", xy=(1.0, zb), xytext=(-0.3, 0),
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2))
    ax.plot([1.0, 0.30], [zb, 2.30], color=GOLD, lw=1.0, ls="--")
    ax.annotate("遮挡体", xy=(0.55, 0.55), xytext=(0.10, 0.95), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))
    ax.set_xlim(-1.0, 1.35)
    ax.set_ylim(-0.28, 2.6)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "fig9-1-scene.png")


def _call():
    pass


def fig9_1():
    deltas = [0.02, 0.05, 0.1, 0.15, 0.2, 0.3]
    res = {"按 A 的密度归一": [], "带来源密度": [], "方向复用": []}
    err = {k: [] for k in res}
    rng = np.random.default_rng(2)
    T = pl.truth(A0)
    for d in deltas:
        As = A0 - d
        vals = {k: [] for k in res}
        for s in range(6):
            n = 200000
            th = pl.sample_theta(n, rng)
            z = pl.theta_to_z(th, As)
            vals["按 A 的密度归一"].append(pl.estimator(A0, z, "reconnect").mean())
            vals["带来源密度"].append(pl.estimator(A0, z, "nojac", ax_src=As).mean())
            vals["方向复用"].append(
                pl.estimator(A0, pl.theta_to_z(np.arctan(z / (pl.WALL_X - As)), A0),
                             "reconnect").mean())
        for k in res:
            res[k].append(np.mean(vals[k]) / T - 1)
            err[k].append(np.std(vals[k]) / T)
        print("delta", d, {k: round(res[k][-1] * 100, 1) for k in res})

    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    for k, col, mk in [("按 A 的密度归一", RED, "o"),
                       ("带来源密度", ACCENT, "s"),
                       ("方向复用", BLUE, "^")]:
        ax.errorbar(np.array(deltas) * 100, np.array(res[k]) * 100,
                    yerr=np.array(err[k]) * 100, fmt=mk + "-", ms=4,
                    color=col, ecolor=LIGHT, elinewidth=0.8, capsize=2, label=k)
    ax.axhline(0, color=INK, lw=0.9, ls=":")
    ax.set_xlabel("邻居与自己的距离（占墙高的百分比）")
    ax.set_ylabel("相对偏差（%）")
    ax.legend(loc="upper left", fontsize=8)
    save(fig, "fig9-2-reconnect.png")


def fig9_2():
    deltas = [0.02, 0.05, 0.1, 0.15, 0.2, 0.3]
    valid, drop_bias = [], []
    rng = np.random.default_rng(3)
    T = pl.truth(A0)
    for d in deltas:
        As = A0 - d
        th = pl.sample_theta(300000, rng)
        z = pl.theta_to_z(th, As)
        v = pl.valid(A0, z)
        valid.append(v.mean())
        est = pl.estimator(A0, z, "nojac", ax_src=As)
        drop_bias.append(np.where(v, est / max(v.mean(), 1e-9), 0.0).mean() / T - 1)
        print("delta", d, "valid", round(valid[-1], 3), "drop bias", round(drop_bias[-1] * 100, 1))

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.2))
    ax = axes[0]
    ax.plot(np.array(deltas) * 100, np.array(valid) * 100, "o-", color=TEAL)
    ax.set_xlabel("邻居与自己的距离（占墙高的百分比）")
    ax.set_ylabel("重连接后线段仍可见的比例（%）")
    ax.set_ylim(0, 100)
    ax.set_title("有效性", fontsize=9)
    ax = axes[1]
    ax.bar(np.array(deltas) * 100, np.array(drop_bias) * 100, width=2.6, color=RED, alpha=0.85)
    for x, v in zip(np.array(deltas) * 100, np.array(drop_bias) * 100):
        ax.text(x, v + 1.2, f"{v:.0f}", ha="center", fontsize=7)
    ax.set_xlabel("邻居与自己的距离（占墙高的百分比）")
    ax.set_ylabel("丢弃被挡样本后的相对偏差（%）")
    ax.set_ylim(0, 70)
    ax.set_title("丢弃的代价", fontsize=9)
    fig.tight_layout()
    save(fig, "fig9-3-validity.png")


def gi_sim(radius=1, M0=4, cap=20, P=12, seeds=24, frames=6, reuse=True):
    """一维像素阵列上的 ReSTIR GI：目标函数是去掉可见性的贡献。"""
    grid = np.linspace(-0.50, -0.12, P)
    tru = np.array([float(pl.truth(a)) for a in grid])
    est = []
    for s in range(seeds):
        rng = np.random.default_rng(100 + s)
        res = None
        out = np.zeros((frames, P))
        for t in range(frames):
            th = pl.sample_theta((P, M0), rng)
            z = pl.theta_to_z(th, grid[:, None])
            ph = pl.target(grid[:, None], z)              # 目标函数：去掉可见性
            w = ph / np.maximum(pl.p_z(z, grid[:, None]), 1e-300)
            W = w.sum(axis=1)
            cdf = np.cumsum(w, axis=1) / np.maximum(W[:, None], 1e-300)
            sel = np.minimum((rng.random((P, 1)) > cdf).sum(axis=1), M0 - 1)
            y = np.take_along_axis(z, sel[:, None], 1)[:, 0]
            phy = pl.target(grid, y)
            cur = dict(y=y, W=W, M=np.full(P, float(M0)), ph=phy)
            if reuse and res is not None:
                for sh in (1, -1):
                    yj = res["y"][np.roll(np.arange(P), sh)]
                    Wj = res["W"][np.roll(np.arange(P), sh)]
                    phj_src = res["ph"][np.roll(np.arange(P), sh)]
                    phj_cur = pl.target(grid, yj)
                    Wb = Wj * phj_cur / np.maximum(phj_src, 1e-300)
                    tot = cur["W"] + Wb
                    pick = rng.random(P) < Wb / np.maximum(tot, 1e-300)
                    cur = dict(y=np.where(pick, yj, cur["y"]), W=tot,
                               M=cur["M"] + res["M"][np.roll(np.arange(P), sh)],
                               ph=np.where(pick, phj_cur, cur["ph"]))
            if reuse and res is not None and radius > 1:
                pass
            capv = np.minimum(1.0, cap / cur["M"])
            cur["W"] = cur["W"] * capv
            cur["M"] = np.minimum(cur["M"], cap)
            est_t = pl.integrand(grid, cur["y"]) / np.maximum(cur["ph"], 1e-300) * cur["W"] / cur["M"]
            out[t] = est_t
            res = cur
        est.append(out)
    e = np.array(est)
    tt = np.broadcast_to(tru, e.shape[1:])
    err = (e[:, 2:] - tt[2:]) / tt[2:]
    return float(err.mean()), float(err.std())


def fig9_3():
    Ms = [1, 2, 4, 8]
    local = []
    reuse = []
    for M in Ms:
        b1, s1 = gi_sim(M0=M, reuse=False, seeds=16)
        b2, s2 = gi_sim(M0=M, reuse=True, seeds=16)
        local.append(s1)
        reuse.append(s2)
        print("M0", M, "不复用", round(s1, 3), "复用", round(s2, 3),
              "bias%", round(b1 * 100, 1), round(b2 * 100, 1))
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.plot(Ms, local, "s-", ms=4, color=BLUE, label="只用本地候选")
    ax.plot(Ms, reuse, "o-", ms=4, color=ACCENT, label="加左右邻居复用")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("每帧每像素的候选数 $M_0$")
    ax.set_ylabel("相对标准差")
    ax.legend(loc="upper right", fontsize=8)
    save(fig, "fig9-4-gi.png")


def fig9_0():
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    ax.plot([-0.9, 1.0], [0, 0], color=INK, lw=2.2)
    ax.plot([1.0, 1.0], [0, 2.0], color=INK, lw=2.2)
    ax.add_patch(plt.Rectangle((0.38, 0), 0.20, 0.72, color=GREY, alpha=0.55, lw=0))
    ax.plot([0.30], [2.30], "*", ms=13, color=GOLD)
    ax.text(0.33, 2.34, "光源", fontsize=8, color=INK)
    for a in (-0.5, -0.3, -0.1):
        ax.plot([a], [0], "o", ms=4.5, color=BLUE)
    ax.text(-0.72, -0.16, "主顶点 $A$", fontsize=8, color=BLUE)
    zb = 1.52
    ax.plot([1.0], [zb], "o", ms=4.5, color=RED)
    ax.text(0.55, zb + 0.04, "二次顶点 $B$", fontsize=8, color=RED)
    ax.annotate("", xy=(1.0, zb), xytext=(-0.3, 0),
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2))
    ax.plot([1.0, 0.30], [zb, 2.30], color=GOLD, lw=1.0, ls="--")
    ax.annotate("遮挡体", xy=(0.55, 0.55), xytext=(0.10, 0.95), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))
    ax.set_xlim(-1.0, 1.35)
    ax.set_ylim(-0.28, 2.6)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "fig9-1-scene.png")


fig9_0()
fig9_1()
fig9_2()
fig9_3()
