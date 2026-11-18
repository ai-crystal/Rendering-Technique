import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from bsdf import *


def fig7_1():
    """多次散射的阶数分布。"""
    n = np.arange(0, 12)
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    for tau, c in [(0.5, BLUE), (2.0, TEAL), (5.0, ACCENT)]:
        p = np.exp(-tau) * tau ** n / np.array([math.factorial(k) for k in n])
        ax.plot(n, p, "o-", color=c, ms=4, label="$\\tau=%.1f$" % tau)
    ax.set_xlabel("散射次数")
    ax.set_ylabel("概率")
    ax.set_xlim(-0.3, 11)
    ax.legend(loc="upper right")
    ax.text(0.03, 0.62, "光学厚度越大，高阶散射占比越高", transform=ax.transAxes,
            fontsize=8, color="#3c4654")
    save(fig, "fig7-1-orders.png")


def velvet_radiance(theta_l, theta_v, tau0=3.0, albedo=0.95):
    """绒面：纤维垂直于表面，法线方向即纤维轴。"""
    T = np.array([0.0, 0.0, 1.0])
    L = spherical(np.array([theta_l]), 0.0)[0]
    V = spherical(np.array([theta_v]), 0.0)[0]
    sL = np.sqrt(max(0.0, 1.0 - np.dot(T, L) ** 2))
    sV = np.sqrt(max(0.0, 1.0 - np.dot(T, V) ** 2))
    single = sL * sV
    tau = tau0 / max(np.cos(theta_v), 0.08)
    multi = albedo * (1.0 - np.exp(-tau)) * 0.35
    return single + multi


def fig7_2():
    """绒面与普通布料的视角响应。"""
    deg = np.linspace(0, 88, 600)
    th = np.deg2rad(deg)
    tl = np.deg2rad(40)
    vel = np.array([velvet_radiance(tl, t) for t in th])
    cloth = 0.35 + 0.55 * (1 - np.cos(th)) ** 5
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.plot(deg, vel / vel.max(), color=ACCENT, label="绒面（纤维垂直表面）")
    ax.plot(deg, cloth / cloth.max(), color=BLUE, ls="--", label="普通平纹布")
    ax.set_xlabel("视线与法线夹角（度）")
    ax.set_ylabel("归一化亮度")
    ax.set_xlim(0, 88)
    ax.legend(loc="upper left")
    ax.annotate("正面凹陷", xy=(0, 0.07), xytext=(18, 0.22), fontsize=8,
                color="#3c4654", arrowprops=dict(arrowstyle="->", color=GREY, lw=0.8))
    save(fig, "fig7-2-models.png")


def render_ball(kind, n=520, Ldir=np.array([0.45, 0.0, 0.89]), Vdir=np.array([0.0, 0.0, 1.0])):
    y, x = np.mgrid[-1:1:n * 1j, -1:1:n * 1j]
    r2 = x ** 2 + y ** 2
    inside = r2 <= 1.0
    z = np.sqrt(np.clip(1.0 - r2, 0.0, 1.0))
    N = np.stack([x, y, z], -1)
    Ld = Ldir / np.linalg.norm(Ldir)
    Vd = Vdir / np.linalg.norm(Vdir)
    ndl = np.clip(N @ Ld, 0, 1)
    ndv = np.clip(N @ Vd, 0, 1)
    out = np.zeros((n, n))
    if kind == "cloth":
        sheen = 0.55 * (1.0 - ndv) ** 5
        out = 0.45 * ndl + sheen * (0.25 + 0.75 * ndl) + 0.08
    else:
        sL = np.sqrt(np.clip(1.0 - (N @ Ld) ** 2, 0, 1))
        sV = np.sqrt(np.clip(1.0 - (N @ Vd) ** 2, 0, 1))
        tau = 3.0 / np.clip(ndv, 0.08, 1.0)
        out = 0.10 + 0.55 * sL * sV + 0.12 * (1 - np.exp(-tau)) * (0.3 + 0.7 * ndl)
    out = np.clip(out, 0, 1) ** (1 / 2.2)
    return np.where(inside, out, np.nan)


def fig7_3():
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.2))
    for ax, kind, title in zip(axes, ["cloth", "velvet"], ["普通平纹布", "绒面天鹅绒"]):
        img = render_ball(kind)
        ax.imshow(np.dstack([img * 0.86, img * 0.83, img * 0.88]), extent=[-1, 1, -1, 1])
        ax.set_title(title, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(True)
            s.set_color("#8a93a0")
    fig.tight_layout()
    save(fig, "fig7-3-ball.png")


fig7_1()
fig7_2()
fig7_3()
