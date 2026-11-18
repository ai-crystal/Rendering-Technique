#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 8 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig8_1():
    """扩散有效的区间：厚度与反照率。"""
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    ap = np.linspace(0.05, 0.999, 300)
    # σs' 取 2，σa 由 α' 决定；μ_eff L 的判据
    for ratio, c, lab in ((0.02, ACCENT, r"$\sigma_a/\sigma_s'=0.02$"),
                          (0.2, TEAL, r"$\sigma_a/\sigma_s'=0.2$"),
                          (1.0, BLUE, r"$\sigma_a/\sigma_s'=1$")):
        # 把 α' 换成 σa/σs'
        r_ = (1 - ap) / ap
        # 上界：L < 1/μ_eff，用 L 以输运自由程为单位表达
        L = 1.0 / np.sqrt(3.0 * r_) / (1 + r_)
        ax.plot(ap, L, color=c, label=lab)
    ax.set_yscale("log")
    ax.set_ylim(0.3, 200)
    ax.set_xlim(0.05, 1.0)
    ax.axhline(3.0, color=GREY, lw=0.9, ls=(0, (4, 3)))
    ax.text(0.07, 3.4, "下界：L = 3ℓ*", fontsize=8, color=GREY)
    ax.fill_between([0.05, 1.0], 3.0, 200, color=ACCENT, alpha=0.05)
    ax.set_xlabel(r"输运反照率 $\alpha'$")
    ax.set_ylabel(r"扩散有效的最大厚度  $L/\ell^*$")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(True, which="both", alpha=0.15)
    save(fig, "fig8-1-regime.png")


def fig8_2():
    """偶极子与蒙特卡洛的剖面对比。"""
    ma, ms, g = 0.002, 10.0, 0.8
    r = np.linspace(0.02, 8, 400)
    rng = np.random.default_rng(5)
    re, kind, ev = mc_slab(ma, ms, g, n_photons=150000, max_events=20000, rng=rng)
    ok = np.isfinite(re)
    edges = np.linspace(0, 8, 90)
    area = np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
    rc = 0.5 * (edges[:-1] + edges[1:])
    cnt, _ = np.histogram(re[ok], bins=edges)
    n_tot = re.size
    mc = cnt / (n_tot * area)
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.semilogy(rc, mc, color=BLUE, label="蒙特卡洛")
    ax.semilogy(r, rd_dipole(r, ma, ms, g, 1.0), color=ACCENT, label="偶极子")
    print("MC 总反射率", round(float(np.mean(kind == 0)), 3))
    print("偶极子总反射率", round(rd_total(lambda x: rd_dipole(x, ma, ms, g, 1.0), 40, 30000), 3))
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$R_d(r)$  (mm$^{-2}$)")
    ax.set_xlim(0, 8)
    ax.set_ylim(1e-5, 3)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.16)
    ax.annotate("近源处偏低", xy=(0.12, 0.55), xytext=(1.3, 1.6), fontsize=8,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    save(fig, "fig8-2-mc-vs-dipole.png")


if __name__ == "__main__":
    fig8_1()
    fig8_2()
