#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 4 章插图：切线空间与拉伸的高光。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from anisocommon import *       # noqa: F401,F403

WI = sph(np.radians(40.0), 0.0)


def fmap(TH, PH, wi, ax, ay, f0=1.0):
    Wo = sph(TH, PH)
    H = normalize(wi[None, None, :] + Wo)
    ch = np.clip(H[..., 2], 1e-4, 1.0)
    ph = np.arctan2(H[..., 1], H[..., 0])
    D = d_aniso(ch, ph, ax, ay)
    ci = wi[2]
    li = lambda_smith(ci, 0.0, ax, ay)
    lo = lambda_smith(np.clip(np.cos(TH), 1e-5, 1.0), PH, ax, ay)
    G = 1.0 / (1.0 + li + lo)
    F = fresnel_schlick(np.clip(np.sum(wi * H, axis=-1), 0, 1), f0)
    return F * D * G / (4.0 * ci * np.clip(np.cos(TH), 1e-5, 1.0))


def fig4_1():
    th = np.linspace(0.5, 80, 320) * np.pi / 180
    ph = np.linspace(0, 2 * np.pi, 480)
    T, P = np.meshgrid(th, ph, indexing="ij")
    F = fmap(T, P, WI, 0.05, 0.40)
    vmax = float(F.max())
    F[th < np.radians(6.0), :] = np.nan
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    pc = ax.pcolormesh(np.degrees(T) * np.cos(P), np.degrees(T) * np.sin(P), F,
                       cmap="inferno", shading="auto", vmin=0, vmax=vmax * 0.9)
    ax.set_aspect("equal")
    ax.set_facecolor("black")
    ax.set_xlabel("$\\theta_o\\cos\\phi_o$ (度)")
    ax.set_ylabel("$\\theta_o\\sin\\phi_o$ (度)")
    ax.set_xlim(-82, 82)
    ax.set_ylim(-82, 82)
    ax.grid(False)
    ax.plot([-40], [0], "o", ms=8, mfc="none", mec="white", mew=1.4)
    ax.annotate("镜面方向", (-40, 0), xytext=(-12, 30), color="white", fontsize=8,
                arrowprops=dict(arrowstyle="->", color="white", lw=0.8))
    cb = fig.colorbar(pc, ax=ax, pad=0.02)
    cb.set_label("$f_r$（归一化后）")
    save(fig, "fig4-1-lobe-map.png")


def fig4_2():
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.0))
    th = np.radians(40.0)
    # 沿 φ 的剖面（θ 固定在镜面方向）
    ph = np.linspace(np.pi - 0.9, np.pi + 0.9, 500)
    P = np.full_like(ph, th)
    a = fmap(P, ph, WI, 0.05, 0.40)
    a = np.ravel(a)
    axes[0].plot(np.degrees(ph - np.pi), a / a.max(), color=ACCENT)
    axes[0].set_xlabel("相对镜面方向的方位偏差 (度)")
    axes[0].set_ylabel("相对强度")
    axes[0].set_title("沿高光带方向", fontsize=9)
    axes[0].set_xlim(-50, 50)
    # 沿 θ 的剖面（φ 固定在 180）
    ths = np.linspace(np.radians(5), np.radians(80), 500)
    T2 = ths
    P2 = np.full_like(ths, np.pi)
    b = fmap(T2, P2, WI, 0.05, 0.40)
    b = np.ravel(b)
    axes[1].plot(np.degrees(ths - th), b / b.max(), color=BLUE)
    axes[1].set_xlabel("相对镜面方向的天顶偏差 (度)")
    axes[1].set_title("垂直高光带方向", fontsize=9)
    axes[1].set_xlim(-50, 50)
    for x in axes:
        x.set_ylim(0, 1.08)
    axes[1].legend(["$a_x$ = 0.05，$a_y$ = 0.40"], fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, "fig4-2-cuts.png")


def fig4_3():
    th = np.linspace(0.5, 80, 260) * np.pi / 180
    ph = np.linspace(0, 2 * np.pi, 400)
    T, P = np.meshgrid(th, ph, indexing="ij")
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.9))
    for pane, (axr, ayr) in zip(axes, [(0.05, 0.40), (0.40, 0.05)]):
        F = fmap(T, P, WI, axr, ayr)
        vmax = float(F.max())
        F[th < np.radians(6.0), :] = np.nan
        pane.pcolormesh(np.degrees(T) * np.cos(P), np.degrees(T) * np.sin(P), F,
                        cmap="inferno", shading="auto", vmin=0, vmax=vmax * 0.9)
        pane.set_aspect("equal")
        pane.set_facecolor("black")
        pane.set_xlim(-82, 82)
        pane.set_ylim(-82, 82)
        pane.set_xticks([-50, 0, 50])
        pane.set_yticks([-50, 0, 50])
        pane.grid(False)
        pane.set_xlabel("$\\theta_o\\cos\\phi_o$ (度)", fontsize=8.5)
        pane.set_title(f"$a_x$ = {axr:.2f}, $a_y$ = {ayr:.2f}", fontsize=9)
    axes[0].set_ylabel("$\\theta_o\\sin\\phi_o$ (度)")
    fig.tight_layout()
    save(fig, "fig4-3-swap.png")


if __name__ == "__main__":
    fig4_1()
    fig4_2()
    fig4_3()
