"""The meeting's figure, drawn from the definitions, by no run of the engine.

Three schematic panels of docs/HIGHLIGHTS.md, the click is the meeting of the
future with the past: the two slits (the emitter's events spread forward through
both gaps, every possibility at once; the backward reading from a realised click
passes both gaps; the share at the screen alternates), one gap closed by an
opaque detector (its events leave the board, the backward reading meets one gap,
one gap's envelope), and a pair as two trees with one root (the backward reading
from one side's click passes the root and continues forward to the partner).
Nothing here is a number of a run.

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
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

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


def board(ax: Axes, closed_gap: tuple[float, float] | None) -> None:
    """The board: the emitter, the wall with its gaps and the screen's regions."""
    frame(ax)
    segments = [0.0, *[edge for gap in GAPS for edge in gap], TOP]
    for low, high in zip(segments[0::2], segments[1::2], strict=True):
        ax.add_patch(Rectangle((WALL - 0.12, low), 0.24, high - low, color=INK))
    if closed_gap is not None:
        height = closed_gap[1] - closed_gap[0]
        ax.add_patch(Rectangle((WALL - 0.12, closed_gap[0]), 0.24, height, color=INK, hatch="////"))
    for k in range(13):
        y = k * TOP / 12
        ax.plot([SCREEN, SCREEN + 0.25], [y, y], color=INK, linewidth=0.6)
    ax.plot([SCREEN, SCREEN], [0, TOP], color=INK, linewidth=1.2)
    ax.plot([0.5], [TOP / 2], "o", color=INK, markersize=4)
    ax.text(0.9, TOP / 2 - 0.5, "the emitter", ha="center", va="top", color=INK)
    ax.text(WALL, -0.25, "the wall", ha="center", va="top", color=INK)
    ax.text(SCREEN + 0.1, -0.25, "the screen", ha="center", va="top", color=INK)


def share_curve(ax: Axes, two_gaps: bool) -> None:
    """The share along the screen: fringes from two gaps, one envelope from one."""
    ys = [k / 60 for k in range(0, 301)]
    values = []
    for y in ys:
        envelope = math.exp(-(((y - TOP / 2) / 1.3) ** 2))
        values.append(envelope * (math.cos(2.4 * (y - TOP / 2)) ** 2 if two_gaps else 1.0))
    ax.plot([SCREEN + 0.5 + 1.6 * v for v in values], ys, color=INK, linewidth=0.9)
    ax.text(SCREEN + 1.5, TOP + 0.15, "the share\nper region", ha="center", va="bottom", color=INK)


def two_slits(ax: Axes) -> None:
    """Both gaps open: the forward events through both, the backward reading through both."""
    board(ax, None)
    fan(ax, (0.5, TOP / 2), WALL, 2.2, PALE)
    for low, high in GAPS:
        fan(ax, (WALL, (low + high) / 2), SCREEN, 2.4, LIGHT)
    click = (SCREEN, TOP / 2)
    for low, high in GAPS:
        centre = (low + high) / 2
        ax.plot([click[0], WALL, 0.5], [click[1], centre, TOP / 2], "--", color=INK, linewidth=0.9)
    ax.plot([click[0]], [click[1]], "s", color=INK, markersize=5)
    share_curve(ax, True)
    ax.text(0.0, TOP + 0.2, "the future: the emitter's\nevents, every possibility", color=MID)
    ax.text(3.4, -0.1, "the past: the reading from\nthe click, Rule3 at $-1$", color=INK, bbox=BOX)
    ax.text(SCREEN - 0.25, TOP / 2 + 0.4, "the click:\nthe meeting", ha="right", color=INK)
    ax.set_title("(a) two gaps: the share alternates", loc="left", pad=14)


def closed(ax: Axes) -> None:
    """One gap closed by an opaque detector: the backward reading meets one gap."""
    board(ax, GAPS[0])
    fan(ax, (0.5, TOP / 2), WALL, 2.2, PALE)
    low, high = GAPS[1]
    fan(ax, (WALL, (low + high) / 2), SCREEN, 2.4, LIGHT)
    click = (SCREEN, 2.9)
    ax.plot([click[0], WALL, 0.5], [click[1], (low + high) / 2, TOP / 2], "--", color=INK, linewidth=0.9)
    ax.plot([click[0]], [click[1]], "s", color=INK, markersize=5)
    share_curve(ax, False)
    ax.text(
        WALL + 0.3,
        -0.1,
        "an opaque detector in the gap:\nwhat enters it leaves the board",
        color=INK,
        bbox=BOX,
    )
    ax.set_title("(b) one gap closed: one gap's envelope", loc="left", pad=14)


def pair(ax: Axes) -> None:
    """A pair: two trees with one root; the backward reading from A passes the root to B."""
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
    ax.text(root[0], root[1] - 0.5, "the root: one event,\ntwo trees", ha="center", va="top", color=INK)
    click_a = (0.8, 3.3)
    ax.plot([click_a[0]], [click_a[1]], "s", color=INK, markersize=5)
    ax.plot([click_a[0], root[0]], [click_a[1], root[1]], "--", color=INK, linewidth=0.9)
    ax.plot([root[0], 9.8], [root[1], 1.9], ":", color=INK, linewidth=1.1)
    ax.plot([9.8], [1.9], "s", color=INK, markerfacecolor="white", markersize=5)
    ax.text(1.3, TOP + 0.2, "the past read back from A's click", color=INK)
    ax.text(2.2, -0.1, "continues forward on B's tree:\nthe root joins, nothing is signalled", color=INK)
    ax.set_title("(c) a pair: the meeting through the root", loc="left", pad=14)


def meeting(output: Path) -> None:
    """The three panels stacked in one figure, at the final width."""
    fig, axes = plt.subplots(3, 1, figsize=(4.69, 6.6))
    two_slits(axes[0])
    closed(axes[1])
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
