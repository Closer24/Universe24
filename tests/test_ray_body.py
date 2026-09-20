"""A body on a set of Nodes with one record (docs/RAY_LAW.md, section 10,
note 30; the model owner, 2026-09-20: the electron of width 3, taken with
the decision on Bohr, "go, and put it as parameters outside the board like
the age"). A measured event declares `span`, three odd extents centred on
its position: its clock, its threshold and its push read the one reading
set summed over its Nodes, its releases are apportioned whole over them,
the step moves the whole set, no collision acts at any of its Nodes. Every
rule is on the measured-event side, the external thing; the rays' flight
and collision are untouched. The expected integers of
docs/TEST_EXPECTATIONS.md ("A body on a set and the turn by momentum"),
written down first:

(a) a set of one Node is today's measured event bit for bit: a free body
    of `m` (content 16, momentum [256, 0, 0], phase 5) at (3, 1, 1) of an
    open 12 x 3 x 3 board at `release` [1, 4] (4 rays per heading per
    self-creation), a fixed counter of `light` at (9, 1, 1) measuring `m`
    in the `wave` detector `d`, a head-on pair of number 2 on +-y at x = 6
    that parks at (6, 1, 1) at the first interval and leaves on +-z; 30
    intervals: the body's x per interval 3 (4 times), 4 (5), 5 (5), 6 (5),
    7 (5), 8 (6); the body at (8, 1, 1), age 30, phase 5, 6 steps, held
    [16, 0]; the counter held [0, 4], 99 units clicked, momentum (-25344,
    0, 0), the record 37348285440 at phase 5; 152 clicks, 20 record lines,
    5 steps, 5 homes (the body stepping onto its own +x ray); the pair's
    clicks on face:-z (phase 40) and face:+z (phase 3) at tick 6; 25 rows
    of 101 units in the store; the transit line 2 + 740 = 101 + 522 + 119;
    the same integers with `span` [1, 1, 1] declared, every record equal;
(b) a set of three Nodes: a fixed body of `light` (content 4) at (4, 0, 1)
    of an open 9 x 1 x 3 bar with span [1, 1, 3] (the Nodes (4, 0, 0),
    (4, 0, 1), (4, 0, 2)) measuring `m` in the `wave` detector `d` of
    threshold 3, `suspension` [1, 1]: three rays of `m` (number 2, amount
    1, phase 0) arriving in one interval, one at each Node, are summed
    over the set: 3 clicks (the counter's events [3, 0], held [0, 4], the
    push (-768, 0, 0) = -4 x 3 x 64), one `record` line naming `d` with
    the record (3 x 32)^2 x 256^2 = 9 x 67108864, the presence 3 and the
    count 3, the owed count `by_clock(0, 3, 1)` = 3; two rays at two of
    the Nodes pass (`threshold` 3), no click, no push; the step: a free
    body of `m` (content 16, momentum [1024, 0, 0]) of span [1, 1, 3] at
    (2, 0, 1) of an open 6 x 1 x 3 bar steps at the ages 2, 4, 6 with all
    three Nodes (x per interval 2, 3, 3, 4, 4, 5, 5); with a fixed anchor
    at (5, 0, 0), a Node of the moved set at the age 6, the step is
    refused and the body stays at (4, 0, 1) with 3 steps counted; without
    it the step of the age 8 leaves the board and the whole body clicks
    on face:+x (one click, node (5, 0, 1), amount 16, the measured line's
    escaped 16, no measured event left); with x periodic it wraps to
    (0, 0, 1) with the Nodes (0, 0, 0), (0, 0, 1), (0, 0, 2); on a bar
    with z periodic of extent 3 the body at (2, 0, 0) is on (2, 0, 2),
    (2, 0, 0), (2, 0, 1) in that order;
(c) the books balance with a set that releases: a free body of `m`
    (content 16) of span [1, 1, 3] at (3, 1, 2) of an open 7 x 3 x 5
    board at `release` [1, 4] on the four headings +-X, +-Y (so that no
    ray of its own enters its set): 4 units per heading per self-creation
    apportioned whole over the three Nodes, [2, 1, 1] at the age 0
    (the leftover to the Node `age mod 3`), [1, 2, 1] at the age 1,
    [1, 1, 2] at the age 2: the rows born at the first interval sum to
    8, 4, 4 units at (3, 1, 1), (3, 1, 2), (3, 1, 3), 16 in all, at the
    second 4, 8, 4; the books balance at every one of 20 intervals and
    equal their recount; a lamp of `light` (content 24, K 24, rate
    [1, 1]) on +Y of span [3, 1, 1] at (1, 0, 0) of a 3 x 6 x 1 board
    releases its one unit per self-creation at the Nodes x = 0, 1, 2 in
    turn (the ages 0, 1, 2): after 3 intervals the rows (0, 1, 0) age 2
    phase 0, (1, 1, 0) age 1 phase 1, (2, 0, 0) age 0 phase 2, held
    [0, 21], the recoil (0, -192, 0), the transit momentum (0, 192, 0);
(f) the refusals, naming the key: `span` "3", [2, 1, 1], [0, 1, 1],
    [5, 1, 1] on an axis of 3, a body leaving the board on an open axis,
    two bodies sharing a Node, a detector naming a Node of a body that is
    not its position; accepted: `span` [3, 1, 1] at x = 0 of a periodic
    axis; the record carries per measured event its `span`, the state
    the same.
"""

