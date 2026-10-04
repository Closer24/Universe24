"""The two slits' blind from the declared file's geometry (ALGEBRA.md, The rows against nature, (g); the paper's Section 9.2, S.23): the far-field spacing lambda L / d = 16 Links, the near-field minima at the rows 15.3 and 32.7 in the regions 3 and 8 of the twelve four-row blocks, the pattern's centre 24 against the blocks' 23.5, the Huygens sum's regional dips, and the opaque NodeReader in one gap that loses the fringes and reads one gap's envelope.

The wavelength is the declared packet's, k = pi / 4, and its rotation is the band's at the vacuum's paces, `rule3.plane_wave_dispersion`; the arrival of the packet at the screen is the band's group velocity (`bands.arrival_intervals`). The run's numbers (N = 270, the clicks' rows) are the reader's and never here.

Usage: `python tools/derivations/two_slits.py` prints them.
"""

from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # the folder's root, rule3.py, by its file
import rule3  # noqa: E402

# the declared file (the paper's Section 9.1): the gaps' rows, their centres and spacing, the screen's distance
GAP_ROWS = ((17, 18, 19), (29, 30, 31))
GAP_CENTRES = (18, 30)
GAP_SPACING = GAP_CENTRES[1] - GAP_CENTRES[0]  # d = 12 Links
SCREEN_DISTANCE = 24  # L = 24 Links from the wall at x = 20 to the screen at x = 44
WAVE_NUMBER = math.pi / 4  # the packet's k, the wavelength 8 Links
SCREEN_ROWS = 48  # the board's y, the rows 0 to 47
BLOCK = 4  # the twelve NodeReaders of four rows each
LIGHT_PAIR = (1, 1)


def wavelength_and_rotation() -> list[float]:
    """[the wavelength 2 pi / k, cos omega of the band at k = pi / 4, omega]: 8 Links and the rotation 0.4456 of the declared packet at the vacuum's paces (The line)."""
    cosine = rule3.plane_wave_dispersion(WAVE_NUMBER, *LIGHT_PAIR)
    return [2 * math.pi / WAVE_NUMBER, cosine, math.acos(cosine)]


def fringe_spacing() -> float:
    """lambda L / d, the far field's spacing: 16 Links (S.23)."""
    return wavelength_and_rotation()[0] * SCREEN_DISTANCE / GAP_SPACING


def path_difference(y: float) -> float:
    """sqrt(L^2 + (y - 18)^2) - sqrt(L^2 + (y - 30)^2), the two gaps' paths to the screen's row y (S.23)."""
    first, second = GAP_CENTRES
    return math.hypot(SCREEN_DISTANCE, y - first) - math.hypot(SCREEN_DISTANCE, y - second)


def near_field_minimum(target: float, low: float, high: float) -> float:
    """The row where the path difference is `target` (half a wavelength, +-4), by bisection on [low, high]."""
    for _ in range(200):
        middle = (low + high) / 2
        if (path_difference(middle) - target) * (path_difference(low) - target) <= 0:
            high = middle
        else:
            low = middle
    return (low + high) / 2


def near_field_minima() -> list[float]:
    """[lambda L / d, the lower minimum's row, the upper minimum's row, its region, the other's region, the pattern's centre, the blocks' centre]: 16, 15.3, 32.7, 3, 8, 24 and 23.5; the minima where the paths differ by half a wavelength, the regions the rows' four-row blocks counted from 0, the centre the gaps' mean row and the blocks' (0 + 47) / 2 (S.23)."""
    half = wavelength_and_rotation()[0] / 2
    lower = near_field_minimum(-half, 0.0, GAP_CENTRES[0])
    upper = near_field_minimum(half, GAP_CENTRES[1], SCREEN_ROWS - 1)
    return [
        fringe_spacing(),
        lower,
        upper,
        lower // BLOCK,
        upper // BLOCK,
        sum(GAP_CENTRES) / 2,
        (SCREEN_ROWS - 1) / 2,
    ]


def huygens_rows(open_gaps: tuple[tuple[int, ...], ...]) -> list[float]:
    """The Huygens sum's intensity at every screen row from the open gaps' Nodes, each a cylindrical wavelet e^(i k r) / sqrt r in the flat board, summed and squared (the paper's Section 9.2, "Huygens's sum")."""
    rows = []
    for y in range(SCREEN_ROWS):
        total = 0j
        for gap in open_gaps:
            for source in gap:
                r = math.hypot(SCREEN_DISTANCE, y - source)
                total += cmath.exp(1j * WAVE_NUMBER * r) / math.sqrt(r)
        rows.append(abs(total) ** 2)
    return rows


def regional_sums(rows: list[float]) -> list[float]:
    """The twelve four-row blocks' sums of a screen row."""
    return [sum(rows[i : i + BLOCK]) for i in range(0, SCREEN_ROWS, BLOCK)]


def interior_minima(values: list[float], low: int, high: int) -> list[int]:
    """The indices in [low, high] where a value is below both its neighbours."""
    return [
        i
        for i in range(max(low, 1), min(high, len(values) - 2) + 1)
        if values[i] < values[i - 1] and values[i] < values[i + 1]
    ]


def huygens_dips() -> list[float]:
    """The regions where the two gaps' Huygens regional sums dip, inside the central pattern (the regions 2 to 9): 3 and 8 under the cylindrical wavelet, and the same under 1 / r, under no decay and under an obliquity factor, the blocks of the near-field rows 15.3 and 32.7; the paper names the blind's dips as expectation.json's regions 4 and 8, the blind file's own reading, which no Huygens sum from the gaps' Nodes here gives."""
    return [float(i) for i in interior_minima(regional_sums(huygens_rows(GAP_ROWS)), 2, 9)]


def opaque_reader_envelope() -> list[float]:
    """[the number of minima of the two gaps' Huygens row across the central pattern (the rows 8 to 40), the same with one gap opaque]: 2 and 0; the opaque NodeReader in one gap takes that gap's inflow, the screen reads the other gap's envelope alone, monotone across the pattern, and the fringes are lost (the paper's Section 5.6)."""
    low, high = 8, 40
    both = len(interior_minima(huygens_rows(GAP_ROWS), low, high))
    one = len(interior_minima(huygens_rows((GAP_ROWS[1],)), low, high))
    return [float(both), float(one)]


if __name__ == "__main__":
    print("the wavelength, cos omega and omega:", [round(v, 4) for v in wavelength_and_rotation()])
    print("the near-field minima:", [round(v, 2) for v in near_field_minima()])
    print("the Huygens regional sums:", [round(v, 2) for v in regional_sums(huygens_rows(GAP_ROWS))])
    print("the Huygens dips:", huygens_dips())
    print("the minima with two gaps and with one opaque:", opaque_reader_envelope())
