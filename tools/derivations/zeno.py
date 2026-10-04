"""The pulsed Zeno column (ALGEBRA.md row (h3); the paper's S.59): the formula (1 - cos^n(pi / n)) / 2 at n = 1, 2, 4, 8, 16, and the folder's latest reading (120, 61, 44, 28, 16 of 120) against it in binomial standard errors, with the excluded column B (1, 0.625, 0.154, 0.005, 0).

Usage: `python tools/derivations/zeno.py` prints them.
"""

from __future__ import annotations

import math

PULSES = (1, 2, 4, 8, 16)
READING = (120, 61, 44, 28, 16)
TRIALS = 120
COLUMN_B = (1.0, 0.625, 0.154, 0.005, 0.0)


def formula_column() -> list[float]:
    """(1 - cos^n(pi / n)) / 2 at n = 1, 2, 4, 8, 16."""
    return [(1 - math.cos(math.pi / n) ** n) / 2 for n in PULSES]


def standard_errors() -> list[float]:
    """The binomial standard error sqrt(p (1 - p) / 120) of the reading at n = 2, 4, 8, 16."""
    return [math.sqrt(p * (1 - p) / TRIALS) for p in (c / TRIALS for c in READING[1:])]


def reading_against_the_formula() -> list[float]:
    """The reading's deviation from the formula in standard errors at n = 2, 4, 8, 16."""
    return [
        (c / TRIALS - f) / s
        for c, f, s in zip(READING[1:], formula_column()[1:], standard_errors(), strict=True)
    ]


def column_b_excluded() -> list[float]:
    """Column B's distance from the reading in standard errors at n = 2, 4, 8, 16."""
    return [
        abs(c / TRIALS - b) / s
        for c, b, s in zip(READING[1:], COLUMN_B[1:], standard_errors(), strict=True)
    ]


if __name__ == "__main__":
    print("formula:", [round(v, 4) for v in formula_column()])
    print("standard errors:", [round(v, 4) for v in standard_errors()])
    print("reading against the formula:", [round(v, 2) for v in reading_against_the_formula()])
    print("column B excluded by:", [round(v, 1) for v in column_b_excluded()])
