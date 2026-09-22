"""The clock of a measured event under the Beam Law (docs/BEAM_LAW.md,
section 3, step 5, "unchanged in form"; the model owner, 2026-09-19: "every
clock tick there is self-creation"): the age is the count of self-creations
and every rate is read off it by whole division (`by_clock`), no remainder
anywhere; the lamp's release costs it by its phase rate (E = h f); the
owed count is read off the clock from the presence; the step by the
momentum; no merge. Re-pinned from `test_event_clock`,
`test_release_costs_by_phase_rate` and `test_border_and_clock_corrections`
(a, c) under the Beam Law. The expected integers of docs/TEST_EXPECTATIONS.md
("The clock under the Beam Law"), written down first:

(a) `by_clock`: at rate 3 / 10 the gains over ages 0 to 9 are 0, 0, 0, 1,
    0, 0, 1, 0, 0, 1; 70 over 30 ages at 7 / 3; `apportion_whole`: 7 over
    [3, 3, 0, 0, 0, 1] from 0 is [3, 3, 0, 0, 0, 1], 5 over [2, 2, 2, 0, 0,
    0] from 2 is [2, 1, 2, 0, 0, 0];
(b) a measured event of content 3 at `release` [1, 10] releases one ray per
    declared direction (the six headings) at its self-creations to ages 4, 7
    and 10: 18 released after 10 intervals, 0 after 3; at K 2 its phase
    steps after four intervals are 1, 3, 4, 6;
(c) a lamp of content 100 at rate [1, 3] on six headings, K 82: the count
    of the rate's accumulator is 1 at the self-creations of the ages 2, 5
    and 8 (`by_drive` on [1, 3]: 0, 0, 1, ...), 18 rays after 9 intervals,
    each of content its turn; the turn is the count of the turn's
    accumulator over K (the fraction-free law, 2026-09-20): 100, 118, 136
    give 1, 1, 1 (the remainder 54), the release of the age 2 costs 6 and
    the content 94, 148, 160 give 1, 1 (78), 172 gives 2 (the remainder
    8: the exact whole part of the content's history), the release of the
    age 5 costs 12 (the content 82), then 90 gives 1, 1, 1 (8) and the
    release of the age 8 costs 6: the content 76, 10 phase steps, 24
    content released (until the fraction-free law the whole part off the
    clock at the current content, `by_clock(age, content, 82)`, gave 1 at
    every age, the content 82 and 9 phase steps: the stall of a falling
    content read as if it had always been the current one), the recoil
    zero over six headings; two
    lamps of turns 4 and 8 (K 4096, contents 4 K + 32 and 8 K + 64, one
    ray per self-creation toward a counter 3 Links away on a 7 x 1 x 1
    bar): after 8 intervals A spent 8 x 4 = 32 and B 8 x 8 = 64, the
    releases of intervals 1 to 3 clicked in intervals 6 to 8 (a ray created
    at tick t first walks at t + 1 and 3 Links take 5 walks): 6 clicks, the
    counter's content 1 + 3 x 4 + 3 x 8 = 37, its momentum (-768, 0, 0)
    (the labels 4 x 64 and 8 x 64 along +X and -X: since 2026-09-19 the
    label of a unit along a heading is Q e_d, Q = 64, BEAM_LAW section 2
    and note 23; A's recoil (-2048, 0, 0), B's (4096, 0, 0)), each click
    record with `content` 4 or 8, 10 rays in flight carrying 60, the books
    balanced; a lamp of turn 0 releases nothing;
(d) the step: content 16 with momentum 1024 (16 x 64, one unit of net
    flow in label units) on +x steps once per two self-creations (three
    after six intervals); with momentum 64 none after 16 and one after 17;
    the momentum untouched; a step onto a Node that holds a measured event
    is refused and, since 2026-09-20, is a contact read through the
    occupant's table (`measure` by the keys): on a bar of 3 x 1 x 1 the
    mover's step of interval 2 onto the resident hands it the 1024 (one
    `contact` record, the mover's momentum 0, its step counted), the
    resident's drive is 1024 at that interval and 2048 = D at the next
    (the step drive of 2026-09-20), so it steps to x = 2 at interval 3
    with the 1024 and leaves through face:+x at interval 5 (the escaped
    momentum (1024, 0, 0), the measured line 16), the mover at x = 0 with
    one step for the rest (the rule as it was, the count off the clock,
    stepped the resident in the interval of the hand-over and out at 4);
(e) the owed count (`engine.count_owed`, since the fraction-free law of
    2026-09-20 the count the owed accumulator gains, `by_drive(acc, k x n,
    d)`, equal to `by_clock(age, k x n, d)` at a constant k from age 0): a
    source of `m` of content k at x = 0 of a
    2 x 1 x 1 bar releasing k rays per direction per self-creation at
    `release` [1, 1] and a probe of `light` (content 1, measuring `m`) at
    x = 1 at `suspension` [1, 4]: the probe reads the presence k every
    interval from the second on (a ray steps at its first interval; 0 at
    the first self-creation), and with k = 1 owes 1 at every fourth
    self-creation that read 1, the ages 4, 8, 12, 16 (the accumulator 0,
    1, 2, 3, 4 -> 1 owed and 0, ...): its age after intervals 1 to 20 is
    1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9, 10, 11, 12, 13, 13, 14, 15, 16, 17,
    waited 3 and 1 owed at the end (until the fraction-free law the whole
    part off the clock, `by_clock(age, 1, 4)`, counted the first
    self-creation as if it had read 1 and owed at the ages 3, 7, 11, 15:
    1, 2, 3, 4, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 12, 13, 14, 15, 16, 16,
    waited 4); with k = 8 it owes 2 at every self-creation that read 8
    (the accumulator 8 -> 2, 0): 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, waited 6
    (the same ages under both forms);
(f) every age against a key is the one `by_clock` (the four unifications,
    the model owner, 2026-09-20, (2); BEAM_LAW note 33; the integers written
    first): the clock's rate `K` as a pair equal to its integer: the world
    of (b) with `"K": [1, 2]` turns 1, 3, 4, 6 as with `K` 2 and its
    snapshot after ten intervals is the same, the record carrying `K` as
    declared (2, and [1, 2] as the pair); the pair [3, 8] on the content 3
    (the turn `by_clock(age, 9, 8)`) turns 1, 2, 3, 4, 5, 6, 7, 9 over eight
    intervals, `world.turn(7, 3)` = 2; the static bound at the rate: the
    content 86 at [3, 8] is refused (2 x 86 x 3 = 516 >= 8 x 64), 85 is
    accepted (the turn 31); the frame's refusal at half the circle kept:
    the content 63 at [1, 2] passes the parser (126 < 128) and is refused
    at the second interval (the turn `by_clock(1, 63, 2)` = 32); `K` 0,
    [0, 8], [3, 0], "8" and [1, 2, 3] are refused naming `K`;
    `by_clock_rows` over the ages 0 to 9 at 3 / 10 is `by_clock`'s 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, and with a numerator per row; `ages_at_key`
    (`by_clock(age - 1, 1, key)` = 1 for a walked row): the ages 0, 1, 2,
    3, 4, 6 against the key 3 read no, no, no, yes, no, yes, against 1
    every age from 1, against 4 the age 4 and not 3; on the GameBoard a
    family of lifetime 3 with a row at rest (the direction index 0) at the
    age 2 and a moving row at the age 0 (7^3, open, no measured event):
    the moving row clicks on the border at the third interval at (3, 3, 3)
    with the age 3, the rest row keeps the age 2 for twenty intervals and
    never clicks; a family without a lifetime under `age_bound` 3: the
    fourth interval's walk (the age 3 to 4) refuses the run naming the
    bound, the third does not.
"""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.core.integer import apportion_whole, by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.engine import count_owed
from event_universe.events.nature_beam import ages_at_key, by_clock_rows
from event_universe.events.world import LIFETIME_NAME

