"""The one reading of a Node under the law of the ray (docs/RAY_LAW.md; the
model owner, 2026-09-19: every piece of logic once, in generic code; "the one
reading function is the amount-weighted moments of order 0, 1 and 2 of the
direction vectors, valid for fans as for the six headings, here entering the
zeroth moment alone"): `read_arrivals` takes ONCE, over one reading set, the
moments of the arrivals' direction vectors weighted by their amounts: the
count split outside / here (a ray that did not step has the direction
(0, 0, 0)), the net flow (sum amount x D) and the traceless tensor (3 x sum
amount x D (x) D less its trace on the diagonal, exact integers), and every
coupling selects its component by key. The expected integers of
docs/TEST_EXPECTATIONS.md ("The one reading"), written down first:

(a) the moments: on the six headings the amounts [3, 1, 4, 1, 5, 9] and 2
    here read outside 23, here 2, the flow (2, 3, -4) and the tensor
    diag(-11, -8, 19) (3 x diag(4, 5, 14) - 23 I), which is the slot
    decomposition of the first ray worlds exactly (its (p_x + p_y - 2 p_z,
    p_x - p_y) = (-19, -1) being -T_zz and (T_xx - T_yy) / 3); for 64 fixed
    random integer amounts on the seven slots the moments equal that slot
    decomposition through the same relations; on a fan (2 on (1, 1, 0), 3
    on (2, -1, 0), 1 on (3, 1, 2), 4 on (1, 0, 0), 5 here) the flow is
    (15, 0, 2) and the tensor [[44, -3, 18], [-3, -19, 6], [18, 6, -25]]
    (3 x the second moment [[27, -1, 6], [-1, 6, 2], [6, 2, 4]] less its
    trace 37), traceless; under each of the 48 signed axis permutations R of
    the board the scalars are fixed, the flow is R x flow and the tensor
    R T R^T (the moments are covariant, on the fan as on the headings); the
    shortest reading, one unit on one heading e, reads outside 1, here 0,
    the flow e and the tensor 3 e e^T - I; the keyed form over Nodes equals
    the readings Node by Node; a reading whose second moment could pass
    2^62 - 1 is refused with `OverflowError` before any product is formed;
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
    phase 32 clicks: the window reads the record, ray by ray;
(e) the dense readings of the board, decomposed on request from the rows
    of the walk for the active Nodes only (added 2026-09-19): on the open
    9 x 3 x 3 board with no measured event, 9 units arriving at (4, 1, 1)
    on +X and 9 on -X, 3 arriving at (2, 1, 1) on +Y and 2 at rest at
    (6, 1, 1), after one interval the count is 18, 3 and 0 at those Nodes
    (21 over the board), the flow (0, 0, 0), (0, 3, 0) and (0, 0, 0), the
    presence 18, 3 and 2 (23 over the board), the Links crossed per Port
    (9, 9, 0, 0, 0, 0) at (4, 1, 1) and (0, 0, 3, 0, 0, 0) at (2, 1, 1)
    (21 over the board); before the first interval, and on an empty
    board, every array is zero with its shape.
"""

from __future__ import annotations

import itertools

import numpy as np
import pytest

from event_universe.core.integer import by_clock
from event_universe.core.lattice import PORT_HEADINGS
from event_universe.events import RaySimulation, parse_ray_world
from event_universe.events.nature_beam import read_arrivals
from event_universe.events.world import MOMENTUM_BOUND

