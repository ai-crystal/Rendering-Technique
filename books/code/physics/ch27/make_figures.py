import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def fig27_1():
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.set_xlim(-0.2, 4 * np.pi + 0.4)
    ax.set_ylim(-1.9, 2.0)
    z = np.linspace(0, 4 * np.pi, 600)
    ax.plot(z, np.cos(z), color=BLUE, label=r"$E_x$")
    ax.plot(z, 0.75 * np.cos(z), color=ACCENT, label=r"$B_y$（$=E/c$）")
    ax.plot(z, np.zeros_like(z), color=GREY, lw=0.9)
    ax.annotate("", xy=(4 * np.pi + 0.2, 0), xytext=(3.4, 0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3, mutation_scale=9))
    ax.text(4 * np.pi - 0.4, 0.22, r"$z$（传播方向）", fontsize=8, color=INK, ha="right")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_xlabel(r"位置 $z$")
    ax.set_ylabel("场强（相对单位）")
    ax.set_xticks([])
    ax.text(0.15, 1.62, r"$\mathbf{E}\perp\mathbf{B}\perp\mathbf{k}$，$E/B=c$", fontsize=8.6)
    save(fig, "fig27-1-plane-wave.png")


def fig27_2():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    ax.set_xlim(0, 6.4)
    ax.set_ylim(-1.6, 1.6)
    ax.axis("off")
    ax.grid(False)
    ax.annotate("", xy=(5.6, 0), xytext=(0.6, 0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=9))
    ax.text(5.2, -0.35, r"$\mathbf{S}$", fontsize=9, color=INK)
    ax.annotate("", xy=(3.0, 1.3), xytext=(3.0, 0.0),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6, mutation_scale=9))
    ax.text(3.08, 1.15, r"$\mathbf{E}$", fontsize=9, color=BLUE)
    ax.text(3.0, -0.75, r"$\odot$", fontsize=20, color=ACCENT, ha="center", va="center")
    ax.text(3.28, -0.75, r"$\mathbf{B}$（向纸外）", fontsize=7.8, color=ACCENT, va="center")
    ax.set_title(r"$\mathbf{S}=\mathbf{E}\times\mathbf{B}/\mu_0$", fontsize=9)

    ax = axes[1]
    r = np.logspace(-0.6, 0.7, 400)
    ax.loglog(r, 1 / r ** 2, color=BLUE)
    ax.set_xlabel(r"距离 $r$（对数）")
    ax.set_ylabel("强度（相对）")
    ax.set_title(r"点光源：$I\propto1/r^{2}$", fontsize=8.8)
    ax.set_xticks([0.3, 0.5, 1, 2, 4])
    ax.set_xticklabels(["0.3", "0.5", "1", "2", "4"])
    ax.minorticks_off()
    ax.text(0.08, 0.12, "斜率 $-2$", transform=ax.transAxes, fontsize=7.8, color=INK)
    fig.tight_layout()
    save(fig, "fig27-2-poynting.png")


def fig27_3():
    bands = [
        (1e-13, 1e-11, "伽马射线", "#dcd7ee"),
        (1e-11, 1e-8, "X 射线", "#cfe2f0"),
        (1e-8, 4e-7, "紫外", "#d9ecdc"),
        (4e-7, 7e-7, "", "#f6e2a8"),
        (7e-7, 1e-3, "红外", "#f4d9c6"),
        (1e-3, 1e-2, "微波", "#d3e9ea"),
        (1e-2, 1e0, "调频广播", "#e6e2ef"),
        (1e0, 1e4, "长波无线电", "#e4e8ea"),
    ]
    fig, ax = plt.subplots(figsize=(7.0, 2.8))
    ax.set_xscale("log")
    ax.set_xlim(1e-13, 1e4)
    ax.set_ylim(-0.6, 1.9)
    for lo, hi, lab, col in bands:
        ax.axvspan(lo, hi, color=col, lw=0)
        if lab:
            ax.text(np.sqrt(lo * hi), -0.05, lab, ha="center", va="center",
                    fontsize=7.4, color=INK)
    ax.axvspan(4e-7, 7e-7, facecolor="none", edgecolor=ACCENT, lw=1.2)
    ax.annotate("可见光", xy=(5.3e-7, 0.30), xytext=(2.0e-7, 1.35),
                fontsize=7.4, color=INK, ha="center",
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.7))
    ax.set_yticks([])
    ax.set_xlabel("波长（m，对数坐标）")
    ax.spines["left"].set_visible(False)
    ax.grid(False)
    save(fig, "fig27-3-spectrum.png")


def fig27_4():
    t = np.linspace(0, 2 * np.pi, 400)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    for d, col, lab in [(0, BLUE, r"$\delta=0$"),
                        (np.pi / 2, ACCENT, r"$\delta=\pi/2$"),
                        (np.pi, TEAL, r"$\delta=\pi$")]:
        ax.plot(np.cos(t), np.cos(t + d), color=col, label=lab, lw=1.4)
    ax.set_aspect("equal")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_xlabel(r"$E_x/E_0$")
    ax.set_ylabel(r"$E_y/E_0$")
    ax.legend(loc="upper right", fontsize=7.4, bbox_to_anchor=(1.02, 1.18))
    ax.set_title("偏振态", fontsize=8.8)

    ax = axes[1]
    th = np.linspace(0, 180, 300)
    ax.plot(th, np.cos(th * np.pi / 180) ** 2, color=BLUE)
    ax.set_xlabel(r"夹角 $\theta$（度）")
    ax.set_ylabel(r"$I/I_0=\cos^{2}\theta$")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 1.05)
    ax.set_title("马吕斯定律", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig27-4-polarization.png")


fig27_1()
fig27_2()
fig27_3()
fig27_4()
