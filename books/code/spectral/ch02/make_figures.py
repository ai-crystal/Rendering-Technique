import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

H_EV_THZ = H_PLANCK * 1e12 / Q_ELECTRON      # eV per THz = 4.135667696e-3


# ------------------------------------------------------------------ 图 2-1
def fig2_1():
    """光电效应：最大动能只由频率决定，与光强无关。"""
    W_NA = 2.28       # 钠的逸出功，eV
    nu = np.linspace(300, 1600, 400)          # THz
    K = H_EV_THZ * nu - W_NA

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))

    ax = axes[0]
    m = K > 0
    ax.plot(nu[m], K[m], color=INK, lw=1.8, label="量子图像（两档光强同一条线）")
    ax.axhline(1.6, color=RED, lw=1.2, ls="--", label="经典波动，强光")
    ax.axhline(0.55, color=RED, lw=1.2, ls=":", label="经典波动，弱光")
    nu0 = W_NA / H_EV_THZ
    ax.axvline(nu0, color=GREY, lw=0.8, ls="-.")
    ax.annotate("截止频率 %.0f THz（%.0f nm）" % (nu0, C_LIGHT / (nu0 * 1e12) * 1e9),
                xy=(nu0, 0.0), xytext=(640, -0.33), fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=GREY))
    ax.set_xlim(300, 1600)
    ax.set_ylim(-0.55, 4.2)
    ax.set_xlabel("频率 ν (THz)")
    ax.set_ylabel("最大动能 $K_{max}$ (eV)")
    ax.set_title("钠：能量随频率线性上升", pad=6)
    ax.legend(loc="upper left", bbox_to_anchor=(0.01, 0.99))

    ax = axes[1]
    for W, c, lab in ((2.28, ACCENT, "钠 2.28 eV"), (4.30, BLUE, "锌 4.30 eV")):
        V = (H_EV_THZ * nu - W)
        mm = V > 0
        ax.plot(nu[mm], V[mm], color=c, lw=1.7, label=lab)
        ax.plot([W / H_EV_THZ], [0], "o", ms=3.4, color=c)
    ax.set_xlim(300, 1700)
    ax.set_ylim(0, 3.0)
    ax.set_xlabel("频率 ν (THz)")
    ax.set_ylabel("截止电压 $V_s$ (V)")
    ax.set_title("两种金属，斜率相同", pad=6)
    ax.legend(loc="upper left", bbox_to_anchor=(0.01, 0.99))
    ax.text(330, 1.78, "斜率 = h/e\n= 4.136e-15 V·s", fontsize=8, color="#3c4654")
    fig.tight_layout()
    save(fig, "fig2-1-photoelectric.png")


# ------------------------------------------------------------------ 图 2-2
def fig2_2():
    """三过程能级图与 A/B 系数随波长的变化。"""
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0),
                             gridspec_kw={"width_ratios": [1.0, 1.05]})

    ax = axes[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.25, 1.35)
    ax.axis("off")
    ax.plot([0.05, 0.95], [0, 0], color=INK, lw=1.8)
    ax.plot([0.05, 0.95], [1, 1], color=INK, lw=1.8)
    ax.text(0.96, -0.02, "g", fontsize=9, va="top", ha="left")
    ax.text(0.96, 1.02, "e", fontsize=9, va="bottom", ha="left")
    ax.text(0.03, 0.5, "2.25 eV", fontsize=8, rotation=90, va="center", ha="right",
            color="#3c4654")

    ax.annotate("", xy=(0.20, 0.96), xytext=(0.20, 0.06),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color=BLUE))
    ax.text(0.235, 0.52, "受激吸收\n$B_{12}\\rho(\\nu)$", fontsize=8, color=BLUE)

    zz_t = np.linspace(0, 1, 200)
    xz = 0.50 + 0.014 * np.sin(zz_t * 18 * np.pi)
    ax.plot(xz, 1 - zz_t * 0.92, color=ACCENT, lw=1.3)
    ax.annotate("", xy=(0.50, 0.03), xytext=(0.50, 0.10),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color=ACCENT))
    ax.text(0.53, 0.52, "自发辐射\n$A_{21}$", fontsize=8, color=ACCENT)

    for dx in (-0.012, 0.012):
        ax.annotate("", xy=(0.78 + dx, 0.04), xytext=(0.78 + dx, 0.96),
                    arrowprops=dict(arrowstyle="-|>", lw=1.2, color=TEAL))
    ax.text(0.81, 0.52, "受激辐射\n$B_{21}\\rho(\\nu)$", fontsize=8, color=TEAL)
    ax.set_title("三个过程", pad=6)

    ax = axes[1]
    lam = np.linspace(380, 780, 300)
    r = einstein_ab_ratio(lam)
    ax.semilogy(lam, r, color=PURPLE, lw=1.8)
    for l0, dx, dy in ((400, 8, 0.46), (550, 6, 0.46), (700, -10, 0.62)):
        v = float(einstein_ab_ratio(l0))
        ax.plot([l0], [v], "o", ms=3.4, color=PURPLE)
        ax.annotate("%.2e" % v, xy=(l0, v), xytext=(l0 + dx, v * dy), fontsize=7.6,
                    color=PURPLE, ha="left")
    ax.set_xlim(380, 780)
    ax.set_ylim(2.2e-14, 1.2e-12)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("$A_{21}/B_{21}$  (J·s/m³)")
    ax.set_title("自发辐射相对受激辐射的强度，∝ ν³", pad=6)
    ax.text(470, 5.6e-13, "蓝端比红端强 5.4 倍", fontsize=8, color="#3c4654")
    fig.tight_layout()
    save(fig, "fig2-3-ab-coefficients.png")


# ------------------------------------------------------------------ 图 2-3
def fig2_3():
    """单个光子的能量与每瓦的光子数。"""
    lam = np.linspace(380, 780, 300)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))

    ax = axes[0]
    ax.plot(lam, photon_energy_ev(lam), color=TEAL, lw=1.8)
    for l0 in (400, 550, 700):
        e = float(photon_energy_ev(l0))
        ax.plot([l0], [e], "o", ms=3.4, color=TEAL)
        ax.annotate("%.2f eV" % e, xy=(l0, e), xytext=(l0 + (26 if l0 == 400 else 8), e + 0.16),
                    fontsize=8, color=TEAL)
    ax.set_xlim(380, 780)
    ax.set_ylim(1.4, 3.5)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("光子能量 $hc/\\lambda$ (eV)")
    ax.set_title("蓝光的光子更重", pad=6)

    ax = axes[1]
    n = photons_per_watt(lam) / 1e18
    ax.plot(lam, n, color=ACCENT, lw=1.8)
    ax.axhline(n.mean(), color=GREY, lw=0.9, ls=":")
    for l0 in (400, 550, 700):
        v = float(photons_per_watt(l0)) / 1e18
        ax.plot([l0], [v], "o", ms=3.4, color=ACCENT)
        ax.annotate("%.2f" % v, xy=(l0, v), xytext=(l0, v + 0.13), fontsize=8,
                    ha="center", color=ACCENT)
    ax.set_xlim(380, 780)
    ax.set_ylim(1.7, 3.9)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("光子数每秒每瓦（10¹⁸）")
    ax.set_title("同样的 1 W，光子数只差 75%", pad=6)
    fig.tight_layout()
    save(fig, "fig2-2-photon-energy.png")


fig2_1()
fig2_2()
fig2_3()
