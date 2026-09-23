"""The trimmed record: a run written under the runner's `--omit-row-clicks`.

A run's `events.jsonl` holds one line per event. In a long run of a
detector world the per-row `click` lines of the measured events (one per
clicked row, written by the measure rule) are nearly the whole record by
count and by bytes; the detector's reading of those rows is the set's
`record` line per interval and, in a recorded world, the `gather` line per
record, and the per-row lines are a GameBoard diagnostic (docs/ENGINE.md,
the record; the finding of 2026-09-23 on the row 10 runs). The runner's
option `--omit-row-clicks` (off by default) leaves those lines out and
writes `omit_row_clicks` true into `run.json`; every other line, and every
file of a run without the option, is byte for byte as it was.

A reading tool that reads the per-row click lines calls
`refuse_trimmed_record(run)` before it opens `events.jsonl`, so that on a
trimmed record it says so plainly instead of reading zero clicks. The
readers of the `record` and `gather` lines need nothing.
"""

from __future__ import annotations

import json
from pathlib import Path

# The field of `run.json` the runner writes, true only under the option.
OMIT_ROW_CLICKS = "omit_row_clicks"


def record_omits_row_clicks(run: Path) -> bool:
    """Whether the run in the folder `run` was written under
    `--omit-row-clicks`: its `run.json` carries `omit_row_clicks` true. False
    for a record without the field (every run before the option, and every
    run without it) and for a folder without a `run.json` (the reader's own
    refusal follows)."""
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
        "--omit-row-clicks), so its events.jsonl holds no per-row click line of a measured "
        "event; this reading needs those lines and has nothing to read. Run the world again "
        "without --omit-row-clicks, or read the record and gather lines instead."
    )


def refuse_trimmed_record(run: Path) -> None:
    """Stop with the note when the run's record is trimmed; nothing otherwise.
    A reader of per-row click lines calls it before opening `events.jsonl`."""
    if record_omits_row_clicks(run):
        raise SystemExit(trimmed_record_note(run))
