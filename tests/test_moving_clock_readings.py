"""The moving clock's readings tool on a tiny synthetic output: the arrival periods, the frame period and the factor from the clicks alone (ALGEBRA.md #the-rows-against-nature (e))."""

from __future__ import annotations

from fractions import Fraction

from tools.moving_clock_readings import arrival_period, band_of_factor, factor, frame_period, report


def output(name: str, clicks: dict[str, list[int]]) -> dict[str, object]:
    return {
        "name": name,
        "verdict": "LAWFUL",
        "clicks": [{"detector": d, "interval": t} for d, ts in clicks.items() for t in ts],
    }


def test_frame_period_cancels_the_doppler_term_and_the_factor_is_rest_over_moving() -> None:
    # a giver of period 10 at rest: both sides read gaps of 10; moving, ahead 6 and behind 14: the mean 10
    rest = output("rest", {"ahead": [5, 15, 25], "behind": [7, 17, 27]})
    moving = output("moving", {"ahead": [3, 9, 15, 21], "behind": [4, 18, 32]})
    assert arrival_period([3, 9, 15, 21]) == Fraction(6)
    assert arrival_period([4]) is None
    assert frame_period(Fraction(6), Fraction(14)) == Fraction(10)
    assert factor(Fraction(10), Fraction(12)) == Fraction(5, 6)
    assert band_of_factor(Fraction(10), Fraction(12)) == Fraction(11, 11) - Fraction(10, 12)
    lines = report(moving, rest, "ahead", "behind")
    assert all(line.startswith("DETECTOR") for line in lines)
    assert lines[-1].startswith("DETECTOR factor P_rest / P_v = 1.0000")


def test_a_side_without_two_clicks_gives_no_factor() -> None:
    rest = output("rest", {"ahead": [5, 15], "behind": [7, 17]})
    moving = output("moving", {"ahead": [3], "behind": [4, 18]})
    assert (
        report(moving, rest, "ahead", "behind")[-1]
        == "DETECTOR factor: none (a side without two clicks)"
    )
