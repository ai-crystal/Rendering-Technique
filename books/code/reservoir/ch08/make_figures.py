import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import lab


def measure(cfg, seeds=20, T=24):
    bs, sd = [], []
    for s in range(seeds):
        r = lab.sim(seed=s * 97, T=T, M0=4, **cfg)
        st = lab.stats(r["est"][8:], r["truth"][8:])
        bs.append(st["bias"])
        sd.append(st["relstd"])
    return float(np.mean(bs) * 100), float(np.mean(sd))


def fig8_1():
    radii = [1, 2, 3]
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3))
    ax = axes[0]
    for cap, col, mk in [(20, ACCENT, "o"), (100, BLUE, "s")]:
        ys = []
        for r in radii:
            _, sd = measure(dict(radius=r, cap=cap), seeds=40)
            ys.append(sd)
            print("cap", cap, "r", r, "relstd", round(sd, 3))
        ax.plot(np.array(radii) * 4, ys, mk + "-", ms=4, color=col, label=f"上限 {cap}")
    ax.set_xlabel("累计借用的邻居数 $4r$")
    ax.set_ylabel("相对标准差")
    ax.set_ylim(0.30, 0.45)
    ax.legend(loc="upper left", fontsize=7.5)
    ax.set_title("借得越多不一定越好", fontsize=9)

    ax = axes[1]
    b = lab.field(64, 64, seed=0)
    ids = np.arange(64).reshape(8, 8)
    med, p90 = [], []
    for r in radii:
        sp = []
        for dy, dx in ((0, r), (0, -r), (r, 0), (-r, 0)):
            j = np.roll(np.roll(ids, dy, 0), dx, 1).ravel()
            ratio = b / b[j]
            sp.append(ratio.max(axis=1) / ratio.min(axis=1))
        sp = np.concatenate(sp)
        med.append(np.median(sp))
        p90.append(np.percentile(sp, 90))
        print("r", r, "median spread", round(med[-1], 2), "p90", round(p90[-1], 2))
    ax.plot(np.array(radii) * 4, med, "o-", color=ACCENT, label="中位数")
    ax.plot(np.array(radii) * 4, p90, "s--", color=BLUE, label="90 分位")
    ax.set_xlabel("累计借用的邻居数 $4r$")
    ax.set_ylabel("相邻像素目标函数的比值跨度")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_title("几何相似度随距离下降", fontsize=9)
    fig.tight_layout()
    save(fig, "fig8-1-radius.png")


def fig8_2():
    names = ["只有初始候选", "只有时间复用", "只有空间复用", "两者都用"]
    cfgs = [dict(temporal=False, spatial=False), dict(spatial=False),
            dict(temporal=False, radius=1), dict(radius=1)]
    rel, bia = [], []
    for c in cfgs:
        b_, s_ = measure(dict(c, cap=20), seeds=24)
        rel.append(s_)
        bia.append(b_)
        print(names[len(rel) - 1], "relstd", round(s_, 3), "bias%", round(b_, 2))
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    x = np.arange(4)
    ax.bar(x, rel, width=0.55, color=[GREY, BLUE, TEAL, ACCENT], alpha=0.9)
    for i, (r_, b_) in enumerate(zip(rel, bia)):
        ax.text(i, r_ + 0.02, f"{r_:.2f}", ha="center", fontsize=8)
        ax.text(i, 0.06, f"{b_:+.1f}%", ha="center", fontsize=7.5, color="white")
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=8.5)
    ax.set_ylabel("相对标准差（$M_{\\max}=20$）")
    ax.set_ylim(0, 1.2)
    ax.text(0.02, 1.12, "柱内数字：相对偏差", fontsize=7.5, color=GREY)
    save(fig, "fig8-2-split.png")


def fig8_3():
    caps = [5, 10, 20, 50, 100, 200, 500]
    rel, bia = [], []
    for c in caps:
        b_, s_ = measure(dict(radius=1, cap=c), seeds=20)
        rel.append(s_)
        bia.append(b_)
        print("cap", c, "relstd", round(s_, 3), "bias%", round(b_, 2))
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.plot(caps, rel, "o-", color=BLUE, label="相对标准差")
    ax.set_xscale("log")
    ax.set_xlabel("候选数上限 $M_{\\max}$")
    ax.set_ylabel("相对标准差")
    ax2 = ax.twinx()
    ax2.plot(caps, bia, "s--", color=RED, label="相对偏差（%）")
    ax2.set_ylabel("相对偏差（%）")
    ax2.grid(False)
    ax2.set_ylim(-4, 4)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower center", fontsize=8)
    ax.axvline(50, color=LIGHT, lw=1.0)
    ax.text(53, 0.4, "50 之后基本不动", fontsize=7.5, color=GREY)
    save(fig, "fig8-3-cap.png")


fig8_1()
fig8_2()
fig8_3()
