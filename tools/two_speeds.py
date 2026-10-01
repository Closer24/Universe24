"""The two speeds' reading (ALGEBRA.md, Nature's numbers enter the board only as clicks, the series' line 1): light at the vacuum content, light at no vacuum content and the massless row's kick, each in its own world of one design (examples/events/two_speeds), read at the far region by the field line of the packet's family (a GameBoard reading labelled so: the count over the region for light, the squared deviation from the rest for the kick), one reading per interval where it changed. Per world: the readings' largest value and its interval (the peak), the half-maximum onset (the first interval at or above half the largest, the crossing placed by the line between the two readings around it), the bump's end (the last interval at or above the half) and its centroid (the readings' mean interval weighted by the reading, over the bump from the onset to the end, the packet's centre crossing the region's centre; the crests' passage averages out over the bump where the peak does not), the total of light's clicks at the region (the measurement, counted beside) and the largest reading of every other family at the region (the light's own wells, a diagnostic of the look's universe file). Then every difference the expectation names (`differences`: a name and the two worlds, the second's arrival taken from the first's), at the onsets and at the centroids (the peaks beside, the crests' passage moving them), beside the blind numbers. No number of the look stands here: the worlds, the region and the families come from the expectation file.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/two_speeds.py --expectation examples/events/two_speeds/expectation.json --outputs <light>.output.json <light_0>.output.json <kick>.output.json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

Series = list[tuple[int, int]]  # (interval, reading), one per field line


def series(output: dict[str, Any], family: str, region: str) -> Series:
    """The field line's readings of one family at one region, in the order written."""
    return [
        (int(line["tick"]), int(line["reading"]))
        for line in output["lines"]
        if line["event"] == "field" and line["family"] == family and line["detector"] == region
    ]


def onset(readings: Series) -> Fraction | None:
    """The half-maximum onset: the interval at which the reading first reaches half its largest value over the run, placed by the line between the reading before and the one at the crossing (the reading holds between two lines); None where nothing was read."""
    if not readings:
        return None
    largest = max(reading for _at, reading in readings)
    half = Fraction(largest, 2)
    for index, (at, reading) in enumerate(readings):
        if reading >= half and reading > 0:
            if index == 0:
                return Fraction(at)
            before_at, before = readings[index - 1]
            if reading == before:
                return Fraction(at)
            return before_at + (at - before_at) * (half - before) / (reading - before)
    return None


def centroid(readings: Series) -> tuple[Fraction, int] | None:
    """The bump's centroid and its end: over the readings from the first at or above half the largest to the last such reading, the mean interval weighted by the reading (each reading holding until the next line); None where nothing was read."""
    if not readings:
        return None
    largest = max(reading for _at, reading in readings)
    above = [index for index, (_at, reading) in enumerate(readings) if 2 * reading >= largest]
    bump = readings[above[0] : above[-1] + 1]
    weight = total = Fraction(0)
    for index, (at, reading) in enumerate(bump):
        held = (bump[index + 1][0] - at) if index + 1 < len(bump) else 1
        weight += Fraction(reading * held)
        total += Fraction(reading * held) * Fraction(2 * at + held - 1, 2)
    return (total / weight if weight else Fraction(bump[-1][0]), bump[-1][0])


def arrival(output: dict[str, Any], family: str, region: str) -> dict[str, Any]:
    """One world's arrival at the region: the packet family's onset, centroid, end and peak, and the other families' largest readings."""
    readings = series(output, family, region)
    peak = max(readings, key=lambda pair: pair[1]) if readings else None
    middle = centroid(readings)
    others = sorted({line["family"] for line in output["lines"] if line["event"] == "field"} - {family})
    return {
        "input": output.get("input"),
        "verdict": output.get("verdict"),
        "intervals": output.get("ticks"),
        "ended": output.get("ended"),
        "family": family,
        "readings": len(readings),
        "largest": peak[1] if peak else None,
        "peak": peak[0] if peak else None,
        "onset": onset(readings),
        "centroid": middle[0] if middle else None,
        "end": middle[1] if middle else None,
        "others": {
            other: max((reading for _at, reading in series(output, other, region)), default=0)
            for other in others
        },
    }


def reading(expectation: dict[str, Any], outputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """The look's reading: each world's arrival by the expectation's families and region, and every named difference (the second world's arrival taken from the first's) at the onsets, the centroids and the peaks, beside the blind numbers."""
    region = str(expectation["region"])
    found = {
        name: arrival(outputs[name], str(family), region)
        for name, family in expectation["families"].items()
        if name in outputs
    }
    differences: dict[str, Any] = {}
    for key, blind in expectation["differences"].items():
        first, second = (found.get(name) for name in blind["worlds"])
        if first is None or second is None:
            continue
        lead: dict[str, Any] = {"worlds": blind["worlds"]}
        for word, at in (("onsets", "onset"), ("centroids", "centroid"), ("peaks", "peak")):
            one, other = first[at], second[at]
            lead[word] = None if one is None or other is None else Fraction(one) - Fraction(other)
        lead["blind"] = {word: blind[word] for word in ("onsets", "centroids", "long_wavelength")}
        differences[key] = lead
    return {"arrivals": found, "differences": differences}


def plain(value: Any) -> Any:
    """The reading with every fraction written as a number for the file."""
    if isinstance(value, Fraction):
        return float(value)
    if isinstance(value, dict):
        return {key: plain(inner) for key, inner in value.items()}
    if isinstance(value, list):
        return [plain(inner) for inner in value]
    return value


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    parser.add_argument(
        "--outputs", type=Path, nargs="+", required=True, help="the worlds' output files"
    )
    args = parser.parse_args(argv)
    expectation = json.loads(args.expectation.read_text(encoding="utf-8"))
    outputs = {}
    for path in args.outputs:
        output = json.loads(path.read_text(encoding="utf-8"))
        name = Path(str(output["input"])).stem
        outputs[name] = output
    print(json.dumps(plain(reading(expectation, outputs)), indent=1))


if __name__ == "__main__":
    main()
