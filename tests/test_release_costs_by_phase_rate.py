"""A release costs the emitter by its phase rate (the model owner, 2026-09-19,
"I approve the proposal"; Highlights 5.4, the law of events): at a
self-creation whose turn is s = by_clock(age, content, K) phase steps, each
unit a lamp releases costs it quantum x s content, carries that content and
the momentum quantum x s along its heading, and gives quantum x s content to
the measured event that measures it, so the content of a click is
proportional to the emitter's frequency, E = h f with h the declared
`quantum`. A self-creation whose turn is 0 releases nothing (no quanta of
zero content). A free family's release costs nothing, whatever its turn, and
its units carry no content; its push reads the flow as before. The content
carried goes with the units at every Node exactly, and the books carry a
content line balanced at every interval. Bars, `suspension` 0, N 64 unless
stated, every measured event `fixed`. The expected integers of
docs/TEST_EXPECTATIONS.md ("A release costs the emitter by its phase rate"),
written down first:

(a) two lamps of one paid family `light` (quantum 1) on a bar of 7 x 1 x 1,
    K 4096: lamp A at x = 0 with content 4 K + 32 = 16416 releasing one unit
    per self-creation on +X, lamp B at x = 6 with content 8 K + 64 = 32832
    releasing one unit per self-creation on -X, a counter of `counter` (paid,
    content 1) at x = 3 measuring `light`, the detector `d` of threshold 1.
    The contents keep (age + 1) x (content - s K) below K through the run,
    so A turns s = 4 steps and B s = 8 at every one of its 8 self-creations.
    After 8 intervals: A spent 8 x 1 x 4 = 32 (content 16384, phase steps
    32, phase 32, momentum (-32, 0, 0)), B spent 8 x 8 = 64 (content 32768,
    phase steps 64, phase 0, momentum (64, 0, 0)); the releases of the
    intervals 1 to 5 reached x = 3 in the intervals 4 to 8 (three Links), so
    the counter clicked 10 times and its content grew by 5 x 4 + 5 x 8 = 60
    (its momentum the pushes, 5 x 4 - 5 x 8 = (-20, 0, 0)), each click
    record carrying `content` 4 (A's number 1) or 8 (B's number 3); 6 units
    in transit carrying 3 x 4 + 3 x 8 = 36, A's slots content 4 x amount and
    momentum (4, 0, 0) per unit, B's 8 x amount and (-8, 0, 0); the books
    balanced at every interval, the content line released 96 = current 36 +
    absorbed 60, spent 96 = measured 60 + in transit 36. The arithmetic of
    `apportion_whole`: 7 over [3, 3, 0, 0, 0, 1] from 0 is [3, 3, 0, 0, 0, 1];
    5 over [2, 2, 2, 0, 0, 0] from 2 is [2, 1, 2, 0, 0, 0] (the ties in Port
    order from 2); 0 over anything is zeros;
(b) the free family costs nothing: on a bar of 9 x 3 x 3 at `release`
    [1, 1] a source of `m` (free, content 16) at x = 0 and a reader of `m`
    (content 4, `read`) at x = 4 with 9 units of number 1 arriving on +X in
    interval 1; after one interval the source released 6 x 16 = 96 units
    and the reader, free too, 6 x 4 = 24 (120 released), nothing spent, the
    contents 16 and 4, nothing carried in transit (content 0), the content
    line all zeros, and the reader pushed by the flow as before,
    -4 x (9, 0, 0) = (-36, 0, 0); the momentum in transit the labels' sum
    (9, 0, 0) (the releases of 16 and of 4 cancel); the same with `m` declared
    without a phase circle (K 2^20) and with a phase circle at K 16 (the
    source turning one step per self-creation, still costing nothing);
(c) a turn of 0 releases nothing: on a bar of 5 x 1 x 1, K 64, N 256, a
    source lamp S of `light` (content 60 K = 3840, rate [1, 4] on +X) at
    x = 0 and a lamp L (content 4, rate [1, 1] on +X, measuring `light`) at
    x = 2. L's turn is 0 at the ages 0 to 4 ((age + 1) x 4 < 64), so through
    the intervals 1 to 5 it releases nothing: content 4, spent nothing,
    nothing of its number in transit, phase 0. S turns 60 steps per
    self-creation and releases at age 3 (interval 4) one unit costing
    60 x 1 = 60 (content 3780, momentum (-60, 0, 0)), carrying content 60
    and momentum (60, 0, 0); it reaches L in interval 6: a click of content
    60 (L's content 64 = K, push (60, 0, 0)), and at L's self-creation of
    that interval its turn is by_clock(5, 64, 64) = 1: it releases one unit
    costing 1, carrying content 1 and momentum (1, 0, 0); in interval 7
    (content 63, by_clock(6, 63, 64) = 1) another. After 7 intervals: L's
    content 62, phase steps 2, momentum (58, 0, 0), one click; S at age 7
    with 417 phase steps (60 x 4 + 59 x 3); spent 62 in all, measured 60, 2
    carried in transit with the momentum (2, 0, 0); the books balanced at
    every interval.
"""

