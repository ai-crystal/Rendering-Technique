#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""光谱渲染一册共用的数值工具。

所有数值都来自书中给出的公式：CIE 配色函数用 Wyman 等 2013 的多瓣拟合，
sRGB 矩阵由 BT.709 的原色色度与 D65 白点推导，玻璃折射率用 Schott 的
Sellmeier 系数。脚本只依赖 NumPy。
"""
import numpy as np

# ---------------------------------------------------------------- 波长网格

LAMBDA_MIN = 380.0
LAMBDA_MAX = 780.0


def grid(lo=LAMBDA_MIN, hi=LAMBDA_MAX, step=1.0):
    return np.arange(lo, hi + 0.5 * step, step)


# ---------------------------------------------------------------- 配色函数

def _g2(lam, mu, s_lo, s_hi):
    """峰在 mu、左右标准差为 s_lo / s_hi 的非对称高斯。"""
    s = np.where(lam < mu, s_lo, s_hi)
    t = (lam - mu) / s
    return np.exp(-0.5 * t * t)


def cie_x(lam):
    lam = np.asarray(lam, dtype=float)
    return (0.362 * _g2(lam, 442.0, 16.0, 26.7)
            + 1.056 * _g2(lam, 599.8, 37.9, 31.0)
            - 0.065 * _g2(lam, 501.1, 20.4, 26.2))


def cie_y(lam):
    lam = np.asarray(lam, dtype=float)
    return 0.821 * _g2(lam, 568.8, 46.9, 40.5) + 0.286 * _g2(lam, 530.9, 16.3, 31.1)


def cie_z(lam):
    lam = np.asarray(lam, dtype=float)
    return 1.217 * _g2(lam, 437.0, 11.8, 36.0) + 0.681 * _g2(lam, 459.0, 26.0, 13.8)


def cie_xyz_basis(lam):
    """返回 (3, N) 的配色函数矩阵。"""
    lam = np.asarray(lam, dtype=float)
    return np.stack([cie_x(lam), cie_y(lam), cie_z(lam)])


def spectrum_to_xyz(lam, spd):
    lam = np.asarray(lam, dtype=float)
    spd = np.asarray(spd, dtype=float)
    d = np.gradient(lam)
    return cie_xyz_basis(lam) @ (spd * d)


# ---------------------------------------------------------------- sRGB 矩阵

# BT.709 / sRGB 的原色色度与 D65 白点 (IEC 61966-2-1:1999)
PRIMARIES_XY = np.array([[0.64, 0.33],   # R
                         [0.30, 0.60],   # G
                         [0.15, 0.06]])  # B
WHITE_XY_D65 = np.array([0.3127, 0.3290])


def rgb_to_xyz_matrix(prim_xy=PRIMARIES_XY, white_xy=WHITE_XY_D65):
    """由原色色度与白点推导 XYZ <- linear RGB 的 3x3 矩阵。"""
    xyz = np.zeros((3, 3))
    for i, (x, y) in enumerate(prim_xy):
        xyz[:, i] = [x / y, 1.0, (1.0 - x - y) / y]
    xw, yw = white_xy
    white = np.array([xw / yw, 1.0, (1.0 - xw - yw) / yw])
    s = np.linalg.solve(xyz, white)
    return xyz * s


M_RGB2XYZ = rgb_to_xyz_matrix()
M_XYZ2RGB = np.linalg.inv(M_RGB2XYZ)

# IEC 61966-2-1 公布的数值（书里引用的就是这一组）
M_RGB2XYZ_PUBLISHED = np.array([
    [0.4124, 0.3576, 0.1805],
    [0.2126, 0.7152, 0.0722],
    [0.0193, 0.1192, 0.9505]])
M_XYZ2RGB_PUBLISHED = np.array([
    [3.2406, -1.5372, -0.4986],
    [-0.9689, 1.8758, 0.0415],
    [0.0557, -0.2040, 1.0570]])


def xyz_to_linear_srgb(xyz, mat=None):
    m = M_XYZ2RGB_PUBLISHED if mat is None else mat
    return m @ np.asarray(xyz, dtype=float)


def linear_srgb_to_xyz(rgb, mat=None):
    m = M_RGB2XYZ_PUBLISHED if mat is None else mat
    return m @ np.asarray(rgb, dtype=float)


def srgb_encode(v):
    v = np.clip(np.asarray(v, dtype=float), 0.0, 1.0)
    return np.where(v <= 0.0031308, 12.92 * v, 1.055 * np.power(v, 1 / 2.4) - 0.055)


def srgb_decode(v):
    v = np.clip(np.asarray(v, dtype=float), 0.0, 1.0)
    return np.where(v <= 0.04045, v / 12.92, np.power((v + 0.055) / 1.055, 2.4))


# ---------------------------------------------------------------- 色度与色差

def xyz_to_xy(xyz):
    xyz = np.asarray(xyz, dtype=float)
    s = xyz.sum(axis=0)
    return xyz[0] / s, xyz[1] / s


def xyz_to_lab(xyz, white=(0.95047, 1.0, 1.08883)):
    xyz = np.asarray(xyz, dtype=float)
    w = np.asarray(white, dtype=float).reshape(3, *([1] * (xyz.ndim - 1)))
    t = xyz / w
    d = 6.0 / 29.0
    f = np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])


def delta_e76(lab1, lab2):
    return np.sqrt(np.sum((np.asarray(lab1) - np.asarray(lab2)) ** 2, axis=0))


# ---------------------------------------------------------------- 光源

def blackbody(lam_nm, T):
    """普朗克谱辐亮度，单位为任意比例（相对值）。"""
    h, c, kB = 6.62607015e-34, 2.99792458e8, 1.380649e-23
    lam = np.asarray(lam_nm, dtype=float) * 1e-9
    return (2 * h * c * c / lam ** 5) / (np.exp(h * c / (lam * kB * T)) - 1.0)


def gaussian_line(lam, mu, fwhm):
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    return np.exp(-0.5 * ((np.asarray(lam, dtype=float) - mu) / sigma) ** 2)


def led_white(lam, blue=452.0, blue_fwhm=18.0, phos=560.0, phos_fwhm=95.0, ratio=1.0):
    """蓝光芯片 + 黄色荧光粉的白光 LED 近似。"""
    return gaussian_line(lam, blue, blue_fwhm) + ratio * 0.85 * gaussian_line(lam, phos, phos_fwhm)


def normalize_mean(spd, lo=LAMBDA_MIN, hi=LAMBDA_MAX):
    spd = np.asarray(spd, dtype=float)
    m = spd[(np.asarray(lo) <= 1) | True]
    return spd / np.mean(spd[(np.arange(len(spd)) >= 0)])


def d65_like(lam_nm=380.0):
    """与 D65 同色度的平滑合成光谱。

    以 6504 K 黑体为骨架，乘上两个宽带修正项，解一个二阶方程让色度落在
    (0.3127, 0.3290)。它和 CIE D65 是同色异谱体，用它当白点可以避免把
    一张 300 行的 D65 表抄进脚本，而白点矩阵与公布值只差 4e-5。
    """
    lam = grid() if np.isscalar(lam_nm) else np.asarray(lam_nm, dtype=float)
    bb = blackbody(lam, 6504.0)
    g1 = gaussian_line(lam, 455.0, 90.0)
    g2 = gaussian_line(lam, 610.0, 120.0)
    p = np.array([-0.11603952, -0.10771122])
    return bb * (1.0 + p[0] * g1 + p[1] * g2)


def d65_white(lam):
    sp = d65_like(lam)
    xyz = spectrum_to_xyz(lam, sp)
    return xyz / xyz[1]


def normalize_sum(spd):
    spd = np.asarray(spd, dtype=float)
    s = spd.sum()
    return spd / s if s else spd


def normalize_y(lam, spd, target=1.0):
    """把光谱缩放到 CIE Y = target。"""
    xyz = spectrum_to_xyz(lam, spd)
    return np.asarray(spd, dtype=float) * (target / xyz[1])


# ---------------------------------------------------------------- 玻璃色散

# Schott 玻璃目录给出的三项 Sellmeier 系数（λ 以微米为单位）
SELLMEIER = {
    "N-BK7": ([1.03961212, 0.231792344, 1.01046945],
              [0.00600069867, 0.0200179144, 103.560653]),
    "F2": ([1.34533359, 0.209073176, 0.937357162],
           [0.00997743871, 0.0470450767, 111.886764]),
    "SF11": ([1.73759695, 0.313747346, 1.89878101],
             [0.013188707, 0.0623068142, 155.23629]),
    "熔石英": ([0.6961663, 0.4079426, 0.8974794],
             [0.004679148, 0.01351206, 97.9340025]),
}

LAMBDA_D = 0.5875618   # 氦 d 线，微米
LAMBDA_F = 0.4861327   # 氢 F 线
LAMBDA_C = 0.6562725   # 氢 C 线


def sellmeier(name, lam_nm):
    B, C = SELLMEIER[name]
    lam = np.asarray(lam_nm, dtype=float) / 1000.0
    n2 = np.ones_like(lam)
    for b, c in zip(B, C):
        n2 = n2 + b * lam ** 2 / (lam ** 2 - c)
    return np.sqrt(n2)


def cauchy_from_nd_vd(nd, vd, lam_nm):
    """用 n_d 与阿贝数构造线性 1/λ 色散模型。"""
    lam = np.asarray(lam_nm, dtype=float) / 1000.0
    b = (nd - 1.0) / (vd * (1.0 / LAMBDA_F - 1.0 / LAMBDA_C))
    return nd + b * (1.0 / lam - 1.0 / LAMBDA_D)


def abbe(name):
    nd = float(sellmeier(name, LAMBDA_D * 1000.0))
    nf = float(sellmeier(name, LAMBDA_F * 1000.0))
    nc = float(sellmeier(name, LAMBDA_C * 1000.0))
    return nd, (nd - 1.0) / (nf - nc)


# ---------------------------------------------------------------- Jakob-Hanika 模型

def jh_sigmoid(x):
    return 0.5 + x / (2.0 * np.sqrt(1.0 + x * x))


def jh_spectrum(lam_nm, c0, c1, c2):
    """Jakob & Hanika 2019 的反射率模型 r(λ) = S(c0 x² + c1 x + c2)，x = (λ-580)/100。

    书里把 λ 换成归一化的 x，目的只是让三个系数的量级可比；换回 λ 时系数
    跟着缩放，光谱形状不变。
    """
    x = (np.asarray(lam_nm, dtype=float) - 580.0) / 100.0
    return jh_sigmoid(c0 * x * x + c1 * x + c2)


def jh_fit(lam, rgb_target, illum=None, starts=None, iters=200):
    """拟合 Jakob-Hanika 的三个系数，返回 (c, 重建光谱, 残差范数)。

    目标是让重建光谱在白点光源下投影回线性 sRGB 时等于 rgb_target。多项式用
    x = (λ-580)/100 归一化，否则 c0 与 c2 的量级差三个数量级，法方程病态。
    三个参数、三个残差，雅可比解析可写；用 Levenberg-Marquardt 加阻尼迭代，
    饱和色需要几个不同的起点，否则容易停在常数光谱的局部极小。
    """
    lam = np.asarray(lam, dtype=float)
    x = (lam - 580.0) / 100.0
    dlam = np.gradient(lam)
    basis = cie_xyz_basis(lam) * dlam
    W = np.ones_like(lam) if illum is None else np.asarray(illum, dtype=float)
    y_white = float((cie_y(lam) * W * dlam).sum())

    def rgb_of(c):
        r = jh_sigmoid(c[0] * x * x + c[1] * x + c[2])
        xyz = basis @ (W * r) / y_white
        return M_XYZ2RGB_PUBLISHED @ xyz

    def jac(c):
        p = c[0] * x * x + c[1] * x + c[2]
        ds = 1.0 / (2.0 * (1.0 + p * p) ** 1.5)
        P = M_XYZ2RGB_PUBLISHED @ (basis * (W * ds)) / y_white
        return np.stack([P @ (x * x), P @ x, P.sum(axis=1)], axis=1)

    target = np.asarray(rgb_target, dtype=float)
    if starts is None:
        starts = [np.zeros(3), np.array([0.0, 0.0, 4.0]), np.array([2.0, 2.0, -1.0]),
                  np.array([-2.0, 2.0, 0.0]), np.array([0.0, 4.0, -2.0])]

    best = (np.inf, np.zeros(3))
    for c in starts:
        c = np.asarray(c, dtype=float).copy()
        res = rgb_of(c) - target
        cost = float(res @ res)
        damp = 1e-4
        for _ in range(iters):
            J = jac(c)
            A = J.T @ J
            try:
                step = np.linalg.solve(A + damp * np.diag(np.diag(A) + 1e-12), -J.T @ res)
            except np.linalg.LinAlgError:
                break
            cn = c + step
            rn = rgb_of(cn) - target
            ccost = float(rn @ rn)
            if ccost < cost:
                c, res, cost = cn, rn, ccost
                damp = max(damp / 3.0, 1e-9)
                if np.linalg.norm(step) < 1e-13:
                    break
            else:
                damp *= 6.0
                if damp > 1e7:
                    break
        if cost < best[0]:
            best = (cost, c.copy())
    c = best[1]
    return c, jh_spectrum(lam, *c), float(np.sqrt(best[0]))


# ---------------------------------------------------------------- 小的数值工具

def reflectance_rgb(mat, illum=None):
    """反射率在白点光源下的线性 sRGB。

    纹理里存的 RGB 是"这块材质在白光下看起来的三个数"，所以积分要乘上白点
    光源的 SPD，再除以白点光源的 Y。少了这一步，等于把材质当成了等能光源 E
    下的光谱，颜色会偏。
    """
    lam = grid()
    W = d65_like(lam) if illum is None else np.asarray(illum, dtype=float)
    d = np.gradient(lam)
    xyz = cie_xyz_basis(lam) @ (np.asarray(mat, dtype=float) * W * d)
    yw = float((cie_y(lam) * W * d).sum())
    return M_XYZ2RGB_PUBLISHED @ (xyz / yw)


def wl_to_srgb(lam_nm, gamma=True):
    """单色光转 sRGB，用于给图上色。负分量裁掉，最大分量归一。"""
    lam = np.atleast_1d(np.asarray(lam_nm, dtype=float))
    xyz = np.stack([cie_x(lam), cie_y(lam), cie_z(lam)])
    rgb = M_XYZ2RGB_PUBLISHED @ xyz
    rgb = np.clip(rgb, 0.0, None)
    m = rgb.max(axis=0)
    rgb = rgb / np.where(m > 0, m, 1.0)
    # 紫色端亮度低，稍微提亮，避免图上出现看不见的暗线
    if gamma:
        rgb = np.power(rgb, 0.8)
    return rgb.T


def xyz_to_srgb01(xyz, scale=None):
    """XYZ → 显示用 sRGB（已编码），可选按某个值归一化。"""
    rgb = M_XYZ2RGB_PUBLISHED @ np.asarray(xyz, dtype=float)
    if scale is not None:
        rgb = rgb / scale
    return srgb_encode(np.clip(rgb, 0.0, None))


def fwhm_band(lam, center, fwhm):
    return gaussian_line(lam, center, fwhm)


def mat2str(m, fmt="%.4f"):
    return "\n".join("  ".join(fmt % v for v in row) for row in np.asarray(m))


if __name__ == "__main__":
    print("RGB->XYZ 推导值")
    print(M_RGB2XYZ)
    print("XYZ->RGB 推导值")
    print(M_XYZ2RGB)
    for g in SELLMEIER:
        nd, vd = abbe(g)
        print(f"{g}: nd={nd:.5f} Vd={vd:.2f}")
