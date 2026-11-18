import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import ris

N = 64
B = ris.make_scene(N, 1, 2, "zipf")[0]
V = ris.visibility(N, 1, 2, soft=True, lo=0.7, hi=1.0)[0]
F = B * V
TRUTH = F.sum()

P_A = np.full(N, 1.0 / N)
P_B = B / B.sum()
P = np.stack([P_A, P_B])
MIS = P / P.sum(axis=0, keepdims=True)


def pooled(Ma, Mb, T, rng, mode):
    """两种技术的候选放进同一个蓄水池。"""
    ia = rng.choice(N, size=(T, Ma), p=P_A)
    ib = rng.choice(N, size=(T, Mb), p=P_B)
    idx = np.concatenate([ia, ib], axis=1)
    src = np.concatenate([np.zeros((T, Ma), int), np.ones((T, Mb), int)], axis=1)
    pi = np.where(src == 0, P_A[idx], P_B[idx])
    if mode == "plain":
        w = B[idx] / pi
    elif mode == "mis":
        k = np.array([Ma, Mb])[src]
        w = MIS[src, idx] * (Ma + Mb) / k * B[idx] / pi
    elif mode == "mis_nofix":
        w = MIS[src, idx] * B[idx] / pi
    ws = w.sum(axis=1)
    cdf = np.cumsum(w, axis=1) / ws[:, None]
    u = rng.random(T)
    sel = np.minimum((u[:, None] > cdf).sum(axis=1), Ma + Mb - 1)
    y = np.take_along_axis(idx, sel[:, None], axis=1)[:, 0]
    return F[y] * (ws / (Ma + Mb)) / B[y]


def separate(Ma, Mb, T, rng):
    out = 0.0
    for M, p in ((Ma, P_A), (Mb, P_B)):
        idx = rng.choice(N, size=(T, M), p=p)
        w = B[idx] / p[idx]
        ws = w.sum(axis=1)
        cdf = np.cumsum(w, axis=1) / ws[:, None]
        u = rng.random(T)
        sel = np.minimum((u[:, None] > cdf).sum(axis=1), M - 1)
        y = np.take_along_axis(idx, sel[:, None], axis=1)[:, 0]
        out = out + F[y] * (ws / M) / B[y]
    return out


CASES = [("合池，不带 MIS 权重", lambda M, T, r: pooled(M, M, T, r, "plain"), GREY),
         ("合池，带 MIS 权重但不补候选数", lambda M, T, r: pooled(M, M, T, r, "mis_nofix"), RED),
         ("合池，带 MIS 权重并补候选数", lambda M, T, r: pooled(M, M, T, r, "mis"), TEAL)]


def fig6_1():
    rng = np.random.default_rng(1)
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.1))
    names, means, stds, cols = [], [], [], []
    for lab, fn, col in CASES:
        e = fn(8, 150000, rng)
        names.append(lab)
        means.append(e.mean() / TRUTH)
        stds.append(e.std() / TRUTH)
        cols.append(col)
        print(f"{lab}: 偏差 {e.mean() / TRUTH - 1:+.4f}，相对标准差 {e.std() / TRUTH:.3f}")
    ax = axes[0]
    ax.barh(np.arange(len(names)), means, color=cols, height=0.6)
    ax.axvline(1.0, color=INK, ls=":", lw=1.0)
    ax.set_yticks(np.arange(len(names)))
    ax.set_yticklabels(names, fontsize=7.6)
    ax.set_xlabel("估计值 / 真值")
    ax.set_xlim(0, 1.20)
    ax.set_title("偏差", fontsize=9)
    ax = axes[1]
    ax.barh(np.arange(len(names)), stds, color=cols, height=0.6)
    ax.set_yticks(np.arange(len(names)))
    ax.set_yticklabels([])
    ax.set_xlabel("相对标准差")
    ax.set_title("方差", fontsize=9)
    save(fig, "fig6-1-merge.png")


def fig6_2():
    rng = np.random.default_rng(2)
    Ms = [2, 4, 8, 16, 32]
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for lab, fn, col in CASES:
        if "不补" in lab:
            continue
        v = [fn(m, 100000, rng).std() / TRUTH for m in Ms]
        ax.plot(Ms, v, "o-", ms=3.5, color=col, label=lab)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks(Ms)
    ax.set_xticklabels([str(m) for m in Ms])
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.set_xlabel("每种技术的候选数")
    ax.set_ylabel("相对标准差")
    ax.legend(loc="lower left", fontsize=7.6)
    save(fig, "fig6-2-variance.png")


fig6_1()
fig6_2()
print("真值", round(TRUTH, 3))
