import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import lab


def fig3_1():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.2))
    ax = axes[0]
    k = np.linspace(0.001, 1, 500)
    for w, lab_, col, ls in [(1.0, "$w=1$", BLUE, "-"), (4.0, "$w=4$", ACCENT, "--")]:
        ax.plot(k, w * k ** (w - 1), ls, color=col, label=lab_)
    ax.axvline(0.6, color=GREY, lw=1.0)
    ax.text(0.61, 3.3, "当前 key", fontsize=7.5, color=GREY)
    ax.fill_between(k[k > 0.6], 0, 4 * k[k > 0.6] ** 3, color=ACCENT, alpha=0.12, lw=0)
    ax.set_xlabel("key 值 $k=u^{1/w}$")
    ax.set_ylabel("概率密度")
    ax.set_ylim(0, 4.6)
    ax.legend(loc="upper left")
    ax.set_title("key 的分布随权重的变化", fontsize=9)
    note(ax, "$p(k)=w\\,k^{w-1}$", x=0.52, y=0.55)

    ax = axes[1]
    rng = np.random.default_rng(11)
    w = np.array([1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 140, 220], float)
    w = w / w.sum()
    trials = 120000
    cnt = np.zeros(w.size)
    for _ in range(trials):
        cnt[lab.wrs_ares(w, rng)] += 1
    freq = cnt / trials
    ax.plot([1e-3, 0.3], [1e-3, 0.3], color=GREY, ls=":", lw=1.0)
    ax.errorbar(w, freq, yerr=np.sqrt(w * (1 - w) / trials), fmt="o", ms=3.6,
                color=ACCENT, ecolor=LIGHT, elinewidth=0.8, capsize=2,
                label="A-Res 实测")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("理论权重 $w_i/W$")
    ax.set_ylabel("被选中的频率")
    ax.legend(loc="upper left")
    ax.set_title("选择频率与权重成正比", fontsize=9)
    print("ares max dev", np.abs(freq - w).max())
    fig.tight_layout()
    save(fig, "fig3-1-keys.png")


def fig3_2():
    ns = np.unique(np.round(np.geomspace(8, 20000, 14)).astype(int))
    draws = [lab.wrs_skip_cost(n, 3000, 5) for n in ns]
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.plot(ns, ns, color=BLUE, label="逐项比较：每次一个随机数")
    ax.plot(ns, draws, "o-", ms=3.5, color=ACCENT, label="跳步：只在接受时取随机数")
    ax.plot(ns, 2 * np.log(ns) + 3, "--", color=GREY, lw=1.0, label="约 $2\\ln n$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("流长度 $n$")
    ax.set_ylabel("均匀随机数消耗")
    ax.legend(loc="upper left")
    for n, d in zip(ns[::3], draws[::3]):
        ax.annotate(f"{d:.0f}", (n, d), textcoords="offset points", xytext=(2, -10),
                    fontsize=6.8, color=ACCENT)
    save(fig, "fig3-2-cost.png")


def fig3_3():
    rng = np.random.default_rng(3)
    wa = rng.random(18) * 2 + 0.2
    wb = rng.random(26) * 2 + 0.2
    ma, mb = 4, 40
    exact, good, bad = lab.merge_check(wa, wb, ma, mb, trials=80000, seed=3)
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    idx = np.arange(exact.size)
    ax.plot(idx, exact, "o", ms=3.4, color=INK, label="精确：$w_i/W$")
    ax.plot(idx, good, "x", ms=5, color=TEAL, label="按 $W$ 合并")
    ax.plot(idx, bad, "^", ms=3.6, color=RED, mfc="none", label="按 $W\\cdot M$ 合并")
    ax.axvline(18 - 0.5, color=LIGHT, lw=1.0)
    ax.text(9, 0.052, "$M=4$", ha="center", fontsize=8, color=GREY)
    ax.text(31, 0.052, "$M=40$", ha="center", fontsize=8, color=GREY)
    ax.set_xlabel("候选在合并池中的序号")
    ax.set_ylabel("被选中的频率")
    ax.set_ylim(0, 0.085)
    ax.legend(loc="upper left", fontsize=7.5)
    print("good dev", np.abs(good - exact).max(), "bad dev", np.abs(bad - exact).max())
    print("b 侧总概率 exact", exact[18:].sum(), "bad", bad[18:].sum())
    save(fig, "fig3-3-merge.png")


fig3_1()
fig3_2()
fig3_3()
