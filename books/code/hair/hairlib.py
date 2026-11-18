#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""毛发几何光学的公共工具。

约定：纤维横截面是半径 1 的圆，纤维轴沿 z，入射光线沿 +x 传播，
入射点位于圆的左侧，偏移 h∈[-1,1]（相对半径，向上为正），
入射点外法线为 n，入射角 θ_i = asin|h|。
所有角度用弧度；φ 是出射方向相对入射方向的角度。

圆截面对称带来的一个后果：光在纤维内部每一段弦与表面的夹角都是同一个 θ_t，
每经过一次内反射方向转过的角度也是同一个值，所以每条路径的 Fresnel 系数
只跟 h 有关、跟它是第几阶无关，各阶能量构成几何级数。

对外接口：
    trace(h, p, eta)            第 p 阶路径的几何（φ、内部长度、Fresnel 权重）
    phi_of_h(p, hs, eta)        路径 p 的 φ(h) 曲线
    order_energy(p, h, fbar, sigma_a, eta)   第 p 阶的能量
    azimuth_density(...)        方位角密度 M_p(φ)（已归一化）
    total_azimuth(...)          含全部阶数的方位角密度
    n_p(...) / pdf_n(...) / sample_theta(...)   纵向分布及其采样
    cdf_phi / sample_phi / pdf_phi              方位角采样
