"""The reader of WORLD (c) OF THE RULE'S OWN UNIVERSE, the fall as the clicks' bias (ALGEBRA.md THE UNIVERSE IS BOUND; Cheshbon's blind numbers of 13:09 Israel, 2026-09-28): from a world and its runner output, the tail's ratio (the largest matter level on the well's side of the body over the largest on the far side, a GameBoard reading of the `level` lines) and the moves' bias (the body's centre along the axis from the `centre` lines: the moves toward the well over all moves, the count's line's clicks as the centre shows them), against the expectation file's `fall` section within its band; a reader of the readings, no law."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


def lines_of(output: dict[str, Any], kind: str, **target: Any) -> list[dict[str, Any]]:
    """The lines of the reading of the kind whose target matches (a node or a body), in the interval's order; empty where none was declared."""
    for line in output.get("readings", []):
        if line.get("kind") == kind and all(line.get(k) == v for k, v in target.items()):
            return sorted(line["lines"], key=lambda e: int(e["interval"]))
    return []


def fall_rows(output: dict[str, Any], fall: dict[str, Any]) -> dict[str, Any]:
    """The tail's ratio and the moves' bias of one run against the `fall` section: the ratio as an exact rational and a decimal, the moves toward the well, away and all, the bias as a rational and a decimal, the centre's drift along the axis over the run; MATCH when both readings lie within `band` of Cheshbon's numbers, MISS else, or the reading alone while no band is written."""
    axis = int(fall["axis"])
    well = [abs(int(e["level"])) for e in lines_of(output, "level", node=list(fall["well_side"]))]
    far = [abs(int(e["level"])) for e in lines_of(output, "level", node=list(fall["far_side"]))]
    ratio = Fraction(max(well), max(far)) if well and far and max(far) else None
    centres = [int(e["node"][axis]) for e in lines_of(output, "centre", body=0)]
    toward_well = int(fall["well_side"][axis]) > int(fall["body"][axis])
    steps = [b - a for a, b in zip(centres, centres[1:], strict=False) if b != a]
    toward = sum(1 for s in steps if (s > 0) == toward_well)
    bias = Fraction(toward, len(steps)) if steps else None
    expected_ratio, expected_bias, band = fall.get("tail_ratio"), fall.get("bias"), fall.get("band")
    if ratio is None or bias is None:
        verdict = "no reading" if not (well and far and centres) else "no move of the centre"
    elif expected_ratio is None or expected_bias is None or band is None:
        verdict = "no band yet"
    else:
        near = abs(float(ratio) - float(expected_ratio)) <= float(band)
        near = near and abs(float(bias) - float(expected_bias)) <= float(band)
        verdict = "MATCH" if near else "MISS"
    return {
        "kind": "fall",
        "tail_ratio": None if ratio is None else [ratio.numerator, ratio.denominator],
        "tail_ratio_decimal": None if ratio is None else round(float(ratio), 4),
        "moves": {"toward_well": toward, "away": len(steps) - toward, "all": len(steps)},
        "bias": None if bias is None else [bias.numerator, bias.denominator],
        "bias_decimal": None if bias is None else round(float(bias), 4),
        "drift_along_axis": (centres[-1] - centres[0]) if centres else None,
        "expected": {"tail_ratio": expected_ratio, "bias": expected_bias, "band": band},
        "verdict": verdict,
    }


def report(world: Path, output: Path) -> dict[str, Any]:
    """The reading of one world and its output: the `fall` row where the expectation declares it."""
    expectation = json.loads(world.with_suffix(".expectation.json").read_text(encoding="utf-8"))
    found = json.loads(output.read_text(encoding="utf-8"))
    rows: dict[str, Any] = {"world": world.name, "output": output.name, "verdict": found.get("verdict")}
    if "fall" in expectation:
        rows["fall"] = fall_rows(found, expectation["fall"])
    return rows


def main() -> None:
    arguments = [Path(a).resolve() for a in sys.argv[1:]]
    worlds, outputs = arguments[0::2], arguments[1::2]
    if not worlds or len(worlds) != len(outputs):
        raise SystemExit(
            "usage: fall_bias.py <world.json> <output.json> [<world.json> <output.json> ...]"
        )
    for world, output in zip(worlds, outputs, strict=True):
        text = json.dumps(report(world, output), indent=1)
        print(text)
        output.with_suffix(".fall.json").write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
