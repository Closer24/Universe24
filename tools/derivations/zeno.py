"""The pulsed Zeno column (ALGEBRA.md row (h3) and What is open, item 46; the paper's S.59): the formula (1 - cos^n(pi / n)) / 2 at n = 1, 2, 4, 8, 16 (S.59 (a), column A) and the excluded column B (1, 0.625, 0.154, 0.005, 0; S.59 (c)), with a reading's distance from each in binomial standard errors, the reading passed in by its caller and held nowhere here (the run is the check and never the claim; the module reads no run); and the body's own period as its window, killed by nature's n = 1 (S.59 (b')), the period the band's rest rotation at the computed pair.

Usage: `python tools/derivations/zeno.py` prints the formula column and the body's own period as its window; `python tools/derivations/zeno.py TRIALS C1 C2 C4 C8 C16` adds a reading, its counts in e at n = 1, 2, 4, 8, 16 of TRIALS trials, against the two columns.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Sequence
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # the folder's root, rule3.py, by its file
import rule3  # noqa: E402

PULSES = (1, 2, 4, 8, 16)
COLUMN_B = (
    1.0,
    0.625,
    0.154,
    0.005,
    0.0,
)  # the click alone written, nothing on a null window (S.59 (c))
MATTER_PAIR = (2, 3)  # the paper's computed pair, the body's rest rotation cos omega_b = 2 / 3
# T_pi of the pulsed gate's world, 768 ticks (ALGEBRA.md, What is open, item 46: "the drive's pi pulse lengthens
# with the Node clock Gamma at a fixed amplitude", "The world: Gamma = 96,000, ..., the pi pulse 768 ticks"; S.59 (a)
# on the paper branch gives T_pi = pi / (2 Omega_R), the full transfer from g to e)
PI_PULSE_TICKS = 768


def probability_excited(n: int) -> float:
    """(1 - cos^n(pi / n)) / 2, the share in e at T_pi after n equally spaced windows (S.59 (a))."""
    return (1 - math.cos(math.pi / n) ** n) / 2


def own_period_as_window() -> list[float]:
    """[P(e) at n = 1, the body's own period 2 pi / omega_b in intervals, P(e) with that period as the window over the pulsed gate's T_pi = 768 ticks]: 1, 7.47 and 0.023; a body reading itself at its own period would suppress every Rabi oscillation longer than it, which nature's full transfer at n = 1 shows it does not, so a bound body's period is not its window (S.59 (b')); omega_b the band's rest rotation at the vacuum's paces, cos omega_b = num / den (The band at a pace); T_pi the pulsed gate's world's (ALGEBRA.md, What is open, item 46, "the pi pulse 768 ticks"; S.59 (a), T_pi = pi / (2 Omega_R))."""
    num, den = MATTER_PAIR
    omega_b = math.acos(rule3.dispersion_at_paces((0.0, 0.0, 0.0), num, den, 1, 1, (1, 1, 1)))
    period = 2 * math.pi / omega_b
    windows = round(PI_PULSE_TICKS / period)
    return [probability_excited(1), period, probability_excited(windows)]


def formula_column() -> list[float]:
    """(1 - cos^n(pi / n)) / 2 at n = 1, 2, 4, 8, 16 (S.59 (a), column A)."""
    return [(1 - math.cos(math.pi / n) ** n) / 2 for n in PULSES]


def standard_errors(counts: Sequence[int], trials: int) -> list[float]:
    """The binomial standard error sqrt(p (1 - p) / trials) of a reading's share p = count / trials at n = 2, 4, 8, 16; `counts` the counts in e at n = 1, 2, 4, 8, 16 of `trials` trials, a run's reading passed in by the caller and held nowhere in this module."""
    return [math.sqrt(p * (1 - p) / trials) for p in (c / trials for c in counts[1:])]


def reading_against_the_formula(counts: Sequence[int], trials: int) -> list[float]:
    """A reading's deviation from the formula's column (S.59 (a)) in its own standard errors at n = 2, 4, 8, 16."""
    return [
        (c / trials - f) / s
        for c, f, s in zip(
            counts[1:], formula_column()[1:], standard_errors(counts, trials), strict=True
        )
    ]


def column_b_excluded(counts: Sequence[int], trials: int) -> list[float]:
    """Column B's distance from a reading in the reading's standard errors at n = 2, 4, 8, 16 (S.59 (c))."""
    return [
        abs(c / trials - b) / s
        for c, b, s in zip(counts[1:], COLUMN_B[1:], standard_errors(counts, trials), strict=True)
    ]


if __name__ == "__main__":
    print("formula:", [round(v, 4) for v in formula_column()])
    print("the body's own period as its window:", [round(v, 3) for v in own_period_as_window()])
    if len(sys.argv) == 2 + len(
        PULSES
    ):  # a reading passed in: the trials and the counts at n = 1, 2, 4, 8, 16
        trials, counts = int(sys.argv[1]), [int(v) for v in sys.argv[2:]]
        print("standard errors:", [round(v, 4) for v in standard_errors(counts, trials)])
        print(
            "reading against the formula:",
            [round(v, 2) for v in reading_against_the_formula(counts, trials)],
        )
        print("column B excluded by:", [round(v, 1) for v in column_b_excluded(counts, trials)])
