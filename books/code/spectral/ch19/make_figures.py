import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "spectral"))
from figstyle import *
import numpy as np
import speclib as S
import neurolib as N

LAM = N.LAM


def fig19_1():
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    ax.axis("off")
    ax.grid(False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.6)

    items = [
        (0.25, "量子描述", "光子 $h\\nu$、统计", PURPLE),
        (2.15, "波动描述", "相位、干涉", BLUE),
        (4.05, "光谱描述", "强度 $\\times$ 波长", TEAL),
        (5.95, "三刺激值", "对波长积分", ACCENT),
        (7.85, "输出码值", "显示变换", GREY),
    ]
    for x, title, body, col in items:
        ax.add_patch(plt.Rectangle((x, 2.05), 1.65, 0.95, facecolor="white",
                                   edgecolor=col, lw=1.5))
        ax.text(x + 0.82, 2.70, title, ha="center", fontsize=9, color=col, fontweight="bold")
        ax.text(x + 0.82, 2.30, body, ha="center", fontsize=7.6, color="#303842")

    for x in [1.94, 3.84, 5.74, 7.64]:
        ax.annotate("", xy=(x + 0.16, 2.52), xytext=(x - 0.02, 2.52),
                    arrowprops=dict(arrowstyle="-|>", color="#9aa3af", lw=1.3,
                                    shrinkA=0, shrinkB=0))

    drops = ["相位", "相干性", "谱线形状", "色域外"]
    for i, (x, d) in enumerate(zip([2.10, 4.00, 5.90, 7.80], drops)):
        ax.annotate("", xy=(x, 1.75), xytext=(x, 2.02),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.1,
                                    linestyle=(0, (3, 2))))
        ax.text(x + 0.08, 1.55, "丢掉" + d, fontsize=7.8, color=RED)

    ax.text(0.25, 1.05, "每一步都是上一步在某个积分下的期望或代理。",
            fontsize=9, color=INK)
    ax.text(0.25, 0.62, "光谱渲染做的事，是把“对波长积分”这一步推迟到最后。",
            fontsize=9, color=INK)
    ax.text(0.25, 0.18, "代价是材质一侧必须能给出谱线，而不只是三个数。",
            fontsize=9, color=GREY)
    save(fig, "fig19-1-ladder.png")


def fig19_2():
    base = 0.30 + 0.45 * np.exp(-0.5 * ((LAM - 555) / 120) ** 2)
    M = S.cie_xyz_basis(LAM)
    P = np.eye(LAM.size) - M.T @ np.linalg.inv(M @ M.T) @ M     # 投影到零空间

    def smooth_null(mu, sig, w):
        g = w * np.exp(-0.5 * ((LAM - mu) / sig) ** 2)
        return P @ g

    d1 = smooth_null(470, 45, 1.0)
    d2 = smooth_null(640, 55, -0.8)
    pert = (d1 + d2) / np.max(np.abs(d1 + d2))
    amp = 0.18
    s1 = base
    s2 = np.clip(base + amp * pert, 0.02, 1)
    s3 = np.clip(base - amp * pert, 0.02, 1)
    xyz = [S.spectrum_to_xyz(LAM, s) for s in (s1, s2, s3)]
    print("XYZ:", [[round(float(v), 3) for v in x] for x in xyz])

    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    for s, c, lab in [(s1, BLUE, "谱线 A"), (s2, ACCENT, "谱线 B"), (s3, TEAL, "谱线 C")]:
        ax.plot(LAM, s, color=c, lw=1.8, label=lab)
    ax.set_xlabel("波长（nm）")
    ax.set_ylabel("反射率")
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 1.0)
    ax.legend(loc="upper right")
    ax.text(392, 0.05, "三条谱线的三刺激值相同，在同一个观察者眼里是同一个颜色",
            fontsize=8, color=GREY)
    save(fig, "fig19-2-metamer.png")


def fig19_3():
    spec = N.make_set(3000, "wide", seed=11)
    test = N.make_set(600, "wide", seed=12)
    mean, full = N.pca_basis(spec, 24)
    ns = [1, 2, 3, 4, 6, 8, 12, 16, 20, 24]
    errs = []
    for k in ns:
        e = np.mean([np.sqrt(np.mean((mean + (t - mean) @ full[:k].T @ full[:k] - t) ** 2))
                     for t in test[:150]])
        errs.append(float(e))
    print("pca errs", [round(e, 3) for e in errs])
    fig, ax = plt.subplots(figsize=(5.2, 3.1))
    ax.plot(ns, errs, marker="o", ms=4, color=TEAL, lw=1.8)
    ax.axvline(3, color=GREY, ls="--", lw=1.0)
    ax.text(3.5, errs[0] * 0.5, "三系数模型", color=GREY, fontsize=8.5)
    ax.set_xlabel("基底个数 N")
    ax.set_ylabel("重建 RMS")
    ax.set_xlim(0, 25)
    save(fig, "fig19-3-pca.png")


def fig19_4():
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.axis("off")
    ax.grid(False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)

    ax.add_patch(plt.Rectangle((0.3, 2.5), 2.6, 2.0, facecolor="#eef2f7",
                               edgecolor=BLUE, lw=1.5))
    ax.text(1.6, 4.15, "三维表", ha="center", fontsize=10, color=BLUE, fontweight="bold")
    ax.text(1.6, 3.55, "RGB → $\\varphi(\\mathbf{c})$", ha="center", fontsize=9, color=INK)
    ax.text(1.6, 2.98, "$32^3$ 体素，每格 16 个数", ha="center", fontsize=7.4, color="#404a58")

    ax.add_patch(plt.Rectangle((0.3, 0.5), 2.6, 1.0, facecolor="#eef7f4",
                               edgecolor=TEAL, lw=1.5))
    ax.text(1.6, 1.22, "一维表", ha="center", fontsize=10, color=TEAL, fontweight="bold")
    ax.text(1.6, 0.78, "波长 → $\\psi(\\lambda)$", ha="center", fontsize=9, color=INK)

    for yy, col in [(4.0, BLUE), (0.8, TEAL)]:
        ax.annotate("", xy=(4.6, 2.6), xytext=(3.0, yy),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4,
                                    connectionstyle="arc3,rad=0.15"))

    ax.add_patch(plt.Circle((5.3, 2.6), 0.62, facecolor="white", edgecolor=ACCENT, lw=1.6))
    ax.text(5.3, 2.6, "点积", ha="center", va="center", fontsize=10, color=ACCENT)

    ax.annotate("", xy=(7.4, 2.6), xytext=(5.95, 2.6),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.5))
    ax.text(7.5, 2.95, "$R(\\lambda)$", fontsize=11, color=INK)
    ax.text(7.5, 2.35, "任意波长、任意颜色", fontsize=7.8, color=GREY)
    ax.text(0.3, 0.05, "渲染时：查两次表，做 16 次乘加。代价与场景无关。",
            fontsize=8.6, color=GREY)
    save(fig, "fig19-4-tensor.png")


fig19_1()
fig19_2()
fig19_3()
fig19_4()
