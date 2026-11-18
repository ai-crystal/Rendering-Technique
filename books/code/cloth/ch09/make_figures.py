import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *


def km_reflectance(KS, Sd, Rg=0.0):
    """Kubelka–Munk 两流解：厚度 S*d、背景 Rg 时的反射率。"""
    KS = np.asarray(KS, dtype=float)
    Sd = np.asarray(Sd, dtype=float)
    out = np.empty(np.broadcast(KS, Sd).shape)
    ks, sd = np.broadcast_arrays(KS, Sd)
    tiny = ks < 1e-7
    out[tiny] = sd[tiny] / (1.0 + sd[tiny] * (1.0 - Rg) / max(1e-9, 1.0))
    a = 1.0 + ks[~tiny]
    b = np.sqrt(np.maximum(a ** 2 - 1.0, 0.0))
    L = b * sd[~tiny]
    num = -(a - b - Rg) * np.exp(-L)
    den = (a + b - Rg) * np.exp(L) - (a - b - Rg) * np.exp(-L)
    A = num / np.where(np.abs(den) < 1e-30, 1e-30, den)
    out[~tiny] = (a - b) + 2 * b * A
    return out


def fig9_1():
    ks = np.logspace(-2.2, 1.2, 400)
    fig, ax = plt.subplots(figsize=(5.9, 3.2))
    ax.semilogx(ks, ks / (1 + ks) * 0 + (1 + ks) - np.sqrt((1 + ks) ** 2 - 1),
                color=INK, lw=1.6, label="无限厚 $R_\\infty$")
    for sd, c in [(0.5, BLUE), (2.0, TEAL), (6.0, ACCENT)]:
        ax.semilogx(ks, km_reflectance(ks, sd), color=c, ls="--",
                    label="厚度 $Sd=%.1f$" % sd)
    ax.set_xlabel("吸收与散射之比 K/S")
    ax.set_ylabel("反射率")
    ax.set_xlim(1e-2, 15)
    ax.set_ylim(0, 1.0)
    ax.legend(loc="upper right", fontsize=7.5)
    ax.annotate("厚度越大越接近无限厚曲线", xy=(0.15, 0.42), xytext=(0.35, 0.18),
                fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
    save(fig, "fig9-1-rmax.png")


def fig9_2():
    r = np.linspace(0.03, 0.95, 500)
    ks = (1 - r) ** 2 / (2 * r)
    sens = (1 - r ** 2) / (2 * r ** 2)
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.0))
    ax = axes[0]
    ax.loglog(r, ks, color=ACCENT)
    ax.set_xlabel("测得的反射率 R")
    ax.set_ylabel("反推的 K/S")
    ax.set_title("反推关系", fontsize=9)
    ax2 = axes[1]
    ax2.loglog(r, sens, color=BLUE)
    ax2.set_xlabel("测得的反射率 R")
    ax2.set_ylabel("误差放大倍数")
    ax2.set_title("反射率 1% 的误差对应的 K/S 误差", fontsize=9)
    ax2.annotate("R = 0.9 时 0.12 倍", xy=(0.9, 0.12), xytext=(0.35, 0.03), fontsize=8,
                 color="#3c4654", arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
    fig.tight_layout()
    save(fig, "fig9-2-inverse.png")


def fig9_3():
    lam = np.linspace(400, 700, 400)
    k0 = 2.4 * np.exp(-0.5 * ((lam - 445) / 55.0) ** 2)
    fig, ax = plt.subplots(figsize=(5.9, 3.2))
    for c, col, lab in [(0.4, "#d9a441", "浅染（0.4）"),
                        (1.0, "#c1741f", "中染（1.0）"),
                        (2.4, "#8a4a12", "深染（2.4）")]:
        R = km_reflectance(c * k0, 3.0)
        ax.plot(lam, R, color=col, label=lab)
    ax.set_xlabel("波长（纳米）")
    ax.set_ylabel("反射率")
    ax.set_xlim(400, 700)
    ax.set_ylim(0, 1.0)
    ax.legend(loc="upper left", fontsize=8)
    ax.text(0.52, 0.82, "染料吸收带在 445 纳米", transform=ax.transAxes,
            fontsize=8, color="#3c4654")
    save(fig, "fig9-3-spectrum.png")


fig9_1()
fig9_2()
fig9_3()
