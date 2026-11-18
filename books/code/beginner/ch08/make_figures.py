import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180


def fig8_1():
    th = np.linspace(0, 89.9, 600)
    c = np.cos(th * D2R)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1))
    fig.subplots_adjust(wspace=0.3)

    ax = axes[0]
    R = fresnel_dielectric(c, 1.5)
    ax.plot(th, R, color=BLUE, lw=2.0)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("反射率")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.02)
    ax.text(12, 0.30, "空气到玻璃", color=BLUE, fontsize=9)
    panel_label(ax, "a")

    ax = axes[1]
    eta = 1 / 1.5
    st = np.sin(th * D2R) / 1.5
    tt = np.degrees(np.arcsin(np.clip(st, 0, 1)))
    ax.plot(th, tt, color=TEAL, lw=2.0)
    ax.plot([0, 90], [0, 90], color=LIGHT, ls="--", lw=1.0)
    tc = np.degrees(np.arcsin(1 / 1.5))
    ax.axvline(tc, color=ACCENT, ls=":", lw=1.2)
    ax.text(tc + 2, 20, "临界角 41.8°", color=ACCENT, fontsize=8.5)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("折射角（度）")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 90)
    ax.text(10, 60, "玻璃到空气", color=TEAL, fontsize=9)
    panel_label(ax, "b")
    save(fig, "fig8-1-refraction.png")


def fig8_2():
    rng = np.random.default_rng(1)
    ui = spherical(np.array([20 * D2R]), np.array([0.0]))[0]
    eta = 1 / 1.5
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    bins = np.linspace(0, 45, 90)
    for alpha, col in [(0.02, BLUE), (0.25, TEAL), (0.5, ACCENT)]:
        devs = []
        for _ in range(4000):
            u1, u2 = rng.random(2)
            h = sample_ggx_vndf(ui, u1, u2, alpha)
            ci = ui @ h
            sin2 = eta ** 2 * (1 - ci ** 2)
            if sin2 >= 1:
                continue
            ct = np.sqrt(1 - sin2)
            wo = -eta * ui + (eta * ci - ct) * h
            wo = normalize(wo)
            c = float(np.clip(np.dot(-wo, ui), -1, 1))
            devs.append(np.degrees(np.arccos(c)))
        devs = np.array(devs)
        hist, edges = np.histogram(devs, bins=bins, density=True)
        ax.plot(0.5 * (edges[1:] + edges[:-1]), hist, color=col, lw=1.8,
                label="α = %.2f，有效率 %.0f%%" % (alpha, 100 * len(devs) / 4000))
    ax.set_xlabel("出射方向与入射方向的夹角（度）")
    ax.set_ylabel("概率密度")
    ax.set_xlim(0, 45)
    ax.legend(loc="upper right", fontsize=7.5)
    save(fig, "fig8-2-rough-transmission.png")


fig8_1()
fig8_2()
