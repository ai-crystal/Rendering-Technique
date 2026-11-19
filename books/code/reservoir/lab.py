#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""后半部分的实验台。

四块内容，各章共用：

1. 半球积分：两技术的 MIS 方差，直接在方向网格上做数值积分，
   不靠蒙特卡洛，所以方差是算出来的而不是估出来的。
2. 加权蓄水池：A-Res 与跳步版本，用来核对选择频率与随机数消耗。
3. ReSTIR 玩具渲染器：一片像素、若干灯、随时间移动的场景，
   可以开关时间复用、空间复用、权重换算、可见性复用与候选数上限。
4. 体积与 GRIS：透射率估计、自由飞行采样、两个技术合并时的份额修正。

所有"真值"都是解析求和或数值积分，不是另一个渲染器算的。
"""
import numpy as np

import ris

TINY = 1e-300


# ------------------------------------------------------------------ 半球网格

def cone_grid(half_angle, tilt=0.0, nmu=400, nphi=256):
    """锥形灯内部的方向网格（绕 z 轴生成后转到灯轴）。mu 上做高斯求积。"""
    mu0 = np.cos(half_angle)
    x, wq = np.polynomial.legendre.leggauss(nmu)
    mu = mu0 + (1 - mu0) * 0.5 * (x + 1.0)
    wm = wq * 0.5 * (1 - mu0)
    ph = (np.arange(nphi) + 0.5) * (2 * np.pi) / nphi
    dph = 2 * np.pi / nphi
    M, P = np.meshgrid(mu, ph, indexing="ij")
    S = np.sqrt(np.maximum(1 - M ** 2, 0.0))
    loc = np.stack([S * np.cos(P), S * np.sin(P), M], axis=-1)
    c, sn = np.cos(tilt), np.sin(tilt)
    R = np.array([[c, 0, sn], [0, 1, 0], [-sn, 0, c]])
    return loc @ R.T, wm[:, None] * dph


def lobe_norm(kappa):
    """Z(k) = 积分 exp(k mu) mu dw，余弦指数叶瓣的归一化常数。"""
    k = np.asarray(kappa, float)
    return 2 * np.pi * (np.exp(k) * (k - 1) + 1) / (k * k)


def mis_study(kappa_f=30.0, kappa_p=9.0, half_angle=0.20, tilt=0.55,
              power=2.0, c_light=0.5, nmu=400, nphi=256):
    """锥形灯加叶瓣状 BRDF，数值积分算四种估计量的方差。

    f(w) = exp(k_f (w.axis)) (w.axis) / Z(k_f)，axis 与法线夹角 tilt；
    p_bsdf = exp(k_p mu_z) mu_z / Z(k_p)；p_light = 1/Omega 在锥内。
    两者都严格归一化，所以方差是积出来的。
    """
    d, dw = cone_grid(half_angle, tilt, nmu, nphi)
    mz = np.clip(d[..., 2], 0.0, 1.0)
    axis = np.array([np.sin(tilt), 0.0, np.cos(tilt)])
    ml = np.clip(d @ axis, 0.0, 1.0)
    omega_l = 2 * np.pi * (1 - np.cos(half_angle))

    zf, zp = lobe_norm(kappa_f), lobe_norm(kappa_p)
    f = np.exp(kappa_f * ml) * ml / zf
    p_b = np.exp(kappa_p * mz) * mz / zp
    p_l = np.full_like(f, 1.0 / omega_l)

    I = np.sum(f * dw)
    v_b = np.sum(f * f / p_b * dw) - I * I
    v_l = np.sum(f * f / p_l * dw) - I * I

    p_mis = p_b + p_l
    v_mis = np.sum(f * f / p_mis * dw) - I * I

    w_l = (c_light * p_l) ** power / ((c_light * p_l) ** power
                                      + ((1 - c_light) * p_b) ** power)
    w_b = 1.0 - w_l
    t_l = (w_l * f / p_l) ** 2 * p_l
    t_b = (w_b * f / p_b) ** 2 * p_b
    v_1 = c_light * np.sum(t_l * dw) + (1 - c_light) * np.sum(t_b * dw) - I * I

    return dict(I=I, omega_l=omega_l, var_bsdf=max(v_b, 0.0), var_light=max(v_l, 0.0),
                var_mis=max(v_mis, 0.0), var_one=max(v_1, 0.0), f=f, dw=dw,
                p_b=p_b, p_l=p_l, p_mis=p_mis, w_l=w_l)


def mis_weights_curve(r, power=2.0, c=0.5):
    """权重随密度比 r = p_light/p_bsdf 的变化（平衡与幂）。"""
    r = np.asarray(r, float)
    num = (c * r) ** power
    den = num + (1 - c) ** power
    return num / np.maximum(den, TINY)


# ------------------------------------------------------------------ 加权蓄水池

def wrs_ares(w, rng):
    """A-Res：key = u^(1/w)，留 key 最大者。"""
    w = np.maximum(np.asarray(w, float), TINY)
    key = rng.random(w.size) ** (1.0 / w)
    return int(np.argmax(key))


def wrs_ares_keys(w, rng):
    w = np.maximum(np.asarray(w, float), TINY)
    return rng.random(w.size) ** (1.0 / w)


def wrs_skip(n, rng):
    """等权流上的跳步采样（A-ExpJ 的等权特例）。返回 (下标, 均匀随机数个数)。"""
    i = 0
    best = 0
    key = rng.random()
    draws = 1
    while True:
        if key >= 1.0 - 1e-15:
            break
        u = rng.random()
        draws += 1
        skip = int(np.floor(np.log(max(u, TINY)) / np.log(key)))
        i += skip + 1
        if i >= n:
            break
        best = i
        key = key + (1.0 - key) * rng.random()
        draws += 1
    return best, draws


def wrs_skip_cost(n, trials=4000, seed=0):
    rng = np.random.default_rng(seed)
    tot = 0
    for _ in range(trials):
        _, d = wrs_skip(n, rng)
        tot += d
    return tot / trials


def merge_check(wa, wb, ma, mb, trials=120000, seed=0):
    """两个蓄水池合并后，样本分布是否等于对整个候选池做一次加权重采样。

    返回 (精确分布, 按 W 合并, 按 W*M 合并) 三组频率。
    """
    rng = np.random.default_rng(seed)
    na = wa.size
    w = np.concatenate([wa, wb])
    exact = w / w.sum()

    def run(pb_prob):
        hit = np.zeros(w.size)
        for _ in range(trials):
            ia = rng.choice(na, p=wa / wa.sum())
            ib = rng.choice(wb.size, p=wb / wb.sum())
            hit[ia if rng.random() >= pb_prob else na + ib] += 1
        return hit / trials

    good = run(wb.sum() / (wa.sum() + wb.sum()))
    bad = run(wb.sum() * mb / (wa.sum() * ma + wb.sum() * mb))
    return exact, good, bad


# ------------------------------------------------------------------ ReSTIR 玩具

def field(P, N, seed=0, profile="zipf", spread=0.9):
    g = int(round(np.sqrt(P)))
    return ris.make_scene(N, g, seed, profile, spread)


def vis_series(P, N, T, seed=0, p_lit=0.62, stick=0.93):
    V = np.zeros((T, P, N))
    for p in range(P):
        V[:, p, :] = ris.visibility(N, T, seed * 131 + p, p_lit, stick,
                                    soft=True, lo=0.10, hi=1.0)
    return V


def sim(P=64, N=64, T=24, M0=4, cap=20, radius=1, temporal=True, spatial=True,
        ratio=True, vis_test=False, amp=0.12, seed=0, profile="zipf",
        vis_p=0.62, skip_blocked=False, block_tol=0.25, motion="sine",
        bug_cap=False, clamp=None, switch_at=None, switch_gain=1.0, switch_frac=0.33,
        stale_mask=False, vis_stick=0.93, cull_weak=0.0, cull_random=0.0,
        deterministic=False, vis_shared=False, chain=False):
    """跑一串帧，返回 est[T,P]、truth[T,P]、M[T,P] 与可见性。

    skip_blocked=True 模拟"可见性复用"的一种错误实现：邻居样本在
    当前像素的可见性太差就直接丢掉，且不修正 M。
    """
    rng = np.random.default_rng(seed + 20260101)
    b = field(P, N, seed, profile)
    V = vis_series(P, N, T, seed, vis_p, stick=vis_stick)
    if vis_shared:
        V = np.repeat(V[:, :1, :], P, axis=1)
    mot = ris.motion_modulation(N, T, amp, seed, mode=motion)
    gain = np.ones((T, N))
    if switch_at is not None:
        rng_sw = np.random.default_rng(seed + 555)
        who = rng_sw.random(N) < switch_frac
        gain[switch_at:, who] = switch_gain

    g = int(round(np.sqrt(P)))
    ids = np.arange(P).reshape(g, g)
    offs = []
    for r in range(1, radius + 1):
        offs += [(0, r), (0, -r), (r, 0), (-r, 0)]
    shifts = [np.roll(np.roll(ids, dy, 0), dx, 1).ravel() for dy, dx in offs]

    est = np.zeros((T, P))
    tru = np.zeros((T, P))
    mh = np.zeros((T, P))
    prev = None

    for t in range(T):
        phat = b * mot[t][None, :] * gain[t][None, :]   # 目标函数：无阴影贡献
        if stale_mask:
            phat = phat * (V[t - 1] if t > 0 else V[0])
        keep = None
        if cull_weak > 0:
            k = int(cull_weak * N)
            keep = np.argsort(b.mean(axis=0))[:k]
        if cull_random > 0:
            rng_c = np.random.default_rng(seed + 9091)
            k = int(cull_random * N)
            keep = rng_c.choice(N, k, replace=False)
        f = phat * V[t]                                 # 真实贡献
        if keep is not None:
            phat = phat.copy()
            phat[:, keep] = 0.0                         # 目标函数里剔除，但真值保留
        tru[t] = f.sum(axis=1)

        # 初始候选
        idx = rng.integers(0, N, size=(P, M0))
        w = np.take_along_axis(phat, idx, axis=1) / (1.0 / N)
        W = w.sum(axis=1)
        cdf = np.cumsum(w, axis=1) / np.maximum(W[:, None], TINY)
        sel = np.minimum((rng.random((P, 1)) > cdf).sum(axis=1), M0 - 1)
        y = np.take_along_axis(idx, sel[:, None], axis=1)[:, 0]
        ph = np.take_along_axis(phat, y[:, None], axis=1)[:, 0]
        Mnew = np.full(P, float(M0))

        def combine(y_a, W_a, M_a, ph_a, y_b, W_b, M_b, ph_b, ph_cur, ph_own_b):
            if not ratio:
                Wb = W_b
            else:
                Wb = W_b * ph_cur / np.maximum(ph_own_b, TINY)
            tot = W_a + Wb
            pick = rng.random(P) < Wb / np.maximum(tot, TINY)
            if deterministic:
                pick = Wb > W_a
            m = M_a + M_b
            scale = np.minimum(1.0, cap / np.maximum(m, 1))
            if bug_cap:
                scale = np.ones_like(scale)        # 只钳 M，不缩 W
            return (np.where(pick, y_b, y_a), tot * scale, np.minimum(m, cap),
                    np.where(pick, ph_cur, ph_a))

        # 时间复用
        if temporal and prev is not None:
            y0, W0, M0_, ph0 = prev
            ph_cur = np.take_along_axis(phat, y0[:, None], axis=1)[:, 0]
            y, W, Mnew, ph = combine(y, W, Mnew, ph, y0, W0, M0_, ph0,
                                     ph_cur, ph0)

        # 空间复用（用快照，避免链式污染）
        if spatial and shifts:
            for sh in shifts:
                if chain:
                    snap = (y, W, Mnew, ph)
                else:
                    snap = (y.copy(), W.copy(), Mnew.copy(), ph.copy())
                y_j = snap[0][sh]
                ph_own = np.take_along_axis(phat[sh], y_j[:, None], axis=1)[:, 0]
                ph_cur = np.take_along_axis(phat, y_j[:, None], axis=1)[:, 0]
                if skip_blocked:
                    v_j = np.take_along_axis(V[t][sh], y_j[:, None], axis=1)[:, 0]
                    v_i = np.take_along_axis(V[t], y_j[:, None], axis=1)[:, 0]
                    bad = np.abs(v_i - v_j) > block_tol
                    if bad.any():
                        y_j = y_j.copy()
                        y_j[bad] = y[bad]
                        W_j = snap[1][sh] * np.where(bad, 0.0, 1.0)
                    else:
                        W_j = snap[1][sh]
                else:
                    W_j = snap[1][sh]
                if clamp is not None:
                    own_avg = np.maximum(W, TINY) / np.maximum(Mnew, 1.0)
                    W_j = np.minimum(W_j, clamp * own_avg * snap[2][sh])
                y, W, Mnew, ph = combine(y, W, Mnew, ph, y_j, W_j, snap[2][sh],
                                         snap[3][sh], ph_cur, ph_own)

        est[t] = np.take_along_axis(f, y[:, None], axis=1)[:, 0] \
            / np.maximum(np.take_along_axis(phat, y[:, None], axis=1)[:, 0], TINY) \
            * (W / Mnew)
        mh[t] = Mnew
        prev = (y, W, Mnew, ph)

    return dict(est=est, truth=tru, m=mh, vis=V, b=b, wsum=prev[1] if prev else None,
                whist=np.array([]) if prev is None else None)


def stats(est, truth):
    """逐像素相对误差的偏差、标准差与均方根。"""
    e = (np.asarray(est) - np.asarray(truth)) / np.maximum(np.asarray(truth), TINY)
    return dict(bias=float(e.mean()), relstd=float(e.std()),
                rmse=float(np.sqrt((e ** 2).mean())))


def bias_study(seeds=12, **cfg):
    """多种子跑同一场景，返回偏差与噪声。"""
    out = []
    for s in range(seeds):
        r = sim(seed=cfg.get("seed", 0) + 97 * s, **{k: v for k, v in cfg.items() if k != "seed"})
        out.append(stats(r["est"], r["truth"]))
    keys = out[0].keys()
    return {k: float(np.mean([o[k] for o in out])) for k in keys}


def curve_over(param, values, seeds=6, **cfg):
    rows = []
    for v in values:
        d = bias_study(seeds=seeds, **{**cfg, param: v})
        d[param] = v
        rows.append(d)
    return rows


# ------------------------------------------------------------------ 体积

def tr_homo(sigma, d):
    return np.exp(-sigma * np.asarray(d, float))


def delta_track(sigma_t, sigma_s, sigma_max, d, rng, mode="binary"):
    """均匀介质里沿距离 d 的透射率估计。返回 (估计值, 步数)。"""
    t = 0.0
    w = 1.0
    steps = 0
    while True:
        t -= np.log(max(rng.random(), TINY)) / sigma_max
        steps += 1
        if t >= d:
            break
        if rng.random() < sigma_t / sigma_max:      # 真碰撞
            if mode == "binary":
                return 0.0, steps
            return 0.0, steps
        w *= 1.0 - sigma_t / sigma_max              # 虚碰撞
        if mode == "binary":
            continue
    return w, steps


def heterogeneous_tau(a, b, L, d):
    """lambda(x) = a(1 + b sin(2 pi x / L)) 在 [0, d] 上的光学厚度。"""
    d = np.asarray(d, float)
    return a * (d + b * L / (2 * np.pi) * (1 - np.cos(2 * np.pi * d / L)))


def delta_track_hetero(tau_fn, sigma_max, d, rng, dmax=None, n_grid=4000):
    """非均匀介质：用查表得到任意位置的 sigma_t，做 delta tracking。"""
    xs = np.linspace(0, dmax, n_grid)
    taus = tau_fn(xs)
    dens = np.gradient(taus, xs)
    t = 0.0
    w = 1.0
    steps = 0
    while True:
        t -= np.log(max(rng.random(), TINY)) / sigma_max
        steps += 1
        if t >= d:
            break
        s = np.interp(t, xs, dens)
        if rng.random() < s / sigma_max:
            return 0.0, steps
        w *= 1.0 - s / sigma_max
    return w, steps


def volume_ris(M, sigma_t, Lfun, rng, mode="ris"):
    """沿一条射线做单次散射的距离采样，返回一次估计。

    Lfun(t) 是 t 处的入射辐亮度。目标函数 phat(t) = Tr(t) sigma_t L(t)，
    候选分布：mode='uniform' 取均匀，'exp' 取 Tr(t) sigma_t。
    """
    dmax = 4.0 / sigma_t
    if mode == "uniform":
        cand = rng.random(M) * dmax
        p = np.full(M, 1.0 / dmax)
    else:
        cand = -np.log(np.maximum(rng.random(M), TINY)) / sigma_t
        p = sigma_t * np.exp(-sigma_t * cand)
    tr = np.exp(-sigma_t * cand)
    phat = tr * sigma_t * Lfun(cand)
    w = phat / np.maximum(p, TINY)
    W = w.sum()
    cdf = np.cumsum(w) / max(W, TINY)
    y = cand[min(int((rng.random() > cdf).sum()), M - 1)]
    val = (W / M) * (tr_of(y, sigma_t) * sigma_t * Lfun(np.array([y]))[0]) / max(phat_of(y, sigma_t, Lfun), TINY)
    return val, W


def tr_of(t, sigma_t):
    return np.exp(-sigma_t * np.asarray(t, float))


def phat_of(t, sigma_t, Lfun):
    return np.exp(-sigma_t * np.asarray(t, float)) * sigma_t * Lfun(np.asarray(t, float))


# ------------------------------------------------------------------ GRIS

def gris_pool(pdf_list, M_list, phat, rng, correction=True, jac=None):
    """把若干技术的候选并成一个池子，返回被选中的候选 (技术号, 值)。

    w_i(x) = (M/M_i) * m_i(x) * phat_i(x) / p_i(x)，m_i 取 1。
    jac[i] 是技术 i 的移位映射雅可比，漏掉它就会把权重整体缩放。
    """
    M = sum(M_list)
    xs, ws, tags = [], [], []
    for i, (p, Mi) in enumerate(zip(pdf_list, M_list)):
        u = rng.random(Mi)
        x = p["inv"](u)
        w = phat(x) / np.maximum(p["pdf"](x), TINY)
        if correction:
            w = w * (M / Mi)
        if jac is not None:
            w = w * jac[i]
        xs.append(x)
        ws.append(w)
        tags.append(np.full(Mi, i))
    x = np.concatenate(xs)
    w = np.concatenate(ws)
    tag = np.concatenate(tags)
    cdf = np.cumsum(w) / max(w.sum(), TINY)
    k = min(int((rng.random() > cdf).sum()), x.size - 1)
    return tag[k], x[k], w.sum() / M

# ------------------------------------------------------------------ 采样器

def f_lobe(d, kappa, axis=(0.0, 0.0, 1.0), half_angle=None):
    """叶瓣状 BRDF 乘余弦：exp(k (w.axis)) (w.axis) / Z(k)，可选灯内指示。"""
    ax = np.asarray(axis, float)
    ml = np.clip(np.asarray(d) @ ax, 0.0, 1.0)
    val = np.exp(kappa * ml) * ml / lobe_norm(kappa)
    if half_angle is not None:
        val = val * ((np.asarray(d) @ ax) > np.cos(half_angle))
    return val


def p_lobe(d, kappa):
    mz = np.clip(np.asarray(d)[..., 2], 0.0, 1.0)
    return np.exp(kappa * mz) * mz / lobe_norm(kappa)


def sample_lobe(kappa, rng, n):
    """从 p ∝ exp(k mu) mu 抽方向，逆 CDF。"""
    mu = np.linspace(0.0, 1.0, 40001)
    cdf = np.cumsum(np.exp(kappa * mu) * mu)
    cdf /= cdf[-1]
    m = np.interp(rng.random(n), cdf, mu)
    s = np.sqrt(np.maximum(1 - m * m, 0.0))
    ph = 2 * np.pi * rng.random(n)
    return np.stack([s * np.cos(ph), s * np.sin(ph), m], axis=-1)


def sample_cone(half_angle, tilt, rng, n):
    mu0 = np.cos(half_angle)
    m = mu0 + (1 - mu0) * rng.random(n)
    s = np.sqrt(np.maximum(1 - m * m, 0.0))
    ph = 2 * np.pi * rng.random(n)
    loc = np.stack([s * np.cos(ph), s * np.sin(ph), m], axis=-1)
    c, sn = np.cos(tilt), np.sin(tilt)
    R = np.array([[c, 0, sn], [0, 1, 0], [-sn, 0, c]])
    return loc @ R.T


def mis_mc(kappa_f=60.0, kappa_p=9.0, half_angle=0.2, tilt=0.55, trials=200000,
           power=2.0, c_light=0.5, seed=0):
    """蒙特卡洛实测四种策略的均值与方差。真值由数值积分给出。"""
    rng = np.random.default_rng(seed)
    axis = (np.sin(tilt), 0.0, np.cos(tilt))
    ol = 2 * np.pi * (1 - np.cos(half_angle))

    d = sample_cone(half_angle, tilt, rng, trials)
    f_l = f_lobe(d, kappa_f, axis, half_angle)
    p_l_ = np.full(trials, 1.0 / ol)
    p_b_l = p_lobe(d, kappa_p)

    d2 = sample_lobe(kappa_p, rng, trials)
    f_b = f_lobe(d2, kappa_f, axis, half_angle)
    p_b_ = p_lobe(d2, kappa_p)
    p_l_b = np.zeros(trials)
    ax = np.asarray(axis)
    inside = (d2 @ ax) > np.cos(half_angle)
    p_l_b[inside] = 1.0 / ol

    est = {}
    est["light"] = f_l / p_l_
    est["bsdf"] = f_b / p_b_

    # 每技术各一个样本的 MIS
    w_l_l = (c_light * p_l_) ** power / ((c_light * p_l_) ** power + ((1 - c_light) * p_b_l) ** power)
    w_b_b = ((1 - c_light) * p_b_) ** power / ((c_light * p_l_b) ** power + ((1 - c_light) * p_b_) ** power)
    est["mis"] = w_l_l * f_l / p_l_ + w_b_b * f_b / p_b_

    # 单样本 MIS：按 c 选技术，除以混合密度 c p_light + (1-c) p_bsdf
    pick = rng.random(trials) < c_light
    mix_l = c_light * p_l_ + (1 - c_light) * p_b_l
    mix_b = c_light * p_l_b + (1 - c_light) * p_b_
    est["one"] = np.where(pick, f_l / np.maximum(mix_l, TINY),
                          f_b / np.maximum(mix_b, TINY))

    truth = mis_study(kappa_f, kappa_p, half_angle, tilt)["I"]
    out = {"truth": truth}
    for k, e in est.items():
        out[k] = dict(mean=float(e.mean()), var=float(e.var()),
                      relstd=float(e.std() / truth))
    return out
