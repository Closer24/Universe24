"""The flight of a ray under the law of the ray (docs/RAY_LAW.md, section 3):
one speed for every direction, 1 / sqrt 3, on the digital line of its
momentum, at most one Link per interval, the age whole on the record and
read modulo the direction's period by the flight; a lone unit is straight
and unchanged; the board's faces open or
periodic (the wrap, the stub of extent 1). The expected integers of
docs/TEST_EXPECTATIONS.md ("The flight"), written down first:

(a) the flight table: for every direction T_d >= S_1 Q and m(tau + 1) -
    m(tau) in {0, 1}; the periods (1, 0, 0) T 110, L 55; (1, 1, 0) T 156,
    L 39; (1, 1, 1) T 192, L 3; (3, 1, 0) T 350, L 175; a rest direction
    never moves; the first arrival of a heading ray at m Links, m = 1..11,
    in the intervals 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19;
(b) the lone unit: every heading and every declared direction of the
    two-slit example, 150 intervals on a periodic 61^3 board: the ray's
    position is the table's digital line, its direction and phase unchanged
    (`phase_per_link` 0), one row at every interval, at most one Link per
    interval; with `phase_per_link` 3 the phase turns 3 per Link crossed;
(c) isotropy: 1000 intervals on (1, 0, 0), (1, 1, 0), (1, 1, 1), (3, 1, 0),
    (5, 2, 1): the Euclidean distance^2 within 2 % of 1000^2 / 3;
(d) the periodic axis (from `test_periodic_axis` (a) to (c), re-pinned): a
    ray on +Z at (2, 0, 0) of a 5 x 1 x 1 bar with {"z": "periodic"} steps
    onto its own Node at every interval the table moves it (the stub) and
    never escapes, its phase 5 kept; on the open bar it clicks on `face:+z`
    at the first interval (every ray steps at its first interval); on a
    1 x 1 x 4 bar with {"z": "periodic"} the ray at z = 3 on +Z is at z = 0
    after the first interval and the ray at z = 0 on -Z at z = 3, the ray on
    +X escapes on `face:+x`; the refusals of the boundary and the record;
(e) `adjacent_node` on (3, 2, 1) with x and z periodic (from
    `test_event_boundaries`): (2, 1, 0) +X -> (0, 1, 0), (0, 1, 0) -X ->
    (2, 1, 0), (1, 1, 0) +Y -> None, +Z and -Z -> (1, 1, 0) itself.
"""

from __future__ import annotations

import json

import numpy as np
import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.core.lattice import PORT_HEADINGS, adjacent_node
from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events import RaySimulation, parse_ray_world
from event_universe.events.nature_beam import Q, flight_table
from event_universe.events.run import execute_ray_run

SLIT_DIRECTIONS = [[1, 1, 0], [1, -1, 0], [2, 1, 0], [2, -1, 0], [3, 1, 0], [3, -1, 0]]
TABLE = (
    (0, 0, 0),
    (0, 0, 0),
    *PORT_HEADINGS,
    *(tuple(v) for v in SLIT_DIRECTIONS),
    (1, 1, 1),
    (5, 2, 1),
)


def test_the_flight_table_steps_at_most_one_link_and_has_the_periods_of_the_design():
    """(a)."""
    table = flight_table(TABLE)
    for index, vector in enumerate(TABLE):
        s1 = sum(abs(c) for c in vector)
        assert int(table.manhattan[index]) == s1
        if s1 == 0:
            assert int(table.period[index]) == 1 and not table.steps[index].any()
            continue
        assert int(table.turns[index]) >= s1 * Q
        ages = np.arange(2 * int(table.period[index]) + 5)
        direction = np.full(ages.shape, index)
        m = table.manhattan_steps(direction, ages)
        assert set((m[1:] - m[:-1]).tolist()) <= {0, 1}
        # The step table over one period walks a whole number of periods of
        # the line: a multiple of v.
        walked = table.steps[index, : int(table.period[index])].sum(axis=0)
        largest = max(range(3), key=lambda axis: abs(vector[axis]))
        multiple = int(walked[largest]) // vector[largest]
        assert walked.tolist() == [c * multiple for c in vector] and multiple >= 1
    periods = {(1, 0, 0): (110, 55), (1, 1, 0): (156, 39), (1, 1, 1): (192, 3), (3, 1, 0): (350, 175)}
    plus_one = flight_table(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS, (1, 1, 0), (1, 1, 1), (3, 1, 0)))
    for vector, (t, period) in periods.items():
        index = plus_one.vectors.tolist().index(list(vector))
        assert (int(plus_one.turns[index]), int(plus_one.period[index])) == (t, period), vector
    position = np.zeros(3, dtype=np.int64)
    arrivals: dict[int, int] = {}
    for tau in range(20):
        position = position + plus_one.steps[2, tau % 55]
        arrivals.setdefault(int(abs(position).sum()), tau + 1)
    assert [arrivals[m] for m in range(1, 12)] == [1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19]


