import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Rectangle, Arc, FancyArrowPatch


def fig25_1():
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.set_xlim(-0.5, 8.0)
    ax.set_ylim(-1.8, 2.4)
    ax.axis("off")
    ax.grid(False)
    # 导线
    ax.plot([0.2, 3.0], [0, 0], color=INK, lw=1.8)
    ax.plot([5.0, 7.6], [0, 0], color=INK, lw=1.8)
    # 电容器板
    ax.plot([3.0, 3.0], [-1.0, 1.0], color=RED, lw=3.0)
    ax.plot([5.0, 5.0], [-1.0, 1.0], color=BLUE, lw=3.0)
    ax.text(2.6, 1.08, "$+$", fontsize=10, color=RED)
    ax.text(5.1, 1.08, "$-$", fontsize=10, color=BLUE)
    # 回路
    ax.add_patch(Arc((4.0, 0), 2.6, 2.2, theta1=200, theta2=340, color=TEAL, lw=1.4, ls="--"))
    ax.add_patch(Arc((4.0, 1.1), 2.6, 3.2, theta1=200, theta2=340, color=ACCENT, lw=1.4, ls="-"))
    ax.plot([2.7, 2.7], [0.0, 0.85], color=TEAL, lw=0.8, ls=":")
    ax.text(1.4, -1.35, "平面圆盘：包围 $I$", fontsize=7.8, color=TEAL)
    ax.text(4.0, 2.05, "碗形曲面：包围为零", fontsize=7.8, color=ACCENT, ha="center")
    ax.annotate("", xy=(2.2, 0.28), xytext=(1.4, 0.28),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1, mutation_scale=7))
    ax.text(1.3, 0.42, "$I$", fontsize=8.5)
    ax.text(3.6, -0.55, "$E$", fontsize=9, color=PURPLE)
    save(fig, "fig25-1-surfaces.png")


def fig25_2():
    t = np.linspace(0, 6, 500)
    I = np.where(t < 3, 1.0, 0.0)
    fig, axes = plt.subplots(2, 1, figsize=(6.0, 3.6), sharex=True,
                             gridspec_kw={"height_ratios": [1.3, 1]})
    ax = axes[0]
    ax.set_xlim(-0.2, 6.2)
    ax.set_ylim(-0.4, 1.4)
    ax.axis("off")
    ax.grid(False)
    ax.plot([0.3, 2.2], [0.5, 0.5], color=INK, lw=1.6)
    ax.plot([3.8, 5.7], [0.5, 0.5], color=INK, lw=1.6)
    ax.plot([2.2, 2.2], [-0.1, 1.1], color=RED, lw=2.6)
    ax.plot([3.8, 3.8], [-0.1, 1.1], color=BLUE, lw=2.6)
    ax.annotate("", xy=(1.8, 0.72), xytext=(0.9, 0.72),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.2, mutation_scale=7))
    ax.text(0.85, 0.85, "$I$", fontsize=8.5, color=ACCENT)
    for x in np.linspace(2.5, 3.5, 5):
        ax.annotate("", xy=(x, 0.5), xytext=(x, 0.12),
                    arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=0.9, mutation_scale=6))
    ax.text(3.0, 1.18, "$I_d$", fontsize=8.5, color=PURPLE, ha="center")
    ax = axes[1]
    ax.plot(t, I, color=ACCENT, label="传导电流 $I$")
    ax.plot(t, I, color=PURPLE, ls="--", label="位移电流 $I_d$")
    ax.set_xlabel("时间")
    ax.set_ylabel("电流")
    ax.set_ylim(0, 1.3)
    ax.set_yticks([])
    ax.legend(loc="upper right", fontsize=7.6)
    fig.tight_layout()
    save(fig, "fig25-2-displacement.png")


def fig25_3():
    R = 1.0
    r = np.linspace(0, 3, 500)
    B = np.where(r < R, r / R ** 2, 1 / r)
    fig, ax = plt.subplots(figsize=(6.0, 2.9))
    ax.plot(r, B, color=BLUE)
    ax.axvline(R, color=GREY, ls=":", lw=0.9)
    ax.text(1.06, 0.9, "$r=R$", fontsize=8, color=GREY)
    ax.text(0.35, 0.75, "板内线性", fontsize=8, color=BLUE)
    ax.text(1.4, 0.55, "板外 $1/r$", fontsize=8, color=BLUE)
    ax.set_xlabel("到轴线的距离 $r$")
    ax.set_ylabel("$B$（相对单位）")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1.1)
    save(fig, "fig25-3-gap-field.png")


fig25_1()
fig25_2()
fig25_3()
