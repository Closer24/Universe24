"""Hand n1 (2026-10-25): den's circle at the brief's two dens and at the G-S1 dens, in integers only.

For each den: its factors; every point (vector, num, s) of the open quadrant by the loader's own
circle_points (src read, not edited); each point's gap g = den - num as thousandths (1000 g div den) and
as parts per million; the lifts (one prime's point at its whole power, v_k = 2 e_k); the heavy lift and
the light lift; the mass ratio s_heavy / s_light as a quotient with its remainder and in parts per
million; the neutron-like step: for every point, 1,000,000 x s / s_heavy as an integer (nature's
s_n / s_p = 1.0013784 is 1,001,378 ppm) and the nearest point above the heavy lift; the composite
points named by their vectors. The sine of a point is s / den; no float anywhere: every reading a
quotient with its remainder or a parts-per-million integer.
"""
from __future__ import annotations

import sys

from event_universe.loader.circle import angled, circle_points, factors

DENS = (3_311_818_282, 697_786, 1_655_909_141, 348_893)
NATURE_N_OVER_P_PPM = 1_001_378  # nature's m_n / m_p = 1.0013784, a comparison column and no input
NATURE_P_OVER_E_PPM = 1_836_152_673  # nature's m_p / m_e x 10^6, a comparison column


def ppm(a: int, b: int) -> int:
    return (1_000_000 * a) // b


def report(den: int) -> None:
    f = factors(den)
    primes, scale = angled(den)
    pts = circle_points(den)
    print(f"den {den} ({den.bit_length()} bits) factors {dict(sorted(f.items()))} scale {scale}")
    print(f"  primes 1 mod 4: {primes}; points in the open quadrant: {len(pts)}")
    lifts = []
    for vector, num, s in pts:
        g = den - num
        kind = "lift" if sum(1 for v in vector if v) == 1 and all(v >= 0 for v in vector) else (
            "mirror-lift" if sum(1 for v in vector if v) == 1 else "composite"
        )
        if kind == "lift":
            lifts.append((s, vector, num))
        print(
            f"  v={vector} num={num} s={s} gap={g} g_thousandths={(1000 * g) // den}"
            f" g_ppm={ppm(g, den)} sine_ppm={ppm(s, den)} {kind}"
        )
    lifts.sort()
    if len(lifts) >= 2:
        s_light, v_light, _ = lifts[0]
        s_heavy, v_heavy, num_heavy = lifts[-1]
        q, r = divmod(s_heavy, s_light)
        print(
            f"  light lift v={v_light} s={s_light}; heavy lift v={v_heavy} s={s_heavy}"
            f" g_heavy_thousandths={(1000 * (den - num_heavy)) // den}"
        )
        print(f"  mass ratio s_heavy / s_light = {q} remainder {r}; ppm {ppm(s_heavy, s_light)}"
              f" (nature's p/e {NATURE_P_OVER_E_PPM} ppm)")
        above = sorted((ppm(s, s_heavy), vector, s) for vector, num, s in pts if s > s_heavy)
        print(f"  points heavier than the heavy lift (s / s_heavy in ppm): {above}")
        if above:
            print(
                f"  the nearest step above the heavy lift: {above[0][0]} ppm against nature's n/p"
                f" {NATURE_N_OVER_P_PPM} ppm; difference {above[0][0] - NATURE_N_OVER_P_PPM} ppm"
            )
        else:
            print("  no point of the circle lies above the heavy lift: the neutron-like step is NOT on this circle")
        # the Compton width of the light lift in Links: den div (s sqrt 3) ~ (den x 1000) div (1732 s), integer
        print(f"  light lift's 1/(sqrt3 sin) in milli-Links: {(1000 * 1000 * den) // (1732 * s_light)} ;"
              f" heavy lift's: {(1000 * 1000 * den) // (1732 * s_heavy)}")
    print()


if __name__ == "__main__":
    dens = [int(a.replace(",", "")) for a in sys.argv[1:]] or list(DENS)
    for d in dens:
        report(d)
