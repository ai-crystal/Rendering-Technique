import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()
LO, HI = 380.0, 780.0


# ------------------------------------------------------------------ 图 10-1
def fig6_1():
    """三种波长采样：均匀、分层、按视觉响应。"""
    rng = np.random.default_rng(7)
    N = 48
    uni = rng.uniform(LO, HI, N)
    strat = LO + (np.arange(N) + rng.uniform(0, 1, N)) * (HI - LO) / N

    y = cie_y(LAM)
    cdf = np.cumsum(y)
    cdf = np.concatenate([[0], cdf / cdf[-1]])
    xs = np.concatenate([[LO], LAM])
    imp = np.interp(rng.uniform(0, 1, N), cdf, xs)

    fig = plt.figure(figsize=(7.0, 3.3))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.0], hspace=0.34)

    ax = fig.add_subplot(gs[0])
    rows = [(uni, "均匀随机"), (strat, "分层"), (imp, r"按 $\bar{y}$ 采样")]
    for i, (s, lab) in enumerate(rows):
        yy = 2 - i
        ax.plot(s, np.full_like(s, yy), "|", color=PALETTE[i], ms=11, mew=1.2)
        ax.text(376, yy, lab, ha="right", va="center", fontsize=8.5)
    ax.set_xlim(376, 784)
    ax.set_ylim(-0.35, 2.55)
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.grid(False)

    ax2 = fig.add_subplot(gs[1])
    ax2.plot(LAM, np.full_like(LAM, 1.0 / (HI - LO)), color=PALETTE[0], lw=1.5,
             label="均匀的密度 1/400")
    ax2.plot(LAM, y / (y.sum() * (LAM[1] - LAM[0])), color=PALETTE[2], lw=1.9, label="正比于视觉响应的密度")
    ax2.set_xlim(380, 780)
    ax2.set_ylim(0, 0.0108)
    ax2.set_xlabel("波长 λ (nm)")
    ax2.set_ylabel("概率密度 (1/nm)")
    ax2.legend(loc="upper right")
    save(fig, "fig10-1-sampling.png")


# ------------------------------------------------------------------ 图 10-2
def _estimate_y(spd, lam_samples, pdf):
    """Y 的蒙特卡洛估计：mean(f(λ) c(λ) / p(λ))。"""
    f = np.interp(lam_samples, LAM, spd) * np.interp(lam_samples, LAM, cie_y(LAM))
    return float(np.mean(f / pdf))


def fig6_2():
    """均匀采样与按响应采样的方差对比。"""
    spd = blackbody(LAM, 3200.0) * (0.05 + 0.9 * gaussian_line(LAM, 560, 120))
    truth = float(np.sum(spd * cie_y(LAM)) * (LAM[1] - LAM[0]))

    y = cie_y(LAM)
    cdf = np.concatenate([[0], np.cumsum(y) / np.cumsum(y)[-1]])
    y_norm = float(np.sum(y * (LAM[1] - LAM[0])))

    rng = np.random.default_rng(11)
    Ns = np.array([4, 8, 16, 32, 64, 128, 256])
    trials = 3000
    err_u, err_i = [], []
    for N in Ns:
        eu, ei = [], []
        for _ in range(trials):
            u = rng.uniform(LO, HI, N)
            eu.append(_estimate_y(spd, u, 1.0 / (HI - LO)) / truth - 1)
            v = np.interp(rng.uniform(0, 1, N), cdf, np.concatenate([[LO], LAM]))
            p = np.interp(v, LAM, y) / y_norm
            ei.append(_estimate_y(spd, v, p) / truth - 1)
        err_u.append(np.sqrt(np.mean(np.square(eu))))
        err_i.append(np.sqrt(np.mean(np.square(ei))))

    fig, ax = plt.subplots(figsize=(6.0, 3.1))
    ax.loglog(Ns, err_u, "o-", color=BLUE, ms=4, label="均匀采样")
    ax.loglog(Ns, err_i, "s-", color=ACCENT, ms=4, label="按视觉响应采样")
    ref = err_u[0] * np.sqrt(Ns[0] / Ns)
    ax.loglog(Ns, ref, ":", color=GREY, lw=1.0, label="1/√N")
    ax.set_xlabel("波长样本数 N")
    ax.set_ylabel("Y 的相对 RMS 误差")
    ax.legend(loc="lower left")
    ax.set_title("斜率都是 $-1/2$，差的是常数", pad=6)
    save(fig, "fig10-2-variance.png")


# ------------------------------------------------------------------ 图 10-3
def fig6_3():
    """波长数 n 与误差：平滑光谱与窄线光谱的不同行为。"""
    smooth = blackbody(LAM, 3200.0)
    line = gaussian_line(LAM, 545, 3.0)

    def rms(spd, n, trials=4000, total=256, seed=3):
        rng = np.random.default_rng(seed)
        truth = float(np.sum(spd * (LAM[1] - LAM[0])))
        errs = []
        paths = total // n
        step = (HI - LO) / n
        for _ in range(trials):
            acc = 0.0
            for _ in range(paths):
                hero = rng.uniform(LO, HI)
                ls = LO + np.mod(hero - LO + np.arange(n) * step, HI - LO)
                acc += np.interp(ls, LAM, spd).mean()
            acc /= paths
            acc *= (HI - LO)
            errs.append(acc / truth - 1)
        return float(np.sqrt(np.mean(np.square(errs))))

    ns = [1, 2, 4, 8, 16]
    e_smooth = [rms(smooth, n) for n in ns]
    e_line = [rms(line, n) for n in ns]

    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.semilogy(ns, e_smooth, "o-", color=BLUE, ms=4.5, label="平滑光谱（3200 K 黑体）")
    ax.semilogy(ns, e_line, "s-", color=ACCENT, ms=4.5, label="窄线光谱（545 nm，宽 3 nm）")
    ax.set_xticks(ns)
    ax.set_xlabel("每条路径的波长数 n（总样本数固定为 256）")
    ax.set_ylabel("估计的相对 RMS 误差")
    ax.legend(loc="best")
    save(fig, "fig10-3-samples.png")


fig6_1()
fig6_2()
fig6_3()
