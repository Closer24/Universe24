"""The weak-force readings tool reads the runner's record and the engine's
flight table and nothing else (the experimenter's rule, 2026-09-20: a
readings tool never replays a rule of the engine; `tools/weak_readings.py`
reads the things' `events`, `age`, `waited`, `steps` and `contacts` off
`run.json`, their `pass`, `become` and the shell's `click` lines off
`events.jsonl`, and the first-arrival age off `nature_beam.direction_flight`).
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
(c) the W world: the bar of `tests/test_w_world.py` (a) (the neutron of
    1839 at x = 2 with `become` at 3 into `p` with the one product
    `[["w", 1, 3]]` on +x, the proton of 1836 at x = 3, the W of charge
    -7344 per unit and lifetime 1), 8 intervals, the model
    `beam-weak-w_exchange-v1`: the neutron's `become` line at tick 3 with
    the products [["w", 1, 3, [1, 0, 0]]], its momentum (-192, 0, 0); the
    proton's click of `w` at tick 4, its clicks {"w": 1}, its content
    1839, its charge (0, 1), its momentum (192, 0, 0); the border
    `lifetime` 0 for `w`; against the pinned integers (at 3, the click
    tick 4, the label 192, the content 1839, the charge [0, 1]) the five
    criteria inside, the kinds DETECTOR (the `become` line, the event's own
    record: record 567, F8), DETECTOR, DETECTOR, DETECTOR, GAMEBOARD; with
    the click tick pinned at 5 the second outside. In (b) the criterion
    "the pair holds" of `j3_deuteron` is the kind DIAGNOSTIC (F9): printed,
    out of the deciding set.
(d) the register of series J2 (`examples/events/weak/expectations.json`)
    derived from the five shipped worlds and the engine's flight table and
    compared, entry by entry (the register's `derivations`; a formula gives,
    a run proves, record 205): the first reader's arrivals are the rows born
    at the ticks up to `ticks` less the age at which a heading row has
    walked the reader's distance (DERIVATIONS_BEAM 11.1); its clicks are the
    arrivals whose phase, the source's stride (its content x the clock's
    rate, the whole part) times the birth ordinal less one over the circle,
    the reader's window admits (`window_admits`, BEAM_LAW note 36; the
    declared width or the half circle); the far detector's clicks are the
    rows born by `ticks` less its own arrival age that no reader's window
    admits (a reader's click takes the row out of the flight, a pass leaves
    it). The five worlds of the register and no other; each entry equal.
(e) the register of series J1 and J3 (`become`) replayed from the shipped
    worlds by the generator's warm run (the re-pin under the fraction-free
    law, 2026-09-21; the register's `derivations`): for `j1_lattice`,
    `j1_source`, `j3_deuteron` and `j3_neutron_free` the range of the count
    each neutron's clock reads over the dwell period (the ticks 61 to 120
    of a warm run of 120 intervals without the `become` keys), the trigger
    ticks at both ends of the range by the clock's rule at + floor(at x c
    / 2^20), the earliest and the latest, the slack, the dwell and the warm
    length equal to the register entry by entry; `j3_deuteron_crowd`'s
    `never` entry the generator's constant. About 25 s per J1 world.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

from event_universe.events import parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight, window_admits
from event_universe.events.run import execute_nature_beam_run
from event_universe.events.world import default_width
from event_universe.world_loading import load_world

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
    # A pinned tick as a range [lo, hi] (the re-pin of 2026-09-21): the
    # tick 3 inside [2, 3] and inside [3, 4], outside [4, 5] and [1, 2].
    assert TOOL.tick_range(3) == (3, 3) and TOOL.tick_range([2, 3]) == (2, 3)
    for pair, inside in (([2, 3], True), ([3, 4], True), ([4, 5], False), ([1, 2], False)):
        ranged = {"become": {"j1_lattice": {"ticks": {"1": pair}, "slack": 0}}}
        assert TOOL.expectations(reading, ranged)[0][1] is inside, pair
    assert [ok for _, ok, _ in criteria] == [True, True, True, True]
    # The trigger tick and the count at the trigger are the neutron's own
    # `become` line: DETECTOR (the audit of record 567, F8).
    assert [kind for _, _, kind in criteria] == [
        TOOL.DETECTOR,
        TOOL.DETECTOR,
        TOOL.DETECTOR,
        TOOL.DETECTOR,
    ]
    # "The pair holds" (the step records) is a GameBoard diagnostic (F9):
    # printed with its verdict, out of the deciding set, the number unchanged.
    reading.name = "j3_deuteron"
    held = TOOL.expectations(reading, {"become": {"j3_deuteron": {"ticks": {"1": 3}, "slack": 0}}})
    pair = [c for c in held if c[0].startswith("the pair holds")]
    assert len(pair) == 1 and pair[0][1] is True and pair[0][2] == TOOL.DIAGNOSTIC
    assert pair[0] not in TOOL.deciding(held) and len(TOOL.deciding(held)) == len(held) - 1
    reading.name = "j1_lattice"
    assert (
        TOOL.expectations(reading, {"become": {"j1_lattice": {"never": True, "gate": 1}}})[0][1] is False
    )


def test_read_run_reads_the_w_world(tmp_path):
    """(c)."""
    document = {
        "law": "beam",
        "model_id": "beam-weak-w_exchange-v1",
        "shape": [7, 1, 1],
        "boundary": "open",
        "ticks": 8,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1 << 20],
        "suspension": 0,
        "families": [
            {"name": "n", "quantum": 0, "phase": False},
            {"name": "p", "quantum": 0, "phase": False, "charge": 4},
            {"name": "w", "quantum": 1, "charge": -7344, "lifetime": 1, "phase": False},
        ],
        "measured": [
            {
                "position": [2, 0, 0],
                "family": "n",
                "amount": 1839,
                "fixed": True,
                "directions": [[1, 0, 0]],
                "become": {"at": 3, "into": "p", "products": [["w", 1, 3]]},
            },
            {"position": [3, 0, 0], "family": "p", "amount": 1836, "fixed": True},
        ],
    }
    folder = tmp_path / "exchange"
    folder.mkdir()
    execute_nature_beam_run(
        parse_nature_beam_world(document), json.dumps(document).encode("utf-8"), folder, "test", 8
    )
    reading = TOOL.read_run(folder)
    assert reading.name == "w_exchange" and reading.completed and reading.balanced
    neutron, proton = reading.things
    assert neutron.become is not None and neutron.become["triggered"] == 3
    assert neutron.become["products"] == [["w", 1, 3, [1, 0, 0]]] and neutron.momentum == (-192, 0, 0)
    assert proton.click_ticks == {"w": [4]} and proton.clicks == {"n": 0, "p": 0, "w": 1}
    assert (proton.content, proton.charge, proton.momentum) == (1839, (0, 1), (192, 0, 0))
    assert reading.border_clicks["w"] == 0
    pinned = {
        "w": {"w_exchange": {"at": 3, "click_tick": 4, "label": 192, "content": 1839, "charge": [0, 1]}}
    }
    criteria = TOOL.expectations(reading, pinned)
    assert [ok for _, ok, _ in criteria] == [True] * 5
    assert [kind for _, _, kind in criteria] == [
        TOOL.DETECTOR,
        TOOL.DETECTOR,
        TOOL.DETECTOR,
        TOOL.DETECTOR,
        TOOL.GAMEBOARD,
    ]
    late = {"w": {"w_exchange": {**pinned["w"]["w_exchange"], "click_tick": 5}}}
    assert [ok for _, ok, _ in TOOL.expectations(reading, late)] == [True, False, True, True, True]


def first_arrival_age(table, distance: int) -> int:
    """The least age at which a heading row's Manhattan steps (the position
    accumulator's count, `Flight.manhattan_steps`) reach `distance`."""
    ages = np.arange(1, 4 * distance + 64, dtype=np.int64)
    steps = table.manhattan_steps(np.full(ages.shape, 2, dtype=np.int64), ages)
    return int(ages[np.flatnonzero(steps >= distance)[0]])


