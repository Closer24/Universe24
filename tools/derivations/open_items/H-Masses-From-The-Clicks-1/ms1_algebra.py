"""ms1: the algebra of the charge and the pairs in integers (2026-10-25).
(1) den's primes and the exact points of den's circle (num, s) with num^2 + s^2 = den^2: the finite spectrum a den holds.
(2) The file's lifts against the circle: exact points or not; the legs' ratios per 10^9; the gaps per 10^9.
(3) The charge per child: the engine's lay (take.lay_amplitude at the vacuum, A^2 >= T s / (2 den - num)) against the law's
    (ALGEBRA.md, The charge written is the Wronskian over T div 2 for every reader: A = largest_below(T div 2), W = A^2 for every row).
(4) The integral lay (K-S2): 4 a b | T for every lift's prime; the exact rest lay T / (4 a b p) a square.
(5) Candidate (b): the unit 3 T s against the massless unit 3 T den: s | den never for a lift (gcd(2ab, a^2 + b^2) = 1).
Usage: python ms1_algebra.py <universe.json> [T]   (integers only; ratios as integers per 10^9)."""
import json
import sys

sys.set_int_max_str_digits(0)

from event_universe.core.paces import sine_den  # noqa: E402
from event_universe.core.rule3 import largest_below, link_unit_of, quotient  # noqa: E402

G9 = 10**9


def factor(n):
    """The prime factors of n by trial division up to the cube root, then one Pollard rho round for a 54-bit den (two factors left)."""
    found = []
    p = 2
    while p * p <= n and p < 2 * 10**6:
        while n % p == 0:
            found.append(p)
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        found += rho(n)
    return sorted(found)


