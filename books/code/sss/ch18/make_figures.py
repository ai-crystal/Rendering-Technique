#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 18 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def _mc_oblique(theta_in, ma, ms, g, n=200000, seed=71):
    d = mc_slab(ma, ms, g, n_photons=n, max_events=3000,
                rng=np.random.default_rng(seed), full=True,
                incident=[np.sin(theta_in), 0.0, np.cos(theta_in)])
    m = d["kind"] == 0
    return d["x"][m], d["y"][m]


def fig18_1():
    ma, ms, g = 0.02, 10.0, 0.8
    th = np.deg2rad(40.0)
    x, y = _mc_oblique(th, ma, ms, g)
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.2))
    ax = axes[0]
    r = np.linspace(0.02, 4, 200)
    ax.contour(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200),
               np.zeros((200, 200)), levels=[0], colors="none")
    # 同心圆等值线（偶极子）
    for rr, c in ((0.2, 0.95), (0.5, 0.6), (0.9, 0.28)):
        ax.add_patch(plt.Circle((0, 0), rr, fill=False, color=ACCENT, lw=1.1,
                                alpha=c))
    ax.plot([0], [0], "+", ms=9, color=INK, mew=1.4)
    ax.annotate("", xy=(0.9 * np.sin(th), 0.9 * np.cos(th) * 0 + 0.9 * 0),
                xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=GREY,
                                               lw=0.9))
    ax.text(0.15, 0.55, r"$\theta'$", fontsize=9, color=GREY)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.set_title("偶极子：同心圆", fontsize=9)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.grid(False)

    ax = axes[1]
    h = ax.hist2d(x, y, bins=90, range=[[-1.5, 1.5], [-1.5, 1.5]],
                  cmap="YlGnBu", norm=matplotlib.colors.LogNorm())
    ax.set_aspect("equal")
    ax.set_title("蒙特卡洛：偏心", fontsize=9)
    ax.set_xlabel("x (mm)")
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlim(-1.5, 1.5)
    ax.grid(False)
    ax.plot([0], [0], "+", ms=9, color=RED, mew=1.4)
    ax.plot([np.mean(x)], [np.mean(y)], "o", ms=5, color="white", mec=RED)
    ax.axvline(0, color="white", lw=0.7, ls=(0, (4, 3)))
    ax.annotate("入射点", xy=(0, 0), xytext=(-1.35, 1.15), fontsize=8, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=0.7))
    ax.text(0.12, -1.32, "白圈：出射分布的重心", fontsize=7.5, color=INK)
    fig.subplots_adjust(wspace=0.26)
    save(fig, "fig18-1-spot.png")


def fig18_2():
    ma, ms, g = 0.02, 10.0, 0.8
    zr = 1.0 / sigma_tr(ma, ms, g)
    ths = np.array([0, 10, 20, 30, 40, 50])
    shifts, est = [], []
    for t in ths:
        tt = np.deg2rad(t)
        x, y = _mc_oblique(tt, ma, ms, g, n=120000, seed=80 + t)
        shifts.append(float(np.mean(x)))
        est.append(np.tan(tt))
    fig, ax = plt.subplots(figsize=(5.0, 2.8))
    ax.plot(ths, np.array(shifts) / zr, "o-", color=ACCENT, ms=4,
            label="蒙特卡洛")
    ax.plot(ths, est, color=GREY, ls=(0, (4, 3)), label=r"$z_r\tan\theta'$")
    ax.set_xlabel(r"折射后的入射角 $\theta'$ (度)")
    ax.set_ylabel(r"偏移 $/z_r$")
    ax.set_xlim(0, 52)
    ax.set_ylim(0, 1.4)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.2)
    print(list(zip(ths, np.round(np.array(shifts) / zr, 3))))
    save(fig, "fig18-2-shift.png")


if __name__ == "__main__":
    fig18_1()
    fig18_2()