def periodic_cube(directions: list[list[int]], per_link: int = 0) -> dict[str, object]:
    return {
        "law": "rays",
        "model_id": "ray-flight-test",
        "shape": [61, 61, 61],
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "ticks": 150,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        # The age bound a board periodic on every axis must declare.
        "age_bound": 256,
        "directions": directions,
        "families": [{"name": "light", "quantum": 1, "phase_per_link": per_link}],
        "measured": [{"position": [0, 0, 0], "family": "light", "amount": 1, "fixed": True}],
        "in_transit": [],
    }


def test_a_lone_unit_is_straight_on_its_digital_line_and_unchanged():
    """(b)."""
    world = periodic_cube(SLIT_DIRECTIONS)
    table = flight_table(parse_ray_world(world).directions)
    vectors = [list(v) for v in PORT_HEADINGS] + SLIT_DIRECTIONS
    for vector in vectors:
        seeded = {
            **world,
            "in_transit": [
                {
                    "position": [30, 30, 30],
                    "family": "light",
                    "number": 1,
                    "direction": vector,
                    "amount": 1,
                    "phase": 17,
                }
            ],
        }
        simulation = RaySimulation(parse_ray_world(seeded))
        store = simulation.stores[0]
        index = table.vectors.tolist().index(vector)
        expected = np.array([30, 30, 30])
        for tau in range(150):
            expected = (expected + table.steps[index, tau % int(table.period[index])]) % 61
            simulation.step()
            assert store.size == 1 and int(store.amount[0]) == 1
            x, y, z = store.coordinates(store.node)
            assert [int(x[0]), int(y[0]), int(z[0])] == expected.tolist(), (vector, tau)
            assert int(store.direction[0]) == index and int(store.phase[0]) == 17
            assert int(store.age[0]) == tau + 1
    turned = {
        **periodic_cube(SLIT_DIRECTIONS, per_link=3),
        "in_transit": [
            {
                "position": [30, 30, 30],
                "family": "light",
                "number": 1,
                "direction": [3, 1, 0],
                "amount": 1,
                "phase": 0,
            }
        ],
    }
    simulation = RaySimulation(parse_ray_world(turned))
    for _ in range(150):
        simulation.step()
    store = simulation.stores[0]
    index = table.vectors.tolist().index([3, 1, 0])
    links = sum(int(table.steps[index, tau % 175].any()) for tau in range(150))
    assert int(store.phase[0]) == (3 * links) % 64 and links > 0


def test_the_flight_is_isotropic_at_one_over_root_three():
    """(c)."""
    table = flight_table(TABLE)
    for vector in ((1, 0, 0), (1, 1, 0), (1, 1, 1), (3, 1, 0), (5, 2, 1)):
        index = table.vectors.tolist().index(list(vector))
        position = np.zeros(3, dtype=np.int64)
        for tau in range(1000):
            position = position + table.steps[index, tau % int(table.period[index])]
        distance = int((position * position).sum())
        assert abs(distance * 3 / 1000**2 - 1) < 0.02, (vector, distance)


def bar(
    shape: list[int], boundary: object, in_transit: list[dict[str, object]], measured_at: list[int]
) -> dict[str, object]:
    return {
        "law": "rays",
        "model_id": "ray-flight-test",
        "shape": shape,
        "boundary": boundary,
        "ticks": 6,
        "K": 16,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}],
        "measured": [{"position": measured_at, "family": "light", "amount": 1, "fixed": True}],
        "in_transit": in_transit,
    }


def unit(position: list[int], direction: list[int], phase: int) -> dict[str, object]:
    return {
        "position": position,
        "family": "light",
        "number": 1,
        "direction": direction,
        "amount": 1,
        "phase": phase,
    }


STUB = bar([5, 1, 1], {"z": "periodic"}, [unit([2, 0, 0], [0, 0, 1], 5)], [0, 0, 0])


