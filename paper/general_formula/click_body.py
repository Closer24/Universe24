"""The click at a NodeDetector, drawn from the definitions, by no run of the engine, in black and grey.

Two panels side by side at the text width of Springer's sn-jnl (131 mm), every lettering 8 pt at the printed
size. (a) Space and time: the arriving record runs forward from its root, every path at once; the click is the
meeting of the forward record with the transition read backward from the click; the write at the drawn Node;
the front, one shell per interval, erases the absorbed record inside the click's causal cone, the empty wave
beyond it at count 0. (b) The NodeDetector's region before the window's close and after the one write at the
drawn Node, the draw at the close between them, the front leaving by Rule3 at one Link per interval. The
absorption's write (the hole, two cases) and the books in whole numbers, the long version's panels (c) and
(d), are the text of the short paper's Section 2.5; the functions that drew them, the_hole and the_books,
stay in this file for the long version's record and are not called.
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
        fontsize=8,
        fontweight="bold",
        zorder=9,
    )


def spacetime(ax: Axes) -> None:
    """(a) The future from the source Node, the meeting at the region, the click, the write at the drawn Node, the front."""
    ax.set_xlim(-1.1, 11.6)
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
    # the NodeDetector's region: two adjacent Nodes, a strip of two world lines
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
    # the world lines: the giver's source Node, the region's two Nodes, the drawn Node written at the click
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
        "emission, per window:\none quantum at\n$\\Omega = \\omega_e - \\omega_g$",
        color=BLUE,
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(
        xr + 0.4,
        2.6,
        "the NodeDetector's\nregion: two Nodes,\nits configuration in $g$",
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(x0 + 0.35, -0.45, "source Node", ha="left", va="center", zorder=9)
    number(ax, x0 - 0.55, 0.0, 1)
    number(ax, 5.5, 6.75, 2)
    number(ax, xr + 0.85, tc - 1.45, 3)
    number(ax, xr - 0.55, 9.5, 4)
    number(ax, 2.3, 11.3, 5, BLUE)
    ax.text(-0.3, 15.65, "a", ha="left", va="top", fontweight="bold", fontsize=9)


def node_box(ax: Axes, cx: float, cy: float, s: float, lw: float = 0.9) -> None:
    """A Node of the lattice: a rounded square with its six Ports, four in the plane, two out of it."""
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
    """The NodeDetector's region: two adjacent Nodes with the Link between them, the dotted boundary of the
    declaration, and the NodeDetector's own record laid over both, equal levels on both, its parts g and e a
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
            for cx in (x2,) if drawn else (x1, x2):
                ax.plot(cx + 0.12, y + 0.16, "o", ms=5.0, color=INK, zorder=6)
    if drawn:
        arrow(ax, (x2 - 0.3, cy - 0.2), (x2 - 0.3, cy + 0.2), color=ORANGE, lw=1.2)
    return x1, x2


def wave(ax: Axes, x1: float, x2: float, y: float, color: str, n: int = 4, amp: float = 0.16) -> None:
    """A short wavy line, the field's quantum on its way."""
    xs = [x1 + (x2 - x1) * i / 60 for i in range(61)]
    ys = [y + amp * math.sin(2 * math.pi * n * (x - x1) / (x2 - x1)) for x in xs]
    ax.plot(xs, ys, color=color, lw=1.1, zorder=5)
    arrow(ax, (x2 - 0.01, y), (x2 + 0.2, y), color=color, lw=1.1)


def the_region(ax: Axes) -> None:
    """(b) The NodeDetector's region before the close and after the one write at the drawn Node."""
    s = 1.6
    y = 15.9
    xa, xb = region(ax, 1.7, y, s, upper=False, drawn=False)
    wave(ax, -0.3, xa - s / 2 - 0.5, y, BLUE)
    ax.text(
        xa - s / 2 - 0.05,
        y + s / 2 + 1.7,
        "before the close",
        ha="left",
        va="bottom",
        fontweight="bold",
    )
    ax.text(
        (xa + xb) / 2,
        y - s / 2 - 0.75,
        "the arriving field,\ncount 1, at the\nregion's boundary",
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
        y + s / 2 + 1.7,
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
        (xc + xd) / 2 - 0.1,
        y - s / 2 - 1.0,
        "the drawn Node, by the share;\nthe front by Rule3,\none Link per interval",
        ha="center",
        va="top",
    )
    number(ax, xa - s / 2 - 0.55, y + s / 2 + 1.95, 2)
    number(ax, xm, y - 0.65, 3)
    number(ax, xd + s / 2 + 0.75, y - s / 2 - 0.5, 4)
    ax.text(-0.3, 19.6, "b", ha="left", va="top", fontweight="bold", fontsize=9)


