import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import lab


def fig7_1():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3))
    ax = axes[0]
    for bug, lab_, col in [(False, "正确：同时缩 $\\hat W$ 与 $M$", ACCENT),
                           (True, "只钳 $M$，不缩 $\\hat W$", BLUE)]:
        errs = []
        for s in range(6):
            r = lab.sim(seed=s * 97, T=24, M0=4, cap=20, radius=1, bug_cap=bug)
            t = r["truth"]
            errs.append(np.sqrt(np.mean(((r["est"] - t) / t) ** 2, axis=1)))
        ax.plot(np.mean(errs, axis=0), color=col, label=lab_)
    ax.set_yscale("log")
    ax.set_xlabel("帧")
    ax.set_ylabel("相对均方根误差")
    ax.legend(loc="lower right", fontsize=7)
    ax.set_title("钳制时漏掉缩放", fontsize=9)

    ax = axes[1]
    fracs = [0.1, 0.25, 0.5]
    for kind, lab_, col, mk in [("weak", "剔除最弱的灯", ACCENT, "o"),
                                ("random", "随机剔除", BLUE, "s")]:
        ys = []
        for f in fracs:
            bs = []
            for s in range(16):
                kw = dict(cull_weak=f) if kind == "weak" else dict(cull_random=f)
                r = lab.sim(seed=s * 97, T=16, M0=4, cap=20, radius=1, **kw)
                bs.append(lab.stats(r["est"][8:], r["truth"][8:])["bias"])
            ys.append(np.mean(bs) * 100)
            print(kind, f, "bias%", round(ys[-1], 1))
        ax.plot(np.array(fracs) * 100, ys, mk + "-", ms=4, color=col, label=lab_)
    ax.axhline(0, color=INK, lw=0.8, ls=":")
    ax.set_xlabel("被剔除的灯所占比例（%）")
    ax.set_ylabel("相对偏差（%）")
    ax.legend(loc="lower left", fontsize=8)
    ax.set_title("支持条件：零权重的灯", fontsize=9)
    fig.tight_layout()
    save(fig, "fig7-1-cap.png")


def fig7_2():
    clamps = [0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0]
    bia, rel = [], []
    for c in clamps:
        bs, sd = [], []
        for s in range(16):
            r = lab.sim(seed=s * 97, T=24, M0=4, cap=20, radius=1, clamp=c)
            st = lab.stats(r["est"][8:], r["truth"][8:])
            bs.append(st["bias"])
            sd.append(st["relstd"])
        bia.append(np.mean(bs) * 100)
        rel.append(np.mean(sd))
        print("clamp", c, "bias%", round(bia[-1], 1), "relstd", round(rel[-1], 3))
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.plot(clamps, bia, "o-", color=RED, label="相对偏差（%）")
    ax.set_xscale("log")
    ax.set_xlabel("钳制系数 $c$：借来的平均权重不超过自有平均权重的 $c$ 倍")
    ax.set_ylabel("相对偏差（%）")
    ax2 = ax.twinx()
    ax2.plot(clamps, rel, "s--", color=BLUE, label="相对标准差")
    ax2.set_ylabel("相对标准差")
    ax2.grid(False)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="center right", fontsize=8)
    save(fig, "fig7-2-clamp.png")


def fig7_3():
    """四类错误的偏差量级对比。"""
    names = ["$M$ 记成非零候选数", "随机剔除 25% 的灯", "空间复用不换算",
             "钳制系数 2", "时间复用不换算"]
    vals = [56.3, -27.4, 16.0, -16.3, -9.6]
    cols = [RED, RED, BLUE, BLUE, BLUE]
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    y = np.arange(len(names))
    ax.barh(y, vals, color=cols, alpha=0.85, height=0.6)
    for yy, v in zip(y, vals):
        ax.text(v + (1.5 if v > 0 else -1.5), yy, f"{v:+.1f}%",
                va="center", ha="left" if v > 0 else "right", fontsize=8)
    ax.axvline(0, color=INK, lw=0.9)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8.5)
    ax.set_xlabel("相对偏差（%）")
    ax.set_xlim(-70, 70)
    ax.invert_yaxis()
    ax.text(35, 4.35, "红色：记账错误", fontsize=7.5, color=RED, ha="center")
    ax.text(-35, 4.35, "蓝色：近似与钳制", fontsize=7.5, color=BLUE, ha="center")
    save(fig, "fig7-3-summary.png")


fig7_1()
fig7_2()
fig7_3()
