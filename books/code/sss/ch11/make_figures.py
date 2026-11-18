#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 11 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig11_1():
    """点源的 Green 函数。"""
    r = np.geomspace(0.02, 40, 500)
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    for ma, c, lab in ((0.0005, BLUE, r"$\sigma_a=5\times10^{-4}$"),
                       (0.01, TEAL, r"$\sigma_a=0.01$"),
                       (0.10, ACCENT, r"$\sigma_a=0.1$")):
        ax.loglog(r, green_infinite(r, ma, 10.0, 0.8), color=c, label=lab)
    ax.loglog(r, 1 / (4 * np.pi * diffusion_coeff(0.01, 10.0, 0.8) * r),
              color=GREY, lw=0.9, ls=(0, (4, 3)))
    ax.text(6.0, 0.02, r"$1/r$", fontsize=9, color=GREY)
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$\phi(r)$（源功率为 1，mm$^{-2}$）")
    ax.set_xlim(0.02, 40)
    ax.set_ylim(1e-4, 30)
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig11-1-green.png")


def fig11_2():
    """一正一负两个源，以及它们的和。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.9))
    ma, ms, g = 0.01, 10.0, 0.8
    mr = mu_eff(ma, ms, g)
    D = diffusion_coeff(ma, ms, g)
    zb = zb_extrapolation(ma, ms, g, 1.4)
    ell = 1.0 / sigma_tr(ma, ms, g)
    d = np.linspace(-4.5, 6.0, 500)

    def src(d0, sgn):
        x = np.abs(d - d0)
        return sgn * np.exp(-mr * np.maximum(x, 1e-3)) / (
            4 * np.pi * D * np.maximum(x, 1e-3))

    ax = axes[0]
    ax.plot(d, src(ell, 1.0), color=ACCENT, label=r"正源（深度 $\ell$）")
    ax.plot(d, src(-ell - 2 * zb, -1.0), color=BLUE,
            label=r"负源（表面上方 $\ell+2z_b$）")
    ax.set_yscale("symlog", linthresh=0.05)
    ax.set_ylim(-3, 4)
    ax.set_xlabel("深度 d (mm)")
    ax.set_ylabel("光通量密度")
    ax.legend(fontsize=7.5, loc="lower right")
    ax.axhline(0, color=GREY, lw=0.7)
    ax.axvline(0, color=GREY, lw=0.7)
    ax.set_title("两个源的场", fontsize=9)

    ax = axes[1]
    tot = src(ell, 1.0) + src(-ell - 2 * zb, -1.0)
    ax.plot(d, tot, color=TEAL)
    ax.set_yscale("symlog", linthresh=0.05)
    ax.set_ylim(-3, 4)
    ax.set_xlabel("深度 d (mm)")
    ax.axhline(0, color=GREY, lw=0.7)
    ax.axvline(0, color=GREY, lw=0.7)
    ax.axvline(-zb, color=RED, lw=0.9, ls=(0, (4, 3)))
    ax.text(-zb - 0.15, 2.2, r"$-z_b$", fontsize=9, color=RED, ha="right")
    ax.set_title("叠加：在 $d=-z_b$ 处为零", fontsize=9)
    fig.subplots_adjust(wspace=0.32)
    save(fig, "fig11-2-superpose.png")


if __name__ == "__main__":
    fig11_1()
    fig11_2()
