"""The click at a NodeReader, drawn from the definitions, by no run of the engine, in black and grey.

Four parts at the page's width. (a) Space and time: the arriving record runs
forward from its root, every path at once, the future (solid lines); it meets
the NodeReader's region, two adjacent Nodes, at the region's boundary; the
NodeReader draws at the window's close, the click, the now; from the click the
same line is read backward, Rule3 at -1, the past (dashed lines), a reading and
never a write; the one write is at the Node the draw picked, the drawn Node,
and its change spreads forward by Rule3 at one Link per interval, the front,
one shell per interval at the causal bound; inside the click's light cone the
record that gave is erased, its levels beyond the front an empty wave with
count 0. (b) The NodeReader's region before the window's close and after the
one write: two Nodes side by side, the NodeReader's own record laid over both
with its parts g and e, the write at the drawn Node. (c) The hole at the drawn
Node by the faces' booking identity, each face writing one level, no factor.
(d) The ledger in whole numbers, the click line, the NodeReader's report, and
the declaration in the file. Nothing here is a number of a run.

    python paper/general_formula/click_body.py --output paper/general_formula/figures

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
        "font.sans-serif": ["Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "mathtext.fontset": "custom",
        "mathtext.rm": "Liberation Sans",
        "mathtext.it": "Liberation Sans:italic",
        "mathtext.bf": "Liberation Sans:bold",
    }
)  # the journal's lettering: 8 pt at the final size, one typeface for the words and the symbols, the figure drawn 1:1 at the page's width of 174 mm at most, fonts embedded
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import (  # noqa: E402
    Circle,
    FancyArrowPatch,
    FancyBboxPatch,
    Polygon,
    Rectangle,
)

HERE = Path(__file__).resolve().parent
INK, GREY, LIGHT, PALE = "#000000", "#7a7a7a", "#c8c8c8", "#efefef"
BLUE, BLUE_MID, BLUE_PALE = (
    "#000000",
    "#b4b4b4",
    "#e6e6e6",
)  # the future, run forward: solid lines, grey fill
ORANGE = "#000000"  # the past, read backward: dashed lines
BOX = {
    "boxstyle": "round,pad=0.15,rounding_size=0.2",
    "facecolor": "white",
    "edgecolor": "none",
    "alpha": 1.0,
}
PNG_DPI = 200  # the PNG beside the PDF, for the reviewers' reading on a screen


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes, the EPS a journal asks for and the PNG for reading, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))
    fig.savefig(path.with_suffix(".png"), dpi=PNG_DPI)


def arrow(
    ax: Axes,
    a: tuple[float, float],
    b: tuple[float, float],
    color: str = INK,
    lw: float = 0.9,
    style: str = "-|>,head_length=3.2,head_width=1.8",
    ls: str = "-",
) -> None:
    """A straight arrow from a to b, its head sized for the 8 pt lettering."""
    ax.add_patch(
        FancyArrowPatch(
            a,
            b,
            arrowstyle=style,
            color=color,
            lw=lw,
            shrinkA=0,
            shrinkB=0,
            linestyle=ls,
            zorder=5,
        )
    )


def number(ax: Axes, x: float, y: float, n: int, color: str = INK) -> None:
    """A numbered marker keyed to the caption."""
    ax.add_patch(Circle((x, y), 0.27, facecolor=color, edgecolor="none", zorder=8))
    ax.text(
        x,
        y,
        str(n),
        ha="center",
        va="center",
        color="white",
        fontsize=7,
        fontweight="bold",
        zorder=9,
    )


def spacetime(ax: Axes) -> None:
    """(a) The future from the root, the meeting at the region, the click, the write at the drawn Node, the front."""
    ax.set_xlim(-0.4, 11.6)
    ax.set_ylim(-1.3, 15.7)
    ax.set_aspect("equal")
    ax.axis("off")
    x0, xb, xr, tm, tc, top = (
        1.0,
        5.9,
        6.6,
        6.0,
        7.6,
        14.9,
    )  # the root, the region's boundary Node, the drawn Node, the meeting, the click, the top
    pace = (
        xb - x0
    ) / tm  # the record's pace, schematic: its edge reaches the region's boundary at the meeting
    bound = 1.45  # the front's pace, the causal bound, faster than the record
    # the small axes of space and time
    arrow(ax, (-0.1, -0.9), (2.2, -0.9), lw=0.7)
    arrow(ax, (-0.1, -0.9), (-0.1, 1.4), lw=0.7)
    ax.text(2.3, -0.9, "space", ha="left", va="center", color=GREY)
    ax.text(-0.1, 1.5, "time", ha="center", va="bottom", color=GREY)
    # the future: the record's fan from the root, every path at once; wavefronts interval by interval
    fan = Polygon(
        [(x0, 0.0), (x0 + pace * top, top), (x0 - 0.9, top)],
        closed=True,
        facecolor=BLUE_PALE,
        edgecolor="none",
        zorder=1,
    )
    ax.add_patch(fan)
    for k in range(1, 18):
        r = k * 0.9
        th = [math.radians(a) for a in range(-100, 101, 4)]
        xs = [x0 + r * math.sin(t) * 0.78 for t in th]
        ys = [r * math.cos(t) * 0.78 + 0.0 for t in th]
        pts = [(x, y) for x, y in zip(xs, ys, strict=True) if y >= 0 and x >= x0 - 0.9 and y <= top]
        if len(pts) > 2:
            (line,) = ax.plot(
                [p[0] for p in pts],
                [p[1] for p in pts],
                color=BLUE_MID,
                lw=0.5,
                zorder=2,
            )
            line.set_clip_path(fan)
    t_erased = (xr - x0 - bound * tc) / (pace - bound)  # where the front overtakes the record's edge
    ax.plot([x0, x0 + pace * t_erased], [0, t_erased], color=BLUE, lw=0.9, zorder=3)
    arrow(ax, (x0 + pace * 2.0, 2.0), (x0 + pace * 3.4, 3.4), color=BLUE, lw=0.9)
    # the NodeReader's region: two adjacent Nodes, a strip of two world lines
    ax.add_patch(
        Rectangle(
            (xb, -0.3),
            xr - xb,
            top + 0.3,
            facecolor=PALE,
            edgecolor="none",
            zorder=2.5,
        )
    )
    # the past: the reading back from the click to the root, dashed, through several paths
    for xm, tmid in ((x0 + 0.9, 3.0), (x0 + 2.2, 1.3), (x0 + 3.5, 4.0)):
        ax.plot([xr, xm, x0], [tc, tmid, 0], color=ORANGE, lw=0.8, ls=(0, (3, 2)), zorder=4)
    xm, tmid = x0 + 2.2, 1.3
    arrow(
        ax,
        (xr - 0.30 * (xr - xm), tc - 0.30 * (tc - tmid)),
        (xr - 0.42 * (xr - xm), tc - 0.42 * (tc - tmid)),
        color=ORANGE,
        lw=1.0,
    )
    # the front from the click: the new future, one shell per interval; the record that gave erased inside
    front = Polygon(
        [(xr, tc), (xr + bound * (top - tc), top), (xr - bound * (top - tc), top)],
        closed=True,
        facecolor="white",
        edgecolor="none",
        zorder=3,
    )
    ax.add_patch(front)
    ax.plot(
        [xr - bound * (top - tc), xr, xr + bound * (top - tc)],
        [top, tc, top],
        color=BLUE,
        lw=1.1,
        zorder=5,
    )
    for k in range(1, 8):
        t = tc + k * 0.85
        ax.plot(
            [xr - bound * (t - tc), xr + bound * (t - tc)],
            [t, t],
            color=BLUE_MID,
            lw=0.5,
            zorder=4,
        )
    # the world lines: the giver's root, the region's two Nodes, the drawn Node written at the click
    ax.plot([x0, x0], [-0.3, top], color=GREY, lw=0.8, zorder=4)
    ax.plot([xb, xb], [-0.3, top], color=INK, lw=0.8, zorder=6)
    ax.plot([xr, xr], [-0.3, tc], color=INK, lw=0.8, zorder=6)
    ax.plot([xr, xr], [tc, top], color=INK, lw=2.6, zorder=6)
    ax.plot(
        [xr, xr + 0.95 * 1.6],
        [top - 1.6, top],
        color=BLUE,
        lw=0.8,
        ls=(0, (1, 1.3)),
        zorder=6,
    )
    # the root, the meeting, the window, the click
    ax.plot(x0, 0, "o", ms=4.5, color=INK, zorder=7)
    ax.plot(xb, tm, "o", ms=4.0, color="white", markeredgecolor=INK, markeredgewidth=0.9, zorder=7)
    ax.plot([xr + 0.18, xr + 0.18], [tc - 1.5, tc], color=INK, lw=0.7, zorder=6)
    ax.plot([xr + 0.08, xr + 0.28], [tc - 1.5, tc - 1.5], color=INK, lw=0.7, zorder=6)
    ax.add_patch(Circle((xr, tc), 0.34, facecolor="white", edgecolor=INK, lw=1.2, zorder=7))
    ax.add_patch(Circle((xr, tc), 0.12, facecolor=INK, edgecolor="none", zorder=8))
    # the words, few, keyed by number to the caption
    ax.text(
        x0 + 1.3,
        0.75,
        "future",
        color=BLUE,
        fontweight="bold",
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(
        x0 + 1.55,
        4.55,
        "past",
        color=ORANGE,
        fontweight="bold",
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(
        xr + 0.55,
        tc + 0.05,
        "click: the now",
        ha="left",
        va="bottom",
        fontweight="bold",
        zorder=9,
        bbox=BOX,
    )
    ax.text(xr + 0.55, tc - 0.75, "window", ha="left", va="center", zorder=9, bbox=BOX)
    ax.text(
        5.15,
        6.75,
        "meeting at the\nregion's boundary",
        ha="right",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(
        2.75,
        11.3,
        "front, one shell\nper interval",
        color=BLUE,
        fontweight="bold",
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(
        x0 - 0.7,
        9.4,
        "empty wave,\ncount 0",
        color=BLUE,
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(
        xr + 0.45,
        9.5,
        "the write at the\ndrawn Node: e",
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(
        xr + 0.45,
        12.5,
        "giving, per window:\none quantum at\n$\\Omega = \\omega_e - \\omega_g$",
        color=BLUE,
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(
        xr + 0.4,
        2.6,
        "the NodeReader's\nregion: two Nodes,\nits record in g",
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(x0 - 0.35, -0.5, "root", ha="right", va="center", zorder=9)
    number(ax, x0 - 0.55, 0.0, 1)
    number(ax, 5.5, 6.75, 2)
    number(ax, xr + 0.85, tc - 1.45, 3)
    number(ax, xr - 0.55, 9.5, 4)
    number(ax, 2.3, 11.3, 5, BLUE)
    ax.text(-0.3, 15.65, "a", ha="left", va="top", fontweight="bold", fontsize=9)


def node_box(ax: Axes, cx: float, cy: float, s: float, lw: float = 0.9) -> None:
    """A Node of the GameBoard: a rounded square with its six Ports, four in the plane, two out of it."""
    ax.add_patch(
        FancyBboxPatch(
            (cx - s / 2, cy - s / 2),
            s,
            s,
            boxstyle="round,pad=0,rounding_size=0.18",
            facecolor="white",
            edgecolor=INK,
            lw=lw,
            zorder=3,
        )
    )
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ax.plot(
            [cx + dx * s / 2, cx + dx * (s / 2 + 0.35)],
            [cy + dy * s / 2, cy + dy * (s / 2 + 0.35)],
            color=INK,
            lw=0.9,
            zorder=2,
        )
    for dx, mark in ((-1, "."), (1, "x")):
        px, py = cx + dx * (s / 2 - 0.26), cy + s / 2 - 0.26
        ax.plot(
            px,
            py,
            "o",
            ms=4.2,
            color="white",
            markeredgecolor=INK,
            markeredgewidth=0.6,
            zorder=4,
        )
        ax.plot(
            px,
            py,
            mark,
            ms=2.6 if mark == "x" else 2.4,
            color=INK,
            markeredgewidth=0.7,
            zorder=5,
        )


def region(ax: Axes, x1: float, cy: float, s: float, upper: bool, drawn: bool) -> tuple[float, float]:
    """The NodeReader's region: two adjacent Nodes with the Link between them, the dotted boundary of the
    declaration, and the NodeReader's own record laid over both, equal levels on both, its parts g and e a
    ladder with the laid part filled. With drawn, the second Node is the drawn Node, written by the click, and the
    record stands in the drawn part at that Node alone.
    Returns the two Nodes' centres."""
    x2 = x1 + s + 0.4
    ax.add_patch(
        FancyBboxPatch(
            (x1 - s / 2 - 0.55, cy - s / 2 - 0.55),
            x2 - x1 + s + 1.1,
            s + 1.1,
            boxstyle="round,pad=0,rounding_size=0.3",
            facecolor="none",
            edgecolor=GREY,
            lw=0.6,
            ls=(0, (2, 2)),
            zorder=1,
        )
    )
    node_box(ax, x1, cy, s)
    node_box(ax, x2, cy, s, lw=1.8 if drawn else 0.9)
    for y, lab, filled in ((cy - 0.4, "g", not upper), (cy + 0.4, "e", upper)):
        ax.plot([x1 - 0.5, x2 + 0.5], [y, y], color=INK, lw=1.0, zorder=4)
        ax.text(x2 + s / 2 + 0.12, y, lab, ha="left", va="center", fontstyle="italic", zorder=5)
        if filled:
            for cx in ((x2,) if drawn else (x1, x2)):
                ax.plot(cx + 0.12, y + 0.16, "o", ms=5.0, color=INK, zorder=6)
    if drawn:
        arrow(ax, (x2 - 0.3, cy - 0.2), (x2 - 0.3, cy + 0.2), color=ORANGE, lw=1.2)
    return x1, x2


