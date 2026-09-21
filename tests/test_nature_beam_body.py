"""A body on a set of Nodes with one record, and the turn by momentum
(docs/BEAM_LAW.md, section 10, note 30; the model owner, 2026-09-20: the
electron of width 3, and "on Bohr, go, and put it as parameters outside
the GameBoard like the age"). A measured event declares `span`, three odd
extents centred on its position: its clock, its threshold and its push read
the one reading set summed over its Nodes, its releases are apportioned
whole over them, the step moves the whole set, no collision acts at any of
its Nodes. A measured event that declares `phase_by_momentum` in a world
with `action` (h) turns its phase at every Link it steps on an axis whose
momentum component is p by the difference of two floors of k x |p| x N / h,
k the count of Links the step rule gives at its age. Every rule is on the
measured-event side, the external thing; the rays' flight and collision are
untouched. The expected integers of docs/TEST_EXPECTATIONS.md ("A body on a
set and the turn by momentum"), written down first:

(a) a set of one Node is today's measured event bit for bit: a free body
    of `m` (content 16, momentum [256, 0, 0], phase 5) at (3, 1, 1) of an
    open 12 x 3 x 3 GameBoard at `release` [1, 4] (4 rays per heading per
    self-creation), a fixed counter of `light` at (9, 1, 1) measuring `m`
    in the `wave` detector `d`, a head-on pair of number 2 on +-y at x = 6
    that parks at (6, 1, 1) at the first interval and leaves on +-z; 30
    intervals: the body's x per interval 3 (4 times), 4 (5), 5 (5), 6 (5),
    7 (5), 8 (6); the body at (8, 1, 1), age 30, phase 5, 6 steps, held
    [16, 0]; the counter held [0, 4], 99 units clicked, momentum (-25344,
    0, 0), the record 37348285440 at phase 5; 152 clicks, 20 record lines,
    5 steps, 5 homes (the body stepping onto its own +x ray); the pair's
    clicks on face:-z (phase 40) and face:+z (phase 3) at tick 6; 25 rows
    of 102 units in the store; the transit line 2 + 740 = 102 + 521 + 119
    (since the crossing rule of 2026-09-21 the step precedes the law, so
    the body reads its own +x ray home in the interval of the step, one
    interval earlier, and one unit fewer leaves through the faces:
    73, 111, 112, 113, 112 through -x, +y, -y, +z, -z; 101 units, 522 escaped and 74,
    111, 111, 113, 113 until then); the same integers with `span` [1, 1,
    1] declared, every record equal;
(b) a set of three Nodes: a fixed body of `light` (content 4) at (4, 0, 1)
    of an open 9 x 1 x 3 bar with span [1, 1, 3] (the Nodes (4, 0, 0),
    (4, 0, 1), (4, 0, 2)) measuring `m` in the `wave` detector `d` of
    threshold 3, `suspension` [1, 1]: three rays of `m` (number 2, amount
    1, phase 0) arriving in one interval, one at each Node, are summed
    over the set: 3 clicks (the counter's events [3, 0], held [0, 4], the
    push (-768, 0, 0) = -4 x 3 x 64), one `record` line naming `d` with
    the record (3 x 32)^2 x 256^2 = 9 x 67108864, the presence 3 and the
    count 3, the owed count `by_clock(0, 3, 1)` = 3; two rays at two of
    the Nodes read the square 4 and click since 2026-09-20 (the `wave`
    threshold on the pointer's square), one ray alone passes (`threshold`
    3), no click, no push; the step: a free
    body of `m` (content 16, momentum [1024, 0, 0]) of span [1, 1, 3] at
    (2, 0, 1) of an open 6 x 1 x 3 bar steps at the ages 2, 4, 6 with all
    three Nodes (x per interval 2, 3, 3, 4, 4, 5, 5); with a fixed anchor
    at (5, 0, 0), a Node of the moved set at the age 6, the step is
    refused and the body stays at (4, 0, 1) with 3 steps counted, its
    momentum handed to the anchor (the contact of 2026-09-20); without
    it the step of the age 8 leaves the GameBoard and the whole body clicks
    on face:+x (one click, node (5, 0, 1), amount 16, the measured line's
    escaped 16, no measured event left); with x periodic it wraps to
    (0, 0, 1) with the Nodes (0, 0, 0), (0, 0, 1), (0, 0, 2); on a bar
    with z periodic of extent 3 the body at (2, 0, 0) is on (2, 0, 2),
    (2, 0, 0), (2, 0, 1) in that order;
(c) the books balance with a set that releases: a free body of `m`
    (content 16) of span [1, 1, 3] at (3, 1, 2) of an open 7 x 3 x 5
    GameBoard at `release` [1, 4] on the four headings +-X, +-Y (so that no
    ray of its own enters its set): 4 units per heading per self-creation
    placed whole over the three Nodes, 1 to every Node and the unit left
    to the Node of the largest claim (the `place` rows of the body's
    table, record 155 of 2026-09-20: the claims (1, 1, 1) -> (-2, 1, 1)
    -> (-1, -1, 2) -> (0, 0, 0) over the four headings, then again), so
    the rows born at the first interval sum to 6, 5, 5 units at (3, 1, 1),
    (3, 1, 2), (3, 1, 3), 16 in all, at the second 5, 6, 5 (until then
    the leftover went to the Node `age mod 3` on every row: 8, 4, 4 and
    4, 8, 4); the books balance at every one of 20 intervals and
    equal their recount; a lamp of `light` (content 24, K 24, rate
    [1, 1]) on +Y of span [3, 1, 1] at (1, 0, 0) of a 3 x 6 x 1 GameBoard
    releases its one unit at the self-creations whose turn is 1, at the
    Node of the largest claim (record 155: x = 0, x = 1, x = 2 in turn,
    whatever the ages; until then the Node counted from the age mod 3):
    since the fraction-free law (2026-09-20) the turn is the count of the
    turn's accumulator, 24 gives 1 at the age 0 (the unit at x = 0 costs
    1), 23 gives 0 at the age 1 (no release), 23 + 23 = 46 gives 1 at the
    age 2 (the remainder 22, the unit at x = 1 with the phase 1; at x = 2
    under the age mod 3): after 3 intervals the rows (0, 1, 0) age 2
    phase 0 and (1, 0, 0) age 0 phase 1, the content 22, the momentum
    (0, -128, 0), the transit line (0, 128, 0) and the claims (-1, -1, 2)
    (until then
    the whole part off the clock at the current content, `by_clock(age,
    content, 24)`, gave 1 at every age: the rows (0, 1, 0) age 2
    phase 0, (1, 1, 0) age 1 phase 1, (2, 0, 0) age 0 phase 2, held
    [0, 21], the recoil (0, -192, 0), the transit momentum (0, 192, 0);
(d) the turn: a free body of `m` (content 16, phase 5, K 2^20: the
    clock's turn 0) of momentum [1024, 0, 0] at x = 20 of an open
    40 x 1 x 1 bar steps at the ages 2, 4, 6, ... (k = age // 2): with
    `action` 65536 (|p| N / h = 1 per Link) its phase after 12 intervals
    is 5 + 6 = 11 and the rays born at tick 2 and at tick 3 carry 6
    (`release` [1, 16] on -X, away from the body's path; since the
    crossing rule of 2026-09-21 the step and its turn precede the law, so
    the release of the interval of a step carries the phase turned at the
    Link: 5 at tick 2 until then);
    with `action` 4096 (16 per Link) 5 + 96 mod 64 =
    37; with momentum [320, 0, 0] and `action` 7 (a remainder each step:
    the steps at the intervals 5, 9, 13, 17, 21, the floors of k x 20480
    / 7 = 2925, 5851, 8777, 11702, 14628) the phase after the intervals
    5, 9, 13, 17, 21, 24 is 50, 32, 14, 59, 41, 41; composed over axes,
    momentum [1024, 320, 0] with `action` 65536 on a 40 x 40 x 1 GameBoard
    (the x steps at the even ages, the y steps at 5, 9, 13, 17, 21: no
    step lost): the y turns floor(0.3125 k) - floor(0.3125 (k - 1)) = 0,
    0, 0, 1, 0, so the phase after 17 intervals is 5 + 8 + 1 = 14 and
    after 24 it is 5 + 12 + 1 = 18; the same worlds without `action` keep
    the phase 5 throughout;
(e) the GameBoard is unchanged by the two keys: 324 fixed rays of `light` on
    the periodic 8 x 8 x 4 GameBoard of `test_nature_beam_age` (e) (number 1, an
    anchor of `light` at (7, 7, 3) their home) with a free body of `m`
    (content 16, momentum [1024, 320, 0], span [1, 1, 3], `pass` for
    `light`, no release) run 40 intervals with `action` 7 and
    `phase_by_momentum` and again without them: the rays' sorted (Node,
    direction, phase, amount, content) rows are identical at every
    interval, the body's Nodes and steps are identical, its phase differs,
    the collision moved rays on the way and the body read rays;
(f) the refusals, naming the key: `action` 0, -1, "8", 1.5;
    `phase_by_momentum` without `action`, on a fixed measured event, on a
    family without a phase circle, not a boolean; `span` "3", [2, 1, 1],
    [0, 1, 1], [5, 1, 1] on an axis of 3, a body leaving the GameBoard on an
    open axis, two bodies sharing a Node, a detector naming a Node of a
    body that is not its position; the turn's bound: `ticks` 2^40 with
    the momentum 2^20 and N 64; accepted: `span` [3, 1, 1] at x = 0 of a
    periodic axis; the record carries `action`, `hypotheses` ["bohr-v1"]
    and per measured event `span` and `phase_by_momentum`, `action` None
    and `hypotheses` [] without the key, the state `span`;
(g) one set object shared by a body and a detector, and one moment table
    over the set (the four unifications, the model owner, 2026-09-20, (3),
    the data only; BEAM_LAW note 33; the integers written first): the body
    of (b) is a set with one measured event, its `DetectorSet.nodes` the
    map of its three Nodes to its number 1 and `Measured.nodes` the three
    in the fixed order, the source outside every detector a set of one
    Node mapped to 2, the engine's index mapping every Node to its set
    (`occupant` 1 at (4, 0, 2), None at (5, 0, 0)), two sets in all; two
    such bodies at (4, 0, 1) and (6, 0, 1) declared in one detector `d`
    are one set of six Nodes mapped to 1 and 2, each body's `nodes` its
    own three: three rays of `m` (number 3, phase 0) arriving at (4, 0,
    0), (6, 0, 1) and (6, 0, 2) read the threshold 3 over the set (the
    pointer 9 units) and click 1 at the first body and 2 at the second,
    the presence 1 and 2, the pushes (-256, 0, 0) and (-512, 0, 0), one
    `record` line naming `d` with the record 9 x 32^2 x 256^2 and no
    Node; the step of the body of (b) moves its Nodes in the set's map
    and in the index (x = 3 after two intervals, the three Nodes there),
    its escape empties both; the presence over a body without arrivals
    0; the one table with the two masks: a reader of `m` (content 4)
    reading a row of 3 units of a paid family of quantum 2 (content 2 per
    unit) on +x reads the flow 192 (3 x 64, the amount's weight) and the
    push (384, 0, 0) (3 x 2 x 64, the label's weight), the content 6;
    under `beam` at threshold 1 and `suspension` [1, 1] the rows of 3
    (phase 0) and 2 (phase 32) at two Nodes of the body pair 2 units and
    click 1: the presence and the count 5 (the units that go on are
    present), the owed count `by_clock(0, 5, 1)` = 5, the events [1, 0],
    the momentum (-256, 0, 0), the record 1, the store's rows 2 and 2.
"""

