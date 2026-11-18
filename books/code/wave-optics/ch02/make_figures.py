import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *

LAM0 = 550.0


def coherent(dL_nm, dlam_nm, lam0=LAM0):
    """高斯型谱线的复相干度模，dL 用纳米。gamma(dL)=exp(-2 pi^2 sigma_nu^2 tau^2)。"""
    # 波长标准差 -> 频率标准差：sigma_nu = c sigma_lam / lam^2
    sigma_lam = dlam_nm / (2 * np.sqrt(2 * np.log(2))) * 1e-9
    sigma_nu = 3e8 * sigma_lam / (lam0 * 1e-9) ** 2
    tau = dL_nm * 1e-9 / 3e8
    return np.exp(-2 * np.pi ** 2 * sigma_nu ** 2 * tau ** 2)


def fig2_1():
    dL = np.linspace(-5000, 5000, 4000)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for dlam, col, lab in [(2, BLUE, "谱宽 2 nm"), (30, ACCENT, "谱宽 30 nm"),
                           (120, TEAL, "谱宽 120 nm")]:
        g = coherent(dL, dlam)
        ax.plot(dL, g * (1 + np.cos(2 * np.pi * dL / LAM0)), color=col, lw=1.3, label=lab)
    ax.set_xlim(-4500, 4500)
    ax.set_ylim(0, 2.15)
    ax.set_yticks([0, 1, 2])
    ax.set_xlabel("光程差（nm）")
    ax.set_ylabel("归一化强度")
    ax.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.16), fontsize=8)
    save(fig, "fig2-1-envelope.png")


def fig2_2():
    dL = np.logspace(-1, 6, 1500)
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    src = [("太阳光　带宽 300 nm", 300, GOLD), ("白光 LED　带宽 25 nm", 25, BLUE),
           ("钠灯　带宽 0.6 nm", 0.6, TEAL), ("氦氖激光　带宽 0.001 nm", 0.001, RED)]
    for lab, dlam, col in src:
        ax.semilogx(dL, coherent(dL, dlam), color=col, lw=1.8, label=lab)
    for x, lab in [(1.0, "1 微米"), (12, "12 微米"), (5e2, "0.5 毫米")]:
        ax.axvline(x, color=LIGHT, lw=0.9, ls=":")
        ax.text(x * 1.15, 1.03, lab, fontsize=7.5, color=GREY)
    ax.set_xlim(0.1, 1e6)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel("光程差（nm）")
    ax.set_ylabel("相干度")
    ax.legend(loc="lower left", fontsize=7.5)
    save(fig, "fig2-2-coherence.png")


def airy_R(lam_nm, d_nm, n1=2.3):
    lam = lam_nm * 1e-9
    d = d_nm * 1e-9
    r01 = (1 - n1) / (1 + n1)
    r12 = (n1 - 1.5) / (n1 + 1.5)
    ph = np.exp(2j * 2 * np.pi * n1 * d / lam)
    r = (r01 + r12 * ph) / (1 + r01 * r12 * ph)
    return np.abs(r) ** 2


def fig2_3():
    lam = np.linspace(380, 780, 2000)
    R = airy_R(lam, 900, 2.3)
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    ax.plot(lam, R, color=INK, lw=0.9, alpha=0.55, label="单色计算")
    for dlam, col in [(2, BLUE), (20, ACCENT), (80, TEAL)]:
        sig = dlam / (2 * np.sqrt(2 * np.log(2)))
        Rs = np.zeros_like(R)
        w = np.exp(-0.5 * ((lam[:, None] - lam[None, :]) / sig) ** 2)
        Rs = (w @ R) / w.sum(axis=1)
        ax.plot(lam, Rs, color=col, lw=1.9, label="带宽 %d nm" % dlam)
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 0.40)
    ax.set_xlabel("波长（nm）")
    ax.set_ylabel("反射率")
    ax.legend(loc="upper center", ncol=4, fontsize=8, bbox_to_anchor=(0.5, 1.15))
    save(fig, "fig2-3-bandwidth.png")


fig2_1()
fig2_2()
fig2_3()
