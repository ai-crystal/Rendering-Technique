import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import lab
import ris

N = 64
B = ris.make_scene(N, 1, 3, "zipf")[0]
V = ris.visibility(N, 1, 3, 0.62, soft=False)[0]
F = B * V
TRUTH = F.sum()


def fig6_1():
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3))

    ax = axes[0]
    M = 8
    x = rng.integers(0, N, M)
    w = np.sort(B[x] * N)[::-1]
    W = w.sum()
    i = 0                                  # 例子里挑中的是权重最大那个
    ax.bar(np.arange(M), w, color=SKY, width=0.65, edgecolor="none")
    ax.axhline(W / M, color=ACCENT, lw=1.6)
    ax.axhline(w[i], color=RED, lw=1.2, ls="--")
    ax.text(M - 0.6, W / M * 1.06, "$\hat W/M$", color=ACCENT, fontsize=8, ha="right")
    ax.text(M - 0.6, w[i] * 0.86, "$w(y)$", color=RED, fontsize=8, ha="right")
    ax.set_yscale("log")
    ax.set_xlabel("候选（按权重排序）")
    ax.set_ylabel("权重 $w=\hat p/p$")
    ax.set_title("$M=8$ 的一个例子", fontsize=9)

    ax = axes[1]
    for M, col in [(4, SKY), (16, BLUE), (64, PURPLE)]:
        vals = []
        for _ in range(40000):
            x = rng.integers(0, N, M)
            w = B[x] * N
            W = w.sum()
            i = rng.choice(M, p=w / W)
            vals.append((W / M) / w[i])
        vals = np.array(vals)
        ax.hist(vals, bins=np.logspace(-1.2, 1.0, 70), histtype="step", lw=1.4,
                color=col, density=True, label=f"$M={M}$")
        print(f"M={M} 中位数 {np.median(vals):.2f} 均值 {vals.mean():.2f} 变异系数 {vals.std()/vals.mean():.3f}")
    ax.axvline(1.0, color=INK, ls=":", lw=1.0)
    ax.set_xscale("log")
    ax.set_xlabel("$(\hat W/M)/w(y)$")
    ax.set_ylabel("密度")
    ax.legend(loc="upper right")
    ax.set_title("括号与选中权重之比", fontsize=9)
    fig.tight_layout()
    save(fig, "fig6-1-bracket.png")


def fig6_2():
    rng = np.random.default_rng(1)
    p = np.full(N, 1.0 / N)
    Ms = [1, 2, 4, 8, 16, 32, 64, 128]
    sel, cand = [], []
    for M in Ms:
        inner, outer = [], []
        for _ in range(20000):
            x = rng.integers(0, N, M)
            w = B[x] * N
            W = w.sum()
            vals = (W / M) * F[x] / (B[x] * N)
            probs = w / W
            EF = np.dot(probs, vals)
            inner.append(np.dot(probs, vals ** 2) - EF ** 2)
            outer.append(EF)
        inner = np.array(inner)
        outer = np.array(outer)
        sel.append(inner.mean())
        cand.append(outer.var())
        print(f"M={M} 选择项 {sel[-1]:.3f} 候选集项 {cand[-1]:.3f} 合计 {sel[-1]+cand[-1]:.3f}")

    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    tot = np.array(sel) + np.array(cand)
    ax.plot(Ms, cand, "s-", ms=4, color=SKY, label="候选集噪声 $\mathrm{Var}(\mathbb{E}[F\mid S])$")
    ax.plot(Ms, sel, "o-", ms=4, color=ACCENT, label="选择噪声 $\mathbb{E}[\mathrm{Var}(F\mid S)]$")
    ax.plot(Ms, tot, "k-", lw=1.0, label="合计")
    ax.axhline(0.19, color=GREY, ls=":", lw=1.0)
    ax.text(1.1, 0.205, "选择噪声的渐近值 0.19", fontsize=7.5, color=GREY)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("候选数 $M$")
    ax.set_ylabel("方差（绝对量）")
    ax.set_ylim(0, 2.45)
    ax.legend(loc="upper right", fontsize=7.5)
    save(fig, "fig6-3-decomp.png")


def fig6_3():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3))

    ax = axes[0]
    amps = [0.1, 0.25, 0.4, 0.55, 0.7]
    for ratio, lab_, col, mk in [(True, "按当前帧重新评估", ACCENT, "o"),
                                 (False, "直接用上一帧的权重和", BLUE, "s")]:
        ys = []
        for a in amps:
            bs = []
            for s in range(20):
                r = lab.sim(seed=s * 97, T=24, M0=4, cap=20, radius=0,
                            spatial=False, temporal=True, ratio=ratio,
                            amp=a, motion="ramp")
                bs.append(lab.stats(r["est"][8:], r["truth"][8:])["bias"])
            ys.append(np.mean(bs) * 100)
            print("amp", a, "ratio", ratio, "bias%", round(ys[-1], 2))
        ax.plot(amps, ys, mk + "-", ms=4, color=col, label=lab_)
    ax.set_xlabel("运动幅度")
    ax.set_ylabel("相对亮度偏差（%）")
    ax.legend(loc="lower left", fontsize=7.5)
    ax.set_title("时间复用", fontsize=9)

    ax = axes[1]
    radii = [1, 2, 3]
    for ratio, lab_, col, mk in [(True, "按邻居的目标函数换算", ACCENT, "o"),
                                 (False, "直接用邻居的权重和", BLUE, "s")]:
        ys = []
        for rr in radii:
            bs = []
            for s in range(20):
                r = lab.sim(seed=s * 97, T=24, M0=4, cap=20, radius=rr, ratio=ratio)
                bs.append(lab.stats(r["est"][8:], r["truth"][8:])["bias"])
            ys.append(np.mean(bs) * 100)
            print("radius", rr, "ratio", ratio, "bias%", round(ys[-1], 2))
        ax.plot(radii, ys, mk + "-", ms=4, color=col, label=lab_)
    ax.set_xlabel("复用半径 $r$")
    ax.set_ylabel("相对亮度偏差（%）")
    ax.legend(loc="upper left", fontsize=7.5)
    ax.set_title("空间复用", fontsize=9)
    fig.tight_layout()
    save(fig, "fig6-2-motion.png")


def numbers():
    rng = np.random.default_rng(5)
    for M in (4, 16):
        prod, Fs = [], []
        for _ in range(30000):
            x = rng.integers(0, N, M)
            w = B[x] * N
            W = w.sum()
            i = rng.choice(M, p=w / W)
            Fs.append((W / M) * F[i] / B[i])
            prod.append((W / M) * (F[i] / B[i]))
        print(f"M={M} E[F]={np.mean(Fs):.2f} 真值 {TRUTH:.2f}  E[W/M]*E[f/phat]={np.mean([W/ M]) if False else 0}")


fig6_1()
fig6_2()
fig6_3()
