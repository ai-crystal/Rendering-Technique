import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *

LAM = 550.0


def fig7_1():
    g = np.linspace(0, 8, 600)
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    ax.plot(g, np.exp(-g), color=GREY, lw=1.9, label="镜面分量 exp(-g)")
    ax.plot(g, 1 - np.exp(-g), color=ACCENT, lw=1.9, label="漫射分量 1-exp(-g)")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("相位方差 g")
    ax.set_ylabel("能量占比")
    ax.legend(loc="center right", fontsize=8)
    ax2 = ax.twiny()
    sh = np.sqrt(g) * LAM / (4 * np.pi)
    ax2.set_xlim(0, 8)
    ticks = [0, 1, 2, 4, 8]
    ax2.set_xticks(ticks)
    ax2.set_xticklabels(["%.0f" % (np.sqrt(t) * LAM / (4 * np.pi)) for t in ticks])
    ax2.set_xlabel("对应的高度标准差（nm）")
    ax2.spines["top"].set_visible(False)
    ax.annotate("g = 1", xy=(1, 0.37), xytext=(1.6, 0.55), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.8))
    save(fig, "fig7-1-split.png")


def lobe(theta_deg, l_over_lam, g=2.0):
    """(7.7) 前三项，theta 为相对镜面方向的偏移角。"""
    q = 2 * np.pi * np.sin(np.radians(theta_deg)) / LAM
    out = np.zeros_like(theta_deg, dtype=float)
    for n in (1, 2, 3):
        out += g ** n / (float(__import__("math").factorial(n)) * n) * np.exp(-(q ** 2) * (l_over_lam * LAM) ** 2 / (4 * n))
    return np.exp(-g) * out


def fig7_2():
    th = np.linspace(-40, 40, 1200)
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    for l, col in [(1, ACCENT), (3, TEAL), (10, BLUE)]:
        I = lobe(th, l)
        ax.plot(th, I / I.max(), color=col, lw=1.8, label="l = %d 个波长" % l)
    ax.set_xlim(-40, 40)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("相对镜面方向的偏移角（度）")
    ax.set_ylabel("归一化强度")
    ax.legend(loc="upper right", fontsize=8)
    ax.text(-39, 0.55, "三条曲线能量相同，宽度不同", fontsize=8, color=GREY)
    save(fig, "fig7-2-lobe.png")


fig7_1()
fig7_2()
