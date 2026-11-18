import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from scipy.special import fresnel as _fresnel


def fresnel_cs(v):
    """返回 C(v), S(v)，用 scipy 的 fresnel（定义为 int cos(pi t^2/2)）。"""
    S, C = _fresnel(v)
    return C, S


def knife(v):
    C, S = fresnel_cs(v)
    return 0.5 * ((C + 0.5) ** 2 + (S + 0.5) ** 2)


def fig3_1():
    lam = 550e-9
    th = np.linspace(-0.75, 0.75, 6000)
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    for a, col, lab in [(1e-6, BLUE, "1 微米"), (3e-6, ACCENT, "3 微米"),
                        (10e-6, TEAL, "10 微米")]:
        b = np.pi * a * np.sin(th) / lam
        I = np.where(np.abs(b) < 1e-12, 1.0, (np.sin(b) / np.where(b == 0, 1, b)) ** 2)
        ax.semilogy(np.degrees(th), I + 1e-6, color=col, lw=1.4, label="缝宽 " + lab)
    ax.set_xlim(-40, 40)
    ax.set_ylim(1e-4, 1.6)
    ax.set_xlabel("衍射角（度）")
    ax.set_ylabel("归一化强度")
    ax.legend(loc="upper center", ncol=3, fontsize=8, bbox_to_anchor=(0.5, 1.17))
    ax.annotate("第一极小 sin(角) = 波长 / 缝宽", xy=(3.2, 2e-4), xytext=(-38, 3.5e-2),
                fontsize=8, color=GREY,
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.9))
    save(fig, "fig3-1-slit.png")


def fig3_2():
    fig = plt.figure(figsize=(6.6, 5.6))
    ax = fig.add_subplot(2, 1, 1)
    v = np.linspace(-6, 6, 1200)
    ax.plot(v, knife(v), color=ACCENT, lw=1.8)
    ax.axvline(0, color=GREY, ls=":", lw=1.0)
    ax.axhline(1.0, color=LIGHT, ls="--", lw=0.9)
    ax.axhline(0.25, color=LIGHT, ls="--", lw=0.9)
    ax.set_xlim(-6, 6)
    ax.set_ylim(0, 1.5)
    ax.set_xlabel("无量纲坐标 v")
    ax.set_ylabel("I / I0")
    ax.text(1.2, 0.33, "v = 0 处强度为 1/4", fontsize=8, color=INK)
    ax.text(-5.8, 1.12, "阴影区", fontsize=8, color=GREY)
    ax.text(4.2, 1.12, "亮区", fontsize=8, color=GREY)
    panel_label(ax, "a", x=-0.10, y=1.02)

    ax2 = fig.add_subplot(2, 1, 2)
    vv = np.linspace(-6, 6, 2000)
    C, S = fresnel_cs(vv)
    ax2.plot(C, S, color=BLUE, lw=1.4)
    ax2.plot([-0.5, 0.5], [-0.5, 0.5], color=GREY, ls=":", lw=0.9)
    for vt in (-4, -2, 0, 2, 4):
        c, s = fresnel_cs(np.array([vt]))
        ax2.plot(c, s, "o", ms=3.2, color=RED)
    ax2.annotate("v = 0", xy=(0, 0), xytext=(0.18, -0.18), fontsize=8,
                 arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.8))
    ax2.set_xlim(-0.85, 0.85)
    ax2.set_ylim(-0.85, 0.85)
    ax2.set_xlabel("C(v)")
    ax2.set_ylabel("S(v)")
    ax2.set_aspect("equal")
    panel_label(ax2, "b", x=-0.10, y=1.02)
    fig.subplots_adjust(hspace=0.45)
    save(fig, "fig3-2-knife.png")


def fig3_3():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    ax = axes[0]
    from scipy.special import j1
    x = np.linspace(-14, 14, 3000)
    xs = np.where(np.abs(x) < 1e-9, 1e-9, x)
    I = (2 * j1(xs) / xs) ** 2
    ax.semilogy(x, I + 1e-7, color=ACCENT, lw=1.6)
    ax.axvline(3.832, color=GREY, ls=":", lw=1.0)
    ax.set_xlim(-12, 12)
    ax.set_ylim(1e-5, 1.6)
    ax.set_xlabel("x = pi * D * sin(角) / 波长")
    ax.set_ylabel("归一化强度")
    ax.annotate("第一暗环 x = 3.83", xy=(3.83, 3e-5), xytext=(-3.0, 2e-3), fontsize=8,
                color=GREY, arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.9))
    panel_label(ax, "a")

    ax = axes[1]
    N = np.linspace(1.4, 32, 500)
    for lam, col, lab in [(450, BLUE, "450 nm"), (550, ACCENT, "550 nm"),
                          (650, TEAL, "650 nm")]:
        d_um = 2.44 * lam * 1e-3 * N
        ax.plot(N, d_um, color=col, lw=1.7, label=lab)
    ax.axhline(4.0, color=GREY, ls="--", lw=1.0)
    ax.text(23.5, 5.2, "像素间距 4 微米", fontsize=8, color=GREY)
    ax.set_xlabel("f 数 N")
    ax.set_ylabel("Airy 斑直径（微米）")
    ax.set_xlim(1.4, 32)
    ax.set_ylim(0, 55)
    ax.legend(loc="upper left", fontsize=8)
    panel_label(ax, "b")
    fig.subplots_adjust(wspace=0.34)
    save(fig, "fig3-3-airy.png")


fig3_1()
fig3_2()
fig3_3()
