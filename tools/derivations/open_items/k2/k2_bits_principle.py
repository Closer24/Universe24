"""Hand K2, the principle "the constants are the largest the 128 bits allow" (BRIEF_k (b)(ii), (b)(iii), (c)).

For each den of the window (1,021 the toy; 348,893; 1,655,909,141; 4,471,099,877; the 54-bit control) at G 16:
(1) the engine's own width (loader/rooms.width_of), the amplitude bound A, the wall's bits, Rule3's total's bits
at A (the test's form: flux_total on the rule's integers with the six arrivals at -A), the volume's deepest level
X(frozen - 1), the paces' running fraction's bits at the deepest content, the take's common denominator's bits,
all at Gamma 1,000 and T 36,000; (2) the predicate P(Gamma, T) := amplitude_bound(rows(den, Gamma), Gamma, T,
128, G) >= X(frozen - 1) (the engine's width_of <= 128 bit for bit, the deep clock by the 128-bit iterated
rounding p(c + 1) = rounded(p(c) (Gamma - 1), Gamma), checked against the engine's exact power at Gamma <= 6,000)
and Gamma <= den (the volume holder's pair (den - den div Gamma, den) needs den div Gamma >= 1); the largest
Gamma at T 36,000, the largest T at Gamma 1,000 and at the largest Gamma, and the curve Gamma_max(T) at four T's;
(3) the resolutions: p_0(Gamma) (the e-fold), isqrt(T div 2), isqrt(T), T div 2, the count units; (4) the
sign holder's alpha pair (E_h T, Gamma) reduced, the engine's.

Run: PYTHONPATH=<worktree>/src python tools/derivations/k2/k2_bits_principle.py > tools/derivations/k2/k2_bits_principle.txt
"""

from __future__ import annotations

import json
import sys
import time

import numpy as np

from event_universe.core import paces, rule3
from event_universe.core.ports import LINK_UNIT, PORTS
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.features import volume
from event_universe.loader import derived
from event_universe.loader.rooms import width_of
from event_universe.loader.universe import universe_of

BITS = 128
DENS = (1021, 348893, 1655909141, 4471099877, 15162856759112389)


def rounded(n: int, w: int) -> int:
    return int(division_forward(n + n, w + w, w)[0])


def iterated_clock(gamma: int, content: int) -> int:
    """p(0) = Gamma, p(c + 1) = rounded(p(c) (Gamma - 1), Gamma): every integer below Gamma^2, within 128 bits."""
    p = gamma
    for _ in range(content):
        p = rounded(p * (gamma - 1), gamma)
    return p


def iterated_frozen(gamma: int) -> tuple[int, int]:
    """The least content at which rounded(p^2, Gamma) is 0 under the iterated clock, and p at the content before."""
    p, c = gamma, 0
    while rounded(p * p, gamma) > 0:
        p = rounded(p * (gamma - 1), gamma)
        c += 1
    # p now at content c (frozen); the pace before it
    before = iterated_clock(gamma, c - 1)
    return c, before


def volume_level(gamma: int, pace: int) -> int:
    """X = ceil(Gamma^(d + 2) / p^(d + 1)), features/volume.volume_of's one division."""
    e = volume.EXPONENT
    return int(division_forward(gamma ** (e + 1) + pace**e - 1, pace**e, 0)[0])


def families_of(den: int, gamma: int, action: int):
    return universe_of({"integers": {"den": den, "node_clock": gamma, "quantum_action": action}})[1]


def predicate(den: int, gamma: int, action: int, unit: int, top: int) -> bool:
    if gamma > den:
        return False
    try:
        fams = families_of(den, gamma, action)
        return derived.amplitude_bound(fams, gamma, action, BITS, unit) >= top
    except ValueError:
        return False


ITERATED_REACH = 20000  # the iterated clock run to the frozen content at Gamma up to this; above it X <= 4 Gamma^3


def top_of(g: int, tops: dict[int, int]) -> int:
    """X(frozen - 1) by the iterated clock at Gamma <= ITERATED_REACH; above it the closed upper bound 4 Gamma^3 (p^2 >= Gamma / 2 at the last pace, so X = ceil(Gamma^5 / p^4) <= 4 Gamma^3, within 1 bit)."""
    if g not in tops:
        if g <= ITERATED_REACH:
            c, p = iterated_frozen(g)
            tops[g] = volume_level(g, p)
        else:
            tops[g] = 4 * g * g * g
    return tops[g]


