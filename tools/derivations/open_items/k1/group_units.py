"""Hand k1, brief k, parts (a) and (b)(i): the four constants in the group's terms, measured on the engine's primitives.

den: the modulus of the integer rotations, Z[i] modulo den; its circle's points and lifts (loader/circle), the gap g of each
lift as an integer quotient at the scale 1000, the exact bands' closure (2 cos omega_0 in {1, 0, -1}: the pairs
[den div 2, den], [0, den], [-(den div 2), den]) under Rule3's own line (core/rule3.rule3) with the remainder read.
Gamma: the identity of the paces' group law, p_0(c_1 + c_2) = p_0(c_1) p_0(c_2) / Gamma (core/paces.clock_alone),
measured as the defect of the composition in the integers, and the clock's half-life in levels (the resolution).
T: the unit of the symplectic area: the lay at (den, den) with A = isqrt(T div 2), W = A^2 = T div 2 per quantum
(core/rule3.largest_below), the drift isqrt(T) (seed.drift_of).
G: the Link's rounding unit: the Link's factor Q(t) = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2 (core/rule3.link_factor)
exact at t = 0 for every G; the least tension that moves Q by one unit (the tension's resolution Gamma / (2 G^2)); the least G
at which one level of tension is resolved; the turn's factor (core/paces.turn_factor) at the vacuum's clock, G-free; the sign's
Link pair (plane.sign_pairs) exact at n = 0 for every G and the count of n in [1, 4 Gamma] at which it is exact.

    PYTHONPATH=src python tools/derivations/k1/group_units.py > tools/derivations/k1/group_units.out
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import largest_below, link_factor, rule3, rule_integers, wall_of  # noqa: E402
from event_universe.loader.circle import circle_points, factors, lift_points, two_squares  # noqa: E402
from event_universe.plane import sign_pairs  # noqa: E402

DENS = (1021, 348893, 1655909141, 4471099877, 15162856759112389)
GAMMAS = (1000, 6000)
UNITS = (1, 2, 4, 8, 16, 32, 64)


def quot(num: int, den: int, scale: int = 1000) -> str:
    q, r = divmod(num * scale, den)
    return f"{q}/{scale} rem {r}" if r else f"{q}/{scale}"


def den_structure() -> None:
    print("== den: the modulus of the integer rotations (Z[i] modulo den), its circle and its lifts ==")
    for den in DENS:
        t0 = time.time()
        primes = factors(den)
        points = circle_points(den)
        lifts = lift_points(den)
        print(f"den {den} ({den.bit_length()} bits): primes {primes}; circle points in the open quadrant {len(points)}; lifts {len(lifts)}; parity {'even' if den % 2 == 0 else 'odd'}")
        for vector, num, sine in lifts:
            g_num, g_den = den - num, den  # g = (den - num) / den
            print(f"  lift {vector}: num {num} s {sine} g {quot(g_num, g_den)} sin {quot(sine, den)} (s^2 + num^2 - den^2 = {sine * sine + num * num - den * den})")
        legs = {p: two_squares(p) for p in primes if p % 4 == 1}
        for p, (a, b) in legs.items():
            hi, lo = max(a, b), min(a, b)
            print(f"  prime {p} = {hi}^2 + {lo}^2: lift g = 2 b^2 / p = {quot(2 * lo * lo, p)}, sin = 2 a b / p = {quot(2 * hi * lo, p)}")
        if len(lifts) >= 2:
            sines = sorted(s for _v, _n, s in lifts)
            print(f"  mass ratio heaviest / lightest lift = {sines[-1] // sines[0]} rem {sines[-1] % sines[0]} (sin_h / sin_l)")
        print(f"  ({time.time() - t0:.1f} s)")


def exact_bands() -> None:
    print("== the exact bands: 2 cos omega_0 = 2 num / den in {1, 0, -1}, the periods 6, 4, 3, under Rule3's line at a uniform level (flux 0) ==")
    print("a Node whose six neighbours stand at its own level: a_next = (w (2 a_now - a_before) - D a_now + r) div w; closure when the state returns with the remainder it started from")
    for den_base in (1021, 348893):
        for den in (den_base, 2 * den_base):
            for gamma in GAMMAS:
                for unit in (1, 16, 64):
                    for num, name in ((den // 2, "[den div 2, den] (6)"), (0, "[0, den] (4)"), (-(den // 2), "[-(den div 2), den] (3)")):
                        rule = rule_integers(num, den, gamma, gamma, gamma, None, unit)
                        wall = wall_of(den, gamma, unit)
                        start = (1000, 0, wall // 2)
                        now, before, rem = start
                        period = None
                        for k in range(1, 13):
                            nxt, rem = rule3(0, rule.mass, rule.wall, now, before, rem, 1)
                            now, before = nxt, now
                            if (now, before, rem) == start:
                                period = k
                                break
                        exact = (2 * num) % den == 0
                        print(f"den {den} Gamma {gamma} G {unit} pair {name}: D/w = {2 * (den - num)}/{den}; 2 cos integer: {exact}; closure period {period}; remainder after 12: {rem} (start {wall // 2}, wall {wall})")


def gamma_identity() -> None:
    print("== Gamma: the identity of the paces' group law, p_0(c_1 + c_2) Gamma = p_0(c_1) p_0(c_2) in the rationals; the integers' defect ==")
    for gamma in GAMMAS:
        worst = 0
        pairs = ((1, 1), (10, 20), (100, 200), (300, 300), (-50, 50), (-100, 300), (600, 600))
        for c1, c2 in pairs:
            a, b, ab = paces.clock_alone(gamma, c1), paces.clock_alone(gamma, c2), paces.clock_alone(gamma, c1 + c2)
            composed = paces.rounded(a * b, gamma)
            defect = composed - ab
            worst = max(worst, abs(defect))
            print(f"Gamma {gamma}: p_0({c1}) = {a}, p_0({c2}) = {b}, rounded(p_0({c1}) p_0({c2}), Gamma) = {composed}, p_0({c1 + c2}) = {ab}, defect {defect}")
        half = 0
        while 2 * paces.clock_alone(gamma, half) > gamma:
            half += 1
        frozen = paces.frozen_content(gamma)
        print(f"Gamma {gamma}: identity p_0(0) = {paces.clock_alone(gamma, 0)}; the clock's half-life {half} levels (the least c with 2 p_0(c) <= Gamma); the Link's zero at content {frozen}; largest composition defect {worst} unit(s)")
        c = frozen - 1
        print(f"Gamma {gamma}: the paces' exact fraction at the deepest admitted content c = {c}: (Gamma - 1)^c has {((gamma - 1) ** c).bit_length()} bits, Gamma^(c - 1) has {(gamma ** (c - 1)).bit_length()} bits (the memo's transient); the clock there {paces.clock_alone(gamma, c)}, the Link's pace {paces.rounded(paces.clock_alone(gamma, c) ** 2, gamma)}")


def t_area() -> None:
    print("== T: the unit of the symplectic area, A = isqrt(T div 2), W = A^2 = T div 2 per quantum to the rounding; the drift isqrt(T) ==")
    for action in (36000, 32768, 2 * 134 * 134, 2 * 135 * 135):
        half = action // 2
        a = largest_below(half)
        print(f"T {action}: T div 2 = {half}, A = isqrt(T div 2) = {a}, A^2 = {a * a} (short of T div 2 by {half - a * a}), drift isqrt(T) = {largest_below(action)}, 3 den T at den 1021 = {3 * 1021 * action}")


def g_unit() -> None:
    print("== G: the Link's rounding unit ==")
    for gamma in GAMMAS:
        for unit in UNITS:
            q0 = link_factor(gamma, unit, 0)
            t = 0
            while link_factor(gamma, unit, t) == unit * unit:
                t += 1
            step = 0
            while link_factor(gamma, unit, step) > unit * unit - 1:
                step += 1
            t_one = link_factor(gamma, unit, 1)
            tie = (gamma * gamma) % 2
            print(f"Gamma {gamma} G {unit}: Q(0) = {q0} (= G^2: {q0 == unit * unit}); Q(1) = {t_one} (one level resolved: {t_one != unit * unit}); least t with Q != G^2: {t}; Gamma / (2 G^2) = {quot(gamma, 2 * unit * unit)} levels per unit of Q; Gamma^2 odd (a half tie possible): {tie}")
        least = 1
        while link_factor(gamma, least, 1) == least * least:
            least *= 2
        print(f"Gamma {gamma}: the least power of two G that resolves one level of tension: {least} (2 G^2 = {2 * least * least} >= Gamma: {2 * least * least >= gamma}); 2^4 = 16 resolves one level: {link_factor(gamma, 16, 1) != 256}")
        for angle in (1, -1, 7, -7, 1000, -1000):
            print(f"Gamma {gamma}: turn_factor({angle}, p_0 = Gamma, Gamma) = {paces.turn_factor(angle, gamma, gamma)} (G enters nowhere; exact: {paces.turn_factor(angle, gamma, gamma) == angle})")
        for unit in (1, 16, 64):
            wall = 4 * gamma
            exact_n = 0
            for n in range(0, wall + 1):
                even, odd = sign_pairs((gamma, gamma), gamma, (unit * unit,), (n,))
                x = 2 * gamma * unit * unit
                circle = wall * wall + n * n
                if (x * (wall * wall - n * n)) % circle == 0 and (x * 2 * wall * n) % circle == 0:
                    exact_n += 1
            even0, odd0 = sign_pairs((gamma, gamma), gamma, (unit * unit,), (0,))
            print(f"Gamma {gamma} G {unit}: the sign's Link pair at n = 0: ({even0[0]}, {odd0[0]}) = (2 num G^2, 0) exact: {even0[0] == 2 * gamma * unit * unit and odd0[0] == 0}; n in [0, 4 Gamma] with both parts exact (no rounding): {exact_n} of {wall + 1}")


if __name__ == "__main__":
    den_structure()
    exact_bands()
    gamma_identity()
    t_area()
    g_unit()
