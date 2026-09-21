"""The octahedron figure of the click-model paper: the Nodes one interval
away from a Node form the L1 unit ball |x| + |y| + |z| <= 1, the octahedron
whose six vertices are the six Ports; its inscribed sphere, of radius
1 / sqrt 3, touches the eight faces on the cube diagonals, and that radius
is the rows' pace c = 1 / sqrt 3 Links per interval (the model section of
main.tex; checks/light_speed.py). The unit cube whose group of 48 signed
axis permutations is also the octahedron's is drawn faint behind it.

    python paper/click_model/octahedron.py --output paper/click_model/figures

Needs matplotlib (the `render` extra). Nothing is read from a run.
"""

from __future__ import annotations

import argparse
import math
from itertools import product
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

HERE = Path(__file__).resolve().parent
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED = "#0b0b0b", "#52514e"

PORTS = {
    (1, 0, 0): "$+x$",
    (-1, 0, 0): "$-x$",
    (0, 1, 0): "$+y$",
    (0, -1, 0): "$-y$",
    (0, 0, 1): "$+z$",
    (0, 0, -1): "$-z$",
}


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
        ax.plot(*zip(a, b, strict=True), color="#d8d7d2", linewidth=0.7)

    # the inscribed sphere of radius 1 / sqrt 3
    radius = 1 / math.sqrt(3)
    u, v = np.mgrid[0 : 2 * np.pi : 36j, 0 : np.pi : 18j]
    ax.plot_wireframe(
        radius * np.cos(u) * np.sin(v),
        radius * np.sin(u) * np.sin(v),
        radius * np.cos(v),
        color=ORANGE,
        linewidth=0.35,
        alpha=0.55,
    )

    # the octahedron, the L1 unit ball
    collection = Poly3DCollection(faces(), alpha=0.18, facecolor=BLUE, edgecolor=BLUE, linewidth=1.1)
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
        ax.scatter(sx / 3, sy / 3, sz / 3, color=ORANGE, s=10, depthshade=False)
    ax.plot([0, 1 / 3], [0, -1 / 3], [0, 1 / 3], color=ORANGE, linewidth=1.0)
    ax.scatter(0, 0, 0, color=INK, s=8, depthshade=False)
    ax.text(0.40, -0.44, 0.14, r"$1/\sqrt{3}$", color=ORANGE, fontsize=9)

    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_zlim(-1.05, 1.05)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=20, azim=-35)
    ax.set_axis_off()
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    output.mkdir(parents=True, exist_ok=True)
    fig.savefig(output / "octahedron.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    args = parser.parse_args()
    draw(args.output)


if __name__ == "__main__":
    main()
