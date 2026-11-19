import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *


# ------------------------------------------------------------------ 图 3-1
def fig3_1():
    """三种光的二阶相干度。"""
    tau = np.linspace(-4, 4, 800)
    thermal = 1.0 + np.exp(-2.0 * np.abs(tau))
    coherent = np.ones_like(tau)
    single = 1.0 - np.exp(-6.0 * np.abs(tau))

    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(tau, thermal, color=ACCENT, lw=1.8, label="热光（混沌光）  1+|g¹|²")
    ax.plot(tau, coherent, color=BLUE, lw=1.8, label="相干光（激光）  1")
    ax.plot(tau, single, color=TEAL, lw=1.5, ls="--", label="单光子源  反聚束")
    ax.axhline(1.0, color=GREY, lw=0.7, ls=":")
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 2.25)
    ax.set_xlabel("延迟 τ / τc")
    ax.set_ylabel("$g^{(2)}(\\tau)$")
    ax.set_title("二阶相干度把三种光分开", pad=6)
    ax.legend(loc="lower left", bbox_to_anchor=(0.015, 0.02))
    ax.annotate("聚束：g²(0)=2", xy=(0, 2.0), xytext=(0.55, 1.55), fontsize=8,
                color=ACCENT, arrowprops=dict(arrowstyle="-", lw=0.6, color=ACCENT))
    ax.annotate("g²(0)=0", xy=(0, 0.0), xytext=(0.45, 0.22), fontsize=8,
                color=TEAL, arrowprops=dict(arrowstyle="-", lw=0.6, color=TEAL))
    fig.tight_layout()
    save(fig, "fig3-1-g2.png")


# ------------------------------------------------------------------ 图 3-2
def fig3_2():
    """相干长度与谱宽的关系。"""
    lam0 = 550.0
    dl = np.logspace(-6, 3, 400)                    # nm
    lc = (lam0 * 1e-9) ** 2 / (dl * 1e-9)           # m

    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.loglog(dl, lc, color=INK, lw=1.8)
    marks = [(100.0, "白光 LED", 2.0, 5.0e-6),
             (0.6, "钠灯 D 双线", 3.0e-2, 4.0e-4),
             (1e-4, "单频激光", 6e-6, 2.5)]
    for d0, lab, tx, ty in marks:
        v = (lam0 * 1e-9) ** 2 / (d0 * 1e-9)
        ax.plot([d0], [v], "o", ms=4, color=ACCENT)
        ax.annotate(lab, xy=(d0, v), xytext=(tx, ty), fontsize=8, color="#3c4654",
                    arrowprops=dict(arrowstyle="-", lw=0.5, color=GREY))
    ax.axhspan(0.1e-6, 2e-6, color=GREEN, alpha=0.12, lw=0)
    ax.text(2e-6, 3.6e-7, "薄膜厚度", fontsize=7.5, color=GREEN)
    ax.set_xlim(1e-6, 1e3)
    ax.set_ylim(1e-7, 1e4)
    ax.set_xlabel("谱宽 Δλ（FWHM, nm）")
    ax.set_ylabel("相干长度 $l_c=\\lambda^2/\\Delta\\lambda$ (m)")

    top = ax.secondary_xaxis("top", functions=(lambda d: C_LIGHT * d * 1e-9 / (lam0 * 1e-9) ** 2 / 1e12,
                                               lambda f: f * 1e12 * (lam0 * 1e-9) ** 2 / (C_LIGHT * 1e-9)))
    top.set_xlabel("对应的谱宽 Δν (THz)", fontsize=8.5)
    ax.set_title("谱宽越窄，相干越长", pad=6)
    fig.tight_layout()
    save(fig, "fig3-2-coherence-length.png")


# ------------------------------------------------------------------ 图 3-3
def fig3_3():
    """薄膜干涉的可见度随膜厚衰减。"""
    lam0, n_film = 550.0, 1.5
    lam = np.linspace(300, 900, 4000)
    d = np.linspace(0, 10000, 500)                  # nm

    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    for dl, c, lab in ((100, ACCENT, "Δλ = 100 nm"), (20, BLUE, "Δλ = 20 nm"),
                       (2, TEAL, "Δλ = 2 nm")):
        S = gaussian_line(lam, lam0, dl)
        phase = 4.0 * np.pi * n_film * d[None, :] / lam[:, None]
        z = np.trapezoid(S[:, None] * np.exp(1j * phase), lam, axis=0)
        ax.plot(d / 1000.0, np.abs(z) / np.trapezoid(S, lam), color=c, lw=1.7, label=lab)
    ax.axvspan(0.1, 2.0, color=GREEN, alpha=0.10, lw=0)
    ax.text(1.55, 0.25, "薄膜", fontsize=8, color=GREEN)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.32)
    ax.set_xlabel("膜厚 d (μm)，折射率 1.5")
    ax.set_ylabel("条纹可见度包络")
    ax.set_title("相干长度决定薄膜还能不能出彩", pad=20)
    ax.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.02),
              columnspacing=1.6, handlelength=1.6)
    fig.tight_layout()
    save(fig, "fig3-3-film-visibility.png")


# ------------------------------------------------------------------ 图 3-4
def fig3_4():
    """散斑对比度与被平均的模式数。"""
    M = np.logspace(0, 6, 300)
    C = 1.0 / np.sqrt(M)
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.loglog(M, C, color=PURPLE, lw=1.8)
    ax.axhline(0.05, color=RED, lw=1.0, ls="--")
    ax.text(1.15, 0.078, "对比度 5%%，肉眼大致可忽睔", fontsize=8, color=RED)
    for m0, lab in ((1, "单模激光"), (12, "多模激光"), (1e4, "宽谱光源")):
        ax.plot([m0], [1 / np.sqrt(m0)], "o", ms=4, color=PURPLE)
        ax.annotate(lab, xy=(m0, 1 / np.sqrt(m0)), xytext=(m0 * 2.2, 1 / np.sqrt(m0) * 0.34),
                    fontsize=8, color="#3c4654")
    ax.set_xlim(1, 1e6)
    ax.set_ylim(1e-3, 1.5)
    ax.set_xlabel("参与的独立模式数 M")
    ax.set_ylabel("散斑对比度 $1/\\sqrt{M}$")
    ax.set_title("散斑：只在模式数少的时候露头", pad=6)
    fig.tight_layout()
    save(fig, "fig3-4-speckle.png")


fig3_1()
fig3_2()
fig3_3()
fig3_4()


