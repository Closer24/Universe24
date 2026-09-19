"""The suspension under the law of events (Highlights 5.4, the model owner,
2026-09-19: "The event carries it; note that the next event is delayed"; "a
measured event that reads a large size releases and turns slower"; the model
owner, 2026-09-19, the suspension reads presence): a reader derives its
suspension from the presence at its Node, the amount that arrived this
interval over every family and every number but its own, times the world's
`suspension` `[n, d]`, the whole part, no amplitude and no square root; the
event carries the count and counts down on itself, and what arrives behind
it waits with it; a measured event reads the presence after its
self-creation and pays the count, one per interval, before its next one, so
its clock is slowed, never stopped. The expected integers of
docs/TEST_EXPECTATIONS.md ("The suspension"), written down first:

(a) a unit of light arriving at a Node together with 16 units of a free
    family at `suspension` [1, 4] reads the presence 16 and carries the count
    16 x 1 // 4 = 4: it is held at the Node for intervals 1 to 4, its count
    read after each interval 3, 2, 1, 0, and leaves in interval 5; a second
    unit arriving in interval 2 joins it and leaves with it, the two together;
(b) a measured event of light (content 1, measuring the free family so that
    nothing of it mixes on) at a Node where 16 units of the free family
    arrive in interval 1 owes nothing in interval 1, so it is created again
    (age 1) and then reads the presence of the 16 units: 16 x 1 // 4 = 4
    owed; intervals 2 to 5 pay them, 3, 2, 1, 0 left, with no
    self-creation; interval 6 is a self-creation again (age 2) that reads
    an empty Node and owes nothing. Its age after intervals 1 to 6: 1, 1,
    1, 1, 1, 2; its intervals waited 4, nothing owed, its phase 0 (K 2^20);
(c) a steady field: a content of the free family of 2048 at `release`
    [1, 128] at the corner x = 0 of a bar of 2 x 1 x 1, five of its six
    exits off the open board, and a measured event of light (content 1,
    measuring the free family, `suspension` [1, 4]) at x = 1. The source is
    created again every interval (nothing of another number reaches it:
    age 30 after 30 intervals) and 16 units reach the probe in every
    interval from the second on (measured: 16 x 29 = 464 units taken after
    30; since 2026-09-19 a free family's units carry no content, its release
    costs nothing, so the probe's content stays [0, 1] where it read
    [464, 1] before), the presence 16, k = 16 x 1 // 4 = 4. The probe: interval 1 a
    self-creation (age 1) that reads nothing; interval 2 a self-creation
    (age 2) that reads 16 and owes 4; intervals 3 to 6 paid; interval 7 a
    self-creation (age 3) that owes 4 again; and so on, once every
    k + 1 = 5 intervals: ages after intervals 1 to 7 are 1, 2, 2, 2, 2, 2,
    3; after 10, 20 and 30 they are 3, 5, 7 (the self-creations at 12, 17,
    22 and 27); after 30 the probe has waited 23 and owes 1. The clock is
    slowed by 1 / 5, not frozen: the age after 30 exceeds the age after 10;
(d) light on light: 16 units of light of number 1 and one unit of light of
    number 2 arrive at one Node on +X in interval 1. At [1, 4] the unit
    reads the presence 16 (the crowd of the other number, the same family)
    and carries 16 x 1 // 4 = 4: its count after intervals 1 to 5 is 3, 2,
    1, 0, 0 and it is a departure of its Node only after interval 5; the
    crowd reads 1, 1 x 1 // 4 = 0, and leaves in interval 1. At [1, 4096]
    the unit reads 16 x 1 // 4096 = 0 and leaves in interval 1 with the
    crowd (its departure on +X after interval 1, nothing held);
(e) one presence, two readers: at a Node with a measured event of light
    (content 1, number 2, measuring the free family and passing light, so
    that the unit is not taken), 16 units of the free
    family (number 1) and one unit of light of a third measured event
    (number 3) arrive on +X in interval 1, `suspension` [1, 4]. The unit in
    transit reads the presence of every number but its own, the 16 units and
    the measured event's content, here (one reading set, 2026-09-19; until
    then 16, the content unread), 16 + 1 = 17, and carries 17 x 1 // 4 = 4
    (3 after interval 1 pays one); the measured event, after its
    self-creation, reads every number but its own, 16 + 1 = 17, and owes
    17 x 1 // 4 = 4: the same count from the same presence. At [1, 16] both
    read 1 (17 // 16).
"""

from __future__ import annotations

from event_universe.events import EventSimulation, parse_event_world

PLUS_X = 0
FAMILIES = [{"name": "m", "kind": "free"}, {"name": "light", "kind": "paid"}]


def world(
    in_transit: list[dict[str, object]],
    measured: list[dict[str, object]],
    suspension: object = (1, 4),
) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "event-suspension-test",
        "shape": [9, 3, 3],
        "boundary": "open",
        "ticks": 6,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": list(suspension) if isinstance(suspension, tuple) else suspension,
        "families": FAMILIES,
        "measured": measured,
        "in_transit": in_transit,
    }


