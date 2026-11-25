import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def fig13_1():
    tau = 1.0
    t = np.linspace(0, 8, 1000)
    frac = t % tau
    e = frac / tau
    fig, ax = plt.subplots(figsize=(6.3, 3.0))
    ax.plot(t, e, color=SKY, lw=0.9, label="单次加速获得的定向动能")
    ax.plot(t, np.full_like(t, 0.5), color=RED, ls="--", lw=1.2, label="平均值")
    ax.set_xlabel("时间（以碰撞间隔为单位）")
    ax.set_ylabel("定向动能（以 $eE\\lambda$ 为单位）")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 1.15)
    ax.legend(loc="upper right", fontsize=7.8)
    ax.set_title("碰撞使定向动能归零，电场重新注入", fontsize=8.8)
    save(fig, "fig13-1-energy.png")


def fig13_2():
    P, R = 100e6, 10.0
    U = np.logspace(3, 6, 400)
    loss = P ** 2 * R / U ** 2
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.loglog(U / 1e3, loss / 1e6, color=BLUE)
    for u, lab in [(10, "10 kV"), (110, "110 kV"), (500, "500 kV")]:
        l = P ** 2 * R / (u * 1e3) ** 2
        ax.plot([u], [l / 1e6], "o", ms=4, color=ACCENT)
        ax.annotate(f"{lab}\n{l/1e6:.2f} MW", (u, l / 1e6), xytext=(5, 8),
                    textcoords="offset points", fontsize=7.2)
    ax.axhline(100, color=GREY, ls=":", lw=0.9)
    ax.text(2e3, 130, "输送功率 100 MW", fontsize=7.5, color=GREY)
    ax.set_xlabel("输电电压（kV）")
    ax.set_ylabel("线路损耗（MW）")
    ax.set_ylim(0.01, 2000)
    save(fig, "fig13-2-transmission.png")


def fig13_3():
    x = np.logspace(-1, 1.5, 400)
    P = 4 * x / (1 + x) ** 2
    eta = x / (1 + x)
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.plot(x, P, color=BLUE, label="$P/P_{\\max}$")
    ax.plot(x, eta, color=ACCENT, label="$\\eta$")
    ax.axvline(1, color=GREY, ls=":", lw=0.9)
    ax.text(1.08, 0.06, "$R=r$", fontsize=8, color=GREY)
    ax.set_xscale("log")
    ax.set_xlabel("负载与内阻之比 $R/r$")
    ax.set_ylabel("归一化量")
    ax.set_ylim(0, 1.08)
    ax.legend(loc="center right", fontsize=8)
    save(fig, "fig13-3-matching.png")


fig13_1()
fig13_2()
fig13_3()
