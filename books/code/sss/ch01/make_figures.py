#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 1 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def walk_2d(sigma_a, sigma_s, g, L, rng, max_steps=4000):
    """在二维截面上追一条光子路径，返回 (x, y) 序列。"""
    st = sigma_a + sigma_s
    x, y = 0.0, 0.0
    ang = np.pi / 2.0                      # 朝下
    pts = [(x, y)]
    for _ in range(max_steps):
        s = -np.log(rng.random()) / st
        x += s * np.cos(ang)
        y += s * np.sin(ang)
        pts.append((x, y))
        if y < 0.0 or y > L:
            break
        # HG 散射：相对原方向偏转 dtheta
        ct = hg_sample_cos(g, rng.random())
        dth = np.arccos(np.clip(ct, -1, 1))
        ang += dth if rng.random() < 0.5 else -dth
    return np.array(pts)


def fig1_1():
    """一束光进去，几条路径出来。"""
    rng = np.random.default_rng(7)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.add_patch(plt.Rectangle((-0.2, 0.0), 14.4, 3.0, facecolor="#f4ece2",
                               edgecolor="none", zorder=0))
    ax.axhline(0.0, color="#5b6472", lw=1.2, zorder=1)
    ax.axhline(3.0, color="#5b6472", lw=0.9, ls=(0, (6, 3)), zorder=1)
    ax.text(13.9, 3.08, "背面  z = 3 mm", ha="right", va="bottom", fontsize=8,
            color="#5b6472")
    cols = [ACCENT, BLUE, TEAL, RED, PURPLE, GREEN]
    for i in range(6):
        p = walk_2d(0.002, 8.0, 0.9, 3.0, rng)
        ax.plot(p[:, 0], p[:, 1], color=cols[i], lw=0.85, alpha=0.85, zorder=2)
    ax.annotate("入射", xy=(0.0, -0.08), xytext=(0.55, -0.30), fontsize=8.5,
                color=INK, arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))
    ax.plot([0.0], [-0.06], marker="v", ms=6, color=INK, zorder=3)
    ax.set_xlim(-0.2, 14.2)
    ax.set_ylim(-0.55, 3.35)
    ax.set_xlabel("横向位置 (mm)")
    ax.set_ylabel("深度 (mm)")
    ax.set_yticks([0, 1, 2, 3])
    ax.grid(False)
    save(fig, "fig1-1-paths.png")


def fig1_2():
    """四种材料的径向出射剖面。"""
    mat = [
        ("牛奶", 0.0003, 25.0, 0.9, ACCENT),
        ("蜡", 0.004, 15.0, 0.85, GOLD),
        ("皮肤", 0.030, 10.0, 0.8, RED),
        ("大理石", 0.0008, 6.0, 0.9, BLUE),
    ]
    r = np.geomspace(0.02, 40, 500)
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    for name, ma, ms, g, c in mat:
        rd = rd_dipole(r, ma, ms, g, eta=1.4)
        ax.loglog(r, rd, color=c, label=name)
    ax.set_xlabel("出射点到入射点的距离 r (mm)")
    ax.set_ylabel("R_d(r)  (mm$^{-2}$)")
    ax.set_xlim(0.02, 40)
    ax.set_ylim(1e-6, 10)
    ax.grid(True, which="both", alpha=0.18)
    ax.legend(loc="lower left", ncol=2, handlelength=1.6, columnspacing=1.2)
    # 1/r² 渐近参考线
    ref = 0.03 * (r / 1.0) ** -2
    ax.loglog(r, ref, lw=0.9, ls=(0, (4, 3)), color=GREY)
    ax.text(3.2, 0.03 * 3.2 ** -2 * 2.2, "$1/r^2$", fontsize=8.5, color=GREY)
    save(fig, "fig1-2-profiles.png")


if __name__ == "__main__":
    fig1_1()
    fig1_2()
