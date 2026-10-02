"""The click's figure, drawn from the definitions, by no run of the engine.

Three schematic panels of the click as the paper states it: the two slits (the
emitter's events spread forward through both gaps, every possibility at once;
the backward reading from a realised click passes both gaps; the detector writes
once, at the one Node from which the quantum reached it, and the change spreads
by Rule3), the detector as a body of the GameBoard with two sides (the front
where the incoming quantum meets its own transition, the other side bound to the
apparatus, the observer's bodies and the record's root), and a pair as two trees
with one root (the one draw of the credit through the root; each side's write at
its own Node). Nothing here is a number of a run.

    python paper/general_formula/meeting.py --output paper/general_formula/figures

Needs matplotlib.
"""

from __future__ import annotations

import argparse
import math
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
)  # the journal's lettering: 8 pt at the final size, the figure drawn 1:1, fonts embedded
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Arc, FancyArrowPatch, Polygon, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
INK, MID, LIGHT, PALE = "#000000", "#808080", "#c8c8c8", "#ececec"
WALL, SCREEN, TOP = 3.0, 8.0, 5.0
BOX = {"boxstyle": "square,pad=0.1", "facecolor": "white", "edgecolor": "none"}
GAPS = ((1.6, 2.1), (2.9, 3.4))


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def fan(ax: Axes, apex: tuple[float, float], x_end: float, half: float, colour: str) -> None:
    """A fan of events from an apex to a line, the schematic of a record spreading."""
    points = [apex, (x_end, apex[1] - half), (x_end, apex[1] + half)]
    ax.add_patch(Polygon(points, closed=True, color=colour, linewidth=0))


def frame(ax: Axes) -> None:
    """The panel's frame, the same for the three."""
    ax.set_xlim(-0.3, 11.0)
    ax.set_ylim(-0.9, TOP + 0.9)
    ax.axis("off")


def spreading(ax: Axes, node: tuple[float, float], towards: float, radii: tuple[float, ...]) -> None:
    """The change written at one Node, carried outward by Rule3: arcs one Link per interval."""
    for radius in radii:
        ax.add_patch(
            Arc(
                node,
                2 * radius,
                2 * radius,
                theta1=towards - 70,
                theta2=towards + 70,
                color=INK,
                linewidth=0.7,
            )
        )


def board(ax: Axes) -> None:
    """The board: the emitter, the wall with its gaps and the screen's regions."""
    frame(ax)
    segments = [0.0, *[edge for gap in GAPS for edge in gap], TOP]
    for low, high in zip(segments[0::2], segments[1::2], strict=True):
        ax.add_patch(Rectangle((WALL - 0.12, low), 0.24, high - low, color=INK))
    for k in range(13):
        y = k * TOP / 12
        ax.plot([SCREEN, SCREEN + 0.25], [y, y], color=INK, linewidth=0.6)
    ax.plot([SCREEN, SCREEN], [0, TOP], color=INK, linewidth=1.2)
    ax.plot([0.5], [TOP / 2], "o", color=INK, markersize=4)
    ax.text(0.9, TOP / 2 - 0.5, "the emitter", ha="center", va="top", color=INK)
    ax.text(WALL, -0.25, "the wall", ha="center", va="top", color=INK)
    ax.text(SCREEN + 0.1, -0.25, "the screen", ha="center", va="top", color=INK)


def share_curve(ax: Axes) -> None:
    """The share along the screen: the fringes from two gaps."""
    ys = [k / 60 for k in range(0, 301)]
    values = [math.exp(-(((y - TOP / 2) / 1.3) ** 2)) * math.cos(2.4 * (y - TOP / 2)) ** 2 for y in ys]
    ax.plot([SCREEN + 0.5 + 1.6 * v for v in values], ys, color=INK, linewidth=0.9)
    ax.text(SCREEN + 1.5, TOP + 0.15, "the share\nper region", ha="center", va="bottom", color=INK)


def two_slits(ax: Axes) -> None:
    """Both gaps open: the forward events, the backward reading, the write at one Node."""
    board(ax)
    fan(ax, (0.5, TOP / 2), WALL, 2.2, PALE)
    for low, high in GAPS:
        fan(ax, (WALL, (low + high) / 2), SCREEN, 2.4, LIGHT)
    click = (SCREEN, TOP / 2)
    for low, high in GAPS:
        centre = (low + high) / 2
        ax.plot([click[0], WALL, 0.5], [click[1], centre, TOP / 2], "--", color=INK, linewidth=0.9)
    ax.add_patch(
        Rectangle(
            (SCREEN - 0.05, TOP / 2 - 0.45), 0.3, 0.9, facecolor="white", edgecolor=INK, linewidth=0.8
        )
    )
    ax.plot([click[0] - 0.05], [click[1]], "s", color=INK, markersize=5)
    spreading(ax, (SCREEN - 0.05, TOP / 2), 180.0, (0.45, 0.8, 1.15))
    share_curve(ax)
    ax.text(0.0, TOP + 0.2, "the future: the emitter's\nevents, every possibility", color=MID)
    ax.text(3.4, -0.1, "the past: the reading from\nthe click, Rule3 at $-1$", color=INK, bbox=BOX)
    ax.text(
        SCREEN - 1.4,
        TOP / 2 + 1.45,
        "the write at the one Node\nthe quantum reached the\ndetector from; the change\nspreads by Rule3",
        ha="right",
        va="bottom",
        color=INK,
        bbox=BOX,
    )
    ax.set_title("(a) two gaps: the meeting, the draw and the one write", loc="left", pad=14)


