"""The series K readings tool reads the engine's own functions (the
experimenter's rule, 2026-09-20: a readings tool never replays a rule of
the engine; `tools/lensing_readings.py` reads the lamp's turn and the
mass's rays per direction off `core.integer.by_clock`, the speed and the
dwell off `nature_beam.flight_table`, the world's keys through
`parse_nature_beam_world`, the records off the runner's record and the
GameBoard view through `NatureBeamSimulation`). Each reading is checked
against the engine on a minimal GameBoard; the expected integers, written
down first:

an open 13 x 5 x 3 GameBoard, K 2^20, N 64, `release` [1, 4], no
suspension, 30 intervals: a lamp of `light` at (1, 3, 1) of content
8 K + 1000 (the turn 8 per self-creation) releasing one unit per
self-creation on (1, 0, 0) alone; a mass of the free phase-less family `m`
of content 4 at (6, 2, 1) on the six headings (one ray per heading per
self-creation, `by_clock(0, 4, 4)` = 1), one Link below the beam's line
(b = 1); a screen of 15 `wall` events at x = 11 read as the one-Node
`wave` detectors `screen_<y>_<z>` with `reads: "age"` for `light`; the
same world without the mass as the control. The reading: the turn 8, the
beam [(1, 0, 0)], the screen at x = 11, the mass at (6, 2, 1) (the
GameBoard's centre in the control), b = 1, the fan 6, one ray per
direction; every pixel's cumulative record and clicks equal to the
engine's detector sets after 30 intervals and the window [0, 30] summing
to them; the arrival at the one pixel (3, 1) at the age 17 (the least age
with m(age) >= 10 Links on a heading, `test_hubble_readings` (a)) from the
tick 18 on, so the centroid (3, 1), the width 0, the mean age 17.0 exactly
and the phase rate 8.000 (one ray per interval, the lamp's phase 8 t);
the crowd at b = 1 by series E's form 6 x (55 / 32) / (4 pi) rays per Node
and that times 55 / 32 as the age moment; the replay: 17 rows of the beam
in flight at most, none at rest, none off the beam's direction, the Node
(6, 3, 1) holding a ray of the beam and a ray of the mass's +y heading in
one interval; the verdicts 6 inside and 0 outside (the control's phase
rate, the mass world's five brackets).
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "lensing_readings_tool", ROOT / "tools" / "lensing_readings.py"
)
TOOL = importlib.util.module_from_spec(SPEC)
sys.modules["lensing_readings_tool"] = TOOL
SPEC.loader.exec_module(TOOL)

K = 1 << 20
TICKS = 30
SHAPE = (13, 5, 3)
SCREEN_X = 11
MASS = (6, 2, 1)
LAMP = (1, 3, 1)


def beam_world(name: str, *, mass: bool) -> dict[str, object]:
    measured: list[dict[str, object]] = [
        {
            "position": list(LAMP),
            "family": "light",
            "amount": 8 * K + 1000,
            "phase": 0,
            "fixed": True,
            "lamp": {"rate": [1, 1], "directions": [[1, 0, 0]]},
            "table": {"m": "pass"},
        }
    ]
    if mass:
        measured.append({"position": list(MASS), "family": "m", "amount": 4, "phase": 0, "fixed": True})
    detectors: list[dict[str, object]] = []
    for y in range(SHAPE[1]):
        for z in range(SHAPE[2]):
            measured.append(
                {
                    "position": [SCREEN_X, y, z],
                    "family": "wall",
                    "amount": 1,
                    "fixed": True,
                    "table": {"light": {"rule": "measure", "reads": "age"}, "m": "pass"},
                }
            )
            detectors.append(
                {
                    "name": f"screen_{y}_{z}",
                    "positions": [[SCREEN_X, y, z]],
                    "threshold": 1,
                    "reading": "wave",
                }
            )
    return {
        "law": "beam",
        "model_id": f"rays-lensing-{name}-space-v1",
        "shape": list(SHAPE),
        "boundary": "open",
        "ticks": TICKS,
        "K": K,
        "N": 64,
        "release": [1, 4],
        "suspension": 0,
        "families": [
            {"name": "light", "quantum": 1},
            {"name": "wall", "quantum": 1},
            {"name": "m", "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": measured,
        "detectors": detectors,
    }


def write_run(tmp_path: Path, name: str, *, mass: bool) -> dict[str, object]:
    document = beam_world(name, mass=mass)
    folder = tmp_path / name
    folder.mkdir()
    execute_nature_beam_run(
        parse_nature_beam_world(document), json.dumps(document).encode("utf-8"), folder, "test", TICKS
    )
    return document


def test_the_speed_and_the_dwell_are_the_flight_tables():
    assert (TOOL.HEADING_PERIOD, TOOL.HEADING_LINKS) == (55, 32)
    assert TOOL.SPEED == 32 / 55 and TOOL.DWELL == 55 / 32


def test_read_run_reads_the_record_and_the_engines_world(tmp_path):
    write_run(tmp_path, "control", mass=False)
    document = write_run(tmp_path, "mass", mass=True)
    readings = TOOL.find_runs(tmp_path, window_start=0)
    assert [r.name for r in readings] == ["control", "mass"]
    control, reading = readings
    assert by_clock(0, 8 * K + 1000, K) == 8
    assert (reading.turn, reading.K, reading.phase_steps) == (8, K, 64)
    assert reading.lamp == LAMP and reading.screen_x == SCREEN_X and reading.centre == MASS
    assert (reading.impact, reading.mass_content, reading.fan, reading.rays_per_direction) == (
        1,
        4,
        6,
        1,
    )
    assert reading.beam == [(1, 0, 0)] and reading.window == (0, TICKS + 1)
    assert control.centre == MASS and control.impact == 1 and control.mass_content is None
    assert reading.completed and reading.balanced and reading.ticks == TICKS
    simulation = NatureBeamSimulation(parse_nature_beam_world(document))
    for _ in range(TICKS):
        simulation.step()
    light = 0
    by_name = {d["name"]: d for d in simulation.detectors()}
    sets = {s.name: s for s in simulation.detector_sets if s.name is not None}
    assert len(reading.pixels) == 15
    for (y, z), pixel in reading.pixels.items():
        name = f"screen_{y}_{z}"
        assert pixel.record == sets[name].record[light]
        assert pixel.clicks == by_name[name]["families"]["light"]["clicks"]
        assert pixel.window_count == pixel.clicks and pixel.window_record == pixel.record
    analysis = TOOL.analyse(reading)
    assert analysis.count == 13 and analysis.lit == 1
    assert (analysis.centroid_y, analysis.centroid_z, analysis.width_y) == (3.0, 1.0, 0.0)
    assert analysis.mean_age == 17.0 and analysis.first_tick == 18
    assert abs(analysis.phase_rate - 8.0) < 1e-9
    assert analysis.escaped == 0 and reading.mass_took == 0
    presence, age_moment = TOOL.crowd_at(reading, 1)
    assert presence == 6 * (55 / 32) / (4 * math.pi)
    assert age_moment == presence * 55 / 32
    assert TOOL.crowd_at(control, 1) == (0.0, 0.0)
    replay = reading.replay
    assert replay is not None
    assert max(replay.rows) == 17 and sum(replay.resting) == 0 and sum(replay.turned) == 0
    assert not replay.turned_nodes and max(replay.meetings) >= 1
    assert max(replay.crowd_rows) > 0 and max(control.replay.crowd_rows) == 0
    assert TOOL.print_readings(readings) == (6, 0)
