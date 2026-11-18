#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 10 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig10_1():
    """μ_eff 与 σa 的关系。"""
    sa = np.geomspace(1e-5, 10, 400)
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    for sp, c, lab in ((2.0, ACCENT, r"$\sigma_s'=2$"),
                       (0.5, TEAL, r"$\sigma_s'=0.5$")):
        ax.loglog(sa, np.sqrt(3 * sa * (sa + sp)), color=c, label=lab)
        ax.loglog(sa, np.sqrt(3 * sa * sp), color=c, ls=(0, (4, 3)), lw=0.9)
    ax.set_xlabel(r"吸收系数 $\sigma_a$  (mm$^{-1}$)")
    ax.set_ylabel(r"$\mu_{\rm eff}$  (mm$^{-1}$)")
    ax.set_xlim(1e-5, 10)
    ax.set_ylim(1e-4, 20)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(True, which="both", alpha=0.16)
    ax.text(3e-3, 0.6, r"$\mu_{\rm eff}\propto\sqrt{\sigma_a}$", fontsize=8.5,
            color=GREY)
    ax.text(2.0, 4.2, r"$\sigma_a\gg\sigma_s'$ 时斜率变为 1", fontsize=8,
            color=GREY, ha="right")
    save(fig, "fig10-1-mueff.png")


def fig10_2():
    """三个几何下的扩散解。"""
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    r = np.geomspace(0.05, 30, 400)
    ma, ms, g = 0.005, 10.0, 0.8
    D = diffusion_coeff(ma, ms, g)
    mu = mu_eff(ma, ms, g)
    ax.loglog(r, green_infinite(r, ma, ms, g), color=ACCENT,
              label=r"点源：$e^{-\mu r}/(4\pi D r)$")
    from scipy.special import k0
    ax.loglog(r, k0(mu * r) / (2 * np.pi * D), color=TEAL,
              label=r"线源：$K_0(\mu\rho)/(2\pi D)$")
    ax.set_xlabel("距离 (mm)")
    ax.set_ylabel("光通量密度（源功率为 1）")
    ax.set_xlim(0.05, 30)
    ax.set_ylim(1e-4, 3)
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig10-2-solutions.png")


if __name__ == "__main__":
    fig10_1()
    fig10_2()
