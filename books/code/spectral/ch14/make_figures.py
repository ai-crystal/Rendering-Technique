import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "ch13"))
import mini_tracer as mt


# ------------------------------------------------------------------ 图 14-1
def fig14_1():
    """RGB 与光谱的色差：材料越"有颜色"，光源越窄，误差越大。"""
    def chroma_de(lf, amp, mc=575.0, mf=45.0):
        light = gaussian_line(LAM, 490, lf)
        mat = 0.5 + amp * gaussian_line(LAM, mc, mf)
        xl = spectrum_to_xyz(LAM, light)
        xm = spectrum_to_xyz(LAM, mat)
        xp = spectrum_to_xyz(LAM, light * mat)
        rl = M_XYZ2RGB_PUBLISHED @ (xl / xl[1])
        rm = reflectance_rgb(mat)
        mul = rl * rm          # 不裁剪，只考察乘法本身
        xm2 = M_RGB2XYZ_PUBLISHED @ mul
        a = xm2 / max(xm2.sum(), 1e-9)
        b = xp / max(xp.sum(), 1e-9)
        lab1 = xyz_to_lab(np.array([a[0] / 0.95047, a[1], a[2] / 1.08883]))
        lab2 = xyz_to_lab(np.array([b[0] / 0.95047, b[1], b[2] / 1.08883]))
        return float(delta_e76(lab1, lab2))

    amps = np.linspace(0, 0.48, 25)
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    for lf, col in [(10, ACCENT), (30, TEAL), (90, BLUE)]:
        ax.plot(amps, [chroma_de(lf, a) for a in amps], "o-", color=col, ms=3,
                lw=1.6, label="光源带宽 %d nm" % lf)
    for y, lab in [(2.3, "刚可察觉"), (5.0, "明显")]:
        ax.axhline(y, color=GREY, lw=0.9, ls=":")
        ax.text(0.05, y + 4, lab, fontsize=7.4, color="#666", ha="left")
    ax.set_xlabel("材料反射带的调制深度（0 为中性灰）")
    ax.set_ylabel("色度上的色差 $\Delta E_{76}$")
    ax.set_xlim(0, 0.48)
    ax.set_ylim(0, None)
    ax.legend(loc="upper left", fontsize=7.6)
    save(fig, "fig14-1-criterion.png")


# ------------------------------------------------------------------ 图 14-2
def fig14_2():
    """实测：波长数对噪声与耗时的影响。"""
    ns = [1, 2, 4, 8, 16]
    mt.NW = 16
    ref = mt.render(w=40, h=30, spp=48, seed=1)
    times, rms = [], []
    for n in ns:
        mt.NW = n
        t0 = time.perf_counter()
        img = mt.render(w=40, h=30, spp=8, seed=7)
        dt = time.perf_counter() - t0
        times.append(dt / 8)
        rms.append(float(np.sqrt(np.mean((img - ref) ** 2)) / np.mean(ref)))

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw={"wspace": 0.32})
    ax = axes[0]
    ax.loglog(ns, rms, "o-", color=ACCENT, ms=4.5)
    ref_curve = rms[0] / np.sqrt(np.array(ns, dtype=float))
    ax.loglog(ns, ref_curve, ":", color=GREY, lw=1.0)
    ax.set_xlabel("每条路径的波长数 n")
    ax.set_ylabel("相对 RMS 噪声")
    ax.set_xticks(ns)
    ax.set_xticklabels(["%d" % n for n in ns])
    ax.set_title("噪声随 n 下降", pad=6)

    ax2 = axes[1]
    ax2.plot(ns, [t * 1000 for t in times], "s-", color=BLUE, ms=4.5)
    ax2.set_xlabel("每条路径的波长数 n")
    ax2.set_ylabel("每个样本的耗时（毫秒）")
    ax2.set_xticks(ns)
    ax2.set_ylim(0, max(t * 1000 for t in times) * 1.35)
    ax2.set_title("这份实现里耗时几乎不变", pad=6)
    save(fig, "fig14-2-performance.png")


