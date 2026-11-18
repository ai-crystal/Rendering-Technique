import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *


def model(theta, sigma, sheen, rho=0.40):
    c = np.cos(theta)
    spec = 0.25 * np.exp(-0.5 * ((theta - np.deg2rad(58)) / sigma) ** 2)
    return rho + spec + sheen * (1 - c) ** 4


def fig11_1():
    """三个参数在视角上的灵敏度：各改 12% 时的反射率变化。"""
    deg = np.linspace(1, 88, 400)
    th = np.deg2rad(deg)
    sig0, s0, rho0 = np.deg2rad(10), 0.40, 0.40
    base = model(th, sig0, s0, rho0)
    cases = [("纱线宽度 sigma", model(th, sig0 * 1.12, s0, rho0), ACCENT),
             ("sheen 强度 s", model(th, sig0, s0 * 1.12, rho0), BLUE),
             ("基础反照率 rho", model(th, sig0, s0, rho0 * 1.12), TEAL)]
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    for name, alt, c in cases:
        ax.plot(deg, np.abs(alt - base), color=c, label=name)
    ax.set_xlabel("观察天顶角（度）")
    ax.set_ylabel("反射率变化量")
    ax.set_xlim(0, 88)
    ax.set_ylim(0, 0.09)
    ax.legend(loc="upper left", fontsize=8)
    ax.text(0.45, 0.10, "三个参数在不同角度上各自主导", transform=ax.transAxes,
            fontsize=8, color="#3c4654")
    save(fig, "fig11-1-sensitivity.png")


def fig11_2():
    """二维误差面：宽度与 sheen 的相关性。"""
    sig = np.deg2rad(np.linspace(3, 26, 240))
    s = np.linspace(0.05, 0.9, 240)
    S, P = np.meshgrid(sig, s, indexing="ij")
    th = np.deg2rad(np.linspace(2, 86, 90))
    truth = model(th, np.deg2rad(10), 0.40)
    E = np.zeros_like(S)
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            E[i, j] = np.mean((model(th, S[i, j], P[i, j]) - truth) ** 2)
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    m = ax.pcolormesh(P, np.rad2deg(S), np.log10(E + 1e-9), cmap="viridis",
                      shading="auto", vmin=-5, vmax=-1)
    ax.contour(P, np.rad2deg(S), E, levels=[1e-4, 1e-3], colors="w", linewidths=0.8)
    ax.set_xlabel("sheen 强度 s")
    ax.set_ylabel("纱线宽度 sigma（度）")
    ax.plot([0.40], [10], "o", color=RED, ms=5)
    ax.annotate("真值", xy=(0.40, 10), xytext=(0.50, 6), fontsize=8, color="w",
                arrowprops=dict(arrowstyle="->", color="w", lw=0.8))
    cb = fig.colorbar(m, ax=ax, pad=0.02)
    cb.set_label("log10 拟合误差", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    ax.text(0.06, 0.94, "等高线拉成斜谷", transform=ax.transAxes, color="w", fontsize=8,
            va="top")
    save(fig, "fig11-2-valley.png")


def fig11_3():
    """噪声水平决定可辨识性。"""
    sig = np.deg2rad(np.linspace(3, 26, 200))
    s = np.linspace(0.05, 0.9, 200)
    S, P = np.meshgrid(sig, s, indexing="ij")
    th = np.deg2rad(np.linspace(2, 86, 80))
    truth = model(th, np.deg2rad(10), 0.40)
    E = np.zeros_like(S)
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            E[i, j] = np.mean((model(th, S[i, j], P[i, j]) - truth) ** 2)
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    for noise, c in [(0.005, BLUE), (0.02, TEAL), (0.05, ACCENT)]:
        ax.contour(P, np.rad2deg(S), E, levels=[noise ** 2], colors=[c], linewidths=1.3)
        ax.plot([], [], color=c, label="噪声 %.1f%%" % (noise * 100))
    ax.plot([0.40], [10], "o", color=RED, ms=5)
    ax.set_xlabel("sheen 强度 s")
    ax.set_ylabel("纱线宽度 sigma（度）")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_xlim(0.05, 0.9)
    ax.set_ylim(3, 26)
    save(fig, "fig11-3-identifiability.png")


fig11_1()
fig11_2()
fig11_3()
