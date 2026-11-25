import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np


def sd_circle(p, c, r):
    return np.linalg.norm(p - c, axis=-1) - r


def scene(p):
    d1 = sd_circle(p, np.array([-0.45, 0.0]), 0.55)
    d2 = sd_circle(p, np.array([0.55, 0.15]), 0.42)
    return np.minimum(d1, d2)


# ---------------------------------------------------------------- 图 10-1
def fig10_1():
    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    th = np.linspace(0, 2 * np.pi, 600)
    for c, r in ((np.array([-0.45, 0.0]), 0.55), (np.array([0.55, 0.15]), 0.42)):
        ax.plot(c[0] + r * np.cos(th), c[1] + r * np.sin(th), color=INK, lw=1.6)

    starts = [np.array([-3.60, 1.05]), np.array([-3.60, 0.10]), np.array([-3.60, -1.00])]
    # 三条光线：从左侧射向原点附近，方向单位化
    targets = [np.array([-0.45, 0.42]), np.array([-0.30, 0.02]), np.array([-0.62, -0.38])]
    for s, tg in zip(starts, targets):
        u = tg - s
        u = u / np.linalg.norm(u)
        t, pts = 0.0, [s.copy()]
        for _ in range(40):
            v = float(scene(s + t * u))
            if v < 2e-3:
                break
            circ = plt.Circle(s + t * u, v, fill=False, ec=BLUE, lw=0.55, alpha=0.55)
            ax.add_patch(circ)
            t += v
            pts.append(s + t * u)
        pts = np.array(pts)
        ax.plot(pts[:, 0], pts[:, 1], "-o", color=ACCENT, ms=2.6, lw=1.0, alpha=0.9)

    ax.set_aspect("equal")
    ax.set_xlim(-3.9, 1.15)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    fig.tight_layout()
    save(fig, "fig10-1-sphere-trace.png")


# ---------------------------------------------------------------- 图 10-2
def march_steps(o, u, eps, maxit=2000):
    t = 0.0
    for i in range(maxit):
        v = float(scene(o + t * u))
        if v < eps:
            return i + 1, t
        t += v
    return maxit, t


def sphere_steps(b, eps, maxit=20000):
    """半径 1 的球，光线从 (-4, b) 沿 +x，返回迭代次数。"""
    t = 0.0
    for i in range(maxit):
        x, y = -4.0 + t, b
        v = np.hypot(x, y) - 1.0
        if v < eps:
            return i + 1
        t += v
        if t > 12.0:
            break
    return maxit


def fig10_2():
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))
    ax = axes[0]
    eps = np.logspace(-6, -1.5, 30)
    for b, col in ((0.0, BLUE), (0.90, TEAL), (0.98, ACCENT), (0.995, RED)):
        cnt = [sphere_steps(b, e) for e in eps]
        ax.loglog(eps, cnt, color=col, lw=1.5, label=f"碰撞参数 b = {b}")
    ax.set_xlabel(r"终止精度 $\epsilon$")
    ax.set_ylabel("迭代次数")
    ax.legend(loc="upper right", fontsize=7.2)
    panel_label(ax, "(a)", x=-0.15, y=1.06)

    ax = axes[1]
    bs = np.linspace(0.0, 0.9995, 120)
    cnt = [sphere_steps(b, 1e-4) for b in bs]
    ang = np.degrees(np.arccos(np.sqrt(np.clip(1 - bs ** 2, 0, 1))))
    ax.semilogy(ang, cnt, color=PURPLE, lw=1.8)
    ax.set_xlabel("光线与表面法线的夹角（度）")
    ax.set_ylabel("迭代次数")
    ax.set_xlim(0, 90)
    note(ax, "越接近掠射，步进越慢", 0.10, 0.86, size=7.5)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig10-2-steps.png")


# ---------------------------------------------------------------- 图 10-3
def fig10_3():
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    for eps0, col in ((1e-2, BLUE), (1e-4, RED)):
        o = np.array([-2.0, 0.0])
        a = np.deg2rad(35.0)
        u = np.array([np.cos(a), np.sin(a)])
        t, resid = 0.0, []
        for _ in range(60):
            v = float(scene(o + t * u))
            # 到真实表面的剩余距离：对每个圆求 | |p-c| - r |
            p_ = o + t * u
            true_res = min(abs(np.linalg.norm(p_ - np.array([-0.45, 0.0])) - 0.55),
                           abs(np.linalg.norm(p_ - np.array([0.55, 0.15])) - 0.42))
            resid.append(true_res)
            if v < eps0:
                break
            t += v
        ax.semilogy(np.arange(len(resid)), resid, color=col, lw=1.6,
                    label="球体追踪，" + r"$\epsilon$ = %g" % eps0)
    ax.set_xlabel("迭代次数")
    ax.set_ylabel("到表面的剩余距离")
    ax.set_ylim(1e-7, 0.5)
    ax.legend(loc="upper right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig10-3-convergence.png")


if __name__ == "__main__":
    fig10_1()
    fig10_2()
    fig10_3()
