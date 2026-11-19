import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import lab
import ris


def single_pixel(N, M, trials=3000, seed=0, K=8):
    """单像素、单帧：M 个候选 + 一条阴影光线。

    权重模型：K 盏近处的灯贡献为 1，其余 (N-K) 盏远处的灯贡献为 1e-3。
    灯越多，随机挑中近处灯的概率越小，这正是"灯多到几千盏"时的处境。
    """
    rng0 = np.random.default_rng(seed)
    b = np.full(N, 1e-3)
    b[rng0.choice(N, K, replace=False)] = 1.0
    b = b / b.sum()
    v = ris.visibility(N, 1, seed, 0.62, soft=False)[0]
    f = b * v
    truth = f.sum()
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, N, size=(trials, M))
    w = b[idx]
    W = w.sum(axis=1)
    cdf = np.cumsum(w, axis=1) / np.maximum(W[:, None], 1e-300)
    sel = np.minimum((rng.random((trials, 1)) > cdf).sum(axis=1), M - 1)
    y = np.take_along_axis(idx, sel[:, None], 1)[:, 0]
    est = f[y] * (W / M) / b[y]
    return truth, est


def fig15_1():
    """256 盏灯时，复用把每帧的灯求值次数压到多少。"""
    N = 256
    Ms = [1, 2, 4, 8, 16]
    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    for cfg, lab_, col, mk in [(dict(temporal=False, spatial=False), "不复用", GREY, "^"),
                               (dict(temporal=True, spatial=False), "只做时间复用", BLUE, "s"),
                               (dict(radius=1), "时间 + 空间复用", ACCENT, "o")]:
        ys = []
        for M in Ms:
            sd = []
            for s_ in range(10):
                r = lab.sim(seed=s_ * 97, T=24, N=N, M0=M, cap=20, **cfg)
                sd.append(lab.stats(r["est"][8:], r["truth"][8:])["relstd"])
            ys.append(float(np.mean(sd)))
            print(lab_, "M0", M, round(ys[-1], 3))
        ax.plot(Ms, ys, mk + "-", ms=4, color=col, label=lab_)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("每帧每像素的灯求值次数 $M_0$")
    ax.set_ylabel("相对标准差")
    ax.legend(loc="upper right", fontsize=8)
    save(fig, "fig15-1-lights.png")


def fig15_2():
    """给定总代价，候选数与光线数怎么分。R 条光线用 R 次独立运行的平均来模拟。"""
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    N = 256
    for R, col in zip([1, 2, 4], [ACCENT, TEAL, BLUE]):
        xs, ys = [], []
        for M in [1, 2, 4, 8, 16]:
            runs = []
            truth = None
            for s in range(8):
                ests = []
                for k in range(R):
                    r = lab.sim(seed=s * 97 + 1000 * k, T=24, N=N, M0=M, cap=20, radius=1)
                    ests.append(r["est"])
                    truth = r["truth"]
                runs.append(np.mean(ests, axis=0))
            e = (np.array(runs) - truth) / truth
            ys.append(float(e.std()))
            xs.append(R * (20 + M))
            print(f"R={R} M={M} cost={R*(20+M)} relstd={ys[-1]:.3f}")
        ax.plot(xs, ys, "o-", ms=4, color=col, label=f"每帧 {R} 条光线")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("代价（1 次灯求值 = 1，1 条阴影光线 = 20）")
    ax.set_ylabel("相对标准差")
    ax.legend(loc="upper right", fontsize=7.5)
    save(fig, "fig15-2-budget.png")


fig15_1()
fig15_2()
