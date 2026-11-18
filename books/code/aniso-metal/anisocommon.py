#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本册专用的公共函数：金属光学常数、各向异性 GGX、能量表。

放在 books/code/aniso-metal/ 下，各章脚本用
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from anisocommon import *
引入。

注意：books/common/bsdf.py 里的 d_ggx_aniso 少了一个 1/cos^4 因子，
归一化不成立（第 3 章图 3-3 会把这件事画出来），本文件给出正确版本。
"""
import numpy as np

EPS = 1e-7

# ------------------------------------------------------------------ 金属数据
# 波长单位微米，顺序 0.65 / 0.55 / 0.45（红、绿、蓝）。
# 数据取自 Johnson & Christy, Phys. Rev. B 6, 4370 (1972) 的可见光部分，
# 经折射率手册（Palik, Handbook of Optical Constants of Solids, 1985）转录。
WL = np.array([0.65, 0.55, 0.45])
WL_NAME = ["0.65 μm", "0.55 μm", "0.45 μm"]

METALS = {
    "金":  [(0.271, 3.196), (0.457, 2.504), (1.713, 1.921)],
    "铜":  [(0.271, 3.609), (0.978, 2.449), (1.194, 2.340)],
    "银":  [(0.143, 3.983), (0.145, 3.129), (0.144, 2.524)],
    "铝":  [(1.437, 7.610), (0.963, 6.333), (0.533, 4.860)],
    "铁":  [(2.911, 3.089), (2.608, 3.347), (2.037, 3.132)],
}

COLORS = ["#c9973a", "#b5651d", "#8a93a0", "#5b6472", "#4f7a4a"]


def f0_from_nk(n, k):
    """垂直入射的导体反射率，式 (2.3)。"""
    n = np.asarray(n, float)
    k = np.asarray(k, float)
    return ((n - 1.0) ** 2 + k ** 2) / ((n + 1.0) ** 2 + k ** 2)


def skin_depth_nm(lam_um, k):
    """振幅衰减到 1/e 的深度，单位纳米。"""
    return lam_um * 1000.0 / (4.0 * np.pi * np.asarray(k, float))


# ------------------------------------------------------------------ 方向
def sph(theta, phi):
    st = np.sin(theta)
    return np.stack([st * np.cos(phi), st * np.sin(phi), np.cos(theta)], axis=-1)


def normalize(v):
    v = np.asarray(v, float)
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), EPS)


def half(wi, wo):
    return normalize(np.asarray(wi, float) + np.asarray(wo, float))


def cos_theta(w):
    return np.clip(np.asarray(w)[..., 2], -1.0, 1.0)


# ------------------------------------------------------------------ Fresnel
def fresnel_conductor(cos_i, n, k):
    """非偏振导体反射率，式 (2.1)(2.2) 的闭式解。"""
    cos_i = np.clip(np.asarray(cos_i, float), 1e-4, 1.0)
    n = np.asarray(n, float)
    k = np.asarray(k, float)
    s2 = 1.0 - cos_i ** 2
    a2 = n ** 2 - k ** 2 - s2
    b2 = 2.0 * n * k
    t = np.sqrt(a2 ** 2 + b2 ** 2)
    a = np.sqrt(np.maximum(0.5 * (t + a2), 0.0))
    b = np.sqrt(np.maximum(0.5 * (t - a2), 0.0))
    rs = ((cos_i - a) ** 2 + b ** 2) / np.maximum((cos_i + a) ** 2 + b ** 2, EPS)
    num = (n ** 2 - k ** 2 - cos_i * a) ** 2 + (2 * n * k - cos_i * b) ** 2
    den = (n ** 2 - k ** 2 + cos_i * a) ** 2 + (2 * n * k + cos_i * b) ** 2
    rp = num / np.maximum(den, EPS)
    return 0.5 * (rs + rp)


def fresnel_schlick(cos_i, f0):
    c = np.clip(1.0 - np.asarray(cos_i, float), 0.0, 1.0)
    return f0 + (1.0 - f0) * c ** 5


# ------------------------------------------------------------------ 各向异性 GGX
def d_aniso(cos_h, phi_h, ax, ay):
    """正确的各向异性 GGX，D = 1/(pi ax ay cos^4) * 1/(1+tan^2(...))^2。"""
    c2 = np.clip(cos_h, 1e-4, 1.0) ** 2
    t2 = (1.0 - c2) / c2
    cph, sph = np.cos(phi_h), np.sin(phi_h)
    den = 1.0 + t2 * (cph ** 2 / ax ** 2 + sph ** 2 / ay ** 2)
    return 1.0 / (np.pi * ax * ay * c2 ** 2 * np.maximum(den ** 2, EPS))


def d_aniso_nocos4(cos_h, phi_h, ax, ay):
    """少了 cos^-4 的错误版本，仅用于图 3-3 的对比。"""
    c2 = np.clip(cos_h, 1e-4, 1.0) ** 2
    t2 = (1.0 - c2) / c2
    cph, sph = np.cos(phi_h), np.sin(phi_h)
    den = 1.0 + t2 * (cph ** 2 / ax ** 2 + sph ** 2 / ay ** 2)
    return 1.0 / (np.pi * ax * ay * np.maximum(den ** 2, EPS))


def alpha_proj(phi, ax, ay):
    """把两个方向的粗糙度投影到方位角 phi 上。"""
    return np.sqrt(ax ** 2 * np.cos(phi) ** 2 + ay ** 2 * np.sin(phi) ** 2)


def lambda_smith(cos_v, phi_v, ax, ay):
    a = alpha_proj(phi_v, ax, ay)
    c2 = np.clip(cos_v, 1e-5, 1.0) ** 2
    return 0.5 * (-1.0 + np.sqrt(1.0 + a ** 2 * (1.0 - c2) / c2))


def g1(cos_v, phi_v, ax, ay):
    return 1.0 / (1.0 + lambda_smith(cos_v, phi_v, ax, ay))


def g2(ci, pi_, co, po, ax, ay):
    return 1.0 / (1.0 + lambda_smith(ci, pi_, ax, ay) + lambda_smith(co, po, ax, ay))


def brdf_aniso(wi, wo, ax, ay, f0=1.0):
    """单次散射各向异性微表面 BRDF，标量方向。"""
    wi = np.asarray(wi, float)
    wo = np.asarray(wo, float)
    h = normalize(wi + wo)
    ci = np.clip(wi[2], 0.0, 1.0)
    co = np.clip(wo[2], 0.0, 1.0)
    if ci <= 0 or co <= 0:
        return 0.0
    ch = np.clip(h[2], 1e-4, 1.0)
    ph = np.arctan2(h[1], h[0])
    D = float(d_aniso(ch, ph, ax, ay))
    G = float(g2(ci, np.arctan2(wi[1], wi[0]), co, np.arctan2(wo[1], wo[0]), ax, ay))
    F = float(np.asarray(fresnel_schlick(np.clip(np.dot(wi, h), 0, 1), f0)))
    return F * D * G / (4.0 * ci * co)


# ------------------------------------------------------------------ 半球积分
def hemi_grid(nt=120, np_=240):
    """旧版网格（θ 均匀），只在需要与早期结果对比时使用。"""
    th = (np.arange(nt) + 0.5) * (np.pi / 2) / nt
    ph = (np.arange(np_) + 0.5) * 2 * np.pi / np_
    T, P = np.meshgrid(th, ph, indexing="ij")
    dw = np.sin(T) * (np.pi / 2 / nt) * (2 * np.pi / np_)
    return T, P, dw


def directional_albedo(mu_i, phi_i, ax, ay, nt=480, np_=480):
    """单次散射的方向反照率，F 取 1（白炉）。式 (5.2)。

    在 μ_o 上均匀取样：掠射处（μ→0）的被积函数极窄，θ 均匀网格会漏掉它。
    用 dω = dμ dφ，被积函数是 f·μ。
    """
    wi = sph(np.arccos(np.clip(mu_i, 1e-4, 1.0)), phi_i)
    mu = (np.arange(nt) + 0.5) / nt
    ph = (np.arange(np_) + 0.5) * 2 * np.pi / np_
    M, P = np.meshgrid(mu, ph, indexing="ij")
    Wo = sph(np.arccos(M), P)
    Hh = normalize(wi[None, None, :] + Wo)
    ch = np.clip(Hh[..., 2], 1e-4, 1.0)
    phh = np.arctan2(Hh[..., 1], Hh[..., 0])
    D = d_aniso(ch, phh, ax, ay)
    G = 1.0 / (1.0 + lambda_smith(np.clip(wi[2], 1e-5, 1.0), phi_i, ax, ay)
               + lambda_smith(M, P, ax, ay))
    f = D * G / (4.0 * np.clip(wi[2], 1e-5, 1) * M)
    return float(np.sum(f * M) * (1.0 / nt) * (2 * np.pi / np_))


def e_table(ax, ay, mus=None, phis=None):
    mus = np.linspace(0.02, 0.995, 40) if mus is None else mus
    phis = np.array([0.0, np.pi / 4, np.pi / 2]) if phis is None else phis
    return mus, [[directional_albedo(m, p, ax, ay) for m in mus] for p in phis]


def e_avg(mus, e):
    """E_avg = 2 ∫ E(μ) μ dμ，式 (5.5)。"""
    return float(2.0 * np.trapezoid(np.asarray(e) * mus, mus))


def f_ms(mu_i, mu_o, E_i, E_o, Eav):
    """Kulla–Conty 的多次散射项，式 (5.6)。"""
    den = np.pi * max(1.0 - Eav, 1e-4)
    return (1.0 - E_i) * (1.0 - E_o) / den