from __future__ import annotations

import json

import pytest

from event_universe.core.integer import by_clock
from event_universe.events import RaySimulation, parse_ray_world
from event_universe.events.world import body_nodes
from event_universe.runner import run_initialization

M, LIGHT = 0, 1
UNIT_RECORD = 32 * 32 * 256 * 256
FAMILIES = [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1}]


def world(**keys: object) -> dict[str, object]:
    base: dict[str, object] = {
        "law": "rays",
        "model_id": "ray-body-test",
        "shape": [12, 3, 3],
        "boundary": "open",
        "ticks": 30,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": FAMILIES,
        "measured": [],
    }
    base.update(keys)
    return base


def ray(position: list[int], direction: list[int], number: int, phase: int = 0) -> dict[str, object]:
    return {
        "position": position,
        "family": "m",
        "number": number,
        "direction": direction,
        "amount": 1,
        "phase": phase,
    }


def rows(simulation: RaySimulation, family: int) -> list[tuple[int, ...]]:
    store = simulation.stores[family]
    return sorted(
        zip(
            store.node.tolist(),
            store.direction.tolist(),
            store.age.tolist(),
            store.phase.tolist(),
            store.amount.tolist(),
            store.content.tolist(),
            strict=True,
        )
    )


# -- (a) ---------------------------------------------------------------------------

BODY_OF_ONE = {
    "position": [3, 1, 1],
    "family": "m",
    "amount": 16,
    "phase": 5,
    "momentum": [256, 0, 0],
}
COUNTER = {
    "position": [9, 1, 1],
    "family": "light",
    "amount": 4,
    "fixed": True,
    "table": {"m": "measure"},
}
PAIR = [ray([6, 0, 1], [0, 1, 0], 2, phase=3), ray([6, 2, 1], [0, -1, 0], 2, phase=40)]


def one_node_world(body: dict[str, object]) -> dict[str, object]:
    return world(
        release=[1, 4],
        measured=[body, COUNTER],
        in_transit=PAIR,
        detectors=[{"name": "d", "positions": [[9, 1, 1]], "threshold": 1, "reading": "wave"}],
    )


def run_one_node(body: dict[str, object]) -> tuple[RaySimulation, list[dict[str, object]], list[int]]:
    records: list[dict[str, object]] = []
    simulation = RaySimulation(parse_ray_world(one_node_world(body)), records.append)
    xs = []
    for tick in range(1, 31):
        simulation.step()
        assert simulation.books()["balanced"], tick
        xs.append(simulation.measured[1].position[0])
    return simulation, records, xs


