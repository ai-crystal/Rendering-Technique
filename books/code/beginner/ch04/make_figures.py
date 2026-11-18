import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180


def fig4_1():
    fig = plt.figure(figsize=(7.0, 3.0))
    ax = fig.add_subplot(1, 2, 1)
    rng = np.random.default_rng(7)
    xs = np.linspace(0, 1, 26)
    hs = 0.10 * rng.standard_normal(26)
    hs -= hs.min()
    ax.plot(xs, hs, color=BLUE, lw=1.6)
    ax.plot([0, 1], [0.02, 0.02], color=GREY, ls="--", lw=1.0)
    ax.text(0.02, 0.055, "宏观平面", color=GREY, fontsize=8)
    for i in (6, 11, 17):
        x0, x1 = xs[i], xs[i + 1]
        ax.plot([x0, x1], [hs[i], hs[i + 1]], color=ACCENT, lw=3.0, solid_capstyle="round")
        mx, my = (x0 + x1) / 2, (hs[i] + hs[i + 1]) / 2
        dx, dy = x1 - x0, hs[i + 1] - hs[i]
        L = np.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        ax.annotate("", xy=(mx + 0.09 * nx, my + 0.09 * ny), xytext=(mx, my),
                    arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.2))
    ax.text(0.40, 0.30, "微面法线 m", color=ACCENT, fontsize=8.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 0.36)
    ax.set_xlabel("表面位置")
    ax.set_ylabel("高度")
    ax.set_yticks([])
    panel_label(ax, "a")

    ax2 = fig.add_subplot(1, 2, 2)
    th = np.linspace(0.05, 89, 600)
    for alpha, col, lab in [(0.1, BLUE, "α = 0.1"), (0.35, ACCENT, "α = 0.35")]:
        D = d_ggx(np.cos(th * D2R), alpha) * np.cos(th * D2R)
        cdf = np.cumsum(D * np.sin(th * D2R)) / np.sum(D * np.sin(th * D2R))
        ax2.plot(th, cdf, color=col, lw=1.9, label=lab)
        k = np.searchsorted(cdf, 0.9)
        ax2.plot([th[k], th[k]], [0, 0.9], color=col, ls=":", lw=1.0)
    ax2.set_xlabel("微面法线与宏观法线夹角（度）")
    ax2.set_ylabel("法线落在该角度内的比例")
    ax2.set_xlim(0, 60)
    ax2.set_ylim(0, 1.02)
    ax2.legend(loc="lower right")
    ax2.text(14, 0.55, "曲线越陡，法线越集中", color=GREY, fontsize=8)
    panel_label(ax2, "b")
    save(fig, "fig4-1-geometry.png")


def fig4_2():
    th = np.linspace(0, 89, 500)
    c = np.cos(th * D2R)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1))
    fig.subplots_adjust(wspace=0.3)

    ax = axes[0]
    for alpha, col in [(0.3, TEAL), (0.6, ACCENT)]:
        ax.plot(th, d_ggx(c, alpha), color=col, lw=1.9, label="α = %.1f" % alpha)
        ax.plot(th, d_beckmann(c, alpha), color=col, lw=1.3, ls="--")
    ax.set_ylim(0, 4.2)
    ax.set_xlabel("微面法线与宏观法线夹角（度）")
    ax.set_xlim(0, 89)
    ax.set_ylabel("D·(n·m)")
    ax.legend(loc="upper right", title="实线 GGX，虚线 Beckmann", title_fontsize=7.5)
    panel_label(ax, "a")

    ax = axes[1]
    for alpha, col in [(0.1, BLUE), (0.3, TEAL), (0.6, ACCENT)]:
        ax.plot(th, d_ggx(c, alpha), color=col, lw=1.9, label="α = %.1f" % alpha)
        ax.plot(th, d_beckmann(c, alpha), color=col, lw=1.3, ls="--")
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 1e3)
    ax.set_xlabel("微面法线与宏观法线夹角（度）")
    ax.set_xlim(0, 89)
    ax.grid(True, which="both", alpha=0.18)
    ax.text(42, 2.5e1, "GGX 尾部按幂律衰减\nBeckmann 按指数衰减",
            color=ACCENT, fontsize=8,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.88, pad=2))
    panel_label(ax, "b")
    save(fig, "fig4-2-ggx-beckmann.png")


def fig4_3():
    r = np.linspace(0.01, 1, 300)
    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    ax.plot(r, r, color=GREY, lw=1.6, label="线性  α = r")
    ax.plot(r, r ** 2, color=ACCENT, lw=2.0, label="平方  α = r²")
    ax.plot(r, r ** 4, color=BLUE, lw=1.6, label="四次方  α = r⁴")
    ax.set_xlabel("美术面板上的粗糙度 r")
    ax.set_ylabel("公式里的 α")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc="upper left")
    ax.text(0.52, 0.10, "平方映射把低粗糙度区间拉开", color=ACCENT, fontsize=8)
    save(fig, "fig4-3-alpha-map.png")


fig4_1()
fig4_2()
fig4_3()
