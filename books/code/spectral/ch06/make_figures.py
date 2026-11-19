import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()


# ------------------------------------------------------------------ 图 6-1
def fig2_1():
    """几种常见光源的光谱功率分布。"""
    bb2800 = blackbody(LAM, 2800.0)
    bb6500 = blackbody(LAM, 6504.0)
    led = led_white(LAM, 452, 18, 560, 95, 1.0)
    # 荧光灯：汞的 436 / 546 / 577 nm 三条线加一层荧光粉连续谱
    fluor = (gaussian_line(LAM, 436, 4) + 1.6 * gaussian_line(LAM, 546, 5)
             + 0.55 * gaussian_line(LAM, 577, 6) + 0.22 * gaussian_line(LAM, 610, 70))
    laser = gaussian_line(LAM, 532, 1.2)

    curves = [(bb2800, "白炽灯 2800 K", RED),
              (bb6500, "日光 6500 K", GOLD),
              (led, "白光 LED", BLUE),
              (fluor, "荧光灯", TEAL),
              (laser, "532 nm 激光", PURPLE)]
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    for spd, lab, col in curves:
        ax.plot(LAM, spd / spd.max(), color=col, lw=1.5, label=lab)
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 1.08)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("相对功率（各自按峰值归一）")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=3,
              columnspacing=1.4, handlelength=1.8)
    save(fig, "fig6-1-spd.png")


# ------------------------------------------------------------------ 图 6-2
def fig2_2():
    """辐亮度的几何：投影面积与立体角。"""
    fig, ax = plt.subplots(figsize=(4.8, 3.1))
    ox = 0.40
    ax.plot([-0.05, 1.00], [0, 0], color="#3c4654", lw=1.6)
    ax.fill_between([ox - 0.07, ox + 0.07], [-0.013, -0.013], [0.013, 0.013], color=ACCENT)
    ax.annotate("", xy=(ox - 0.07, -0.070), xytext=(ox + 0.07, -0.070),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=ACCENT))
    ax.text(ox, -0.125, r"$dA$", color=ACCENT, ha="center", fontsize=9)

    ax.annotate("", xy=(ox, 0.55), xytext=(ox, 0.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#5b6472"))
    ax.text(ox - 0.045, 0.53, r"$n$", fontsize=9, color="#3c4654")

    th = np.deg2rad(45)
    L = 0.70
    tip = np.array([ox + L * np.sin(th), L * np.cos(th)])

    half = np.deg2rad(8.5)
    r0 = 0.32
    a1, a2 = th - half, th + half
    wedge = np.array([[ox + r0 * np.sin(a1), r0 * np.cos(a1)],
                      [ox + r0 * np.sin(a2), r0 * np.cos(a2)],
                      [ox + L * np.sin(a2), L * np.cos(a2)],
                      [ox + L * np.sin(a1), L * np.cos(a1)]])
    ax.add_patch(plt.Polygon(wedge, closed=True, facecolor=BLUE, alpha=0.13, lw=0))
    for a in (a1, a2):
        ax.plot([ox + r0 * np.sin(a), ox + L * np.sin(a)],
                [r0 * np.cos(a), L * np.cos(a)], color=BLUE, lw=0.7, ls=":")
    ax.annotate("", xy=tip, xytext=(ox, 0.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.2, color=BLUE))
    ax.text(tip[0] + 0.025, tip[1] + 0.045, r"$\omega_i$", fontsize=9, color=BLUE)
    ax.text(ox + 0.395, 0.30, r"$d\omega_i$", fontsize=9, color=BLUE, ha="left")

    arc2 = np.linspace(0, th, 40)
    ax.plot(ox + 0.16 * np.sin(arc2), 0.16 * np.cos(arc2), color="#3c4654", lw=0.8)
    ax.text(ox + 0.028, 0.172, r"$\theta_i$", fontsize=9, color="#3c4654")

    # 投影长度 dA cos θ，沿垂直于 ω 的方向
    p = np.array([np.cos(th), -np.sin(th)])
    c = np.array([ox, 0.0]) + 0.215 * np.array([np.sin(th), np.cos(th)])
    ax.annotate("", xy=c + 0.070 * p, xytext=c - 0.070 * p,
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color=GREY))
    ax.annotate(r"$dA\cos\theta_i$", xy=tuple(c - 0.02 * p), xytext=(0.012, 0.245),
                fontsize=8.5, color="#5b6472",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=GREY))
    ax.set_xlim(-0.06, 1.00)
    ax.set_ylim(-0.16, 0.86)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "fig6-2-radiance.png")


# ------------------------------------------------------------------ 图 6-3
def fig2_3():
    """两块面元之间的几何，以及辐照度按 1/r² 衰减而辐亮度不变。"""
    fig = plt.figure(figsize=(7.0, 3.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.15], wspace=0.34)

    ax = fig.add_subplot(gs[0])
    ax.plot([0.08, 0.42], [0, 0], color="#3c4654", lw=1.5)
    ax.plot([0.62, 0.96], [0.72, 0.72], color="#3c4654", lw=1.5)
    ax.plot([0.25, 0.79], [0, 0.72], color="#8a93a0", lw=0.8, ls="--")
    ax.annotate("", xy=(0.25, 0.26), xytext=(0.25, 0.0),
                arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#3c4654"))
    ax.annotate("", xy=(0.79, 0.46), xytext=(0.79, 0.72),
                arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#3c4654"))
    ax.annotate("", xy=(0.79, 0.72), xytext=(0.25, 0.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.2, color=BLUE))
    ax.text(0.44, 0.47, r"$r$", color=BLUE, fontsize=9, rotation=41)
    ax.text(0.25, -0.11, r"$dA_1$", ha="center", fontsize=9)
    ax.text(0.79, 0.82, r"$dA_2$", ha="center", fontsize=9)
    ax.text(0.285, 0.10, r"$\theta_1$", fontsize=9, color="#3c4654")
    ax.text(0.745, 0.56, r"$\theta_2$", fontsize=9, color="#3c4654")
    ax.set_xlim(0, 1.02)
    ax.set_ylim(-0.18, 0.95)
    ax.set_aspect("equal")
    ax.axis("off")

    ax2 = fig.add_subplot(gs[1])
    # 半径 R=1 的圆盘光源，正对轴线上距离 d 处的辐照度 E = pi L R^2 / (R^2 + d^2)
    d = np.logspace(-1.2, 0.8, 400)
    E = np.pi / (1.0 + d ** 2)
    ax2.loglog(d, E, color=ACCENT, lw=1.9, label="辐照度 $E$")
    ax2.loglog(d, np.full_like(d, 1.0), color=GREY, lw=1.4, ls="--", label="辐亮度 $L$")
    ax2.loglog(d, np.pi / d ** 2, color=BLUE, lw=1.0, ls=":", label=r"$\pi R^2 L/d^2$")
    ax2.set_xlabel("距离 d（单位：圆盘半径 R）")
    ax2.set_ylabel("相对值")
    ax2.set_ylim(0.02, 12)
    ax2.set_xlim(0.06, 6)
    ax2.legend(loc="lower left", ncol=1)
    save(fig, "fig6-3-irradiance.png")


fig2_1()
fig2_2()
fig2_3()
