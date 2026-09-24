"""Draw the three worlds as a square within a square (the model owner's word
of 2026-09-24): the GameBoard inside the clicks, and what the clicks lead to,
nature. Drawn from the definitions (docs/ALGEBRA.md chapters 1, 3 and 8;
docs/GLOSSARY.md sections 4 to 6); no run. Writes figures/worlds.pdf.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402


def draw(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    ax.set_xlim(0, 12.8)
    ax.set_ylim(-0.45, 7.0)
    ax.set_aspect("equal")
    ax.axis("off")
    # The outer square: the clicks, the Outside.
    ax.add_patch(
        FancyBboxPatch(
            (0.25, 0.25), 8.6, 6.5, boxstyle="round,pad=0.02", fc="#f4f4f4", ec="black", lw=1.2
        )
    )
    ax.text(
        0.45, 6.4, "the clicks (the Outside): detectors and their clicks only", fontsize=9, weight="bold"
    )
    # The inner square: the GameBoard, the Inside.
    ax.add_patch(
        FancyBboxPatch((0.7, 1.95), 7.7, 4.1, boxstyle="round,pad=0.02", fc="white", ec="black", lw=1.2)
    )
    ax.text(0.85, 5.72, "the GameBoard (the Inside): where no one measures", fontsize=9, weight="bold")
    # A small lattice of Nodes with a block of cells.
    x0, y0, d = 1.05, 2.25, 0.42
    for i in range(6):
        for j in range(6):
            x, y = x0 + d * i, y0 + d * j
            if i < 5:
                ax.plot([x, x + d], [y, y], color="#bbbbbb", lw=0.6, zorder=1)
            if j < 5:
                ax.plot([x, x], [y, y + d], color="#bbbbbb", lw=0.6, zorder=1)
            ax.plot(x, y, "o", color="black", ms=2.2, zorder=2)
    ax.add_patch(
        Rectangle(
            (x0 + d * 3 - 0.12, y0 + d * 1 - 0.12),
            d * 2 + 0.24,
            d * 2 + 0.24,
            fc="#dbe6f5",
            ec="#2b4c7e",
            lw=1.0,
            zorder=0,
        )
    )
    ax.text(x0 + d * 4, y0 + d * 1.0 - 0.34, "a block", fontsize=6.8, ha="center", color="#2b4c7e")
    lines = [
        "the symmetry group of the cube: $48 = 24$ rotations $+$ reflections",
        "the phase circle $\\mathbb{Z}_N$: the record's clock, a second group",
        "a record at a Node: two integer levels and a remainder",
        "one pair per kind: light $[1, 1]$, matter $[800, 809]$; the mass",
        "the block: cells of the 48's shape with a lower pair;",
        "   its clock the bound mode of its record",
        "a foreign object's table: a shift t of the phase on $\\mathbb{Z}_N$, linear",
        "one rule of six operations at every Node and interval",
    ]
    for k, line in enumerate(lines):
        ax.text(3.65, 5.35 - 0.38 * k, line, fontsize=6.1, va="top")
    # The detectors on the rim of the inner square.
    for x, y in [(0.7, 3.4), (8.4, 3.0), (4.4, 1.95)]:
        ax.add_patch(
            Rectangle((x - 0.16, y - 0.16), 0.32, 0.32, fc="#f7d9a8", ec="#8a5a00", lw=1.0, zorder=3)
        )
    ax.text(
        0.5,
        1.55,
        "a detector: a set of Nodes with a rung $W$; it counts when the quadratic form of the record's values\n"
        "in its cells crosses $W$; a body is a detector of itself; one click per record, its completion one gather\n"
        "over its detectors, the one non-local step",
        fontsize=6.2,
        va="top",
    )
    ax.text(
        0.5,
        0.62,
        "the click list: (the Node, the detector's own count, the record's birth stamp); nothing else leaves the Inside",
        fontsize=6.5,
        weight="bold",
        va="top",
    )
    # What the clicks lead to: nature.
    ax.add_patch(
        FancyBboxPatch(
            (9.4, 0.7), 3.15, 5.6, boxstyle="round,pad=0.02", fc="#eaf3e6", ec="black", lw=1.2
        )
    )
    ax.text(9.55, 6.05, "nature", fontsize=9, weight="bold", va="top")
    ax.text(9.55, 5.55, "counts per Node:\nthe fringes, Malus, Bell", fontsize=6.8, va="top")
    ax.text(
        9.55,
        4.85,
        "counts between clicks on\na body's record: the clock,\nthe muon, the redshift",
        fontsize=6.8,
        va="top",
    )
    ax.text(9.55, 3.85, "from the birth to the click:\nSagnac, the light clock", fontsize=6.8, va="top")
    ax.text(
        9.55,
        3.15,
        'every row a ratio, so no\nunits enter; "matches",\nnever "is"',
        fontsize=6.8,
        style="italic",
        va="top",
    )
    ax.text(
        9.55,
        2.15,
        "the 48 seen in $c$'s isotropy\nand the cubic dispersion;\n$\\mathbb{Z}_N$ in $2\\sqrt{2}$ and $\\cos^2$;\nthe pair in the clocks",
        fontsize=6.4,
        va="top",
    )
    ax.add_patch(
        FancyArrowPatch(
            (8.9, 3.5), (9.35, 3.5), arrowstyle="-|>", mutation_scale=14, lw=1.2, color="black"
        )
    )
    ax.text(9.12, 3.68, "ratios", fontsize=6.5, ha="center")
    # The passage, written under the squares.
    ax.text(
        0.25,
        -0.2,
        "the passage: the algebra $\\rightarrow$ the pin, computed before the run $\\rightarrow$ the run Inside $\\rightarrow$ the clicks Outside $\\rightarrow$ a ratio $\\rightarrow$ nature's number",
        fontsize=7.4,
    )
    fig.savefig(output / "worlds.pdf", bbox_inches="tight")


if __name__ == "__main__":
    draw(Path(__file__).resolve().parent / "figures")
