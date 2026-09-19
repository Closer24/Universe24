"""The one reading of a Node under the law of the ray (docs/RAY_LAW.md; the
model owner, 2026-09-19: every piece of logic once, in generic code): the
seven slots of a Node (the six Ports a ray arrived through and here) are
decomposed ONCE by `read_arrivals` into two scalars (outside, here), the net
flow (a vector) and the traceless tensor (two components), and every
coupling selects its component by key. The expected integers of
docs/TEST_EXPECTATIONS.md ("The one reading"), written down first:

(a) the decomposition: the seven basis vectors are mutually orthogonal; the
    slots [3, 1, 4, 1, 5, 9, 2] read outside 23, here 2, the flow
    (2, 3, -4), the tensor (4 + 5 - 28, 4 - 5) = (-19, -1), and
    12 x slots = sum_i (12 / |e_i|^2) c_i e_i (the slots recovered); under
    each of the 48 signed axis permutations of the board the scalars are
    fixed, the flow is the rotated flow, and the tensor of the rotated slots
    is the tensor of the permuted axis pairs (a representation of the
    group); the shortest slot vectors, one unit on one Port, read outside 1,
    here 0 and the flow the Port's heading;
(b) the push reads the flow of every number but the reader's own (from
    `test_one_reading_set` (b) and `test_phaseless_family` (c), re-pinned
    under the ray law): a free reader of content 4 met by 9 rays of number 1
    arriving on +X and 9 of number 2 arriving on -X is pushed by
    -4 x (9, 0, 0) - 4 x (-9, 0, 0) = (0, 0, 0) and reads 18; by the 9 of
    number 1 alone (-36, 0, 0); with 5 of its own number arriving too the
    own add nothing (5 home, created again at the same interval's
    self-creation on its first declared direction, age 0 mod 1);
(c) the presence counts every ray at the Node of another number, rest and
    moving alike, and never the own number: a measured event at `suspension`
    [1, 4] beside 64 rays of number 2 that arrived and 16 rays of number 3
    at rest owes `by_clock(0, 80 x 1, 4)` = 20 after its first self-creation;
    with 8 of its own number among the arrivals still 20 (the own excluded);
(d) a detector's threshold reads the set of every number but its own and
    the window each ray's own phase: a receiver at threshold 3 met by 2 rays
    of number 2 and 1 of number 3 clicks all three (`events` 3), the 2 alone
    pass with a `pass` record each (`threshold` 3); at threshold 1 with the
    window 32, the two rays at phase 0 pass (`window` 32) and the ray at
    phase 32 clicks: the window reads the record, ray by ray.
"""

from __future__ import annotations

import itertools

import numpy as np

from event_universe.core.integer import by_clock
from event_universe.core.lattice import PORT_HEADINGS
from event_universe.events import RaySimulation, parse_ray_world
from event_universe.events.gonen_beam import READING_BASIS, read_arrivals

NODE = [4, 1, 1]
PLUS_X, MINUS_X = [1, 0, 0], [-1, 0, 0]
NO_RESPONSE = {"home": 0, "read": 0, "measure": 0, "rerelease": 0}
FAMILIES = [{"name": "m", "kind": "free"}, {"name": "light", "kind": "paid"}]


def cube_group() -> list[tuple[int, ...]]:
    """The 48 signed axis permutations as maps on the six Port indices."""
    maps = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            image = []
            for port in range(6):
                axis, forward = port >> 1, (port & 1) == 0
                sign = (1 if forward else -1) * signs[axis]
                image.append(2 * perm[axis] + (0 if sign > 0 else 1))
            maps.append(tuple(image))
    return maps


