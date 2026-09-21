"""The width of the push (the model owner's D1, 2026-09-19, Highlights 5.4;
docs/BEAM_LAW.md, section 3, step 5 and implementation note 15): the world
key `width` S, the Q S M of the step rule's wall. One rule in isolation on
a bar; no push arrives (`release` [0, 1]). Since the directional drive of
2026-09-21 (BEAM_LAW note 49; `tests/test_directional_drive.py`) a free
measured event of content M with the momentum p on a heading steps at the
rate |p| x 64 against the wall Q S M x 64 + |p| x 110 (T_D = 110 the
heading's resolution), one Link per self-creation at most, so that one unit
of net flow, p = Q M, gives the speed 64 / (64 S + 110) for every content
(until then one Link per (Q S M + p) / p self-creations, the speed 1 / (S +
1)). The expected integers of docs/TEST_EXPECTATIONS.md ("The width of the
push"), re-pinned on 2026-09-21 with the old integers kept here as history:

Since 2026-09-19 the label of a unit along a heading is Q e_d with Q = 64
(BEAM_LAW section 2 and note 23), and every declared `momentum` is in label
units.

(a) S = 1: content 16 with momentum 1024 (16 x 64: one unit of net flow;
    rate 65536, wall 178176, the speed 0.3678) on +x from x = 4 steps at
    the self-creations of ages 3, 6, 9 (x after intervals 1 to 6: 4, 4, 5,
    5, 5, 6; `steps` 0, 0, 1, 1, 1, 2), with `width` 1 declared and with
    the key absent alike; with momentum 64 (rate 4096, wall 72576) none
    after 17 intervals and one after 18 (until 2026-09-21 the ages 2, 4, 6,
    x 4, 5, 5, 6, 6, 7, and at 64 none after 16, one after 17);
(b) S = 8 with p = Q M: content 16 with momentum 1024 (rate 65536, wall
    636928, the speed 0.10289 = 64 / 622) steps once per 9.72
    self-creations, at the ages 10, 20, 30 (x = 4 through interval 9, 5
    from 10, 6 from 20; `steps` 0, 1, 2 over 27 intervals); a content of 3
    with momentum 192 (rate 12288, wall 119424, the same speed) steps at
    the same ages (the speed a unit of flow gives, 64 / (64 S + 110), is
    the same for every content; until 2026-09-21 once per 9, at 9, 18, 27,
    x 4, 5, 6, 7 and `steps` 3 after 27);
(c) the step is counted on the body's record with the remainder kept: with
    `suspension` [1, 4] and a crowd of 4 rays of another number at rest on
    every Node it visits, the probe of (b) owes one interval after every
    self-creation (age after interval n is ceil(n / 2)); since the
    crossing rule (2026-09-21, BEAM_LAW note 48: the step before the law,
    the drive advanced at the self-creation itself) the step of the ages
    10, 20, 30 lands on the self-creation, the intervals 19, 39, 59 (x
    after intervals 17, 18, 35, 36, 53, 54, 60: 3, 3, 4, 4, 5, 5, 6; after
    19, 20, 39, 40, 59, 60: 4, 4, 5, 5, 6, 6; age 30 and waited 30 after
    60), and after every interval `steps` is the whole part of age x
    65536 / 636928, nothing carried (until 2026-09-21 the ages 9, 18, 27 at
    the intervals 17, 35, 53, x 4, 4, 5, 5, 6, 6, 6 after 17, 18, 35, 36,
    53, 54, 60 and `steps` the whole part of age x 16 / 144; with the step
    after the law and the count owed, until the crossing rule, the steps
    fell at 18, 36, 54; the first run corrected the interval of the step
    from 17 to 18: the order of the frame, not the rule);
(d) a world without `width` parses to 1; `width` 8 parses to 8 and the
    runner's record carries it; 0, -1, a string and a fraction are refused
    naming `width`.
"""

from __future__ import annotations

import json

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.engine import step_line
from event_universe.runner import run_initialization

REST = 0  # The first rest direction of the table ("here a").


def bar(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    """An open bar of 12 x 1 x 1 whose measured events release nothing."""
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "push-width-test",
        "shape": [12, 1, 1],
        "boundary": "open",
        "ticks": 8,
        "K": 1024,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "m", "quantum": 0, "charge": 0, "phase": False}],
        "measured": measured,
    }
    world.update(keys)
    return world


def mover(content: int, momentum: int, x: int = 4) -> dict[str, object]:
    return {"position": [x, 0, 0], "family": "m", "amount": content, "momentum": [momentum, 0, 0]}


