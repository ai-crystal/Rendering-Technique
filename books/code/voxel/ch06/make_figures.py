import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

rng = np.random.default_rng(11)


# ---------------------------------------------------------------- 图 6-1
def fig6_1():
    R = 1.0
    b = np.linspace(0, 0.98, 60)

    def steps(b, relax=1.0, eps=1e-4, tmax=12.0):
        p = np.array([b, 0.0, -3.0])
        d = np.array([0.0, 0.0, 1.0])
        t, n = 0.0, 0
        while n < 4000:
            q = p + t * d
            dist = np.linalg.norm(q) - R
            if dist < eps:
                return n
            t += relax * dist
            n += 1
            if t > tmax:
                return n
        return n

    s1 = np.array([steps(x, 1.0) for x in b])
    s2 = np.array([steps(x, 0.9) for x in b])

    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(b, s1, color=BLUE, label="步长 = 距离")
    ax.plot(b, s2, color=ACCENT, ls="--", label="步长 = 0.9 × 距离")
    ax.set_xlabel("射线到球心的距离（球半径归一）")
    ax.set_ylabel("步进次数")
    ax.set_yscale("log")
    ax.legend(loc="upper left")
    note(ax, "球半径 1，起点距球心 3，终止阈值 $10^{-4}$", 0.30, 0.90)
    fig.tight_layout()
    save(fig, "fig6-1-steps.png")


# ---------------------------------------------------------------- 图 6-2
def sdf_sphere(p, R):
    return np.linalg.norm(p, axis=-1) - R


def trilinear(p, R, h):
    g = p / h
    i0 = np.floor(g).astype(int)
    f = g - i0
    val = 0.0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = ((f[:, 0] if dx else 1 - f[:, 0]) *
                     (f[:, 1] if dy else 1 - f[:, 1]) *
                     (f[:, 2] if dz else 1 - f[:, 2]))
                c = (i0 + np.array([dx, dy, dz])) * h
                val = val + w * sdf_sphere(c, R)
    return val


def fig6_2():
    R = 1.0
    ratios = np.array([4, 6, 8, 12, 16, 24, 32, 48, 64, 96])
    rms_tri, rms_occ = [], []
    N = 4000
    d = rng.normal(size=(N, 3))
    d /= np.linalg.norm(d, axis=1)[:, None]
    pts = d * R
    for r in ratios:
        h = R / r
        f = trilinear(pts, R, h)
        rms_tri.append(np.sqrt(np.mean(f ** 2)))
        rms_occ.append(1.0)          # 占据率表面的误差恒为一个格子量级
    rms_tri = np.array(rms_tri)

    fig, ax = plt.subplots(figsize=(6.1, 3.4))
    ax.loglog(ratios, rms_tri, color=BLUE, marker="o", ms=3,
              label="三线性插值距离场")
    ax.loglog(ratios, 0.35 / ratios, color=GREY, ls=":", label="误差 $\propto h$")
    ax.loglog(ratios, 0.35 / ratios ** 2, color=TEAL, ls="--", label="误差 $\propto h^2$")
    ax.set_xlabel("球半径 / 体素边长")
    ax.set_ylabel("表面位置误差（球半径归一）")
    ax.legend(loc="lower left", fontsize=7.6)
    note(ax, "误差按真实球面上的 4000 个点统计", 0.40, 0.93)
    fig.tight_layout()
    save(fig, "fig6-2-interp.png")


# ---------------------------------------------------------------- 图 6-3
def fig6_3():
    h = 0.1
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1), sharey=True)
    for ax, off, ttl in ((axes[0], 0.0, "格子对齐板心"),
                         (axes[1], 0.5, "格子偏移半格")):
        x = np.linspace(-4.5, 4.5, 400)
        for d, col in ((0.25, RED), (0.5, GOLD), (1.0, TEAL), (2.0, BLUE)):
            f = np.abs(x) - d / 2
            ax.plot(x, f, color=col, lw=1.3, label=f"厚度 {d:.2f} 格")
            xs = np.arange(-5, 6) + off
            fs = np.abs(xs) - d / 2
            ax.plot(xs, fs, "o", color=col, ms=3.4)
        ax.axhline(0, color=INK, lw=0.8)
        ax.set_xlabel("沿板法线的位置（体素边长）")
        ax.set_title(ttl, fontsize=8.5)
        ax.set_xlim(-4.6, 4.6)
    axes[0].set_ylabel("距离场的采样值（体素边长）")
    axes[0].set_ylim(-1.4, 3.6)
    h1, l1 = axes[0].get_legend_handles_labels()
    fig.legend(h1, l1, loc="lower center", ncol=4, fontsize=7.6,
               bbox_to_anchor=(0.5, -0.04), frameon=False)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "fig6-3-thin.png")


if __name__ == "__main__":
    fig6_1()
    fig6_2()
    fig6_3()
