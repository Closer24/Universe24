"""The clock reading of series T and X from the detector's click lines alone.

The register's tools (`examples/events/shell_clock/read_runs.py`, series
T's reading): per window, 1 + z is the inverse slope of the birth ordinal
against the click's tick, the least-squares slope taken exactly on the
integers (a reduced pair); k = z. Nothing else of the record is opened.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from common import events, ordinal

DETECTOR_NUMBER = 1


def clicks(folder: Path) -> list[tuple[int, int, int]]:
    """(tick, birth ordinal, age) of the detector's clicks, in tick order."""
    found = []
    for line in events(folder, {"click"}):
        if line.get("measured") == DETECTOR_NUMBER and "record" in line:
            found.append((int(line["tick"]), ordinal(int(line["record"])), int(line["age"])))
    return sorted(found)


def slope(points: list[tuple[int, int]]) -> Fraction:
    """The least-squares slope of y against x on integer points, exact."""
    n = len(points)
    sx = sum(x for x, _ in points)
    sy = sum(y for _, y in points)
    sxx = sum(x * x for x, _ in points)
    sxy = sum(x * y for x, y in points)
    return Fraction(n * sxy - sx * sy, n * sxx - sx * sx)


def one_plus_z(found, window: tuple[int, int]) -> tuple[Fraction, int]:
    lo, hi = window
    selected = [(t, o) for t, o, _ in found if lo <= t < hi]
    return 1 / slope(selected), len(selected)
