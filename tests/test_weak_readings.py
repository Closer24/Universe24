"""The weak-force readings tool reads the runner's record and the engine's
flight table and nothing else (the experimenter's rule, 2026-09-20: a
readings tool never replays a rule of the engine; `tools/weak_readings.py`
reads the things' `events`, `age`, `waited`, `steps` and `contacts` off
`run.json`, their `pass`, `become` and the shell's `click` lines off
`events.jsonl`, and the first-arrival age off `nature_beam.flight_table`).
Two fast cases pin the tool to the engine's record:

(a) J2: a bar of 40 x 1 x 1, K 4096, N 64, `release` [1, 4096], a fixed
    `nu` source of content 4096 at x = 0 releasing one ray per
    self-creation on +x (the stride 1), three readers of the paid family
    `d` at x = 8, 9 and 10 measuring `nu` in the window 0 of width 1, and
    a far detector at x = 30 measuring without a window, 205 intervals,
    the model `beam-weak-j2_filter-v1`, run through the runner. The
    expected integers, written down first from the flight table's m(tau)
    = (128 tau + 110) // 220: the first-arrival ages 13 at 8 Links (m(13)
    = 8, m(12) = 7) and 51 at 30 (m(51) = 6638 // 220 = 30, m(50) = 29);
    the first reader's arrivals 192 (the rays born at the ticks 1 .. 205 -
    13), its clicks 3 (the phases 0 of the rays born at the ticks 1, 65
    and 129), its passes 189; the readers at 9 and 10 no click; the far
    detector 151 clicks (154 rays born at the ticks 1 .. 205 - 51 reach 30
    Links, less the three of phase 0); the stride 1; the criteria of
    `j2_filter` all inside (the fraction 3 / 192 = 1 / 64, nothing behind,
    the far count); the record completed and balanced.
(b) J1: an open 9^3 GameBoard, K 2^20, `release` [1, 4096], `suspension`
    [1, 2^20], the toy of `tests/test_become.py` with the beta content 3
    (`n` content 7 fixed at the centre with `become` at 3 into `p` (charge
    [1, 4]: +1 on the 4 left) with the products beta (1, 3; charge -1) and
    nu (1, 0)), a shell of `d` at r = 2 (62 Nodes: the 6 axis Nodes, the
    24 of the kind (2, 1, 0), the 24 of (2, 1, 1) and the 8 of (1, 1, 1),
    each within a half Link of 2) as one `beam` set measuring `beta` with
    `reads` `age` and passing `n`, `p` and `nu`, 12 intervals, the model
    `beam-weak-j1_lattice-v1`: the neutron's `become` line triggered at
    tick 3 with the count 0; the beta product on +y (the clock age 2) at
    (4, 6, 4) at tick 6 (the age 3, m(3) = 2): the shell's clicks {6: 1},
    the contents {3: 1}, the ages [3]; the nu product on -y passes the
    shell; against a pinned expectation of the tick 3 with no slack the
    criteria inside: the tick, the content 3, the count 1 of 1, the step
    (one click: the width 0 over the median 6); the clock's age 12 and
    waited 0, no step and no attempted step (the event is fixed), the key
    `at` 3 read off the record.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

from event_universe.events import parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("weak_readings_tool", ROOT / "tools" / "weak_readings.py")
TOOL = importlib.util.module_from_spec(SPEC)
sys.modules["weak_readings_tool"] = TOOL
SPEC.loader.exec_module(TOOL)


def reader(x: int, windowed: bool) -> dict[str, object]:
    entry: dict[str, object] = {"rule": "measure"}
    if windowed:
        entry.update({"phase_window": 0, "phase_width": 1})
    return {"position": [x, 0, 0], "family": "d", "amount": 1, "fixed": True, "table": {"nu": entry}}


def test_read_run_reads_the_runners_record(tmp_path):
    """(a)."""
    document = {
        "law": "beam",
        "model_id": "beam-weak-j2_filter-v1",
        "shape": [40, 1, 1],
        "boundary": "open",
        "ticks": 205,
        "K": 4096,
        "N": 64,
        "release": [1, 4096],
        "suspension": 0,
        "families": [{"name": "nu", "quantum": 0}, {"name": "d", "quantum": 1, "phase": False}],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "nu",
                "amount": 4096,
                "phase": 0,
                "fixed": True,
                "directions": [[1, 0, 0]],
            },
            reader(8, True),
            reader(9, True),
            reader(10, True),
            reader(30, False),
        ],
    }
    folder = tmp_path / "filter"
    folder.mkdir()
    execute_nature_beam_run(
        parse_nature_beam_world(document), json.dumps(document).encode("utf-8"), folder, "test", 205
    )
    assert TOOL.first_arrival_age(8) == 13 and TOOL.first_arrival_age(30) == 51
    reading = TOOL.read_run(folder)
    assert reading.name == "j2_filter" and reading.stride == 1 and reading.shape == (40, 1, 1)
    assert reading.completed and reading.balanced and reading.ticks == 205
    first, second, third, far = reading.of_family("d")
    assert first.position == (8, 0, 0) and first.arrivals("nu") == 192
    assert first.clicks == {"nu": 3, "d": 0} and first.passes == {"nu": 189}
    assert second.clicks["nu"] == 0 and third.clicks["nu"] == 0
    assert far.position == (30, 0, 0) and far.clicks["nu"] == 151 and far.passes == {}
    criteria = TOOL.expectations(reading)
    assert [ok for _, ok, _ in criteria] == [True, True, True]
    assert all(kind == TOOL.DETECTOR for _, _, kind in criteria)
    assert TOOL.find_runs(tmp_path)[0].name == "j2_filter"


def test_read_run_reads_a_transformation_and_the_shells_curve(tmp_path):
    """(b)."""
    centre = (4, 4, 4)
    nodes = [
        [x, y, z]
        for x in range(9)
        for y in range(9)
        for z in range(9)
        if abs(math.dist((x, y, z), centre) - 2) < 0.5
    ]
    assert len(nodes) == 62
    shell_table = {"n": "pass", "p": "pass", "nu": "pass", "beta": {"rule": "measure", "reads": "age"}}
    document = {
        "law": "beam",
        "model_id": "beam-weak-j1_lattice-v1",
        "shape": [9, 9, 9],
        "boundary": "open",
        "ticks": 12,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 4096],
        "suspension": [1, 1 << 20],
        "families": [
            {"name": "n", "quantum": 0, "phase": False},
            {"name": "p", "quantum": 0, "phase": False, "charge": [1, 4]},
            {"name": "beta", "quantum": 1, "charge": -1},
            {"name": "nu", "quantum": 0},
            {"name": "d", "quantum": 1, "phase": False},
        ],
        "measured": [
            {
                "position": list(centre),
                "family": "n",
                "amount": 7,
                "fixed": True,
                "become": {"at": 3, "into": "p", "products": [["beta", 1, 3], ["nu", 1, 0]]},
            },
            *(
                {"position": node, "family": "d", "amount": 1, "fixed": True, "table": shell_table}
                for node in nodes
            ),
        ],
        "detectors": [{"name": "shell", "positions": nodes, "threshold": 1, "reading": "beam"}],
    }
    folder = tmp_path / "lattice"
    folder.mkdir()
    execute_nature_beam_run(
        parse_nature_beam_world(document), json.dumps(document).encode("utf-8"), folder, "test", 12
    )
    reading = TOOL.read_run(folder)
    assert reading.name == "j1_lattice" and reading.completed and reading.balanced
    neutron = reading.of_family("n")[0]
    assert (
        neutron.become is not None
        and neutron.become["triggered"] == 3
        and neutron.become["counted"] == 0
    )
    assert neutron.become["products"] == [["beta", 1, 3, [0, 1, 0]], ["nu", 1, 0, [0, -1, 0]]]
    assert (neutron.age, neutron.waited, neutron.steps, neutron.attempts, neutron.at) == (12, 0, 0, 0, 3)
    assert (
        reading.shell_clicks == {6: 1} and reading.shell_contents == {3: 1} and reading.shell_ages == [3]
    )
    assert TOOL.curve_shape(reading.shell_clicks) == (6, 6, 6, 0.0)
    pinned = {"become": {"j1_lattice": {"ticks": {"1": 3}, "slack": 0, "counts": {"1": 0}}}}
    criteria = TOOL.expectations(reading, pinned)
    assert [ok for _, ok, _ in criteria] == [True, True, True, True]
    assert [kind for _, _, kind in criteria] == [
        TOOL.GAMEBOARD,
        TOOL.DETECTOR,
        TOOL.DETECTOR,
        TOOL.DETECTOR,
    ]
    assert (
        TOOL.expectations(reading, {"become": {"j1_lattice": {"never": True, "gate": 1}}})[0][1] is False
    )
