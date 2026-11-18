import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np


# ---------------------------------------------------------------- 图 4-1
def fig4_1():
    h = 0.01
    t = np.logspace(-1, np.log10(60), 400)
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for th, col in ((15.0, BLUE), (35.0, ACCENT)):
        r = t * np.tan(np.deg2rad(th))
        lev = np.log2(np.maximum(2 * r / h, 1.0))
        ax.plot(t, lev, color=col, lw=1.8, label=f"锥半角 {th:.0f} 度，连续值")
        ax.step(t, np.round(lev), color=col, lw=0.9, ls=":", alpha=0.9,
                label=f"锥半角 {th:.0f} 度，取整")
    ax.axhspan(0, 1, color=GREY, alpha=0.12)
    ax.text(0.12, 0.25, "层级 0 = 原始体素", fontsize=7.5, color="#3c4654")
    ax.set_xscale("log")
    ax.set_xlabel("沿锥的距离（m）")
    ax.set_ylabel("需要的 mip 层级")
    ax.set_ylim(-0.4, 12)
    ax.legend(loc="upper left", fontsize=7.4)
    note(ax, "体素边长 1 cm，层级按 $\\log_2(2r/h)$ 取", 0.30, 0.06)
    fig.tight_layout()
    save(fig, "fig4-1-cone-level.png")


# ---------------------------------------------------------------- 图 4-2
def fig4_2():
    h = 0.01
    thick = 0.20
    t = np.logspace(-1, np.log10(40), 300)
    half = np.deg2rad(15.0)
    r = t * np.tan(half)
    lev = np.log2(np.maximum(2 * r / h, 1.0))
    D = h * 2.0 ** np.round(lev)
    alpha = np.minimum(1.0, thick / D)
    T_box = 1.0 - alpha

    # 双层级插值：在 floor 与 ceil 两个层级之间按小数部分混合
    lo = np.floor(lev)
    f = lev - lo
    a_lo = np.minimum(1.0, thick / (h * 2.0 ** lo))
    a_hi = np.minimum(1.0, thick / (h * 2.0 ** (lo + 1)))
    T_lerp = (1 - f) * (1 - a_lo) + f * (1 - a_hi)

    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    ax.semilogx(t, T_box, color=RED, label="盒式 mip，取最近层级")
    ax.semilogx(t, T_lerp, color=BLUE, ls="--", label="两个层级线性插值")
    ax.axhline(0.0, color=GREEN, lw=1.4, label="保守 mip（取最大值）")
    ax.set_xlabel("遮挡板到相机中心的距离（m）")
    ax.set_ylabel("穿过去的能量比例")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="lower right", fontsize=7.6)
    note(ax, "板厚 0.20 m，体素 1 cm，锥半角 15 度，只考虑这一块板", 0.03, 0.97)
    fig.tight_layout()
    save(fig, "fig4-2-leak.png")


# ---------------------------------------------------------------- 图 4-3
def fig4_3():
    psi = np.linspace(3, 90, 300)
    extra = np.log2(1.0 / np.sin(np.deg2rad(psi)))
    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    ax.plot(psi, extra, color=PURPLE)
    ax.set_xlabel("视线与表面的夹角（度）")
    ax.set_ylabel("需要的额外 mip 层级")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 5.2)
    for p in (5, 10, 30):
        v = np.log2(1 / np.sin(np.deg2rad(p)))
        ax.plot([p], [v], "o", color=PURPLE, ms=4)
        ax.text(p + 2, v + 0.15, f"{v:.1f} 层", fontsize=7.6, color="#3c4654")
    note(ax, "足迹沿表面被拉长 $1/\\sin\\psi$ 倍", 0.42, 0.88)
    fig.tight_layout()
    save(fig, "fig4-3-aniso.png")


if __name__ == "__main__":
    fig4_1()
    fig4_2()
    fig4_3()
