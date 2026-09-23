"""The trimmed record (2026-09-23, a host option): the runner's
`--omit-row-clicks`, off by default, leaves the per-row `click` lines of the
measured events out of `events.jsonl` (the lines the measure rule writes per
clicked row, a GameBoard diagnostic that is nearly the whole record of a long
detector run by count and by bytes; the finding on the row 10 runs of
docs/designs/fail_rows) and writes `omit_row_clicks` true into `run.json`.
Nothing of the law changes and no world key exists: the record's verbosity
is the host's. The expectations of docs/TEST_EXPECTATIONS.md ("The trimmed
record"), written down first:

(a) the option on: a small registered world run twice, with and without it,
    on the gate world `detector/grouped_12_nodes.json` at its declared 4
    intervals (a set of 12 Nodes with a threshold, three rows clicked at the
    4th) and on the catalog world `lamp_mirror_screen.json` at its declared
    50 intervals (a lamp, two mirrors that re-release and a screen: records,
    gathers and per-row clicks of records); the kept lines are byte-identical
    line for line and in order (the trimmed record is a subsequence of the
    full one), the omitted lines are exactly the `click` lines whose
    `measured` is a number and that carry `push` (the measure rule's per-row
    lines; the face clicks, with `measured` None or a body's number and
    `momentum`, the border's, the `gather`, `record`, `birth`, `split`,
    `cancel`, `read`, `pass`, `rerelease`, `step`, `home` and `become`
    lines all kept), `run.json` carries `omit_row_clicks` true and every
    other field of `run.json` but `elapsed_seconds` equal, `state.json`
    byte-identical; the series runner passes the option to its child and
    the child's `run.json` carries it;
(b) the default off: `run.json` carries no `omit_row_clicks` key and the
    record of `detector/grouped_12_nodes.json` at its cap replays to the
    three digests pinned in `gate_set.json` byte for byte (the gate the
    other digest tests replay too);
(c) the readers: `refuse_trimmed_record` stops with a plain sentence naming
    the folder on a trimmed record and does nothing on a full one, on a
    folder without `run.json` or on a `run.json` without the field.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from event_universe.events.run import execute_nature_beam_run
from event_universe.runner import run_initialization
from event_universe.trimmed_record import (
    OMIT_ROW_CLICKS,
    record_omits_row_clicks,
    refuse_trimmed_record,
    trimmed_record_note,
)

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events"
GATE_SET = WORLDS / "gate_set.json"
DETECTOR = "detector/grouped_12_nodes.json"
LAMP = "catalog/lamp_mirror_screen.json"

SPEC = importlib.util.spec_from_file_location("run_series", ROOT / "tools/run_series.py")
RUN_SERIES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN_SERIES)


def lines_of(folder: Path) -> list[str]:
    return (folder / "events.jsonl").read_text(encoding="utf-8").splitlines(keepends=True)


def is_row_click(line: str) -> bool:
    """The measure rule's per-row click line of a measured event: `click`,
    `measured` a number (a face's row click has None) and `push` (a face's
    or the border's line carries `momentum`)."""
    event = json.loads(line)
    return event["event"] == "click" and event["measured"] is not None and "push" in event


def run_twice(tmp_path: Path, world: str) -> tuple[Path, Path]:
    full = tmp_path / "full"
    trimmed = tmp_path / "trimmed"
    run_initialization(WORLDS / world, full)
    run_initialization(WORLDS / world, trimmed, omit_row_clicks=True)
    return full, trimmed


@pytest.mark.parametrize("world", [DETECTOR, LAMP])
def test_the_option_omits_exactly_the_per_row_click_lines(tmp_path: Path, world: str):
    """(a)."""
    full, trimmed = run_twice(tmp_path, world)
    full_lines, trimmed_lines = lines_of(full), lines_of(trimmed)
    omitted = [line for line in full_lines if is_row_click(line)]
    kept = [line for line in full_lines if not is_row_click(line)]
    assert omitted, world  # the world clicks rows at a measured event
    # The kept lines byte-identical, line for line and in order.
    assert trimmed_lines == kept
    assert not any(is_row_click(line) for line in trimmed_lines)
    # Every kind but the per-row click is still there.
    kinds = {json.loads(line)["event"] for line in trimmed_lines}
    assert "record" in kinds and "click" in {json.loads(line)["event"] for line in full_lines}
    if world == LAMP:
        assert {"birth", "gather", "record", "rerelease"} <= kinds
        # The gathers, the detector's clicks of the records, all kept.
        gathers = [line for line in full_lines if json.loads(line)["event"] == "gather"]
        assert (
            gathers
            and [line for line in trimmed_lines if json.loads(line)["event"] == "gather"] == gathers
        )
    # The metadata: the field set, everything else equal but the clock.
    full_record = json.loads((full / "run.json").read_text(encoding="utf-8"))
    trimmed_record = json.loads((trimmed / "run.json").read_text(encoding="utf-8"))
    assert trimmed_record[OMIT_ROW_CLICKS] is True
    assert OMIT_ROW_CLICKS not in full_record
    del trimmed_record[OMIT_ROW_CLICKS]
    for record in (full_record, trimmed_record):
        del record["elapsed_seconds"]
    assert trimmed_record == full_record
    assert (full / "state.json").read_bytes() == (trimmed / "state.json").read_bytes()
    assert record_omits_row_clicks(trimmed) and not record_omits_row_clicks(full)


def test_the_series_runner_passes_the_option_to_its_child(tmp_path: Path):
    """(a): `tools/run_series.py --omit-row-clicks`."""
    rows = RUN_SERIES.run_series(
        [WORLDS / DETECTOR], tmp_path / "series", jobs=1, python=sys.executable, omit_row_clicks=True
    )
    assert rows[0]["status"] == "completed"
    run = tmp_path / "series" / "grouped_12_nodes" / "run"
    assert json.loads((run / "run.json").read_text(encoding="utf-8"))[OMIT_ROW_CLICKS] is True
    assert "--omit-row-clicks" in (tmp_path / "series" / "grouped_12_nodes" / "log.txt").read_text()
    assert not any(is_row_click(line) for line in lines_of(run))
    plain = RUN_SERIES.run_series([WORLDS / DETECTOR], tmp_path / "plain", jobs=1, python=sys.executable)
    assert plain[0]["events_sha256"] != rows[0]["events_sha256"]
    assert plain[0]["state_sha256"] == rows[0]["state_sha256"]
    assert plain[0]["audit_sha256"] == rows[0]["audit_sha256"]


def test_the_default_is_off_and_the_record_replays_to_its_pinned_digests(tmp_path: Path):
    """(b)."""
    entry = next(
        e for e in json.loads(GATE_SET.read_text(encoding="utf-8"))["worlds"] if e["path"] == DETECTOR
    )
    out = tmp_path / "run"
    # Through the command line without the flag: the default.
    command = [sys.executable, "-m", "event_universe", "--init", str(WORLDS / DETECTOR)]
    command += ["--output", str(out), "--ticks", str(int(entry["cap"]))]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join([str(ROOT / "src"), environment.get("PYTHONPATH", "")])
    subprocess.run(command, check=True, env=environment, capture_output=True)
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert OMIT_ROW_CLICKS not in record
    digests = entry["digests"]
    assert hashlib.sha256((out / "state.json").read_bytes()).hexdigest() == digests["state_sha256"]
    assert (
        hashlib.sha256(json.dumps(record["audit"]).encode("utf-8")).hexdigest()
        == digests["audit_sha256"]
    )
    assert hashlib.sha256((out / "events.jsonl").read_bytes()).hexdigest() == digests["events_sha256"]
    # The library entry points too: the option's default is off.
    assert run_initialization.__kwdefaults__["omit_row_clicks"] is False
    assert execute_nature_beam_run.__kwdefaults__["omit_row_clicks"] is False
    assert RUN_SERIES.run_series.__kwdefaults__["omit_row_clicks"] is False


def test_a_reader_of_row_clicks_refuses_a_trimmed_record_plainly(tmp_path: Path):
    """(c)."""
    full, trimmed = run_twice(tmp_path, DETECTOR)
    refuse_trimmed_record(full)  # nothing
    refuse_trimmed_record(tmp_path / "absent")  # no run.json: nothing here
    with pytest.raises(SystemExit) as stop:
        refuse_trimmed_record(trimmed)
    note = str(stop.value)
    assert note == trimmed_record_note(trimmed)
    assert str(trimmed) in note and "omit_row_clicks" in note and "--omit-row-clicks" in note
    assert "trimmed record" in note and "gather" in note
    # A record without the field, or with it false, is a full record.
    other = tmp_path / "other"
    other.mkdir()
    (other / "run.json").write_text(json.dumps({"omit_row_clicks": False}), encoding="utf-8")
    assert not record_omits_row_clicks(other)
    (other / "run.json").write_text("{", encoding="utf-8")
    assert not record_omits_row_clicks(other)
