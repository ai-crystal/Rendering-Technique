import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180


def lobel(ui_deg=45, n=400):
    th = np.linspace(0, 89.5, n) * D2R
    ph = np.full_like(th, np.pi)
    uo = spherical(th, ph)
    ui = spherical(np.array([ui_deg * D2R]), np.array([0.0]))[0]
    return th / D2R, ui, uo


def fig1_1():
    ang, ui, uo = lobel()
    f0_metal = 0.92
    mirror = np.array([brdf_ggx(ui, w, 0.06, f0_metal) for w in uo])
    plastic = np.array([brdf_ggx(ui, w, 0.18, 0.04) for w in uo]) + 0.35 / np.pi
    # 布料：一个偏侧的宽瓣（示意模型，见正文），加一个很弱的底
    c = np.clip(np.cos((ang - 55) * D2R), 0, 1)
    cloth = 1.6 * c ** 4 + 0.06
    skin = np.array([brdf_ggx(ui, w, 0.25, 0.03) for w in uo]) + 0.55 * np.exp(-0.5 * ((ang - 20) / 45) ** 2)

    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    for y, lab, col in [(mirror, "抛光金属 (alpha=0.06)", BLUE),
                        (plastic, "塑料 (漫反射 + 高光)", TEAL),
                        (cloth, "布料 (偏侧宽瓣)", ACCENT),
                        (skin, "皮肤 (窄峰 + 宽底)", RED)]:
        ax.semilogy(ang, np.maximum(y, 1e-4), color=col, label=lab, lw=1.8)
    ax.set_xlabel("出射方向与法线夹角（度）")
    ax.set_ylabel("反射强度 $f_r\\cos\\theta_o$")
    ax.set_xlim(0, 89)
    ax.set_ylim(1e-3, 2e3)
    ax.axvline(45, color=GREY, lw=1.0, ls="--")
    ax.text(46.5, 900, "镜面反射方向", color=GREY, fontsize=8)
    ax.legend(loc="upper right", ncol=1)
    save(fig, "fig1-1-lobes.png")


def fig1_2():
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.grid(False)

    layers = [
        (0.6, 3.5, "界面层", "Fresnel\n反射与折射的比例", BLUE),
        (0.6, 1.9, "微观几何层", "微表面分布\n反射的方向分布", ACCENT),
        (0.6, 0.3, "体积层", "吸收与散射\n颜色、半透明", TEAL),
    ]
    for x, y, title, body, col in layers:
        ax.add_patch(plt.Rectangle((x, y), 3.4, 1.25, facecolor="white",
                                   edgecolor=col, lw=1.6, joinstyle="round"))
        ax.text(x + 0.2, y + 1.02, title, fontsize=10, color=col, fontweight="bold", va="center")
        ax.text(x + 0.2, y + 0.44, body, fontsize=8.5, color="#303842", va="center")

    ax.annotate("", xy=(6.0, 2.95), xytext=(4.05, 3.95),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4))
    ax.annotate("", xy=(6.0, 2.15), xytext=(4.05, 2.45),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.4))
    ax.annotate("", xy=(6.0, 1.35), xytext=(4.05, 0.95),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.4))

    ax.add_patch(plt.Rectangle((6.0, 1.1), 3.2, 2.1, facecolor="#f6f7f9",
                               edgecolor="#9aa3af", lw=1.2))
    ax.text(7.6, 2.75, "一个材质的 BSDF", fontsize=9.5, ha="center", color=INK)
    ax.text(7.6, 2.0, "$f_r(\\omega_i,\\omega_o)$", fontsize=13, ha="center", color=INK)
    ax.text(7.6, 1.35, "无吸收时积分等于 1", fontsize=8, ha="center", color=GREY)
    save(fig, "fig1-2-layers.png")


fig1_1()
fig1_2()
