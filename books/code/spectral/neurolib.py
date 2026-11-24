"""神经光谱两章共用的合成数据与工具。

谱线由若干宽高斯叠加，再乘上若干窄吸收带，近似颜料材料的样子。
这不是真实测量数据，只用来演示"从三刺激值反推谱线"的流程。
"""
import numpy as np
import speclib as S

LAM = S.grid(380, 780, 1.0)
FAMILIES = {
    "wide": dict(k=(2, 4), sig=(18, 70), sat=(0.15, 1.0)),
    "narrow": dict(k=(2, 2), sig=(60, 110), sat=(0.45, 1.0)),
}


def random_spectrum(rng, family="wide"):
    p = FAMILIES[family]
    s = np.zeros_like(LAM)
    for _ in range(rng.integers(p["k"][0], p["k"][1] + 1)):
        mu = rng.uniform(410, 750)
        sig = rng.uniform(*p["sig"])
        s += rng.uniform(0.2, 1.0) * np.exp(-0.5 * ((LAM - mu) / sig) ** 2)
    s += rng.uniform(0.05, 0.2)
    s = s / s.max() * rng.uniform(*p["sat"])
    for _ in range(rng.integers(1, 4)):
        mu = rng.uniform(400, 740)
        sig = rng.uniform(5, 22)
        depth = rng.uniform(0.2, 0.7)
        s = s * (1 - depth * np.exp(-0.5 * ((LAM - mu) / sig) ** 2))
    return np.clip(s, 0, 1)


def make_set(n, family="wide", seed=0):
    rng = np.random.default_rng(seed)
    return np.array([random_spectrum(rng, family) for _ in range(n)])


def to_rgb_batch(spec):
    xyz = np.stack([S.spectrum_to_xyz(LAM, s) for s in spec])
    rgb = np.clip(xyz @ S.M_XYZ2RGB.T, 0, None)
    return rgb / np.maximum(rgb.max(axis=1, keepdims=True), 1e-6)


def pca_basis(spec, n):
    mean = spec.mean(axis=0)
    _, _, vt = np.linalg.svd(spec - mean, full_matrices=False)
    return mean, vt[:n]