M, LIGHT = 0, 1


def world(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    base: dict[str, object] = {
        "law": "beam",
        "model_id": "ray-clock-test",
        "shape": [41, 5, 5],
        "boundary": "open",
        "ticks": 17,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 10],
        "suspension": 0,
        "per_axis_drive": True,  # the per-axis drive of history (2026-09-22): the integers as registered
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
        steps.append(simulation.measured[1].turned)
    assert steps == [1, 3, 4, 6]


def lamp(x: int, amount: int, direction: list[int], rate: list[int]) -> dict[str, object]:
    return {
        "position": [x, 0, 0],
        "family": "light",
        "amount": amount,
        "fixed": True,
        "lamp": {"wheel": [1, 64], "rate": rate, "directions": [direction]},
    }


def test_a_lamp_releases_off_its_clock_at_the_cost_of_its_turn_and_takes_the_recoil():
    """(c)."""
    six = {
        "position": [20, 2, 2],
        "family": "light",
        "amount": 100,
        "fixed": True,
        "lamp": {"wheel": [1, 64], "rate": [1, 3]},
    }
    simulation = NatureBeamSimulation(parse_nature_beam_world(world([six], release=[0, 1], K=82)))
    for _ in range(9):
        simulation.step()
        assert simulation.books()["balanced"]
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    assert simulation.ledger.transit_released[LIGHT] == 18 and entry.held == [0, 76]
    assert simulation.ledger.held_spent[LIGHT] == 24 and entry.momentum == [0, 0, 0]
    assert entry.turned == 10 and simulation.ledger.content_released[LIGHT] == 24
    assert entry.acc_turn == 8 and entry.acc_lamp == 0
    escaped = simulation.ledger.escaped_amount(LIGHT)
    assert int(light.amount.sum()) + escaped == 18 and set(light.content.tolist()) == {1, 2}

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
    assert slow.turned == 32 and fast.turned == 64
    assert slow.momentum == [-2048, 0, 0] and fast.momentum == [4096, 0, 0]
    clicks = [r for r in records if r["event"] == "click"]
    assert [r["tick"] for r in clicks] == [6, 6, 7, 7, 8, 8]
    assert sorted(r["content"] for r in clicks) == [4, 4, 4, 8, 8, 8]
    assert gate.held == [1, 3 * 4 + 3 * 8] and gate.clicks == [0, 6] and gate.momentum == [-768, 0, 0]
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
        first = simulation.measured[1]
        assert first.position == (0, 0, 0) and first.momentum == [1024 if tick < 2 else 0, 0, 0], tick
        assert first.steps == min(tick // 2, 1), tick
        if tick < 5:
            second = simulation.measured[2]
            assert second.position == (1 if tick < 3 else 2, 0, 0), tick
            assert second.momentum == [0 if tick < 2 else 1024, 0, 0] and second.steps == (
                0 if tick < 3 else 1
            )
            assert books["families"]["m"]["measured"]["current"] == 32
            assert books["momentum"]["measured"] == [1024, 0, 0]
        else:
            assert 2 not in simulation.measured
            # The measured line carries `became` since 2026-09-20 (the
            # transformation `become`): 0 without one.
            assert books["families"]["m"]["measured"] == {
                "initial": 32,
                "measured": 0,
                "became": 0,
                "current": 16,
                "spent": 0,
                "escaped": 16,
                "balanced": True,
            }
            assert books["momentum"]["escaped"] == [1024, 0, 0]
    assert [(r["event"], r["tick"], r["number"]) for r in records] == [
        ("contact", 2, 1),
        ("step", 3, 2),
        ("click", 5, 2),
    ]
    assert (
        records[0]["component"] == 1024
        and records[0]["occupant"] == 2
        and records[0]["rule"] == "measure"
    )
    assert records[1]["to"] == [2, 0, 0] and records[2]["detector"] == "face:+x"


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
    # The owed count, the one place it lives (`engine.count_owed`): the
    # accumulator's count, `by_clock`'s at a constant presence from 0.
    owed, accumulator = [], 0
    for _ in range(8):
        count, accumulator = count_owed(accumulator, 1, (1, 4))
        owed.append(count)
    assert owed == [0, 0, 0, 1, 0, 0, 0, 1] and accumulator == 0
    assert count_owed(2, 8, (1, 4)) == (2, 2) and count_owed(5, 9, (0, 1)) == (0, 5)
    ages, waited, owed = ages_of_a_probe(1, 20)
    assert ages == [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 9, 10, 11, 12, 13, 13, 14, 15, 16, 17]
    assert waited == 3 and owed == 1
    ages, waited, owed = ages_of_a_probe(8, 10)
    assert ages == [1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    assert waited == 6 and owed == 0


def test_every_age_against_a_key_is_the_one_by_clock():
    """(f)."""
    content_three = {"position": [20, 2, 2], "family": "m", "amount": 3, "fixed": True}
    # The pair [1, K] is the integer K: the same turns, the same snapshot.
    snapshots = []
    for clock in (2, [1, 2]):
        simulation = NatureBeamSimulation(parse_nature_beam_world(world([content_three], K=clock)))
        assert simulation.world.turn_rate == (1, 2)
        assert simulation.world.K == (2 if clock == 2 else (1, 2))
        steps = []
        for _ in range(10):
            simulation.step()
            steps.append(simulation.measured[1].turned)
        assert steps[:4] == [1, 3, 4, 6], clock
        snapshots.append(simulation.snapshot())
    assert snapshots[0] == snapshots[1]
    # A rate with a numerator: [3, 8] on the content 3 turns by_clock(age, 9, 8).
    simulation = NatureBeamSimulation(parse_nature_beam_world(world([content_three], K=[3, 8])))
    assert simulation.world.turn_rate == (3, 8) and simulation.world.turn(7, 3) == 2
    steps = []
    for _ in range(8):
        simulation.step()
        assert simulation.books()["balanced"]
        steps.append(simulation.measured[1].turned)
    assert steps == [1, 2, 3, 4, 5, 6, 7, 9]
    assert steps == [sum(by_clock(age, 9, 8) for age in range(k + 1)) for k in range(8)]
    # The static bound at the rate, and the frame's refusal at half the circle.
    with pytest.raises(ValueError, match="below K x N"):
        parse_nature_beam_world(world([{**content_three, "amount": 86}], K=[3, 8]))
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world([{**content_three, "amount": 85}], K=[3, 8]))
    )
    simulation.step()
    assert simulation.measured[1].turn == 31
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(world([{**content_three, "amount": 63}], K=[1, 2]))
    )
    simulation.step()
    assert simulation.measured[1].turn == 31
    with pytest.raises(ValueError, match="half the circle"):
        simulation.step()
    for bad in (0, [0, 8], [3, 0], "8", [1, 2, 3]):
        with pytest.raises(ValueError, match="K"):
            parse_nature_beam_world(world([content_three], K=bad))
    # The primitive over rows, and every age against a key.
    ages = np.arange(10, dtype=np.int64)
    assert by_clock_rows(ages, 3, 10).tolist() == [by_clock(age, 3, 10) for age in range(10)]
    assert by_clock_rows(ages, ages + 1, 10).tolist() == [by_clock(a, a + 1, 10) for a in range(10)]
    with pytest.raises(ValueError, match="positive denominator"):
        by_clock_rows(ages, 1, 0)
    at = np.array([0, 1, 2, 3, 4, 6], dtype=np.int64)
    assert ages_at_key(at, 3).tolist() == [False, False, False, True, False, True]
    assert ages_at_key(at, 1).tolist() == [False, True, True, True, True, True]
    assert ages_at_key(np.array([3, 4]), 4).tolist() == [False, True]
    # On the GameBoard: the lifetime's click and the age bound are that
    # primitive; a rest row keeps its age and is never at the key.
    rest = {"position": [3, 5, 5], "family": "s", "number": 1, "direction": 0, "amount": 1, "age": 2}
    moving = {"position": [1, 3, 3], "family": "s", "number": 1, "direction": [1, 0, 0], "amount": 1}
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "ray-clock-key-test",
        "shape": [7, 7, 7],
        "boundary": "open",
        "ticks": 20,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "per_axis_drive": True,  # the per-axis drive of history (2026-09-22): the integers as registered
        "families": [{"name": "s", "quantum": 0, "phase": False, "lifetime": 3}],
        "measured": [],
        "in_transit": [rest, moving],
    }
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), records.append)
    store = simulation.stores[0]
    for tick in range(1, 21):
        simulation.step()
        assert simulation.books()["balanced"], tick
        clicks = [r for r in records if r["event"] == "click"]
        assert len(clicks) == (1 if tick >= 3 else 0), tick
        assert sorted(store.age.tolist()) == sorted([2, tick] if tick < 3 else [2]), tick
    assert clicks[0]["tick"] == 3 and clicks[0]["node"] == [3, 3, 3]
    assert clicks[0]["detector"] == LIFETIME_NAME and simulation.ledger.lifetime_amount == [1]
    # A lone rest row flips between the two rest slots by the collision
    # table (a class of two states); it keeps its age.
    assert store.size == 1 and int(store.direction[0]) in (0, 1) and int(store.age[0]) == 2
    bounded_world = {
        **document,
        "families": [{"name": "s", "quantum": 0, "phase": False}],
        "age_bound": 3,
        "in_transit": [moving],
    }
    simulation = NatureBeamSimulation(parse_nature_beam_world(bounded_world))
    for _ in range(3):
        simulation.step()
    assert simulation.stores[0].age.tolist() == [3]
    with pytest.raises(OverflowError, match="beyond the world's age_bound 3"):
        simulation.step()
