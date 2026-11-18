import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180


def fig2_1():
    fig = plt.figure(figsize=(6.8, 3.4))
    ax = fig.add_subplot(1, 2, 1, projection="3d")

    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi / 2, 30)
    U, V = np.meshgrid(u, v)
    X = np.cos(U) * np.sin(V)
    Y = np.sin(U) * np.sin(V)
    Z = np.cos(V)
    ax.plot_wireframe(X, Y, Z, color=LIGHT, lw=0.4, rstride=3, cstride=4)
    ax.plot([0, 0], [0, 0], [0, 1.25], color=INK, lw=1.2)
    ax.text(0, 0, 1.32, "$n$", fontsize=10, ha="center")

    # 入射方向与立体角小块
    ti, pi_ = 55 * D2R, 35 * D2R
    wi = spherical(np.array([ti]), np.array([pi_]))[0]
    ax.quiver(0, 0, 0, wi[0], wi[1], wi[2], color=BLUE, lw=1.6, arrow_length_ratio=0.12)
    ax.text(wi[0] * 1.05, wi[1] * 1.05, wi[2] * 1.05, r"$\omega_i$", color=BLUE, fontsize=11)

    du = np.linspace(pi_ - 0.18, pi_ + 0.18, 10)
    dv = np.linspace(ti - 0.16, ti + 0.16, 10)
    DU, DV = np.meshgrid(du, dv)
    ax.plot_surface(np.cos(DU) * np.sin(DV), np.sin(DU) * np.sin(DV), np.cos(DV),
                    color=ACCENT, alpha=0.55, linewidth=0)
    ax.text(0.62, -0.30, 0.80, r"$d\omega$", color=ACCENT, fontsize=10)

    ax.set_box_aspect((1, 1, 0.62))
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(0, 1.15)
    ax.set_axis_off()
    ax.view_init(elev=24, azim=-62)

    # 右图：投影面积随入射角变化
    ax2 = fig.add_subplot(1, 2, 2)
    th = np.linspace(0, 89, 300)
    ax2.plot(th, np.ones_like(th), color=GREY, lw=1.3, ls="--")
    ax2.plot(th, np.cos(th * D2R), color=ACCENT, lw=2.0)
    ax2.set_xlabel("入射方向与法线夹角（度）")
    ax2.set_ylabel("相对投影面积")
    ax2.set_xlim(0, 89)
    ax2.set_ylim(0, 1.08)
    ax2.text(58, 0.72, "投影面积 $\\cos\\theta$", color=ACCENT, fontsize=9)
    ax2.text(20, 1.02, "截面面积", color=GREY, fontsize=9)
    ax2.grid(True)
    save(fig, "fig2-1-hemisphere.png")


def spec_integral(alpha, n_theta=70, n_phi=140):
    T, P, domega = hemisphere_grid(n_theta, n_phi)
    W = spherical(T, P)
    coso = np.cos(T)
    ang = np.linspace(2, 89, 20)
    out = []
    for a in ang:
        wi = spherical(np.array([a * D2R]), np.array([0.0]))[0]
        h = normalize(wi + W)
        ci, co = wi[2], np.clip(W[..., 2], 0, 1)
        D = d_ggx(h[..., 2], alpha)
        G = g2_smith(ci, co, alpha)
        spec = np.where(co > 0, D * G / np.maximum(4 * ci * co, EPS), 0.0)
        out.append(np.sum(spec * coso * domega))
    return ang, np.array(out)


def fig2_2():
    ang, E = spec_integral(0.4)
    rho, F = 0.80, 0.5
    good = (1 - F) * rho + F * E
    bad = rho + F * E

    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.3), sharey=True)
    ax = axes[0]
    ax.plot(ang, good, color=BLUE, lw=2.0, label="正确：反射 + 吸收 = 1")
    ax.axhline(1.0, color=GREY, ls="--", lw=1.0)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("方向反照率")
    ax.set_ylim(0, 1.25)
    ax.set_xlim(0, 90)
    panel_label(ax, "a")
    ax.text(6, 1.12, "反射 + 透射 + 吸收 = 1", color=BLUE, fontsize=8.5)

    ax = axes[1]
    ax.plot(ang, bad, color=RED, lw=2.0)
    ax.axhline(1.0, color=GREY, ls="--", lw=1.0)
    ax.set_xlabel("入射角（度）")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.25)
    panel_label(ax, "b")
    ax.text(6, 1.12, "分层处漏掉 (1-F)，能量凭空多出", color=RED, fontsize=8.5)
    save(fig, "fig2-2-energy.png")


fig2_1()
fig2_2()
