#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 9 到 11 章共用的二维路径场景。

平面布局（x 向右，z 向上）：

    z
    |            * 点光源 P
    |   [block]  |
    |   +----+   |
    |   |    |   |  ← 墙 x = 1，二次顶点 B 在墙上
    |   +----+   |
    +---------------- x    ← 地板 z = 0，主顶点 A 在地板上
      A

一次弹射的间接光：A 看到墙上的 B，B 由点光源照亮。遮挡体同时挡住
一部分 A 与 B、一部分 B 与光源。所有量都解析可算，真值用细网格积分。
"""
import numpy as np

WALL_X = 1.0
WALL_H = 2.0
LIGHT = np.array([0.30, 2.30])
BLOCK = (0.38, 0.58, 0.0, 0.72)      # x0, x1, z0, z1


def _segment_blocked(p, q, block=BLOCK):
    """线段 pq 是否穿过轴对齐矩形（参数裁剪，端点顺序无关）。"""
    x0, x1, z0, z1 = block
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    d = q - p
    t0 = np.zeros(np.broadcast_shapes(p.shape[:-1], q.shape[:-1]))
    t1 = np.ones_like(t0)
    for k, (lo, hi) in enumerate([(x0, x1), (z0, z1)]):
        dk = d[..., k]
        pk = p[..., k]
        with np.errstate(divide="ignore", invalid="ignore"):
            a = (lo - pk) / dk
            b = (hi - pk) / dk
        a, b = np.minimum(a, b), np.maximum(a, b)
        par = np.abs(dk) < 1e-12
        inside = (pk >= lo) & (pk <= hi)
        a = np.where(par, np.where(inside, -1e9, 1e9), a)
        b = np.where(par, np.where(inside, 1e9, -1e9), b)
        t0 = np.maximum(t0, a)
        t1 = np.minimum(t1, b)
    return t1 > t0


def geometry(ax, zb):
    """A=(ax,0) 到 B=(WALL_X, zb) 的几何量：r2、两端的余弦、可见性。"""
    ax, zb = np.broadcast_arrays(np.asarray(ax, float), np.asarray(zb, float))
    dx = WALL_X - ax
    r2 = dx ** 2 + zb ** 2
    r = np.sqrt(r2)
    cos_a = np.clip(zb / r, 0, 1)             # A 处法线 +z
    cos_b = np.clip(dx / r, 0, 1)             # 墙法线 -x
    vis = ~_segment_blocked(np.stack([ax, np.zeros_like(ax)], -1),
                            np.stack([np.full_like(ax, WALL_X), zb], -1))
    return r2, cos_a, cos_b, vis


def wall_radiance(zb, power=6.0):
    """墙上 B 点受到的点光源直接照明（含遮挡）。"""
    zb = np.asarray(zb, float)
    dx = LIGHT[0] - WALL_X
    dz = LIGHT[1] - zb
    r2 = dx ** 2 + dz ** 2
    cos_l = np.clip(-dx / np.sqrt(r2), 0, 1)      # 墙法线 (-1,0) 与指向光源的方向
    vis = ~_segment_blocked(np.stack([np.full_like(zb, WALL_X), zb], -1),
                            np.broadcast_to(LIGHT, zb.shape + (2,)))
    return power / (4 * np.pi * r2) * cos_l * vis


def integrand(ax, zb):
    """间接光被积函数（对墙上的弧长积分）。省略了常数因子 1/pi。"""
    r2, cos_a, cos_b, vis = geometry(ax, zb)
    on_wall = (zb >= 0.0) & (zb <= WALL_H)
    return wall_radiance(zb) * cos_a * cos_b / np.maximum(r2, 1e-12) * vis * on_wall


def target(ax, zb):
    """目标函数：去掉可见性的贡献，用于重采样权重（对应 DI 里的无阴影贡献）。"""
    r2, cos_a, cos_b, _ = geometry(ax, zb)
    on_wall = (zb >= 0.0) & (zb <= WALL_H)
    return wall_radiance(zb) * cos_a * cos_b / np.maximum(r2, 1e-12) * on_wall


def truth(ax, n=4001):
    zb = np.linspace(1e-4, WALL_H, n)
    val = integrand(ax, zb)
    return np.trapezoid(val, zb, axis=-1) if np.ndim(ax) else np.trapezoid(val, zb)


# ------------------------------------------------------------------ 采样

def sample_theta(n, rng):
    """地板上按 cos 权重抽方向：p(theta) = cos(theta)/2，theta in [-pi/2, pi/2]。"""
    u = rng.random(n)
    s = np.sqrt(u)                      # CDF: (1 + sin theta)/2 = u  =>  sin = 2u - 1
    s = 2 * u - 1
    return np.arcsin(np.clip(s, -1, 1))


def p_theta(theta):
    return np.cos(theta) / 2.0


def theta_to_z(theta, ax):
    d = WALL_X - np.asarray(ax, float)
    return d * np.tan(theta)


def p_z(zb, ax):
    """同一个墙上位置在 A 的方向采样下对应的弧长密度。"""
    d = WALL_X - np.asarray(ax, float)
    th = np.arctan(np.asarray(zb) / d)
    return p_theta(th) / (d * (1 + (np.asarray(zb) / d) ** 2))


def estimator(ax, zb, mode, ax_src=None):
    """给定墙上位置，返回三种做法下的贡献值。

    mode="reconnect"  重连接，按 A 的密度归一（正确）
    mode="nojac"      重连接，按来源像素的密度归一（漏掉雅可比）
    mode="direction"  方向复用（等价于按 A 的密度归一）
    """
    f = integrand(ax, zb)
    if mode == "nojac":
        return f / np.maximum(p_z(zb, ax_src), 1e-300)
    return f / np.maximum(p_z(zb, ax), 1e-300)


def valid(ax, zb):
    return geometry(ax, zb)[3]
