#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 21 章插图。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from ssscommon import *         # noqa: F401,F403


def melanin(wl_nm, frac=0.02):
    """黑色素吸收，Jacques 2013 的幂律拟合（lambda 以 nm 计，返回 1/mm）。"""
    return frac * 6.6e11 * np.asarray(wl_nm, float) ** -3.33 / 10.0


def haemoglobin(wl_nm, frac=0.02):
    """血红蛋白吸收的双高斯带模型（中心 542 与 577 nm），仅用于展示形状。"""
    wl = np.asarray(wl_nm, float)
    band = np.exp(-((wl - 542) ** 2) / (2 * 28 ** 2)) \
        + 0.75 * np.exp(-((wl - 577) ** 2) / (2 * 22 ** 2))
    return frac * 4.0 * band


def fig21_1():
    layers = [("角质层", 0.015, "#e8d9c8"), ("表皮", 0.08, "#e2c6b4"),
              ("真皮", 1.5, "#d8a79a"), ("皮下组织", 4.0, "#e6d2b8")]
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    y = 0.0
    for name, t, c in layers:
        h = np.log10(1 + t * 1000) / 3.0
        ax.add_patch(plt.Rectangle((0, -y - h), 3.2, h, facecolor=c,
                                   edgecolor="white", lw=0.9))
        lab = f"{name}　{t * 1000:.0f} μm" if t < 0.1 else f"{name}　{t * 1:.1f} mm"
        ax.text(3.3, -y - h / 2, lab, fontsize=8.5, va="center")
        ax.text(0.1, -y - h / 2, {"角质层": "σa 小, σs' 1–5",
                                  "表皮": "黑色素",
                                  "真皮": "血红蛋白 + 胶原",
                                  "皮下组织": "脂肪"}[name],
                fontsize=7.5, va="center", color="#4a4038")
        y += h
    ax.set_xlim(0, 6.5)
    ax.set_ylim(-y - 0.15, 0.15)
    ax.axis("off")
    save(fig, "fig21-1-layers.png")


def fig21_2():
    wl = np.linspace(400, 800, 400)
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.semilogy(wl, melanin(wl, 0.01), color=INK, label="黑色素 1%")
    ax.semilogy(wl, melanin(wl, 0.10), color=INK, ls=(0, (5, 2)),
                label="黑色素 10%")
    for w, lab in ((542, "血红蛋白 542"), (577, "577")):
        ax.axvline(w, color=RED, lw=0.9, ls=(0, (3, 2)))
    ax.text(545, 4e-4, "血红蛋白吸收带", fontsize=8, color=RED)
    ax.set_xlabel("波长 (nm)")
    ax.set_ylabel(r"$\sigma_a^{mel}$  (mm$^{-1}$)")
    ax.set_xlim(400, 800)
    ax.set_ylim(1e-4, 30)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.16)
    save(fig, "fig21-2-spectra.png")


if __name__ == "__main__":
    fig21_1()
    fig21_2()
