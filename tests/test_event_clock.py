"""The clock of a measured event under the law of events (Highlights 5.4, the
model owner, 2026-09-19: "every clock tick there is self-creation, that is,
no transfer to the next Port"): its age is the count of its self-creations,
and every rate is read off it by whole division, no remainder anywhere
(`by_clock`). The expected integers of docs/TEST_EXPECTATIONS.md ("The clock
of a measured event"), written down first:

(a) `by_clock`: at rate 3 / 10 the gains over ages 0 to 9 are
    0, 0, 0, 1, 0, 0, 1, 0, 0, 1 (a unit at the self-creations to ages 4, 7
    and 10), three in ten, exact;
(b) a measured event of content 3 at `release` [1, 10] releases one unit per
    Port at its self-creations to ages 4, 7 and 10 and nothing else: 18 units
    released after 10 intervals, 0 after 3; its phase at K = 2 turns by 3 / 2
    per self-creation, 1, 2, 1, 2: six steps after four intervals;
(c) a lamp at rate [1, 3] releases at ages 3, 6 and 9: three units per
    heading after 9 intervals, its content down by their cost and its
    momentum the recoil, zero over six headings. Since 2026-09-19 a release
    costs the emitter by its phase rate (each unit quantum x s, s the turn
    of that self-creation, and a turn of 0 releases nothing), so the world
    of (c) declares K 82: the content 100 then 94 then 88 keeps
    (age + 1) x (content - K) below K through the run, so s = 1 at every
    self-creation and each unit costs quantum x 1 = 1, the content
    100 - 18 = 82 (at the K 2^20 of the other cases s would be 0 and the
    lamp would release nothing); each unit in transit carries content 1 and
    the momentum 1 along its heading;
(d) the step off the clock: content 16 with momentum 16 on +x steps once
    per two self-creations (16 / (16 + 16)), three steps after six
    intervals; with momentum 1 once per seventeen, none after 16 and one
    after 17; the momentum untouched.
"""

from __future__ import annotations

from event_universe.events import EventSimulation, parse_event_world
from event_universe.events.engine import by_clock


def world(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    base: dict[str, object] = {
        "law": "events",
        "model_id": "event-clock-test",
        "shape": [41, 5, 5],
        "boundary": "open",
        "ticks": 17,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 10],
        "suspension": 0,
        "families": [{"name": "m", "kind": "free"}, {"name": "light", "kind": "paid"}],
        "measured": measured,
    }
    base.update(keys)
    return base


def test_by_clock_gains_the_whole_part_exactly():
    """(a)."""
    assert [by_clock(age, 3, 10) for age in range(10)] == [0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
    assert sum(by_clock(age, 7, 3) for age in range(30)) == 70


def test_a_small_measured_event_releases_off_its_clock_and_turns_its_phase():
    """(b): content 3 at rate 1 / 10 releases, and at K = 2 turns 1, 2, 1, 2."""
    simulation = EventSimulation(
        parse_event_world(world([{"position": [20, 2, 2], "family": "m", "amount": 3, "fixed": True}]))
    )
    released = []
    for _ in range(10):
        simulation.step()
        assert simulation.books()["balanced"]
        released.append(simulation.transit_released[0])
    assert released[2] == 0 and released[3] == 6 and released[6] == 12 and released[9] == 18
    simulation = EventSimulation(
        parse_event_world(
            world([{"position": [20, 2, 2], "family": "m", "amount": 3, "fixed": True}], K=2, N=64)
        )
    )
    steps = []
    for _ in range(4):
        simulation.step()
        steps.append(simulation.measured[1].phase_steps)
    assert steps == [1, 3, 4, 6]


def test_a_lamp_releases_off_its_clock_and_takes_the_recoil():
    """(c)."""
    lamp = {
        "position": [20, 2, 2],
        "family": "light",
        "amount": 100,
        "fixed": True,
        "lamp": {"rate": [1, 3]},
    }
    # K 82: the turn is one step at every self-creation of the run, so each
    # unit costs quantum x 1 = 1 (at K 2^20 the turn is 0 and nothing leaves).
    simulation = EventSimulation(parse_event_world(world([lamp], release=[0, 1], K=82)))
    for _ in range(9):
        simulation.step()
        assert simulation.books()["balanced"]
    entry = simulation.measured[1]
    assert simulation.transit_released[1] == 18 and entry.held == [0, 82]
    assert simulation.held_spent[1] == 18 and entry.momentum == [0, 0, 0]
    assert entry.phase_steps == 9 and simulation.content_released[1] == 18
    light = simulation.transits[1]
    assert int(light.arr_con.sum()) + int(light.fly_con.sum()) == 18 - light.escaped_content
    assert set(light.fly_con[light.fly_amt > 0].tolist()) <= {1}


def test_a_measured_event_steps_off_its_clock_with_its_momentum_untouched():
    """(d)."""
    for momentum, ticks, expected_x in ((16, 6, 4 + 3), (1, 16, 4), (1, 17, 5)):
        simulation = EventSimulation(
            parse_event_world(
                world(
                    [{"position": [4, 2, 2], "family": "m", "amount": 16, "momentum": [momentum, 0, 0]}],
                    release=[0, 1],
                )
            )
        )
        for _ in range(ticks):
            simulation.step()
            assert simulation.books()["balanced"]
        entry = simulation.measured[1]
        assert entry.position == (expected_x, 2, 2), (momentum, ticks, entry.position)
        assert entry.momentum == [momentum, 0, 0] and entry.steps == expected_x - 4
