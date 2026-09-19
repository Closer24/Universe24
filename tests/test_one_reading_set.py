"""One reading set for every coupling (Highlights 5.4, the model owner,
2026-09-19: "everything present at the Node but the reader's own number,
including here"): the presence a reader reads, the flow a measured event is
pushed by, the amount a detector's threshold gates and the phase its window
reads are all formed over the same set, every number at the Node but the
reader's own, and the seventh exit, here, counts in it: the units waiting
at a Node as arrivals (as before) and the content of the measured event at
the Node under its number (new); a measured event's own content and its own
number's units coming home are its own number and are never read. The
expected integers of docs/TEST_EXPECTATIONS.md ("One reading set"), written
down first. K 2^20 so that no phase moves, `release` [0, 1].

(a) presence: (1) a bar of 9 x 1 x 1 at `suspension` [1, 4], three lamps
    of light (content 1) at x = 0, 8 and 7 as the numbers 1, 2 and 3; at
    x = 4 64 units of number 1 on +X and 16 of number 2 on -X, at x = 3 one
    unit of number 3 on +X. Interval 1: number 1 reads 16 and carries 4,
    number 2 reads 64 and carries 16 (3 and 15 after the cycle pays one).
    Interval 2: the lone unit of number 3 arrives at x = 4 beside the 80
    waiting units and reads them, 80 x 1 // 4 = 20 (19 after the payment;
    the counts at x = 4 then 2, 14, 19, the arrivals 64, 16, 1, as before
    this change). (2) a measured event of `m` (content 2^10, number 1,
    passing light) at x = 4 and a lamp of light (content 1, number 2) at
    x = 8; one unit of light of number 2 at x = 3 on +X. Interval 2: the
    unit passes the measured event and reads its content, here,
    1024 x 1 // 4 = 256 (255 after the payment), and is held there; the
    measured event, after its self-creation (age 2), reads the unit, 1,
    and owes 1 x 1 // 4 = 0 (until this change the unit read 0);
(b) the push: a phase-less free family `m` on 9 x 3 x 3, `suspension` 0,
    sources of content 16 at x = 0 (number 1) and x = 8 (number 2), a
    reader of content 4 at x = 4 (number 3, `read`); at the reader 9 units
    of number 1 on +X, 9 of number 2 on -X and 5 of its own number 3 on +X
    arriving in interval 1. The flows (9, 0, 0) and (-9, 0, 0) push -4 x
    each, (-36, 0, 0) + (36, 0, 0) = (0, 0, 0): the push taken (0, 0, 0),
    18 read, 5 home (not read, not content: the content stays 4), the 5
    created again at the self-creation of the same interval whole on +X
    (the heading its clock points at, age 0 mod 6), the two others'
    departures 18; the 9 of number 1 alone push (-36, 0, 0); the 9 of
    number 1 with the 5 of the own number push (-36, 0, 0), the own adding
    nothing, 5 home;
(c) the threshold and the window: a receiver of `m` (content 4, number 1)
    measuring light in the detector `d` of threshold 3, lamps of light
    (content 4) at x = 0 (number 2) and x = 8 (number 3); 2 units of number
    2 on +X and 1 unit of number 3 on -X arrive in interval 1: the set is 3,
    at the threshold, and clicks: `events` [0, 3], `held` [4, 3] (a seeded
    unit carries one phase step of content), the push the carried momenta
    (2, 0, 0) + (-1, 0, 0) = (1, 0, 0), the detector's report 3 measured
    and 3 clicks, nothing left in transit, two click records in rank
    order, number 2 (amount 2, push (2, 0, 0), content 2) and number 3
    (amount 1, push (-1, 0, 0), content 1), each with the set's phase 0;
    the 2 alone are below the threshold and pass, leaving whole on +X; the
    window: the receiver measuring light through the window 32 at
    threshold 1, the 2 units of number 2 at phase 0 and the unit of number
    3 at phase 32: the set's phase is that of 45 at 0 and 32 at 32 (in
    32nds, isqrt(2 x 1024) = 45), 13 x 256 on the cosine axis, step 0,
    outside the window 32: both pass with a `pass` record each (phase 0,
    window 32) and the 3 units mix on, while the unit of number 3 alone
    (phase 32) clicks with phase 32: the detector reads the set, not one
    number;
(d) the own number excluded everywhere: a measured event of light (content
    2^10, number 1, passing light) at x = 4 on the bar at `suspension`
    [1, 1] and a lamp of light (content 1, number 2) at x = 8; at x = 4 one
    unit of number 1 on +X (home) and one unit of number 2 on -X arrive in
    interval 1: the measured event reads the unit of number 2 only and owes
    1 (its content 1024 and its homing unit excluded), the unit of number 2
    reads 1024 + 1 = 1025 (1024 after the payment), the homing unit is
    taken with no count (1 home, created again on +X); and at the detector
    of (c), 2 units of number 2 with 5 units of the receiver's own number 1
    make a set of 2, below 3: no click, 5 home (the content 4 unchanged),
    the 5 created again whole on +X with their content 5, the 2 mixing on.
"""

