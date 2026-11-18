import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import ris


def scene_at(n_lights, profile, seed=3, lit=0.75):
    """取单个着色点，返回 b（无阴影贡献）与 v（可见性）。"""
    b = ris.make_scene(n_lights, 1, seed, profile)[0]
    v = ris.visibility(n_lights, 1, seed, p_lit=lit, soft=False)[0]
    return b, v


def fig1_1():
    Ns = np.unique(np.round(np.geomspace(4, 512, 22)).astype(int))
    K = 16
    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    for prof, lab, col in [("uniform", "功率相同", BLUE),
                           ("zipf", "功率按 1/i 递减", ACCENT),
                           ("spike", "一盏主灯 + 若干弱灯", RED)]:
        ys = []
        for n in Ns:
            rs = []
            for sd in range(8):
                b, v = scene_at(n, prof, seed=3 + sd)
                var = ris.var_uniform(b[None, :], v, K)[0]
                rs.append(np.sqrt(var) / (b @ v))
            ys.append(np.mean(rs))
        ax.plot(Ns, ys, "o-", ms=3, color=col, label=lab)
    ax.axhline(0.05, color=GREY, ls=":", lw=1.0)
    ax.text(Ns[-1], 0.055, "5% 误差", ha="right", va="bottom", color=GREY, fontsize=8)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_yticks([0.05, 0.1, 0.2, 0.5, 1.0, 2.0])
    ax.set_yticklabels(["0.05", "0.1", "0.2", "0.5", "1", "2"])
    ax.set_ylim(0.035, 3.0)
    ax.set_xlabel("灯的数量 $N$")
    ax.set_ylabel("估计值的相对标准差")
    ax.legend(loc="upper left")
    save(fig, "fig1-1-relstd-vs-N.png")


def fig1_2():
    N = 128
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    for prof, lab, col in [("uniform", "功率相同", BLUE),
                           ("zipf", "功率按 1/i 递减", ACCENT),
                           ("spike", "一盏主灯 + 若干弱灯", RED)]:
        b, v = scene_at(N, prof)
        f = np.sort(b * v)[::-1]
        cum = np.cumsum(f) / f.sum()
        x = np.arange(1, N + 1) / N
        ax.plot(x, cum, color=col, label=lab)
        neff = f.sum() ** 2 / (f ** 2).sum()
        print(f"{prof}: N_eff={neff:.1f}  前10%的灯占{cum[int(0.1 * N) - 1] * 100:.0f}%")
    ax.plot([0, 1], [0, 1], color=GREY, ls=":", lw=1.0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("按贡献排序后的灯的比例")
    ax.set_ylabel("累计贡献占比")
    ax.legend(loc="lower right")
    save(fig, "fig1-2-pareto.png")


def fig1_3():
    Ns = np.unique(np.round(np.geomspace(4, 512, 18)).astype(int))
    rng = np.random.default_rng(0)
    fig, ax = plt.subplots(figsize=(6.3, 3.6))
    res = {"均匀选灯": [], "按无阴影贡献选灯": [], "RIS，8 个候选": []}
    for n in Ns:
        b, v = scene_at(n, "zipf")
        f = b * v
        I = f.sum()
        res["均匀选灯"].append(np.sqrt(ris.var_uniform(b[None, :], v, 1)[0]) / I)
        p = b / b.sum()
        res["按无阴影贡献选灯"].append(np.sqrt(np.sum(f ** 2 / p) - I ** 2) / I)
        est = []
        for _ in range(1500):
            y, ws = ris.ris_step(b[None, :], 8, rng)
            est.append(float(ris.shade(b[None, :], v[None, :],
                                       ris.Res(y, ws, np.array([8]), np.array([b[y[0]]])),
                                       b[None, :])[0]))
        res["RIS，8 个候选"].append(np.std(est) / I)
    for (k, ys), col, st in zip(res.items(), [BLUE, TEAL, ACCENT],
                                ["o-", "s-", "D-"]):
        ax.plot(Ns, ys, st, ms=3.2, color=col, label=k, lw=1.6)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_yticks([0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 4])
    ax.set_yticklabels(["0.02", "0.05", "0.1", "0.2", "0.5", "1", "2", "4"])
    ax.set_xlabel("灯的数量 $N$")
    ax.set_ylabel("相对标准差")
    ax.legend(loc="upper left")
    save(fig, "fig1-3-strategies.png")


fig1_1()
fig1_2()
fig1_3()

rng = np.random.default_rng(7)
for n in (16, 64, 256, 512):
    b, v = scene_at(n, "zipf")
    f = b * v
    I = f.sum()
    print(f"N={n} relstd(K=16)={np.sqrt(ris.var_uniform(b[None, :], v, 16)[0]) / I:.3f}"
          f"  Neff={I ** 2 / (f ** 2).sum():.1f}  fmax/tot={f.max() / I:.3f}")
    p = b / b.sum()
    print(f"    importance K=1 relstd={np.sqrt(np.sum(f**2/p)-I**2)/I:.3f}"
          f"  K_for_1pct_uniform={(np.sqrt(ris.var_uniform(b[None,:],v,1)[0])/I/0.01)**2:.0f}"
          f"  K_for_1pct_is={(np.sqrt(np.sum(f**2/p)-I**2)/I/0.01)**2:.0f}")
    est=[]
    for _ in range(20000):
        y, ws = ris.ris_step(b[None, :], 8, rng)
        est.append(float(ris.shade(b[None, :], v[None, :], ris.Res(y, ws, np.array([8]), np.array([b[y[0]]])), b[None, :])[0]))
    print(f"    RIS M=8 relstd={np.std(est)/I:.3f}")
