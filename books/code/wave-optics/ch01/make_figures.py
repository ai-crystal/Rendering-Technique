import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def airy_R(lam_nm, d_nm, n1, n0=1.0, n2=4.1 + 0.03j, theta0=0.0):
    """单层膜反射率，lam 与 d 都用纳米，n2 可以是复数。"""
    lam = lam_nm * 1e-9
    d = d_nm * 1e-9
    s0 = np.sin(theta0)
    c0 = np.sqrt(1 - s0 ** 2)
    s1 = n0 * s0 / n1
    c1 = np.sqrt(1 - s1 ** 2)
    s2 = n0 * s0 / n2
    c2 = np.sqrt(1 - s2 ** 2)
    r01 = (n0 * c0 - n1 * c1) / (n0 * c0 + n1 * c1)
    r12 = (n1 * c1 - n2 * c2) / (n1 * c1 + n2 * c2)
    beta = 2 * np.pi * n1 * d * c1 / lam
    ph = np.exp(2j * beta)
    r = (r01 + r12 * ph) / (1 + r01 * r12 * ph)
    return np.abs(r) ** 2


def fig1_1():
    lam = np.linspace(380, 780, 900)
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    for d, col, lab in [(60, BLUE, "60 nm"), (90, ACCENT, "90 nm"), (120, TEAL, "120 nm")]:
        ax.plot(lam, airy_R(lam, d, 1.46) * 100, color=col, lw=1.9, label=lab)
    ax.axvspan(380, 780, color="#f2ecdf", zorder=0)
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 62)
    ax.set_xlabel("波长（nm）")
    ax.set_ylabel("反射率（%）")
    ax.legend(loc="upper left", title="氧化层厚度", title_fontsize=7.5, ncol=3)
    ax.annotate("绿色被压掉\n表面呈紫红", xy=(520, 4), xytext=(470, 26),
                fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.9))
    save(fig, "fig1-1-oxide.png")


def fig1_2():
    lam = np.linspace(380, 780, 1200)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for dL, col in [(263, BLUE), (400, TEAL), (550, GOLD), (800, RED)]:
        ax.plot(lam, 1 + np.cos(2 * np.pi * dL / lam), color=col, lw=1.7,
                label="光程差 %d nm" % dL)
    ax.set_xlim(380, 780)
    ax.set_ylim(-0.15, 2.45)
    ax.set_xlabel("波长（nm）")
    ax.set_ylabel("归一化强度")
    ax.set_yticks([0, 1, 2])
    ax.legend(loc="upper right", ncol=2, fontsize=7.5)
    save(fig, "fig1-2-fringes.png")


def fig1_3():
    """两条边界由公式定：相位延迟 2pi(n-1)d/lam，衍射半角 arcsin(lam/a)。"""
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    n = 1.46
    d_a = 0.25 / (n - 1)      # 相位延迟 pi/2
    d_b = 1.0 / (n - 1)       # 相位延迟 2pi
    ax.axvspan(1e-2, 0.5, color="#eddcd8", alpha=0.55, lw=0)
    ax.axvspan(0.5, 20, color="#dde5ec", alpha=0.55, lw=0)
    ax.axvspan(20, 1e3, color="#f0f0ea", alpha=0.55, lw=0)
    ax.axhline(d_a, color=BLUE, lw=1.2, ls="--")
    ax.axhline(d_b, color=BLUE, lw=1.2, ls="--")
    ax.axvline(0.5, color=RED, lw=1.2, ls=":")
    ax.axvline(20, color=RED, lw=1.2, ls=":")

    ax.text(3.2, 220, "几何光学", fontsize=10, color=INK, ha="center")
    ax.text(3.2, 1.05, "薄膜与光栅", fontsize=10, color=INK, ha="center")
    ax.text(3.2, 0.025, "超薄：等效界面", fontsize=10, color=INK, ha="center")
    ax.text(0.06, 1.05, "亚波长", fontsize=10, color=INK, ha="center")
    ax.text(0.06, 0.025, "偏振主导", fontsize=9, color=INK, ha="center")
    ax.text(0.06, 220, "矢量衍射", fontsize=9, color=INK, ha="center")

    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=BLUE, ls="--", lw=1.2, label="相位延迟 pi/2 与 2pi"),
               Line2D([], [], color=RED, ls=":", lw=1.2, label="衍射半角 30 度与 3 度")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.16),
              ncol=2, fontsize=8)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("横向特征尺寸 / 波长")
    ax.set_ylabel("厚度或高度 / 波长")
    ax.set_xlim(1e-2, 1e3)
    ax.set_ylim(1e-2, 1e3)
    save(fig, "fig1-3-regimes.png")


fig1_1()
fig1_2()
fig1_3()
