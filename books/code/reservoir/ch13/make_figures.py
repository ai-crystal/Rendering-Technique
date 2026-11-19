import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import lab


def measure(M0, cap, seeds=12, T=24, **kw):
    sd = []
    for s in range(seeds):
        r = lab.sim(seed=s * 97, T=T, M0=M0, cap=cap, radius=1, **kw)
        st = lab.stats(r["est"][8:], r["truth"][8:])
        sd.append((st["relstd"], st["bias"]))
    a = np.array(sd)
    return a[:, 0].mean(), a[:, 1].mean()


def fig13_1():
    Ms = [1, 2, 4, 8, 16]
    caps = [8, 16, 32, 64, 128]
    grid = np.zeros((len(Ms), len(caps)))
    for i, m in enumerate(Ms):
        for j, c in enumerate(caps):
            rel, bia = measure(m, c)
            grid[i, j] = rel
            print(f"M0={m} cap={c} relstd={rel:.3f} bias={bia*100:+.1f}%")
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    im = ax.imshow(grid, cmap="YlGnBu_r", origin="lower", aspect="auto")
    for i in range(len(Ms)):
        for j in range(len(caps)):
            ax.text(j, i, f"{grid[i, j]:.2f}", ha="center", va="center", fontsize=7.5,
                    color="white" if grid[i, j] < grid.min() + 0.06 else INK)
    ax.set_xticks(range(len(caps)))
    ax.set_xticklabels(caps)
    ax.set_yticks(range(len(Ms)))
    ax.set_yticklabels(Ms)
    ax.set_xlabel("候选数上限 $M_{\\max}$")
    ax.set_ylabel("初始候选数 $M_0$")
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02)
    cb.set_label("相对标准差", fontsize=8)
    save(fig, "fig13-1-grid.png")


def fig13_2():
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for M0, col in [(1, RED), (2, ACCENT), (4, TEAL), (8, BLUE)]:
        errs = []
        for s in range(12):
            r = lab.sim(seed=s * 97, T=28, M0=M0, cap=20, radius=1)
            t = r["truth"]
            errs.append(np.sqrt(np.mean(((r["est"] - t) / t) ** 2, axis=1)))
        ax.plot(np.mean(errs, axis=0), color=col, label=f"$M_0={M0}$")
        print("M0", M0, "末帧误差", round(float(np.mean(errs, axis=0)[-1]), 3))
    ax.set_yscale("log")
    ax.set_xlabel("帧")
    ax.set_ylabel("相对均方根误差")
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    save(fig, "fig13-2-convergence.png")


def fig13_3():
    """稳态候选数与实测噪声的关系：候选数涨，噪声不降。"""
    pts = []
    for M0, cap in [(1, 10), (2, 10), (4, 20), (4, 50), (8, 20), (8, 50), (8, 100), (16, 100)]:
        r = lab.sim(seed=5, T=24, M0=M0, cap=cap, radius=1)
        m_ss = float(r["m"][-1].mean())
        rel, _ = measure(M0, cap, seeds=8)
        pts.append((m_ss, rel, M0, cap))
        print(f"M0={M0} cap={cap} 稳态 M={m_ss:.1f} relstd={rel:.3f}")
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-", ms=5, color=ACCENT)
    for m_ss, rel, M0, cap in pts:
        ax.annotate(f"{M0}/{cap}", (m_ss, rel), textcoords="offset points",
                    xytext=(4, 5), fontsize=7, color=GREY)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("稳态候选数 $M$（标注为 $M_0$/上限）")
    ax.set_ylabel("相对标准差")
    ax.set_ylim(0.3, 0.6)
    save(fig, "fig13-3-steadystate.png")


fig13_1()
fig13_2()
fig13_3()
