import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import ris

BASE = dict(grid=16, frames=32, M=4, cap=32, amp=0.1, radius=1)


def fig9_1():
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.1))
    for ax, (cfg, lab) in zip(axes, [
            (dict(temporal=False, spatial=False), "不复用"),
            (dict(temporal=True, spatial=True), "时间 + 空间复用")]):
        c = dict(BASE)
        c.update(cfg)
        r = ris.run(seed=3, **c)
        e = (r["est"][-1] / r["truth"][-1] - 1).reshape(16, 16)
        v = np.abs(e).max()
        im = ax.imshow(e, cmap="RdBu_r", vmin=-v, vmax=v)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_title(lab, fontsize=9)
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
        cb.ax.tick_params(labelsize=7)
        print(f"{lab}: 相邻像素误差的相关系数 "
              f"{np.corrcoef(e[:, :-1].ravel(), e[:, 1:].ravel())[0, 1]:+.2f}")
    save(fig, "fig9-1-errormap.png")


def fig9_2():
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    b = ris.make_scene(64, 1, 0, "zipf")[0]
    zero = np.zeros(64)
    zero[np.argmax(b)] = 1.0
    mask_bad = np.ones(64)
    mask_bad[np.argmax(b)] = 0.0
    for mask, lab, col in [(None, "目标函数完整", TEAL), (mask_bad, "目标函数漏掉最亮的一盏灯", RED)]:
        vals = []
        for s in range(60):
            r = ris.run(seed=200 + s, mask=mask,
                        grid=8, frames=32, M=4, cap=32, amp=0.1, radius=1,
                        temporal=True, spatial=True)
            vals.append(r["est"].mean() / r["truth"].mean())
        vals = np.array(vals)
        ax.hist(vals, bins=18, color=col, alpha=0.55, label=lab, density=True)
        print(f"{lab}: 均值 {vals.mean():.4f}，标准差 {vals.std():.4f}")
    ax.axvline(1.0, color=INK, ls=":", lw=1.2)
    ax.set_xlabel("整段序列的平均值除以真值")
    ax.set_ylabel("密度")
    ax.legend(loc="upper left")
    save(fig, "fig9-2-mean-test.png")


fig9_1()
fig9_2()
