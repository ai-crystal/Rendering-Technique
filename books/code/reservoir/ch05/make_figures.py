import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import lab
import ris


def multi(cfg, seeds=12, T=24, **kw):
    est, tru, m = [], [], []
    for s in range(seeds):
        r = lab.sim(seed=s * 97, T=T, M0=4, **(cfg | kw))
        est.append(r["est"])
        tru.append(r["truth"])
        m.append(r["m"])
    return np.array(est), np.array(tru), np.array(m).mean(0)


def fig5_1():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3))
    ax = axes[0]
    for cfg, lab_, col in [(dict(cap=2000, spatial=False), "只做时间复用（上限 2000）", BLUE),
                           (dict(cap=100), "时间 + 空间复用，上限 100", TEAL),
                           (dict(cap=20), "时间 + 空间复用，上限 20", ACCENT)]:
        _, _, m = multi(cfg, seeds=4)
        ax.plot(m.mean(axis=1), color=col, label=lab_)
    ax.set_yscale("log")
    ax.set_xlabel("帧")
    ax.set_ylabel("候选数 $M$")
    ax.legend(loc="lower right", fontsize=7)
    ax.set_title("历史样本让 $M$ 增长", fontsize=9)

    ax = axes[1]
    for cfg, lab_, col in [(dict(temporal=False, spatial=False), "只用初始候选", GREY),
                           (dict(temporal=True, spatial=False), "加时间复用", BLUE),
                           (dict(radius=1), "加空间复用", ACCENT)]:
        est, tru, _ = multi(cfg, seeds=16)
        err = np.sqrt(np.mean((est - tru) ** 2, axis=2) / np.mean(tru, axis=2) ** 2)
        ax.plot(err.mean(axis=0), color=col, label=lab_)
    ax.axhline(0.585, color=LIGHT, ls=":", lw=1.0)
    ax.text(12.0, 0.60, "按 $b$ 完美采样的单条光线", fontsize=7, color=GREY)
    ax.set_yscale("log")
    ax.set_ylim(0.15, 3)
    ax.set_xlabel("帧")
    ax.set_ylabel("相对均方根误差")
    ax.legend(loc="upper right", fontsize=7.5)
    ax.set_title("误差随帧下降，然后停住", fontsize=9)
    fig.tight_layout()
    save(fig, "fig5-2-frames.png")


def fig5_2():
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    Ms = [1, 2, 4, 8, 16, 32, 64, 128]
    out = []
    for M0 in Ms:
        sd = []
        for s in range(20):
            r = lab.sim(seed=s * 97, T=16, M0=M0, cap=20, temporal=False, spatial=False)
            sd.append(lab.stats(r["est"][8:], r["truth"][8:])["relstd"])
        out.append(np.mean(sd))
        print("M0", M0, "relstd", round(out[-1], 3))
    ax.plot(Ms, out, "s-", ms=4, color=BLUE, label="不复用，$M_0$ 个候选")

    for cap, col, mk in [(20, ACCENT, "o"), (100, TEAL, "^")]:
        xs, ys = [], []
        for M0 in (1, 2, 4, 8):
            sd = []
            for s in range(20):
                r = lab.sim(seed=s * 97, T=16, M0=M0, cap=cap, radius=1)
                sd.append(lab.stats(r["est"][8:], r["truth"][8:])["relstd"])
            xs.append(M0)
            ys.append(np.mean(sd))
            print("reuse M0", M0, "cap", cap, "relstd", round(ys[-1], 3))
        ax.plot(xs, ys, mk + "-", ms=4, color=col, label=f"时间 + 空间复用，上限 {cap}")
    ax.axhline(0.585, color=LIGHT, ls=":", lw=1.0)
    ax.text(1.05, 0.60, "按 $b$ 完美采样的单条光线", fontsize=7, color=GREY)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("每帧每像素的灯求值次数")
    ax.set_ylabel("相对标准差")
    ax.set_ylim(0.25, 3)
    ax.legend(loc="upper right", fontsize=7.5)
    save(fig, "fig5-3-cost.png")


def fig5_3():
    b = ris.make_scene(64, 8, 2, "zipf", 3.5)
    g = 8
    i = 27
    j = i + 1                      # 右邻
    ratio = b[i] / b[j]
    order = np.argsort(-ratio)
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.plot(np.arange(64), ratio[order], "o-", ms=3.2, color=ACCENT, lw=1.0)
    ax.axhline(1.0, color=INK, lw=1.0, ls=":")
    ax.set_yscale("log")
    ax.set_xlabel("灯（按比值排序）")
    ax.set_ylabel("$\\hat p_i(k)/\\hat p_j(k)$")
    med = np.median(ratio)
    ax.axhline(med, color=BLUE, lw=1.0, ls="--")
    ax.text(40, med * 1.08, f"中位数 {med:.2f}", fontsize=7.5, color=BLUE)
    ax.set_ylim(0.25, 2.8)
    ax.text(3.0, 0.27, "把整条曲线当成一条水平线，就是单点换算", fontsize=7.5, color=GREY)
    print("ratio min", ratio.min(), "max", ratio.max(), "median", med,
          "spread", ratio.max() / ratio.min())
    save(fig, "fig5-1-ratio.png")


fig5_1()
fig5_2()
fig5_3()
