import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

rng = np.random.default_rng(3)


def fib_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    theta = np.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(theta) * np.sin(phi),
                     np.sin(theta) * np.sin(phi),
                     np.cos(phi)], axis=1)


def sh_basis(d):
    x, y, z = d[:, 0], d[:, 1], d[:, 2]
    return np.stack([
        0.282095 * np.ones_like(x),
        0.488603 * y, 0.488603 * z, 0.488603 * x,
        1.092548 * x * y, 1.092548 * y * z,
        0.315392 * (3 * z * z - 1), 1.092548 * x * z,
        0.546274 * (x * x - y * y)], axis=1)


# ---------------------------------------------------------------- 图 5-1
def fig5_1():
    k = np.arange(0, 31)
    fig, ax = plt.subplots(figsize=(6.1, 3.3))
    for rho, col in ((0.5, BLUE), (0.7, TEAL), (0.85, ACCENT)):
        ax.semilogy(k, rho ** k, color=col, marker="o", ms=3,
                    label=f"反照率 {rho}")
        n1 = int(np.ceil(np.log(0.01) / np.log(rho)))
        ax.plot([n1], [rho ** n1], "o", mfc="none", mec=col, ms=9, mew=1.2)
    ax.axhline(0.01, color=GREY, ls=":", lw=1.1)
    ax.text(9.4, 0.0125, "1% 残差", fontsize=7.5, color="#3c4654")
    ax.set_xlabel("弹射次数（迭代次数）")
    ax.set_ylabel("剩余能量比例")
    ax.set_ylim(1e-3, 1.4)
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, "fig5-1-bounces.png")


# ---------------------------------------------------------------- 图 5-2
def fig5_2():
    dirs = fib_sphere(6000)
    dw = 4 * np.pi / len(dirs)
    w0 = np.array([0.0, 0.0, 1.0])
    B = sh_basis(dirs)
    nrm = fib_sphere(1200)

    kappas = np.array([0.0, 0.4, 0.8, 1.5, 3, 6, 12, 25, 60, 150, 400])
    half_angle = []
    err_scalar, err_cube, err_sh1, err_sh2 = [], [], [], []
    A = np.array([np.pi, 2 * np.pi / 3, 2 * np.pi / 3, 2 * np.pi / 3,
                  np.pi / 4, np.pi / 4, np.pi / 4, np.pi / 4, np.pi / 4])

    for kap in kappas:
        L = np.exp(kap * (dirs @ w0 - 1.0))
        L = L / (L.sum() * dw) * 4 * np.pi          # 总能量归一，便于比较
        # 真实辐照度
        cosn = np.clip(nrm @ dirs.T, 0, None)
        E_true = (cosn * L[None, :]).sum(axis=1) * dw
        # 单标量：存平均辐亮度，重建时当各向同性
        s = (L * dw).sum() / (4 * np.pi)
        E_s = np.pi * s * np.ones_like(E_true)
        # 环境立方体：六个轴上的投影
        axes = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0],
                         [0, -1, 0], [0, 0, 1], [0, 0, -1]], float)
        Ec = np.array([(np.clip(dirs @ a, 0, None) * L).sum() * dw for a in axes])
        W = np.clip(nrm @ axes.T, 0, None)
        E_c = W @ Ec
        # 球谐：1 阶（4 项）与 2 阶（9 项）
        c = B.T @ (L * dw)
        for deg, store in ((1, err_sh1), (2, err_sh2)):
            m = 4 if deg == 1 else 9
            E_sh = (sh_basis(nrm)[:, :m] * (A[:m] * c[:m])[None, :]).sum(axis=1)
            store.append(np.sqrt(np.mean((E_sh - E_true) ** 2)) / E_true.mean())
        err_scalar.append(np.sqrt(np.mean((E_s - E_true) ** 2)) / E_true.mean())
        err_cube.append(np.sqrt(np.mean((E_c - E_true) ** 2)) / E_true.mean())
        half_angle.append(np.rad2deg(np.arccos(np.clip(1 - np.log(2) / kap, -1, 1)))
                          if kap > 0 else 180.0)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.semilogx(half_angle, np.array(err_scalar) * 100, color=RED, marker="o", ms=3,
                label="单标量")
    ax.semilogx(half_angle, np.array(err_cube) * 100, color=GOLD, marker="s", ms=3,
                label="六方向（环境立方体）")
    ax.semilogx(half_angle, np.array(err_sh1) * 100, color=TEAL, marker="^", ms=3,
                label="球谐 1 阶（4 项）")
    ax.semilogx(half_angle, np.array(err_sh2) * 100, color=BLUE, marker="d", ms=3,
                label="球谐 2 阶（9 项）")
    ax.invert_xaxis()
    ax.set_xlabel("入射光的半高角宽度（度）")
    ax.set_ylabel("辐照度的相对均方根误差（%）")
    ax.legend(loc="upper left", fontsize=7.6)
    fig.tight_layout()
    save(fig, "fig5-2-directionality.png")


if __name__ == "__main__":
    fig5_1()
    fig5_2()
