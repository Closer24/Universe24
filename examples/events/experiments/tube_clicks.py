"""The reader of THE RULE'S OWN UNIVERSE's first looks (a) and (b) (ALGEBRA.md THE THREE COLOURS ARE THREE INTERVAL STATES, THE THIRD; the owner's word of 13:01 Israel, 2026-09-28): from a world and its runner output, (a) the white pixel's three consecutive levels at its Node summing to 0 at every interval and its quantum a_now^2 - a_next a_before constant (a GameBoard reading of the `level` lines), and (b) the tube's clicks at the pulled third: their intervals, the spacing between consecutive clicks (the tension, the third's count per Node), the tally's sense along the tube's axis, against the expectation file's `white` and `tube` sections (Cheshbon's blind number before the run); a reader of the clicks, no law."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


def level_lines(output: dict[str, Any], node: list[int]) -> list[tuple[int, int]]:
    """The `level` reading at the Node, (interval, level) in order; empty where none was declared."""
    for line in output.get("readings", []):
        if line.get("kind") == "level" and list(line.get("node", [])) == list(node):
            return sorted((int(e["interval"]), int(e["level"])) for e in line["lines"])
    return []


def white_rows(output: dict[str, Any], white: dict[str, Any]) -> dict[str, Any]:
    """(a) THE THREE COLOURS ARE THREE INTERVAL STATES: over consecutive readings at the body's Node the sum a_before + a_now + a_next at every interval (0 exactly where the band is exact), its amplitude over the level's amplitude as an exact rational and as a decimal (`sum_ratio`, Cheshbon's blind number), the rotation's period in intervals from the level's sign changes, and the quantum a_now^2 - a_next a_before least and largest; MATCH when the ratio lies within `band` of the expected one, else MISS, or the reading alone while no band is written."""
    levels = level_lines(output, list(white["node"]))
    values = [v for _, v in levels]
    sums = [b + n + a for b, n, a in zip(values, values[1:], values[2:], strict=False)]
    quanta = [n * n - a * b for b, n, a in zip(values, values[1:], values[2:], strict=False)]
    amplitude, sum_amplitude = (
        max((abs(v) for v in values), default=0),
        max((abs(s) for s in sums), default=0),
    )
    ratio = Fraction(sum_amplitude, amplitude) if amplitude else None
    crossings = [
        t for (t, x), (_, y) in zip(levels, levels[1:], strict=False) if (x < 0 <= y) or (y < 0 <= x)
    ]
    period = 2 * (crossings[-1] - crossings[0]) / (len(crossings) - 1) if len(crossings) > 1 else None
    expected, band = white.get("sum_ratio"), white.get("band")
    if not levels:
        verdict = "no level reading at the Node"
    elif expected is None or band is None or ratio is None:
        verdict = "no band yet"
    else:
        verdict = "MATCH" if abs(float(ratio) - float(expected)) <= float(band) else "MISS"
    return {
        "kind": "white",
        "node": list(white["node"]),
        "intervals": len(sums),
        "sums_nonzero": sum(1 for s in sums if s != 0),
        "sum_ratio": None if ratio is None else [ratio.numerator, ratio.denominator],
        "sum_ratio_decimal": None if ratio is None else round(float(ratio), 6),
        "period": None if period is None else round(period, 4),
        "quantum": [min(quanta), max(quanta)] if quanta else None,
        "expected": {"sum_ratio": expected, "period": white.get("period"), "band": band},
        "verdict": verdict,
    }


def tube_rows(output: dict[str, Any], tube: dict[str, Any]) -> dict[str, Any]:
    """(b) the clicks at the third's detector in order: their intervals, the spacings between consecutive clicks, the mean spacing as an exact rational [numerator, denominator], the tally's sense along the tube's axis (how many point forward, backward, none); against the expectation's `tension` within `band` when it is written, else the reading alone."""
    axis = int(tube["axis"])
    clicks = sorted(
        (c for c in output.get("clicks", []) if c.get("detector") == tube["detector"]),
        key=lambda c: int(c["interval"]),
    )
    intervals = [int(c["interval"]) for c in clicks]
    spacings = [b - a for a, b in zip(intervals, intervals[1:], strict=False)]
    mean = Fraction(sum(spacings), len(spacings)) if spacings else None
    senses = [int(c["tally"][axis]) for c in clicks if c.get("tally") is not None]
    tension, band = tube.get("tension"), tube.get("band")
    if tension is None or band is None:
        verdict = "no blind number yet"
    elif mean is None:
        verdict = "MISS"
    else:
        verdict = "MATCH" if abs(mean - Fraction(int(tension))) <= int(band) else "MISS"
    return {
        "kind": "tube",
        "detector": tube["detector"],
        "clicks": len(clicks),
        "intervals": intervals,
        "spacings": spacings,
        "mean_spacing": None if mean is None else [mean.numerator, mean.denominator],
        "sense_along_axis": {
            "forward": sum(1 for s in senses if s > 0),
            "backward": sum(1 for s in senses if s < 0),
            "none": sum(1 for s in senses if s == 0),
        },
        "tension": tension,
        "band": band,
        "verdict": verdict,
    }


def report(world: Path, output: Path) -> dict[str, Any]:
    """The reading of one world and its output: the `white` row where the expectation declares it, the `tube` row where it does, each MATCH or MISS or the reading alone."""
    expectation = json.loads(world.with_suffix(".expectation.json").read_text(encoding="utf-8"))
    found = json.loads(output.read_text(encoding="utf-8"))
    rows: dict[str, Any] = {"world": world.name, "output": output.name, "verdict": found.get("verdict")}
    if "white" in expectation:
        rows["white"] = white_rows(found, expectation["white"])
    if "tube" in expectation:
        rows["tube"] = tube_rows(found, expectation["tube"])
    return rows


def main() -> None:
    arguments = [Path(a).resolve() for a in sys.argv[1:]]
    worlds, outputs = arguments[0::2], arguments[1::2]
    if not worlds or len(worlds) != len(outputs):
        raise SystemExit(
            "usage: tube_clicks.py <world.json> <output.json> [<world.json> <output.json> ...]"
        )
    for world, output in zip(worlds, outputs, strict=True):
        text = json.dumps(report(world, output), indent=1)
        print(text)
        output.with_suffix(".tube.json").write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
