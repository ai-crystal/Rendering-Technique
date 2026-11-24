"""第 20 章插图：训练一个 RGB→谱线 的小型网络。

数据是合成谱线（见 neurolib）。流程：先 PCA 得基底，再学 RGB→系数。
所有数字都是真跑出来的，没有手编。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "spectral"))
from figstyle import *
import numpy as np
import speclib as S
import neurolib as N

LAM = N.LAM
NB = 12
rng = np.random.default_rng(5)


def train_mlp(x, y, hidden=64, iters=2500, lr=0.02, seed=0):
    r = np.random.default_rng(seed)
    W1 = r.normal(0, 1 / np.sqrt(x.shape[1]), (x.shape[1], hidden)); b1 = np.zeros(hidden)
    W2 = r.normal(0, 1 / np.sqrt(hidden), (hidden, hidden)); b2 = np.zeros(hidden)
    W3 = r.normal(0, 1 / np.sqrt(hidden), (hidden, y.shape[1])); b3 = np.zeros(y.shape[1])
    params = [W1, b1, W2, b2, W3, b3]
    mom = [np.zeros_like(p) for p in params]
    losses = []
    for _ in range(iters):
        idx = r.integers(0, x.shape[0], 256)
        xb, yb = x[idx], y[idx]
        h1 = np.tanh(xb @ W1 + b1)
        h2 = np.tanh(h1 @ W2 + b2)
        pred = h2 @ W3 + b3
        err = pred - yb
        losses.append(float(np.mean(err ** 2)))
        g3 = 2 * err / err.size
        gW3 = h2.T @ g3; gb3 = g3.sum(0)
        gh2 = (g3 @ W3.T) * (1 - h2 ** 2)
        gW2 = h1.T @ gh2; gb2 = gh2.sum(0)
        gh1 = (gh2 @ W2.T) * (1 - h1 ** 2)
        gW1 = xb.T @ gh1; gb1 = gh1.sum(0)
        for p, g, m in zip(params, [gW1, gb1, gW2, gb2, gW3, gb3], mom):
            m *= 0.9; m += g * 0.1; p -= lr * m
    return params, losses


def forward(params, x):
    W1, b1, W2, b2, W3, b3 = params
    h1 = np.tanh(x @ W1 + b1)
    h2 = np.tanh(h1 @ W2 + b2)
    return h2 @ W3 + b3


def rms(a, b):
    return float(np.sqrt(np.mean((a - b) ** 2)))


train_w = N.make_set(6000, "wide", 21)
test_w = N.make_set(1200, "wide", 22)
rgb_w, rgb_wt = N.to_rgb_batch(train_w), N.to_rgb_batch(test_w)
mean, basis = N.pca_basis(train_w, NB)
coef_w = (train_w - mean) @ basis.T

params, losses = train_mlp(rgb_w, coef_w)
pred_mlp = forward(params, rgb_wt)

A = np.hstack([rgb_w, np.ones((rgb_w.shape[0], 1))])
W_lin, *_ = np.linalg.lstsq(A, coef_w, rcond=None)
pred_lin = np.hstack([rgb_wt, np.ones((rgb_wt.shape[0], 1))]) @ W_lin

G = 8
flat = (np.clip((rgb_w * G).astype(int), 0, G - 1) * np.array([G * G, G, 1])).sum(1)
csum = np.zeros((G ** 3, NB)); cnt = np.zeros(G ** 3)
np.add.at(csum, flat, coef_w); np.add.at(cnt, flat, 1)
cmean = csum / np.maximum(cnt, 1)[:, None]
flat_t = (np.clip((rgb_wt * G).astype(int), 0, G - 1) * np.array([G * G, G, 1])).sum(1)
pred_bin = cmean[flat_t]

C3 = S.cie_xyz_basis(LAM) @ basis[:3].T
C3i = np.linalg.inv(C3)
xyz_t = np.stack([S.spectrum_to_xyz(LAM, s) for s in test_w[:200]])
pred_three = xyz_t @ C3i.T


def err(pred, spec=None, mu=mean, bs=basis):
    spec = test_w if spec is None else spec
  
    return float(np.mean([rms(mu + pred[i] @ bs, spec[i]) for i in range(200)]))


e_three = err(pred_three, bs=basis[:3])
e_lin = err(pred_lin)
e_bin = err(pred_bin)
e_mlp = err(pred_mlp)
e_oracle = float(np.mean([rms(mean + (test_w[i] - mean) @ basis.T @ basis, test_w[i])
                          for i in range(200)]))

train_n = N.make_set(4000, "narrow", 31)
test_n = N.make_set(800, "narrow", 32)
rgb_n, rgb_nt = N.to_rgb_batch(train_n), N.to_rgb_batch(test_n)
mean_n, basis_n = N.pca_basis(train_n, NB)
params_n, _ = train_mlp(rgb_n, (train_n - mean_n) @ basis_n.T, seed=1)
e_narrow = err(forward(params_n, rgb_nt), test_n, mean_n, basis_n)

print("three %.3f lin %.3f bin %.3f mlp %.3f oracle %.3f narrow %.3f"
      % (e_three, e_lin, e_bin, e_mlp, e_oracle, e_narrow))


def fig20_1():
    pts = np.array([S.xyz_to_xy(S.spectrum_to_xyz(LAM, s)) for s in train_w[:700]])
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    ax.plot([0.17, 0.08, 0.13, 0.21, 0.30, 0.42, 0.52, 0.58, 0.64, 0.64],
            [0.005, 0.09, 0.22, 0.33, 0.40, 0.43, 0.42, 0.39, 0.33, 0.33],
            color=LIGHT, lw=1.2)
    ax.scatter(pts[:, 0], pts[:, 1], s=4, color=ACCENT, alpha=0.45, linewidths=0)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_xlim(0, 0.75); ax.set_ylim(0, 0.85)
    ax.set_aspect("equal")
    ax.text(0.06, 0.76, "训练集的色度分布", color=INK, fontsize=9)
    save(fig, "fig20-1-coverage.png")


def fig20_2():
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    ax.plot(np.arange(1, len(losses) + 1), losses, color=BLUE, lw=0.9)
    ax.set_xlabel("迭代次数")
    ax.set_ylabel("训练均方误差（系数空间）")
    ax.set_xlim(0, len(losses))
    ax.set_ylim(min(losses) * 0.85, losses[0] * 1.05)
    ax.text(0.35, 0.72, "损失很快压到平台，剩下的差距由数据决定",
            transform=ax.transAxes, fontsize=8.3, color=GREY)
    save(fig, "fig20-2-loss.png")


def fig20_3():
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    for i, c in zip([0, 1, 2], [BLUE, TEAL, ACCENT]):
        ax.plot(LAM, test_w[i], color=c, lw=1.8, label="真实 %d" % (i + 1))
        ax.plot(LAM, np.clip(mean + pred_mlp[i] @ basis, 0, 1), color=c, lw=1.3,
                ls="--", label="预测 %d" % (i + 1))
    ax.set_xlabel("波长（nm）"); ax.set_ylabel("反射率")
    ax.set_xlim(380, 780); ax.set_ylim(0, 1.05)
    ax.legend(fontsize=7, ncol=2, loc="upper right")
    save(fig, "fig20-3-recon.png")


def fig20_4():
    labels = ["三系数解析", "线性回归", "分箱均值", "小型网络", "窄分布上的网络"]
    vals = [e_three, e_lin, e_bin, e_mlp, e_narrow]
    cols = [RED, GREY, TEAL, ACCENT, BLUE]
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    bars = ax.bar(range(len(vals)), vals, color=cols, width=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.006, "%.3f" % v,
                ha="center", fontsize=8.5, color=INK)
    ax.axhline(e_oracle, color=INK, ls=":", lw=1.1)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labels, fontsize=7.8)
    ax.set_ylabel("测试集重建 RMS")
    ax.set_ylim(0, max(vals) * 1.18)
    save(fig, "fig20-4-compare.png")


def fig20_5():
    spd = S.blackbody(LAM, 6500.0)
    spd = spd / spd.max()
    refl = (0.06 + 0.5 * np.exp(-0.5 * ((LAM - 620) / 45) ** 2)
            + 0.2 * np.exp(-0.5 * ((LAM - 450) / 60) ** 2))
    integrand = refl * spd * S.cie_y(LAM)
    trap = getattr(np, "trapezoid", None) or getattr(np, "trapz")
    exact = float(trap(integrand, LAM))
    qn = S.cie_y(LAM) / float(trap(S.cie_y(LAM), LAM))
    cdf = np.cumsum(qn)
    cdf /= cdf[-1]

    rng2 = np.random.default_rng(0)
    Ns = [4, 16, 64, 256]
    su, sq = [], []
    for n in Ns:
        u = rng2.random((3000, n))
        vals_u = np.interp(380 + 400 * u, LAM, integrand) * 400
        lq = np.interp(rng2.random((3000, n)), cdf, LAM)
        vals_q = np.interp(lq, LAM, integrand) / np.interp(lq, LAM, qn)
        su.append(float(vals_u.mean(1).std()))
        sq.append(float(vals_q.mean(1).std()))
    print("wavevar exact", round(exact, 3), "uniform", [round(x, 3) for x in su],
          "q", [round(x, 3) for x in sq])

    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    ax.loglog(Ns, su, marker="o", ms=4, color=GREY, lw=1.8, label="均匀分布")
    ax.loglog(Ns, sq, marker="s", ms=4, color=ACCENT, lw=1.8, label="按配色函数抽样")
    ax.loglog(Ns, [su[0] * np.sqrt(Ns[0] / n) for n in Ns], color=INK, ls=":", lw=1.0,
              label="斜率 −1/2 参考线")
    ax.set_xlabel("每像素的波长样本数")
    ax.set_ylabel("估计值的标准差")
    ax.legend(loc="lower left", fontsize=8)
    save(fig, "fig20-5-wavevar.png")


fig20_1()
fig20_2()
fig20_3()
fig20_4()
fig20_5()