from __future__ import annotations

import json

import numpy as np
import pytest

from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.world import BOHR_RULE, body_nodes
from event_universe.runner import run_initialization
from tests.test_nature_beam_age import crowd

M, LIGHT = 0, 1
UNIT_RECORD = 32 * 32 * 256 * 256
FAMILIES = [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1}]


def world(**keys: object) -> dict[str, object]:
    base: dict[str, object] = {
        "law": "beam",
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


def beam(position: list[int], direction: list[int], number: int, phase: int = 0) -> dict[str, object]:
    return {
        "position": position,
        "family": "m",
        "number": number,
        "direction": direction,
        "amount": 1,
        "phase": phase,
    }


def rows(simulation: NatureBeamSimulation, family: int) -> list[tuple[int, ...]]:
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
PAIR = [beam([6, 0, 1], [0, 1, 0], 2, phase=3), beam([6, 2, 1], [0, -1, 0], 2, phase=40)]


def one_node_world(body: dict[str, object]) -> dict[str, object]:
    return world(
        release=[1, 4],
        measured=[body, COUNTER],
        in_transit=PAIR,
        detectors=[{"name": "d", "positions": [[9, 1, 1]], "threshold": 1, "reading": "wave"}],
    )


def run_one_node(
    body: dict[str, object],
) -> tuple[NatureBeamSimulation, list[dict[str, object]], list[int]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(one_node_world(body)), records.append)
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
    # The step of tick 30 onto the counter is refused and is a contact: the
    # body's 256 handed to the counter (until 2026-09-20 the body kept it
    # and the counter read -25344).
    assert (body.age, body.phase, body.momentum, body.steps, body.held) == (
        30,
        5,
        [0, 0, 0],
        6,
        [16, 0],
    )
    assert counter.held == [0, 4] and counter.clicks == [99, 0] and counter.contacts == [1, 0]
    assert counter.momentum == [-25344 + 256, 0, 0]
    assert counter.detector_set.record == [37348285440, 0] and counter.detector_set.phase == [5, None]
    kinds = {
        kind: sum(1 for r in records if r["event"] == kind)
        for kind in ("click", "record", "step", "home", "contact")
    }
    assert kinds == {"click": 152, "record": 20, "step": 5, "home": 5, "contact": 1}
    assert [(r["tick"], r["component"], r["occupant"]) for r in records if r["event"] == "contact"] == [
        (30, 256, 2)
    ]
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
    assert store.size == 25 and int(store.amount.sum()) == 102
    transit = simulation.books()["families"]["m"]["transit"]
    assert transit == {
        "initial": 2,
        "released": 740,
        "current": 102,
        "escaped": 521,
        "absorbed": 119,
        "balanced": True,
    }
    assert {port: units[M] for port, units in simulation.ledger.face_amount.items()} == {
        0: 0,
        1: 73,
        2: 111,
        3: 112,
        4: 113,
        5: 112,
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


def set_world(beams: list[dict[str, object]], suspension: object = 0) -> dict[str, object]:
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
        in_transit=beams,
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
    three = [beam([3, 0, z], [1, 0, 0], 2) for z in range(3)]
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(set_world(three, suspension=[1, 1])), records.append
    )
    body = simulation.measured[1]
    assert body.span == (1, 1, 3) and body.nodes == SET_NODES
    assert {node: simulation.occupant(node) for node in SET_NODES} == dict.fromkeys(SET_NODES, 1)
    simulation.step()
    assert simulation.books()["balanced"]
    assert body.clicks == [3, 0] and body.held == [0, 4] and body.momentum == [-768, 0, 0]
    assert body.presence == 3 and body.counted == 3
    assert body.owed == by_clock(0, 3, 1) == 3
    assert body.detector_set.record == [9 * UNIT_RECORD, 0] and body.phase == 0
    lines = [r for r in records if r["event"] == "record"]
    assert len(lines) == 1 and lines[0]["detector"] == "d" and lines[0]["record"] == 9 * UNIT_RECORD
    assert [r["node"] for r in records if r["event"] == "click"] == [[4, 0, 1]] * 3
    assert simulation.stores[M].size == 0
    # A smaller set passes: the threshold reads the pointer's square over
    # the set (one ray, 1 < 3; two rays in phase would read 4 and click).
    records.clear()
    simulation = NatureBeamSimulation(parse_nature_beam_world(set_world(three[:1])), records.append)
    simulation.step()
    assert simulation.books()["balanced"]
    assert [(r["event"], r["threshold"]) for r in records] == [("pass", 3)]
    body = simulation.measured[1]
    assert body.clicks == [0, 0] and body.momentum == [0, 0, 0] and body.detector_set.record == [0, 0]
    assert simulation.stores[M].size == 1
    # The step moves the whole set; a Node of the moved set held by another
    # measured event refuses it.
    anchor = {"position": [5, 0, 0], "family": "m", "amount": 1, "fixed": True}
    simulation = NatureBeamSimulation(parse_nature_beam_world(mover_world([anchor])))
    body = simulation.measured[1]
    xs = []
    for tick in range(1, 7):
        simulation.step()
        assert simulation.books()["balanced"], tick
        xs.append(body.position[0])
        assert body.nodes == tuple((body.position[0], 0, z) for z in range(3)), tick
        assert all(simulation.occupant(node) == 1 for node in body.nodes), tick
    assert xs == [2, 3, 3, 4, 4, 4] and body.steps == 3 and simulation.occupant((5, 0, 0)) == 2
    assert len(simulation.at) == 4
    # The refused step is a contact: the body's x component handed to the anchor.
    assert body.momentum == [0, 0, 0] and simulation.measured[2].momentum == [1024, 0, 0]
    assert simulation.measured[2].contacts == [1, 0]
    # Without the anchor the whole body clicks on the face at the age 8.
    records.clear()
    simulation = NatureBeamSimulation(parse_nature_beam_world(mover_world([])), records.append)
    body = simulation.measured[1]
    xs = []
    for _ in range(7):
        simulation.step()
        xs.append(body.position[0])
    assert xs == [2, 3, 3, 4, 4, 5, 5] and [r["event"] for r in records] == ["step"] * 3
    assert [r["phase"] for r in records] == [0, 0, 0]
    simulation.step()
    assert simulation.measured == {} and simulation.at == {}
    clicks = [r for r in records if r["event"] == "click"]
    assert [(r["detector"], r["node"], r["measured"], r["amount"]) for r in clicks] == [
        ("face:+x", [5, 0, 1], 1, 16)
    ]
    books = simulation.books()
    assert books["balanced"] and books["families"]["m"]["measured"]["escaped"] == 16
    # On a periodic axis the set wraps.
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(mover_world([], boundary={"x": "periodic"}))
    )
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


