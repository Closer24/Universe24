"""DECODE3h's readings file, computed once (never at read time): readings3h.json.
- (3b)'s per-K cuts, two tails: for K = 20 to 39 windows read, the chi-square on K degrees at 5/12 per cent a tail (the
  half's 5/6 per cent, R3's family of six at 5 per cent by the union bound). hi_K is the least whole thousandth whose
  upper tail is at most the level; lo_K is the greatest whose lower tail is at most it, less K (each window's z_k is
  floored to thousandths, so the floored sum may sit up to K below the true one).
  - even K = 2m: P(X <= x) = 1 - e^(-x/2) SUM_(j < m) (x/2)^j / j!  (the Poisson sum);
  - odd K = 2m + 1: P(X <= x) = sqrt(2x / pi) U, U = T - e^(-x/2) SUM_(j=1..m) x^(j-1) / (2j - 1)!!, with
    T = SUM_n (-1)^n (x/2)^n / (n! (2n + 1)) (erf's series), compared squared: 2 x U^2 against pi a^2, no root;
  pi by Machin's arctangents; e^x by its series.
- CUT_FW at N_T 70 and 82 (one degree at 5 / N_T per cent); C2 and C4 as DECODE3g's.
Whole numbers; Rule3's carry the one division. argv: the output name (the readings file)."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

SC = 10 ** 90
TERMS = 320


def atan_inv(x):
    total, k, power, sign = 0, 0, x, 1
    while True:
        t, _ = carry(SC, (k + k + 1) * power, 0)
        if t == 0:
            return total
        total += sign * t
        sign, k, power = -sign, k + 1, power * x * x


PI = 16 * atan_inv(5) - 4 * atan_inv(239)


def exp_half(c):
    total, fact = 0, 1
    for k in range(TERMS):
        total += carry(SC * c ** k, 2000 ** k * fact, 0)[0]
        fact *= k + 1
    return total


def poisson_part(c, m):
    total, fact = 0, 1
    for j in range(m):
        total += carry(SC * c ** j, 2000 ** j * fact, 0)[0]
        fact *= j + 1
    return total


def odd_u(c, m):
    T, fact, sign = 0, 1, 1
    for n in range(TERMS):
        T += sign * carry(SC * c ** n, 2000 ** n * fact * (n + n + 1), 0)[0]
        sign, fact = -sign, fact * (n + 1)
    R, dfact = 0, 1
    for j in range(1, m + 1):
        dfact *= j + j - 1
        R += carry(SC * c ** (j - 1), 1000 ** (j - 1) * dfact, 0)[0]
    return T - carry(R * SC, exp_half(c), 0)[0]


def cdf_le(c, K, num, den):
    """True where P(X_K <= c / 1,000) <= num / den."""
    m, odd = carry(K, 2, 0)
    if odd == 0:
        E, S = exp_half(c), poisson_part(c, m)
        return den * (E - S) <= num * E
    U = odd_u(c, m)
    return 2 * c * U * U * den * den <= 1000 * PI * SC * num * num


def cdf_ge(c, K, num, den):
    """True where P(X_K <= c / 1,000) >= num / den."""
    m, odd = carry(K, 2, 0)
    if odd == 0:
        E, S = exp_half(c), poisson_part(c, m)
        return den * (E - S) >= num * E
    U = odd_u(c, m)
    return 2 * c * U * U * den * den >= 1000 * PI * SC * num * num


def least(ok, lo, hi):
    while hi - lo > 1:
        mid, _ = carry(lo + hi, 2, 0)
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi


def greatest(ok, lo, hi):
    while hi - lo > 1:
        mid, _ = carry(lo + hi, 2, 0)
        if ok(mid):
            lo = mid
        else:
            hi = mid
    return lo


def one_ok(c, n):
    T, fact, sign = 0, 1, 1
    for k in range(TERMS):
        t, _ = carry(SC * c ** k, 2000 ** k * fact * (k + k + 1), 0)
        T += sign * t
        sign, fact = -sign, fact * (k + 1)
    return 2 * c * T * T * (20 * n) ** 2 >= 1000 * PI * SC * (20 * n - 1) ** 2


B3 = {}
for K in range(20, 40):
    hi = least(lambda c: cdf_ge(c, K, 239, 240), 1000 * K, 1000 * (K + 80))
    lo0 = greatest(lambda c: cdf_le(c, K, 1, 240), 1, 1000 * K)
    B3[K] = [lo0 - K, hi]
readings = {"convention": "the least whole thousandth whose tail is at most its level; SHOWN where the floored"
                          " statistic is at most the cut (upper tails), at least the cut (lower tails)",
            "B3": B3, "C2": 9575, "C4": 13696, "K_MIN": 20, "E_MIN_TWO": 10, "FIVE": 5, "AMBIG": 2,
            "R2_GATE": 20, "CUT_FW": {nt: least(lambda c: one_ok(c, nt), 3000, 30000) for nt in (46, 58, 70, 82)}}
HERE.joinpath(sys.argv[1]).write_text(json.dumps(readings, indent=1, sort_keys=True) + "\n", encoding="utf-8")
