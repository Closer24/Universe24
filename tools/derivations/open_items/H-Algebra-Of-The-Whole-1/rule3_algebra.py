"""ag1, items (1) and (2): Rule3's step and the paces, derived and measured on the engine's own functions (core/rule3, core/paces,
node.rotate on a 3-cube torus). Integers only. Every check prints PREDICTED then MEASURED and a WORKS / DEPARTS line.

(1a) The flux form identity: w (a_next - 2 a_now + a_before) + r' - r = SUM_j R_j (m_j - a_now) - D a_now, measured on rule3.rule3
     and on Node.rotate against the law's first form (S a_now - w a_before + SUM R m + r, tests/laws.arrivals_rule3) and the
     remainder in [0, w).
(1b) The conserved form to the remainders (the theorem derived in the report): with the weights c_i = L / p_i^2 (L the lcm of the
     distinct p_i^2) and K_ij = c_i R_ij symmetric, F(x, y) = SUM_i c_i [w (x_i^2 + y_i^2) - S_i x_i y_i] - SUM_ij K_ij x_i y_j obeys
     F(a_next, a_now) - F(a_now, a_before) = SUM_i c_i (a_next_i - a_before_i) (r_i - r'_i) exactly.
(1c) The inverse: rotate at -1 returns (a_now, a_before, r) bit for bit; carried_division at -1 on random totals.
(1d) The one rule of the remainder: the mirror w - 1 - r is the ones' complement, floor((w - 1 - u) / w) = -floor(u / w) for every u;
     two mirrors the identity; the odd rounding equals sign(x) rounded(|x|) at every x in a range; the two's complement w - r fails
     exactly where w divides u.
(2a) The clock p_0(c) against the exact power rounded half up, (2 Gamma (Gamma - 1)^c + Gamma^c) div (2 Gamma^c), at every content
     whose oracle fits 128 bits; (2b) the Link's pace p_a = rounded(p_0^2, Gamma) at every content to the frozen one; the frozen content;
     (2c) the clock's certificate (no undecided content).
"""

from __future__ import annotations

import random
import sys
import time

import numpy as np

sys.set_int_max_str_digits(0)

from event_universe.core import paces, rule3  # noqa: E402
from event_universe.core.ports import PORTS, across  # noqa: E402
from event_universe.core.rule3 import carried_division, mirrored, rule_integers  # noqa: E402
from event_universe.rows import Line  # noqa: E402


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def report(name: str, predicted: object, measured: object) -> bool:
    ok = predicted == measured
    print(f"{name}: PREDICTED {predicted} MEASURED {measured} -> {'WORKS' if ok else 'DEPARTS'}")
    return ok


def first_form(reaches, arrivals, s, w, now, before, rem):
    total = sum(r * m for r, m in zip(reaches, arrivals, strict=True)) + s * now - w * before
    return carried_division(total, w, rem, 1)


def flux_form(reaches, arrivals, mass, w, now, before, rem):
    flux = sum(r * (m - now) for r, m in zip(reaches, arrivals, strict=True))
    return rule3.rule3(flux, mass, w, now, before, rem, 1)


