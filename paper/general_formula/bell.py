"""Bell's figure, drawn from the documents' rows, by no run of the engine.

The correlation E at the four CHSH settings against the sum of the settings'
calibrated phases, as docs/ALGEBRA.md holds them in row (h) of the rows against
nature: E by the signs alone on both sides with every quantum credited (the
marks, DETECTOR, the classical pair under a local credit, S = 2.000), the
triangle 1 - 2 |phi| / pi of a shared classical phase read by its sign, and the
cosine, nature's E = cos(delta_A + delta_B) and the meeting's blind row for the
run to come. Every number below is the law's document's.

    python paper/general_formula/bell.py --output paper/general_formula/figures

Needs matplotlib. Nothing is read from a run.
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
    }
)
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

HERE = Path(__file__).resolve().parent
INK, MID = "#000000", "#808080"

# The calibrated phases of the settings, in degrees: a and a' on the right, b and b' on the left.
PHASES = {"a": 0.0, "a'": 73.6, "b": -37.2, "b'": -108.8}
SETTINGS = [("a", "b"), ("a", "b'"), ("a'", "b"), ("a'", "b'")]
# E by the signs alone on both sides, every quantum credited (S = 2.000).
SIGNS = [0.625, -0.250, 0.500, 0.625]


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def bell(output: Path) -> None:
    """E against the phases' sum: the two readings beside the cosine and the triangle."""
    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    degrees = [d / 2 for d in range(-360, 361)]
    ax.plot(
        degrees,
        [math.cos(math.radians(d)) for d in degrees],
        "-",
        color=INK,
        linewidth=0.9,
        label=r"nature, and the meeting's blind row: $\cos(\delta_A + \delta_B)$, $S = 2.83$",
    )
    ax.plot(
        degrees,
        [1 - 2 * abs(d) / 180 for d in degrees],
        ":",
        color=MID,
        linewidth=0.9,
        label="the triangle of a shared classical phase",
    )
    sums = [PHASES[a] + PHASES[b] for a, b in SETTINGS]
    ax.plot(
        sums,
        SIGNS,
        "s",
        color=INK,
        markersize=5,
        label="run: the signs alone, $S = 2.000$ (DETECTOR)",
    )
    offsets = {
        ("a", "b"): (-14, 6),
        ("a", "b'"): (-16, 0),
        ("a'", "b"): (14, 6),
        ("a'", "b'"): (12, -12),
    }
    for (a, b), total, value in zip(SETTINGS, sums, SIGNS, strict=True):
        ax.annotate(
            f"({a}, {b})",
            (total, value),
            textcoords="offset points",
            xytext=offsets[(a, b)],
            ha="center",
            fontsize=6,
            color=MID,
        )
    ax.axhline(0, color=MID, linewidth=0.5)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-1.1, 1.25)
    ax.set_xticks(range(-180, 181, 60))
    ax.set_xlabel(r"$\delta_A + \delta_B$, the settings' calibrated phases, in degrees")
    ax.set_ylabel("$E$")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=1, fontsize=6.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    save(fig, output / "bell.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    arguments = parser.parse_args()
    arguments.output.mkdir(parents=True, exist_ok=True)
    bell(arguments.output)


if __name__ == "__main__":
    main()
