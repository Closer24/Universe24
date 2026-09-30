"""The two branches' figure, drawn from the documents' rows, by no run of the engine.

The three masses of a body along its two branches (docs/ALGEBRA.md, the rows
against nature, (u): the advisor's tables, a reading of the algebra and no click,
the counts in the advisor's unit, the vacuum's share): the well over the count,
the inertia over the count and the fall against a free packet's, for the cloud
(the wide branch) and for the compact pixel (the narrow branch), each against
its total count. Every number below is the law's document's.

    python paper/general_formula/branches.py --output paper/general_formula/figures

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

# The cloud along its branch: total count, well / count, inertia / count, fall / free.
CLOUD: list[tuple[int, float | None, float | None, float | None]] = [
    (4000, 0.985, 1.061, 0.92),
    (3000, 0.991, 1.037, 0.95),
    (2000, 0.995, 1.022, 0.97),
    (1500, 0.996, 1.016, 0.98),
]
# The compact pixel along its branch: total count, well / count, inertia / count, fall / free
# (None where the document gives no number).
PIXEL: list[tuple[int, float | None, float | None, float | None]] = [
    (2541, 0.70, 1.04, None),
    (2640, 0.62, 0.99, 0.27),
    (3005, 0.54, None, None),
    (3449, 0.49, 0.90, 0.11),
    (4413, 0.42, None, None),
    (4917, 0.40, 0.83, 0.03),
    (5440, 0.39, 0.83, None),
]


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def points(
    rows: list[tuple[int, float | None, float | None, float | None]], column: int
) -> list[tuple[int, float]]:
    """The rows that carry a number in the column, as (total count, the number)."""
    found: list[tuple[int, float]] = []
    for row in rows:
        value = row[column]
        if value is not None:
            found.append((row[0], value))
    return found


def panel(ax: Axes, column: int, title: str) -> None:
    """One mass over the count against the total count, both branches."""
    cloud = points(CLOUD, column)
    pixel = points(PIXEL, column)
    ax.plot(
        [c for c, _ in cloud], [v for _, v in cloud], "o-", color=INK, markersize=4, label="the cloud"
    )
    ax.plot(
        [c for c, _ in pixel],
        [v for _, v in pixel],
        "s--",
        color=INK,
        markerfacecolor="white",
        markersize=4,
        label="the compact pixel",
    )
    ax.axhline(1.0, color=MID, linewidth=0.6)
    ax.set_title(title, fontsize=8)
    ax.set_xlabel("total count, in quanta")
    ax.set_xlim(1000, 5800)
    ax.set_ylim(0, 1.15)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def branches(output: Path) -> None:
    """The figure: three panels, one per mass."""
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.3))
    panel(axes[0], 1, "the well over the count")
    panel(axes[1], 2, "the inertia over the count")
    panel(axes[2], 3, "the fall against a free packet's")
    axes[0].legend(frameon=False, loc="lower left")
    fig.tight_layout()
    save(fig, output / "branches.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    arguments = parser.parse_args()
    arguments.output.mkdir(parents=True, exist_ok=True)
    branches(arguments.output)


if __name__ == "__main__":
    main()
