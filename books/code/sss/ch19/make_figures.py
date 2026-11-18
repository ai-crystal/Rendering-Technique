#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 19 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig19_1():
    """收敛速度：多次独立重复的标准差。"""
    ma, ms, g = 0.002, 10.0, 0.8
    ns = np.array([250, 500, 1000, 2000, 4000, 8000])
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    sds = []
    for n in ns:
        vals = []
        for k in range(40):
            d = mc_slab(ma, ms, g, n_photons=n, max_events=4000,
                        rng=np.random.default_rng(7000 + 17 * k + int(n)),
                        full=True)
            m = d["kind"] == 0
            vals.append(float(np.mean((d["r"][m] > 1.0) & (d["r"][m] < 1.3))))
        sds.append(float(np.std(vals, ddof=1)))
    sds = np.array(sds)
    ax.loglog(ns, sds, "o-", color=ACCENT, ms=4, label="40 次重复的标准差")
    ax.loglog(ns, sds[0] * (ns / ns[0]) ** -0.5, color=BLUE, lw=0.9,
              ls=(0, (4, 3)), label=r"$\propto N^{-1/2}$")
    ax.set_xlabel("每次运行的样本数 N")
    ax.set_ylabel("估计量的标准差")
    ax.set_xlim(200, 12000)
    ax.set_ylim(2e-3, 0.2)
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.16)
    print("sds", np.round(sds, 4))
    save(fig, "fig19-1-convergence.png")


def fig19_2():
    """平均散射次数与出射半径。"""
    aps = np.array([0.5, 0.7, 0.85, 0.95, 0.99, 0.999])
    ms = 2.0 / (1 - 0.8)
    ev_mean, depth = [], []
    for ap in aps:
        ma = ms * (1 - 0.8) * (1 - ap) / ap
        d = mc_slab(ma, ms, 0.8, n_photons=50000, max_events=4000,
                    rng=np.random.default_rng(121), full=True)
        m = d["kind"] == 0
        ev_mean.append(float(np.mean(d["events"][m])))
        depth.append(float(np.percentile(d["r"][m], 90)))
        print(ap, round(ev_mean[-1], 1), round(depth[-1], 2))
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    ax.semilogy(aps, ev_mean, "o-", color=ACCENT, ms=4, label="平均散射次数")
    ax.set_xlabel(r"输运反照率 $\alpha'$")
    ax.set_ylabel("平均散射次数")
    ax.set_xlim(0.45, 1.02)
    ax.grid(True, which="both", alpha=0.16)
    ax2 = ax.twinx()
    ell = 1.0 / 2.0
    ax2.semilogy(aps, np.array(depth) / ell, "s--", color=BLUE, ms=3.5,
                 label=r"90% 分位的出射半径 $/\ell^*$")
    ax2.set_ylabel(r"出射半径 $/\ell^*$", color=BLUE)
    ax2.tick_params(axis="y", colors=BLUE)
    ax2.spines["right"].set_visible(True)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=7.5, loc="upper left")
    save(fig, "fig19-2-cost.png")


if __name__ == "__main__":
    fig19_1()
    fig19_2()