from __future__ import annotations

from event_universe.events import EventSimulation, parse_event_world

PLUS_X, MINUS_X = 0, 1
M, LIGHT = 0, 1
NODE = [4, 1, 1]
NO_RESPONSE = {"home": 0, "read": 0, "measure": 0, "rerelease": 0}
FAMILIES = [{"name": "m", "kind": "free", "phase": False}, {"name": "light", "kind": "paid"}]


def world(
    shape: list[int],
    families: list[dict[str, object]],
    measured: list[dict[str, object]],
    in_transit: list[dict[str, object]],
    suspension: object = 0,
    detectors: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "one-reading-set-test",
        "shape": shape,
        "boundary": "open",
        "ticks": 3,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": suspension,
        "families": families,
        "measured": measured,
        "in_transit": in_transit,
        "detectors": detectors or [],
    }


def fixed(position: list[int], family: str, amount: int, **keys: object) -> dict[str, object]:
    return {"position": position, "family": family, "amount": amount, "fixed": True, **keys}


def unit(
    position: list[int], family: str, number: int, heading: list[int], amount: int, phase: int = 0
) -> dict[str, object]:
    return {
        "position": position,
        "family": family,
        "number": number,
        "heading": heading,
        "amount": amount,
        "phase": phase,
    }


def test_the_presence_counts_the_waiting_units_and_the_measured_content_here():
    """(a)."""
    lamps = [
        fixed([0, 0, 0], "light", 1, table={"light": "pass"}),
        fixed([8, 0, 0], "light", 1, table={"light": "pass"}),
        fixed([7, 0, 0], "light", 1, table={"light": "pass"}),
    ]
    in_transit = [
        unit([4, 0, 0], "light", 1, [1, 0, 0], 64),
        unit([4, 0, 0], "light", 2, [-1, 0, 0], 16),
        unit([3, 0, 0], "light", 3, [1, 0, 0], 1),
    ]
    simulation = EventSimulation(
        parse_event_world(world([9, 1, 1], FAMILIES, lamps, in_transit, [1, 4]))
    )
    light = simulation.transits[LIGHT]
    assert light.rank == {1: 0, 2: 1, 3: 2}
    simulation.step()
    assert simulation.books()["balanced"]
    assert light.suspended[4, 0, 0].tolist() == [3, 15, 0]
    simulation.step()
    assert simulation.books()["balanced"]
    assert light.suspended[4, 0, 0].tolist() == [2, 14, 19]
    assert light.arr_amt[4, 0, 0].sum(axis=-1).tolist() == [64, 16, 1]

    measured = [
        fixed([4, 0, 0], "m", 1 << 10, table={"light": "pass"}),
        fixed([8, 0, 0], "light", 1, table={"light": "pass"}),
    ]
    simulation = EventSimulation(
        parse_event_world(
            world([9, 1, 1], FAMILIES, measured, [unit([3, 0, 0], "light", 2, [1, 0, 0], 1)], [1, 4])
        )
    )
    light, entry = simulation.transits[LIGHT], simulation.measured[1]
    for _ in range(2):
        simulation.step()
        assert simulation.books()["balanced"]
    assert int(light.suspended[4, 0, 0, light.rank[2]]) == 255
    assert int(light.arr_amt[4, 0, 0, light.rank[2], PLUS_X]) == 1 and int(light.fly_amt.sum()) == 0
    assert entry.age == 2 and entry.owed == 0 and entry.held == [1 << 10, 0]


