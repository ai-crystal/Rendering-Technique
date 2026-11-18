import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np


# ---------------------------------------------------------------- 图 8-1
def fig8_1():
    A = 5.0e5
    h = np.logspace(np.log10(0.02), np.log10(0.2), 200)
    sparse = 4.0 * 2 * A / h ** 2
    bricks = (A / (64 * h ** 2)) * (64 + 4)
    dag = bricks / 8.0

    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    ax.loglog(h * 100, sparse / 1e9, color=ACCENT, label="稀疏体素（4 字节/格）")
    ax.loglog(h * 100, bricks / 1e9, color=BLUE, label="位掩码砖块（68 字节/砖）")
    ax.loglog(h * 100, dag / 1e9, color=GREEN, label="砖块 + DAG 去重（8 倍）")
    ax.axhline(4.0, color=RED, ls="--", lw=1.1)
    ax.axhline(24.0, color=RED, ls=":", lw=1.1)
    ax.text(2.1, 4.6, "4 GB", color=RED, fontsize=7.5)
    ax.text(2.1, 27.0, "24 GB", color=RED, fontsize=7.5)
    ax.set_xlabel("体素边长 h（cm）")
    ax.set_ylabel("显存占用（GB）")
    ax.set_ylim(1e-3, 1e2)
    ax.legend(loc="lower left", fontsize=7.6)
    fig.tight_layout()
    save(fig, "fig8-2-budget.png")


# ---------------------------------------------------------------- 图 8-2
def fig8_2():
    v, dt = 5.0, 1.0 / 60.0
    h = np.logspace(np.log10(0.005), np.log10(0.1), 200)
    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    for (A, P, lab), col in zip(((6, 12, "1 m 见方"), (54, 36, "3 m 见方"),
                                 (600, 240, "10 m 见方")),
                                (BLUE, GOLD, RED)):
        n = 2 * (A + P * v * dt) / h ** 2
        ax.loglog(h * 100, n / 1e6, color=col, label=lab)
    ax.axhline(3.3, color=GREY, ls="--", lw=1.1)
    ax.text(2.2, 4.3, "16 ms 的预算，按每秒两亿格", fontsize=7.4, color="#3c4654")
    ax.set_xlabel("体素边长（cm）")
    ax.set_ylabel("每帧写入的体素数（百万）")
    ax.set_ylim(0.02, 200)
    ax.legend(loc="upper right", title="物体尺寸，速度 5 m/s", title_fontsize=7.6,
              fontsize=7.6)
    fig.tight_layout()
    save(fig, "fig8-3-dynamic.png")


# ---------------------------------------------------------------- 图 8-3
def fig8_3():
    h, H, fov = 0.05, 1080, np.deg2rad(60)
    d = np.logspace(np.log10(1), np.log10(3000), 400)
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for lvl, col in ((0, BLUE), (1, TEAL), (2, GOLD), (3, ACCENT)):
        px = (h * 2 ** lvl) / (2 * d * np.tan(fov / 2)) * H
        ax.loglog(d, px, color=col, label=f"LOD {lvl}，格 {h*2**lvl*100:.0f} cm")
    ax.axhline(1.0, color=RED, ls="--", lw=1.1)
    ax.text(1.2, 1.15, "1 像素", color=RED, fontsize=7.5)
    ax.set_xlabel("到相机的距离（m）")
    ax.set_ylabel("一个体素在屏幕上的尺寸（像素）")
    ax.set_ylim(1e-2, 1e3)
    ax.legend(loc="lower left", fontsize=7.4, ncol=2)
    note(ax, "1080 行，垂直视场 60 度", 0.62, 0.93)
    fig.tight_layout()
    save(fig, "fig8-1-lod.png")


if __name__ == "__main__":
    fig8_1()
    fig8_2()
    fig8_3()
