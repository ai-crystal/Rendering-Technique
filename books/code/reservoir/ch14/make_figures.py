import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import lab


def fig14_1():
    r = lab.sim(seed=7, T=48, M0=4, cap=20, radius=1)
    e = (r["est"] - r["truth"]) / r["truth"]
    g = 8
    single = e[20].reshape(g, g)
    mean = e[8:].mean(axis=0).reshape(g, g)
    print("单帧误差 std", round(float(single.std()), 3),
          "长序列均值 std", round(float(mean.std()), 3))
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.2))
    for ax, m, ttl in [(axes[0], single, "单帧"), (axes[1], mean, "40 帧平均")]:
        im = ax.imshow(m, cmap="RdBu_r", vmin=-0.8, vmax=0.8, interpolation="nearest")
        ax.set_title(ttl, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
    cb = fig.colorbar(im, ax=axes, fraction=0.035, pad=0.02)
    cb.set_label("相对误差", fontsize=8)
    save(fig, "fig14-1-maps.png")


def fig14_2():
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    settings = [(dict(), "正确实现", ACCENT), (dict(deterministic=True), "确定性挑大的", BLUE)]
    for cfg, lab_, col in settings:
        runs = []
        for s in range(12):
            r = lab.sim(seed=s * 97, T=40, M0=4, cap=20, radius=1, **cfg)
            e = (r["est"] / r["truth"]).ravel()
            runs.append(np.cumsum(e) / np.arange(1, e.size + 1))
        runs = np.array(runs)
        mean = runs.mean(axis=0)
        se = runs.std(axis=0) / np.sqrt(runs.shape[0])
        n = np.arange(1, mean.size + 1)
        ax.plot(n, (mean - 1) * 100, color=col, label=lab_)
        ax.fill_between(n, (mean - 1 - 2 * se) * 100, (mean - 1 + 2 * se) * 100,
                        color=col, alpha=0.18, lw=0)
        print(lab_, "末帧偏差%", round(float((mean[-1] - 1) * 100), 1))
    ax.axhline(0, color=INK, lw=0.8, ls=":")

    ax.set_xlabel("累计样本数（帧 × 像素）")
    ax.set_ylabel("平均亮度偏差（%）")
    ax.legend(loc="lower left", fontsize=8)
    save(fig, "fig14-2-mean.png")


fig14_1()
fig14_2()