def test_the_push_reads_the_flow_of_every_number_but_the_readers_own():
    """(b)."""
    families = [FAMILIES[M]]
    measured = [fixed([0, 1, 1], "m", 16), fixed([8, 1, 1], "m", 16), fixed(NODE, "m", 4)]
    first = unit(NODE, "m", 1, [1, 0, 0], 9)
    second = unit(NODE, "m", 2, [-1, 0, 0], 9)
    own = unit(NODE, "m", 3, [1, 0, 0], 5)
    for in_transit, push, read, home in (
        ([first, second, own], [0, 0, 0], 18, 5),
        ([first], [-36, 0, 0], 9, 0),
        ([first, own], [-36, 0, 0], 9, 5),
    ):
        simulation = EventSimulation(parse_event_world(world([9, 3, 3], families, measured, in_transit)))
        reader, transit = simulation.measured[3], simulation.transits[M]
        assert transit.rank == {1: 0, 2: 1, 3: 2}
        simulation.step()
        assert simulation.books()["balanced"], in_transit
        assert reader.pushed == push and reader.momentum == push, in_transit
        assert reader.measured[M] == {**NO_RESPONSE, "read": read, "home": home}, in_transit
        assert reader.held == [4] and reader.home == [0] and reader.age == 1, in_transit
        # What came home is created again whole on +X (age 0 mod 6), not read.
        assert transit.fly_amt[4, 1, 1, transit.rank[3]].tolist() == [home, 0, 0, 0, 0, 0], in_transit
        assert int(transit.fly_amt[4, 1, 1, :2].sum()) == read, in_transit
        assert int(transit.arr_amt.sum()) == 0, in_transit


def test_a_detectors_threshold_and_window_read_the_set_of_every_number_but_its_own():
    """(c)."""
    sources = [fixed([0, 1, 1], "light", 4), fixed([8, 1, 1], "light", 4)]
    detector = [{"name": "d", "positions": [NODE], "threshold": 3}]
    two = unit(NODE, "light", 2, [1, 0, 0], 2)
    one = unit(NODE, "light", 3, [-1, 0, 0], 1)
    receiver = fixed(NODE, "m", 4, table={"light": "measure"})
    records: list[dict[str, object]] = []
    simulation = EventSimulation(
        parse_event_world(world([9, 3, 3], FAMILIES, [receiver, *sources], [two, one], 0, detector)),
        records.append,
    )
    entry, light = simulation.measured[1], simulation.transits[LIGHT]
    assert entry.threshold == 3 and light.rank == {2: 0, 3: 1}
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 3] and entry.held == [4, 3]
    assert entry.momentum == [1, 0, 0] and entry.pushed == [1, 0, 0]
    assert entry.measured[LIGHT] == {**NO_RESPONSE, "measure": 3}
    assert simulation.detectors()[0]["families"]["light"] == {"measured": 3, "clicks": 3}
    assert int(light.arr_amt.sum()) == 0 and int(light.fly_amt.sum()) == 0
    common = {"event": "click", "tick": 1, "node": NODE, "measured": 1, "detector": "d"}
    common.update({"family": "light", "phase": 0})
    assert records == [
        {**common, "number": 2, "amount": 2, "push": [2, 0, 0], "content": 2},
        {**common, "number": 3, "amount": 1, "push": [-1, 0, 0], "content": 1},
    ]

    records.clear()
    simulation = EventSimulation(
        parse_event_world(world([9, 3, 3], FAMILIES, [receiver, *sources], [two], 0, detector)),
        records.append,
    )
    entry, light = simulation.measured[1], simulation.transits[LIGHT]
    simulation.step()
    assert simulation.books()["balanced"] and records == []
    assert entry.events == [0, 0] and entry.held == [4, 0] and entry.momentum == [0, 0, 0]
    assert int(light.fly_amt[4, 1, 1, light.rank[2], PLUS_X]) == 2 and int(light.fly_amt.sum()) == 2

    gate = fixed(NODE, "m", 4, table={"light": {"rule": "measure", "phase_window": 32}})
    late = unit(NODE, "light", 3, [-1, 0, 0], 1, phase=32)
    records.clear()
    simulation = EventSimulation(
        parse_event_world(world([9, 3, 3], FAMILIES, [gate, *sources], [two, late])), records.append
    )
    entry, light = simulation.measured[1], simulation.transits[LIGHT]
    assert entry.threshold == 1 and entry.windows == [None, 32]
    simulation.step()
    assert simulation.books()["balanced"]
    passed = {"event": "pass", "tick": 1, "node": NODE, "measured": 1, "detector": None}
    passed.update({"family": "light", "phase": 0, "window": 32})
    assert records == [{**passed, "number": 2, "amount": 2}, {**passed, "number": 3, "amount": 1}]
    assert entry.events == [0, 0] and entry.held == [4, 0] and int(light.fly_amt.sum()) == 3

    records.clear()
    simulation = EventSimulation(
        parse_event_world(world([9, 3, 3], FAMILIES, [gate, *sources], [late])), records.append
    )
    entry = simulation.measured[1]
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 1] and entry.held == [4, 1]
    assert len(records) == 1 and records[0]["event"] == "click" and records[0]["phase"] == 32


