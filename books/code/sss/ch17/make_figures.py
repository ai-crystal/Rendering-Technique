#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 17 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403
from scipy.optimize import brentq


def burley(r, d, A=1.0):
    """Christensen & Burley 2015 的归一化剖面（面积分为 A）。"""
    r = np.maximum(np.asarray(r, float), 1e-9)
    return A * (np.exp(-r / d) + np.exp(-r / (3 * d))) / (8 * np.pi * d * r)


def half_width_in_d():
    """归一化剖面的半衰减半径，以 d 为单位。"""
    f = lambda x: burley(x, 1.0) - burley(0.02, 1.0) / np.e
    return brentq(f, 0.05, 10.0)


def fig17_1():
    ap = 0.99
    ms = 2.0 / (1 - 0.8)
    ma = ms * (1 - 0.8) * (1 - ap) / ap
    d = mc_slab(ma, ms, 0.8, n_photons=200000, max_events=3000,
                rng=np.random.default_rng(51), full=True)
    ok = d["kind"] == 0
    n = d["r"].size
    edges = np.geomspace(0.03, 6, 55)
    area = np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
    rc = np.sqrt(edges[:-1] * edges[1:])
    cnt, _ = np.histogram(d["r"][ok], bins=edges)
    mc = cnt / (n * area)
    keep = cnt > 30
    tot = float(np.mean(d["kind"] == 0))

    r = np.geomspace(0.03, 6, 500)
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    ax.loglog(rc[keep], mc[keep], "o", ms=3, color=BLUE, label="蒙特卡洛")
    ax.loglog(r, rd_dipole(r, ma, ms, 0.8, 1.0), color=ACCENT, label="偶极子")
    for dd, c, ls in ((0.25, TEAL, (0, (5, 2))), (0.5, PURPLE, (0, (1, 2)))):
        ax.loglog(r, burley(r, dd, tot), color=c, ls=ls,
                  label=rf"归一化剖面 $d={dd}$ mm")
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$R_d(r)$  (mm$^{-2}$)")
    ax.set_xlim(0.03, 6)
    ax.set_ylim(1e-5, 3)
    ax.legend(fontsize=7.5, loc="lower left")
    ax.grid(True, which="both", alpha=0.16)
    print("MC total", round(tot, 3),
          "dipole", round(rd_total(lambda x: rd_dipole(x, ma, ms, 0.8, 1.0), 40, 30000), 3))
    save(fig, "fig17-1-profiles.png")


def fig17_2():
    """两个指数 = 两个扩散模式的叠加。"""
    d = 0.30
    r = np.geomspace(0.02, 4, 500)
    fig, ax = plt.subplots(figsize=(5.0, 2.9))
    m1 = np.exp(-r / d) / (8 * np.pi * d * r) / 4
    m2 = np.exp(-r / (3 * d)) / (8 * np.pi * d * r) * 3 / 4
    ax.loglog(r, m1, color=BLUE, ls=(0, (5, 2)), label=r"第一模式 $e^{-r/d}$")
    ax.loglog(r, m2, color=TEAL, ls=(0, (1, 2)), label=r"第二模式 $e^{-r/(3d)}$")
    ax.loglog(r, m1 + m2, color=ACCENT, label="两者之和（归一化剖面）")
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$R(r)$  (mm$^{-2}$)")
    ax.set_xlim(0.02, 4)
    ax.set_ylim(1e-5, 3)
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig17-2-modes.png")


if __name__ == "__main__":
    fig17_1()
    fig17_2()
