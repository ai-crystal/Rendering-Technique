import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np


# ---------------------------------------------------------------- 图 2-1
def fig2_1():
    L = np.arange(1, 13)
    dense = (2.0 ** L) ** 3
    full = (8.0 ** (L + 1) - 1) / 7.0
    surf = np.zeros_like(dense)
    for l in L:
        # 表面叶节点按面积增长：第 l 层大约是 6*4^l（立方体表面，常数取 6/4）
        surf = np.array([1.5 * 4.0 ** l for l in L])
    surface_nodes = surf * (1 + 1 / 4 + 1 / 16 + 1 / 64)   # 等比求和

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.semilogy(L, dense, color=ACCENT, marker="o", ms=3, label="稠密网格（全部体素）")
    ax.semilogy(L, full, color=GREY, ls="--", label="满八叉树（所有节点）")
    ax.semilogy(L, surface_nodes, color=BLUE, marker="s", ms=3,
                label="表面八叉树（只有表面附近）")
    ax.set_xlabel("层级 L（单轴分辨率 $2^L$）")
    ax.set_ylabel("节点数")
    ax.set_xticks(L[::2])
    ax.annotate("差 $2^L$ 倍", xy=(9.7, 1.6e5), xytext=(10.4, 2.2e7),
                fontsize=8, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.9))
    ax.legend(loc="upper left")
    fig.tight_layout()
    save(fig, "fig2-1-node-count.png")


# ---------------------------------------------------------------- 图 2-2
def fig2_2():
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    ax.set_xlim(0, 72)
    ax.set_ylim(0, 8)
    ax.axis("off")

    segs = [(0, 21, "x：21 位", BLUE), (21, 42, "y：21 位", TEAL),
            (42, 63, "z：21 位", PURPLE), (63, 64, "", GREY)]
    for a, b, lab, col in segs:
        ax.add_patch(plt.Rectangle((a, 5.0), b - a, 1.9, facecolor=col,
                                   alpha=0.22, edgecolor=col, lw=1.0))
        if lab:
            ax.text((a + b) / 2, 5.95, lab, ha="center", va="center", fontsize=8)
    ax.annotate("f", xy=(63.5, 6.9), xytext=(66.5, 7.3), fontsize=8,
                ha="left", arrowprops=dict(arrowstyle="-", lw=0.7, color=INK))
    ax.text(0, 7.5, "64 位体素地址（Morton 键）", fontsize=9, color=INK)
    for b in (21, 42, 63):
        ax.text(b, 4.65, str(b), fontsize=6.5, ha="center", va="top", color="#5b6472")

    ax.add_patch(plt.Rectangle((0, 1.6), 8, 1.9, facecolor=GOLD, alpha=0.30,
                               edgecolor=GOLD, lw=1.0))
    ax.text(4, 2.55, "8 位", ha="center", va="center", fontsize=7.5)
    ax.add_patch(plt.Rectangle((8, 1.6), 24, 1.9, facecolor=GREEN, alpha=0.22,
                               edgecolor=GREEN, lw=1.0))
    ax.text(20, 2.55, "24 位：砖块偏移或子表偏移", ha="center", va="center",
            fontsize=7.5)
    ax.text(0, 4.05, "32 位内节点", fontsize=9, color=INK)
    ax.text(36, 2.55, "砖块 8³ × 4 字节 = 2 KB", fontsize=8,
            color="#3c4654", va="center")
    fig.tight_layout()
    save(fig, "fig2-2-bitlayout.png")


# ---------------------------------------------------------------- 图 2-3
def fig2_3():
    L = np.arange(4, 11)
    octree = 3.4 * L                      # 每层平均访问节点数 3.4
    dda = 2.0 ** L / 2.0                  # 沿一条对角线穿过的体素数
    bvh = 12 + 2.0 * np.log2(3.0 * 4.0 ** L)   # 节点数 ∝ 表面积

    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    ax.semilogy(L, dda, color=ACCENT, marker="o", ms=3, label="稠密网格 DDA")
    ax.semilogy(L, octree, color=BLUE, marker="s", ms=3, label="稀疏八叉树")
    ax.semilogy(L, bvh, color=GREEN, marker="^", ms=3, label="BVH")
    ax.set_xlabel("层级 L（单轴分辨率 $2^L$）")
    ax.set_ylabel("一次求交访问的节点数")
    ax.set_xticks(L)
    ax.legend(loc="upper left")
    note(ax, "模型：八叉树每层 3.4 个节点，DDA 穿 $2^L/2$ 格，BVH 每层 2 个节点", 0.22, 0.22)
    fig.tight_layout()
    save(fig, "fig2-3-traversal.png")


if __name__ == "__main__":
    fig2_1()
    fig2_2()
    fig2_3()
