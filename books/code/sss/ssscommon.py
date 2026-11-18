#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本册共用的物理函数。

所有函数都是"教科书公式的直接实现"，不包含任何拟合系数。各章脚本只调用这里，
避免同一个偶极子公式在二十个文件里各写一遍、各错一遍。

记号：长度单位一律用毫米（mm），吸收与散射系数单位 mm^-1。
方向约定：法线 +z 指向介质外部，介质占 z<0，深度 d = -z 为正。
"""
import numpy as np

from bsdf import fresnel_dielectric

EPS = 1e-12

# ---------------------------------------------------------------- 基本量


def sigma_tr(sigma_a, sigma_s, g):
    """约化（输运）消光系数 σ_tr = σa + (1-g)σs。"""
    return sigma_a + (1.0 - g) * sigma_s


def sigma_s_prime(sigma_s, g):
    return (1.0 - g) * sigma_s


def albedo_prime(sigma_a, sigma_s, g):
    """输运反照率 α' = σs' / (σa + σs')。"""
    return sigma_s_prime(sigma_s, g) / (sigma_a + sigma_s_prime(sigma_s, g))


def diffusion_coeff(sigma_a, sigma_s, g):
    """扩散系数 D = 1 / (3 σ_tr)。"""
    return 1.0 / (3.0 * sigma_tr(sigma_a, sigma_s, g))


def beer_lambert(sigma_t, d):
    return np.exp(-sigma_t * np.asarray(d, dtype=float))


def mean_free_path(sigma_t):
    return 1.0 / sigma_t


def transport_mfp(sigma_a, sigma_s, g):
    return 1.0 / sigma_tr(sigma_a, sigma_s, g)


def penetration_depth(sigma_a, sigma_s, g):
    """扩散理论给出的特征衰减长度 δ = sqrt(D/σa) = 1/sqrt(3σa σ_tr)。"""
    return np.sqrt(diffusion_coeff(sigma_a, sigma_s, g) / max(sigma_a, EPS))


def mu_eff(sigma_a, sigma_s, g):
    """有效衰减系数 μ_eff = sqrt(σa / D) = sqrt(3 σa σ_tr)。"""
    return np.sqrt(max(sigma_a, EPS)
                   / diffusion_coeff(sigma_a, sigma_s, g))


# ---------------------------------------------------------------- 相函数


def hg_phase(cos_theta, g):
    """Henyey–Greenstein 相函数，归一化到 ∫p dω = 1。"""
    c = np.asarray(cos_theta, dtype=float)
    den = np.maximum((1.0 + g * g - 2.0 * g * c) ** 1.5, EPS)
    return (1.0 - g * g) / (4.0 * np.pi * den)


def hg_sample_cos(g, u):
    """由均匀随机数 u 采样 HG 的 cosθ。"""
    if abs(g) < 1e-6:
        return 2.0 * u - 1.0
    s = (1.0 - g * g) / (1.0 - g + 2.0 * g * u)
    return np.clip((1.0 + g * g - s * s) / (2.0 * g), -1.0, 1.0)


def hg_moments(g, n=6):
    """HG 的 Legendre 矩：第 l 阶等于 g^l。"""
    return np.array([g ** l for l in range(n)])


def rayleigh_phase(cos_theta):
    return 3.0 / (16.0 * np.pi) * (1.0 + np.asarray(cos_theta, dtype=float) ** 2)


def phase_legendre(cos_theta, moments, n_theta=None):
    """按 Legendre 矩展开的相函数 p(cosθ) = (1/4π) Σ (2l+1) a_l P_l(cosθ)。"""
    from numpy.polynomial import legendre as L
    c = np.asarray(cos_theta, dtype=float)
    out = np.zeros_like(c)
    for l, a in enumerate(moments):
        out += (2 * l + 1) * a * L.legval(c, [0] * l + [1])
    return out / (4.0 * np.pi)


# ---------------------------------------------------------------- 边界


def fdr_diffuse(eta, n=4000):
    """漫射光从介质内部射向界面时的半球平均反射率 F_dr。

    介质折射率为 eta，外部为 1。超过临界角的部分全反射，不计入透射。
    """
    th = (np.arange(n) + 0.5) * (np.pi / 2) / n
    F = fresnel_dielectric(np.cos(th), 1.0 / eta)
    return float(np.sum(F * 2.0 * np.cos(th) * np.sin(th)) * (np.pi / 2) / n)


def boundary_A(eta):
    """外推边界参数 A = (1 + F_dr) / (1 - F_dr)。"""
    f = fdr_diffuse(eta)
    return (1.0 + f) / (1.0 - f)


def zb_extrapolation(sigma_a, sigma_s, g, eta):
    """外推边界距离 z_b = 2 A D。"""
    return 2.0 * boundary_A(eta) * diffusion_coeff(sigma_a, sigma_s, g)


# ---------------------------------------------------------------- 扩散解的核


def green_infinite(r, sigma_a, sigma_s, g, power=1.0):
    """无限介质中点源的 fluence：φ = P e^{-μ_eff r} / (4π D r)。"""
    D = diffusion_coeff(sigma_a, sigma_s, g)
    r = np.maximum(np.asarray(r, dtype=float), EPS)
    return power * np.exp(-mu_eff(sigma_a, sigma_s, g) * r) / (4.0 * np.pi * D * r)


def flux_surface(ma, ms, g, z, r):
    """深度 z 处的点源在表面上半径 r 处产生的出射度（Fick 定律，法向分量）。"""
    m = mu_eff(ma, ms, g)
    d = np.sqrt(r * r + z * z)
    return np.abs(z) * (m * d + 1.0) * np.exp(-m * d) / (4.0 * np.pi * d ** 3)


def rd_dipole(r, sigma_a, sigma_s, g, eta=1.3, alpha_prime=None):
    """偶极子的径向剖面 R_d(r)，单位 mm^-2（Farrell 1992 / Jensen 2001）。

    返回"每单位入射功率、每单位面积"的出射，∫ R_d 2πr dr = 总反射率。
    指数用有效衰减系数 μ_eff = sqrt(3σa σ_tr)。
    """
    ap = albedo_prime(sigma_a, sigma_s, g) if alpha_prime is None else alpha_prime
    st = sigma_tr(sigma_a, sigma_s, g)
    m = mu_eff(sigma_a, sigma_s, g)
    zb = zb_extrapolation(sigma_a, sigma_s, g, eta)
    zr = 1.0 / st
    zv = zr + 2.0 * zb
    r = np.asarray(r, dtype=float)
    dr = np.sqrt(r * r + zr * zr)
    dv = np.sqrt(r * r + zv * zv)
    return ap / (4.0 * np.pi) * (
        zr * (m * dr + 1.0) * np.exp(-m * dr) / dr ** 3
        + zv * (m * dv + 1.0) * np.exp(-m * dv) / dv ** 3)


def rd_multipole(r, L, sigma_a, sigma_s, g, eta=1.3, n_images=30):
    """厚度 L 的平板：多极子的反射与透射剖面（Donner & Jensen 2005，式 11-13）。

    返回 (R, T)，单位 mm^-2。n_images = 0 时 R 退化为半无限介质的偶极子，
    T 恒为零——这正是偶极子看不见薄片的原因。
    """
    ap = albedo_prime(sigma_a, sigma_s, g)
    st = sigma_tr(sigma_a, sigma_s, g)
    m = mu_eff(sigma_a, sigma_s, g)
    zb = zb_extrapolation(sigma_a, sigma_s, g, eta)
    ell = 1.0 / st
    P = 2.0 * (L + 2.0 * zb)
    r = np.asarray(r, dtype=float)
    R = np.zeros_like(r)
    T = np.zeros_like(r)

    for i in range(-n_images, n_images + 1):
        for z, sgn in ((i * P + ell, 1.0), (i * P - ell - 2.0 * zb, -1.0)):
            d = np.sqrt(r * r + z * z)
            R += sgn * z * (m * d + 1.0) * np.exp(-m * d) / d ** 3
            z2 = L - z
            d2 = np.sqrt(r * r + z2 * z2)
            T += sgn * z2 * (m * d2 + 1.0) * np.exp(-m * d2) / d2 ** 3
    return ap * R / (4.0 * np.pi), ap * T / (4.0 * np.pi)


def ss_radiance(cos_o, sigma_a, sigma_s, g):
    """半无限介质、平面波垂直入射时，单次散射的出射辐亮度（单位入射辐照度）。

    L_ss(θ_o) = σs p(-cosθ_o) / (σt (1 + cosθ_o))，与出射点位置无关。
    散射角的余弦是 -cosθ_o：入射朝内、出射朝外，两者夹角是 π-θ_o。
    """
    st = sigma_a + sigma_s
    c = np.clip(np.asarray(cos_o, dtype=float), 0.0, 1.0)
    return sigma_s * hg_phase(-c, g) / (st * (1.0 + c))


def ss_reflectance(sigma_a, sigma_s, g, n=400):
    """单次散射的总漫反射率：对半球积分 L_ss cosθ dω。"""
    th = (np.arange(n) + 0.5) * (np.pi / 2) / n
    c = np.cos(th)
    L = ss_radiance(c, sigma_a, sigma_s, g)
    return float(np.sum(L * c * 2.0 * np.pi * np.sin(th)) * (np.pi / 2) / n)


def rd_total(rd, r_max=None, n=20000):
    """对径向剖面做 2πr 积分，得到总漫反射率。"""
    if r_max is None:
        r_max = 40.0
    r = (np.arange(n) + 0.5) * r_max / n
    dr = r_max / n
    return float(np.sum(rd(r) * 2.0 * np.pi * r) * dr)


# ---------------------------------------------------------------- 蒙特卡洛


def _scatter(dirs, g, rng):
    """对一批方向做 HG 散射（全向量化）。"""
    n = dirs.shape[0]
    ct = hg_sample_cos(g, rng.random(n))
    st = np.sqrt(np.maximum(0.0, 1.0 - ct * ct))
    phi = 2.0 * np.pi * rng.random(n)
    a = np.where(np.abs(dirs[:, 2:3]) < 0.9,
                 np.array([[0.0, 0.0, 1.0]]), np.array([[1.0, 0.0, 0.0]]))
    t = np.cross(a, dirs)
    t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), EPS)
    b = np.cross(dirs, t)
    out = (st[:, None] * (np.cos(phi)[:, None] * t + np.sin(phi)[:, None] * b)
           + ct[:, None] * dirs)
    return out / np.maximum(np.linalg.norm(out, axis=1, keepdims=True), EPS)


