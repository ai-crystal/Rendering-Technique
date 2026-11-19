import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid(200.0, 4000.0, 2.0)


# ------------------------------------------------------------------ 图 1-1
def fig1_1():
    """三个温度的黑体谱：形状与绝对量级。"""
    temps = [(5800, SKY, "5800 K"), (3000, ACCENT, "3000 K"), (1000, RED, "1000 K")]

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    ax = axes[0]
    for T, c, lab in temps:
        B = planck_radiance(LAM, T)
        ax.plot(LAM, B / B.max(), color=c, lw=1.6, label=lab)
        lm = wien_peak_nm(T)
        ax.plot([lm, lm], [0, 1.02], color=c, lw=0.7, ls=":")
    ax.set_xlim(200, 4000)
    ax.set_ylim(0, 1.30)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("相对谱辐亮度（各自归一）")
    ax.set_title("峰值随温度左移", pad=20)
    ax.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.02),
              columnspacing=1.4, handlelength=1.5)
    ax.annotate("500 nm", xy=(500, 1.0), xytext=(640, 1.04), fontsize=8,
                color="#3c4654", arrowprops=dict(arrowstyle="-", lw=0.55, color=GREY))
    ax.annotate("966 nm", xy=(966, 0.62), xytext=(1180, 0.80), fontsize=8,
                color="#3c4654", arrowprops=dict(arrowstyle="-", lw=0.55, color=GREY))
    ax.annotate("2898 nm", xy=(2898, 0.35), xytext=(2130, 0.50), fontsize=8,
                color="#3c4654", arrowprops=dict(arrowstyle="-", lw=0.55, color=GREY))

    ax = axes[1]
    for T, c, lab in temps:
        ax.plot(LAM, planck_radiance(LAM, T), color=c, lw=1.6, label=lab)
    ax.set_yscale("log")
    ax.set_xlim(200, 4000)
    ax.set_ylim(1e-9, 1e7)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("Bλ  W/(m²·sr·nm)")
    ax.set_title("绝对量级（对数坐标）", pad=20)
    ax.legend(loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout()
    save(fig, "fig1-1-planck-curves.png")


# ------------------------------------------------------------------ 图 1-2
def fig1_2():
    """瑞利–金斯公式与普朗克公式在短波端的分离。"""
    T = 5000.0
    lam = grid(80.0, 12000.0, 1.0)
    p = planck_radiance(lam, T)
    rj = rayleigh_jeans_radiance(lam, T)
    w = wien_radiance(lam, T)

    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.loglog(lam, p, color=INK, lw=1.8, label="普朗克 1901")
    ax.loglog(lam, rj, color=RED, lw=1.6, ls="--", label="瑞利–金斯 1900/1905")
    ax.loglog(lam, w, color=BLUE, lw=1.4, ls=":", label="维恩 1896")
    ax.set_xlim(80, 12000)
    ax.set_ylim(1e-6, 1e14)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("Bλ  W/(m²·sr·nm)")
    ax.axvspan(80, 300, color=RED, alpha=0.05, lw=0)

    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0))
    i100 = np.argmin(np.abs(lam - 100))
    ax.annotate("100 nm 处瑞利–金斯\n高估 %.0e 倍" % (rj[i100] / p[i100]),
                xy=(100, rj[i100]), xytext=(150, 2e12), fontsize=8,
                color=RED, arrowprops=dict(arrowstyle="-", lw=0.6, color=RED))
    ax.annotate("长波端三者合流", xy=(6000, planck_radiance(6000, T)),
                xytext=(1150, 2.2e-3), fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=GREY))
    ax.set_title("5000 K：黑体谱在短波端的三种答案", pad=6)
    fig.tight_layout()
    save(fig, "fig1-2-ultraviolet.png")


