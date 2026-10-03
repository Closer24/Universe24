"""The click at a bound body, drawn from the definitions, by no run of the engine.

Two schematic panels. (a) Space and time at one Node of a bound body: the
emitter's record runs forward from its root, every path at once, the future; at
the body's Node the arriving quantum meets the body's own transition and the
instrument draws at the window's close, the click, the present; from the click
the same line is read backward, Rule3 at -1, the past, a reading and never a
write; forward the body's change spreads by Rule3 at one Link per interval, the
front, and inside the click's light cone the record that gave is erased, its
levels beyond the front an empty wave with count 0. (b) The one Node before the
window, at its close and after the write: the record's levels, the body's parts
g and e, the six Ports, the draw and the click line to the detector's file.
Nothing here is a number of a run.

    python paper/general_formula/click_body.py --output paper/general_formula/figures

Needs matplotlib.
"""

from __future__ import annotations

import argparse
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
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
INK, MID, LIGHT, PALE = "#000000", "#808080", "#c8c8c8", "#ececec"
BOX = {"boxstyle": "square,pad=0.1", "facecolor": "white", "edgecolor": "none"}


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def frame(ax: Axes, xlim: tuple[float, float], ylim: tuple[float, float]) -> None:
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def arrow(
    ax: Axes,
    a: tuple[float, float],
    b: tuple[float, float],
    color: str = INK,
    lw: float = 0.8,
) -> None:
    """A straight arrow from a to b, its head sized for the 8 pt lettering."""
    ax.add_patch(
        FancyArrowPatch(
            a, b, arrowstyle="-|>,head_length=3,head_width=1.6", color=color, lw=lw, shrinkA=0, shrinkB=0
        )
    )


def spacetime(ax: Axes) -> None:
    """(a) The future from the root, the click at the body's Node, the past read back, the front."""
    ax.set_xlim(-0.5, 10.6)
    ax.set_ylim(-1.1, 10.8)
    ax.axis("off")
    x0, xb, tc, top = 0.3, 7.0, 6.5, 10.2  # the root, the body's Node, the click's interval, the top
    pace = (xb - x0) / tc  # the record's pace, schematic: its edge reaches the body at the click
    bound = 1.35  # the front's pace, the causal bound, faster than the record
    # axes
    arrow(ax, (-0.2, -0.2), (10.4, -0.2), lw=0.6)
    arrow(ax, (-0.2, -0.2), (-0.2, 10.5), lw=0.6)
    ax.text(10.4, -0.4, "x, Links", ha="right", va="top")
    ax.text(0.05, 10.45, "t, intervals", ha="left", va="top")
    # the future: the record's fan from the root, every path at once (the emitter backed by a face)
    ax.add_patch(
        Polygon(
            [(x0, 0.0), (x0 + pace * top, top), (x0, top)], closed=True, facecolor=PALE, edgecolor="none"
        )
    )
    for k in range(1, 10):
        t = k * 1.1
        if t < top:
            ax.plot([x0, x0 + pace * t], [t, t], color=LIGHT, lw=0.5)
    ax.plot([x0, x0 + pace * top], [0, top], color=MID, lw=0.7)
    # the front from the click, one Link per interval, erasing the record that gave inside the light cone
    ax.add_patch(
        Polygon(
            [(xb, tc), (xb + bound * (top - tc), top), (xb - bound * (top - tc), top)],
            closed=True,
            facecolor="white",
            edgecolor="none",
            zorder=2.5,
        )
    )
    ax.plot(
        [xb - bound * (top - tc), xb, xb + bound * (top - tc)],
        [top, tc, top],
        color=INK,
        lw=0.9,
        zorder=3,
    )
    for k in range(1, 4):
        t = tc + k * 0.95
        ax.plot(
            [xb - bound * (t - tc), xb + bound * (t - tc)],
            [t, t],
            color=LIGHT,
            lw=0.5,
            ls=(0, (1, 1.5)),
            zorder=3,
        )
    # the past: dashed readings from the click back to the root, through the record's paths
    for xm, tm in ((2.0, 3.2), (3.6, 2.4), (4.8, 4.1)):
        ax.plot([xb, xm, x0], [tc, tm, 0], color=INK, lw=0.6, ls=(0, (2.5, 2)))
    ax.plot([xb, x0], [tc, 0], color=INK, lw=0.8, ls=(0, (4, 2)))
    ax.plot(x0, 0, "o", ms=3.2, color=INK)
    ax.text(x0 + 0.15, -0.5, "the root: the giver's record laid", ha="left", va="top")
    # the body's world line, one Node: its part g before the click, e after it
    ax.plot([xb, xb], [0, tc], color=INK, lw=0.9)
    ax.plot([xb, xb], [tc, top], color=INK, lw=2.4, zorder=3)
    ax.plot([xb, xb + 0.95 * (top - 8.7)], [8.7, top], color=MID, lw=0.7, ls=(0, (1, 1.2)), zorder=3)
    # the window on the body's line
    ax.plot([xb - 0.15, xb - 0.15], [tc - 1.7, tc], color=INK, lw=0.6)
    ax.plot([xb - 0.25, xb - 0.05], [tc - 1.7, tc - 1.7], color=INK, lw=0.6)
    # the click
    ax.plot(xb, tc, "o", ms=6, color="white", markeredgecolor=INK, markeredgewidth=1.0, zorder=4)
    ax.plot(xb, tc, "o", ms=2.4, color=INK, zorder=4)
    # the labels
    ax.text(
        1.3,
        1.35,
        "the future: the record\nrun forward from the root,\nevery path at once",
        ha="left",
        va="center",
        bbox=BOX,
    )
    ax.text(
        3.0,
        4.9,
        "the past: read back from\nthe click, Rule3 at $-1$,\na reading and no write",
        ha="center",
        va="center",
        bbox=BOX,
    )
    ax.text(
        0.5,
        8.9,
        "beyond the front:\nthe empty wave,\ncount 0, no credit",
        ha="left",
        va="center",
        bbox=BOX,
    )
    ax.text(
        4.7,
        9.3,
        "the front, one Link per\ninterval: the record that\ngave erased inside the\nclick's light cone",
        ha="center",
        va="center",
        bbox=BOX,
    )
    ax.text(xb - 0.35, tc - 0.85, "the\nwindow", ha="right", va="center", bbox=BOX)
    ax.text(
        xb + 0.3,
        tc - 0.1,
        "the click, the now:\nthe two quanta meet\nat the one Node,\nthe instrument draws",
        ha="left",
        va="top",
        bbox=BOX,
    )
    ax.text(
        xb + 0.3,
        1.6,
        "the bound body at its\none Node, its part g laid",
        ha="left",
        va="center",
        bbox=BOX,
    )
    ax.text(
        xb + 0.3,
        8.0,
        "the body changed: e laid,\nthe quantum held\nuntil its giving (dotted)",
        ha="left",
        va="center",
        bbox=BOX,
    )
    ax.text(-0.5, 10.8, "(a)", ha="left", va="top", fontweight="bold")


