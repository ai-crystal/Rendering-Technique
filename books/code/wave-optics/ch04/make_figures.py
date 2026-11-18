import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def r_signed(n0, n1, n2):
    r01 = (n0 - n1) / (n0 + n1)
    r12 = (n1 - n2) / (n1 + n2)
    return r01, r12


def refl(lam, d, n0, n1, n2):
    r01 = (n0 - n1) / (n0 + n1)
    r12 = (n1 - n2) / (n1 + n2)
    delta = 4 * np.pi * n1 * d / lam
    r = (r01 + r12 * np.exp(1j * delta)) / (1 + r01 * r12 * np.exp(1j * delta))
    return np.abs(r) ** 2


def fig4_1():
    d = np.linspace(0, 900, 1400)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for lam, col, lab in [(450, BLUE, "450 nm"), (550, ACCENT, "550 nm"),
                          (650, TEAL, "650 nm")]:
        ax.plot(d, refl(lam, d, 1.0, 2.3, 1.52) * 100, color=col, lw=1.8, label=lab)
    ax.set_xlim(0, 900)
    ax.set_ylim(0, 34)
    ax.set_xlabel("膜厚（nm）")
    ax.set_ylabel("反射率（%）")
    ax.legend(loc="upper center", ncol=3, fontsize=8, bbox_to_anchor=(0.5, 1.17))
    ax.annotate("d = 0 时回到裸玻璃的 4.1%", xy=(8, 4.1), xytext=(150, 13),
                fontsize=8, color=GREY,
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.9))
    save(fig, "fig4-1-thickness.png")


def fig4_2():
    delta = np.linspace(0, 4 * np.pi, 3000)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for Rf, col, lab in [(0.04, BLUE, "R = 0.04"), (0.30, TEAL, "R = 0.30"),
                         (0.70, GOLD, "R = 0.70"), (0.90, RED, "R = 0.90")]:
        F = 4 * Rf / (1 - Rf) ** 2
        T = 1 / (1 + F * np.sin(delta / 2) ** 2)
        ax.plot(delta / (2 * np.pi), T, color=col, lw=1.7, label=lab)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1.06)
    ax.set_xlabel("相位差 / 2π（自由光谱范围）")
    ax.set_ylabel("透射率")
    ax.legend(loc="upper center", fontsize=8, ncol=4, bbox_to_anchor=(0.5, 1.17),
              title="界面反射率", title_fontsize=8)
    save(fig, "fig4-2-airy.png")


def fig4_3():
    lam = np.linspace(400, 700, 900)
    d = 550 / (4 * 1.38)
    di = 550 / (4 * 1.2332)
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    ax.plot(lam, refl(lam, 0, 1.0, 1.0, 1.52) * 100, color=GREY, lw=1.5, label="裸玻璃")
    ax.plot(lam, refl(lam, d, 1.0, 1.38, 1.52) * 100, color=BLUE, lw=1.9,
            label="氟化镁 100 nm")
    ax.plot(lam, refl(lam, di, 1.0, 1.2332, 1.52) * 100, color=ACCENT, lw=1.7,
            ls="--", label="理想折射率 1.233")
    for y, col, txt in [(refl(lam, 0, 1.0, 1.0, 1.52).mean() * 100, GREY, ""),
                        (refl(lam, d, 1.0, 1.38, 1.52).mean() * 100, BLUE, "")]:
        ax.axhline(y, color=col, lw=0.9, ls=":")
    ax.set_xlim(400, 700)
    ax.set_ylim(0, 5)
    ax.set_xlabel("波长（nm）")
    ax.set_ylabel("反射率（%）")
    ax.legend(loc="upper left", fontsize=8)
    ax.text(430, 3.15, "点线为 400 至 700 nm 的平均值", fontsize=7.5, color=GREY)
    save(fig, "fig4-3-ar.png")


fig4_1()
fig4_2()
fig4_3()
