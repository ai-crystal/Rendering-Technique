#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 5 章插图：各向异性下的多次散射补偿。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from anisocommon import *       # noqa: F401,F403

MUS = np.linspace(0.10, 0.995, 24)
PHIS = np.linspace(0, 2 * np.pi, 9)[:-1]


def e_curve(ax, ay, phi, mus=MUS):
    return np.array([directional_albedo(m, phi, ax, ay) for m in mus])


def e_avg_hemi(ax, ay, mus=MUS, phis=PHIS):
    """半球平均：E_avg = (1/π) ∫∫ E(μ,φ) μ dμ dφ。"""
    tot = 0.0
    for p in phis:
        e = e_curve(ax, ay, p, mus)
        tot += e_avg(mus, e)
    return tot / len(phis)


def fig5_1():
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    e = e_curve(0.30, 0.30, 0.0)
    ax.plot(MUS, e, color=GREY, ls="--", label="各向同性，$a$ = 0.30")
    e0 = e_curve(0.05, 0.80, 0.0)
    e9 = e_curve(0.05, 0.80, np.pi / 2)
    ax.plot(MUS, e0, color=ACCENT, label="各向异性，$\\phi$ = 0")
    ax.plot(MUS, e9, color=BLUE, label="各向异性，$\\phi$ = 90°")
    ax.set_xlabel("入射方向余弦 $\\mu_i$")
    ax.set_ylabel("单次散射方向反照率 $E$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.5, 1.02)
    ax.legend(loc="lower right")
    save(fig, "fig5-1-E-curves.png")


def fig5_2():
    """补偿项把能量补成一层很宽很低的底。"""
    ax_r, ay_r = 0.05, 0.80
    mus = np.linspace(0.10, 0.995, 24)
    e = e_curve(ax_r, ay_r, 0.0, mus)
    eav = e_avg_hemi(ax_r, ay_r, mus, PHIS)
    wi = sph(np.radians(45.0), 0.0)
    ths = np.linspace(np.radians(2), np.radians(88), 600)
    phis = np.full_like(ths, np.pi)
    Wo = sph(ths, phis)
    H = normalize(wi[None, :] + Wo)
    ch = np.clip(H[..., 2], 1e-4, 1.0)
    ph = np.arctan2(H[..., 1], H[..., 0])
    D = d_aniso(ch, ph, ax_r, ay_r)
    li = lambda_smith(wi[2], 0.0, ax_r, ay_r)
    lo = lambda_smith(np.clip(np.cos(ths), 1e-5, 1.0), phis, ax_r, ay_r)
    G = 1.0 / (1.0 + li + lo)
    single = D * G / (4.0 * wi[2] * np.clip(np.cos(ths), 1e-5, 1.0))
    ei = float(np.interp(wi[2], mus, e))
    eo = np.interp(np.cos(ths), mus, e)
    ms = (1 - ei) * (1 - eo) / (np.pi * (1 - eav))
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.semilogy(np.degrees(ths), single, color=ACCENT, label="单次散射 $f_{ss}$")
    ax.semilogy(np.degrees(ths), single + ms, color=TEAL, label="$f_{ss}+f_{ms}$")
    ax.semilogy(np.degrees(ths), ms, color=GREY, ls=":", label="补偿项 $f_{ms}$")
    ax.set_xlabel("出射天顶角 $\\theta_o$ (度)，$\\phi_o$ = 180°")
    ax.set_ylabel("$f_r$  ($\\mathrm{sr^{-1}}$)")
    ax.set_xlim(0, 88)
    ax.set_ylim(1e-4, 30)
    ax.legend(loc="lower left")
    print("E_i(45deg) =", round(ei, 3), " E_avg =", round(eav, 3))
    save(fig, "fig5-3-ms-pedestal.png")


def fig5_3():
    a = 0.20
    rs = np.array([1, 1.5, 2, 3, 4, 6, 8, 12, 16])
    vals = []
    for r in rs:
        ax_ = a / np.sqrt(r)
        ay_ = a * np.sqrt(r)
        vals.append(e_avg_hemi(ax_, ay_))
        print("r", r, "ax", round(ax_, 3), "ay", round(ay_, 3), "Eavg", round(vals[-1], 4))
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    ax.plot(rs, vals, "o-", color=PURPLE, ms=5)
    ax.axhline(vals[0], color=GREY, ls="--", lw=1.0)
    ax.annotate(f"各向同性 {vals[0]:.3f}", (rs[0], vals[0]), xytext=(2.2, vals[0] + 0.012),
                fontsize=8, color="#3c4654")
    ax.set_xlabel("拉伸比 $a_y/a_x$（几何平均 $\\sqrt{a_xa_y}$ = 0.20）")
    ax.set_ylabel("半球平均反照率 $E_{avg}$")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 8, 16])
    ax.set_xticklabels(["1", "2", "4", "8", "16"])
    ax.set_ylim(0.60, 0.93)
    save(fig, "fig5-2-eavg-vs-stretch.png")


if __name__ == "__main__":
    fig5_1()
    fig5_2()
    fig5_3()
