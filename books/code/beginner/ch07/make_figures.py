import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180
T, P, domega = hemisphere_grid(90, 180)
W = spherical(T, P)
COSO = np.cos(T)


def E_of(mu, alpha, G2=True):
    wi = np.array([np.sqrt(max(0.0, 1 - mu ** 2)), 0.0, mu])
    h = normalize(wi + W)
    ci, co = mu, np.clip(W[..., 2], 0, 1)
    D = d_ggx(h[..., 2], alpha)
    G = g2_smith(ci, co, alpha)
    spec = np.where(co > 0, D * G / np.maximum(4 * ci * co, EPS), 0.0)
    return float(np.sum(spec * COSO * domega))


def fig7_1():
    mus = np.cos(np.linspace(2, 88, 22) * D2R)
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    for alpha, col in [(0.2, BLUE), (0.4, TEAL), (0.6, ACCENT), (0.8, PURPLE), (1.0, RED)]:
        E = [E_of(m, alpha) for m in mus]
        ax.plot(np.degrees(np.arccos(np.clip(mus, 0, 1))), E, color=col, marker="o", ms=3,
                lw=1.6, label="α = %.1f" % alpha)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("方向反照率（F 取 1）")
    ax.set_xlim(0, 90)
    ax.set_ylim(0.4, 1.02)
    ax.axhline(1.0, color=GREY, ls="--", lw=1.0)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=5, fontsize=7.5)
    save(fig, "fig7-1-white-furnace.png")


def fig7_2():
    mus = np.cos(np.linspace(2, 88, 22) * D2R)
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    for alpha, col in [(0.4, TEAL), (0.8, ACCENT)]:
        E = np.array([E_of(m, alpha) for m in mus])
        Eavg = float(np.sum(E * mus) / np.sum(mus))
        comp = E + (1 - E) * (1 - 1) + (1 - E)  # 单项补偿后总量回到 1
        ang = np.degrees(np.arccos(np.clip(mus, 0, 1)))
        ax.plot(ang, E, color=col, lw=1.5, ls="--", label="单次散射 α = %.1f" % alpha)
        ax.plot(ang, np.minimum(comp, 1.0), color=col, lw=2.2,
                label="加补偿 α = %.1f" % alpha)
    ax.axhline(1.0, color=GREY, ls=":", lw=1.0)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("总反射率")
    ax.set_xlim(0, 90)
    ax.set_ylim(0.4, 1.06)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=7.5)
    save(fig, "fig7-2-compensated.png")


def fig7_3():
    f = np.linspace(0.04, 0.99, 200)
    fig, ax = plt.subplots(figsize=(5.0, 3.1))
    for eavg, col, lab in [(0.6, ACCENT, "E_avg = 0.6"), (0.8, TEAL, "E_avg = 0.8")]:
        mult = f ** 2 * eavg / (1 - f * (1 - eavg))
        ax.plot(f, mult, color=col, lw=1.9, label=lab)
    ax.set_xlabel("平均 Fresnel 反射率 F_avg")
    ax.set_ylabel("多次散射项的额外倍率")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc="upper left")
    ax.text(0.12, 0.12, "电介质 F_avg 约 0.05", color=GREY, fontsize=8)
    ax.text(0.55, 0.12, "金属 F_avg 可达 0.9", color=GREY, fontsize=8)
    save(fig, "fig7-3-saturation.png")


fig7_1()
fig7_2()
fig7_3()
