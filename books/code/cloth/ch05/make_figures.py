import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *


def d_sphere_gauss(theta, sigma, norm_cos=True):
    """球面高斯。norm_cos=True 时满足 int D(h) cos(theta) domega = 1。"""
    D = np.exp(-0.5 * (theta / sigma) ** 2) / (2 * np.pi * sigma ** 2)
    if norm_cos:
        return D
    return D / np.clip(np.cos(theta), 1e-3, 1.0)


def flake_brdf(wi, wo, sigma, f0=1.0, norm_cos=True, use_g=True):
    ci = np.clip(wi[..., 2], 1e-4, 1.0)
    co = np.clip(wo[..., 2], 1e-4, 1.0)
    h = wi + wo
    h = h / np.linalg.norm(h, axis=-1, keepdims=True)
    th = np.arccos(np.clip(h[..., 2], -1, 1))
    D = d_sphere_gauss(th, sigma, norm_cos)
    G = g2_smith(ci, co, sigma) if use_g else 1.0
    F = fresnel_schlick(np.clip(np.sum(wi * h, axis=-1), 0, 1), f0)
    return np.where((wi[..., 2] > 0) & (wo[..., 2] > 0), F * D * G / (4 * ci * co), 0.0)


def albedo(theta_i, sigma, f0=1.0, norm_cos=True, use_g=True, n=120, m=240):
    th = (np.arange(n) + 0.5) * (np.pi / 2) / n
    ph = (np.arange(m) + 0.5) * 2 * np.pi / m
    T, P = np.meshgrid(th, ph, indexing="ij")
    W = spherical(T, P)
    wi = spherical(theta_i, 0.0)
    v = flake_brdf(wi, W, sigma, f0, norm_cos, use_g) * np.cos(T)
    dw = np.sin(T) * (np.pi / 2 / n) * (2 * np.pi / m)
    return np.sum(v * dw)


def fig5_1():
    """微面片法线分布与对应的反射瓣宽度。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.0))
    ax = axes[0]
    th = np.deg2rad(np.linspace(0, 60, 600))
    for s, c in [(np.deg2rad(8), BLUE), (np.deg2rad(15), TEAL), (np.deg2rad(25), ACCENT)]:
        ax.plot(np.rad2deg(th), d_sphere_gauss(th, s) / d_sphere_gauss(0, s),
                color=c, label="$\\sigma=%.0f$ 度" % np.rad2deg(s))
    ax.set_xlabel("面片法线与纱线法线的夹角（度）")
    ax.set_ylabel("归一化密度")
    ax.set_xlim(0, 60)
    ax.legend(loc="upper right")
    ax.set_title("面片朝向分布", fontsize=9)

    ax2 = axes[1]
    sig = np.deg2rad(np.linspace(3, 35, 120))
    fw = 2 * np.rad2deg(sig) * np.sqrt(2 * np.log(2))
    ax2.plot(np.rad2deg(sig), fw, color=ACCENT)
    ax2.set_xlabel("面片分布宽度（度）")
    ax2.set_ylabel("反射瓣半高全宽（度）")
    ax2.set_title("由面片分布得到的反射瓣", fontsize=9)
    ax2.set_xlim(3, 35)
    fig.tight_layout()
    save(fig, "fig5-1-flake.png")


def fig5_2():
    """遮蔽项对方向反照率的影响。"""
    deg = np.array([0, 15, 30, 45, 60, 70, 80, 85])
    sig = np.deg2rad(14)
    r1 = [albedo(np.deg2rad(d), sig, 1.0, True, True) for d in deg]
    r2 = [albedo(np.deg2rad(d), sig, 1.0, True, False) for d in deg]
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    ax.plot(deg, r1, "o-", color=BLUE, ms=4, label="含 Smith 遮蔽")
    ax.plot(deg, r2, "s--", color=RED, ms=4, label="省略遮蔽项")
    ax.axhline(1.0, color=GREY, lw=0.9, ls=":")
    ax.set_xlabel("入射天顶角（度）")
    ax.set_ylabel("方向反照率")
    ax.set_ylim(0.4, 1.7)
    ax.legend(loc="upper left", fontsize=8)
    ax.annotate("掠射时超出 1", xy=(82, 1.12), xytext=(52, 1.45), fontsize=8, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
    save(fig, "fig5-3-albedo.png")


def fig5_3():
    """纱线法线分布、叠加绒毛、以及定向毛羽对分布的影响。"""
    th = np.deg2rad(np.linspace(-80, 80, 900))
    core = np.exp(-0.5 * (th / np.deg2rad(8)) ** 2)
    fuzz = 0.35 * np.exp(-0.5 * (th / np.deg2rad(30)) ** 2) + 0.03
    mixed = 0.75 * core + fuzz
    directed = 0.75 * core + 0.30 * np.exp(-0.5 * ((th - np.deg2rad(26)) / np.deg2rad(12)) ** 2)
    mixed = mixed / mixed.max()
    directed = directed / directed.max()

    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.semilogy(np.rad2deg(th), core, color=GREY, ls=":", label="只有纱线芯部")
    ax.semilogy(np.rad2deg(th), mixed, color=BLUE, label="叠加各向同性绒毛")
    ax.semilogy(np.rad2deg(th), directed, color=ACCENT, label="绒毛定向倾斜 26 度")
    ax.set_xlabel("法线相对纱线径向的倾角（度）")
    ax.set_ylabel("归一化密度")
    ax.set_xlim(-80, 80)
    ax.set_ylim(5e-4, 1.6)
    ax.legend(loc="lower left", fontsize=7.5)
    save(fig, "fig5-2-fuzz.png")


fig5_1()
fig5_2()
fig5_3()
