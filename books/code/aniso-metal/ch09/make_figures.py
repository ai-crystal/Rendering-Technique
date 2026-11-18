#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 9 章插图：白炉、互易性与补偿残差。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from anisocommon import *       # noqa: F401,F403

MUS = np.linspace(0.10, 0.995, 24)


def compensated(mu_i, phi_i, ax, ay, mus=MUS):
    """用真实二维 E 做补偿，返回总反照率（应接近 1）。"""
    e = np.array([directional_albedo(m, phi_i, ax, ay) for m in mus])
    nt, np_ = 400, 360
    mu = (np.arange(nt) + 0.5) / nt
    ph = (np.arange(np_) + 0.5) * 2 * np.pi / np_
    M, P = np.meshgrid(mu, ph, indexing="ij")
    eo = np.interp(M, mus, e)
    eav = float(2.0 * np.sum(eo[:, 0] * mu) / nt)      # 与积分用同一套网格
    ei = float(np.interp(mu_i, mus, e))
    fms = (1 - ei) * (1 - eo) / (np.pi * (1 - eav))
    return ei + float(np.sum(fms * M) * (1 / nt) * (2 * np.pi / np_))


def fig9_1():
    ax_r, ay_r = 0.05, 0.80
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for phi, c, lab in [(0.0, ACCENT, "$\\phi$ = 0"), (np.pi / 2, BLUE, "$\\phi$ = 90°")]:
        single = np.array([directional_albedo(m, phi, ax_r, ay_r) for m in MUS])
        total = np.array([compensated(m, phi, ax_r, ay_r) for m in MUS])
        ax.plot(MUS, single, color=c, ls="--", label=f"单次散射，{lab}")
        ax.plot(MUS, total, color=c, label=f"补偿后，{lab}")
        print(lab, "补偿后残差", round(float(np.max(np.abs(total - 1))), 4))
    ax.axhline(1.0, color=INK, lw=0.9, ls=":")
    ax.set_xlabel("入射方向余弦 $\\mu_i$")
    ax.set_ylabel("方向反照率")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.55, 1.06)
    ax.legend(loc="lower right", fontsize=7.8, ncol=2)
    save(fig, "fig9-1-white-furnace.png")


def brdf_pair(wi, wo, ax, ay, wrong=False):
    h = normalize(wi + wo)
    ci, co = max(wi[2], 1e-5), max(wo[2], 1e-5)
    ch = max(h[2], 1e-4)
    ph = np.arctan2(h[1], h[0])
    D = float(d_aniso(ch, ph, ax, ay))
    G = float(g2(ci, np.arctan2(wi[1], wi[0]), co, np.arctan2(wo[1], wo[0]), ax, ay))
    ang = float(np.dot(wi, h))
    F = float(fresnel_schlick(np.clip(ang, 0, 1), 0.9))
    den = 4 * ci * (co ** 2 if wrong else co)
    return F * D * G / den


def fig9_2():
    rng = np.random.default_rng(7)
    ax_r, ay_r = 0.12, 0.45
    n = 1200
    th_i = np.arccos(rng.uniform(0.15, 0.99, n))
    th_o = np.arccos(rng.uniform(0.15, 0.99, n))
    ph_i = rng.uniform(0, 2 * np.pi, n)
    ph_o = rng.uniform(0, 2 * np.pi, n)
    fig, ax = plt.subplots(figsize=(5.8, 3.9))
    for wrong, c, lab in [(False, TEAL, "正确：用 $\\omega\\cdot h$"),
                          (True, RED, "错误：分母写成 $4\\cos\\theta_i\\cos^2\\theta_o$")]:
        a, b = [], []
        for i in range(n):
            wi = sph(th_i[i], ph_i[i])
            wo = sph(th_o[i], ph_o[i])
            a.append(brdf_pair(wi, wo, ax_r, ay_r, wrong))
            b.append(brdf_pair(wo, wi, ax_r, ay_r, wrong))
        a, b = np.array(a), np.array(b)
        ok = (a > 1e-6) & (b > 1e-6)
        ax.loglog(a[ok], b[ok], ".", ms=2.2, color=c, alpha=0.5, label=lab)
        err = np.median(np.abs(np.log10(b[ok] / a[ok])))
        print(lab, " 中位相对偏差(10^x):", round(float(err), 4))
    lo, hi = 1e-3, 1e4
    ax.plot([lo, hi], [lo, hi], color=INK, lw=0.8, ls=":")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel("$f_r(\\omega_i\\to\\omega_o)$")
    ax.set_ylabel("$f_r(\\omega_o\\to\\omega_i)$")
    ax.legend(loc="upper left", fontsize=7.8)
    save(fig, "fig9-2-reciprocity.png")


def fig9_3():
    axs = np.array([0.05, 0.08, 0.12, 0.20, 0.35])
    ays = np.array([0.05, 0.10, 0.20, 0.40, 0.80])
    mu_i = 0.707
    R = np.zeros((len(axs), len(ays)))
    for i, a_x in enumerate(axs):
        for j, a_y in enumerate(ays):
            e_true = np.array([directional_albedo(m, 0.0, a_x, a_y) for m in MUS])
            ei = float(np.interp(mu_i, MUS, e_true))
            g = np.sqrt(a_x * a_y)
            e1 = np.array([directional_albedo(m, 0.0, g, g) for m in MUS])
            eav = e_avg(MUS, e1)
            e1i = float(np.interp(mu_i, MUS, e1))
            nt, np_ = 300, 200
            mu = (np.arange(nt) + 0.5) / nt
            ph = (np.arange(np_) + 0.5) * 2 * np.pi / np_
            M, P = np.meshgrid(mu, ph, indexing="ij")
            eo = np.interp(M, MUS, e1)
            fms = (1 - e1i) * (1 - eo) / (np.pi * (1 - eav))
            R[i, j] = ei + float(np.sum(fms * M) * (1 / nt) * (2 * np.pi / np_)) - 1.0
    print(np.round(R, 3))
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    im = ax.imshow(R, origin="lower", cmap="RdBu_r", vmin=-0.12, vmax=0.12,
                   extent=[0, len(ays), 0, len(axs)], aspect="auto")
    ax.set_xticks(np.arange(len(ays)) + 0.5)
    ax.set_xticklabels([f"{v:.2f}" for v in ays])
    ax.set_yticks(np.arange(len(axs)) + 0.5)
    ax.set_yticklabels([f"{v:.2f}" for v in axs])
    ax.grid(False)
    ax.set_xlabel("$a_y$")
    ax.set_ylabel("$a_x$")
    for i in range(len(axs)):
        for j in range(len(ays)):
            ax.text(j + 0.5, i + 0.5, f"{R[i, j] * 100:+.0f}%", ha="center", va="center",
                    fontsize=7.2, color="black")
    fig.colorbar(im, ax=ax, pad=0.02).set_label("反照率残差", fontsize=8)
    save(fig, "fig9-3-residual-map.png")


if __name__ == "__main__":
    fig9_1()
    fig9_2()
    fig9_3()