def detector(ax: Axes) -> None:
    """The detector as a body of the GameBoard with two sides."""
    frame(ax)
    left, right, low, high = 5.2, 7.4, 1.3, 3.9
    apex = (0.5, 2.6)
    ax.add_patch(
        Rectangle((left, low), right - left, high - low, facecolor=PALE, edgecolor=INK, linewidth=0.8)
    )
    ax.plot([left, left], [low, high], color=INK, linewidth=1.6)
    fan(ax, apex, left, 1.2, LIGHT)
    ax.plot([apex[0]], [apex[1]], "o", color=INK, markersize=4)
    ax.text(0.0, TOP + 0.2, "the future: the incoming record's\nquantum, run forward", color=MID)
    node = (left, 2.6)
    ax.plot([node[0]], [node[1]], "s", color=INK, markersize=5)
    spreading(ax, node, 180.0, (0.4, 0.75, 1.1))
    for y in (1.9, 3.3):
        ax.plot([left + 0.4, left + 1.2], [y, y], color=INK, linewidth=1.0)
    ax.add_patch(
        FancyArrowPatch(
            (left + 0.8, 1.95),
            (left + 0.8, 3.25),
            arrowstyle="-|>",
            mutation_scale=8,
            color=INK,
            linewidth=0.8,
        )
    )
    ax.text(
        left + 1.35,
        2.6,
        "its own\ntransition:\nthe past,\nread back",
        va="center",
        color=INK,
        fontsize=7,
    )
    ax.text(
        (left + right) / 2,
        high + 0.15,
        "the detector: a body\nof the GameBoard",
        ha="center",
        va="bottom",
        color=INK,
    )
    ax.text(
        0.0,
        4.55,
        "the front: two quanta meet;\nthe draw with the declared seed;\nthe write at this one Node",
        va="top",
        color=INK,
        bbox=BOX,
    )
    for y in (1.9, 2.6, 3.3):
        ax.plot([right, right + 0.8], [y, y], color=INK, linewidth=0.7)
        ax.add_patch(
            Rectangle((right + 0.8, y - 0.2), 0.45, 0.4, facecolor="white", edgecolor=INK, linewidth=0.7)
        )
    ax.text(
        right + 1.45,
        2.6,
        "the other side:\nthe apparatus,\nthe observer's\nbodies",
        va="center",
        color=INK,
    )
    ax.plot(
        [right, right + 0.5, 0.9, apex[0]],
        [low, 0.35, 0.35, apex[1] - 0.15],
        ":",
        color=INK,
        linewidth=1.0,
    )
    ax.text(
        4.0,
        0.1,
        "and, through the record it took, the record's root, the common past",
        ha="center",
        va="top",
        color=INK,
        bbox=BOX,
    )
    ax.set_title("(b) the detector: two sides, both on the GameBoard", loc="left", pad=14)


def pair(ax: Axes) -> None:
    """A pair: two trees with one root; the one draw through the root; each side's write."""
    frame(ax)
    root = (5.3, TOP / 2)
    for x_screen, label in ((0.8, "A"), (9.8, "B")):
        ax.plot([x_screen, x_screen], [0.6, TOP - 0.6], color=INK, linewidth=1.2)
        for k in range(9):
            y = 0.6 + k * (TOP - 1.2) / 8
            step = -0.25 if x_screen < root[0] else 0.25
            ax.plot([x_screen, x_screen + step], [y, y], color=INK, linewidth=0.6)
        ax.text(x_screen, -0.25, f"the side {label}", ha="center", va="top", color=INK)
    fan(ax, root, 0.8, 1.9, LIGHT)
    fan(ax, root, 9.8, 1.9, LIGHT)
    ax.plot([root[0]], [root[1]], "o", color=INK, markersize=4)
    ax.text(
        root[0],
        root[1] - 0.5,
        "the root: one event, two trees;\nthe credit's one draw through it",
        ha="center",
        va="top",
        color=INK,
    )
    click_a = (0.8, 3.3)
    ax.plot([click_a[0]], [click_a[1]], "s", color=INK, markersize=5)
    spreading(ax, click_a, 0.0, (0.35, 0.65))
    ax.plot([click_a[0], root[0]], [click_a[1], root[1]], "--", color=INK, linewidth=0.9)
    ax.plot([root[0], 9.8], [root[1], 1.9], ":", color=INK, linewidth=1.1)
    ax.plot([9.8], [1.9], "s", color=INK, markersize=5)
    spreading(ax, (9.8, 1.9), 180.0, (0.35, 0.65))
    ax.text(1.3, TOP + 0.2, "the past read back from A's click, through the root to B", color=INK)
    ax.text(
        1.5,
        -0.1,
        "each side writes at its own Node, the change spreading by Rule3;\nthe correlation sits in the one draw, nothing is signalled",
        color=INK,
        bbox=BOX,
    )
    ax.set_title("(c) a pair: the meeting through the root", loc="left", pad=14)


def meeting(output: Path) -> None:
    """The three panels stacked in one figure, at the final width."""
    fig, axes = plt.subplots(3, 1, figsize=(4.68, 6.6))
    two_slits(axes[0])
    detector(axes[1])
    pair(axes[2])
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.01, hspace=0.38)
    save(fig, output / "meeting.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    arguments = parser.parse_args()
    arguments.output.mkdir(parents=True, exist_ok=True)
    meeting(arguments.output)


if __name__ == "__main__":
    main()
