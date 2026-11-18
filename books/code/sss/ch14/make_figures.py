#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 14 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403
from bsdf import fresnel_dielectric


def fig14_1():
    """S 的二维图。"""
    ma, ms, g, eta = 0.02, 10.0, 0.8, 1.4
    r = np.geomspace(0.05, 8, 260)
    th = np.linspace(0, 82, 200)
    R, T = np.meshgrid(r, th)
    Ft = 1 - fresnel_dielectric(np.cos(np.deg2rad(T)), eta)
    S = Ft * rd_dipole(R, ma, ms, g, eta) * Ft / np.pi
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    cs = ax.contourf(R, T, np.log10(S), levels=18, cmap="YlGnBu_r")
    ax.contour(R, T, np.log10(S), levels=18, colors="white", linewidths=0.3,
               alpha=0.5)
    cb = fig.colorbar(cs, ax=ax, pad=0.02)
    cb.set_label(r"$\log_{10}S$", fontsize=8)
    cb.ax.tick_params(labelsize=7.5)
    ax.set_xscale("log")
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"入射角 $\theta_i$ (度)")
    ax.set_ylim(0, 82)
    ax.grid(False)
    save(fig, "fig14-1-separable2d.png")


def fig14_2():
    """角分布是否随半径变化。"""
    ma, ms, g = 0.02, 10.0, 0.8
    rng = np.random.default_rng(9)
    re, kind, ev, co = mc_slab(ma, ms, g, n_photons=200000, max_events=2000,
                               rng=rng, with_angle=True)
    ok = np.isfinite(re)
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    bands = [(0.1, 0.3, ACCENT, "r = 0.1–0.3 mm"),
             (0.5, 1.5, TEAL, "r = 0.5–1.5 mm"),
             (2.0, 5.0, BLUE, "r = 2–5 mm")]
    edges = np.linspace(0, 1, 21)
    for lo, hi, c, lab in bands:
        m = ok & (re >= lo) & (re < hi)
        cnt, _ = np.histogram(co[m], bins=edges, density=True)
        ax.plot(0.5 * (edges[:-1] + edges[1:]), cnt, "o-", ms=3, color=c,
                label=lab)
    ax.set_xlabel(r"$\cos\theta_o$")
    ax.set_ylabel("概率密度")
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 6)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig14-2-angle.png")


if __name__ == "__main__":
    fig14_1()
    fig14_2()
