import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()


# ------------------------------------------------------------------ 图 13-1
def fig13_1():
    """白炉测试：像素值应该恒为 1，误差随样本数下降。"""
    rng = np.random.default_rng(4)
    spd = np.ones_like(LAM)                      # 均匀白炉
    y = cie_y(LAM)
    cdf = np.concatenate([[0], np.cumsum(y) / np.cumsum(y)[-1]])
    truth = float(np.sum(spd * y) * (LAM[1] - LAM[0]))
    xs = np.concatenate([[380.0], LAM])

    Ns = np.array([1, 2, 4, 8, 16, 32, 64, 128])
    trials = 4000
    res = {}
    for n in (1, 4):
        errs = []
        for N in Ns:
            es = []
            for _ in range(trials):
                acc = 0.0
                for _ in range(N):
                    hero = rng.uniform(380, 780)
                    ls = 380 + np.mod(hero - 380 + np.arange(n) * (400 / n), 400)
                    acc += np.mean(np.interp(ls, LAM, spd * y)) / (1.0 / 400)
                es.append(acc / N / truth - 1)
            errs.append(float(np.sqrt(np.mean(np.square(es)))))
        res[n] = errs

    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    ax.loglog(Ns, res[1], "o-", color=BLUE, ms=4, label="1 波长 / 路径")
    ax.loglog(Ns, res[4], "s-", color=ACCENT, ms=4, label="4 波长 / 路径")
    ax.set_xlabel("每条路径的样本数（spp）")
    ax.set_ylabel("白炉亮度的相对误差")
    ax.legend(loc="lower left")
    ax.set_title("白炉测试：所有波长都应为 1", pad=6)
    save(fig, "fig13-2-furnace.png")


# ------------------------------------------------------------------ 图 13-2
def _nnls(A, b, n=60000):
    w = np.abs(np.linalg.lstsq(A, b, rcond=None)[0])
    lip = np.linalg.eigvalsh(A.T @ A).max()
    for _ in range(n):
        w = np.clip(w - (A.T @ (A @ w - b)) / lip, 0, None)
    return w


def _two_lights():
    """两盏三刺激值相同、光谱完全不同的灯：钨丝灯与"汞灯 + 荧光粉"。"""
    warm = blackbody(LAM, 2800.0)
    warm = warm / warm.max()
    tgt = spectrum_to_xyz(LAM, warm)
    bumps = np.stack([gaussian_line(LAM, c, w) for c, w in
                      [(436, 5), (470, 40), (546, 6), (577, 7), (610, 75), (700, 120)]])
    A = np.stack([spectrum_to_xyz(LAM, b) for b in bumps], axis=1)
    spiky = bumps.T @ _nnls(A, tgt)
    return [warm, spiky]


def fig13_2():
    """两盏同色异谱的灯照同一块材料：RGB 说一样，光谱说不一样。"""
    lights = _two_lights()
    wall = 0.05 + 0.9 * gaussian_line(LAM, 540, 35)

    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.16, 0.94, "钨丝灯", fontsize=8.2, ha="center", va="center")
    ax.text(0.52, 0.94, "汞灯 + 荧光粉", fontsize=8.2, ha="center", va="center")
    ax.text(0.83, 0.94, "两者色差", fontsize=8.2, ha="center", va="center")

    def rgb_of(spd, spectral):
        if spectral:
            xyz = spectrum_to_xyz(LAM, spd * wall)
            return M_XYZ2RGB_PUBLISHED @ xyz, xyz
        sl = spectrum_to_xyz(LAM, spd)
        c = np.clip(M_XYZ2RGB_PUBLISHED @ (sl / sl[1]), 0, None)
        cw = np.clip(reflectance_rgb(wall), 0, None)
        rgbv = c * cw
        return rgbv, M_RGB2XYZ_PUBLISHED @ rgbv

    for r, (spectral, name) in enumerate([(False, "RGB 逐通道相乘"), (True, "光谱逐波长相乘")]):
        y = 0.60 - r * 0.40
        ax.text(0.02, y + 0.20, name, fontsize=8.4, va="center")
        outs = []
        for spd in lights:
            rgbv, xyz = rgb_of(spd, spectral)
            outs.append((rgbv, xyz))
        scale = max(np.max(o[0]) for o in outs)
        for k, (rgbv, xyz) in enumerate(outs):
            c = srgb_encode(np.clip(rgbv / scale, 0, 1))
            ax.add_patch(plt.Rectangle((0.02 + 0.36 * k, y - 0.10), 0.30, 0.22,
                                       color=c, ec="#3a3a3a", lw=0.6))
        de = float(delta_e76(xyz_to_lab(outs[0][1] / outs[0][1][1]),
                             xyz_to_lab(outs[1][1] / outs[1][1][1])))
        ax.text(0.83, y, "%.2f" % de, fontsize=9, ha="center", va="center",
                color=ACCENT if de > 2 else "#444")
    ax.text(0.02, 0.005, "两盏灯的三刺激值完全相同，材料是一条 540 nm 的窄反射带",
            fontsize=7.6, color="#666")
    save(fig, "fig13-3-shadows.png")


