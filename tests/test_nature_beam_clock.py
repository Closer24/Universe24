"""The clock of a measured event under the law of the ray (docs/RAY_LAW.md,
section 3, step 5, "unchanged in form"; the model owner, 2026-09-19: "every
clock tick there is self-creation"): the age is the count of self-creations
and every rate is read off it by whole division (`by_clock`), no remainder
anywhere; the lamp's release costs it by its phase rate (E = h f); the
owed count is read off the clock from the presence; the step by the
momentum; no merge. Re-pinned from `test_event_clock`,
`test_release_costs_by_phase_rate` and `test_border_and_clock_corrections`
(a, c) under the ray law. The expected integers of docs/TEST_EXPECTATIONS.md
("The clock under the ray law"), written down first:

(a) `by_clock`: at rate 3 / 10 the gains over ages 0 to 9 are 0, 0, 0, 1,
    0, 0, 1, 0, 0, 1; 70 over 30 ages at 7 / 3; `apportion_whole`: 7 over
    [3, 3, 0, 0, 0, 1] from 0 is [3, 3, 0, 0, 0, 1], 5 over [2, 2, 2, 0, 0,
    0] from 2 is [2, 1, 2, 0, 0, 0];
(b) a measured event of content 3 at `release` [1, 10] releases one ray per
    declared direction (the six headings) at its self-creations to ages 4, 7
    and 10: 18 released after 10 intervals, 0 after 3; at K 2 its phase
    steps after four intervals are 1, 3, 4, 6;
(c) a lamp of content 100 at rate [1, 3] on six headings, K 82 (the turn 1
    at every self-creation): 18 rays after 9 intervals, each of content 1,
    the content 82, 9 phase steps, the recoil zero over six headings; two
    lamps of turns 4 and 8 (K 4096, contents 4 K + 32 and 8 K + 64, one
    ray per self-creation toward a counter 3 Links away on a 7 x 1 x 1
    bar): after 8 intervals A spent 8 x 4 = 32 and B 8 x 8 = 64, the
    releases of intervals 1 to 3 clicked in intervals 6 to 8 (a ray created
    at tick t first walks at t + 1 and 3 Links take 5 walks): 6 clicks, the
    counter's content 1 + 3 x 4 + 3 x 8 = 37, its momentum (-768, 0, 0)
    (the labels 4 x 64 and 8 x 64 along +X and -X: since 2026-09-19 the
    label of a unit along a heading is Q e_d, Q = 64, RAY_LAW section 2
    and note 23; A's recoil (-2048, 0, 0), B's (4096, 0, 0)), each click
    record with `content` 4 or 8, 10 rays in flight carrying 60, the books
    balanced; a lamp of turn 0 releases nothing;
(d) the step: content 16 with momentum 1024 (16 x 64, one unit of net
    flow in label units) on +x steps once per two self-creations (three
    after six intervals); with momentum 64 none after 16 and one after 17;
    the momentum untouched; a step onto a Node that holds a measured event
    is refused, both remain, the step counted;
(e) the count off the clock: a source of `m` of content k at x = 0 of a
    2 x 1 x 1 bar releasing k rays per direction per self-creation at
    `release` [1, 1] and a probe of `light` (content 1, measuring `m`) at
    x = 1 at `suspension` [1, 4]: the probe reads the presence k every
    interval from the second on (a ray steps at its first interval), and
    with k = 1 owes `by_clock(age, 1, 4)`, 1 at the self-creations from the
    ages 3, 7, 11, 15: its age after intervals 1 to 20 is 1, 2, 3, 4, 4, 5,
    6, 7, 8, 8, 9, 10, 11, 12, 12, 13, 14, 15, 16, 16; with k = 8 it owes 2
    at every self-creation: 1, 2, 2, 2, 3, 3, 3, 4, 4, 4.
"""

from __future__ import annotations

from event_universe.core.integer import apportion_whole, by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.engine import count_owed

M, LIGHT = 0, 1


def world(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    base: dict[str, object] = {
        "law": "rays",
        "model_id": "ray-clock-test",
        "shape": [41, 5, 5],
        "boundary": "open",
        "ticks": 17,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 10],
        "suspension": 0,
        "families": [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1}],
        "measured": measured,
    }
    base.update(keys)
    return base


def test_by_clock_and_apportion_whole_are_exact():
    """(a)."""
    assert [by_clock(age, 3, 10) for age in range(10)] == [0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
    assert sum(by_clock(age, 7, 3) for age in range(30)) == 70
    assert apportion_whole(7, [3, 3, 0, 0, 0, 1], 0) == [3, 3, 0, 0, 0, 1]
    assert apportion_whole(5, [2, 2, 2, 0, 0, 0], 2) == [2, 1, 2, 0, 0, 0]
    assert apportion_whole(0, [1] * 6, 3) == [0] * 6


def test_a_small_measured_event_releases_off_its_clock_and_turns_its_phase():
    """(b)."""
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(
            world([{"position": [20, 2, 2], "family": "m", "amount": 3, "fixed": True}])
        )
    )
    released = []
    for _ in range(10):
        simulation.step()
        assert simulation.books()["balanced"]
        released.append(simulation.ledger.transit_released[M])
    assert released[2] == 0 and released[3] == 6 and released[6] == 12 and released[9] == 18
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(
            world([{"position": [20, 2, 2], "family": "m", "amount": 3, "fixed": True}], K=2)
        )
    )
    steps = []
    for _ in range(4):
        simulation.step()
        steps.append(simulation.measured[1].phase_steps)
    assert steps == [1, 3, 4, 6]


def lamp(x: int, amount: int, direction: list[int], rate: list[int]) -> dict[str, object]:
    return {
        "position": [x, 0, 0],
        "family": "light",
        "amount": amount,
        "fixed": True,
        "lamp": {"rate": rate, "directions": [direction]},
    }


