import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()
DL = np.gradient(LAM)
W = d65_like(LAM)
YW = float((cie_y(LAM) * W * DL).sum())
A = (cie_xyz_basis(LAM) * (W * DL)) / YW          # 3 x N，白点 Y = 1
PRIM = [M_RGB2XYZ_PUBLISHED[:, i] for i in range(3)]


def primaries(iters=40000):
    """Mallett–Yuksel 式求解：三个原色各自是带箱约束的最小二乘解。"""
    lip = np.linalg.eigvalsh(A @ A.T).max()
    out = []
    for b in PRIM:
        s = np.full(len(LAM), 0.5)
        for _ in range(iters):
            s = np.clip(s - (A.T @ (A @ s - b)) / lip, 0.0, 1.0)
        out.append(s)
    return np.stack(out)          # 3 x N


PRIMS = primaries()


def srgb_to_rgb(xyz_rgb):
    return M_XYZ2RGB_PUBLISHED @ xyz_rgb


def mallett(rgb):
    return np.clip(rgb, 0, 1) @ PRIMS


def jh(rgb):
    c, s, res = jh_fit(LAM, np.clip(rgb, 0, 1), illum=W)
    return s


NAIVE_B = np.stack([gaussian_line(LAM, 610, 55), gaussian_line(LAM, 550, 55),
                    gaussian_line(LAM, 465, 55)])
NAIVE_N = (NAIVE_B * (W * DL)).sum(axis=1) / YW
NAIVE_B = NAIVE_B / NAIVE_N[:, None]


def naive(rgb):
    return np.clip(rgb, 0, 1) @ NAIVE_B


def roundtrip(s):
    xyz = A @ s
    return M_XYZ2RGB_PUBLISHED @ xyz


def dE(s, rgb_target):
    back = roundtrip(s)
    lab1 = xyz_to_lab(A @ (np.clip(rgb_target, 0, 1) @ np.linalg.lstsq(A, M_RGB2XYZ_PUBLISHED @ np.clip(rgb_target, 0, 1), rcond=None)[0]))
    lab2 = xyz_to_lab(A @ s)
    return float(delta_e76(lab1, lab2))


# ------------------------------------------------------------------ 图 8-1
def fig8_1():
    fig = plt.figure(figsize=(7.0, 3.7))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.30)

    ax = fig.add_subplot(gs[0])
    targets = [((1, 1, 1), "白 (1,1,1)", GREY),
               ((0.5, 0.5, 0.5), "灰 (0.5,0.5,0.5)", "#5b6472"),
               ((0.9, 0.85, 0.1), "黄 (0.9,0.85,0.1)", GOLD),
               ((0.1, 0.2, 0.85), "蓝 (0.1,0.2,0.85)", BLUE)]
    for rgb, lab, col in targets:
        ax.plot(LAM, jh(rgb) if False else jh_fit(LAM, np.array(rgb, float), illum=W)[1],
                color=col, lw=1.6, label=lab)
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("重建的反射率")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2,
              fontsize=7.4, columnspacing=1.2)
    ax.set_title("同一模型，四种颜色", pad=6)

    ax2 = fig.add_subplot(gs[1])
    rgb = np.array([0.80, 0.30, 0.20])
    ax2.plot(LAM, jh_fit(LAM, rgb, illum=W)[1], color=ACCENT, lw=1.8, label="多项式×S 形")
    ax2.plot(LAM, mallett(rgb), color=BLUE, lw=1.5, label="三原色线性分解")
    ax2.plot(LAM, naive(rgb), color=TEAL, lw=1.4, ls="--", label="三个高斯")
    ax2.set_xlim(380, 780)
    ax2.set_ylim(0, 1.05)
    ax2.set_xlabel("波长 λ (nm)")
    ax2.set_ylabel("重建的反射率")
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2,
                fontsize=7.4, columnspacing=1.2)
    ax2.set_title("同一个 sRGB (0.80, 0.30, 0.20)", pad=6)
    ax2.annotate("三高斯超过 1", xy=(660, 1.04), xytext=(690, 0.62), fontsize=7.6,
                 color=TEAL, arrowprops=dict(arrowstyle="-", lw=0.6, color=TEAL))
    save(fig, "fig8-1-spectra.png")


# ------------------------------------------------------------------ 图 8-2
def fig8_2():
    rng = np.random.default_rng(2)
    cols = [ACCENT, BLUE, TEAL]
    names = ["多项式×S 形", "三原色分解", "三个高斯"]
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    for k, (fn, name, col) in enumerate(zip([jh, mallett, naive], names, cols)):
        xs, ys = [], []
        for _ in range(120):
            rgb = rng.uniform(0, 1, 3)
            s = fn(rgb)
            slope = float(np.abs(np.gradient(s, LAM)).max())
            back = roundtrip(s)
            err = float(np.max(np.abs(back - rgb)))
            xs.append(slope)
            ys.append(max(err, 1e-6))
        ax.loglog(xs, ys, "o", color=col, ms=3.6, alpha=0.75, label=name)
    ax.set_xlabel("光谱的最大斜率（1/nm）")
    ax.set_ylabel("往返之后 sRGB 的最大误差")
    ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.55))
    save(fig, "fig8-2-roundtrip.png")


# ------------------------------------------------------------------ 图 8-3
def fig8_3():
    """压力测试：宽谱光源下三种重建看不出差别，窄带光源下分道扬镳。"""
    rgb = np.array([0.85, 0.25, 0.15])
    recs = [("多项式×S 形", jh_fit(LAM, rgb, illum=W)[1]),
            ("三原色分解", mallett(rgb)),
            ("三个高斯", naive(rgb))]

    lights = [("D65（宽谱）", W), ("460 nm 窄带", gaussian_line(LAM, 460, 20))]

    fig = plt.figure(figsize=(7.0, 3.3))
    gs = fig.add_gridspec(1, 2, width_ratios=[0.85, 1.35], wspace=0.24)
    ax = fig.add_subplot(gs[0])
    ax.plot(LAM, gaussian_line(LAM, 460, 20), color=PURPLE, lw=1.6)
    ax.fill_between(LAM, 0, gaussian_line(LAM, 460, 20), color=PURPLE, alpha=0.15, lw=0)
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("相对功率")
    ax.set_title("两盏灯", pad=6)

    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    for j, (name, _) in enumerate(recs):
        ax2.text(0.13 + 0.29 * j, 0.97, name, fontsize=7.4, ha="center", va="center")

    def under(light, s):
        y_l = float((cie_y(LAM) * light * DL).sum())
        return (cie_xyz_basis(LAM) * (light * DL / y_l)) @ s

    for r, (lname, light) in enumerate(lights):
        xyzs = [under(light, s) for _, s in recs]
        rgbs = [M_XYZ2RGB_PUBLISHED @ x for x in xyzs]
        ymax = max(float(np.max(v)) for v in rgbs)
        y0 = 0.60 - r * 0.44
        ax2.text(0.01, y0 + 0.30, lname, fontsize=7.8, va="center", color="#444")
        for j, (xyz, v) in enumerate(zip(xyzs, rgbs)):
            c = srgb_encode(np.clip(v / ymax, 0, 1))
            ax2.add_patch(plt.Rectangle((0.02 + 0.29 * j, y0), 0.22, 0.24,
                                        color=c, ec="#3a3a3a", lw=0.6))
            ax2.text(0.13 + 0.29 * j, y0 - 0.03, "Y=%.3f" % float(xyz[1]),
                     fontsize=7.2, ha="center", va="top", color="#555")
    save(fig, "fig8-3-pressure.png")




fig8_1()
fig8_2()
fig8_3()
