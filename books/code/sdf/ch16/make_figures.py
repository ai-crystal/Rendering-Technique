import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.ticker import NullFormatter
import numpy as np

SIG = 1.6


# ---------------------------------------------------------------- 图 16-1
def fig16_1():
    # 一个薄层：sigma(t) 在 t=0.3 附近有尖峰
    grid = np.linspace(0, 1, 20001)
    sig = SIG * np.exp(-((grid - 0.30) / 0.045) ** 2)
    od = np.concatenate([[0.0], np.cumsum(0.5 * (sig[1:] + sig[:-1]) * np.diff(grid))])
    trans = np.exp(-od)
    Iref = np.trapezoid(sig * trans, grid)

    def sig_of(t):
        return SIG * np.exp(-((t - 0.30) / 0.045) ** 2)

    def trans_of(t):
        return np.interp(t, grid, trans)

    rng = np.random.default_rng(12)
    Ns = np.unique(np.round(np.logspace(2, 4.5, 16)).astype(int))
    vu, vi = [], []
    for N in Ns:
        est_u, est_i = [], []
        for _ in range(120):
            t = rng.random(N)
            est_u.append(np.mean(sig_of(t) * trans_of(t)))
            # 以尖峰为中心的高斯提议分布，截断到 [0,1]
            z = 0.30 + 0.09 * rng.normal(size=N)
            ok = (z > 0) & (z < 1)
            q = np.exp(-0.5 * ((z - 0.30) / 0.09) ** 2) / (0.09 * np.sqrt(2 * np.pi)) / 0.9997
            est_i.append(np.mean(ok * sig_of(z) * trans_of(z) / q))
        vu.append(np.var(est_u))
        vi.append(np.var(est_i))

    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.loglog(Ns, vu, "o-", color=BLUE, ms=3.4, lw=1.5, label="沿光线均匀采样")
    ax.loglog(Ns, vi, "s--", color=ACCENT, ms=3.2, lw=1.5,
              label="按密度的重要性采样")
    ax.loglog(Ns, vu[0] * Ns[0] / Ns, color=GREY, ls=":", lw=1.1, label=r"$O(1/N)$")
    ax.set_xlabel("样本数")
    ax.set_ylabel("估计量的方差")
    ax.legend(loc="lower left", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig16-2-variance.png")


# ---------------------------------------------------------------- 图 16-2
def fig16_2():
    N = np.logspace(2, 7, 200)
    bvh = 2.2 * np.log2(N) + 10
    sdf = np.full_like(N, 42.0)
    # 混合：60% 的三角形用 BVH，40% 的物体用 SDF（代价常数）
    mixed = 0.55 * bvh + 0.45 * 42.0

    fig, ax = plt.subplots(figsize=(6.3, 3.1))
    ax.loglog(N, bvh, color=BLUE, lw=1.8, label="BVH")
    ax.loglog(N, sdf, color=ACCENT, lw=1.8, label="SDF 步进")
    ax.loglog(N, mixed, color=TEAL, lw=1.6, ls="--", label="混合（55% / 45%）")
    ax.set_xlabel("场景三角形数")
    ax.set_ylabel("单次求交代价（相对）")
    ax.set_ylim(5, 200)
    ax.legend(loc="upper left", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig16-3-hybrid.png")


# ---------------------------------------------------------------- 图 16-3
def torus(p):
    rho = np.hypot(p[..., 0], p[..., 2])
    return np.hypot(rho - 1.0, p[..., 1]) - 0.35


def torus_grad(p):
    rho = np.hypot(p[..., 0], p[..., 2])
    q0, q1 = rho - 1.0, p[..., 1]
    n = np.hypot(q0, q1)
    gx = q0 / n * p[..., 0] / np.maximum(rho, 1e-9)
    gy = q1 / n
    gz = q0 / n * p[..., 2] / np.maximum(rho, 1e-9)
    return np.stack([gx, gy, gz], -1)


def fig16_3():
    rng = np.random.default_rng(6)
    P = rng.normal(size=(400, 3))
    P = P / np.linalg.norm(P, axis=1, keepdims=True) * rng.uniform(1.0, 2.0, (400, 1))
    errs = []
    Q = P.copy()
    for k in range(8):
        d = torus(Q)
        Q = Q - d[:, None] * torus_grad(Q)
        errs.append(np.abs(torus(Q)).mean())

    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.semilogy(np.arange(1, 9), errs, "o-", color=BLUE, ms=5, lw=1.7)
    ax.set_xlabel("投影迭代次数")
    ax.set_ylabel("到表面的平均剩余距离")
    ax.set_ylim(1e-8, 1.0)
    ax.text(2.2, 3e-3, "一步之后通常在 $10^{-2}$ 量级，\\n三步之后到 $10^{-5}$", fontsize=8,
            color="#3c4654")
    fig.tight_layout()
    save(fig, "fig16-1-projection.png")


if __name__ == "__main__":
    fig16_1()
    fig16_2()
    fig16_3()
