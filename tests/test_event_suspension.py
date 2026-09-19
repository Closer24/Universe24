"""The suspension under the law of events (Highlights 5.4, the model owner,
2026-09-19: "The event carries it; note that the next event is delayed"): an
exit derives its suspension from the sizes read at the Node, the event
carries the count and counts down on itself, and what arrives behind it
waits with it; a measured event whose count is spent reads again and its
clock does not tick while it counts. The expected integers of
docs/TEST_EXPECTATIONS.md ("The suspension"), written down first:

(a) a unit of light arriving at a Node together with 16 units of a free
    family (the size 32 sqrt 16 = 128 in 32nds, 4 whole units) at
    `suspension` 1 carries the count 4: it is held at the Node for intervals
    1 to 4, its count read after each interval 3, 2, 1, 0, and leaves in
    interval 5; a second unit arriving in interval 2 joins it and leaves
    with it, the two together;
(b) a measured event of light (content 1, measuring the free family so that
    nothing of it mixes on) at a Node where 16 units of the free family
    arrive in interval 1 is suspended for 4 intervals: its clock is 0 after
    interval 4 and 2 after interval 6, its intervals waited 4, and its phase
    does not move meanwhile.
"""

from __future__ import annotations

from event_universe.events import EventSimulation, parse_event_world

PLUS_X = 0
FAMILIES = [{"name": "m", "kind": "free"}, {"name": "light", "kind": "paid"}]


def world(in_transit: list[dict[str, object]], measured: list[dict[str, object]]) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "event-suspension-test",
        "shape": [9, 3, 3],
        "boundary": "open",
        "ticks": 6,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 1,
        "families": FAMILIES,
        "measured": measured,
        "in_transit": in_transit,
    }


MASS = {"position": [0, 1, 1], "family": "m", "amount": 16, "fixed": True}
LAMP = {"position": [8, 1, 1], "family": "light", "amount": 4, "fixed": True}


def test_a_suspended_event_counts_down_on_itself_and_the_next_waits_with_it():
    """(a)."""
    simulation = EventSimulation(
        parse_event_world(
            world(
                [
                    {
                        "position": [4, 1, 1],
                        "family": "m",
                        "number": 1,
                        "heading": [1, 0, 0],
                        "amount": 16,
                    },
                    {
                        "position": [4, 1, 1],
                        "family": "light",
                        "number": 2,
                        "heading": [1, 0, 0],
                        "amount": 1,
                    },
                    {
                        "position": [3, 1, 1],
                        "family": "light",
                        "number": 2,
                        "heading": [1, 0, 0],
                        "amount": 1,
                    },
                ],
                [MASS, LAMP],
            )
        )
    )
    light = simulation.transits[1]
    counts = []
    for tick in range(1, 6):
        simulation.step()
        assert simulation.books()["balanced"], tick
        counts.append(int(light.suspended[4, 1, 1, 0]))
        if tick < 5:
            assert int(light.fly_amt[4, 1, 1, 0].sum()) == 0, tick
    assert counts == [3, 2, 1, 0, 0]
    assert int(light.fly_amt[4, 1, 1, 0, PLUS_X]) == 2 and int(light.arr_amt.sum()) == 0


def test_a_measured_event_is_suspended_by_the_sizes_it_reads_and_its_clock_waits():
    """(b)."""
    probe = {
        "position": [4, 1, 1],
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"m": "measure"},
    }
    simulation = EventSimulation(
        parse_event_world(
            world(
                [
                    {
                        "position": [4, 1, 1],
                        "family": "m",
                        "number": 1,
                        "heading": [1, 0, 0],
                        "amount": 16,
                    }
                ],
                [MASS, probe],
            )
        )
    )
    entry = simulation.measured[2]
    ages = []
    for tick in range(1, 7):
        simulation.step()
        assert simulation.books()["balanced"], tick
        ages.append(entry.age)
    assert ages == [0, 0, 0, 0, 1, 2]
    assert entry.waited == 4 and entry.owed == 0 and entry.phase == 0
