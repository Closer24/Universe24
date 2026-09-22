"""The nucleus readings tool reads the runner's record and nothing else
(the experimenter's rule, 2026-09-20: a readings tool never replays a rule
of the engine; `tools/nucleus_readings.py` reads the bodies' `read`,
`contact`, `step` and `click` records off `events.jsonl` and the run off
`run.json`). One fast case pins the tool to the engine's record: the
design's pair on the six headings (`tests/test_contact.py` (a); the
physicist's DESIGN.md test (f)), two protons of `p` (amount 4, charge 3)
holding one unit of `g` (strong 11 with the sign minus, lifetime 3) at one
Link on an open 9^3 GameBoard, `release` [1, 1], `width` 1, 12 intervals,
the model `beam-nucleus-pair-space-v1`, run through the runner. The
expected integers, written down first: the push per interval at the
reference tick 20 is not read (the run is shorter), so the tool's
reference is moved to tick 3 for the test: body 1 reads (128, 0, 0), the
`p` rows (-7936, 0, 0) and the `g` rows (8064, 0, 0), body 2 the mirror;
the hand-overs of body 1 at ticks 3 (256), 4 (128) and 9 (640), three in
all, the first at tick 3, the largest 640, the label 0 after each; body 2
none; no step; the border `lifetime` clicking 12 rows per interval from
tick 4 (6 per body); the pair's separation 1.00 throughout (the
hand-overs since the step drive and the crossing rule are the ones
`test_contact.py` (a) pins, cited at the assertion); the run
completed and balanced over 12 ticks; the `g` reads per body 11 (one per
interval from tick 2); the criteria of a world outside the register's
eight are none.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.events import parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "nucleus_readings_tool", ROOT / "tools" / "nucleus_readings.py"
)
TOOL = importlib.util.module_from_spec(SPEC)
sys.modules["nucleus_readings_tool"] = TOOL
SPEC.loader.exec_module(TOOL)


def test_read_run_reads_the_runners_record(tmp_path, monkeypatch):
    document = {
        "law": "beam",
        "model_id": "beam-nucleus-pair-space-v1",
        "shape": [9, 9, 9],
        "boundary": "open",
        "ticks": 12,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "width": 1,
        "families": [
            {"name": "p", "quantum": 0, "phase": False, "charge": 3},
            {
                "name": "g",
                "quantum": 0,
                "phase": False,
                "columns": {"strong": {"value": 11, "sign": -1}},
                "lifetime": 3,
            },
        ],
        "measured": [
            {"position": [3, 4, 4], "family": "p", "amount": 4, "held": {"g": 1}},
            {"position": [4, 4, 4], "family": "p", "amount": 4, "held": {"g": 1}},
        ],
    }
    folder = tmp_path / "pair"
    folder.mkdir()
    execute_nature_beam_run(
        parse_nature_beam_world(document), json.dumps(document).encode("utf-8"), folder, "test", 12
    )
    monkeypatch.setattr(TOOL, "REFERENCE_TICK", 3)
    reading = TOOL.read_run(folder)
    assert reading.name == "pair" and reading.strong == 11 and reading.lifetime == 3
    assert reading.completed and reading.balanced and reading.ticks == 12
    first, second = reading.bodies
    assert (first.family, first.start, first.kick) == ("p", (3, 4, 4), (0, 0, 0))
    assert first.push == (128, 0, 0) and second.push == (-128, 0, 0)
    assert first.push_by_family == {"p": (-7936, 0, 0), "g": (8064, 0, 0)}
    # Since the crossing rule (2026-09-21, the step before the law): p1
    # hands at ticks 5 (384), 8 (256) and 11 (128), p2 back at 6 (-128) and
    # 10 (-256); test_contact (a) derives them (under the step drive of
    # 2026-09-20 one interval earlier, 4, 7, 10 and 5, 9; the rule as it
    # was: 3, 3, 640 and p2 never handing).
    assert (first.contacts, first.first_contact, first.largest_handed, first.handed_to_zero) == (
        3,
        5,
        384,
        True,
    )
    assert (second.contacts, second.first_contact, second.largest_handed, second.handed_to_zero) == (
        2,
        6,
        256,
        True,
    )
    assert first.steps == 0 and second.steps == 0
    assert first.strong_reads == 11 and second.strong_reads == 11
    assert min(reading.lifetime_clicks) == 4 and reading.lifetime_clicks[4] == 12
    assert first.cumulative[:4] == [(0, 0, 0), (128, 0, 0), (256, 0, 0), (384, 0, 0)]
    assert first.kicked_back_at is None
    assert TOOL.separation_summary(reading, 1, 2) == (1.0, 1.0, 1.0, False)
    assert TOOL.expectations(reading) == []
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    handed = [e for e in events if e["event"] == "contact"]
    assert [(e["tick"], e["component"]) for e in handed] == [
        (5, 384),
        (6, -128),
        (8, 256),
        (10, -256),
        (11, 128),
    ]
    border = [e for e in events if e["event"] == "click" and e["detector"] == "lifetime"]
    assert len(border) == sum(reading.lifetime_clicks.values()) == 12 * 9
    assert TOOL.find_runs(tmp_path)[0].name == "pair"


def test_a_step_or_a_separation_is_a_diagnostic_and_a_push_or_a_click_decides():
    """A criterion reading a body's own records (its pushes, reads,
    hand-overs, kicks, the clicks) counts inside or outside; one reading the
    step records (no step, the pair separates, the cluster disperses, the
    largest separation) is a GameBoard diagnostic, printed and not counted
    (records 562 and 564; the audit of record 567, F12)."""
    assert TOOL.deciding("the push on the proton 310,967,280,640 toward the neutron")
    assert TOOL.deciding("the label 0 after every hand-over")
    # The shear is a sum of the bodies' own pushes per row: a detector pin.
    assert TOOL.deciding("the shear 49,090,283,970 per row per interval")
    assert TOOL.deciding(
        "290 lifetime clicks per body per interval at tick 20 (the border, a fixed detector)"
    )
    assert TOOL.deciding("the kick outweighed by the pushes read")
    # An onset in host ticks is the record's ordering: a GameBoard
    # diagnostic (the clock audit of 2026-09-22), even beside a click or a kick.
    assert not TOOL.deciding(f"the border's first clicks at tick 4, {TOOL.ONSET}")
    assert not TOOL.deciding(f"the kick outweighed by tick 5, {TOOL.ONSET}")
    assert TOOL.deciding("both bodies leave through the faces")
    assert not TOOL.deciding("no step in the run")
    assert not TOOL.deciding("the pair separates beyond 10 Links and never returns")
    assert not TOOL.deciding("the cluster disperses (the largest separation beyond 3 Links)")
