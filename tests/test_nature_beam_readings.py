"""The one reading of a Node under the Beam Law (docs/BEAM_LAW.md; the
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
    decomposition of the first NatureBeam worlds exactly (its (p_x + p_y - 2 p_z,
    p_x - p_y) = (-19, -1) being -T_zz and (T_xx - T_yy) / 3); for 64 fixed
    random integer amounts on the seven slots the moments equal that slot
    decomposition through the same relations; on a fan (2 on (1, 1, 0), 3
    on (2, -1, 0), 1 on (3, 1, 2), 4 on (1, 0, 0), 5 here) the flow is
    (15, 0, 2) and the tensor [[44, -3, 18], [-3, -19, 6], [18, 6, -25]]
    (3 x the second moment [[27, -1, 6], [-1, 6, 2], [6, 2, 4]] less its
    trace 37), traceless; under each of the 48 signed axis permutations R of
    the GameBoard the scalars are fixed, the flow is R x flow and the tensor
    R T R^T (the moments are covariant, on the fan as on the headings); the
    shortest reading, one unit on one heading e, reads outside 1, here 0,
    the flow e and the tensor 3 e e^T - I; the keyed form over Nodes equals
    the readings Node by Node; a reading whose second moment could pass
    2^62 - 1 is refused with `OverflowError` before any product is formed;
(b) the push reads the flow of every number but the reader's own (from
    `test_one_reading_set` (b) and `test_phaseless_family` (c), re-pinned
    under the Beam Law): a free reader of content 4 met by 9 rays of number 1
    arriving on +X and 9 of number 2 arriving on -X is pushed by
    -4 x (576, 0, 0) - 4 x (-576, 0, 0) = (0, 0, 0) and reads 18; by the 9
    of number 1 alone (-2304, 0, 0) (the label of a unit along a heading
    is 64 e_d since 2026-09-19, BEAM_LAW section 2 and note 23; the
    reading's moments are taken on the unit vectors u_d at the scale
    Q = 64, its zeroth moment unchanged); with 5 of its own number arriving too the
    own add nothing (5 home, created again at the same interval's
    self-creation on its first declared direction, age 0 mod 1);
(c) the presence counts every ray at the Node of another number, rest and
    moving alike, and never the own number: a measured event at `suspension`
    [1, 4] beside 64 rays of number 2 that arrived and 16 rays of number 3
    at rest reads the presence 80 and, since clock-age-v1 (2026-09-21), its
    clock counts the age moment 64 x 1 + 16 x 0 = 64 and owes
    `by_clock(0, 64, 4)` = 16 after its first self-creation (the presence
    80 and 20 until the word); with 8 of its own number among the arrivals
    still 80, 64 and 16 (the own excluded);
(d) a detector's threshold reads the set of every number but its own and
    the window each ray's own phase: a receiver at threshold 3 met by 2 rays
    (since 2026-09-20 the threshold under `wave` reads the pointer's
    square, so the smaller set is one ray, 1 < 3, where two in phase read 4)
    of number 2 and 1 of number 3 clicks all three (`events` 3), the 2 alone
    pass with a `pass` record each (`threshold` 3); at threshold 1 with the
    window 32, the two rays at phase 0 pass (`window` 32) and the ray at
    phase 32 clicks: the window reads the record, ray by ray;
(e) the dense readings of the GameBoard, decomposed on request from the rows
    of the walk for the active Nodes only (added 2026-09-19): on the open
    9 x 3 x 3 GameBoard with no measured event, 9 units arriving at (4, 1, 1)
    on +X and 9 on -X, 3 arriving at (2, 1, 1) on +Y and 2 at rest at
    (6, 1, 1), after one interval the count is 18, 3 and 0 at those Nodes
    (21 over the GameBoard), the flow (0, 0, 0), (0, 192, 0) (3 x 64 on the
    unit vector of +Y) and (0, 0, 0), the presence 18, 3 and 2 (23 over
    the GameBoard), the Links crossed per Port
    (9, 9, 0, 0, 0, 0) at (4, 1, 1) and (0, 0, 3, 0, 0, 0) at (2, 1, 1)
    (21 over the GameBoard); before the first interval, and on an empty
    GameBoard, every array is zero with its shape.
"""

from __future__ import annotations

import itertools

