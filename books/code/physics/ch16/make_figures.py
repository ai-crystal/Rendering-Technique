import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Circle, FancyArrowPatch, Arc

D2R = np.pi / 180


def fig16_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    for ax, enclosed in zip(axes, [True, False]):
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.grid(False)
        ax.plot([0], [0], "o", ms=5, color=RED)
        ax.text(0.08, 0.08, "$I$", fontsize=9, color=RED)
        for rr in (0.25, 0.55):
            ax.add_patch(Circle((0, 0), rr, facecolor="none", edgecolor=SKY, lw=0.7))
        if enclosed:
            th = np.linspace(0, 2 * np.pi, 300)
            ax.plot(0.95 * np.cos(th), 0.95 * np.sin(th), color=BLUE, lw=1.5)
            ax.annotate("", xy=(0.95 * np.cos(0.2), 0.95 * np.sin(0.2)),
                        xytext=(0.95 * np.cos(-0.15), 0.95 * np.sin(-0.15)),
                        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.3, mutation_scale=8))
            ax.set_title(r"套住导线：$\oint\mathbf{B}\cdot d\mathbf{l}=\mu_0I$", fontsize=8.4)
        else:
            th = np.linspace(0, 2 * np.pi, 300)
            ax.plot(0.55 + 0.55 * np.cos(th), 0.35 * np.sin(th), color=ACCENT, lw=1.5)
            ax.annotate("", xy=(1.03, 0.16), xytext=(1.05, -0.10),
                        arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.3, mutation_scale=8))
            ax.set_title(r"不套住：环量为零", fontsize=8.4)
    fig.tight_layout()
    save(fig, "fig16-1-loop.png")


def fig16_2():
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.set_xlim(0, 8.2)
    ax.set_ylim(-1.4, 1.6)
    ax.axis("off")
    ax.grid(False)
    # 螺线管轮廓
    ax.add_patch(plt.Rectangle((1.0, -0.7), 6.0, 1.4, facecolor="#f4f7fa",
                               edgecolor=GREY, lw=1.0))
    for x in np.linspace(1.15, 6.85, 16):
        ax.plot([x, x], [-0.7, 0.7], color=ACCENT, lw=1.0)
    for y in (-0.35, 0.0, 0.35):
        ax.annotate("", xy=(6.65, y), xytext=(1.35, y),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.9, mutation_scale=6))
    # 回路
    ax.plot([2.0, 2.0, 7.2, 7.2, 2.0], [0.0, 1.15, 1.15, 0.0, 0.0],
            color=TEAL, lw=1.4, ls="--")
    ax.text(4.6, 1.22, "安培回路", fontsize=8, color=TEAL, ha="center")
    ax.plot([2.0, 7.2], [0.0, 0.0], color=TEAL, lw=1.0, ls=":")
    ax.text(4.4, -1.15, r"管内 $B=\mu_0 nI$，管外 $B=0$，回路包围 $nlI$",
            fontsize=8.2, ha="center")
    save(fig, "fig16-2-solenoid.png")


def fig16_3():
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.7))
    r = np.linspace(0.12, 3, 400)
    axes[0].plot(r, 1 / r, color=BLUE)
    axes[0].set_title("长直导线：$1/r$", fontsize=8.4)
    axes[0].set_xlabel("$r$")
    axes[0].set_ylabel("$B$（相对值）")

    a, b = 1.0, 1.6
    rr = np.linspace(a, b, 200)
    axes[1].plot(rr, np.full_like(rr, 1.0), color=BLUE)
    axes[1].axhline(0, color=GREY, lw=0.8)
    axes[1].set_xlim(0, 2.2)
    axes[1].set_ylim(0, 1.4)
    axes[1].set_title("长螺线管：管内均匀", fontsize=8.4)
    axes[1].set_xlabel("$r$")

    rr = np.linspace(a, b, 200)
    axes[2].plot(rr, 1 / rr, color=BLUE)
    axes[2].set_title("环形螺线管：$1/r$", fontsize=8.4)
    axes[2].set_xlabel("$r$")
    fig.tight_layout()
    save(fig, "fig16-3-compare.png")


fig16_1()
fig16_2()
fig16_3()