def test_a_lamp_releases_off_its_clock_at_the_cost_of_its_turn_and_takes_the_recoil():
    """(c)."""
    six = {
        "position": [20, 2, 2],
        "family": "light",
        "amount": 100,
        "fixed": True,
        "lamp": {"rate": [1, 3]},
    }
    simulation = NatureBeamSimulation(parse_nature_beam_world(world([six], release=[0, 1], K=82)))
    for _ in range(9):
        simulation.step()
        assert simulation.books()["balanced"]
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    assert simulation.ledger.transit_released[LIGHT] == 18 and entry.held == [0, 82]
    assert simulation.ledger.held_spent[LIGHT] == 18 and entry.momentum == [0, 0, 0]
    assert entry.phase_steps == 9 and simulation.ledger.content_released[LIGHT] == 18
    escaped = simulation.ledger.escaped_units(LIGHT)
    assert int(light.amount.sum()) + escaped == 18 and set(light.content.tolist()) == {1}

    clock = 4096
    counter = {
        "position": [3, 0, 0],
        "family": "m",
        "amount": 1,
        "fixed": True,
        "table": {"light": "measure"},
    }
    pair = world(
        [
            lamp(0, 4 * clock + 32, [1, 0, 0], [1, 1]),
            counter,
            lamp(6, 8 * clock + 64, [-1, 0, 0], [1, 1]),
        ],
        shape=[7, 1, 1],
        K=clock,
        release=[0, 1],
        detectors=[{"name": "d", "positions": [[3, 0, 0]], "threshold": 1}],
    )
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(pair), records.append)
    slow, gate, fast = simulation.measured[1], simulation.measured[2], simulation.measured[3]
    for tick in range(1, 9):
        simulation.step()
        assert simulation.books()["balanced"], tick
    assert (
        simulation.ledger.held_spent[LIGHT] == 96
        and slow.held == [0, 4 * clock]
        and fast.held == [0, 8 * clock]
    )
    assert slow.phase_steps == 32 and fast.phase_steps == 64
    assert slow.momentum == [-2048, 0, 0] and fast.momentum == [4096, 0, 0]
    clicks = [r for r in records if r["event"] == "click"]
    assert [r["tick"] for r in clicks] == [6, 6, 7, 7, 8, 8]
    assert sorted(r["content"] for r in clicks) == [4, 4, 4, 8, 8, 8]
    assert gate.held == [1, 3 * 4 + 3 * 8] and gate.events == [0, 6] and gate.momentum == [-768, 0, 0]
    light = simulation.stores[LIGHT]
    assert int(light.amount.sum()) == 10 and int((light.amount * light.content).sum()) == 5 * 4 + 5 * 8
    # A turn of 0 releases nothing.
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world([lamp(0, 4, [1, 0, 0], [1, 1])], shape=[7, 1, 1], release=[0, 1]))
    )
    for _ in range(5):
        simulation.step()
    assert simulation.stores[LIGHT].size == 0 and simulation.measured[1].held == [0, 4]


def test_a_measured_event_steps_off_its_clock_and_a_step_onto_another_is_refused():
    """(d)."""
    for momentum, ticks, expected_x in ((1024, 6, 4 + 3), (64, 16, 4), (64, 17, 5)):
        simulation = NatureBeamSimulation(
            parse_nature_beam_world(
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
    mover = {"position": [0, 0, 0], "family": "m", "amount": 16, "momentum": [1024, 0, 0]}
    resident = {"position": [1, 0, 0], "family": "m", "amount": 16}
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world([mover, resident], shape=[3, 1, 1], release=[0, 1], K=16)),
        records.append,
    )
    for tick in range(1, 7):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], tick
        first, second = simulation.measured[1], simulation.measured[2]
        assert first.position == (0, 0, 0) and second.position == (1, 0, 0), tick
        assert first.momentum == [1024, 0, 0] and second.momentum == [0, 0, 0], tick
        assert first.steps == tick // 2 and second.steps == 0, tick
        assert books["families"]["m"]["measured"]["current"] == 32
    assert records == []


def ages_of_a_probe(presence: int, ticks: int) -> tuple[list[int], int, int]:
    source = {"position": [0, 0, 0], "family": "m", "amount": presence, "fixed": True}
    probe = {
        "position": [1, 0, 0],
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"m": "measure"},
    }
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(
            world([source, probe], shape=[2, 1, 1], release=[1, 1], suspension=[1, 4])
        )
    )
    entry = simulation.measured[2]
    ages = []
    for tick in range(1, ticks + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert entry.age + entry.waited == tick
        assert simulation.measured[1].age == tick
        if tick > 1 and entry.creating:
            assert entry.presence == presence, tick
        ages.append(entry.age)
    return ages, entry.waited, entry.owed


def test_the_count_a_measured_event_owes_is_read_off_its_clock():
    """(e)."""
    assert [by_clock(age, 1, 4) for age in range(8)] == [0, 0, 0, 1, 0, 0, 0, 1]
    # The owed count, the one place it lives (`engine.count_owed`).
    assert [count_owed(age, 1, (1, 4)) for age in range(8)] == [0, 0, 0, 1, 0, 0, 0, 1]
    assert count_owed(2, 8, (1, 4)) == 2 and count_owed(5, 9, (0, 1)) == 0
    ages, waited, owed = ages_of_a_probe(1, 20)
    assert ages == [1, 2, 3, 4, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 12, 13, 14, 15, 16, 16]
    assert waited == 4 and owed == 0
    ages, waited, owed = ages_of_a_probe(8, 10)
    assert ages == [1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    assert waited == 6 and owed == 0