def positions(world: dict[str, object], ticks: int) -> tuple[list[int], list[int]]:
    """The mover's x and its `steps` after each of `ticks` intervals, the
    books balanced at every one."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    xs, steps = [], []
    for tick in range(1, ticks + 1):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert entry.momentum == world["measured"][0]["momentum"]  # type: ignore[index]
        xs.append(entry.position[0])
        steps.append(entry.steps)
    return xs, steps


def test_width_one_is_the_rule_as_it_was():
    """(a)."""

    # The rule of one self-creation, the one place it lives for the tools
    # (`engine.step_line`): the sign of the Link stepped on the line, or
    # None, and the drive after it (the directional drive of 2026-09-21).
    def fired(momentum: int, content: int, width: int, count: int) -> list[int | None]:
        drive, deficits, line, found = 0, [0, 0, 0], (0, 0, 0), []
        for _ in range(count):
            step, drive, line = step_line(drive, deficits, line, [momentum, 0, 0], content, width)
            found.append(None if step is None else step[1])
        return found

    assert fired(1024, 16, 1, 9) == [None, None, 1, None, None, 1, None, None, 1]
    assert fired(-64, 16, 1, 18)[16] is None and fired(-64, 16, 1, 18)[17] == -1
    assert fired(1024, 16, 8, 10)[8] is None and fired(1024, 16, 8, 10)[9] == 1
    assert step_line(7, [0, 0, 0], (1, 0, 0), [0, 0, 0], 16, 1) == (None, 7, (1, 0, 0))
    expected = [4, 4, 5, 5, 5, 6]
    assert positions(bar([mover(16, 1024)]), 6) == (expected, [0, 0, 1, 1, 1, 2])
    assert positions(bar([mover(16, 1024)], width=1), 6) == (expected, [0, 0, 1, 1, 1, 2])
    xs, steps = positions(bar([mover(16, 64)]), 18)
    assert xs[16] == 4 and xs[17] == 5 and steps[16] == 0 and steps[17] == 1


def test_width_eight_steps_once_per_nine_self_creations():
    """(b)."""
    expected = [4] * 9 + [5] * 10 + [6] * 8
    xs, steps = positions(bar([mover(16, 1024)], width=8), 27)
    assert xs == expected
    assert steps == [0] * 9 + [1] * 10 + [2] * 8
    xs, steps = positions(bar([mover(3, 192)], width=8), 27)
    assert xs == expected and steps[-1] == 2
    xs, steps = positions(bar([mover(3, 192)], width=8), 30)
    assert xs[-1] == 7 and steps[-1] == 3


def test_the_step_is_counted_off_the_clock_with_no_remainder():
    """(c)."""
    anchor = {"position": [11, 0, 0], "family": "m", "amount": 1, "fixed": True}
    crowds = [
        {"position": [x, 0, 0], "family": "m", "number": 2, "direction": REST, "amount": 4, "phase": 0}
        for x in range(3, 8)
    ]
    world = bar([mover(16, 1024, x=3), anchor], width=8, suspension=[1, 4], in_transit=crowds, ticks=60)
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    entry = simulation.measured[1]
    xs = {}
    for tick in range(1, 61):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert entry.age == (tick + 1) // 2 and entry.waited == tick // 2, tick
        # The drive advances at the self-creation (the step before the law,
        # the crossing rule of 2026-09-21): the count is the whole part of
        # age x 65536 / 636928 after every interval, odd and even alike.
        assert entry.steps == entry.age * 65536 // 636928, tick
        assert entry.momentum == [1024, 0, 0]
        xs[tick] = entry.position[0]
    assert [xs[t] for t in (17, 18, 35, 36, 53, 54, 60)] == [3, 3, 4, 4, 5, 5, 6]
    assert [xs[t] for t in (19, 20, 39, 40, 59, 60)] == [4, 4, 5, 5, 6, 6]
    assert entry.age == 30 and entry.waited == 30 and entry.steps == 3


def test_the_key_parses_with_its_default_and_its_refusals(tmp_path):
    """(d)."""
    world = bar([mover(16, 1024)])
    assert parse_nature_beam_world(world).width == 1
    assert parse_nature_beam_world({**world, "width": 8}).width == 8
    for bad in (0, -1, "8", 1.5):
        with pytest.raises(ValueError, match="width must be an integer from 1"):
            parse_nature_beam_world({**world, "width": bad})
    path = tmp_path / "world.json"
    path.write_text(json.dumps({**world, "width": 8, "ticks": 2}), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert record["width"] == 8 and record["status"] == "completed"
