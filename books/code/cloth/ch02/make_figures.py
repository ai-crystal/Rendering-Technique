import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

from matplotlib.colors import ListedColormap


def weave_patterns(n=12):
    """三种组织的经纬浮沉矩阵：1 表示经纱浮在表面，0 表示纬纱。"""
    plain = np.zeros((n, n), dtype=int)
    twill = np.zeros((n, n), dtype=int)
    satin = np.zeros((n, n), dtype=int)
    for j in range(n):          # 行 = 纬纱序号
        for i in range(n):      # 列 = 经纱序号
            plain[j, i] = 1 if (i + j) % 2 == 0 else 0
            twill[j, i] = 1 if (i + j) % 4 < 2 else 0
            satin[j, i] = 1 if (2 * i + j) % 5 == 0 else 0
    return {"平纹": plain, "斜纹 2/2": twill, "缎纹 5/2": satin}


def fig2_1():
    pats = weave_patterns(12)
    cmap = ListedColormap(["#e8e2d6", "#a8443c"])
    fig, axes = plt.subplots(1, 3, figsize=(6.8, 2.7))
    for ax, (name, m) in zip(axes, pats.items()):
        ax.imshow(m, cmap=cmap, interpolation="nearest", origin="upper")
        ax.set_title(name, fontsize=9.5)
        ax.set_xticks(range(0, 12, 4))
        ax.set_yticks(range(0, 12, 4))
        ax.set_xticklabels(["1", "5", "9"])
        ax.set_yticklabels(["1", "5", "9"])
        ax.set_xlabel("经纱序号", fontsize=8)
        ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(True)
            s.set_color("#8a93a0")
    axes[0].set_ylabel("纬纱序号", fontsize=8)
    fig.tight_layout()
    save(fig, "fig2-1-weave.png")


def fig2_2():
    """捻角与法线倾角分布。"""
    T = np.linspace(100, 1600, 400)          # 捻/米
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.1))
    ax = axes[0]
    for r, c in [(0.10e-3, BLUE), (0.20e-3, ACCENT)]:
        beta = np.arctan(2 * np.pi * r * T)
        ax.plot(T, np.rad2deg(beta), color=c, label="纱线半径 %.1f mm" % (r * 1000))
    ax.set_xlabel("捻度（捻/米）")
    ax.set_ylabel("捻角（度）")
    ax.legend(loc="upper left")
    ax.set_xlim(100, 1600)
    ax.set_ylim(0, 70)

    ax2 = axes[1]
    th = np.linspace(-90, 90, 900)
    for T_, c in [(400, BLUE), (800, TEAL), (1200, ACCENT)]:
        beta = np.rad2deg(np.arctan(2 * np.pi * 0.15e-3 * T_))
        dens = np.exp(-((th - beta) / 9.0) ** 2) + np.exp(-((th + beta) / 9.0) ** 2)
        ax2.plot(th, dens / dens.max(), color=c,
                 label="%d 捻/米，捻角 %.0f 度" % (T_, beta))
    ax2.set_xlabel("纤维法线相对纱线径向的倾角（度）")
    ax2.set_ylabel("归一化密度")
    ax2.set_xlim(-90, 90)
    ax2.set_ylim(0, 1.35)
    ax2.legend(loc="upper left", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig2-2-twist.png")


def fig2_3():
    """三种组织的表面高度场与法线方位角分布。"""
    n = 256
    p = 1.0
    x = np.linspace(0, 4 * p, n)
    X, Y = np.meshgrid(x, x)
    fields = {}
    fields["平纹"] = 0.5 * (np.cos(2 * np.pi * X / p) + np.cos(2 * np.pi * Y / p))
    fields["斜纹"] = 0.5 * (np.cos(2 * np.pi * (X + Y) / (1.4 * p)) +
                           np.cos(2 * np.pi * (X - Y) / (1.4 * p)))
    fields["缎纹"] = 0.62 * np.cos(2 * np.pi * X / (3.5 * p)) + 0.12 * np.cos(2 * np.pi * Y / p)

    fig, axes = plt.subplots(1, 4, figsize=(7.2, 2.7),
                             gridspec_kw={"width_ratios": [1, 1, 1, 1.15]})
    for ax, (name, Z) in zip(axes[:3], fields.items()):
        ax.imshow(Z, cmap="bone", interpolation="bilinear", extent=[0, 4, 0, 4])
        ax.set_title(name, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(True)
            s.set_color("#8a93a0")
    axes[0].set_ylabel("组织循环", fontsize=8)

    axp = fig.add_subplot(1, 4, 4, projection="polar")
    for (name, Z), c in zip(fields.items(), [GREY, ACCENT, BLUE]):
        gy, gx = np.gradient(Z, x, x)
        az = np.arctan2(gy, gx)
        mag = np.hypot(gx, gy)
        hist, edges = np.histogram(az, bins=72, range=(-np.pi, np.pi), weights=mag)
        centers = 0.5 * (edges[:-1] + edges[1:])
        axp.plot(centers, hist / hist.max(), color=c, lw=1.2, label=name)
    axp.set_yticklabels([])
    axp.set_xticks(np.deg2rad([0, 45, 90, 135]))
    axp.set_xticklabels(["0", "45", "90", "135"], fontsize=7)
    axp.grid(alpha=0.3)
    axp.set_xticklabels(["0", "45", "90", "135"], fontsize=7)
    fig.legend(*axp.get_legend_handles_labels(), loc="lower center", ncol=3,
               fontsize=7.5, bbox_to_anchor=(0.62, -0.04))
    fig.tight_layout()
    save(fig, "fig2-3-aniso.png")


fig2_1()
fig2_2()
fig2_3()
