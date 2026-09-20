"""The A10 low-rate readings tool reads the engine's own functions (the
experimenter's rule, 2026-09-20: a readings tool never replays a rule of
the engine; `tools/buildup_readings.py` reads the lamp's turn and rate off
`core.integer.by_clock`, one unit's amplitude at a phase off
`nature_beam.coherent_pointer` with the circle's tables, the world's keys
through `parse_nature_beam_world`, the spread readings off
`tools/heisenberg_readings.py` and the records off the runner's record).
Each reading is checked against the engine on a minimal GameBoard; the
expected integers, written down first:

a 14 x 5 x 1 plane (z periodic, K 2^20, N 64, 45 intervals): a lamp of
`light` at (1, 2, 0) of content 8 K + 1000 (the turn 8 per self-creation)
releasing `rate` units per self-creation on (1, 0, 0); a wall of five
`wall` events at x = 4 whose middle Node re-emits on (1, 0, 0) alone, so
that what arrives leaves as one row toward the screen's centre pixel; a
screen of five `wall` events at x = 12 read as the `wave` detectors
`screen_0` .. `screen_4`. Two runs, the rates 2 and 1 (the models
`rays-buildup-w1-rate<n>-v1`), ordered by the rate descending. The
reading: the width 1 and the rate off the model name and the lamp's
`rate` through `by_clock`, the wavelength (64 / 8) / sqrt 3, the screen at
x = 12 (L = 8), the centre pixel 2; every pixel's cumulative record and
clicks equal to the engine's detector sets after 45 intervals and the
window [0, 30) summing to them; at the rate 2 every interval of the centre
pixel clicks one row of amount 2 (in phase: the record 4 units' squares,
the incoherent sum 2), so the cells with two or more rays are every cell,
R / I = 2 exactly and the cross term equals I; at the rate 1 one unit per
interval, no coincidence, R / I = 1 exactly and the cross term 0; the
other pixels never click.
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
    "buildup_readings_tool", ROOT / "tools" / "buildup_readings.py"
)
TOOL = importlib.util.module_from_spec(SPEC)
sys.modules["buildup_readings_tool"] = TOOL
SPEC.loader.exec_module(TOOL)

K = 1 << 20
TICKS = 45
WALL_X, SCREEN_X, HEIGHT = 4, 12, 5


def opening_world(rate: int) -> dict[str, object]:
    measured: list[dict[str, object]] = [
        {
            "position": [1, 2, 0],
            "family": "light",
            "amount": 8 * K + 1000,
            "phase": 0,
            "fixed": True,
            "lamp": {"rate": [rate, 1], "directions": [[1, 0, 0]]},
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
            entry["directions"] = [[1, 0, 0]]
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
        "law": "beam",
        "model_id": f"rays-buildup-w1-rate{rate}-v1",
        "shape": [14, HEIGHT, 1],
        "boundary": {"z": "periodic"},
        "ticks": TICKS,
        "K": K,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}, {"name": "wall", "quantum": 1}],
        "measured": measured,
        "detectors": detectors,
    }


def test_read_run_reads_the_record_and_the_engines_world(tmp_path):
    documents = {}
    for rate in (1, 2):
        document = opening_world(rate)
        folder = tmp_path / f"rate{rate}"
        folder.mkdir()
        execute_nature_beam_run(
            parse_nature_beam_world(document),
            json.dumps(document).encode("utf-8"),
            folder,
            "test",
            TICKS,
        )
        documents[rate] = document
    readings = TOOL.find_runs(tmp_path, window_start=0)
    assert [(r.name, r.rate, r.width) for r in readings] == [("w1_rate2", 2, 1), ("w1_rate1", 1, 1)]
    for reading in readings:
        assert by_clock(0, reading.rate, 1) == reading.rate
        assert reading.wavelength == (64 / 8) / math.sqrt(3)
        assert (reading.wall_x, reading.screen_x, reading.distance, reading.centre) == (4, 12, 8, 2)
        assert reading.completed and reading.balanced and reading.window == (0, TICKS + 1)
        simulation = NatureBeamSimulation(parse_nature_beam_world(documents[reading.rate]))
        for _ in range(TICKS):
            simulation.step()
        light = 0
        sets = {s.name: s for s in simulation.detector_sets if s.name is not None}
        clicks = {d["name"]: d["families"]["light"]["clicks"] for d in simulation.detectors()}
        for y, pixel in reading.pixels.items():
            assert pixel.record == sets[f"screen_{y}"].record[light] == pixel.window_record
            assert pixel.clicks == clicks[f"screen_{y}"] == pixel.count
            if y != 2:
                assert pixel.count == 0 and pixel.cells == 0
        centre = reading.pixels[2]
        assert centre.cells > 0 and centre.count == reading.rate * centre.cells
        analysis = TOOL.analyse(reading)
        assert analysis.peak == 2 and analysis.clicks == centre.count
        if reading.rate == 2:
            assert centre.coincidences == centre.cells and centre.coincident_clicks == centre.count
            assert analysis.ratio_peak == 2.0 and analysis.cross == centre.incoherent
        else:
            assert centre.coincidences == 0 and centre.coincident_clicks == 0
            assert analysis.ratio_peak == 1.0 and analysis.cross == 0
