import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()


# ------------------------------------------------------------------ 图 1-1
def fig1_1():
    """青色 LED 照黄塑料：光谱域与 RGB 域给出的两个答案。"""
    light = 0.95 * gaussian_line(LAM, 490, 18)
    mat = 0.05 + 0.90 * gaussian_line(LAM, 575, 45)
    prod = light * mat

    xyz_l = spectrum_to_xyz(LAM, light)
    xyz_m = spectrum_to_xyz(LAM, mat)
    xyz_p = spectrum_to_xyz(LAM, prod)
    rgb_l = M_XYZ2RGB_PUBLISHED @ (xyz_l / xyz_l[1])
    rgb_m = reflectance_rgb(mat)
    rgb_mul = np.clip(rgb_l, 0, None) * np.clip(rgb_m, 0, None)
    rgb_spe = M_XYZ2RGB_PUBLISHED @ (xyz_p / xyz_l[1])

    fig = plt.figure(figsize=(7.0, 3.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.62, 1.0], wspace=0.22)
    ax = fig.add_subplot(gs[0])
    ax.plot(LAM, light, color=GREY, lw=1.5)
    ax.plot(LAM, mat, color=TEAL, lw=1.7)
    ax.fill_between(LAM, 0, prod * 12, color=ACCENT, alpha=0.4, lw=0)
    ax.plot(LAM, prod * 12, color=ACCENT, lw=1.5)
    ax.annotate("光源 490 nm", xy=(486, 0.93), xytext=(404, 0.86),
                fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="-", lw=0.6, color="#8a93a0"))
    ax.annotate("塑料反射率", xy=(596, 0.60), xytext=(624, 0.72),
                fontsize=8, color=TEAL,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=TEAL))
    ax.annotate("乘积（放大 12 倍）", xy=(497, 0.46), xytext=(508, 0.24),
                fontsize=8, color=ACCENT,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=ACCENT))
    ax.set_xlim(400, 720)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("相对强度")
    ax.set_title("两条曲线在波长轴上几乎不重叠", pad=6)

    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    scale = rgb_mul.max()
    rows = [(0.62, srgb_encode(np.clip(rgb_mul / scale, 0, 1)),
             "RGB 逐通道相乘", "(%.2f, %.2f, %.2f)" % tuple(rgb_mul / scale * 1.0)),
            (0.22, srgb_encode(np.clip(rgb_spe / scale, 0, 1)),
             "光谱逐波长相乘", "(%.2f, %.2f, %.2f)" % tuple(rgb_spe / scale))]
    for y, c, t1, t2 in rows:
        ax2.add_patch(plt.Rectangle((0.02, y), 0.26, 0.22, color=c, ec="#3a3a3a", lw=0.6))
        ax2.text(0.35, y + 0.15, t1, fontsize=8.5, va="center", ha="left")
        ax2.text(0.35, y + 0.05, "线性 RGB " + t2, fontsize=7.8, va="center", ha="left", color="#555")
    ax2.text(0.02, 0.93, "同一场景，同一曝光", fontsize=9, va="center", ha="left")
    ax2.text(0.02, 0.03, "真实反射只占入射能量的 %.0f%%" % (100 * xyz_p[1] / xyz_l[1]),
             fontsize=8, color=ACCENT, va="bottom", ha="left")
    save(fig, "fig1-1-multiply.png")


# ------------------------------------------------------------------ 图 1-2
def nnls(A, b, n=60000):
    """投影梯度解 min ||A w - b||，w >= 0。只用到三个约束，够小。"""
    w = np.abs(np.linalg.lstsq(A, b, rcond=None)[0])
    lip = np.linalg.eigvalsh(A.T @ A).max()
    for _ in range(n):
        w = np.clip(w - (A.T @ (A @ w - b)) / lip, 0, None)
    return w


