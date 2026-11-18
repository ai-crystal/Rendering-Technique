import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import ris

# 二维经验：用 16×16 像素的场景比较连通度与对应的二维几何近似无关，
# 场景沿 8×8 的平面铺开，这里用 16 网格获得更细的半径梯度。

BASE = dict(grid=16, frames=40, M=4, cap=32, amp=0.1)
SEEDS = range(6)


def curve(**kw):
    c = dict(BASE)
    c.update(kw)
    errs = []
    for s in SEEDS:
        r = ris.run(seed=s, **c)
        errs.append(np.abs(r["est"] / r["truth"] - 1).mean(axis=1))
    return np.mean(errs, axis=0)


def fig8_1():
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    radii = [0, 1, 2, 3, 4, 6]
    means, last = [], []
    for R in radii:
        e = curve(radius=R, spatial=R > 0)
        means.append(e.mean())
        last.append(e[-1])
        print(f"半径 {R}: 全帧平均 {e.mean():.3f}，末帧 {e[-1]:.3f}")
    ax.plot(radii, means, "o-", ms=4, color=BLUE, label="全帧平均")
    ax.plot(radii, last, "s-", ms=4, color=ACCENT, label="第 40 帧")
    ax.set_xlabel("空间复用半径（像素）")
    ax.set_ylabel("平均相对误差")
    ax.set_xticks(radii)
    ax.legend(loc="upper right")
    save(fig, "fig8-1-radius.png")


def fig8_2():
    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    for M0, col, mk in [(2, SKY, "o"), (4, TEAL, "s"), (8, ACCENT, "D"), (16, RED, "v")]:
        xs, ys = [], []
        for R in [0, 1, 2, 3]:
            e = curve(M=M0, radius=R, spatial=R > 0).mean()
            cost = M0 * (1 + 4 * R)
            xs.append(cost)
            ys.append(e)
        ax.plot(xs, ys, mk + "-", ms=4, color=col, label=f"每帧新抽 {M0} 个")
        print(f"M0={M0}: " + " ".join(f"({c},{y:.3f})" for c, y in zip(xs, ys)))
    ax.set_xscale("log", base=2)
    ax.set_xlabel("每帧的候选总数（约等于工作量）")
    ax.set_ylabel("平均相对误差")
    ax.legend(loc="upper right")
    save(fig, "fig8-2-cost.png")


fig8_1()
fig8_2()
