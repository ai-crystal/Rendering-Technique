import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180


def fig5_2():
    # 一个可控的剖面：三个峰，两个谷
    px = [0.0, 0.9, 1.6, 2.2, 2.9, 3.6, 4.3, 5.0, 5.7, 6.2, 6.9, 7.6, 8.4, 9.2, 10.0]
    py = [0.35, 0.55, 0.30, 0.75, 1.20, 0.45, 0.80, 0.30, 0.60, 0.35, 1.05, 0.50, 0.85, 0.40, 0.70]

    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.plot(px, py, color=BLUE, lw=1.8, solid_joinstyle="round")

    def ray(p0, p1, col, lw=1.4, ls="-", head=True):
        ax.annotate("", xy=p1, xytext=p0,
                    arrowprops=dict(arrowstyle="-|>" if head else "-", color=col, lw=lw, ls=ls))

    # A：顺利进出
    A = (1.25, 0.42)
    ray((0.35, 2.35), A, ACCENT)
    ray(A, (0.65, 2.30), BLUE)
    ax.plot(*A, "o", ms=5, color=ACCENT)
    ax.text(0.30, 0.02, "A", color=ACCENT, fontsize=10, fontweight="bold")
    ax.text(0.05, 2.45, "入射", color=ACCENT, fontsize=8.5)
    ax.text(0.62, 2.42, "出射", color=BLUE, fontsize=8.5)

    # B：入射被峰挡住
    B = (3.55, 0.44)
    ray((2.55, 2.35), (2.92, 1.22), RED)
    ax.plot([2.92], [1.22], marker="x", ms=8, color=RED, mew=1.8)
    ray((2.92, 1.22), B, RED, ls=":", head=False)
    ax.text(2.05, 0.85, "B", color=RED, fontsize=10, fontweight="bold")
    ax.text(3.05, 1.32, "入射被峰挡住", color=RED, fontsize=8.5)

    # C：出射被挡
    C = (6.55, 0.72)
    ray((5.75, 2.35), C, ACCENT)
    ray(C, (7.05, 1.10), PURPLE)
    ax.plot([7.05], [1.10], marker="x", ms=8, color=PURPLE, mew=1.8)
    ax.text(6.35, 0.42, "C", color=PURPLE, fontsize=10, fontweight="bold")
    ax.text(7.20, 1.05, "出射被峰挡住", color=PURPLE, fontsize=8.5)

    ax.set_xlim(0, 10)
    ax.set_ylim(-0.1, 2.7)
    ax.set_xlabel("表面位置")
    ax.set_ylabel("高度")
    ax.set_yticks([])
    save(fig, "fig5-2-masking.png")


def fig5_1():
    th = np.linspace(1, 89, 400)
    c = np.cos(th * D2R)
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    for alpha, col in [(0.2, BLUE), (0.4, TEAL), (0.6, ACCENT), (1.0, RED)]:
        ax.plot(th, g1_smith(c, alpha), color=col, lw=1.9, label="α = %.1f" % alpha)
    ax.plot(th, g1_uncorrelated(c, 0.6), color=GREY, lw=1.2, ls="--",
            label="不相关近似 α = 0.6")
    ax.set_xlabel("方向与法线夹角（度）")
    ax.set_ylabel("G1")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="lower left")
    save(fig, "fig5-1-g1.png")


fig5_1()
fig5_2()
