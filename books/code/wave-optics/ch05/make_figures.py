import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *


def adm(n, th, pol="s"):
    c = np.cos(th)
    return n * c if pol == "s" else n / c


def stack(lam, ns, ds, nsub, n0=1.0, th0=0.0, pol="s", want_field=False):
    st = n0 * np.sin(th0)
    th = [np.emath.arcsin(st / n) for n in ns]
    ths = np.emath.arcsin(st / nsub)
    Ms = []
    for n, d, t in zip(ns, ds, th):
        e = adm(n, t, pol)
        phi = 2 * np.pi * n * d * np.cos(t) / lam
        Ms.append(np.array([[np.cos(phi), -1j * np.sin(phi) / e],
                            [-1j * e * np.sin(phi), np.cos(phi)]], dtype=complex))
    M = np.eye(2, dtype=complex)
    for m in Ms:
        M = M @ m
    e0 = adm(n0, th0, pol)
    es = adm(nsub, ths, pol)
    B, C = M @ np.array([1.0, es])
    r = (e0 * B - C) / (e0 * B + C)
    t = 2 * e0 / (e0 * B + C)
    R = abs(r) ** 2
    T = 4 * np.real(e0) * np.real(es) / abs(e0 * B + C) ** 2
    if not want_field:
        return R, T

    # 自下而上复原行波振幅：基底 -> 顶层
    E, H = t, es * t
    segs = [None] * len(ns)
    for j in range(len(ns) - 1, -1, -1):
        n, d, thj = ns[j], ds[j], th[j]
        e = adm(n, thj, pol)
        phi = 2 * np.pi * n * d * np.cos(thj) / lam
        Ed, Hd = E, H
        a = 0.5 * (Ed + Hd / e) * np.exp(-1j * phi)
        b = 0.5 * (Ed - Hd / e) * np.exp(1j * phi)
        z = np.linspace(0, d, 90)
        Ef = a * np.exp(1j * 2 * np.pi * n * np.cos(thj) * z / lam) +              b * np.exp(-1j * 2 * np.pi * n * np.cos(thj) * z / lam)
        segs[j] = (z, np.abs(Ef) ** 2)
        # 向上走要用逆矩阵（行列式为 1，把 i 换成 -i）
        Mj_inv = np.array([[np.cos(phi), -1j * np.sin(phi) / e],
                           [-1j * e * np.sin(phi), np.cos(phi)]], dtype=complex)
        E, H = Mj_inv @ np.array([Ed, Hd])
    return R, T, segs


DS = [90.0, 115.0, 55.0]
NS = [1.38, 2.05, 1.70]
NSUB = 1.52


def fig5_1():
    lam = np.linspace(400, 700, 700)
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    R0 = [stack(l, [], [], NSUB)[0] for l in lam]
    R1 = [stack(l, [1.38], [550 / (4 * 1.38)], NSUB)[0] for l in lam]
    R3 = [stack(l, NS, DS, NSUB)[0] for l in lam]
    ax.plot(lam, np.array(R0) * 100, color=GREY, lw=1.5, label="裸玻璃")
    ax.plot(lam, np.array(R1) * 100, color=BLUE, lw=1.7, label="单层 1.38")
    ax.plot(lam, np.array(R3) * 100, color=ACCENT, lw=2.0, label="三层设计")
    ax.set_xlim(400, 700)
    ax.set_ylim(0, 4.6)
    ax.set_xlabel("波长（nm）")
    ax.set_ylabel("反射率（%）")
    ax.legend(loc="upper center", ncol=3, fontsize=8, bbox_to_anchor=(0.5, 1.16))
    ax.text(430, 2.55, "三层平均 0.24%", fontsize=8, color=ACCENT)
    ax.text(430, 3.6, "单层平均 1.5%", fontsize=8, color=BLUE)
    save(fig, "fig5-1-design.png")


def fig5_2():
    lam = 550.0
    R, T, segs = stack(lam, NS, DS, NSUB, want_field=True)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    off = 0.0
    for z, I in segs:
        ax.plot(z + off, I, color=ACCENT, lw=1.7)
        off += z[-1]
    edges = [0, DS[0], DS[0] + DS[1], sum(DS)]
    for x in edges[1:-1]:
        ax.axvline(x, color=GREY, ls=":", lw=1.0)
    names = ["空气", "氟化镁", "氧化锆", "氧化铝", "玻璃"]
    xs = [edges[0], (edges[0] + edges[1]) / 2, (edges[1] + edges[2]) / 2,
          (edges[2] + edges[3]) / 2, edges[3]]
    for x, nm in zip(xs, names):
        ax.text(x, 1.16, nm, fontsize=8, color=GREY,
                ha="left" if x == edges[3] else "center")
    ax.axhline(1.0, color=LIGHT, ls="--", lw=0.9)
    ax.set_xlim(0, sum(DS))
    ax.set_ylim(0, 1.35)
    ax.set_xlabel("深度（nm）")
    ax.set_ylabel("|E|^2 / |E_inc|^2")
    ax.text(6, 0.12, "反射率 %.2f%%，透射率 %.2f%%" % (R * 100, T * 100),
            fontsize=8, color=INK)
    save(fig, "fig5-2-field.png")


def fig5_3():
    th = np.linspace(0, 80, 240)
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    for pol, col, lab in [("s", BLUE, "s 偏振"), ("p", ACCENT, "p 偏振")]:
        Rs = [stack(550, NS, DS, NSUB, th0=np.radians(t), pol=pol)[0] for t in th]
        ax.plot(th, np.array(Rs) * 100, color=col, lw=1.8, label=lab)
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 12)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("反射率（%）")
    ax.legend(loc="upper left", fontsize=8)
    ax.text(20, 1.6, "550 nm，三层膜系", fontsize=8, color=GREY)
    save(fig, "fig5-3-angle.png")


fig5_1()
fig5_2()
fig5_3()
