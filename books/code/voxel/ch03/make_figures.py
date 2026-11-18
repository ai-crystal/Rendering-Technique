import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
from figstyle import *
import numpy as np

rng = np.random.default_rng(7)


# ---------------------------------------------------------------- 图 3-1
def tri_overlaps_box(v, cell, size):
    """2D 分离轴测试：三角形与轴对齐方格是否相交。"""
    cx, cy = cell
    box = [(cx, cy), (cx + size, cy), (cx, cy + size), (cx + size, cy + size)]
    axes = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
    for i in range(3):
        e = v[(i + 1) % 3] - v[i]
        axes.append(np.array([-e[1], e[0]]))
    for a in axes:
        tp = v @ a
        bp = np.array([p[0] * a[0] + p[1] * a[1] for p in box])
        if tp.max() < bp.min() - 1e-12 or bp.max() < tp.min() - 1e-12:
            return False
    return True


def inside_tri(p, v):
    d = []
    for i in range(3):
        a, b = v[i], v[(i + 1) % 3]
        d.append((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]))
    d = np.array(d)
    return (d >= -1e-12).all() or (d <= 1e-12).all()


def fig3_1():
    size = 1.0
    nx, ny = 12, 8
    v = np.array([[0.6, 0.5], [11.5, 2.9], [2.6, 7.4]])

    samp, cons = [], []
    for i in range(nx):
        for j in range(ny):
            c = (i, j)
            ctr = np.array([i + 0.5, j + 0.5])
            s = inside_tri(ctr, v)
            o = tri_overlaps_box(v, c, size)
            if s:
                samp.append(c)
            if o:
                cons.append(c)

    fig, ax = plt.subplots(figsize=(6.3, 3.9))
    for (i, j) in cons:
        if (i, j) not in samp:
            ax.add_patch(plt.Rectangle((i, j), 1, 1, facecolor=ACCENT, alpha=0.28,
                                       edgecolor="none"))
    for (i, j) in samp:
        ax.add_patch(plt.Rectangle((i, j), 1, 1, facecolor=BLUE, alpha=0.42,
                                   edgecolor="none"))
    for i in range(nx + 1):
        ax.plot([i, i], [0, ny], color=LIGHT, lw=0.6)
    for j in range(ny + 1):
        ax.plot([0, nx], [j, j], color=LIGHT, lw=0.6)
    ax.add_patch(plt.Polygon(v, closed=True, facecolor="none", edgecolor=INK, lw=1.4))

    only = [c for c in cons if c not in samp]
    for (i, j) in only:
        ax.plot(i + 0.5, j + 0.5, "x", color=RED, ms=4)
    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("中心采样（蓝）与保守覆盖（蓝 + 橙），叉号是漏掉的格子", fontsize=8.5)
    ax.text(nx - 0.2, -0.55, f"采样 {len(samp)} 格，保守 {len(cons)} 格",
            ha="right", fontsize=8, color="#3c4654")
    fig.tight_layout()
    save(fig, "fig3-1-coverage.png")


# ---------------------------------------------------------------- 图 3-2
def fig3_2():
    ratios = np.arange(1.0, 8.01, 0.5)
    miss, cells_s, cells_c = [], [], []
    ntri, npts = 240, 900
    for r in ratios:
        m_acc, s_acc, c_acc = 0.0, 0.0, 0.0
        for _ in range(ntri):
            ctr = rng.uniform(0, 40, 2) * 1.0
            ang = rng.uniform(0, 2 * np.pi)
            R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
            # 等边三角形，边长 r
            base = np.array([[0, 0], [r, 0], [r / 2, r * np.sqrt(3) / 2]])
            v = base @ R.T + ctr
            # 在三角形内随机取点，看点所在的格子中心是否落在三角形内
            u = rng.random((npts, 2))
            flip = u.sum(axis=1) > 1
            u[flip] = 1 - u[flip]
            p = v[0] + u[:, :1] * (v[1] - v[0]) + u[:, 1:] * (v[2] - v[0])
            ok = 0
            for q in p[:200]:
                c = np.floor(q)
                if inside_tri(c + 0.5, v):
                    ok += 1
            m_acc += 1.0 - ok / 200.0
            # 覆盖格数（保守）与中心采样格数
            lo = np.floor(v.min(axis=0)) - 1
            hi = np.ceil(v.max(axis=0)) + 1
            ns = nc = 0
            for i in range(int(lo[0]), int(hi[0])):
                for j in range(int(lo[1]), int(hi[1])):
                    if tri_overlaps_box(v, (i, j), 1.0):
                        nc += 1
                    if inside_tri(np.array([i + 0.5, j + 0.5]), v):
                        ns += 1
            area = 0.25 * np.sqrt(3) * r * r
            s_acc += ns / area
            c_acc += nc / area
        miss.append(m_acc / ntri)
        cells_s.append(s_acc / ntri)
        cells_c.append(c_acc / ntri)

    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(ratios, np.array(miss) * 100, color=RED, marker="o", ms=3,
            label="未被覆盖的面积（中心采样）")
    ax.set_xlabel("三角形边长 / 体素边长")
    ax.set_ylabel("未被中心采样覆盖的面积（%）")
    ax.set_ylim(0, 100)
    ax2 = ax.twinx()
    ax2.plot(ratios, cells_s, color=BLUE, marker="s", ms=3, ls="--",
             label="中心采样写入格数")
    ax2.plot(ratios, cells_c, color=GREEN, marker="^", ms=3, ls="-.",
             label="保守覆盖写入格数")
    ax2.set_ylabel("每单位三角形面积写入的格数")
    ax2.grid(False)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper center", fontsize=7.5)
    fig.tight_layout()
    save(fig, "fig3-2-miss-rate.png")


# ---------------------------------------------------------------- 图 3-3
def fig3_3():
    hr = np.linspace(0.005, 0.4, 200)
    err = np.rad2deg(hr / 2.0)
    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    ax.plot(hr, err, color=BLUE, label=r"面积加权平均，$h/(2R)$")
    ax.axhline(45.0, color=ACCENT, ls="--", lw=1.3, label="格子面法线（与 h 无关）")
    ax.set_xlabel("体素边长 / 曲率半径")
    ax.set_ylabel("法线角度误差（度）")
    ax.set_ylim(0, 52)
    ax.legend(loc="center right")
    note(ax, "平均法线把误差压到 h/(2R)，代价是一个格子只有一个朝向", 0.03, 0.93)
    fig.tight_layout()
    save(fig, "fig3-3-normal-average.png")


if __name__ == "__main__":
    fig3_1()
    fig3_2()
    fig3_3()
