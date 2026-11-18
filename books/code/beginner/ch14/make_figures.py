import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *

fig, ax = plt.subplots(figsize=(6.8, 3.4))
ax.axis("off")
ax.grid(False)
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.4)

boxes = [
    (0.4, 4.00, "参数与贴图", "base color / metallic\nroughness / normal", GREY),
    (0.4, 2.40, "底层 BSDF", "金属：导体 Fresnel + GGX\n非金属：漫反射 + GGX", BLUE),
    (0.4, 0.80, "涂层", "Fresnel 权重\n几何级数归一化", ACCENT),
]
for x, y, title, body, col in boxes:
    ax.add_patch(plt.Rectangle((x, y), 3.25, 1.15, facecolor="white",
                               edgecolor=col, lw=1.5))
    ax.text(x + 0.18, y + 0.86, title, fontsize=9.5, color=col, fontweight="bold", va="center")
    ax.text(x + 0.18, y + 0.40, body, fontsize=8, color="#303842", va="center")

# 垂直汇流线
ax.plot([4.05, 4.05], [1.38, 4.57], color="#9aa3af", lw=1.2)
for y in [4.57, 2.97, 1.38]:
    ax.annotate("", xy=(4.05, y), xytext=(3.70, y),
                arrowprops=dict(arrowstyle="-|>", color="#9aa3af", lw=1.2,
                                shrinkA=0, shrinkB=0))

ax.annotate("", xy=(4.95, 2.97), xytext=(4.05, 2.97),
            arrowprops=dict(arrowstyle="-|>", color="#9aa3af", lw=1.4,
                            shrinkA=0, shrinkB=0))

ax.add_patch(plt.Rectangle((4.95, 2.30), 2.75, 1.35, facecolor="#f6f7f9",
                           edgecolor="#9aa3af", lw=1.2))
ax.text(6.32, 3.34, "组合", fontsize=9.5, ha="center", color=INK)
ax.text(6.32, 2.92, "f = F·f_coat + (1−F)²·f_base", fontsize=8, ha="center", color=INK)
ax.text(6.32, 2.55, "分母 1 − F·f_base", fontsize=8, ha="center", color=GREY)

ax.annotate("", xy=(8.55, 2.97), xytext=(7.72, 2.97),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.5,
                            shrinkA=0, shrinkB=0))
ax.add_patch(plt.Rectangle((8.55, 2.25), 1.3, 1.45, facecolor="white",
                           edgecolor=BLUE, lw=1.5))
ax.text(9.2, 3.38, "BSDF", fontsize=9.5, ha="center", color=BLUE, fontweight="bold")
ax.text(9.2, 2.94, "eval", fontsize=8, ha="center", color="#303842")
ax.text(9.2, 2.62, "sample", fontsize=8, ha="center", color="#303842")
ax.text(9.2, 2.36, "pdf", fontsize=8, ha="center", color="#303842")

ax.text(0.4, 0.35, "权重之和超过 1 时在编译阶段报错，是避免能量问题最便宜的办法",
        fontsize=8, color=GREY)
save(fig, "fig14-1-structure.png")
