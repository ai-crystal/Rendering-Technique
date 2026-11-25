import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

# ---------------------------------------------------------------- 场景：地面 + 墙 + 球
WALL_D, WALL_H, WALL_T = 0.75, 1.0, 0.10


def sd_box2(x, y, cx, cy, hx, hy):
    qx, qy = abs(x - cx) - hx, abs(y - cy) - hy
    return np.hypot(max(qx, 0.0), max(qy, 0.0)) + min(max(qx, qy), 0.0)


def scene(p):
    x, y, z = p
    floor = y
    wall = sd_box2(x, y, WALL_D, WALL_H / 2, WALL_T / 2, WALL_H / 2)
    return min(floor, wall)


# ---------------------------------------------------------------- 图 11-1 AO
def ao_ref(p, n, n_dir=1500, rng=None):
    """半球方向均匀采样，逐方向在场景里步进，统计被遮挡的比例。"""
    rng = rng or np.random.default_rng(7)
    u = rng.random((n_dir, 2))
    ct = u[:, 0]
    phi = 2 * np.pi * u[:, 1]
    st = np.sqrt(1 - ct ** 2)
    a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
    t1 = np.cross(n, a); t1 /= np.linalg.norm(t1)
    t2 = np.cross(n, t1)
    dirs = st[:, None] * (np.cos(phi)[:, None] * t1 + np.sin(phi)[:, None] * t2)         + ct[:, None] * n
    blocked = np.zeros(n_dir, bool)
    for i in range(n_dir):
        d = dirs[i]
        if d[1] <= 0.0:
            blocked[i] = True
            continue
        t = 0.02
        for _ in range(120):
            q = p + d * t
            v = min(sd_box2(q[0], q[1], WALL_D, WALL_H / 2, WALL_T / 2, WALL_H / 2), 3.0)
            if v < 2e-3:
                blocked[i] = True
                break
            t += max(v, 0.01)
            if t > 3.0:
                break
    return 1.0 - blocked.mean()


def ao_sdf(p, n, scale=3.0, taps=5):
    occ, sca = 0.0, 1.0
    for i in range(taps):
        h = 0.02 + 0.30 * i / (taps - 1)
        d = scene(p + n * h)
        occ += (h - d) * sca
        sca *= 0.95
    return float(np.clip(1.0 - scale * occ, 0.0, 1.0))


def fig11_1():
    rng = np.random.default_rng(11)
    xs = np.linspace(0.15, 1.4, 26)
    mc, sdf = [], []
    for x in xs:
        p = np.array([x, 0.0, 0.0])
        n = np.array([0.0, 1.0, 0.0])
        mc.append(ao_ref(p, n, 1500, rng))
        sdf.append(ao_sdf(p, n))

    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(xs, mc, color=INK, lw=2.0, label="半球步进参考（1500 条）")
    ax.plot(xs, sdf, color=ACCENT, lw=1.6, ls="--", label="沿法线 5 次采样")
    ax.axvline(WALL_D, color=GREY, ls=":", lw=1.0)
    ax.text(WALL_D + 0.02, 0.94, "墙", fontsize=8, color=GREY)
    ax.set_xlabel("着色点到墙的距离（沿地面）")
    ax.set_ylabel("环境光可见性")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig11-1-ao.png")


# ---------------------------------------------------------------- 图 11-2 软阴影
LIGHT_C = np.array([0.0, 4.00, 0.0])
LIGHT_R = 1.00
SPH_C = np.array([0.0, 1.00, 0.0])
SPH_R = 0.30


