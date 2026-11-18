import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180


def lobe(alpha, ui_deg=30, f0=0.9, n=300, with_G=True, with_F=True):
    th = np.linspace(0, 89.9, n) * D2R
    uo = spherical(th, np.full_like(th, np.pi))
    ui = spherical(np.array([ui_deg * D2R]), np.array([0.0]))[0]
    out = []
    for w in uo:
        h = normalize(ui + w)
        ci, co = ui[2], max(w[2], 1e-6)
        vh = np.clip(ui @ h, 0, 1)
        F = fresnel_schlick(vh, f0) if with_F else 1.0
        D = d_ggx(h[2], alpha)
        G = g2_smith(ci, co, alpha) if with_G else 1.0
        out.append(F * D * G / (4 * ci * co) * co)
    return th / D2R, np.array(out)


def fig6_1():
    fig, ax = plt.subplots(figsize=(5.6, 3.3))
    for alpha, col in [(0.1, BLUE), (0.3, TEAL), (0.6, ACCENT)]:
        ang, y = lobe(alpha)
        ax.semilogy(ang, np.maximum(y, 1e-4), color=col, lw=1.9, label="α = %.1f" % alpha)
    ax.set_xlabel("出射角（度）")
    ax.set_ylabel("反射强度 f·cosθ")
    ax.set_xlim(0, 90)
    ax.set_ylim(1e-3, 3e2)
    ax.axvline(30, color=GREY, ls="--", lw=1.0)
    ax.text(31, 60, "镜面反射方向", color=GREY, fontsize=8)
    ax.legend(loc="lower left")
    save(fig, "fig6-1-lobes.png")


def fig6_2():
    fig, ax = plt.subplots(figsize=(5.8, 3.3))
    for kw, col, lab in [({}, BLUE, "完整 D·F·G"),
                         ({"with_G": False}, TEAL, "去掉 G"),
                         ({"with_F": False}, ACCENT, "去掉 F")]:
        ang, y = lobe(0.4, **kw)
        ax.semilogy(ang, np.maximum(y, 1e-3), color=col, lw=1.9, label=lab)
    ax.set_xlabel("出射角（度）")
    ax.set_ylabel("反射强度 f·cosθ")
    ax.set_xlim(0, 90)
    ax.set_ylim(5e-4, 3.0)
    ax.legend(loc="upper left")
    ax.text(8, 1.15, "去掉 G 后，掠射角不再被压制", color=TEAL, fontsize=8)
    save(fig, "fig6-2-parts.png")


fig6_1()
fig6_2()