def born_by_node(simulation: NatureBeamSimulation, family: int) -> dict[int, int]:
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
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world(shape=[7, 3, 5], release=[1, 4], measured=[body]))
    )
    store = simulation.stores[M]
    nodes = [store.flat((3, 1, z)) for z in (1, 2, 3)]
    for tick in range(1, 21):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], tick
        assert simulation.books(recount=True) == books, tick
        # The placement by the Nodes' claims (`place_over_nodes`, record
        # 155 of 2026-09-20): each heading's 4 units give 1 to every Node
        # and the unit left to the Node of the largest claim, the claims
        # (1, 1, 1) -> (-2, 1, 1) -> (-1, -1, 2) -> (0, 0, 0) -> (1, 1, 1)
        # over the four headings, so the first interval places 6, 5, 5
        # and the second 5, 6, 5 (8, 4, 4 and 4, 8, 4 until then, the
        # leftover to the Node `age mod 3` on every row).
        if tick == 1:
            assert born_by_node(simulation, M) == dict(zip(nodes, (6, 5, 5), strict=True))
            assert simulation.ledger.transit_released[M] == 16 and store.size == 12
            assert simulation.measured[1].counts.values("place") == [-2, 1, 1]
        if tick == 2:
            assert born_by_node(simulation, M) == dict(zip(nodes, (5, 6, 5), strict=True))
            assert simulation.ledger.transit_released[M] == 32
            assert simulation.measured[1].counts.values("place") == [-1, -1, 2]
    assert simulation.measured[1].momentum == [0, 0, 0]
    # A lamp on a set: one unit per self-creation at the Nodes in turn of
    # their claims (`place_over_nodes`: x = 0, then x = 1, then x = 2,
    # whatever the ages of the self-creations that release; until record
    # 155 the Node counted from the age mod 3).
    lamp = {
        "position": [1, 0, 0],
        "family": "light",
        "amount": 24,
        "fixed": True,
        "span": [3, 1, 1],
        "lamp": {"wheel": [1, 64], "rate": [1, 1], "directions": [[0, 1, 0]]},
    }
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world(shape=[3, 6, 1], K=24, measured=[lamp]))
    )
    store = simulation.stores[LIGHT]
    for tick in range(1, 4):
        simulation.step()
        assert simulation.books()["balanced"], tick
    assert rows(simulation, LIGHT) == [
        (store.flat((0, 1, 0)), 4, 2, 0, 1, 1),
        (store.flat((1, 0, 0)), 4, 0, 1, 1, 1),
    ]
    entry = simulation.measured[1]
    assert entry.held == [0, 22] and entry.momentum == [0, -128, 0]
    assert entry.turned == 2 and entry.acc_turn == 22
    assert entry.counts.values("place") == [-1, -1, 2]
    assert simulation.transit_momentum() == [0, 128, 0]


