"""Koide's 2/3 on whole counts: the three masses as a held spring's three values, in whole numbers alone.

Every division is Rule3's carry (tensor24.algebra.carry.carry); no float, no fraction, no root but Newton's steps in
carries. The spring at a Node-clock is the A1 part n0 and an E part (e1, e2) on the diagonal, its values
s = (n0 + e1, n0 - e1 + e2, n0 - e2), read as the roots of the three masses (board2mass 7.2); with a T2 part t the
spring is the symmetric matrix with that diagonal and t's entries S23, S13 and S12 off it, its eigenvalues the
roots.

(a) the identity: sum s = 3 n0 and sum s^2 = 3 n0^2 + 2 N, N = e1^2 - e1 e2 + e2^2, so Koide's ratio
    Q = sum s^2 / (sum s)^2 = 1/3 + 2 N / (9 n0^2), and Q = 2/3 reads 2 N = 3 n0^2;
(b) no whole solution on the diagonal: the search over 1 <= n0 <= 60 and |e1|, |e2| <= 60;
(c) why: N is the Eisenstein norm of e1 + e2 w, 2 stays prime in the Eisenstein integers, so every nonzero norm has
    an even power of 2, while 3 n0^2 / 2 = N needs an odd one; the parity over |e1|, |e2| <= 300;
(d) the nearest approaches: 3 n0^2 - 2 N = 1 (Q = 2/3 - 1 / (9 n0^2), from below) with three values above 0, found
    for every odd n0 up to 400 by solving for e2 (4 N - 3 e1^2 a square); none from above, 2 N - 3 n0^2 = 1;
(e) with a T2 part, at n0 = 4: the whole (e1, e2, t) with 2 (N + |t|^2) = 3 n0^2 whose spring is positive definite
    (its three leading minors above 0) with three distinct eigenvalues (the discriminant of its cubic not 0): their
    number, and one of them;
(f) nature's ratio from the charged leptons' masses (PDG 2024, S. Navas and others, Phys. Rev. D 110, 030001 (2024):
    m_e = 0.51099895000 MeV, m_mu = 105.6583755 MeV, m_tau = 1776.93 +- 0.09 MeV), the roots by Newton's steps at
    a fine scale.

Usage: python3 -I koide_whole.py <src of main at 0df0e8385>
"""

import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402


def root(n):
    """The whole square root of n: the largest x with x x at most n, by Newton's steps in carries."""
    if n < 2:
        return n
    x, y = n, carry(n + 1, 2, 0)[0]
    while y < x:
        x, y = y, carry(y + carry(n, y, 0)[0], 2, 0)[0]
    return x


def two_power(n):
    """The power of 2 that divides n (n not 0)."""
    k = 0
    q, r = carry(n, 2, 0)
    while r == 0:
        n, k = q, k + 1
        q, r = carry(n, 2, 0)
    return k


def norm(e1, e2):
    return e1 * e1 - e1 * e2 + e2 * e2


# (a) the identity
ok_a, count_a = True, 0
for n0 in range(1, 31):
    for e1 in range(-30, 31):
        for e2 in range(-30, 31):
            s = (n0 + e1, n0 - e1 + e2, n0 - e2)
            ok_a = ok_a and sum(s) == 3 * n0 and sum(v * v for v in s) == 3 * n0 * n0 + 2 * norm(e1, e2)
            count_a += 1
print(f"(a) sum s = 3 n0 and sum s^2 = 3 n0^2 + 2 N on all {count_a} whole (n0, e1, e2) with 1 <= n0 <= 30 and"
      f" |e1|, |e2| <= 30: {ok_a}; so Q = 2/3 reads 2 N = 3 n0^2")

# (b) no whole solution on the diagonal
found_b = [(n0, e1, e2) for n0 in range(1, 61) for e1 in range(-60, 61) for e2 in range(-60, 61)
           if 2 * norm(e1, e2) == 3 * n0 * n0]
print(f"(b) whole (n0, e1, e2) with 1 <= n0 <= 60, |e1|, |e2| <= 60 and 2 N = 3 n0^2: {len(found_b)}")

# (c) the parity of 2 in the norms
odd_power, nonzero = 0, 0
for e1 in range(-300, 301):
    for e2 in range(-300, 301):
        n = norm(e1, e2)
        if n:
            nonzero += 1
            odd_power += carry(two_power(n), 2, 0)[1]
print(f"(c) of the {nonzero} nonzero norms N = e1^2 - e1 e2 + e2^2 with |e1|, |e2| <= 300, those with an odd power"
      f" of 2:"
      f" {odd_power}; 3 n0^2 = 2 N needs n0 even and then N = 6 (n0 / 2)^2, whose power of 2 is odd")


