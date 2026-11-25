import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.ticker import NullFormatter
import numpy as np

L = 2.0        # 场景边长，米
A = 10.0       # 表面积，平方米
KB, MB, GB = 1e3, 1e6, 1e9


def dense(h):      return (L / h) ** 3 * 4
def band(h, k=3):  return 2 * k * A / h ** 2 * 4
def octree(h, k=3):return 1.33 * 2 * k * A / h ** 2 * 8
def brick(h, k=3):
    n = 2 * k * A / h ** 2
    return n * 2 * 1.05 + (L / (8 * h)) ** 3 * 8 * 0.05
def hashed(h, k=3):return 2 * k * A / h ** 2 * 2 * 1.1


# ---------------------------------------------------------------- 图 15-1
def fig15_1():
    hs = np.logspace(np.log10(0.02), np.log10(0.001), 120)
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    ax.loglog(hs * 1000, dense(hs) / MB, color=RED, lw=1.9, label="稠密网格（fp32）")
    ax.loglog(hs * 1000, octree(hs) / MB, color=PURPLE, lw=1.6, label="八叉树（窄带叶子）")
    ax.loglog(hs * 1000, band(hs) / MB, color=BLUE, lw=1.6, label="窄带 k=3（fp32）")
    ax.loglog(hs * 1000, brick(hs) / MB, color=TEAL, lw=1.6, ls="--", label="砖块 8³（fp16）")
    ax.loglog(hs * 1000, hashed(hs) / MB, color=ACCENT, lw=1.6, ls="-.", label="稀疏哈希（fp16）")
    ax.axhline(8192, color=GREY, ls=":", lw=1.0)
    ax.text(20, 9500, "8 GB 预算", fontsize=7.5, color=GREY)
    ax.invert_xaxis()
    ax.set_xlabel("体素边长（毫米）")
    ax.set_ylabel("内存（MB）")
    ax.set_ylim(0.5, 2e4)
    ax.legend(loc="upper left", fontsize=7.0)
    ax.set_xticks([20, 10, 5, 2, 1])
    ax.set_xticklabels(["20", "10", "5", "2", "1"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    fig.tight_layout()
    save(fig, "fig15-1-memory.png")


# ---------------------------------------------------------------- 图 15-2
def fig15_2():
    names = ["稠密网格", "窄带", "八叉树", "砖块", "稀疏哈希"]
    q = [32, 32, 56, 26, 60]        # 单次三线性查询读取的字节数
    build = [100, 22, 34, 20, 18]   # 相对构建时间
    cols = [RED, BLUE, PURPLE, TEAL, ACCENT]

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))
    ax = axes[0]
    ax.barh(names, q, color=cols, height=0.62)
    ax.set_xlabel("单次三线性查询读取的字节数")
    ax.set_xlim(0, 70)
    for i, v in enumerate(q):
        ax.text(v + 1.5, i, str(v), va="center", fontsize=8)
    panel_label(ax, "(a)", x=-0.30, y=1.06)

    ax = axes[1]
    ax.barh(names, build, color=cols, height=0.62)
    ax.set_xlabel("相对构建时间（稠密网格为 100）")
    ax.set_xlim(0, 115)
    for i, v in enumerate(build):
        ax.text(v + 2, i, str(v), va="center", fontsize=8)
    panel_label(ax, "(b)", x=-0.30, y=1.06)
    fig.tight_layout()
    save(fig, "fig15-2-query.png")


# ---------------------------------------------------------------- 图 15-3
def fig15_3():
    hs = np.logspace(np.log10(0.02), np.log10(0.001), 120)
    fig, ax = plt.subplots(figsize=(6.3, 3.1))
    ax.loglog(hs * 1000, dense(hs) / 1e6 * 1.2, color=RED, lw=1.9, label="稠密网格")
    ax.loglog(hs * 1000, band(hs) / 1e6 * 3.0, color=BLUE, lw=1.6, label="窄带 EDT")
    ax.loglog(hs * 1000, brick(hs) / 1e6 * 1.4, color=TEAL, lw=1.6, ls="--", label="砖块（GPU）")
    ax.invert_xaxis()
    ax.set_xlabel("体素边长（毫米）")
    ax.set_ylabel("构建时间（秒，模型估算）")
    ax.set_xticks([20, 10, 5, 2, 1])
    ax.set_xticklabels(["20", "10", "5", "2", "1"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.legend(loc="upper right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig15-3-build.png")


if __name__ == "__main__":
    fig15_1()
    fig15_2()
    fig15_3()
