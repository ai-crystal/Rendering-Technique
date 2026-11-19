import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import lab


def errors(**cfg):
    est, tru = [], []
    for s in range(12):
        r = lab.sim(seed=s * 97, T=24, M0=4, cap=20, radius=1, **cfg)
        est.append(r["est"])
        tru.append(r["truth"])
    e = np.array(est)
    t = np.array(tru)
    return (e - t) / t


def corr_neighbors(e):
    g = int(round(np.sqrt(e.shape[-1])))
    a = e.reshape(e.shape[0], e.shape[1], g, g)
    x = np.concatenate([a[:, :, :, :-1].ravel(), a[:, :, :-1, :].ravel()])
    y = np.concatenate([a[:, :, :, 1:].ravel(), a[:, :, 1:, :].ravel()])
    return float(np.corrcoef(x, y)[0, 1])


def fig12_1():
    e_ind = errors(vis_shared=False)
    e_sha = errors(vis_shared=True)
    print("独立", round(corr_neighbors(e_ind), 3), "共享", round(corr_neighbors(e_sha), 3))

    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    for e, lab_, col in [(e_ind, "每个像素独立抽样", ACCENT), (e_sha, "所有像素共享抽样", BLUE)]:
        g = 8
        b = e.reshape(e.shape[0], e.shape[1], g, g)
        xs, ys = [], []
        for size in (1, 2, 4):
            k = g // size
            blk = b[:, :, :k * size, :k * size].reshape(e.shape[0], e.shape[1], k, size, k, size)
            m = blk.mean(axis=(3, 5))
            xs.append(size * size)
            ys.append(m.std())
        ax.plot(xs, ys, "o-", ms=4.5, color=col, label=lab_)
        print(lab_, [round(v, 3) for v in ys])
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("参与平均的像素数")
    ax.set_ylabel("相对误差的标准差")
    ax.legend(loc="lower left", fontsize=8)
    save(fig, "fig12-1-rng.png")


def fig12_2():
    r1 = lab.sim(seed=11, T=8, M0=4, cap=20, radius=1, vis_shared=False)
    r2 = lab.sim(seed=11, T=8, M0=4, cap=20, radius=1, vis_shared=True)
    e_ind = ((r1["est"] - r1["truth"]) / r1["truth"])[None]
    e_sha = ((r2["est"] - r2["truth"]) / r2["truth"])[None]
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.2))
    for ax, e, title in [(axes[0], e_ind, "每像素独立"), (axes[1], e_sha, "全屏共享相同随机数")]:
        g = 8
        m = e.reshape(e.shape[0], e.shape[1], g, g)
        mean_err = m[0, -1]
        im = ax.imshow(mean_err, cmap="RdBu_r", vmin=-1.5, vmax=1.5,
                       interpolation="nearest")
        print(mean_err.std())
        ax.set_title(title, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
    cb = fig.colorbar(im, ax=axes, fraction=0.035, pad=0.02)
    cb.set_label("单帧相对误差", fontsize=8)
    save(fig, "fig12-2-pattern.png")


fig12_1()
fig12_2()
