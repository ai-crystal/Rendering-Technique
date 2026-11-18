import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import ris

N = 64
M = 8
G = 8


def vdc(i, base=2):
    """van der Corput 序列的第 i 个数。"""
    out, f = 0.0, 1.0
    while i > 0:
        f /= base
        out += f * (i % base)
        i //= base
    return out


def sets_for(mode, frame, rng):
    """返回 (G, G, M) 的候选下标。"""
    out = np.zeros((G, G, M), dtype=int)
    for i in range(G):
        for j in range(G):
            p = i * G + j
            if mode == "same":
                r = np.random.default_rng(frame)
                out[i, j] = r.integers(0, N, size=M)
            elif mode == "vdc":
                k = p * M
                out[i, j] = [int(vdc(k + s) * N) for s in range(M)]
            else:
                r = np.random.default_rng(p * 7919 + frame * 104729 + 17)
                out[i, j] = r.integers(0, N, size=M)
    return out


def overlap(mode, dist, trials=30):
    vals = []
    for t in range(trials):
        a = sets_for(mode, t, None)
        A = a[:, :-dist].reshape(-1, M)
        B = a[:, dist:].reshape(-1, M)
        inter = [len(set(x) & set(y)) for x, y in zip(A, B)]
        uni = [len(set(x) | set(y)) for x, y in zip(A, B)]
        vals.append(np.mean(np.array(inter) / np.array(uni)))
    return float(np.mean(vals))


def fig7_1():
    ds = [1, 2, 3, 4]
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    for mode, lab, col, mk in [
            ("same", "每帧一条序列，所有像素共用", RED, "o-"),
            ("hash", "每像素按坐标散列种子", TEAL, "s-")]:
        ys = [overlap(mode, d) for d in ds]
        ax.plot(ds, ys, mk, ms=4, color=col, label=lab)
        print(lab, " ".join(f"{y:.3f}" for y in ys))
    ax.set_xlabel("像素间距")
    ax.set_ylabel("候选集的 Jaccard 重叠率")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="center right")
    save(fig, "fig7-1-overlap.png")


def clamp_experiment(limit, M=8, frames=40, trials=250, cap=32):
    b = ris.make_scene(N, 1, 0, "zipf")[0]
    vis = ris.visibility(N, frames, 0, soft=True, lo=0.7, hi=1.0)
    mot = ris.motion_modulation(N, frames, 0.1, 0)
    truth = np.array([float((b * mot[t] * vis[t]).sum()) for t in range(frames)])
    errs = []
    for s in range(trials):
        rng = np.random.default_rng(2000 + s)
        prev, seq = None, []
        for t in range(frames):
            phat = b * mot[t]
            y, ws = ris.ris_step(phat[None, :], M, rng)
            cur = ris.Res(y, ws, np.array([M]), np.array([phat[y[0]]]))
            if prev is not None:
                phc = np.array([phat[prev.y[0]]])
                wb = min(float((prev.wsum * phc / prev.ph)[0]), limit)
                tot = cur.wsum + wb
                pick = rng.random(1) < wb / tot
                m_tot = int(cur.m[0] + prev.m[0])
                scale = min(1.0, cap / m_tot)
                cur = ris.Res(np.where(pick, prev.y, cur.y), tot * scale,
                              np.array([min(cap, m_tot)]),
                              np.where(pick, phc, cur.ph))
            seq.append(float(ris.shade(b[None, :], (vis[t] * mot[t])[None, :],
                                       cur, phat[None, :])[0]))
            prev = cur
        errs.append(np.array(seq) / truth - 1)
    e = np.array(errs)
    return float(e.mean()), float(e.std())


def fig7_2():
    limits = [128, 256, 512, 1024, 2048, 8192, 1e9]
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    bs, ss = [], []
    for L in limits:
        bm, bs_ = clamp_experiment(L)
        bs.append(bm * 100)
        ss.append(bs_ * 100)
        print(f"上限 {L:>9.0f}: 偏差 {bm * 100:+.2f}%  标准差 {bs_ * 100:.1f}%")
    x = np.arange(len(limits))
    ax.plot(x, np.abs(bs), "o-", ms=4, color=RED, label="偏差的绝对值")
    ax.plot(x, ss, "s-", ms=4, color=BLUE, label="标准差")
    ax.set_xticks(x)
    ax.set_xticklabels(["128", "256", "512", "1k", "2k", "8k", "不限"])
    ax.set_xlabel("历史权重和的上限")
    ax.set_ylabel("百分比（%）")
    ax.legend(loc="upper right")
    save(fig, "fig7-2-clamp.png")


fig7_1()
fig7_2()
