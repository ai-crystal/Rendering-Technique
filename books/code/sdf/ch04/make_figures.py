import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

# ---------------------------------------------------------------- 场与解析梯度
def torus_d(p, R=1.0, r=0.35):
    rho = np.hypot(p[0], p[2])
    return np.hypot(rho - R, p[1]) - r


def torus_grad(p, R=1.0, r=0.35):
    rho = np.hypot(p[0], p[2])
    q = np.array([rho - R, p[1]])
    n = np.linalg.norm(q)
    gx = q[0] / n * p[0] / rho
    gz = q[0] / n * p[2] / rho
    gy = q[1] / n
    return np.array([gx, gy, gz])


def grad_forward(f, p, h):
    e = np.eye(3) * h
    return np.array([(f(p + e[i]) - f(p)) / h for i in range(3)])


def grad_central(f, p, h):
    e = np.eye(3) * h
    return np.array([(f(p + e[i]) - f(p - e[i])) / (2 * h) for i in range(3)])


TETRA = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3.0)


def grad_tetra(f, p, h):
    s = np.zeros(3)
    for n in TETRA:
        s += f(p + h * n) * n
    return s * 3.0 / (4.0 * h)


# ---------------------------------------------------------------- 图 4-1
def fig4_1():
    p0 = np.array([1.0 + 0.12, 0.10, 0.0])
    g0 = torus_grad(p0)
    hs = np.logspace(-7, -1, 60)
    errs = {"fwd": [], "ctr": [], "tet": []}
    for h in hs:
        errs["fwd"].append(np.linalg.norm(grad_forward(torus_d, p0, h) - g0))
        errs["ctr"].append(np.linalg.norm(grad_central(torus_d, p0, h) - g0))
        errs["tet"].append(np.linalg.norm(grad_tetra(torus_d, p0, h) - g0))

    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.loglog(hs, errs["fwd"], color=RED, label="前向差分")
    ax.loglog(hs, errs["ctr"], color=BLUE, label="中心差分")
    ax.loglog(hs, errs["tet"], color=TEAL, ls="--", label="四面体法")
    ax.loglog(hs, 0.5 * hs, color=GREY, ls=":", lw=1.1, label=r"$O(h)$")
    ax.loglog(hs, 0.25 * hs ** 2, color=GREY, ls="-.", lw=1.1, label=r"$O(h^2)$")
    ax.set_xlabel("差分步长 h")
    ax.set_ylabel("梯度误差（2-范数）")
    ax.set_ylim(1e-12, 1e2)
    ax.legend(loc="lower right", ncol=2, fontsize=7.5)
    ax.axvspan(1e-7, 3e-5, color=GREY, alpha=0.10)
    ax.text(0.03, 0.30, "灰区为舍入误差主导的区间", transform=ax.transAxes,
            fontsize=7.5, color="#3c4654", va="bottom")
    fig.tight_layout()
    save(fig, "fig4-1-gradient-error.png")


# ---------------------------------------------------------------- 图 4-2
def hess_eigs_sphere(t, h):
    """半径 1 的球，在半径 1+t 处用中心差分估 Hessian 的两个特征值。"""
    p = np.array([1.0 + t, 0.0, 0.0])

    def f(x):
        return np.linalg.norm(x) - 1.0

    H = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            ei, ej = np.eye(3)[i], np.eye(3)[j]
            H[i, j] = (f(p + h * ei + h * ej) - f(p + h * ei - h * ej)
                       - f(p - h * ei + h * ej) + f(p - h * ei - h * ej)) / (4 * h * h)
    w = np.linalg.eigvalsh(H)
    return w


