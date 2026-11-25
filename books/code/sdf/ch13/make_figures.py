import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

VOX = 0.05      # 体素边长
WALL_H = 1.0
WALL_D = 0.75


def wall_sd(x, y):
    qx, qy = abs(x - WALL_D) - 0.05, abs(y - WALL_H / 2) - WALL_H / 2
    return np.hypot(max(qx, 0.0), max(qy, 0.0)) + min(max(qx, qy), 0.0)


# ---------------------------------------------------------------- 图 13-1
def fig13_1():
    ts = np.linspace(0.02, 6.0, 400)
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0))
    ax = axes[0]
    for deg, col in ((4, BLUE), (10, TEAL), (25, ACCENT)):
        th = np.deg2rad(deg)
        ax.plot(ts, np.tan(th) * ts, color=col, lw=1.6, label=f"半角 {deg} 度")
    ax.plot(ts, ts * 0 + 1.5 * VOX, color=GREY, ls=":", lw=1.1,
            label="最小半径 1.5 体素")
    ax.set_xlabel("到锥顶的距离 t")
    ax.set_ylabel("锥在该处的半径")
    ax.set_ylim(0, 2.6)
    ax.legend(loc="upper left", fontsize=7.4)
    panel_label(ax, "(a)", x=-0.15, y=1.06)

    ax = axes[1]
    for deg, col in ((4, BLUE), (10, TEAL), (25, ACCENT)):
        th = np.deg2rad(deg)
        r = np.maximum(np.tan(th) * ts, 1.5 * VOX)
        lvl = np.floor(np.log2(np.maximum(2 * r / VOX, 1.0)))
        ax.plot(ts, lvl, color=col, lw=1.7, label=f"半角 {deg} 度")
    ax.set_xlabel("到锥顶的距离 t")
    ax.set_ylabel("mip 层级")
    ax.set_ylim(0, 10)
    ax.legend(loc="lower right", fontsize=7.4)
    panel_label(ax, "(b)", x=-0.15, y=1.06)
    fig.tight_layout()
    save(fig, "fig13-1-cone-mip.png")


# ---------------------------------------------------------------- 图 13-2
def blocked_fraction(p, half_angle, n_dir=4000, rng=None):
    rng = rng or np.random.default_rng(2)
    ct = 1 - rng.random(n_dir) * (1 - np.cos(half_angle))
    phi = 2 * np.pi * rng.random(n_dir)
    st = np.sqrt(np.maximum(1 - ct ** 2, 0))
    dirs = np.stack([st * np.cos(phi), ct, st * np.sin(phi)], -1)
    blocked = np.zeros(n_dir, bool)
    for i in range(n_dir):
        d = dirs[i]
        if d[1] <= 0:
            blocked[i] = True
            continue
        t = 0.01
        for _ in range(200):
            q = p + d * t
            v = wall_sd(q[0], q[1])
            if v < 2e-3:
                blocked[i] = True
                break
            t += max(v, 0.01)
            if t > 4.0:
                break
    return blocked.mean()


def fig13_2():
    halves = np.deg2rad(np.linspace(1, 60, 40))
    fig, ax = plt.subplots(figsize=(6.4, 3.1))
    for x0, col in ((0.30, BLUE), (0.58, ACCENT)):
        p = np.array([x0, 0.0, 0.0])
        vals = [blocked_fraction(p, h, 1200) for h in halves]
        ax.plot(np.rad2deg(halves), vals, color=col, lw=1.8,
                label=f"着色点离墙 {(WALL_D - x0):.2f} 米")
    ax.set_xlabel("锥的半角（度）")
    ax.set_ylabel("锥内被遮挡的方向比例")
    ax.set_ylim(-0.03, 1.03)
    ax.legend(loc="lower right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig13-2-leak.png")


# ---------------------------------------------------------------- 图 13-3
def cone_ao(p, half_angle, n_cone=24, n_sub=40, rng=None):
    rng = rng or np.random.default_rng(9)
    ct = 1 - rng.random(n_sub) * (1 - np.cos(half_angle))
    phi = 2 * np.pi * rng.random(n_sub)
    st = np.sqrt(np.maximum(1 - ct ** 2, 0))
    dirs = np.stack([st * np.cos(phi), ct, st * np.sin(phi)], -1)
    occ = 0.0
    for d in dirs:
        t, hit = 0.01, False
        for _ in range(120):
            q = p + d * t
            v = wall_sd(q[0], q[1])
            if v < 2e-3:
                hit = True
                break
            t += max(v, 0.01)
            if t > 3.0:
                break
        occ += 1.0 if hit else 0.0
    return 1.0 - occ / len(dirs)


def fig13_3():
    rng = np.random.default_rng(21)
    xs = np.linspace(0.20, 1.30, 18)
    ref = [blocked_fraction(np.array([x, 0.0, 0.0]), np.pi / 2, 2500, rng) for x in xs]
    ref = 1 - np.array(ref)

    fig, ax = plt.subplots(figsize=(6.4, 3.1))
    ax.plot(xs, ref, color=INK, lw=2.1, label="半球参考")
    for deg, col in ((25, BLUE), (45, TEAL), (70, ACCENT)):
        vals = [cone_ao(np.array([x, 0.0, 0.0]), np.deg2rad(deg), 12, 140, rng) for x in xs]
        ax.plot(xs, vals, color=col, lw=1.5, ls="--", label=f"单条锥，半角 {deg} 度")
    ax.set_xlabel("着色点到墙的距离（沿地面）")
    ax.set_ylabel("可见性")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right", fontsize=7.2)
    fig.tight_layout()
    save(fig, "fig13-3-cone-ao.png")


if __name__ == "__main__":
    fig13_1()
    fig13_2()
    fig13_3()
