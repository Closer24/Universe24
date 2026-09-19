"""The detector under the law of the ray (docs/RAY_LAW.md, section 5): the
wave is a reading of a crowd of rays at a detector and lives nowhere else.
At a detector Node, per interval and family, the clicked rays' amplitudes
A_u = 32 x amount_u at their phases (the 1/256 tables) are summed
by the one decomposition, and the record is X^2 + Y^2 of its scalar; the
threshold gates every response of a detector's Node, a receiver's and a
re-emitter's alike, a smaller set passing with a `pass` record; a release
reads no threshold. The expected integers of docs/TEST_EXPECTATIONS.md ("The
detector's record"), written down first. K 2^20, `suspension` 0, `release`
[0, 1], the families `m` (free) and `light` (paid), every measured event
`fixed`:

(a) two rays of amount 1 arriving in one interval at a counter of threshold
    1, in phase (0 and 0): the record 4 x 32^2 x 256^2 = 268435456, the
    amount 2 and two clicks; in antiphase (0 and 32): the record 0, the
    amount 2 and two clicks; one ray alone: 32^2 x 256^2 = 67108864; the
    `record` line of `events.jsonl` carries the pointer (X, Y) and the
    square; the run's detector report carries the cumulative record;
(b) a receiver (a measured event of `m`, content 4, measuring light) at
    threshold 3 (from `test_detector_sensitivity` (a), re-pinned): 2 rays of
    another number pass with a `pass` record (`threshold` 3), no click, no
    push, the rays going on whole; 3 rays are measured: 3 clicks, `held`
    [4, 3], the momentum (3, 0, 0), nothing left in the store, the report 3
    measured, 3 clicks, the record (3 x 32)^2 x 256^2 = 9 x 32^2 x 256^2
    (a row of three identical rays is one coherent amplitude);
(c) a re-emitter at threshold 3 (from (b) there): 2 rays pass; 3 rays are
    taken (re-released 3, no click, the push (3, 0, 0), the recoil at the
    re-emission -(1, 1, 1) leaving the momentum (2, -1, -1)) and created again at the
    same interval's self-creation, one per declared direction (+X, +Y, +Z),
    with the re-emitter's number, the arriving phase 20, content 1, age 0;
(d) an emitter inside a detector reads no threshold: a lamp of light
    (content 24, K 24, rate [1, 1]) in a detector of threshold 5 releases
    one unit per heading per interval, its content 18 then 12; a reader of
    `m` (content 4) at threshold 4 passes 3 rays and reads 4, pushed by
    -M c = (-16, 0, 0).
"""

from __future__ import annotations

from event_universe.events import RaySimulation, parse_ray_world

M, LIGHT = 0, 1
NODE = [4, 1, 1]
NO_RESPONSE = {"home": 0, "read": 0, "measure": 0, "rerelease": 0}
FAMILIES = [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1}]
SOURCE = {"position": [0, 1, 1], "family": "light", "amount": 4, "fixed": True}
UNIT_RECORD = 32 * 32 * 256 * 256


def world(
    measured: list[dict[str, object]],
    in_transit: list[dict[str, object]],
    threshold: int,
    clock: int = 1 << 20,
) -> dict[str, object]:
    return {
        "law": "rays",
        "model_id": "ray-detector-test",
        "shape": [9, 3, 3],
        "boundary": "open",
        "ticks": 2,
        "K": clock,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": FAMILIES,
        "measured": measured,
        "in_transit": in_transit,
        "detectors": [{"name": "d", "positions": [NODE], "threshold": threshold}],
    }


def arrival(
    amount: int,
    family: str = "light",
    number: int = 2,
    phase: int = 0,
    direction: list[int] | None = None,
) -> dict[str, object]:
    """Rays one Link before the detector's Node, arriving in interval 1."""
    heading = direction or [1, 0, 0]
    return {
        "position": [NODE[0] - heading[0], NODE[1] - heading[1], NODE[2] - heading[2]],
        "family": family,
        "number": number,
        "direction": heading,
        "amount": amount,
        "phase": phase,
    }


def test_two_rays_in_phase_record_four_units_and_in_antiphase_nothing():
    """(a)."""
    counter = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "fixed": True,
        "table": {"light": "measure"},
    }
    other = {"position": [8, 1, 1], "family": "light", "amount": 4, "fixed": True}
    for phases, expected in (((0, 0), 4 * UNIT_RECORD), ((0, 32), 0), ((0,), UNIT_RECORD)):
        rays = [arrival(1, number=2, phase=phases[0])]
        if len(phases) == 2:
            rays.append(arrival(1, number=3, phase=phases[1], direction=[-1, 0, 0]))
        records: list[dict[str, object]] = []
        simulation = RaySimulation(
            parse_ray_world(world([counter, SOURCE, other], rays, 1)), records.append
        )
        entry = simulation.measured[1]
        simulation.step()
        assert simulation.books()["balanced"]
        assert entry.events == [0, len(phases)] and entry.record == [0, expected], phases
        assert simulation.detectors()[0]["families"]["light"] == {
            "measured": len(phases),
            "clicks": len(phases),
            "record": expected,
        }
        lines = [r for r in records if r["event"] == "record"]
        assert len(lines) == 1 and lines[0]["record"] == expected and lines[0]["detector"] == "d"
        pointer = lines[0]["pointer"]
        assert pointer[0] ** 2 + pointer[1] ** 2 == expected


