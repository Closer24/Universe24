"""The circle of den: its Pythagorean points from den's primes and the lightest among them (the owner's word of 2026-10-24, 09:1x UTC, "the charged plane family at rest is the lightest point of the circle"; ALGEBRA.md, The lightest point is derived): the primes by Miller and Rabin's witnesses and Pollard's rho (`is_prime`, `split`, `factors`), a prime 1 mod 4 as two squares by Fermat and Hermite and Serret's act (`two_squares`), every point of the circle from them and the least leg (`lightest_point`), every division the division act and no root; the loader's tool for the labels of the born pairs, writing no row (the owner's word of 09:4x UTC, declaring a family is forbidden). Beside the lightest point, every point of the circle with its label (the owner's word of 2026-10-24, "declaring a family is forbidden; they must emerge by themselves at the click"; ALGEBRA.md, A family's declaration, The circle of den): the file holds den and no family row, and the loader derives from den's integers the Pythagorean points num^2 + s^2 = den^2 of the open quadrant (num > 0, s > 0), every one a product of den's Gaussian primes turned into the quadrant by the units and labelled by its exponent vector over den's primes 1 mod 4 and nothing else (`circle_points`, `label_of`, `vector_of`): for the primes 1 mod 4 with their exponents e_i every vector v with v_i in {-2 e_i, ..., 2 e_i} by twos, the point z = scale x PROD g_i^k_i conj(g_i)^(2 e_i - k_i) with k_i = (v_i + 2 e_i) / 2, g_i = a + i b the prime's two squares with a > b (`two_squares`, `gaussian_of`) and scale the part of den outside those primes (the twos and the primes 3 mod 4, no angle, `angled`), rotated by i until both legs are positive (`quadrant`), so that the vectors and the points of the quadrant correspond one to one (3^n - 1 points for n primes 1 mod 4 each once; 242 at den 53,567,765 = 5 x 17 x 73 x 89 x 97, 26 at the three-prime den 1,166,991,900,949,580,266,237) and the vector -v is the point with the legs swapped; the zero vector is the axis (den, 0), the massless point, no row of the circle."""

from __future__ import annotations

from functools import cache
from math import gcd

from event_universe.core.ports import PORTS, SIDES
from event_universe.core.rule3 import division_forward, largest_below


def primes_below(bound: int) -> list[int]:
    """The primes below `bound`, each found by the division act against the primes before it (Eratosthenes by trial), the witnesses of `is_prime`."""
    found: list[int] = []
    for n in range(2, bound):
        if all(division_forward(n, p, 0)[1] for p in found if p * p <= n):
            found.append(n)
    return found


def is_prime(n: int) -> bool:
    """Whether n is prime, by Miller and Rabin's test with every prime below 2^6 as a witness (18 witnesses: exact below 3.3 x 10^24, the first twelve, and a probable prime beyond it, the loader's tool and no line of the law): n - 1 = d 2^s by the division act, a^d and its squares read modulo n by Python's own modular power."""
    if n < 2:
        return False
    witnesses = primes_below(SIDES**PORTS)
    if n in witnesses:
        return True
    if any(division_forward(n, p, 0)[1] == 0 for p in witnesses):
        return False
    d, s = n - 1, 0
    while division_forward(d, 2, 0)[1] == 0:
        d, s = int(division_forward(d, 2, 0)[0]), s + 1
    for a in witnesses:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def split(n: int) -> int:
    """A proper factor of the composite n by Pollard's rho with Brent's cycle (the squares x -> x^2 + c modulo n by Python's modular power, the hare's run doubling each round and the common divisor of x - y and n by Euclid's act, `gcd`, at every step of the run), the loader's tool for the circle's primes: the constant c counted up from 1 where the cycle closes on n itself; no count of this function's own (one divisor per round over the round's product needs the product reduced by the division act at every step and measured slower, 31 s against 22 s on the PeV den's 155 bits; a batch of six steps 17 s, set aside for its constant); the same factors as Floyd's cycle with three modular powers and one divisor per step, the loader's split to 2026-10-24, kept by name (52 s on the PeV den)."""
    c = 1
    while True:
        y, r, g = 2, 1, 1
        while g == 1:
            x = y
            for _ in range(r):
                y = pow(y, 2, n) + c
            k = 0
            while k < r and g == 1:
                y = pow(y, 2, n) + c
                g, k = gcd(x - y, n), k + 1
            r += r
        if g != n:
            return g
        c += 1


