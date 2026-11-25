import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def fig26_1():
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.1)
    ax.axis("off")
    ax.grid(False)
    boxes = [
        (0.4, 3.4, [r"$\nabla\cdot\mathbf{E}=\rho/\varepsilon_0$"], "电荷是源"),
        (0.4, 1.0, [r"$\nabla\times\mathbf{E}=-\partial\mathbf{B}/\partial t$"], "变化的磁场生电场"),
        (5.4, 3.4, [r"$\nabla\cdot\mathbf{B}=0$"], "无磁单极"),
        (5.4, 1.0, [r"$\nabla\times\mathbf{B}=\mu_0\mathbf{J}$",
                    r"$+\ \mu_0\varepsilon_0\,\partial\mathbf{E}/\partial t$"], "电流与变化电场生磁场"),
    ]
    for x, y, lines, note in boxes:
        ax.add_patch(FancyBboxPatch((x, y), 4.2, 1.75, boxstyle="round,pad=0.08",
                                    facecolor="#f6f8fb", edgecolor=GREY, lw=0.9))
        if len(lines) == 1:
            ax.text(x + 2.1, y + 1.12, lines[0], fontsize=10.5, ha="center")
        else:
            ax.text(x + 2.1, y + 1.25, lines[0], fontsize=10.5, ha="center")
            ax.text(x + 2.1, y + 0.85, lines[1], fontsize=9, ha="center")
        ax.text(x + 2.1, y + 0.38, note, fontsize=7.8, ha="center", color=GREY)

    ax.add_patch(FancyArrowPatch((2.5, 3.35), (2.5, 2.85), arrowstyle="-|>",
                                 mutation_scale=10, color=BLUE, lw=1.1))
    ax.add_patch(FancyArrowPatch((2.5, 2.80), (7.5, 2.80), arrowstyle="-|>",
                                 mutation_scale=10, color=BLUE, lw=1.1,
                                 connectionstyle="arc3,rad=-0.22"))
    ax.add_patch(FancyArrowPatch((7.5, 2.85), (7.5, 3.35), arrowstyle="-|>",
                                 mutation_scale=10, color=BLUE, lw=1.1))
    ax.text(5.0, 5.85, "两个旋度方程通过时间导数互相激发", fontsize=8.4,
            ha="center", color=BLUE)
    save(fig, "fig26-1-equations.png")


def fig26_2():
    events = [
        (1785, "库仑扭秤", 1), (1820, "奥斯特实验", -1), (1827, "欧姆定律", 1),
        (1831, "法拉第感应", -1), (1865, "麦克斯韦方程", 1),
        (1888, "赫兹验证", -1),
    ]
    fig, ax = plt.subplots(figsize=(7.0, 2.8))
    ax.set_xlim(1775, 1900)
    ax.set_ylim(-1.6, 1.6)
    ax.plot([1785, 1888], [0, 0], color=INK, lw=1.4)
    for x, lab, side in events:
        ax.plot([x, x], [0, 0.18 * side], color=ACCENT, lw=1.0)
        ax.plot([x], [0], "o", ms=5, color=ACCENT)
        ax.text(x, 0.30 * side, lab, ha="center",
                va="bottom" if side > 0 else "top", fontsize=8)
        ax.text(x, 0.55 * side, str(x), ha="center",
                va="bottom" if side > 0 else "top", fontsize=7.2, color=GREY)
    ax.set_yticks([])
    ax.set_xticks([1780, 1800, 1820, 1840, 1860, 1880, 1900])
    ax.grid(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlabel("年份")
    save(fig, "fig26-2-history.png")


fig26_1()
fig26_2()
