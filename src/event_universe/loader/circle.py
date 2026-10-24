"""Den's circle (the owner's word of 2026-10-24, "declaring a family is forbidden; they must emerge by themselves at the click"; ALGEBRA.md, A family's declaration, The circle of den): the universe file holds den and no family row, and the loader derives from den's integers what the engine's internals need, the Pythagorean points num^2 + s^2 = den^2 of the open quadrant (num > 0, s > 0), every one a product of den's Gaussian primes turned into the quadrant by the units, labelled by its exponent vector over den's primes 1 mod 4 and nothing else (`circle_points`, `label_of`): den factored by trial division through its fourth root and Pollard's rho, a cofactor beyond the reach's square a prime by Miller-Rabin's witnesses 2 and 3 (`factored`, `probable_prime`, `rho`), each prime 1 mod 4 split once as a^2 + b^2 with a > b by the search on the square (`features/click.two_squares`, `split`), and for the primes 1 mod 4 with their exponents e_i every vector v with v_i in {-2 e_i, ..., 2 e_i} by twos, the point z = scale x PROD g_i^k_i conj(g_i)^(2 e_i - k_i) with k_i = (v_i + 2 e_i) / 2 and scale the part of den outside those primes (the twos and the primes 3 mod 4, no angle), rotated by i until both legs are positive, so that the vectors and the points of the quadrant correspond one to one (3^n - 1 points for n primes 1 mod 4 each once; 242 at den 53,567,765 = 5 x 17 x 73 x 89 x 97, 26 at the three-prime den of the constants hand) and the vector -v is the point with the legs swapped; the zero vector is the axis (den, 0), the massless point, no row of the circle."""

from __future__ import annotations

from math import gcd

from event_universe.core.rule3 import division_forward
from event_universe.features.click import two_squares

Gauss = tuple[int, int]  # a Gaussian integer a + i b
Point = tuple[tuple[int, ...], int, int]  # a point of the circle: its exponent vector, num and s
WITNESSES = (2, 3)  # Miller-Rabin's witnesses for a cofactor beyond trial division's reach: exact below 1,373,653, probable above


def probable_prime(number: int) -> bool:
    """Whether a number above 1 passes Miller-Rabin at the witnesses 2 and 3 (`WITNESSES`): exact below 1,373,653 and a probable prime above it; `factored` asks it of a cofactor beyond the square of trial division's reach alone, and a false prime there would give den's circle fewer points and no wrong one."""
    if number < 2:
        return False
    for witness in WITNESSES:
        if number % witness == 0:
            return number == witness
    odd, twos = number - 1, 0
    while odd % 2 == 0:
        odd, twos = odd // 2, twos + 1
    for witness in WITNESSES:
        power = pow(witness, odd, number)
        if power in (1, number - 1):
            continue
        for _ in range(twos - 1):
            power = power * power % number
            if power == number - 1:
                break
        else:
            return False
    return True


def rho(number: int) -> int:
    """One proper factor of a composite number by Pollard's rho (Floyd's cycle), the polynomial x^2 + c at c = 1, 2, 3, ... until a factor shows."""
    constant = 1
    while True:
        slow, fast, found = 2, 2, 1
        while found == 1:
            slow = (slow * slow + constant) % number
            fast = (fast * fast + constant) % number
            fast = (fast * fast + constant) % number
            found = gcd(abs(slow - fast), number)
        if found != number:
            return found
        constant += 1


def factored(number: int) -> list[tuple[int, int]]:
    """The prime factorization of a number from 1 as (prime, exponent) pairs in rising order: trial division through the number's fourth root, and through the cofactor's square root while the cofactor stays below the reach's fourth power (a small number factored whole), then every cofactor below the reach's square is prime outright (no factor below the reach, and two above it would pass the square), and a cofactor beyond it is a prime by the witnesses (`probable_prime`) or is split by Pollard's rho (`rho`); at the one universe's den 53,567,765 the reach is 85, the cofactor 89 x 97 split and both exact, and at the constants hand's three-prime den the two lighter primes exact and the heaviest, 132,260,701, by the witnesses."""
    found: dict[int, int] = {}
    rest, trial = number, 2
    while trial * trial <= rest and (trial**4 <= number or rest < trial**4):
        while rest % trial == 0:
            found[trial], rest = found.get(trial, 0) + 1, rest // trial
        trial += 1 if trial == 2 else 2
    stack = [rest] if rest > 1 else []
    while stack:
        rest = stack.pop()
        if rest < trial * trial or probable_prime(rest):
            found[rest] = found.get(rest, 0) + 1
            continue
        part = rho(rest)
        stack += [part, rest // part]
    return sorted(found.items())


def split(prime: int) -> Gauss:
    """A prime 1 mod 4 as a^2 + b^2 with a > b > 0, the Gaussian prime a + i b above it (Fermat), by the search on the square (`features/click.two_squares`)."""
    pair = two_squares(prime)
    assert pair is not None and pair[1] > 0, f"{prime} is no prime 1 mod 4"
    return pair


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
    """Den's primes 1 mod 4 with their exponents, the ones that carry an angle, and the scale, den's part outside them (the twos and the primes 3 mod 4), which carries none."""
    primes = [(prime, power) for prime, power in factored(den) if prime % 4 == 1]
    scale = den
    for prime, power in primes:
        scale = int(division_forward(scale, prime**power, 0)[0])
    return primes, scale


def circle_points(den: int) -> list[Point]:
    """Every point of den's circle in the open quadrant with its exponent vector over den's primes 1 mod 4 (the module's sentence), in the vectors' order; none where den has no prime 1 mod 4."""
    primes, scale = angled(den)
    vectors: list[tuple[int, ...]] = [()]
    for _prime, power in primes:
        vectors = [v + (step,) for v in vectors for step in range(-2 * power, 2 * power + 1, 2)]
    found = []
    for vector in vectors:
        if not any(vector):
            continue  # the axis, the massless point (den, 0)
        point: Gauss = (scale, 0)
        for (prime, power), step in zip(primes, vector, strict=True):
            gauss = split(prime)
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


def label_of(vector: tuple[int, ...]) -> str:
    """A point's label, read from its integers alone: the word point and its exponents over den's primes 1 mod 4 in rising order, "point -2 2 2 -2 2" the least leg's at den 53,567,765."""
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
