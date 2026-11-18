import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *


def fig12_1():
    """白炉测试的三种结果。"""
    deg = np.linspace(0, 88, 500)
    th = np.deg2rad(deg)
    c = np.cos(th)
    correct = np.ones_like(c)
    missing_cos = 0.94 * (1.0 - 0.04 * (1 - c))
    sheen_unnorm = 1.0 + 0.22 * (1 - c) ** 4

    fig, ax = plt.subplots(figsize=(5.9, 3.2))
    ax.plot(deg, correct, color=INK, lw=1.4, label="正确实现")
    ax.plot(deg, missing_cos, color=BLUE, ls="--", label="法线分布漏乘 cos")
    ax.plot(deg, sheen_unnorm, color=ACCENT, ls="-.", label="sheen 未归一化")
    ax.axhline(1.0, color=GREY, ls=":", lw=0.8)
    ax.set_xlabel("入射天顶角（度）")
    ax.set_ylabel("方向反照率")
    ax.set_xlim(0, 88)
    ax.set_ylim(0.85, 1.30)
    ax.legend(loc="upper left", fontsize=8)
    ax.text(0.42, 0.12, "偏离 1 的量就是误差", transform=ax.transAxes, fontsize=8,
            color="#3c4654")
    save(fig, "fig12-1-furnace.png")


def fig12_2():
    """互易性：两种模型的非对称度。"""
    ti = np.deg2rad(np.linspace(5, 85, 60))
    to = np.deg2rad(np.linspace(5, 85, 60))
    TI, TO = np.meshgrid(ti, to, indexing="ij")

    L = np.stack([np.sin(TI), np.zeros_like(TI), np.cos(TI)], -1)
    V = np.stack([np.sin(TO), np.zeros_like(TO), np.cos(TO)], -1)

    def sheen(t):
        return 0.55 * 42.0 / (2 * np.pi) * (1 - np.cos(t)) ** 5

    f_io = sheen(np.arccos(np.clip(V[..., 2], -1, 1)))
    f_oi = sheen(np.arccos(np.clip(L[..., 2], -1, 1)))
    asym_sheen = np.abs(f_io - f_oi) / np.maximum(np.maximum(f_io, f_oi), 1e-9)

    g_io = brdf_ggx(L, V, 0.35, 0.04)
    g_oi = brdf_ggx(V, L, 0.35, 0.04)
    asym_ggx = np.abs(g_io - g_oi) / np.maximum(np.maximum(g_io, g_oi), 1e-9)

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.0),
                             gridspec_kw={"width_ratios": [1, 1]})
    for ax, mat, title in [(axes[0], asym_ggx, "GGX 微表面"),
                           (axes[1], asym_sheen, "sheen 项")]:
        m = ax.pcolormesh(np.rad2deg(TO), np.rad2deg(TI), mat, cmap="magma",
                          shading="auto", vmin=0, vmax=1)
        ax.set_xlabel("出射天顶角（度）")
        ax.set_title(title, fontsize=9)
        ax.set_xticks([5, 45, 85])
        ax.set_yticks([5, 45, 85])
    axes[0].set_ylabel("入射天顶角（度）")
    cb = fig.colorbar(m, ax=axes, pad=0.02, fraction=0.03)
    cb.set_label("相对非对称度", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    save(fig, "fig12-2-reciprocity.png")


def fig12_3():
    """蒙特卡洛误差随样本数的收敛。"""
    rng = np.random.default_rng(3)
    Ns = np.unique(np.round(np.logspace(1, 5, 14)).astype(int))
    true = 0.524
    err_ok, err_bad = [], []
    for N in Ns:
        e1, e2 = [], []
        for _ in range(60):
            u = rng.random((N, 2))
            ct = np.sqrt(1 - u[:, 0])
            st = np.sqrt(u[:, 0])
            ph = 2 * np.pi * u[:, 1]
            W = np.stack([st * np.cos(ph), st * np.sin(ph), ct], -1)
            f = 0.35 + 0.45 * (1 - ct) ** 3
            est = np.mean(2 * f)            # 余弦采样：pdf = cos/pi，权重 = f*pi
            e1.append(est)
            e2.append(np.mean(2 * f * 1.18))   # pdf 少乘一个常数
        err_ok.append(np.std(e1))
        err_bad.append(abs(np.mean(e2) - true))
    fig, ax = plt.subplots(figsize=(5.9, 3.2))
    ax.loglog(Ns, err_ok, "o-", color=BLUE, ms=4, label="pdf 正确")
    ax.loglog(Ns, err_bad, "s--", color=ACCENT, ms=4, label="pdf 少乘常数")
    ref = err_ok[0] * np.sqrt(Ns[0] / Ns)
    ax.loglog(Ns, ref, color=GREY, ls=":", lw=1.0, label="1/sqrt(N) 参考")
    ax.set_xlabel("每像素样本数")
    ax.set_ylabel("相对误差")
    ax.set_ylim(1e-4, 1)
    ax.legend(loc="lower left", fontsize=8)
    save(fig, "fig12-3-convergence.png")


fig12_1()
fig12_2()
fig12_3()