def wave(ax: Axes, x1: float, x2: float, y: float, color: str, n: int = 4, amp: float = 0.16) -> None:
    """A short wavy line, the record's quantum on its way."""
    xs = [x1 + (x2 - x1) * i / 60 for i in range(61)]
    ys = [y + amp * math.sin(2 * math.pi * n * (x - x1) / (x2 - x1)) for x in xs]
    ax.plot(xs, ys, color=color, lw=1.1, zorder=5)
    arrow(ax, (x2 - 0.01, y), (x2 + 0.2, y), color=color, lw=1.1)


def the_region(ax: Axes) -> None:
    """(b) The NodeReader's region before the close and after the one write at the drawn Node."""
    s = 1.6
    y = 15.9
    xa, xb = region(ax, 1.7, y, s, upper=False, drawn=False)
    wave(ax, -0.3, xa - s / 2 - 0.5, y, BLUE)
    ax.text(
        xa - s / 2 - 0.05,
        y + s / 2 + 0.75,
        "before the close",
        ha="left",
        va="bottom",
        fontweight="bold",
    )
    ax.text(
        (xa + xb) / 2,
        y - s / 2 - 0.75,
        "the arriving record,\ncount 1, at the\nregion's boundary",
        color=BLUE,
        ha="center",
        va="top",
    )
    # the draw between them
    x_after = 9.0
    xm = (xb + x_after) / 2
    arrow(ax, (xb + s / 2 + 0.75, y), (x_after - s / 2 - 0.75, y), lw=1.0)
    ax.text(xm, y + 0.3, "the draw\nat the\nclose", ha="center", va="bottom")
    # after: one write at the drawn Node; the record's part e; the front leaves through its Ports
    xc, xd = region(ax, x_after, y, s, upper=True, drawn=True)
    ax.text(
        xc - s / 2 - 0.55,
        y + s / 2 + 0.75,
        "after the write",
        ha="left",
        va="bottom",
        fontweight="bold",
    )
    for dx, dy in ((1, 0), (0, 1)):
        a = (xd + dx * (s / 2 + 0.35), y + dy * (s / 2 + 0.35))
        b = (xd + dx * (s / 2 + 0.95), y + dy * (s / 2 + 0.95))
        arrow(ax, a, b, color=BLUE, lw=0.9)
    ax.text(
        xd + 0.25,
        y + s / 2 + 0.95,
        "front",
        color=BLUE,
        ha="left",
        va="center",
        fontweight="bold",
    )
    ax.plot([xd, xd], [y - s / 2 - 0.5, y - s / 2 - 0.9], color=INK, lw=0.8, zorder=6)
    ax.plot(xd, y - s / 2 - 0.5, "^", ms=4.5, color=INK, zorder=7)
    ax.text(
        (xc + xd) / 2 + 0.3,
        y - s / 2 - 1.0,
        "the drawn Node, by the share;\nthe front by Rule3,\none Link per interval",
        ha="center",
        va="top",
    )
    number(ax, xa - s / 2 - 0.55, y + s / 2 + 1.0, 2)
    number(ax, xm, y - 0.65, 3)
    number(ax, xd + s / 2 + 0.75, y - s / 2 - 0.5, 4)
    ax.text(-0.3, 18.85, "b", ha="left", va="top", fontweight="bold", fontsize=9)


