"""THE GENERATOR BY THE RULE, tools/body_generator.py (ALGEBRA.md 9.118; the Boss's record
2233): the period by the one-Node rule equals the shipped emitters' periods and the nearest
integer to 2 pi / omega on random clocks; the vacuum profile is today's iteration bit for
bit; the run's rule reading on the emitter's unit world shows the content's share (a
finding, 9.118 item 3); the refusals by name."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import pytest

from tests.test_emitter import emitter_world
from tools.body_generator import check_world, period_by_the_rule, run_rule_reading, vacuum_profile

ROOT = Path(__file__).resolve().parents[1]


def test_the_period_is_the_nearest_integer_to_two_pi_over_omega_with_no_pi():
    """On the shipped emitters' clocks and on a sweep of clocks a / b, the first return
    within half a step after half a turn is round(2 pi / acos(a / 2 b)) (the test may use
    pi; the tool never does); the shipped light clock's 9 and the point chain's 35."""
    assert period_by_the_rule(1651150, 1048576) == 9  # the light clock's clock
    assert period_by_the_rule(2076636, 1048576) == 45  # the dark body's second emitter: the file says 46
    b = 1 << 20
    for a in range(-2 * b + 1, 2 * b, 20_101):
        omega = math.acos(a / (2 * b))
        expected = round(2 * math.pi / omega)
        assert period_by_the_rule(a, b) == expected, (a, b)
    assert period_by_the_rule(0, 1) == 4 and period_by_the_rule(1, 1) == 6  # a quarter turn; a sixth


def test_the_refusals_by_name():
    with pytest.raises(ValueError, match=r"the clock \[2, 1\] is no rotation"):
        period_by_the_rule(2, 1)
    with pytest.raises(ValueError, match=r"the clock \[1, 0\] is no rotation"):
        period_by_the_rule(1, 0)


def test_the_vacuum_profile_is_todays_iteration_and_the_runs_rule_moves_the_mode_by_the_content():
    """On the emitter's unit world the tool's vacuum profile is the file's seed bit for bit
    with its clock; the run's rule (the pace Gamma - c at the body's Nodes, its content 2 at
    Gamma = 10^4) shifts the mode's 2 cos omega by about one unit of b; on the shipped light
    clock (the content 65) it shifts it by thousands of units and the file's profile passes
    the vacuum's residual but not the run's (9.118 item 3, the finding)."""
    document = emitter_world(stock=1, ticks=2)
    entry = document["measured"][0]
    flat, clock, iterations = vacuum_profile(document, 0, int(max(abs(v) for v in entry["seed"])))
    assert flat == entry["seed"] and list(clock) == list(entry["clock"]) and iterations >= 1
    reading = run_rule_reading(document, 0)
    assert reading.content_at_body == 2
    assert Fraction(1, 4) < reading.shift_in_units_of_b < 4
    assert (
        reading.worst_residual_ratio_vacuum < 2 and reading.worst_residual_ratio_run < 2
    )  # a light body
    # the shipped light clock, its content 65 at Gamma = 10^4: the run's rule shifts the mode's
    # 2 cos omega by thousands of units of b and the file's profile fails the run's residual
    light_clock = json.loads(
        (ROOT / "examples" / "events" / "massive_record" / "light_clock.json").read_text()
    )
    shipped = run_rule_reading(light_clock, 0)
    assert shipped.content_at_body == 65 and shipped.clock == (1651150, 1048576)
    assert 3000 < shipped.shift_in_units_of_b < 5000
    assert shipped.worst_residual_ratio_vacuum < 2 < shipped.worst_residual_ratio_run


def test_check_world_names_the_period_that_differs():
    """The shipped dark body's bright world: its second emitter's period 46 is not the nearest
    integer to 2 pi / omega of its own clock, 45 (the generator's float omega_b against the
    file's clock); the line names it."""
    lines = check_world(ROOT / "examples" / "events" / "dark_body" / "bright.json")
    assert any("measured[1]" in line and "45; the file's 46 (DIFFERS)" in line for line in lines)
    assert any("measured[0]" in line and "8; the file's 8 (the same)" in line for line in lines)
    assert (
        json.loads((ROOT / "examples" / "events" / "dark_body" / "bright.json").read_text())["measured"][
            1
        ]["emitter"]["period"]
        == 46
    )
