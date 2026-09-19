"""A family without a phase circle (the model owner, 2026-09-19: the field of
matter without phase; `"phase": false` in the family's entry): its events
carry phase 0 and never turn, and at a Node its arrivals are mutually
incoherent. The rule of the Node is one (`mixing.mix_arrivals` for every
family, the model owner, 2026-09-19: "everything generic must be replaced by
generic"): only the weights of the sides know the family. For a family with
a phase circle they are the coherent |c_h|^2, c_h = S - 3 a_opp(h); for one
without they are the diagonal of the same expansion,
|c_h|^2 = |S|^2 - 6 Re(S conj(a_opp)) + 9 |a_opp|^2 with every cross term
between different arrivals dropped, so with |a_k|^2 = 32^2 x amount_k

    weight_h = 32^2 x (sum_k amount_k + 3 x amount_opp(h))

(`mixing.diagonal_weights`): a lone arrival weighs 4 back and 1 to each
other side, the four ninths back and one ninth each other way of a lone
scatter; two arrivals through opposite Ports never cancel. The placement is
the common one: per number whole units by the largest remainder with the
ties in the tick's Port order, once per group and not once per Port; a
number with no whole share for any side goes whole to the heading nearest
the momentum it carries; the group's momentum is apportioned over its
departures exactly (`apportion_carried`); every phase leaving is 0. The push
of a free family reads the net flow of the bundle, amount times travel
heading summed over the six Ports, not the momentum labels the units carry.
The expected integers of docs/TEST_EXPECTATIONS.md ("A family without a
phase circle"), derived by hand first, on one Node of a transit of shape
(1, 1, 1) with one number, N = 8, tick 1:

(a) a lone arrival of 9 units on +X carrying (9, 0, 0): the weights
    9 x 1024 x [1, 4, 1, 1, 1, 1], 4 back on -X and 1 to each other side,
    [1, 4, 1, 1, 1, 1], every phase 0, the x momentum 1, 4, 1, 1, 1, 1 with
    the units, the sum (9, 0, 0); nothing kept;
(b) two arrivals of 9, on +X carrying (9, 0, 0) and on -X carrying
    (-9, 0, 0): the amount present 18, the weights 1024 x [45, 45, 18, 18,
    18, 18] (18 + 27 along the axis), 18 units placed as 18 x w / 162 =
    w / 9 exactly, [5, 5, 2, 2, 2, 2], no cancellation (under the coherent
    rule the same two in antiphase would leave 9 and 9 along x and nothing
    transverse; the phase-less integers alone are asserted here); every
    phase 0; the group's momentum is the net (0, 0, 0), so every label
    leaving is 0 (until 2026-09-19 the per-Port scatter apportioned each
    Port's own, -3 on +X and 3 on -X); the sum (0, 0, 0). The edge: 2 units
    on +X carrying (2, 0, 0) with the 9 on -X: the amount present 11, the
    weights 1024 x [38, 17, 11, 11, 11, 11] (11 + 27 on +X, 11 + 6 on -X),
    11 units: the floors 11 x w // 99 = [4, 1, 1, 1, 1, 1] with the
    remainders [22, 88, 22, 22, 22, 22], two units left, one to -X (88) and
    one to the first of the tied 22s from tick 1, +Y: [4, 2, 2, 1, 1, 1]
    (the per-Port scatter gave [6, 1, 1, 1, 1, 1], the 2 whole on +X and the
    9 mirrored; the 2 now join the group's placement); the momentum
    (-7, 0, 0) over [4, 2, 2, 1, 1, 1]: the floors 7 x w // 11 =
    [2, 1, 1, 0, 0, 0] with the remainders [6, 3, 3, 7, 7, 7], three left to
    the 7s: -[2, 1, 1, 1, 1, 1], the sum (-7, 0, 0);
(c) the push reads the flow: a measured event of content 4 (number 2) of a
    phase-less free family at a Node where 9 units of number 1 arrive on +X
    travel and 9 on -X travel, the labels rewritten to (9, 0, 0) and
    (-3, 0, 0): the flow (0, 0, 0), the push (0, 0, 0), while the labels
    sum to (6, 0, 0); the units leave [5, 5, 2, 2, 2, 2] as in (b), and the
    momentum in transit the books report is the labels' sum (6, 0, 0),
    exact; a lone 9 on +X travel: the flow (9, 0, 0), the push
    -4 x (9, 0, 0) = (-36, 0, 0), the measured event's momentum (-36, 0, 0);
(d) the identity: a bundle of 7 on +X, 5 on +Y and 3 on -Z (15 present) has
    the weights 1024 x [15, 15 + 21, 15, 15 + 15, 15 + 9, 15] =
    1024 x [15, 36, 15, 30, 24, 15] exactly; the bundle three times over
    (21, 15, 9; 45 units) places as 45 x 3 w / (9 x 45) = w / 3 exactly,
    [5, 12, 5, 10, 8, 5]; a second number's arrivals at the Node add nothing
    to the first's weights (no cross term survives between mutually
    incoherent arrivals, of different Ports or of different numbers; the
    diagonal over all numbers instead would let a dense field of one number
    steer another's labels, measured at 4 to 10 times the pair world's push);
    a lone arrival of 9 on +X of a family with a phase circle has the
    coherent weights 256^2 x the diagonal ones (the phase table's scale
    squared; no cross term exists for one arrival).
"""

