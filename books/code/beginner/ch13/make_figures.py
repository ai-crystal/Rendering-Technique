import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *

D2R = np.pi / 180
LAM = np.linspace(380, 780, 500)


def gauss(x, mu, sig):
    return np.exp(-0.5 * ((x - mu) / sig) ** 2)


def fig13_1():
    light = gauss(LAM, 452, 5) + gauss(LAM, 612, 5)
    refl = 0.05 + 0.70 * np.exp(-0.5 * ((LAM - 535) / 30) ** 2)
    prod = light * refl
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.plot(LAM, light / light.max(), color=ACCENT, lw=1.8, label="光源光谱（两条窄线）")
    ax.plot(LAM, refl, color=TEAL, lw=1.8, label="滤光片透过率")
    ax.plot(LAM, prod / max(light.max(), 1e-9), color=INK, lw=2.2, label="逐波长相乘")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("波长（nm）")
    ax.set_ylabel("相对值")
    ax.set_xlim(400, 680)
    ax.set_ylim(-0.02, 1.05)
    ax.legend(loc="upper right", fontsize=8)
    ax.annotate("乘积为零", xy=(535, 0.0), xytext=(540, 0.28), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.0))
    save(fig, "fig13-1-rgb-vs-spectral.png")


def fig13_2():
    th = np.linspace(0, 89.9, 500)
    c = np.cos(th * D2R)
    eta = 1.5
    sin2 = (1 - c ** 2) / eta ** 2
    ct = np.sqrt(np.clip(1 - sin2, 0, 1))
    rs = (c - eta * ct) / (c + eta * ct)
    rp = (eta * c - ct) / (eta * c + ct)
    Rs, Rp = rs ** 2, rp ** 2
    M11 = 0.5 * (Rs + Rp)
    M12 = 0.5 * (Rs - Rp)
    M33 = np.sqrt(Rs * Rp)
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    ax.plot(th, M11, color=BLUE, lw=2.0, label="M11 = (Rs+Rp)/2")
    ax.plot(th, M12, color=ACCENT, lw=1.8, label="M12 = (Rs−Rp)/2")
    ax.plot(th, M33, color=TEAL, lw=1.8, ls="--", label="M33 = √(RsRp)")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_xlabel("入射角（度）")
    ax.set_ylabel("Mueller 矩阵元素")
    ax.set_xlim(0, 90)
    ax.set_ylim(-0.35, 1.02)
    ax.legend(loc="upper left", fontsize=8)
    ax.text(58, -0.28, "M12 在布儒斯特角附近达到极值", fontsize=8, color=ACCENT)
    save(fig, "fig13-2-mueller.png")


fig13_1()
fig13_2()
