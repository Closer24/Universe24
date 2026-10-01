"""Two figures of the paper drawn from the definitions, by no run of the engine.

The band: light's rotation along one axis at a content x read into the paces,
2 cos omega = 2 - 2 (1 - 2 x)^2 (1 - cos k) (docs/ALGEBRA.md, the clock once and
the Link twice, at num = den), at three contents; the band's bottom rises with
the content and its top stays at 2, and the slope at k = 0 is light's speed
(1 - 2 x) / sqrt 3 Links per interval.

The channels: the three ways one family acts on another (docs/ALGEBRA.md, the
interval; docs/HIGHLIGHTS.md, the coupling is the click alone): the read at act
(i), the write at act (iv) and the click at act (iii), the detector's reading of the
record's current through its boundary, each one line of the law.

    python paper/general_formula/band_and_channels.py --output paper/general_formula/figures

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
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)  # the journal's lettering: 8 pt at the final size, each figure drawn 1:1, fonts embedded
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
# Black and white only.
INK, DARK, MID, LIGHT = "#000000", "#404040", "#808080", "#c8c8c8"


def save(fig: Figure, path: Path) -> None:
    """The PDF the paper includes and the EPS a journal asks for, side by side."""
    fig.savefig(path)
    fig.savefig(path.with_suffix(".eps"))


def band(output: Path) -> None:
    """Light's band at three contents, the doubled cosine against the wave number."""
    fig, ax = plt.subplots(figsize=(3.6, 2.4))
    steps = 400
    wave_numbers = [math.pi * i / steps for i in range(steps + 1)]
    for content, style in ((0.0, "-"), (0.1, "--"), (0.25, ":")):
        pace = (1 - 2 * content) ** 2
        doubled = [2 - 2 * pace * (1 - math.cos(k)) for k in wave_numbers]
        ax.plot(wave_numbers, doubled, style, color=INK, linewidth=1.0, label=f"$x = {content}$")
    ax.axhline(2, color=LIGHT, linewidth=0.6)
    ax.axhline(-2, color=LIGHT, linewidth=0.6)
    ax.set_xlim(0, math.pi)
    ax.set_ylim(-2.3, 2.3)
    ax.set_xticks([0, math.pi / 4, math.pi / 2, 3 * math.pi / 4, math.pi])
    ax.set_xticklabels(["$0$", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])
    ax.set_xlabel("wave number $k$ per Link")
    ax.set_ylabel(r"$2\cos\omega$")
    ax.legend(frameon=False, loc="lower left")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    save(fig, output / "band.pdf")
    plt.close(fig)


def box(ax: Axes, x: float, y: float, w: float, h: float, text: str, fill: str = "white") -> None:
    """A rounded box with its label."""
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.02", linewidth=0.8, edgecolor=INK, facecolor=fill
        )
    )
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center")


def arrow(
    ax: Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    style: str = "-",
    rad: float = 0.0,
    width: float = 1.0,
) -> None:
    """One channel's arrow."""
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=9,
        linewidth=width,
        linestyle=style,
        color=INK,
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(patch)


def label(ax: Axes, x: float, y: float, text: str, ha: str = "center") -> None:
    """A channel's line, on white so that it reads over the arrows."""
    ax.text(
        x,
        y,
        text,
        ha=ha,
        va="center",
        color=DARK,
        bbox={"boxstyle": "square,pad=0.1", "facecolor": "white", "edgecolor": "none"},
    )


def channels(output: Path) -> None:
    """The three channels: the read, the write and the click."""
    fig, ax = plt.subplots(figsize=(4.69, 3.1))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    # The lane of a family of quanta: its record, its bookings and what a detector sees.
    box(ax, 0.1, 4.4, 3.0, 1.0, "the record\n(now, before), (re, im)")
    box(ax, 3.5, 4.4, 3.0, 1.0, "the bookings\n$D$, $W$, $F$, $T_{aa}$")
    box(ax, 6.9, 4.4, 3.0, 1.0, "the current $F$ through\na region's boundary")
    # The lane of a held family, and the Outside.
    box(ax, 3.5, 0.6, 3.0, 1.0, "the held level\n(time part, tensions)", fill="#f2f2f2")
    box(ax, 6.9, 0.6, 3.0, 1.0, "a declared detector,\na region of Nodes", fill="#f2f2f2")
    # Rule3 steps the record; the bookings read it.
    arrow(ax, (0.55, 6.35), (0.55, 5.45))
    label(ax, 0.75, 6.0, "Rule3, act (ii)", ha="left")
    arrow(ax, (3.1, 4.9), (3.5, 4.9))
    label(ax, 3.3, 5.75, "read, no write")
    arrow(ax, (6.5, 4.9), (6.9, 4.9))
    label(ax, 6.7, 5.75, "summed over the passage")
    # The read: the held level into the record's paces.
    arrow(ax, (3.5, 1.1), (2.7, 4.4), rad=-0.2)
    label(
        ax,
        0.1,
        2.7,
        "the read (i):\nthe level into\nthe paces, the clock\nonce, the Link twice",
        ha="left",
    )
    # The write: the bookings into the held level.
    arrow(ax, (5.0, 4.4), (5.0, 1.6), style="--")
    label(
        ax, 5.0, 3.0, "the write (iv),\none per held part:\n$(\\sum_f w_f q_f + r)\\ \\mathrm{div}\\ E$"
    )
    # The click: the detector's reading, one quantum per wall of inflow, credited.
    arrow(ax, (8.4, 4.4), (8.4, 1.6), width=1.8)
    label(ax, 8.4, 3.0, "the click (iii):\none quantum per $W_c$\nof inflow, credited\nby the shares")
    ax.text(0.1, 4.05, "a family of quanta", color=MID, style="italic")
    ax.text(0.1, 0.25, "a held family, and the Outside", color=MID, style="italic")
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    save(fig, output / "channels.pdf")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=HERE / "figures")
    arguments = parser.parse_args()
    arguments.output.mkdir(parents=True, exist_ok=True)
    band(arguments.output)
    channels(arguments.output)


if __name__ == "__main__":
    main()
