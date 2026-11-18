import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

SHEEN_NORM = 42.0 / (2 * np.pi)      # int_0^{pi/2} 42/(2pi) (1-c)^5 c dc * 2pi = 1


def sheen_lobe(theta_o, n=5):
    """掠射方向的 sheen 瓣，形状为 (1-cos)^n，按 int f cos domega = 1 归一化。"""
    from math import gamma
    # int_0^1 (1-c)^n c dc = 1/((n+1)(n+2))
    norm = ((n + 1) * (n + 2)) / (2 * np.pi)
    return norm * (1.0 - np.cos(theta_o)) ** n


def integrate(fn, theta_i, n=200, m=400):
    th = (np.arange(n) + 0.5) * (np.pi / 2) / n
    ph = (np.arange(m) + 0.5) * 2 * np.pi / m
    T, P = np.meshgrid(th, ph, indexing="ij")
    W = spherical(T, P)
    wi = spherical(theta_i, 0.0)
    v = fn(wi, W) * np.cos(T)
    dw = np.sin(T) * (np.pi / 2 / n) * (2 * np.pi / m)
    return float(np.sum(v * dw))


def base_albedo(theta_i, rho=0.35, alpha=0.30, f0=0.04):
    lam = rho
    ggx = integrate(lambda wi, wo: brdf_ggx(wi, wo, alpha, f0), theta_i)
    return lam + ggx


def fig6_1():
    """sheen 瓣的形状随幂次变化。"""
    th = np.deg2rad(np.linspace(0, 89, 700))
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    for n, c in [(2, BLUE), (5, TEAL), (10, ACCENT)]:
        ax.semilogy(np.rad2deg(th), sheen_lobe(th, n) / sheen_lobe(np.deg2rad(89), n),
                    color=c, label="$n=%d$" % n)
    ax.set_xlabel("出射天顶角（度）")
    ax.set_ylabel("归一化强度（对数）")
    ax.set_xlim(0, 89)
    ax.set_ylim(1e-3, 1.3)
    ax.legend(loc="lower right")
    ax.text(0.05, 0.15, "峰值在掠射端，宽度由幂次控制", transform=ax.transAxes,
            fontsize=8, color="#3c4654")
    save(fig, "fig6-1-sheen-lobe.png")


def fig6_2():
    """有无 sheen 的视角亮度曲线。"""
    deg = np.linspace(0, 89, 700)
    th = np.deg2rad(deg)
    L = np.array([0.0, 0.0, 1.0])
    base, full = [], []
    for t in th:
        V = spherical(np.array([t]), 0.0)[0]
        b = 0.35 + float(brdf_ggx(L, V, 0.30, 0.04))
        base.append(b)
        full.append(b + 0.55 * sheen_lobe(t))
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.semilogy(deg, base, color=BLUE, label="漫反射 + GGX（无 sheen）")
    ax.semilogy(deg, full, color=ACCENT, label="再加 sheen 项")
    ax.set_xlabel("视线与法线夹角（度）")
    ax.set_ylabel("相对亮度（对数）")
    ax.set_xlim(0, 89)
    ax.set_ylim(0.2, 3.0)
    ax.legend(loc="upper left")
    ax.annotate("掠射端抬升一个数量级以上", xy=(87, 1.05), xytext=(30, 0.26),
                fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
    save(fig, "fig6-2-sheen-view.png")


def fig6_3():
    """基础层反照率与 sheen 强度之和的上限。"""
    s = np.linspace(0, 1.0, 200)
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    for deg, c in [(0, BLUE), (45, TEAL), (75, ACCENT)]:
        R = base_albedo(np.deg2rad(deg))
        ax.plot(s, R + s, color=c, label="入射角 %d 度（基础 %.2f）" % (deg, R))
        smax = 1.0 - R
        if smax < 1.0:
            ax.plot([smax], [1.0], "o", color=c, ms=4)
    ax.axhline(1.0, color=GREY, ls=":", lw=1.0)
    ax.set_xlabel("sheen 强度 s")
    ax.set_ylabel("总方向反照率")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0.3, 1.8)
    ax.legend(loc="lower right", fontsize=7.5)
    ax.text(0.04, 0.93, "圆点为能量上限 s = 1 - R", transform=ax.transAxes,
            fontsize=8, color="#3c4654", va="top")
    save(fig, "fig6-3-sheen-energy.png")


fig6_1()
fig6_2()
fig6_3()
