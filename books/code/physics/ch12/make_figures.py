import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
from matplotlib.patches import Rectangle, FancyArrowPatch

D2R = np.pi / 180


def battery(ax, x, y, label, r_label=None):
    ax.plot([x - 0.06, x - 0.06], [y - 0.16, y + 0.16], color=INK, lw=2.0)
    ax.plot([x + 0.06, x + 0.06], [y - 0.09, y + 0.09], color=INK, lw=1.0)
    ax.text(x, y + 0.26, label, ha="center", fontsize=8)


def resistor(ax, x0, x1, y, label):
    ax.add_patch(Rectangle((x0, y - 0.09), x1 - x0, 0.18, facecolor="white",
                           edgecolor=INK, lw=1.1, zorder=3))
    ax.text((x0 + x1) / 2, y + 0.20, label, ha="center", fontsize=8)


def fig12_1():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    ax = axes[0]
    ax.set_xlim(0, 4.4)
    ax.set_ylim(-1.0, 2.4)
    ax.axis("off")
    ax.grid(False)
    ax.plot([0.5, 0.5], [0.3, 1.7], color=INK, lw=1.1)
    ax.plot([3.5, 3.5], [0.3, 1.7], color=INK, lw=1.1)
    ax.plot([0.5, 1.1], [1.7, 1.7], color=INK, lw=1.1)
    ax.plot([2.9, 3.5], [1.7, 1.7], color=INK, lw=1.1)
    resistor(ax, 1.1, 2.9, 1.7, "$R$")
    ax.plot([0.5, 0.5], [0.3, 0.3], color=INK, lw=1.1)
    ax.plot([0.5, 1.5], [0.3, 0.3], color=INK, lw=1.1)
    ax.plot([2.5, 3.5], [0.3, 0.3], color=INK, lw=1.1)
    battery(ax, 2.0, 0.3, "$\\mathcal{E}$")
    ax.text(2.0, -0.32, "$r$", ha="center", fontsize=8)
    ax.annotate("", xy=(0.35, 1.0), xytext=(0.65, 1.0),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.1, mutation_scale=7))
    ax.text(0.18, 1.06, "$I$", fontsize=8.5, color=BLUE)
    ax.set_title("电源与负载", fontsize=8.8)

    ax = axes[1]
    E, r = 12.0, 1.5
    I = np.linspace(0, E / r, 200)
    ax.plot(I, E - r * I, color=BLUE)
    ax.annotate("$\\mathcal{E}$", (0, E), xytext=(0.35, E - 0.5), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.plot([E / r], [0], "o", ms=4, color=ACCENT)
    ax.text(E / r - 0.6, 0.45, "短路", fontsize=8, color=ACCENT, ha="right")
    ax.set_xlabel("电流 $I$（A）")
    ax.set_ylabel("端电压 $U$（V）")
    ax.set_xlim(0, E / r * 1.02)
    ax.set_ylim(0, E * 1.08)
    ax.set_title("$U=\\mathcal{E}-Ir$", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig12-1-emf.png")


def fig12_2():
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.set_xlim(0, 7.2)
    ax.set_ylim(-0.6, 4.4)
    ax.axis("off")
    ax.grid(False)
    # 左回路
    ax.plot([0.6, 0.6], [0.4, 3.4], color=INK, lw=1.1)
    ax.plot([0.6, 3.4], [3.4, 3.4], color=INK, lw=1.1)
    ax.plot([0.6, 3.4], [0.4, 0.4], color=INK, lw=1.1)
    ax.plot([3.4, 3.4], [0.4, 3.4], color=INK, lw=1.1)
    resistor(ax, 1.3, 2.7, 3.4, "$R_1=4\\ \\Omega$")
    battery(ax, 0.6, 2.0, "$\\mathcal{E}_1=12$ V")
    ax.text(0.85, 2.0, "$r_1=1\\ \\Omega$", fontsize=7.5, va="center")
    # 右回路
    ax.plot([3.4, 6.4], [3.4, 3.4], color=INK, lw=1.1)
    ax.plot([3.4, 6.4], [0.4, 0.4], color=INK, lw=1.1)
    ax.plot([6.4, 6.4], [0.4, 3.4], color=INK, lw=1.1)
    resistor(ax, 4.1, 5.6, 3.4, "$R_2=2\\ \\Omega$")
    battery(ax, 6.4, 2.0, "$\\mathcal{E}_2=6$ V")
    ax.text(6.0, 2.0, "$r_2=1\\ \\Omega$", fontsize=7.5, va="center", ha="right")
    resistor(ax, 3.4 - 0.0, 3.4, 2.0, "")
    ax.add_patch(Rectangle((3.30, 1.6), 0.20, 1.0, facecolor="white",
                           edgecolor=INK, lw=1.1, zorder=3))
    ax.text(3.62, 2.1, "$R_3=6\\ \\Omega$", fontsize=7.8)
    ax.annotate("", xy=(3.0, 3.12), xytext=(2.0, 3.12),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.1, mutation_scale=7))
    ax.text(2.1, 2.86, "$I_1$", fontsize=8.5, color=BLUE)
    ax.annotate("", xy=(5.4, 3.12), xytext=(4.4, 3.12),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.1, mutation_scale=7))
    ax.text(5.2, 2.86, "$I_2$", fontsize=8.5, color=ACCENT)
    ax.text(1.9, -0.3, "回路 1", fontsize=8.5, color=INK)
    ax.text(4.9, -0.3, "回路 2", fontsize=8.5, color=INK)
    save(fig, "fig12-2-two-loop.png")


