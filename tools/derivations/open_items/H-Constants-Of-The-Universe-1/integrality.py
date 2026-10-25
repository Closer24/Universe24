"""Hand k1, brief k, the Addition: what den, Gamma, T and G must be so that every division the law calls exact leaves the remainder 0, measured on the engine's primitives and the loader.

Derived conditions (the report's section 2b): the exact bands 6 and 3 need 2 | den (num = den div 2 a point); the half wall's move
w (X_now - X_before) div 2 is exact for every (den, Gamma, G) since 6 | w; the odd rounding at the wall Gamma meets a tie only where
Gamma is even (2 x = Gamma mod 2 Gamma needs Gamma even), so Gamma odd leaves no tie in the turn's factor and the Link's pace;
the clock's own rounding never meets a tie for Gamma > 2 (Gamma^(c - 1) | 2 (Gamma - 1)^c is impossible); the Link's factor
Q = G^2 (Gamma - t)^2 / Gamma^2 is exact at every tension iff Gamma | G (G = Gamma the least); the Wronskian per quantum W = T div 2
is a lay's A^2 exactly iff T = 2 A^2; the drift's share is one quantum exactly iff T is a square (the two never together);
the sign holder's alpha T / Gamma is an integer iff Gamma | T; the volume holder's rest is the clock's level exactly iff Gamma | den;
the take's quotient den / s at a lift is never an integer (s = 2 a b den / p with p odd), the take's remainder the law's own.

    PYTHONPATH=src python tools/derivations/open_items/H-Constants-Of-The-Universe-1/integrality.py > tools/derivations/open_items/H-Constants-Of-The-Universe-1/integrality.out
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import largest_below, link_factor, wall_of  # noqa: E402
from event_universe.loader.circle import lift_points  # noqa: E402
from event_universe.loader.rooms import width_of  # noqa: E402
from event_universe.loader.universe import universe_of  # noqa: E402

BITS = 128


def ties() -> None:
    print("== the odd rounding's ties: turn_factor(angle, p_0, Gamma) = odd_rounded(angle p_0, Gamma); a tie where 2 angle p_0 = Gamma mod 2 Gamma ==")
    for gamma in (1000, 1001, 6000, 6001):
        p0 = gamma - 1
        tied = sum(1 for angle in range(-5000, 5001) if (2 * angle * p0 - gamma) % (2 * gamma) == 0)
        frozen = paces.frozen_content(gamma)
        link_ties = sum(1 for c in range(frozen) if (2 * paces.clock_alone(gamma, c) ** 2 - gamma) % (2 * gamma) == 0)
        clock_ties = sum(1 for c in range(1, 400) if (2 * gamma * (gamma - 1) ** c - gamma**c) % (2 * gamma**c) == 0)
        q_ties = sum(1 for t in range(0, gamma + 1) if (2 * 256 * (gamma - t) ** 2 - gamma * gamma) % (2 * gamma * gamma) == 0)
        print(f"Gamma {gamma} ({'even' if gamma % 2 == 0 else 'odd'}): turn ties over angles [-5000, 5000] at p_0 = Gamma - 1: {tied}; Link's pace rounding ties over c in [0, {frozen}): {link_ties}; clock's rounding ties over c in [1, 400): {clock_ties}; Q's ties at G 16 over t in [0, Gamma]: {q_ties}")


def link_exactness() -> None:
    print("== the Link's factor exact (no rounding) at every tension iff Gamma | G ==")
    for gamma in (1000, 1001):
        for unit in (16, 32, gamma, 2 * gamma):
            exact = sum(1 for t in range(0, gamma + 1) if (unit * unit * (gamma - t) ** 2) % (gamma * gamma) == 0)
            check = all(link_factor(gamma, unit, t) * gamma * gamma == unit * unit * (gamma - t) ** 2 for t in range(0, gamma + 1)) if gamma % unit == 0 or unit % gamma == 0 else None
            print(f"Gamma {gamma} G {unit}: tensions t in [0, Gamma] with Q exact: {exact} of {gamma + 1}; Gamma | G: {unit % gamma == 0}; link_factor exact everywhere: {check}")


def walls_and_pairs() -> None:
    print("== the walls, the half wall, the pairs ==")
    for den in (10, 1021, 2042, 348893, 697786, 1655909141, 3311818282):
        for gamma in (1000, 1001):
            for unit in (16, gamma):
                w = wall_of(den, gamma, unit)
                print(f"den {den} Gamma {gamma} G {unit}: w = 6 den Gamma^2 G^2 = {w} ({w.bit_length()} bits), w mod 2 = {w % 2} (the half wall's move exact: {w % 2 == 0}), w mod 12 = {w % 12}; den mod Gamma = {den % gamma} (the volume holder's rest exactly 1/Gamma: {den % gamma == 0}), volume pair ({den - den // gamma}, {den})")
    for action in (36000, 32768, 35912, 36100, 18, 50, 2 * 1001 * 1001):
        half = action // 2
        a = largest_below(half)
        v = largest_below(action)
        print(f"T {action}: T even {action % 2 == 0}; T div 2 = {half} a square: {a * a == half} (A = {a}, short {half - a * a}); T a square: {v * v == action} (drift {v}, short {action - v * v}); T mod 1000 = {action % 1000}, T mod 1001 = {action % 1001}, T mod 12 = {action % 12}")
    print("== the take's quotient at a lift: den / s with s = 2 a b den / p, never an integer (p odd) ==")
    for den in (10, 1021, 2042, 348893, 1655909141, 15162856759112389):
        for vector, num, s in lift_points(den):
            print(f"den {den} lift {vector}: s = {s}, den mod s = {den % s}, den div s = {den // s} (3 T s | 3 den T iff den mod s = 0: {den % s == 0}); 6 den (T div 2) at T 36000 over 3 T s: {(6 * den * 18000) // (3 * 36000 * s)} rem {(6 * den * 18000) % (3 * 36000 * s)}")


def loader_sets() -> None:
    print("== the loader on integral sets: den even with a lift, Gamma odd, T = 2 Gamma^2 (A = Gamma, Gamma | T), G = Gamma ==")
    for den, gamma, action, unit in ((10, 3, 18, 3), (10, 5, 50, 5), (10, 15, 450, 15), (10, 101, 2 * 101 * 101, 101), (2042, 1001, 2 * 1001 * 1001, 1001), (2042, 1001, 36036, 16), (3311818282, 1001, 2 * 1001 * 1001, 1001), (3311818282, 1001, 36036, 16)):
        t0 = time.time()
        try:
            families = universe_of({"integers": {"den": den, "node_clock": gamma, "quantum_action": action}})[1]
            width = width_of(families, gamma, action, unit)
            print(f"den {den} Gamma {gamma} T {action} G {unit}: families {len(families)}, width {width} bits (within {BITS}: {width <= BITS}), w {wall_of(den, gamma, unit).bit_length()} bits, A = isqrt(T div 2) = {largest_below(action // 2)} ({time.time() - t0:.1f} s)")
        except ValueError as refusal:
            print(f"den {den} Gamma {gamma} T {action} G {unit}: REFUSED by the loader: {str(refusal)[:200]}")
    print("== the largest odd Gamma within 128 bits with T = 2 Gamma^2 and G = Gamma, at den 2042 and 3311818282 ==")
    for den in (2042, 3311818282):
        def fits(gamma: int) -> bool:
            try:
                families = universe_of({"integers": {"den": den, "node_clock": gamma, "quantum_action": 2 * gamma * gamma}})[1]
                return width_of(families, gamma, 2 * gamma * gamma, gamma) <= BITS
            except ValueError:
                return False
        low, high = 3, 5
        while fits(high):
            low, high = high, 2 * high + 1
        while high - low > 2:
            middle = (low + high) // 2
            middle += (middle % 2 == 0)
            if middle >= high:
                middle -= 2
            if fits(middle):
                low = middle
            else:
                high = middle
        print(f"den {den}: the largest odd Gamma with T = 2 Gamma^2, G = Gamma within {BITS} bits: {low} (T = {2 * low * low}, w bits {wall_of(den, low, low).bit_length()}); next odd {low + 2} fits: {fits(low + 2)}")


if __name__ == "__main__":
    ties()
    link_exactness()
    walls_and_pairs()
    loader_sets()
