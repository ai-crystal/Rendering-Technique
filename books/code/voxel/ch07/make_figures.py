import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

rng = np.random.default_rng(5)


def occ_sphere(p, R, h):
    """三线性插值后的占据率（格心采样，二值）。"""
    g = p / h
    i0 = np.floor(g).astype(int)
    f = g - i0
    val = 0.0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                c = (i0 + np.array([dx, dy, dz])) * h
                o = (np.linalg.norm(c, axis=1) < R).astype(float)
                w = ((f[:, 0] if dx else 1 - f[:, 0]) *
                     (f[:, 1] if dy else 1 - f[:, 1]) *
                     (f[:, 2] if dz else 1 - f[:, 2]))
                val = val + w * o
    return val


SUB = (np.arange(8) + 0.5) / 8.0


def cell_frac(idx, R, h):
    base = np.array(idx) * h
    pts = np.stack(np.meshgrid(base[0] + SUB * h, base[1] + SUB * h,
                               base[2] + SUB * h, indexing="ij"), axis=-1)
    return (np.linalg.norm(pts.reshape(-1, 3), axis=1) < R).mean()


def occ_frac(p, R, h, cache):
    g = p / h
    i0 = np.floor(g).astype(int)
    f = g - i0
    val = np.zeros(len(i0))
    for k in range(len(i0)):
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    key = (i0[k, 0] + dx, i0[k, 1] + dy, i0[k, 2] + dz)
                    if key not in cache:
                        cache[key] = cell_frac(key, R, h)
                    w = ((f[k, 0] if dx else 1 - f[k, 0]) *
                         (f[k, 1] if dy else 1 - f[k, 1]) *
                         (f[k, 2] if dz else 1 - f[k, 2]))
                    val[k] += w * cache[key]
    return val


def gradient_angle(fun, pts, d, h):
    gs = []
    for ax in range(3):
        e = np.zeros(3)
        e[ax] = h
        gs.append(fun(pts + e) - fun(pts - e))
    g = np.stack(gs, axis=1)
    n = np.linalg.norm(g, axis=1)
    ok = n > 1e-9
    gn = g[ok] / n[ok, None]
    ang = np.rad2deg(np.arccos(np.clip(-(gn * d[ok]).sum(axis=1), -1, 1)))
    return np.median(ang)


def fig7_1():
    R = 1.0
    ratios = np.array([6, 8, 12, 16, 24, 32, 48, 64])
    err_bin, err_frac = [], []
    N = 120
    d = rng.normal(size=(N, 3))
    d /= np.linalg.norm(d, axis=1)[:, None]

    for r in ratios:
        h = R / r
        pts = d * R
        err_bin.append(gradient_angle(lambda q: occ_sphere(q, R, h), pts, d, h))
        cache = {}
        err_frac.append(gradient_angle(lambda q: occ_frac(q, R, h, cache), pts, d, h))

    fig, ax = plt.subplots(figsize=(6.1, 3.4))
    ax.semilogx(ratios, err_bin, color=RED, marker="o", ms=3, label="二值占据率的梯度")
    ax.semilogx(ratios, err_frac, color=BLUE, marker="s", ms=3, label="分数占据率的梯度")
    ax.axhline(45.0, color=ACCENT, ls=":", label="格子面法线")
    ax.set_xlabel("球半径 / 体素边长")
    ax.set_ylabel("法线角度误差（度，中位数）")
    ax.set_ylim(0, 50)
    ax.legend(loc="center right", fontsize=7.6)
    fig.tight_layout()
    save(fig, "fig7-1-gradient.png")


# ---------------------------------------------------------------- 图 7-2
def ggx_D(n_dot_h, alpha):
    a2 = alpha * alpha
    c2 = np.clip(n_dot_h, 1e-6, 1.0) ** 2
    return a2 / (np.pi * (c2 * (a2 - 1.0) + 1.0) ** 2)


def fig7_2():
    delta = np.linspace(0, 40, 400)
    fig, ax = plt.subplots(figsize=(6.1, 3.4))
    for a, col in ((0.1, RED), (0.2, GOLD), (0.4, BLUE)):
        y = ggx_D(np.cos(np.deg2rad(delta)), a) / ggx_D(1.0, a)
        ax.plot(delta, y * 100, color=col, label=f"$\\alpha$ = {a}")
    ax.axvline(5, color=GREY, ls=":", lw=1.0)
    ax.text(5.6, 78, "5 度", fontsize=7.5, color="#3c4654")
    ax.set_xlabel("法线误差（度）")
    ax.set_ylabel("高光峰值（相对无误差）%")
    ax.set_ylim(0, 105)
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, "fig7-3-specular-loss.png")


# ---------------------------------------------------------------- 图 7-3
def fig7_3():
    sig = np.linspace(0.0, 0.05, 40)
    x = np.linspace(0, 1, 400)
    truth = 0.25 * np.sin(2 * np.pi * x) + 0.5
    win = 5
    k = np.ones(win) / win
    raw, rec = [], []
    for s in sig:
        obs = truth + rng.normal(0, s, size=x.shape)
        sl = slice(win, -win)
        raw.append(np.sqrt(np.mean((obs[sl] - truth[sl]) ** 2)))
        obs_p = np.pad(obs, win, mode="reflect")
        sm = np.convolve(obs_p, k, mode="same")[win:win + len(obs)][sl]
        rec.append(np.sqrt(np.mean((sm - truth[sl]) ** 2)))

    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    ax.plot(sig * 1000, np.array(raw) * 1000, color=ACCENT, label="原始采样")
    ax.plot(sig * 1000, np.array(rec) * 1000, color=BLUE, label="重建（5 格窗口平均）")
    ax.plot(sig * 1000, sig * 1000 / np.sqrt(win), color=GREY, ls=":",
            label=r"$\sigma/\sqrt{5}$")
    ax.set_xlabel("采样噪声标准差（毫米）")
    ax.set_ylabel("表面高度误差（毫米）")
    ax.legend(loc="upper left")
    fig.tight_layout()
    save(fig, "fig7-2-denoise.png")


if __name__ == "__main__":
    fig7_1()
    fig7_2()
    fig7_3()
