import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Rectangle, FancyArrowPatch


def fig24_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    ax = axes[0]
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.2, 1.2)
    ax.plot([-1.5, 1.5], [0, 0], color=INK, lw=2.0)
    ax.add_patch(Rectangle((-0.55, -0.25), 1.1, 0.5, facecolor="#e9f0f7",
                           edgecolor=BLUE, lw=1.1, alpha=0.9))
    ax.annotate("", xy=(0, 0.45), xytext=(0, 0.15),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2, mutation_scale=7))
    ax.annotate("", xy=(0, -0.45), xytext=(0, -0.15),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2, mutation_scale=7))
    ax.text(0.62, 0.34, r"$\mathbf{n}$", fontsize=9, color=RED)
    ax.text(-0.5, -0.62, "介质 1", fontsize=8.5)
    ax.text(-0.5, 0.40, "介质 2", fontsize=8.5)
    ax.text(0.0, -0.95, r"$D_{2n}-D_{1n}=\sigma$，$B_{2n}=B_{1n}$",
            fontsize=8.5, ha="center")
    ax.axis("off")
    ax.grid(False)
    ax.set_title("扁药盒：法向分量", fontsize=8.8)

    ax = axes[1]
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.2, 1.2)
    ax.plot([-1.5, 1.5], [0, 0], color=INK, lw=2.0)
    ax.add_patch(Rectangle((-0.7, -0.10), 1.4, 0.20, facecolor="#fdf1e4",
                           edgecolor=ACCENT, lw=1.1))
    ax.annotate("", xy=(0.55, 0.05), xytext=(-0.55, 0.05),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.0, mutation_scale=7))
    ax.text(-0.0, -0.42, "小矩形回路", fontsize=8, ha="center", color=ACCENT)
    ax.text(0.0, -0.95, r"$E_{1t}=E_{2t}$，$H_{1t}-H_{2t}=K$",
            fontsize=8.5, ha="center")
    ax.axis("off")
    ax.grid(False)
    ax.set_title("小回路：切向分量", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig24-1-boundary.png")


def fig24_2():
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.grid(False)
    boxes = [
        (0.5, 3.6, "散度", r"$\nabla\cdot\mathbf{D}=\rho$", "电荷是源"),
        (5.3, 3.6, "散度", r"$\nabla\cdot\mathbf{B}=0$", "无磁单极"),
        (0.5, 1.0, "旋度", r"$\nabla\times\mathbf{E}=-\partial\mathbf{B}/\partial t$", "变化的磁场生电场"),
        (5.3, 1.0, "旋度", r"$\nabla\times\mathbf{H}=\mathbf{J}+\partial\mathbf{D}/\partial t$", "电流与变化电场生磁场"),
    ]
    for x, y, tag, eq, note in boxes:
        ax.add_patch(plt.Rectangle((x, y), 4.2, 1.9, facecolor="#f6f8fb",
                                   edgecolor=GREY, lw=0.9))
        ax.text(x + 0.15, y + 1.62, tag, fontsize=8, color=GREY)
        ax.text(x + 2.1, y + 1.05, eq, fontsize=10, ha="center")
        ax.text(x + 2.1, y + 0.45, note, fontsize=7.8, ha="center", color=INK)
    ax.text(5.0, 6.15, "箭头表示时间导数把两组方程耦合起来", fontsize=7.6,
            ha="center", color=BLUE)
    ax.annotate("", xy=(5.3, 5.5), xytext=(4.7, 5.5),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.1, mutation_scale=8))
    ax.annotate("", xy=(4.7, 2.9), xytext=(5.3, 2.9),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.1, mutation_scale=8))
    save(fig, "fig24-2-structure.png")


fig24_1()
fig24_2()