def mc_slab(sigma_a, sigma_s, g, L=np.inf, eta=1.0, n_photons=100000,
            rng=None, max_events=3000, fresnel=False, with_angle=False,
            incident=None, full=False):
    """平板内的光子随机游走（标量、等权）。

    返回 (r, kind, events)：出射半径、0=从入射面出射 1=从背面出射、散射次数。
    入射为沿 +z 的准直光束，从深度 0 处射入。吸收用相似法处理：每次碰撞以
    概率 α = σs/σt 继续散射，否则被吸收（kind 记为 -2）。
    """
    rng = np.random.default_rng(0) if rng is None else rng
    st = sigma_a + sigma_s
    alpha = sigma_s / st

    pos = np.zeros((n_photons, 3))
    d0 = np.array([0.0, 0.0, 1.0]) if incident is None else np.asarray(incident, float)
    d0 = d0 / np.linalg.norm(d0)
    dirs = np.tile(d0, (n_photons, 1))
    alive = np.ones(n_photons, dtype=bool)
    events = np.zeros(n_photons, dtype=int)
    r_exit = np.full(n_photons, np.nan)
    cos_out = np.full(n_photons, np.nan)
    x_exit = np.full(n_photons, np.nan)
    y_exit = np.full(n_photons, np.nan)
    kind = np.full(n_photons, -1, dtype=int)

    for _ in range(max_events):
        idx = np.flatnonzero(alive)
        if idx.size == 0:
            break
        m = idx.size
        s = -np.log(rng.random(m)) / st
        p = pos[idx] + dirs[idx] * s[:, None]
        events[idx] += 1
        keep = np.ones(m, dtype=bool)

        top = np.flatnonzero(p[:, 2] < 0.0)
        if top.size:
            esc = top
            if fresnel:
                cosv = np.abs(dirs[idx[top], 2])
                F = fresnel_dielectric(cosv, 1.0 / eta)
                ref = rng.random(top.size) < F
                tl = top[ref]
                p[tl, 2] = -p[tl, 2]
                dirs[idx[tl], 2] = -dirs[idx[tl], 2]
                esc = top[~ref]
            r_exit[idx[esc]] = np.hypot(p[esc, 0], p[esc, 1])
            cos_out[idx[esc]] = np.abs(dirs[idx[esc], 2])
            x_exit[idx[esc]] = p[esc, 0]
            y_exit[idx[esc]] = p[esc, 1]
            kind[idx[esc]] = 0
            keep[esc] = False

        if np.isfinite(L):
            bot = np.flatnonzero(p[:, 2] > L)
            if bot.size:
                r_exit[idx[bot]] = np.hypot(p[bot, 0], p[bot, 1])
                kind[idx[bot]] = 1
                keep[bot] = False

        loc = np.flatnonzero(keep)
        if loc.size == 0:
            alive[idx] = False
            continue
        gidx = idx[loc]
        # 吸收：以概率 1-α 死亡
        if alpha < 1.0:
            dead = rng.random(loc.size) >= alpha
            if np.any(dead):
                kind[gidx[dead]] = -2
                alive[gidx[dead]] = False
                loc = loc[~dead]
                gidx = gidx[~dead]
        alive[idx[~keep]] = False
        if gidx.size == 0:
            continue
        pos[gidx] = p[loc]
        dirs[gidx] = _scatter(dirs[gidx], g, rng)

    if full:
        return dict(r=r_exit, kind=kind, events=events, cos=cos_out,
                        x=x_exit, y=y_exit)
    if with_angle:
        return r_exit, kind, events, cos_out
    return r_exit, kind, events


def mc_radial_profile(r_exit, n_bins=120, r_max=6.0):
    """把出射半径做成每单位面积的径向概率密度（∫2πr R dr = 1）。"""
    r_exit = r_exit[np.isfinite(r_exit)]
    n = r_exit.size
    edges = np.linspace(0.0, r_max, n_bins + 1)
    cnt, _ = np.histogram(r_exit, bins=edges)
    r = 0.5 * (edges[:-1] + edges[1:])
    area = np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
    return r, cnt / (n * area), n