# ------------------------------------------------------------------ 图 14-3
def _refract(d, nrm, eta):
    cosi = -np.dot(d, nrm)
    if cosi < 0:
        nrm, cosi, eta = -nrm, -np.dot(d, nrm), 1.0 / eta
    k = 1 - eta ** 2 * (1 - cosi ** 2)
    if k < 0:
        return None
    return eta * d + (eta * cosi - np.sqrt(k)) * nrm


def fig14_3():
    """同一块棱镜：光谱渲染给出连续光带，RGB 渲染只给三条线。"""
    A = np.deg2rad(60.0)
    apex = np.array([0.0, np.sqrt(3) / 2])
    left, right = np.array([-0.5, 0.0]), np.array([0.5, 0.0])
    nL = np.array([-np.cos(A / 2), np.sin(A / 2)])
    nR = np.array([np.cos(A / 2), np.sin(A / 2)])

    def hit(p, d, a, b):
        e = b - a
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-12:
            return None
        t = ((a[0] - p[0]) * e[1] - (a[1] - p[1]) * e[0]) / den
        u = ((a[0] - p[0]) * d[1] - (a[1] - p[1]) * d[0]) / den
        if t > 1e-9 and -1e-9 <= u <= 1 + 1e-9:
            return p + t * d
        return None

    p0 = np.array([-1.3, 0.50])
    d0 = np.array([np.cos(np.deg2rad(-10)), np.sin(np.deg2rad(-10))])
    screen_x = 2.2

    def landing(lam, n_override=None):
        n = float(sellmeier("N-BK7", lam)) if n_override is None else n_override
        p1 = hit(p0, d0, left, apex)
        d1 = _refract(d0, nL, 1.0 / n)
        if d1 is None:
            return None
        p2 = hit(p1 + 1e-7 * d1, d1, apex, right)
        if p2 is None:
            return None
        d2 = _refract(d1, nR, n)
        if d2 is None or abs(d2[0]) < 1e-9:
            return None
        t = (screen_x - p2[0]) / d2[0]
        return (p2 + t * d2)[1]

    probe = [landing(l) for l in np.linspace(400, 700, 61)]
    probe = [y for y in probe if y is not None]
    lo, hi = min(probe), max(probe)
    pad = (hi - lo) * 0.35 + 1e-3
    ys = np.linspace(lo - pad, hi + pad, 900)
    spec = np.zeros_like(ys)
    for lam in np.linspace(400, 700, 301):
        y = landing(lam)
        if y is None:
            continue
        spec += np.exp(-0.5 * ((ys - y) / 0.00006) ** 2)

    rgb_curves = []
    for lam, col in [(610.0, RED), (550.0, GREEN), (465.0, BLUE)]:
        y = landing(lam)
        if y is None:
            rgb_curves.append((col, np.zeros_like(ys)))
            continue
        rgb_curves.append((col, np.exp(-0.5 * ((ys - y) / 0.00006) ** 2)))

    fig, axes = plt.subplots(2, 1, figsize=(6.4, 3.6), sharex=True,
                             gridspec_kw={"hspace": 0.18})
    ax = axes[0]
    ax.plot(ys, spec / spec.max(), color="#333", lw=1.4)
    ax.fill_between(ys, 0, spec / spec.max(), color=ACCENT, alpha=0.35, lw=0)
    ax.set_ylabel("光谱渲染", fontsize=8.5)
    ax.set_yticks([])
    ax.set_title("屏幕上一条光带的亮度分布", pad=6)

    ax2 = axes[1]
    for col, c in rgb_curves:
        ax2.plot(ys, c, color=col, lw=1.6)
    ax2.set_ylabel("RGB 渲染", fontsize=8.5)
    ax2.set_yticks([])
    ax2.set_xlabel("屏幕上的位置")
    save(fig, "fig14-3-prism-compare.png")




fig14_1()
fig14_2()
fig14_3()
