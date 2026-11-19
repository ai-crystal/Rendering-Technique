import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

RNG = np.random.default_rng(20261119)


# ------------------------------------------------------------------ 图 4-1
def fig4_1():
    """泊松分布与相对噪声。"""
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))

    ax = axes[0]
    for mu, c in ((1.0, ACCENT), (4.0, BLUE), (16.0, TEAL)):
        k = np.arange(0, 45)
        pmf = np.exp(-mu) * mu ** k / np.array([math.factorial(int(i)) for i in k])
        ax.plot(k, pmf, "o-", ms=3.0, lw=1.2, color=c, label="均值 %.0f" % mu)
    ax.set_xlim(-0.5, 40)
    ax.set_ylim(0, 0.42)
    ax.set_xlabel("一个像素收到的光子数 N")
    ax.set_ylabel("概率")
    ax.set_title("光子数是离散的", pad=6)
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.98))

    ax = axes[1]
    N = np.logspace(0, 6, 200)
    ax.loglog(N, 1 / np.sqrt(N), color=INK, lw=1.8)
    for n0 in (1, 10, 100, 1e4, 1e6):
        v = 1 / np.sqrt(n0)
        ax.plot([n0], [v], "o", ms=3.4, color=ACCENT)
        ax.annotate("%.0f%%" % (v * 100) if v >= 0.01 else "%.2f%%" % (v * 100),
                    xy=(n0, v), xytext=(n0 * 1.25, v * 1.9), fontsize=7.6, color=ACCENT)
    ax.set_xlim(1, 1e6)
    ax.set_ylim(1e-3, 2)
    ax.set_xlabel("平均光子数 $\\bar{N}$")
    ax.set_ylabel("相对噪声 $\\sigma/\\bar{N}$")
    ax.set_title("噪声按 1/√N 下降", pad=6)
    fig.tight_layout()
    save(fig, "fig4-1-poisson.png")


# ------------------------------------------------------------------ 图 4-2
def fig4_2():
    """同一张图在三个曝光档下的光子噪声。"""
    n = 240
    xs = np.linspace(-1, 1, n)
    X, Y = np.meshgrid(xs, xs)
    R2 = X ** 2 + Y ** 2
    mask = R2 <= 1.0
    Z = np.sqrt(np.clip(1.0 - R2, 0, None))
    l = np.array([-0.42, 0.55, 0.72])
    l = l / np.linalg.norm(l)
    cos = np.clip(X * l[0] + Y * l[1] + Z * l[2], 0, None)
    L = np.where(mask, 0.8 / np.pi * cos, 0.0)

    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.9))
    for ax, peak in zip(axes, (0.6, 60.0, 6000.0)):
        mean = L / L.max() * peak
        img = RNG.poisson(mean).astype(float)
        shown = srgb_encode(np.clip(img / peak, 0, 1))
        shown = np.where(mask, shown, 0.0)
        ax.imshow(shown, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)
        lab = ("%.1f" % peak) if peak < 1 else ("%.0f" % peak)
        ax.set_title("峰值 %s 个光子/像素" % lab, fontsize=9, pad=5)
    fig.tight_layout()
    save(fig, "fig4-2-photon-noise.png")


fig4_1()
fig4_2()
