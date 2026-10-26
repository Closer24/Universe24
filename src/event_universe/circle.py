"""den's circle, a reader's derivation from den alone (MS-S2, the owner's word of 2026-10-25 through the Boss, 6399410929): den's primes by Pollard's rho with the gcd rule3's lattice, each prime 1 mod 4 as a^2 + b^2 by a search by comparisons, every point (num, s) with num^2 + s^2 = den^2 by the Gaussian products (3^k - 1 points for k distinct primes 1 mod 4); the finite spectrum the pairs are drawn from, printed by gate 19 and refused off by the Node at the load."""

from __future__ import annotations

from event_universe.core import rule3

LEAST_PRIME, GAUSS_MODULUS = (
    2,
    4,
)  # the first prime (the trial division's start, the strong test's power of two); a prime splits in the Gaussian integers where it is 1 mod 4


def witnesses(n: int) -> list[int]:
    """The primes below n's bit length (and two), the strong test's witnesses: the primes to 7 decide below 2^31, to 37 below 2^81."""
    bound = n.bit_length() + LEAST_PRIME
    return [p for p in range(LEAST_PRIME, bound) if all(p % q for q in range(LEAST_PRIME, p))]


def is_prime(n: int) -> bool:
    """A prime by the strong test at the witnesses, enough far beyond the width."""
    if n < LEAST_PRIME:
        return False
    small = witnesses(n)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % LEAST_PRIME == 0:
        d, s = d // LEAST_PRIME, s + 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def divisor_of(n: int) -> int:
    """A proper divisor of a composite n by Pollard's rho (Brent's cycle), the gcd rule3's lattice; the constant stepped where the walk closes."""
    if n % LEAST_PRIME == 0:
        return LEAST_PRIME
    c = 1
    while True:
        y, m, g, r, q = LEAST_PRIME, n.bit_length(), 1, 1, 1
        x = ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g, k = int(rule3.lattice(q, n)), k + m
            r += r
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = int(rule3.lattice(abs(x - ys), n))
        if g != n:
            return g
        c += 1


def circle_of(den: int) -> list[tuple[int, int]]:
    """den's circle (MS-S2): den's primes (rho), each prime 1 mod 4 as a^2 + b^2 by a search by comparisons, every point (num, s) with num^2 + s^2 = den^2, num > 0 and s > 0, by the Gaussian products (3^k - 1 points for k distinct primes 1 mod 4), sorted by num."""
    primes: list[int] = []
    stack = [den]
    while stack:
        n = stack.pop()
        if n == 1:
            continue
        if is_prime(n):
            primes.append(n)
            continue
        d = divisor_of(n)
        stack += [d, n // d]
    scale, gauss = 1, []
    for p in sorted(set(primes)):
        e = primes.count(p)
        if p % GAUSS_MODULUS != 1:
            scale *= p**e
            continue
        a = 1
        while True:
            b = rule3.largest_below(p - a * a)
            if b * b == p - a * a:
                break
            a += 1
        gauss.append(((a, b), e))
    points = {(scale, 0)}
    for (a, b), e in gauss:
        grown = set()
        for x, y in points:
            for j in range(e + e + 1):
                zx, zy = 1, 0
                for _ in range(j):
                    zx, zy = zx * a - zy * b, zx * b + zy * a
                for _ in range(e + e - j):
                    zx, zy = zx * a + zy * b, -zx * b + zy * a
                grown.add((x * zx - y * zy, x * zy + y * zx))
        points = grown
    return sorted({(abs(u), abs(v)) for x, y in points for (u, v) in ((x, y), (y, x)) if u and v})
