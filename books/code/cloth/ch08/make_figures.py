import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *


def refract(d, n, eta):
    ci = -np.dot(d, n)
    s2 = eta ** 2 * (1.0 - ci ** 2)
    if s2 >= 1.0:
        return None
    ct = np.sqrt(1.0 - s2)
    return eta * d + (eta * ci - ct) * n


def hit_circle(o, d, c, R):
    oc = o - c
    B = 2 * np.dot(oc, d)
    C = np.dot(oc, oc) - R ** 2
    disc = B * B - 4 * C
    if disc < 0:
        return None, None
    s = (-B - np.sqrt(disc)) / 2
    if s < 0:
        s = (-B + np.sqrt(disc)) / 2
    p = o + s * d
    n = (p - c) / R
    return p, n


def fig8_1():
    R = 0.52
    centers = [np.array([-0.58, 0.0]), np.array([0.60, 0.0])]
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    th = np.linspace(0, 2 * np.pi, 400)
    for c in centers:
        ax.fill(c[0] + R * np.cos(th), c[1] + R * np.sin(th), color="#efe9dc", zorder=1)
        ax.plot(c[0] + R * np.cos(th), c[1] + R * np.sin(th), color=INK, lw=1.2, zorder=2)

    d = normalize(np.array([0.24, -1.0]))

    # 穿过空隙的光
    o1 = np.array([-0.42, 1.75])
    ax.annotate("", xy=o1 + 3.2 * d, xytext=o1,
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.3, shrinkA=0, shrinkB=0))
    ax.text(-1.35, 1.55, "穿过空隙", color=BLUE, fontsize=8)

    # 穿过纤维的光
    o2 = np.array([0.42, 1.75])
    p, n = hit_circle(o2, d, centers[1], R)
    t1 = refract(d, n, 1 / 1.55)
    s = -2 * np.dot(p - centers[1], t1)
    q = p + s * t1
    n2 = (q - centers[1]) / R
    t2 = refract(t1, -n2, 1.55)
    ax.annotate("", xy=p, xytext=o2, arrowprops=dict(arrowstyle="-|>", color=GREY,
                                                     lw=1.0, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=ACCENT,
                                                    lw=1.2, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=q + 0.85 * t2, xytext=q, arrowprops=dict(arrowstyle="-|>", color=ACCENT,
                                                               lw=1.2, shrinkA=0, shrinkB=0))
    ax.text(0.95, -1.05, "穿过纤维", color=ACCENT, fontsize=8)
    ax.annotate("", xy=(0.06, 0.0), xytext=(0.06, 0.0))
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, 1.7)
    ax.set_ylim(-1.75, 1.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.set_xlabel("沿纬向的截面：两个经纱截面之间是空隙", fontsize=8)
    save(fig, "fig8-1-paths.png")


def fig8_2():
    """透射的角分布：直射分量与漫透射分量。"""
    deg = np.linspace(-88, 88, 900)
    d = np.deg2rad(deg)
    theta_i = 25.0
    direct = np.exp(-0.5 * ((deg - theta_i) / 1.2) ** 2)
    diffuse = np.clip(np.cos(d), 0, 1) ** 1.5

    cases = [(0.90, 0.55, BLUE, "稀疏薄纱（空隙多）"),
             (0.55, 0.18, TEAL, "中等密度"),
             (0.28, 0.03, ACCENT, "紧密织物（几乎无空隙）")]
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    for tt, wd, c, lab in cases:
        y = tt * (wd * direct + (1 - wd) * diffuse)
        ax.semilogy(deg, y + 1e-4, color=c, label=lab)
    ax.set_xlabel("透射出射方向（度，入射 25 度）")
    ax.set_ylabel("透射强度（对数）")
    ax.set_xlim(-88, 88)
    ax.set_ylim(1e-3, 1.2)
    ax.legend(loc="lower center", fontsize=7.5)
    ax.annotate("直射", xy=(25, 0.45), xytext=(45, 0.62), fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
    save(fig, "fig8-2-btdf.png")


def fig8_3():
    """覆盖率与能量分配。"""
    C = np.linspace(0.4, 1.0, 300)
    R = 0.06 * C
    Td = 0.92 * (1 - C)
    Tf = 0.72 * C * (1 - np.exp(-2.0))
    total = R + Td + Tf
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    ax.plot(C, R, color=BLUE, label="反射 R")
    ax.plot(C, Td, color=TEAL, label="空隙直射 T")
    ax.plot(C, Tf, color=ACCENT, label="纤维漫透射 T")
    ax.plot(C, total, color=INK, ls="--", lw=1.2, label="R + T")
    ax.axhline(1.0, color=GREY, ls=":", lw=0.9)
    ax.fill_between(C, total, 1.0, color=LIGHT, alpha=0.45)
    ax.set_xlabel("覆盖率 C")
    ax.set_ylabel("能量比例")
    ax.set_xlim(0.4, 1.0)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="center left", fontsize=7.5)
    ax.text(0.72, 0.90, "吸收", fontsize=8, color="#3c4654")
    save(fig, "fig8-3-energy.png")


fig8_1()
fig8_2()
fig8_3()
