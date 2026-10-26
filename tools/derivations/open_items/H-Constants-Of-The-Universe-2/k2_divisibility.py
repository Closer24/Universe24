"""Hand K2, the owner's addition to BRIEF_k: what den, Gamma, T and G must be so that every division the law calls exact is exact (remainder 0) and where a rounding is the law's own. Measured on the engine's primitives, integers only.

(1) the paces' group law: (Gamma - 1)^c mod Gamma^(c - 1), never 0 at c >= 2 ((Gamma - 1)^c = (-1)^c mod Gamma), the clock's one rounding the law's own; the integer group law's defect clock(c1 + c2) against rounded(clock(c1) clock(c2), Gamma);
(2) the half walls: w = 6 den Gamma^2 G^2 even at every den (the half-wall move exact), Gamma^2 div 2 (the Link factor's half) exact iff Gamma even, the phase line's D div 2 = 4 Gamma^2 always;
(3) the ties: rounded(p^2, Gamma) over every content below the frozen one (a tie needs Gamma even), odd_rounded(angle p_0, Gamma) over angles and clocks, link_factor over every tension;
(4) the take's walls 3 T s: 9 T^2 (den^2 - num^2) a perfect square at every point of den's circle (Pythagoras: s^2 = den^2 - num^2), and W_c div 2 exact iff T s even;
(5) the Wronskian over T div 2: T even; T div 6 for the three-plane split: 6 | T;
(6) the lay's amplitude: A^2 = T den / (2 s) integral iff 2 s | T den, 4 a b | T for a lift of p = a^2 + b^2; no T makes both light's A^2 = T / 2 and a lift's A^2 = T p / (4 a b) squares (p-adic: v_p odd against even), measured by a scan;
(7) the volume holder's pair (den - den div Gamma, den): its gap exactly 1 / Gamma iff Gamma | den; den = Gamma x (angled part) makes it exact with the circle's points scaled by Gamma;
(8) G: Q = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2 exact at every tension iff Gamma | G; G | Gamma buys nothing; G = 2^e a choice;
(9) the smallest integral set and the largest within 128 bits under (2), (5), (6), (7): den = Gamma x angled, Gamma = 2^a 3^b even, T even with 4 a_k b_k | T for every lift, G = 1 or 16.

Run: PYTHONPATH=<worktree>/src python tools/derivations/open_items/H-Constants-Of-The-Universe-2/k2_divisibility.py > tools/derivations/open_items/H-Constants-Of-The-Universe-2/k2_divisibility.txt
"""

from __future__ import annotations

import json
from math import gcd

from event_universe.core import paces, rule3
from event_universe.core.ports import LINK_UNIT
from event_universe.core.rule3 import division_forward, largest_below, link_factor, wall_of
from event_universe.loader import derived
from event_universe.loader.circle import circle_points, factors, lift_points, two_squares
from event_universe.loader.universe import volume_pair

DENS = (1021, 348893, 1655909141, 4471099877, 15162856759112389)
BITS = 128


def rem(a: int, b: int) -> int:
    return int(division_forward(a, b, 0)[1])


def rounded(n: int, w: int) -> int:
    return int(division_forward(n + n, w + w, w)[0])


def lifts_ab(den: int) -> list[tuple[int, int, int, int, int]]:
    """Per lift: (p, a, b, num, s)."""
    found = []
    primes = sorted(p for p in factors(den) if rem(p, 4) == 1)
    for (vector, num, s), p in zip(lift_points(den), primes, strict=True):
        a, b = two_squares(p)
        a, b = max(a, b), min(a, b)
        found.append((p, a, b, num, s))
    return found


