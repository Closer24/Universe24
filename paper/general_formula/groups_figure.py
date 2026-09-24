"""Draw how a click is reached from the groups (the model owner's word of
2026-09-24: "with a hexagon if possible, and a cube; a few things one inside
the other"). Drawn from the definitions (docs/ALGEBRA.md chapters 1, 2, 3
and 8; docs/GLOSSARY.md); no run. Writes figures/groups_to_click.pdf.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle  # noqa: E402


def cube(ax, cx, cy, s):
    """A cube in oblique view with its six face centres marked (the six Ports)."""
    d = 0.42 * s
    front = [
        (cx - s / 2, cy - s / 2),
        (cx + s / 2, cy - s / 2),
        (cx + s / 2, cy + s / 2),
        (cx - s / 2, cy + s / 2),
    ]
    back = [(x + d, y + d) for (x, y) in front]
    ax.add_patch(Polygon(back, closed=True, fc="none", ec="#888888", lw=0.8, ls="--"))
    for a, b in zip(front, back, strict=True):
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#888888", lw=0.8, ls="--")
    ax.add_patch(Polygon(front, closed=True, fc="none", ec="black", lw=1.0))
    # The six face centres: right, left, top, bottom (mid-depth), front, back.
    h = d / 2
    centres = [
        (cx + s / 2 + h, cy + h),
        (cx - s / 2 + h, cy + h),
        (cx + h, cy + s / 2 + h),
        (cx + h, cy - s / 2 + h),
        (cx, cy),
        (cx + d, cy + d),
    ]
    for x, y in centres:
        ax.plot(x, y, "o", color="#2b4c7e", ms=4)
    return centres


def hexagon(ax, cx, cy, r):
    """The same six Ports seen along a body diagonal: a hexagon's vertices."""
    pts = [
        (cx + r * np.cos(np.pi / 6 + k * np.pi / 3), cy + r * np.sin(np.pi / 6 + k * np.pi / 3))
        for k in range(6)
    ]
    ax.add_patch(Polygon(pts, closed=True, fc="none", ec="black", lw=1.0))
    for x, y in pts:
        ax.plot(x, y, "o", color="#2b4c7e", ms=4)
    for k in range(3):
        ax.plot([pts[k][0], pts[k + 3][0]], [pts[k][1], pts[k + 3][1]], color="#bbbbbb", lw=0.7)
    return pts


