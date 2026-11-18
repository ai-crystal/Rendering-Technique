import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def fig6_1():
    lam = np.linspace(380, 780, 500)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    for ax, d, ms in [(axes[0], 1600, [0, 1, 2]), (axes[1], 600, [0, 1])]:
        for m in ms:
            s = m * lam / d
            ok = np.abs(s) <= 1
            th = np.where(ok, np.degrees(np.arcsin(np.clip(s, -1, 1))), np.nan)
            ax.plot(lam, th, lw=1.8, color=PALETTE[m % len(PALETTE)],
                    label="m = %d" % m)
        ax.set_xlim(380, 780)
        ax.set_ylim(0, 92)
        ax.set_xlabel("波长（nm）")
        ax.set_ylabel("衍射角（度）")
        ax.set_title("d = %d nm" % d, fontsize=9)
        ax.legend(loc="lower right", fontsize=7.5)
    fig.subplots_adjust(wspace=0.3)
    save(fig, "fig6-1-grating.png")


def fig6_2():
    delta = np.linspace(-3, 3, 4000)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for N, col in [(2, BLUE), (5, TEAL), (20, ACCENT)]:
        num = np.sin(N * np.pi * delta) ** 2
        den = np.sin(np.pi * delta) ** 2
        I = np.where(np.abs(den) < 1e-10, N ** 2, num / np.maximum(den, 1e-12))
        ax.plot(delta, I / N ** 2, color=col, lw=1.3, label="N = %d" % N)
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("相邻缝的相位差 / 2π")
    ax.set_ylabel("归一化强度")
    ax.legend(loc="upper center", ncol=3, fontsize=8, bbox_to_anchor=(0.5, 1.16))
    ax.text(-2.9, 0.55, "峰宽约 1/N", fontsize=8, color=GREY)
    save(fig, "fig6-2-nslit.png")


def fig6_3():
    th = np.linspace(0, 70, 400)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    # 多层膜：Bragg-Snell
    n1, D1 = 1.6, 195.0
    lam1 = 2 * D1 * np.sqrt(n1 ** 2 - np.sin(np.radians(th)) ** 2)
    # 二维光子晶体：有效折射率更低，周期更大
    n2, D2 = 1.35, 260.0
    lam2 = 2 * D2 * np.sqrt(n2 ** 2 - np.sin(np.radians(th)) ** 2)
    # 光栅：d = 350 nm
    d3 = 800.0
    lam3 = d3 * np.sin(np.radians(th))
    ax.plot(th, lam1, color=BLUE, lw=1.9, label="多层膜")
    ax.plot(th, lam2, color=TEAL, lw=1.9, label="二维光子晶体")
    ax.plot(th, lam3, color=ACCENT, lw=1.9, label="光栅，d = 800 nm")
    ax.axhspan(380, 780, color="#f4efe4", alpha=0.7, zorder=0)
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 900)
    ax.set_xlabel("观察方向与法线的夹角（度）")
    ax.set_ylabel("反射峰波长（nm）")
    ax.legend(loc="upper right", fontsize=8)
    ax.text(2, 810, "可见光范围", fontsize=7.5, color=GREY)
    save(fig, "fig6-3-shift.png")


fig6_1()
fig6_2()
fig6_3()