def main() -> None:
    out: dict[str, object] = {}
    # (1) the paces' group law
    law = {}
    for gamma in (1000, 1021, 6000, 1024, 972):
        rems = [rem((gamma - 1) ** c, gamma ** (c - 1)) for c in range(2, 7)]
        side = paces.side_of(gamma, 120)
        clocks = side.clocks
        defects = []
        for c1 in range(0, 61):
            for c2 in range(0, 61):
                defects.append(abs(clocks[c1 + c2] - rounded(clocks[c1] * clocks[c2], gamma)))
        law[str(gamma)] = {
            "remainders_(Gamma-1)^c_mod_Gamma^(c-1)_c_2_to_6": rems,
            "group_law_defect_count_nonzero_c1_c2_le_60": sum(1 for d in defects if d),
            "group_law_defect_largest_units": max(defects),
            "pairs": len(defects),
        }
    out["paces_group_law"] = law
    # (2) the half walls
    halves = {}
    for den in DENS:
        for gamma in (1000, 1021):
            w = int(wall_of(den, gamma, LINK_UNIT))
            halves[f"den_{den}_Gamma_{gamma}"] = {
                "w_mod_2": rem(w, 2),
                "Gamma2_mod_2": rem(gamma * gamma, 2),
                "D_phase_mod_2": rem(2 * (2 * gamma) ** 2, 2),
                "w_mod_12_den_G2": rem(w, 12 * den * LINK_UNIT * LINK_UNIT),
                "count_unit_3denT_mod_2_T36000": rem(3 * den * 36000, 2),
            }
    out["half_walls"] = halves
    # (3) the ties
    ties = {}
    for gamma in (1000, 1021, 6000):
        frozen = paces.frozen_content(gamma)
        reach = min(frozen, 3 * gamma)
        clocks = paces.side_of(gamma, reach - 1).clocks[:reach]
        pace_ties = sum(1 for p in clocks if rem(2 * p * p, 2 * gamma) == gamma)
        turn_ties = 0
        for p in clocks[:21]:
            for angle in range(-2000, 2001):
                n = angle * p
                if rem(2 * abs(n), 2 * gamma) == gamma:
                    turn_ties += 1
        link_ties = sum(
            1
            for t in range(gamma)
            if rem(LINK_UNIT * LINK_UNIT * (gamma - t) ** 2, gamma * gamma) == int(division_forward(gamma * gamma, 2, 0)[0])
        )
        ties[str(gamma)] = {
            "contents_scanned": reach,
            "link_pace_rounding_ties": pace_ties,
            "turn_odd_rounding_ties_angles_pm2000_clocks_0_to_20": turn_ties,
            "link_factor_ties_over_all_t_G16": link_ties,
            "Gamma_even": rem(gamma, 2) == 0,
        }
    out["ties"] = ties
    # (4) the take's walls 3 T s and (6) the lay
    walls = {}
    for den in DENS:
        points = circle_points(den)
        T = 36000
        squares = all(
            largest_below(9 * T * T * (den * den - num * num)) ** 2 == 9 * T * T * (den * den - num * num)
            for _v, num, _s in points
        )
        units_even = all(rem(3 * T * s, 2) == 0 for _v, _num, s in points)
        lifts = lifts_ab(den)
        lay = []
        for p, a, b, num, s in lifts:
            r = rem(T * den, 2 * s)
            need = 4 * a * b
            lay.append(
                {
                    "p": p,
                    "a": a,
                    "b": b,
                    "num": num,
                    "s": s,
                    "T_den_mod_2s_at_T36000": r,
                    "4ab": need,
                    "T36000_mod_4ab": rem(T, need),
                    "least_T_with_A2_square": need * p,  # T p / (4 a b) = p^2 at T = 4 a b p
                }
            )
        walls[str(den)] = {
            "points": len(points),
            "3Ts_exact_at_every_point": squares,
            "W_c_even_at_every_point_T36000": units_even,
            "lifts": lay,
            "lcm_4ab_over_lifts": __import__("math").lcm(*[4 * a * b for _p, a, b, _n, _s in lifts]),
        }
    out["take_walls_and_lay"] = walls
    # (6) no T makes both light's and the lift's lays exact (den 1021, scan T <= 2 x 10^6)
    p, a, b, num, s = lifts_ab(1021)[0]
    both = 0
    for T in range(2, 2_000_001, 2):
        light = T // 2
        if largest_below(light) ** 2 != light:
            continue
        if rem(T * p, 4 * a * b) == 0:
            lift = T * p // (4 * a * b)
            if largest_below(lift) ** 2 == lift:
                both += 1
    out["T_with_both_lays_exact_den_1021_T_le_2e6"] = both
    # (5) T's parity
    out["T"] = {str(T): {"mod_2": rem(T, 2), "mod_6": rem(T, 6), "mod_12": rem(T, 12)} for T in (36000, 36001, 32768)}
    # (7) the volume holder's pair
    vol = {}
    for den, gamma in ((1021, 1000), (1021, 1021), (1021000, 1000), (348893, 1000), (348893, 1297), (348893, 269), (15162856759112389, 1000)):
        pr = volume_pair(den, gamma)
        vol[f"den_{den}_Gamma_{gamma}"] = {
            "pair": list(pr),
            "den_mod_Gamma": rem(den, gamma),
            "gap_x_Gamma_over_den_exact": (den - pr[0]) * gamma == den,
            "gap_defect_per_million": int(division_forward(abs((den - pr[0]) * gamma - den) * 1_000_000, den, 0)[0]),
        }
    out["volume_pair"] = vol
    out["den_54bit_factors"] = {str(k): v for k, v in factors(15162856759112389).items()}
    out["den_348893_factors"] = {str(k): v for k, v in factors(348893).items()}
    out["den_1655909141_factors"] = {str(k): v for k, v in factors(1655909141).items()}
    out["den_4471099877_factors"] = {str(k): v for k, v in factors(4471099877).items()}
    # (8) G
    gq = {}
    for gamma in (1000, 1024):
        for g in (1, 8, 16, 125, 200, 1000, 1024):
            exact = sum(1 for t in range(gamma) if rem(g * g * (gamma - t) ** 2, gamma * gamma) == 0)
            gq[f"Gamma_{gamma}_G_{g}"] = {"tensions_exact_of_Gamma": exact, "G_divides_Gamma": rem(gamma, g) == 0, "Gamma_divides_G": rem(g, gamma) == 0}
    out["link_factor_exactness"] = gq
    # (9) the smallest integral set and the largest within 128 bits
    # smallest: den = Gamma x p with p the least prime 1 mod 4 (5 = 2^2 + 1^2), Gamma = 2 (even), T = lcm(2, 4 a b) = 8, G = 1
    small = {"den": 10, "Gamma": 2, "T": 8, "G": 1}
    pts = circle_points(10)
    small["points"] = [(num, s) for _v, num, s in pts]
    small["volume_pair"] = list(volume_pair(10, 2))
    small["wall"] = int(wall_of(10, 2, 1))
    small["A2_lift_T_den_over_2s"] = [(8 * 10) // (2 * s) for _v, _n, s in pts]
    small["A2_light_T_div_2"] = 4
    out["smallest_integral_set"] = small
    # largest within 128 bits: den = Gamma x angled, Gamma = 2^a 3^b, the light line's Rule3 total at A = 4 Gamma^3 within 128 at G 16 and at G 1
    largest = {}
    for angled in (1021, 348893, 617 * 196613):
        lifts = lifts_ab(angled)
        need = __import__("math").lcm(2, *[4 * a * b for _p, a, b, _n, _s in lifts])
        for unit in (16, 1):
            best = None
            for a_ in range(1, 40):
                for b_ in range(0, 25):
                    gamma = (2**a_) * (3**b_)
                    den = gamma * angled
                    w = int(wall_of(den, gamma, unit))
                    amp = 4 * gamma**3
                    total = 3 * w * amp + 2 * w * amp + w + 2 * w * amp + w
                    if total.bit_length() <= BITS and (best is None or gamma > best[0]):
                        best = (gamma, a_, b_, den, w.bit_length(), total.bit_length())
            if best:
                gamma, a_, b_, den, wb, tb = best
                largest[f"angled_{angled}_G_{unit}"] = {
                    "Gamma": gamma,
                    "2^a_3^b": [a_, b_],
                    "den": den,
                    "den_bits": den.bit_length(),
                    "wall_bits": wb,
                    "light_total_bits_at_4Gamma3": tb,
                    "T_least_multiple": need,
                    "volume_pair_exact": (den - volume_pair(den, gamma)[0]) * gamma == den,
                }
    out["largest_integral_within_128"] = largest
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