from __future__ import annotations

from event_universe.events import EventSimulation, parse_event_world
from event_universe.events.engine import apportion_whole

PLUS_X, MINUS_X = 0, 1
LIGHT, COUNTER = 0, 1


def bar(
    shape: list[int],
    families: list[dict[str, object]],
    measured: list[dict[str, object]],
    clock: int,
    *,
    steps: int = 64,
    release: list[int] | None = None,
    in_transit: list[dict[str, object]] | None = None,
    detectors: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "release-cost-test",
        "shape": shape,
        "boundary": "open",
        "ticks": 8,
        "K": clock,
        "N": steps,
        "release": release or [0, 1],
        "suspension": 0,
        "families": families,
        "measured": measured,
        "in_transit": in_transit or [],
        "detectors": detectors or [],
    }


def lamp(x: int, amount: int, heading: list[int], rate: list[int], **keys: object) -> dict[str, object]:
    return {
        "position": [x, 0, 0],
        "family": "light",
        "amount": amount,
        "fixed": True,
        "lamp": {"rate": rate, "headings": [heading]},
        **keys,
    }


def test_each_unit_costs_its_emitter_quantum_times_its_turn_and_a_click_measures_it():
    """(a)."""
    assert apportion_whole(7, [3, 3, 0, 0, 0, 1], 0) == [3, 3, 0, 0, 0, 1]
    assert apportion_whole(5, [2, 2, 2, 0, 0, 0], 2) == [2, 1, 2, 0, 0, 0]
    assert apportion_whole(0, [1, 1, 1, 1, 1, 1], 3) == [0] * 6
    clock = 4096
    world = bar(
        [7, 1, 1],
        [{"name": "light", "kind": "paid"}, {"name": "counter", "kind": "paid"}],
        [
            lamp(0, 4 * clock + 32, [1, 0, 0], [1, 1]),
            {"position": [3, 0, 0], "family": "counter", "amount": 1, "fixed": True},
            lamp(6, 8 * clock + 64, [-1, 0, 0], [1, 1]),
        ],
        clock,
        detectors=[{"name": "d", "positions": [[3, 0, 0]], "threshold": 1}],
    )
    records: list[dict[str, object]] = []
    simulation = EventSimulation(parse_event_world(world), records.append)
    slow, counter, fast = simulation.measured[1], simulation.measured[2], simulation.measured[3]
    light = simulation.transits[LIGHT]
    for tick in range(1, 9):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], (tick, books)
        # Every unit in transit carries quantum x s content and that
        # content along its heading as its momentum.
        for rank, turn, sign in ((light.rank[1], 4, 1), (light.rank[3], 8, -1)):
            for amounts, contents, momenta in (
                (light.fly_amt, light.fly_con, light.fly_mom),
                (light.arr_amt, light.arr_con, light.arr_mom),
            ):
                amount, content, momentum = (
                    amounts[:, :, :, rank],
                    contents[:, :, :, rank],
                    momenta[:, :, :, rank],
                )
                assert (content == turn * amount).all(), (tick, turn)
                assert (momentum[..., 0] == sign * content).all() and not momentum[..., 1:].any()
    assert slow.age == fast.age == 8 and slow.phase_steps == 32 and fast.phase_steps == 64
    assert slow.phase == 32 and fast.phase == 0
    assert slow.held == [4 * clock, 0] and fast.held == [8 * clock, 0]
    assert slow.momentum == [-32, 0, 0] and fast.momentum == [64, 0, 0]
    assert simulation.held_spent[LIGHT] == 96 and simulation.transit_released[LIGHT] == 16
    assert counter.events == [10, 0] and counter.held == [60, 1]
    assert counter.pushed == [-20, 0, 0] and counter.momentum == [-20, 0, 0]
    assert simulation.held_measured[LIGHT] == 60 and simulation.transit_absorbed[LIGHT] == 10
    assert light.current() == 6 and light.content() == 36 and light.escaped_content == 0
    clicks = [record for record in records if record["event"] == "click"]
    assert len(clicks) == len(records) == 10
    assert (
        sorted((record["number"], record["content"]) for record in clicks) == [(1, 4)] * 5 + [(3, 8)] * 5
    )
    assert all(record["amount"] == 1 and record["tick"] >= 4 for record in clicks)
    line = simulation.books()["families"]["light"]
    assert line["content"] == {
        "initial": 0,
        "released": 96,
        "current": 36,
        "escaped": 0,
        "absorbed": 60,
        "balanced": True,
    }
    assert line["measured"]["spent"] == line["measured"]["measured"] + line["content"]["current"]