from __future__ import annotations

import numpy as np

from event_universe.core.phase import PHASE_COSINE_SCALE
from event_universe.events import EventSimulation, parse_event_world
from event_universe.events.mixing import (
    MIXING_AMPLITUDE_SCALE,
    OPPOSITE,
    coherent_weights,
    diagonal_weights,
)
from event_universe.events.transit import HEADINGS, Transit

PLUS_X, MINUS_X, PLUS_Y, MINUS_Y, PLUS_Z, MINUS_Z = range(6)


def one_node(*, phased: bool = False) -> Transit:
    """One Node, one number, a family without a phase circle, tick 1."""
    transit = Transit(0, (1, 1, 1), (1,), 8, 1 << 20, phased=phased)
    transit.tick = 1
    return transit


def arrive(transit: Transit, port: int, amount: int, momentum: tuple[int, int, int]) -> None:
    cell = (0, 0, 0, 0, port)
    transit.arr_amt[cell] = amount
    transit.arr_mom[cell] = momentum


def scattered(transit: Transit) -> tuple[list[int], list[int], list[list[int]]]:
    """One cycle: the departures per Port, their phases and their momenta;
    nothing kept."""
    arrived = int(transit.arr_amt.sum())
    transit.cycle()
    assert not transit.arr_amt.any() and not transit.suspended.any()
    assert int(transit.fly_amt.sum()) == arrived
    return (
        [int(v) for v in transit.fly_amt[0, 0, 0, 0]],
        [int(v) for v in transit.fly_ph[0, 0, 0, 0]],
        transit.fly_mom[0, 0, 0, 0].tolist(),
    )


def test_a_lone_arrival_scatters_four_ninths_back_and_one_ninth_each_other_way():
    """(a)."""
    transit = one_node()
    arrive(transit, PLUS_X, 9, (9, 0, 0))
    amounts, phases, momenta = scattered(transit)
    assert amounts == [1, 4, 1, 1, 1, 1]
    assert phases == [0, 0, 0, 0, 0, 0]
    assert [m[0] for m in momenta] == [1, 4, 1, 1, 1, 1]
    assert [sum(m[axis] for m in momenta) for axis in range(3)] == [9, 0, 0]


def test_two_arrivals_through_opposite_ports_add_their_weights_without_cancelling():
    """(b)."""
    transit = one_node()
    arrive(transit, PLUS_X, 9, (9, 0, 0))
    arrive(transit, MINUS_X, 9, (-9, 0, 0))
    amounts, phases, momenta = scattered(transit)
    assert amounts == [5, 5, 2, 2, 2, 2]
    assert phases == [0, 0, 0, 0, 0, 0]
    assert [m[0] for m in momenta] == [0, 0, 0, 0, 0, 0]
    assert [sum(m[axis] for m in momenta) for axis in range(3)] == [0, 0, 0]
    transit = one_node()
    arrive(transit, PLUS_X, 2, (2, 0, 0))
    arrive(transit, MINUS_X, 9, (-9, 0, 0))
    amounts, _, momenta = scattered(transit)
    assert amounts == [4, 2, 2, 1, 1, 1]
    assert [m[0] for m in momenta] == [-2, -1, -1, -1, -1, -1]
    assert [sum(m[axis] for m in momenta) for axis in range(3)] == [-7, 0, 0]


