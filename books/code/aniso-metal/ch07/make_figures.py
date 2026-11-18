#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 7 章插图：氧化膜的单层干涉。

膜层用 Cu2O（n = 2.70），基底用附录 B 的铜；垂直入射。
"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "common"))
sys.path.insert(0, str(HERE.parents[0]))
from figstyle import *          # noqa: F401,F403
from anisocommon import *       # noqa: F401,F403

NF = 2.70


def airy(d_nm, lam_um, n1=NF, sub=(0.978, 2.449)):
    """单层膜在垂直入射下的反射率，复振幅叠加。d 单位 nm，lam 单位 μm。"""
    n2 = sub[0] + 1j * sub[1]
    r01 = (1.0 - n1) / (1.0 + n1)
    r12 = (n1 - n2) / (n1 + n2)
    delta = 2 * np.pi * n1 * (d_nm * 1e-3) / lam_um
    e = np.exp(2j * delta)
    r = (r01 + r12 * e) / (1.0 + r01 * r12 * e)
    return float(np.abs(r) ** 2)


def incoherent(d_nm, lam_um, n1=NF, sub=(0.978, 2.449)):
    """忽略干涉：两次界面的强度反射率串联。"""
    R01 = ((1 - n1) / (1 + n1)) ** 2
    R12 = float(f0_from_nk(*sub))
    return R01 + (1 - R01) ** 2 * R12 / (1 - R01 * R12)


def fig7_1():
    d = np.linspace(0, 600, 1200)
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    cols = [ACCENT, TEAL, BLUE]
    for j, c in enumerate(cols):
        sub = METALS["铜"][j]
        ax.plot(d, [airy(x, WL[j], sub=sub) for x in d], color=c, label=WL_NAME[j])
    ax.set_xlabel("氧化膜厚度 $d$ (nm)")
    ax.set_ylabel("反射率 $R$")
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="lower center", ncol=3, bbox_to_anchor=(0.5, 1.0))
    print("Cu2O on Cu, d=0:", [round(airy(0, WL[j], sub=METALS["铜"][j]), 3) for j in range(3)])
    print("d=60:", [round(airy(60, WL[j], sub=METALS["铜"][j]), 3) for j in range(3)])
    print("d=150:", [round(airy(150, WL[j], sub=METALS["铜"][j]), 3) for j in range(3)])
    save(fig, "fig7-1-R-vs-thickness.png")


def fig7_2():
    ds = [0, 20, 50, 100]
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    x = np.arange(len(ds))
    w = 0.26
    for j in range(3):
        vals = [airy(dn, WL[j], sub=METALS["铜"][j]) for dn in ds]
        ax.bar(x + (j - 1) * w, vals, w, label=WL_NAME[j],
               color=[ACCENT, TEAL, BLUE][j], edgecolor="white", lw=0.6)
        for xi, v in zip(x, vals):
            ax.text(xi + (j - 1) * w, v + 0.02, f"{v:.2f}", ha="center", fontsize=6.6)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{dn} nm" for dn in ds])
    ax.set_xlabel("氧化膜厚度")
    ax.set_ylabel("反射率 $R$")
    ax.set_ylim(0, 1.18)
    ax.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.0))
    ax.grid(axis="x", visible=False)
    save(fig, "fig7-2-R-vs-wavelength.png")


def fig7_3():
    d = np.linspace(0, 600, 900)
    sub = METALS["铜"][1]
    a = np.array([airy(x, 0.55, sub=sub) for x in d])
    b = np.array([incoherent(x, 0.55, sub=sub) for x in d])
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    ax.plot(d, a, color=ACCENT, label="完整干涉（Airy）")
    ax.plot(d, b, color=GREY, ls="--", label="忽略干涉的串联近似")
    ax.fill_between(d, a, b, color=RED, alpha=0.15)
    ax.set_xlabel("氧化膜厚度 $d$ (nm)，$\\lambda$ = 0.55 μm")
    ax.set_ylabel("反射率 $R$")
    ax.set_xlim(0, 600)
    ax.set_ylim(0.1, 1.0)
    ax.legend(loc="upper right")
    ax.annotate(f"最大偏差 {np.max(np.abs(a - b)):.2f}", (d[np.argmax(np.abs(a - b))],
                a[np.argmax(np.abs(a - b))]), xytext=(300, 0.55), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.7, color=GREY))
    save(fig, "fig7-3-approx-error.png")


if __name__ == "__main__":
    fig7_1()
    fig7_2()
    fig7_3()
