import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Circle, FancyArrowPatch

D2R = np.pi / 180


def fig6_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.3))
    ax = axes[0]
    ax.set_aspect("equal")
    for a in np.arange(0, 360, 30):
        ar = a * D2R
        ax.annotate("", xy=(0.92 * np.cos(ar), 0.92 * np.sin(ar)),
                    xytext=(0.12 * np.cos(ar), 0.12 * np.sin(ar)),
                    arrowprops=dict(arrowstyle="-|>", color=SKY, lw=0.9,
                                    mutation_scale=7))
    ax.add_patch(Circle((0, 0), 0.06, color=RED, zorder=3))
    ax.text(0.03, 0.08, "$+Q$", fontsize=9, color=RED)
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.axis("off")
    ax.grid(False)
    ax.set_title("正电荷的电场线", fontsize=8.8)

    ax = axes[1]
    r = np.logspace(-1, 1, 300)
    E = 8.99e9 * 1e-6 / r ** 2
    ax.loglog(r, E, color=BLUE, label="$E=kQ/r^{2}$")
    ax.set_xlabel("距离 $r$（m）")
    ax.set_ylabel(r"$E$（$\mathrm{V\,m^{-1}}$）")
    ax.legend(loc="upper right", fontsize=8)
    ax.text(0.05, 0.10, "双对数坐标下斜率为 $-2$", transform=ax.transAxes,
            fontsize=7.8, color=INK)
    ax.set_title("点电荷的场强", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig6-1-point-charge.png")


def fig6_2():
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    th = np.linspace(0.001, np.pi - 0.001, 600)
    for R in (0.35, 0.55, 0.8, 1.15, 1.6, 2.2):
        r = R * np.sin(th) ** 2
        x = r * np.sin(th)
        z = r * np.cos(th)
        keep = (np.abs(x) < 2.3) & (np.abs(z) < 1.7)
        ax.plot(x[keep], z[keep], color=SKY, lw=0.9)
        ax.plot(-x[keep], z[keep], color=SKY, lw=0.9)
        ax.plot([0], [R], 'o', ms=0)
    ax.add_patch(Circle((0, 0.045), 0.05, color=RED, zorder=4))
    ax.add_patch(Circle((0, -0.045), 0.05, color=BLUE, zorder=4))
    ax.text(0.07, 0.03, "$+q$", fontsize=8.5, color=RED)
    ax.text(0.07, -0.10, "$-q$", fontsize=8.5, color=BLUE)
    ax.annotate("", xy=(0, -0.42), xytext=(0, -0.62),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text(0.06, -0.63, "$\\mathbf{p}$", fontsize=9, color=INK)
    ax.set_xlim(-2.35, 2.35)
    ax.set_ylim(-1.75, 1.75)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    ax.set_title("偶极子的电场线（$r=R\\sin^{2}\\theta$，远场近似）", fontsize=8.8)
    save(fig, "fig6-2-dipole-lines.png")


def fig6_3():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1))
    k = 8.99e9
    p = 6.17e-30  # 约 1.85 D
    r = np.logspace(-9, -7.5, 300)
    ax = axes[0]
    ax.loglog(r, 2 * k * p / r ** 3, color=BLUE, label=r"轴线 $2kp/r^{3}$")
    ax.loglog(r, k * p / r ** 3, color=ACCENT, label=r"中垂线 $kp/r^{3}$")
    ax.set_xlabel("距离 $r$（m）")
    ax.set_ylabel(r"$E$（$\mathrm{V\,m^{-1}}$）")
    ax.legend(loc="upper right", fontsize=7.8)
    ax.text(0.04, 0.06, "斜率均为 $-3$", transform=ax.transAxes, fontsize=7.6, color=INK)
    ax.set_title("偶极子场随距离衰减", fontsize=8.8)

    ax = axes[1]
    th = np.linspace(0, 360, 600)
    ax.plot(th, np.sin(th * D2R), color=BLUE, label=r"$\tau/(pE)=\sin\theta$")
    ax.plot(th, -np.cos(th * D2R), color=ACCENT, label=r"$U/(pE)=-\cos\theta$")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("偶极矩与场的夹角 $\\theta$（度）")
    ax.set_ylabel("无量纲量")
    ax.set_xlim(0, 360)
    ax.set_ylim(-1.35, 1.35)
    ax.set_xticks([0, 90, 180, 270, 360])
    ax.legend(loc="upper right", fontsize=7.8)
    ax.set_title("均匀场中的力矩与势能", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig6-3-dipole-field.png")


fig6_1()
fig6_2()
fig6_3()