# ------------------------------------------------------------------ 图 13-3
def fig13_3():
    """波长采样的噪声：同一场景在 4、16、64 个波长样本下的样子。"""
    W, H = 190, 130
    xs, ys = np.meshgrid(np.linspace(-1.0, 1.0, W), np.linspace(-1.0, 1.0, H))
    r2 = xs ** 2 + ys ** 2
    inside = r2 < 0.62 ** 2
    shade = np.where(inside, np.sqrt(np.clip(1 - r2 / 0.62 ** 2, 0, 1)) * 0.8 + 0.2, 0.95)
    albedo = np.where(inside, 0.9, 0.55)

    light = blackbody(LAM, 3200.0)
    light = light / light.max()
    spec = light * albedo[..., None]
    # 球面上加一个宽吸收带，让光谱有结构
    mask = (0.05 + 0.9 * gaussian_line(LAM, 560, 70))[None, None, :]
    spec = np.where(inside[..., None], spec * mask, spec)

    rng = np.random.default_rng(21)
    imgs = []
    for n in (4, 16, 64):
        xyz = np.zeros((H, W, 3))
        for _ in range(n):
            lam = rng.uniform(400, 780, (H, W))
            idx = np.clip(np.round(lam - 380).astype(int), 0, len(LAM) - 1)
            w = np.stack([cie_x(LAM[idx]), cie_y(LAM[idx]), cie_z(LAM[idx])], axis=-1)
            xyz += np.take_along_axis(spec, idx[..., None], axis=2) * w * (380.0)
        xyz /= n
        xyz *= shade[..., None]
        imgs.append(np.einsum("ijc,dc->ijd", xyz, M_XYZ2RGB_PUBLISHED))

    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.4), gridspec_kw={"wspace": 0.05})
    scale = np.percentile(imgs[-1], 99.0)
    for ax, img, n in zip(axes, imgs, (4, 16, 64)):
        ax.imshow(srgb_encode(np.clip(img / scale, 0, 1)), origin="lower")
        ax.set_title("%d 波长 / 像素" % n, fontsize=8.5, pad=4)
        ax.axis("off")
    save(fig, "fig13-4-noise.png")




# ------------------------------------------------------------------ 图 13-4
def fig13_4():
    """最小实现渲染出的图。"""
    import mini_tracer as mt
    img = mt.render(w=150, h=110, spp=20, seed=3)
    rgb = np.einsum("ijc,dc->ijd", img, M_XYZ2RGB_PUBLISHED)
    scale = np.percentile(rgb, 99.0)
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    ax.imshow(np.power(np.clip(rgb / scale, 0, 1), 1 / 2.2), origin="upper")
    ax.axis("off")
    save(fig, "fig13-1-render.png")


fig13_4()
fig13_1()
fig13_2()
fig13_3()
