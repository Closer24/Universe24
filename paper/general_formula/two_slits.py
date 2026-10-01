"""The two slits' figure, drawn from the documents' rows, by no run of the engine.

The clicks credited to each of the screen's twelve declared detectors (the bars,
DETECTOR, the measurement) beside the blind row written before the run (the
dashed line), for the three worlds of docs/ALGEBRA.md, row (g) of the rows
against nature: the bright packet, the dilute packet and the which-way world
with the lower gap closed. Each detector is a region of four rows of the
screen's column, from the row 0. Every number below is the law's document's.

    python paper/general_formula/two_slits.py --output paper/general_formula/figures

Needs matplotlib. Nothing is read from a run.
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
    }
)
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

HERE = Path(__file__).resolve().parent
INK, MID = "#000000", "#808080"

# The bright world: the blind row per region (273 in all) and the clicks credited by
# the shares of what the screen saw (281 in all, the engine of the share).
BRIGHT_BLIND = [21, 20, 26, 15, 9, 40, 45, 16, 11, 25, 22, 25]
BRIGHT_CLICKS = [21, 20, 27, 16, 9, 41, 48, 15, 12, 27, 22, 23]
# The dilute world: the blind row (12.9 in all) and the clicks credited (28 in all).
DILUTE_BLIND = [1.0, 0.9, 1.2, 0.7, 0.4, 1.9, 2.1, 0.8, 0.5, 1.2, 1.0, 1.2]
DILUTE_CLICKS = [2, 2, 3, 2, 1, 4, 5, 1, 1, 3, 2, 2]
# The which-way world, the lower gap closed: the open gap's envelope (136.5 in all)
# and the clicks credited (142 in all).
WHICH_WAY_BLIND = [3.7, 4.9, 6.5, 8.7, 11.3, 14.1, 16.5, 17.6, 16.9, 14.8, 12.0, 9.3]
WHICH_WAY_CLICKS = [4, 5, 6, 8, 11, 14, 15, 16, 16, 16, 13, 18]


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def panel(ax: Axes, clicks: list[int], blind: list[float], title: str, top: float) -> None:
    """One world: the credited clicks per region beside the blind row."""
    assert len(clicks) == 12 and len(blind) == 12
    regions = list(range(12))
    ax.bar(regions, clicks, width=0.8, color=INK, label="the clicks credited (DETECTOR)")
    ax.plot(
        regions,
        blind,
        "o--",
        color=MID,
        markersize=3,
        linewidth=1.0,
        label="blind: written before the run",
    )
    ax.set_title(title, fontsize=8)
    ax.set_xlim(-0.8, 11.8)
    ax.set_ylim(0, top)
    ax.set_xticks(regions)
    ax.set_xticklabels([str(4 * region) for region in regions], fontsize=6)
    ax.set_xlabel("the detector's first row, $y$")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def two_slits(output: Path) -> None:
    """The three worlds side by side."""
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.9))
    panel(axes[0], BRIGHT_CLICKS, BRIGHT_BLIND, "bright: 281 clicks (blind 273)", 55)
    panel(axes[1], DILUTE_CLICKS, DILUTE_BLIND, "dilute: 28 clicks (blind 13)", 6)
    panel(axes[2], WHICH_WAY_CLICKS, WHICH_WAY_BLIND, "lower gap closed: 142 (blind 137)", 22)
    axes[0].set_ylabel("quanta over the window")
    axes[1].legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=2, fontsize=7)
    fig.subplots_adjust(left=0.08, right=0.99, top=0.9, bottom=0.36, wspace=0.3)
    save(fig, output / "two_slits.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    arguments = parser.parse_args()
    arguments.output.mkdir(parents=True, exist_ok=True)
    two_slits(arguments.output)


if __name__ == "__main__":
    main()
