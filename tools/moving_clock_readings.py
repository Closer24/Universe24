"""THE MOVING CLOCK'S READINGS (ALGEBRA.md #the-rows-against-nature (e)): the runner's output files of a moving giver and of the same giver at rest, read at the detectors at rest alone; every line labelled DETECTOR, none replays the engine. Per detector the clicks' intervals in the run's order, the gaps between consecutive clicks and their mean: the arrival period at that detector. The giver's period in the GameBoard's frame is the mean of the arrival periods ahead of and behind the giver (P_v (1 - v / u) ahead and P_v (1 + v / u) behind cancel the Doppler term of the light's group velocity u to the first order), and the tick's factor is the resting period over the moving one, P_rest / P_v, printed beside the expectation the caller names. The band is the rounding's: one interval on each period, carried to the factor."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


def clicks_by_detector(output: dict[str, Any]) -> dict[str, list[int]]:
    """The click intervals per detector from the runner's output, each list in the run's order (DETECTOR)."""
    if output.get("verdict") != "LAWFUL":
        raise ValueError(
            f"{output.get('name')}: the verdict is {output.get('verdict')}, no clicks to read"
        )
    by: dict[str, list[int]] = {}
    for click in output["clicks"]:
        detector = click["detector"]
        if isinstance(detector, str):
            by.setdefault(detector, []).append(int(click["interval"]))
    return by


def arrival_period(intervals: list[int]) -> Fraction | None:
    """The mean gap between consecutive clicks at one detector, exact; None below two clicks."""
    if len(intervals) < 2:
        return None
    ordered = sorted(intervals)
    return Fraction(ordered[-1] - ordered[0], len(ordered) - 1)


def frame_period(ahead: Fraction | None, behind: Fraction | None) -> Fraction | None:
    """The giver's period in the GameBoard's frame: the mean of the arrival periods ahead and behind; None where one side has no period."""
    if ahead is None or behind is None:
        return None
    return (ahead + behind) / 2


def factor(rest: Fraction | None, moving: Fraction | None) -> Fraction | None:
    """The tick's factor P_rest / P_v; None where a period is missing or zero."""
    if rest is None or moving is None or moving == 0:
        return None
    return rest / moving


def band_of_factor(rest: Fraction, moving: Fraction) -> Fraction:
    """The rounding's band carried to the factor: one interval on each period, (P_rest + 1) / (P_v - 1) - P_rest / P_v."""
    return (rest + 1) / (moving - 1) - rest / moving if moving > 1 else Fraction(0)


def report(moving: dict[str, Any], rest: dict[str, Any], ahead: str, behind: str) -> list[str]:
    """The lines of the reading, each labelled DETECTOR: the clicks per detector in both runs, the arrival periods, the frame period and the factor with its band."""
    lines: list[str] = []
    periods: dict[str, dict[str, Fraction | None]] = {}
    for label, output in (("moving", moving), ("rest", rest)):
        by = clicks_by_detector(output)
        periods[label] = {}
        for detector in sorted(set(by) | {ahead, behind}):
            intervals = by.get(detector, [])
            period = arrival_period(intervals)
            periods[label][detector] = period
            first = intervals[0] if intervals else None
            shown = None if period is None else f"{period} = {float(period):.4f}"
            lines.append(
                f"DETECTOR {label} {detector}: clicks {len(intervals)}, first {first}, arrival period {shown}"
            )
    moving_frame = frame_period(periods["moving"][ahead], periods["moving"][behind])
    rest_frame = frame_period(periods["rest"][ahead], periods["rest"][behind])
    lines.append(f"DETECTOR frame period rest {rest_frame} moving {moving_frame}")
    found = factor(rest_frame, moving_frame)
    if found is None or rest_frame is None or moving_frame is None:
        lines.append("DETECTOR factor: none (a side without two clicks)")
    else:
        band = band_of_factor(rest_frame, moving_frame)
        lines.append(f"DETECTOR factor P_rest / P_v = {float(found):.4f} +- {float(band):.4f}")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--moving", type=Path, required=True, help="the runner's output of the moving giver"
    )
    parser.add_argument(
        "--rest", type=Path, required=True, help="the runner's output of the giver at rest"
    )
    parser.add_argument("--ahead", required=True, help="the detector ahead of the giver")
    parser.add_argument("--behind", required=True, help="the detector behind the giver")
    parser.add_argument(
        "--expected", type=float, help="the blind expectation of the factor, printed beside"
    )
    args = parser.parse_args(argv)
    moving = json.loads(args.moving.read_text(encoding="utf-8"))
    rest = json.loads(args.rest.read_text(encoding="utf-8"))
    for line in report(moving, rest, args.ahead, args.behind):
        print(line)
    if args.expected is not None:
        print(f"EXPECTED (blind, written before the run) {args.expected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