def check_1a(rng: random.Random, den: int, gamma: int, num: int, trials: int) -> bool:
    unit = rule3.link_unit_of(gamma)
    ok = True
    for _ in range(trials):
        c = rng.randint(0, 2000)
        clock, pace = paces.clock(gamma, c), paces.link_pace(gamma, c)
        factors = tuple(rule3.link_factor(gamma, unit, rng.randint(0, gamma // 4)) for _ in range(PORTS))
        r = rule_integers(num, den, gamma, clock, pace, factors, unit)
        now, before = rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)
        arrivals = [rng.randint(-10**6, 10**6) for _ in range(PORTS)]
        rem = rng.randint(0, r.wall - 1)
        a = first_form(r.reaches, arrivals, r.self_coefficient, r.wall, now, before, rem)
        b = flux_form(r.reaches, arrivals, r.mass, r.wall, now, before, rem)
        nxt, rem2 = b
        # the identity's two sides as integers
        left = r.wall * (nxt - 2 * now + before) + rem2 - rem
        right = sum(rr * (m - now) for rr, m in zip(r.reaches, arrivals, strict=True)) - r.mass * now
        ok = ok and a == b and left == right and 0 <= rem2 < r.wall
        # the own weight identity S = 2 w - D - SUM R
        ok = ok and r.self_coefficient == 2 * r.wall - r.mass - sum(r.reaches)
        # the inverse of the carried division
        back2 = rule3.rule3(
            sum(rr * (m - now) for rr, m in zip(r.reaches, arrivals, strict=True)),
            r.mass,
            r.wall,
            now,
            nxt,
            rem2,
            -1,
        )
        ok = ok and back2 == (before, rem)
    return ok


def torus_rows(rng: random.Random, shape, bound: int, wall: int, lines: int = 1) -> list[Line]:
    found = []
    for _ in range(lines):
        now = np.array([rng.randint(-bound, bound) for _ in range(27)], dtype=object).reshape(shape)
        before = np.array([rng.randint(-bound, bound) for _ in range(27)], dtype=object).reshape(shape)
        rem = np.array([rng.randint(0, wall - 1) for _ in range(27)], dtype=object).reshape(shape)
        found.append(Line(now, before, rem, wall))
    return found


class Rotator:
    """A bare rotate of node.py's text over arrays (no Node built: no file), the same function body."""

    def __init__(self) -> None:
        self.max_transient = 0

    def arrivals(self, at, r):
        totals = [0] * len(at)
        for port, reach in enumerate(r.reaches):
            found = [across(a, port) for a in at]
            totals = [t + reach * m for t, m in zip(totals, found, strict=True)]
        return totals


def check_1b_1c(rng: random.Random, den: int, gamma: int, num: int, trials: int) -> tuple[bool, bool]:
    """The weighted conserved form's change against the remainders' sum, and rotate's inverse, by node.Node.rotate itself."""
    from event_universe.node import Node

    unit = rule3.link_unit_of(gamma)
    shape = (3, 3, 3)
    ok_form = ok_inv = True
    for t in range(trials):
        # two distinct contents over the board, so the paces differ Node by Node (the weights 1 / p_i^2 are not one)
        contents = np.array([rng.choice([0, 7]) for _ in range(27)], dtype=object).reshape(shape)
        clocks = paces.clock_of(gamma, contents)
        pace = paces.link_pace_of(gamma, contents)
        # one symmetric Link factor per Link: read the same from both ends (a tension per Link at random)
        tension = [np.array([rng.randint(0, gamma // 5) for _ in range(27)], dtype=object).reshape(shape) for _ in range(3)]
        factors = []
        for port in range(PORTS):
            axis, side = divmod(port, 2)
            # the Link toward +axis belongs to the Node; the Link toward -axis is the neighbour's +axis Link
            tt = tension[axis] if side == 0 else across(tension[axis], port)
            factors.append(np.vectorize(lambda x: int(rule3.link_factor(gamma, unit, int(x))), otypes=[object])(tt))
        r = rule_integers(num, den, gamma, clocks, pace, tuple(factors), unit)
        lines = torus_rows(rng, shape, 4000, r.wall)
        held = [line.copy() for line in lines]
        node = Node.__new__(Node)
        node.max_transient = 0
        node.X, node.gamma = 0, gamma
        stepped = Node.rotate(node, lines, r, None, 1, None, None)
        # (1b) the weighted form
        p2 = {int(x) for x in (pace * pace).reshape(-1)}
        L = 1
        for v in p2:
            L = lcm(L, v)
        c = np.vectorize(lambda v: L // int(v), otypes=[object])(pace * pace)

        def form(x, y):
            own = c * (r.wall * (x * x + y * y) - r.self_coefficient * x * y)
            link = 0
            for port, reach in enumerate(r.reaches):
                link = link + c * reach * x * across(y, port)
            return int(np.sum(own - link))

        f0 = form(held[0].now, held[0].before)
        f1 = form(stepped[0].now, stepped[0].before)
        drift = int(np.sum(c * (stepped[0].now - held[0].before) * (held[0].rem - stepped[0].rem)))
        ok_form = ok_form and (f1 - f0 == drift)
        if t == 0:
            print(f"  (1b) sample: F before {f0} F after {f1} change {f1 - f0} the remainders' sum {drift}; bits of F {f0.bit_length()}")
            # the symmetry K_ij = K_ji checked on every Link
            sym = True
            for axis in range(3):
                kp = c * r.reaches[2 * axis]
                km = across(c * r.reaches[2 * axis + 1], 2 * axis)
                sym = sym and bool(np.all(kp == km))
            print(f"  (1b) K_ij = K_ji on every Link: {sym}; distinct p_i^2: {sorted(p2)}; L bits {L.bit_length()}")
        # (1c) the inverse by rotate at -1
        back = Node.rotate(node, stepped, r, None, -1, None, None)
        same = all(
            bool(np.all(a.now == b.now)) and bool(np.all(a.before == b.before)) and bool(np.all(a.rem == b.rem))
            for a, b in zip(back, held, strict=True)
        )
        ok_inv = ok_inv and same
    return ok_form, ok_inv


def check_1d(rng: random.Random) -> bool:
    ok = True
    for _ in range(2000):
        w = rng.randint(2, 10**9)
        u = rng.randint(-10**12, 10**12)
        r = rng.randint(0, w - 1)
        ok = ok and ((w - 1 - u) // w == -(u // w))
        ok = ok and mirrored(mirrored(r, w, 1), w, 1) == r and mirrored(r, w, 1) == w - 1 - r
        ok = ok and mirrored(r, w, 2) == r
    # the two's complement w - r fails exactly where w divides u
    twos_fail = twos_fail_div = 0
    for _ in range(2000):
        w = rng.randint(2, 1000)
        u = rng.randint(-10**6, 10**6)
        if ((w - u) % w) != (w - (u % w)) % w or (-(u // w)) != ((w - u) // w):
            twos_fail += 1
            twos_fail_div += (u % w == 0)
    ok = ok and twos_fail == twos_fail_div
    print(f"  (1d) the two's complement parts from the mirror at {twos_fail} of 2000 u, every one with w | u: {twos_fail == twos_fail_div}")
    # the odd rounding
    odd_ok = True
    for wall in (1, 2, 3, 7, 1000, 36000):
        for x in range(-5 * wall - 3, 5 * wall + 4):
            s = 1 if x >= 0 else -1
            odd_ok = odd_ok and int(paces.odd_rounded(x, wall)) == s * int(paces.rounded(s * x, wall))
            odd_ok = odd_ok and int(paces.odd_rounded(-x, wall)) == -int(paces.odd_rounded(x, wall))
    print(f"  (1d) odd_rounded(x) = sign(x) rounded(|x|) and odd at every x over six walls: {odd_ok}")
    return ok and odd_ok


def check_2(gamma: int) -> tuple[bool, bool, int, int]:
    """The clock against the exact power where the oracle fits 128 bits; the Link's pace the clock twice; the frozen content."""
    ok_clock = True
    last = 0
    for c in range(0, 400):
        oracle_num = 2 * gamma * (gamma - 1) ** c + gamma**c
        if oracle_num.bit_length() > 128:
            break
        last = c
        exact = oracle_num // (2 * gamma**c)
        ok_clock = ok_clock and paces.clock(gamma, c) == exact
    frozen = paces.frozen_content(gamma)
    ok_link = True
    for c in range(0, frozen + 1):
        p0 = paces.clock(gamma, c)
        ok_link = ok_link and paces.link_pace(gamma, c) == int(paces.rounded(p0 * p0, gamma))
    ok_link = ok_link and paces.link_pace(gamma, frozen) == 0 and paces.link_pace(gamma, frozen - 1) > 0
    ok_link = ok_link and paces.clock(gamma, frozen) ** 2 < (gamma + 1) // 2 + 1
    return ok_clock, ok_link, last, frozen


def main() -> None:
    t0 = time.monotonic_ns()
    rng = random.Random(24)
    den, gamma = 15162856759112389, 1000
    nums = [den, 15162854575528411, 2458210083751875, den - den // gamma]
    all_ok = True
    print("== (1a) the flux form identity, the own weight, the remainder's range, the inverse of the division ==")
    for num in nums:
        ok = check_1a(rng, den, gamma, num, 300)
        all_ok = report(f"(1a) num {num}: first form == flux form, identity, 0 <= r' < w, inverse, 300 trials", True, ok) and all_ok
    print("== (1b) the weighted conserved form to the remainders, (1c) rotate's inverse, 3-cube torus, two contents, tensions ==")
    # the toy den 1,021 = 30^2 + 11^2 with its one circle point (779, 660), so every integer of the form stays within 128 bits
    for num in (1021, 779, 1020):
        ok_form, ok_inv = check_1b_1c(rng, 1021, gamma, num, 12)
        all_ok = report(f"(1b) num {num}: F(next, now) - F(now, before) == SUM c_i (next - before)(r - r'), 12 boards", True, ok_form) and all_ok
        all_ok = report(f"(1c) num {num}: rotate at -1 returns the start bit for bit, 12 boards", True, ok_inv) and all_ok
    print("== (1d) the one rule of the remainder ==")
    all_ok = report("(1d) the ones' complement commutes with the floor; two mirrors the identity; the odd rounding", True, check_1d(rng)) and all_ok
    print("== (2) the paces ==")
    ok_clock, ok_link, last, frozen = check_2(gamma)
    all_ok = report(f"(2a) p_0(c) == (2 Gamma (Gamma-1)^c + Gamma^c) div (2 Gamma^c) for c in 0..{last} (the oracle within 128 bits)", True, ok_clock) and all_ok
    all_ok = report(f"(2b) p_a(c) == rounded(p_0^2, Gamma) for c in 0..{frozen}; p_a(frozen) == 0 and p_a(frozen - 1) > 0", True, ok_link) and all_ok
    print(f"  (2b) frozen content at Gamma {gamma}: {frozen}; p_0 there {paces.clock(gamma, frozen)}; p_a one below {paces.link_pace(gamma, frozen - 1)}")
    certified = paces.certified(gamma)
    all_ok = report("(2c) certified(Gamma) returns the frozen content with no undecided content", frozen, certified) and all_ok
    print(f"VERDICT items (1) and (2): {'WORKS' if all_ok else 'DEPARTS'}; seconds {(time.monotonic_ns() - t0) // 10**9}")


if __name__ == "__main__":
    main()
