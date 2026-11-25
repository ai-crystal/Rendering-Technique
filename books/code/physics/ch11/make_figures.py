import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def fig11_1():
    rng = np.random.default_rng(7)
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    x, y = 0.0, 0.0
    xs, ys = [x], [y]
    for _ in range(60):
        x += rng.uniform(0.05, 0.16)
        y += rng.normal(0, 0.12)
        xs.append(x); ys.append(y)
    ax.plot(xs, ys, color=SKY, lw=0.8)
    ax.plot([0, xs[-1]], [0, ys[-1]], color=RED, lw=1.8)
    ax.annotate("漂移", (xs[-1], ys[-1]), xytext=(xs[-1] - 0.5, ys[-1] - 0.55),
                fontsize=8.5, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
    ax.annotate("热运动 + 碰撞", (xs[22], ys[22]), xytext=(xs[22] - 0.3, ys[22] + 0.55),
                fontsize=8, color=SKY)
    ax.annotate("", xy=(-0.05, 0.75), xytext=(0.25, 0.75),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=8))
    ax.text(0.28, 0.78, "$\\mathbf{E}$", fontsize=9, color=INK)
    ax.set_xlim(-0.2, 6.4)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("沿导线方向的位置")
    ax.set_yticks([])
    ax.grid(False)
    save(fig, "fig11-1-drift.png")


def fig11_2():
    rho0 = 1.68e-8
    alpha = 3.9e-3
    T = np.linspace(0, 100, 300)
    rho = rho0 * (1 + alpha * (T - 20))
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9))
    ax = axes[0]
    ax.plot(T, rho * 1e8, color=BLUE)
    ax.set_xlabel("温度 $T$（$^\\circ$C）")
    ax.set_ylabel(r"$\rho_e$（$10^{-8}\ \Omega\cdot$m）")
    ax.set_title("铜的电阻率", fontsize=8.8)
    ax = axes[1]
    ax.plot(T, (rho / rho0 - 1) * 100, color=ACCENT)
    ax.set_xlabel("温度 $T$（$^\\circ$C）")
    ax.set_ylabel("相对 $20\\ ^\\circ$C 的变化（%）")
    ax.set_title("相对变化近似线性", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig11-2-resistivity.png")


def fig11_3():
    U = np.linspace(0, 1.0, 300)
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.plot(U, 2.0 * U, color=BLUE, label="线性电阻 $I=U/R$")
    # 钨丝：R 随温度升高而增大，用 I = U/(R0(1+b U^2)) 模拟
    ax.plot(U, 2.0 * U / (1 + 2.2 * U ** 2), color=ACCENT, label="钨丝（电阻随温度升高）")
    Is = 0.05 * (np.exp(9 * U) - 1)
    ax.plot(U, Is, color=TEAL, label="二极管（指数关系）")
    ax.set_xlabel("电压 $U$（V）")
    ax.set_ylabel("电流 $I$（A）")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 3.2)
    ax.legend(loc="upper left", fontsize=7.8)
    save(fig, "fig11-3-ohmic.png")


fig11_1()
fig11_2()
fig11_3()
