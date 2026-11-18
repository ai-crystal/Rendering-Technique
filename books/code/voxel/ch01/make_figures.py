import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

# ---------------------------------------------------------------- 图 1-1
def fig1_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0))

    # (a) 阶梯高度误差：平面倾斜 30 度，量化到边长 h 的格子里
    ax = axes[0]
    hs = np.linspace(0.002, 0.04, 60)          # 单位 m
    theta = np.deg2rad(30.0)
    rms, mx = [], []
    for h in hs:
        x = np.arange(0.0, 2.0, h / 40.0)
        true = x * np.tan(theta)
        stair = np.floor(true / h) * h
        e = stair - true
        rms.append(np.sqrt(np.mean(e ** 2)))
        mx.append(np.max(np.abs(e)))
    ax.plot(hs * 1000, np.array(rms) * 1000, color=BLUE, label="均方根误差")
    ax.plot(hs * 1000, np.array(mx) * 1000, color=ACCENT, label="最大误差")
    ax.plot(hs * 1000, hs / np.sqrt(3) * 1000, color=GREY, ls=":", lw=1.4,
            label=r"$h/\sqrt{3}$")
    ax.set_xlabel("体素边长 h（mm）")
    ax.set_ylabel("表面位置误差（mm）")
    ax.set_title("位置误差与 h 成正比")
    ax.legend(loc="upper left")

    # (b) 法线误差：阶梯只有轴对齐的面，与 h 无关
    ax = axes[1]
    th = np.linspace(0.5, 89.5, 300)
    t = np.deg2rad(th)
    frac_h = 1.0 / (1.0 + np.tan(t))
    frac_v = np.tan(t) / (1.0 + np.tan(t))
    mean_err = frac_h * th + frac_v * (90.0 - th)
    ax.plot(th, mean_err, color=RED, label="阶梯表面平均误差")
    ax.axhline(45.0, color=GREY, ls=":", lw=1.2, label="45 度")
    ax.set_xlabel("表面倾角（度）")
    ax.set_ylabel("法线夹角误差（度）")
    ax.set_ylim(0, 90)
    ax.set_title("法线误差与 h 无关")
    ax.legend(loc="lower center")

    fig.tight_layout()
    save(fig, "fig1-1-staircase.png")


# ---------------------------------------------------------------- 图 1-2
def ggx_D(n_dot_h, alpha):
    a2 = alpha * alpha
    c2 = np.clip(n_dot_h, 1e-6, 1.0) ** 2
    return a2 / (np.pi * (c2 * (a2 - 1.0) + 1.0) ** 2)


VIEW = np.array([0.0, 0.0, 1.0])
LIGHT = np.array([-0.42, 0.0, 0.91])
LIGHT = LIGHT / np.linalg.norm(LIGHT)
HALF = (VIEW + LIGHT) / np.linalg.norm(VIEW + LIGHT)


def sphere_normals(n=241, cells=None):
    xs = (np.arange(n) + 0.5) / n * 2.0 - 1.0
    X, Y = np.meshgrid(xs, xs)
    r2 = X * X + Y * Y
    mask = r2 <= 1.0
    Z = np.sqrt(np.clip(1.0 - r2, 0.0, None))
    if cells is None:
        return X, Y, Z, mask
    # 体素球：正面看过去，每个柱体最高处的面朝向 +z；轮廓一圈是侧面
    r = np.sqrt(np.maximum(r2, 1e-12))
    ring = r > 1.0 - 1.0 / cells
    ang = np.round(np.arctan2(Y, X) / (np.pi / 4.0)) * (np.pi / 4.0)
    nx = np.where(ring, np.cos(ang), 0.0)
    ny = np.where(ring, np.sin(ang), 0.0)
    nz = np.where(ring, 0.0, 1.0)
    return nx, ny, nz, mask


def shade(alpha, n=241, cells=None):
    nx, ny, nz, mask = sphere_normals(n, cells)
    ndoth = nx * HALF[0] + ny * HALF[1] + nz * HALF[2]
    ndotv = np.clip(nz, 1e-3, None)
    val = ggx_D(ndoth, alpha) / (4.0 * ndotv)
    return np.where(mask, val, np.nan)


