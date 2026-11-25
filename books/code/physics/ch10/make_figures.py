import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Circle, FancyArrowPatch, Polygon

D2R = np.pi / 180


def fig10_1():
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.set_xlim(-0.6, 6.6)
    ax.set_ylim(-1.9, 1.9)
    ax.axis("off")
    ax.grid(False)
    ax.plot([0.5, 4.5], [1.0, 1.0], color=RED, lw=3.0, solid_capstyle="butt")
    ax.plot([0.5, 4.5], [-1.0, -1.0], color=BLUE, lw=3.0, solid_capstyle="butt")
    ax.text(2.5, 1.25, "$+Q$", ha="center", fontsize=9, color=RED)
    ax.text(2.5, -1.32, "$-Q$", ha="center", fontsize=9, color=BLUE)
    for x in np.linspace(1.0, 4.0, 7):
        ax.annotate("", xy=(x, -0.94), xytext=(x, 0.94),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=7))
    # 边缘场线
    for sgn in (1, -1):
        for k, (dx, dy) in enumerate([(0.55, 0.55), (0.85, 0.9), (1.05, 1.25)]):
            ax.annotate("", xy=(4.5 + dx * 0.55, sgn * (1.0 - dy * 0.75)),
                        xytext=(4.5, sgn * 1.0),
                        arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.7,
                                        connectionstyle="arc3,rad=-0.35", mutation_scale=6))
    ax.text(5.6, 0.55, "边缘效应", fontsize=8, color=GREY)
    ax.annotate("", xy=(2.5, -1.5), xytext=(2.5, -1.05),
                arrowprops=dict(arrowstyle="<|-|>", color=GREY, lw=0.8, mutation_scale=7))
    ax.text(2.6, -1.42, "$d$", fontsize=8.5, color=GREY)
    ax.annotate("", xy=(0.35, -1.0), xytext=(0.35, 1.0),
                arrowprops=dict(arrowstyle="<|-|>", color=GREY, lw=0.8, mutation_scale=7))
    ax.text(0.0, 0.0, "$U$", fontsize=8.5, color=GREY)
    ax.text(2.5, 1.62, "板间 $E=\\sigma/\\varepsilon_0$，两板外侧 $E=0$",
            ha="center", fontsize=8)
    save(fig, "fig10-1-parallel-plate.png")


def fig10_2():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    for ax, medium in zip(axes, [False, True]):
        ax.set_xlim(-0.6, 5.6)
        ax.set_ylim(-1.6, 1.6)
        ax.axis("off")
        ax.grid(False)
        ax.plot([0.4, 4.4], [1.0, 1.0], color=RED, lw=2.6)
        ax.plot([0.4, 4.4], [-1.0, -1.0], color=BLUE, lw=2.6)
        for x in np.linspace(0.9, 3.9, 5):
            ax.annotate("", xy=(x, -0.9), xytext=(x, 0.9),
                        arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=6))
        if medium:
            ax.add_patch(plt.Rectangle((0.45, -0.93), 3.9, 1.86,
                                       facecolor="#f6efdc", edgecolor="#d9c48a", lw=0.8, zorder=2))
            for x in np.linspace(1.28, 3.53, 4):
                for y in np.linspace(-0.55, 0.55, 3):
                    ax.add_patch(Circle((x, y + 0.075), 0.055, color=RED, zorder=4))
                    ax.add_patch(Circle((x, y - 0.075), 0.055, color=BLUE, zorder=4))
            ax.text(2.3, -1.38, "介质中 $E=E_0/\\varepsilon_r$", ha="center", fontsize=8)
            ax.set_title("插入介质后", fontsize=8.8)
        else:
            ax.text(2.3, -1.38, "真空中 $E_0=\\sigma/\\varepsilon_0$", ha="center", fontsize=8)
            ax.set_title("真空", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig10-2-dielectric.png")


def fig10_3():
    C = 1.0
    Q = 3.0
    q = np.linspace(0, Q, 200)
    fig, ax = plt.subplots(figsize=(5.8, 3.3))
    ax.plot(q, q / C, color=BLUE, label="$u=q/C$")
    ax.fill_between(q, 0, q / C, color=SKY, alpha=0.35, lw=0)
    ax.plot([Q], [Q / C], "o", color=ACCENT)
    ax.annotate("面积 $=\\frac{1}{2}QU$", (Q * 0.62, Q * 0.32 / C), fontsize=8.5, color=INK)
    edges = np.linspace(0, Q, 4)
    for a, b in zip(edges[:-1], edges[1:]):
        ax.plot([a, a, b], [a / C, b / C, b / C], color=ACCENT, lw=1.1)
    ax.set_xlabel("已充入的电荷 $q$")
    ax.set_ylabel("电压 $u$")
    ax.set_xlim(0, Q * 1.08)
    ax.set_ylim(0, Q / C * 1.12)
    ax.legend(loc="lower right", fontsize=8)
    ax.set_title("分步充电的梯形面积", fontsize=8.8)
    save(fig, "fig10-3-charging.png")


fig10_1()
fig10_2()
fig10_3()
