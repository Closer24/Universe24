"""The well's clocks, GameBoard readings beside the bending (ALGEBRA.md #the-rows-against-nature (a) and (b); docs/ENGINE.md, the readings): from one run's output, (1) the light's wavelength along the beam's axis inside the well and outside it, read from the family's `rows` reading (the level along the axis, the mean distance between its sign changes, doubled; a record's rotation per interval is its giver's everywhere, so the well shows in the wave number), (2) the light's period at two Nodes from their `level` readings every interval (the mean interval between sign changes, doubled; the check that the rotation is conserved), and (3) the matter clocks' mean cycle from their `cycle` readings (the distance between the first and the last cycle start over the cycles between); every number an exact fraction and a diagnostic labelled GAMEBOARD, never compared with nature. The readings' names and the windows along the axis come from the expectation file's `WELL` section beside the world. Run from the repository root: python tools/well_clocks.py <world.json> <world.output.json>; the report is printed and written beside the output as <name>.well.json."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


def mean_between_sign_changes(values: list[int]) -> Fraction | None:
    """Twice the mean distance between consecutive sign changes of the sequence (a wavelength or a period), None below two changes; a zero keeps the sign before it."""
    changes: list[int] = []
    sign = 0
    for index, value in enumerate(values):
        here = (value > 0) - (value < 0)
        if here and sign and here != sign:
            changes.append(index)
        if here:
            sign = here
    if len(changes) < 2:
        return None
    return 2 * Fraction(changes[-1] - changes[0], len(changes) - 1)


def lines_of(output: dict[str, Any], name: str) -> list[dict[str, Any]]:
    """The lines of the named reading of the output; refused by name where the output lacks it."""
    for reading in output.get("readings", []):
        if reading["name"] == name:
            return list(reading["lines"])
    raise ValueError(f"the output has no reading named {name!r}")


def wavelengths(
    output: dict[str, Any], shape: list[int], rows: str, axis_y: int, windows: list[list[int]]
) -> list[dict[str, Any]]:
    """Per `rows` line and per window [x0, x1] along the axis y, the wavelength from the level's sign changes there; only the lines whose window holds one."""
    found: list[dict[str, Any]] = []
    for line in lines_of(output, rows):
        level = line["rows"]
        if not level:
            continue
        for x0, x1 in windows:
            along = [int(level[(x * int(shape[1]) + axis_y) * int(shape[2])]) for x in range(x0, x1 + 1)]
            wavelength = mean_between_sign_changes(along)
            if wavelength is not None:
                found.append(
                    {
                        "interval": int(line["interval"]),
                        "window": [x0, x1],
                        "wavelength": [wavelength.numerator, wavelength.denominator],
                    }
                )
    return found


def period_at(output: dict[str, Any], name: str) -> Fraction | None:
    """The light's period at a Node from its `level` reading every interval: twice the mean interval between sign changes."""
    return mean_between_sign_changes([int(line["level"]) for line in lines_of(output, name)])


def mean_cycle(output: dict[str, Any], name: str) -> Fraction | None:
    """A body's mean cycle from its `cycle` reading: the distance from the first cycle start to the last over the cycles between; None below two cycles."""
    starts = sorted(
        {int(line["cycle_start"]) for line in lines_of(output, name) if int(line["cycle_length"]) > 0}
    )
    if len(starts) < 2:
        return None
    return Fraction(starts[-1] - starts[0], len(starts) - 1)


def pair(value: Fraction | None) -> list[int] | None:
    return None if value is None else [value.numerator, value.denominator]


def report(world_path: Path, output_path: Path) -> dict[str, Any]:
    """The report: the wavelengths per window, the periods at the two Nodes with their ratio, the clocks' mean cycles with their ratio, and the light's relative shift of wave number over the clock's relative shift of cycle (the pace line's reading); every number GAMEBOARD."""
    world = json.loads(world_path.read_text(encoding="utf-8"))
    output = json.loads(output_path.read_text(encoding="utf-8"))
    well = json.loads(world_path.with_suffix(".expectation.json").read_text(encoding="utf-8"))["WELL"]
    periods = [period_at(output, name) for name in well["levels"]]
    cycles = [mean_cycle(output, name) for name in well["clocks"]]
    found = wavelengths(output, world["shape"], well["rows"], int(well["axis_y"]), well["windows"])
    light = mean_wavelength_shift(found, well["windows"])
    clock = cycles[0] / cycles[1] - 1 if cycles[0] and cycles[1] else None
    return {
        "input": world_path.stem,
        "kind": "GAMEBOARD",
        "wavelengths": found,
        "light_periods": [pair(p) for p in periods],
        "light_period_ratio": pair(periods[0] / periods[1] if periods[0] and periods[1] else None),
        "clock_cycles": [pair(c) for c in cycles],
        "clock_ratio": pair(cycles[0] / cycles[1] if cycles[0] and cycles[1] else None),
        "light_wave_number_shift": pair(light),
        "clock_cycle_shift": pair(clock),
        "shift_ratio": pair(light / clock if light is not None and clock else None),
    }


def mean_wavelength_shift(found: list[dict[str, Any]], windows: list[list[int]]) -> Fraction | None:
    """The light's relative shift of wave number in the well: the mean wavelength outside (the second window) over the mean inside (the first) minus one, k = 2 pi / lambda; None where a window read none."""
    means = []
    for window in windows[:2]:
        read = [Fraction(*w["wavelength"]) for w in found if w["window"] == list(window)]
        means.append(sum(read) / len(read) if read else None)
    return means[1] / means[0] - 1 if means[0] and means[1] else None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.splitlines()[-1])
        return 2
    world_path, output_path = Path(argv[0]), Path(argv[1])
    text = json.dumps(report(world_path, output_path), indent=1)
    print(text)
    output_path.with_name(f"{world_path.stem}.well.json").write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