def fig1_2():
    """同色异谱：两条三刺激值相同的窄带与宽带光谱，透过陷波滤光片后分开。"""
    lam = LAM
    rgb = np.array([0.78, 0.55, 0.22])
    target = M_RGB2XYZ_PUBLISHED @ rgb

    lines = np.stack([gaussian_line(lam, c, 9) for c in (452, 548, 632)])
    A_l = np.stack([spectrum_to_xyz(lam, l) for l in lines], axis=1)
    a = lines.T @ np.linalg.lstsq(A_l, target, rcond=None)[0]

    centers = np.arange(420, 706, 28)
    bumps = np.stack([gaussian_line(lam, c, 34) for c in centers])
    A_b = np.stack([spectrum_to_xyz(lam, b) for b in bumps], axis=1)
    b = bumps.T @ nnls(A_b, target)

    xa, xb = spectrum_to_xyz(lam, a), spectrum_to_xyz(lam, b)
    de = float(delta_e76(xyz_to_lab(xa / xa[1]), xyz_to_lab(xb / xb[1])))

    filt = 1.0 - 0.97 * gaussian_line(lam, 600, 30)
    xra, xrb = spectrum_to_xyz(lam, a * filt), spectrum_to_xyz(lam, b * filt)
    de_f = float(delta_e76(xyz_to_lab(xra / xra[1]), xyz_to_lab(xrb / xrb[1])))

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.05),
                            gridspec_kw={"width_ratios": [1.5, 1.0], "wspace": 0.26})
    ax = axes[0]
    ax.plot(lam, a / a.max(), color=ACCENT, lw=1.4, label="光谱 A：三条窄线")
    ax.plot(lam, b / a.max(), color=BLUE, lw=1.7, label="光谱 B：宽带")
    ax.set_xlim(400, 720)
    ax.set_ylim(0, 1.42)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("相对功率（同一比例）")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.02))
    ax.set_title("两条光谱的三刺激值相同", pad=6)

    ax2 = axes[1]
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    ax2.text(0.02, 0.93, "不加滤光片", fontsize=8.5, va="center")
    ax2.text(0.02, 0.45, "加 600 nm 吸收滤光片", fontsize=8.5, va="center")
    exposure = 1.55
    for y, (pa, pb), label in [(0.66, (xa, xb), r"$\Delta E_{76}$ = %.2f" % de),
                               (0.18, (xra, xrb), r"$\Delta E_{76}$ = %.1f" % de_f)]:
        for j, xyz in enumerate((pa, pb)):
            c = srgb_encode(np.clip(M_XYZ2RGB_PUBLISHED @ (xyz / xyz[1]) / exposure, 0, 1))
            ax2.add_patch(plt.Rectangle((0.03 + 0.29 * j, y), 0.24, 0.19,
                                        color=c, ec="#3a3a3a", lw=0.6))
            ax2.text(0.15 + 0.29 * j, y - 0.02, "AB"[j], ha="center", va="top", fontsize=7.5)
        ax2.text(0.66, y + 0.095, label, fontsize=7.8, ha="left", va="center", color="#444")
    save(fig, "fig1-2-metamer.png")


# ------------------------------------------------------------------ 图 1-3
def _refract(d, n, eta):
    """d 是单位入射方向，n 是面向入射侧的向外法线，eta = ni/nt。"""
    cosi = -np.dot(d, n)
    if cosi < 0:
        n, cosi, eta = -n, -np.dot(d, n), 1.0 / eta
    k = 1 - eta ** 2 * (1 - cosi ** 2)
    if k < 0:
        return None
    return eta * d + (eta * cosi - np.sqrt(k)) * n


def _hit(p, d, a, b):
    e = b - a
    den = d[0] * e[1] - d[1] * e[0]
    if abs(den) < 1e-12:
        return None
    t = ((a[0] - p[0]) * e[1] - (a[1] - p[1]) * e[0]) / den
    s = ((a[0] - p[0]) * d[1] - (a[1] - p[1]) * d[0]) / den
    if t > 1e-9 and -1e-9 <= s <= 1 + 1e-9:
        return p + t * d
    return None


