import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import ris

N = 64
B_SCENE = ris.make_scene(N, 1, 5, "zipf")[0]
V_SCENE = ris.visibility(N, 1, 5, p_lit=0.7, soft=False)[0]
F_SCENE = B_SCENE * V_SCENE
TRUTH = F_SCENE.sum()


def ris_batch(M, T, rng, phat=None, drop_zero=False, p=None):
    """T 次独立的 RIS 估计，返回数组 (T,)。p 缺省为均匀。"""
    phat = B_SCENE if phat is None else phat
    if p is None:
        p = np.full(N, 1.0 / N)
    idx = rng.choice(N, size=(T, M), p=p)
    w = phat[idx] / p[idx]
    if drop_zero:
        mm = np.maximum((w > 0).sum(axis=1), 1)
    else:
        mm = np.full(T, M)
    wsum = w.sum(axis=1)
    cdf = np.cumsum(w, axis=1) / np.maximum(wsum, 1e-300)[:, None]
    u = rng.random(T)
    sel = np.minimum((u[:, None] > cdf).sum(axis=1), M - 1)
    y = np.take_along_axis(idx, sel[:, None], axis=1)[:, 0]
    out = F_SCENE[y] / p[y] * (wsum / mm) / np.maximum(phat[y] / p[y], 1e-300)
    return np.where(wsum > 0, out, 0.0)


def fig2_1():
    """重采样把候选分布变成目标分布：选中样本的分布随 M 变化。"""
    rng = np.random.default_rng(11)
    order = np.argsort(-B_SCENE)
    T = 400000
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    target = B_SCENE / B_SCENE.sum()
    ax.plot(np.arange(N), target[order], color=INK, lw=1.6, label="目标分布")
    for M, col, mk in [(1, SKY, "o"), (2, TEAL, "s"), (8, ACCENT, "D"), (64, PURPLE, "^")]:
        idx = rng.integers(0, N, size=(T, M))
        w = B_SCENE[idx]
        cdf = np.cumsum(w, axis=1) / w.sum(axis=1, keepdims=True)
        u = rng.random(T)
        sel = np.minimum((u[:, None] > cdf).sum(axis=1), M - 1)
        y = np.take_along_axis(idx, sel[:, None], axis=1)[:, 0]
        freq = np.bincount(y, minlength=N) / T
        ax.plot(np.arange(N), freq[order], mk, ms=3.2, color=col, label=f"M = {M}")
        print(f"M={M}: 主灯被选中频率 {freq[order[0]]:.3f}，目标 {target[order[0]]:.3f}")
    ax.set_xlabel("灯，按无阴影贡献从大到小排序")
    ax.set_ylabel("被选中的频率")
    ax.set_xlim(-1, N)
    ax.legend(loc="upper right")
    save(fig, "fig2-1-selection.png")


def fig2_2():
    rng = np.random.default_rng(2)
    Ms = [1, 2, 4, 8, 16, 32, 64]
    var_ris, var_uni = [], []
    for M in Ms:
        var_ris.append(ris_batch(M, 60000, rng).var() / TRUTH ** 2)
        idx = rng.integers(0, N, size=(30000, M))
        var_uni.append((N * F_SCENE[idx]).mean(axis=1).var() / TRUTH ** 2)
    p = B_SCENE / B_SCENE.sum()
    ideal = np.sum(F_SCENE ** 2 / p) - TRUTH ** 2
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.plot(Ms, var_ris, "o-", color=ACCENT, label="RIS，M 个候选（1 条阴影光线）")
    ax.plot(Ms, var_uni, "s-", color=BLUE, label="普通蒙特卡洛，M 个样本（M 条阴影光线）")
    ax.axhline(ideal / TRUTH ** 2, color=GREY, ls="--", lw=1.0)
    ax.text(Ms[0], ideal / TRUTH ** 2 * 1.12, "直接按目标函数采样一次", ha="left",
            color=GREY, fontsize=8)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("候选数 M（RIS）或阴影光线数 M（普通蒙特卡洛）")
    ax.set_ylabel("相对方差")
    ax.legend(loc="lower left")
    save(fig, "fig2-3-variance.png")


def fig2_3():
    rng = np.random.default_rng(3)
    n, runs = 300, 5000
    ok = np.cumsum(ris_batch(8, n * runs, rng).reshape(n, runs), axis=1)
    bad = np.cumsum(ris_batch(8, n * runs, rng, phat=F_SCENE,
                              drop_zero=True).reshape(n, runs), axis=1)
    k = np.arange(1, runs + 1)
    ok, bad = ok / k, bad / k
    mo, mb = ok.mean(0), bad.mean(0)
    so, sb = ok.std(0) / np.sqrt(n), bad.std(0) / np.sqrt(n)
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.plot(k, mo, color=ACCENT, label="按式 (2.11) 实现")
    ax.fill_between(k, mo - 2 * so, mo + 2 * so, color=ACCENT, alpha=0.20)
    ax.plot(k, mb, color=RED, label="丢掉零权重候选后重算 M")
    ax.fill_between(k, mb - 2 * sb, mb + 2 * sb, color=RED, alpha=0.14)
    ax.axhline(TRUTH, color=INK, ls=":", lw=1.0)
    ax.set_xscale("log")
    ax.set_xlabel("独立重复次数")
    ax.set_ylabel("累计平均值")
    ax.legend(loc="center right")
    save(fig, "fig2-2-unbiased.png")
    print(f"正确实现偏差 {mo[-1] / TRUTH - 1:+.4f}；错误实现偏差 {mb[-1] / TRUTH - 1:+.4f}"
          f"；真值 {TRUTH:.3f}")


def fig2_4():
    rng = np.random.default_rng(4)
    Ms = [1, 2, 4, 8, 16, 32]
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    for alpha, lab, col in [(0.0, "候选分布：均匀", BLUE),
                            (0.5, "候选分布：正比于 b 的平方根", TEAL),
                            (1.0, "候选分布：正比于 b", ACCENT)]:
        p = B_SCENE ** alpha
        p = p / p.sum()
        vals = []
        for M in Ms:
            e = ris_batch(M, 40000, rng, p=p)
            vals.append(np.var(e) / TRUTH ** 2)
        ax.plot(Ms, vals, "o-", color=col, label=lab)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_yticks([0.3, 0.4, 0.6, 1.0, 2.0, 3.0, 6.0])
    ax.set_yticklabels(["0.3", "0.4", "0.6", "1", "2", "3", "6"])
    ax.set_xlabel("候选数 M")
    ax.set_ylabel("相对方差")
    ax.legend(loc="upper right")
    save(fig, "fig2-4-source.png")


fig2_1()
fig2_2()
fig2_3()
fig2_4()
print("真值", round(TRUTH, 3), "可见灯数", int(V_SCENE.sum()), "B", round(B_SCENE.sum(), 1))