def the_hole(ax: Axes) -> None:
    """(c) The absorption's write at the drawn Node: one comparison of the field's booked share there against its own
    quantum W_rec; the sparse Node zeroed by the face Rule3 presents, the dense record undepleted with its count in
    the books (the advisor's words of 2026-10-04, #1793 comment 5985040913)."""
    ax.text(-0.3, 12.5, "c", ha="left", va="top", fontweight="bold", fontsize=9)
    ax.text(
        0.4,
        12.3,
        "the absorption: one comparison,\ntwo cases, no partial hole",
        ha="left",
        va="top",
        fontweight="bold",
    )
    zero, b, v = 0.9, 2.3, 4.6
    for case, y0, colour, lines in (
        (
            "sparse",
            10.15,
            BLUE,
            (
                "sparse: share at the Node $\\leq W_{\\mathrm{rec}}$:",
                "the hole to 0 by the face Rule3",
                "presents; the count down by one",
            ),
        ),
        (
            "dense",
            8.55,
            ORANGE,
            (
                "dense: share at the Node $> W_{\\mathrm{rec}}$:",
                "nothing written, the levels stand;",
                "the quantum moves in the books",
            ),
        ),
    ):
        arrow(ax, (0.3, y0), (5.6, y0), lw=0.7)
        ax.text(5.7, y0, "$x$", ha="left", va="center", color=GREY)
        for x, lab in ((zero, "0"), (b, "$b$"), (v, "$v$")):
            ax.plot([x, x], [y0 - 0.12, y0 + 0.12], color=INK, lw=0.7, zorder=5)
            ax.text(x, y0 - 0.2, lab, ha="center", va="top")
        if case == "sparse":
            arrow(ax, (v - 0.1, y0 + 0.5), (zero + 0.1, y0 + 0.5), lw=0.9)
            ax.text(
                (v + zero) / 2,
                y0 + 0.62,
                "the face: $v, b, r \\to 0$",
                ha="center",
                va="bottom",
                color=colour,
            )
        else:
            ax.text(
                (v + zero) / 2,
                y0 + 0.62,
                "nothing written",
                ha="center",
                va="bottom",
                color=colour,
                fontweight="bold",
            )
        for k, line in enumerate(lines):
            ax.text(
                6.25,
                y0 + 0.55 - k * 0.46,
                line,
                ha="left",
                va="top",
                fontweight="bold" if k == 0 else None,
                color=colour if k == 0 else INK,
            )
    ax.text(
        0.4, 7.5, "$W_{\\mathrm{rec}}$ = (the laid share + count div 2) div count", ha="left", va="top"
    )
    ax.text(0.4, 7.1, "$v$: the level Rule3 would write without the face", ha="left", va="top")


def the_books(ax: Axes) -> None:
    """(d) The books in whole numbers, the click line to the file and the declaration."""
    ax.text(-0.3, 6.85, "d", ha="left", va="top", fontweight="bold", fontsize=9)
    rows = (
        ("the arriving field's count", "1", "0"),
        ("its levels and remainder at the drawn Node", "$v$, $b$, $r$", "0, 0, 0"),
        ("the NodeDetector's configuration, its parts $g$ / $e$", "1 / 0", "0 / 1"),
    )
    yt = 6.4
    ax.text(0.4, yt, "the books", ha="left", va="center", fontweight="bold")
    ax.text(9.6, yt, "before", ha="center", va="center", fontweight="bold")
    ax.text(12.0, yt, "after", ha="center", va="center", fontweight="bold")
    ax.plot([0.0, 13.0], [yt - 0.35, yt - 0.35], color=INK, lw=0.6)
    for i, (name, before, after) in enumerate(rows):
        yy = yt - 0.85 - i * 0.58
        ax.text(0.0, yy, name, ha="left", va="center")
        ax.text(9.6, yy, before, ha="center", va="center", color=BLUE if i < 2 else INK)
        ax.text(12.0, yy, after, ha="center", va="center", color=ORANGE if i == 2 else INK)
    # the click line: the NodeDetector's report, the only measurement
    for ybox, text in (
        (
            2.1,
            "the click line, the NodeDetector's report, the one\n"
            "measurement: the window's index, the NodeDetector, the\n"
            "family, the part, the count before and after, the\n"
            "NodeDetector's own clock; no Node",
        ),
        (
            -0.3,
            "the declaration in the NodeDetector's file: its Nodes,\n"
            "two or more connected (one Node with a configuration of its\n"
            "own: its parts g, e and the lifetime); the world's draw,\n"
            "a body's NodeDetector's own seed",
        ),
    ):
        ax.add_patch(
            FancyBboxPatch(
                (0.0, ybox),
                13.0,
                2.05,
                boxstyle="round,pad=0,rounding_size=0.12",
                facecolor=PALE,
                edgecolor=INK,
                lw=0.6,
                zorder=3,
            )
        )
        ax.text(0.25, ybox + 1.025, text, ha="left", va="center", zorder=4, linespacing=1.1)


def the_node(ax: Axes) -> None:
    """(b) alone in its frame: the region before the close and after the write (the long version's (c) and (d) are the text of the short paper)."""
    ax.set_xlim(-0.3, 14.3)
    ax.set_ylim(12.9, 19.7)
    ax.set_aspect("equal")
    ax.axis("off")
    the_region(ax)


def click_body(output: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(5.16, 3.3), gridspec_kw={"width_ratios": (2.47, 2.69)})
    spacetime(axes[0])
    the_node(axes[1])
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005, wspace=0.02)
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