import numpy as np
import pytest

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import read_arrivals
from event_universe.events.world import MOMENTUM_BOUND

NODE = [4, 1, 1]
PLUS_X, MINUS_X = [1, 0, 0], [-1, 0, 0]
NO_RESPONSE = {"home": 0, "read": 0, "measure": 0, "rerelease": 0}
FAMILIES = [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1}]
HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)
# The seven slot vectors of the first NatureBeam worlds: the six headings and here.
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
    assert reading.flow.tolist() == components[2:5].tolist()
    tensor = reading.tensor
    assert int(tensor.trace()) == 0 and (tensor == tensor.T).all()
    assert int(tensor[2, 2]) == -components[5] and int(tensor[0, 0] - tensor[1, 1]) == 3 * components[6]
    assert not (tensor - np.diag(np.diag(tensor))).any()


def test_the_moments_equal_the_slot_decomposition_and_respect_the_game_board_symmetries():
    """(a)."""
    slots = np.array([3, 1, 4, 1, 5, 9, 2], dtype=np.int64)
    reading = read_arrivals(SLOT_VECTORS, slots)
    assert int(reading.outside) == 23 and int(reading.here) == 2 and int(reading.presence) == 25
    assert reading.flow.tolist() == [2, 3, -4]
    assert reading.tensor.tolist() == np.diag([-11, -8, 19]).tolist()
    assert_slot_decomposition(slots)
    amounts = np.random.default_rng(20260919).integers(0, 1000, size=(64, 7), dtype=np.int64)
    for row in amounts:
        assert_slot_decomposition(row)
    fan = read_arrivals(FAN, FAN_AMOUNTS)
    assert int(fan.outside) == 10 and int(fan.here) == 5 and fan.flow.tolist() == [15, 0, 2]
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
            assert rotated.flow.tolist() == (matrix @ base.flow).tolist()
            assert rotated.tensor.tolist() == (matrix @ base.tensor @ matrix.T).tolist()
    for heading in HEADINGS:
        one = read_arrivals(heading[None, :], np.array([1]))
        assert int(one.outside) == 1 and int(one.here) == 0 and one.flow.tolist() == heading.tolist()
        expected = 3 * np.outer(heading, heading) - np.eye(3, dtype=np.int64)
        assert one.tensor.tolist() == expected.tolist()
    keyed = read_arrivals(
        np.concatenate([SLOT_VECTORS, FAN]),
        np.concatenate([slots, FAN_AMOUNTS]),
        np.array([1] * 7 + [0] * 5),
        2,
    )
    assert keyed.outside.tolist() == [10, 23] and keyed.here.tolist() == [5, 2]
    assert keyed.flow.tolist() == [[15, 0, 2], [2, 3, -4]]
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
        "law": "beam",
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