def test_the_decomposition_is_orthogonal_sums_back_and_respects_the_board_symmetries():
    """(a)."""
    gram = READING_BASIS @ READING_BASIS.T
    assert (gram == np.diag(np.diag(gram))).all() and (np.diag(gram) == [6, 1, 2, 2, 2, 12, 4]).all()
    slots = np.array([3, 1, 4, 1, 5, 9, 2])
    reading = read_arrivals(slots)
    assert int(reading.outside) == 23 and int(reading.here) == 2 and int(reading.scalar) == 25
    assert reading.vector.tolist() == [2, 3, -4] and reading.tensor.tolist() == [-19, -1]
    components = np.concatenate([[reading.outside, reading.here], reading.vector, reading.tensor])
    recovered = ((12 // np.diag(gram)) * components) @ READING_BASIS
    assert recovered.tolist() == (12 * slots).tolist()
    for port, heading in enumerate(PORT_HEADINGS):
        unit = np.zeros(7, dtype=np.int64)
        unit[port] = 1
        one = read_arrivals(unit)
        assert int(one.outside) == 1 and int(one.here) == 0 and one.vector.tolist() == list(heading)
    group = cube_group()
    assert len(set(group)) == 48
    headings = np.array(PORT_HEADINGS)
    for image in group:
        rotated = np.zeros(7, dtype=np.int64)
        rotated[6] = slots[6]
        for port in range(6):
            rotated[image[port]] = slots[port]
        other = read_arrivals(rotated)
        assert int(other.outside) == 23 and int(other.here) == 2
        # The flow is a vector: the rotation of the six headings carries it.
        expected_flow = sum(int(slots[port]) * headings[image[port]] for port in range(6))
        assert other.vector.tolist() == expected_flow.tolist()
        # The tensor: the axis pairs permute with the axes.
        pairs = [slots[0] + slots[1], slots[2] + slots[3], slots[4] + slots[5]]
        permuted = [0, 0, 0]
        for axis in range(3):
            permuted[image[2 * axis] >> 1] = pairs[axis]
        assert other.tensor.tolist() == [
            permuted[0] + permuted[1] - 2 * permuted[2],
            permuted[0] - permuted[1],
        ]


def world(
    families: list[dict[str, object]],
    measured: list[dict[str, object]],
    in_transit: list[dict[str, object]],
    suspension: object = 0,
    detectors: list[dict[str, object]] | None = None,
    shape: list[int] | None = None,
) -> dict[str, object]:
    return {
        "law": "rays",
        "model_id": "ray-readings-test",
        "shape": shape or [9, 3, 3],
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


def ray(
    position: list[int], family: str, number: int, direction: list[int], amount: int, phase: int = 0
) -> dict[str, object]:
    """A ray one Link before `position` on `direction`, arriving there in
    interval 1 (every ray steps at its first interval)."""
    origin = [p - d for p, d in zip(position, direction, strict=True)]
    return {
        "position": origin,
        "family": family,
        "number": number,
        "direction": direction,
        "amount": amount,
        "phase": phase,
    }


def test_the_push_reads_the_flow_of_every_number_but_the_readers_own():
    """(b)."""
    families = [FAMILIES[0]]
    measured = [
        fixed([0, 1, 1], "m", 16),
        fixed([8, 1, 1], "m", 16),
        fixed(NODE, "m", 4, directions=[PLUS_X]),
    ]
    first = ray(NODE, "m", 1, PLUS_X, 9)
    second = ray(NODE, "m", 2, MINUS_X, 9)
    own = ray(NODE, "m", 3, PLUS_X, 5)
    for in_transit, push, read, home in (
        ([first, second, own], [0, 0, 0], 18, 5),
        ([first], [-36, 0, 0], 9, 0),
        ([first, own], [-36, 0, 0], 9, 5),
    ):
        simulation = RaySimulation(parse_ray_world(world(families, measured, in_transit)))
        reader, store = simulation.measured[3], simulation.stores[0]
        simulation.step()
        assert simulation.books()["balanced"], in_transit
        assert reader.pushed == push and reader.momentum == push, in_transit
        assert reader.measured[0] == {**NO_RESPONSE, "read": read, "home": home}, in_transit
        assert reader.held == [4] and reader.pending == [[]] and reader.age == 1, in_transit
        at_node = store.node == store.flat((4, 1, 1))
        # What came home is created again on the reader's one direction, age 0.
        recreated = at_node & (store.number == 3)
        assert int(store.amount[recreated].sum()) == home and (store.age[recreated] == 0).all()
        assert int(store.amount[at_node & (store.number != 3)].sum()) == read


def test_the_presence_counts_rest_and_moving_rays_of_other_numbers_and_never_the_own():
    """(c)."""
    lamps = [fixed([8, 0, 0], "light", 1), fixed([7, 0, 0], "light", 1)]
    probe = fixed([4, 0, 0], "light", 1, table={"light": "pass"})
    moving = ray([4, 0, 0], "light", 2, PLUS_X, 64)
    rest = {"position": [4, 0, 0], "family": "light", "number": 3, "direction": 0, "amount": 16}
    for in_transit in ([moving, rest], [moving, rest, ray([4, 0, 0], "light", 1, MINUS_X, 8)]):
        simulation = RaySimulation(
            parse_ray_world(world([FAMILIES[1]], [probe, *lamps], in_transit, [1, 4], shape=[9, 1, 1]))
        )
        simulation.step()
        assert simulation.books()["balanced"]
        entry = simulation.measured[1]
        assert entry.presence == 80 and entry.owed == by_clock(0, 80, 4) == 20
        assert entry.age == 1 and entry.held == [1]


def test_a_detectors_threshold_reads_the_set_and_its_window_each_rays_own_phase():
    """(d)."""
    sources = [fixed([0, 1, 1], "light", 4), fixed([8, 1, 1], "light", 4)]
    detector = [{"name": "d", "positions": [NODE], "threshold": 3}]
    two = ray(NODE, "light", 2, PLUS_X, 2)
    one = ray(NODE, "light", 3, MINUS_X, 1)
    receiver = fixed(NODE, "m", 4, table={"light": "measure"})
    records: list[dict[str, object]] = []
    simulation = RaySimulation(
        parse_ray_world(world(FAMILIES, [receiver, *sources], [two, one], 0, detector)), records.append
    )
    entry = simulation.measured[1]
    assert entry.threshold == 3
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 3] and entry.held == [4, 3]
    assert entry.momentum == [1, 0, 0] and entry.pushed == [1, 0, 0]
    assert simulation.detectors()[0]["families"]["light"]["clicks"] == 3
    assert simulation.stores[1].size == 0
    clicks = [record for record in records if record["event"] == "click"]
    assert [(c["number"], c["amount"], c["push"], c["content"], c["phase"]) for c in clicks] == [
        (2, 2, [2, 0, 0], 2, 0),
        (3, 1, [-1, 0, 0], 1, 0),
    ]
    assert [record["event"] for record in records if record["event"] != "click"] == ["record"]

    records.clear()
    simulation = RaySimulation(
        parse_ray_world(world(FAMILIES, [receiver, *sources], [two], 0, detector)), records.append
    )
    entry = simulation.measured[1]
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 0] and entry.held == [4, 0] and entry.momentum == [0, 0, 0]
    assert simulation.stores[1].size == 1 and int(simulation.stores[1].amount.sum()) == 2
    assert [(r["event"], r["amount"], r["threshold"], r["window"]) for r in records] == [
        ("pass", 2, 3, None)
    ]

    gate = fixed(NODE, "m", 4, table={"light": {"rule": "measure", "phase_window": 32}})
    late = ray(NODE, "light", 3, MINUS_X, 1, phase=32)
    records.clear()
    simulation = RaySimulation(
        parse_ray_world(world(FAMILIES, [gate, *sources], [two, late])), records.append
    )
    entry = simulation.measured[1]
    assert entry.threshold == 1 and entry.windows == [None, 32]
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 1] and entry.held == [4, 1]
    kinds = [(r["event"], r["number"], r.get("phase"), r.get("window")) for r in records]
    assert kinds == [("pass", 2, 0, 32), ("click", 3, 32, None), ("record", 0, None, None)]
