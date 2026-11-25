import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Circle, FancyArrowPatch, Arc, Wedge

D2R = np.pi / 180


def fig15_1():
    fig, ax = plt.subplots(figsize=(5.8, 3.4))
    ax.set_xlim(-1.2, 2.2)
    ax.set_ylim(-1.2, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    # 导线（沿 z 轴，用斜线表示出纸面）
    ax.plot([0, 0], [-1.0, 1.3], color=INK, lw=2.2)
    ax.text(-0.10, 1.34, "$I$", fontsize=9, ha="right")
    ax.annotate("", xy=(0, 1.1), xytext=(0, 0.75),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, mutation_scale=8))
    # 电流元
    ax.plot([0], [0.15], "o", ms=5, color=ACCENT)
    ax.text(-0.14, 0.18, "$I\\,d\\mathbf{l}$", fontsize=8.5, ha="right", color=ACCENT)
    # 观察点与位置矢量
    P = (1.55, 0.95)
    ax.plot([P[0]], [P[1]], "o", ms=4, color=BLUE)
    ax.text(P[0] + 0.06, P[1] + 0.04, "$P$", fontsize=9, color=BLUE)
    ax.plot([0, P[0]], [0.15, P[1]], color=GREY, lw=0.9, ls="--")
    ax.text(0.72, 0.62, "$\\mathbf{r}$", fontsize=9, color=GREY)
    # dB 方向：dl x r
    ax.annotate("", xy=(P[0] - 0.42, P[1] - 0.42), xytext=P,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6, mutation_scale=10))
    ax.text(P[0] - 0.72, P[1] - 0.55, "$d\\mathbf{B}$", fontsize=9, color=RED)
    # 磁感线圆
    for rr in (0.45, 0.8, 1.15):
        ax.add_patch(Arc((0, 0), 2 * rr, 2 * rr * 0.42, theta1=200, theta2=340,
                         color=SKY, lw=0.7))
    ax.text(2.02, -0.55, "磁感线", fontsize=7.5, color=SKY, ha="right")
    save(fig, "fig15-1-element.png")


def fig15_2():
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-0.7, 2.1)
    ax.axis("off")
    ax.grid(False)
    ax.plot([0, 0], [-0.5, 1.9], color=INK, lw=2.0)
    ax.text(0.08, 1.92, "$I$", fontsize=9)
    ax.plot([0.9, 0.9], [-0.35, 1.55], color=INK, lw=1.0, ls=":")
    ax.plot([0.9], [0.55], "o", ms=5, color=BLUE)
    ax.text(1.0, 0.60, "$P$", fontsize=9, color=BLUE)
    ax.plot([0, 0.9], [0.55, 0.55], color=GREY, lw=1.0)
    ax.text(0.40, 0.40, "$a$", fontsize=8.5, color=GREY)
    for z, th in [(1.25, 38), (0.0, 0), (-0.9, -38)]:
        ax.plot([0], [z], "o", ms=4, color=ACCENT)
        ax.plot([0, 0.9], [z, 0.55], color=LIGHT, lw=0.8, ls="--")
    ax.annotate(r"$\theta_2$", (0.30, 0.72), fontsize=8.5)
    ax.annotate(r"$\theta_1$", (0.30, 0.32), fontsize=8.5)
    ax.annotate("", xy=(0.06, 1.1), xytext=(0.14, 1.05),
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.8))
    ax.text(0.95, -0.10, "$r=\\sqrt{a^{2}+z^{2}}$", fontsize=8.5, color=GREY)
    ax.text(-2.3, -0.55, "$z=a\\tan\\theta$，积分限从 $\\theta_1$ 到 $\\theta_2$",
            fontsize=8, color=INK)
    save(fig, "fig15-2-straight.png")


def fig15_3():
    z = np.linspace(-6, 6, 800)
    B = 1.0 / (1 + z ** 2) ** 1.5
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    ax.plot(z, B, color=BLUE)
    ax.set_xlabel("$z/R$")
    ax.set_ylabel("$B/(\\mu_0I/2R)$")
    ax.set_title("轴线上磁场", fontsize=8.8)
    ax = axes[1]
    zz = np.linspace(1.2, 30, 400)
    ax.loglog(zz, 1 / (1 + zz ** 2) ** 1.5, color=BLUE, label="精确值")
    ax.loglog(zz, 1 / zz ** 3, "--", color=GREY, lw=1.0, label="$1/z^{3}$")
    ax.set_xlabel("$z/R$")
    ax.set_ylabel("相对强度")
    ax.legend(loc="lower left", fontsize=7.8)
    ax.set_title("远处按 $1/z^{3}$ 衰减", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig15-3-loop.png")


fig15_1()
fig15_2()
fig15_3()
