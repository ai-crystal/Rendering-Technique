import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import FancyArrowPatch


def arr3(ax, origin, vec, color, label=None, lw=1.6, off=(0.05, 0.05)):
    ax.add_patch(FancyArrowPatch(origin, (origin[0] + vec[0], origin[1] + vec[1]),
                                 arrowstyle="-|>", mutation_scale=10, color=color,
                                 lw=lw, shrinkA=0, shrinkB=0))
    if label:
        ax.text(origin[0] + vec[0] + off[0], origin[1] + vec[1] + off[1], label,
                color=color, fontsize=9)


def fig14_1():
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.set_xlim(-1.6, 2.0)
    ax.set_ylim(-0.6, 1.9)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    # 坐标：x 向右，y 向上，z 用斜向表示
    origin = (0, 0)
    arr3(ax, origin, (1.3, 0), BLUE, r"$\mathbf{v}$")
    arr3(ax, origin, (0, 1.4), TEAL, r"$\mathbf{B}$")
    arr3(ax, origin, (0.55, -0.85), RED, r"$\mathbf{F}=q\mathbf{v}\times\mathbf{B}$")
    ax.plot([0, 0.55], [0, -0.85], color=LIGHT, lw=0.7, ls=":")
    ax.plot([1.3, 0.55], [0, -0.85], color=LIGHT, lw=0.7, ls=":")
    ax.plot([0, 1.3], [1.4, 1.4], color=LIGHT, lw=0.7, ls=":")
    ax.text(-0.1, -0.12, "$q>0$", fontsize=9, color=INK, ha="right")
    ax.annotate("$\\mathbf{v}\\parallel\\mathbf{B}$ 时 $F=0$", (-1.4, 1.55), fontsize=8.5,
                color=GREY)
    ax.set_title("洛伦兹力的方向", fontsize=9)
    save(fig, "fig14-1-lorentz.png")


def fig14_2():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    for y in np.linspace(0.4, 4.4, 9):
        ax.annotate("", xy=(5.4, y), xytext=(0.2, y),
                    arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=0.7, mutation_scale=6))
    for x0, ang, lab in [(1.4, 0, r"$\theta=0$"), (3.0, 50, r"$\theta=50^\circ$"),
                         (4.5, 75, r"$\theta=75^\circ$")]:
        L = 1.6
        dx, dy = L * np.sin(ang * np.pi / 180) / 2, L * np.cos(ang * np.pi / 180) / 2
        ax.plot([x0 - dx, x0 + dx], [2.4 - dy, 2.4 + dy], color=ACCENT, lw=2.0)
        ax.text(x0, 0.95, lab, ha="center", fontsize=7.8)
    ax.set_xlim(0, 5.6)
    ax.set_ylim(0.6, 4.8)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("磁通量随倾角变化", fontsize=8.8)

    ax = axes[1]
    th = np.linspace(0, 90, 200)
    ax.plot(th, np.cos(th * np.pi / 180), color=TEAL)
    ax.set_xlabel(r"法线与 $\mathbf{B}$ 的夹角 $\theta$（度）")
    ax.set_ylabel(r"$\Phi/(BS)$")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.05)
    ax.set_title("余弦关系", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig14-2-flux.png")


def fig14_3():
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    th = np.linspace(0.001, np.pi - 0.001, 700)
    for R in (0.30, 0.50, 0.75, 1.05, 1.45, 2.0):
        r = R * np.sin(th) ** 2
        x = r * np.sin(th)
        z = r * np.cos(th)
        keep = (np.abs(x) < 2.2) & (np.abs(z) < 1.9)
        inside = (np.abs(x) < 0.26) & (np.abs(z) < 0.62)
        x = np.where(inside, np.nan, x)
        z = np.where(inside, np.nan, z)
        ax.plot(x[keep], z[keep], color=TEAL, lw=0.8)
        ax.plot(-x[keep], z[keep], color=TEAL, lw=0.8)
    # 磁铁
    ax.add_patch(plt.Rectangle((-0.22, -0.55), 0.44, 1.1, facecolor="#e8ecef",
                               edgecolor=INK, lw=1.0))
    ax.add_patch(plt.Rectangle((-0.22, 0.0), 0.44, 0.55, facecolor="#c9504a",
                               edgecolor=INK, lw=1.0))
    ax.text(0, 0.74, "N", ha="center", fontsize=9, color=INK)
    ax.text(0, -0.72, "S", ha="center", fontsize=9, color=INK)
    ax.set_xlim(-2.25, 2.25)
    ax.set_ylim(-1.95, 1.95)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    ax.set_title("条形磁铁的磁感线（偶极场，$r=R\\sin^{2}\\theta$）", fontsize=8.8)
    save(fig, "fig14-3-bar-magnet.png")


def fig14_4():
    items = [
        (1e-10, "星际空间", 1),
        (5e-5, "地磁场", -1),
        (0.5, "永磁体", 1),
        (3.0, "核磁共振", -1),
        (20.0, "超导磁体", 1),
        (1e8, "中子星表面", -1),
    ]
    fig, ax = plt.subplots(figsize=(6.8, 2.3))
    ax.set_xscale("log")
    ax.set_xlim(1e-11, 1e10)
    ax.set_ylim(-1, 1)
    ax.axhline(0, color=INK, lw=1.1)
    for x, name, side in items:
        ax.plot([x], [0], "o", ms=5, color=TEAL, zorder=3)
        ax.plot([x, x], [0, 0.14 * side], color=TEAL, lw=0.9)
        ax.text(x, 0.20 * side, name, ha="center",
                va="bottom" if side > 0 else "top", fontsize=8, color=INK)
        ax.text(x, 0.37 * side, f"$10^{{{int(np.log10(x))}}}$", ha="center",
                va="bottom" if side > 0 else "top", fontsize=7.2, color=GREY)
    ax.set_yticks([])
    ax.set_xlabel("磁感应强度（T，对数坐标）")
    ax.spines["left"].set_visible(False)
    ax.grid(False)
    save(fig, "fig14-4-scale.png")


fig14_1()
fig14_2()
fig14_3()
fig14_4()