def bits_only_gamma(den: int, unit: int) -> int:
    """The largest Gamma at which the light line's Rule3 total at A = 4 Gamma^3 stays within 128 bits, den's bound set aside: 3 w A + D A + w + 2 w A + w with w = 6 den Gamma^2 G^2 and D = 2 w."""
    lo, hi = 8, 1 << 40

    def ok(g: int) -> bool:
        a = 4 * g * g * g
        w = int(rule3.wall_of(den, g, unit))
        total = 3 * w * a + 2 * w * a + w + 2 * w * a + w
        return total.bit_length() <= BITS

    while hi - lo > 1:
        mid = int(division_forward(lo + hi, 2, 0)[0])
        if ok(mid):
            lo = mid
        else:
            hi = mid
    return lo


def largest_gamma(den: int, action: int, unit: int, tops: dict[int, int]) -> int:
    """Bisection on Gamma in [8, min(den, the bits-only bound + 1)]: the predicate is monotone (X grows as Gamma^3, A falls with the wall)."""

    def top_of_(g: int) -> int:
        return top_of(g, tops)

    lo, hi = 8, min(den, bits_only_gamma(den, unit) + 1)
    if not predicate(den, lo, action, unit, top_of_(lo)):
        return 0
    if predicate(den, hi, action, unit, top_of_(hi)):
        return hi
    while hi - lo > 1:
        mid = int(division_forward(lo + hi, 2, 0)[0])
        if predicate(den, mid, action, unit, top_of_(mid)):
            lo = mid
        else:
            hi = mid
    return lo


def largest_action(den: int, gamma: int, unit: int, top: int) -> int:
    """Bisection on T in [1, 2^127]: the predicate falls with T (the writes' walls and the sign's numerators carry T)."""
    lo, hi = 1, 1 << 127
    if not predicate(den, gamma, lo, unit, top):
        return 0
    if predicate(den, gamma, hi, unit, top):
        return hi
    while hi - lo > 1:
        mid = int(division_forward(lo + hi, 2, 0)[0])
        if predicate(den, gamma, mid, unit, top):
            lo = mid
        else:
            hi = mid
    return lo


def rule3_total_bits(num: int, den: int, gamma: int, unit: int, bound: int) -> list[int]:
    found = []
    for content in (0, paces.frozen_content(gamma) - 1, -gamma):
        clock, pace = paces.node_paces(gamma, content)
        rule = rule3.rule_integers(num, den, gamma, clock, pace, None, unit)
        total = rule3.flux_total(
            sum(r * (-bound - bound) for r in rule.reaches), rule.mass, rule.wall, bound, -bound
        )
        found.append((abs(int(total)) + int(rule.wall)).bit_length())
    return found


