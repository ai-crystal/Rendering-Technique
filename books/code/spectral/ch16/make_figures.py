import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from speclib import *

LAM = grid()


# ------------------------------------------------------------------ 图 16-1
def fig12_1():
    """菲涅耳两个分量与偏振度。"""
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1), gridspec_kw={"wspace": 0.30})

    th = np.linspace(0, 89.5, 500)
    n = float(sellmeier("N-BK7", 550.0))
    ci, si = np.cos(np.deg2rad(th)), np.sin(np.deg2rad(th))
    ct = np.sqrt(np.maximum(1 - (si / n) ** 2, 0))
    rs = ((ci - n * ct) / (ci + n * ct)) ** 2
    rp = ((n * ci - ct) / (n * ci + ct)) ** 2
    ax = axes[0]
    ax.plot(th, rs, color=BLUE, lw=1.7, label="$R_s$（垂直偏振）")
    ax.plot(th, rp, color=ACCENT, lw=1.7, label="$R_p$（平行偏振）")
    ax.plot(th, np.abs(rs - rp) / (rs + rp), color=PURPLE, lw=1.3, ls="--",
            label="偏振度")
    th_b = np.degrees(np.arctan(n))
    ax.axvline(th_b, color=GREY, lw=0.9, ls=":")
    ax.text(th_b + 1.5, 0.72, "布儒斯特角\n%.1f°" % th_b, fontsize=7.4, color="#666")
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("反射率 / 偏振度")
    ax.set_xlim(0, 89)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="upper left", fontsize=7.4)
    ax.set_title("N-BK7，550 nm", pad=6)

    # 自然光经 45 度镜面反射后变成部分偏振光，再用检偏器看亮度
    ax2 = axes[1]
    thi = np.deg2rad(49.0)
    cti = np.cos(thi)
    sti = np.sin(thi)
    ctt = np.sqrt(1 - (sti / n) ** 2)
    Rs = ((cti - n * ctt) / (cti + n * ctt)) ** 2
    Rp = ((n * cti - ctt) / (n * cti + ctt)) ** 2
    ang = np.linspace(0, 360, 361)
    S0 = 0.5 * (Rs + Rp)
    S1 = 0.5 * (Rs - Rp)
    I = 0.5 * (S0 + S1 * np.cos(np.deg2rad(2 * ang)))
    I_norm = I / I[0]
    ax2.plot(ang, I_norm, color=ACCENT, lw=1.8, label="偏振追踪")
    ax2.axhline(0.5 * (1 + Rp / Rs), color=GREY, lw=1.4, ls="--", label="标量模型")
    ax2.annotate("$R_p/R_s$ = %.3f" % (Rp / Rs), xy=(90, Rp / Rs), xytext=(150, 0.30),
                 fontsize=7.8, color="#3c4654",
                 arrowprops=dict(arrowstyle="-", lw=0.6, color="#8a93a0"))
    ax2.set_xlabel("检偏器转角（度）")
    ax2.set_ylabel("相对亮度（以 0 度为 1）")
    ax2.set_xlim(0, 360)
    ax2.set_ylim(0, 1.12)
    ax2.legend(loc="upper right", fontsize=7.4)
    ax2.set_title("45 度镜面反射后的检偏曲线", pad=6)
    save(fig, "fig16-1-polarization.png")


# ------------------------------------------------------------------ 图 16-2
def _mueller(n, th_deg):
    """单界面的 4x4 Mueller 矩阵（反射）。"""
    thi = np.deg2rad(th_deg)
    cti, sti = np.cos(thi), np.sin(thi)
    ctt = np.sqrt(1 - (sti / n) ** 2)
    rs = (cti - n * ctt) / (cti + n * ctt)
    rp = (n * cti - ctt) / (n * cti + ctt)
    Rs, Rp = rs ** 2, rp ** 2
    delta = 0.0 if rs * rp > 0 else np.pi
    c, s_ = np.cos(delta), np.sin(delta)
    M = np.zeros((4, 4))
    M[0, 0] = M[1, 1] = 0.5 * (Rs + Rp)
    M[0, 1] = M[1, 0] = 0.5 * (Rs - Rp)
    M[2, 2] = np.sqrt(Rs * Rp) * c
    M[2, 3] = np.sqrt(Rs * Rp) * s_
    M[3, 2] = -np.sqrt(Rs * Rp) * s_
    M[3, 3] = np.sqrt(Rs * Rp) * c
    return M


def fig12_2():
    """偏振模式下 BSDF 要返回的东西：4x4 Mueller 矩阵。"""
    n = float(sellmeier("N-BK7", 550.0))
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2), gridspec_kw={"wspace": 0.34})
    for ax, th in zip(axes, [45.0, 65.0]):
        M = _mueller(n, th)
        im = ax.imshow(M, cmap="RdBu_r", vmin=-0.12, vmax=0.12)
        for i in range(4):
            for j in range(4):
                ax.text(j, i, "%.3f" % M[i, j], ha="center", va="center", fontsize=7,
                        color="white" if abs(M[i, j]) > 0.07 else "#222")
        ax.set_xticks(range(4))
        ax.set_yticks(range(4))
        ax.set_xticklabels(["I", "Q", "U", "V"], fontsize=8)
        ax.set_yticklabels(["I", "Q", "U", "V"], fontsize=8)
        ax.set_title("入射角 %.0f°" % th, pad=6)
        ax.grid(False)
    cb = fig.colorbar(im, ax=axes, pad=0.02, fraction=0.03)
    cb.set_label("矩阵元素", fontsize=8)
    cb.ax.tick_params(labelsize=7.5)
    save(fig, "fig16-2-mueller.png")


fig12_1()
fig12_2()
