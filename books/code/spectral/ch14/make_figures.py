import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()


def media():
    """三种吸收介质的系数（单位 1/mm）。散射很小，直接用 Beer–Lambert。"""
    red_ink_a = 2.2 * gaussian_line(LAM, 520, 85) + 1.4 * gaussian_line(LAM, 440, 55) + 0.04
    red_ink_s = 0.10 * gaussian_line(LAM, 520, 120)
    green_glass_a = 1.5 * gaussian_line(LAM, 655, 75) + 0.02
    green_glass_s = np.full_like(LAM, 0.002)
    amber_glass_a = 1.8 * gaussian_line(LAM, 445, 70) + 0.03
    amber_glass_s = np.full_like(LAM, 0.002)
    milk_a = 0.02 + 0.10 * gaussian_line(LAM, 420, 60)
    milk_s = 12.0 * (LAM / 550.0) ** -1.2
    return [("红墨水", red_ink_a, red_ink_s, RED),
            ("绿玻璃", green_glass_a, green_glass_s, GREEN),
            ("茶色玻璃", amber_glass_a, amber_glass_s, GOLD),
            ("牛奶", milk_a, milk_s, "#7a7a7a")]


# ------------------------------------------------------------------ 图 14-1
def fig10_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1), gridspec_kw={"wspace": 0.28})
    ax = axes[0]
    for name, sa, ss, col in media():
        ax.plot(LAM, sa, color=col, lw=1.7, label=name)
    ax.set_yscale("log")
    ax.set_xlim(380, 780)
    ax.set_ylim(1e-3, 30)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("吸收系数 σa (1/mm)")
    ax.legend(loc="upper right", fontsize=7.6)
    ax.set_title("吸收决定颜色", pad=6)

    ax2 = axes[1]
    for name, sa, ss, col in media():
        ax2.plot(LAM, ss, color=col, lw=1.7, label=name)
    ax2.set_yscale("log")
    ax2.set_xlim(380, 780)
    ax2.set_ylim(1e-3, 40)
    ax2.set_xlabel("波长 λ (nm)")
    ax2.set_ylabel("散射系数 σs (1/mm)")
    ax2.legend(loc="lower left", fontsize=7.6)
    ax2.set_title("散射差四个量级", pad=6)
    save(fig, "fig14-1-coefficients.png")


# ------------------------------------------------------------------ 图 14-2
def fig10_2():
    """厚度 × 介质 的颜色矩阵。"""
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    thick = [1, 5, 20, 80]
    white = blackbody(LAM, 6504.0)
    for j, t in enumerate(thick):
        ax.text(0.20 + 0.19 * j, 0.92, "%d mm" % t, fontsize=8, ha="center", va="center")
    for i, (name, sa, ss, col) in enumerate(media()[:3]):
        ax.text(0.01, 0.73 - i * 0.245, name, fontsize=8.4, va="center")
        for j, t in enumerate(thick):
            T = np.exp(-(sa + ss) * t)
            xyz = spectrum_to_xyz(LAM, white * T)
            c = srgb_encode(np.clip(M_XYZ2RGB_PUBLISHED @ (xyz / spectrum_to_xyz(LAM, white)[1]) / 1.2, 0, 1))
            ax.add_patch(plt.Rectangle((0.12 + 0.19 * j, 0.62 - i * 0.245), 0.16, 0.21,
                                       color=c, ec="#3a3a3a", lw=0.6))
    ax.text(0.55, 0.02, "6500 K 光源穿过介质之后的颜色", fontsize=8, ha="center", color="#555")
    save(fig, "fig14-2-slabs.png")


# ------------------------------------------------------------------ 图 14-3
def fig10_3():
    """自由程的指数分布：不同波长差别很大，采样要用上界。"""
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    sig = {450: 1.20, 550: 0.60, 650: 0.35}
    t = np.linspace(0, 8, 400)
    for lam, s, col in [(450, 1.20, BLUE), (550, 0.60, TEAL), (650, 0.35, RED)]:
        ax.plot(t, s * np.exp(-s * t), color=col, lw=1.7, label="λ = %d nm，σt = %.2f" % (lam, s))
    smax = 1.55
    ax.plot(t, smax * np.exp(-smax * t), color=GREY, lw=1.2, ls="--",
            label="采样用的上界 σmax = %.2f（含 null 碰撞）" % smax)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 1.72)
    ax.set_xlabel("距离（mm）")
    ax.set_ylabel("概率密度 (1/mm)")
    ax.legend(loc="upper right", fontsize=7.4)
    save(fig, "fig14-3-freepath.png")


fig10_1()
fig10_2()
fig10_3()