def test_the_weights_of_a_phaseless_family_are_the_diagonal_of_the_coherent_sum():
    """(d)."""
    transit = one_node()
    arrive(transit, PLUS_X, 7, (7, 0, 0))
    arrive(transit, PLUS_Y, 5, (0, 5, 0))
    arrive(transit, MINUS_Z, 3, (0, 0, -3))
    amounts = transit.arr_amt[0, 0, 0, 0]
    expected = MIXING_AMPLITUDE_SCALE**2 * (int(amounts.sum()) + 3 * amounts[OPPOSITE])
    assert expected.tolist() == [1024 * w for w in (15, 36, 15, 30, 24, 15)]
    weights = diagonal_weights(transit.arr_amt.astype(np.int64))
    assert weights.shape == (1, 1, 1, 1, 6)
    assert weights[0, 0, 0, 0].tolist() == expected.tolist()
    transit = one_node()
    arrive(transit, PLUS_X, 21, (0, 0, 0))
    arrive(transit, PLUS_Y, 15, (0, 0, 0))
    arrive(transit, MINUS_Z, 9, (0, 0, 0))
    amounts_out, phases, _ = scattered(transit)
    assert amounts_out == [5, 12, 5, 10, 8, 5]
    assert phases == [0, 0, 0, 0, 0, 0]
    two = Transit(0, (1, 1, 1), (1, 2), 8, 1 << 20, phased=False)
    two.tick = 1
    two.arr_amt[0, 0, 0, 0] = amounts
    two.arr_amt[0, 0, 0, 1, MINUS_X] = 1000
    weights = diagonal_weights(two.arr_amt.astype(np.int64))
    assert weights.shape == (1, 1, 1, 2, 6)
    assert weights[0, 0, 0, 0].tolist() == expected.tolist()
    assert weights[0, 0, 0, 1].tolist() == [1024 * 1000 * w for w in (4, 1, 1, 1, 1, 1)]
    two.cycle()
    assert two.fly_amt[0, 0, 0, 1].tolist() == [4000 // 9 + 1, 1000 // 9, 111, 111, 111, 111]
    assert int(two.fly_amt[0, 0, 0, 0].sum()) == 15
    phased = one_node(phased=True)
    arrive(phased, PLUS_X, 9, (9, 0, 0))
    coherent, *_ = coherent_weights(
        phased, phased.arr_amt.astype(np.int64), phased.arr_ph.astype(np.int64)
    )
    diagonal = diagonal_weights(phased.arr_amt.astype(np.int64))
    assert coherent.tolist() == (PHASE_COSINE_SCALE**2 * diagonal).tolist()
    assert diagonal[0, 0, 0, 0].tolist() == [1024 * w for w in (9, 36, 9, 9, 9, 9)]


def world(in_transit: list[dict[str, object]]) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "phaseless-family-test",
        "shape": [9, 3, 3],
        "boundary": "open",
        "ticks": 1,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "m", "kind": "free", "phase": False}],
        "measured": [
            {"position": [0, 1, 1], "family": "m", "amount": 16, "fixed": True},
            {"position": [4, 1, 1], "family": "m", "amount": 4, "fixed": True},
        ],
        "in_transit": in_transit,
    }


def unit(heading: list[int], amount: int) -> dict[str, object]:
    return {"position": [4, 1, 1], "family": "m", "number": 1, "heading": heading, "amount": amount}


def test_the_push_of_a_free_family_reads_the_net_flow_and_not_the_labels():
    """(c)."""
    simulation = EventSimulation(parse_event_world(world([unit([1, 0, 0], 9), unit([-1, 0, 0], 9)])))
    transit = simulation.transits[0]
    cell = (4, 1, 1, transit.rank[1])
    transit.arr_mom[(*cell, MINUS_X)] = (-3, 0, 0)
    assert [int(v) for v in transit.arr_mom[cell].sum(axis=0)] == [6, 0, 0]
    assert [int(v) for v in transit.arr_amt[cell] @ HEADINGS] == [0, 0, 0]
    simulation.step()
    books = simulation.books()
    assert books["balanced"]
    reader = simulation.measured[2]
    assert reader.pushed == [0, 0, 0] and reader.momentum == [0, 0, 0]
    assert reader.measured[0]["read"] == 18 and reader.phase == 0 and reader.phase_steps == 0
    assert [int(v) for v in transit.fly_amt[cell]] == [5, 5, 2, 2, 2, 2]
    assert books["momentum"]["transit"] == [6, 0, 0] and books["momentum"]["measured"] == [0, 0, 0]
    simulation = EventSimulation(parse_event_world(world([unit([1, 0, 0], 9)])))
    simulation.step()
    assert simulation.books()["balanced"]
    reader = simulation.measured[2]
    assert reader.pushed == [-36, 0, 0] and reader.momentum == [-36, 0, 0]
