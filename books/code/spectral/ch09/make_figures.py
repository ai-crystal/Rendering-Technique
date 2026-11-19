import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()


# ------------------------------------------------------------------ 图 9-1
def fig5_1():
    """一条路径上的光谱：光源、第一次反射、第二次反射。"""
    light = normalize_y(LAM, blackbody(LAM, 3200.0))
    m1 = 0.04 + 0.86 * gaussian_line(LAM, 600, 70)      # 暖色墙面
    m2 = 0.04 + 0.80 * gaussian_line(LAM, 470, 60)      # 偏冷的地面
    s0 = light
    s1 = light * m1
    s2 = light * m1 * m2

    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    k = 1.0 / s0.max()
    ax.plot(LAM, s0 * k, color=GOLD, lw=1.6, label="光源")
    ax.plot(LAM, s1 * k, color=ACCENT, lw=1.6, label="第一次反射后")
    ax.plot(LAM, s2 * k, color=PURPLE, lw=1.7, label="第二次反射后")
    ax.set_yscale("log")
    ax.set_xlim(380, 780)
    ax.set_ylim(2e-3, 1.4)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("光谱辐亮度（按光源峰值归一）")
    ax.legend(loc="lower left")
    ax.set_title("每一次反弹都是一次逐波长的乘法", pad=6)
    save(fig, "fig9-1-path-spectra.png")


# ------------------------------------------------------------------ 图 9-2
def fig5_2():
    """有色介质的透射率随厚度变化。"""
    # 吸收带在 590 nm 附近（类似某些有色玻璃），两端吸收小
    sigma = (0.9 * gaussian_line(LAM, 590, 55) + 0.35 * gaussian_line(LAM, 470, 70)
             + 0.06)
    ds = [0.5, 1.5, 4.0]
    fig = plt.figure(figsize=(7.0, 3.1))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.55, 1.0], wspace=0.26)

    ax = fig.add_subplot(gs[0])
    for d, col in zip(ds, [BLUE, TEAL, ACCENT]):
        T = np.exp(-sigma * d)
        ax.plot(LAM, T, color=col, lw=1.7, label="厚度 %.1f mm" % d)
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("内透射率 T(λ)")
    ax.legend(loc="lower right")
    ax.set_title("指数关系把微小差异放大", pad=6)

    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    white = blackbody(LAM, 6504.0)
    for i, d in enumerate(ds):
        T = np.exp(-sigma * d)
        xyz = spectrum_to_xyz(LAM, white * T)
        c = srgb_encode(np.clip(M_XYZ2RGB_PUBLISHED @ (xyz / xyz[1]) / 1.35, 0, 1))
        y = 0.66 - i * 0.24
        ax2.add_patch(plt.Rectangle((0.04, y), 0.30, 0.19, color=c, ec="#3a3a3a", lw=0.6))
        ax2.text(0.42, y + 0.12, "%.1f mm" % d, fontsize=8, va="center")
        ax2.text(0.42, y + 0.04, "Y = %.2f" % (xyz[1] / spectrum_to_xyz(LAM, white)[1]),
                 fontsize=7.5, va="center", color="#555")
    ax2.text(0.04, 0.94, "6500 K 光源下透过玻璃的颜色", fontsize=8.2, va="center")
    save(fig, "fig9-2-transmittance.png")


# ------------------------------------------------------------------ 图 9-3
def fig5_3():
    """多次反弹把反射率的差异累积成饱和度。"""
    R = 0.05 + 0.90 * gaussian_line(LAM, 620, 55)
    fig, ax = plt.subplots(figsize=(6.3, 3.2))
    for k, col in zip([1, 2, 4, 8], [BLUE, TEAL, ACCENT, PURPLE]):
        ax.plot(LAM, R ** k, color=col, lw=1.7, label="%d 次反弹" % k)
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("累积反射率 R(λ)$^k$")
    ax.legend(loc="upper left", ncol=2, columnspacing=1.0)
    ax.text(0.98, 0.42, "红色通道 0.95$^k$\n蓝色通道 0.05$^k$", transform=ax.transAxes,
            fontsize=8, ha="right", color="#3c4654")
    save(fig, "fig9-3-bounces.png")


fig5_1()
fig5_2()
fig5_3()