def test_a_periodic_axis_wraps_and_an_open_face_clicks(tmp_path):
    """(d) and the refusals."""
    records: list[dict[str, object]] = []
    simulation = RaySimulation(parse_ray_world(STUB), records.append)
    store = simulation.stores[0]
    for tick in range(1, 7):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], tick
        assert store.size == 1 and int(store.node[0]) == store.flat((2, 0, 0))
        assert int(store.phase[0]) == 5 and int(store.direction[0]) == 6
        assert books["momentum"] == {"measured": [0, 0, 0], "transit": [0, 0, 64], "escaped": [0, 0, 0]}
    assert records == [] and simulation.face_detectors()[0]["name"] == "face:+x"
    assert [face["name"] for face in simulation.face_detectors()] == [
        "face:+x",
        "face:-x",
        "face:+y",
        "face:-y",
    ]
    records.clear()
    simulation = RaySimulation(parse_ray_world({**STUB, "boundary": "open"}), records.append)
    simulation.step()
    assert simulation.stores[0].size == 0
    assert records == [
        {
            "event": "click",
            "tick": 1,
            "node": [2, 0, 0],
            "measured": None,
            "detector": "face:+z",
            "family": "light",
            "number": 1,
            "amount": 1,
            "phase": 5,
            "momentum": [0, 0, 64],
            "content": 1,
        }
    ]
    books = simulation.books()
    assert books["balanced"] and books["momentum"]["escaped"] == [0, 0, 64]
    assert simulation.face_detectors()[4]["families"]["light"] == {
        "measured": 1,
        "clicks": 1,
        "content": 1,
        "record": 32 * 32 * (phase_cosines(64)[5] ** 2 + phase_sines(64)[5] ** 2),
        "measured_content": 0,
    }
    world = bar(
        [1, 1, 4],
        {"z": "periodic"},
        [unit([0, 0, 3], [0, 0, 1], 5), unit([0, 0, 0], [0, 0, -1], 6), unit([0, 0, 2], [1, 0, 0], 7)],
        [0, 0, 1],
    )
    records.clear()
    simulation = RaySimulation(parse_ray_world(world), records.append)
    simulation.step()
    store = simulation.stores[0]
    rows = sorted(
        (int(store.node[i]), int(store.direction[i]), int(store.phase[i])) for i in range(store.size)
    )
    assert rows == [(0, 6, 5), (3, 7, 6)]
    assert [record["detector"] for record in records] == ["face:+x"]
    books = simulation.books()
    assert books["balanced"] and books["momentum"]["escaped"] == [64, 0, 0]
    assert books["families"]["light"]["transit"] == {
        "initial": 3,
        "released": 0,
        "current": 2,
        "escaped": 1,
        "absorbed": 0,
        "balanced": True,
    }
    for refused in ("closed", {"z": "closed"}, {"w": "periodic"}, {"z": 1}, "periodic"):
        with pytest.raises(ValueError, match="closed board is refused"):
            parse_ray_world({**STUB, "boundary": refused})
        report = validate_configuration(json.dumps({**STUB, "boundary": refused}))
        assert not report.valid and report.issues[0].code == "validation"
    parsed = parse_ray_world(STUB)
    assert parsed.periodic == (False, False, True) and parsed.boundary == {"z": "periodic"}
    report = validate_configuration(json.dumps(STUB))
    assert report.valid and report.summary["boundary"] == {"x": "open", "y": "open", "z": "periodic"}
    assert report.summary["law"] == "rays-v1" and report.kind == "rays"
    output = tmp_path / "run"
    output.mkdir()
    record = json.loads(
        execute_ray_run(parsed, json.dumps(STUB).encode(), output, "test", 3).read_text()
    )
    assert record["boundary"] == {"z": "periodic"} and record["status"] == "completed"
    assert record["law"] == "rays-v1" and record["completed_ticks"] == 3
    assert record["escaped"][0]["amount"] == 0
    state = json.loads((output / "state.json").read_text(encoding="utf-8"))
    assert state["law"] == "rays-v1" and state["boundary"] == {"z": "periodic"} and state["tick"] == 3
    assert state["nodes"][0]["families"][0]["rays"][0]["direction"] == [0, 0, 1]


@pytest.mark.parametrize(
    "position,port,expected",
    [
        ((2, 1, 0), 0, (0, 1, 0)),
        ((0, 1, 0), 1, (2, 1, 0)),
        ((1, 0, 0), 2, (1, 1, 0)),
        ((1, 1, 0), 2, None),
        ((1, 0, 0), 3, None),
        ((1, 1, 0), 4, (1, 1, 0)),
        ((1, 1, 0), 5, (1, 1, 0)),
    ],
)
def test_adjacent_node_has_the_declared_signed_links(position, port, expected):
    """(e)."""
    assert adjacent_node(position, port, (3, 2, 1), (True, False, True)) == expected
    if expected is not None:
        assert adjacent_node(expected, port ^ 1, (3, 2, 1), (True, False, True)) == position