def test_the_readers_own_number_is_excluded_everywhere():
    """(d)."""
    families = [FAMILIES[LIGHT]]
    measured = [
        fixed([4, 0, 0], "light", 1 << 10, table={"light": "pass"}),
        fixed([8, 0, 0], "light", 1, table={"light": "pass"}),
    ]
    in_transit = [unit([4, 0, 0], "light", 1, [1, 0, 0], 1), unit([4, 0, 0], "light", 2, [-1, 0, 0], 1)]
    simulation = EventSimulation(
        parse_event_world(world([9, 1, 1], families, measured, in_transit, [1, 1]))
    )
    light, entry = simulation.transits[0], simulation.measured[1]
    assert light.rank == {1: 0, 2: 1}
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.age == 1 and entry.owed == 1 and entry.held == [1 << 10]
    assert entry.measured[0] == {**NO_RESPONSE, "home": 1} and entry.home == [0]
    assert light.suspended[4, 0, 0].tolist() == [0, 1024]
    assert light.arr_amt[4, 0, 0, light.rank[2]].tolist() == [0, 1, 0, 0, 0, 0]
    assert light.fly_amt[4, 0, 0, light.rank[1]].tolist() == [1, 0, 0, 0, 0, 0]

    receiver = fixed(NODE, "m", 4, table={"light": "measure"})
    source = fixed([8, 1, 1], "light", 4)
    detector = [{"name": "d", "positions": [NODE], "threshold": 3}]
    in_transit = [unit(NODE, "light", 2, [1, 0, 0], 2), unit(NODE, "light", 1, [-1, 0, 0], 5)]
    simulation = EventSimulation(
        parse_event_world(world([9, 3, 3], FAMILIES, [receiver, source], in_transit, 0, detector))
    )
    entry, light = simulation.measured[1], simulation.transits[LIGHT]
    assert light.rank == {1: 0, 2: 1}
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 0] and entry.held == [4, 0] and entry.pushed == [0, 0, 0]
    assert entry.measured[LIGHT] == {**NO_RESPONSE, "home": 5} and entry.home == [0, 0]
    assert light.fly_amt[4, 1, 1, light.rank[1]].tolist() == [5, 0, 0, 0, 0, 0]
    assert light.fly_con[4, 1, 1, light.rank[1]].tolist() == [5, 0, 0, 0, 0, 0]
    assert int(light.fly_amt[4, 1, 1, light.rank[2]].sum()) == 2 and int(light.fly_amt.sum()) == 7
