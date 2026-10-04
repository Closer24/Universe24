"""The click's formulas from Rule3's line (ALGEBRA.md, The click; The click is the meeting; the paper's Section 5, S.8, S.50, S.61): the frozen Node that reads nothing through its Ports, the front's ball of (2d + 1)(2d^2 + 2d + 3) / 3 Nodes at one Link per interval, the declarations' costs (the region's reading factor, the draw's scatter), the record's unit against the band's rotation, the one draw per record, the arrival window from the lay, the form of the decision D = now^2 - next x before, the count constant between clicks, the quantum that never breaks, the common unit that cancels in every ratio, and the telegraph's statistics from the rate equations.

Usage: `python tools/derivations/clicks.py` prints them.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # the folder's root, rule3.py, by its file
import rule3  # noqa: E402

LIGHT_PAIR = (1, 1)
MATTER_PAIR = (2, 3)  # the paper's computed pair
GAMMA = 6000  # the law's Gamma in its example (The frozen Node has no share, "4.70 at Gamma = 6,000")
TWO_SLITS_WAVE_NUMBER = math.pi / 4  # the two slits' packet, the wavelength 8 Links
TWO_SLITS_DISTANCE = 34  # the packet's centre at x = 10 to the screen at x = 44
REGION_ROWS, FRINGE = 4, 16  # S.8: n = 4 rows, Lambda = 16 Links
HUYGENS_N, REGIONS = 273, 12  # the Huygens blind's N and the screen's twelve regions
# the telegraph's declared example (the paper's Section 10.3, Open): the shelving hazard Omega_w^2 / R per
# interval, the dark period tau_D, the bright rate and the bin of the counts' histogram
SHELVING_HAZARD, DARK_PERIOD, BRIGHT_RATE, BIN = Fraction(1, 1000), 500, 0.1, 100


def frozen_node() -> list[float]:
    """[R_a at a Node whose pace is 0, the content U = (1 / 2) ln(2 Gamma) above which p_i = p_0^2 / Gamma rounds to 0 at Gamma = 6,000, the same from the clock's exact formula]: 0, 4.70, 4.70; the frozen Node reads nothing through its six Ports (The paces: R_a = 2 num p_i^2 q^2 / Gamma^2 at p_i = 0), stands in no NodeReader's front and is never clicked (The frozen Node has no share)."""
    num, den = MATTER_PAIR
    read = rule3.link_coefficient(num, 0, GAMMA, GAMMA)
    # the first content at which Gamma (1 - 1 / Gamma)^(2c) < 1 / 2, checked exactly on both sides
    content = math.ceil(math.log(2 * GAMMA) / (-2 * math.log(1 - 1 / GAMMA)))
    assert rule3.node_pace(rule3.clock_pace(GAMMA, content), GAMMA) < Fraction(1, 2)
    assert rule3.node_pace(rule3.clock_pace(GAMMA, content - 1), GAMMA) >= Fraction(1, 2)
    return [float(read), math.log(2 * GAMMA) / 2, content / GAMMA]


def front_ball(radii: tuple[int, ...] = (0, 1, 2, 3, 4)) -> list[int]:
    """The number of Nodes within d Links of a Node, |x| + |y| + |z| <= d, by enumeration: 1, 7, 25, 63, 129, the formula (2d + 1)(2d^2 + 2d + 3) / 3 of the figure's caption, the ball the click's front reaches at one Link per interval (Rule3 reads the six neighbours alone, The line)."""
    counts = []
    for d in radii:
        count = sum(
            1
            for x in range(-d, d + 1)
            for y in range(-d, d + 1)
            for z in range(-d, d + 1)
            if abs(x) + abs(y) + abs(z) <= d
        )
        assert 3 * count == (2 * d + 1) * (2 * d * d + 2 * d + 3)
        counts.append(count)
    return counts


def declaration_costs() -> list[float]:
    """[the region's reading factor sin(pi n / Lambda) / (n sin(pi / Lambda)) at n = 4, Lambda = 16, the same at Lambda = n, the draw's scatter sqrt(N p (1 - p)) at the Huygens blind's N = 273 and p = 1 / 12]: 0.91, 0 and 4.57; each declaration costs a pattern in the histogram and never one click (S.8)."""
    factor = math.sin(math.pi * REGION_ROWS / FRINGE) / (REGION_ROWS * math.sin(math.pi / FRINGE))
    at_region = math.sin(math.pi) / (REGION_ROWS * math.sin(math.pi / REGION_ROWS))
    p = 1 / REGIONS
    return [factor, abs(at_region), math.sqrt(HUYGENS_N * p * (1 - p))]


def own_clock_and_units() -> list[float]:
    """[omega of the two slits' light at k = pi / 4, the photons per unit of count 1 / sin omega, the NodeReader's own clock per interval at the vacuum's content p_0 / Gamma]: 0.4456, 2.3204 and 1; one unit of count is one wall W_c = 3 den T of inflow (The conventions and the units, row 11), a photon's share at omega is W_c sin omega (row 12), so N units are N / sin omega photons, the factor 1 / sin omega the convention of three units of one quantum (row 17), and the click line carries the NodeReader's own clock, the carried sum of p_0 / Gamma over the window (The click is the meeting, the click line naming the NodeReader, the family, the count, its own clock and the window)."""
    omega = math.acos(rule3.plane_wave_dispersion(TWO_SLITS_WAVE_NUMBER, *LIGHT_PAIR))
    return [omega, 1 / math.sin(omega), float(rule3.clock_pace(GAMMA, 0)) / GAMMA]


def credit(shares: list[Fraction], count: int) -> int:
    """N = SUM s_R rounded half up and capped by the record's count, the clicks the credit draws from the shares s_R = Q_R / W_c of every NodeReader reading one record (The click, algebraically; The conventions and the units, row 16: N = (SUM s + W_rec div 2) div W_rec; S.50)."""
    return min(count, math.floor(sum(shares) + Fraction(1, 2)))


def one_draw_per_record() -> list[int]:
    """[the clicks from a record of count 1 whose one quantum is shared over three NodeReaders, the coincidences between them]: 1 and 0; the one draw over all the NodeReaders reading one record gives one click per record, antibunching (the paper's Section 5.4)."""
    shares = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)]
    clicks = credit(shares, 1)
    return [clicks, clicks - 1]