@cache
def factors(n: int) -> dict[int, int]:
    """The prime factors of n with their exponents (`is_prime`, `split`), 2 divided out first by the division act; a pure function of n, memoized within the process (the loader's one derivation of the circle from den, asked by `circle_points`, `lightest_point` and the eras log's header; the pattern of `plane.turned_room`, 2026-10-24: the PeV den's factoring once per process, never a file, never a key)."""
    found: dict[int, int] = {}
    while n > 1 and division_forward(n, 2, 0)[1] == 0:
        found[2], n = found.get(2, 0) + 1, int(division_forward(n, 2, 0)[0])
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if is_prime(m):
            found[m] = found.get(m, 0) + 1
        else:
            piece = split(m)
            stack += [piece, int(division_forward(m, piece, 0)[0])]
    return found


def two_squares(p: int) -> tuple[int, int]:
    """A prime p = 1 mod 4 as a sum of two squares, a^2 + b^2 = p (Fermat; Hermite and Serret's act): a root of x^2 = -1 modulo p from a non-residue's power by Python's modular power, then Euclid's remainders on (p, x) by the division act down to the first below the root of p (`largest_below`), the two legs the last two remainders."""
    quarter = int(division_forward(int(division_forward(p - 1, 2, 0)[0]), 2, 0)[0])
    witness = 2
    while pow(witness, 2 * quarter, p) != p - 1:  # a quadratic residue: the next witness
        witness += 1
    a, b, root = p, pow(witness, quarter, p), largest_below(p)
    while b > root:
        a, b = b, int(division_forward(a, b, 0)[1])
    return b, int(division_forward(a, b, 0)[1])


def lightest_point(den: int) -> tuple[int, int]:
    """The lightest point of the circle of den (the owner's word of 2026-10-24, 09:1x UTC, "the charged plane family at rest is the lightest point of the circle"; ALGEBRA.md, The one universe, the extremal sentence, The lightest point is the electron): among the Pythagorean points (num, s, den), num > 0 and s > 0 and num^2 + s^2 = den^2, the one of the least leg s, m_e / T = s_min(den) / den; every point from den's primes (`factors`): a prime 1 mod 4 contributes its two legs as a Gaussian prime a + b i (`two_squares`), each of its 2 e appearances the prime or its conjugate, 2 contributes (2 i)^e and a prime 3 mod 4 its real power, the unit one of four, so the points are enumerated whole (4 x 3^k for k such primes once each: 972 at den 53,567,765 = 5 x 17 x 73 x 89 x 97, 108 under three primes), the least leg among those in the first quadrant; (num, s) = (53,567,757, 29,276) at the one universe's den, the electron's row of the file; refused by name where the circle has no such point (no prime 1 mod 4 in den)."""
    points = [(1, 0)]
    for prime, exponent in factors(den).items():
        if prime == 2:
            for _ in range(exponent):
                points = [(-b - b, a + a) for a, b in points]  # times 2 i
            continue
        if (
            division_forward(prime, SIDES + SIDES, 0)[1] != 1
        ):  # a prime 3 mod 4: its real power, den^2 even in it
            points = [(a * prime**exponent, b * prime**exponent) for a, b in points]
            continue
        legs = two_squares(prime)
        powers = [(1, 0)]
        for _ in range(
            2 * exponent
        ):  # the prime's 2 e appearances in den^2, each the prime or its conjugate
            powers = [(a * legs[0] - b * legs[1], a * legs[1] + b * legs[0]) for a, b in powers] + [
                (a * legs[0] + b * legs[1], b * legs[0] - a * legs[1]) for a, b in powers[-1:]
            ]
        points = [(a * c - b * d, a * d + b * c) for a, b in points for c, d in powers]
    found = sorted(
        (min(abs(a), abs(b)), max(abs(a), abs(b))) for a, b in points if a * b
    )  # the four units turn a point into the first quadrant as (|a|, |b|) and (|b|, |a|): the least leg of either
    if not found:
        raise ValueError(
            f"the circle of den {den} has no point with both legs above 0 (no prime 1 mod 4 divides it): the "
            "lightest point, the least leg of den's circle, is not derived (ALGEBRA.md, The one universe)"
        )
    s, num = found[0]
    return num, s


Gauss = tuple[int, int]  # a Gaussian integer a + i b
Point = tuple[tuple[int, ...], int, int]  # a point of the circle: its exponent vector, num and s


