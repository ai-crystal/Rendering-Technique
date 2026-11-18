import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import *

# 二维场景：地面 y=0，墙 x=3，灯在 (2.4, 2.6)，遮挡球在 (1.2, 1.0)
WALL = 1.2
WALL_H = 2.4
LIGHT = np.array([0.75, 2.05])
R_LIGHT = 0.11
BLOCK = np.array([0.34, 0.42])
R_BLOCK = 0.12
ALB, LPOW = 0.8, 9.0


def hit_wall(p, w):
    """从 p 沿 w 打到墙 x=WALL，返回交点与距离；打不到返回 None。"""
    if w[0] <= 1e-6:
        return None
    t = (WALL - p[0]) / w[0]
    q = p + t * w
    if q[1] <= 0.0 or q[1] >= WALL_H:
        return None
    return q, t


def visible(a, b):
    """线段 a-b 是否被遮挡球挡住。"""
    d = b - a
    L2 = d @ d
    t = np.clip(((BLOCK - a) @ d) / L2, 0.0, 1.0)
    c = a + t * d
    return np.linalg.norm(c - BLOCK) > R_BLOCK


def contribution(p, alpha):
    """p 沿 alpha 的次级弹射贡献，返回 (值, 是否有效)。"""
    w = np.array([np.cos(alpha), np.sin(alpha)])
    h = hit_wall(p, w)
    if h is None:
        return 0.0
    q, t = h
    cos_p = w[1]
    if cos_p <= 0 or not visible(p, q):
        return 0.0
    if not visible(q, LIGHT):
        return 0.0
    d2 = (LIGHT - q) @ (LIGHT - q)
    cos_l = max(0.0, (q[0] - LIGHT[0]) / np.sqrt(d2))
    return ALB / np.pi * cos_p * LPOW * cos_l / (2.0 * np.pi * d2)


def truth(x, n=4000):
    a = (np.arange(n) + 0.5) / n * np.pi
    w = np.pi / n
    return float(sum(contribution(np.array([x, 0.0]), t) * w for t in a))


def sample_dir(rng, k):
    u = rng.random(k)
    return np.arcsin(u)          # 余弦加权在 [0, pi/2] 上的逆变换


def fig5_1():
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    ax.fill_between([-1.3, WALL], [-0.06, -0.06], [0, 0], color=INK)
    ax.fill_between([WALL, WALL + 0.06], [0, 0], [WALL_H, WALL_H], color=INK)
    th = np.linspace(0, 2 * np.pi, 100)
    ax.fill(LIGHT[0] + R_LIGHT * np.cos(th), LIGHT[1] + R_LIGHT * np.sin(th),
            color=GOLD)
    ax.fill(BLOCK[0] + R_BLOCK * np.cos(th), BLOCK[1] + R_BLOCK * np.sin(th),
            color=GREY)
    ax.text(LIGHT[0] + 0.05, LIGHT[1] - 0.22, "灯", fontsize=8, color=INK)
    ax.text(BLOCK[0] - 0.02, BLOCK[1] + 0.14, "遮挡体", fontsize=8, color=GREY)
    for x, col, lab, angs in [(-0.55, BLUE, "像素 i", (0.4, 0.8)),
                              (-0.10, ACCENT, "像素 j", (0.4, 0.8))]:
        p = np.array([x, 0.0])
        ax.plot(*p, "o", color=col, ms=4.5)
        ax.text(x, -0.14, lab, ha="center", fontsize=8, color=col)
        for a in angs:
            w = np.array([np.cos(a), np.sin(a)])
            h = hit_wall(p, w)
            if h is None:
                continue
            q = h[0]
            ok = visible(p, q) and visible(q, LIGHT)
            ax.plot([p[0], q[0]], [p[1], q[1]], lw=1.1,
                    color=col if ok else GREY, ls="-" if ok else ":")
            ax.plot(*q, "o", ms=3.2, color=col if ok else GREY,
                    mfc="white" if not ok else col)
    ax.set_xlim(-1.32, WALL + 0.1)
    ax.set_ylim(-0.24, WALL_H + 0.05)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    save(fig, "fig5-1-paths.png")


def fig5_2():
    rng = np.random.default_rng(7)
    xs = [-0.70, -0.50, -0.30, -0.10, 0.10, 0.30, 0.50]
    K, radius = 4, 2
    res = {"不复用": [], "复用并重算": [], "复用但沿用来源贡献": []}
    for trial in range(60):
        for mode in res:
            errs = []
            for i, x in enumerate(xs):
                est = 0.0
                for j in range(max(0, i - radius), min(len(xs), i + radius + 1)):
                    src = np.array([xs[j], 0.0])
                    for _ in range(K):
                        a = sample_dir(rng, 1)[0]
                        if mode == "复用但沿用来源贡献":
                            v = contribution(src, a)
                        else:
                            v = contribution(np.array([x, 0.0]), a)
                        est += v / np.cos(a) / K
                est /= (min(len(xs), i + radius + 1) - max(0, i - radius))
                errs.append(est / truth(x) - 1)
            res[mode].append(errs)
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    for (k, v), col, mk in zip(res.items(), [GREY, TEAL, RED], ["o-", "s-", "v-"]):
        arr = np.array(v)
        ax.plot(xs, arr.mean(axis=0) * 100, mk, ms=3.5, color=col, label=k)
        print(f"{k}: 平均偏差 {arr.mean() * 100:+.1f}%，RMS {np.sqrt((arr**2).mean()) * 100:.1f}%")
    ax.axhline(0, color=INK, lw=0.8, ls=":")
    ax.set_yscale("symlog", linthresh=10)
    ax.set_yticks([-100, -10, 0, 10, 100, 800])
    ax.set_yticklabels(["-100", "-10", "0", "10", "100", "800"])
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.set_xlabel("像素位置（x = 0.1 处是遮挡体的阴影边界）")
    ax.set_ylabel("估计值的相对误差（%）")
    ax.legend(loc="lower left", framealpha=0.9, frameon=True)
    save(fig, "fig5-2-reuse.png")


fig5_1()
fig5_2()
print("几个点的真值:", [round(truth(x), 4) for x in (-0.7, 0.0, 0.5)])
