import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Rectangle, Arc, FancyArrowPatch


def fig21_1():
    t = np.linspace(0, 5, 500)
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.plot(t, 1 - np.exp(-t), color=BLUE, label="通电：$1-e^{-t/\\tau}$")
    ax.plot(t, np.exp(-t), color=ACCENT, ls="--", label="断电：$e^{-t/\\tau}$")
    ax.axvline(1, color=GREY, ls=":", lw=0.9)
    ax.axhline(0.632, color=GREY, ls=":", lw=0.9)
    ax.plot([1], [0.632], "o", ms=4, color=INK)
    ax.annotate("$t=\\tau$，$63\\%$", (1, 0.632), xytext=(1.7, 0.45), fontsize=7.8,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.set_xlabel("$t/\\tau$")
    ax.set_ylabel("归一化电流")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="center right", fontsize=8)
    save(fig, "fig21-1-lr.png")


def fig21_2():
    t = np.linspace(0, 8, 500)
    I = 1 - np.exp(-t)
    P = I * np.exp(-t)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    ax.plot(t, P, color=ACCENT, label="$\\mathcal{E}_L I$")
    ax.fill_between(t, 0, P, color=SKY, alpha=0.35, lw=0)
    ax.set_xlabel("$t/\\tau$")
    ax.set_ylabel("功率（相对单位）")
    ax.text(2.2, 0.22, "面积 $=\\frac{1}{2}LI^{2}$", fontsize=8, color=INK)
    ax.set_title("通电过程中的功率", fontsize=8.8)

    ax = axes[1]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 3)
    ax.add_patch(Rectangle((0.6, 0.5), 3.8, 1.6, facecolor="#f4f7fa", edgecolor=INK))
    for x in np.linspace(0.85, 4.2, 10):
        ax.add_patch(Arc((x, 1.3), 0.4, 1.5, theta1=-90, theta2=90, color=ACCENT, lw=1.1))
    for y in (0.85, 1.3, 1.75):
        ax.annotate("", xy=(4.3, y), xytext=(0.8, y),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.7, mutation_scale=5))
    ax.text(2.5, 0.25, "$u_B=B^{2}/2\\mu_0$", fontsize=8.5, ha="center")
    ax.axis("off")
    ax.grid(False)
    ax.set_title("螺线管内的磁能", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig21-2-energy.png")


def fig21_3():
    t = np.linspace(0, 3, 600)
    w = 2 * np.pi
    q = np.cos(w * t)
    I = -np.sin(w * t)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    ax.plot(t, q, color=BLUE, label="$q/q_0$")
    ax.plot(t, I, color=ACCENT, label="$I/(q_0\omega)$")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("$t/T$")
    ax.legend(loc="upper right", fontsize=7.6)
    ax.set_title("电荷与电流相差 $90^\circ$", fontsize=8.6)
    ax = axes[1]
    ax.plot(t, 0.5 * q ** 2 / 0.5, color=TEAL, label="电场能量")
    ax.plot(t, 0.5 * I ** 2 / 0.5, color=PURPLE, label="磁场能量")
    ax.plot(t, 0.5 * q ** 2 / 0.5 + 0.5 * I ** 2 / 0.5, color=INK, ls="--", label="总量")
    ax.set_xlabel("$t/T$")
    ax.set_ylim(0, 1.15)
    ax.legend(loc="center right", fontsize=7.6)
    ax.set_title("能量在电场与磁场间转换", fontsize=8.6)
    fig.tight_layout()
    save(fig, "fig21-3-lc.png")


fig21_1()
fig21_2()
fig21_3()