def draw(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.2, 4.9))
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 7.0)
    ax.set_aspect("equal")
    ax.axis("off")
    # 1. The first group: the cube and its hexagon.
    ax.text(0.2, 6.7, "1. the first group,\non the directions", fontsize=7.4, weight="bold", va="top")
    cube(ax, 1.5, 4.6, 1.5)
    ax.text(
        0.2,
        3.35,
        "the six Ports, the face centres;\nthe $48$ signed permutations, the\n$24$ rotations the group of order $24$",
        fontsize=6.6,
        va="top",
    )
    hexagon(ax, 1.5, 1.35, 0.85)
    ax.text(
        2.55,
        1.6,
        "the same six Ports\nalong a body diagonal:\nthe hexagon; the cubic\npattern of the dispersion",
        fontsize=6.4,
        va="top",
    )
    # 2. Inside one Node: the record, its pair, and the second group, the phase circle.
    ax.add_patch(
        FancyBboxPatch(
            (4.55, 2.4), 3.2, 3.6, boxstyle="round,pad=0.02", fc="#fbfbfb", ec="black", lw=1.0
        )
    )
    ax.text(
        4.7, 6.7, "2. one Node: the record,\nthe second group", fontsize=7.4, weight="bold", va="top"
    )
    ax.text(
        4.7,
        5.85,
        "two integer levels $(a_{\\rm before}, a_{\\rm now})$\nand a remainder; one pair per kind,\n$[\\mathrm{num}, \\mathrm{den}]$: the mass",
        fontsize=6.6,
        va="top",
    )
    circ = Circle((6.15, 3.65), 0.85, fc="none", ec="black", lw=1.0)
    ax.add_patch(circ)
    for k in range(12):
        a = 2 * np.pi * k / 12
        ax.plot(6.15 + 0.85 * np.cos(a), 3.65 + 0.85 * np.sin(a), "o", color="black", ms=2)
    ax.add_patch(
        FancyArrowPatch(
            (6.15 + 0.85 * np.cos(0.3), 3.65 + 0.85 * np.sin(0.3)),
            (6.15 + 0.85 * np.cos(1.1), 3.65 + 0.85 * np.sin(1.1)),
            connectionstyle="arc3,rad=0.3",
            arrowstyle="-|>",
            mutation_scale=10,
            lw=1.0,
            color="#8a1c1c",
        )
    )
    ax.text(6.15, 3.65, "$\\mathbb{Z}_N$", fontsize=8, ha="center", va="center")
    ax.text(
        4.7,
        2.65,
        "the phase circle: the record's phase\nadvances by the wheel; a table shifts it\nby $t$, linear on the pair",
        fontsize=6.4,
        va="top",
    )
    # 3. The block inside the board, the detector around it.
    ax.text(
        8.45,
        6.7,
        "3. the block on the board,\nthe rung around it",
        fontsize=7.4,
        weight="bold",
        va="top",
    )
    ax.add_patch(
        FancyBboxPatch((8.3, 2.4), 4.6, 3.6, boxstyle="round,pad=0.02", fc="#f4f4f4", ec="black", lw=1.0)
    )
    ax.text(8.45, 5.85, "the GameBoard", fontsize=6.8, style="italic", va="top")
    x0, y0, d = 8.7, 2.85, 0.38
    for i in range(9):
        for j in range(7):
            ax.plot(x0 + d * i, y0 + d * j, "o", color="#999999", ms=1.6)
    ax.add_patch(
        Rectangle(
            (x0 + d * 3 - 0.1, y0 + d * 2 - 0.1),
            d * 3 + 0.2,
            d * 3 + 0.2,
            fc="#dbe6f5",
            ec="#2b4c7e",
            lw=1.0,
        )
    )
    ax.text(
        x0 + d * 4.5,
        y0 + d * 3.5,
        "the block:\ncells of the\n48's shape,\na lower pair;\nits bound mode\nthe clock",
        fontsize=5.4,
        ha="center",
        va="center",
    )
    ax.add_patch(
        Rectangle(
            (x0 + d * 3 - 0.28, y0 + d * 2 - 0.28),
            d * 3 + 0.56,
            d * 3 + 0.56,
            fc="none",
            ec="#8a5a00",
            lw=1.2,
            ls="--",
        )
    )
    ax.text(
        x0 + d * 7.4,
        y0 + d * 5.4,
        "the detector's cells,\nthe rung $W$",
        fontsize=5.6,
        ha="center",
        color="#8a5a00",
    )
    # 4. The click.
    ax.add_patch(
        FancyBboxPatch(
            (8.3, 0.25), 4.6, 1.75, boxstyle="round,pad=0.02", fc="#eaf3e6", ec="black", lw=1.0
        )
    )
    ax.text(8.45, 1.85, "4. the click", fontsize=8, weight="bold", va="top")
    ax.text(
        8.45,
        1.4,
        "the quadratic form of the record's values in the\ncells crosses $W$: one click, in the detector's own\ncount, with the record's birth stamp; one per record,\nits completion one gather over its detectors",
        fontsize=6.2,
        va="top",
    )
    # The arrows of the chain.
    for a, b in [((3.5, 4.6), (4.5, 4.6)), ((7.8, 4.4), (8.25, 4.4))]:
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, lw=1.1, color="black"))
    ax.add_patch(
        FancyArrowPatch(
            (10.6, 2.35), (10.6, 2.05), arrowstyle="-|>", mutation_scale=12, lw=1.1, color="black"
        )
    )
    ax.text(4.0, 4.75, "the rule\ncommutes", fontsize=6, ha="center")
    ax.text(8.02, 4.55, "on every\ncell", fontsize=6, ha="center")
    ax.text(
        0.2,
        0.15,
        "the band from the group and the pair; the tables from the circle; the clock from the block; the click from the rung",
        fontsize=6.6,
    )
    fig.savefig(output / "groups_to_click.pdf", bbox_inches="tight")


if __name__ == "__main__":
    draw(Path(__file__).resolve().parent / "figures")