def fig12_3():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    ax = axes[0]
    ax.set_xlim(-1.6, 1.9)
    ax.set_ylim(-1.5, 1.5)
    ax.axis("off")
    ax.grid(False)
    pts = {"A": (0, 1.2), "B": (1.1, 0), "C": (0, -1.2), "D": (-1.1, 0)}
    for a, b in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]:
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], color=INK, lw=1.0)
    labels = {"A": "$R_1$", "B": "$R_2$", "C": "$R_3$", "D": "$R_4$"}
    for a, b in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]:
        mx, my = (pts[a][0] + pts[b][0]) / 2, (pts[a][1] + pts[b][1]) / 2
        ax.text(mx, my, labels[a], fontsize=8.5, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.16", fc="white", ec=GREY, lw=0.6))
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], color=INK, lw=1.0)
    ax.plot([0, 0], [1.2, -1.2], color=TEAL, lw=0.9)
    ax.text(0.10, 0.0, "G", fontsize=8.5, color=TEAL)
    ax.plot([-1.1, -1.55], [0, 0], color=INK, lw=1.0)
    ax.plot([1.1, 1.55], [0, 0], color=INK, lw=1.0)
    ax.plot([-1.55, -1.55], [-0.3, 0.3], color=INK, lw=2.0)
    ax.plot([1.55, 1.55], [-0.18, 0.18], color=INK, lw=1.0)
    ax.text(-1.55, 0.45, "$\\mathcal{E}$", fontsize=8.5, ha="center")
    ax.set_title("惠斯通电桥", fontsize=8.8)

    ax = axes[1]
    R1, R2, R3 = 100.0, 200.0, 150.0
    R4 = np.linspace(100, 500, 300)
    # 检流计电流比例：正比于两中点电势差
    dU = R1 / (R1 + R2) - R3 / (R3 + R4)
    ax.plot(R4, dU * 1e3, color=BLUE)
    ax.axhline(0, color=GREY, lw=0.8)
    Rbal = R2 * R3 / R1
    ax.plot([Rbal], [0], "o", ms=5, color=ACCENT)
    ax.annotate(f"$R_4={Rbal:.0f}\\ \\Omega$", (Rbal, 0), xytext=(Rbal + 40, 60),
                fontsize=7.8, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
    ax.set_xlabel("$R_4$（$\\Omega$）")
    ax.set_ylabel("两中点电势差（相对值）")
    ax.set_title("平衡点附近", fontsize=8.8)
    fig.tight_layout()
    save(fig, "fig12-3-bridge.png")


fig12_1()
fig12_2()
fig12_3()