def gaussian_of(prime: int) -> Gauss:
    """The Gaussian prime a + i b above a prime 1 mod 4 with a > b > 0, its two squares (`two_squares`) ordered."""
    legs = two_squares(prime)
    return max(legs), min(legs)


def times(left: Gauss, right: Gauss) -> Gauss:
    """The product of two Gaussian integers."""
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def quadrant(point: Gauss) -> Gauss:
    """A Gaussian integer off the axes turned by i into the open first quadrant, both legs positive."""
    assert point[0] != 0 and point[1] != 0, f"{point} lies on an axis"
    while point[0] <= 0 or point[1] <= 0:
        point = -point[1], point[0]
    return point


def angled(den: int) -> tuple[list[tuple[int, int]], int]:
    """Den's primes 1 mod 4 with their exponents in rising order, the ones that carry an angle (`factors`), and the scale, den's part outside them (the twos and the primes 3 mod 4), which carries none."""
    primes = sorted(
        (prime, power)
        for prime, power in factors(den).items()
        if division_forward(prime, SIDES + SIDES, 0)[1] == 1
    )
    scale = den
    for prime, power in primes:
        scale = int(division_forward(scale, prime**power, 0)[0])
    return primes, scale


def circle_points(den: int) -> list[Point]:
    """Every point of den's circle in the open quadrant with its exponent vector over den's primes 1 mod 4 (the module's sentence), in the vectors' order; none where den has no prime 1 mod 4."""
    primes, scale = angled(den)
    gaussians = {prime: gaussian_of(prime) for prime, _power in primes}  # each prime split once
    vectors: list[tuple[int, ...]] = [()]
    for _prime, power in primes:
        vectors = [v + (step,) for v in vectors for step in range(-2 * power, 2 * power + 1, 2)]
    found = []
    for vector in vectors:
        if not any(vector):
            continue  # the axis, the massless point (den, 0)
        point: Gauss = (scale, 0)
        for (prime, power), step in zip(primes, vector, strict=True):
            gauss = gaussians[prime]
            lift = int(division_forward(step + 2 * power, 2, 0)[0])
            for _ in range(lift):
                point = times(point, gauss)
            for _ in range(2 * power - lift):
                point = times(point, (gauss[0], -gauss[1]))
        if point[0] == 0 or point[1] == 0:
            continue
        num, sine = quadrant(point)
        assert num * num + sine * sine == den * den, f"{vector}: no point of den {den}"
        found.append((vector, num, sine))
    return found


@cache
def lift_points(den: int) -> tuple[Point, ...]:
    """The lifts of den's primes, the bodies' points (ALGEBRA.md, Matter's birth from light, the birth's selector, 2026-10-24, 13:xx UTC; No family is declared: each charged family is the lift of its prime's point): among the circle's points (`circle_points`) the ones whose exponent vector carries one prime alone at its whole power, v_k = 2 e_k and every other entry 0, the point pi_k^(2 e_k) x PROD over j != k of h_j^(e_j) x scale turned into the quadrant, at twice the prime's angle where e_k = 1, its leg s = 2 a b x den / h_k for pi_k = a + i b with a > b; one lift per prime 1 mod 4 (three at the dens of three primes, the least leg the electron's, then the proton's and the neutron's by mass; one at den 1,021, (779, 660); one at den 6,000, the prime 5's whole power (2112, 5616)), in the vectors' order; the vector -v is the lift's swap, a point near the top where the lift is near the axis, a vector with two or more nonzero entries a composed word of the lifts and the zero vector the top (den, 0): the swaps, the composed points and the top are no bodies and never candidates (the composed points' and the top's derivations of 2026-10-24); a function of den alone, made once per den (`cache`)."""
    primes, _scale = angled(den)
    return tuple(
        point
        for point in circle_points(den)
        if sum(1 for step in point[0] if step) == 1
        and all(step in (0, 2 * power) for step, (_prime, power) in zip(point[0], primes, strict=True))
    )


def label_of(vector: tuple[int, ...]) -> str:
    """A point's label, read from its integers alone: the word point and its exponents over den's primes 1 mod 4 in rising order, "point 0 2 0" the least leg's at the three-prime den (the lift of its middle prime), "point 0 0 2" the heaviest prime's."""
    return "point " + " ".join(str(step) for step in vector)


def vector_of(label: str) -> tuple[int, ...] | None:
    """The exponent vector a label names (`label_of`), None for a name that is no point's."""
    words = label.split()
    if len(words) < 2 or words[0] != "point":
        return None
    try:
        return tuple(int(word) for word in words[1:])
    except ValueError:
        return None