def fig1_3():
    """等边棱镜：13 条波长的真实光路，出射后角的差别放大 12 倍。"""
    ang = np.deg2rad(60.0)
    apex = np.array([0.0, np.sqrt(3) / 2])
    left, right = np.array([-0.5, 0.0]), np.array([0.5, 0.0])
    nL = np.array([-np.cos(ang / 2), np.sin(ang / 2)])
    nR = np.array([np.cos(ang / 2), np.sin(ang / 2)])

    d0 = np.array([np.cos(np.deg2rad(-8)), np.sin(np.deg2rad(-8))])
    p0 = np.array([-1.25, 0.42])
    lams = np.linspace(400, 700, 13)
    glass = "SF11"

    paths, devs = [], []
    for lam in lams:
        n = float(sellmeier(glass, lam))
        p1 = _hit(p0, d0, left, apex)
        d1 = _refract(d0, nL, 1.0 / n)
        p2 = _hit(p1 + 1e-7 * d1, d1, apex, right)
        d2 = _refract(d1, nR, n)
        dev = np.rad2deg(np.arctan2(d2[1], d2[0]) - np.arctan2(d0[1], d0[0]))
        paths.append((lam, p1, p2, d2))
        devs.append(dev)
    devs = np.array(devs)
    gain = 45.0

    fig = plt.figure(figsize=(7.0, 3.3))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.30, 1.0], wspace=0.46)
    ax = fig.add_subplot(gs[0])
    ax.add_patch(plt.Polygon([left, apex, right], closed=True, facecolor="#e8f0f2",
                             edgecolor="#5b6472", lw=1.0, zorder=1))
    for (lam, p1, p2, d2), dev in zip(paths, devs):
        c = wl_to_srgb(lam)[0]
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="0.62", lw=0.9, zorder=2)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=c, lw=1.1, zorder=3)
        a2 = np.deg2rad(np.rad2deg(np.arctan2(d0[1], d0[0])) + devs.mean()
                        + gain * (dev - devs.mean()))
        d2x = np.array([np.cos(a2), np.sin(a2)])
        ax.plot([p2[0], p2[0] + 0.80 * d2x[0]], [p2[1], p2[1] + 0.80 * d2x[1]],
                color=c, lw=1.2, zorder=3)
    ax.text(-1.22, 0.47, "白光", fontsize=8.5, color="#333")
    ax.text(0.02, 0.04, "出射后的角差放大 %d 倍" % gain, transform=ax.transAxes,
            fontsize=7.6, color="#666")
    ax.set_xlim(-1.32, 0.98)
    ax.set_ylim(-0.15, 1.0)
    ax.set_aspect("equal")
    ax.axis("off")

    ax2 = fig.add_subplot(gs[1])
    lam = grid()
    for name, col in [("N-BK7", BLUE), ("SF11", ACCENT)]:
        ds = []
        for l in lams:
            n = float(sellmeier(name, l))
            d1 = _refract(d0, nL, 1.0 / n)
            d2 = _refract(d1, nR, n)
            ds.append(np.rad2deg(np.arctan2(d2[1], d2[0]) - np.arctan2(d0[1], d0[0])))
        ax2.plot(lams, np.array(ds) - ds[-1], "o-", color=col, ms=3, lw=1.2,
                 label="%s（V$_d$ = %.1f）" % (name, abbe(name)[1]))
    ax2.axhline(0, color=LIGHT, lw=0.8)
    ax2.set_xlabel("波长 λ (nm)")
    ax2.set_ylabel("偏向角相对 700 nm 的差（度）")
    ax2.legend(loc="upper right")
    ax2.set_title("偏向角随波长变化", pad=6)
    save(fig, "fig1-3-prism.png")




fig1_1()
fig1_2()
fig1_3()