def the_hole(ax: Axes) -> None:
    """(c) The hole at the drawn Node by the booking identity: each of the two faces writes one level."""
    y0 = 9.65  # the level axis
    b, v, x1, x2, zero = (
        2.2,
        4.9,
        4.28,
        1.35,
        0.9,
    )  # the past, the present, face 1's root, face 2's level, 0
    depth, w_rec = 1.35, 0.9  # the parabola's depth at the midpoint and the quantum's line, schematic
    ax.text(-0.3, 12.5, "c", ha="left", va="top", fontweight="bold", fontsize=9)
    ax.text(
        0.4,
        12.3,
        "the hole at the drawn Node,\none level per face",
        ha="left",
        va="top",
        fontweight="bold",
    )
    arrow(ax, (0.3, y0), (6.2, y0), lw=0.7)
    ax.text(6.3, y0, "$x$", ha="left", va="center", color=GREY)
    for x, lab in ((zero, "0"), (b, "$b$, past"), (v, "$v$, present")):
        ax.plot([x, x], [y0 - 0.12, y0 + 0.12], color=INK, lw=0.7, zorder=5)
        ax.text(x, y0 + 0.22, lab, ha="center", va="bottom")
    # the identity dQ = w (x - v)(x - b) below the axis between b and v, the line at one quantum, the root
    xs = [b - 0.35 + (v - b + 0.7) * i / 80 for i in range(81)]
    ys = [y0 - depth * 4 * (x - b) * (v - x) / (v - b) ** 2 for x in xs]
    ax.plot(xs, ys, color=GREY, lw=0.8, zorder=4)
    ax.plot([zero + 0.3, v + 0.5], [y0 - w_rec, y0 - w_rec], color=INK, lw=0.6, ls=(0, (3, 2)), zorder=4)
    ax.text(zero + 0.25, y0 - w_rec - 0.1, "$dQ = -W_{\\mathrm{rec}}$", ha="left", va="top")
    ax.plot([x1, x1], [y0 - w_rec, y0], color=INK, lw=0.6, ls=(0, (1, 1.2)), zorder=4)
    ax.plot(x1, y0 - w_rec, "o", ms=3.6, color=INK, zorder=6)
    for x, lab in ((x1, "$x_1$"), (x2, "$x_2$")):
        ax.plot(x, y0, "o", ms=4.2, color="white", markeredgecolor=INK, markeredgewidth=0.9, zorder=6)
        ax.text(x + 0.14, y0 - 0.2, lab, ha="left", va="top")
    # face 1 writes the present level to the root nearest v, face 2 writes the past level, the rest
    arrow(ax, (v - 0.1, y0 + 0.85), (x1 + 0.1, y0 + 0.85), lw=0.9)
    ax.text((v + x1) / 2 + 0.1, y0 + 0.98, "face 1", ha="center", va="bottom", fontweight="bold")
    arrow(ax, (b - 0.1, y0 + 0.85), (x2 + 0.1, y0 + 0.85), lw=0.9)
    ax.text((b + x2) / 2, y0 + 0.98, "face 2", ha="center", va="bottom", fontweight="bold")
    lines = (
        "$dQ = w\\,(x - v)(x - b)$, per face:",
        "face 1: one quantum exactly,",
        "at the root nearest $v$, where",
        "$w\\,(v - b)^2 \\geq 4\\,W_{\\mathrm{rec}}$; else the",
        "most it can, $w\\,(v - b)^2 / 4$,",
        "at the midpoint",
        "face 2: the rest",
        "hole to 0, the levels and the",
        "remainder, where the share",
        "$O + C/2 \\leq W_{\\mathrm{rec}}$; the record's",
        "count down by one",
    )
    for i, line in enumerate(lines):
        ax.text(7.1, 11.95 - i * 0.48, line, ha="left", va="baseline")
    ax.text(
        0.4,
        8.0,
        "$W_{\\mathrm{rec}}$ = (the laid share\n+ count div 2) div count",
        ha="left",
        va="top",
    )


