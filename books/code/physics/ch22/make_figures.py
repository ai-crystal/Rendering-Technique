import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Rectangle


def fig22_1():
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.set_xlim(-0.3, 5.9)
    ax.set_ylim(-0.7, 3.6)
    ax.axis("off")
    ax.grid(False)
    s = 1.1
    for i in range(2):
        for j in range(2):
            x, y = 0.8 + i * s, 0.5 + j * s
            ax.add_patch(Rectangle((x, y), s, s, facecolor="#f2f6fa",
                                   edgecolor=INK, lw=0.9))
    ax.plot([0.8 + s, 0.8 + s], [0.5, 0.5 + 2 * s], color=ACCENT, lw=2.4)
    ax.plot([0.8, 0.8 + 2 * s], [0.5 + s, 0.5 + s], color=ACCENT, lw=2.4)
    ax.text(0.8 + s + 0.14, 0.5 + 1.42, "共享面", fontsize=7.6, color=ACCENT)
    ax.text(0.8 + s + 0.14, 0.5 + 1.22, "通量抵消", fontsize=7.6, color=ACCENT)
    for x in (1.0, 2.2):
        for y in (0.7, 1.9):
            ax.annotate("", xy=(x + 0.42, y + 0.42), xytext=(x, y),
                        arrowprops=dict(arrowstyle="-|>", color=SKY, lw=0.7, mutation_scale=5))
    ax.text(1.9, 3.25, "内部面两两抵消，只剩外表面", fontsize=8.4, ha="center")
    ax.text(3.7, 1.75, r"$\int_V \nabla\cdot\mathbf{A}\,dV$", fontsize=10, ha="left")
    ax.text(3.7, 1.20, r"$=\oint_S \mathbf{A}\cdot d\mathbf{S}$", fontsize=10, ha="left")
    ax.text(1.9, 0.1, "（为看清，把小块压成方格）", fontsize=7.2, ha="center", color=GREY)
    save(fig, "fig22-1-cube.png")


def fig22_2():
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.set_xlim(-0.3, 5.9)
    ax.set_ylim(-0.7, 3.6)
    ax.axis("off")
    ax.grid(False)
    n = 3
    s = 1.0
    for i in range(n):
        for j in range(n):
            x, y = 0.7 + i * s, 0.5 + j * s
            ax.add_patch(Rectangle((x, y), s, s, facecolor="none", edgecolor=GREY, lw=0.7))
            ax.annotate("", xy=(x + 0.75, y + 0.5), xytext=(x + 0.25, y + 0.5),
                        arrowprops=dict(arrowstyle="-|>", color=SKY, lw=0.8, mutation_scale=6))
    ax.add_patch(Rectangle((0.7, 0.5), 3 * s, 3 * s, facecolor="none",
                           edgecolor=ACCENT, lw=2.0))
    ax.text(2.2, 3.25, "内部边成对抵消，只剩外边界", fontsize=8.4, ha="center", color=ACCENT)
    ax.text(0.7, -0.35, r"$\int_S(\nabla\times\mathbf{A})\cdot d\mathbf{S}=\oint_L\mathbf{A}\cdot d\mathbf{l}$",
            fontsize=9.5)
    save(fig, "fig22-2-loop.png")


def fig22_3():
    x = np.linspace(-1.2, 1.2, 20)
    y = np.linspace(-1.2, 1.2, 20)
    X, Y = np.meshgrid(x, y)
    fig, axes = plt.subplots(2, 2, figsize=(6.2, 5.0))
    cases = [
        (-X, -Y, "无源无旋", r"$\mathbf{A}=\nabla\varphi$"),
        (-Y, X, "无源有旋", r"$\nabla\times\mathbf{A}\neq0$"),
        (X, Y, "有源无旋", r"$\nabla\cdot\mathbf{A}\neq0$"),
        (X - Y, Y + X, "有源有旋", "两者都不为零"),
    ]
    for ax, (U, V, title, note) in zip(axes.ravel(), cases):
        ax.quiver(X, Y, U, V, color=BLUE, width=0.006)
        ax.set_title(title, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.55, 1.4)
        ax.grid(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.text(0.0, -1.48, note, fontsize=7.6, ha="center", color=GREY)
    fig.tight_layout()
    save(fig, "fig22-3-types.png")


fig22_1()
fig22_2()
fig22_3()
