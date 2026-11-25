import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *

D2R = np.pi / 180


def fig2_1():
    t = np.linspace(0, 3, 400)
    x = 5 * t ** 2
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(t, x, color=BLUE, label=r"$x=5t^{2}$")
    for h, col, ls in [(1.0, GREY, "--"), (0.5, TEAL, "-."), (0.1, ACCENT, ":")]:
        slope = (5 * (2 + h) ** 2 - 20) / h
        tt = np.array([2, 2 + h])
        ax.plot(tt, 20 + slope * (tt - 2), color=col, ls=ls, lw=1.2,
                label=f"割线 $h={h:g}$，斜率 {slope:.1f}")
    ttan = np.array([1.65, 2.45])
    ax.plot(ttan, 20 + 20 * (ttan - 2), color=RED, lw=2.0, label="切线，斜率 20")
    ax.plot([2], [20], "o", color=INK, ms=5)
    ax.set_xlabel("时间 $t$（s）")
    ax.set_ylabel("位置 $x$（m）")
    ax.set_xlim(1.4, 3.0)
    ax.set_ylim(8, 46)
    ax.legend(loc="upper left", fontsize=7.2)
    save(fig, "fig2-1-secant.png")


def fig2_2():
    f = lambda t: 2 + 3 * t
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.8), sharey=True)
    tt = np.linspace(0, 2, 300)
    for ax, n in zip(axes, (4, 8, 32)):
        edges = np.linspace(0, 2, n + 1)
        for a, b in zip(edges[:-1], edges[1:]):
            ax.add_patch(plt.Rectangle((a, 0), b - a, f(a), facecolor=SKY,
                                       edgecolor="white", alpha=0.55, lw=0.5))
        approx = float(np.sum(f(edges[:-1]) * np.diff(edges)))
        ax.plot(tt, f(tt), color=RED, lw=1.6)
        ax.set_title(f"$n={n}$，面积 $\\approx${approx:.2f}", fontsize=8.5)
        ax.set_xlabel("$t$（s）")
        ax.set_xlim(0, 2)
        ax.set_ylim(0, 9)
        ax.set_xticks([0, 1, 2])
    axes[0].set_ylabel("$v$（m/s）")
    fig.tight_layout()
    save(fig, "fig2-2-riemann.png")


def fig2_3():
    v0, g = 20.0, 9.81
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for th in (15, 30, 45, 60, 75):
        T = 2 * v0 * np.sin(th * D2R) / g
        t = np.linspace(0, T, 300)
        x = v0 * np.cos(th * D2R) * t
        y = v0 * np.sin(th * D2R) * t - 0.5 * g * t ** 2
        ax.plot(x, y, lw=1.5, label=f"{th}°，射程 {x[-1]:.1f} m")
    ax.set_xlabel("水平距离 $x$（m）")
    ax.set_ylabel("高度 $y$（m）")
    ax.set_xlim(0, 44)
    ax.set_ylim(0, 22)
    ax.legend(loc="upper right", fontsize=7.2, ncol=1)
    ax.text(0.02, 0.96, r"$v_0=20\ \mathrm{m\,s^{-1}}$，忽略空气阻力",
            transform=ax.transAxes, fontsize=7.5, va="top", color=GREY)
    save(fig, "fig2-3-projectile.png")


def fig2_4():
    R = 1.0
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.2))
    ax = axes[0]
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(R * np.cos(th), R * np.sin(th), color=GREY, lw=1.2)
    for ang in (30, 120, 210, 300):
        a = ang * D2R
        px, py = R * np.cos(a), R * np.sin(a)
        ax.annotate("", xy=(px, py), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=LIGHT, lw=1.0))
        vx, vy = -np.sin(a), np.cos(a)
        ax.annotate("", xy=(px + 0.42 * vx, py + 0.42 * vy), xytext=(px, py),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4))
        ax.annotate("", xy=(px - 0.34 * np.cos(a), py - 0.34 * np.sin(a)), xytext=(px, py),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.35, 1.35)
    ax.set_aspect("equal")
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("位置、速度与向心加速度", fontsize=8.8)

    ax = axes[1]
    Rv = np.linspace(0.2, 4, 300)
    for v, col in [(5, TEAL), (10, ACCENT)]:
        ax.plot(Rv, v ** 2 / Rv, color=col, label=f"$v={v}\\ \\mathrm{{m/s}}$")
    ax.set_xlabel("半径 $R$（m）")
    ax.set_ylabel(r"$a=v^{2}/R$（$\mathrm{m\,s^{-2}}$）")
    ax.set_ylim(0, 120)
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title("速率给定时，半径越小加速度越大", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig2-4-circular.png")


fig2_1()
fig2_2()
fig2_3()
fig2_4()
