"""The two slits mid-run: three lattice readings of the one experiment, a diagnostic and no measurement.

The engine's own look tool (`PYTHONPATH=src python tools/look/record.py examples/events/two_slits/two_slits.json
--intervals 130`, docs/ENGINE.md section 6, item 10) steps the shipped two-slits file by the engine's own step, Rule3 at
every Node with the file's lay, its faces and its NodeDetectors' reads, and writes every interval's arrays, labelled
"lattice reading", the engine's label at the recorded commit. This script draws three of its frames: the level now of the light record over the declared
board at the intervals 18 (the packet's centre at the wall), 40 (the two wavelets past the gaps) and 62 (the
packet's centre at the screen), as grey, the wall with its two gaps and the screen's twelve regions drawn from the
file's declarations. Nothing on the figure is a measurement; the measurement of this file is the screen's row of
two_slits_rows.py (Fig. 6 of the paper).

    python paper/general_formula/two_slits_frames.py                      draws figures/two_slits_frames.pdf and .eps
    python paper/general_formula/two_slits_frames.py --look <world>.look.json   records the three frames first

The recording figures/two_slits_frames.json holds the three frames alone (interval, shape, offset, the sparse level
array) as the look tool wrote them, so that the figure is reproducible without the 14 MB look file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

matplotlib.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
        "font.size": 8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "mathtext.fontset": "custom",
        "mathtext.rm": "sans",
        "mathtext.it": "sans:italic",
        "mathtext.bf": "sans:bold",
        "axes.linewidth": 0.5,
    }
)  # the journal's lettering: 8 pt at the drawn size, one typeface, fonts embedded, black and grey

HERE = Path(__file__).resolve().parent
FIGURES = HERE / "figures"
RECORDING = FIGURES / "two_slits_frames.json"
INTERVALS = (18, 40, 62)
INK = "black"
GREY = "0.55"

# the file's declarations (examples/events/two_slits/design.json, two_slits.json): the declared board, the wall, the screen
LENGTH, HEIGHT = 45, 48
WALL = 20
GAPS = ((17, 19), (29, 31))
SCREEN = 44
ROWS_PER_REGION = 4
PACKET_AMPLITUDE = 1328


def record(look_path: Path) -> None:
    """Keep the three frames of the look file, as written, in the recording beside the figures."""
    look = json.loads(look_path.read_text())
    assert look["label"] == "lattice reading" and look["verdict"] == "LAWFUL", look.get("verdict")
    frames = {frame["interval"]: frame for frame in look["frames"]}
    kept = []
    for interval in INTERVALS:
        frame = frames[interval]
        now = frame["families"]["charge"]["now"]
        kept.append(
            {
                "interval": interval,
                "shape": frame["shape"],
                "offset": frame["offset"],
                "at": now["at"],
                "values": now["values"],
            }
        )
    RECORDING.write_text(
        json.dumps(
            {
                "label": look["label"],
                "world": look["world"],
                "verdict": look["verdict"],
                "intervals": look["intervals"],
                "family": "charge",
                "array": "now, the level at the interval, sparse: index = x * shape_y + y over the grown board, x at the file's coordinates minus offset_x",
                "frames": kept,
            },
            separators=(",", ":"),
        )
        + "\n"
    )


def level_over_the_declared_board(frame: dict) -> np.ndarray:
    """The level now over the declared 45 x 48 board at the file's coordinates; the grown layers beyond the receding
    faces are not drawn."""
    shape_x, shape_y = frame["shape"][0], frame["shape"][1]
    offset_x = frame["offset"][0]
    grown = np.zeros((shape_x, shape_y))
    at = np.asarray(frame["at"])
    grown[at // shape_y, at % shape_y] = frame["values"]
    return grown[offset_x : offset_x + LENGTH, :]


def panel(ax: Axes, frame: dict, letter: str) -> None:
    level = level_over_the_declared_board(frame)
    magnitude = np.abs(level).T / PACKET_AMPLITUDE  # rows y up, columns x right
    ax.imshow(
        1 - np.clip(magnitude, 0, 1) ** 0.6,
        cmap="gray",
        vmin=0,
        vmax=1,
        origin="lower",
        extent=(-0.5, LENGTH - 0.5, -0.5, HEIGHT - 0.5),
        interpolation="nearest",
    )
    # the wall with its gaps open: the inner face the file declares, every Node of the column but the gaps
    for y in range(HEIGHT):
        if any(low <= y <= high for low, high in GAPS):
            continue
        ax.add_patch(Rectangle((WALL - 0.5, y - 0.5), 1, 1, facecolor=INK, edgecolor="none", zorder=3))
    # the screen's twelve regions: a bracket per region at the last column
    for region in range(HEIGHT // ROWS_PER_REGION):
        y0 = region * ROWS_PER_REGION - 0.5
        ax.add_patch(
            Rectangle(
                (SCREEN - 0.5, y0 + 0.15),
                1,
                ROWS_PER_REGION - 0.3,
                facecolor="none",
                edgecolor=INK,
                lw=0.6,
                zorder=3,
            )
        )
    ax.set_xlim(-0.5, LENGTH - 0.5)
    ax.set_ylim(-0.5, HEIGHT - 0.5)
    ax.set_aspect("equal")
    ax.set_xticks([0, 10, 20, 30, 44])
    ax.set_yticks([0, 16, 32, 47])
    ax.tick_params(length=2, width=0.5, pad=1.5)
    ax.set_xlabel("$x$, the column (Links)", labelpad=1)
    ax.text(0.0, 1.02, letter, transform=ax.transAxes, ha="left", va="bottom", fontweight="bold")
    ax.text(
        0.5,
        1.02,
        f"interval {frame['interval']} of 130",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
    )


def draw(output: Path) -> None:
    recording = json.loads(RECORDING.read_text())
    frames = {frame["interval"]: frame for frame in recording["frames"]}
    width_in = 174 / 25.4
    fig, axes = plt.subplots(1, 3, figsize=(width_in, 2.45))
    for ax, interval, letter in zip(axes, INTERVALS, "abc", strict=True):
        panel(ax, frames[interval], letter)
    axes[0].set_ylabel("$y$, the row (Links)", labelpad=1)
    for ax in axes[1:]:
        ax.set_yticklabels([])
    axes[0].text(WALL + 0.8, 46.5, "the wall", ha="left", va="top", color=INK)
    axes[0].text(SCREEN - 1.2, 1.0, "the screen", ha="right", va="bottom", color=INK)
    fig.text(
        0.995,
        0.01,
        "lattice reading (a diagnostic): the level of the light record, darker where larger; "
        "the measurement is the screen's row of Fig. 6",
        ha="right",
        va="bottom",
        color=GREY,
    )
    fig.subplots_adjust(left=0.05, right=0.995, bottom=0.21, top=0.89, wspace=0.08)
    fig.savefig(output)
    fig.savefig(output.with_suffix(".eps"))
    fig.savefig(output.with_suffix(".png"), dpi=150)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--look",
        type=Path,
        default=None,
        help="a look file of the two slits; records its three frames first",
    )
    parser.add_argument("--output", type=Path, default=FIGURES / "two_slits_frames.pdf")
    args = parser.parse_args()
    if args.look is not None:
        record(args.look)
    draw(args.output)


if __name__ == "__main__":
    main()
