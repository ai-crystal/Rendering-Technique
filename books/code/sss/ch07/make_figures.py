#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 7 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig7_1():
    """单次散射的角分布。"""
    th = np.linspace(0, 89, 400)
    c = np.cos(np.deg2rad(th))
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    for g, col, lab in ((0.0, GREY, "各向同性"), (0.5, TEAL, r"$g=0.5$"),
                        (0.8, RED, r"$g=0.8$")):
        L = ss_radiance(c, 1e-6, 10.0, g)
        ax.semilogy(th, L, color=col, label=lab)
        print(lab, "R_ss =", round(ss_reflectance(1e-6, 10.0, g), 4))
    ax.set_xlabel(r"出射角 $\theta_o$ (度)")
    ax.set_ylabel(r"$L_{\rm ss}$  (每单位入射辐照度)")
    ax.set_xlim(0, 89)
    ax.set_ylim(1e-4, 2e-1)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig7-1-ss-angle.png")


def fig7_2():
    """单次散射与多次散射的径向分布。"""
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    rng = np.random.default_rng(3)
    re, kind, ev = mc_slab(0.002, 10.0, 0.8, n_photons=150000,
                           max_events=2500, rng=rng)
    ok = np.isfinite(re)
    r1 = re[ok & (ev <= 2)]
    r2 = re[ok & (ev >= 3)]
    edges = np.linspace(0, 6, 70)
    area = np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
    rc = 0.5 * (edges[:-1] + edges[1:])
    n_tot = re.size
    for rr, c, lab in ((r1, ACCENT, "只散射一次"),
                       (r2, BLUE, "散射两次以上")):
        cnt, _ = np.histogram(rr, bins=edges)
        ax.semilogy(rc, cnt / (n_tot * area), color=c, label=lab)
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$R_d(r)$  (mm$^{-2}$)")
    ax.set_xlim(0, 6)
    ax.set_ylim(1e-5, 30)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig7-2-ss-radial.png")


def fig7_3():
    """单次散射的能量占比。"""
    fig, ax = plt.subplots(figsize=(4.9, 2.8))
    aps, fracs = [], []
    for ap in (0.40, 0.55, 0.70, 0.85, 0.95, 0.99, 0.999):
        ms = 2.0 / (1 - 0.8)
        ma = ms * (1 - 0.8) * (1 - ap) / ap
        re, kind, ev = mc_slab(ma, ms, 0.8, n_photons=60000, max_events=2000,
                               rng=np.random.default_rng(11))
        ok = np.isfinite(re)
        frac = np.mean(ev[ok] <= 2)
        aps.append(ap)
        fracs.append(frac)
        print("alpha'", ap, "fraction", round(frac, 3), "escaped", round(ok.mean(), 3))
    ax.plot(aps, fracs, "o-", color=ACCENT, ms=3.5)
    ax.set_xlabel(r"输运反照率 $\alpha'$")
    ax.set_ylabel("单次散射占出射能量的比例")
    ax.set_xlim(0.35, 1.02)
    ax.set_ylim(0, 1.0)
    ax.grid(alpha=0.2)
    save(fig, "fig7-3-ss-fraction.png")


if __name__ == "__main__":
    fig7_1()
    fig7_2()
    fig7_3()
