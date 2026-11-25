import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

SIG = 2.0      # 最大消光系数
R = 1.0


def sigma(d, w):
    t = np.clip(0.5 - d / w, 0.0, 1.0)
    s = t * t * (3 - 2 * t)
    return SIG * s


# ---------------------------------------------------------------- 图 12-1
def fig12_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))
    ax = axes[0]
    d = np.linspace(-0.6, 0.6, 600)
    for w, col in ((0.05, BLUE), (0.2, TEAL), (0.5, ACCENT)):
        ax.plot(d, sigma(d, w), color=col, lw=1.7, label=f"w = {w}")
    ax.axvline(0.0, color=GREY, ls=":", lw=1.0)
    ax.set_xlabel("有符号距离 d")
    ax.set_ylabel(r"消光系数 $\sigma_t$")
    ax.set_ylim(-0.05, 2.2)
    ax.legend(loc="center right", fontsize=7.5)
    panel_label(ax, "(a)", x=-0.15, y=1.06)

    ax = axes[1]
    b = 0.95
    L = 2 * np.sqrt(R ** 2 - b ** 2)
    s = np.linspace(0, L, 900)
    d = np.abs(s - L / 2) - L / 2
    ax.plot(s, np.exp(-SIG * s), color=INK, lw=1.8, label="均匀介质 exp(-2s)")
    for w, col in ((0.05, BLUE), (0.2, TEAL), (0.5, ACCENT)):
        od = np.concatenate([[0.0], np.cumsum(0.5 * (sigma(d[1:], w) + sigma(d[:-1], w))
                                              * np.diff(s))])
        ax.plot(s, np.exp(-od), color=col, lw=1.5, ls="--", label=f"边界宽度 w = {w}")
    ax.set_xlabel("沿光线穿过球体的距离")
    ax.set_ylabel("透射率")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="upper right", fontsize=7.2)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig12-1-density.png")


# ---------------------------------------------------------------- 图 12-2
def march_error(n_steps, adaptive=False, w=0.12, offset=0.0):
    total = 2.0 * R + 2.0
    if adaptive:
        seg, t = [], 0.0
        for _ in range(n_steps):
            x = -2.0 + t
            dd = abs(x) - R
            h = max(0.5 * abs(dd), 0.004)
            seg.append((t, min(t + h, total)))
            t = min(t + h, total)
            if t >= total:
                break
        seg = np.array(seg)
        x0, x1 = -2.0 + seg[:, 0], -2.0 + seg[:, 1]
    else:
        edges = np.linspace(0.0, total, n_steps + 1) + offset * total / n_steps
        edges = np.clip(edges, 0.0, total)
        x0, x1 = -2.0 + edges[:-1], -2.0 + edges[1:]
    d0, d1 = np.abs(x0) - R, np.abs(x1) - R
    od = np.sum(0.5 * (sigma(d0, w) + sigma(d1, w)) * (x1 - x0))
    fine = np.linspace(-2.0, total - 2.0, 200000)
    od_ref = np.trapezoid(sigma(np.abs(fine) - R, w), fine)
    return abs(od - od_ref) / od_ref


def fig12_2():
    ns = np.unique(np.round(np.logspace(1.1, 3.4, 34)).astype(int))
    rng = np.random.default_rng(4)
    offs = rng.random(16)
    uni, ada = [], []
    for n in ns:
        uni.append(np.sqrt(np.mean([march_error(n, False, 0.12, o) ** 2 for o in offs])))
        ada.append(np.sqrt(np.mean([march_error(n, True) ** 2 for o in offs])))
    fig, ax = plt.subplots(figsize=(6.3, 3.1))
    ax.loglog(ns, uni, "o-", color=BLUE, ms=3.4, lw=1.5, label="均匀步长")
    ax.loglog(ns, ada, "s--", color=ACCENT, ms=3.2, lw=1.5, label="按距离自适应步长")
    ax.loglog(ns, 2.0 / ns, color=GREY, ls=":", lw=1.1, label=r"$O(1/N)$")
    ax.set_xlabel("采样次数")
    ax.set_ylabel("光学厚度的相对误差（16 个偏移的均方根）")
    ax.set_ylim(1e-6, 1.0)
    ax.legend(loc="lower left", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig12-2-integration.png")


# ---------------------------------------------------------------- 图 12-3
def alpha_profile(bs, w):
    out = []
    for b in bs:
        chord = 2 * np.sqrt(max(R ** 2 - b ** 2, 0.0))
        s = np.linspace(0, max(chord, 1e-6), 800)
        d = np.sqrt((b) ** 2 + (s - chord / 2) ** 2) - R
        od = np.trapezoid(sigma(d, w), s)
        out.append(1 - np.exp(-od))
    return np.array(out)


def fig12_3():
    bs = np.linspace(0.55, 1.25, 500)
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    for w, col in ((0.04, BLUE), (0.12, TEAL), (0.30, ACCENT)):
        ax.plot(bs, alpha_profile(bs, w), color=col, lw=1.7, label=f"w = {w}")
    ax.axvline(1.0, color=GREY, ls=":", lw=1.0)
    ax.text(1.005, 0.15, "几何轮廓 b = R", fontsize=7.5, color=GREY)
    ax.set_xlabel("光线到球心的距离 b")
    ax.set_ylabel(r"不透明度 $1-T$")
    ax.set_ylim(-0.03, 1.03)
    ax.legend(loc="lower left", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig12-3-silhouette.png")


if __name__ == "__main__":
    fig12_1()
    fig12_2()
    fig12_3()
