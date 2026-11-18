import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180


def fig9_1():
    fig, ax = plt.subplots(figsize=(5.2, 3.1))
    n = np.arange(0, 9)
    for F, fb, col in [(0.04, 0.9, BLUE), (0.04, 0.3, TEAL), (0.30, 0.9, ACCENT)]:
        terms = np.array([(1 - F) ** 2 * fb * (F * fb) ** k for k in range(0, 9)])
        cum = F + np.concatenate(([0.0], np.cumsum(terms)[:-1]))
        ax.plot(n, cum, marker="o", ms=4, color=col, lw=1.7,
                label="F=%.2f, 基底反射率=%.1f" % (F, fb))
    ax.set_xlabel("计算到第几次内部反射")
    ax.set_ylabel("累积反射率")
    ax.set_xlim(-0.2, 8.2)
    ax.set_ylim(0, 1.0)
    ax.legend(loc="lower right", fontsize=7.5)
    save(fig, "fig9-1-series.png")


def fig9_2():
    # 基底的方向分布与涂层模糊核的卷积
    th = np.linspace(-90, 90, 601)
    base = np.exp(-0.5 * (th / 4.0) ** 2)
    base /= base.sum()
    fig, ax = plt.subplots(figsize=(5.6, 3.1))
    for sigma, col in [(0.0, BLUE), (6.0, TEAL), (14.0, ACCENT)]:
        if sigma == 0:
            y = base
        else:
            k = np.exp(-0.5 * (th / sigma) ** 2)
            k /= k.sum()
            y = np.convolve(base, k, mode="same")
        ax.plot(th, y / y.max(), color=col, lw=1.8,
                label="涂层粗糙度对应模糊 σ = %.0f°" % sigma)
    ax.set_xlabel("出射方向（度）")
    ax.set_ylabel("归一化强度")
    ax.set_xlim(-60, 60)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper right", fontsize=7.5)
    save(fig, "fig9-2-rough-coat.png")


fig9_1()
fig9_2()
