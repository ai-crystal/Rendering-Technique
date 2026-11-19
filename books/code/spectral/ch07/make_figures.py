import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()
LAM1 = grid(380, 780, 1.0)


# ------------------------------------------------------------------ 图 7-1
def fig3_1():
    """CIE 1931 标准观察者的配色函数。"""
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(LAM1, cie_x(LAM1), color=RED, lw=1.7, label=r"$\bar{x}(\lambda)$")
    ax.plot(LAM1, cie_y(LAM1), color=GREEN, lw=1.7, label=r"$\bar{y}(\lambda)$")
    ax.plot(LAM1, cie_z(LAM1), color=BLUE, lw=1.7, label=r"$\bar{z}(\lambda)$")
    ax.axvline(555, color=GREY, lw=0.8, ls=":")
    ax.annotate("555 nm\n$\\bar{y}$ 的峰值", xy=(556, 1.02), xytext=(492, 1.46),
                fontsize=8, color="#3c4654",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=GREY))
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 1.85)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("响应")
    ax.legend(loc="upper right", ncol=1)
    save(fig, "fig7-1-cmf.png")


# ------------------------------------------------------------------ 图 7-2
def fig3_2():
    """xy 色度图、光谱轨迹与三个色域三角形。"""
    Lx = grid(400, 700, 1.0)
    x, y = xyz_to_xy(cie_xyz_basis(Lx))
    fig, ax = plt.subplots(figsize=(5.4, 4.3))
    # 光谱轨迹：按波长上色
    for i in range(len(Lx) - 1):
        c = wl_to_srgb(Lx[i], gamma=False)[0]
        c = 0.25 + 0.75 * np.array(c) / max(c.max(), 1e-6)
        ax.plot(x[i:i + 2], y[i:i + 2], color=np.clip(c, 0, 1), lw=2.4)
    # 紫线
    ax.plot([x[0], x[-1]], [y[0], y[-1]], color="#9a5b8f", lw=1.6, ls="--")

    gamuts = [("sRGB / BT.709", [(0.64, 0.33), (0.30, 0.60), (0.15, 0.06)], BLUE),
              ("Display P3", [(0.680, 0.320), (0.265, 0.690), (0.150, 0.060)], TEAL),
              ("Rec.2020", [(0.708, 0.292), (0.170, 0.797), (0.131, 0.046)], ACCENT)]
    for name, tri, col in gamuts:
        pts = np.array(tri + [tri[0]])
        ax.plot(pts[:, 0], pts[:, 1], color=col, lw=1.2, label=name)
    ax.plot(0.3127, 0.3290, "o", color="#333", ms=4)
    ax.annotate("D65", xy=(0.3127, 0.3290), xytext=(0.335, 0.375), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.6, color="#666"))
    ax.text(0.16, 0.83, "520", fontsize=7.5, color="#555")
    ax.text(0.635, 0.345, "650", fontsize=7.5, color="#555")
    ax.text(0.145, 0.045, "460", fontsize=7.5, color="#555")
    ax.set_xlim(0, 0.78)
    ax.set_ylim(0, 0.88)
    ax.set_xlabel("色度坐标 x")
    ax.set_ylabel("色度坐标 y")
    ax.legend(loc="upper right", fontsize=7.8)
    save(fig, "fig7-2-chromaticity.png")


# ------------------------------------------------------------------ 图 7-3
def fig3_3():
    """单色光在 sRGB 里的分量：负值意味着色域外。"""
    lams = np.arange(430, 681, 25)
    rgb = []
    for l in lams:
        c = M_XYZ2RGB_PUBLISHED @ np.array([cie_x(l), cie_y(l), cie_z(l)])
        rgb.append(c / c.max())
    rgb = np.array(rgb)

    fig = plt.figure(figsize=(7.0, 3.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1.0], wspace=0.30)
    ax = fig.add_subplot(gs[0])
    h = 0.26
    for j, (col, lab) in enumerate([(RED, "R"), (GREEN, "G"), (BLUE, "B")]):
        ax.barh(np.arange(len(lams)) + (j - 1) * h, rgb[:, j], height=h * 0.92,
                color=col, alpha=0.85, label=lab)
    ax.axvline(0, color="#3c4654", lw=0.9)
    ax.set_yticks(np.arange(len(lams)))
    ax.set_yticklabels(["%d" % l for l in lams], fontsize=7.5)
    ax.set_xlabel("线性 sRGB 分量（按最大分量归一）")
    ax.set_ylabel("波长 (nm)")
    ax.set_xlim(-1.15, 1.15)
    leg = ax.legend(loc="lower left", ncol=3, columnspacing=0.9, frameon=True,
                    facecolor="white", edgecolor="none", framealpha=0.92)
    leg.set_zorder(10)
    ax.set_title("负分量出现在色域之外", pad=6)

    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    for i, l in enumerate([470, 500, 532, 580, 610]):
        c0 = M_XYZ2RGB_PUBLISHED @ np.array([cie_x(l), cie_y(l), cie_z(l)])
        c0 = c0 / c0.max()
        cc = srgb_encode(np.clip(c0, 0, 1))
        yy = 0.86 - i * 0.18
        ax2.add_patch(plt.Rectangle((0.06, yy - 0.07), 0.18, 0.13, color=cc,
                                    ec="#3a3a3a", lw=0.6))
        ax2.text(0.30, yy - 0.005, "%d nm" % l, fontsize=8, va="center")
        ax2.text(0.54, yy - 0.005, "(%+.2f, %+.2f, %+.2f)" % tuple(c0),
                 fontsize=7.6, va="center", color="#444")
    ax2.text(0.06, 0.97, "裁到 [0,1] 之后的显示色", fontsize=8.5, va="center")
    save(fig, "fig7-3-gamut-clip.png")


fig3_1()
fig3_2()
fig3_3()