def admitted(reader: dict, phase: int, modulus: int) -> bool:
    """Whether the reader's window admits the phase: the declared width or
    the half circle, by the engine's one floor."""
    entry = reader["table"]["nu"]
    width = int(entry.get("phase_width", default_width(modulus)))
    return bool(window_admits((phase - int(entry["phase_window"])) % modulus, width, modulus))


def test_the_j2_register_is_derived_from_the_worlds_and_the_flight_rule():
    """(d)."""
    folder = ROOT / "examples" / "events" / "weak"
    registered = json.loads((folder / "expectations.json").read_text(encoding="utf-8"))
    assert registered["format"] == "weak-expectations-v1"
    assert set(registered["derivations"]) == {"j2", "become", "w"}
    derived: dict[str, dict[str, int]] = {}
    for path in sorted(folder.glob("j2_*.json")):
        world = json.loads(path.read_text(encoding="utf-8"))
        source, *readers = world["measured"]
        (direction,) = source["directions"]
        table = direction_flight(((0, 0, 0), (0, 0, 0), tuple(direction)))
        ticks, modulus = int(world["ticks"]), int(world["N"])
        stride = TOOL.stride_of(world, source)
        far = readers.pop()
        assert far["table"] == {"nu": {"rule": "measure"}}
        first = readers[0]
        born_first = ticks - first_arrival_age(table, first["position"][0])
        born_far = ticks - first_arrival_age(table, far["position"][0])
        phases = [(stride * (t - 1)) % modulus for t in range(1, max(born_first, born_far) + 1)]

        derived[path.stem] = {
            "first_arrivals": born_first,
            "first_clicks": sum(1 for p in phases[:born_first] if admitted(first, p, modulus)),
            "far": sum(
                1 for p in phases[:born_far] if not any(admitted(r, p, modulus) for r in readers)
            ),
        }
    assert derived == registered["j2"]


def test_the_j1_and_j3_register_is_the_generators_warm_run_on_the_shipped_worlds():
    """(e)."""
    folder = ROOT / "examples" / "events" / "weak"
    registered = json.loads((folder / "expectations.json").read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location("weak_make_worlds", folder / "make_worlds.py")
    assert spec is not None and spec.loader is not None
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    assert (
        registered["become"]["j3_deuteron_crowd"]
        == generator.become_expectations({"j3_deuteron_crowd": {}})["j3_deuteron_crowd"]
    )
    for name in ("j1_lattice", "j1_source", "j3_deuteron", "j3_neutron_free"):
        path = folder / f"{name}.json"
        loaded = load_world(path.read_bytes(), base_dir=path.parent, root=path.parent.parent)
        shipped = json.loads(loaded.expanded_source)
        derived = generator.become_expectations({name: shipped})[name]
        assert derived == registered["become"][name], name
        assert (
            derived["dwell"] == list(generator.DWELL) and derived["warm_ticks"] == generator.WARM_TICKS
        )
        for number, (low, high) in derived["counts"].items():
            assert low <= high
            assert derived["ticks"][number] == [
                generator.trigger_tick(low),
                generator.trigger_tick(high),
            ]
