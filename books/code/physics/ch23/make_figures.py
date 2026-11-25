import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle


def fig23_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    ax = axes[0]
    x = np.linspace(-1.6, 1.6, 300)
    X, Y = np.meshgrid(x, x)
    phi = X ** 2 + Y ** 2
    cs = ax.contour(X, Y, phi, levels=[0.3, 0.8, 1.5, 2.4], colors=SKY, linewidths=0.9)
    for r in (0.55, 1.0, 1.5):
        for a in np.linspace(0, 2 * np.pi, 8, endpoint=False):
            ax.arrow(r * np.cos(a), r * np.sin(a), 0.12 * np.cos(a), 0.12 * np.sin(a),
                     head_width=0.06, color=BLUE, lw=0.8, length_includes_head=True)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.set_title(r"$\varphi=x^{2}+y^{2}$ 与 $\nabla\varphi$", fontsize=8.8)

    ax = axes[1]
    a = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(a), np.sin(a), color=GREY, lw=0.8)
    ax.annotate("", xy=(0.5, 0.866), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.5, mutation_scale=9))
    ax.text(0.52, 0.90, r"$\nabla\varphi$", fontsize=9, color=ACCENT)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.set_title("方向导数在梯度方向最大", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig23-1-gradient.png")


def fig23_2():
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6))
    x = np.linspace(-1, 1, 17)
    y = np.linspace(-1, 1, 17)
    X, Y = np.meshgrid(x, y)
    fields = [(X, Y, r"$\nabla\cdot\mathbf{A}>0$"),
              (-X, -Y, r"$\nabla\cdot\mathbf{A}<0$"),
              (np.ones_like(X), np.zeros_like(Y), r"$\nabla\cdot\mathbf{A}=0$")]
    for ax, (U, V, lab) in zip(axes, fields):
        ax.quiver(X, Y, U, V, color=BLUE, width=0.012)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_title(lab, fontsize=9)
    fig.tight_layout()
    save(fig, "fig23-2-divergence.png")


def fig23_3():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.add_patch(Rectangle((-0.45, -0.35), 0.9, 0.7, facecolor="#eef3f8",
                           edgecolor=ACCENT, lw=1.1))
    for (x0, y0), (dx, dy) in [((-0.45, 0), (0.9, 0)), ((0.45, 0), (0, 0.7)),
                               ((0.45, 0.35), (-0.9, 0)), ((-0.45, 0.35), (0, -0.7))]:
        ax.annotate("", xy=(x0 + dx, y0 + dy), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0, mutation_scale=7))
    ax.text(0.0, -0.62, r"$\oint\mathbf{A}\cdot d\mathbf{l}$", fontsize=9, ha="center")
    ax.axis("off")
    ax.grid(False)
    ax.set_title("小面元的环量", fontsize=8.8)

    ax = axes[1]
    th = np.linspace(0, 2 * np.pi, 400)
    for r in (0.35, 0.7, 1.05):
        ax.plot(r * np.cos(th), r * np.sin(th), color=SKY, lw=1.0)
        for a in np.linspace(0, 2 * np.pi, 6, endpoint=False):
            ax.arrow(r * np.cos(a), r * np.sin(a),
                     -0.10 * np.sin(a) * r, 0.10 * np.cos(a) * r,
                     head_width=0.05, color=BLUE, lw=0.8, length_includes_head=True)
    ax.set_aspect("equal")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("绕圈的场：旋度非零", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig23-3-curl.png")


fig23_1()
fig23_2()
fig23_3()
