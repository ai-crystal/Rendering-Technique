#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本书各章共用的玩具场景与重采样模拟器。

场景：一片像素被 N 个点光源照射。每盏灯对一个像素的无阴影贡献记作 b，
可见性记作 v（0 或 1），真实贡献是 b*v。目标函数（ReSTIR 里的 p̂）取 b
本身——它不含可见性，便宜、可解析，正是实际实现里"用近似目标函数"的
对应物。

所有章节的实验都调用这里，数字之间可以互相比较。
"""
import numpy as np

TINY = 1e-300


# ---------------------------------------------------------------- 场景

def _powers(n_lights, profile):
    if profile == "uniform":
        return np.ones(n_lights)
    if profile == "zipf":
        return 1.0 / np.arange(1, n_lights + 1)
    if profile == "spike":
        p = np.ones(n_lights)
        p[0] = 200.0
        return p
    if profile == "geometric":
        return 0.85 ** np.arange(n_lights)
    raise ValueError(profile)


def make_scene(n_lights=64, grid=1, seed=0, profile="zipf", spread=1.0):
    """返回 b[P, N]：每个像素、每盏灯的无阴影贡献（已归一化到均值为 1）。

    grid=1 表示单个着色点；grid=g 表示 g×g 的像素平铺在 z=0 平面上。
    """
    rng = np.random.default_rng(seed)
    pw = _powers(n_lights, profile)

    az = rng.uniform(-1.25, 1.25, n_lights)
    el = rng.uniform(0.20, 1.10, n_lights)
    dist = rng.uniform(1.7, 3.4, n_lights)
    lx = dist * np.cos(el) * np.sin(az)
    ly = dist * np.sin(el)
    lz = dist * np.cos(el) * np.cos(az)

    if grid > 1:
        c = np.linspace(-spread, spread, grid)
        X, Y = np.meshgrid(c, c)
        xp, yp = X.ravel(), Y.ravel()
    else:
        xp, yp = np.array([0.0]), np.array([0.0])

    dx = lx[None, :] - xp[:, None]
    dy = ly[None, :] - yp[:, None]
    dz = np.broadcast_to(lz[None, :], (xp.size, n_lights))
    d2 = dx ** 2 + dy ** 2 + dz ** 2
    cos = dz / np.sqrt(d2)
    b = pw[None, :] * np.maximum(cos, 0.0) / d2
    return b / b.mean()


def visibility(n_lights, frames, seed=0, p_lit=0.5, stickiness=0.93, soft=True,
               lo=0.2, hi=1.0):
    """可见性序列 v[T, N]。

    soft=True 时是软的（半影，取值在 0.2 到 1 之间缓慢游走），
    soft=False 时是硬的 0/1，两种都带时间相关性。
    """
    rng = np.random.default_rng(seed + 7919)
    if soft:
        mid = 0.5 * (lo + hi)
        v = np.zeros((frames, n_lights))
        cur = rng.uniform(lo, hi, n_lights)
        for t in range(frames):
            cur = mid + 0.9 * (cur - mid) + 0.06 * (hi - lo) * rng.standard_normal(n_lights)
            cur = np.clip(cur, lo, hi)
            v[t] = cur
        return v
    v = np.zeros((frames, n_lights))
    cur = (rng.random(n_lights) < p_lit).astype(float)
    for t in range(frames):
        flip = rng.random(n_lights) > stickiness
        new = (rng.random(n_lights) < p_lit).astype(float)
        cur = np.where(flip, new, cur)
        v[t] = cur
    return v


def motion_modulation(n_lights, frames, amp=0.0, seed=0, rate=0.25, mode="sine"):
    """m[T, N]：随帧变化的调制因子，模拟物体移动后距离与夹角的变化。

    mode="sine" 是来回摆动，mode="ramp" 是单向漂移（相机一直朝一个方向走）。
    """
    if amp == 0.0:
        return np.ones((frames, n_lights))
    rng = np.random.default_rng(seed + 104729)
    t = np.arange(frames)[:, None]
    if mode == "ramp":
        g = rng.uniform(0.5, 1.5, n_lights)
        return 1.0 + amp * (t / max(frames - 1, 1)) * g[None, :]
    ph = rng.uniform(0, 2 * np.pi, n_lights)
    w = rng.uniform(0.6, 1.4, n_lights) * rate
    return 1.0 + amp * np.sin(w[None, :] * t + ph[None, :])


def take(a, idx):
    return np.take_along_axis(a, idx, axis=-1)


# ---------------------------------------------------------------- 普通估计量

def mc_uniform(b, v, K, rng):
    """均匀选灯，K 个样本：F = N * mean(b_i v_i)。"""
    n = b.shape[-1]
    idx = rng.integers(0, n, size=b.shape[:-1] + (K,))
    return n * np.mean(take(b, idx) * v[idx], axis=-1)


def var_uniform(b, v, K=1):
    """均匀选灯的方差闭式：Var = (N Σ (b v)^2 - I^2)/K。"""
    f = b * v[None, :]
    n = b.shape[-1]
    I = f.sum(axis=-1)
    return (n * (f ** 2).sum(axis=-1) - I ** 2) / K


# ---------------------------------------------------------------- 蓄水池

def ris_step(phat, M, rng, p=None):
    """一次 RIS：从 p 抽 M 个候选，按 w = phat/p 选中一个。返回 (y, wsum)。"""
    n = phat.shape[-1]
    if p is None:
        p = np.full_like(phat, 1.0 / n)
    idx = rng.integers(0, n, size=phat.shape[:-1] + (M,))
    w = take(phat, idx) / take(p, idx)
    wsum = w.sum(axis=-1)
    cdf = np.cumsum(w, axis=-1) / np.maximum(wsum, TINY)[..., None]
    u = rng.random(phat.shape[:-1] + (1,))
    sel = np.minimum((u > cdf).sum(axis=-1), M - 1)
    return take(idx, sel[..., None])[..., 0], wsum


def shade(b, v, res, phat):
    """F = f(y)/p(y) * (wsum/M) / (phat(y)/p(y))，p 均匀时约掉。"""
    by = take(b, res.y[..., None])[..., 0]
    vy = take(v, res.y[..., None])[..., 0]
    phy = np.maximum(take(phat, res.y[..., None])[..., 0], TINY)
    return by * vy * (res.wsum / np.maximum(res.m, 1)) / phy


class Res:
    """一组蓄水池。y 选中的样本，wsum 权重和，m 候选数，ph 目标函数在该样本处的值。"""

    __slots__ = ("y", "wsum", "m", "ph")

    def __init__(self, y, wsum, m, ph):
        self.y, self.wsum, self.m, self.ph = y, wsum, m, ph

    @staticmethod
    def combine(a, b, ph_cur, cap, rng, ratio=True):
        """把 b 并进 a。ph_cur 是当前目标函数对 b.y 的评估。

        按 wb/(wa+wb) 的概率选中 b 的样本——这里必须真随机，
        取"谁权重大就选谁"会引入偏差。
        """
        rb = ph_cur / np.maximum(b.ph, TINY) if ratio else np.ones_like(b.wsum)
        wb = b.wsum * rb
        tot = a.wsum + wb
        u = rng.random(a.wsum.shape)
        pick = u < wb / np.maximum(tot, TINY)
        m = a.m + b.m
        scale = np.minimum(1.0, cap / np.maximum(m, 1))
        return Res(
            np.where(pick, b.y, a.y),
            tot * scale,
            np.minimum(m, cap),
            np.where(pick, ph_cur, a.ph),
        )


# ---------------------------------------------------------------- 完整模拟

DEFAULT = dict(M=8, cap=20, radius=0, frames=48, temporal=True, spatial=True,
               ratio=True, amp=0.1, p_lit=0.5, profile="zipf",
               n_lights=64, grid=1, seed=0, soft=True, vis=(0.7, 1.0))


def run(**kw):
    """跑一串帧，返回 dict(est[T,P], truth[T,P], m[T,P], wsum[T,P])。"""
    cfg = dict(DEFAULT)
    cfg.update(kw)
    rng = np.random.default_rng(cfg["seed"] + 12345)
    N, P = cfg["n_lights"], cfg["grid"] ** 2
    b = make_scene(N, cfg["grid"], cfg["seed"], cfg["profile"])
    mot = motion_modulation(N, cfg["frames"], cfg["amp"], cfg["seed"])
    vis = visibility(N, cfg["frames"], cfg["seed"], cfg["p_lit"],
                     soft=cfg["soft"], lo=cfg["vis"][0], hi=cfg["vis"][1])
    mask = np.ones(N) if cfg.get("mask") is None else np.asarray(cfg["mask"], float)
    cap = cfg["cap"]

    shifts = []
    if cfg["grid"] > 1:
        g = cfg["grid"]
        ids = np.arange(P).reshape(g, g)
        for r in range(1, cfg["radius"] + 1):
            for dy, dx in ((0, r), (0, -r), (r, 0), (-r, 0)):
                sh = np.roll(np.roll(ids, dy, axis=0), dx, axis=1)
                shifts.append(sh.ravel())
        shifts = np.array(shifts) if shifts else np.zeros((0, P), int)
    else:
        shifts = np.zeros((0, P), int)

    est = np.zeros((cfg["frames"], P))
    tru = np.zeros((cfg["frames"], P))
    mhist = np.zeros((cfg["frames"], P))
    prev = None

    for t in range(cfg["frames"]):
        phat = b * mot[t][None, :] * mask[None, :]
        f = b * mot[t][None, :] * vis[t][None, :]
        tru[t] = f.sum(axis=1)

        y, wsum = ris_step(phat, cfg["M"], rng)
        res = Res(y, wsum, np.full(P, cfg["M"]), take(phat, y[..., None])[..., 0])

        if cfg["temporal"] and prev is not None:
            ph_cur = take(phat, prev.y[..., None])[..., 0]
            res = Res.combine(res, prev, ph_cur, cap, rng, ratio=cfg["ratio"])

        if cfg["spatial"] and shifts.shape[0] > 0:
            snap = Res(res.y.copy(), res.wsum.copy(), res.m.copy(), res.ph.copy())
            for j in shifts:
                y_j = snap.y[j]
                ph_own = take(phat[j], y_j[..., None])[..., 0]
                ph_cur = take(phat, y_j[..., None])[..., 0]
                other = Res(y_j, snap.wsum[j], snap.m[j], ph_own)
                res = Res.combine(res, other, ph_cur, cap, rng, ratio=cfg["ratio"])

        est[t] = shade(b, vis[t][None, :] * mot[t][None, :], res, phat)
        mhist[t] = res.m
        prev = res

    return dict(est=est, truth=tru, m=mhist, wsum=prev.wsum)