def test_a_set_of_one_node_is_todays_measured_event():
    """(a)."""
    simulation, records, xs = run_one_node(BODY_OF_ONE)
    assert xs == [3] * 4 + [4] * 5 + [5] * 5 + [6] * 5 + [7] * 5 + [8] * 6
    body, counter = simulation.measured[1], simulation.measured[2]
    assert body.position == (8, 1, 1) and body.nodes == ((8, 1, 1),) and body.span == (1, 1, 1)
    assert (body.age, body.phase, body.momentum, body.steps, body.held) == (
        30,
        5,
        [256, 0, 0],
        6,
        [16, 0],
    )
    assert counter.held == [0, 4] and counter.events == [99, 0]
    assert counter.momentum == [-25344, 0, 0]
    assert counter.detector_set.record == [37348285440, 0] and counter.detector_set.phase == [5, None]
    kinds = {
        kind: sum(1 for r in records if r["event"] == kind)
        for kind in ("click", "record", "step", "home")
    }
    assert kinds == {"click": 152, "record": 20, "step": 5, "home": 5}
    by_detector = {}
    for r in records:
        if "detector" in r:
            key = (r["detector"], r["event"])
            by_detector[key] = by_detector.get(key, 0) + 1
    assert by_detector == {
        ("face:-z", "click"): 28,
        ("face:+z", "click"): 28,
        ("face:-y", "click"): 27,
        ("face:+y", "click"): 27,
        ("d", "click"): 24,
        ("d", "record"): 20,
        ("face:-x", "click"): 18,
        (None, "home"): 5,
    }
    pair = [
        (r["tick"], r["detector"], r["phase"])
        for r in records
        if r.get("number") == 2 and r["event"] == "click"
    ]
    assert pair == [(6, "face:-z", 40), (6, "face:+z", 3)]
    store = simulation.stores[M]
    assert store.size == 25 and int(store.amount.sum()) == 101
    transit = simulation.books()["families"]["m"]["transit"]
    assert transit == {
        "initial": 2,
        "released": 740,
        "current": 101,
        "escaped": 522,
        "absorbed": 119,
        "balanced": True,
    }
    assert {port: units[M] for port, units in simulation.ledger.face_units.items()} == {
        0: 0,
        1: 74,
        2: 111,
        3: 111,
        4: 113,
        5: 113,
    }
    # The span declared as one Node: every record equal, every row equal.
    declared, declared_records, declared_xs = run_one_node({**BODY_OF_ONE, "span": [1, 1, 1]})
    assert declared_xs == xs and declared_records == records
    assert rows(declared, M) == rows(simulation, M)
    assert (
        declared.measured[1].state() == body.state() and declared.measured[2].state() == counter.state()
    )


# -- (b) ---------------------------------------------------------------------------

SET_NODES = ((4, 0, 0), (4, 0, 1), (4, 0, 2))


def set_world(rays: list[dict[str, object]], suspension: object = 0) -> dict[str, object]:
    counter = {
        "position": [4, 0, 1],
        "family": "light",
        "amount": 4,
        "fixed": True,
        "span": [1, 1, 3],
        "table": {"m": "measure"},
    }
    source = {"position": [8, 0, 1], "family": "m", "amount": 1, "fixed": True}
    return world(
        shape=[9, 1, 3],
        suspension=suspension,
        measured=[counter, source],
        in_transit=rays,
        detectors=[{"name": "d", "positions": [[4, 0, 1]], "threshold": 3, "reading": "wave"}],
    )


