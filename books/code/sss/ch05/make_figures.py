#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 5 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig5_1():
    """HG 相函数的极坐标形状。"""
    fig = plt.figure(figsize=(3.9, 3.9))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_position([0.10, 0.13, 0.78, 0.76])
    th = np.linspace(0, 2 * np.pi, 500)
    for g, c in ((0.0, GREY), (0.5, TEAL), (0.9, RED), (-0.5, BLUE)):
        p = hg_phase(np.cos(th), g)
        ax.plot(th, p, color=c, lw=1.5, label=rf"$g={g}$")
    ax.set_rlim(0, 1.6)
    ax.set_rticks([])
    ax.set_thetagrids([0, 90, 180, 270], ["前向", "90°", "后向", "270°"],
                      fontsize=8)
    ax.grid(alpha=0.25)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=4,
              fontsize=8, handlelength=1.2, columnspacing=0.8)
    ax.set_title(r"$p_{\rm HG}(\cos\theta)$", fontsize=9, pad=8)
    save(fig, "fig5-1-hg.png")


def fig5_2():
    """相似关系：偶极子完全重合，蒙特卡洛在近源处仍有差别。"""
    sets = [(10.0, 0.8, RED, r"$\sigma_s=10,\ g=0.8$"),
            (2.0, 0.0, TEAL, r"$\sigma_s=2,\ g=0$"),
            (4.0, 0.5, BLUE, r"$\sigma_s=4,\ g=0.5$")]
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.0))

    ax = axes[0]
    r = np.linspace(0.01, 6.0, 500)
    for ms, g, c, lab in sets:
        ax.semilogy(r, rd_dipole(r, 0.005, ms, g, 1.4), color=c, label=lab,
                    lw=2.6 if g == 0.8 else 1.3,
                    alpha=0.85 if g == 0.8 else 1.0)
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$R_d(r)$  (mm$^{-2}$)")
    ax.set_xlim(0, 6)
    ax.set_ylim(1e-5, 1.5)
    ax.legend(fontsize=7.5, loc="upper right")
    ax.grid(True, which="both", alpha=0.16)
    ax.set_title("偶极子公式：三条曲线重合", fontsize=9)

    ax = axes[1]
    for ms, g, c, lab in sets:
        re, kind, ev = mc_slab(0.005, ms, g, n_photons=40000, max_events=1500)
        rr, R, n = mc_radial_profile(re, 90, 6.0)
        ax.semilogy(rr, R, color=c, label=lab)
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"蒙特卡洛的 $R_d(r)$  (mm$^{-2}$)")
    ax.set_xlim(0, 6)
    ax.set_ylim(1e-5, 1.5)
    ax.grid(True, which="both", alpha=0.16)
    ax.set_title("蒙特卡洛：差别在噪声以内", fontsize=9)
    ax.text(0.06, 3e-5, "三组参数的差别在噪声以内", fontsize=7.5, color=GREY)

    fig.subplots_adjust(wspace=0.32)
    save(fig, "fig5-2-similarity.png")


def fig5_3():
    """方向记忆按 g^n 衰减。"""
    n = np.arange(0, 41)
    fig, ax = plt.subplots(figsize=(4.8, 2.7))
    for g, c in ((0.5, BLUE), (0.8, TEAL), (0.9, ACCENT), (0.95, RED)):
        ax.semilogy(n, g ** n, color=c, label=rf"$g={g}$")
        k = np.log(1 / np.e) / np.log(g)
        if k <= 40:
            ax.plot([k], [1 / np.e], "o", ms=3, color=c)
    ax.axhline(1 / np.e, color=GREY, lw=0.8, ls=(0, (4, 3)))
    ax.set_xlabel("散射次数 n")
    ax.set_ylabel(r"$\langle\cos\theta\rangle^n$")
    ax.set_xlim(0, 40)
    ax.set_ylim(1e-3, 1.4)
    ax.legend(fontsize=8, loc="lower left")
    ax.text(2, 0.42, r"$1/e$", fontsize=8, color=GREY)
    save(fig, "fig5-3-memory.png")


if __name__ == "__main__":
    fig5_1()
    fig5_2()
    fig5_3()
