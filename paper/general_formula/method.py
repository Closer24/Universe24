"""The method's three layers and the way from nature's measurements to the paper's row, by no run.

Drawn from the paper's words (Section 1.1, the three layers; Section 5.3, the NodeDetector's
declaration; Section 10.1, the calibration series; Section 2.4, the implementation): the clicks of
nature on bound bodies are read, one click per coefficient, into the files' integers; the files
declare the world; the lattice is stepped by Rule3, one interval of acts, and writes the
NodeDetectors' click lines; the reader prints the run's row beside the blind row written before the
run; and only there the computed world meets the clicks it approaches. What is fixed and what is
free is written at each layer as the paper states it. Nothing here is a number of a run.

    python paper/general_formula/method.py --output paper/general_formula/figures

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
        "mathtext.fontset": "custom",
        "mathtext.rm": "Liberation Sans",
        "mathtext.it": "Liberation Sans:italic",
        "mathtext.bf": "Liberation Sans:bold",
    }
)  # the journal's lettering: 8 pt at the final size, one typeface for the words and the symbols, the figure drawn 1:1 at the page's width of 174 mm at most, fonts embedded
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
INK, GREY, PALE = "#000000", "#7a7a7a", "#efefef"


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def box(
    ax: Axes, x: float, y: float, w: float, h: float, title: str, body: str, shaded: bool = False
) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0,rounding_size=0.12",
            facecolor=PALE if shaded else "white",
            edgecolor=INK,
            lw=0.8,
        )
    )
    ax.text(x + w / 2, y + h - 0.22, title, ha="center", va="top", fontweight="bold", fontsize=7.5)
    ax.text(x + w / 2, y + h - 0.62, body, ha="center", va="top", fontsize=6.2, linespacing=1.15)


def arrow(
    ax: Axes, a: tuple[float, float], b: tuple[float, float], text: str = "", above: bool = True
) -> None:
    ax.add_patch(
        FancyArrowPatch(
            a,
            b,
            arrowstyle="-|>,head_length=3.2,head_width=1.8",
            color=INK,
            lw=0.9,
            shrinkA=0,
            shrinkB=0,
        )
    )
    if text:
        ax.text(
            (a[0] + b[0]) / 2,
            (a[1] + b[1]) / 2 + (0.14 if above else -0.14),
            text,
            ha="center",
            va="bottom" if above else "top",
            fontsize=6.5,
            color=GREY,
        )


def method(ax: Axes) -> None:
    ax.set_xlim(0, 14.2)
    ax.set_ylim(-0.55, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")
    w, h, y, gap = 2.45, 2.15, 0.95, 0.45
    xs = [0.1 + i * (w + gap) for i in range(5)]
    box(
        ax,
        xs[0],
        y,
        w,
        h,
        "nature's measurements",
        "measured numbers of bound bodies\nagainst a declared clock;\nnever a lattice reading",
        shaded=True,
    )
    box(
        ax,
        xs[1],
        y,
        w,
        h,
        "the files",
        "the universe file: the pairs\n$[\\mathrm{num}, \\mathrm{den}]$, $\\Gamma$, $T$, the\nholders' weights; the run's file:\nthe Nodes, the lays, the faces;\nthe NodeDetectors' four declarations",
    )
    box(
        ax,
        xs[2],
        y,
        w,
        h,
        "the lattice",
        "a NodeState at every Node;\none interval: Rule3 on the\nsix Ports, the read, the write;\nreversible, integers, no draw",
    )
    box(
        ax,
        xs[3],
        y,
        w,
        h,
        "the click lines",
        "the only measurement:\nregion, the NodeDetector's clock\nand window, family, count;\nthe NodeDetector's draw by\nthe shares, its declared seed",
    )
    box(
        ax,
        xs[4],
        y,
        w,
        h,
        "the reading",
        "the blind row written before\nthe run beside the run's row,\nits deviation and extrema;\nthe back-in-time gate: MATCH",
        shaded=True,
    )
    arrow(ax, (xs[0] + w, y + h / 2), (xs[1], y + h / 2))
    arrow(ax, (xs[1] + w, y + h / 2), (xs[2], y + h / 2))
    arrow(ax, (xs[2] + w, y + h / 2), (xs[3], y + h / 2))
    arrow(ax, (xs[3] + w, y + h / 2), (xs[4], y + h / 2))
    ax.text(
        xs[0] + w + gap / 2,
        y + h + 0.1,
        "the calibration series:\none click per coefficient",
        ha="center",
        va="bottom",
        fontsize=6.5,
        color=GREY,
    )
    ax.text(
        xs[1] + w + gap / 2,
        y + h + 0.1,
        "the loader:\nrefusals at load",
        ha="center",
        va="bottom",
        fontsize=6.5,
        color=GREY,
    )
    ax.text(
        xs[2] + w + gap / 2,
        y + h + 0.1,
        "the NodeDetector's\nwindow closes",
        ha="center",
        va="bottom",
        fontsize=6.5,
        color=GREY,
    )
    ax.text(
        xs[3] + w + gap / 2,
        y + h + 0.1,
        "the reader,\nafter the run",
        ha="center",
        va="bottom",
        fontsize=6.5,
        color=GREY,
    )
    # the comparison, only on the clicks' side: the reading back to nature's measurements
    ax.add_patch(
        FancyArrowPatch(
            (xs[4] + w / 2, y - 0.05),
            (xs[0] + w / 2, y - 0.05),
            arrowstyle="-|>,head_length=3.2,head_width=1.8",
            color=GREY,
            lw=0.8,
            connectionstyle="arc3,rad=0.0",
            shrinkA=0,
            shrinkB=0,
            linestyle=(0, (3, 2)),
        )
    )
    ax.text(
        (xs[0] + xs[4] + w) / 2,
        y - 0.2,
        "compared only here, click against measurement: the paper claims the method, never that nature is so",
        ha="center",
        va="top",
        fontsize=6.5,
        color=GREY,
    )
    # the three layers, fixed and free
    ax.text(
        xs[1] + w / 2,
        0.3,
        "the numbers:\nall free, as few\nas the rule allows",
        ha="center",
        va="top",
        fontsize=6.3,
    )
    ax.text(
        xs[2] + w / 2,
        0.3,
        "the lattice's rules:\nRule3 fixed,\nthe file's rows free",
        ha="center",
        va="top",
        fontsize=6.3,
    )
    ax.text(
        xs[3] + w / 2,
        0.3,
        "the click: its one\nform fixed, the four\ndeclarations free",
        ha="center",
        va="top",
        fontsize=6.3,
    )
    ax.text(
        xs[0] + w / 2,
        0.3,
        "the three layers of\nthe method, each with\na fixed and a free part:",
        ha="center",
        va="top",
        fontsize=6.3,
        color=GREY,
    )


def method_figure(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.85, 2.3))
    method(ax)
    fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
    output.mkdir(parents=True, exist_ok=True)
    save(fig, output / "method.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    args = parser.parse_args()
    method_figure(args.output)


if __name__ == "__main__":
    main()