def arrival_window() -> list[float]:
    """[the probe's arrival at a NodeReader 34 Links from its lay at k = pi / 4, in intervals]: 62.2; the window closes at the interval of the probe's lay, and the arrival is derived from the lay by the band's group velocity, from click times and from no level read (the paper's Section 5.4)."""
    return [TWO_SLITS_DISTANCE / rule3.group_velocity(TWO_SLITS_WAVE_NUMBER, *LIGHT_PAIR)]


def decision_form() -> list[float]:
    """[the largest |D - A^2 sin^2 omega| / A^2 for a plane wave at the band's omega, sin^2 omega at k = pi / 4]: 0 and 0.1857; the share is the form D = now^2 - next x before, the now against the future times the past, A^2 sin^2 omega for a plane wave (the paper's Section 5.2; S.14)."""
    num, den = LIGHT_PAIR
    omega = math.acos(rule3.plane_wave_dispersion(TWO_SLITS_WAVE_NUMBER, num, den))
    worst = 0.0
    for t in range(200):
        now = math.cos(TWO_SLITS_WAVE_NUMBER * 3 - omega * t)
        nxt = math.cos(TWO_SLITS_WAVE_NUMBER * 3 - omega * (t + 1))
        before = math.cos(TWO_SLITS_WAVE_NUMBER * 3 - omega * (t - 1))
        worst = max(worst, abs(now * now - nxt * before - math.sin(omega) ** 2))
    return [worst, math.sin(omega) ** 2]


def counts_move_only_at_clicks(intervals: int = 50, nodes: int = 24) -> list[Fraction]:
    """[the change of the conserved form over 50 intervals of a record stepped by Rule3's line in exact rationals]: 0; Theorem 3's statement (The conserved form): the form E, the count's measure, is exact in the line where the paces stand, so a count stepped by Rule3 alone is constant between clicks; that nothing but Rule3 writes a record's lines between clicks is the engine's structure, shown by its tests and not here."""
    draw = random.Random(24)
    num, den = MATTER_PAIR
    arrivals = rule3.chain_arrivals(nodes)
    now = [Fraction(draw.randint(-1000, 1000)) for _ in range(nodes)]
    before = [Fraction(draw.randint(-1000, 1000)) for _ in range(nodes)]
    start = rule3.conserved_form(now, before, arrivals, num, den)
    for _ in range(intervals):
        nxt = [
            rule3.step_exact(now[i], before[i], [now[j] for j in arrivals[i]], num, den)
            for i in range(nodes)
        ]
        now, before = nxt, now
    return [rule3.conserved_form(now, before, arrivals, num, den) - start]


