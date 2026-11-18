#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 20 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig20_1():
    ma, ms, g = 0.02, 10.0, 0.8
    r = np.linspace(1e-3, 8, 4000)
    rd = rd_dipole(r, ma, ms, g, 1.4)
    p = 2 * np.pi * r * rd
    inc = 0.5 * (p[1:] + p[:-1]) * np.diff(r)
    cdf = np.concatenate([[0.0], np.cumsum(inc)])
    tot = cdf[-1]
    cdf /= tot
    rng = np.random.default_rng(3)
    rs = np.interp(rng.random(30000), cdf, r)

    fig, axes = plt.subplots(2, 1, figsize=(5.4, 3.9), sharex=True)
    ax = axes[0]
    ax.plot(r, p / tot, color=ACCENT)
    ax.set_ylabel(r"$p(r)$  (1/mm)")
    ax.set_xlim(0, 6)
    ax.grid(alpha=0.18)
    for q, c, lab in ((0.5, BLUE, "50%"), (0.9, TEAL, "90%")):
        rq = float(np.interp(q, cdf, r))
        for a in axes:
            a.axvline(rq, color=c, lw=0.9, ls=(0, (4, 3)))
        ax.text(rq + 0.06, ax.get_ylim()[1] * 0.55, lab, fontsize=8, color=c)
        print(lab, round(rq, 2))
    ax = axes[1]
    ax.hist(rs, bins=np.linspace(0, 6, 60), density=True, color=GREY,
            alpha=0.55, label="采样直方图")
    ax.plot(r, p / tot, color=ACCENT, label="理论曲线")
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel("概率密度")
    ax.set_xlim(0, 6)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.18)
    fig.subplots_adjust(hspace=0.16)
    save(fig, "fig20-1-sampling.png")


def fig20_2():
    """重要性采样与均匀采样估计同一积分的方差。"""
    ma, ms, g = 0.02, 10.0, 0.8
    r = np.linspace(1e-3, 8, 4000)
    rd = rd_dipole(r, ma, ms, g, 1.4)
    p = 2 * np.pi * r * rd
    inc = 0.5 * (p[1:] + p[:-1]) * np.diff(r)
    cdf = np.concatenate([[0.0], np.cumsum(inc)])
    tot = cdf[-1]
    cdf /= tot
    # 真值：r < 1 mm 内的能量
    rq = float(np.interp(1.0, r, np.arange(r.size))) if False else None
    below = cdf[np.searchsorted(r, 0.15)]
    truth = tot * below
    print("truth", round(truth, 4), "R_tot", round(tot, 4))

    ns = np.array([32, 128, 512, 2048, 8192])
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    for kind, c, lab in (("uniform", GREY, "均匀采样"),
                         ("import", ACCENT, "按 $R_d$ 重要性采样")):
        sds = []
        for n in ns:
            vals = []
            for k in range(80):
                rng = np.random.default_rng(900 + 7 * k)
                if kind == "uniform":
                    R = 2.0
                    rr = R * np.sqrt(rng.random(n))
                    v = np.sum(rd_dipole(rr, ma, ms, g, 1.4) * 2 * np.pi * rr
                               * (rr < 0.15) * np.pi * R ** 2) / n
                else:
                    rr = np.interp(rng.random(n), cdf, r)
                    v = tot * np.mean(rr < 0.15)
                vals.append(v)
            sds.append(float(np.std(vals, ddof=1)))
        ax.loglog(ns, sds, "o-", ms=4, color=c, label=lab)
        print(lab, np.round(sds, 4))
    ax.set_xlabel("每次估计的样本数 N")
    ax.set_ylabel("估计量的标准差")
    ax.set_xlim(25, 12000)
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig20-2-variance.png")


if __name__ == "__main__":
    fig20_1()
    fig20_2()
