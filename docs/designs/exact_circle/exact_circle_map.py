"""The exact circle: the click's weight as an element of the real cyclotomic
ring, in integers (exact-circle-v1, docs/designs/exact_circle/DESIGN.md).

A host map of the design, not a run: every number of the design's sections
1, 2 and 4 is printed here from integers and fractions. The real embedding
(the value of cos(2 pi d / N) as a number) is used only in the CHECKS, at
60 decimal digits through `decimal`, to confirm the integer identities;
no float enters a number of the design.
"""

from __future__ import annotations

import random
from decimal import Decimal, getcontext
from fractions import Fraction

from event_universe.core.phase import phase_cosines, phase_sines

getcontext().prec = 60
OUT: list[str] = []


def say(line: str = "") -> None:
    OUT.append(line)


# -- the minimal polynomial of theta = 2 cos(2 pi / N), N a power of two ----


def dickson(d: int) -> list[int]:
    """P_d(t) with 2 cos(d a) = P_d(2 cos a): P_0 = 2, P_1 = t,
    P_(d+1) = t P_d - P_(d-1); integer coefficients, monic for d >= 1."""
    prev, cur = [2], [0, 1]
    if d == 0:
        return prev
    for _ in range(d - 1):
        shifted = [0] + cur
        nxt = [shifted[i] - (prev[i] if i < len(prev) else 0) for i in range(len(shifted))]
        prev, cur = cur, nxt
    return cur


def two_cos(d: int, n: int) -> Decimal:
    """2 cos(2 pi d / n) at 60 digits: the nested square root of the
    power of two, then the Dickson recurrence; a check value only."""
    # theta_k = 2 cos(2 pi / 2^k): theta_2 = 0, theta_(k+1) = sqrt(2 + theta_k)
    k = n.bit_length() - 1
    theta = Decimal(0)
    for _ in range(k - 2):
        theta = (Decimal(2) + theta).sqrt()
    prev, cur = Decimal(2), theta
    if d == 0:
        return prev
    for _ in range(d - 1):
        prev, cur = cur, theta * cur - prev
    return cur


def section_1(n: int) -> None:
    half = n // 2
    quarter = n // 4
    say(f"(1) N = {n}: the real subring Z[theta], theta = 2 cos(2 pi / N)")
    psi = dickson(quarter)
    if n <= 64:
        say(f"  the minimal polynomial Psi_N(t) = P_(N/4)(t), degree {len(psi) - 1}, coefficients {psi}")
    else:
        say(
            f"  the minimal polynomial Psi_N(t) = P_(N/4)(t), degree {len(psi) - 1}, "
            f"the largest coefficient {max(abs(c) for c in psi).bit_length()} bits (not printed)"
        )
    if n <= 64:
        value = sum(Decimal(c) * two_cos(1, n) ** i for i, c in enumerate(psi))
        say(f"  check: Psi_N(theta) at 60 digits = {value:.3e} (zero to the digits kept)")
    else:
        say(
            "  check of Psi_N(theta): not made, the cancellation at this degree needs more than 60 digits"
        )
    say(
        f"  the basis: 1 and 2 cos(d a) for d = 1 .. {quarter - 1} (a = 2 pi / N): {quarter} integers per element"
    )
    say("  the reduction of every cos(d a), d in Z_N, to the basis by the circle's symmetries alone:")
    say("    cos((N/2 - d) a) = -cos(d a), cos((N/4) a) = 0, cos((N - d) a) = cos(d a)")
    # the weight w = sum_d c_d cos(d a) with c the autocorrelation (c_d = c_(N-d))
    say(
        "  the weight w = sum over d in Z_N of c_d cos(d a), c_d = sum_j f_j f_(j+d) (the autocorrelation):"
    )
    say(
        "    e_0 = c_0 - c_(N/2),  e_d = 2 (c_d - c_(N/2 - d)) for d = 1 .. N/4 - 1,  w = e_0 + sum_d e_d cos(d a)"
    )
    # check on random vectors
    rng = random.Random(64)
    worst = Decimal(0)
    trials = 20 if n <= 64 else 2
    for _ in range(trials):
        f = [rng.randint(0, 40) if rng.random() < (0.3 if n <= 64 else 0.01) else 0 for _ in range(n)]
        c = [sum(f[j] * f[(j + d) % n] for j in range(n)) for d in range(n)]
        e = [c[0] - c[half]] + [2 * (c[d] - c[half - d]) for d in range(1, quarter)]
        exact = e[0] + sum(Decimal(e[d]) * two_cos(d, n) / 2 for d in range(1, quarter))
        x = sum(Decimal(f[j]) * two_cos(j, n) / 2 for j in range(n))
        y = sum(Decimal(f[j]) * (two_cos((j - quarter) % n, n) / 2) for j in range(n))
        direct = x * x + y * y
        worst = max(worst, abs(exact - direct))
    say(f"  check: on {trials} random phase-count vectors |e . cos - (X^2 + Y^2)| at most {worst:.1e}")
    say(
        "  the coefficients' size: |e_d| <= 2 sum_j f_j^2 <= 2 (sum_j f_j)^2 = 2 A^2, A the summed amplitude 32 x amount"
    )
    say()


