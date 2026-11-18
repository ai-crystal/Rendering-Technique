import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

NTH, NPH = 64, 128
TH = (np.arange(NTH) + 0.5) * (np.pi / 2) / NTH
PH = (np.arange(NPH) + 0.5) * 2 * np.pi / NPH
T, P = np.meshgrid(TH, PH, indexing="ij")
WDIR = spherical(T, P)
DW = np.sin(T) * (np.pi / 2 / NTH) * (2 * np.pi / NPH)


def ggx_albedo(mu_i, alpha, f0=0.04):
    wi = np.array([np.sqrt(max(0.0, 1 - mu_i ** 2)), 0.0, mu_i])
    v = brdf_ggx(wi, WDIR, alpha, f0) * np.cos(T)
    return float(np.sum(v * DW))


def build_table(n_mu=24, n_a=24, mus=None, alphas=None):
    mus = np.linspace(0.02, 1.0, n_mu) if mus is None else mus
    alphas = np.linspace(0.02, 1.0, n_a) if alphas is None else alphas
    tab = np.array([[ggx_albedo(m, a) for a in alphas] for m in mus])
    return mus, alphas, tab


def bilinear(mus, alphas, tab, mu, a):
    i = np.clip(np.searchsorted(mus, mu) - 1, 0, len(mus) - 2)
    j = np.clip(np.searchsorted(alphas, a) - 1, 0, len(alphas) - 2)
    tm = (mu - mus[i]) / (mus[i + 1] - mus[i])
    ta = (a - alphas[j]) / (alphas[j + 1] - alphas[j])
    return ((1 - tm) * (1 - ta) * tab[i, j] + tm * (1 - ta) * tab[i + 1, j]
            + (1 - tm) * ta * tab[i, j + 1] + tm * ta * tab[i + 1, j + 1])


def fig10_1():
    mus, alphas, tab = build_table(22, 22)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0),
                             gridspec_kw={"width_ratios": [1.1, 1.0]})
    ax = axes[0]
    m = ax.pcolormesh(alphas, mus, tab, cmap="viridis", shading="auto")
    ax.set_xlabel("粗糙度 alpha")
    ax.set_ylabel("cos(theta_i)")
    ax.set_title("GGX 单次散射反照率", fontsize=9)
    cb = fig.colorbar(m, ax=ax, pad=0.02)
    cb.ax.tick_params(labelsize=7)

    rng = np.random.default_rng(7)
    ax2 = axes[1]
    for n, c in [(8, ACCENT), (16, TEAL), (32, BLUE)]:
        mus2, al2, tab2 = build_table(n, n)
        errs = []
        for _ in range(300):
            mu = rng.uniform(0.05, 1.0)
            a = rng.uniform(0.05, 0.95)
            exact = ggx_albedo(mu, a)
            approx = bilinear(mus2, al2, tab2, mu, a)
            errs.append(abs(approx - exact) / max(exact, 1e-6))
        errs = np.array(errs) * 100
        ax2.plot(sorted(errs), np.linspace(0, 1, len(errs)), color=c,
                 label="%d x %d" % (n, n))
    ax2.set_xscale("log")
    ax2.set_xlabel("相对误差（%）")
    ax2.set_ylabel("累积比例")
    ax2.set_title("双线性查表的误差分布", fontsize=9)
    ax2.legend(loc="lower right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig10-1-lut.png")


def fig10_2():
    """单次散射损失与多次散射补偿。"""
    mus = np.linspace(0.08, 1.0, 24)
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.9))
    ax = axes[0]
    ax2 = axes[1]
    for a, c in [(0.2, BLUE), (0.5, TEAL), (0.9, ACCENT)]:
        R = np.array([ggx_albedo(m, a, 1.0) for m in mus])
        ax.plot(mus, R, color=c, label="alpha = %.1f" % a)
        ax2.plot(mus, 1 - R, color=c, label="alpha = %.1f" % a)
    ax.set_xlabel("cos(theta_i)")
    ax.set_ylabel("单次散射反照率")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper left", fontsize=7.5)
    ax.set_title("单次散射", fontsize=9)
    ax2.set_xlabel("cos(theta_i)")
    ax2.set_ylabel("能量缺口 1 - R")
    ax2.set_ylim(0, 0.35)
    ax2.set_title("需要补偿的比例", fontsize=9)
    fig.tight_layout()
    save(fig, "fig10-2-compensate.png")


def fig10_3():
    """多层叠加的能量：逐层加入 fuzz 与 sheen。"""
    deg = np.linspace(0, 85, 300)
    th = np.deg2rad(deg)

    def albedo(theta):
        base = ggx_albedo(np.cos(theta), 0.35) + 0.60
        fuzz = 0.12 * (1 - np.cos(theta))
        sheen = 0.55 * (1 - np.cos(theta)) ** 4
        return base, base + fuzz, base + fuzz + sheen

    a0 = np.array([albedo(t)[0] for t in th])
    a1 = np.array([albedo(t)[1] for t in th])
    a2 = np.array([albedo(t)[2] for t in th])
    fig, ax = plt.subplots(figsize=(5.9, 3.2))
    ax.plot(deg, a0, color=BLUE, label="底层（漫反射 + 微表面）")
    ax.plot(deg, a1, color=TEAL, label="加毛羽层")
    ax.plot(deg, a2, color=ACCENT, label="再加 sheen")
    ax.axhline(1.0, color=GREY, ls=":", lw=0.9)
    ax.fill_between(deg, 1.0, a2, where=a2 > 1.0, color=RED, alpha=0.18)
    ax.set_xlabel("入射天顶角（度）")
    ax.set_ylabel("累计方向反照率")
    ax.set_xlim(0, 85)
    ax.set_ylim(0.2, 1.5)
    ax.legend(loc="upper left", fontsize=7.5)
    ax.text(0.55, 0.60, "超过 1 的部分必须压回去", transform=ax.transAxes,
            fontsize=8, color=RED)
    save(fig, "fig10-3-layers.png")


fig10_1()
fig10_2()
fig10_3()
