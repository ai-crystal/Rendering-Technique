import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Rectangle, FancyArrowPatch, Arc, Circle

D2R = np.pi / 180


def fig20_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    for ax, inserting in zip(axes, [True, False]):
        ax.set_xlim(0, 6)
        ax.set_ylim(-1.6, 1.9)
        ax.axis("off")
        ax.grid(False)
        # 线圈
        for x in np.linspace(2.4, 3.6, 6):
            ax.add_patch(Arc((x, 0), 0.55, 1.5, theta1=-90, theta2=90, color=ACCENT, lw=1.3))
        ax.add_patch(Rectangle((0.4, -0.28), 1.6, 0.56, facecolor="#e9edf1", edgecolor=INK))
        ax.add_patch(Rectangle((0.4, -0.28), 0.5, 0.56, facecolor="#c9504a", edgecolor=INK))
        ax.text(0.65, 0.0, "N", ha="center", va="center", fontsize=9, color="white")
        ax.text(1.75, 0.0, "S", ha="center", va="center", fontsize=9)
        if inserting:
            ax.annotate("", xy=(2.1, 0), xytext=(1.6, 0),
                        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4, mutation_scale=8))
            ax.text(1.5, 0.45, "$v$", fontsize=8.5, color=BLUE)
            ax.text(3.0, 1.55, "感应磁场反向，上端为 N", fontsize=7.8, ha="center", color=RED)
            ax.set_title("插入：磁通量增加", fontsize=8.6)
        else:
            ax.annotate("", xy=(0.9, 0), xytext=(1.45, 0),
                        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4, mutation_scale=8))
            ax.text(1.2, 0.45, "$v$", fontsize=8.5, color=BLUE)
            ax.text(3.0, 1.55, "感应磁场同向，上端为 S", fontsize=7.8, ha="center", color=BLUE)
            ax.set_title("拔出：磁通量减少", fontsize=8.6)
    fig.tight_layout()
    save(fig, "fig20-1-lenz.png")


def fig20_2():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1))
    ax = axes[0]
    ax.set_xlim(0, 6)
    ax.set_ylim(-1.6, 1.6)
    ax.axis("off")
    ax.grid(False)
    ax.add_patch(Rectangle((1.0, -1.0), 4.0, 2.0, facecolor="#eef1f4", edgecolor=INK))
    for r in (0.35, 0.6, 0.85):
        ax.add_patch(Arc((3.0 + 0.4, 0), 2 * r, 1.2 * r, theta1=-60, theta2=240,
                         color=RED, lw=1.1))
    ax.annotate("", xy=(2.3, 0.6), xytext=(2.6, 0.6),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4, mutation_scale=8))
    ax.text(2.35, 0.78, "$v$", fontsize=8.5, color=BLUE)
    ax.text(3.0, -1.35, "整块金属：涡流成环", fontsize=8, ha="center")
    ax.set_title("涡流与阻尼", fontsize=8.6)

    ax = axes[1]
    ax.set_xlim(0, 6)
    ax.set_ylim(-1.6, 1.6)
    ax.axis("off")
    ax.grid(False)
    for i in range(6):
        ax.add_patch(Rectangle((1.0 + i * 0.55, -1.0), 0.42, 2.0,
                               facecolor="#eef1f4", edgecolor=INK, lw=0.7))
    ax.plot([0.65, 5.6], [1.15, 1.15], color=RED, lw=1.6)
    ax.plot([0.65, 5.6], [-1.15, -1.15], color=RED, lw=1.6)
    ax.text(3.0, -1.35, "叠片铁芯：涡流被切断", fontsize=8, ha="center")
    ax.set_title("叠片", fontsize=8.6)
    fig.tight_layout()
    save(fig, "fig20-2-eddy.png")


def fig20_3():
    t = np.linspace(0, 2, 600)
    w = 2 * np.pi
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9))
    ax = axes[0]
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-0.9, 0.9)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    for y in np.linspace(-0.7, 0.7, 7):
        ax.annotate("", xy=(1.3, y), xytext=(-1.3, y),
                    arrowprops=dict(arrowstyle="-|>", color=SKY, lw=0.7, mutation_scale=5))
    th = 35 * D2R
    ax.add_patch(Rectangle((-0.55, -0.22), 1.1, 0.44,
                           facecolor="#f3e2c4", edgecolor=ACCENT, lw=1.4,
                           angle=35, rotation_point="center"))
    ax.set_title("线圈在磁场中转动", fontsize=8.6)

    ax = axes[1]
    ax.plot(t, np.cos(w * t), color=TEAL, label=r"$\Phi\propto\cos\omega t$")
    ax.plot(t, np.sin(w * t), color=ACCENT, label=r"$\mathcal{E}\propto\sin\omega t$")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("$t/T$")
    ax.legend(loc="upper right", fontsize=7.6)
    ax.set_title("磁通量与电动势", fontsize=8.6)
    fig.tight_layout()
    save(fig, "fig20-3-generator.png")


fig20_1()
fig20_2()
fig20_3()
