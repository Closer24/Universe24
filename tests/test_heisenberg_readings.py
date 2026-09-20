"""The Heisenberg readings tool reads the engine's own functions (Highlights
5.4, the architecture review of 2026-09-20: `tools/heisenberg_readings.py`
now reads the lamp's turn off `engine.by_clock` and the world's keys through
`parse_nature_beam_world`; the records are the run's `DetectorSet` records). The
tool's reading of a run is checked against the engine on a minimal board;
the expected values of docs/TEST_EXPECTATIONS.md ("The tools read the
engine"), written down first:

a 14 x 5 x 1 plane (z periodic, K 2^20, N 64, 30 intervals): a lamp of
`light` at (1, 2, 0) of content 8 K + 1000 (the turn 8 per self-creation,
`by_clock(0, content, K)`) releasing 3 units per self-creation on (1, 0, 0);
a wall of five `wall` events at x = 4 whose middle Node re-emits on
(1, 0, 0), (1, 1, 0) and (1, -1, 0), the detector `opening` of that one
Node; a screen of five `wall` events at x = 12 read as the detectors
`screen_0` .. `screen_4` under `wave`. The reading: the width 1 and the
reading `wave` off the model name, the wall at x = 4, the screen at x = 12
(L = 8), the centre pixel 2, the wavelength (64 / 8) / sqrt 3 = 4.6188;
the record and the count per pixel equal to the engine's detector sets
after 30 intervals (the screen's centre pixel clicked, the others not); the
opening's re-releases the engine's; the escape the engine's face detectors'
(the diagonal rays leave through the y faces); completed and balanced.
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
    "heisenberg_readings_tool", ROOT / "tools" / "heisenberg_readings.py"
)
TOOL = importlib.util.module_from_spec(SPEC)
sys.modules["heisenberg_readings_tool"] = TOOL
SPEC.loader.exec_module(TOOL)

K = 1 << 20
TICKS = 30
WALL_X, SCREEN_X, HEIGHT = 4, 12, 5


def opening_world() -> dict[str, object]:
    measured: list[dict[str, object]] = [
        {
            "position": [1, 2, 0],
            "family": "light",
            "amount": 8 * K + 1000,
            "phase": 0,
            "fixed": True,
            "lamp": {"rate": [3, 1], "directions": [[1, 0, 0]]},
        }
    ]
    for y in range(HEIGHT):
        entry: dict[str, object] = {
            "position": [WALL_X, y, 0],
            "family": "wall",
            "amount": 1,
            "fixed": True,
        }
        if y == 2:
            entry["table"] = {"light": "rerelease"}
            entry["directions"] = [[1, 0, 0], [1, 1, 0], [1, -1, 0]]
        measured.append(entry)
    for y in range(HEIGHT):
        measured.append({"position": [SCREEN_X, y, 0], "family": "wall", "amount": 1, "fixed": True})
    detectors: list[dict[str, object]] = [
        {"name": "opening", "positions": [[WALL_X, 2, 0]], "threshold": 1, "reading": "wave"}
    ]
    detectors += [
        {"name": f"screen_{y}", "positions": [[SCREEN_X, y, 0]], "threshold": 1, "reading": "wave"}
        for y in range(HEIGHT)
    ]
    return {
        "law": "rays",
        "model_id": "rays-heisenberg-w1-wave-v1",
        "shape": [14, HEIGHT, 1],
        "boundary": {"z": "periodic"},
        "ticks": TICKS,
        "K": K,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "directions": [[1, 1, 0], [1, -1, 0]],
        "families": [{"name": "light", "quantum": 1}, {"name": "wall", "quantum": 1}],
        "measured": measured,
        "detectors": detectors,
    }


def test_read_run_reads_the_record_and_the_engines_world(tmp_path):
    document = opening_world()
    world = parse_nature_beam_world(document)
    folder = tmp_path / "w1_wave"
    folder.mkdir()
    execute_nature_beam_run(world, json.dumps(document).encode("utf-8"), folder, "test", TICKS)
    reading = TOOL.read_run(folder)
    assert (reading.name, reading.width, reading.reading) == ("w1_wave", 1, "wave")
    assert (reading.wall_x, reading.screen_x, reading.distance, reading.centre) == (4, 12, 8, 2)
    assert by_clock(0, 8 * K + 1000, K) == 8
    assert reading.wavelength == (64 / 8) / math.sqrt(3)
    assert round(reading.wavelength, 4) == 4.6188
    assert reading.completed and reading.balanced and reading.ticks == TICKS
    simulation = NatureBeamSimulation(world)
    for _ in range(TICKS):
        simulation.step()
        assert simulation.books()["balanced"]
    light = 0
    screen_sets = simulation.detector_sets[1 : 1 + HEIGHT]
    assert reading.record == [detector_set.record[light] for detector_set in screen_sets]
    clicks = [entry["families"]["light"]["clicks"] for entry in simulation.detectors()[1 : 1 + HEIGHT]]
    assert reading.count == clicks
    assert reading.record[2] > 0 and reading.count[2] > 0
    assert all(value == 0 for y, value in enumerate(reading.record) if y != 2)
    opening = simulation.measured[2 + 2]
    assert opening.detector == 0
    assert reading.opening_clicks == opening.measured[light]["rerelease"] > 0
    assert reading.escaped == simulation.ledger.escaped_units(light) > 0
    assert [r.name for r in TOOL.find_runs(tmp_path)] == ["w1_wave"]
    analysis = TOOL.analyse(reading)
    assert analysis["expected_width"] is None and analysis["product"] is None
