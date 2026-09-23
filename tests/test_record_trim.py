"""The trimmed record (2026-09-23, the host's default): by the model owner's
word (record 1296 of docs/LOG_2026-09-20.md, "if we record the click, we
do not need it for the experiment... only if you need to keep the click,
keep it") the runner leaves the per-row `click` lines of the measured
events out of `events.jsonl` (the lines the measure rule writes per
clicked row, a GameBoard diagnostic that is nearly the whole record of a
long detector run by count and by bytes; the finding on the row 10 runs of
docs/designs/fail_rows) and writes `omit_row_clicks` true into `run.json`;
the option `--keep-row-clicks` (the keyword `keep_row_clicks`) keeps them
and writes no field. Nothing of the law changes and no world key exists:
the record's verbosity is the host's. The expectations of
docs/TEST_EXPECTATIONS.md ("The trimmed record"), written down first, on
the gate world `detector/grouped_12_nodes.json` at its declared 4
intervals (a set of 12 Nodes with a threshold, three rows clicked at the
4th) and the gate's lamp world `bell/a0_b0.json` at its declared 160 (a
lamp and two detector sets: births, records, gathers and per-row clicks
of records):

(a) the default: a run without the option holds no per-row click line (the
    `click` lines whose `measured` is a number and that carry `push`; the
    face clicks, with `measured` None or a body's number and `momentum`,
    the border's, the `gather`, `record` and `birth` lines all written)
    and its `run.json` carries `omit_row_clicks` true; the default of every
    library entry point is off;
(b) the option: run with it, the record holds exactly the lines of the
    default run plus the per-row click lines, byte-identical line for line
    and in order (the default record is a subsequence of the kept one),
    `run.json` carries no `omit_row_clicks` key and every other field but
    `elapsed_seconds` is equal, `state.json` byte-identical;
(c) the series runner: its default child's `run.json` carries the field
    and its `events_sha256` alone differs from the child under
    `--keep-row-clicks`, whose log carries the option;
(d) the gate digests: every gate world that carries `digests` and runs to
    its cap in about a second (the six of `GATE_WORLDS_WITH_DIGESTS`, the
    detector world among them) replays under `--keep-row-clicks` through
    the command line to its three digests of `gate_set.json` byte for
    byte (the gate tests/test_amplitude_click.py replays in-process too);
    the default record's `state_sha256` and `audit_sha256` are the same
    and its `events_sha256` differs exactly when the world clicks a row;
(e) the start-of-run line: `world_needs_row_clicks` is true of a world
    that declares a detector set and false of a world of rays alone;
    `run_initialization` prints `row_clicks_note` to stderr, one line
    naming the world file, `--keep-row-clicks` and the readers, on the
    detector world by default, nothing under the option and nothing on
    the plain world; the parser fills every measured event's table with
    its families' default rules (`read` on a free family, `measure` on a
    paid one), so a world with a measured event and no detector set needs
    the lines as well, and the plain world is one of rays alone;
(f) the readers: `refuse_trimmed_record` stops with a plain sentence naming
    the folder and `--keep-row-clicks` on a trimmed record and does nothing
    on a kept one, on a folder without `run.json` or on a `run.json`
    without the field.
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

from event_universe.events import parse_nature_beam_world
from event_universe.events.engine import NatureBeamSimulation
from event_universe.events.run import execute_nature_beam_run
from event_universe.runner import run_initialization
from event_universe.trimmed_record import (
    KEEP_ROW_CLICKS,
    OMIT_ROW_CLICKS,
    ROW_CLICK_READERS,
    record_omits_row_clicks,
    refuse_trimmed_record,
    row_clicks_note,
    trimmed_record_note,
    world_needs_row_clicks,
)
from event_universe.world_loading import load_world

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events"
GATE_SET = WORLDS / "gate_set.json"
DETECTOR = "detector/grouped_12_nodes.json"
LAMP = "bell/a0_b0.json"
# The gate worlds with `digests` (the worlds without a lamp) whose cap runs
# in about a second; the heavy ones (alpha_square, j3_deuteron, r2) are
# replayed in-process by tests/test_amplitude_click.py.
GATE_WORLDS_WITH_DIGESTS = [
    DETECTOR,
    "coupling/1b_m16.json",
    "weak/j2_ladder.json",
    "weak/j3_deuteron_crowd.json",
    "drive_b/plane_b.json",
    "hubble/pushing_age.json",
]

SPEC = importlib.util.spec_from_file_location("run_series", ROOT / "tools/run_series.py")
RUN_SERIES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN_SERIES)

# A world of rays alone: one family, no measured event, no detector set,
# one ray in flight on a periodic GameBoard (the plain world of (e)).
PLAIN_WORLD = {
    "law": "beam",
    "model_id": "record-trim-plain-world",
    "shape": [4, 4, 4],
    "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
    "ticks": 3,
    "K": 1 << 20,
    "N": 64,
    "release": [0, 1],
    "suspension": 0,
    "age_bound": 16,
    "directions": [[1, 1, 0]],
    "families": [{"name": "light", "quantum": 1, "phase_per_link": 5}],
    "measured": [],
    "in_transit": [
        {
            "position": [0, 0, 0],
            "family": "light",
            "number": 1,
            "direction": [1, 0, 0],
            "amount": 1,
            "phase": 0,
        }
    ],
}


def lines_of(folder: Path) -> list[str]:
    return (folder / "events.jsonl").read_text(encoding="utf-8").splitlines(keepends=True)


def is_row_click(line: str) -> bool:
    """The measure rule's per-row click line of a measured event: `click`,
    `measured` a number (a face's row click has None) and `push` (a face's
    or the border's line carries `momentum`)."""
    event = json.loads(line)
    return event["event"] == "click" and event["measured"] is not None and "push" in event


def kinds_of(lines: list[str]) -> set[str]:
    return {json.loads(line)["event"] for line in lines}


def run_both_ways(tmp_path: Path, world: str) -> tuple[Path, Path]:
    """The world run by default and under the option: (default, kept)."""
    default = tmp_path / "default"
    kept = tmp_path / "kept"
    run_initialization(WORLDS / world, default)
    run_initialization(WORLDS / world, kept, keep_row_clicks=True)
    return default, kept


def digests_of(out: Path) -> dict[str, str]:
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    return {
        "state_sha256": hashlib.sha256((out / "state.json").read_bytes()).hexdigest(),
        "audit_sha256": hashlib.sha256(json.dumps(record["audit"]).encode("utf-8")).hexdigest(),
        "events_sha256": hashlib.sha256((out / "events.jsonl").read_bytes()).hexdigest(),
    }


def gate_entry(world: str) -> dict[str, object]:
    document = json.loads(GATE_SET.read_text(encoding="utf-8"))
    return next(entry for entry in document["worlds"] if entry["path"] == world)


def run_command_line(world: str, out: Path, *options: str) -> subprocess.CompletedProcess[str]:
    """`python -m event_universe` on the world at its gate cap."""
    command = [sys.executable, "-m", "event_universe", "--init", str(WORLDS / world)]
    command += ["--output", str(out), "--ticks", str(int(gate_entry(world)["cap"])), *options]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join([str(ROOT / "src"), environment.get("PYTHONPATH", "")])
    return subprocess.run(command, check=True, env=environment, capture_output=True, text=True)


@pytest.mark.parametrize("world", [DETECTOR, LAMP])
def test_the_default_leaves_out_the_per_row_click_lines_and_marks_the_record(tmp_path: Path, world: str):
    """(a)."""
    default, kept = run_both_ways(tmp_path, world)
    default_lines = lines_of(default)
    assert any(is_row_click(line) for line in lines_of(kept)), world  # the world clicks rows
    assert not any(is_row_click(line) for line in default_lines)
    # Every other kind is still written: the detector's own reading.
    assert "record" in kinds_of(default_lines)
    if world == LAMP:
        assert {"birth", "gather", "record"} <= kinds_of(default_lines)
    record = json.loads((default / "run.json").read_text(encoding="utf-8"))
    assert record[OMIT_ROW_CLICKS] is True
    assert record_omits_row_clicks(default)


def test_the_default_of_every_entry_point_is_off():
    """(a): the library entry points and the series runner."""
    assert run_initialization.__kwdefaults__["keep_row_clicks"] is False
    assert execute_nature_beam_run.__kwdefaults__["keep_row_clicks"] is False
    assert NatureBeamSimulation.__init__.__kwdefaults__["keep_row_clicks"] is False
    assert RUN_SERIES.run_series.__kwdefaults__["keep_row_clicks"] is False
    assert RUN_SERIES.run_one.__kwdefaults__["keep_row_clicks"] is False


@pytest.mark.parametrize("world", [DETECTOR, LAMP])
def test_the_option_keeps_exactly_the_per_row_click_lines(tmp_path: Path, world: str):
    """(b)."""
    default, kept = run_both_ways(tmp_path, world)
    default_lines, kept_lines = lines_of(default), lines_of(kept)
    row_clicks = [line for line in kept_lines if is_row_click(line)]
    others = [line for line in kept_lines if not is_row_click(line)]
    assert row_clicks, world
    # The default record is the kept one without its per-row click lines,
    # byte-identical line for line and in order.
    assert default_lines == others
    if world == LAMP:
        # The gathers, the detector's clicks of the records, written either way.
        gathers = [line for line in kept_lines if json.loads(line)["event"] == "gather"]
        assert gathers
        assert [line for line in default_lines if json.loads(line)["event"] == "gather"] == gathers
    # The metadata: the field on the default record alone, everything else
    # equal but the clock.
    default_record = json.loads((default / "run.json").read_text(encoding="utf-8"))
    kept_record = json.loads((kept / "run.json").read_text(encoding="utf-8"))
    assert OMIT_ROW_CLICKS not in kept_record
    assert default_record.pop(OMIT_ROW_CLICKS) is True
    for record in (default_record, kept_record):
        del record["elapsed_seconds"]
    assert kept_record == default_record
    assert (default / "state.json").read_bytes() == (kept / "state.json").read_bytes()
    assert not record_omits_row_clicks(kept)


def test_the_in_process_observer_is_whole_under_the_option_and_trimmed_by_default():
    """(a), (b): `NatureBeamSimulation(world, observer, keep_row_clicks=True)`."""
    path = WORLDS / DETECTOR
    world = load_world(path.read_bytes(), base_dir=path.parent).world
    trimmed: list[dict[str, object]] = []
    whole: list[dict[str, object]] = []
    for lines, keep in ((trimmed, False), (whole, True)):
        simulation = NatureBeamSimulation(world, observer=lines.append, keep_row_clicks=keep)
        for _ in range(world.ticks):
            simulation.step()
    row_clicks = [
        e for e in whole if e["event"] == "click" and e["measured"] is not None and "push" in e
    ]
    assert row_clicks
    assert trimmed == [e for e in whole if e not in row_clicks]


def test_the_series_runner_passes_the_option_to_its_child(tmp_path: Path):
    """(c): `tools/run_series.py --keep-row-clicks`."""
    default = RUN_SERIES.run_series(
        [WORLDS / DETECTOR], tmp_path / "default", jobs=1, python=sys.executable
    )
    assert default[0]["status"] == "completed"
    default_run = tmp_path / "default" / "grouped_12_nodes" / "run"
    assert json.loads((default_run / "run.json").read_text(encoding="utf-8"))[OMIT_ROW_CLICKS] is True
    default_log = (tmp_path / "default" / "grouped_12_nodes" / "log.txt").read_text().splitlines()
    assert KEEP_ROW_CLICKS not in default_log[0]  # the command
    assert row_clicks_note(WORLDS / DETECTOR) in default_log  # the child's start-of-run line
    assert not any(is_row_click(line) for line in lines_of(default_run))
    kept = RUN_SERIES.run_series(
        [WORLDS / DETECTOR], tmp_path / "kept", jobs=1, python=sys.executable, keep_row_clicks=True
    )
    assert kept[0]["status"] == "completed"
    kept_run = tmp_path / "kept" / "grouped_12_nodes" / "run"
    assert OMIT_ROW_CLICKS not in json.loads((kept_run / "run.json").read_text(encoding="utf-8"))
    kept_log = (tmp_path / "kept" / "grouped_12_nodes" / "log.txt").read_text().splitlines()
    assert KEEP_ROW_CLICKS in kept_log[0] and row_clicks_note(WORLDS / DETECTOR) not in kept_log
    assert any(is_row_click(line) for line in lines_of(kept_run))
    assert default[0]["events_sha256"] != kept[0]["events_sha256"]
    assert default[0]["state_sha256"] == kept[0]["state_sha256"]
    assert default[0]["audit_sha256"] == kept[0]["audit_sha256"]


@pytest.mark.parametrize("world", GATE_WORLDS_WITH_DIGESTS)
def test_the_gate_digests_replay_under_the_option_through_the_command_line(tmp_path: Path, world: str):
    """(d)."""
    registered = gate_entry(world)["digests"]
    kept = run_command_line(world, tmp_path / "kept", KEEP_ROW_CLICKS)
    assert kept.stderr == ""
    record = json.loads((tmp_path / "kept" / "run.json").read_text(encoding="utf-8"))
    assert OMIT_ROW_CLICKS not in record
    assert digests_of(tmp_path / "kept") == registered
    # The default record: the state and the books the same, the events
    # differing by the omitted lines alone (none where no row clicks).
    default = run_command_line(world, tmp_path / "default")
    assert default.stderr.rstrip("\n") == row_clicks_note(WORLDS / world)
    assert json.loads((tmp_path / "default" / "run.json").read_text(encoding="utf-8"))[OMIT_ROW_CLICKS]
    found = digests_of(tmp_path / "default")
    assert found["state_sha256"] == registered["state_sha256"]
    assert found["audit_sha256"] == registered["audit_sha256"]
    clicks_a_row = any(is_row_click(line) for line in lines_of(tmp_path / "kept"))
    assert clicks_a_row == (world == DETECTOR)
    assert (found["events_sha256"] != registered["events_sha256"]) == clicks_a_row


def test_the_start_of_run_line_names_the_option_and_the_readers(tmp_path: Path, capsys):
    """(e)."""
    detector = load_world((WORLDS / DETECTOR).read_bytes(), base_dir=WORLDS / "detector").world
    assert detector.detectors and world_needs_row_clicks(detector)
    plain_path = tmp_path / "plain.json"
    plain_path.write_text(json.dumps(PLAIN_WORLD), encoding="utf-8")
    plain = parse_nature_beam_world(PLAIN_WORLD)
    assert not plain.detectors and not plain.measured and not world_needs_row_clicks(plain)
    # A measured event without a table or a detector set: the parser's
    # default rules (`measure` on a paid family) make it need the lines.
    with_event = dict(PLAIN_WORLD)
    with_event["families"] = [{"name": "atom", "quantum": 1, "phase_per_link": 5}]
    with_event["in_transit"] = []
    with_event["measured"] = [{"position": [1, 1, 1], "family": "atom", "amount": 1, "phase": 0}]
    parsed = parse_nature_beam_world(with_event)
    assert parsed.measured[0].table == ("measure",) and world_needs_row_clicks(parsed)
    # The line on stderr: the detector world by default, once.
    run_initialization(WORLDS / DETECTOR, tmp_path / "default")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == row_clicks_note(WORLDS / DETECTOR) + "\n"
    note = captured.err
    assert note.count("\n") == 1
    assert str(WORLDS / DETECTOR) in note and KEEP_ROW_CLICKS in note and ROW_CLICK_READERS in note
    assert "hubble.py" in note and "weak.py" in note and OMIT_ROW_CLICKS in note
    # Nothing under the option, nothing on the plain world (its record has
    # no per-row click line to leave out, and is marked as any default one).
    run_initialization(WORLDS / DETECTOR, tmp_path / "kept", keep_row_clicks=True)
    assert capsys.readouterr().err == ""
    run_initialization(plain_path, tmp_path / "plain")
    assert capsys.readouterr().err == ""
    assert "click" not in kinds_of(lines_of(tmp_path / "plain"))
    assert record_omits_row_clicks(tmp_path / "plain")


def test_a_reader_of_row_clicks_refuses_a_trimmed_record_plainly(tmp_path: Path):
    """(f)."""
    default, kept = run_both_ways(tmp_path, DETECTOR)
    refuse_trimmed_record(kept)  # nothing
    refuse_trimmed_record(tmp_path / "absent")  # no run.json: nothing here
    with pytest.raises(SystemExit) as stop:
        refuse_trimmed_record(default)
    note = str(stop.value)
    assert note == trimmed_record_note(default)
    assert str(default) in note and OMIT_ROW_CLICKS in note and KEEP_ROW_CLICKS in note
    assert "trimmed record" in note and "gather" in note and "--omit-row-clicks" not in note
    # A record without the field (older than the option, written whole), or
    # with it false, is read as a kept record.
    other = tmp_path / "other"
    other.mkdir()
    (other / "run.json").write_text(json.dumps({"status": "completed"}), encoding="utf-8")
    assert not record_omits_row_clicks(other)
    (other / "run.json").write_text(json.dumps({OMIT_ROW_CLICKS: False}), encoding="utf-8")
    assert not record_omits_row_clicks(other)
    (other / "run.json").write_text("{", encoding="utf-8")
    assert not record_omits_row_clicks(other)
