import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def fresnel(n1, n2, th):
    s1 = np.sin(th)
    c1 = np.cos(th)
    c2 = np.sqrt(1 - (n1 / n2 * s1) ** 2 + 0j)
    rs = (n1 * c1 - n2 * c2) / (n1 * c1 + n2 * c2)
    rp = (n2 * c1 - n1 * c2) / (n2 * c1 + n1 * c2)
    return rs, rp


def fresnel_mueller(rp, rs):
    Rp, Rs = abs(rp) ** 2, abs(rs) ** 2
    u = (rp * np.conj(rs)).real
    v = (rp * np.conj(rs)).imag
    return 0.5 * np.array([[Rp + Rs, Rp - Rs, 0, 0],
                           [Rp - Rs, Rp + Rs, 0, 0],
                           [0, 0, 2 * u, -2 * v],
                           [0, 0, 2 * v, 2 * u]])


def fig9_1():
    th = np.linspace(0, 89.9, 900)
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    for n, col in [(1.5, ACCENT), (1.33, TEAL)]:
        st = np.sin(np.radians(th))
        ct = np.sqrt(1 - (st / n) ** 2)
        ratio = n ** 2 * ct / np.cos(np.radians(th))
        ax.semilogx(th, ratio, color=col, lw=1.9, label="n_t = %.2f" % n)
    ax.set_xlim(0.5, 89.9)
    ax.set_ylim(0, 12)
    ax.set_xlabel("入射角（度，对数刻度）")
    ax.set_ylabel("dω_i / dω_t")
    ax.legend(loc="upper right", fontsize=8)
    ax.text(1.0, 6.0, "掠射时发散", fontsize=8, color=GREY)
    save(fig, "fig9-1-jacobian.png")


def fig9_2():
    # 玻璃球内壁：外部 45 度入射对应内部 28.1 度
    th_in = np.arcsin(np.sin(np.radians(45)) / 1.5)
    rs, rp = fresnel(1.5, 1.0, th_in)
    M = fresnel_mueller(rp, rs)
    S = np.array([1.0, 0, 0, 0])
    Is, dop = [1.0], [0.0]
    Mp = np.eye(4)
    for k in range(1, 11):
        Mp = M @ Mp
        Sk = Mp @ S
        Is.append(Sk[0])
        dop.append(np.sqrt(Sk[1] ** 2 + Sk[2] ** 2 + Sk[3] ** 2) / max(Sk[0], 1e-30))
    n = np.arange(0, 11)
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    ax.semilogy(n, np.maximum(Is, 1e-9), "o-", color=ACCENT, lw=1.7, ms=4,
                label="强度 I")
    ax.set_xlabel("反射次数")
    ax.set_ylabel("I / I_inc（对数）")
    ax.set_xlim(-0.3, 10.3)
    ax2 = ax.twinx()
    ax2.plot(n, dop, "s--", color=BLUE, lw=1.5, ms=4, label="偏振度")
    ax2.set_ylim(0, 1.05)
    ax2.set_ylabel("偏振度", color=BLUE)
    ax2.spines["right"].set_visible(True)
    ax.legend(loc="lower left", fontsize=8)
    ax2.legend(loc="center right", fontsize=8)
    save(fig, "fig9-2-bounces.png")


fig9_1()
fig9_2()

print("R_s, R_p at 45:", abs(fresnel(1.5, 1.0, np.radians(45))[0]) ** 2,
      abs(fresnel(1.5, 1.0, np.radians(45))[1]) ** 2)