"""
import sys
import pathlib

import numpy as np

_here = pathlib.Path(__file__).resolve()
sys.path.insert(0, str(_here.parents[2] / "common"))

EPS = 1e-9
ETA = 1.55            # 角质层折射率（人发约 1.55）


# ---------------------------------------------------------------- Fresnel

def fresnel(cos_i, eta):
    """非偏振反射率。eta 是透射侧相对入射侧的折射率。"""
    cos_i = np.clip(np.asarray(cos_i, dtype=float), 0.0, 1.0)
    sin2_t = (1.0 - cos_i ** 2) / eta ** 2
    tir = sin2_t >= 1.0
    cos_t = np.sqrt(np.clip(1.0 - sin2_t, 0.0, 1.0))
    rs = (cos_i - eta * cos_t) / np.maximum(cos_i + eta * cos_t, EPS)
    rp = (eta * cos_i - cos_t) / np.maximum(eta * cos_i + cos_t, EPS)
    val = 0.5 * (rs ** 2 + rp ** 2)
    return np.where(tir, 1.0, val)


def _unit(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), EPS)


# ---------------------------------------------------------------- 路径追踪

def trace(h, p, eta=ETA):
    """追踪第 p 阶路径（p=0 为 R，p=1 为 TT，p=2 为 TRT，p≥3 为高阶）。

    返回 (phi, L, w, ok)：
        phi  出射方向相对入射方向的角度
        L    光在纤维内部走过的长度（以半径为 1）
        w    几何光学权重（各界面 Fresnel 的乘积），不含吸收
        ok   是否成功出射
    """
    h = float(np.clip(h, -1.0 + 1e-9, 1.0 - 1e-9))
    P = np.array([-np.sqrt(1.0 - h * h), h])
    n_in = _unit(P)
    d = np.array([1.0, 0.0])
    cos_i = -float(np.dot(d, n_in))
    sin_i = np.sqrt(max(0.0, 1.0 - cos_i ** 2))

    if p == 0:
        r = d - 2.0 * np.dot(d, n_in) * n_in
        return np.arctan2(r[1], r[0]), 0.0, float(fresnel(cos_i, eta)), True

    sin_t = sin_i / eta
    if sin_t >= 1.0:
        return 0.0, 0.0, 0.0, False
    cos_t = np.sqrt(1.0 - sin_t ** 2)
    t = _unit(d / eta + (cos_t - cos_i / eta) * (-n_in))

    w = 1.0 - float(fresnel(cos_i, eta))
    L = 0.0
    cur, pos = t, P.copy()
    ft = float(fresnel(cos_t, 1.0 / eta))

    for _ in range(p - 1):
        b = float(np.dot(pos, cur))
        s = -b + np.sqrt(max(b * b - (float(np.dot(pos, pos)) - 1.0), 0.0))
        pos = pos + s * cur
        L += s
        nn = _unit(pos)
        cur = cur - 2.0 * float(np.dot(cur, nn)) * nn
        w *= ft

    b = float(np.dot(pos, cur))
    s = -b + np.sqrt(max(b * b - (float(np.dot(pos, pos)) - 1.0), 0.0))
    pos = pos + s * cur
    L += s
    nn = _unit(pos)
    ct = float(np.dot(cur, nn))
    st = np.sqrt(max(0.0, 1.0 - ct * ct))
    sin_out = eta * st
    if sin_out >= 1.0:
        return 0.0, L, 0.0, False
    cos_out = np.sqrt(1.0 - sin_out ** 2)
    w *= 1.0 - ft
    out = _unit(eta * cur + (cos_out - eta * ct) * nn)
    return np.arctan2(out[1], out[0]), L, w, True


def path_points(h, p, eta=ETA, back=0.55):
    """返回第 p 阶路径的折线点，用于画示意剖面。

    起点在纤维左侧外侧 back 处，终点沿出射方向延伸到圆外。
    """
    h = float(np.clip(h, -1.0 + 1e-4, 1.0 - 1e-4))
    P = np.array([-np.sqrt(1.0 - h * h), h])
    n_in = _unit(P)
    d = np.array([1.0, 0.0])
    cos_i = -float(np.dot(d, n_in))
    start = P - back * d
    if p == 0:
        r = d - 2.0 * np.dot(d, n_in) * n_in
        return np.array([start, P, P + back * r])
    sin_t = np.sqrt(max(0.0, 1 - cos_i ** 2)) / eta
    cos_t = np.sqrt(1 - sin_t ** 2)
    cur = _unit(d / eta + (cos_t - cos_i / eta) * (-n_in))
    pts, pos = [start, P], P.copy()
    for _ in range(p):
        b = float(np.dot(pos, cur))
        s = -b + np.sqrt(max(b * b - (float(np.dot(pos, pos)) - 1.0), 0.0))
        pos = pos + s * cur
        pts.append(pos.copy())
        if len(pts) == p + 2:
            break
        nn = _unit(pos)
        cur = cur - 2.0 * float(np.dot(cur, nn)) * nn
    nn = _unit(pos)
    ct = float(np.dot(cur, nn))
    st = np.sqrt(max(0.0, 1 - ct * ct))
    so = eta * st
    if so < 1.0:
        co = np.sqrt(1 - so ** 2)
        out = _unit(eta * cur + (co - eta * ct) * nn)
    else:
        out = cur
    pts.append(pos + back * out)
    return np.array(pts)


def path_length(p, h, eta=ETA):
    """解析形式：第 p 阶路径的内部长度 = 2p·cos(θ_t)。"""
    h = np.clip(np.asarray(h, dtype=float), -1.0, 1.0)
    return 2.0 * p * np.sqrt(np.clip(1.0 - (h / eta) ** 2, 0.0, 1.0))


def phi_of_h(p, hs, eta=ETA):
    hs = np.atleast_1d(np.asarray(hs, dtype=float))
    phi = np.empty_like(hs)
    L = np.empty_like(hs)
    w = np.empty_like(hs)
    for i, h in enumerate(hs):
        a, ll, ww, ok = trace(h, p, eta)
        phi[i] = a
        L[i] = ll
        w[i] = ww if ok else 0.0
    return phi, L, w


def specular_deviation(phi, p):
    """把出射角换成相对该阶理想方向的偏差：偶数阶相对镜面方向，奇数阶相对透射方向。"""
    ref = np.pi if p % 2 == 0 else 0.0
    return (np.asarray(phi) - ref + np.pi) % (2.0 * np.pi) - np.pi


def internal_reflectance(h, eta=ETA):
    """单次内反射的 Fresnel 反射率（与阶数无关，只跟 h 有关）。"""
    h = np.clip(np.asarray(h, dtype=float), -1.0, 1.0)
    return fresnel(np.sqrt(np.clip(1.0 - (h / eta) ** 2, 0.0, 1.0)), 1.0 / eta)


# ---------------------------------------------------------------- 能量

def order_energy(p, h, fbar=None, sigma_a=0.0, eta=ETA):
    """第 p 阶路径的能量权重。

    fbar 给定时用这个平均内反射率代替几何值（用于粗糙纤维的经验模型）。
    """
    h = np.asarray(h, dtype=float)
    ci = np.sqrt(np.clip(1.0 - h * h, 0.0, 1.0))
    fi = fresnel(ci, eta)
    if p == 0:
        w = fi
        L = 0.0
    else:
        ft = internal_reflectance(h, eta) if fbar is None else fbar
        w = (1.0 - fi) * ft ** (p - 1) * (1.0 - ft)
        L = path_length(p, h, eta)
    return w * np.exp(-sigma_a * L)


# ---------------------------------------------------------------- 方位角分布

def azimuth_density(p, sigma_a=0.0, eta=ETA, fbar=None, n=6000, bins=181):
    """路径 p 的方位角密度 M_p(φ)，由 h→φ 的映射换算：

        M_p(φ) = ∫ δ(φ - φ_p(h)) A_p(h) dh,

    A_p 是第 p 阶的能量。返回值 (centers, density)，归一化到 ∫M_p dφ = 1
    （φ 覆盖 [-π, π]）。
    """
    hs = np.linspace(-1 + 1e-4, 1 - 1e-4, n)
    phi, L, w = phi_of_h(p, hs, eta)
    dev = specular_deviation(phi, p)
    if fbar is None:
        w = w * np.exp(-sigma_a * L)
    else:
        w = order_energy(p, hs, fbar=fbar, sigma_a=sigma_a, eta=eta) * (w > 0)
    e = np.linspace(-np.pi, np.pi, bins + 1)
    idx = np.clip(np.digitize(dev, e) - 1, 0, len(e) - 2)
    dh = hs[1] - hs[0]
    dens = np.zeros(len(e) - 1)
    np.add.at(dens, idx, w * dh)
    centers = 0.5 * (e[1:] + e[:-1])
    dphi = e[1] - e[0]
    tot = dens.sum() * dphi
    return centers, (dens / tot if tot > 0 else dens)


def mean_energy(p, fbar=None, sigma_a=0.0, eta=ETA, n=6000):
    """第 p 阶携带的能量份额（对入射能量归一，等于 ∫A_p(h) dh）。"""
    hs = np.linspace(-1 + 1e-4, 1 - 1e-4, n)
    _, _, w = phi_of_h(p, hs, eta)
    if fbar is None:
        _, L, _ = phi_of_h(p, hs, eta)
        a = w * np.exp(-sigma_a * L)
    else:
        a = order_energy(p, hs, fbar=fbar, sigma_a=sigma_a, eta=eta) * (w > 0)
    return float(np.trapezoid(a, hs)) / 2.0


def total_azimuth(kmax=6, fbar=None, sigma_a=0.0, eta=ETA, bins=181, n=6000):
    """含 p=0..kmax 全部阶数的方位角密度（按各阶能量加权）。

    返回 (centers, density, energy)，density 的积分等于 energy，
    energy 是这些阶数加起来占入射能量的比例。
    """
    c, d = azimuth_density(0, sigma_a, eta, fbar, n=n, bins=bins)
    e = mean_energy(0, fbar, sigma_a, eta)
    d = d * e
    for p in range(1, kmax + 1):
        _, dp = azimuth_density(p, sigma_a, eta, fbar, n=n, bins=bins)
        ep = mean_energy(p, fbar, sigma_a, eta)
        d = d + dp * ep
        e += ep
    return c, d, e


def cdf_phi(p, sigma_a=0.0, eta=ETA, fbar=None, bins=181):
    """M_p 的累积分布，供逆变换采样用。返回 (centers, cdf)。"""
    c, d = azimuth_density(p, sigma_a, eta, fbar, bins=bins)
    dc = c[1] - c[0]
    cdf = np.concatenate([[0.0], np.cumsum(d) * dc])
    cdf /= cdf[-1]
    edges = np.concatenate([c - 0.5 * dc, [c[-1] + 0.5 * dc]])
    return edges, cdf


def sample_phi(p, u, sigma_a=0.0, eta=ETA, fbar=None, bins=361):
    """按 M_p 逆变换采样 φ。u 为 [0,1) 的数组。"""
    edges, cdf = cdf_phi(p, sigma_a, eta, fbar, bins=bins)
    return np.interp(u, cdf, edges)


def pdf_phi(p, phi, sigma_a=0.0, eta=ETA, fbar=None, bins=361):
    c, d = azimuth_density(p, sigma_a, eta, fbar, bins=bins)
    return np.interp(np.asarray(phi, dtype=float), c, d, left=0.0, right=0.0)


# ---------------------------------------------------------------- 纵向分布

def gauss(x, s):
    s = max(float(s), 1e-6)
    return np.exp(-0.5 * (x / s) ** 2) / (np.sqrt(2 * np.pi) * s)


def _tilt_nodes(spread, n_alpha=33):
    alphas = np.linspace(-3.2 * spread, 3.2 * spread, n_alpha)
    pa = gauss(alphas, spread)
    return alphas, pa / pa.sum()


def n_p(theta_i, theta_o, p, beta=0.2, spread=0.06):
    """纵向分布 N_p(θ_i, θ_o)。

    角质层倾斜角 α 取均值 0、标准差 spread 的分布；在倾斜面上，
        R   : θ_o + θ_i - 2α = 0
        TT  : θ_o - θ_i      = 0
        TRT : θ_o + θ_i      = 0
    再与粗糙度 β 的塔尖分布（高斯）卷积。返回对 θ_o 积分为 1 的密度。
    """
    alphas, pa = _tilt_nodes(spread)
    if p == 1:
        beta = 0.5 * beta      # 两次折射把微面的角偏差压缩一半
    ti = np.asarray(theta_i, dtype=float)
    to = np.asarray(theta_o, dtype=float)
    if p == 0:
        dev = to[..., None] + ti[..., None] - 2.0 * alphas
    elif p == 1:
        dev = to[..., None] - ti[..., None] + 0.0 * alphas
    else:
        dev = to[..., None] + ti[..., None] + 0.0 * alphas
    return (gauss(dev, beta) * pa).sum(axis=-1)


def sample_theta(theta_i, p, beta=0.3, spread=0.35, u1=0.5, u2=0.5):
    """按 N_p 采样 θ_o：先抽倾斜角分量，再抽高斯偏差。"""
    alphas, pa = _tilt_nodes(spread)
    cdf = np.cumsum(pa)
    cdf /= cdf[-1]
    k = np.searchsorted(cdf, np.clip(np.asarray(u1, dtype=float), 0, 0.999999))
    k = np.clip(k, 0, len(alphas) - 1)
    a = alphas[k]
    z = np.sqrt(2.0) * _erfinv(2.0 * np.clip(u2, 1e-6, 1 - 1e-6) - 1.0)
    if p == 0:
        return -theta_i + 2.0 * a + beta * z
    if p == 1:
        return theta_i + beta * z
    return -theta_i + beta * z


def _erfinv(y):
    """Winitzki 近似的 erfinv，精度约 1e-4，够画图用。"""
    y = np.asarray(y, dtype=float)
    a = 0.147
    ln = np.log(np.clip(1 - y * y, 1e-12, None))
    t = 2.0 / (np.pi * a) + ln / 2.0
    return np.sign(y) * np.sqrt(np.sqrt(t * t - ln / a) - t)


# ---------------------------------------------------------------- 吸收

SIGMA_EU = np.array([0.419, 0.697, 1.37])     # 真黑色素，RGB 三个通道
SIGMA_PHEO = np.array([0.187, 0.400, 1.050])  # 褐黑色素


def sigma_a(melanin=0.5, redness=0.0, eumel=SIGMA_EU, pheomel=SIGMA_PHEO):
    """黑色素吸收系数（RGB），取自 PBRT 里的系数集。"""
    return (eumel * (1.0 - redness) + pheomel * redness) * melanin


def transmittance(L, sa):
    """Beer–Lambert：路径长度 L 上的透射率，sa 可以是三元组。"""
    return np.exp(-np.asarray(sa)[..., None] * np.asarray(L))
