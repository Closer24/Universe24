"""Draw how a click is reached from the groups, in the paper's grey, in three
dimensions and with few words (the model owner's words of 2026-09-24: a
cube, a hexagon, an octahedron, things one inside the other). Drawn from the
definitions (docs/ALGEBRA.md chapters 1, 3 and 8; docs/GLOSSARY.md); no run.
Writes figures/groups_to_click.pdf.
"""

from itertools import product
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
matplotlib.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
        "font.size": 8,
    }
)  # the journal's lettering: Helvetica or Arial, 8 to 12 pt
import matplotlib.pyplot as plt  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

GREY = "#555555"
LIGHT = "#bbbbbb"
PORTS = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], dtype=float)


def save(fig, path):
    """The PDF the paper includes and the EPS the journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def wire_cube(ax, centre, half, color=GREY, lw=0.9, ls="-"):
    c = np.asarray(centre, dtype=float)
    corners = np.array(list(product([-half, half], repeat=3))) + c
    for i, a in enumerate(corners):
        for b in corners[i + 1 :]:
            if np.sum(np.abs(a - b) > 1e-9) == 1:
                ax.plot([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], color=color, lw=lw, ls=ls)


def octahedron(ax, centre, r, alpha=0.18):
    c = np.asarray(centre, dtype=float)
    v = PORTS * r + c
    faces = []
    for sx, sy, sz in product([0, 1], repeat=3):
        faces.append([v[sx], v[2 + sy], v[4 + sz]])
    ax.add_collection3d(
        Poly3DCollection(faces, facecolors="#dddddd", edgecolors=GREY, linewidths=0.7, alpha=alpha)
    )


def bare(ax):
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 1))


def draw(output: Path) -> None:
    fig = plt.figure(figsize=(9.6, 3.1))
    # 1. The cube and the octahedron: the six Ports, the symmetry group of the cube.
    ax = fig.add_subplot(1, 4, 1, projection="3d")
    wire_cube(ax, (0, 0, 0), 1.0)
    octahedron(ax, (0, 0, 0), 1.0)
    ax.scatter(PORTS[:, 0], PORTS[:, 1], PORTS[:, 2], color="black", s=16, depthshade=False)
    ax.view_init(elev=22, azim=-55)
    lim = 1.25
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    bare(ax)
    ax.set_title(
        "the six Ports: the cube's group, $48$;\nits rotations, $24$; the octahedron, the front",
        fontsize=8.2,
        color="black",
    )
    # 2. The same six Ports along a body diagonal: the hexagon.
    ax = fig.add_subplot(1, 4, 2, projection="3d")
    wire_cube(ax, (0, 0, 0), 1.0, color=LIGHT)
    octahedron(ax, (0, 0, 0), 1.0, alpha=0.25)
    ax.scatter(PORTS[:, 0], PORTS[:, 1], PORTS[:, 2], color="black", s=16, depthshade=False)
    ax.view_init(elev=35.264, azim=45)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    bare(ax)
    ax.set_title("along a body diagonal:\nthe hexagon, the cubic pattern", fontsize=8.2, color="black")
    # 3. The GameBoard with the block of cells inside it: the block is the detector, its rung W;
    #    a light record runs on the free Nodes and passes through the block.
    ax = fig.add_subplot(1, 4, 3, projection="3d")
    n = 5
    g = np.array(list(product(range(n), repeat=3)), dtype=float)
    ax.scatter(g[:, 0], g[:, 1], g[:, 2], color=LIGHT, s=4, depthshade=False)
    wire_cube(ax, (2, 2, 2), 2.0, color=LIGHT, lw=0.6)
    wire_cube(ax, (2, 2, 2), 0.5, color="black", lw=1.1)
    ax.text(2.55, 2.0, 2.65, "$W$", fontsize=8, color="black")
    ax.plot([-0.1, 4.1], [2.0, 2.0], [2.0, 2.0], color=GREY, lw=1.0)
    # The phase circle on the block: the record's clock, a ring around the block's centre.
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(2 + 0.75 * np.cos(t), 2 + 0.75 * np.sin(t), 2 + 0 * t, color="black", lw=0.8)
    for k in range(12):
        a = 2 * np.pi * k / 12
        ax.scatter(
            [2 + 0.75 * np.cos(a)], [2 + 0.75 * np.sin(a)], [2], color="black", s=5, depthshade=False
        )
    ax.view_init(elev=20, azim=-50)
    ax.set_xlim(-0.2, 4.2)
    ax.set_ylim(-0.2, 4.2)
    ax.set_zlim(-0.2, 4.2)
    bare(ax)
    ax.set_title(
        "on the board: the block is the detector, its rung $W$;\nthe circle $\\mathbb{Z}_N$ the record's clock; light through it",
        fontsize=8.2,
        color="black",
    )
    # 4. The click: the quadratic form in the cells crossing the rung.
    ax = fig.add_subplot(1, 4, 4)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    x = np.linspace(0.08, 0.92, 200)
    y = 0.22 + 0.55 * (1 - np.exp(-((x - 0.08) * 4.0))) * (1 + 0.08 * np.sin(40 * x))
    ax.plot(x, y, color="black", lw=1.0)
    ax.axhline(0.62, xmin=0.06, xmax=0.94, color=GREY, lw=0.9, ls="--")
    xc = x[np.argmax(y >= 0.62)]
    ax.plot([xc], [0.62], "o", color="black", ms=5)
    ax.text(0.9, 0.65, "$W$", fontsize=8, ha="right")
    ax.text(xc, 0.7, "click", fontsize=8.5, ha="center")
    ax.text(
        0.5,
        0.1,
        "the record's motion squared in the cells, against the count",
        fontsize=8.8,
        ha="center",
    )
    ax.set_title(
        "the click: the form crosses the rung,\nthe only thing that leaves the board",
        fontsize=8.2,
        color="black",
    )
    fig.subplots_adjust(left=0.01, right=0.99, top=0.82, bottom=0.04, wspace=0.05)
    save(fig, output / "groups_to_click.pdf")


if __name__ == "__main__":
    draw(Path(__file__).resolve().parent / "figures")
