"""The two slits: the declared file and its screen's row, the blind beside the law's real line.

(a) The GameBoard as the file declares it (examples/events/two_slits/two_slits.json, read through
design.json): the flat GameBoard of 45 x 48 Nodes, the packet of light at the wavelength 8 Links
laid over the columns 4 to 16, the wall at the column 20 with its two gaps of three rows 12 Links
apart, the screen at the column 44, twelve declared NodeReaders of four rows each. (b) The screen's
row per region: the Huygens blind written before the run (expectation.json, N = 273, with the
draw's scatter sqrt(N p (1 - p)) per region) beside the law's real line stepped on the same
world by the paper's script two_slits_real_line.py (N = 277.85 in the engine's labels). The
numbers are typed from those two files; nothing is read from a run of the engine.

    python paper/general_formula/two_slits_rows.py --output paper/general_formula/figures

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
from matplotlib.patches import Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
INK, GREY, LIGHT, PALE = "#000000", "#7a7a7a", "#c8c8c8", "#efefef"

# expectation.json: the Huygens blind row per region of four rows, N = 273 through the screen
BLIND = (21, 20, 26, 15, 9, 40, 45, 16, 11, 25, 22, 25)
BLIND_N = 273.0
# two_slits_real_line.txt: the law's real line on the same file, the window 45 to 130, the engine's labels
REAL = (20.32, 19.47, 26.75, 16.38, 9.31, 40.33, 47.31, 14.40, 12.38, 26.62, 21.39, 23.19)
REAL_N = 277.85
# the file's numbers (design.json, two_slits.json): the board, the packet, the wall, the gaps, the screen
LENGTH, HEIGHT = 45, 48
PACKET_X, PACKET_Y = (4, 16), (4, 44)
WALL_X, GAPS = 20, ((17, 19), (29, 31))
SCREEN_X, ROWS_PER_REGION = 44, 4


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def world(ax: Axes) -> None:
    """(a) The declared file: the board, the packet, the wall with its gaps, the screen's regions."""
    ax.set_xlim(-1.5, LENGTH + 1.5)
    ax.set_ylim(-12.0, HEIGHT + 7.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), LENGTH, HEIGHT, facecolor="white", edgecolor=INK, lw=0.8))
    # the packet: a raised cosine along x over the columns 4 to 16, flat across y
    for x in range(PACKET_X[0], PACKET_X[1] + 1):
        u = (x - 10) / 6.0
        shade = 0.5 * (1 + math.cos(math.pi * u)) if abs(u) <= 1 else 0.0
        g = 1 - 0.55 * shade
        ax.add_patch(
            Rectangle((x, PACKET_Y[0]), 1, PACKET_Y[1] - PACKET_Y[0]),
        )
        ax.patches[-1].set(facecolor=(g, g, g), edgecolor="none")
    ax.annotate(
        "", xy=(19.0, 24), xytext=(13.5, 24), arrowprops={"arrowstyle": "-|>", "lw": 0.8, "color": INK}
    )
    ax.text(6.5, -1.2, "the packet,\n$\\lambda = 8$", ha="center", va="top", fontsize=7)
    # the wall at the column 20 with the two gaps
    ax.add_patch(Rectangle((WALL_X, 0), 1, HEIGHT, facecolor=INK, edgecolor="none"))
    for lo, hi in GAPS:
        ax.add_patch(Rectangle((WALL_X, lo), 1, hi - lo + 1, facecolor="white", edgecolor="none"))
    ax.text(WALL_X + 4.5, -1.2, "the wall,\ntwo gaps\n$d = 12$", ha="center", va="top", fontsize=7)
    # the screen: twelve regions of four rows
    for r in range(12):
        y = r * ROWS_PER_REGION
        ax.add_patch(
            Rectangle(
                (SCREEN_X, y),
                1,
                ROWS_PER_REGION,
                facecolor=PALE if r % 2 else LIGHT,
                edgecolor=INK,
                lw=0.4,
            )
        )
    ax.text(
        SCREEN_X + 0.5, -1.2, "the screen:\n12 NodeReaders\nof 4 rows", ha="center", va="top", fontsize=7
    )
    ax.annotate(
        "",
        xy=(SCREEN_X, HEIGHT + 1.4),
        xytext=(WALL_X + 1, HEIGHT + 1.4),
        arrowprops={"arrowstyle": "<->", "lw": 0.6, "color": GREY},
    )
    ax.text(
        (WALL_X + SCREEN_X) / 2 + 0.5,
        HEIGHT + 2.0,
        "$L = 24$ Links",
        ha="center",
        va="bottom",
        fontsize=7,
        color=GREY,
    )
    ax.text(-1.2, HEIGHT / 2, "$y$", ha="right", va="center")
    ax.text(LENGTH / 2, -0.4 - 5.0, "", ha="center")
    ax.text(-1.2, HEIGHT + 6.0, "a", ha="right", va="bottom", fontweight="bold", fontsize=9)


def rows(ax: Axes) -> None:
    """(b) The screen's row per region: the blind with its scatter, the real line beside it."""
    xs = list(range(12))
    w = 0.38
    scatter = [math.sqrt(BLIND_N * (c / BLIND_N) * (1 - c / BLIND_N)) for c in BLIND]
    ax.bar(
        [x - w / 2 for x in xs],
        BLIND,
        width=w,
        facecolor="white",
        edgecolor=INK,
        lw=0.8,
        label="the blind: Huygens, written before the run ($N = 273$)",
    )
    ax.errorbar(
        [x - w / 2 for x in xs], BLIND, yerr=scatter, fmt="none", ecolor=INK, elinewidth=0.6, capsize=1.5
    )
    ax.bar(
        [x + w / 2 for x in xs],
        REAL,
        width=w,
        facecolor=LIGHT,
        edgecolor=INK,
        lw=0.5,
        label="the law's real line on the same file ($N = 277.85$)",
    )
    ax.set_xticks(xs)
    ax.set_xticklabels([str(x) for x in xs])
    ax.set_xlabel("the screen's region, from the row 0 across $y$")
    ax.set_ylabel("quanta over the window")
    ax.set_ylim(0, 66)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=2, labelsize=7)
    ax.text(5.55, 50.5, "the central maximum", ha="right", va="bottom", fontsize=7, color=GREY)
    for r in (4, 8):
        ax.text(
            r,
            max(BLIND[r], REAL[r]) + scatter[r] + 3.2,
            "a minimum",
            ha="center",
            va="bottom",
            fontsize=7,
            color=GREY,
        )
    ax.legend(loc="upper right", frameon=False, fontsize=7, handlelength=1.2, bbox_to_anchor=(1.0, 1.02))
    ax.text(-1.5, 65, "b", ha="left", va="top", fontweight="bold", fontsize=9)


def two_slits_rows(output: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(6.85, 2.9), gridspec_kw={"width_ratios": (1.0, 1.55)})
    world(axes[0])
    rows(axes[1])
    fig.subplots_adjust(left=0.01, right=0.995, top=0.95, bottom=0.17, wspace=0.18)
    output.mkdir(parents=True, exist_ok=True)
    save(fig, output / "two_slits_rows.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    args = parser.parse_args()
    two_slits_rows(args.output)


if __name__ == "__main__":
    main()