NODE = [4, 1, 1]
PLUS_X, MINUS_X = [1, 0, 0], [-1, 0, 0]
NO_RESPONSE = {"home": 0, "read": 0, "measure": 0, "rerelease": 0}
FAMILIES = [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1}]
HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)
# The seven slot vectors of the first ray worlds: the six headings and here.
SLOT_VECTORS = np.concatenate([HEADINGS, np.zeros((1, 3), dtype=np.int64)])
# The slot decomposition the moments replace (the reference of this test):
# outside, here, the flow, and (p_x + p_y - 2 p_z, p_x - p_y) with p the sum
# of the two slots of an axis.
SLOT_BASIS = np.array(
    [
        [1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [1, -1, 0, 0, 0, 0, 0],
        [0, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, 0, 1, -1, 0],
        [1, 1, 1, 1, -2, -2, 0],
        [1, 1, -1, -1, 0, 0, 0],
    ],
    dtype=np.int64,
)
FAN = np.array([[1, 1, 0], [2, -1, 0], [3, 1, 2], [1, 0, 0], [0, 0, 0]], dtype=np.int64)
FAN_AMOUNTS = np.array([2, 3, 1, 4, 5], dtype=np.int64)


def cube_group() -> list[np.ndarray]:
    """The 48 signed axis permutations as integer matrices."""
    matrices = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            matrix = np.zeros((3, 3), dtype=np.int64)
            for axis in range(3):
                matrix[perm[axis], axis] = signs[axis]
            matrices.append(matrix)
    return matrices


def assert_slot_decomposition(slots: np.ndarray) -> None:
    """The moments on the seven slots equal the slot decomposition exactly."""
    components = slots @ SLOT_BASIS.T
    reading = read_arrivals(SLOT_VECTORS, slots)
    assert int(reading.outside) == components[0] and int(reading.here) == components[1]
    assert reading.vector.tolist() == components[2:5].tolist()
    tensor = reading.tensor
    assert int(tensor.trace()) == 0 and (tensor == tensor.T).all()
    assert int(tensor[2, 2]) == -components[5] and int(tensor[0, 0] - tensor[1, 1]) == 3 * components[6]
    assert not (tensor - np.diag(np.diag(tensor))).any()


def test_the_moments_equal_the_slot_decomposition_and_respect_the_board_symmetries():
    """(a)."""
    slots = np.array([3, 1, 4, 1, 5, 9, 2], dtype=np.int64)
    reading = read_arrivals(SLOT_VECTORS, slots)
    assert int(reading.outside) == 23 and int(reading.here) == 2 and int(reading.scalar) == 25
    assert reading.vector.tolist() == [2, 3, -4]
    assert reading.tensor.tolist() == np.diag([-11, -8, 19]).tolist()
    assert_slot_decomposition(slots)
    amounts = np.random.default_rng(20260919).integers(0, 1000, size=(64, 7), dtype=np.int64)
    for row in amounts:
        assert_slot_decomposition(row)
    fan = read_arrivals(FAN, FAN_AMOUNTS)
    assert int(fan.outside) == 10 and int(fan.here) == 5 and fan.vector.tolist() == [15, 0, 2]
    assert fan.tensor.tolist() == [[44, -3, 18], [-3, -19, 6], [18, 6, -25]]
    assert int(fan.tensor.trace()) == 0
    second = (FAN_AMOUNTS[:, None, None] * FAN[:, :, None] * FAN[:, None, :]).sum(axis=0)
    assert second.tolist() == [[27, -1, 6], [-1, 6, 2], [6, 2, 4]]
    assert (fan.tensor == 3 * second - 37 * np.eye(3, dtype=np.int64)).all()
    group = cube_group()
    assert len({matrix.tobytes() for matrix in group}) == 48
    for vectors, weights in ((SLOT_VECTORS, slots), (FAN, FAN_AMOUNTS)):
        base = read_arrivals(vectors, weights)
        for matrix in group:
            rotated = read_arrivals(vectors @ matrix.T, weights)
            assert int(rotated.outside) == int(base.outside) and int(rotated.here) == int(base.here)
            assert rotated.vector.tolist() == (matrix @ base.vector).tolist()
            assert rotated.tensor.tolist() == (matrix @ base.tensor @ matrix.T).tolist()
    for heading in HEADINGS:
        one = read_arrivals(heading[None, :], np.array([1]))
        assert int(one.outside) == 1 and int(one.here) == 0 and one.vector.tolist() == heading.tolist()
        expected = 3 * np.outer(heading, heading) - np.eye(3, dtype=np.int64)
        assert one.tensor.tolist() == expected.tolist()
    keyed = read_arrivals(
        np.concatenate([SLOT_VECTORS, FAN]),
        np.concatenate([slots, FAN_AMOUNTS]),
        np.array([1] * 7 + [0] * 5),
        2,
    )
    assert keyed.outside.tolist() == [10, 23] and keyed.here.tolist() == [5, 2]
    assert keyed.vector.tolist() == [[15, 0, 2], [2, 3, -4]]
    assert keyed.tensor[0].tolist() == fan.tensor.tolist()
    assert keyed.tensor[1].tolist() == reading.tensor.tolist()
    with pytest.raises(OverflowError, match="moments of a reading"):
        read_arrivals(np.array([[64, 0, 0]]), np.array([MOMENTUM_BOUND // 4096 + 1]))
    read_arrivals(np.array([[64, 0, 0]]), np.array([MOMENTUM_BOUND // 4096]))


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
    assert [(r["event"], r["phase"]) for r in records if r["event"] != "click"] == [("record", 0)]

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
    assert kinds == [("pass", 2, 0, 32), ("click", 3, 32, None), ("record", 0, 32, None)]


def test_the_dense_readings_on_request_equal_the_arrivals_node_by_node():
    """(e)."""
    rays = [
        ray(NODE, "m", 1, PLUS_X, 9),
        ray(NODE, "m", 1, MINUS_X, 9),
        ray([2, 1, 1], "m", 1, [0, 1, 0], 3),
        {"position": [6, 1, 1], "family": "m", "number": 1, "direction": 0, "amount": 2, "phase": 0},
    ]
    simulation = RaySimulation(parse_ray_world(world([FAMILIES[0]], [], rays)))
    zero = simulation.count[0], simulation.flow[0], simulation.presence[0], simulation.per_port[0]
    assert [a.shape for a in zero] == [(9, 3, 3), (9, 3, 3, 3), (9, 3, 3), (9, 3, 3, 6)]
    assert all(int(np.abs(a).sum()) == 0 for a in zero)
    simulation.step()
    count, flow = simulation.count[0], simulation.flow[0]
    presence, per_port = simulation.presence[0], simulation.per_port[0]
    assert count[4, 1, 1] == 18 and flow[4, 1, 1].tolist() == [0, 0, 0] and presence[4, 1, 1] == 18
    assert count[2, 1, 1] == 3 and flow[2, 1, 1].tolist() == [0, 3, 0] and presence[2, 1, 1] == 3
    assert count[6, 1, 1] == 0 and presence[6, 1, 1] == 2
    assert int(count.sum()) == 21 and int(presence.sum()) == 23
    assert flow.sum(axis=(0, 1, 2)).tolist() == [0, 3, 0]
    assert per_port[4, 1, 1].tolist() == [9, 9, 0, 0, 0, 0]
    assert per_port[2, 1, 1].tolist() == [0, 0, 3, 0, 0, 0] and int(per_port.sum()) == 21
    empty = RaySimulation(parse_ray_world(world([FAMILIES[0]], [], [])))
    empty.step()
    assert int(empty.count[0].sum()) == 0 and int(empty.per_port[0].sum()) == 0