def fig4_2():
    ts = np.linspace(0.0, 0.9, 200)
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))

    ax = axes[0]
    ax.plot(ts, 1.0 / (1.0 + ts), color=BLUE, lw=1.6,
            label=r"解析：$\kappa/(1+\kappa t)=1/(1+t)$")
    for h, col in ((0.05, RED), (0.02, TEAL)):
        vals = [hess_eigs_sphere(t, h)[2] for t in ts[::10]]
        ax.plot(ts[::10], vals, "o", ms=3.2, color=col, label=f"二阶差分 h = {h}")
    ax.set_xlabel("离表面的距离 t")
    ax.set_ylabel("切向特征值")
    ax.set_ylim(0.4, 1.3)
    ax.legend(loc="upper right", fontsize=7.5)
    panel_label(ax, "(a)", x=-0.15, y=1.06)

    ax = axes[1]
    hs = np.logspace(-4, -0.7, 40)
    fig2 = []
    for h in hs:
        w = hess_eigs_sphere(0.2, h)
        fig2.append(abs(w[2] - 1.0 / 1.2))
    ax.loglog(hs, fig2, color=PURPLE, marker="o", ms=3, lw=1.2)
    ax.loglog(hs, 2.0 * hs ** 2, color=GREY, ls=":", lw=1.1, label=r"$O(h^2)$")
    ax.set_xlabel("差分步长 h")
    ax.set_ylabel("特征值误差")
    ax.legend(loc="lower right", fontsize=7.5)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig4-2-curvature.png")


# ---------------------------------------------------------------- 图 4-3
C1 = np.array([-1.0, 0.0])
C2 = np.array([1.0, 0.0])
R = 0.56


def two_circles(p):
    d1 = np.linalg.norm(p - C1, axis=-1) - R
    d2 = np.linalg.norm(p - C2, axis=-1) - R
    return np.minimum(d1, d2)


def fig4_3():
    n = 420
    xs = np.linspace(-2.1, 2.1, n)
    ys = np.linspace(-1.5, 1.5, n)
    X, Y = np.meshgrid(xs, ys)
    hstep = xs[1] - xs[0]

    def f2(x, y):
        return np.minimum(np.hypot(x - C1[0], y - C1[1]) - R,
                          np.hypot(x - C2[0], y - C2[1]) - R)

    d1 = np.hypot(X - C1[0], Y - C1[1])
    d2 = np.hypot(X - C2[0], Y - C2[1])
    use1 = d1 < d2
    gx = np.where(use1, (X - C1[0]) / d1, (X - C2[0]) / d2)
    gy = np.where(use1, (Y - C1[1]) / d1, (Y - C2[1]) / d2)

    step = 6 * hstep
    ngx = (f2(X + step, Y) - f2(X - step, Y)) / (2 * step)
    ngy = (f2(X, Y + step) - f2(X, Y - step)) / (2 * step)
    nrm = np.maximum(np.hypot(ngx, ngy), 1e-12)
    ang = np.degrees(np.arccos(np.clip((ngx * gx + ngy * gy) / nrm, -1, 1)))
    d = f2(X, Y)
    ang = np.where(d > 0.05, ang, np.nan)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))
    ax = axes[0]
    im = ax.pcolormesh(X, Y, ang, cmap="inferno", shading="auto", vmin=0, vmax=30)
    ax.contour(X, Y, d, levels=[0.0], colors="cyan", linewidths=1.3)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label("法线夹角误差（度）", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    panel_label(ax, "(a)", x=-0.16, y=1.06)

    ax = axes[1]
    xx = np.linspace(-0.40, 0.40, 800)
    for mult, col in ((2, BLUE), (6, TEAL), (14, RED)):
        hh = mult * hstep
        gxn = (f2(xx + hh, 0.0) - f2(xx - hh, 0.0)) / (2 * hh)
        gyn = (f2(xx, hh) - f2(xx, -hh)) / (2 * hh)
        ax.plot(xx, np.hypot(gxn, gyn), color=col, label=f"差分步长 {mult} 格")
    ax.axhline(1.0, color=GREY, ls=":", lw=1.0)
    ax.text(-0.39, 1.02, "解析值恒为 1", fontsize=7.5, color=GREY)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel("跨越中轴的位置 x")
    ax.set_ylabel("差分梯度长度")
    ax.legend(loc="lower right", fontsize=7.5)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig4-3-medial-normal.png")


if __name__ == "__main__":
    fig4_1()
    fig4_2()
    fig4_3()
