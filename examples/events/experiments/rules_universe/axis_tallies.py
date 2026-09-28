"""The reader of worlds (a) and (b) of the rule's own universe (ALGEBRA.md THE COLOURS ARE THE THREE AXES; the Closer's assignment of 2026-09-28, 13:52 Israel): from a world and its runner output, the clicks at the pixel's detector and their tallies per axis: the net tally (the sum of the components) and the raw (the sum of the magnitudes) per axis, the net per interval at the peak interval, the net and the raw over the three axes, the first click's interval, against the expectation file's `axes` section (Cheshbon's blind numbers before the run): the net 0 on every axis reads white, the net leaning along one axis reads the pull; a reader of the clicks, no law."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any


def clicks_at(output: dict[str, Any], detector: str) -> list[dict[str, Any]]:
    """The clicks at the detector in the order of their intervals, those with a tally."""
    found = [c for c in output.get("clicks", []) if c.get("detector") == detector and c.get("tally")]
    return sorted(found, key=lambda c: int(c["interval"]))


def over_axes(values: list[int]) -> list[list[int]]:
    """The three values over the largest magnitude among them as exact rationals [numerator, denominator]; 0 : 0 : 0 where all vanish."""
    largest = max((abs(v) for v in values), default=0)
    return [
        [Fraction(v, largest).numerator, Fraction(v, largest).denominator] if largest else [0, 1]
        for v in values
    ]


def tally_rows(output: dict[str, Any], axes: dict[str, Any]) -> dict[str, Any]:
    """THE COLOURS ARE THE THREE AXES: per axis the net tally and the raw over all clicks at the detector, the net per interval at the interval where the net along the leaning axis peaks, the net and the raw over the axes, the first click's interval; MATCH when the peak's net lies within `band` of `net_per_interval` on every axis, else MISS, or the reading alone while no band is written; `white` where the net vanishes on every axis."""
    clicks = clicks_at(output, str(axes["detector"]))
    tallies = [[int(t) for t in c["tally"]] for c in clicks]
    net = [sum(t[a] for t in tallies) for a in range(3)]
    raw = [sum(abs(t[a]) for t in tallies) for a in range(3)]
    per_interval: dict[int, list[int]] = defaultdict(lambda: [0, 0, 0])
    for click, tally in zip(clicks, tallies, strict=True):
        for a in range(3):
            per_interval[int(click["interval"])][a] += tally[a]
    expected, band = axes.get("net_per_interval"), axes.get("band")
    leaning = max(range(3), key=lambda a: abs(expected[a]) if expected else 0)
    peak_interval = max(per_interval, key=lambda t: abs(per_interval[t][leaning]), default=None)
    peak = per_interval[peak_interval] if peak_interval is not None else None
    if not clicks:
        verdict = "no click at the detector"
    elif expected is None or band is None:
        verdict = "no band yet"
    else:
        within = all(abs(peak[a] - int(expected[a])) <= float(band) for a in range(3))
        verdict = "MATCH" if within else "MISS"
    return {
        "kind": "axes",
        "detector": axes["detector"],
        "clicks": len(clicks),
        "first_click": int(clicks[0]["interval"]) if clicks else None,
        "net": net,
        "raw": raw,
        "net_over_axes": over_axes(net),
        "raw_over_axes": over_axes(raw),
        "peak_interval": peak_interval,
        "net_per_interval_at_peak": peak,
        "white": bool(clicks) and all(v == 0 for v in net),
        "expected": {"net_per_interval": expected, "first_click": axes.get("first_click"), "band": band},
        "verdict": verdict,
    }


def report(world: Path, output: Path) -> dict[str, Any]:
    """The reading of one world and its output: the `axes` row where the expectation declares it, MATCH or MISS or the reading alone."""
    expectation = json.loads(world.with_suffix(".expectation.json").read_text(encoding="utf-8"))
    found = json.loads(output.read_text(encoding="utf-8"))
    rows: dict[str, Any] = {"world": world.name, "output": output.name, "verdict": found.get("verdict")}
    if "axes" in expectation:
        rows["axes"] = tally_rows(found, expectation["axes"])
    return rows


def main() -> None:
    arguments = [Path(a).resolve() for a in sys.argv[1:]]
    worlds, outputs = arguments[0::2], arguments[1::2]
    if not worlds or len(worlds) != len(outputs):
        raise SystemExit(
            "usage: axis_tallies.py <world.json> <output.json> [<world.json> <output.json> ...]"
        )
    for world, output in zip(worlds, outputs, strict=True):
        text = json.dumps(report(world, output), indent=1)
        print(text)
        output.with_suffix(".axes.json").write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