# ------------------------------------------------------------------ 图 1-3
def fig1_3():
    """普朗克轨迹与两条热辐射定律。"""
    fig = plt.figure(figsize=(7.4, 2.9))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 1.0], wspace=0.42)

    # 左：色度图上的普朗克轨迹
    ax = fig.add_subplot(gs[0])
    lam_b = grid(380.0, 780.0, 1.0)
    xyz = cie_xyz_basis(lam_b)
    s = xyz.sum(axis=0)
    ax.plot(xyz[0] / s, xyz[1] / s, color=GREY, lw=1.0)
    ax.plot([0.174, 0.735], [0.005, 0.265], color=GREY, lw=0.9, ls=":")
    Ts = np.arange(1200, 20001, 50)
    xy = []
    for T in Ts:
        e = spectrum_to_xyz(lam_b, planck_radiance(lam_b, T))
        xy.append([e[0] / e.sum(), e[1] / e.sum()])
    xy = np.array(xy)
    sc = ax.scatter(xy[:, 0], xy[:, 1], c=Ts, cmap="coolwarm_r", s=5, lw=0, zorder=3)
    lab = [(2000, 0.062, 0.016), (4500, -0.128, 0.062),
           (6500, -0.125, -0.048), (20000, 0.036, -0.070)]
    for T, dx, dy in lab:
        e = spectrum_to_xyz(lam_b, planck_radiance(lam_b, T))
        x, y = e[0] / e.sum(), e[1] / e.sum()
        ax.plot([x], [y], "o", ms=3.2, color=INK, zorder=4)
        ax.annotate(f"{T}", xy=(x, y), xytext=(x + dx, y + dy), fontsize=7.5,
                    ha="center", color=INK,
                    arrowprops=dict(arrowstyle="-", lw=0.5, color=GREY))
    ax.set_xlim(0.10, 0.75)
    ax.set_ylim(0.0, 0.86)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("普朗克轨迹（数字为色温 K）", pad=6)

    # 中：维恩位移
    ax = fig.add_subplot(gs[1])
    T = np.logspace(np.log10(300), np.log10(20000), 200)
    ax.loglog(T, wien_peak_nm(T), color=ACCENT, lw=1.7)
    for Tv, dx, dy in ((1000, 1.45, 0.30), (3000, 1.45, 0.30), (6500, 0.30, 0.42)):
        ax.plot([Tv], [wien_peak_nm(Tv)], "o", ms=3.2, color=ACCENT)
        ax.annotate(f"{Tv}K {float(wien_peak_nm(Tv)):.0f}nm",
                    xy=(Tv, float(wien_peak_nm(Tv))),
                    xytext=(Tv * dx, float(wien_peak_nm(Tv)) * dy), fontsize=7.2,
                    color="#3c4654")
    ax.axhspan(380, 780, color=GREEN, alpha=0.10, lw=0)
    ax.text(340, 560, "可见光", fontsize=7.5, color=GREEN)
    ax.set_xlim(300, 20000)
    ax.set_ylim(80, 12000)
    ax.set_xlabel("温度 T (K)")
    ax.set_ylabel("λmax (nm)")
    ax.set_title("维恩位移 λmax = b/T", pad=6)

    # 右：斯特藩–玻尔兹曼
    ax = fig.add_subplot(gs[2])
    T = np.logspace(np.log10(300), np.log10(20000), 200)
    M = stefan_boltzmann(T) / 1e6
    ax.loglog(T, M, color=BLUE, lw=1.7)
    ax.loglog(T, 2.2 * M, ls=":", lw=1.0, color=GREY)
    ax.text(0.04, 0.90, "虚线为同斜率参考", transform=ax.transAxes,
            fontsize=7.6, color=GREY)
    ax.set_xlim(300, 20000)
    ax.set_ylim(1e-2, 1e6)
    ax.set_xlabel("温度 T (K)")
    ax.set_ylabel("M  MW/m²")
    ax.set_title("斯特藩–玻尔兹曼 M = σT⁴", pad=6)
    fig.tight_layout()
    save(fig, "fig1-3-locus-wien.png")


fig1_1()
fig1_2()
fig1_3()
