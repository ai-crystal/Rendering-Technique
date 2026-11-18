#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 16 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def fig16_1():
    """镜像序列。"""
    ma, ms, g, eta = 0.02, 10.0, 0.8, 1.4
    zb = zb_extrapolation(ma, ms, g, eta)
    zr = 1.0 / sigma_tr(ma, ms, g)
    L = 2.4
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    ax.add_patch(plt.Rectangle((0, 0), 6.4, L, facecolor="#f0e6da",
                               edgecolor="none", zorder=0))
    ax.axhline(0, color=INK, lw=1.4)
    ax.axhline(L, color=INK, lw=1.4)
    ax.axhline(-zb, color=RED, lw=0.9, ls=(0, (5, 3)))
    ax.axhline(L + zb, color=RED, lw=0.9, ls=(0, (5, 3)))
    ax.text(6.35, -zb - 0.28, r"$-z_b$", fontsize=9, color=RED, ha="right")
    ax.text(6.35, L + zb + 0.10, r"$L+z_b$", fontsize=9, color=RED, ha="right")
    P = 2 * (L + 2 * zb)
    for i in (-2, -1, 0, 1, 2):
        for z, sgn in ((i * P + zr, 1), (i * P - zr - 2 * zb, -1)):
            if -zb - 0.4 < z < L + zb + 0.4:
                ax.plot([3.2], [z], "o", ms=7,
                        color=ACCENT if sgn > 0 else BLUE,
                        mfc=ACCENT if sgn > 0 else "white", zorder=4)
    ax.annotate("", xy=(1.0, 0), xytext=(1.0, L),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=0.8,
                                mutation_scale=6))
    ax.text(0.85, L / 2, r"$L$", fontsize=9, ha="right")
    ax.text(0.15, -zb - 0.30, "上外推平面", fontsize=8, color=RED)
    ax.text(0.15, L + zb + 0.10, "下外推平面", fontsize=8, color=RED)
    ax.text(3.55, L + zb + 0.10, "周期 $2(L+2z_b)$", fontsize=8.5, color=GREY)
    ax.set_xlim(0, 6.4)
    ax.set_ylim(-zb - 0.7, L + zb + 0.7)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_ylabel("深度")
    ax.set_title("介质（上）与外部（上下两端）", fontsize=9)
    ax.grid(False)
    save(fig, "fig16-1-images.png")


def fig16_2():
    """Donner 表的柱状图。"""
    labels = [r"$2$ mfp", r"$10$ mfp", r"$20$ mfp"]
    mc_r = [51.6, 83.4, 89.0]
    mp_r = [49.8, 83.8, 89.0]
    dp_r = [90.2, 90.2, 90.2]
    mc_t = [49.8, 13.8, 6.0]
    mp_t = [48.1, 13.8, 5.9]
    dp_t = [26.5, 3.0, 3.0]
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    x = np.arange(3)
    w = 0.13
    for j, (vals, c, name) in enumerate((
            (mc_r, ACCENT, "蒙特卡洛·反射"),
            (mp_r, TEAL, "多极子·反射"),
            (dp_r, BLUE, "偶极子·反射"))):
        ax.bar(x + (j - 1) * w, vals, w, color=c, label=name, edgecolor="white",
               lw=0.6)
    for j, (vals, c, name) in enumerate((
            (mc_t, ACCENT, "蒙特卡洛·透射"),
            (mp_t, TEAL, "多极子·透射"),
            (dp_t, BLUE, "偶极子·透射"))):
        ax.bar(x + (j + 2) * w, vals, w, color=c, alpha=0.45, label=name,
               edgecolor="white", lw=0.6, hatch="///")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("百分比 (%)")
    ax.set_ylim(0, 105)
    ax.legend(fontsize=7, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, 1.16), columnspacing=1.0, handlelength=1.2)
    ax.grid(axis="x", visible=False)
    ax.text(0.02, 96, "实心：反射", fontsize=7.5, color=GREY)
    ax.text(0.02, 89, "斜线：透射", fontsize=7.5, color=GREY)
    save(fig, "fig16-2-table.png")


def fig16_3():
    """透射光斑剖面。"""
    ma, ms, g = 0.002, 10.0, 0.8
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    for L, c, lab in ((0.3, ACCENT, r"$L=0.3$ mm"), (2.0, BLUE, r"$L=2$ mm")):
        d = mc_slab(ma, ms, g, L=L, n_photons=120000, max_events=3000,
                    rng=np.random.default_rng(41), full=True)
        m = d["kind"] == 1
        r = d["r"][m]
        edges = np.linspace(0, 4, 60)
        area = np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
        rc = 0.5 * (edges[:-1] + edges[1:])
        cnt, _ = np.histogram(r, bins=edges)
        ax.semilogy(rc, cnt / (d["r"].size * area), color=c, label=lab)
        print(lab, "T =", round(float(np.mean(d["kind"] == 1)), 3))
    ax.set_xlabel("距离 r (mm)")
    ax.set_ylabel(r"$T_d(r)$  (mm$^{-2}$)")
    ax.set_xlim(0, 4)
    ax.set_ylim(1e-5, 5)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig16-3-transmission.png")


if __name__ == "__main__":
    fig16_1()
    fig16_2()
    fig16_3()
