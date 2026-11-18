import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180


def fig11_1():
    m = np.linspace(0, 1, 200)
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    ax.plot(m, 0.04 + m * (1 - 0.04), color=BLUE, lw=2.0, label="镜面项的 F0")
    ax.plot(m, 1 - m, color=ACCENT, lw=2.0, label="漫反射项的权重")
    ax.fill_between(m, 0, 0.04 + m * (1 - 0.04), color=BLUE, alpha=0.08)
    ax.set_xlabel("金属度 m")
    ax.set_ylabel("相对权重")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="center right")
    ax.axvspan(0.25, 0.75, color=GREY, alpha=0.12)
    ax.text(0.5, 1.0, "中间区间没有物理对应", ha="center", color=GREY, fontsize=8)
    save(fig, "fig11-1-metallic.png")


def fig11_2():
    # 双峰粗糙度分布在 mip 平均下的表观粗糙度：先对 r 平均，再映射；以及对 alpha 平均
    levels = np.arange(0, 7)
    r1, r2 = 0.10, 0.70
    alpha_a, alpha_b = [], []
    p = 0.5
    for _ in levels:
        mean_r = (r1 + r2) / 2
        mean_a = (r1 ** 2 + r2 ** 2) / 2
        alpha_a.append(mean_r ** 2)
        alpha_b.append(np.sqrt(mean_a))
        d = (r2 - r1) * np.sqrt(p) / 2
        r1, r2 = mean_r - d, mean_r + d
        p /= 2
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    ax.plot(levels, alpha_a, marker="o", color=RED, lw=1.8, label="先平均 r，再算 α = r²")
    ax.plot(levels, alpha_b, marker="s", color=BLUE, lw=1.8, label="平均 α，再开方得等效 α")
    ax.set_xlabel("mip 级别")
    ax.set_ylabel("表观粗糙度 α")
    ax.set_xlim(-0.2, 6.2)
    ax.legend(loc="center right", fontsize=7.5)
    ax.text(0.1, 0.055, "两块粗糙度不同的区域混合后，两种做法给出不同的高光", fontsize=8, color=GREY)
    save(fig, "fig11-2-coupling.png")


fig11_1()
fig11_2()