# (d) the nearest approaches: 3 n0^2 - 2 N = 1 (from below) and 2 N - 3 n0^2 = 1 (from above), three values above 0
def approaches(n0, target_twice):
    """The (e1, e2) with 2 N = target_twice and the three values n0 + e1, n0 - e1 + e2, n0 - e2 above 0."""
    out = []
    q, odd = carry(target_twice, 2, 0)
    if odd:
        return out
    big_n = q
    for e1 in range(-n0 + 1, 2 * n0):
        disc = 4 * big_n - 3 * e1 * e1  # e2 = (e1 +- root(disc)) / 2
        if disc < 0:
            continue
        r = root(disc)
        if r * r != disc:
            continue
        for e2_twice in (e1 + r, e1 - r):
            e2, rest = carry(e2_twice, 2, 0)
            if rest == 0 and norm(e1, e2) == big_n:
                s = (n0 + e1, n0 - e1 + e2, n0 - e2)
                if min(s) > 0 and (e1, e2) not in out:
                    out.append((e1, e2))
    return out


below_n0, below_total, above_total, example = [], 0, 0, None
for n0 in range(1, 401):
    got = approaches(n0, 3 * n0 * n0 - 1)
    if got:
        below_n0.append(n0)
        below_total += len(got)
        if n0 == 389:
            example = [(e1, e2, (n0 + e1, n0 - e1 + e2, n0 - e2)) for e1, e2 in got if e1 == -361]
    above_total += len(approaches(n0, 3 * n0 * n0 + 1))
print(f"(d) 3 n0^2 - 2 N = 1, three values above 0, n0 from 1 to 400: at {len(below_n0)} values of n0, {below_total}"
      f" (n0, e1, e2) in all (each is Q = 2/3 - 1 / (9 n0^2)); at n0 = 389 with e1 = -361: {example}; 2 N - 3 n0^2 = 1"
      f" (from above): {above_total}")

# (e) with a T2 part at n0 = 4: 2 (N + |t|^2) = 3 n0^2 = 48
n0 = 4
sols, first = 0, None
for e1 in range(-8, 9):
    for e2 in range(-8, 9):
        rest_t = 24 - norm(e1, e2)
        if rest_t < 0:
            continue
        for t1 in range(-5, 6):
            for t2 in range(-5, 6):
                for t3 in range(-5, 6):
                    if t1 * t1 + t2 * t2 + t3 * t3 != rest_t:
                        continue
                    d1, d2, d3 = n0 + e1, n0 - e1 + e2, n0 - e2
                    m1 = d1
                    m2 = d1 * d2 - t3 * t3
                    m3 = d1 * (d2 * d3 - t1 * t1) - t3 * (t3 * d3 - t1 * t2) + t2 * (t3 * t1 - d2 * t2)
                    if m1 <= 0 or m2 <= 0 or m3 <= 0:
                        continue
                    # the characteristic cubic x^3 - a x^2 + b x - c, its discriminant
                    a = d1 + d2 + d3
                    b = d1 * d2 + d2 * d3 + d1 * d3 - t1 * t1 - t2 * t2 - t3 * t3
                    c = m3
                    disc = 18 * a * b * c - 4 * a**3 * c + a * a * b * b - 4 * b**3 - 27 * c * c
                    if disc == 0:
                        continue
                    sols += 1
                    if (e1, e2, t1, t2, t3) == (-3, -5, -2, 0, 1):
                        first = [[d1, t3, t2], [t3, d2, t1], [t2, t1, d3]]
print(f"(e) a T2 part at n0 = 4, 2 (N + |t|^2) = 48, the spring positive definite with three distinct eigenvalues:"
      f" {sols} whole (e1, e2, t1, t2, t3); E (-3, -5) with T2 (-2, 0, 1) among them: {first is not None}, the spring"
      f" {first}")

# (f) nature's ratio: masses in units of 10^-11 MeV, roots at a scale of 10^12 more
M_E, M_MU = 51099895000, 10565837550000
SCALE = 10**24
lines_f = []
for label, m_tau in (("m_tau - 0.09", 177684000000000), ("m_tau", 177693000000000), ("m_tau + 0.09", 177702000000000)):
    total = M_E + M_MU + m_tau
    roots = root(M_E * SCALE) + root(M_MU * SCALE) + root(m_tau * SCALE)  # each root(m) times 10^12
    q = carry(total * SCALE * 10**9, roots * roots, 0)[0]  # Q times 10^9
    whole, frac = carry(q, 10**9, 0)
    lines_f.append(f"{label}: Q = {whole}.{frac:09d}")
print("(f) nature's ratio Q = (m_e + m_mu + m_tau) / (root m_e + root m_mu + root m_tau)^2, PDG 2024: "
      + "; ".join(lines_f) + "; 2/3 = 0.666666667")
