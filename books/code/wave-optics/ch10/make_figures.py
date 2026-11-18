import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *

NS = [1.38, 2.05, 1.70]
DS = [90.0, 115.0, 55.0]


def refl_single(lam, d, n0, n1, n2):
    r01 = (n0 - n1) / (n0 + n1)
    r12 = (n1 - n2) / (n1 + n2)
    delta = 4 * np.pi * n1 * d / lam
    r = (r01 + r12 * np.exp(1j * delta)) / (1 + r01 * r12 * np.exp(1j * delta))
    return np.abs(r) ** 2


def stack_RT(lam, ns, ds, nsub, th0=0.0):
    st = np.sin(th0)
    th = [np.emath.arcsin(st / n) for n in ns]
    ths = np.emath.arcsin(st / nsub)
    M = np.eye(2, dtype=complex)
    for n, d, t in zip(ns, ds, th):
        e = n * np.cos(t)
        phi = 2 * np.pi * n * d * np.cos(t) / lam
        # 从基底往上走，用逆矩阵
        M = M @ np.array([[np.cos(phi), -1j * np.sin(phi) / e],
                          [-1j * e * np.sin(phi), np.cos(phi)]])
    e0 = np.cos(th0)
    es = nsub * np.cos(ths)
    B, C = M @ np.array([1.0, es])
    r = (e0 * B - C) / (e0 * B + C)
    t = 2 * e0 / (e0 * B + C)
    return abs(r) ** 2, (np.real(es) / np.real(e0)) * abs(t) ** 2


def R_stack(lam, th0=0.0):
    return stack_RT(lam, NS, DS, 1.52, th0)[0]


def fig10_1():
    lam = np.linspace(380, 780, 4000)
    R = refl_single(lam, 900.0, 1.0, 2.3, 1.5)
    S = lambda x: 1.0 + 0.3 * np.cos((x - 500) / 120)
    truth = np.trapezoid(R * S(lam), lam)
    rng = np.random.default_rng(3)
    Ns = np.array([1, 2, 4, 8, 16, 32])
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for strat, col, lab in [(False, BLUE, "独立采样"), (True, ACCENT, "分层采样")]:
        sd = []
        for n in Ns:
            vals = [integrate(lam, R, S, n, strat, rng) for _ in range(2000)]
            sd.append(np.std(vals))
        ax.loglog(Ns, np.array(sd) / truth, "o-", color=col, lw=1.8, ms=4, label=lab)
    ax.plot(Ns, 0.28 / np.sqrt(Ns), "--", color=GREY, lw=1.0)
    ax.set_xlabel("每个样本的波长数")
    ax.set_ylabel("估计值的相对标准差")
    ax.set_xlim(1, 40)
    ax.set_ylim(0.01, 0.4)
    ax.legend(loc="lower left", fontsize=8)
    ax.text(2.2, 0.30, "灰线斜率 -1/2", fontsize=8, color=GREY)
    save(fig, "fig10-1-stratify.png")


def integrate(lam, R, S, n, strat, rng):
    lo, hi = 380.0, 780.0
    if strat:
        edges = np.linspace(lo, hi, n + 1)
        x = edges[:-1] + rng.random(n) * (hi - lo) / n
    else:
        x = lo + rng.random(n) * (hi - lo)
    w = (hi - lo) / n
    return np.sum(np.interp(x, lam, R) * S(x) * w)


THK_NS = []
THK_DS = []
for _k in range(10):
    THK_NS += [2.05, 1.38]
    THK_DS += [4 * 550 / (4 * 2.05), 4 * 550 / (4 * 1.38)]


def fig10_2():
    lam_hi = np.linspace(400, 700, 700)
    th_hi = np.arccos(np.linspace(1.0, 0.26, 64))
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    counts = [8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256]
    for ns, ds, col, lab in [(NS, DS, ACCENT, "三层膜系，总厚 260 nm"),
                             (THK_NS, THK_DS, BLUE, "二十层膜系，总厚 6.7 微米")]:
        TRUE = np.array([[stack_RT(l, ns, ds, 1.52, t)[0] for l in lam_hi] for t in th_hi])
        scale = TRUE.max()
        errs = []
        for nl in counts:
            lam_t = np.linspace(400, 700, nl)
            th_t = np.arccos(np.linspace(1.0, 0.26, 64))
            T = np.array([[stack_RT(l, ns, ds, 1.52, t)[0] for l in lam_t] for t in th_t])
            mx = 0.0
            for i_t, t in enumerate(th_t):
                frac = (1.0 - np.cos(t)) / (1.0 - 0.26)
                k = np.clip(frac * 63, 0, 62)
                i0 = int(k)
                w = k - i0
                row = (1 - w) * T[i0] + w * T[i0 + 1]
                est = np.interp(lam_hi, lam_t, row)
                mx = max(mx, np.max(np.abs(est - TRUE[i_t])) / scale)
            errs.append(mx * 100)
        ax.plot(counts, errs, "o-", color=col, lw=1.8, ms=3.5, label=lab)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("波长方向的表点数")
    ax.set_ylabel("双线性插值的最大误差（%）")
    ax.set_xlim(6, 320)
    ax.legend(loc="upper right", fontsize=8)
    ax.text(7.0, 2.6, "误差以最大反射率为基准", fontsize=7.5, color=GREY)
    save(fig, "fig10-2-table.png")


def fig10_3():
    lam = np.linspace(400, 700, 500)
    ns = [1.38, 2.05 + 0.05j, 1.70]
    R, T = [], []
    for l in lam:
        r, t = stack_RT(l, ns, DS, 1.52)
        R.append(r)
        T.append(t)
    R = np.array(R)
    T = np.array(T)
    A = 1 - R - T
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.plot(lam, R * 100, color=BLUE, lw=1.8, label="反射率 R")
    ax.plot(lam, T * 100, color=TEAL, lw=1.8, label="透射率 T")
    ax.plot(lam, A * 100, color=ACCENT, lw=1.8, label="吸收率 A")
    ax.plot(lam, (R + T + A) * 100, color=GREY, lw=1.0, ls="--", label="R + T + A")
    ax.set_xlim(400, 700)
    ax.set_ylim(0, 103)
    ax.set_xlabel("波长（nm）")
    ax.set_ylabel("占比（%）")
    ax.legend(loc="center right", fontsize=8)
    save(fig, "fig10-3-energy.png")


fig10_1()
fig10_2()
fig10_3()
