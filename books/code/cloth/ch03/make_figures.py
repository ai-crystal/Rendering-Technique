import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *


def fig3_1():
    """圆柱截面的反射扇面，以及单根圆柱的出射强度分布。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3))
    ax = axes[0]

    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color=INK, lw=1.4)

    phi_L = np.deg2rad(-25)
    u = np.array([np.cos(phi_L), np.sin(phi_L)])
    perp = np.array([-u[1], u[0]])
    cmap = plt.get_cmap("viridis")
    for k, b in enumerate(np.linspace(-0.95, 0.95, 11)):
        o = b * perp - 2.2 * u
        B = 2 * (o @ u)
        C = o @ o - 1.0
        disc = B * B - 4 * C
        if disc < 0:
            continue
        s = (-B - np.sqrt(disc)) / 2
        p = o + s * u
        n = p / np.linalg.norm(p)
        r = u - 2 * (u @ n) * n
        c = cmap(k / 10)
        ax.plot([o[0], p[0]], [o[1], p[1]], color=LIGHT, lw=0.7)
        ax.annotate("", xy=p, xytext=p - 0.55 * u,
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=1.0, shrinkA=0, shrinkB=0))
        ax.plot([p[0], p[0] + 1.5 * r[0]], [p[1], p[1] + 1.5 * r[1]], color=c, lw=1.0)
    ax.set_aspect("equal")
    ax.set_xlim(-2.3, 2.4)
    ax.set_ylim(-1.6, 2.1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.set_xlabel("入射方向与反射方向", fontsize=8)
    ax.text(-2.15, 1.85, "反射扇面张开约 180 度", fontsize=8, color="#3c4654")

    # 右图：出射强度正比于 Fresnel 反射率，d(alpha)/d(psi) 为常数
    ax2 = axes[1]
    alpha = np.linspace(-np.pi / 2, np.pi / 2, 900)
    for eta, c in [(1.55, ACCENT), (1.33, BLUE)]:
        cos_i = np.abs(np.cos((alpha - phi_L) / 2))
        F = fresnel_dielectric(cos_i, eta)
        I = 2.0 * F
        ax2.plot(np.rad2deg(alpha), I / I.max(), color=c, label="$n=%.2f$" % eta)
    ax2.set_xlabel("出射方向相对法线的角度（度）")
    ax2.set_ylabel("归一化强度")
    ax2.set_xlim(-90, 90)
    ax2.legend(loc="lower center")
    ax2.text(0.03, 0.93, "单根圆柱：宽而平，没有尖峰", transform=ax2.transAxes,
             fontsize=8, color="#3c4654", va="top")
    fig.tight_layout()
    save(fig, "fig3-1-cylinder-fan.png")


def fig3_2():
    """三维中的高光带：sin(T,H) 的幂次在出射方向球面上的分布。"""
    T = np.array([0.0, 1.0, 0.0])
    L = normalize(np.array([0.5, 0.3, 0.8]))
    phi = np.linspace(-np.pi, np.pi, 720)
    th = np.linspace(0.02, np.pi / 2, 360)
    P, TH = np.meshgrid(phi, th)
    V = spherical(TH, P)
    H = V + L
    H = H / np.linalg.norm(H, axis=-1, keepdims=True)
    s = np.linalg.norm(np.cross(T, H), axis=-1)
    I = s ** 60

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.1),
                             gridspec_kw={"width_ratios": [1.45, 1.0]})
    ax = axes[0]
    m = ax.pcolormesh(np.rad2deg(P), np.rad2deg(TH), I, cmap="magma", shading="auto",
                      vmin=0, vmax=1)
    ax.set_xlabel("出射方位角（度）")
    ax.set_ylabel("出射天顶角（度）")
    ax.set_yticks([0, 30, 60, 90])
    cb = fig.colorbar(m, ax=ax, pad=0.02)
    cb.set_label("归一化强度", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    ax2 = axes[1]
    deg = np.linspace(0, 80, 700)
    d = np.deg2rad(deg)
    for p, c in [(10, BLUE), (60, TEAL), (300, ACCENT)]:
        ax2.semilogy(deg, np.cos(d) ** p, color=c, label="$p=%d$" % p)
    ax2.set_xlabel("偏离带中心的角距（度）")
    ax2.set_ylabel("相对强度")
    ax2.set_xlim(0, 80)
    ax2.set_ylim(1e-4, 1.4)
    ax2.legend(loc="lower left")
    fig.tight_layout()
    save(fig, "fig3-2-band.png")


def fig3_3():
    """半高全宽与幂次的关系：精确解、近似式与相对误差。"""
    p = np.logspace(np.log10(4), np.log10(600), 300)
    exact = 2 * np.rad2deg(np.arccos(np.clip(2 ** (-1.0 / p), -1, 1)))
    approx = 2 * np.rad2deg(np.sqrt(2 * np.log(2) / p))
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.0))
    ax = axes[0]
    ax.loglog(p, exact, color=ACCENT, label="精确解")
    ax.loglog(p, approx, color=BLUE, ls="--", label="小角近似")
    ax.set_xlabel("幂次 p")
    ax.set_ylabel("半高全宽（度）")
    ax.legend(loc="upper right")
    ax.annotate("p = 60 时 17.4 度", xy=(60, 17.4), xytext=(95, 33), fontsize=8,
                color="#3c4654", arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))

    ax2 = axes[1]
    err = 100 * (approx - exact) / exact
    ax2.semilogx(p, err, color=TEAL)
    ax2.set_xlabel("幂次 p")
    ax2.set_ylabel("近似相对误差（%）")
    ax2.set_ylim(0, 12)
    ax2.axhline(err.max(), color=LIGHT, ls=":", lw=0.9)
    ax2.text(5, err.max() + 0.4, "最大 %.1f%%" % err.max(), fontsize=8, color="#3c4654")
    fig.tight_layout()
    save(fig, "fig3-3-fwhm.png")


fig3_1()
fig3_2()
fig3_3()
