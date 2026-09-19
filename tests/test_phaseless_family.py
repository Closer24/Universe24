"""A family without a phase circle (the model owner, 2026-09-19: the field of
matter without phase; `"phase": false` in the family's entry): its events
carry phase 0 and never turn, and at a Node its arrivals do not sum
coherently. Each Port's arrival scatters on its own with the shares of a lone
arrival, four ninths back out through the Port it came in by and one ninth to
each of the other five sides, whole units by the largest remainder with the
ties in the tick's Port order, per Port; a Port's arrival with no whole share
for any side goes whole to its own momentum's heading; its momentum is
apportioned over its own departures exactly (`apportion_carried` per Port),
and the six Ports' departures are added per heading
(`mixing.scatter_arrivals`, chosen by `Transit.cycle`). The push of a free
family reads the net flow of the bundle, amount times travel heading summed
over the six Ports, not the momentum labels the units carry. The expected
integers of docs/TEST_EXPECTATIONS.md ("A family without a phase circle"),
written down first, on one Node of a transit of shape (1, 1, 1) with one
number, N = 8, tick 1:

(a) a lone arrival of 9 units on +X carrying (9, 0, 0): 4 back on -X and 1
    to each other side, [1, 4, 1, 1, 1, 1], every phase 0, the x momentum
    1, 4, 1, 1, 1, 1 with the units, the sum (9, 0, 0); nothing kept;
(b) two arrivals of 9, on +X carrying (9, 0, 0) and on -X carrying
    (-9, 0, 0): 4 back each way and 1 forward each, 5 on +X and 5 on -X,
    and 2 on each transverse side (1 + 1), [5, 5, 2, 2, 2, 2], no
    cancellation (under the coherent rule the same two in antiphase would
    leave 9 and 9 along x and nothing transverse; the phase-less integers
    alone are asserted here); every phase 0; the x momentum per heading
    1 - 4 = -3 on +X, 4 - 1 = 3 on -X and 0 transverse, the sum (0, 0, 0);
    the edge: 2 units on +X carrying (2, 0, 0) with the 9 on -X: the 2 go
    whole on +X with (2, 0, 0) and the 9 scatter as in (a) mirrored,
    [6, 1, 1, 1, 1, 1];
(c) the push reads the flow: a measured event of content 4 (number 2) of a
    phase-less free family at a Node where 9 units of number 1 arrive on +X
    travel and 9 on -X travel, the labels rewritten to (9, 0, 0) and
    (-3, 0, 0): the flow (0, 0, 0), the push (0, 0, 0), while the labels
    sum to (6, 0, 0); the units scatter on, the departures
    [5, 5, 2, 2, 2, 2], and the momentum in transit the books report is the
    labels' sum (6, 0, 0), exact; a lone 9 on +X travel: the flow
    (9, 0, 0), the push -4 x (9, 0, 0) = (-36, 0, 0), the measured event's
    momentum (-36, 0, 0).
"""

from __future__ import annotations

from event_universe.events import EventSimulation, parse_event_world
from event_universe.events.transit import HEADINGS, Transit

PLUS_X, MINUS_X, PLUS_Y, MINUS_Y, PLUS_Z, MINUS_Z = range(6)


def one_node() -> Transit:
    """One Node, one number, a family without a phase circle, tick 1."""
    transit = Transit(0, (1, 1, 1), (1,), 8, 1 << 20, phased=False)
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


def test_two_arrivals_through_opposite_ports_scatter_each_on_its_own_without_cancelling():
    """(b)."""
    transit = one_node()
    arrive(transit, PLUS_X, 9, (9, 0, 0))
    arrive(transit, MINUS_X, 9, (-9, 0, 0))
    amounts, phases, momenta = scattered(transit)
    assert amounts == [5, 5, 2, 2, 2, 2]
    assert phases == [0, 0, 0, 0, 0, 0]
    assert [m[0] for m in momenta] == [-3, 3, 0, 0, 0, 0]
    assert [sum(m[axis] for m in momenta) for axis in range(3)] == [0, 0, 0]
    transit = one_node()
    arrive(transit, PLUS_X, 2, (2, 0, 0))
    arrive(transit, MINUS_X, 9, (-9, 0, 0))
    amounts, _, momenta = scattered(transit)
    assert amounts == [6, 1, 1, 1, 1, 1]
    assert [m[0] for m in momenta] == [2 - 4, -1, -1, -1, -1, -1]


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
