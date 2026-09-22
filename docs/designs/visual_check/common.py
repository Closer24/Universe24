"""Shared helpers of the visual check (docs/designs/visual_check/VISUAL.md).

Every figure script of this folder reads a run's record alone (the runner's
`run.json` and `events.jsonl`; the world file beside them) and draws it
headless with matplotlib's Agg backend. Nothing of the law is computed
here: a click is counted, a tick is read, a Node is placed. The only
arithmetic on a physical number is exact (integers and `fractions.Fraction`);
floats appear in the drawing coordinates alone.

Every figure names the kind of what it shows (the model owner, record 281
of docs/LOG_2026-09-20.md): DETECTOR, a detector's click or gather lines;
GAMEBOARD, the host's view of the board (a body's `step` lines), a
diagnostic and never a measurement. A picture is a diagnostic in either
case: it is never compared with nature.

    PYTHONPATH=src .venv/bin/python docs/designs/visual_check/fig_<name>.py RUNS_DIR OUT_DIR

`RUNS_DIR` holds one folder per re-run world, named `<series>__<world>`
(the runner's output folder); `OUT_DIR` receives the PNG and nothing else.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Iterator
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DETECTOR = "DETECTOR"
GAMEBOARD = "GAMEBOARD"
ORDINAL_MASK = 0xFFFFFFFF
# Black and white with one grey, as the paper's figures (the model owner,
# 2026-09-21): series are told apart by fill, marker and line style.
INK, MID, LIGHT, PALE = "#000000", "#808080", "#c8c8c8", "#eeeeee"


def run_folder(runs: Path, series: str, world: str) -> Path:
    folder = runs / f"{series}__{world}"
    if not (folder / "run.json").exists():
        raise SystemExit(f"no run record under {folder}")
    return folder


def run_json(folder: Path) -> dict:
    with (folder / "run.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def events(folder: Path, kinds: set[str] | None = None) -> Iterator[dict]:
    """The lines of `events.jsonl`, in the record's order, filtered by `event`."""
    with (folder / "events.jsonl").open(encoding="utf-8") as lines:
        for line in lines:
            event = json.loads(line)
            if kinds is None or event.get("event") in kinds:
                yield event


def ordinal(record: int) -> int:
    """The birth ordinal of a record (its low 32 bits; the register's tools)."""
    return record & ORDINAL_MASK


def fingerprint(folder: Path) -> str:
    """The run's source fingerprint, the first twelve hex digits of the engine's sha256."""
    return str(run_json(folder)["source_sha256"])[:12]


def cost(folder: Path) -> str:
    record = run_json(folder)
    return f"{record['completed_ticks']} intervals in {record['elapsed_seconds']:.1f} s (host)"


def status_line(folder: Path) -> str:
    record = run_json(folder)
    return (
        f"status {record['status']}, conserved at every completed tick: "
        f"{record['conserved_at_every_completed_tick']}"
    )


def mean(values: list[int]) -> Fraction:
    return Fraction(sum(values), len(values))


def fmt(value: Fraction, digits: int = 4) -> str:
    """A reduced pair printed as a decimal for the caption (the drawing side)."""
    return f"{value.numerator}/{value.denominator} = {float(value):.{digits}f}"


def style(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(MID)
    ax.tick_params(colors=MID, labelcolor=INK)
    ax.grid(axis="y", color=PALE, linewidth=0.6)
    ax.set_axisbelow(True)


def save(fig, out: Path, name: str) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.png"
    fig.savefig(path, dpi=110, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"figure {path}")
    return path


def arguments() -> tuple[Path, Path]:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    return Path(sys.argv[1]), Path(sys.argv[2])