def beam(
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
    first = beam(NODE, "m", 1, PLUS_X, 9)
    second = beam(NODE, "m", 2, MINUS_X, 9)
    own = beam(NODE, "m", 3, PLUS_X, 5)
    for in_transit, push, read, home in (
        ([first, second, own], [0, 0, 0], 18, 5),
        ([first], [-2304, 0, 0], 9, 0),
        ([first, own], [-2304, 0, 0], 9, 5),
    ):
        simulation = NatureBeamSimulation(parse_nature_beam_world(world(families, measured, in_transit)))
        reader, store = simulation.measured[3], simulation.stores[0]
        simulation.step()
        assert simulation.books()["balanced"], in_transit
        assert reader.pushed == push and reader.momentum == push, in_transit
        assert reader.taken[0] == {**NO_RESPONSE, "read": read, "home": home}, in_transit
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
    moving = beam([4, 0, 0], "light", 2, PLUS_X, 64)
    rest = {"position": [4, 0, 0], "family": "light", "number": 3, "direction": 0, "amount": 16}
    for in_transit in ([moving, rest], [moving, rest, beam([4, 0, 0], "light", 1, MINUS_X, 8)]):
        simulation = NatureBeamSimulation(
            parse_nature_beam_world(
                world([FAMILIES[1]], [probe, *lamps], in_transit, [1, 4], shape=[9, 1, 1])
            )
        )
        simulation.step()
        assert simulation.books()["balanced"]
        entry = simulation.measured[1]
        # clock-age-v1 (2026-09-21): the presence is 80 and the count the
        # clock read is the age moment, 64 x 1 (the arrivals at age 1) +
        # 16 x 0 (the rays at rest at age 0) = 64, owed by_clock(0, 64, 4)
        # = 16 (20 on the presence until the word).
        assert entry.presence == 80 and entry.counted == 64
        assert entry.owed == by_clock(0, 64, 4) == 16
        assert entry.age == 1 and entry.held == [1]


def test_a_detectors_threshold_reads_the_set_and_its_window_the_sets_phase_by_default():
    """(d)."""
    sources = [fixed([0, 1, 1], "light", 4), fixed([8, 1, 1], "light", 4)]
    detector = [{"name": "d", "positions": [NODE], "threshold": 3}]
    two = beam(NODE, "light", 2, PLUS_X, 2)
    one = beam(NODE, "light", 3, MINUS_X, 1)
    receiver = fixed(NODE, "m", 4, table={"light": "measure"})
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world(FAMILIES, [receiver, *sources], [two, one], 0, detector)),
        records.append,
        keep_row_clicks=True,
    )
    entry = simulation.measured[1]
    assert entry.threshold == 3
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.clicks == [0, 3] and entry.held == [4, 3]
    assert entry.momentum == [64, 0, 0] and entry.pushed == [64, 0, 0]
    assert simulation.detectors()[0]["families"]["light"]["clicks"] == 3
    assert simulation.stores[1].size == 0
    clicks = [record for record in records if record["event"] == "click"]
    assert [(c["number"], c["amount"], c["push"], c["content"], c["phase"]) for c in clicks] == [
        (2, 2, [128, 0, 0], 2, 0),
        (3, 1, [-64, 0, 0], 1, 0),
    ]
    assert [(r["event"], r["phase"]) for r in records if r["event"] != "click"] == [("record", 0)]

    records.clear()
    alone = beam(NODE, "light", 2, PLUS_X, 1)
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world(FAMILIES, [receiver, *sources], [alone], 0, detector)),
        records.append,
        keep_row_clicks=True,
    )
    entry = simulation.measured[1]
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.clicks == [0, 0] and entry.held == [4, 0] and entry.momentum == [0, 0, 0]
    assert simulation.stores[1].size == 1 and int(simulation.stores[1].amount.sum()) == 1
    assert [(r["event"], r["amount"], r["threshold"], r["window"]) for r in records] == [
        ("pass", 1, 3, None)
    ]

    gate = fixed(NODE, "m", 4, table={"light": {"rule": "measure", "phase_window": 32}})
    late = beam(NODE, "light", 3, MINUS_X, 1, phase=32)
    # Under the default reading `wave` (since 2026-09-20) the window reads
    # the set's phase, the pointer of the arrivals: 2 units at phase 0 and
    # 1 at phase 32 point to phase 0, outside the window 32, so all pass.
    records.clear()
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world(FAMILIES, [gate, *sources], [two, late])),
        records.append,
        keep_row_clicks=True,
    )
    entry = simulation.measured[1]
    assert entry.threshold == 1 and entry.windows == [None, 32]
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.clicks == [0, 0] and entry.held == [4, 0]
    kinds = [(r["event"], r["number"], r.get("phase"), r.get("window")) for r in records]
    assert kinds == [("pass", 2, 0, 32), ("pass", 3, 32, 32)]
    # Declared `beam`, the window reads each ray's own phase: the ray at
    # phase 32 clicks, the two at phase 0 pass.
    records.clear()
    gate_detectors = [{"name": "gate", "positions": [NODE], "reading": "beam"}]
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world(FAMILIES, [gate, *sources], [two, late], 0, gate_detectors)),
        records.append,
        keep_row_clicks=True,
    )
    entry = simulation.measured[1]
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.clicks == [0, 1] and entry.held == [4, 1]
    kinds = [(r["event"], r["number"], r.get("phase"), r.get("window")) for r in records]
    assert kinds == [("pass", 2, 0, 32), ("click", 3, 32, None), ("record", 0, 32, None)]


