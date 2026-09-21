"""The orbit readings tool reads the engine's own functions (Highlights 5.4,
the architecture review of 2026-09-20: `tools/orbit_readings.py` now reads
the fan's labels off `nature_beam.direction_flight`, the release off
`engine.by_clock` and the world's keys through `parse_nature_beam_world`). Each
reading of the tool is checked against the engine on a minimal GameBoard; the
expected values of docs/TEST_EXPECTATIONS.md ("The tools read the
engine"), written down first:

(a) the fan's label: on a world declaring the directions (1, 1, 0) and
    (3, 1, 0), a source releasing on (1, 0, 0), (1, 1, 0) and (3, 1, 0) has
    the mean |u_d| / Q of the engine's labels (64, 0, 0), (45, 45, 0) and
    (61, 20, 0) (`test_nature_beam_label` (a)): (64 + hypot(45, 45) + hypot(61,
    20)) / (3 x 64) = 0.99914;
(b) the emission: at `release` [1, 10] a source of content 4 on those three
    directions emits 3 x 4 / 10 = 1.2 units per interval in the mean (the
    clock's gains over the ages 0 .. 9 are 0, 0, 1, 0, 1, 0, 0, 1, 0, 1 per
    direction); on the GameBoard it has released 12 units after 10 intervals
    (the books' transit line);
(c) `read_run` on a run of a 9 x 9 x 1 plane (z periodic) written by the
    runner: a fixed source of content 16 at (4, 4, 0) on the four in-plane
    headings and the four diagonals at `release` [1, 4] (4 units per
    direction per self-creation), a free probe of content 1 at (7, 1, 0)
    with the momentum (0, 64, 0) along +y (the tool reads the momentum's
    y component: the orbits' probes move tangentially), the family's
    charge 1 so that the electric push cancels gravity's and the probe
    keeps its momentum (under gravity alone the +x rows read at the ticks
    6 and 7 push it into their stream, -256 each, and it steps -x from
    tick 8), width 1, 12 intervals: the reading's emission is 8 x 16 / 4 = 32.0, its label (4 x
    64 + 4 x hypot(45, 45)) / (8 x 64), its momentum 64, its radius 3 and
    width 1 off the model name, its reads and units the sums over the
    probe's `read` records, how the run ended read off the record (a
    `click` of the probe on a face, or the Node beside the source reached;
    here neither: the least radius 3 at (7, 4, 0)), the run completed and
    balanced. The probe's `read` lines, derived under the crossing rule
    (2026-09-21, BEAM_LAW note 48; the probe steps +y at the ticks 2, 4,
    6, 8, 10, 12, at (7, 4, 0) from tick 6 and (7, 6, 0) from tick 10; the
    source's +x row born at tick k at x = 4 + m(t - k), m = 0, 1, 1, 2, 2,
    3, 3, ..., its (1, 1, 0) row on the line (5, 4), (5, 5), (6, 5), (6, 6),
    (7, 6), (7, 7) at the count m' = 0, 1, 2, 2, 3, 4, 5, 6, 7): at tick 6
    the +x row of tick 1 arrives at (7, 4, 0) as the probe enters it (C3,
    both arrived), at tick 7 the +x row of tick 2 arrives (C3), at tick 8
    the +x row of tick 3 arrives at the probe's origin as it steps to (7,
    5, 0) (not met, no crossing), at tick 10 the (1, 1, 0) row of tick 4
    arrives at (7, 6, 0) from (6, 6, 0) as the probe enters it (C3, the
    row's step +x against the probe's +y), at tick 11 the row of tick 5
    arrives (C3), and at tick 12 that row moves (7, 6, 0) -> (7, 7, 0)
    with the probe's step (C3', met once at 11): 4 lines, at the ticks 6,
    7, 10, 11, of amount 4 each, every push (0, 0, 0) and the units 0
    (until the crossing rule the probe at (7,
    4, 0) on +y read the diagonal row that reached its origin as it
    stepped away, the leapfrog read the rule removes: from there it meets
    no row of the eight directions in 12 intervals).
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "orbit_readings_tool", ROOT / "tools" / "orbit_readings.py"
)
TOOL = importlib.util.module_from_spec(SPEC)
sys.modules["orbit_readings_tool"] = TOOL
SPEC.loader.exec_module(TOOL)

Q = 64
DIAGONAL = math.hypot(45, 45)


def plane(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "rays-orbit-s1-r3-plane-v1",
        "shape": [9, 9, 1],
        "boundary": {"z": "periodic"},
        "ticks": 12,
        "K": 1024,
        "N": 64,
        "release": [1, 4],
        "suspension": 0,
        "width": 1,
        "directions": [[1, 1, 0], [-1, 1, 0], [-1, -1, 0], [1, -1, 0], [3, 1, 0]],
        "families": [{"name": "m", "quantum": 0, "phase": False}],
        "measured": measured,
    }
    world.update(keys)
    return world


def test_the_fans_label_is_the_engines_label_table():
    """(a)."""
    source = {
        "position": [4, 4, 0],
        "family": "m",
        "amount": 4,
        "fixed": True,
        "directions": [[1, 0, 0], [1, 1, 0], [3, 1, 0]],
    }
    world = parse_nature_beam_world(plane([source]))
    expected = (64 + DIAGONAL + math.hypot(61, 20)) / (3 * Q)
    assert math.isclose(TOOL.fan_label(world, world.measured[0]), expected, rel_tol=1e-12)
    assert round(expected, 5) == 0.99914


def test_the_emission_is_the_engines_release_off_the_clock():
    """(b)."""
    source = {
        "position": [4, 4, 0],
        "family": "m",
        "amount": 4,
        "fixed": True,
        "directions": [[1, 0, 0], [1, 1, 0], [3, 1, 0]],
    }
    world = parse_nature_beam_world(plane([source], release=[1, 10]))
    assert TOOL.fan_emission(world, world.measured[0]) == 1.2
    simulation = NatureBeamSimulation(world)
    for _ in range(10):
        simulation.step()
        assert simulation.books()["balanced"]
    assert simulation.ledger.transit_released[0] == 12


def test_read_run_reads_the_record_and_the_engines_world(tmp_path):
    """(c)."""
    source = {
        "position": [4, 4, 0],
        "family": "m",
        "amount": 16,
        "fixed": True,
        "directions": [
            [1, 0, 0],
            [0, 1, 0],
            [-1, 0, 0],
            [0, -1, 0],
            [1, 1, 0],
            [-1, 1, 0],
            [-1, -1, 0],
            [1, -1, 0],
        ],
    }
    probe = {"position": [7, 1, 0], "family": "m", "amount": 1, "momentum": [0, Q, 0]}
    document = plane(
        [source, probe], families=[{"name": "m", "quantum": 0, "phase": False, "charge": 1}]
    )
    folder = tmp_path / "s1_r3"
    folder.mkdir()
    execute_nature_beam_run(
        parse_nature_beam_world(document), json.dumps(document).encode("utf-8"), folder, "test", 12
    )
    reading = TOOL.read_run(folder)
    assert (reading.name, reading.width, reading.radius, reading.momentum) == ("s1_r3", 1, 3, Q)
    assert reading.emission == 32.0
    assert math.isclose(reading.label, (4 * 64 + 4 * DIAGONAL) / (8 * Q), rel_tol=1e-12)
    assert reading.completed and reading.balanced and reading.ticks == 12
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    reads = [e for e in events if e["event"] == "read" and e["measured"] == TOOL.PROBE]
    assert reading.reads == len(reads) == 4
    assert [(e["tick"], e["amount"], e["node"]) for e in reads] == [
        (6, 4, [7, 4, 0]),
        (7, 4, [7, 4, 0]),
        (10, 4, [7, 6, 0]),
        (11, 4, [7, 6, 0]),
    ]
    assert reading.units == sum(abs(e["push"][0]) + abs(e["push"][1]) for e in reads) == 0
    assert all(e["push"] == [0, 0, 0] for e in reads)
    assert reading.least_radius == 3.0 and reading.ended == ""
    clicks = [e for e in events if e["event"] == "click" and e.get("measured") == TOOL.PROBE]
    if clicks:
        assert reading.ended == f"escaped through {clicks[0]['detector']} at tick {clicks[0]['tick']}"
    else:
        assert reading.ended == (
            "reached the Node beside the source" if reading.least_radius <= 1 else ""
        )
    assert [r.name for r in TOOL.find_runs(tmp_path)] == ["s1_r3"]
