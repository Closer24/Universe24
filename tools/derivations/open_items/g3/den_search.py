"""Hand g3 (2026-10-25): the den search. A lift of den's prime p = a^2 + b^2 (a > b > 0) is the point pi^2 x den / p with
num / den = (a^2 - b^2) / p and s / den = 2 a b / p (loader/circle.lift_points), so its gap is g = 2 b^2 / p and its sine 2 a b / p,
exact rationals of the prime alone. The search: every prime 1 mod 4 below 2^21 split by the loader's own two_squares; the heavy
lifts whose g lies in the window [g_lo, g_hi] (the brief's (a), this hand's window.py: 620 to 700 thousandths for a body four
Links wide over 100 intervals with the beat within 1/6 of the clock; the Compton window 10 to 41 thousandths listed beside);
the light lifts whose Compton length 1 / (sqrt 3 omega_0) lies in [10, 100] Links (a cloud); the dens the products p_heavy x
p_light within the bit bound (59 bits as the acts stand, 67 with the sum term by term; both far above these products);
the three best by the mass ratio s_heavy / s_light (nature's order 1,836 as far as the integers allow), as integer quotients
with remainders, with den's bits, each lift's g and Compton width in thousandths. The control den 15,162,856,759,112,389 is
read the same way. Floats stand only in `float_check`.
Run: PYTHONPATH=<worktree>/src python tools/derivations/g3/den_search.py > tools/derivations/g3/den_search.out
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F

from event_universe.loader import circle

BOUND = 1 << 21
BIT_BOUND_ACTS, BIT_BOUND_TERMWISE = 59, 67


def primes_1_mod_4(bound: int) -> list[int]:
    sieve = bytearray([1]) * bound
    sieve[0] = sieve[1] = 0
    for i in range(2, math.isqrt(bound) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(range(i * i, bound, i)))
    return [p for p in range(5, bound, 4) if sieve[p]]


def lift_of(p: int) -> dict:
    a, b = circle.gaussian_of(p)  # a > b > 0
    g = F(2 * b * b, p)
    sine = F(2 * a * b, p)
    omega0 = math.acos(float(1 - g))
    compton = 1 / (math.sqrt(3) * omega0)
    return {"p": p, "a": a, "b": b, "g": g, "sin": sine, "g_thousandths": [int(g * 1000), (2 * b * b * 1000) % p],
            "sin_thousandths": int(sine * 1000), "compton_thousandths": int(compton * 1000), "float_check": {"omega0": omega0, "compton": compton}}


def ratio_with_remainder(sin_h: F, sin_l: F) -> list[int]:
    q = sin_h / sin_l
    return [q.numerator // q.denominator, q.numerator % q.denominator, q.denominator]


def main() -> None:
    g_lo = F(int(sys.argv[1]), 1000) if len(sys.argv) > 1 else F(620, 1000)
    g_hi = F(int(sys.argv[2]), 1000) if len(sys.argv) > 2 else F(700, 1000)
    lifts = [lift_of(p) for p in primes_1_mod_4(BOUND)]
    heavy = [x for x in lifts if g_lo <= x["g"] <= g_hi]
    compton_heavy = [x for x in lifts if 2000 <= x["compton_thousandths"] <= 4000]
    light = [x for x in lifts if 10000 <= x["compton_thousandths"] <= 100000]
    dens = []
    for h in heavy:
        for l in light:
            den = h["p"] * l["p"]
            if den.bit_length() > BIT_BOUND_TERMWISE:
                continue
            dens.append({"den": den, "bits": den.bit_length(), "within_59": den.bit_length() <= BIT_BOUND_ACTS,
                         "heavy": h, "light": l, "mass_ratio": ratio_with_remainder(h["sin"], l["sin"])})
    dens.sort(key=lambda d: (-(d["mass_ratio"][0]), d["den"]))
    best = dens[:3]
    # the smallest den of the window (the fast toy) and the control den
    smallest = min(dens, key=lambda d: d["den"]) if dens else None
    control = 15162856759112389
    control_lifts = [lift_of(p) for p in sorted(circle.factors(control))]

    def shown(x: dict) -> dict:
        return {k: (str(v) if isinstance(v, F) else v) for k, v in x.items()}

    def den_shown(d: dict) -> dict:
        return {"den": d["den"], "bits": d["bits"], "within_59_bits": d["within_59"], "heavy": shown(d["heavy"]), "light": shown(d["light"]),
                "mass_ratio_quotient_remainder_divisor": d["mass_ratio"]}

    out = {
        "window_g_thousandths": [int(g_lo * 1000), int(g_hi * 1000)],
        "primes_1_mod_4_below": BOUND, "count": len(lifts), "heavy_in_window": len(heavy), "light_cloud_10_to_100": len(light),
        "heavy_lifts_in_window_smallest_primes": [shown(x) for x in sorted(heavy, key=lambda x: x["p"])[:12]],
        "compton_window_2_to_4_links_lifts_smallest_primes": [shown(x) for x in sorted(compton_heavy, key=lambda x: x["p"])[:8]],
        "dens_two_primes_count": len(dens),
        "best_three_by_mass_ratio": [den_shown(d) for d in best],
        "smallest_den_of_window": den_shown(smallest) if smallest else None,
        "control_den": {"den": control, "bits": control.bit_length(), "lifts": [shown(x) for x in control_lifts],
                        "mass_ratio_heavy_over_light": [ratio_with_remainder(h["sin"], control_lifts[-1]["sin"]) for h in control_lifts[:2]]},
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
