import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Circle


def fig8_1():
    R = 1.0
    r = np.linspace(0.02, 3.0, 800)
    shell = np.where(r < R, 1.0, R / r)
    solid = np.where(r < R, (3 - r ** 2 / R ** 2) / 2, R / r)
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.plot(r, shell, color=BLUE, label="带电球壳")
    ax.plot(r, solid, color=ACCENT, ls="--", label="均匀带电实心球")
    ax.axvline(R, color=GREY, ls=":", lw=0.9)
    ax.set_xlabel("距离 $r$（以 $R$ 为单位）")
    ax.set_ylabel(r"$\varphi$（以 $kQ/R$ 为单位）")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1.75)
    ax.legend(loc="upper right", fontsize=8)
    ax.text(0.06, 1.06, "球壳内部等势", fontsize=7.8, color=BLUE)
    ax.text(0.55, 1.42, "实心球中心为球面的 1.5 倍", fontsize=7.8, color=ACCENT)
    save(fig, "fig8-1-sphere-potential.png")


def fig8_2():
    x = np.linspace(-2.2, 2.2, 500)
    z = np.linspace(-2.2, 2.2, 500)
    X, Z = np.meshgrid(x, z)
    Rr = np.sqrt(X ** 2 + Z ** 2)
    Rr[Rr < 0.05] = np.nan
    phi = Z / Rr ** 3

    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    levels = [-0.9, -0.55, -0.3, -0.15, 0.15, 0.3, 0.55, 0.9]
    ax.contour(X, Z, phi, levels=levels, colors=BLUE, linewidths=0.9, linestyles="solid")
    ax.contour(X, Z, phi, levels=[0.0], colors=GREY, linewidths=0.8, linestyles=":")
    th = np.linspace(0.001, np.pi - 0.001, 600)
    for R in (0.45, 0.7, 1.0, 1.45, 2.0):
        r = R * np.sin(th) ** 2
        xx = r * np.sin(th)
        zz = r * np.cos(th)
        keep = (np.abs(xx) < 2.1) & (np.abs(zz) < 2.1)
        ax.plot(xx[keep], zz[keep], color=SKY, lw=0.7, alpha=0.9)
        ax.plot(-xx[keep], zz[keep], color=SKY, lw=0.7, alpha=0.9)
    ax.plot([0], [0.05], "o", color=RED, ms=5)
    ax.plot([0], [-0.05], "o", color=BLUE, ms=5)
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-2.15, 2.15)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$z$")
    ax.text(-1.9, 1.95, "蓝线：等势线；浅蓝细线：场线；灰点线：零势面",
            fontsize=7.4, color=INK)
    save(fig, "fig8-2-equipotential.png")


fig8_1()
fig8_2()
