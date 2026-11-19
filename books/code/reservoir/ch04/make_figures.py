import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import ris

N = 64
B = ris.make_scene(N, 1, 3, "zipf")[0]
V = ris.visibility(N, 1, 3, 0.62, soft=False)[0]
F = B * V
TRUTH = F.sum()


def ris_estimate(M, rng, phat=None, shade_field=None):
    phat = B if phat is None else phat
    y, wsum = ris.ris_step(phat[None, :], M, rng)
    y = int(y[0])
    ph = max(phat[y], 1e-300)
    return F[y] * (wsum[0] / M) / ph


def fig4_1():
    rng = np.random.default_rng(1)
    Ms = [1, 4, 32]
    trials = 20000
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.9), sharey=True)
    tgt = B / B.sum()
    for ax, M in zip(axes, Ms):
        cnt = np.zeros(N)
        for _ in range(trials):
            y, _ = ris.ris_step(B[None, :], M, rng)
            cnt[int(y[0])] += 1
        order = np.argsort(-tgt)
        ax.bar(np.arange(N), cnt[order] / trials, color=SKY, width=0.85,
               edgecolor="none", label="选中频率" if M == Ms[0] else None)
        ax.plot(np.arange(N), tgt[order], color=ACCENT, lw=1.6,
                label="目标分布" if M == Ms[0] else None)
        ax.set_title(f"$M={M}$", fontsize=9)
        ax.set_xlabel("灯（按目标权重排序）")
        top = int(np.argmax(tgt))
        print(f"M={M} 最强灯选中频率 {cnt[top] / trials:.3f} 目标 {tgt[top]:.3f}")
    axes[0].set_ylabel("频率")
    axes[0].legend(loc="upper right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig4-1-approach.png")


def fig4_2():
    rng = np.random.default_rng(2)
    Ms = [1, 2, 4, 8, 16, 32, 64]
    trials = 30000
    ris_std, mc_std = [], []
    for M in Ms:
        e = np.array([ris_estimate(M, rng) for _ in range(trials)])
        ris_std.append(e.std() / TRUTH)
        e = np.array([N * np.mean(F[rng.integers(0, N, M)]) for _ in range(trials)])
        mc_std.append(e.std() / TRUTH)
        print(f"M={M} RIS {ris_std[-1]:.3f} 均匀 {mc_std[-1]:.3f}")

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3))
    ax = axes[0]
    ax.plot(Ms, mc_std, "s-", ms=4, color=BLUE, label="直接采样，$M$ 条阴影光线")
    ax.plot(Ms, ris_std, "o-", ms=4, color=ACCENT, label="RIS，$M$ 次灯求值 + 1 条阴影光线")
    ax.axhline(0.485, color=GREY, ls=":", lw=1.0)
    ax.text(1.0, 0.52, "按 $b$ 完美采样", fontsize=7, color=GREY)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("候选数 / 样本数 $M$")
    ax.set_ylabel("相对标准差")
    ax.legend(loc="lower left", fontsize=7)
    ax.set_ylim(0.2, 3)
    ax.set_title("同样的 $M$", fontsize=9)

    ax = axes[1]
    ray = 20.0
    mc_cost = [M * (1 + ray) for M in Ms]
    ris_cost = [M * 1.0 + ray for M in Ms]
    ax.plot(mc_cost, mc_std, "s-", ms=4, color=BLUE, label="直接采样")
    ax.plot(ris_cost, ris_std, "o-", ms=4, color=ACCENT, label="RIS")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("代价（1 次灯求值 = 1，1 条阴影光线 = 20）")
    ax.set_ylabel("相对标准差")
    ax.legend(loc="lower left", fontsize=7.5)
    ax.set_title("同样的代价", fontsize=9)
    fig.tight_layout()
    save(fig, "fig4-2-variance-M.png")


def fig4_3():
    rng = np.random.default_rng(3)
    M = 8
    trials = 40000
    phat = F                      # 目标函数里含可见性，出现零权重
    good, bad = [], []
    sg = sb = 0.0
    for i in range(1, trials + 1):
        sg += ris_estimate(M, rng, phat=phat)
        good.append(sg / i)
        # 错误做法：丢掉零权重候选，M 改成非零个数
        idx = rng.integers(0, N, M)
        w = phat[idx] * N
        nz = w > 0
        idx_nz = idx[nz]
        if idx_nz.size == 0:
            sb += 0.0
            bad.append(sb / i)
            continue
        ww = w[nz]
        p = ww / ww.sum()
        y = int(rng.choice(idx_nz, p=p))
        sb += F[y] * (ww.sum() / idx_nz.size) / phat[y]
        bad.append(sb / i)
    print(f"真值 {TRUTH:.2f} 正确 {good[-1]:.2f} 错误 {bad[-1]:.2f} 偏差 {(bad[-1]/TRUTH-1)*100:.1f}%")
    print("非零候选平均个数", np.mean([np.sum(rng.choice(F, M) > 0) for _ in range(2000)]))
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.plot(good, color=ACCENT, lw=1.4, label="按 RIS 定义实现")
    ax.plot(bad, color=RED, lw=1.4, label="丢掉零权重候选、$M$ 改成非零个数")
    ax.axhline(TRUTH, color=GREY, ls=":", lw=1.0)
    ax.text(trials * 0.02, TRUTH * 1.02, f"真值 {TRUTH:.1f}", fontsize=7.5, color=GREY)
    ax.set_xscale("log")
    ax.set_xlabel("累计估计次数")
    ax.set_ylabel("累计平均值")
    ax.legend(loc="lower right", fontsize=7.5)
    save(fig, "fig4-3-bias.png")


fig4_1()
fig4_2()
fig4_3()
