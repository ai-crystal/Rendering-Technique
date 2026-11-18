import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()


# ------------------------------------------------------------------ 图 9-1
def fig9_1():
    """四种玻璃的折射率曲线。"""
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    styles = [("N-BK7", BLUE), ("F2", TEAL), ("SF11", ACCENT), ("熔石英", GREEN)]
    for name, col in styles:
        nd, vd = abbe(name)
        ax.plot(LAM, sellmeier(name, LAM), color=col, lw=1.7,
                label="%s（$n_d$=%.4f，$V_d$=%.1f）" % (name, nd, vd))
    ax.set_xlim(380, 780)
    ax.set_ylim(1.43, 1.84)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("折射率 n(λ)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2,
              fontsize=7.6, columnspacing=1.4)
    ax.set_title("折射率随波长下降，短波端更陡", pad=6)
    save(fig, "fig9-1-ior.png")


# ------------------------------------------------------------------ 图 9-2
def fig9_2():
    """单界面：菲涅耳曲线，以及布儒斯特角与临界角随波长的移动。"""
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1), gridspec_kw={"wspace": 0.30})

    ax = axes[0]
    th = np.linspace(0, 89.5, 500)
    n = float(sellmeier("N-BK7", 550.0))
    ci, si = np.cos(np.deg2rad(th)), np.sin(np.deg2rad(th))
    ct = np.sqrt(np.maximum(1 - (si / n) ** 2, 0))
    rs = ((ci - n * ct) / (ci + n * ct)) ** 2
    rp = ((n * ci - ct) / (n * ci + ct)) ** 2
    ax.plot(th, rs, color=BLUE, lw=1.7, label="$R_s$")
    ax.plot(th, rp, color=ACCENT, lw=1.7, label="$R_p$")
    th_b = np.degrees(np.arctan(n))
    ax.axvline(th_b, color=GREY, lw=0.9, ls=":")
    ax.text(th_b + 1.5, 0.55, "布儒斯特角\n%.1f°" % th_b, fontsize=7.6, color="#666")
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("反射率")
    ax.set_xlim(0, 89)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="upper left")
    ax.set_title("空气到 N-BK7（550 nm）", pad=6)

    ax2 = axes[1]
    lam = np.linspace(400, 700, 80)
    for name, col in [("N-BK7", BLUE), ("SF11", ACCENT)]:
        n = sellmeier(name, lam)
        tb = np.degrees(np.arctan(n))
        tc = np.degrees(np.arcsin(1.0 / n))
        ax2.plot(lam, tb - np.interp(550, lam, tb), color=col, lw=1.7,
                 label="%s 布儒斯特角" % name)
        ax2.plot(lam, tc - np.interp(550, lam, tc), color=col, lw=1.4, ls="--",
                 label="%s 临界角" % name)
    ax2.axhline(0, color=LIGHT, lw=0.8)
    ax2.set_xlabel("波长 λ (nm)")
    ax2.set_ylabel("相对 550 nm 的角度变化（度）")
    ax2.set_xlim(400, 700)
    ax2.legend(loc="upper left", fontsize=7.2)
    ax2.set_title("两个特征角的波长依赖", pad=6)
    save(fig, "fig9-2-fresnel.png")


# ------------------------------------------------------------------ 图 9-3
def fig9_3():
    """球透镜的纵向色差。"""
    R = 10.0
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    for name, col in [("N-BK7", BLUE), ("SF11", ACCENT)]:
        n = sellmeier(name, LAM)
        f = n * R / (2 * (n - 1))
        f0 = np.interp(550, LAM, f)
        ax.plot(LAM, f - f0, color=col, lw=1.8, label="%s" % name)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlim(380, 780)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("焦距相对 550 nm 的偏移 (mm)")
    ax.legend(loc="lower right")
    ax.set_title("半径 10 mm 的玻璃球，蓝光焦点更近", pad=6)
    save(fig, "fig9-3-balllens.png")


fig9_1()
fig9_2()
fig9_3()
