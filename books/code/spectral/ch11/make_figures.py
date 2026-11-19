import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()
LO, HI = 380.0, 780.0
N = 4
STEP = (HI - LO) / N


# ------------------------------------------------------------------ 图 11-1
def fig7_1():
    """hero wavelength：每组 n 个波长等间隔，整组随 hero 平移。"""
    rng = np.random.default_rng(5)
    rows = 14
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    for r in range(rows):
        hero = rng.uniform(LO, HI)
        ls = LO + np.mod(hero - LO + np.arange(N) * STEP, HI - LO)
        ax.plot([LO, HI], [r, r], color=LIGHT, lw=0.6, zorder=0)
        ax.plot(ls, np.full(N, r), "o", color=PALETTE[r % 4], ms=4.2, zorder=2)
        ax.plot([ls.min(), ls.max()], [r, r], color=PALETTE[r % 4], lw=1.0, alpha=0.45, zorder=1)
    ax.set_xlim(LO, HI)
    ax.set_ylim(-0.8, rows - 0.2)
    ax.set_yticks([])
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("路径编号")
    ax.grid(False)
    ax.text(392, rows - 0.9, "每组 4 个波长，间距 100 nm，越过上界后绕回下界",
            fontsize=8, color="#3c4654")
    save(fig, "fig11-1-hero.png")


# ------------------------------------------------------------------ 图 11-2
def fig7_2():
    """次级波长的概率密度是 hero 密度的平移。"""
    def dens(lam, mu=550.0, sg=60.0):
        return np.exp(-0.5 * ((lam - mu) / sg) ** 2) / (sg * np.sqrt(2 * np.pi))

    fig, ax = plt.subplots(figsize=(6.4, 3.1))
    ax.plot(LAM, dens(LAM), color=ACCENT, lw=1.8, label=r"$p_0(\lambda)$：hero 的密度")
    ax.plot(LAM, dens(LAM - 100.0), color=BLUE, lw=1.8, ls="--",
            label=r"$p_1(\lambda)=p_0(\lambda-100)$")
    peak = float(dens(550.0))
    ax.plot([550.0], [peak], "o", color=ACCENT, ms=5, zorder=3)
    ax.plot([650.0], [peak], "o", color=BLUE, ms=5, zorder=3)
    ax.annotate("", xy=(650, peak), xytext=(550, peak),
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=GREY, ls=":"))
    ax.text(560, peak * 1.06, "+100 nm", fontsize=7.8, color="#666")
    ax.text(544, peak * 0.55, r"$p_0(\lambda_0)$", fontsize=8, color=ACCENT, ha="right")
    ax.text(624, peak * 0.22, r"$p_1(\lambda_1)=p_0(\lambda_0)$", fontsize=8,
            color=BLUE, ha="left")
    ax.set_xlim(380, 780)
    ax.set_ylim(0, peak * 1.35)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("概率密度 (1/nm)")
    ax.legend(loc="upper left")
    save(fig, "fig11-2-pdf-shift.png")


# ------------------------------------------------------------------ 图 11-3
def _refract(d, n, eta):
    cosi = -np.dot(d, n)
    if cosi < 0:
        n, cosi, eta = -n, -np.dot(d, n), 1.0 / eta
    k = 1 - eta ** 2 * (1 - cosi ** 2)
    if k < 0:
        return None
    return eta * d + (eta * cosi - np.sqrt(k)) * n


def fig7_3():
    """色散让两个波长折射到不同方向。"""
    fig = plt.figure(figsize=(7.0, 3.1))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.0], wspace=0.32)

    ax = fig.add_subplot(gs[0])
    thetas = np.linspace(0, 80, 200)
    for name, col in [("N-BK7", BLUE), ("SF11", ACCENT)]:
        spread = []
        for th in thetas:
            d = np.array([np.sin(np.deg2rad(th)), -np.cos(np.deg2rad(th))])
            nrm = np.array([0.0, 1.0])
            d1 = _refract(d, nrm, 1.0 / float(sellmeier(name, 450)))
            d2 = _refract(d, nrm, 1.0 / float(sellmeier(name, 650)))
            if d1 is None or d2 is None:
                spread.append(np.nan)
                continue
            ang = np.degrees(np.arccos(np.clip(np.dot(d1, d2), -1, 1)))
            spread.append(ang)
        ax.plot(thetas, spread, color=col, lw=1.7, label=name)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("450 nm 与 650 nm 折射方向夹角（度）")
    ax.set_xlim(0, 80)
    ax.legend(loc="upper right")
    ax.set_title("单次折射的方向分离", pad=6)

    ax2 = fig.add_subplot(gs[1])
    # 60 度等边棱镜：两个界面各折射一次，出射方向的色散角随入射角变化
    A = np.deg2rad(64.0)
    nL = np.array([-np.cos(A / 2), np.sin(A / 2)])
    nR = np.array([np.cos(A / 2), np.sin(A / 2)])
    ang_in = np.linspace(25, 75, 120)
    for name, col in [("N-BK7", BLUE), ("SF11", ACCENT)]:
        spread = []
        for th in ang_in:
            outs = []
            for lam_nm in (400.0, 700.0):
                n = float(sellmeier(name, lam_nm))
                d = np.array([np.sin(np.deg2rad(th)), -np.cos(np.deg2rad(th))])
                d1 = _refract(d, nL, 1.0 / n)
                if d1 is None:
                    outs.append(np.nan)
                    continue
                d2 = _refract(d1, nR, n)
                if d2 is None:
                    outs.append(np.nan)
                    continue
                outs.append(np.degrees(np.arctan2(d2[1], d2[0])))
            spread.append(abs(outs[0] - outs[1]))
        ax2.plot(ang_in, spread, color=col, lw=1.7, label=name)
    n_d = float(sellmeier("N-BK7", 587.6))
    th_min = np.degrees(np.arcsin(n_d * np.sin(A / 2)))
    ax2.axvline(th_min, color=GREY, lw=0.9, ls=":")
    ax2.text(th_min + 1.6, 0.95, "最小偏向角\n入射角 %.0f°" % th_min, fontsize=7.4, color="#666")
    ax2.set_xlabel("棱镜入射角（度）")
    ax2.set_ylabel("400 与 700 nm 的偏向角之差（度）")
    ax2.set_xlim(25, 75)
    ax2.set_ylim(0, 1.15)
    ax2.legend(loc="lower left")
    ax2.set_title("整块棱镜的色散角", pad=6)
    save(fig, "fig11-3-dispersion.png")


fig7_1()
fig7_2()
fig7_3()
