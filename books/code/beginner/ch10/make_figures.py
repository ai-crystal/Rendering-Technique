import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180
ALPHA, THI, F0 = 0.4, 40.0, 0.9
UI = spherical(np.array([THI * D2R]), np.array([0.0]))[0]


def integrand(W):
    return brdf_ggx(UI, W, ALPHA, F0) * np.clip(W[..., 2], 0.0, 1.0)


def reference(n_theta=300, n_phi=600):
    T, P, dw = hemisphere_grid(n_theta, n_phi)
    W = spherical(T, P)
    return float(np.sum(integrand(W) * dw))


def vndf_batch(wi, alpha, u):
    """向量化的 GGX 可见法线分布采样，u 是 (n,2)。"""
    vh = np.stack([alpha * wi[0], alpha * wi[1], wi[2]])
    vh = vh / np.linalg.norm(vh)
    lensq = vh[0] ** 2 + vh[1] ** 2
    if lensq < 1e-12:
        t1 = np.array([1.0, 0.0, 0.0])
    else:
        t1 = np.array([-vh[1], vh[0], 0.0]) / np.sqrt(lensq)
    t2 = np.cross(vh, t1)
    r = np.sqrt(u[:, 0])
    phi = 2 * np.pi * u[:, 1]
    p1 = r * np.cos(phi)
    p2 = r * np.sin(phi)
    s = 0.5 * (1.0 + vh[2])
    p2 = (1 - s) * np.sqrt(np.maximum(1 - p1 ** 2, 0)) + s * p2
    nh = (p1[:, None] * t1 + p2[:, None] * t2
          + np.sqrt(np.maximum(0, 1 - p1 ** 2 - p2 ** 2))[:, None] * vh)
    h = np.stack([alpha * nh[:, 0], alpha * nh[:, 1], np.maximum(nh[:, 2], 0)], axis=-1)
    return h / np.maximum(np.linalg.norm(h, axis=-1, keepdims=True), 1e-9)


def fig10_1():
    rng = np.random.default_rng(0)
    ref = reference()
    Ns = [16, 64, 256, 1024]
    trials = 60
    res = {"半球均匀": [], "余弦": [], "VNDF": []}
    for N in Ns:
        e_u, e_c, e_v = [], [], []
        for _ in range(trials):
            u = rng.random((N, 2))
            # 均匀
            ct = u[:, 0]
            st = np.sqrt(1 - ct ** 2)
            ph = 2 * np.pi * u[:, 1]
            W = np.stack([st * np.cos(ph), st * np.sin(ph), ct], axis=-1)
            e_u.append(np.mean(integrand(W) * 2 * np.pi))
            # 余弦
            ct2 = np.sqrt(1 - u[:, 0])
            st2 = np.sqrt(u[:, 0])
            W2 = np.stack([st2 * np.cos(ph), st2 * np.sin(ph), ct2], axis=-1)
            e_c.append(np.mean(integrand(W2) / np.maximum(ct2, 1e-6) * np.pi))
            # VNDF
            h = vndf_batch(UI, ALPHA, u)
            wo = 2 * (h @ UI)[:, None] * h - UI
            ok = wo[:, 2] > 0
            if ok.sum() == 0:
                e_v.append(0.0)
                continue
            p = g1_smith(UI[2], ALPHA) * d_ggx(np.clip(h[ok, 2], 0, 1), ALPHA) / (4 * UI[2])
            e_v.append(np.mean(integrand(wo[ok]) / p) * ok.mean())
        res["半球均匀"].append(np.std(e_u))
        res["余弦"].append(np.std(e_c))
        res["VNDF"].append(np.std(e_v))

    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    for key, col in [("半球均匀", GREY), ("余弦", TEAL), ("VNDF", ACCENT)]:
        ax.loglog(Ns, res[key], marker="o", ms=4, color=col, lw=1.7, label=key + "采样")
    ax.set_xlabel("每像素样本数")
    ax.set_ylabel("估计值的标准差")
    ax.set_ylim(1e-4, 5)
    ax.legend(loc="lower left")
    ax.text(20, 2.0, "参考值 %.3f" % ref, color=GREY, fontsize=8)
    save(fig, "fig10-1-variance.png")


def ndf_batch(alpha, u):
    ct = np.sqrt((1 - u[:, 0]) / (1 + (alpha ** 2 - 1) * u[:, 0]))
    st = np.sqrt(np.maximum(0, 1 - ct ** 2))
    ph = 2 * np.pi * u[:, 1]
    return np.stack([st * np.cos(ph), st * np.sin(ph), ct], axis=-1)


def fig10_2():
    rng = np.random.default_rng(2)
    angs = np.linspace(5, 85, 17)
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    for alpha, col in [(0.2, TEAL), (0.5, ACCENT)]:
        acc, acc_ndf = [], []
        for a in angs:
            ui = spherical(np.array([a * D2R]), np.array([0.0]))[0]
            h = vndf_batch(ui, alpha, rng.random((4000, 2)))
            wo = 2 * (h @ ui)[:, None] * h - ui
            acc.append(np.mean(wo[:, 2] > 0))
            hn = ndf_batch(alpha, rng.random((4000, 2)))
            won = 2 * (hn @ ui)[:, None] * hn - ui
            acc_ndf.append(np.mean(won[:, 2] > 0))
        ax.plot(angs, acc, color=col, marker="o", ms=3.5, lw=1.7,
                label="VNDF，α = %.1f" % alpha)
        ax.plot(angs, acc_ndf, color=col, marker="s", ms=3, lw=1.2, ls="--",
                label="NDF，α = %.1f" % alpha)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("有效样本比例")
    ax.set_xlim(0, 90)
    ax.set_ylim(0.3, 1.02)
    ax.legend(loc="lower left", fontsize=7, ncol=2)
    save(fig, "fig10-2-acceptance.png")


def fig10_3():
    th = np.linspace(0.5, 89.5, 500) * D2R
    ui = spherical(np.array([30 * D2R]), np.array([0.0]))[0]
    uo = spherical(th, np.full_like(th, np.pi))
    h = normalize(ui + uo)
    ci = ui[2]
    vh = np.clip(np.sum(ui * h, axis=-1), 1e-6, 1)
    D = d_ggx(h[..., 2], 0.35)
    p_ok = g1_smith(ci, 0.35) * D / (4 * ci)
    p_bad = D * np.clip(h[..., 2], 0, 1) / (4 * vh)
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    ax.semilogy(np.degrees(th), p_ok / p_ok.max(), color=BLUE, lw=2.0, label="pdf 正确")
    ax.semilogy(np.degrees(th), p_bad / p_bad.max(), color=RED, lw=1.6, ls="--",
                label="NDF 采样的 pdf")
    ax.set_xlabel("出射方向与法线夹角（度）")
    ax.set_ylabel("pdf（按最大值归一化）")
    ax.set_xlim(0, 90)
    ax.set_ylim(1e-5, 2)
    ax.legend(loc="lower left")
    ax.text(34, 3e-4, "两种采样器的 pdf 形状不同", color=GREY, fontsize=8)
    save(fig, "fig10-3-pdf-error.png")


fig10_1()
fig10_2()
fig10_3()
