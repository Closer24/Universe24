"""The octahedron and lattice figures of the paper: the Nodes one interval
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
    }
)  # the journal's lettering: Helvetica or Arial, 8 to 12 pt
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

HERE = Path(__file__).resolve().parent
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


def save(fig, path):
    """The PDF the paper includes and the EPS the journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def faces() -> list[list[tuple[int, int, int]]]:
    """The eight triangular faces of the octahedron, one per sign octant."""
    found = []
    for sx, sy, sz in product((1, -1), repeat=3):
        found.append([(sx, 0, 0), (0, sy, 0), (0, 0, sz)])
    return found


def draw(output: Path) -> None:
    fig = plt.figure(figsize=(4.6, 4.4))
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
        color=MID,
        linewidth=0.35,
        alpha=0.7,
    )

    # the octahedron, the L1 unit ball
    collection = Poly3DCollection(faces(), alpha=0.22, facecolor=LIGHT, edgecolor=INK, linewidth=1.1)
    ax.add_collection3d(collection)

    # the six Ports
    for port, label in PORTS.items():
        ax.scatter(*port, color=INK, s=18, depthshade=False)
        offset = tuple(0.17 * c for c in port)
        ax.text(
            *(p + o for p, o in zip(port, offset, strict=True)),
            label,
            color=INK,
            fontsize=9,
            ha="center",
            va="center",
        )

    # the touching points on the cube diagonals, one per face
    for sx, sy, sz in product((1, -1), repeat=3):
        ax.scatter(sx / 3, sy / 3, sz / 3, facecolors="none", edgecolors=INK, s=14, depthshade=False)
    ax.plot([0, 1 / 3], [0, -1 / 3], [0, 1 / 3], color=INK, linewidth=1.0, linestyle="--")
    ax.scatter(0, 0, 0, color=INK, s=8, depthshade=False)
    ax.text(0.40, -0.44, 0.14, r"$1/\sqrt{3}$", color=INK, fontsize=9)

    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_zlim(-1.05, 1.05)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=20, azim=-35)
    ax.set_axis_off()
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    output.mkdir(parents=True, exist_ok=True)
    save(fig, output / "octahedron.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    parser.add_argument("--png", type=Path, default=None, help="also write a PNG preview here")
    args = parser.parse_args()
    draw(args.output)
    if args.png is not None:
        args.png.mkdir(parents=True, exist_ok=True)
        original = plt.Figure.savefig

        def save_png(fig, path, *rest, **options):
            original(fig, args.png / (Path(path).stem + ".png"), dpi=150)

        plt.Figure.savefig = save_png  # type: ignore[method-assign]
        draw(args.output)


if __name__ == "__main__":
    main()