def fig1_2():
    alpha = 0.25
    n = 241
    exact = shade(alpha, n)
    v8 = shade(alpha, n, cells=8)
    vmax = np.nanmax(exact)
    disp = lambda a: np.clip(a / vmax, 0, 1) ** 0.45

    fig, axes = plt.subplots(2, 2, figsize=(7.2, 4.6),
                             gridspec_kw={"height_ratios": [1, 1.05]})
    for ax, img, ttl in ((axes[0, 0], exact, "解析法线"),
                         (axes[0, 1], v8, "体素球，半径 8 格")):
        ax.imshow(disp(img), cmap="inferno", origin="lower",
                  extent=[-1, 1, -1, 1], vmin=0, vmax=1)
        ax.set_title(ttl, pad=3)
        ax.set_xticks([]); ax.set_yticks([])
        ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_xlabel("同一光照，alpha = 0.25", labelpad=2)

    x = np.linspace(-1, 1, n)
    ax = axes[1, 0]
    ax.plot(x, exact[n // 2] / vmax, color=BLUE, label="解析法线")
    ax.plot(x, v8[n // 2] / vmax, color=RED, lw=1.2, label="半径 8 格")
    ax.set_xlabel("屏幕横坐标（球半径归一）")
    ax.set_ylabel("辐亮度 / 解析峰值")
    ax.set_title("过球心的剖面")
    ax.set_xlim(-0.86, 0.86)
    ax.set_ylim(0, 1.12)
    ax.legend(loc="upper left")

    ax = axes[1, 1]
    for cells, col, ls in ((8, RED, "-"), (32, GOLD, "--"), (64, GREEN, ":")):
        nx, ny, nz, mask = sphere_normals(n, cells)
        X, Y = np.meshgrid(np.linspace(-1, 1, n), np.linspace(-1, 1, n))
        r = np.minimum(np.sqrt(np.maximum(X ** 2 + Y ** 2, 1e-12)), 1.0)
        ct = np.clip(nx * X + ny * Y + nz * np.sqrt(np.clip(1 - r ** 2, 0, 1)), -1, 1)
        err = np.rad2deg(np.arccos(ct))
        err[r > 1.0 - 1.5 / cells] = np.nan
        ax.plot(x, err[n // 2], color=col, ls=ls, lw=1.4, label=f"{cells} 格")
    ax.set_xlabel("屏幕横坐标（球半径归一）")
    ax.set_ylabel("法线与真实法线夹角（度）")
    ax.set_title("法线误差不随分辨率缩小")
    ax.set_xlim(-0.95, 0.95)
    ax.legend(loc="upper center")

    fig.tight_layout(w_pad=0.6)
    save(fig, "fig1-2-highlight.png")


# ---------------------------------------------------------------- 图 1-3
def fig1_3():
    hs = np.logspace(np.log10(0.001), np.log10(0.10), 200)   # m
    A = 2 * (10 * 10) + 4 * (10 * 4)                          # 房间内表面 m^2
    V = 10 * 10 * 4
    bytes_dense = V / hs ** 3 * 4
    bytes_shell = A * (2 * hs) / hs ** 3 * 4
    bytes_octree = 1.33 * (A / hs ** 2) * 12
    bytes_sdf = A * (6 * hs) / hs ** 3 * 4

    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.loglog(hs * 1000, bytes_dense / 1e9, color=ACCENT, label="稠密网格")
    ax.loglog(hs * 1000, bytes_sdf / 1e9, color=TEAL, label="窄带距离场（带宽 6 格）")
    ax.loglog(hs * 1000, bytes_shell / 1e9, color=BLUE, label="两层表面壳")
    ax.loglog(hs * 1000, bytes_octree / 1e9, color=GREEN, label="稀疏八叉树")
    ax.axhline(8.0, color=RED, ls="--", lw=1.2)
    ax.text(1.1, 9.2, "8 GB 预算", color=RED, fontsize=8)
    ax.set_xlabel("体素边长 h（mm）")
    ax.set_ylabel("内存（GB）")
    ax.set_ylim(1e-4, 1e4)
    ax.legend(loc="upper right")
    note(ax, "10 m × 10 m × 4 m 房间，每体素 4 字节", 0.03, 0.06)
    fig.tight_layout()
    save(fig, "fig1-3-memory.png")


if __name__ == "__main__":
    fig1_1()
    fig1_2()
    fig1_3()
