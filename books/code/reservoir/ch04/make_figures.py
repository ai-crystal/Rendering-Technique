import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import ris

N = 64
B2 = ris.make_scene(N, 2, 0, "zipf", 0.6)
BA, BB = B2[0], B2[1]
V = ris.visibility(N, 1, 3, soft=True, lo=0.7, hi=1.0)[0]
TRUTH = float(BA @ V)
M_A = 4


def merge_experiment(M, T, rng, mode="approx"):
    """把像素 B 的蓄水池并进 A。mode: none / approx / exact"""
    p = np.full(N, 1.0 / N)
    idx_b = rng.integers(0, N, size=(T, M))
    w_b = BB[idx_b] / p[idx_b]
    W_B = w_b.sum(axis=1)
    cdf = np.cumsum(w_b, axis=1) / W_B[:, None]
    u = rng.random(T)
    sel = np.minimum((u[:, None] > cdf).sum(axis=1), M - 1)
    y_b = np.take_along_axis(idx_b, sel[:, None], axis=1)[:, 0]

    if mode == "exact":
        W_in = (BA[idx_b] / p[idx_b]).sum(axis=1)
    elif mode == "approx":
        W_in = W_B * BA[y_b] / BB[y_b]
    else:
        W_in = W_B

    idx_a = rng.integers(0, N, size=(T, M_A))
    w_a = BA[idx_a] / p[idx_a]
    W_A = w_a.sum(axis=1)
    cdf_a = np.cumsum(w_a, axis=1) / W_A[:, None]
    ua = rng.random(T)
    sa = np.minimum((ua[:, None] > cdf_a).sum(axis=1), M_A - 1)
    y_a = np.take_along_axis(idx_a, sa[:, None], axis=1)[:, 0]

    tot = W_A + W_in
    y = np.where(rng.random(T) < W_in / tot, y_b, y_a)
    return V[y] * tot / (M_A + M)


def fig4_1():
    rng = np.random.default_rng(1)
    Ms = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    for mode, lab, col, mk in [("none", "不换算", RED, "v-"),
                               ("approx", "单点换算", ACCENT, "o-"),
                               ("exact", "逐候选换算", TEAL, "s-")]:
        bs = [merge_experiment(M, 150000, rng, mode).mean() / TRUTH - 1 for M in Ms]
        ax.plot(Ms, np.abs(bs) * 100, mk, ms=3.4, color=col, label=lab)
        print(f"{lab}: " + " ".join(f"{b * 100:+.1f}%" for b in bs))
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks(Ms)
    ax.set_xticklabels([str(m) for m in Ms])
    ax.set_yticks([0.05, 0.1, 0.5, 1, 2, 5, 10, 20])
    ax.set_yticklabels(["0.05", "0.1", "0.5", "1", "2", "5", "10", "20"])
    ax.set_xlabel("被合并蓄水池的候选数 M（本像素固定 4 个）")
    ax.set_ylabel("偏差的绝对值（百分比）")
    ax.legend(loc="upper right")
    save(fig, "fig4-1-merge-bias.png")


def cap_experiment(mode, M=8, frames=48, trials=400, cap=32):
    b = ris.make_scene(N, 1, 0, "zipf")[0]
    vis = ris.visibility(N, frames, 0, soft=True, lo=0.7, hi=1.0)
    mot = ris.motion_modulation(N, frames, 0.3, 0)
    out = []
    for s in range(trials):
        rng = np.random.default_rng(1000 + s)
        prev, seq = None, []
        for t in range(frames):
            phat = b * mot[t]
            y, ws = ris.ris_step(phat[None, :], M, rng)
            cur = ris.Res(y, ws, np.array([M]), np.array([phat[y[0]]]))
            if prev is not None:
                phc = np.array([phat[prev.y[0]]])
                if mode == "scale":
                    cur = ris.Res.combine(cur, prev, phc, cap, rng)
                elif mode == "keepM":
                    wb = prev.wsum * phc / prev.ph
                    tot = cur.wsum + wb
                    pick = rng.random(1) < wb / tot
                    cur = ris.Res(np.where(pick, prev.y, cur.y), tot,
                                  np.array([cap]), np.where(pick, phc, cur.ph))
                else:
                    if (cur.m + prev.m)[0] > cap:
                        prev = None
                    else:
                        cur = ris.Res.combine(cur, prev, phc, cap, rng)
            seq.append(float(ris.shade(b[None, :], (vis[t] * mot[t])[None, :],
                                       cur, phat[None, :])[0]))
            prev = cur
        out.append(seq)
    out = np.array(out)
    truth = np.array([float((b * mot[t] * vis[t]).sum()) for t in range(frames)])
    rel = (out / truth[None, :] - 1).mean(axis=0)
    return np.cumsum(rel) / np.arange(1, frames + 1)


def fig4_2():
    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    for mode, lab, col, mk in [("scale", "按比例缩放权重和", TEAL, "s-"),
                               ("drop", "超限时丢弃传入的蓄水池", BLUE, "o-"),
                               ("keepM", "只改 M，不缩放权重和", RED, "v-")]:
        m = cap_experiment(mode)
        ax.plot(np.arange(1, len(m) + 1), np.abs(m) * 100, mk, ms=3, color=col, label=lab)
        print(f"{lab}: 帧8 {m[7] * 100:+.2f}% 帧48 {m[-1] * 100:+.1f}%")
    ax.set_yscale("log")
    ax.set_xlabel("帧")
    ax.set_ylabel("累计偏差的绝对值（百分比）")
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.legend(loc="upper left")
    save(fig, "fig4-2-cap.png")


def fig4_3():
    rng = np.random.default_rng(3)
    f = BA * V
    order = np.argsort(-f)
    ks = [0, 1, 2, 4, 8, 16, 32]
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    xs, ys = [], []
    for k in ks:
        phat = BA.copy()
        phat[order[:k]] = 0.0
        T = 400000
        idx = rng.integers(0, N, size=(T, 8))
        w = phat[idx] * N
        ok = w.sum(axis=1) > 0
        cdf = np.cumsum(w, axis=1) / np.maximum(w.sum(axis=1), 1e-30)[:, None]
        u = rng.random(T)
        sel = np.minimum((u[:, None] > cdf).sum(axis=1), 7)
        y = np.take_along_axis(idx, sel[:, None], axis=1)[:, 0]
        val = BA[y] * V[y] * N * (w.sum(axis=1) / 8) / np.maximum(phat[y] * N, 1e-30)
        est = np.where(ok, val, 0.0)
        share = f[order[:k]].sum() / TRUTH
        bias = est.mean() / TRUTH - 1
        xs.append(share * 100)
        ys.append(bias * 100)
        print(f"k={k}: 被置零的贡献占比 {share * 100:.1f}%，实测偏差 {bias * 100:+.1f}%")
    ax.plot(xs, ys, "o-", ms=4, color=RED, label="实测")
    ax.plot([0, max(xs)], [0, -max(xs)], ls="--", color=GREY, lw=1.1, label="偏差等于负的缺失份额")
    ax.set_xlabel("目标函数为零、实际有贡献的那部分占比（%）")
    ax.set_ylabel("偏差（%）")
    ax.legend(loc="lower left")
    save(fig, "fig4-3-support.png")


fig4_1()
fig4_2()
fig4_3()
print("真值", round(TRUTH, 3))
