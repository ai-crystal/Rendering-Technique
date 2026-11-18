import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180
T, P, dw = hemisphere_grid(80, 160)
W = spherical(T, P)
COSO = np.cos(T)


def albedo(alpha, variant="ok"):
    mus = np.cos(np.linspace(3, 88, 20) * D2R)
    out = []
    for mu in mus:
        wi = np.array([np.sqrt(max(0, 1 - mu ** 2)), 0.0, mu])
        h = normalize(wi + W)
        co = np.clip(W[..., 2], 0, 1)
        D = d_ggx(h[..., 2], alpha)
        if variant == "noG":
            G = 1.0
        elif variant == "badD":
            D = d_ggx(h[..., 2], alpha) * np.clip(h[..., 2], 0, 1)
            G = g2_smith(mu, co, alpha)
        else:
            G = g2_smith(mu, co, alpha)
        val = np.where(co > 0, D * G / np.maximum(4 * mu * co, EPS), 0.0)
        out.append(float(np.sum(val * COSO * dw)))
    return mus, np.array(out)


def fig12_1():
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    for variant, col, lab in [("ok", BLUE, "标准实现"), ("noG", ACCENT, "漏掉遮蔽项 G"),
                              ("badD", TEAL, "法线分布忘了乘 n·m")]:
        mus, a = albedo(0.5, variant)
        ax.plot(np.degrees(np.arccos(np.clip(mus, 0, 1))), a, color=col, lw=1.8, label=lab)
    ax.axhline(1.0, color=GREY, ls="--", lw=1.0)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("方向反照率")
    ax.set_xlim(0, 90)
    ax.set_ylim(0.4, 1.3)
    ax.legend(loc="upper right")
    save(fig, "fig12-1-furnace.png")


def fig12_2():
    rng = np.random.default_rng(5)
    ui = spherical(np.array([35 * D2R]), np.array([0.0]))[0]
    Ns = [16, 64, 256, 1024]
    res = {"均匀": [], "余弦": []}
    for N in Ns:
        e1, e2 = [], []
        for _ in range(80):
            u = rng.random((N, 2))
            ct = u[:, 0]
            st = np.sqrt(1 - ct ** 2)
            ph = 2 * np.pi * u[:, 1]
            Wq = np.stack([st * np.cos(ph), st * np.sin(ph), ct], axis=-1)
            f = brdf_ggx(ui, Wq, 0.4, 0.9) * np.clip(Wq[..., 2], 0, 1)
            e1.append(np.mean(f * 2 * np.pi))
            ct2 = np.sqrt(1 - u[:, 0])
            st2 = np.sqrt(u[:, 0])
            W2 = np.stack([st2 * np.cos(ph), st2 * np.sin(ph), ct2], axis=-1)
            f2 = brdf_ggx(ui, W2, 0.4, 0.9) * np.clip(W2[..., 2], 0, 1)
            e2.append(np.mean(f2 / np.maximum(ct2, 1e-6) * np.pi))
        res["均匀"].append(np.std(e1))
        res["余弦"].append(np.std(e2))
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    ax.loglog(Ns, res["均匀"], marker="o", color=GREY, lw=1.8, label="均匀采样")
    ax.loglog(Ns, res["余弦"], marker="s", color=TEAL, lw=1.8, label="余弦采样")
    ref = np.array(Ns, dtype=float)
    ax.loglog(Ns, res["余弦"][0] * np.sqrt(Ns[0] / ref), color=INK, ls=":", lw=1.0,
              label="斜率 −1/2 参考线")
    ax.set_xlabel("样本数")
    ax.set_ylabel("估计值标准差")
    ax.legend(loc="lower left")
    save(fig, "fig12-2-convergence.png")


fig12_1()
fig12_2()
