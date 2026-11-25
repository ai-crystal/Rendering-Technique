import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Circle, Polygon, FancyArrowPatch

D2R = np.pi / 180


def arr(ax, p0, p1, color, lw=1.4, ls="-", style="-|>", ms=9):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0))


def fig3_1():
    mus, muk, N = 0.5, 0.35, 10.0
    F = np.linspace(0, 8, 300)
    f = np.where(F <= mus * N, F, muk * N)
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.plot(F, f, color=BLUE, lw=1.8)
    ax.axvline(mus * N, color=GREY, ls="--", lw=0.9)
    ax.axhline(muk * N, color=GREY, ls=":", lw=0.9)
    ax.annotate("最大静摩擦 $\\mu_sN$", (mus * N, mus * N), xytext=(3.4, 3.3),
                fontsize=7.8, color=INK,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.annotate("动摩擦 $\\mu_kN$", (6.6, muk * N), xytext=(5.0, 1.4),
                fontsize=7.8, color=INK,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.text(1.0, 4.5, "静止：$f=F$", fontsize=8, color=BLUE)
    ax.text(5.4, 5.0, "滑动：$f=\\mu_kN$", fontsize=8, color=BLUE)
    ax.set_xlabel("水平拉力 $F$（N）")
    ax.set_ylabel("摩擦力 $f$（N）")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 6)
    save(fig, "fig3-1-friction.png")


def fig3_2():
    th = 30 * D2R
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    ax = axes[0]
    ax.set_aspect("equal")
    ax.plot([0, 4], [0, 4 * np.tan(th)], color=INK, lw=1.6)
    ax.plot([0, 4], [0, 0], color=INK, lw=1.0)
    # 滑块位置
    s = 2.4
    bx, by = s * np.cos(th), s * np.sin(th)
    w, h = 0.55, 0.30
    nx, ny = -np.sin(th), np.cos(th)
    tx, ty = np.cos(th), np.sin(th)
    corners = []
    for du, dv in [(-w / 2, 0), (w / 2, 0), (w / 2, h), (-w / 2, h)]:
        corners.append((bx + du * tx + dv * nx, by + du * ty + dv * ny))
    ax.add_patch(Polygon(corners, closed=True, facecolor="#dfe6ee",
                         edgecolor=INK, lw=1.0))
    cx = bx + 0.15 * nx
    cy = by + 0.15 * ny
    arr(ax, (cx, cy), (cx, cy - 1.5), RED, lw=1.5)
    ax.text(cx + 0.06, cy - 1.62, "$mg$", fontsize=8.5, color=RED)
    # 两个分量：沿斜面向下 1.5sin(theta)，垂直斜面压入 1.5cos(theta)
    L = 1.5
    ex, ey = cx - L * np.sin(th) * np.cos(th), cy - L * np.sin(th) * np.sin(th)
    nx2, ny2 = cx + L * np.cos(th) * np.sin(th), cy - L * np.cos(th) * np.cos(th)
    arr(ax, (cx, cy), (ex, ey), ACCENT, lw=1.1, ls="--")
    arr(ax, (cx, cy), (nx2, ny2), BLUE, lw=1.1, ls="--")
    ax.plot([ex, cx, nx2], [ey, cy - 1.5, ny2], color=LIGHT, lw=0.7, ls=":")
    ax.text(ex - 0.10, ey - 0.16, r"$mg\sin\theta$", fontsize=8, color=ACCENT, ha="right")
    ax.text(nx2 + 0.10, ny2 - 0.10, r"$mg\cos\theta$", fontsize=8, color=BLUE)
    # 角
    ax.annotate("", xy=(1.1, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.text(0.85, 0.12, r"$\theta$", fontsize=8.5, color=INK)
    ax.set_xlim(-0.4, 4.3)
    ax.set_ylim(-0.4, 2.9)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("受力分解", fontsize=8.8)

    ax = axes[1]
    ang = np.linspace(5, 75, 300)
    for mu, col, lab in [(0.0, BLUE, r"$\mu_k=0$"), (0.2, TEAL, r"$\mu_k=0.2$"),
                         (0.5, ACCENT, r"$\mu_k=0.5$")]:
        a = 9.81 * (np.sin(ang * D2R) - mu * np.cos(ang * D2R))
        ax.plot(ang, a, color=col, label=lab)
        if mu > 0:
            th0 = np.degrees(np.arctan(mu))
            ax.plot([th0], [0], "o", ms=3.5, color=col)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("斜面倾角 $\\theta$（度）")
    ax.set_ylabel(r"下滑加速度 $a$（$\mathrm{m\,s^{-2}}$）")
    ax.legend(loc="upper left", fontsize=7.8)
    ax.set_xlim(0, 75)
    ax.set_ylim(-3, 10)
    ax.set_title("加速度随倾角", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig3-2-incline.png")


def fig3_3():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    ax = axes[0]
    ax.set_aspect("equal")
    ax.add_patch(Circle((2.0, 2.4), 0.28, facecolor="#eceff3", edgecolor=INK, lw=1.1))
    ax.plot([2.0], [2.4], "o", color=INK, ms=3)
    ax.plot([1.72, 1.72], [2.4, 1.0], color=INK, lw=1.0)
    ax.plot([2.28, 2.28], [2.4, 1.7], color=INK, lw=1.0)
    ax.add_patch(plt.Rectangle((1.42, 0.55), 0.60, 0.45, facecolor="#dfe6ee", edgecolor=INK))
    ax.add_patch(plt.Rectangle((1.98, 1.25), 0.60, 0.45, facecolor="#dfe6ee", edgecolor=INK))
    arr(ax, (1.72, 1.02), (1.72, 1.70), BLUE, lw=1.3)
    arr(ax, (2.28, 1.72), (2.28, 2.35), BLUE, lw=1.3)
    ax.text(1.58, 1.66, "$T$", fontsize=8.5, color=BLUE, ha="right")
    ax.text(2.36, 2.05, "$T$", fontsize=8.5, color=BLUE)
    arr(ax, (1.72, 1.05), (1.72, 0.50), RED, lw=1.0, ls="--")
    arr(ax, (2.58, 1.48), (2.58, 0.98), RED, lw=1.0, ls="--")
    ax.text(1.60, 0.62, "$m_1g$", fontsize=8, color=RED, ha="right")
    ax.text(2.66, 1.05, "$m_2g$", fontsize=8, color=RED)
    ax.set_xlim(0.9, 3.1)
    ax.set_ylim(0.2, 2.9)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("装置与受力", fontsize=8.8)

    ax = axes[1]
    r = np.linspace(1.02, 8, 300)
    ax.plot(r, (r - 1) / (r + 1), color=BLUE, label=r"$a/g$")
    ax.plot(r, 2 * r / (r + 1), color=ACCENT, label=r"$T/(m_2g)$")
    ax.set_xlabel("质量比 $m_1/m_2$")
    ax.set_ylabel("无量纲量")
    ax.set_ylim(0, 2.1)
    ax.set_xlim(1, 8)
    ax.legend(loc="center right", fontsize=8)
    ax.axhline(1, color=GREY, ls=":", lw=0.8)
    ax.set_title("加速度与张力", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig3-3-atwood.png")


fig3_1()
fig3_2()
fig3_3()
