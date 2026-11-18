#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 6 章插图：三种工艺的表面统计。

高度场全部由下面写明的公式合成，没有使用实测数据。
"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from anisocommon import *       # noqa: F401,F403

RNG = np.random.default_rng(20261118)


def brushed(nx=1400, dx=0.4, n=28):
    """单向丝纹：h 只随 x 变化，谐波波长对数均匀分布。"""
    x = np.arange(nx) * dx
    lam = np.exp(RNG.uniform(np.log(0.6), np.log(40.0), n))
    amp = 0.012 * lam
    ph = RNG.uniform(0, 2 * np.pi, n)
    h = sum(a * np.sin(2 * np.pi * x / l + p) for a, l, p in zip(amp, lam, ph))
    H = np.tile(h, (nx, 1))
    return H, dx


def sandblasted(n=260, size=520.0, res=520):
    """喷砂：大量随机方向、随机波长的谐波叠加，各向同性。"""
    x = np.linspace(0, size, res)
    X, Y = np.meshgrid(x, x, indexing="ij")
    H = np.zeros_like(X)
    lam = np.exp(RNG.uniform(np.log(1.0), np.log(60.0), n))
    amp = 0.010 * lam
    ang = RNG.uniform(0, np.pi, n)
    ph = RNG.uniform(0, 2 * np.pi, n)
    for a, l, t, p in zip(amp, lam, ang, ph):
        H += a * np.sin(2 * np.pi * (np.cos(t) * X + np.sin(t) * Y) / l + p)
    return H, x[1] - x[0]


def hammered(nd=46, size=2400.0, res=900):
    """锤纹：一批随机位置的圆顶凹坑，半径远大于丝纹尺度。"""
    x = np.linspace(0, size, res)
    X, Y = np.meshgrid(x, x, indexing="ij")
    H = np.zeros_like(X)
    for _ in range(nd):
        cx, cy = RNG.uniform(0, size, 2)
        s = RNG.uniform(70, 190)
        d = RNG.uniform(3, 11)
        H -= d * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * s * s))
    return H, x[1] - x[0]


def slopes(H, dx):
    gy, gx = np.gradient(H, dx)
    return gx.ravel(), gy.ravel()


def fig6_1():
    fig, axes = plt.subplots(3, 1, figsize=(6.4, 4.4), sharex=True)
    specs = [("拉丝（单向丝纹）", brushed, ACCENT),
             ("喷砂（各向同性）", sandblasted, BLUE),
             ("锤纹（低频凹坑）", hammered, TEAL)]
    for ax, (name, fn, c) in zip(axes, specs):
        H, dx = fn()
        n = H.shape[0]
        mid = n // 2
        x = np.arange(n) * dx
        ax.plot(x - x[-1] / 2, H[mid] - H[mid].mean(), color=c, lw=1.0)
        ax.set_ylabel("高度 (μm)", fontsize=8)
        ax.text(0.01, 0.86, name, transform=ax.transAxes, fontsize=8.5, color=c)
        ax.set_xlim(-520, 520)
    axes[-1].set_xlabel("位置 $x$ (μm)")
    fig.tight_layout()
    save(fig, "fig6-1-profiles.png")


def fig6_2():
    """两个方向的斜率边缘分布。"""
    fig, axes = plt.subplots(1, 3, figsize=(6.9, 2.6))
    q = np.linspace(0.005, 0.8, 400)
    for pane, (name, fn) in zip(axes, [("拉丝", brushed), ("喷砂", sandblasted),
                                       ("锤纹", hammered)]):
        H, dx = fn()
        gx, gy = slopes(H, dx)
        for comp, c, lab in [(gx, ACCENT, "$x$ 方向"), (gy, BLUE, "$y$ 方向")]:
            a = np.sort(np.abs(comp))
            surv = 1.0 - np.searchsorted(a, q) / a.size
            pane.semilogy(q, np.maximum(surv, 1e-4), color=c, lw=1.6, label=lab)
        pane.set_title(name, fontsize=9)
        pane.set_xlabel("$|m|$（斜率绝对值）", fontsize=8.5)
        pane.set_xlim(0, 0.8)
        pane.set_ylim(1e-4, 1.2)
    axes[0].set_ylabel("$P(|m|>q)$")
    axes[0].annotate("$y$ 方向的坡度在 0.01 处落到零", xy=(0.015, 0.004), xytext=(0.26, 2.5e-4),
                     fontsize=7.6, color="#3c4654",
                     arrowprops=dict(arrowstyle="->", lw=0.7, color=GREY))
    axes[0].legend(fontsize=7.6, loc="upper right")
    fig.tight_layout()
    save(fig, "fig6-2-marginals.png")


def fig6_3():
    """patch 平均斜率：衡量法线的空间相关长度。"""
    fig, axes = plt.subplots(1, 3, figsize=(6.9, 2.7))
    for pane, (name, fn) in zip(axes, [("拉丝", brushed), ("喷砂", sandblasted),
                                       ("锤纹", hammered)]):
        H, dx = fn()
        gx, gy = slopes(H, dx)
        n = H.shape[0]
        g = gx.reshape(n, n)
        m = 40
        k = n // m
        coarse = g[:k * m, :k * m].reshape(k, m, k, m).mean(axis=(1, 3))
        im = pane.imshow(coarse, cmap="RdBu_r", vmin=-0.06, vmax=0.06)
        pane.set_xticks([])
        pane.set_yticks([])
        pane.grid(False)
        pane.set_title(f"{name}，patch = {m * dx:.0f} μm", fontsize=8.5)
        print(name, "patch mean slope std =", round(float(np.std(coarse)), 4))
    fig.colorbar(im, ax=axes, pad=0.015, fraction=0.03).set_label("patch 平均斜率 $\\bar{m}_x$",
                                                                 fontsize=8)
    save(fig, "fig6-3-patch-mean.png")


if __name__ == "__main__":
    fig6_1()
    fig6_2()
    fig6_3()
