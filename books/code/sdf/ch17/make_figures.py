import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

R = 0.80
H = 48


def target(P):
    return np.linalg.norm(P, axis=-1) - R


class MLP:
    def __init__(self, seed=0):
        rng = np.random.default_rng(seed)
        self.W1 = rng.normal(0, 1 / np.sqrt(2), (2, H))
        self.b1 = np.zeros(H)
        self.W2 = rng.normal(0, 1 / np.sqrt(H), (H, H))
        self.b2 = np.zeros(H)
        self.W3 = rng.normal(0, 1 / np.sqrt(H), (H, 1))
        self.b3 = np.zeros(1)
        self.params = ["W1", "b1", "W2", "b2", "W3", "b3"]

    def forward(self, X):
        z1 = np.tanh(X @ self.W1 + self.b1)
        z2 = np.tanh(z1 @ self.W2 + self.b2)
        out = (z2 @ self.W3 + self.b3)[:, 0]
        return out, (X, z1, z2)

    def grads(self, X, cache, dout):
        X0, z1, z2 = cache
        g = {}
        g["W3"] = z2.T @ dout[:, None]
        g["b3"] = np.array([dout.sum()])
        dz2 = (dout[:, None] @ self.W3.T) * (1 - z2 ** 2)
        g["W2"] = z1.T @ dz2
        g["b2"] = dz2.sum(0)
        dz1 = (dz2 @ self.W2.T) * (1 - z1 ** 2)
        g["W1"] = X0.T @ dz1
        g["b1"] = dz1.sum(0)
        return g


def train(use_eik, iters=1400, lam=0.03, seed=0):
    rng = np.random.default_rng(seed)
    net = MLP(seed)
    m = {k: np.zeros_like(getattr(net, k)) for k in net.params}
    v = {k: np.zeros_like(getattr(net, k)) for k in net.params}
    lr, b1, b2 = 3e-3, 0.9, 0.999
    hist = []
    eps = 1e-3
    for it in range(iters):
        P = rng.uniform(-1.6, 1.6, (512, 2))
        y = target(P)
        pred, cache = net.forward(P)
        d = pred - y
        g = net.grads(P, cache, 2 * d / len(P))
        for k in net.params:
            m[k] = b1 * m[k] + (1 - b1) * g[k]
            v[k] = b2 * v[k] + (1 - b2) * g[k] ** 2
            mh = m[k] / (1 - b1 ** (it + 1))
            vh = v[k] / (1 - b2 ** (it + 1))
            setattr(net, k, getattr(net, k) - lr * mh / (np.sqrt(vh) + 1e-8))
        hist.append(float(np.mean(d ** 2)))
    return net, hist


def fig17_1():
    net_plain, h1 = train(False, seed=1)

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.1))
    ax = axes[0]
    ax.semilogy(h1, color=BLUE, lw=1.6)
    ax.set_xlabel("迭代次数")
    ax.set_ylabel("均方误差")
    panel_label(ax, "(a)", x=-0.15, y=1.06)

    ax = axes[1]
    X, Y = np.meshgrid(np.linspace(-1.4, 1.4, 320), np.linspace(-1.4, 1.4, 320))
    P = np.stack([X, Y], -1).reshape(-1, 2)
    f, _ = net_plain.forward(P)
    ax.contour(X, Y, f.reshape(X.shape), levels=[0.0], colors=BLUE, linewidths=1.7)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(R * np.cos(th), R * np.sin(th), color=INK, lw=1.4, ls="--")
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xticks([]); ax.set_yticks([])
    ax.plot([], [], color=BLUE, lw=1.7, label="网络的零等值线")
    ax.plot([], [], color=INK, lw=1.4, ls="--", label="解析圆")
    ax.legend(loc="lower right", fontsize=7.5)
    panel_label(ax, "(b)", x=-0.12, y=1.06)
    fig.tight_layout()
    save(fig, "fig17-1-mlp.png")


def fig17_2():
    net, _ = train(False, seed=2)
    rng = np.random.default_rng(3)
    P = rng.uniform(-1.2, 1.2, (4000, 2))
    eps = 1e-3
    fx1, _ = net.forward(P + np.array([eps, 0.0]))
    fx0, _ = net.forward(P - np.array([eps, 0.0]))
    fy1, _ = net.forward(P + np.array([0.0, eps]))
    fy0, _ = net.forward(P - np.array([0.0, eps]))
    g = np.hypot((fx1 - fx0) / (2 * eps), (fy1 - fy0) / (2 * eps))

    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.hist(np.clip(g, 0, 3), bins=80, color=BLUE, alpha=0.7, density=True)
    ax.axvline(1.0, color=RED, lw=1.6, ls="--")
    ax.text(1.05, 0.9 * ax.get_ylim()[1], "理想的 Eikonal 值", color=RED, fontsize=8)
    ax.set_xlabel(r"$\Vert\nabla f\Vert$")
    ax.set_ylabel("概率密度")
    fig.tight_layout()
    save(fig, "fig17-2-eikonal.png")


def fig17_3():
    net, _ = train(False, seed=4)
    X, Y = np.meshgrid(np.linspace(-1.3, 1.3, 400), np.linspace(-1.3, 1.3, 400))
    P = np.stack([X, Y], -1)
    f, _ = net.forward(P.reshape(-1, 2))
    err = np.abs(f.reshape(X.shape) - target(P))
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    im = ax.pcolormesh(X, Y, err, cmap="magma_r", shading="auto", vmin=0, vmax=0.12)
    ax.contour(X, Y, f.reshape(X.shape), levels=[0.0], colors="cyan", linewidths=1.2)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label("绝对误差", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    fig.tight_layout()
    save(fig, "fig17-3-error.png")


if __name__ == "__main__":
    fig17_1()
    fig17_2()
    fig17_3()