def section_2(n: int) -> None:
    quarter = n // 4
    degree = quarter
    say(
        f"(2) the sign of an element x = sum e_d 2cos(d a) (an algebraic integer of degree {degree}) at N = {n}"
    )
    say(
        f"  x = 0 exactly iff every e_d = 0 (the basis is a basis); otherwise |N(x)| >= 1 over the {degree} conjugates,"
    )
    say(f"  each conjugate at most 2 sum_d |e_d| in size, so |x| >= (2 sum_d |e_d|)^-({degree - 1})")
    for log_a in (10, 20, 25):
        s = 2 * (1 << (2 * log_a))  # 2 A^2 with A = 2^log_a
        bits = (degree - 1) * (2 * s).bit_length() + 2
        say(
            f"  A = 2^{log_a} (sum |e_d| <= 2 A^2 = 2^{2 * log_a + 1}): the precision that decides the sign, {bits} bits"
        )
    say(
        "  the rung: u < b_k  iff  2 W C_k - (2 u + 1) T >= 0, one element of the ring (C_k, T cumulative weights);"
    )
    say(
        "  the vector of its coefficients is exact (additions), equality is the zero vector, the sign as above."
    )
    say()


def section_4_tables(n: int) -> None:
    say(f"(4) the tables at 1/256 against the exact circle, N = {n}")
    cos_t, sin_t = phase_cosines(n), phase_sines(n)
    worst_c = Fraction(0)
    worst_sq = (10**9, -(10**9))
    for d in range(n):
        exact = two_cos(d, n) / 2 * 256
        err = abs(Decimal(cos_t[d]) - exact)
        worst_c = max(worst_c, Fraction(str(err)))
        sq = cos_t[d] ** 2 + sin_t[d] ** 2
        worst_sq = (min(worst_sq[0], sq), max(worst_sq[1], sq))
    say(
        f"  |C_d - 256 cos(d a)| at most {float(worst_c):.4f} (<= 1/2 by the rounding); C_d^2 + S_d^2 from {worst_sq[0]} to {worst_sq[1]} against 65536"
    )
    say(
        f"  the entries at the multiples of N/4: C = {cos_t[0]}, {cos_t[n // 4]}, {cos_t[n // 2]}, {cos_t[3 * n // 4]}; S = {sin_t[0]}, {sin_t[n // 4]}, {sin_t[n // 2]}, {sin_t[3 * n // 4]} (exact)"
    )
    d8 = n // 8
    say(
        f"  the entry at N/8 (45 degrees): C = {cos_t[d8]} against 128 sqrt 2 = {two_cos(d8, n) / 2 * 256:.6f}; C^2 = {cos_t[d8] ** 2} against 32768"
    )
    say(
        f"  the two-slit weight 32761 / 163840 = 181^2 / (5 x 2^15) of L2 becomes 32768 / 163840 = {Fraction(32768, 163840)} exactly"
    )
    say(
        "  a Gram entry G_jk = C_j C_k + S_j S_k errs by at most 2 x (256 x 1/2 + 256 x 1/2 + 1/4) = 512.5 on 65536, a part in 128 (the crude bound);"
    )
    say(
        "  the registered totals 65448 .. 65773 on 65536 (L1, note 37 (xii)) show a part in 276 on the norm."
    )
    for w in (64, 4096):
        eps = Fraction(237, 65536)
        say(
            f"  a rung at W = {w} moves by at most ceil(W x 237 / 65536) = {-(-w * 237 // 65536)} ({float(w * eps):.3f})"
        )
    say()


def section_4_cost(n: int) -> None:
    quarter = n // 4
    say(
        f"  the host cost at N = {n}: today the Gram matrix has {n * n} entries (stored through N = 512, formed beyond);"
    )
    say(
        f"  the exact form keeps {quarter} integers per weight and per cumulative rung, no matrix; the autocorrelation of a"
    )
    say(
        "  vector with s nonzero phases costs s^2 products; the sign test one P-bit inner product over N/4 terms."
    )
    say()


def main() -> None:
    for n in (64, 4096):
        section_1(n)
    for n in (64, 4096):
        section_2(n)
    section_4_tables(64)
    for n in (64, 4096):
        section_4_cost(n)
    print("\n".join(OUT))


if __name__ == "__main__":
    main()
