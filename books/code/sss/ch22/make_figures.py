#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 22 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403
from scipy.optimize import nnls


def fig22_1():
    ma, ms, g = 0.02, 10.0, 0.8
    r = np.linspace(0.05, 3.0, 400)
    rd = rd_dipole(r, ma, ms, g, 1.4)
    sigmas = np.array([0.06, 0.15, 0.4, 1.1])
    A = np.stack([np.exp(-r ** 2 / (2 * s ** 2)) / (2 * np.pi * s ** 2)
                  for s in sigmas], axis=1)
    w, _ = nnls(A, rd)
    fit = A @ w
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.loglog(r, rd, color=ACCENT, label="偶极子剖面")
    ax.loglog(r, fit, color=TEAL, ls=(0, (5, 2)), label="4 个高斯之和")
    for s, wi in zip(sigmas, w):
        ax.loglog(r, wi * np.exp(-r ** 2 / (2 * s ** 2)) / (2 * np.pi * s ** 2),
                  color=GREY, lw=0.8, alpha=0.7)
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$R_d(r)$  (mm$^{-2}$)")
    ax.set_xlim(0.05, 3.0)
    ax.set_ylim(1e-3, 1.5)
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.16)
    print("weights", np.round(w, 4))
    print("max rel err", round(float(np.max(np.abs(fit - rd) / rd)), 3),
          "mean", round(float(np.mean(np.abs(fit - rd) / rd)), 3))
    save(fig, "fig22-1-gaussians.png")


def fig22_2():
    """能量积分随积分半径的饱和。"""
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    ms = 2.0 / (1 - 0.8)
    R = np.geomspace(0.02, 60, 600)
    for ap, c in ((0.999, RED), (0.95, ACCENT), (0.7, TEAL)):
        ma = ms * (1 - 0.8) * (1 - ap) / ap
        rd = rd_dipole(R, ma, ms, 0.8, 1.0)
        inc = 2 * np.pi * R * rd
        cum = np.cumsum(0.5 * (inc[1:] + inc[:-1]) * np.diff(R))
        cum = np.concatenate([[0], cum])
        tot = cum[-1]
        ax.semilogx(R, cum / tot, color=c, label=rf"$\alpha'={ap}$")
        r90 = float(np.interp(0.9, cum / tot, R))
        ax.axvline(r90, color=c, lw=0.7, ls=(0, (3, 2)), alpha=0.7)
        print(ap, "r90", round(r90, 2))
    ax.set_xlabel("积分半径 R (mm)")
    ax.set_ylabel("累积反射率 / 总反射率")
    ax.set_xlim(0.02, 60)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(True, which="both", alpha=0.16)
    ax.text(0.035, 0.93, "虚线：90% 的反射率已计入", fontsize=7.5, color=GREY)
    save(fig, "fig22-2-furnace.png")


if __name__ == "__main__":
    fig22_1()
    fig22_2()
