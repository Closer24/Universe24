"""DECODE3g's cuts, computed once for the readings file (never at read time). One convention: C is the least whole
thousandth whose tail is at most the level; a reading is SHOWN where its floored statistic is at most C.
- one degree: P(X > c) = 1 - erf(s), s^2 = c / 2,000 (c in thousandths); erf(s)^2 = (2 c / pi) T^2 with
  T = SUM (-1)^n (c / 2,000)^n / (n! (2n + 1)); pi by Machin's arctangents;
- two degrees: P(X > c) = e^(-c / 2,000);
- four degrees: P(X > c) = e^(-c / 2,000) (1 + c / 2,000);
e^x by its series to 200 terms (the remainder below 10^-100 here). Levels: 5 / (100 N) for N tests.
Whole numbers; Rule3's carry the one division. argv: the output name."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

SC = 10 ** 80


def atan_inv(x):
    total, k, power, sign = 0, 0, x, 1
    while True:
        t, _ = carry(SC, (k + k + 1) * power, 0)
        if t == 0:
            return total
        total += sign * t
        sign, k, power = -sign, k + 1, power * x * x


PI = 16 * atan_inv(5) - 4 * atan_inv(239)


def one_ok(c, n):
    T, fact, sign = 0, 1, 1
    for k in range(200):
        t, _ = carry(SC * c ** k, 2000 ** k * fact * (k + k + 1), 0)
        T += sign * t
        sign, fact = -sign, fact * (k + 1)
    return 2 * c * T * T * (20 * n) ** 2 >= 1000 * PI * SC * (20 * n - 1) ** 2


def exp_half(c):
    """e^(c / 2,000), scaled by SC."""
    total, fact = 0, 1
    for k in range(200):
        total += carry(SC * c ** k, 2000 ** k * fact, 0)[0]
        fact *= k + 1
    return total


def two_ok(c, n):
    return exp_half(c) >= 20 * n * SC


def four_ok(c, n):
    return 2000 * exp_half(c) >= 20 * n * SC * (2000 + c)


def least(ok, n):
    lo, hi = 1000, 40000
    while hi - lo > 1:
        mid, _ = carry(lo + hi, 2, 0)
        if ok(mid, n):
            hi = mid
        else:
            lo = mid
    return hi


out = []
for n in (1, 6, 18, 20, 26, 30, 34, 46, 58):
    out.append(f"N {n}: one degree {least(one_ok, n)}")
for n in (1, 6):
    out.append(f"N {n}: two degrees {least(two_ok, n)}; four degrees {least(four_ok, n)}")
HERE.joinpath(sys.argv[1]).write_text("\n".join(out) + "\n", encoding="utf-8")
