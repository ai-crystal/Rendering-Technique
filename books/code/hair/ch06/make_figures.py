#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 6 章插图：CDF 采样、联合分布校验、方差对比。"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import *
import hairlib as H

ETA = 1.55
BETA = 0.18
SPREAD = 0.06


def fig_cdf():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
    ax = axes[0]
    edges, cdf = H.cdf_phi(2, bins=361)
    ax.plot(np.degrees(edges), cdf, color=RED, lw=1.8, label="累积分布")
    ax.plot(np.degrees(edges), edges / (2 * np.pi) + 0.5, color=BLUE, lw=1.2,
            ls=(0, (4, 3)), label="均匀分布")
    for u in [0.25, 0.5, 0.75]:
        i = np.searchsorted(cdf, u)
        ax.plot([np.degrees(edges[i])] * 2, [0, u], color=GREY, lw=0.8, ls=":")
        ax.plot([-180, np.degrees(edges[i])], [u, u], color=GREY, lw=0.8, ls=":")
    ax.set_xlim(-40, 40)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("方位角（度）")
    ax.set_ylabel("累积概率")
    ax.legend(loc="lower right", fontsize=8, handlelength=1.6)
    panel_label(ax, "（a）", x=-0.15, y=1.02)

    ax = axes[1]
    rng = np.random.default_rng(7)
    n = 40000
    s = H.sample_phi(2, rng.random(n), bins=361)
    hgt, e = np.histogram(s, bins=120, range=(-np.pi, np.pi), density=True)
    ctr = np.degrees(0.5 * (e[1:] + e[:-1]))
    ax.bar(ctr, hgt, width=np.degrees(e[1] - e[0]) * 0.9, color=RED, alpha=0.35,
           lw=0, label="采样直方图")
    cc, dd = H.azimuth_density(2, bins=361)
    ax.plot(np.degrees(cc), dd, color=RED, lw=1.5, label="解析密度")
    ax.set_xlim(-40, 40)
    ax.set_xlabel("方位角（度）")
    ax.set_ylabel("密度（每弧度）")
    ax.legend(loc="lower left", fontsize=8, handlelength=1.6)
    panel_label(ax, "（b）", x=-0.15, y=1.02)
    fig.tight_layout()
    save(fig, "fig6-1-cdf.png")


def fig_joint():
    rng = np.random.default_rng(11)
    n = 60000
    ti = -0.5
    phi = H.sample_phi(2, rng.random(n), bins=361)
    tho = H.sample_theta(ti, 2, beta=BETA, spread=SPREAD,
                         u1=rng.random(n), u2=rng.random(n))
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    ax.hist2d(np.degrees(phi), np.degrees(tho), bins=[60, 60],
              range=[[-32, 32], [-10, 70]], cmap="YlOrBr", cmin=1)
    P = np.linspace(-0.56, 0.56, 200)
    T = np.linspace(-0.17, 1.22, 200)
    PP, TT = np.meshgrid(P, T)
    Z = H.pdf_phi(2, PP, bins=361) * H.n_p(ti, TT, 2, beta=BETA, spread=SPREAD)
    Z = Z / Z.max()
    ax.contour(np.degrees(PP), np.degrees(TT), Z, levels=[0.2, 0.5, 0.8],
               colors="#33393f", linewidths=0.7)
    ax.set_xlim(-32, 32)
    ax.set_ylim(-10, 70)
    ax.set_xlabel(r"$\varphi$（度）")
    ax.set_ylabel(r"$\theta_o$（度）")
    ax.text(-30, 64, "灰线：解析 pdf 的等值线", fontsize=7.5, color="#33393f")
    fig.tight_layout()
    save(fig, "fig6-2-joint.png")


def fig_variance():
    rng = np.random.default_rng(3)
    ti = -0.5
    cc, dd = H.azimuth_density(2, bins=361)
    edges, cdf = H.cdf_phi(2, bins=361)
    area = 2 * np.pi * 2.8

    def pdf_phi_local(x):
        return np.interp(x, cc, dd, left=0.0, right=0.0)

    def f_cos(phi, tho):
        return pdf_phi_local(phi) * H.n_p(ti, tho, 2, beta=BETA, spread=SPREAD)             * np.cos(tho)

    Ns = [16, 32, 64, 128, 256, 512]
    trials = 200
    rel_u, rel_i, mean_val = [], [], None
    for N in Ns:
        est_u, est_i = [], []
        for _ in range(trials):
            pu = rng.uniform(-np.pi, np.pi, N)
            tu = rng.uniform(-1.4, 1.4, N)
            est_u.append(f_cos(pu, tu).mean() * area)
            pi_ = np.interp(rng.random(N), cdf, edges)
            ti_ = H.sample_theta(ti, 2, beta=BETA, spread=SPREAD,
                                 u1=rng.random(N), u2=rng.random(N))
            est_i.append(np.cos(ti_).mean())
        rel_u.append(np.std(est_u) / abs(np.mean(est_u)))
        rel_i.append(np.std(est_i) / abs(np.mean(est_i)))
        mean_val = np.mean(est_u)

    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.loglog(Ns, rel_u, "o-", color=BLUE, lw=1.5, ms=4, label="均匀采样")
    ax.loglog(Ns, rel_i, "o-", color=ACCENT, lw=1.5, ms=4, label="重要性采样")
    ref = rel_i[0] * np.sqrt(Ns[0] / np.array(Ns, dtype=float))
    ax.loglog(Ns, ref, color=GREY, lw=1.0, ls=(0, (4, 3)), label=r"$1/\sqrt{N}$")
    from matplotlib.ticker import NullFormatter
    ax.set_xticks([16, 64, 256])
    ax.set_xticklabels(["16", "64", "256"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_xlim(12, 640)
    ax.set_xlabel("每像素样本数 $N$")
    ax.set_ylabel("估计值的相对标准差")
    ax.legend(loc="lower left", fontsize=8, handlelength=1.6)
    fig.tight_layout()
    save(fig, "fig6-3-variance.png")


if __name__ == "__main__":
    fig_cdf()
    fig_joint()
    fig_variance()
