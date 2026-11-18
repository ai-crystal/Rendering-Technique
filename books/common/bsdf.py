#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全系列共用的 BSDF 基本函数，只用 NumPy，标量或数组都能传。

约定：方向都是单位向量，法线为 +z；角度用弧度。
"""
import numpy as np

EPS = 1e-7


def normalize(v):
    v = np.asarray(v, dtype=float)
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), EPS)


def cos_theta(w):
    return np.clip(w[..., 2], -1.0, 1.0)


def spherical(theta, phi):
    """由天顶角、方位角构造单位方向。"""
    st, ct = np.sin(theta), np.cos(theta)
    return np.stack([st * np.cos(phi), st * np.sin(phi), ct], axis=-1)


def half_vector(wi, wo):
    h = wi + wo
    n = np.linalg.norm(h, axis=-1, keepdims=True)
    return h / np.maximum(n, EPS)


# ---------------------------------------------------------------- Fresnel

def fresnel_dielectric(cos_i, eta):
    """无吸收电介质界面的非偏振反射率。eta = n2/n1。"""
    cos_i = np.clip(np.asarray(cos_i, dtype=float), 0.0, 1.0)
    sin2_t = (1.0 - cos_i ** 2) / eta ** 2
    tir = sin2_t >= 1.0
    cos_t = np.sqrt(np.clip(1.0 - sin2_t, 0.0, 1.0))
    rs = (cos_i - eta * cos_t) / np.maximum(cos_i + eta * cos_t, EPS)
    rp = (eta * cos_i - cos_t) / np.maximum(eta * cos_i + cos_t, EPS)
    r = 0.5 * (rs ** 2 + rp ** 2)
    return np.where(tir, 1.0, r)


def fresnel_schlick(cos_i, f0):
    c = np.clip(1.0 - np.asarray(cos_i, dtype=float), 0.0, 1.0)
    return f0 + (1.0 - f0) * c ** 5


def fresnel_conductor(cos_i, n, k):
    """导体界面反射率（非偏振），n、k 为复折射率的实部与虚部。"""
    cos_i = np.clip(np.asarray(cos_i, dtype=float), 0.0, 1.0)
    n = np.asarray(n, dtype=float)
    k = np.asarray(k, dtype=float)
    sin2 = 1.0 - cos_i ** 2
    a2 = n ** 2 - k ** 2 - sin2
    b2 = 2.0 * n * k
    t = np.sqrt(a2 ** 2 + b2 ** 2)
    a = np.sqrt(np.maximum(0.5 * (t + a2), 0.0))
    b = np.sqrt(np.maximum(0.5 * (t - a2), 0.0))
    rs = ((cos_i - a) ** 2 + b ** 2) / np.maximum((cos_i + a) ** 2 + b ** 2, EPS)
    num = (n ** 2 - k ** 2 - cos_i * a) ** 2 + (2 * n * k - cos_i * b) ** 2
    den = (n ** 2 - k ** 2 + cos_i * a) ** 2 + (2 * n * k + cos_i * b) ** 2
    rp = num / np.maximum(den, EPS)
    return 0.5 * (rs + rp)


# ---------------------------------------------------------------- NDF

def d_ggx(cos_h, alpha):
    """Trowbridge-Reitz（GGX）法线分布，各向同性。"""
    a2 = alpha ** 2
    c2 = np.clip(cos_h, 0.0, 1.0) ** 2
    den = c2 * (a2 - 1.0) + 1.0
    return a2 / (np.pi * np.maximum(den ** 2, EPS))


def d_beckmann(cos_h, alpha):
    c2 = np.clip(cos_h, 1e-6, 1.0) ** 2
    t2 = (1.0 - c2) / c2
    return np.exp(-t2 / alpha ** 2) / (np.pi * alpha ** 2 * c2 ** 2)


def d_ggx_aniso(cos_h, phi_h, ax, ay):
    """各向异性 GGX，ax、ay 为两个切线方向的粗糙度。"""
    sh2 = np.sin(phi_h) ** 2
    ch2 = np.cos(phi_h) ** 2
    c2 = np.clip(cos_h, 1e-6, 1.0) ** 2
    t2 = (1.0 - c2) / c2
    den = 1.0 + t2 * (ch2 / ax ** 2 + sh2 / ay ** 2)
    return 1.0 / (np.pi * ax * ay * np.maximum(c2 ** 2, EPS)
                  * np.maximum(den ** 2, EPS))


# ---------------------------------------------------------------- 遮蔽

def lambda_ggx(cos_v, alpha):
    c2 = np.clip(cos_v, 0.0, 1.0) ** 2
    a2 = alpha ** 2
    return 0.5 * (-1.0 + np.sqrt(1.0 + a2 * (1.0 - c2) / np.maximum(c2, EPS)))


def g1_smith(cos_v, alpha):
    return 1.0 / (1.0 + lambda_ggx(cos_v, alpha))


def g2_smith(cos_i, cos_o, alpha):
    return 1.0 / (1.0 + lambda_ggx(cos_i, alpha) + lambda_ggx(cos_o, alpha))


def g1_uncorrelated(cos_v, alpha):
    """不相关假设下的遮蔽-阴影函数，用作对比。"""
    c2 = np.clip(cos_v, 0.0, 1.0) ** 2
    return 2.0 * np.clip(cos_v, 0.0, 1.0) / (np.clip(cos_v, 0.0, 1.0)
                                             + np.sqrt(alpha ** 2 + (1 - alpha ** 2) * c2))


# ---------------------------------------------------------------- 微表面 BRDF

def brdf_ggx(wi, wo, alpha, f0, use_vndf=True):
    """单次散射 GGX 微表面 BRDF，返回标量或数组。"""
    wi = np.asarray(wi, float)
    wo = np.asarray(wo, float)
    h = half_vector(wi, wo)
    ci = np.clip(cos_theta(wi), 0.0, 1.0)
    co = np.clip(cos_theta(wo), 0.0, 1.0)
    ch = np.clip(cos_theta(h), 0.0, 1.0)
    F = fresnel_schlick(np.clip(np.sum(wi * h, axis=-1), 0, 1), f0)
    D = d_ggx(ch, alpha)
    G = g2_smith(ci, co, alpha)
    val = F * D * G / np.maximum(4.0 * ci * co, EPS)
    return np.where((ci > 0) & (co > 0), val, 0.0)


def sample_ggx_vndf(wi, u1, u2, alpha):
    """可见法线分布采样，返回半程向量。参考 Heitz 2018。"""
    wi = np.asarray(wi, float)
    vh = normalize(np.array([alpha * wi[0], alpha * wi[1], wi[2]]))
    lensq = vh[0] ** 2 + vh[1] ** 2
    t1 = np.array([1.0, 0.0, 0.0]) if lensq < 1e-12 else \
        np.array([-vh[1], vh[0], 0.0]) / np.sqrt(lensq)
    t2 = np.cross(vh, t1)
    r = np.sqrt(u1)
    phi = 2 * np.pi * u2
    p1 = r * np.cos(phi)
    p2 = r * np.sin(phi)
    s = 0.5 * (1.0 + vh[2])
    p2 = (1.0 - s) * np.sqrt(np.maximum(1.0 - p1 ** 2, 0.0)) + s * p2
    nh = p1 * t1 + p2 * t2 + np.sqrt(np.maximum(0.0, 1.0 - p1 ** 2 - p2 ** 2)) * vh
    h = normalize(np.array([alpha * nh[0], alpha * nh[1], max(nh[2], 0.0)]))
    return h


def pdf_ggx_vndf(wi, h, alpha):
    """VNDF 采样的 pdf（对半程向量）。"""
    wi = np.asarray(wi, float)
    h = np.asarray(h, float)
    ci = np.clip(wi[2], 0.0, 1.0)
    if ci <= 0 or h[2] <= 0:
        return 0.0
    G1 = g1_smith(ci, alpha)
    D = d_ggx(h[2], alpha)
    return G1 * np.clip(np.sum(wi * h), 0, 1) * D / max(ci, EPS)


# ---------------------------------------------------------------- 积分工具

def hemisphere_grid(n_theta=180, n_phi=360):
    """返回半球上均匀划分的 (theta, phi) 网格与对应的 dω 权重。"""
    theta = (np.arange(n_theta) + 0.5) * (np.pi / 2) / n_theta
    phi = (np.arange(n_phi) + 0.5) * 2 * np.pi / n_phi
    T, P = np.meshgrid(theta, phi, indexing="ij")
    domega = np.sin(T) * (np.pi / 2 / n_theta) * (2 * np.pi / n_phi)
    return T, P, domega


def integrate_hemisphere(fn, n_theta=180, n_phi=360):
    """在半球上积分 fn(wi, wo) * cos(theta_o) dω_o。"""
    T, P, domega = hemisphere_grid(n_theta, n_phi)
    W = spherical(T, P)
    return np.sum(fn(W) * np.cos(T) * domega)
