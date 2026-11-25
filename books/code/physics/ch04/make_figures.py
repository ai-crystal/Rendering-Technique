import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def fig4_1():
    x = np.linspace(0, 1, 400)
    F = 6 * x * (1 - x)
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.fill_between(x, 0, F, color=SKY, alpha=0.35, lw=0)
    ax.plot(x, F, color=BLUE, lw=1.8)
    for a, b in [(0.1, 0.2), (0.45, 0.55), (0.8, 0.9)]:
        m = (a + b) / 2
        ax.add_patch(plt.Rectangle((a, 0), b - a, 6 * m * (1 - m), facecolor="none",
                                   edgecolor=ACCENT, lw=1.1))
    ax.annotate("面积 $=\\int_0^1 F\\,dx=1$ J", (0.5, 0.8), xytext=(0.58, 1.25),
                fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.set_xlabel("位移 $x$（m）")
    ax.set_ylabel("力 $F$（N）")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.7)
    ax.set_title("力随位移变化，功是曲线下的面积", fontsize=8.8)
    save(fig, "fig4-1-work.png")


def fig4_2():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1))
    k = 20.0
    x = np.linspace(-0.3, 0.3, 300)
    U = 0.5 * k * x ** 2
    ax = axes[0]
    ax.plot(x, U, color=BLUE, lw=1.8)
    for xx in (-0.22, 0.22):
        ax.annotate("", xy=(xx - 0.05 * np.sign(xx), 0.1), xytext=(xx, 0.1),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.3))
    ax.annotate("$F=-kx$", xy=(0.20, 0.40), xytext=(0.02, 0.78), fontsize=8.5,
                color=RED, arrowprops=dict(arrowstyle="-", color=RED, lw=0.7))
    ax.text(-0.28, 0.75, "$U=\\frac{1}{2}kx^{2}$", fontsize=8.5, color=BLUE)
    ax.set_xlabel("位移 $x$（m）")
    ax.set_ylabel("势能 $U$（J）")
    ax.set_xlim(-0.3, 0.3)
    ax.set_ylim(0, 1.0)
    ax.set_title("弹簧：抛物线势能", fontsize=8.8)

    ax = axes[1]
    y = np.linspace(0, 3, 300)
    ax.plot(y, y, color=TEAL, lw=1.8, label="$U=mgy$（重力）")
    yy = np.linspace(0.8, 2.2, 300)
    barrier = 0.9 + 0.8 * np.exp(-((yy - 1.5) / 0.28) ** 2)
    ax.plot(yy, barrier, color=PURPLE, lw=1.5, ls="--", label="一个势垒形状")
    ax.annotate("", xy=(1.42, 1.28), xytext=(1.62, 1.75),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
    ax.text(1.06, 1.78, "力指向势能下降方向", fontsize=7.8, color=RED)
    ax.set_xlabel("高度 $y$（m）")
    ax.set_ylabel("势能 $U$（J）")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 2.6)
    ax.legend(loc="upper left", fontsize=7.8)
    ax.set_title("直线势能与势垒", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig4-2-potential.png")


def fig4_3():
    m1, m2, v1, v2 = 2.0, 1.0, 3.0, -1.0
    p0 = m1 * v1 + m2 * v2
    K0 = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2

    def after(e):
        # 动量 + 恢复系数
        # m1 v1' + m2 v2' = p0 ;  v2' - v1' = e (v1 - v2)
        rel = e * (v1 - v2)
        v1p = (p0 - m2 * rel) / (m1 + m2)
        v2p = v1p + rel
        return v1p, v2p

    cases = [("完全非弹性\n$e=0$", 0.0), ("弹性\n$e=1$", 1.0), ("部分弹性\n$e=0.5$", 0.5)]
    P0, P1, K1 = [], [], []
    for _, e in cases:
        a, b = after(e)
        P1.append(m1 * a + m2 * b)
        K1.append(0.5 * m1 * a ** 2 + 0.5 * m2 * b ** 2)
    P0 = [p0] * 3

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    xx = np.arange(3)
    w = 0.34
    for ax, y0, y1, ylab, title in [(axes[0], P0, P1, "总动量（$\\mathrm{kg\\,m\\,s^{-1}}$）", "动量守恒"),
                                    (axes[1], [K0] * 3, K1, "总动能（J）", "动能在非弹性碰撞中减少")]:
        ax.bar(xx - w / 2, y0, w, color=SKY, label="碰前")
        ax.bar(xx + w / 2, y1, w, color=ACCENT, label="碰后")
        for i in range(3):
            ax.text(xx[i] - w / 2, y0[i] + 0.12, f"{y0[i]:.2f}", ha="center", fontsize=7.2)
            ax.text(xx[i] + w / 2, y1[i] + 0.12, f"{y1[i]:.2f}", ha="center", fontsize=7.2)
        ax.set_xticks(xx)
        ax.set_xticklabels([c[0] for c in cases], fontsize=7.6)
        ax.set_ylabel(ylab)
        ax.set_ylim(0, max(max(y0), max(y1)) * 1.30)
        ax.legend(loc="upper right", fontsize=7.6)
        ax.set_title(title, fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig4-3-collision.png")


fig4_1()
fig4_2()
fig4_3()
