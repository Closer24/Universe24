"""The lattice and octahedron figures of the paper, drawn from the definitions.

The lattice: a cubic array of Nodes, here 6 x 6 x 6, each joined to its six
neighbours by Links through the Ports, one Node and its six neighbours marked.
The octahedron: the Nodes one interval
away from a Node form the L1 unit ball |x| + |y| + |z| <= 1, the octahedron
whose six vertices are the six Ports; its inscribed sphere, of radius
1 / sqrt 3, touches the eight faces on the cube diagonals, and that radius
is light's speed at long wavelength, 1 / sqrt 3 Links per interval
(docs/ALGEBRA.md, the lattice constants). The unit cube whose group of 48 signed
axis permutations is also the octahedron's is drawn faint behind it.

    python paper/general_formula/octahedron.py --output paper/general_formula/figures

Needs matplotlib (the `render` extra). Nothing is read from a run.
"""

from __future__ import annotations

import argparse
import math
from itertools import product
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
        "font.size": 8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)  # the journal's lettering: Helvetica or Arial, 8 to 12 pt at the final size, fonts embedded
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

HERE = Path(__file__).resolve().parent
# The final printed width of each figure in inches, at most 119 mm (4.69 in), drawn 1:1.
SIDE = 2.6
BOX = {"boxstyle": "square,pad=0.05", "facecolor": "white", "edgecolor": "none"}
# Black and white only.
INK, DARK, MID, LIGHT, PALE = "#000000", "#404040", "#808080", "#c8c8c8", "#e4e4e4"

PORTS = {
    (1, 0, 0): "$+x$",
    (-1, 0, 0): "$-x$",
    (0, 1, 0): "$+y$",
    (0, -1, 0): "$-y$",
    (0, 0, 1): "$+z$",
    (0, 0, -1): "$-z$",
}


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS the journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def faces() -> list[list[tuple[int, int, int]]]:
    """The eight triangular faces of the octahedron, one per sign octant."""
    found = []
    for sx, sy, sz in product((1, -1), repeat=3):
        found.append([(sx, 0, 0), (0, sy, 0), (0, 0, sz)])
    return found


def lattice(output: Path) -> None:
    panel = "(a)"
    """The lattice in space: 6 x 6 x 6 Nodes, the Links faint, one Node and its six neighbours marked."""
    n = 6
    fig = plt.figure(figsize=(SIDE, SIDE))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_proj_type("ortho")
    span = range(n)
    for a in span:
        for b in span:
            ax.plot([0, n - 1], [a, a], [b, b], color=PALE, linewidth=0.4)
            ax.plot([a, a], [0, n - 1], [b, b], color=PALE, linewidth=0.4)
            ax.plot([a, a], [b, b], [0, n - 1], color=PALE, linewidth=0.4)
    nodes = [(i, j, k) for i in span for j in span for k in span]
    ax.scatter(*zip(*nodes, strict=True), s=3, color=MID, depthshade=False)
    centre = (2, 2, 2)
    for port, label in PORTS.items():
        neighbour = tuple(c + d for c, d in zip(centre, port, strict=True))
        ax.plot(*zip(centre, neighbour, strict=True), color=INK, linewidth=1.4)
        ax.scatter(*neighbour, s=18, color="white", edgecolors=INK, linewidths=0.9, depthshade=False)
        ax.text(
            *(c + 1.75 * d for c, d in zip(centre, port, strict=True)),
            label,
            ha="center",
            va="center",
            color=INK,
            bbox=BOX,
        )
    ax.scatter(*centre, s=26, color=INK, depthshade=False)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=-58)
    ax.set_axis_off()
    fig.subplots_adjust(left=-0.08, right=1.08, bottom=-0.08, top=1.08)
    fig.text(0.03, 0.97, panel, ha="left", va="top", color=INK)
    output.mkdir(parents=True, exist_ok=True)
    save(fig, output / "lattice.pdf")
    plt.close(fig)


def draw(output: Path) -> None:
    panel = "(b)"
    fig = plt.figure(figsize=(SIDE, SIDE))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_proj_type("ortho")

    # the unit cube, the group of 48 shared by both solids
    for a, b in (
        ((-1, -1, -1), (1, -1, -1)),
        ((-1, -1, -1), (-1, 1, -1)),
        ((-1, -1, -1), (-1, -1, 1)),
        ((1, 1, 1), (-1, 1, 1)),
        ((1, 1, 1), (1, -1, 1)),
        ((1, 1, 1), (1, 1, -1)),
        ((1, -1, -1), (1, 1, -1)),
        ((1, -1, -1), (1, -1, 1)),
        ((-1, 1, -1), (1, 1, -1)),
        ((-1, 1, -1), (-1, 1, 1)),
        ((-1, -1, 1), (1, -1, 1)),
        ((-1, -1, 1), (-1, 1, 1)),
    ):
        ax.plot(*zip(a, b, strict=True), color=LIGHT, linewidth=0.7)

    # the inscribed sphere of radius 1 / sqrt 3
    radius = 1 / math.sqrt(3)
    u, v = np.mgrid[0 : 2 * np.pi : 36j, 0 : np.pi : 18j]
    ax.plot_wireframe(
        radius * np.cos(u) * np.sin(v),
        radius * np.sin(u) * np.sin(v),
        radius * np.cos(v),
        color=LIGHT,
        linewidth=0.35,
    )

    # the octahedron, the L1 unit ball
    collection = Poly3DCollection(faces(), facecolor="none", edgecolor=INK, linewidth=1.1)
    ax.add_collection3d(collection)

    # the six Ports
    for port, label in PORTS.items():
        ax.scatter(*port, color=INK, s=18, depthshade=False)
        offset = tuple(0.17 * c for c in port)
        ax.text(
            *(p + o for p, o in zip(port, offset, strict=True)),
            label,
            color=INK,
            ha="center",
            va="center",
            bbox=BOX,
        )

    # the touching points on the cube diagonals, one per face
    for sx, sy, sz in product((1, -1), repeat=3):
        ax.scatter(sx / 3, sy / 3, sz / 3, facecolors="none", edgecolors=INK, s=14, depthshade=False)
    ax.plot([0, 1 / 3], [0, -1 / 3], [0, 1 / 3], color=INK, linewidth=1.0, linestyle="--")
    ax.scatter(0, 0, 0, color=INK, s=8, depthshade=False)
    fig.text(0.97, 0.03, r"the dashed radius: $1/\sqrt{3}$", ha="right", color=INK)

    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_zlim(-1.05, 1.05)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=20, azim=-35)
    ax.set_axis_off()
    fig.subplots_adjust(left=-0.08, right=1.08, bottom=-0.08, top=1.08)
    fig.text(0.03, 0.97, panel, ha="left", va="top", color=INK)
    output.mkdir(parents=True, exist_ok=True)
    save(fig, output / "octahedron.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    args = parser.parse_args()
    lattice(args.output)
    draw(args.output)


if __name__ == "__main__":
    main()