# -- (d) ---------------------------------------------------------------------------


def turning_world(momentum: list[int], action: int | None, **keys: object) -> dict[str, object]:
    body = {
        "position": [20, 0, 0],
        "family": "m",
        "amount": 16,
        "phase": 5,
        "momentum": momentum,
        "directions": [[-1, 0, 0]],
        "phase_by_momentum": action is not None,
    }
    document = world(measured=[body], ticks=24, **{"shape": [40, 1, 1], **keys})
    if action is not None:
        document["action"] = action
    return document


def phases(document: dict[str, object], ticks: int) -> tuple[list[int], list[int], NatureBeamSimulation]:
    simulation = NatureBeamSimulation(parse_nature_beam_world(document))
    entry = simulation.measured[1]
    found, xs = [], []
    for tick in range(1, ticks + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
        found.append(entry.phase)
        xs.append(entry.position[0])
    return found, xs, simulation


def test_a_body_turns_its_phase_by_its_momentum_at_every_link_it_steps():
    """(d)."""
    assert [by_clock(k, 320 * 64, 7) for k in range(5)] == [2925, 2926, 2926, 2925, 2926]
    assert [(k * 20480) // 7 for k in range(1, 6)] == [2925, 5851, 8777, 11702, 14628]
    # One step of the circle per Link: k = age // 2.
    turned, xs, simulation = phases(turning_world([1024, 0, 0], 65536, release=[1, 16]), 12)
    assert xs == [20 + (tick // 2) for tick in range(1, 13)] and xs[-1] == 26
    assert turned == [5 + (tick // 2) for tick in range(1, 13)] and turned[-1] == 11
    store = simulation.stores[M]
    born_at = {2: 6, 3: 6}
    for tick, phase in born_at.items():
        age = 12 - tick
        assert set(store.phase[store.age == age].tolist()) == {phase}, tick
    # Sixteen steps per Link.
    turned, _, _ = phases(turning_world([1024, 0, 0], 4096), 12)
    assert turned[-1] == (5 + 6 * 16) % 64 == 37
    # A remainder each step: the steps at 5, 9, 13, 17, 21.
    turned, xs, _ = phases(turning_world([320, 0, 0], 7), 24)
    assert [xs[t - 1] for t in (4, 5, 9, 13, 17, 21, 24)] == [20, 21, 22, 23, 24, 25, 25]
    assert [turned[t - 1] for t in (4, 5, 9, 13, 17, 21, 24)] == [5, 50, 32, 14, 59, 41, 41]
    assert turned[-1] == (5 + 14628) % 64
    # The axes compose: x steps at the even ages, y at 5, 9, 13, 17, 21.
    document = turning_world([1024, 320, 0], 65536, shape=[40, 40, 1])
    document["measured"][0]["position"] = [4, 4, 0]  # type: ignore[index]
    turned, _, simulation = phases(document, 24)
    assert simulation.measured[1].position == (16, 9, 0)
    assert turned[16] == 14 and turned[23] == 18
    # Without `action` the phase is today's: the clock's turn alone, 0.
    for momentum in ([1024, 0, 0], [320, 0, 0]):
        turned, _, _ = phases(turning_world(momentum, None), 24)
        assert turned == [5] * 24


# -- (e) ---------------------------------------------------------------------------


def torus(turning: bool) -> dict[str, object]:
    anchor = {"position": [7, 7, 3], "family": "light", "amount": 1, "fixed": True}
    body = {
        "position": [0, 0, 0],
        "family": "m",
        "amount": 16,
        "phase": 5,
        "momentum": [1024, 320, 0],
        "span": [1, 1, 3],
        "table": {"light": "pass"},
        "phase_by_momentum": turning,
    }
    document = world(
        shape=[8, 8, 4],
        boundary={"x": "periodic", "y": "periodic", "z": "periodic"},
        ticks=40,
        age_bound=128,
        directions=[[1, 1, 0], [2, -1, 1]],
        families=[{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1, "phase_per_link": 5}],
        measured=[anchor, body],
        in_transit=crowd(),
    )
    if turning:
        document["action"] = 7
    return document


def game_board(simulation: NatureBeamSimulation) -> np.ndarray:
    store = simulation.stores[LIGHT]
    found = np.stack([store.node, store.direction, store.phase, store.amount, store.content], axis=1)
    return found[np.lexsort(found.T[::-1])]


def test_the_game_board_is_unchanged_by_the_two_keys():
    """(e)."""
    with_keys = NatureBeamSimulation(parse_nature_beam_world(torus(True)))
    without = NatureBeamSimulation(parse_nature_beam_world(torus(False)))
    collided = False
    phases_differed = False
    read = 0
    for _ in range(40):
        before = with_keys.stores[LIGHT].direction.copy()
        with_keys.step()
        without.step()
        assert np.array_equal(game_board(with_keys), game_board(without))
        turning, plain = with_keys.measured[2], without.measured[2]
        assert turning.nodes == plain.nodes and turning.steps == plain.steps
        collided = collided or before.shape != with_keys.stores[LIGHT].direction.shape
        collided = collided or bool((before != with_keys.stores[LIGHT].direction).any())
        phases_differed = phases_differed or turning.phase != plain.phase
        read += turning.presence
    assert collided and phases_differed and read > 0 and turning.steps > 0
    assert plain.phase == 5


# -- (f) ---------------------------------------------------------------------------


def refused(document: dict[str, object], text: str) -> None:
    with pytest.raises(ValueError, match=text):
        parse_nature_beam_world(document)


def test_the_refusals_and_the_record(tmp_path):
    """(f)."""
    mover = {"position": [4, 1, 1], "family": "m", "amount": 16, "momentum": [1024, 0, 0]}
    base = world(measured=[mover])
    for bad in (0, -1, "8", 1.5):
        refused({**base, "action": bad}, "action must be an integer from 1")
    refused(
        world(measured=[{**mover, "phase_by_momentum": True}]),
        "phase_by_momentum needs the world's `action`",
    )
    refused(
        world(action=64, measured=[{**mover, "phase_by_momentum": True, "fixed": True}]),
        "refused on a fixed measured event",
    )
    refused(
        world(
            action=64,
            families=[{"name": "m", "quantum": 0, "phase": False}, FAMILIES[1]],
            measured=[{**mover, "phase_by_momentum": True}],
        ),
        "without a phase circle",
    )
    refused(world(action=64, measured=[{**mover, "phase_by_momentum": 1}]), "must be true or false")
    refused(world(measured=[{**mover, "span": "3"}]), "three odd integers")
    refused(
        world(measured=[{**mover, "span": [2, 1, 1]}]), "three odd integers from 1 \\(a centred body\\)"
    )
    refused(world(measured=[{**mover, "span": [0, 1, 1]}]), "from 1 through 12")
    refused(world(measured=[{**mover, "span": [1, 5, 1]}]), "from 1 through 3")
    refused(
        world(measured=[{**mover, "position": [0, 1, 1], "span": [3, 1, 1]}]), "leaves the GameBoard"
    )
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
    refused(
        world(
            action=64,
            ticks=1 << 40,
            measured=[{**mover, "momentum": [1 << 20, 0, 0], "phase_by_momentum": True}],
        ),
        "turn by momentum forms k x \\|p\\| x N up to .* beyond the integer bound",
    )
    parsed = parse_nature_beam_world(
        world(boundary={"x": "periodic"}, measured=[{**mover, "position": [0, 1, 1], "span": [3, 1, 1]}])
    )
    assert parsed.measured[0].span == (3, 1, 1) and parsed.action is None
    assert parse_nature_beam_world(base).measured[0].span == (1, 1, 1)
    assert not parse_nature_beam_world(base).measured[0].phase_by_momentum
    # The record.
    turning = world(
        action=64, ticks=2, measured=[{**mover, "span": [1, 3, 1], "phase_by_momentum": True}]
    )
    path = tmp_path / "world.json"
    path.write_text(json.dumps(turning), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert (
        record["action"] == 64
        and record["hypotheses"] == [BOHR_RULE]
        and record["status"] == "completed"
    )
    # `become` per number since 2026-09-20 (the transformation): None without.
    assert record["numbers"]["1"] == {
        "position": [4, 1, 1],
        "family": "m",
        "span": [1, 3, 1],
        "phase_by_momentum": True,
        "become": None,
    }
    assert record["measured"][0]["span"] == [1, 3, 1]
    state = json.loads((tmp_path / "run" / "state.json").read_text(encoding="utf-8"))
    assert state["measured"][0]["span"] == [1, 3, 1]
    path.write_text(json.dumps({**base, "ticks": 2}), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "plain").read_text(encoding="utf-8"))
    assert record["action"] is None and record["hypotheses"] == []
    assert (
        record["numbers"]["1"]["span"] == [1, 1, 1]
        and record["numbers"]["1"]["phase_by_momentum"] is False
    )


def test_one_set_object_shared_by_a_body_and_a_detector_and_one_table_over_it():
    """(g)."""
    three = [beam([3, 0, z], [1, 0, 0], 2) for z in range(3)]
    simulation = NatureBeamSimulation(parse_nature_beam_world(set_world(three)))
    body, source = simulation.measured[1], simulation.measured[2]
    assert body.detector_set.nodes == dict.fromkeys(SET_NODES, 1) and body.nodes == SET_NODES
    assert body.detector_set.name == "d" and body.detector_set.numbers == [1]
    assert source.detector_set.nodes == {(8, 0, 1): 2} and source.nodes == ((8, 0, 1),)
    assert (
        simulation.at[(4, 0, 1)] is body.detector_set and simulation.at[(8, 0, 1)] is source.detector_set
    )
    assert simulation.occupant((4, 0, 2)) == 1 and simulation.occupant((5, 0, 0)) is None
    assert len(simulation.detector_sets) == 2 and len(simulation.at) == 4
    # Several measured events in one set: two bodies of three Nodes each.
    document = set_world(
        [beam([3, 0, 0], [1, 0, 0], 3), beam([5, 0, 1], [1, 0, 0], 3), beam([5, 0, 2], [1, 0, 0], 3)]
    )
    measured = document["measured"]
    assert isinstance(measured, list)
    second = {**measured[0], "position": [6, 0, 1]}
    measured.insert(1, second)
    detectors = document["detectors"]
    assert isinstance(detectors, list)
    detectors[0]["positions"] = [[4, 0, 1], [6, 0, 1]]
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), records.append)
    first, second_body = simulation.measured[1], simulation.measured[2]
    assert first.detector_set is second_body.detector_set
    assert first.detector_set.nodes == {
        **dict.fromkeys(SET_NODES, 1),
        (6, 0, 0): 2,
        (6, 0, 1): 2,
        (6, 0, 2): 2,
    }
    assert second_body.nodes == ((6, 0, 0), (6, 0, 1), (6, 0, 2))
    simulation.step()
    assert simulation.books()["balanced"]
    assert (first.clicks, second_body.clicks) == ([1, 0], [2, 0])
    assert (first.presence, second_body.presence) == (1, 2)
    assert (first.momentum, second_body.momentum) == ([-256, 0, 0], [-512, 0, 0])
    lines = [r for r in records if r["event"] == "record"]
    assert len(lines) == 1 and lines[0]["detector"] == "d" and lines[0]["record"] == 9 * UNIT_RECORD
    assert lines[0]["node"] is None and lines[0]["measured"] is None
    # The step moves the body's Nodes in the set's map and in the index;
    # the escape empties both; a body without arrivals reads the presence 0.
    simulation = NatureBeamSimulation(parse_nature_beam_world(mover_world([])))
    body = simulation.measured[1]
    simulation.step()
    assert body.presence == 0 and body.counted == 0
    simulation.step()
    assert body.position == (3, 0, 1)
    assert body.detector_set.nodes == {(3, 0, 0): 1, (3, 0, 1): 1, (3, 0, 2): 1}
    assert set(simulation.at) == set(body.nodes) and body.nodes == ((3, 0, 0), (3, 0, 1), (3, 0, 2))
    for _ in range(6):
        simulation.step()
    assert simulation.measured == {} and simulation.at == {} and body.detector_set.nodes == {}
    # The one table with the two masks: the reading with the amount's
    # weight, the push with the label's weight (content x amount for a
    # paid family).
    reader = {
        "position": [4, 0, 1],
        "family": "m",
        "amount": 4,
        "fixed": True,
        "table": {"light": "read"},
    }
    lamp_side = {"position": [8, 0, 1], "family": "light", "amount": 4, "fixed": True}
    row = {
        "position": [3, 0, 1],
        "family": "light",
        "number": 2,
        "direction": [1, 0, 0],
        "amount": 3,
        "phase": 0,
    }
    records = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(
            world(
                shape=[9, 1, 3],
                families=[{"name": "m", "quantum": 0}, {"name": "light", "quantum": 2}],
                measured=[reader, lamp_side],
                in_transit=[row],
            )
        ),
        records.append,
    )
    simulation.step()
    assert simulation.books()["balanced"]
    reads = [r for r in records if r["event"] == "read"]
    assert len(reads) == 1 and reads[0]["amount"] == 3 and reads[0]["content"] == 6
    assert reads[0]["push"] == [384, 0, 0] and reads[0]["reading"] == [192, 0, 0]
    assert simulation.measured[1].momentum == [384, 0, 0] and simulation.measured[1].presence == 3
    # `beam`'s pairing splits a row: the units that go on are present for
    # the clock, the units that click are the admitted rows.
    document = set_world(
        [
            {**beam([3, 0, 0], [1, 0, 0], 2), "amount": 3},
            {**beam([3, 0, 2], [1, 0, 0], 2, phase=32), "amount": 2},
        ],
        suspension=[1, 1],
    )
    detectors = document["detectors"]
    assert isinstance(detectors, list)
    detectors[0].update({"reading": "beam", "threshold": 1})
    records = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), records.append)
    body = simulation.measured[1]
    simulation.step()
    assert simulation.books()["balanced"]
    assert (body.presence, body.counted, body.owed) == (5, 5, by_clock(0, 5, 1))
    assert body.clicks == [1, 0] and body.momentum == [-256, 0, 0]
    assert body.detector_set.record == [1, 0] and body.detector_set.phase == [0, None]
    assert [r["amount"] for r in records if r["event"] == "click"] == [1]
    assert [r["amount"] for r in records if r.get("cancelled")] == [2, 2]
    assert sorted(simulation.stores[M].amount.tolist()) == [2, 2]
