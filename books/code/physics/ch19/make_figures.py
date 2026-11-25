import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle

D2R = np.pi / 180


def fig19_1():
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.set_xlim(0, 7.2)
    ax.set_ylim(-0.7, 2.9)
    ax.axis("off")
    ax.grid(False)
    # 导轨
    ax.plot([0.8, 0.8], [0.4, 2.2], color=INK, lw=1.6)
    ax.plot([0.8, 5.6], [2.2, 2.2], color=INK, lw=1.4)
    ax.plot([0.8, 5.6], [0.4, 0.4], color=INK, lw=1.4)
    # 棒
    ax.plot([3.6, 3.6], [0.4, 2.2], color=ACCENT, lw=3.0)
    ax.annotate("", xy=(4.6, 1.3), xytext=(3.7, 1.3),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.5, mutation_scale=9))
    ax.text(4.2, 1.45, "$v$", fontsize=9, color=BLUE)
    # 磁场符号
    for x in np.linspace(1.2, 5.2, 5):
        for y in (0.85, 1.75):
            ax.plot([x], [y], "x", color=GREY, ms=5)
    ax.text(5.35, 2.35, "$\\mathbf{B}$（向纸内）", fontsize=8, color=GREY)
    # 电荷分离
    ax.plot([3.6], [2.05], "+", color=RED, ms=8)
    ax.plot([3.6], [0.55], "-", color=BLUE, ms=8)
    ax.annotate("$+$", (3.68, 2.0), fontsize=10, color=RED)
    ax.annotate("$-$", (3.68, 0.50), fontsize=10, color=BLUE)
    ax.text(2.1, -0.35, r"$\mathcal{E}=Blv$", fontsize=9, color=INK)
    save(fig, "fig19-1-motional.png")


def fig19_2():
    t = np.linspace(0, 2, 600)
    w = 2 * np.pi
    Phi = np.cos(w * t)
    emf = np.sin(w * t)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9))
    ax = axes[0]
    ax.plot(t, Phi, color=TEAL)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("$t/T$")
    ax.set_ylabel(r"$\Phi/(B_0S)$")
    ax.set_title("磁通量", fontsize=8.8)
    ax = axes[1]
    ax.plot(t, emf, color=ACCENT)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("$t/T$")
    ax.set_ylabel(r"$\mathcal{E}/(B_0S\omega)$")
    ax.set_title("感应电动势", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig19-2-sine.png")


def fig19_3():
    R = 1.0
    r = np.linspace(0, 3.2, 500)
    E = np.where(r < R, r, 1.0 / np.maximum(r, 1e-9))
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    ax.plot(r, E, color=BLUE)
    ax.axvline(R, color=GREY, ls=":", lw=0.9)
    ax.text(1.06, 0.9, "$r=R$", fontsize=8, color=GREY)
    ax.text(0.15, 0.62, "管内线性", fontsize=8, color=BLUE)
    ax.text(1.45, 0.5, "管外 $1/r$", fontsize=8, color=BLUE)
    ax.set_xlabel("到轴线的距离 $r$")
    ax.set_ylabel("$E$（相对单位）")
    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 1.1)
    ax.set_title("涡旋电场的大小", fontsize=8.8)

    ax = axes[1]
    ax.set_aspect("equal")
    ax.add_patch(plt.Circle((0, 0), R, facecolor="#eef3f8", edgecolor=GREY, lw=1.0))
    for rr in (0.35, 0.65, 0.95, 1.3, 1.7):
        th = np.linspace(0, 2 * np.pi, 300)
        ax.plot(rr * np.cos(th), rr * np.sin(th), color=SKY, lw=0.8)
        for a in np.linspace(0, 2 * np.pi, 4, endpoint=False):
            ax.arrow(rr * np.cos(a), rr * np.sin(a), -0.10 * rr * np.sin(a),
                     0.10 * rr * np.cos(a), head_width=0.05, color=BLUE, lw=0.7,
                     length_includes_head=True)
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-1.9, 1.9)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("场线闭合，绕轴成圈", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig19-3-vortex.png")


fig19_1()
fig19_2()
fig19_3()