def mover_world(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    body = {
        "position": [2, 0, 1],
        "family": "m",
        "amount": 16,
        "momentum": [1024, 0, 0],
        "span": [1, 1, 3],
    }
    return world(shape=[6, 1, 3], measured=[body, *measured], **keys)


def test_a_body_on_three_nodes_reads_steps_and_clicks_as_one():
    """(b)."""
    three = [ray([3, 0, z], [1, 0, 0], 2) for z in range(3)]
    records: list[dict[str, object]] = []
    simulation = RaySimulation(parse_ray_world(set_world(three, suspension=[1, 1])), records.append)
    body = simulation.measured[1]
    assert body.span == (1, 1, 3) and body.nodes == SET_NODES
    assert {node: simulation.at[node] for node in SET_NODES} == dict.fromkeys(SET_NODES, 1)
    simulation.step()
    assert simulation.books()["balanced"]
    assert body.events == [3, 0] and body.held == [0, 4] and body.momentum == [-768, 0, 0]
    assert body.presence == 3 and body.counted == 3
    assert body.owed == by_clock(0, 3, 1) == 3
    assert body.detector_set.record == [9 * UNIT_RECORD, 0] and body.phase == 0
    lines = [r for r in records if r["event"] == "record"]
    assert len(lines) == 1 and lines[0]["detector"] == "d" and lines[0]["record"] == 9 * UNIT_RECORD
    assert [r["node"] for r in records if r["event"] == "click"] == [[4, 0, 1]] * 3
    assert simulation.stores[M].size == 0
    # A smaller set passes: the threshold reads the sum over the set.
    records.clear()
    simulation = RaySimulation(parse_ray_world(set_world(three[:2])), records.append)
    simulation.step()
    assert simulation.books()["balanced"]
    assert [(r["event"], r["threshold"]) for r in records] == [("pass", 3), ("pass", 3)]
    body = simulation.measured[1]
    assert body.events == [0, 0] and body.momentum == [0, 0, 0] and body.detector_set.record == [0, 0]
    assert simulation.stores[M].size == 2
    # The step moves the whole set; a Node of the moved set held by another
    # measured event refuses it.
    anchor = {"position": [5, 0, 0], "family": "m", "amount": 1, "fixed": True}
    simulation = RaySimulation(parse_ray_world(mover_world([anchor])))
    body = simulation.measured[1]
    xs = []
    for tick in range(1, 7):
        simulation.step()
        assert simulation.books()["balanced"], tick
        xs.append(body.position[0])
        assert body.nodes == tuple((body.position[0], 0, z) for z in range(3)), tick
        assert all(simulation.at[node] == 1 for node in body.nodes), tick
    assert xs == [2, 3, 3, 4, 4, 4] and body.steps == 3 and simulation.at[(5, 0, 0)] == 2
    assert len(simulation.at) == 4
    # Without the anchor the whole body clicks on the face at the age 8.
    records.clear()
    simulation = RaySimulation(parse_ray_world(mover_world([])), records.append)
    body = simulation.measured[1]
    xs = []
    for _ in range(7):
        simulation.step()
        xs.append(body.position[0])
    assert xs == [2, 3, 3, 4, 4, 5, 5] and [r["event"] for r in records] == ["step"] * 3
    simulation.step()
    assert simulation.measured == {} and simulation.at == {}
    clicks = [r for r in records if r["event"] == "click"]
    assert [(r["detector"], r["node"], r["measured"], r["amount"]) for r in clicks] == [
        ("face:+x", [5, 0, 1], 1, 16)
    ]
    books = simulation.books()
    assert books["balanced"] and books["families"]["m"]["measured"]["escaped"] == 16
    # On a periodic axis the set wraps.
    simulation = RaySimulation(parse_ray_world(mover_world([], boundary={"x": "periodic"})))
    for _ in range(8):
        simulation.step()
    body = simulation.measured[1]
    assert body.position == (0, 0, 1) and body.nodes == ((0, 0, 0), (0, 0, 1), (0, 0, 2))
    assert set(simulation.at) == set(body.nodes)
    assert body_nodes((2, 0, 0), (1, 1, 3), (6, 1, 3), (False, False, True)) == (
        (2, 0, 2),
        (2, 0, 0),
        (2, 0, 1),
    )
    assert body_nodes((2, 0, 0), (1, 1, 3), (6, 1, 3), (False, False, False)) is None
    assert body_nodes((2, 0, 1), (1, 1, 1), (6, 1, 3), (False, False, False)) == ((2, 0, 1),)


# -- (c) ---------------------------------------------------------------------------


def born_by_node(simulation: RaySimulation, family: int) -> dict[int, int]:
    store = simulation.stores[family]
    fresh = store.age == 0
    found: dict[int, int] = {}
    for node, amount in zip(store.node[fresh].tolist(), store.amount[fresh].tolist(), strict=True):
        found[node] = found.get(node, 0) + amount
    return found


def test_the_books_balance_with_a_set_that_releases():
    """(c)."""
    body = {
        "position": [3, 1, 2],
        "family": "m",
        "amount": 16,
        "span": [1, 1, 3],
        "directions": [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]],
    }
    simulation = RaySimulation(parse_ray_world(world(shape=[7, 3, 5], release=[1, 4], measured=[body])))
    store = simulation.stores[M]
    nodes = [store.flat((3, 1, z)) for z in (1, 2, 3)]
    for tick in range(1, 21):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], tick
        assert simulation.books(recount=True) == books, tick
        if tick == 1:
            assert born_by_node(simulation, M) == dict(zip(nodes, (8, 4, 4), strict=True))
            assert simulation.ledger.transit_released[M] == 16 and store.size == 12
        if tick == 2:
            assert born_by_node(simulation, M) == dict(zip(nodes, (4, 8, 4), strict=True))
            assert simulation.ledger.transit_released[M] == 32
    assert simulation.measured[1].momentum == [0, 0, 0]
    # A lamp on a set: one unit per self-creation at the Nodes in turn.
    lamp = {
        "position": [1, 0, 0],
        "family": "light",
        "amount": 24,
        "fixed": True,
        "span": [3, 1, 1],
        "lamp": {"rate": [1, 1], "directions": [[0, 1, 0]]},
    }
    simulation = RaySimulation(parse_ray_world(world(shape=[3, 6, 1], K=24, measured=[lamp])))
    store = simulation.stores[LIGHT]
    for tick in range(1, 4):
        simulation.step()
        assert simulation.books()["balanced"], tick
    assert rows(simulation, LIGHT) == [
        (store.flat((0, 1, 0)), 4, 2, 0, 1, 1),
        (store.flat((1, 1, 0)), 4, 1, 1, 1, 1),
        (store.flat((2, 0, 0)), 4, 0, 2, 1, 1),
    ]
    entry = simulation.measured[1]
    assert entry.held == [0, 21] and entry.momentum == [0, -192, 0]
    assert simulation.transit_momentum() == [0, 192, 0]


