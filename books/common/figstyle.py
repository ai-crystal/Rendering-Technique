#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全系列共用的插图样式。各章脚本只需：

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "common"))
    from figstyle import *

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ...
    save(fig, "fig1-1-lobes.png")

图会存到 books/<册名>/images/<章号>/ 下。
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"],
    "font.family": "sans-serif",
    "axes.unicode_minus": False,
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "axes.grid": True,
    "grid.alpha": 0.22,
    "grid.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#5b6472",
    "axes.labelcolor": "#1f2430",
    "xtick.color": "#3c4654",
    "ytick.color": "#3c4654",
    "font.size": 9,
    "axes.titlesize": 9.5,
    "axes.labelsize": 9,
    "legend.fontsize": 8,
    "legend.frameon": False,
    "lines.linewidth": 1.7,
    "lines.antialiased": True,
})

INK = "#1f2430"
ACCENT = "#b5651d"
BLUE = "#2f6f9f"
SKY = "#6fa3c8"
TEAL = "#2f8f8a"
RED = "#b0453c"
GREY = "#8a93a0"
LIGHT = "#c8ccd4"
GOLD = "#c9973a"
PURPLE = "#6b4b8a"
GREEN = "#4f7a4a"

PALETTE = [ACCENT, BLUE, TEAL, RED, PURPLE, GREEN, GOLD, GREY]


def save(fig, name, pad=0.02, transparent=False):
    here = Path(sys.argv[0]).resolve().parent
    book = here.parent.name
    ch = here.name
    out = here.parents[2] / book / "images" / ch[2:]
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / name, bbox_inches="tight", pad_inches=pad,
                facecolor="none" if transparent else "white",
                transparent=transparent)
    plt.close(fig)
    print("saved", (out / name).as_posix())


def note(ax, text, x=0.02, y=0.96, color="#3c4654", size=8):
    ax.text(x, y, text, transform=ax.transAxes, ha="left", va="top",
            color=color, fontsize=size)


def panel_label(ax, s, x=-0.16, y=1.10):
    ax.text(x, y, s, transform=ax.transAxes, ha="left", va="top",
            fontsize=10, fontweight="bold", color=INK)
