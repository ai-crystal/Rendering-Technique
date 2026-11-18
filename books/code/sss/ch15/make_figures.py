#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 15 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig15_1():
    """偶极子与蒙特卡洛的比值。"""
    ell = 1.0 / 2.0
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    for ap, c in ((0.999, RED), (0.9, ACCENT)):
        ms = 2.0 / (1 - 0.8)
        ma = ms * (1 - 0.8) * (1 - ap) / ap
        re, kind, ev = mc_slab(ma, ms, 0.8, n_photons=200000, max_events=4000,
                               rng=np.random.default_rng(21))
        ok = np.isfinite(re)
        edges = np.geomspace(0.02, 8, 60)
        area = np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
        rc = np.sqrt(edges[:-1] * edges[1:])
        cnt, _ = np.histogram(re[ok], bins=edges)
        mc = cnt / (ok.sum() * area)
        ax.plot(rc / ell, mc / rd_dipole(rc, ma, ms, 0.8, 1.0), "o-", ms=2.5,
                lw=1.1, color=c, label=rf"$\alpha'={ap}$")
    ax.axhline(1.0, color=GREY, lw=0.9, ls=(0, (4, 3)))
    ax.text(6.0, 1.1, "一致", fontsize=8, color=GREY)
    ax.set_xscale("log")
    ax.set_xlim(0.05, 16)
    ax.set_ylim(0.8, 20)
    ax.set_yscale("log")
    ax.set_xlabel(r"距离 $r/\ell^*$")
    ax.set_ylabel("蒙特卡洛 / 偶极子")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig15-1-ratio.png")


def fig15_2():
    """平板反射率随厚度的变化。"""
    ma, ms, g = 0.002, 10.0, 0.8
    Ls = np.array([0.2, 0.4, 0.8, 1.5, 3.0, 6.0, 12.0, 24.0])
    Rs = []
    for L in Ls:
        re, kind, ev = mc_slab(ma, ms, g, L=L, n_photons=80000,
                               max_events=4000, rng=np.random.default_rng(31))
        Rs.append(float(np.mean(kind == 0)))
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.semilogx(Ls, Rs, "o-", color=BLUE, ms=4, label="蒙特卡洛（反射）")
    dip = rd_total(lambda r: rd_dipole(r, ma, ms, g, 1.0), 40, 30000)
    ax.axhline(dip, color=ACCENT, ls=(0, (5, 3)), label="偶极子（与厚度无关）")
    ax.set_xlabel("板厚 L (mm)")
    ax.set_ylabel("总反射率")
    ax.set_ylim(0, 1.0)
    ax.set_xlim(0.15, 30)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(True, which="both", alpha=0.16)
    ax.axvspan(0.15, 1.0, color=GREY, alpha=0.08)
    ax.text(0.2, 0.90, r"$\sigma_tL<10$：扩散不适用", fontsize=8, color=GREY)
    save(fig, "fig15-2-thickness.png")


if __name__ == "__main__":
    fig15_1()
    fig15_2()
