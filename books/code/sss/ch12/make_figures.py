#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 12 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig12_1():
    """F_dr 与 A 随折射率的变化。"""
    eta = np.linspace(1.0, 2.0, 200)
    fdr = np.array([fdr_diffuse(e) for e in eta])
    A = (1 + fdr) / (1 - fdr)
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.8))
    ax = axes[0]
    ax.plot(eta, fdr, color=ACCENT)
    ax.axvline(1.4, color=GREY, lw=0.8, ls=(0, (4, 3)))
    ax.plot([1.4], [fdr_diffuse(1.4)], "o", ms=4, color=ACCENT)
    ax.annotate(r"$F_{dr}(1.4)=0.53$", xy=(1.4, fdr_diffuse(1.4)),
                xytext=(1.46, 0.30), fontsize=8,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
    ax.set_xlabel(r"相对折射率 $\eta$")
    ax.set_ylabel(r"$F_{dr}$")
    ax.set_xlim(1.0, 2.0)
    ax.set_ylim(0, 0.85)

    ax = axes[1]
    ax.plot(eta[1:], A[1:], color=BLUE)
    ax.axvline(1.4, color=GREY, lw=0.8, ls=(0, (4, 3)))
    ax.plot([1.4], [(1 + fdr_diffuse(1.4)) / (1 - fdr_diffuse(1.4))], "o",
            ms=4, color=BLUE)
    ax.set_xlabel(r"相对折射率 $\eta$")
    ax.set_ylabel(r"$A=(1+F_{dr})/(1-F_{dr})$")
    ax.set_xlim(1.0, 2.0)
    ax.set_ylim(0.8, 9)
    fig.subplots_adjust(wspace=0.34)
    save(fig, "fig12-1-fdr.png")


def fig12_2():
    """外推边界的几何与 fluence 的外推。"""
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.9))
    ma, ms, g, eta = 0.01, 10.0, 0.8, 1.4
    zb = zb_extrapolation(ma, ms, g, eta)
    D = diffusion_coeff(ma, ms, g)
    mr = mu_eff(ma, ms, g)
    ell = 1.0 / sigma_tr(ma, ms, g)

    ax = axes[0]
    ax.add_patch(plt.Rectangle((-0.1, 0), 6.4, 3.2, facecolor="#f0e6da",
                               edgecolor="none"))
    ax.axhline(0, color=INK, lw=1.4)
    ax.axhline(-zb, color=RED, lw=1.0, ls=(0, (5, 3)))
    ax.annotate("", xy=(6.2, 0), xytext=(6.2, -zb),
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=0.9,
                                mutation_scale=6))
    ax.text(5.9, -zb / 2, r"$z_b$", color=RED, fontsize=9, ha="right")
    ax.plot([3.0], [0.0], marker="v", ms=5, color=ACCENT)
    ax.annotate("", xy=(3.0, 0.9), xytext=(3.0, 0.05),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.1,
                                mutation_scale=8))
    ax.text(3.15, 0.75, "入射", fontsize=8.5, color=ACCENT)
    ax.text(0.15, 1.5, "介质", fontsize=9, color="#8a7a66")
    ax.text(0.15, 0.18, "真空", fontsize=9, color="#5b6472")
    ax.set_xlim(-0.1, 6.4)
    ax.set_ylim(3.2, -1.4)
    ax.set_xlabel("横向位置")
    ax.set_ylabel("深度 d")
    ax.set_title("几何", fontsize=9)
    ax.grid(False)

    ax = axes[1]
    d = np.linspace(-0.02, 3.0, 400)
    phi = green_infinite(np.abs(d - ell), ma, ms, g) - green_infinite(
        np.abs(d + ell + 2 * zb), ma, ms, g)
    ax.plot(d, phi, color=TEAL, label=r"$\phi(d)$")
    # 边界条件给出的线性近似：phi(0)(1 + d/zb)，在 d = -zb 处为零
    phi0 = float(np.interp(0.0, d, phi))
    dl = np.linspace(-zb - 0.2, 1.2, 40)
    ax.plot(dl, phi0 * (1 + dl / zb), color=ACCENT, lw=1.0,
            ls=(0, (4, 3)), label=r"$\phi(0)(1+d/z_b)$")
    ax.axvline(0, color=INK, lw=1.2)
    ax.axvline(-zb, color=RED, lw=0.9, ls=(0, (5, 3)))
    ax.axhline(0, color=GREY, lw=0.7)
    ax.set_xlim(-zb - 0.35, 3.0)
    ax.set_ylim(0, 0.9)
    ax.set_xlabel("深度 d (mm)")
    ax.set_ylabel("光通量密度 φ")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title(r"外推零值在 $d=-z_b$", fontsize=9)
    fig.subplots_adjust(wspace=0.30)
    save(fig, "fig12-2-extrapolation.png")


if __name__ == "__main__":
    fig12_1()
    fig12_2()
