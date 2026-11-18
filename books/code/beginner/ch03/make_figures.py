import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180


def fresnel_sp(cos_i, eta):
    cos_i = np.clip(cos_i, 0, 1)
    sin2 = (1 - cos_i ** 2) / eta ** 2
    tir = sin2 >= 1
    cos_t = np.sqrt(np.clip(1 - sin2, 0, 1))
    rs = (cos_i - eta * cos_t) / np.maximum(cos_i + eta * cos_t, 1e-9)
    rp = (eta * cos_i - cos_t) / np.maximum(eta * cos_i + cos_t, 1e-9)
    return np.where(tir, 1, rs ** 2), np.where(tir, 1, rp ** 2)


def fig3_1():
    th = np.linspace(0, 89.9, 600)
    c = np.cos(th * D2R)
    Rs, Rp = fresnel_sp(c, 1.5)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2))
    fig.subplots_adjust(wspace=0.36)

    ax = axes[0]
    ax.plot(th, Rs, color=BLUE, label="$R_s$")
    ax.plot(th, Rp, color=ACCENT, label="$R_p$")
    ax.plot(th, 0.5 * (Rs + Rp), color=INK, lw=2.0, label="非偏振平均")
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("反射率")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="upper left")
    tb = np.degrees(np.arctan(1.5))
    ax.axvline(tb, color=GREY, ls=":", lw=1.0)
    ax.annotate("布儒斯特角 56.3°", xy=(tb, 0.06), xytext=(tb - 34, 0.30),
                fontsize=8, color=GREY,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    panel_label(ax, "a")

    ax = axes[1]
    tt = np.linspace(0, 89.9, 600)
    st = np.clip(1.5 * np.sin(tt * D2R), 0, 1)
    ang_t = np.degrees(np.arcsin(st))
    ax.plot(tt, ang_t, color=TEAL, lw=2.0)
    ax.plot([0, 90], [0, 90], color=LIGHT, ls="--", lw=1.0)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("折射角（度）")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 90)
    ax.text(30, 66, "空气到玻璃", color=TEAL, fontsize=9)
    ax.text(62, 60, "无折射时", color=GREY, fontsize=8)
    panel_label(ax, "b")
    save(fig, "fig3-1-fresnel.png")


def fig3_2():
    th = np.linspace(0, 89.9, 600)
    c = np.clip(np.cos(th * D2R), 0, 1)
    Rs, Rp = fresnel_sp(c, 1.5)
    F = 0.5 * (Rs + Rp)
    S = fresnel_schlick(c, 0.04)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2))
    fig.subplots_adjust(wspace=0.36)

    ax = axes[0]
    ax.plot(th, F, color=BLUE, lw=2.2, label="精确 Fresnel")
    ax.plot(th, S, color=ACCENT, lw=1.6, ls="--", label="Schlick 近似")
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("反射率")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="upper left")
    panel_label(ax, "a")

    ax = axes[1]
    ax.plot(th, F - S, color=RED, lw=1.8)
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("误差")
    ax.set_xlim(0, 90)
    i = np.argmax(np.abs(F - S))
    ax.annotate(f"最大偏差 {abs(F-S)[i]:.3f}\n在 {th[i]:.0f}°", xy=(th[i], (F - S)[i]),
                xytext=(40, -0.022), fontsize=8, color=RED,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.8))
    panel_label(ax, "b")
    save(fig, "fig3-2-schlick-error.png")


def fig3_3():
    # 550 nm 处的复折射率（Johnson & Christy 1972）
    metals = [("金 Au", 0.47, 2.40), ("铜 Cu", 0.88, 2.42), ("铝 Al", 0.96, 6.70)]
    th = np.linspace(0, 89.9, 600)
    c = np.clip(np.cos(th * D2R), 0, 1)
    fig, ax = plt.subplots(figsize=(5.4, 3.3))
    for (name, n, k), col in zip(metals, [GOLD, ACCENT, BLUE]):
        R = fresnel_conductor(c, n, k)
        f0 = (n - 1) ** 2 + k ** 2
        f0 = f0 / ((n + 1) ** 2 + k ** 2)
        ax.plot(th, R, color=col, lw=2.0, label=f"{name}，$F_0={f0:.2f}$")
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("反射率")
    ax.set_xlim(0, 90)
    ax.set_ylim(0.3, 1.02)
    ax.legend(loc="lower right")
    save(fig, "fig3-3-metal-fresnel.png")


fig3_1()
fig3_2()
fig3_3()
