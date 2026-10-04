"""The pulsed Zeno column (ALGEBRA.md row (h3); the paper's S.59): the formula (1 - cos^n(pi / n)) / 2 at n = 1, 2, 4, 8, 16, and the folder's latest reading (120, 61, 44, 28, 16 of 120) against it in binomial standard errors, with the excluded column B (1, 0.625, 0.154, 0.005, 0); and the body's own period as its window, killed by nature's n = 1 (S.59 (b')), the period the band's rest rotation at the computed pair.

Usage: `python tools/derivations/zeno.py` prints them.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # the folder's root, rule3.py, by its file
import rule3  # noqa: E402

PULSES = (1, 2, 4, 8, 16)
READING = (120, 61, 44, 28, 16)
TRIALS = 120
COLUMN_B = (1.0, 0.625, 0.154, 0.005, 0.0)
MATTER_PAIR = (2, 3)  # the paper's computed pair, the body's rest rotation cos omega_b = 2 / 3
PI_PULSE_TICKS = 768  # T_pi of the pulsed gate's design (S.59, "T_pi = 768 ticks")


def probability_excited(n: int) -> float:
    """(1 - cos^n(pi / n)) / 2, the share in e at T_pi after n equally spaced windows (S.59 (a))."""
    return (1 - math.cos(math.pi / n) ** n) / 2


def own_period_as_window() -> list[float]:
    """[P(e) at n = 1, the body's own period 2 pi / omega_b in intervals, P(e) with that period as the window over T_pi = 768]: 1, 7.47 and 0.023; a body reading itself at its own period would suppress every Rabi oscillation longer than it, which nature's full transfer at n = 1 shows it does not, so a bound body's period is not its window (S.59 (b')); omega_b the band's rest rotation at the vacuum's paces, cos omega_b = num / den (The band at a pace)."""
    num, den = MATTER_PAIR
    omega_b = math.acos(rule3.dispersion_at_paces((0.0, 0.0, 0.0), num, den, 1, 1, (1, 1, 1)))
    period = 2 * math.pi / omega_b
    windows = round(PI_PULSE_TICKS / period)
    return [probability_excited(1), period, probability_excited(windows)]


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
    print("the body's own period as its window:", [round(v, 3) for v in own_period_as_window()])
