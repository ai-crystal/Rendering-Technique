import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

D2R = np.pi / 180


def fig17_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    ax = axes[0]
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(1.0 * np.cos(th), 1.0 * np.sin(th), color=GREY, lw=1.2)
    for a in (0, 90, 180, 270):
        x, y = np.cos(a * D2R), np.sin(a * D2R)
        ax.annotate("", xy=(x - 0.28 * np.sin(a * D2R), y + 0.28 * np.cos(a * D2R)),
                    xytext=(x, y),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.2, mutation_scale=8))
    ax.plot([0], [0], "x", color=RED, ms=7)
    ax.text(0.08, 0.08, r"$\mathbf{B}\otimes$", fontsize=9, color=RED)
    ax.set_aspect("equal")
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("垂直入射：圆周", fontsize=8.8)

    ax = axes[1]
    t = np.linspace(0, 6 * np.pi, 600)
    ax.plot(0.5 * np.cos(t), 0.5 * np.sin(t) + 0.16 * t, color=BLUE, lw=1.2)
    ax.plot([0, 0], [0, 3.2], color=GREY, lw=0.9, ls=":")
    ax.annotate("", xy=(0, 3.0), xytext=(0, 2.6),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.3, mutation_scale=8))
    ax.text(0.08, 3.0, r"$\mathbf{B}$", fontsize=9, color=RED)
    ax.set_aspect("equal")
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(-0.7, 3.4)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("斜入射：螺旋线", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig17-1-cyclotron.png")


def fig17_2():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    ax.set_xlim(0, 6.4)
    ax.set_ylim(-1.6, 1.6)
    ax.axis("off")
    ax.grid(False)
    for y in (-1.0, 1.0):
        ax.plot([0.4, 5.6], [y, y], color=INK, lw=1.6)
    for x in np.linspace(1.2, 5.2, 6):
        ax.annotate("", xy=(x, 0.95), xytext=(x, -0.95),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.8, mutation_scale=6))
    ax.annotate("", xy=(5.2, 0.0), xytext=(0.5, 0.0),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.4, mutation_scale=8))
    ax.text(0.55, 0.16, "$v=E/B$", fontsize=8.5, color=ACCENT)
    ax.text(2.6, -1.45, "电场向下，磁场垂直纸面向里", fontsize=7.8, ha="center")
    ax.set_title("速度选择器", fontsize=8.8)

    ax = axes[1]
    ax.set_xlim(-3.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    ax.plot([-3.0, 0.0], [0, 0], color=ACCENT, lw=1.0, ls="--")
    for rr, lab, col in [(0.9, "$m_1$", BLUE), (1.5, "$m_2$", TEAL)]:
        th = np.linspace(np.pi / 2, -np.pi / 2, 200)
        ax.plot(rr * np.cos(th), rr * np.sin(th) + 0.0, color=col, lw=1.3)
        ax.text(0.1, -rr - 0.25, lab, fontsize=8.5, color=col)
    ax.text(-2.9, 0.15, "狭缝", fontsize=8)
    ax.set_title("质谱仪：$r\\propto\\sqrt{m/q}$", fontsize=8.6)
    fig.tight_layout()
    save(fig, "fig17-2-selector.png")


def fig17_3():
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.set_xlim(0, 6.6)
    ax.set_ylim(-1.8, 1.8)
    ax.axis("off")
    ax.grid(False)
    ax.add_patch(Rectangle((1.2, -0.8), 3.6, 1.6, facecolor="#f2f5f8",
                           edgecolor=INK, lw=1.0))
    ax.annotate("", xy=(5.2, 0.0), xytext=(0.4, 0.0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3, mutation_scale=8))
    ax.text(0.5, 0.15, "$I$", fontsize=9)
    for x in np.linspace(1.6, 4.4, 4):
        ax.annotate("", xy=(x, 0.42), xytext=(x, -0.42),
                    arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=0.9, mutation_scale=6))
    ax.text(2.0, 0.55, "$\\mathbf{v}_d$", fontsize=8.5, color=ACCENT)
    ax.text(3.0, 0.98, r"$\mathbf{B}$ 垂直纸面向外", fontsize=8, ha="center", color=BLUE)
    ax.annotate("", xy=(3.0, -0.85), xytext=(3.0, -1.35),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2, mutation_scale=8))
    ax.text(3.1, -1.45, "洛伦兹力使载流子偏向一侧", fontsize=7.8, color=RED)
    ax.plot([1.2, 1.2], [-0.8, 0.8], color=RED, lw=2.4)
    ax.plot([4.8, 4.8], [-0.8, 0.8], color=BLUE, lw=2.4)
    ax.text(1.0, 0.95, "$-$", fontsize=11, color=RED)
    ax.text(4.9, 0.95, "$+$", fontsize=11, color=BLUE)
    ax.text(3.0, -1.72, "$V_H=IB/(nqd)$", fontsize=8.5, ha="center")
    save(fig, "fig17-3-hall.png")


fig17_1()
fig17_2()
fig17_3()