def the_books(ax: Axes) -> None:
    """(d) The ledger in whole numbers, the click line to the file and the declaration."""
    ax.text(-0.3, 6.7, "d", ha="left", va="top", fontweight="bold", fontsize=9)
    rows = (
        ("the arriving record's count", "1", "0"),
        ("its levels and remainder at the drawn Node", "$v$, $b$, $r$", "0, 0, 0"),
        ("the NodeReader's record, its parts g / e", "1 / 0", "0 / 1"),
    )
    yt = 6.25
    ax.text(0.4, yt, "the ledger", ha="left", va="center", fontweight="bold")
    ax.text(9.6, yt, "before", ha="center", va="center", fontweight="bold")
    ax.text(12.0, yt, "after", ha="center", va="center", fontweight="bold")
    ax.plot([0.0, 13.0], [yt - 0.35, yt - 0.35], color=INK, lw=0.6)
    for i, (name, before, after) in enumerate(rows):
        yy = yt - 0.9 - i * 0.62
        ax.text(0.0, yy, name, ha="left", va="center")
        ax.text(9.6, yy, before, ha="center", va="center", color=BLUE if i < 2 else INK)
        ax.text(12.0, yy, after, ha="center", va="center", color=ORANGE if i == 2 else INK)
    # the click line: the NodeReader's report, the only measurement
    for ybox, text in (
        (
            1.95,
            "the click line, the NodeReader's report, the only measurement:\n"
            "the window's index, the NodeReader, the family and the part,\n"
            "the count before and after, the NodeReader's own clock; no Node",
        ),
        (
            -0.1,
            "the declaration in the NodeReader's file: its seed; its Nodes,\n"
            "two or more, connected; its own record with the parts g and e\n"
            "and the lifetime where declared",
        ),
    ):
        ax.add_patch(
            FancyBboxPatch(
                (0.0, ybox),
                13.0,
                1.75,
                boxstyle="round,pad=0,rounding_size=0.12",
                facecolor=PALE,
                edgecolor=INK,
                lw=0.6,
                zorder=3,
            )
        )
        ax.text(0.25, ybox + 0.875, text, ha="left", va="center", zorder=4, linespacing=1.25)


def the_node(ax: Axes) -> None:
    """(b), (c) and (d) in one frame: the region, the hole and the books."""
    ax.set_xlim(-0.3, 13.2)
    ax.set_ylim(-0.3, 18.9)
    ax.set_aspect("equal")
    ax.axis("off")
    the_region(ax)
    the_hole(ax)
    the_books(ax)


def click_body(output: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(6.85, 4.8), gridspec_kw={"width_ratios": (3.35, 3.4)})
    spacetime(axes[0])
    the_node(axes[1])
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005, wspace=0.03)
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
