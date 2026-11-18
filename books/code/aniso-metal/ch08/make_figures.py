#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 8 章插图：实时近似的代价。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from anisocommon import *       # noqa: F401,F403


def ab_terms(mu_i, phi_i, ax, ay, nt=480, np_=480):
    """split-sum 的 A、B 两项，见式 (8.3)(8.4)。"""
    wi = sph(np.arccos(np.clip(mu_i, 1e-4, 1.0)), phi_i)
    mu = (np.arange(nt) + 0.5) / nt
    ph = (np.arange(np_) + 0.5) * 2 * np.pi / np_
    M, P = np.meshgrid(mu, ph, indexing="ij")
    Wo = sph(np.arccos(M), P)
    H = normalize(wi[None, None, :] + Wo)
    ch = np.clip(H[..., 2], 1e-4, 1.0)
    phh = np.arctan2(H[..., 1], H[..., 0])
    D = d_aniso(ch, phh, ax, ay)
    G = 1.0 / (1.0 + lambda_smith(wi[2], phi_i, ax, ay) + lambda_smith(M, P, ax, ay))
    f = D * G / (4.0 * wi[2] * M)
    w = np.clip(np.sum(wi[None, None, :] * H, axis=-1), 0, 1)
    s5 = (1.0 - w) ** 5
    dmu = (1.0 / nt) * (2 * np.pi / np_)
    A = float(np.sum(f * (1 - s5) * M) * dmu)
    B = float(np.sum(f * s5 * M) * dmu)
    return A, B


def fig8_1():
    mus = np.linspace(0.06, 0.995, 22)
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.1))
    for a, c in [(0.30, ACCENT), (0.60, BLUE)]:
        A = np.array([ab_terms(m, 0, a, a)[0] for m in mus])
        B = np.array([ab_terms(m, 0, a, a)[1] for m in mus])
        axes[0].plot(mus, A, color=c, label=f"$A$，$a$ = {a:.1f}")
        axes[0].plot(mus, B, color=c, ls="--", label=f"$B$，$a$ = {a:.1f}")
        axes[1].plot(mus, A + B, color=c, label=f"$a$ = {a:.1f}")
        print("a", a, "A+B mu=1:", round(float(A[-1] + B[-1]), 3),
              " mu=0.5:", round(float(np.interp(0.5, mus, A + B)), 3))
    axes[0].set_ylabel("项值")
    axes[0].legend(loc="lower right", fontsize=7.8)
    axes[1].axhline(1.0, color=INK, lw=0.9, ls=":")
    axes[1].set_ylabel("$A+B$")
    axes[1].set_ylim(0.4, 1.05)
    axes[1].legend(loc="lower right", fontsize=7.8)
    for pane in axes:
        pane.set_xlabel("入射方向余弦 $\\mu_i$")
        pane.set_xlim(0, 1)
    axes[0].set_ylim(0, 1.0)
    fig.tight_layout()
    save(fig, "fig8-1-splitsum.png")


def band_width(ax_r, ay_r, mu_i=0.766, th_i=40.0):
    """沿高光带方向的半高全宽（度）。"""
    th = np.radians(th_i)
    ph = np.linspace(np.pi - 1.1, np.pi + 1.1, 3000)
    P = np.full_like(ph, th)
    Wo = sph(P, ph)
    wi = sph(th, 0.0)
    H = normalize(wi[None, :] + Wo)
    ch = np.clip(H[..., 2], 1e-4, 1.0)
    phh = np.arctan2(H[..., 1], H[..., 0])
    D = d_aniso(ch, phh, ax_r, ay_r)
    li = lambda_smith(wi[2], 0.0, ax_r, ay_r)
    lo = lambda_smith(np.clip(np.cos(P), 1e-5, 1.0), P, ax_r, ay_r)
    f = D * (1.0 / (1 + li + lo)) / (4 * wi[2] * np.clip(np.cos(P), 1e-5, 1))
    f = f / f.max()
    idx = np.where(f > 0.5)[0]
    return float(np.degrees(ph[idx[-1]] - ph[idx[0]])), float(np.max(f))


def fig8_2():
    rs = np.array([1, 2, 3, 4, 6, 8, 12, 16])
    a = 0.20
    exact, approx = [], []
    for r in rs:
        ax_ = a / np.sqrt(r)
        ay_ = a * np.sqrt(r)
        w_ex, _ = band_width(ax_, ay_)
        w_ap, _ = band_width(a, a)
        exact.append(w_ex)
        approx.append(w_ap)
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    ax.plot(rs, exact, "o-", color=ACCENT, label="各向异性，精确")
    ax.plot(rs, approx, "s--", color=GREY, label="几何平均替代（各向同性 $a$ = 0.20）")
    ax.set_xlabel("拉伸比 $a_y/a_x$")
    ax.set_ylabel("高光带半高全宽 (度)")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 8, 16])
    ax.set_xticklabels(["1", "2", "4", "8", "16"])
    ax.legend(loc="upper left")
    for r, e, ap in zip(rs, exact, approx):
        print("r", r, "exact", round(e, 1), "approx", round(ap, 1),
              "err", f"{(ap - e) / e * 100:+.0f}%")
    save(fig, "fig8-2-lut-error.png")


def fig8_3():
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    th = np.radians(40.0)
    ph = np.linspace(np.pi - 0.9, np.pi + 0.9, 900)
    wi = sph(th, 0.0)
    for (axr, ayr), c, lab in [((0.05, 0.40), ACCENT, "各向异性 0.05 / 0.40"),
                               ((0.20, 0.20), BLUE, "几何平均 0.20 / 0.20"),
                               ((0.05, 0.05), TEAL, "只用较小的 $a$ = 0.05")]:
        P = np.full_like(ph, th)
        Wo = sph(P, ph)
        H = normalize(wi[None, :] + Wo)
        ch = np.clip(H[..., 2], 1e-4, 1.0)
        phh = np.arctan2(H[..., 1], H[..., 0])
        D = d_aniso(ch, phh, axr, ayr)
        li = lambda_smith(wi[2], 0.0, axr, ayr)
        lo = lambda_smith(np.clip(np.cos(P), 1e-5, 1.0), P, axr, ayr)
        f = D * (1.0 / (1 + li + lo)) / (4 * wi[2] * np.clip(np.cos(P), 1e-5, 1))
        ax.plot(np.degrees(ph - np.pi), f / f.max(), color=c, label=lab)
    ax.set_xlabel("相对镜面方向的方位偏差 (度)")
    ax.set_ylabel("相对强度")
    ax.set_xlim(-50, 50)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper right")
    save(fig, "fig8-3-mobile.png")


if __name__ == "__main__":
    fig8_1()
    fig8_2()
    fig8_3()
