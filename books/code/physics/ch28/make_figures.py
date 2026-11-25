import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import FancyBboxPatch


def fig28_1():
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.grid(False)
    ax.text(2.6, 5.55, "SI", fontsize=10, ha="center", color=BLUE, fontweight="bold")
    ax.text(7.4, 5.55, "高斯制", fontsize=10, ha="center", color=ACCENT, fontweight="bold")
    rows = [
        (r"$F=\dfrac{q_1q_2}{4\pi\varepsilon_0r^{2}}$", r"$F=\dfrac{q_1q_2}{r^{2}}$"),
        (r"$\nabla\cdot\mathbf{E}=\rho/\varepsilon_0$", r"$\nabla\cdot\mathbf{E}=4\pi\rho$"),
        (r"$\nabla\times\mathbf{B}=\mu_0\mathbf{J}+\mu_0\varepsilon_0\dot{\mathbf{E}}$",
         r"$\nabla\times\mathbf{B}=\dfrac{4\pi}{c}\mathbf{J}+\dfrac{1}{c}\dot{\mathbf{E}}$"),
        ("电荷：库仑（独立单位）", "电荷：statC（由力学导出）"),
        (r"$E$：V/m，$B$：T（量纲不同）", r"$E$ 与 $B$ 量纲相同"),
    ]
    ys = [4.5, 3.6, 2.7, 1.65, 0.75]
    for (l, r), y in zip(rows, ys):
        ax.text(2.6, y, l, fontsize=9, ha="center")
        ax.text(7.4, y, r, fontsize=9, ha="center")
    ax.plot([5.0, 5.0], [0.3, 5.15], color=GREY, lw=0.8, ls=":")
    save(fig, "fig28-1-units.png")


def fig28_2():
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.set_xlim(-1.4, 4.4)
    ax.set_ylim(-1.5, 2.0)
    ax.axis("off")
    ax.grid(False)
    ax.plot([0, 4.2], [0, 0], color=INK, lw=2.0)
    ax.add_patch(plt.Rectangle((0, 0), 1.8, 1.9, facecolor="#f2f6fa", alpha=0.5, lw=0))
    ax.add_patch(plt.Rectangle((1.8, 0), 2.3, 1.9, facecolor="#fdf4e6", alpha=0.6, lw=0))
    ax.text(0.35, 1.62, "介质 1（$n_1$）", fontsize=8)
    ax.text(2.2, 1.62, "介质 2（$n_2$）", fontsize=8)
    ax.annotate("", xy=(1.8, 0), xytext=(0.7, 1.3),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4, mutation_scale=8))
    ax.annotate("", xy=(2.55, 1.15), xytext=(1.8, 0),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.4, mutation_scale=8))
    ax.annotate("", xy=(1.05, 1.15), xytext=(1.8, 0),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.2, mutation_scale=8))
    ax.text(0.55, 1.42, "入射", fontsize=7.6, color=BLUE)
    ax.text(2.62, 1.10, "折射", fontsize=7.6, color=ACCENT)
    ax.text(0.62, 1.02, "反射", fontsize=7.6, color=TEAL)
    ax.plot([1.8, 1.8], [-0.2, 1.45], color=GREY, lw=0.8, ls=":")
    ax.text(1.55, 1.40, r"$\theta_1$", fontsize=8)
    ax.text(1.90, 0.55, r"$\theta_2$", fontsize=8)
    ax.text(1.0, -0.95, r"$n_1\sin\theta_1=n_2\sin\theta_2$", fontsize=9, ha="center")
    ax.text(3.5, -0.35, r"$E_{t}$、$B_{n}$ 连续", fontsize=7.8, color=GREY)
    save(fig, "fig28-2-interface.png")


fig28_1()
fig28_2()
