"""Hand n1 (2026-10-25): the charge's unit T div 2 and its thirds on the lay's integers; the neutrino's room on den's circle.

Integers only. (1) At T = 36,000 (the file's) and T = 32,768 (the paper's): T div 2 (the unit, one quantum's
Wronskian at the quarter-turn lay), T div 6 (a third) with its remainder; whether a third is a square (a plane laid
at the quarter turn with equal legs carries W = A^2); the tightest split of T div 2 into three sums of two squares
(the law's exact split 5450 + 5458 + 5476 = 16384 at T 32768 re-derived) and into three equal thirds; the count a
plane of W = T div 6 reads under the law's one division by the unit, (n |W| + (T div 2) div 2) div (T div 2) for
n = 1 and n = 3 planes; the birth's lay A = isqrt(T div 2) and its W = A^2. (2) The neutrino's room: the least leg of
any point of den's circle is at least isqrt(2 den - 1) (s^2 = g (2 den - g), g >= 1), so the least sine ratio
to the light lift at the record's den is isqrt(2 den - 1) over s_light in ppm; nature's m_nu / m_e below 1.6 x 10^-6
(0.8 eV over 511 keV) asks a Gaussian prime a^2 + 1 with 1 / a below that ratio times the light lift's sine: the
bits of the den that would carry it, against the hands' bound on Rule3's total (den's bits + 64 within 128).
"""
from __future__ import annotations

from math import isqrt

from event_universe.loader.circle import circle_points


def two_square_sums(upto: int) -> set[int]:
    found = set()
    a = 0
    while a * a <= upto:
        b = a
        while a * a + b * b <= upto:
            found.add(a * a + b * b)
            b += 1
        a += 1
    return found


def tightest_three(total: int) -> tuple[int, int, int] | None:
    """The tightest split of `total` into three sums of two squares (each a plane's |z|^2), the spread least."""
    ok = two_square_sums(total)
    best = None
    third = total // 3
    for spread in range(0, third + 1):
        for x in range(third - spread, third + spread + 1):
            for y in range(x, third + spread + 1):
                z = total - x - y
                if z < y:
                    break
                if z - x > spread:
                    continue
                if x in ok and y in ok and z in ok:
                    return (x, y, z)
    return best


def unit_report(T: int) -> None:
    unit = T // 2
    third, rem = divmod(T, 6)
    A = isqrt(unit)
    print(f"T = {T}: the unit T div 2 = {unit}; a third T div 6 = {third} remainder {rem}; 6 divides T: {rem == 0}")
    print(f"  the birth's lay A = isqrt(T div 2) = {A}, its W = A^2 = {A * A}, short of the unit by {unit - A * A}")
    r = isqrt(third)
    print(f"  a third as a square: isqrt({third}) = {r}, {r}^2 = {r * r}, {(r + 1)}^2 = {(r + 1) ** 2}: a third is a square: {r * r == third}")
    # a plane of W = third at unequal legs A x B = third: the factor pairs
    pairs = [(a, third // a) for a in range(1, isqrt(third) + 1) if third % a == 0]
    print(f"  W = A x B = {third} by the lay (A, 0), (0, B): {len(pairs)} factor pairs, e.g. {pairs[-3:]}")
    for n in (1, 2, 3):
        count = (n * third + unit // 2) // unit
        print(f"  {n} plane(s) of W = T div 6 read the count (n W + unit div 2) div unit = {count}")
    print(f"  the tightest split of T div 2 into three planes' |z|^2 (sums of two squares): {tightest_three(unit)}")
    print(f"  the equal thirds {third}, {third}, {third} sum to {3 * third} against T div 2 = {unit}: exact thirds: {3 * third == unit}")
    print()


def neutrino_room(den: int) -> None:
    pts = circle_points(den)
    s_light = min(s for _v, _n, s in pts)
    floor = isqrt(2 * den - 1)
    print(f"den {den}: the least leg of any point is at least isqrt(2 den - 1) = {floor}; the light lift's s = {s_light}")
    print(f"  so no point of this den is lighter than the light lift ({(1_000_000 * floor) // s_light} ppm of it at the very least;"
          f" the lightest point IS the light lift, the theorem)")
    nu_ppm = 2  # nature's m_nu / m_e below 1.6 x 10^-6 = 1.6 ppm, rounded up to 2 ppm, a comparison column
    sine_light_ppm = (1_000_000 * s_light) // den
    # a new prime p = a^2 + 1 carries the angle about 1 / a (b = 1): need 10^6 / a <= nu_ppm x sine_light_ppm / 10^6
    a_min = (10**12) // (nu_ppm * sine_light_ppm) + 1
    p_min = a_min * a_min + 1
    den_new = den * p_min
    print(f"  a neutrino-like lift at or below {nu_ppm} ppm of the light lift needs a prime a^2 + 1 with a >= {a_min}"
          f" ({p_min.bit_length()} bits), the den then {den_new.bit_length()} bits; Rule3's total den's bits + 64 = {den_new.bit_length() + 64}"
          f" against 128: within 128: {den_new.bit_length() + 64 <= 128}")
    print()


if __name__ == "__main__":
    for T in (36_000, 32_768):
        unit_report(T)
    for den in (1_655_909_141, 348_893):
        neutrino_room(den)