def test_a_receiver_measures_only_a_set_at_its_threshold_and_a_smaller_one_passes():
    """(b)."""
    receiver = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "fixed": True,
        "table": {"light": "measure"},
    }
    records: list[dict[str, object]] = []
    simulation = RaySimulation(
        parse_ray_world(world([receiver, SOURCE], [arrival(2)], 3)), records.append
    )
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    assert entry.detector == 0 and entry.threshold == 3
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 0] and entry.held == [4, 0] and entry.momentum == [0, 0, 0]
    assert entry.measured[LIGHT] == NO_RESPONSE
    assert light.size == 1 and int(light.amount[0]) == 2 and int(light.node[0]) == light.flat((4, 1, 1))
    assert [(r["event"], r["amount"], r["threshold"]) for r in records] == [("pass", 2, 3)]
    simulation.step()
    assert simulation.books()["balanced"] and light.size == 1 and int(light.amount[0]) == 2

    records.clear()
    simulation = RaySimulation(
        parse_ray_world(world([receiver, SOURCE], [arrival(3)], 3)), records.append
    )
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 3] and entry.held == [4, 3] and entry.momentum == [3, 0, 0]
    assert entry.pushed == [3, 0, 0] and entry.measured[LIGHT] == {**NO_RESPONSE, "measure": 3}
    assert light.size == 0
    assert simulation.detectors()[0]["families"]["light"] == {
        "measured": 3,
        "clicks": 3,
        "record": 9 * UNIT_RECORD,
    }
    assert [r["event"] for r in records] == ["click", "record"]


def test_a_re_emitter_takes_only_a_set_at_its_threshold_and_creates_it_again_as_its_own():
    """(c)."""
    emitter = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "phase": 9,
        "fixed": True,
        "directions": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "table": {"light": "rerelease"},
    }
    simulation = RaySimulation(parse_ray_world(world([emitter, SOURCE], [arrival(2, phase=20)], 3)))
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    simulation.step()
    assert simulation.books()["balanced"]
    assert (
        entry.measured[LIGHT] == NO_RESPONSE
        and entry.pending == [[], []]
        and entry.momentum == [0, 0, 0]
    )
    assert light.size == 1 and int(light.amount[0]) == 2 and int(light.number[0]) == 2

    records: list[dict[str, object]] = []
    simulation = RaySimulation(
        parse_ray_world(world([emitter, SOURCE], [arrival(3, phase=20)], 3)), records.append
    )
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    simulation.step()
    assert simulation.books()["balanced"]
    assert [(r["event"], r["amount"], r["push"]) for r in records] == [("rerelease", 3, [3, 0, 0])]
    assert entry.measured[LIGHT] == {**NO_RESPONSE, "rerelease": 3} and entry.events == [0, 0]
    assert entry.held == [4, 0] and entry.pending == [[], []]
    assert entry.pushed == [3, 0, 0] and entry.momentum == [2, -1, -1]
    assert (
        simulation.ledger.transit_absorbed[LIGHT] == 3 and simulation.ledger.transit_released[LIGHT] == 3
    )
    rows = sorted(
        (
            int(light.direction[i]),
            int(light.amount[i]),
            int(light.phase[i]),
            int(light.age[i]),
            int(light.number[i]),
            int(light.content[i]),
        )
        for i in range(light.size)
    )
    assert rows == [(2, 1, 20, 0, 1, 1), (4, 1, 20, 0, 1, 1), (6, 1, 20, 0, 1, 1)]
    assert set(light.node.tolist()) == {light.flat((4, 1, 1))}
    simulation.step()
    assert simulation.books()["balanced"]
    assert sorted(light.node.tolist()) == sorted(
        light.flat(p) for p in ((5, 1, 1), (4, 2, 1), (4, 1, 2))
    )


def test_a_release_reads_no_threshold_and_a_reading_is_gated_like_a_measurement():
    """(d)."""
    lamp = {"position": NODE, "family": "light", "amount": 24, "fixed": True, "lamp": {"rate": [1, 1]}}
    simulation = RaySimulation(parse_ray_world(world([lamp], [], 5, clock=24)))
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    assert entry.detector == 0 and entry.threshold == 5
    for tick in (1, 2):
        simulation.step()
        assert simulation.books()["balanced"], tick
        fresh = light.age == 0
        assert sorted(light.direction[fresh].tolist()) == [2, 3, 4, 5, 6, 7], tick
        assert (light.content[fresh] == 1).all() and (light.amount[fresh] == 1).all()
        assert entry.held == [0, 24 - 6 * tick] and simulation.ledger.held_spent[LIGHT] == 6 * tick, tick
        assert simulation.ledger.transit_released[LIGHT] == 6 * tick and entry.momentum == [0, 0, 0], (
            tick
        )
    assert simulation.detectors()[0]["families"]["light"] == {"measured": 0, "clicks": 0, "record": 0}

    source = {"position": [0, 1, 1], "family": "m", "amount": 16, "fixed": True}
    reader = {"position": NODE, "family": "m", "amount": 4, "fixed": True, "table": {"m": "read"}}
    for amount, push, read in ((3, [0, 0, 0], 0), (4, [-16, 0, 0], 4)):
        simulation = RaySimulation(
            parse_ray_world(world([source, reader], [arrival(amount, family="m", number=1)], 4))
        )
        entry, m = simulation.measured[2], simulation.stores[M]
        simulation.step()
        assert simulation.books()["balanced"], amount
        assert entry.momentum == push and entry.pushed == push, amount
        assert entry.measured[M] == {**NO_RESPONSE, "read": read}, amount
        assert entry.held == [4, 0] and entry.events == [0, 0], amount
        assert m.size == 1 and int(m.amount[0]) == amount and int(m.number[0]) == 1, amount
        assert simulation.detectors()[0]["families"]["m"] == {"measured": 0, "clicks": 0, "record": 0}, (
            amount
        )