def visibility_ref(p, n_samp=4000, rng=None):
    rng = rng or np.random.default_rng(3)
    # 在光源圆盘上均匀采样（法向沿 -y）
    r = LIGHT_R * np.sqrt(rng.random(n_samp))
    th = 2 * np.pi * rng.random(n_samp)
    lp = np.stack([LIGHT_C[0] + r * np.cos(th), np.full(n_samp, LIGHT_C[1]),
                   LIGHT_C[2] + r * np.sin(th)], -1)
    d = lp - p
    L2 = np.sum(d * d, axis=1)
    # 射线与球相交（单位化前）
    oc = p - SPH_C
    b = 2 * np.sum(d * oc, axis=1)
    c = oc @ oc - SPH_R ** 2
    disc = b * b - 4 * L2 * c
    hit = (disc > 0) & (-b - np.sqrt(np.maximum(disc, 0)) > 0) & \
          (-b - np.sqrt(np.maximum(disc, 0)) < 2 * L2)
    return 1.0 - hit.mean()


def sdf_scene_shadow(p):
    return float(np.linalg.norm(p - SPH_C) - SPH_R)


def soft_shadow_sdf(p, k, steps=96):
    Lv = LIGHT_C - p
    dist = np.linalg.norm(Lv)
    u = Lv / dist
    res, t = 1.0, 0.02
    for _ in range(steps):
        h = sdf_scene_shadow(p + u * t)
        res = min(res, k * h / t)
        t += np.clip(h, 0.02, 0.15)
        if res < 0.005 or t > dist:
            break
    return float(np.clip(res, 0.0, 1.0))


def fig11_2():
    rng = np.random.default_rng(5)
    xs = np.linspace(0.0, 1.8, 45)
    ref = [visibility_ref(np.array([x, 0.0, 0.0]), 3000, rng) for x in xs]

    fig, ax = plt.subplots(figsize=(6.5, 3.3))
    ax.plot(xs, ref, color=INK, lw=2.2, label="圆盘光源的可见比例（参考）")
    for k, col in ((8, BLUE), (16, TEAL), (48, RED)):
        ax.plot(xs, [soft_shadow_sdf(np.array([x, 0.0, 0.0]), k) for x in xs],
                color=col, lw=1.5, ls="--", label=f"SDF 软阴影，k = {k}")
    ax.set_xlabel("地面上沿 x 的位置")
    ax.set_ylabel("可见比例（0 为全影，1 为全亮）")
    ax.set_ylim(-0.05, 1.08)
    ax.legend(loc="upper right", fontsize=7.2)
    fig.tight_layout()
    save(fig, "fig11-2-soft-shadow.png")


# ---------------------------------------------------------------- 图 11-3 半影宽度
def penumbra_width(hs, rng):
    out = []
    for h in hs:
        globals()["SPH_C"] = np.array([0.0, h, 0.0])
        xs = np.linspace(-0.1, 2.4, 220)
        v = np.array([visibility_ref(np.array([x, 0.0, 0.0]), 1200, rng) for x in xs])
        # 只取单调上升的那一段
        k = np.searchsorted(xs, 0.0)
        vv = np.maximum(np.minimum.accumulate(v[::-1])[::-1], 0.0)
        x10 = np.interp(0.1, vv[k:], xs[k:])
        x90 = np.interp(0.9, vv[k:], xs[k:])
        out.append(max(x90 - x10, 1e-3))
    return np.array(out)


def fig11_3():
    hs = np.linspace(0.45, 1.35, 12)
    w = penumbra_width(hs, np.random.default_rng(17))
    # 几何预测：半影宽度 ≈ 2 R * h / (H - h)
    pred = 2 * LIGHT_R * hs / (LIGHT_C[1] - hs)

    fig, ax = plt.subplots(figsize=(6.3, 3.1))
    ax.plot(hs, w, "o-", color=BLUE, ms=4, lw=1.6, label="数值测得的 10%–90% 宽度")
    ax.plot(hs, pred, color=RED, lw=1.6, ls="--", label="几何预测 $2Rh/(H-h)$")
    ax.set_xlabel("遮挡球的高度 h")
    ax.set_ylabel("半影宽度（地面上）")
    ax.legend(loc="upper left", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig11-3-penumbra.png")


if __name__ == "__main__":
    fig11_1()
    fig11_2()
    fig11_3()
