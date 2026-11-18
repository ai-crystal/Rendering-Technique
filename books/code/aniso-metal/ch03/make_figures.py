#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 3 章插图：各向异性法线分布与归一化。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from anisocommon import *       # noqa: F401,F403


def fig3_1():
    """D(h) 在 (θ, φ) 平面上的等值线。"""
    ax_r, ay_r = 0.08, 0.50
    th = np.linspace(0.1, 70, 360) * np.pi / 180
    ph = np.linspace(0, 2 * np.pi, 480)
    T, P = np.meshgrid(th, ph, indexing="ij")
    D = d_aniso(np.cos(T), P, ax_r, ay_r)
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    pc = ax.pcolormesh(np.degrees(P), np.degrees(T), np.log10(np.maximum(D, 1e-6)),
                       cmap="magma", shading="auto")
    cs = ax.contour(np.degrees(P), np.degrees(T), np.log10(np.maximum(D, 1e-6)),
                    levels=[-2, -1, 0, 1, 1.5, 2], colors="white", linewidths=0.7)
    ax.clabel(cs, fmt=lambda v: f"1e{v:g}", fontsize=6.5)
    ax.set_xlabel("方位角 $\\phi_h$ (度)")
    ax.set_ylabel("天顶角 $\\theta_h$ (度)")
    ax.set_xticks([0, 90, 180, 270, 360])
    ax.set_yticks([0, 20, 40, 60])
    ax.grid(False)
    cb = fig.colorbar(pc, ax=ax, pad=0.02)
    cb.set_label("$\\log_{10} D$")
    save(fig, "fig3-1-D-map.png")


def fig3_2():
    """φ = 0 与 φ = 90° 两个方向的切片。"""
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    th = np.linspace(0.0, 75, 500) * np.pi / 180
    c = np.cos(th)
    ax.semilogy(np.degrees(th), d_aniso(c, 0.0, 0.08, 0.50), color=ACCENT,
                label="$\\phi_h$ = 0，沿 $a_x$ = 0.08")
    ax.semilogy(np.degrees(th), d_aniso(c, np.pi / 2, 0.08, 0.50), color=BLUE,
                label="$\\phi_h$ = 90°，沿 $a_y$ = 0.50")
    ax.semilogy(np.degrees(th), d_aniso(c, 0.0, 0.20, 0.20), color=GREY, ls="--",
                label="各向同性，$a$ = 0.20")
    ax.set_xlabel("$\\theta_h$ (度)")
    ax.set_ylabel("$D(h)$")
    ax.set_xlim(0, 75)
    ax.set_ylim(1e-4, 1e3)
    ax.legend(loc="upper right")
    save(fig, "fig3-2-D-slices.png")


def fig3_3():
    """归一化积分的数值检验：正确版本与漏掉 cos^-4 的版本。"""
    def integ(fn, ax_, ay_, nt=420, npp=840):
        th = (np.arange(nt) + 0.5) * (np.pi / 2) / nt
        ph = (np.arange(npp) + 0.5) * 2 * np.pi / npp
        T, P = np.meshgrid(th, ph, indexing="ij")
        dw = np.sin(T) * (np.pi / 2 / nt) * (2 * np.pi / npp)
        return float(np.sum(fn(np.cos(T), P, ax_, ay_) * np.cos(T) * dw))

    ratio = np.linspace(1.0, 12.0, 24)
    good, bad = [], []
    for r in ratio:
        ax_, ay_ = 0.1, 0.1 * r
        good.append(integ(d_aniso, ax_, ay_))
        bad.append(integ(d_aniso_nocos4, ax_, ay_))
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    ax.plot(ratio, good, "o-", color=TEAL, ms=4, label="带 $1/\\cos^4\\theta$ 的版本")
    ax.plot(ratio, bad, "s-", color=RED, ms=4, label="漏掉 $1/\\cos^4\\theta$ 的版本")
    ax.axhline(1.0, color=INK, lw=0.9, ls=":")
    ax.set_xlabel("拉伸比 $a_y/a_x$（$a_x$ = 0.1）")
    ax.set_ylabel("$\\int D(h)\\,\\cos\\theta_h\\,\\mathrm{d}\\omega_h$")
    ax.set_ylim(0.4, 1.12)
    ax.legend(loc="lower left")
    save(fig, "fig3-3-normalization.png")


if __name__ == "__main__":
    fig3_1()
    fig3_2()
    fig3_3()
