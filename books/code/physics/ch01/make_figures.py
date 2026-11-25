import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def box(ax, x, y, w, h, text, color=INK, fc="#f4f6f9", ec="#9aa5b4", fs=8):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.08",
                       linewidth=0.9, edgecolor=ec, facecolor=fc, zorder=2)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=color, zorder=3)


def arrow(ax, p0, p1, color=GREY, ls="-"):
    a = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=8,
                        color=color, linewidth=0.9, linestyle=ls,
                        shrinkA=0.5, shrinkB=0.5, zorder=1)
    ax.add_patch(a)


def fig1_1():
    fig, ax = plt.subplots(figsize=(6.9, 4.2))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    ax.grid(False)

    W, H = 3.3, 0.60
    cols = {"力学": (0.25, ACCENT), "电学": (4.25, BLUE), "磁学": (8.25, TEAL)}
    for name, (x0, col) in cols.items():
        ax.text(x0 + W / 2, 5.95, name, ha="center", fontsize=9.5,
                color=col, fontweight="bold")

    rows = [5.05, 4.05, 3.05, 2.05, 1.05]
    chains = [
        [
            ("米 m　　秒 s　　千克 kg", "#eef1f5"),
            (r"速度　$\mathrm{m\,s^{-1}}$", "#f7f9fb"),
            (r"加速度　$\mathrm{m\,s^{-2}}$", "#f7f9fb"),
            (r"力　$\mathrm{N=kg\,m\,s^{-2}}$", "#f7f9fb"),
            (r"能量　$\mathrm{J=kg\,m^{2}\,s^{-2}}$", "#f7f9fb"),
        ],
        [
            ("安培 A", "#eef1f5"),
            (r"电荷　$\mathrm{C=A\,s}$", "#f7f9fb"),
            (r"电势　$\mathrm{V=kg\,m^{2}\,s^{-3}\,A^{-1}}$", "#f7f9fb"),
            (r"电阻　$\mathrm{\Omega=V\,A^{-1}}$", "#f7f9fb"),
            (r"电容　$\mathrm{F=C\,V^{-1}}$", "#f7f9fb"),
        ],
        [
            ("由 $F=qvB$ 反解", "#eef1f5"),
            (r"磁感应强度　$\mathrm{T=kg\,s^{-2}\,A^{-1}}$", "#f7f9fb"),
            (r"磁通量　$\mathrm{Wb=T\,m^{2}}$", "#f7f9fb"),
            (r"电感　$\mathrm{H=Wb\,A^{-1}}$", "#f7f9fb"),
            (r"电流密度　$\mathrm{A\,m^{-2}}$", "#f7f9fb"),
        ],
    ]
    for (name, (x0, col)), chain in zip(cols.items(), chains):
        for y, (text, fc) in zip(rows, chain):
            box(ax, x0, y, W, H, text, fc=fc, fs=7.6)
            if y != rows[-1]:
                arrow(ax, (x0 + W / 2, y), (x0 + W / 2, y - H + 0.03))

    ax.text(0.1, 0.10, "从上往下：由基本单位与定义式一步步导出",
            fontsize=7.4, color=GREY, va="bottom")
    save(fig, "fig1-1-units.png")


def fig1_2():
    g = 9.81
    l = np.linspace(0.05, 2.0, 400)
    T = 2 * np.pi * np.sqrt(l / g)

    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.1))
    ax = axes[0]
    ax.plot(l, T, color=BLUE)
    for ll in (0.25, 1.0, 2.0):
        tt = 2 * np.pi * np.sqrt(ll / g)
        ax.plot([ll], [tt], "o", ms=4, color=ACCENT)
        ax.annotate(f"$l={ll:g}$ m\n$T={tt:.2f}$ s", (ll, tt),
                    textcoords="offset points", xytext=(6, -20), fontsize=7.3, color=INK)
    ax.set_xlabel("摆长 $l$（m）")
    ax.set_ylabel("周期 $T$（s）")
    ax.set_xlim(0, 2.0)
    ax.set_ylim(0, 3.0)

    ax = axes[1]
    ax.loglog(l, T, color=BLUE, label=r"$T=2\pi\sqrt{l/g}$")
    ref = T[0] * (l / l[0]) ** 0.5
    ax.loglog(l, ref, "--", color=GREY, lw=1.0, label="斜率 1/2 的参考线")
    ax.set_xlabel("摆长 $l$（m）")
    ax.set_ylabel("周期 $T$（s）")
    ax.legend(loc="upper left", fontsize=7.5)
    ax.text(0.32, 0.60, r"$g=9.81\ \mathrm{m\,s^{-2}}$", transform=ax.transAxes,
            fontsize=7.5, color=GREY)
    fig.tight_layout()
    save(fig, "fig1-2-pendulum.png")


def fig1_3():
    items = [
        (0.84e-15, "质子半径", r"$0.84\times10^{-15}$ m", 1),
        (1.0e-10, "原子", r"$10^{-10}$ m", -1),
        (5.0e-7, "可见光波长", r"$5\times10^{-7}$ m", 1),
        (1.7, "人的身高", r"$1.7$ m", -1),
        (6.37e6, "地球半径", r"$6.4\times10^{6}$ m", 1),
        (1.5e11, "日地距离", r"$1.5\times10^{11}$ m", -1),
    ]
    fig, ax = plt.subplots(figsize=(6.8, 2.3))
    ax.set_xscale("log")
    ax.set_xlim(1e-16, 1e13)
    ax.set_ylim(-1, 1)
    ax.axhline(0, color=INK, lw=1.2)
    for x, name, val, side in items:
        ax.plot([x], [0], "o", color=ACCENT, ms=5, zorder=3)
        ax.plot([x, x], [0, 0.14 * side], color=ACCENT, lw=0.9)
        ax.text(x, 0.20 * side, name, ha="center",
                va="bottom" if side > 0 else "top", fontsize=8, color=INK)
        ax.text(x, 0.37 * side, val, ha="center",
                va="bottom" if side > 0 else "top", fontsize=7.5, color=GREY)
    ax.set_yticks([])
    ax.set_xlabel("长度（m，对数坐标）")
    ax.spines["left"].set_visible(False)
    ax.grid(False)
    save(fig, "fig1-3-scales.png")


fig1_1()
fig1_2()
fig1_3()
