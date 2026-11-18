import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *


def fig1_1():
    """双瓣目标与单瓣拟合。目标由两个尺度的瓣叠加，拟合在 log 空间做网格搜索。"""
    x = np.linspace(-90, 90, 1801)
    narrow = 0.55 * np.exp(-(x / 4.5) ** 2)
    wide = 0.30 * np.exp(-(x / 40.0) ** 2) + 0.03
    target = narrow + wide

    # 单瓣候选：GGX 的角度分布，峰值对齐 0 度，扫描 alpha 与幅度
    alphas = np.linspace(0.02, 1.2, 400)
    amps = np.linspace(0.02, 1.5, 400)
    best = (1e9, None, None)
    c = np.cos(np.deg2rad(x))
    for a in alphas:
        shape = d_ggx(c, a)
        shape = shape / shape.max()
        for k in amps:
            single = k * shape
            e = np.mean((np.log10(single + 1e-4) - np.log10(target + 1e-4)) ** 2)
            if e < best[0]:
                best = (e, a, k)
    _, a_best, k_best = best
    shape = d_ggx(c, a_best)
    single = k_best * shape / shape.max()

    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.2),
                             gridspec_kw={"width_ratios": [1.55, 1.0]})
    ax = axes[0]
    ax.semilogy(x, target, color=ACCENT, label="真实布料的分布")
    ax.semilogy(x, single, color=BLUE, ls="--", label="单瓣拟合（$\\alpha=%.2f$）" % a_best)
    ax.semilogy(x, narrow, color=GREY, lw=0.9, ls=":", label="纱线高光带")
    ax.semilogy(x, wide, color=TEAL, lw=0.9, ls=":", label="纤维 sheen")
    ax.set_xlabel("相对镜面方向的偏角（度）")
    ax.set_ylabel("归一化反射强度")
    ax.set_xlim(-90, 90)
    ax.set_ylim(1e-3, 2)
    ax.legend(loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.03))

    ax2 = axes[1]
    ratio = target / np.maximum(single, 1e-9)
    ax2.plot(x, ratio, color=RED)
    ax2.axhline(1.0, color=LIGHT, lw=0.8, ls="--")
    ax2.set_xlabel("偏角（度）")
    ax2.set_ylabel("目标与拟合之比")
    ax2.set_xlim(-90, 90)
    ax2.set_ylim(0, 2.4)
    ax2.text(0.03, 0.94, "同一组参数\n两端差 %.1f 倍" % ratio.max(),
             transform=ax2.transAxes, va="top", fontsize=8, color="#3c4654")
    fig.tight_layout()
    save(fig, "fig1-1-two-lobes.png")


def fig1_2():
    """垂直入射的单方向光下，出射亮度随视角的变化。"""
    deg = np.linspace(0, 88, 700)
    th = np.deg2rad(deg)
    c = np.cos(th)

    lam = np.ones_like(c) * 0.35
    ggx = 0.35 + 0.9 * 0.15 * d_ggx(c, 0.25)
    sheen = 0.35 + 0.15 * d_ggx(c, 0.25) * 0.9
    sheen = sheen + 0.85 * (1.0 - c) ** 4
    sheen = sheen + 0.38 * np.exp(-((deg - 58.0) / 4.5) ** 2)

    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(deg, lam, color=GREY, label="漫反射")
    ax.plot(deg, ggx, color=BLUE, label="漫反射 + GGX 高光")
    ax.plot(deg, sheen, color=ACCENT, label="漫反射 + sheen + 偏侧高光带")
    ax.set_xlabel("视线与法线夹角（度）")
    ax.set_ylabel("相对亮度")
    ax.set_xlim(0, 88)
    ax.set_ylim(0, 1.9)
    ax.legend(loc="upper left")
    ax.annotate("掠射时整体抬升", xy=(84, 1.15), xytext=(52, 1.50),
                fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
    save(fig, "fig1-2-view-angle.png")


fig1_1()
fig1_2()
