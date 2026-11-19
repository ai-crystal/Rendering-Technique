import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()
LAM_UV = grid(330, 780)


# ------------------------------------------------------------------ 图 15-1
def fig11_1():
    """吸收谱、发射谱与能级过程。"""
    fig = plt.figure(figsize=(7.0, 3.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1.0], wspace=0.28)

    ax = fig.add_subplot(gs[0])
    a = gaussian_line(LAM, 450, 55)
    e = gaussian_line(LAM, 560, 85)
    ax.plot(LAM, a, color=BLUE, lw=1.8, label="吸收谱")
    ax.plot(LAM, e / e.max() * 0.92, color=GREEN, lw=1.8, label="发射谱")
    ax.fill_between(LAM, 0, a, color=BLUE, alpha=0.10, lw=0)
    ax.fill_between(LAM, 0, e / e.max() * 0.92, color=GREEN, alpha=0.10, lw=0)
    ax.annotate("", xy=(560, 1.06), xytext=(450, 1.06),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color="#3c4654"))
    ax.text(505, 1.09, "Stokes 位移 110 nm", fontsize=7.8, ha="center", color="#3c4654")
    ax.set_xlim(380, 780)
    ax.set_ylim(0, 1.22)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("相对强度")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title("吸收在短波，发射在长波", pad=6)

    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    # 能级：S0 与 S1，各带两个振动态
    lv = [(0.10, "S$_0$"), (0.86, "S$_1$")]
    for y, lab in lv:
        ax2.plot([0.12, 0.62], [y, y], color="#3c4654", lw=2.0)
        ax2.plot([0.12, 0.62], [y + 0.09, y + 0.09], color="#9aa7b4", lw=0.9)
        ax2.text(0.06, y + 0.045, lab, fontsize=9, va="center")
    # 吸收
    ax2.annotate("", xy=(0.25, 0.95), xytext=(0.25, 0.19),
                 arrowprops=dict(arrowstyle="-|>", lw=1.5, color=BLUE))
    ax2.text(0.27, 0.55, "吸收\n450 nm", fontsize=7.6, color=BLUE)
    # 非辐射弛豫
    xs = np.linspace(0.44, 0.56, 40)
    ax2.plot(xs, 0.95 - 0.06 * np.sin((xs - 0.44) / 0.12 * 6 * np.pi), color="#8a93a0", lw=1.0)
    ax2.text(0.50, 1.00, "弛豫（发热）", fontsize=7.2, ha="center", color="#666")
    # 发射
    ax2.annotate("", xy=(0.56, 0.19), xytext=(0.56, 0.86),
                 arrowprops=dict(arrowstyle="-|>", lw=1.5, color=GREEN))
    ax2.text(0.58, 0.50, "发射\n560 nm", fontsize=7.6, color=GREEN)
    save(fig, "fig15-1-spectra.png")


# ------------------------------------------------------------------ 图 15-2
def fig11_2():
    """再辐射矩阵：输入波长到输出波长。"""
    a = gaussian_line(LAM, 450, 55)
    e = gaussian_line(LAM, 560, 85)
    R = np.outer(a, e)
    for i, li in enumerate(LAM):
        R[i, LAM < li] = 0.0          # 只有长波发射
    R = R / R.max()

    fig, ax = plt.subplots(figsize=(5.4, 4.0))
    im = ax.imshow(R.T, origin="lower", aspect="auto", cmap="magma",
                   extent=[LAM[0], LAM[-1], LAM[0], LAM[-1]], vmin=0, vmax=1)
    ax.plot([LAM[0], LAM[-1]], [LAM[0], LAM[-1]], color="#9fd", lw=0.9, ls="--")
    cb = fig.colorbar(im, ax=ax, pad=0.02)
    cb.set_label("相对转换系数", fontsize=8)
    cb.ax.tick_params(labelsize=7.5)
    ax.set_xlabel(r"入射波长 $\lambda_i$ (nm)")
    ax.set_ylabel(r"出射波长 $\lambda_o$ (nm)")
    ax.text(520, 430, "对角线以下为零", fontsize=8, color="white")
    ax.text(470, 655, "非零区在长波一侧", fontsize=8, color="white", ha="left")
    save(fig, "fig15-2-matrix.png")


# ------------------------------------------------------------------ 图 15-3
def fig11_3():
    """荧光增白剂：紫外光下的白纸。"""
    uv = gaussian_line(LAM_UV, 365, 18)
    paper = 0.85
    absorb = 0.60 * gaussian_line(LAM_UV, 372, 42)
    emit = gaussian_line(LAM_UV, 440, 55)

    # 无增白剂：只反射
    out_plain = uv * paper
    # 有增白剂：反射 + 把吸收的能量以 440 nm 发射（量子效率 0.9）
    emitted = emit / emit.sum() * (absorb * uv).sum() * 0.9
    out_fluo = uv * np.clip(paper - absorb, 0, 1) + emitted

    xyz_p = spectrum_to_xyz(LAM_UV, out_plain)
    xyz_f = spectrum_to_xyz(LAM_UV, out_fluo)

    fig = plt.figure(figsize=(7.0, 3.1))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.45, 1.0], wspace=0.26)
    ax = fig.add_subplot(gs[0])
    ax.plot(LAM_UV, uv / uv.max(), color=PURPLE, lw=1.5, label="入射紫外")
    ax.plot(LAM_UV, out_plain / uv.max(), color=GREY, lw=1.6, ls="--", label="无增白剂的反射")
    ax.plot(LAM_UV, out_fluo / uv.max(), color=BLUE, lw=1.7, label="有增白剂的反射")
    ax.axvspan(380, 430, color=BLUE, alpha=0.06, lw=0)
    ax.set_xlim(330, 620)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("波长 λ (nm)")
    ax.set_ylabel("相对功率")
    ax.legend(loc="upper right", fontsize=7.6)
    ax.set_title("吸收不可见的紫外，发射可见的蓝紫", pad=6)

    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    for i, (xyz, lab) in enumerate([(xyz_p, "无增白剂"), (xyz_f, "有增白剂")]):
        c = srgb_encode(np.clip(M_XYZ2RGB_PUBLISHED @ (xyz / max(xyz[1], 1e-9)) * min(1.0, xyz[1] * 6), 0, 1))
        y = 0.58 - i * 0.34
        ax2.add_patch(plt.Rectangle((0.10, y), 0.30, 0.24, color=c, ec="#3a3a3a", lw=0.6))
        ax2.text(0.46, y + 0.17, lab, fontsize=8.2, va="center")
        ax2.text(0.46, y + 0.06, "Y = %.3f" % xyz[1], fontsize=7.6, va="center", color="#555")
    ax2.text(0.5, 0.96, "紫外灯下的白纸", fontsize=8.6, ha="center", va="center")
    save(fig, "fig15-3-brightener.png")


fig11_1()
fig11_2()
fig11_3()