def is_prime(n):
    if n < 2:
        return False
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % a == 0:
            return n == a
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def rho(n):
    if is_prime(n):
        return [n]
    from math import gcd

    c = 1
    while True:
        x = y = 2
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return sorted(rho(d) + rho(n // d))
        c += 1


def two_squares(p):
    """p = a^2 + b^2 with a > b > 0 for a prime p = 1 mod 4 (a search by comparisons)."""
    a = largest_below(p)
    while a * a > p // 2:
        b2 = p - a * a
        b = largest_below(b2)
        if b * b == b2:
            return a, b
        a -= 1
    raise ValueError(f"{p} is no sum of two squares")


def points(den):
    """Every exact point (num, s) of den's circle with 0 < num < den, 0 < s: the Gaussian integers of norm den^2 up to units and conjugation, enumerated over the exponents of each prime's two conjugate factors."""
    primes = factor(den)
    from collections import Counter

    exps = Counter(primes)
    gauss = []  # (re, im, exponent) per distinct prime 1 mod 4; a prime 3 mod 4 or 2 contributes a real factor
    real = 1
    for p, e in sorted(exps.items()):
        if p == 2 or p % 4 == 3:
            real *= p**e
        else:
            a, b = two_squares(p)
            gauss.append((a, b, e))
    found = set()

    def walk(k, re, im):
        if k == len(gauss):
            re, im = re * real, im * real
            num, s = abs(re), abs(im)
            if 0 < num < den and s > 0:
                found.add((num, s))
            return
        a, b, e = gauss[k]
        for j in range(2 * e + 1):
            r, i = re, im
            for _ in range(j):
                r, i = r * a - i * b, r * b + i * a
            for _ in range(2 * e - j):
                r, i = r * a + i * b, i * a - r * b
            walk(k + 1, r, i)

    walk(0, 1, 0)
    return primes, sorted(found)


def main():
    universe = json.load(open(sys.argv[1]))
    ints = universe["integers"]
    den, gamma, T = int(ints["den"]), int(ints["node_clock"]), int(ints["quantum_action"])
    if len(sys.argv) > 2:
        T = int(sys.argv[2])
    G = link_unit_of(gamma)
    primes, pts = points(den)
    print(f"den {den} bits {den.bit_length()} primes {primes}")
    print(f"exact points of den's circle (num < den, s > 0): {len(pts)}")
    legs = sorted(s for _n, s in pts)
    print("points sorted by leg (num, s, gap per 1e9 = (den-num) 1e9 div den):")
    for num, s in sorted(pts, key=lambda p: p[1]):
        print(f"  num {num} s {s} gap_1e9 {(den - num) * G9 // den} s/den_1e9 {s * G9 // den}")
    print("leg ratios of consecutive-by-leg points per 1e9 (s_k / s_0 for all k):")
    for s in legs[1:]:
        print(f"  {s * G9 // legs[0]}")
    print("all pairwise leg ratios per 1e9 nearest to 1836152673 (p/e) and 1001378419 (n/p) and 206768283 (mu/e):")
    best = {}
    for name, target in (("p/e", 1836152673), ("n/p", 1001378419), ("mu/e", 206768283 * 1000 // 1000)):
        bb = None
        for i in range(len(legs)):
            for j in range(len(legs)):
                if legs[j] > legs[i]:
                    r = legs[j] * G9 // legs[i]
                    if bb is None or abs(r - target) < abs(bb[0] - target):
                        bb = (r, legs[i], legs[j])
        best[name] = bb
        print(f"  {name}: nearest ratio {bb[0] if bb else None} (legs {bb[1] if bb else None}, {bb[2] if bb else None}); off by {abs(bb[0]-target) if bb else None} per 1e9")
    print()
    print("the file's plane rows against the circle:")
    half_T = T // 2
    A_law = largest_below(half_T)
    print(f"T {T} T div 2 {half_T} A_law = largest_below(T div 2) = {A_law}, W_law = A_law^2 = {A_law * A_law} for every row")
    w_eng = {}
    for r in universe["rows"]:
        if int(r["shape"]) != 2:
            continue
        num = int(r["pair"][0])
        s = sine_den(num, den)
        exact = s * s == den * den - num * num
        gap = den - num
        # the engine's lay at the vacuum: weight = 2 D + sum R = 12 Gamma^2 G^2 (2 den - num); target = 3 T s 4 Gamma^2 G^2
        weight = 12 * gamma * gamma * G * G * (2 * den - num)
        target = 3 * T * s * 4 * gamma * gamma * G * G
        A = largest_below(quotient(target, weight))
        while weight * A * A < target:
            A += 1
        w_eng[num] = A * A
        unit = 3 * T * s
        print(f"  num {num} gap {gap} s {s} exact_point {exact} unit 3Ts {unit} bits {unit.bit_length()}")
        print(f"     engine lay at the vacuum: A {A} W_child = A^2 = {A * A}; W_eng per T div 2, per 1e9: {A * A * G9 // half_T}")
        print(f"     law's lay: A {A_law} W {A_law * A_law}; lone share 6 den A^2 per massless unit 3 den T, per 1e9: {6 * den * A_law * A_law * G9 // (3 * den * T)}")
        print(f"     law's child counted in its own unit (6 den A^2 / 3 T s), per 1e9: {6 * den * A_law * A_law * G9 // unit if s else None}")
    ws = sorted(v for v in w_eng.values() if v)
    if len(ws) > 1:
        print(f"  the engine's W per child: least {ws[0]} largest {ws[-1]} ratio per 1e9 {ws[-1] * G9 // ws[0]}; the law's: one value {A_law * A_law} for every row")
    print()
    print("K-S2's integral lay 4 a b | T per prime of den, and the exact rest lay T / (4 a b p) a square:")
    for p in sorted(set(primes)):
        if p % 4 == 1:
            a, b = two_squares(p)
            four_ab = 4 * a * b
            k2 = T % (four_ab * p)
            print(f"  p {p} = {a}^2 + {b}^2, 4ab {four_ab}, T mod 4ab {T % four_ab}, sin omega_p = 2ab/p per 1e9 {2 * a * b * G9 // p}, T mod (4ab p) {k2}")
    print()
    print("candidate (b): s | den for the file's lifts? (the unit 3 T s dividing the massless unit 3 T den)")
    for num, s in pts:
        print(f"  num {num}: den mod s = {den % s}  (divides: {den % s == 0})")
    print()
    print("candidate (d): the rest rotation at content c, 2 cos omega_c = 2 - D/w with D/w = 2 (den - num) p0^2 / (den Gamma^2): the step is one carried division at the wall w, the remainder in [0, w): no tie at any content for any pair (a theorem of the carried division; nothing to select).")


if __name__ == "__main__":
    main()
