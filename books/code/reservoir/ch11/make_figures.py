import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *

B2 = 2.6


def phat(x):
    x = np.asarray(x, float)
    return np.exp(-((x - 0.72) / 0.10) ** 2) + 0.55 * np.exp(-((x - 0.28) / 0.14) ** 2)


def p1(x):
    return np.ones_like(np.asarray(x, float))


def p2(x):
    return (B2 + 1.0) * np.clip(np.asarray(x, float), 0, 1) ** B2


def P2_inv(u):
    return np.clip(np.asarray(u, float), 0, 1) ** (1.0 / (B2 + 1.0))


XS = np.linspace(1e-5, 1 - 1e-5, 20001)
TRUTH = np.trapezoid(phat(XS), XS)


def pooled(M1, M2, rng, share="equal", correction=True, trials=40000, f=None):
    """两个技术合成一个池子。

    share="equal" 给两个技术相同的话语权，share="count" 按候选数分配。
    correction=True 时乘上 M/M_i。
    """
    M = M1 + M2
    x1 = rng.random((trials, M1))
    x2 = P2_inv(rng.random((trials, M2)))
    w1 = phat(x1) / p1(x1)
    w2 = phat(x2) / p2(x2)
    if share == "equal":
        m1, m2 = 0.5, 0.5
    else:
        m1, m2 = M1 / M, M2 / M
    w1 = w1 * m1
    w2 = w2 * m2
    if correction:
        w1 = w1 * (M / M1)
        w2 = w2 * (M / M2)
    x = np.concatenate([x1, x2], axis=1)
    w = np.concatenate([w1, w2], axis=1)
    W = w.sum(axis=1)
    cdf = np.cumsum(w, axis=1) / np.maximum(W[:, None], 1e-300)
    idx = np.minimum((rng.random((trials, 1)) > cdf).sum(axis=1), M - 1)
    y = np.take_along_axis(x, idx[:, None], 1)[:, 0]
    return W / M, y


def fig11_1():
    rng = np.random.default_rng(0)
    M1, M2 = 4, 28
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3))

    ax = axes[0]
    cases = [("equal", True, "等权 + $M/M_i$", ACCENT),
             ("count", True, "按候选数 + $M/M_i$", GREY),
             ("equal", False, "等权，不乘 $M/M_i$", BLUE)]
    for share, corr, lab_, col in cases:
        est, y = pooled(M1, M2, rng, share=share, correction=corr)
        rel = est.mean() / TRUTH - 1
        print(f"{lab_}: bias {rel*100:+.2f}%")
        ax.hist(y, bins=70, range=(0, 1), density=True, histtype="step", lw=1.4,
                color=col, label=f"{lab_}（{rel*100:+.0f}%）")
    xs = np.linspace(0.001, 0.999, 600)
    ax.plot(xs, phat(xs) / TRUTH, color=INK, lw=1.0, ls=":", label="归一化目标")
    ax.set_xlabel("样本位置 $x$")
    ax.set_ylabel("选中样本的密度")
    ax.legend(loc="upper left", fontsize=7)
    ax.set_title("$M_1=4$，$M_2=28$", fontsize=9)

    ax = axes[1]
    ratios = [1, 2, 4, 7, 10]
    for share, corr, lab_, col, mk in [("equal", True, "等权 + $M/M_i$", ACCENT, "o"),
                                       ("count", True, "按候选数 + $M/M_i$", GREY, "^"),
                                       ("equal", False, "等权，不乘", BLUE, "s"),
                                       ("count", False, "按候选数，不乘", RED, "d")]:
        ys = []
        for r_ in ratios:
            e, _ = pooled(4, 4 * r_, rng, share=share, correction=corr, trials=12000)
            ys.append((e.mean() / TRUTH - 1) * 100)
            print("ratio", r_, lab_, round(ys[-1], 1))
        ax.plot(ratios, ys, mk + "-", ms=4, color=col, label=lab_)
    ax.axhline(0, color=INK, lw=0.8, ls=":")
    ax.set_xlabel("候选数之比 $M_2/M_1$（$M_1=4$）")
    ax.set_ylabel("相对偏差（%）")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=2, fontsize=7)
    ax.set_title("份额修正的作用", fontsize=9)
    fig.tight_layout()
    save(fig, "fig11-1-share.png")


def fig11_2():
    """移位映射把密度搬到另一个域：漏掉 |dx/du| 的后果。"""
    rng = np.random.default_rng(1)
    scales = [1.0, 1.2, 1.5, 1.8, 2.2]
    good, bad = [], []
    M = 24
    for s in scales:
        x = rng.random((20000, M)) * s            # 技术 2 抽在 [0, s]，在 x 上的密度是 1/s
        w_ok = phat(x) / (1.0 / s)                # 正确的密度 1/s
        w_bad = phat(x) / 1.0                     # 忘了换域，仍按 1 算
        for w, acc in [(w_ok, good), (w_bad, bad)]:
            W = w.sum(axis=1)
            acc.append((W / M).mean() / TRUTH - 1)
        print(f"s={s}: 正确 {good[-1]*100:+.1f}% 漏掉 {bad[-1]*100:+.1f}%")
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    ax.plot(scales, np.array(good) * 100, "o-", color=ACCENT, label="按换域后的密度归一")
    ax.plot(scales, np.array(bad) * 100, "s--", color=BLUE, label="漏掉雅可比")
    ax.axhline(0, color=INK, lw=0.8, ls=":")
    ax.set_xlabel("移位映射的缩放因子 $s$（技术 2 的样本集中在 $[0,s]$）")
    ax.set_ylabel("相对偏差（%）")
    ax.legend(loc="lower left", fontsize=8)
    save(fig, "fig11-2-jacobian.png")


def fig11_3():
    """退化：单个技术、M_i = M 时，修正因子等于 1，GRIS 就是 RIS。"""
    rng = np.random.default_rng(2)
    M = 8
    x = rng.random((20000, M))
    w = phat(x)
    W = w.sum(axis=1)
    cdf = np.cumsum(w, axis=1) / np.maximum(W[:, None], 1e-300)
    idx = np.minimum((rng.random((20000, 1)) > cdf).sum(axis=1), M - 1)
    y = np.take_along_axis(x, idx[:, None], 1)[:, 0]
    est = W / M

    # 拆成两个技术，每个 4 个候选，等权并乘 M/M_i = 8/4 = 2
    x1 = rng.random((20000, 4))
    x2 = rng.random((20000, 4))
    w1 = phat(x1) * 0.5 * 2.0
    w2 = phat(x2) * 0.5 * 2.0
    W2 = np.concatenate([w1, w2], axis=1).sum(axis=1)
    est2 = W2 / M
    print("单技术", round(float(est.mean()), 5), "拆成两技术", round(float(est2.mean()), 5),
          "真值", round(float(TRUTH), 5))

    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    ax.hist(y, bins=80, range=(0, 1), density=True, histtype="step", lw=1.5,
            color=ACCENT, label="单技术 RIS，$M=8$")
    xs = np.linspace(0.001, 0.999, 600)
    ax.plot(xs, phat(xs) / TRUTH, color=INK, lw=1.0, ls=":", label="归一化目标")
    ax.set_xlabel("样本位置 $x$")
    ax.set_ylabel("密度")
    ax.legend(loc="upper left", fontsize=8)
    save(fig, "fig11-3-degenerate.png")


fig11_1()
fig11_2()
fig11_3()
