import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()
BASIS = cie_xyz_basis(LAM) * np.gradient(LAM)     # 已含 dλ


def residual_fraction(f):
    """f 落在 span{x̄,ȳ,z̄} 之外的能量比例。"""
    A = BASIS.T
    coef, *_ = np.linalg.lstsq(A, f, rcond=None)
    r = f - A @ coef
    return float(np.sqrt(np.sum(r ** 2) / np.sum(f ** 2)))


# ------------------------------------------------------------------ 图 8-1
def fig4_1():
    """三条基函数的乘积跑出三维子空间。"""
    x, y, z = cie_x(LAM), cie_y(LAM), cie_z(LAM)
    fig = plt.figure(figsize=(7.0, 3.1))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0], wspace=0.30)

    ax = fig.add_subplot(gs[0])
    ax.plot(LAM, x, color=RED, lw=1.3, label=r"$\bar{x}$")
    ax.plot(LAM, y, color=GREEN, lw=1.3, label=r"$\bar{y}$")
    ax.plot(LAM, x * y / (x * y).max(), color=PURPLE, lw=1.8, ls="--",
            label=r"$\bar{x}\bar{y}$（归一）")
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 1.85)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("响应")
    ax.legend(loc="upper right")
    ax.set_title("两个基函数的乘积是一个新的形状", pad=6)

    ax2 = fig.add_subplot(gs[1])
    names = [r"$\bar{x}^2$", r"$\bar{y}^2$", r"$\bar{z}^2$",
             r"$\bar{x}\bar{y}$", r"$\bar{x}\bar{z}$", r"$\bar{y}\bar{z}$"]
    pair = [(x, x), (y, y), (z, z), (x, y), (x, z), (y, z)]
    vals = [residual_fraction(a * b) for a, b in pair]
    cols = [RED, GREEN, BLUE, PURPLE, GOLD, TEAL]
    ax2.bar(range(6), vals, color=cols, alpha=0.88, width=0.66)
    for i, v in enumerate(vals):
        ax2.text(i, v + 0.02, "%.2f" % v, ha="center", va="bottom", fontsize=7.8)
    ax2.set_xticks(range(6))
    ax2.set_xticklabels(names, fontsize=9)
    ax2.set_ylim(0, 0.78)
    ax2.set_ylabel("落在三维子空间之外的比例")
    ax2.set_title("乘积无法写回三条基函数", pad=6)
    save(fig, "fig8-1-products.png")


# ------------------------------------------------------------------ 图 8-2
def _mul_vs_spec(light_center, light_fwhm, mat_center=575.0, mat_fwhm=45.0, dark=0.05):
    light = gaussian_line(LAM, light_center, light_fwhm)
    mat = dark + (1 - dark) * gaussian_line(LAM, mat_center, mat_fwhm)
    xl = spectrum_to_xyz(LAM, light)
    xm = spectrum_to_xyz(LAM, mat)
    xp = spectrum_to_xyz(LAM, light * mat)
    rl = M_XYZ2RGB_PUBLISHED @ (xl / xl[1])
    rm = reflectance_rgb(mat)
    mul = np.clip(rl, 0, None) * np.clip(rm, 0, None)
    y_mul = (M_RGB2XYZ_PUBLISHED @ mul)[1]
    y_spec = xp[1] / xl[1]
    return y_mul, y_spec, mul, xp / xl[1]


def fig4_2():
    """带宽越窄，RGB 乘法把亮度高估得越多。"""
    fwhms = np.logspace(np.log10(4), np.log10(160), 30)
    ratios = []
    for f in fwhms:
        ym, ys, _, _ = _mul_vs_spec(490, f)
        ratios.append(ym / ys)
    ratios = np.array(ratios)

    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.semilogx(fwhms, ratios, color=ACCENT, lw=1.9)
    ax.axhline(1.0, color=GREY, lw=1.1, ls="--")
    ax.set_xlabel("光源带宽（半高宽，nm）")
    ax.set_ylabel("RGB 结果的 Y / 光谱结果的 Y")
    ax.set_ylim(0, 13)
    for f in (12, 45, 120):
        ym, ys, _, _ = _mul_vs_spec(490, f)
        ax.plot([f], [ym / ys], "o", color=BLUE, ms=4)
        ax.annotate("%.0f nm：%.1f 倍" % (f, ym / ys), xy=(f, ym / ys),
                    xytext=(f * 1.25, ym / ys * 1.05), fontsize=7.8, color="#3c4654")
    ax.text(6, 2.2, "比值 1 表示两条路径一致", fontsize=8, color="#666")
    save(fig, "fig8-2-bandwidth.png")


# ------------------------------------------------------------------ 图 8-3
def fig4_3():
    """光源扫过材质反射带：RGB 乘法既会高估上百倍，也会造出超过入射的能量。"""
    centers = np.arange(420, 681, 2.0)
    y_rgb, y_spec = [], []
    for c in centers:
        ym, ys, _, _ = _mul_vs_spec(c, 20.0, mat_center=575.0, mat_fwhm=45.0)
        y_rgb.append(ym)
        y_spec.append(ys)
    y_rgb = np.array(y_rgb)
    y_spec = np.array(y_spec)

    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    ax.plot(centers, y_spec, color=BLUE, lw=1.9, label="逐波长相乘的反射光")
    ax.plot(centers, y_rgb, color=ACCENT, lw=1.9, ls="--", label="RGB 逐通道相乘")
    ax.axhline(1.0, color=GREY, lw=1.0, ls=":")
    ax.text(600, 1.07, "入射能量", fontsize=7.6, color="#666")
    ax.set_xlabel("窄带光源的中心波长 (nm)，带宽 20 nm")
    ax.set_ylabel("反射光的 Y（入射为 1）")
    ax.set_ylim(0, 3.4)
    ax.set_xlim(420, 680)

    ir = int(np.argmax(y_rgb / np.maximum(y_spec, 1e-9)))
    ax.text(424, 3.15, "%d nm 附近比值 %.0f 倍" % (centers[ir], y_rgb[ir] / y_spec[ir]),
            fontsize=7.8, color="#3c4654")
    i2 = int(np.argmin(np.abs(centers - 645)))
    ax.annotate("高估 %.0f 倍" % (y_rgb[i2] / y_spec[i2]),
                xy=(centers[i2], y_rgb[i2]), xytext=(560, 2.55),
                fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="-", lw=0.6, color="#8a93a0"))
    i3 = int(np.argmin(y_rgb[10:60])) + 10
    ax.annotate("RGB 归零", xy=(centers[i3], y_rgb[i3] + 0.02), xytext=(centers[i3] + 42, 0.22),
                fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="-", lw=0.6, color="#8a93a0"))
    ax.annotate("带内两条曲线最接近", xy=(578, 0.88), xytext=(470, 1.62),
                fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="-", lw=0.6, color="#8a93a0"))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2,
              columnspacing=1.6, handlelength=1.9)
    save(fig, "fig8-3-sweep.png")


fig4_1()
fig4_2()
fig4_3()
