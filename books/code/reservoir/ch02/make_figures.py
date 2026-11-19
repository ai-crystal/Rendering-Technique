import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *
import lab

TILT = 0.55
KF, KP = 60.0, 9.0


def fig2_1():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.2))
    r = np.logspace(-3, 3, 400)

    ax = axes[0]
    for power, lab_, col, ls in [(1.0, "平衡启发式（β = 1）", BLUE, "-"),
                                 (2.0, "幂启发式（β = 2）", ACCENT, "--")]:
        w = lab.mis_weights_curve(r, power, c=0.5)
        ax.plot(r, w, ls, color=col, label=lab_)
    ax.set_xscale("log")
    ax.set_xlabel("密度比 $p_{\\mathrm{light}}/p_{\\mathrm{bsdf}}$")
    ax.set_ylabel("灯采样的份额 $w_{\\mathrm{light}}$")
    ax.set_ylim(-0.02, 1.05)
    ax.legend(loc="upper left")
    ax.set_title("两个技术", fontsize=9)

    ax = axes[1]
    p1 = np.logspace(-4, 1, 400)
    p2 = np.full_like(p1, 0.5)
    p3 = np.full_like(p1, 0.05)
    tot = p1 + p2 + p3
    ax.plot(p1, p1 / tot, color=BLUE, label="$w_1$")
    ax.plot(p1, p2 / tot, color=ACCENT, ls="--", label="$w_2$")
    ax.plot(p1, p3 / tot, color=GREEN, ls=":", label="$w_3$")
    ax.plot(p1, tot / tot, color=GREY, lw=3.0, alpha=0.45, label="$w_1+w_2+w_3$")
    ax.axvline(0.5, color=LIGHT, lw=1.0)
    ax.text(0.6, 0.90, "$p_1=p_2$", fontsize=7.5, color=GREY)
    ax.set_xscale("log")
    ax.set_xlabel("技术 1 的密度 $p_1$（$p_2=0.5$，$p_3=0.05$）")
    ax.set_ylabel("份额")
    ax.set_ylim(-0.03, 1.06)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, fontsize=7.5)
    ax.set_title("三个技术：份额之和恒为 1", fontsize=9)
    fig.tight_layout()
    save(fig, "fig2-1-weights.png")


def fig2_2():
    has = np.array([0.08, 0.11, 0.15, 0.20, 0.27, 0.36, 0.48, 0.64, 0.85, 1.10, 1.40])
    res = {"light": [], "bsdf": [], "mis": [], "one": []}
    for ha in has:
        r = lab.mis_mc(KF, KP, half_angle=ha, tilt=TILT, trials=120000, seed=5)
        for k in res:
            res[k].append(r[k]["relstd"])
        print(f"ha={ha:.2f} truth={r['truth']:.4f} " +
              " ".join(f"{k}={r[k]['relstd']:.3f}" for k in res))

    fig, ax = plt.subplots(figsize=(6.3, 3.9))
    lab_map = [("light", "只做灯采样", ACCENT, "o-"),
               ("bsdf", "只做叶瓣采样", BLUE, "s-"),
               ("mis", "MIS，每个技术一个样本", TEAL, "-"),
               ("one", "单样本 MIS（一个样本）", PURPLE, "--")]
    for k, lab_, col, st in lab_map:
        if k == "mis":
            ax.plot(has, res[k], "-", lw=4.2, alpha=0.45, color=TEAL, label=lab_)
        else:
            ax.plot(has, res[k], st, ms=4, color=col, label=lab_)
    ax.set_yscale("log")
    ax.set_xlabel("灯的半角（弧度）")
    ax.set_ylabel("估计值的相对标准差")
    ax.set_ylim(0.03, 30)
    ax.axvspan(0.08, 0.2, color=LIGHT, alpha=0.35, lw=0)
    ax.text(0.14, 0.04, "小灯", ha="center", fontsize=8, color=GREY)
    ax.text(1.2, 0.04, "大灯", ha="center", fontsize=8, color=GREY)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=7.5)
    save(fig, "fig2-2-crossover.png")


def budget_four(ha, trials=120000, seed=7):
    """4 个样本的预算，四种分法。"""
    rng = np.random.default_rng(seed)
    ol = 2 * np.pi * (1 - np.cos(ha))
    ax_ = (np.sin(TILT), 0.0, np.cos(TILT))

    out = {}
    # 四个灯样本
    d = lab.sample_cone(ha, TILT, rng, (trials, 4))
    f = lab.f_lobe(d, KF, ax_, ha)
    pl = np.full_like(f, 1.0 / ol)
    pb = lab.p_lobe(d, KP)
    out["4 个灯样本"] = (f / pl).mean(axis=1)
    # 四个叶瓣样本
    d2 = lab.sample_lobe(KP, rng, (trials, 4))
    f2 = lab.f_lobe(d2, KF, ax_, ha)
    p2 = lab.p_lobe(d2, KP)
    out["4 个叶瓣样本"] = (f2 / p2).mean(axis=1)
    # 2 + 2 的 MIS
    wl_l = pl / (pl + pb)
    p_light_b = ((d2 @ np.asarray(ax_)) > np.cos(ha)) / ol
    wl_b = p_light_b / (p_light_b + p2 + 1e-30)
    out["MIS，2 + 2"] = 0.5 * ((wl_l * f / pl).mean(axis=1) + (wl_b * f2 / p2).mean(axis=1))
    # 4 个单样本 MIS
    pick = rng.random((trials, 4)) < 0.5
    mix_l = 0.5 * pl + 0.5 * pb
    mix_b = 0.5 * p_light_b + 0.5 * p2
    v = np.where(pick, f / mix_l, f2 / mix_b)
    out["单样本 MIS，4 个"] = v.mean(axis=1)
    truth = lab.mis_study(KF, KP, ha, TILT)["I"]
    return truth, {k: (np.mean(v), np.std(v) / truth) for k, v in out.items()}


def fig2_3():
    has = [0.15, 0.40, 1.00]
    labels = ["4 个灯样本", "4 个叶瓣样本", "MIS，2 + 2", "单样本 MIS，4 个"]
    shades = [(0.32, "半角 0.15"), (0.58, "半角 0.40"), (0.88, "半角 1.00")]
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    width = 0.26
    for j, (ha, (al, name)) in enumerate(zip(has, shades)):
        truth, res = budget_four(ha)
        xs = np.arange(len(labels)) + (j - 1) * width
        vals = [res[l][1] for l in labels]
        ax.bar(xs, vals, width=width * 0.92, color=ACCENT, alpha=al,
               edgecolor="white", linewidth=0.5, label=name)
        for x, v in zip(xs, vals):
            ax.text(x, v * 1.05, f"{v:.2f}", ha="center", va="bottom", fontsize=6.6)
        print(f"ha={ha:.2f} truth={truth:.4f}", {k: round(v[1], 3) for k, v in res.items()})
    ax.set_yscale("log")
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("相对标准差（4 个样本）")
    ax.set_ylim(0.07, 12)
    ax.legend(loc="upper left", fontsize=7.5, title="灯的半角", title_fontsize=7.5)
    save(fig, "fig2-3-budget.png")


fig2_1()
fig2_2()
fig2_3()
