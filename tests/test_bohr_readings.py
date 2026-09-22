"""The Bohr readings tool reads the engine's own functions (the experimenter's
rule, 2026-09-20: a readings tool never replays a rule of the engine;
`tools/bohr_readings.py` reads the flight time off `Flight.manhattan_steps`,
the coherent pointer off `nature_beam.coherent_pointer` with the circle's
tables of `core/phase.py`, and the run off the runner's record). Each reading
is checked against the engine on a minimal GameBoard; the expected integers,
written down first:

(a) the flight time from the centre's plane to a face: on a heading a ray
    has made 5 Manhattan steps first at the age 8 (m(8) = (1024 + 110) //
    220 = 5, m(7) = 4) and 6 steps at the age 10; one step at the age 1;
(b) the coherent pointer per turn and the coherence ratio: two units at
    phase 0 in the first turn and one unit at phase 32 in the second (N =
    64) give the pointers (16384, 0) and (-8192, 0) (32 x amount at the
    table's 256 and -256), the cumulative records 16384^2 and 8192^2 and
    C = 8192^2 / (16384^2 + 8192^2) = 0.2; the second unit at phase 0
    instead gives (8192, 0), 24576^2 and C = 1.8; a turn without clicks has
    the pointer (0, 0); the log-log slope of [1, 4, 9] is 2;
(c) `read_run` on a run written by the runner: an open 11 x 11 x 3 GameBoard,
    a fixed proton of `p` (content 4, charge [1, 1]) at (5, 5, 1) on the
    four in-plane headings at `release` [1, 4], an electron of `e` (content
    16, charge -15, phase 5) at (8, 5, 1) of span [1, 1, 3] with the
    momentum [0, 320, 0] (the steps at the ages 5, 9, 13, 17), `pass` for
    `p` (no push: the momentum constant), `phase_by_momentum` and `action`
    65536 (320 / 1024 of a step per Link: the phases 5, 5, 5, 6 after the
    four steps), releasing on the four in-plane headings, 20 intervals, the
    model `rays-bohr-r3-space-v1`: the reading's radius 3, action 65536,
    the design's j = 4 x 320 x 3 / 65536 = 0.05859375, the flight to
    face:+x 8 intervals (5 Links) and to face:-x 8, the run completed and
    balanced over 20 ticks, the electron's clicks per face equal to the
    record's click lines of `e` on that face (the -x rays born at tick 1
    at x = 8 leaving through the face at tick 16, their ninth Link, m(15)
    = 9), the electron's reads equal to its `read` lines
    (none), its steps' phases those of the step lines, the orbit's angle
    below one turn;
(d) the generator's pins under the two drives (docs/designs/drive_b/DEFAULT.md
    section (c); the line drive the law's since 2026-09-22): the shipped
    `expectations.json` is `expectations()` under the line drive, h = 16 p(8)
    = 5536242544 with p(8) = 346015159 and p(12) = 293783192 (the atoms
    series' integers, derived for form B's circle on 2026-09-21), j = 2 at
    r = 8, r = 2 closing (0.963) and r = 4 between (1.478); the seven
    world files carry the register's momentum, action and intervals; under
    the per-axis drive of history `expectations(AXIS_DRIVE)` gives the
    registered integers of 2026-09-20, h = 5414584320 with p(8) = 338411520
    and p(12) = 288249497, and `derive(AXIS_DRIVE)` the width 45120 from
    v = 0.06; the first Link of the electron at r = 8 is the 18th interval
    under the line drive by `by_line` on the world's wall (Q^2 S M_e + p
    T_D = 377 442 ... over p Q per interval), the 9th under `centred_step`,
    both as `first_link` gives.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

from event_universe.core.integer import by_line
from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events import parse_nature_beam_world
from event_universe.events.nature_beam import coherent_pointer
from event_universe.events.run import execute_nature_beam_run

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("bohr_readings_tool", ROOT / "tools" / "bohr_readings.py")
TOOL = importlib.util.module_from_spec(SPEC)
sys.modules["bohr_readings_tool"] = TOOL
SPEC.loader.exec_module(TOOL)
WORLDS = ROOT / "examples" / "events" / "bohr"
GENERATOR_SPEC = importlib.util.spec_from_file_location("bohr_make_worlds", WORLDS / "make_worlds.py")
GENERATOR = importlib.util.module_from_spec(GENERATOR_SPEC)
sys.modules["bohr_make_worlds"] = GENERATOR
GENERATOR_SPEC.loader.exec_module(GENERATOR)

IN_PLANE = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]


def test_the_flight_time_is_the_engines_manhattan_steps():
    """(a)."""
    assert TOOL.flight_delay((1, 0, 0), 5) == 8
    assert TOOL.flight_delay((0, -1, 0), 6) == 10
    assert TOOL.flight_delay((0, 1, 0), 1) == 1


def test_the_pointer_per_turn_is_the_engines_coherent_pointer():
    """(b)."""
    cosines = np.array(phase_cosines(64), dtype=np.int64)
    sines = np.array(phase_sines(64), dtype=np.int64)
    x, y = coherent_pointer(np.array([2]), np.array([0]), np.zeros(1, dtype=np.int64), cosines, sines)
    assert (x[0], y[0]) == (16384, 0)
    pointers = TOOL.pointer_by_turn([(1, 1, 0), (1, 1, 0), (2, 1, 32)], 2, 64)
    assert pointers == [(16384, 0), (-8192, 0)]
    cumulative, ratio = TOOL.coherence(pointers)
    assert cumulative == [16384**2, 8192**2] and ratio == 0.2
    pointers = TOOL.pointer_by_turn([(1, 1, 0), (1, 1, 0), (2, 1, 0)], 3, 64)
    assert pointers == [(16384, 0), (8192, 0), (0, 0)]
    cumulative, ratio = TOOL.coherence(pointers[:2])
    assert cumulative == [16384**2, 24576**2] and ratio == 1.8
    assert abs(TOOL.slope([1, 4, 9]) - 2) < 1e-12 and TOOL.slope([0, 5]) is None


def test_read_run_reads_the_record_and_the_engines_world(tmp_path):
    """(c)."""
    document = {
        "law": "beam",
        "model_id": "rays-bohr-r3-space-v1",
        "shape": [11, 11, 3],
        "boundary": "open",
        "ticks": 20,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 4],
        "suspension": 0,
        "per_axis_drive": True,  # the per-axis drive of history (2026-09-22): the integers as registered
        "action": 65536,
        "families": [
            {"name": "p", "quantum": 0, "charge": [1, 1], "phase": False},
            {"name": "e", "quantum": 0, "charge": -15, "phase": True},
        ],
        "measured": [
            {"position": [5, 5, 1], "family": "p", "amount": 4, "fixed": True, "directions": IN_PLANE},
            {
                "position": [8, 5, 1],
                "family": "e",
                "amount": 16,
                "phase": 5,
                "momentum": [0, 320, 0],
                "span": [1, 1, 3],
                "phase_by_momentum": True,
                "directions": IN_PLANE,
                "table": {"p": "pass"},
            },
        ],
    }
    folder = tmp_path / "r3"
    folder.mkdir()
    execute_nature_beam_run(
        parse_nature_beam_world(document), json.dumps(document).encode("utf-8"), folder, "test", 20
    )
    reading = TOOL.read_run(folder)
    assert (reading.name, reading.radius, reading.action) == ("r3", 3, 65536)
    assert reading.derived_j == 4 * 320 * 3 / 65536 == 0.05859375
    assert reading.delays[0] == 8 and reading.delays[1] == 8 and reading.delays[2] == 8
    assert reading.completed and reading.balanced and reading.ticks == 20
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    for face, name in enumerate(TOOL.FACE_NAMES[:4]):
        clicks = [
            e for e in events if e["event"] == "click" and e["family"] == "e" and e["detector"] == name
        ]
        assert len(reading.clicks.get(face, [])) == len(clicks) > 0, name
    reads = [e for e in events if e["event"] == "read" and e["measured"] == TOOL.ELECTRON]
    assert reading.reads == len(reads) == 0
    steps = [e for e in events if e["event"] == "step" and e["number"] == TOOL.ELECTRON]
    assert [(e["tick"], e["phase"]) for e in steps] == [(5, 5), (9, 5), (13, 5), (17, 6)]
    assert reading.turns == [] and 0 < reading.angle_turns < 1
    minus = [
        e["tick"]
        for e in events
        if e["event"] == "click" and e["family"] == "e" and e["detector"] == "face:-x"
    ]
    assert min(minus) == 16


def test_the_generators_pins_under_the_two_drives():
    """(d)."""
    pinned = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    expected = json.loads(json.dumps(GENERATOR.expectations()))
    expected.pop("replicated", None)
    pinned.pop("replicated", None)
    assert pinned == expected
    assert pinned["format"] == GENERATOR.EXPECTATIONS_FORMAT
    assert pinned["drive"] == GENERATOR.LINE_DRIVE and pinned["centred"] is False
    assert pinned["width"] == 45120 and pinned["action"] == 16 * 346015159 == 5536242544
    worlds = pinned["worlds"]
    assert worlds["r8"]["momentum"] == 346015159 and worlds["r12"]["momentum"] == 293783192
    assert worlds["r8"]["j"] == 2.0 and worlds["r8"]["kind"] == "closing"
    assert abs(worlds["r2"]["j"] - 0.963) < 5e-4 and worlds["r2"]["kind"] == "closing"
    assert abs(worlds["r4"]["j"] - 1.478) < 5e-4 and worlds["r4"]["kind"] == "between"
    assert abs(worlds["r8"]["pace"] - 346015159 / (64 * 45120 * 1836 + 346015159 * 110 / 64)) < 1e-12
    for name, entry in worlds.items():
        document = json.loads((WORLDS / f"{name}.json").read_text(encoding="utf-8"))
        assert document["measured"][1]["momentum"] == [0, entry["momentum"], 0], name
        assert document["action"] == pinned["action"] and document["ticks"] == entry["ticks"], name
        assert document["width"] == pinned["width"] and "per_axis_drive" not in document, name
    history = GENERATOR.expectations(GENERATOR.AXIS_DRIVE)
    assert history["drive"] == GENERATOR.AXIS_DRIVE and history["action"] == 5414584320
    assert history["worlds"]["r8"]["momentum"] == 338411520
    assert history["worlds"]["r12"]["momentum"] == 288249497
    assert abs(history["worlds"]["r8"]["pace"] - 0.06) < 5e-5
    assert GENERATOR.derive(GENERATOR.AXIS_DRIVE)[1] == 45120
    # The first Link by the engine's own line rule on the world's wall.
    p = 346015159
    wall = 64 * 64 * 45120 * 1836 + p * 110
    for centred, expected_tick in ((False, 18), (True, 9)):
        drives = [0, 0, 0]
        fired = None
        for tick in range(1, 40):
            axis, _sign, drives = by_line(drives, [0, p * 64, 0], wall, centred)
            if axis is not None:
                fired = tick
                break
        assert fired == expected_tick == GENERATOR.first_link(p, 45120, GENERATOR.LINE_DRIVE, centred)
    assert worlds["r8"]["first_link"] == 18