# -- (f) ---------------------------------------------------------------------------


def refused(document: dict[str, object], text: str) -> None:
    with pytest.raises(ValueError, match=text):
        parse_ray_world(document)


def test_the_refusals_and_the_record(tmp_path):
    """(f)."""
    mover = {"position": [4, 1, 1], "family": "m", "amount": 16, "momentum": [1024, 0, 0]}
    base = world(measured=[mover])
    refused(world(measured=[{**mover, "span": "3"}]), "three odd integers")
    refused(
        world(measured=[{**mover, "span": [2, 1, 1]}]), "three odd integers from 1 \\(a centred body\\)"
    )
    refused(world(measured=[{**mover, "span": [0, 1, 1]}]), "from 1 through 12")
    refused(world(measured=[{**mover, "span": [1, 5, 1]}]), "from 1 through 3")
    refused(world(measured=[{**mover, "position": [0, 1, 1], "span": [3, 1, 1]}]), "leaves the board")
    refused(
        world(
            measured=[{**mover, "span": [3, 1, 1]}, {**mover, "position": [6, 1, 1], "span": [3, 1, 1]}]
        ),
        "share the Node \\[5, 1, 1\\]",
    )
    refused(
        world(
            measured=[{**mover, "fixed": True, "span": [3, 1, 1]}],
            detectors=[{"name": "d", "positions": [[5, 1, 1]]}],
        ),
        "a Node of a body on a set .* not its position",
    )
    parsed = parse_ray_world(
        world(boundary={"x": "periodic"}, measured=[{**mover, "position": [0, 1, 1], "span": [3, 1, 1]}])
    )
    assert parsed.measured[0].span == (3, 1, 1)
    assert parse_ray_world(base).measured[0].span == (1, 1, 1)
    # The record.
    wide = world(ticks=2, measured=[{**mover, "span": [1, 3, 1]}])
    path = tmp_path / "world.json"
    path.write_text(json.dumps(wide), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert record["status"] == "completed"
    assert record["numbers"]["1"] == {"position": [4, 1, 1], "family": "m", "span": [1, 3, 1]}
    assert record["measured"][0]["span"] == [1, 3, 1]
    state = json.loads((tmp_path / "run" / "state.json").read_text(encoding="utf-8"))
    assert state["measured"][0]["span"] == [1, 3, 1]
    path.write_text(json.dumps({**base, "ticks": 2}), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "plain").read_text(encoding="utf-8"))
    assert record["numbers"]["1"]["span"] == [1, 1, 1]
