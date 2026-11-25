import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def fig9_1():
    d, U = 0.01, 100.0
    x = np.linspace(0, d, 200)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    ax.plot(x * 1e3, U * x / d, color=BLUE)
    ax.set_xlabel("位置 $x$（mm）")
    ax.set_ylabel("电势 $\\varphi$（V）")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 105)
    ax.text(1.0, 78, "斜率 $=-E=-10^{4}\\ \\mathrm{V/m}$", fontsize=7.8, color=INK)
    ax.set_title("电势线性下降", fontsize=8.8)

    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.2, 1.2)
    ax.axhline(1.0, color=RED, lw=2.0)
    ax.axhline(-1.0, color=BLUE, lw=2.0)
    ax.text(0.2, 1.08, "正极板", fontsize=8, color=RED)
    ax.text(0.2, -1.30, "负极板", fontsize=8, color=BLUE)
    for xx in np.linspace(1, 9, 9):
        ax.annotate("", xy=(xx, -0.55), xytext=(xx, 0.55),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=7))
    ax.axis("off")
    ax.grid(False)
    ax.set_title("电场均匀，由正指向负", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig9-1-parallel-plate.png")


def fig9_2():
    R, Q = 0.1, 1e-9
    k = 8.99e9
    z = np.linspace(-0.6, 0.6, 500)
    phi = k * Q / np.sqrt(R ** 2 + z ** 2)
    Ez = k * Q * z / (R ** 2 + z ** 2) ** 1.5
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    ax.plot(z, phi, color=BLUE)
    ax.set_xlabel("轴向位置 $z$（m）")
    ax.set_ylabel("电势 $\\varphi$（V）")
    ax.set_title("轴线上的电势", fontsize=8.8)
    ax = axes[1]
    ax.plot(z, Ez, color=ACCENT)
    zmax = R / np.sqrt(2)
    Emax = k * Q * zmax / (R ** 2 + zmax ** 2) ** 1.5
    ax.plot([zmax], [Emax], "o", ms=4, color=INK)
    ax.annotate("$z=R/\\sqrt{2}$", (zmax, Emax), xytext=(0.16, Emax * 0.86),
                fontsize=7.8, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("轴向位置 $z$（m）")
    ax.set_ylabel("电场 $E_z$（V/m）")
    ax.set_title("轴线上的电场", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig9-2-ring.png")


def fig9_3():
    x = np.linspace(-1.5, 1.5, 400)
    z = np.linspace(-1.5, 1.5, 400)
    X, Z = np.meshgrid(x, z)
    a = 0.42
    Rp = np.sqrt(X ** 2 + (Z - a) ** 2)
    Rn = np.sqrt(X ** 2 + (Z + a) ** 2)
    Rp[Rp < 0.03] = np.nan
    Rn[Rn < 0.03] = np.nan
    phi = 1.0 / Rp - 1.0 / Rn
    Ex = X / Rp ** 3 - X / Rn ** 3
    Ez = (Z - a) / Rp ** 3 - (Z + a) / Rn ** 3
    E = np.sqrt(Ex ** 2 + Ez ** 2)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    ax = axes[0]
    ax.contour(X, Z, phi, levels=[-3, -1.5, -0.8, -0.4, 0.4, 0.8, 1.5, 3],
               colors=BLUE, linewidths=0.9, linestyles="solid")
    ax.plot([0], [0.42], "o", ms=4, color=RED)
    ax.plot([0], [-0.42], "o", ms=4, color=BLUE)
    ax.set_aspect("equal")
    ax.set_title("等势线在电荷附近变密", fontsize=8.6)
    ax = axes[1]
    im = ax.imshow(np.log10(E), extent=[-1.5, 1.5, -1.5, 1.5], origin="lower",
                   cmap="Blues", vmin=0, vmax=4)
    ax.set_aspect("equal")
    ax.set_title("场强大小（对数灰度）", fontsize=8.6)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03,
                 label="$\\log_{10}|\\mathbf{E}|$")
    fig.tight_layout()
    save(fig, "fig9-3-density.png")


fig9_1()
fig9_2()
fig9_3()
