import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Wedge

D2R = np.pi / 180


def fig7_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    ax = axes[0]
    for y in np.linspace(0.4, 4.6, 9):
        ax.annotate("", xy=(6.2, y), xytext=(0.2, y),
                    arrowprops=dict(arrowstyle="-|>", color=SKY, lw=0.8, mutation_scale=6))
    for x0, ang, lab in [(1.6, 0, r"$\theta=0$"), (3.3, 45, r"$\theta=45^\circ$"),
                         (5.0, 70, r"$\theta=70^\circ$")]:
        L = 1.7
        dx, dy = L * np.sin(ang * D2R) / 2, L * np.cos(ang * D2R) / 2
        ax.plot([x0 - dx, x0 + dx], [2.5 - dy, 2.5 + dy], color=ACCENT, lw=2.2)
        ax.text(x0, 1.05, lab, ha="center", fontsize=8)
    ax.set_xlim(0, 6.4)
    ax.set_ylim(0.6, 5.0)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("同一束场线穿过不同倾角的面", fontsize=8.8)

    ax = axes[1]
    th = np.linspace(0, 90, 200)
    ax.plot(th, np.cos(th * D2R), color=BLUE)
    ax.set_xlabel(r"面元法线与场的夹角 $\theta$（度）")
    ax.set_ylabel(r"$\Phi/(E\,dS)=\cos\theta$")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.05)
    for t in (0, 45, 70):
        ax.plot([t], [np.cos(t * D2R)], "o", ms=4, color=ACCENT)
    ax.set_title("通量按余弦衰减", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig7-1-flux.png")


def fig7_2():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.4))
    ax = axes[0]
    ax.set_aspect("equal")
    ax.add_patch(Circle((0, 0), 1.0, facecolor="none", edgecolor=GREY, lw=1.2))
    ax.plot([0.35], [0.15], "o", color=RED, ms=6)
    ax.text(0.42, 0.22, "$Q$", fontsize=9, color=RED)
    for a in np.arange(10, 360, 40):
        ar = a * D2R
        ax.annotate("", xy=(0.98 * np.cos(ar), 0.98 * np.sin(ar)),
                    xytext=(0.36 + 0.1 * np.cos(ar), 0.16 + 0.1 * np.sin(ar)),
                    arrowprops=dict(arrowstyle="-|>", color=SKY, lw=0.7, mutation_scale=5))
    ax.plot([0.35, 1.0], [0.15, 0.15], color=LIGHT, ls=":", lw=0.8)
    ax.text(0.55, 0.03, "$r$", fontsize=8, color=GREY)
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("电荷不在球心，通量仍是 $Q/\\varepsilon_0$", fontsize=8.4)

    ax = axes[1]
    ax.set_aspect("equal")
    th = np.linspace(0, 2 * np.pi, 400)
    rr = 1.0 + 0.22 * np.sin(3 * th) + 0.10 * np.cos(5 * th)
    ax.plot(rr * np.cos(th), rr * np.sin(th), color=GREY, lw=1.2)
    ax.plot([0.15], [0.10], "o", color=RED, ms=6)
    ax.text(0.22, 0.16, "$Q$", fontsize=9, color=RED)
    ax.plot([0.15, 1.45], [0.10, 0.42], color=SKY, lw=0.7)
    ax.plot([0.15, -1.3], [0.10, 1.05], color=SKY, lw=0.7)
    ax.annotate("", xy=(1.36, 0.40), xytext=(1.10, 0.32),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0, mutation_scale=7))
    ax.text(1.18, 0.50, "出", fontsize=8, color=BLUE)
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.45, 1.45)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("任意闭合曲面，内部电荷的线只出不回", fontsize=8.4)
    fig.tight_layout()
    save(fig, "fig7-2-solid-angle.png")


def fig7_3():
    R = 1.0
    r = np.linspace(0.02, 3.0, 800)
    shell = np.where(r < R, 0.0, 1.0 / r ** 2)
    solid = np.where(r < R, r / R ** 3, 1.0 / r ** 2)
    fig, ax = plt.subplots(figsize=(6.3, 3.2))
    ax.plot(r, shell, color=BLUE, label="带电球壳")
    ax.plot(r, solid, color=ACCENT, ls="--", label="均匀带电实心球")
    ax.axvline(R, color=GREY, ls=":", lw=0.9)
    ax.text(R + 0.04, 0.86, "$r=R$", fontsize=8, color=GREY)
    ax.annotate("壳内 $E=0$", (0.5, 0.03), xytext=(0.45, 0.30), fontsize=8,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.set_xlabel("距离 $r$（以 $R$ 为单位）")
    ax.set_ylabel(r"$E$（以 $kQ/R^{2}$ 为单位）")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1.1)
    ax.legend(loc="upper right", fontsize=8)
    save(fig, "fig7-3-spherical.png")


fig7_1()
fig7_2()
fig7_3()
