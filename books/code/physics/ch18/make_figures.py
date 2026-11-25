import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


def fig18_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1))
    rng = np.random.default_rng(3)
    for ax, ordered in zip(axes, [False, True]):
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 3.4)
        ax.axis("off")
        ax.grid(False)
        ax.add_patch(Rectangle((0.5, 0.3), 5.0, 2.8, facecolor="#f5f7fa",
                               edgecolor=INK, lw=1.0))
        xs = np.linspace(1.0, 5.0, 5)
        ys = np.linspace(0.85, 2.55, 3)
        for x in xs:
            for y in ys:
                if ordered:
                    ang = 0.0
                else:
                    ang = rng.uniform(0, np.pi)
                dx, dy = 0.20 * np.cos(ang), 0.20 * np.sin(ang)
                ax.annotate("", xy=(x + dx, y + dy), xytext=(x - dx, y - dy),
                            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0,
                                            mutation_scale=6))
        if ordered:
            ax.annotate("", xy=(5.75, 1.7), xytext=(5.55, 1.7),
                        arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.6, mutation_scale=8))
            ax.text(5.0, 0.42, "表面磁化电流", fontsize=7.8, color=ACCENT, ha="center")
            ax.set_title("磁化后：磁矩转向", fontsize=8.6)
        else:
            ax.set_title("无外场：磁矩杂乱", fontsize=8.6)

    fig.tight_layout()
    save(fig, "fig18-1-domains.png")


def fig18_2():
    H = np.linspace(-3, 3, 600)
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.plot(H, -1e-3 * H, color=BLUE, label="抗磁（$\\chi_m<0$）")
    ax.plot(H, 2e-3 * H, color=TEAL, label="顺磁（$\\chi_m>0$）")
    ax.plot(H, np.tanh(2.2 * H), color=ACCENT, lw=1.8, label="铁磁")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.axvline(0, color=GREY, lw=0.8)
    ax.set_xlabel("$H$（相对单位）")
    ax.set_ylabel("$M$（相对单位）")
    ax.set_ylim(-1.4, 1.4)
    ax.legend(loc="lower right", fontsize=7.6)
    ax.set_title("三种磁性的磁化曲线", fontsize=8.8)
    save(fig, "fig18-2-types.png")


def fig18_3():
    Hc, Br, Bs = 1.0, 1.2, 1.8
    t = np.linspace(-8, 8, 2000)
    # 简化模型：上升支与下降支用平移的双曲正切
    up = Bs * np.tanh((t + Hc) * 1.1)
    down = Bs * np.tanh((t - Hc) * 1.1)
    fig, ax = plt.subplots(figsize=(5.8, 3.4))
    ax.plot(t, down, color=BLUE, label="下降支")
    ax.plot(t, up, color=ACCENT, label="上升支")
    ax.annotate("", xy=(2.6, 1.75), xytext=(1.9, 1.78),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.9, mutation_scale=7))
    ax.annotate("", xy=(-2.4, -1.55), xytext=(-1.8, -1.45),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.9, mutation_scale=7))
    ax.axhline(0, color=GREY, lw=0.8)
    ax.axvline(0, color=GREY, lw=0.8)
    ax.plot([0], [Bs * np.tanh(Hc * 1.1)], "o", ms=4, color=INK)
    ax.annotate("$B_r$", (0, Bs * np.tanh(Hc * 1.1)), xytext=(0.18, 0.95),
                fontsize=8.5, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.plot([-Hc], [0], "o", ms=4, color=INK)
    ax.annotate("$-H_c$", (-Hc, 0), xytext=(-1.5, -0.35), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.set_xlabel("$H$（相对单位）")
    ax.set_ylabel("$B$（相对单位）")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-2.1, 2.1)
    ax.legend(loc="lower right", fontsize=7.8)
    ax.set_title("磁滞回线（简化模型）", fontsize=8.8)
    save(fig, "fig18-3-hysteresis.png")


fig18_1()
fig18_2()
fig18_3()
