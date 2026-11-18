import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *


def refract(d, n, eta):
    """由外部到内部的折射，n 为朝外的法线，eta = n1/n2。"""
    ci = -np.dot(d, n)
    s2 = eta ** 2 * (1.0 - ci ** 2)
    if s2 >= 1.0:
        return None
    ct = np.sqrt(1.0 - s2)
    return eta * d + (eta * ci - ct) * n


def trace_paths(n_eta=1.55, b=0.45):
    """在单位圆截面内追踪 R、TT、TRT 三条路径。"""
    R = 1.0
    u = normalize(np.array([0.75, -0.55]))
    perp = np.array([-u[1], u[0]])
    o = b * perp - 2.0 * u
    B = 2 * (o @ u)
    C = o @ o - R ** 2
    s = (-B - np.sqrt(B * B - 4 * C)) / 2
    p0 = o + s * u
    n0 = p0 / np.linalg.norm(p0)

    paths = {}
    # R
    r = u - 2 * (u @ n0) * n0
    paths["R"] = [[o, p0], [p0, p0 + 1.5 * r]]

    t1 = refract(u, n0, 1.0 / n_eta)
    s1 = -2 * (p0 @ t1)
    p1 = p0 + s1 * t1
    n1 = p1 / np.linalg.norm(p1)
    # TT
    t2 = refract(t1, -n1, n_eta)
    paths["TT"] = [[o, p0], [p0, p1], [p1, p1 + 1.3 * t2]]
    # TRT
    r2 = t1 - 2 * (t1 @ n1) * n1
    s2 = -2 * (p1 @ r2)
    p2 = p1 + s2 * r2
    n2 = p2 / np.linalg.norm(p2)
    t3 = refract(r2, -n2, n_eta)
    paths["TRT"] = [[o, p0], [p0, p1], [p1, p2], [p2, p2 + 0.95 * t3]]
    return paths


def fig4_1():
    paths = trace_paths()
    colors = {"R": ACCENT, "TT": BLUE, "TRT": TEAL}
    titles = {"R": "R：表面反射", "TT": "TT：两次折射", "TRT": "TRT：内部反射一次"}
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.7))
    th = np.linspace(0, 2 * np.pi, 500)
    for ax, name in zip(axes, ["R", "TT", "TRT"]):
        ax.plot(np.cos(th), np.sin(th), color=INK, lw=1.4)
        ax.fill(np.cos(th), np.sin(th), color="#f4f1ea", zorder=0)
        segs = paths[name]
        for k, (a, b) in enumerate(segs):
            c = GREY if k == 0 else colors[name]
            ax.annotate("", xy=b, xytext=a,
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=1.2,
                                        shrinkA=0, shrinkB=0, mutation_scale=9))
        ax.set_title(titles[name], fontsize=8.5)
        ax.set_aspect("equal")
        ax.set_xlim(-2.35, 2.1)
        ax.set_ylim(-1.9, 2.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
    axes[0].set_xlabel("纤维截面（$n=1.55$）", fontsize=8)
    fig.tight_layout()
    save(fig, "fig4-1-paths.png")


def fig4_2():
    """纵向分布 M(theta) 与方位角分布 N(phi)。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.0))
    ax = axes[0]
    th = np.deg2rad(np.linspace(-60, 60, 900))
    MR = np.exp(-0.5 * (th / np.deg2rad(12)) ** 2)
    MTT = 0.85 * np.exp(-0.5 * (th / np.deg2rad(16)) ** 2)
    MTRT = np.exp(-0.5 * ((th + np.deg2rad(16)) / np.deg2rad(14)) ** 2)
    ax.plot(np.rad2deg(th), MR, color=ACCENT, label="R")
    ax.plot(np.rad2deg(th), MTT, color=BLUE, ls="--", label="TT")
    ax.plot(np.rad2deg(th), MTRT, color=TEAL, ls="-.", label="TRT")
    ax.set_xlabel("纵向角偏离镜面锥的角距（度）")
    ax.set_ylabel("归一化强度")
    ax.set_xlim(-60, 60)
    ax.set_ylim(0, 1.25)
    ax.legend(loc="upper right", ncol=3, fontsize=7.5)
    ax.annotate("TRT 偏移 16 度", xy=(-16, 1.0), xytext=(-56, 0.62), fontsize=8,
                color="#3c4654", arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))

    ax2 = axes[1]
    phi = np.linspace(-np.pi, np.pi, 900)
    NR = np.exp(-0.5 * (phi / 0.16) ** 2)
    NTT = 0.55 * np.exp(-0.5 * (phi / 0.95) ** 2) + 0.08
    NTRT = np.exp(-0.5 * ((phi - 0.38) / 0.42) ** 2)
    for y, c, ls, lab in [(NR, ACCENT, "-", "R"), (NTT, BLUE, "--", "TT"),
                          (NTRT, TEAL, "-.", "TRT")]:
        ax2.plot(np.rad2deg(phi), y / y.max(), color=c, ls=ls, label=lab)
    ax2.set_xlabel("方位角（度）")
    ax2.set_ylabel("归一化强度")
    ax2.set_xlim(-180, 180)
    ax2.set_xticks([-180, -90, 0, 90, 180])
    ax2.set_ylim(0, 1.2)
    ax2.legend(loc="upper left", ncol=3, fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig4-2-MN.png")


def fig4_3():
    """同一纱线上纤维捻向不同时，高光分裂成两条。"""
    th_o = np.linspace(-80, 80, 900)
    ti = 35.0
    sig = 9.0

    def lobe(shift):
        return np.exp(-0.5 * ((th_o - (ti - shift)) / sig) ** 2)

    single = lobe(0.0)
    one_side = lobe(18.0)
    both = 0.85 * lobe(18.0) + 0.85 * lobe(-18.0)
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    ax.plot(th_o, single, color=GREY, ls="--", label="纤维全平行（镜面方向）")
    ax.plot(th_o, one_side, color=BLUE, label="纤维同向倾斜 9 度")
    ax.plot(th_o, both, color=ACCENT, label="两组反向倾斜，混纺")
    ax.set_xlabel("出射天顶角（度，入射角 35 度）")
    ax.set_ylabel("归一化强度")
    ax.set_xlim(-80, 80)
    ax.set_ylim(0, 1.15)
    ax.legend(loc="upper left", fontsize=7.5)
    ax.annotate("分叉", xy=(35, 0.55), xytext=(44, 0.95), fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
    save(fig, "fig4-3-split.png")


fig4_1()
fig4_2()
fig4_3()
