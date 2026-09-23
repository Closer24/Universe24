"""The trimmed record: a run written without the runner's `--keep-row-clicks`.

A run's `events.jsonl` holds one line per event. In a long run of a
detector world the per-row `click` lines of the measured events (one per
clicked row, written by the measure rule) are nearly the whole record by
count and by bytes; the detector's reading of those rows is the set's
`record` line per interval and, in a recorded world, the `gather` line per
record, and the per-row lines are a GameBoard diagnostic (docs/ENGINE.md,
the record; the finding of 2026-09-23 on the row 10 runs). By the model
owner's word of 2026-09-23 (record 1296 of docs/LOG_2026-09-20.md: "if we
record the click, we do not need it for the experiment... only if you need
to keep the click, keep it") the runner leaves those lines out by default
and writes `omit_row_clicks` true into `run.json`; the option
`--keep-row-clicks` writes them and no such field, the record as it was
before the option, byte for byte. Every other line is written either way.

A reading tool that reads the per-row click lines calls
`refuse_trimmed_record(run)` before it opens `events.jsonl`, so that on a
trimmed record it says so plainly instead of reading zero clicks; a record
older than the field, written whole, is read as before. The readers of the
`record` and `gather` lines need nothing. At the start of a default run of
a world whose rows can click (`world_needs_row_clicks`) the runner prints
`row_clicks_note` to stderr, one line naming the option and the readers
that need the lines, and runs on.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from event_universe.events.world import NatureBeamWorld

# The field of `run.json` the runner writes, true on every record written
# without the per-row click lines (the default) and absent under the option.
OMIT_ROW_CLICKS = "omit_row_clicks"

# The option that keeps the lines, on `python -m event_universe` and
# `tools/run_series.py` (the keyword `keep_row_clicks` on
# `run_initialization`, `execute_nature_beam_run` and `NatureBeamSimulation`).
KEEP_ROW_CLICKS = "--keep-row-clicks"

# The readers of the per-row click lines, the ones that call
# `refuse_trimmed_record`; named in the runner's start-of-run line.
ROW_CLICK_READERS = (
    "tools/click_readings/bell.py, bell_choosers.py, c_measured.py, flow_link.py, hubble.py, "
    "hubble_stars.py, lensing.py, orbit_lamp.py and weak.py, tools/amplitude_path.py, "
    "tools/amplitude_probe.py, tools/moving_detector_readings.py, "
    "tools/newton_side_readings.py and the reading scripts of docs/designs"
)

# The table entries at which a row of a measured event ends and the measure
# rule writes a per-row click line: the click (`measure`), the reading of
# the push (`read`) and the pass through (`pass`).
ROW_CLICK_RULES = frozenset({"measure", "read", "pass"})


def record_omits_row_clicks(run: Path) -> bool:
    """Whether the run in the folder `run` was written without the per-row
    click lines: its `run.json` carries `omit_row_clicks` true. False for a
    record without the field (every run before the option, written whole,
    and every run under `--keep-row-clicks`) and for a folder without a
    `run.json` (the reader's own refusal follows)."""
    path = run / "run.json"
    if not path.is_file():
        return False
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return False
    return isinstance(record, dict) and record.get(OMIT_ROW_CLICKS) is True


def trimmed_record_note(run: Path) -> str:
    """The plain sentence a reader of per-row click lines prints on a trimmed
    record."""
    return (
        f"{run}: a trimmed record: its run.json carries omit_row_clicks true (the runner's "
        "default), so its events.jsonl holds no per-row click line of a measured event; this "
        "reading needs those lines and has nothing to read. Run the world again with "
        f"{KEEP_ROW_CLICKS}, or read the record and gather lines instead."
    )


def refuse_trimmed_record(run: Path) -> None:
    """Stop with the note when the run's record is trimmed; nothing otherwise.
    A reader of per-row click lines calls it before opening `events.jsonl`."""
    if record_omits_row_clicks(run):
        raise SystemExit(trimmed_record_note(run))


def world_needs_row_clicks(world: NatureBeamWorld) -> bool:
    """Whether a run of `world` can write a per-row click line: it declares
    a detector set, or a measured event with a `measure`, `read` or `pass`
    entry or a window (declared or read from a reading). The parser fills
    every measured event's table with its families' default rules
    (`world.default_table`: `read` on a free family, `measure` on a paid
    one), so every world with a measured event is such a world; a world
    without one (rays alone) is not."""
    if world.detectors:
        return True
    for measured in world.measured:
        if any(rule in ROW_CLICK_RULES for rule in measured.table):
            return True
        if any(window is not None for window in measured.windows):
            return True
        if any(read is not None for read in measured.window_reads):
            return True
    return False


def row_clicks_note(initialization: Path) -> str:
    """The one line the runner prints to stderr at the start of a default run
    of a world whose rows can click (`world_needs_row_clicks`): the record
    is written without the per-row click lines, the option keeps them, and
    the readers that need them are named. The run goes on."""
    return (
        f"{initialization}: the per-row click lines of the measured events are left out of "
        f"events.jsonl (run.json omit_row_clicks true); {KEEP_ROW_CLICKS} keeps them for the "
        f"readers that need them ({ROW_CLICK_READERS})."
    )
