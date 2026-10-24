"""The charge per quantum of the sign holder's readers (ALGEBRA.md, The constants: the charge is the Wronskian per quantum and the sign's reader is Pythagorean, the owner's words of 2026-10-24): each reader's Wronskian enters the holder's one write times 3 T den over its own count unit W_c sin omega_0 = 3 T den sin omega_0 (`derived.count_wall`), one over the sine, so that every quantum of every family writes T / 2 per count (`charge_factors`: the readers' units brought to one wall by their least common multiple as the tension lines' dens are, the factors and the multiple reduced once by their common divisor, a massless reader's factor the multiple itself); a reader whose sine is irrational is refused by name (`pythagorean_readers`), as the conversion refuses it from every exact list (ALGEBRA.md 180); the former behaviour of 236e74ed0 (the count unit rounded once, the lcm of units sharing no structure) kept by name as its defect."""

from __future__ import annotations

from math import gcd

from event_universe.core.ports import PORTS, SIDES
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.loader.derived import FamilyRule, count_wall, readers_of


def pythagorean_readers(families: tuple[FamilyRule, ...], index: int) -> None:
    """The sign's reader is Pythagorean (the owner's word of 2026-10-24, (ii), "closed"; ALGEBRA.md, The constants): a reader of the holder of the sign `index` writes its charge per quantum by its count unit, exact for a Pythagorean pair alone; a reader with an irrational sine is refused by name, as the conversion refuses it from every exact list (ALGEBRA.md, The conversion, 180), the sentence naming the reader, its pair and its den^2 - num^2; a massless reader (num = den) carries its Wronskian as before. The former behaviour of 236e74ed0, the count unit rounded once and the readers' units brought to one wall by their lcm, kept by name as its defect."""
    holder = families[index]
    for other in readers_of(families, index):
        num, den = families[other].pair
        gap = den * den - num * num
        if (
            families[other].plane and abs(num) != den and largest_below(gap) ** 2 != gap
        ):  # a real-line reader is refused as no plane (loader/universe)
            raise ValueError(
                f"{families[other].name!r} reads the holder of the sign {holder.name!r} with the pair "
                f"[{num}, {den}], whose sine is irrational (den^2 - num^2 = {gap}, no square): a reader of "
                "the sign writes its charge per quantum by its count unit, exact for a Pythagorean pair "
                "alone; a reader with an irrational sine is refused, as the conversion refuses it from every "
                "exact list (ALGEBRA.md, The conversion, 180; The constants, the owner's word of 2026-10-24; "
                "the rounded count unit and the lcm of 236e74ed0 the former behaviour, kept by name as its defect)"
            )


def charge_factors(
    families: tuple[FamilyRule, ...], index: int, action: int
) -> tuple[dict[int, int], int]:
    """The sign holder's readers' charge factors and the walls' charge multiple (ALGEBRA.md, The constants, 2026-10-24): per reader with a gap 3 T den over its count unit, the units brought to their least common multiple by the division act on the greatest common divisor, the factors and the multiple reduced once by their common divisor; a massless reader's factor the multiple itself; the readers Pythagorean first (`pythagorean_readers`), so that every unit is 3 T times an integer sine and the multiple stays within the den."""
    pythagorean_readers(families, index)
    sources = readers_of(families, index)
    units = {
        other: count_wall(families[other], action)
        for other in sources
        if abs(families[other].pair[0]) != families[other].pair[1]
    }
    charge = 1
    for unit_of_one in units.values():
        charge = int(division_forward(charge * unit_of_one, gcd(charge, unit_of_one), 0)[0])
    factors = {
        other: 3 * action * families[other].pair[1] * int(division_forward(charge, units[other], 0)[0])
        if other in units
        else charge
        for other in sources
    }
    common = charge
    for factor in factors.values():
        common = gcd(common, factor)
    charge = int(division_forward(charge, common, 0)[0])
    return {
        other: int(division_forward(factor, common, 0)[0]) for other, factor in factors.items()
    }, charge


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
    """A proper factor of the composite n by Pollard's rho (Floyd's cycle on x -> x^2 + c modulo n, the squares by Python's modular power and the common divisor by Euclid's act, `gcd`), the loader's tool for the circle's primes: the constant c counted up from 1 where the cycle closes on n itself."""
    c = 1
    while True:
        x, y, d = 2, 2, 1
        while d == 1:
            x = pow(x, 2, n) + c
            y = pow(pow(y, 2, n) + c, 2, n) + c
            d = gcd(abs(x - y), n)
        if d != n:
            return d
        c += 1


def factors(n: int) -> dict[int, int]:
    """The prime factors of n with their exponents (`is_prime`, `split`), 2 divided out first by the division act."""
    found: dict[int, int] = {}
    while n > 1 and division_forward(n, 2, 0)[1] == 0:
        found[2], n = found.get(2, 0) + 1, int(division_forward(n, 2, 0)[0])
    pending = [n] if n > 1 else []
    while pending:
        m = pending.pop()
        if is_prime(m):
            found[m] = found.get(m, 0) + 1
        else:
            piece = split(m)
            pending += [piece, int(division_forward(m, piece, 0)[0])]
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
            "lightest point, the electron's pair, is not derived (ALGEBRA.md, The one universe)"
        )
    s, num = found[0]
    return num, s
