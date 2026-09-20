"""The width of the push (the model owner's D1, 2026-09-19, Highlights 5.4;
docs/RAY_LAW.md, section 3, step 5 and implementation note 15): a free
measured event of content M with the momentum component p on an axis steps
one Link per (S x M + p) / p self-creations on that axis, `by_clock(age,
|p|, S x M + |p|)`, S the world key `width` (an integer from 1; 1 by
default, the rule as it was: one Link per (M + p) / p). One rule in
isolation on a bar; no push arrives (`release` [0, 1]). The expected
integers of docs/TEST_EXPECTATIONS.md ("The width of the push"), written
down first:

Since 2026-09-19 the label of a unit along a heading is Q e_d with Q = 64
(RAY_LAW section 2 and note 23), every declared `momentum` is in label
units, and the rule reads `by_clock(age, |p|, Q x S x M + |p|)`: the
momenta below are the first pins times 64 and every position is unchanged
(`by_clock(age, Q n, Q k) = by_clock(age, n, k)`).

(a) S = 1 reads exactly as the rule was: content 16 with momentum 1024
    (16 x 64: one unit of net flow) on +x from x = 4 steps at the
    self-creations of ages 2, 4, 6 (x after intervals 1 to 6: 4, 5, 5, 6,
    6, 7), with `width` 1 declared and with the key absent alike; with
    momentum 64 none after 16 intervals and one after 17;
(b) S = 8 with p = Q M: content 16 with momentum 1024 steps once per 9
    self-creations, at the ages 9, 18, 27 (x = 4 through interval 8, 5 from
    9, 6 from 18, 7 at 27; `steps` 0, 1, 2, 3); a content of 3 with momentum
    192 steps at the same ages (the speed a unit of flow gives, 1 / (S + 1),
    is the same for every content);
(c) the step is counted off the clock with no stored remainder: with
    `suspension` [1, 4] and a crowd of 4 rays of another number at rest on
    every Node it visits, the probe of (b) owes one interval after every
    self-creation (age after interval n is ceil(n / 2)); the step of the
    ages 9, 18, 27 lands on the interval that pays the count (a measured
    event steps only when it owes nothing, the engine's frame), the
    intervals 18, 36, 54 (x after intervals 17, 18, 35, 36, 53, 54, 60: 3,
    4, 4, 5, 5, 6, 6; age 30 and waited 30 after 60), and after every
    paying interval `steps` is the whole part of age x 1024 / 9216 (= age
    x 16 / 144), after every self-creation that of (age - 1) x 16 / 144,
    nothing carried
    (the first run corrected the interval of the step from 17 to 18: the
    order of the frame, not the rule);
(d) a world without `width` parses to 1; `width` 8 parses to 8 and the
    runner's record carries it; 0, -1, a string and a fraction are refused
    naming `width`.
"""

from __future__ import annotations

import json

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.engine import step_axis
from event_universe.runner import run_initialization

REST = 0  # The first rest direction of the table ("here a").


def bar(measured: list[dict[str, object]], **keys: object) -> dict[str, object]:
    """An open bar of 12 x 1 x 1 whose measured events release nothing."""
    world: dict[str, object] = {
        "law": "rays",
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
    # The rule of one axis, the one place it lives (`engine.step_axis`):
    # the sign of the Link stepped at this age, or None.
    assert [step_axis(age, 1024, 16, 1) for age in range(1, 7)] == [None, 1, None, 1, None, 1]
    assert step_axis(16, -64, 16, 1) is None and step_axis(17, -64, 16, 1) == -1
    assert step_axis(9, 1024, 16, 8) == 1 and step_axis(5, 0, 16, 1) is None
    expected = [4, 5, 5, 6, 6, 7]
    assert positions(bar([mover(16, 1024)]), 6) == (expected, [0, 1, 1, 2, 2, 3])
    assert positions(bar([mover(16, 1024)], width=1), 6) == (expected, [0, 1, 1, 2, 2, 3])
    xs, steps = positions(bar([mover(16, 64)]), 17)
    assert xs[15] == 4 and xs[16] == 5 and steps[15] == 0 and steps[16] == 1


def test_width_eight_steps_once_per_nine_self_creations():
    """(b)."""
    expected = [4] * 8 + [5] * 9 + [6] * 9 + [7]
    xs, steps = positions(bar([mover(16, 1024)], width=8), 27)
    assert xs == expected
    assert steps == [0] * 8 + [1] * 9 + [2] * 9 + [3]
    xs, steps = positions(bar([mover(3, 192)], width=8), 27)
    assert xs == expected and steps[-1] == 3


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
        counted = entry.age if tick % 2 == 0 else entry.age - 1
        assert entry.steps == counted * 1024 // 9216 == counted * 16 // 144, tick
        assert entry.momentum == [1024, 0, 0]
        xs[tick] = entry.position[0]
    assert [xs[t] for t in (17, 18, 35, 36, 53, 54, 60)] == [3, 4, 4, 5, 5, 6, 6]
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