MASS = {"position": [0, 1, 1], "family": "m", "amount": 16, "fixed": True}
LAMP = {"position": [8, 1, 1], "family": "light", "amount": 4, "fixed": True}


def unit(position: list[int], family: str, number: int, amount: int) -> dict[str, object]:
    return {
        "position": position,
        "family": family,
        "number": number,
        "heading": [1, 0, 0],
        "amount": amount,
    }


def test_a_suspended_event_counts_down_on_itself_and_the_next_waits_with_it():
    """(a)."""
    simulation = EventSimulation(
        parse_event_world(
            world(
                [
                    unit([4, 1, 1], "m", 1, 16),
                    unit([4, 1, 1], "light", 2, 1),
                    unit([3, 1, 1], "light", 2, 1),
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


def test_a_measured_event_is_suspended_by_the_presence_it_reads_and_its_clock_waits():
    """(b)."""
    probe = {
        "position": [4, 1, 1],
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"m": "measure"},
    }
    simulation = EventSimulation(parse_event_world(world([unit([4, 1, 1], "m", 1, 16)], [MASS, probe])))
    entry = simulation.measured[2]
    ages = []
    for tick in range(1, 7):
        simulation.step()
        assert simulation.books()["balanced"], tick
        ages.append(entry.age)
    assert ages == [1, 1, 1, 1, 1, 2]
    assert entry.waited == 4 and entry.owed == 0 and entry.phase == 0
    assert entry.age + entry.waited == simulation.tick


def test_a_measured_event_in_a_steady_field_is_slowed_by_its_count_and_never_frozen():
    """(c)."""
    source = {"position": [0, 0, 0], "family": "m", "amount": 2048, "fixed": True}
    probe = {
        "position": [1, 0, 0],
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"m": "measure"},
    }
    definition = world([], [source, probe])
    definition.update({"shape": [2, 1, 1], "ticks": 30, "release": [1, 128]})
    simulation = EventSimulation(parse_event_world(definition))
    source_entry, entry = simulation.measured[1], simulation.measured[2]
    ages = []
    for tick in range(1, 31):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert entry.age + entry.waited == tick
        ages.append(entry.age)
    assert ages[:7] == [1, 2, 2, 2, 2, 2, 3]
    assert (ages[9], ages[19], ages[29]) == (3, 5, 7)
    assert ages[29] > ages[9]
    assert entry.waited == 23 and entry.owed == 1
    # The 464 units of the free family were taken, carrying no content: a
    # free family's release costs nothing and gives nothing (2026-09-19).
    assert source_entry.age == 30 and entry.held == [0, 1]
    assert entry.measured[0]["measure"] == 464 and simulation.transit_absorbed[0] == 464
    assert simulation.held_measured[0] == 0 and simulation.content_absorbed[0] == 0


def test_a_crowd_of_a_paid_family_suspends_a_unit_of_another_number_of_it():
    """(d): light on light, at [1, 4] and at [1, 4096]."""
    lamp_two = {"position": [0, 1, 1], "family": "light", "amount": 4, "fixed": True}
    for width, expected_counts, departed_first in (
        ((1, 4), [3, 2, 1, 0, 0], 0),
        ((1, 4096), [0, 0, 0, 0, 0], 1),
    ):
        simulation = EventSimulation(
            parse_event_world(
                world(
                    [unit([4, 1, 1], "light", 1, 16), unit([4, 1, 1], "light", 2, 1)],
                    [LAMP, lamp_two],
                    width,
                )
            )
        )
        light = simulation.transits[1]
        crowd, single = light.rank[1], light.rank[2]
        counts = []
        for tick in range(1, 6):
            simulation.step()
            assert simulation.books()["balanced"], (width, tick)
            counts.append(int(light.suspended[4, 1, 1, single]))
            if tick == 1:
                assert int(light.suspended[4, 1, 1, crowd]) == 0
                assert int(light.fly_amt[4, 1, 1, crowd].sum()) == 16
                assert int(light.fly_amt[4, 1, 1, single, PLUS_X]) == departed_first, width
        assert counts == expected_counts, width
        if departed_first == 0:
            assert int(light.fly_amt[4, 1, 1, single, PLUS_X]) == 1


def test_a_unit_in_transit_and_a_measured_event_read_the_same_presence():
    """(e): the same count from the same presence, each less its own number."""
    probe = {
        "position": [4, 1, 1],
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"m": "measure", "light": "pass"},
    }
    for width, expected in (((1, 4), 4), ((1, 16), 1)):
        simulation = EventSimulation(
            parse_event_world(
                world(
                    [unit([4, 1, 1], "m", 1, 16), unit([4, 1, 1], "light", 3, 1)],
                    [MASS, probe, LAMP],
                    width,
                )
            )
        )
        light = simulation.transits[1]
        simulation.step()
        assert simulation.books()["balanced"], width
        entry = simulation.measured[2]
        # The unit's count was written at 16 x n // d and paid by one in the
        # cycle; the measured event's was written after its self-creation.
        assert int(light.suspended[4, 1, 1, light.rank[3]]) == expected - 1, width
        assert entry.owed == expected and entry.age == 1, width
