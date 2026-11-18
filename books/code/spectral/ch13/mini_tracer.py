import numpy as np

LMIN, LMAX = 380.0, 780.0
NW = 4                                     # 每条路径的波长数


# ---------------------------------------------------------------- 波长组
def sample_wavelengths(rng, n=None):
    n = NW if n is None else n
    hero = rng.uniform(LMIN, LMAX)
    step = (LMAX - LMIN) / n
    lams = LMIN + np.mod(hero - LMIN + step * np.arange(n), LMAX - LMIN)
    return lams, np.full(n, 1.0 / (LMAX - LMIN))


# ---------------------------------------------------------------- 配色函数（解析拟合）
def _g(lam, mu, s):
    return np.exp(-0.5 * ((lam - mu) / s) ** 2)


def cmf(lam):
    x = 0.362 * _g(lam, 442.0, 16.0) + 1.056 * _g(lam, 599.8, 37.9) - 0.065 * _g(lam, 501.1, 20.4)
    y = 0.821 * _g(lam, 568.8, 46.9) + 0.286 * _g(lam, 530.9, 16.3)
    z = 1.217 * _g(lam, 437.0, 11.8) + 0.681 * _g(lam, 459.0, 26.0)
    return np.stack([x, y, z], axis=-1)


# ---------------------------------------------------------------- 场景
SPHERE_C, SPHERE_R = np.array([0.0, 0.0, 3.0]), 1.0
LIGHT_P = np.array([2.0, 3.0, 1.5])


def sphere_albedo(lam):
    return 0.05 + 0.90 * np.exp(-0.5 * ((lam - 560.0) / 45.0) ** 2)


def plane_albedo(lam):
    return np.full_like(lam, 0.55)


def light_spd(lam):
    return np.exp(-0.5 * ((lam - 452.0) / 12.0) ** 2) + np.exp(-0.5 * ((lam - 611.0) / 12.0) ** 2)


def intersect(o, d):
    """返回 (t, 法线, 反射率函数)，取最近的交点。"""
    best = (np.inf, None, None)
    oc = o - SPHERE_C
    a = d @ d
    b = 2 * oc @ d
    c = oc @ oc - SPHERE_R ** 2
    disc = b * b - 4 * a * c
    if disc > 0:
        t = (-b - np.sqrt(disc)) / (2 * a)
        if 1e-4 < t < best[0]:
            p = o + t * d
            best = (t, (p - SPHERE_C) / SPHERE_R, sphere_albedo)
    if abs(d[1]) > 1e-9:
        t = -o[1] / d[1]
        if 1e-4 < t < best[0]:
            best = (t, np.array([0.0, 1.0, 0.0]), plane_albedo)
    return best


def trace(o, d, lams):
    """单条路径：只算一次直接光照，返回每个波长的辐亮度。"""
    t, nrm, albedo = intersect(o, d)
    if nrm is None:
        return np.zeros_like(lams)
    p = o + t * d
    if nrm @ d > 0:
        nrm = -nrm
    L = LIGHT_P - p
    dist2 = L @ L
    cos_p = max(0.0, nrm @ (L / np.sqrt(dist2)))
    # 阴影射线
    tn, _, _ = intersect(p + 1e-4 * nrm, L / np.sqrt(dist2))
    vis = 0.0 if tn < np.sqrt(dist2) - 1e-3 else 1.0
    irr = vis * cos_p / dist2
    return albedo(lams) / np.pi * light_spd(lams) * irr


# ---------------------------------------------------------------- 渲染
def render(w=48, h=36, spp=16, seed=0):
    rng = np.random.default_rng(seed)
    film = np.zeros((h, w, 3))
    eye = np.array([0.0, 1.0, 0.0])
    for _ in range(spp):
        lams, pdf = sample_wavelengths(rng)
        for j in range(h):
            for i in range(w):
                u = (i + 0.5) / w * 2 - 1
                v = 1 - (j + 0.5) / h * 2
                d = np.array([u * 1.2, v * 0.9, 1.0])
                d /= np.linalg.norm(d)
                S = trace(eye, d, lams)
                xyz = (cmf(lams) * S[:, None] / pdf[:, None]).mean(axis=0)
                film[j, i] += xyz
    return film / spp


if __name__ == "__main__":
    img = render(spp=8)
    print("image range", img.min(), img.max())
    print("center xyz", img[18, 24])