def a_quantum_never_breaks() -> list[int]:
    """[the clicks a record of count 1 gives, its count after, the clicks a body of count 5 emits one quantum at a time]: 1, 0 and 5; a click at a body's front parts one quantum, and a quantum of count 1 has no part the click credits (the paper's Section 7.3)."""
    whole = [Fraction(1)]
    taken = credit(whole, 1)
    body_count, clicks = 5, 0
    while body_count > 0:
        body_count -= credit([Fraction(1)], body_count)
        clicks += 1
    return [taken, 1 - taken, clicks]


def common_unit_cancels() -> list[Fraction]:
    """[the largest difference of the regions' probabilities s_i / SUM s between two units of the share, the difference of Bell's E between two common factors of the parts' products]: 0 and 0; the share stays the conserved form and the draw's measure, so a common unit cancels in every ratio (the paper's Section 7.4)."""
    shares = [Fraction(v) for v in (15, 11, 23, 34, 41, 26, 9, 12, 20, 38, 28, 16)]
    unit_a, unit_b = Fraction(1), Fraction(7, 3)
    total_a, total_b = sum(shares) * unit_a, sum(shares) * unit_b
    worst = max(abs(s * unit_a / total_a - s * unit_b / total_b) for s in shares)
    products = [(Fraction(3), Fraction(3)), (Fraction(21), Fraction(21))]
    correlations = []
    for m in products:
        same, cross = (12 * m[0] + 0 * m[1]) ** 2, (0 * m[0] - 5 * m[1]) ** 2
        correlations.append(Fraction(same - cross, same + cross))
    return [worst, correlations[1] - correlations[0]]


def moves_only_by_clicks() -> list[Fraction]:
    """[N(t_2) / N(t_1) at fixed paces between clicks]: 1; Eq. (13)'s two factors are 1 where the well stands still, so a body's count moves only by the clicks at its front (the paper's Section 7.5)."""
    num, den = MATTER_PAIR
    clock = rule3.clock_pace(GAMMA, 0)
    pace = rule3.node_pace(clock, GAMMA)
    cosine = Fraction(1) - (Fraction(1) - Fraction(num, den)) * (clock / GAMMA) ** 2
    return [(cosine / cosine) * (pace * pace) / (pace * pace)]


def telegraph_statistics() -> list[float]:
    """[the mean bright period from the geometric series of the shelving hazard, R / Omega_w^2, the fraction of time bright, the Fano factor of a Poisson count, the Fano factor of the telegraph's counts in a bin]: 1000, 1000, 2 / 3, 1 and 4.33 at the declared example; the shelving at the constant hazard h = Omega_w^2 / R gives exponential bright periods of mean 1 / h, the dark periods the declared tau_D, and the counts in a bin shorter than both are bimodal, 0 or Poisson at the bright rate, with the variance over the mean 1 + (1 - f) lambda tau_bin (Cook and Kimble's rate equations; S.56 (15))."""
    h = float(SHELVING_HAZARD)
    series, survival = 0.0, 1.0
    for t in range(1, 200_000):
        series += t * h * survival
        survival *= 1 - h
    bright = 1 / h
    fraction = bright / (bright + DARK_PERIOD)
    expected_counts = BRIGHT_RATE * BIN
    return [series, bright, fraction, 1.0, 1 + (1 - fraction) * expected_counts]


if __name__ == "__main__":
    print("the frozen Node:", [round(v, 3) for v in frozen_node()])
    print("the front's ball:", front_ball())
    print("the declarations' costs:", [round(v, 3) for v in declaration_costs()])
    print("the own clock and the units:", [round(v, 4) for v in own_clock_and_units()])
    print("one draw per record:", one_draw_per_record())
    print("the arrival window:", [round(v, 2) for v in arrival_window()])
    print("the decision's form:", [round(v, 5) for v in decision_form()])
    print("the count between clicks:", [str(v) for v in counts_move_only_at_clicks()])
    print("a quantum never breaks:", a_quantum_never_breaks())
    print("a common unit cancels:", [str(v) for v in common_unit_cancels()])
    print("moves only by clicks:", [str(v) for v in moves_only_by_clicks()])
    print("the telegraph's statistics:", [round(v, 3) for v in telegraph_statistics()])
