import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import ris

SEEDS = range(8)
BASE = dict(grid=8, frames=32, M=4, cap=32, amp=0.1, radius=1)


def err_curve(cfg, seeds=SEEDS):
    e, m = [], []
    for s in seeds:
        r = ris.run(seed=s, **cfg)
        e.append(np.abs(r["est"] / r["truth"] - 1).mean(axis=1))
        m.append(r["m"].mean(axis=1))
    return np.mean(e, axis=0), np.mean(m, axis=0)


def fig3_1():
    fig, ax = plt.subplots(figsize=(6.3, 3.6))
    for cfg, lab, col, st in [
            (dict(temporal=False, spatial=False), "不复用", GREY, "o-"),
            (dict(temporal=True, spatial=False), "时间复用", BLUE, "s-"),
            (dict(temporal=True, spatial=True), "时间 + 空间复用", ACCENT, "D-")]:
        c = dict(BASE)
        c.update(cfg)
        e, m = err_curve(c)
        ax.plot(np.arange(1, len(e) + 1), e, st, ms=3, color=col, label=lab)
        print(f"{lab}: 帧1 {e[0]:.3f} 帧8 {e[7]:.3f} 帧32 {e[-1]:.3f}，M 末 {m[-1]:.0f}")
    ax.set_yscale("log")
    ax.set_yticks([0.15, 0.2, 0.3, 0.5, 0.7, 1.0])
    ax.set_yticklabels(["0.15", "0.2", "0.3", "0.5", "0.7", "1"])
    ax.set_ylim(0.14, 1.0)
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.set_xlabel("帧")
    ax.set_ylabel("平均相对误差")
    ax.legend(loc="lower left")
    save(fig, "fig3-1-frames.png")


def fig3_2():
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    caps = [4, 8, 16, 32, 64, 128]
    rows = {4: [], 16: [], 32: []}
    for cap in caps:
        e, _ = err_curve(dict(BASE, cap=cap))
        for f in rows:
            rows[f].append(e[f - 1])
    for (f, ys), col, mk in zip(rows.items(), [SKY, TEAL, ACCENT], ["o-", "s-", "D-"]):
        ax.plot(caps, ys, mk, ms=3.5, color=col, label=f"第 {f} 帧")
        print(f"cap={cap} 第{f}帧={ys[-1]:.3f}")
    ax.set_xscale("log", base=2)
    ax.set_yticks([0.15, 0.2, 0.3, 0.4, 0.6, 0.8])
    ax.set_yticklabels(["0.15", "0.2", "0.3", "0.4", "0.6", "0.8"])
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.set_xticks(caps)
    ax.set_xticklabels([str(c) for c in caps])
    ax.set_xlabel("候选数上限")
    ax.set_ylabel("平均相对误差")
    ax.legend(loc="upper right")
    save(fig, "fig3-2-mcap.png")


def fig3_3():
    b = ris.make_scene(64, 2, 1, "zipf", 1.0)
    r = b[0] / b[1]
    order = np.argsort(-b[0])
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    ax.plot(np.arange(1, 65), r[order], "o-", ms=3, color=BLUE, lw=1.2)
    med = np.median(r)
    ax.axhline(med, color=ACCENT, ls="--", lw=1.2)
    ax.text(63, med * 1.12, f"中位数 {med:.2f}", ha="right", color=ACCENT, fontsize=8)
    ax.set_yscale("log")
    ax.set_yticks([0.2, 0.35, 0.5, 1.0, 2.0, 3.0])
    ax.set_yticklabels(["0.2", "0.35", "0.5", "1", "2", "3"])
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.set_xlabel("灯，按像素 i 的目标函数排序")
    ax.set_ylabel("两像素目标函数之比")
    save(fig, "fig3-3-ratio.png")
    print(f"比值 {r.min():.2f} 到 {r.max():.2f}，中位数 {med:.2f}")


fig3_1()
fig3_2()
fig3_3()