def node(
    ax: Axes,
    cx: float,
    cy: float,
    levels: tuple[int, int, int],
    title: str,
    note: str,
    hole: bool = False,
) -> None:
    """One Node of the GameBoard: its square, six Ports, and three bars for the levels."""
    s = 1.8
    ax.add_patch(Rectangle((cx - s / 2, cy - s / 2), s, s, facecolor="white", edgecolor=INK, lw=0.8))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # four Ports in the plane
        ax.plot(
            [cx + dx * s / 2, cx + dx * (s / 2 + 0.35)],
            [cy + dy * s / 2, cy + dy * (s / 2 + 0.35)],
            color=INK,
            lw=0.8,
        )
    for dx, mark in ((-1, "."), (1, "x")):  # two Ports out of the plane
        px, py = cx + dx * (s / 2 - 0.24), cy + s / 2 - 0.24
        ax.plot(px, py, "o", ms=3.4, color="white", markeredgecolor=INK, markeredgewidth=0.6)
        ax.plot(px, py, mark, ms=2.2 if mark == "x" else 2.0, color=INK, markeredgewidth=0.6)
    base = cy - s / 2 + 0.28
    w = 0.32
    xs = (cx - 0.55, cx, cx + 0.55)
    for x, h, f in zip(xs, levels, (LIGHT, INK, "white"), strict=True):
        if h > 0:
            ax.add_patch(Rectangle((x - w / 2, base), w, 0.3 * h, facecolor=f, edgecolor=INK, lw=0.6))
        ax.plot([x - w / 2 - 0.05, x + w / 2 + 0.05], [base, base], color=INK, lw=0.6)
    if hole:
        ax.text(xs[0], base + 0.45, "0", ha="center", va="center", fontsize=7)
    for x, lab in zip(xs, ("rec.", "g", "e"), strict=True):
        ax.text(x, cy - s / 2 - 0.45, lab, ha="center", va="top", fontsize=7)
    ax.text(cx, cy + s / 2 + 0.45, title, ha="center", va="bottom", fontweight="bold")
    ax.text(cx, cy - s / 2 - 0.95, note, ha="center", va="top", fontsize=7, linespacing=1.05)


def the_node(ax: Axes) -> None:
    """(b) The one Node before the window's close, at the draw and after the write; the file."""
    ax.set_xlim(-0.5, 13.3)
    ax.set_ylim(-3.9, 2.4)
    ax.set_aspect("equal")
    ax.axis("off")
    y = 0.4
    node(
        ax,
        1.6,
        y,
        (3, 2, 0),
        "before",
        "the record's levels\narrive through the\nPorts; the body holds\nits part g, e empty",
    )
    node(
        ax,
        5.1,
        y,
        (3, 2, 0),
        "the window closes",
        "the share, now$^2$ minus\nnext times before, at\nresonance; the draw with\nthe seed: realised, and\nat which one Node",
    )
    node(
        ax,
        8.6,
        y,
        (0, 1, 1),
        "after: one write",
        "the hole: the record's\nlevels and remainder\nto 0, count down one;\ng down one, e laid up one;\nRule3 steps it on",
        hole=True,
    )
    for x in (2.9, 6.4, 9.9):
        arrow(ax, (x, y), (x + 0.7, y), lw=0.7)
    ax.add_patch(Rectangle((10.95, y - 0.9), 2.15, 1.8, facecolor=PALE, edgecolor=INK, lw=0.6))
    ax.text(
        12.02,
        y,
        "the click line:\nregion, interval,\nfamily, count",
        ha="center",
        va="center",
        fontsize=7,
    )
    ax.text(12.02, y + 0.9 + 0.45, "the file", ha="center", va="bottom", fontweight="bold")
    ax.text(
        12.02,
        y - 0.9 - 0.45,
        "the report,\nthe only\nmeasurement",
        ha="center",
        va="top",
        fontsize=7,
        linespacing=1.05,
    )
    ax.text(-0.45, 2.35, "(b)", ha="left", va="top", fontweight="bold")


def click_body(output: Path) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(4.68, 6.2), gridspec_kw={"height_ratios": (11.9, 6.3)})
    spacetime(axes[0])
    the_node(axes[1])
    fig.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005, hspace=0.02)
    output.mkdir(parents=True, exist_ok=True)
    save(fig, output / "click_body.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    args = parser.parse_args()
    click_body(args.output)


if __name__ == "__main__":
    main()