def test_a_free_family_costs_nothing_and_its_push_reads_the_flow_as_before():
    """(b)."""
    for family, clock in (
        ({"name": "m", "kind": "free", "phase": False}, 1 << 20),
        ({"name": "m", "kind": "free"}, 16),
    ):
        world = bar(
            [9, 3, 3],
            [family],
            [
                {"position": [0, 1, 1], "family": "m", "amount": 16, "fixed": True},
                {
                    "position": [4, 1, 1],
                    "family": "m",
                    "amount": 4,
                    "fixed": True,
                    "table": {"m": "read"},
                },
            ],
            clock,
            release=[1, 1],
            in_transit=[
                {
                    "position": [4, 1, 1],
                    "family": "m",
                    "number": 1,
                    "heading": [1, 0, 0],
                    "amount": 9,
                }
            ],
        )
        simulation = EventSimulation(parse_event_world(world))
        source, reader, transit = simulation.measured[1], simulation.measured[2], simulation.transits[0]
        simulation.step()
        books = simulation.books()
        assert books["balanced"], family
        assert simulation.transit_released[0] == 96 + 24 and simulation.held_spent[0] == 0, family
        assert source.held == [16] and simulation.content_released[0] == 0, family
        assert transit.content() == 0 and not transit.fly_con.any(), family
        assert books["families"]["m"]["content"] == {
            "initial": 0,
            "released": 0,
            "current": 0,
            "escaped": 0,
            "absorbed": 0,
            "balanced": True,
        }, family
        assert reader.pushed == [-36, 0, 0] and reader.momentum == [-36, 0, 0], family
        assert reader.measured[0]["read"] == 9 and reader.held == [4], family
        assert books["momentum"]["transit"] == [9, 0, 0], family
        assert source.phase_steps == (0 if family.get("phase") is False else 1), family


def test_a_turn_of_zero_releases_nothing_and_a_turn_of_one_releases_at_quantum_times_one():
    """(c)."""
    clock = 64
    world = bar(
        [5, 1, 1],
        [{"name": "light", "kind": "paid"}],
        [
            lamp(0, 60 * clock, [1, 0, 0], [1, 4]),
            lamp(2, 4, [1, 0, 0], [1, 1], table={"light": "measure"}),
        ],
        clock,
        steps=256,
    )
    records: list[dict[str, object]] = []
    simulation = EventSimulation(parse_event_world(world), records.append)
    source, probe, light = simulation.measured[1], simulation.measured[2], simulation.transits[0]
    own = light.rank[2]
    for tick in range(1, 6):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert probe.age == tick and probe.held == [4] and probe.phase_steps == 0, tick
        assert not light.fly_amt[..., own, :].any() and not light.arr_amt[..., own, :].any(), tick
        if tick < 4:
            assert simulation.held_spent[0] == 0 and light.content() == 0 and light.current() == 0, tick
        else:
            assert simulation.held_spent[0] == 60 and light.content() == 60 and light.current() == 1, (
                tick
            )
            assert source.held == [60 * clock - 60] and source.momentum == [-60, 0, 0], tick
    assert records == []
    simulation.step()
    assert simulation.books()["balanced"]
    assert probe.events == [1] and probe.held == [clock - 1] and probe.pushed == [60, 0, 0]
    assert probe.phase_steps == 1 and probe.momentum == [59, 0, 0]
    assert (
        int(light.fly_amt[2, 0, 0, own, PLUS_X]) == 1 and int(light.fly_con[2, 0, 0, own, PLUS_X]) == 1
    )
    assert light.fly_mom[2, 0, 0, own, PLUS_X].tolist() == [1, 0, 0]
    simulation.step()
    assert simulation.books()["balanced"]
    assert probe.held == [clock - 2] and probe.phase_steps == 2 and probe.momentum == [58, 0, 0]
    assert source.age == 7 and source.phase_steps == 60 * 4 + 59 * 3
    assert simulation.held_spent[0] == 62 and simulation.held_measured[0] == 60
    assert light.content() == 2 and light.current() == 2 and light.escaped_content == 0
    assert simulation.books()["momentum"]["transit"] == [2, 0, 0]
    assert [record["event"] for record in records] == ["click"]
    assert records[0]["content"] == 60 and records[0]["amount"] == 1 and records[0]["tick"] == 6
