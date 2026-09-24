"""The two readers of clicks of `examples/events/massive_record/read_runs.py` (the launch list
RUN_LIST.md, the Boss's order of 2026-09-23 23:40Z item (b)): `screen_clicks` (the ray law's
screens, the click count per detector set) and `light_clicks` (a light detector's train, the
sorted click stamps), readers of clicks only, each tested on the tracked run
`EXPLORATORY_chain_screen/` (the first build's chain world of `tests/test_detector_law.py`,
80 Nodes, 900 intervals, run headless by `python -m event_universe`) with the expected counts,
and the edge case: an empty train (an empty events file, or none) reads zero clicks and no
exception."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "examples" / "events" / "massive_record"
TRACKED = SERIES / "EXPLORATORY_chain_screen"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


read_runs = load("massive_record_read_runs", SERIES / "read_runs.py")


def test_screen_clicks_count_the_tracked_chains_screen():
    """The tracked chain run: the lamp at x = 2 births one record per 40 intervals from a stock
    of 6; the screen at x = 70 takes the records that reach it (the take at the Port, one click
    per record at the first rung of its chosen cell); the reader counts the gather lines chosen
    at `screen` and nothing else (a record clicking back at the lamp's body `measured:0` or at
    the face is no screen click). The counts are the tracked file's own, read once and written
    here (DETECTOR): screen 4 of 6 births (two records left by the -x face beside the lamp)."""
    gathers = read_runs.run_lines(TRACKED, "gather")
    assert gathers, "the tracked run carries gather lines"
    counts = read_runs.screen_clicks(TRACKED)
    assert counts == {"screen": 4}
    # every counted click is a gather line chosen at the screen
    chosen = [g for g in gathers if g["chosen"] and g["chosen"][0][0] == "screen"]
    assert len(chosen) == counts["screen"]
    # the other prefix reads nothing (the sets are named)
    assert read_runs.screen_clicks(TRACKED, prefix="no_such_set") == {}


def test_light_clicks_read_the_screens_train_in_order():
    """The light detector's train at the screen: the click stamps sorted, one per record
    ([156, 236, 316, 356]), each 116 intervals after its birth (between 104 and 132, the front
    at L / c over 68 Links; the first build's own bound, test_detector_law.py); the mean
    interval between clicks 200 / 3 over the run (the births at 40, 120, 200 and 240 of the
    lamp's stock; the two born at 80 and 160 left by the -x face) and 80 over the window
    [0, 300] (the first two clicks)."""
    stamps = read_runs.light_clicks(TRACKED, "screen")
    assert stamps == [156, 236, 316, 356]
    births = {g["record"]: g["birth"] for g in read_runs.run_lines(TRACKED, "gather")}
    flights = [
        g["click"] - g["birth"]
        for g in read_runs.run_lines(TRACKED, "gather")
        if g["chosen"] and g["chosen"][0][0] == "screen"
    ]
    assert flights == [116, 116, 116, 116]
    assert births
    assert abs(read_runs.mean_interval(stamps) - 200.0 / 3.0) < 1e-9
    assert read_runs.mean_interval(stamps, (0, 300)) == 80.0
    assert read_runs.mean_interval(stamps, (0, stamps[0])) is None
    assert read_runs.light_clicks(TRACKED, "no_such_set") == []


def test_an_empty_train_reads_zero_clicks_without_exception(tmp_path: Path):
    """The edge case: a run directory with an empty events file, and one with no events file,
    read no click: `screen_clicks` {} and `light_clicks` [] (no exception); a train of births
    without a gather (the records still in flight) reads the same."""
    empty = tmp_path / "empty"
    empty.mkdir()
    (empty / "events.jsonl").write_text("", encoding="utf-8")
    assert read_runs.screen_clicks(empty) == {}
    assert read_runs.light_clicks(empty, "screen") == []
    assert read_runs.mean_interval([]) is None
    missing = tmp_path / "missing"
    assert read_runs.screen_clicks(missing) == {}
    assert read_runs.light_clicks(missing, "screen") == []
    in_flight = tmp_path / "in_flight"
    in_flight.mkdir()
    (in_flight / "events.jsonl").write_text(
        json.dumps({"event": "birth", "tick": 1, "record": 1}) + "\n", encoding="utf-8"
    )
    assert read_runs.screen_clicks(in_flight) == {}
    assert read_runs.light_clicks(in_flight, "screen") == []