def test_the_dense_readings_on_request_equal_the_arrivals_node_by_node():
    """(e)."""
    beams = [
        beam(NODE, "m", 1, PLUS_X, 9),
        beam(NODE, "m", 1, MINUS_X, 9),
        beam([2, 1, 1], "m", 1, [0, 1, 0], 3),
        {"position": [6, 1, 1], "family": "m", "number": 1, "direction": 0, "amount": 2, "phase": 0},
    ]
    simulation = NatureBeamSimulation(parse_nature_beam_world(world([FAMILIES[0]], [], beams)))
    zero = simulation.arrived[0], simulation.flow[0], simulation.presence[0], simulation.per_port[0]
    assert [a.shape for a in zero] == [(9, 3, 3), (9, 3, 3, 3), (9, 3, 3), (9, 3, 3, 6)]
    assert all(int(np.abs(a).sum()) == 0 for a in zero)
    simulation.step()
    count, flow = simulation.arrived[0], simulation.flow[0]
    presence, per_port = simulation.presence[0], simulation.per_port[0]
    assert count[4, 1, 1] == 18 and flow[4, 1, 1].tolist() == [0, 0, 0] and presence[4, 1, 1] == 18
    assert count[2, 1, 1] == 3 and flow[2, 1, 1].tolist() == [0, 192, 0] and presence[2, 1, 1] == 3
    assert count[6, 1, 1] == 0 and presence[6, 1, 1] == 2
    assert int(count.sum()) == 21 and int(presence.sum()) == 23
    assert flow.sum(axis=(0, 1, 2)).tolist() == [0, 192, 0]
    assert per_port[4, 1, 1].tolist() == [9, 9, 0, 0, 0, 0]
    assert per_port[2, 1, 1].tolist() == [0, 0, 3, 0, 0, 0] and int(per_port.sum()) == 21
    empty = NatureBeamSimulation(parse_nature_beam_world(world([FAMILIES[0]], [], [])))
    empty.step()
    assert int(empty.arrived[0].sum()) == 0 and int(empty.per_port[0].sum()) == 0


def test_a_fans_flow_reads_q_per_unit_direction_blind():
    """(f) (added 2026-09-19 with the label along the unit vector, BEAM_LAW
    note 23): the reading's vector moment is taken on the unit vectors u_d
    at the scale Q = 64, so a ray of amount q on (7, 5, 0) enters the flow
    as q x (52, 37, 0), |flow| = 64 q within 1.35 %, as a ray on a heading
    enters as q x 64 e_d, and not as q x (7, 5, 0) (8.6 q): a free reader
    of content 1 met by 5 units on (7, 5, 0) (arriving on the first step of
    its line, +X) and 5 on +X is pushed by -(5 x (52, 37, 0) + 5 x (64, 0,
    0)) = (-580, -185, 0) and reads 10, the dense flow at its Node (580,
    185, 0); by the 5 on (7, 5, 0) and 5 on (-7, -5, 0) (arriving on -X)
    the push is (0, 0, 0) exactly (u_{-D} = -u_D) and the reading 10."""
    reader = fixed(NODE, "m", 1)
    sources = [fixed([0, 1, 1], "m", 16), fixed([8, 1, 1], "m", 16)]
    fan_beam = {"position": [3, 1, 1], "family": "m", "number": 2, "direction": [7, 5, 0], "amount": 5}
    back_beam = {
        "position": [5, 1, 1],
        "family": "m",
        "number": 3,
        "direction": [-7, -5, 0],
        "amount": 5,
    }
    for in_transit, push in (
        ([fan_beam, beam(NODE, "m", 3, PLUS_X, 5)], [-580, -185, 0]),
        ([fan_beam, back_beam], [0, 0, 0]),
    ):
        document = world([FAMILIES[0]], [reader, *sources], in_transit)
        document["directions"] = [[7, 5, 0], [-7, -5, 0]]
        simulation = NatureBeamSimulation(parse_nature_beam_world(document))
        entry = simulation.measured[1]
        simulation.step()
        assert simulation.books()["balanced"]
        assert entry.pushed == push and entry.taken[0]["read"] == 10, in_transit
        assert simulation.flow[0][4, 1, 1].tolist() == [-p for p in push]
        assert simulation.arrived[0][4, 1, 1] == 10
    fan_label = 5 * np.array([52, 37, 0], dtype=np.int64)
    assert (63 * 5) ** 2 < int(fan_label @ fan_label) < (65 * 5) ** 2
