import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Circle, FancyArrowPatch, Arc


def arr(ax, p0, p1, color, lw=1.4, ms=9):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0))


def fig5_1():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.grid(False)

    # 悬丝与顶盘
    ax.plot([5, 5], [5.9, 3.2], color=GREY, lw=1.1)
    ax.add_patch(plt.Rectangle((4.2, 5.75), 1.6, 0.18, facecolor="#dfe6ee", edgecolor=INK))
    ax.text(5.95, 5.8, "扭转角读数", fontsize=8)
    # 水平杆
    ax.plot([3.2, 6.9], [3.2, 3.2], color=INK, lw=2.2)
    ax.add_patch(Circle((5, 3.2), 0.07, color=INK, zorder=4))
    # 带电球与配重
    ax.add_patch(Circle((6.9, 3.2), 0.24, facecolor="#f3c9c4", edgecolor=RED, lw=1.2))
    ax.text(6.70, 2.82, "$q_1$", fontsize=9, color=RED)
    ax.add_patch(Circle((3.2, 3.2), 0.20, facecolor="#dfe6ee", edgecolor=INK))
    ax.text(2.68, 3.28, "配重", fontsize=8)
    # 固定球
    ax.add_patch(Circle((8.4, 3.2), 0.24, facecolor="#cfe0ef", edgecolor=BLUE, lw=1.2))
    ax.text(8.75, 3.28, "$q_2$", fontsize=9, color=BLUE)
    ax.plot([8.4, 8.4], [3.2, 1.2], color=INK, lw=1.0)
    ax.plot([8.4, 9.5], [1.2, 1.2], color=INK, lw=1.0)
    ax.text(8.7, 0.95, "可转动底座", fontsize=8)
    # 力
    arr(ax, (7.2, 3.2), (7.85, 3.2), ACCENT, lw=1.3)
    arr(ax, (8.1, 3.2), (7.45, 3.2), ACCENT, lw=1.3)
    ax.text(7.52, 3.42, "$F$", fontsize=9, color=ACCENT)
    # 距离标注
    ax.annotate("", xy=(7.2, 2.55), xytext=(8.4, 2.55),
                arrowprops=dict(arrowstyle="<|-|>", color=GREY, lw=0.9, mutation_scale=8))
    ax.text(7.55, 2.28, "$r$", fontsize=9, color=GREY)
    ax.text(0.2, 0.3, "悬丝的扭转力矩与电力矩平衡：$\\kappa\\theta=F\\,r$",
            fontsize=8, color=INK)
    save(fig, "fig5-1-torsion.png")


def fig5_2():
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    ax.set_xlim(-0.08, 0.40)
    ax.set_ylim(-0.05, 0.50)
    ax.set_aspect("equal")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    pts = [(0.0, 0.0, "$q_1=+1.0\\ \\mu$C", RED),
           (0.30, 0.0, "$q_2=+2.0\\ \\mu$C", BLUE),
           (0.0, 0.40, "$q_3=-1.5\\ \\mu$C", PURPLE)]
    for x, y, lab, col in pts:
        ax.plot([x], [y], "o", ms=7, color=col, zorder=3)
        ax.text(x + 0.012, y + 0.012, lab, fontsize=8, color=col)

    ax.annotate("", xy=(0.30, 0.0), xytext=(0.0, 0.0),
                arrowprops=dict(arrowstyle="-", color=LIGHT, lw=0.8, ls=":"))
    ax.text(0.13, -0.035, "$0.30$ m", fontsize=7.5, color=GREY)
    ax.text(-0.065, 0.20, "$0.40$ m", fontsize=7.5, color=GREY, rotation=90, va="center")

    # 力：F13 指向 q1（向下），F23 指向 q2（右下）
    arr(ax, (0.0, 0.40), (0.0, 0.31), ACCENT, lw=1.5)
    ax.text(0.008, 0.325, "$F_{13}$", fontsize=8.5, color=ACCENT)
    scale = 0.10 / 0.108
    arr(ax, (0.0, 0.40), (0.0606, 0.40 - 0.0806), TEAL, lw=1.5)
    ax.text(0.040, 0.365, "$F_{23}$", fontsize=8.5, color=TEAL)
    # 合力
    arr(ax, (0.0, 0.40), (0.0647, 0.40 - 0.171), PURPLE, lw=2.0)
    ax.text(0.068, 0.30, "$\\mathbf{F}$", fontsize=9, color=PURPLE)
    ax.plot([0.0647, 0.0647], [0.40 - 0.171, 0.40], color=LIGHT, lw=0.7, ls="--")
    ax.plot([0.0, 0.0647], [0.40 - 0.171, 0.40 - 0.171], color=LIGHT, lw=0.7, ls="--")
    ax.set_xlabel("$x$（m）")
    ax.set_ylabel("$y$（m）")
    ax.set_title("$q_3$ 受两个力，合力为矢量和", fontsize=8.8)
    save(fig, "fig5-2-superposition.png")


def fig5_3():
    k = 8.99e9
    q1 = q2 = 1e-6
    r = np.logspace(-2, 1, 300)
    F = k * q1 * q2 / r ** 2
    F1 = k * q1 * q2 / r
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.loglog(r, F, color=BLUE, label="$F\\propto1/r^{2}$（库仑定律）")
    ax.loglog(r, F1, "--", color=GREY, label="$\\propto1/r$（对比）")
    for rr in (0.01, 0.1, 1.0):
        ax.plot([rr], [k * q1 * q2 / rr ** 2], "o", ms=4, color=ACCENT)
    ax.set_xlabel("距离 $r$（m）")
    ax.set_ylabel("力 $F$（N）")
    ax.legend(loc="upper right", fontsize=8)
    ax.text(0.03, 0.06, "双对数坐标下斜率为 $-2$", transform=ax.transAxes,
            fontsize=7.8, color=INK)
    save(fig, "fig5-3-inverse-square.png")


fig5_1()
fig5_2()
fig5_3()