def main() -> None:
    unit = LINK_UNIT
    gamma0, action0 = 1000, 36000
    out: dict[str, object] = {"G": unit, "BITS": BITS}
    # the iterated clock against the engine's exact power
    check = {}
    for gamma in (1000, 6000):
        frozen = paces.frozen_content(gamma)
        c_iter, p_iter = iterated_frozen(gamma)
        reach = 400  # the exact power at the first 400 contents (the running fraction's cost beyond is the 128-bit problem itself), the deepest content alone below
        exact = [paces.clock_alone(gamma, c) for c in range(reach)]
        iter_all = []
        p = gamma
        for c in range(reach):
            iter_all.append(p)
            p = rounded(p * (gamma - 1), gamma)
        differing = sum(1 for a, b in zip(exact, iter_all, strict=True) if a != b)
        largest_gap = max(abs(a - b) for a, b in zip(exact, iter_all, strict=True))
        x_engine = volume_level(gamma, paces.clock_alone(gamma, frozen - 1))  # width_of's own form: the clock by its own power, one division; volume_of's memo to the deepest content is the 128-bit transient itself and is not run here
        check[str(gamma)] = {
            "contents_compared": reach,
            "frozen_engine": frozen,
            "frozen_iterated": c_iter,
            "p0_at_frozen_minus_1_engine": paces.clock_alone(gamma, frozen - 1),
            "p0_at_frozen_minus_1_iterated": p_iter,
            "contents_where_the_two_clocks_differ": differing,
            "largest_difference_in_units": largest_gap,
            "X_engine": x_engine,
            "X_iterated": volume_level(gamma, p_iter),
            "X_bits": x_engine.bit_length(),
            "paces_fraction_bits_at_deepest": (
                2 * gamma * (gamma - 1) ** (frozen - 1) + gamma ** (frozen - 1)
            ).bit_length(),
            "p0_at_content_Gamma_iterated": iterated_clock(gamma, gamma),
            "Gamma_x1000_over_p0_at_Gamma": int(
                division_forward(gamma * 1000, iterated_clock(gamma, gamma), 0)[0]
            ),
        }
    out["iterated_clock_against_engine"] = check
    tops: dict[int, int] = {}
    for den in DENS:
        t0 = time.time()
        row: dict[str, object] = {"den_bits": den.bit_length()}
        fams = families_of(den, gamma0, action0)
        row["rows"] = len(fams)
        row["pairs_num"] = [f.pair[0] for f in fams][:6]
        width = width_of(fams, gamma0, action0, unit)
        bound = derived.amplitude_bound(fams, gamma0, action0, width, unit)
        row["width_engine_at_1000_36000"] = width
        row["A_at_width"] = bound
        row["A_at_128"] = (
            derived.amplitude_bound(fams, gamma0, action0, BITS, unit) if width <= BITS else None
        )
        row["wall_bits"] = int(rule3.wall_of(den, gamma0, unit)).bit_length()
        row["rule3_total_bits_light_at_A_(vac,frozen-1,-Gamma)"] = rule3_total_bits(
            den, den, gamma0, unit, bound
        )
        row["take_common_denominator_bits"] = ((4 * gamma0 * gamma0 * unit * unit) ** (1 + PORTS)).bit_length()
        row["count_unit_light_3denT"] = 3 * den * action0
        row["count_unit_light_bits"] = (3 * den * action0).bit_length()
        row["drift_isqrt_T"] = largest_below(action0)
        row["A1_isqrt_T_div_2"] = largest_below(int(division_forward(action0, 2, 0)[0]))
        row["W_per_quantum_T_div_2"] = int(division_forward(action0, 2, 0)[0])
        sign = [i for i, f in enumerate(fams) if f.held and f.wronskian][0]
        row["alpha_pair_EhT_Gamma_reduced"] = list(
            derived.alpha_of(fams, sign, gamma0, action0)
        )
        # the volume holder's pair at Gamma = den and den + 1
        from event_universe.loader.universe import volume_pair

        row["volume_pair_at_Gamma_den"] = list(volume_pair(den, den))
        row["volume_pair_at_Gamma_den_plus_1"] = list(volume_pair(den, den + 1))
        # the principle
        g_max = largest_gamma(den, action0, unit, tops)
        row["Gamma_max_at_T_36000"] = g_max
        row["Gamma_max_bounded_by_den"] = g_max == den
        row["top_X_at_Gamma_max"] = tops.get(g_max)
        row["top_by_closed_form_4Gamma3"] = g_max > ITERATED_REACH
        t_max_1000 = largest_action(den, gamma0, unit, top_of(gamma0, tops))
        row["T_max_at_Gamma_1000"] = t_max_1000
        row["T_max_at_Gamma_1000_bits"] = t_max_1000.bit_length()
        if g_max:
            t_max_g = largest_action(den, g_max, unit, tops[g_max])
            row["T_max_at_Gamma_max"] = t_max_g
            row["T_max_at_Gamma_max_bits"] = t_max_g.bit_length()
        curve = {}
        for t in (36000, 1 << 30):
            curve[str(t)] = largest_gamma(den, t, unit, tops)
        row["Gamma_max_curve_over_T"] = curve
        # the engine's exact width at the found Gamma_max where feasible (Gamma <= 6000)
        if 0 < g_max <= 6000:
            fams_g = families_of(den, g_max, action0)
            row["width_engine_at_Gamma_max"] = width_of(fams_g, g_max, action0, unit)
            if g_max + 1 <= den:
                try:
                    fams_g1 = families_of(den, g_max + 1, action0)
                    row["width_engine_at_Gamma_max_plus_1"] = width_of(fams_g1, g_max + 1, action0, unit)
                except ValueError as e:
                    row["width_engine_at_Gamma_max_plus_1"] = f"refused: {str(e)[:80]}"
        lo = bits_only_gamma(den, unit)
        row["Gamma_bits_only_light_total_128"] = lo
        row["seconds"] = int(time.time() - t0)
        out[f"den_{den}"] = row
        print(json.dumps({f"den_{den}": row}, indent=1), file=sys.stderr)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
