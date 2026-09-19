"""An event in transit under the law of events (Highlights 5.4, the model
owner, 2026-09-19): a single quantum goes whole in one direction, by its
momentum, and does not turn; a part a crowded Node turned back returns to its
momentum's line at the next lone Node. The expected integers of
docs/TEST_EXPECTATIONS.md ("An event in transit"), written down first:

(a) one unit of a paid family with quantum 3 released on +X at phase 5 walks
    a bar of seven Nodes one Link per interval, whole, its phase 5 at every
    Node (no turn in transit), its momentum (3, 0, 0), and escapes at the
    edge with it;
(b) nine units on +X carrying (9, 0, 0) at a Node send 4 back with
    (12, 0, 0) at quantum 3; at the next Node the 4 are apportioned again,
    2 back toward +X (one by the share, 4 x 4 / 9, one by the largest
    remainder) and one to each of two transverse headings, nothing kept;
    two units carrying (6, 0, 0) alone at a Node, no side reaching a whole,
    go whole to +X;
(c) a lone unit of a free family carrying its momentum from birth goes
    straight too: a measured event of content 1 releasing at rate 1 per
    Port sends one unit each way every interval, and the first six are at
    distance two after three intervals, created outward, none turned back.
"""

from __future__ import annotations

from event_universe.events import EventSimulation, parse_event_world

PLUS_X, MINUS_X = 0, 1


def bar(in_transit: list[dict[str, object]], families: list[dict[str, object]]) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "event-transit-test",
        "shape": [7, 3, 3],
        "boundary": "open",
        "ticks": 8,
        "K": 16,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": families,
        "measured": [{"position": [0, 1, 1], "family": families[0]["name"], "amount": 4, "fixed": True}],
        "in_transit": in_transit,
    }


LIGHT = [{"name": "light", "kind": "paid", "quantum": 3}]


def departures(simulation: EventSimulation, family: int = 0) -> list[tuple[int, int, int, int, int]]:
    transit = simulation.transits[family]
    return [
        (int(x), int(y), int(z), int(port), int(transit.fly_amt[x, y, z, n, port]))
        for x, y, z, n, port in zip(*transit.fly_amt.nonzero(), strict=True)
    ]


def test_a_single_quantum_goes_whole_by_its_momentum_and_does_not_turn():
    """(a)."""
    world = bar(
        [
            {
                "position": [1, 1, 1],
                "family": "light",
                "number": 1,
                "heading": [1, 0, 0],
                "amount": 1,
                "phase": 5,
            }
        ],
        LIGHT,
    )
    simulation = EventSimulation(parse_event_world(world))
    transit = simulation.transits[0]
    for tick in range(1, 7):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert departures(simulation) == [(tick, 1, 1, PLUS_X, 1)], tick
        assert int(transit.fly_ph[tick, 1, 1, 0, PLUS_X]) == 5
        assert transit.fly_mom[tick, 1, 1, 0, PLUS_X].tolist() == [3, 0, 0]
    simulation.step()
    assert departures(simulation) == [] and transit.escaped == 1
    assert transit.escaped_momentum.tolist() == [3, 0, 0]


def test_a_part_turned_back_returns_to_its_momentums_line_at_the_next_lone_node():
    """(b)."""
    world = bar(
        [
            {
                "position": [3, 1, 1],
                "family": "light",
                "number": 1,
                "heading": [1, 0, 0],
                "amount": 9,
                "phase": 0,
            }
        ],
        LIGHT,
    )
    simulation = EventSimulation(parse_event_world(world))
    transit = simulation.transits[0]
    simulation.step()
    assert int(transit.fly_amt[3, 1, 1, 0, MINUS_X]) == 4
    assert transit.fly_mom[3, 1, 1, 0, MINUS_X].tolist() == [4 * 3, 0, 0]
    simulation.step()
    # The 4 arrived at x = 2 travelling -X: 2 back toward +X, 2 transverse.
    assert int(transit.fly_amt[2, 1, 1, 0, PLUS_X]) == 2
    assert int(transit.fly_amt[2, 1, 1, 0, MINUS_X]) == 0
    assert int(transit.fly_amt[2, 1, 1, 0].sum()) == 4 and int(transit.arr_amt.sum()) == 0
    world = bar(
        [{"position": [3, 1, 1], "family": "light", "number": 1, "heading": [1, 0, 0], "amount": 2}],
        LIGHT,
    )
    simulation = EventSimulation(parse_event_world(world))
    simulation.step()
    assert departures(simulation) == [(3, 1, 1, PLUS_X, 2)]
    assert simulation.transits[0].fly_mom[3, 1, 1, 0, PLUS_X].tolist() == [6, 0, 0]


def test_a_lone_unit_of_a_free_family_goes_straight_from_its_release():
    """(c)."""
    world = {
        "law": "events",
        "model_id": "event-transit-test-free",
        "shape": [7, 7, 7],
        "boundary": "open",
        "ticks": 3,
        "K": 16,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "families": [{"name": "m", "kind": "free"}],
        "measured": [{"position": [3, 3, 3], "family": "m", "amount": 1, "fixed": True}],
    }
    simulation = EventSimulation(parse_event_world(world))
    simulation.step()
    assert sorted(departures(simulation)) == sorted([(3, 3, 3, port, 1) for port in range(6)])
    for _ in range(2):
        simulation.step()
    # After the first release two more were made; the first six are at
    # distance two, none turned back, and the books close.
    assert simulation.books()["balanced"]
    far = [entry for entry in departures(simulation) if max(abs(v - 3) for v in entry[:3]) == 2]
    assert len(far) == 6 and all(amount == 1 for *_, amount in far)
    assert all(entry[port_axis(port)] - 3 == port_sign(port) * 2 for *entry, port, _ in far)


def port_axis(port: int) -> int:
    return port >> 1


def port_sign(port: int) -> int:
    return 1 if port % 2 == 0 else -1
