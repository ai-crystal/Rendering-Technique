import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def fresnel(n1, n2, th):
    s1 = np.sin(th)
    c1 = np.cos(th)
    c2 = np.sqrt(1 - (n1 / n2 * s1) ** 2 + 0j)
    rs = (n1 * c1 - n2 * c2) / (n1 * c1 + n2 * c2)
    rp = (n2 * c1 - n1 * c2) / (n2 * c1 + n1 * c2)
    return rs, rp


def fig8_1():
    fig, axes = plt.subplots(1, 4, figsize=(7.2, 2.4))
    t = np.linspace(0, 2 * np.pi, 400)
    for ax, deg in zip(axes, [0, 45, 90, 135]):
        d = np.radians(deg)
        ex = np.cos(t)
        ey = np.cos(t + d)
        ax.plot(ex, ey, color=ACCENT, lw=1.6)
        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.35)
        ax.set_aspect("equal")
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_title("δ = %d°" % deg, fontsize=8.5)
        ax.grid(alpha=0.2)
    axes[0].set_ylabel("E_y / a")
    axes[1].set_xlabel("E_x / a")
    fig.subplots_adjust(wspace=0.42)
    save(fig, "fig8-1-ellipse.png")


def fig8_2():
    th = np.linspace(0, 89.9, 900)
    rs, rp = fresnel(1.0, 1.5, np.radians(th))
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 4.6), sharex=True)
    ax = axes[0]
    ax.plot(th, np.real(rs), color=BLUE, lw=1.7, label="r_s")
    ax.plot(th, np.real(rp), color=ACCENT, lw=1.7, label="r_p")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_ylabel("振幅反射系数")
    ax.legend(loc="lower right", fontsize=8)
    ax.annotate("布儒斯特角 56.3°", xy=(56.3, 0), xytext=(62, 0.28), fontsize=8,
                color=GREY, arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.8))
    ax.set_ylim(-1.05, 0.32)

    ax = axes[1]
    ax.plot(th, np.abs(rs) ** 2, color=BLUE, lw=1.7, label="R_s")
    ax.plot(th, np.abs(rp) ** 2, color=ACCENT, lw=1.7, label="R_p")
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("反射率")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="upper left", fontsize=8)
    save(fig, "fig8-2-fresnel.png")


def tir_delta(n1, n2, th):
    # 根号内是 sin^2 - (n2/n1)^2
    root = np.sqrt(np.maximum(np.sin(th) ** 2 - (n2 / n1) ** 2, 0))
    c = np.cos(th)
    ds = -2 * np.arctan2(root, c)
    dp = -2 * np.arctan2(root, (n2 / n1) ** 2 * c)
    return np.degrees(dp - ds)


def fig8_3():
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    for n, col in [(1.5, BLUE), (1.8, ACCENT)]:
        tc = np.degrees(np.arcsin(1 / n))
        th = np.linspace(tc + 0.05, 89.9, 800)
        ax.plot(th, np.abs(tir_delta(n, 1.0, np.radians(th))), color=col, lw=1.9,
                label="n = %.1f，临界角 %.1f°" % (n, tc))
        ax.plot([tc], [0], "o", ms=3, color=col)
    ax.axhline(45, color=GREY, ls=":", lw=1.0)
    ax.text(60, 47, "45 度", fontsize=8, color=GREY)
    ax.set_xlim(30, 90)
    ax.set_ylim(0, 95)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("相位差 δ_p - δ_s（度）")
    ax.legend(loc="upper left", fontsize=8)
    save(fig, "fig8-3-tir.png")


fig8_1()
fig8_2()
fig8_3()

print("check:", tir_delta(1.51, 1.0, np.radians(54.0)))
