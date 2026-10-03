"""The click at a bound body, drawn from the definitions, by no run of the engine, in black and grey.

Two panels at the page's width. (a) Space and time: the giver's record runs
forward from its root, every path at once, the future (solid lines); at the body's one
Node the arriving quantum meets the body's own transition and the instrument
draws at the window's close, the click, the now; from the click the same line is
read backward, Rule3 at -1, the past (dashed lines), a reading and never a write; the
body's change spreads forward by Rule3 at one Link per interval, the front, and
inside the click's light cone the record that gave is erased, its levels beyond
the front an empty wave with count 0. (b) The one Node before and after the
write: the body's two parts g and e, the arriving record, the draw at the
window's close, the hole and the lay, the click line to the detector's file.
Nothing here is a number of a run.

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
        "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
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
)

HERE = Path(__file__).resolve().parent
INK, GREY, LIGHT, PALE = "#000000", "#7a7a7a", "#c8c8c8", "#efefef"
BLUE, BLUE_MID, BLUE_PALE = (
    "#000000",
    "#b4b4b4",
    "#e6e6e6",
)  # the future, run forward: solid lines, grey fill
ORANGE, ORANGE_PALE = "#000000", "#e6e6e6"  # the past, read backward: dashed lines
BOX = {
    "boxstyle": "round,pad=0.15,rounding_size=0.2",
    "facecolor": "white",
    "edgecolor": "none",
    "alpha": 1.0,
}


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


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
    ax.add_patch(Circle((x, y), 0.26, facecolor=color, edgecolor="none", zorder=8))
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
    """(a) The future from the root, the click at the body's Node, the past read back, the front."""
    ax.set_xlim(-0.4, 10.8)
    ax.set_ylim(-1.3, 10.9)
    ax.set_aspect("equal")
    ax.axis("off")
    x0, xb, tc, top = (
        1.0,
        7.4,
        6.2,
        10.3,
    )  # the giver's root, the body's Node, the click, the top
    pace = (xb - x0) / tc  # the record's pace, schematic: its edge reaches the body at the click
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
    for k in range(1, 12):
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
    ax.plot([x0, x0 + pace * top], [0, top], color=BLUE, lw=0.9, zorder=3)
    arrow(ax, (x0 + pace * 2.0, 2.0), (x0 + pace * 3.4, 3.4), color=BLUE, lw=0.9)
    # the past: the reading back from the click to the root, dashed, through several paths
    for xm, tm in ((x0 + 0.9, 2.8), (x0 + 2.4, 1.6), (x0 + 3.9, 3.6)):
        ax.plot([xb, xm, x0], [tc, tm, 0], color=ORANGE, lw=0.8, ls=(0, (3, 2)), zorder=4)
    xm, tm = x0 + 2.4, 1.6
    arrow(
        ax,
        (xb - 0.30 * (xb - xm), tc - 0.30 * (tc - tm)),
        (xb - 0.42 * (xb - xm), tc - 0.42 * (tc - tm)),
        color=ORANGE,
        lw=1.0,
    )
    # the front from the click: the new future, one Link per interval; the record that gave erased inside
    front = Polygon(
        [(xb, tc), (xb + bound * (top - tc), top), (xb - bound * (top - tc), top)],
        closed=True,
        facecolor="white",
        edgecolor="none",
        zorder=3,
    )
    ax.add_patch(front)
    ax.plot(
        [xb - bound * (top - tc), xb, xb + bound * (top - tc)],
        [top, tc, top],
        color=BLUE,
        lw=1.1,
        zorder=5,
    )
    for k in range(1, 5):
        t = tc + k * 0.85
        ax.plot(
            [xb - bound * (t - tc), xb + bound * (t - tc)],
            [t, t],
            color=BLUE_MID,
            lw=0.5,
            zorder=4,
        )
    # the world lines: the giver and the bound body at its one Node
    ax.plot([x0, x0], [-0.3, top], color=GREY, lw=0.8, zorder=4)
    ax.plot([xb, xb], [-0.3, tc], color=INK, lw=1.0, zorder=6)
    ax.plot([xb, xb], [tc, top], color=INK, lw=2.6, zorder=6)
    ax.plot(
        [xb, xb + 0.95 * (top - 8.9)],
        [8.9, top],
        color=BLUE,
        lw=0.8,
        ls=(0, (1, 1.3)),
        zorder=6,
    )
    # the root, the window, the click
    ax.plot(x0, 0, "o", ms=4.5, color=INK, zorder=7)
    ax.plot([xb + 0.18, xb + 0.18], [tc - 1.5, tc], color=INK, lw=0.7, zorder=6)
    ax.plot([xb + 0.08, xb + 0.28], [tc - 1.5, tc - 1.5], color=INK, lw=0.7, zorder=6)
    ax.add_patch(Circle((xb, tc), 0.34, facecolor="white", edgecolor=INK, lw=1.2, zorder=7))
    ax.add_patch(Circle((xb, tc), 0.12, facecolor=INK, edgecolor="none", zorder=8))
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
        xb + 0.55,
        tc + 0.05,
        "click: the now",
        ha="left",
        va="bottom",
        fontweight="bold",
        zorder=9,
        bbox=BOX,
    )
    ax.text(xb + 0.55, tc - 0.75, "window", ha="left", va="center", zorder=9, bbox=BOX)
    ax.text(
        xb - 0.3,
        9.0,
        "front",
        color=BLUE,
        fontweight="bold",
        ha="right",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(
        x0 - 0.6,
        9.3,
        "empty\nwave",
        color=BLUE,
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(xb - 0.45, 7.7, "body\nchanged: e", ha="right", va="center", zorder=9, bbox=BOX)
    ax.text(
        xb + 1.0,
        10.05,
        "giving",
        color=BLUE,
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(
        xb + 0.4,
        2.2,
        "bound body\nat its Node: g",
        ha="left",
        va="center",
        zorder=9,
        bbox=BOX,
    )
    ax.text(x0 - 0.35, -0.5, "root", ha="right", va="center", zorder=9)
    number(ax, x0 - 0.55, 0.0, 1)
    number(ax, x0 + 3.9, 2.3, 2, BLUE)
    number(ax, xb + 0.75, tc - 1.45, 3)
    number(ax, xb - 0.9, tc + 0.1, 4, ORANGE)
    number(ax, xb - 2.1, 9.0, 5, BLUE)
    ax.text(-0.3, 10.85, "a", ha="left", va="top", fontweight="bold", fontsize=9)


def node_box(ax: Axes, cx: float, cy: float, s: float) -> None:
    """A Node of the GameBoard: a rounded square with its six Ports, four in the plane, two out of it."""
    ax.add_patch(
        FancyBboxPatch(
            (cx - s / 2, cy - s / 2),
            s,
            s,
            boxstyle="round,pad=0,rounding_size=0.18",
            facecolor="white",
            edgecolor=INK,
            lw=0.9,
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


def ladder(ax: Axes, cx: float, cy: float, upper: bool) -> None:
    """The body's two parts at the Node, g below and e above, the laid part a filled dot."""
    for y, lab, filled in ((cy - 0.42, "g", not upper), (cy + 0.42, "e", upper)):
        ax.plot([cx - 0.45, cx + 0.45], [y, y], color=INK, lw=1.0, zorder=4)
        ax.text(cx + 0.58, y, lab, ha="left", va="center", fontstyle="italic", zorder=5)
        if filled:
            ax.plot(cx, y + 0.17, "o", ms=5.5, color=ORANGE if upper else INK, zorder=6)


def wave(ax: Axes, x1: float, x2: float, y: float, color: str, n: int = 4, amp: float = 0.16) -> None:
    """A short wavy line, the record's quantum on its way."""
    xs = [x1 + (x2 - x1) * i / 60 for i in range(61)]
    ys = [y + amp * math.sin(2 * math.pi * n * (x - x1) / (x2 - x1)) for x in xs]
    ax.plot(xs, ys, color=color, lw=1.1, zorder=5)
    arrow(ax, (x2 - 0.01, y), (x2 + 0.2, y), color=color, lw=1.1)


def the_node(ax: Axes) -> None:
    """(b) The one Node before the window closes and after the one write, and the file."""
    ax.set_xlim(-0.3, 10.9)
    ax.set_ylim(-4.65, 5.3)
    ax.set_aspect("equal")
    ax.axis("off")
    s = 2.3
    y = 2.6
    xa, xb = 1.7, 7.0
    # before: the record's quantum arrives, the body holds g
    node_box(ax, xa, y, s)
    ladder(ax, xa - 0.15, y, upper=False)
    wave(ax, xa - 2.3, xa - s / 2 - 0.4, y, BLUE)
    ax.text(
        xa - s / 2 - 0.1,
        y + s / 2 + 0.55,
        "before the close",
        ha="left",
        va="bottom",
        fontweight="bold",
    )
    ax.text(
        xa - 1.4,
        y - 0.75,
        "the record,\ncount 1",
        color=BLUE,
        ha="center",
        va="top",
        fontsize=7,
    )
    # the draw between them
    arrow(ax, (xa + s / 2 + 0.45, y), (xb - s / 2 - 0.45, y), lw=1.0)
    ax.text(
        (xa + xb) / 2,
        y + 0.3,
        "the draw at the\nwindow's close",
        ha="center",
        va="bottom",
        fontsize=7,
    )
    ax.text(
        (xa + xb) / 2,
        y - 0.3,
        "by the labels'\nsquares: realised?\nat which Node?",
        ha="center",
        va="top",
        fontsize=7,
    )
    # after: one write at the Node; the body holds e; the front leaves through the Ports
    node_box(ax, xb, y, s)
    ladder(ax, xb - 0.15, y, upper=True)
    arrow(ax, (xb - 0.15, y - 0.25), (xb - 0.15, y + 0.25), color=ORANGE, lw=1.2)
    ax.text(
        xb,
        y + s / 2 + 0.55,
        "after the write",
        ha="center",
        va="bottom",
        fontweight="bold",
    )
    for dx, dy in ((1, 0), (0, 1), (0, -1)):
        a = (xb + dx * (s / 2 + 0.35), y + dy * (s / 2 + 0.35))
        b = (xb + dx * (s / 2 + 0.95), y + dy * (s / 2 + 0.95))
        arrow(ax, a, b, color=BLUE, lw=0.9)
    ax.text(
        xb + s / 2 + 1.05,
        y,
        "front",
        color=BLUE,
        ha="left",
        va="center",
        fontweight="bold",
    )
    ax.text(
        xb,
        y - s / 2 - 1.1,
        "by Rule3, one Link per interval",
        color=BLUE,
        ha="center",
        va="top",
        fontsize=7,
    )
    # the ledger: what the write changes at the Node, in whole numbers
    rows = (
        ("the record's count", "1", "0"),
        ("its levels and remainder", "now, before", "0, 0"),
        ("the body's part g / e", "1 / 0", "0 / 1"),
    )
    yt = -1.0
    ax.text(0.0, yt, "at the Node", ha="left", va="center", fontweight="bold", fontsize=7)
    ax.text(5.2, yt, "before", ha="center", va="center", fontsize=7, fontweight="bold")
    ax.text(7.6, yt, "after", ha="center", va="center", fontsize=7, fontweight="bold")
    ax.plot([0.0, 8.9], [yt - 0.32, yt - 0.32], color=INK, lw=0.6)
    for i, (name, before, after) in enumerate(rows):
        yy = yt - 0.85 - i * 0.6
        ax.text(0.0, yy, name, ha="left", va="center", fontsize=7)
        ax.text(
            5.2,
            yy,
            before,
            ha="center",
            va="center",
            fontsize=7,
            color=BLUE if i < 2 else INK,
        )
        ax.text(
            7.6,
            yy,
            after,
            ha="center",
            va="center",
            fontsize=7,
            color=ORANGE if i == 2 else INK,
        )
    ax.text(
        8.0,
        yt - 0.85,
        "the hole",
        ha="left",
        va="center",
        fontsize=7,
        color=GREY,
        fontstyle="italic",
    )
    ax.text(
        8.0,
        yt - 1.45,
        "one quantum's share",
        ha="left",
        va="center",
        fontsize=6,
        color=GREY,
        fontstyle="italic",
    )
    # the click line to the file: the report, the only measurement
    ax.add_patch(
        FancyBboxPatch(
            (0.0, -4.55),
            8.9,
            0.95,
            boxstyle="round,pad=0,rounding_size=0.12",
            facecolor=PALE,
            edgecolor=INK,
            lw=0.6,
            zorder=3,
        )
    )
    ax.text(
        0.25,
        -4.075,
        "the click line to the file, the only measurement:\nregion, the detector's clock and window, family, count",
        ha="left",
        va="center",
        fontsize=7,
        zorder=4,
    )
    number(ax, xa - s / 2 - 0.5, y + s / 2 + 0.72, 3)
    number(ax, xb + s / 2 + 0.2, y - s / 2 - 0.2, 5, BLUE)
    ax.text(-0.3, 5.25, "b", ha="left", va="top", fontweight="bold", fontsize=9)


def click_body(output: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(6.85, 3.75), gridspec_kw={"width_ratios": (11.2, 11.2)})
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
