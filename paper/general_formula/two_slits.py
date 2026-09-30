"""The two slits' figure, drawn from the documents' rows, by no run of the engine.

The screen's rises over the window (the bars, DETECTOR, the measurement) beside
the blind row written before the run (the dashed curve), across the screen's 48
Nodes, as docs/ALGEBRA.md holds them in row (g) of the rows against nature. The
pattern is read on y = 4 to 43; the outer four Nodes on either side carry the y
faces' reflections. Every number below is the law's document's.

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
from matplotlib.figure import Figure  # noqa: E402

HERE = Path(__file__).resolve().parent
INK, MID, LIGHT = "#000000", "#808080", "#d0d0d0"

# The blind row, written before the run: the count through each screen Node over the window.
BLIND = [2, 6, 7, 6, 3, 3, 6, 8, 8, 6, 6, 6, 6, 4, 3, 2, 1, 2, 2, 4, 7, 9, 11, 13]
BLIND += [13, 12, 11, 9, 7, 4, 3, 2, 1, 2, 3, 5, 5, 6, 6, 8, 9, 6, 3, 4, 7, 8, 7, 3]
# The measured row: the screen's rises over the window 45 to 120 (DETECTOR).
MEASURED = [0, 4, 10, 4, 6, 0, 0, 7, 5, 7, 6, 3, 7, 1, 1, 2, 0, 0, 6, 7, 6, 8, 12, 17]
MEASURED += [18, 17, 12, 8, 7, 6, 6, 0, 0, 2, 2, 2, 5, 4, 2, 3, 10, 1, 3, 4, 9, 10, 6, 2]
PATTERN = (4, 43)


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def two_slits(output: Path) -> None:
    """The bars of the measurement beside the dashed blind row."""
    assert len(BLIND) == 48 and len(MEASURED) == 48
    fig, ax = plt.subplots(figsize=(6.2, 2.7))
    nodes = list(range(48))
    ax.bar(nodes, MEASURED, width=0.8, color=INK, label="measured: the rises over the window (DETECTOR)")
    ax.plot(nodes, BLIND, "--", color=MID, linewidth=1.0, label="blind: written before the run")
    for edge in (PATTERN[0] - 0.5, PATTERN[1] + 0.5):
        ax.axvline(edge, color=LIGHT, linewidth=0.8)
    for y in (8, 24, 40):
        ax.text(y, 19.2, "max", ha="center", fontsize=7, color=MID)
    for y in (16, 32):
        ax.text(y, 19.2, "min", ha="center", fontsize=7, color=MID)
    ax.set_xlim(-0.8, 47.8)
    ax.set_ylim(0, 21)
    ax.set_xticks(range(0, 48, 4))
    ax.set_xlabel("the screen's Node, $y$")
    ax.set_ylabel("quanta over the window")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize=7)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
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
