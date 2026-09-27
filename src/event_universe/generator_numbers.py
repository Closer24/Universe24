"""The numbers a generator writes into the files for the engine to read (a host module).

The engine's loader computes no float (the integer rule, the model owner's record
2071; tests/test_integer_algebra.py), so the roundings that ALGEBRA.md names as
written once from a declared pair are computed here, by the generators, and
written into the world file and the universe file under the stamp: the twist
"own" of a body's record and of a given record (ALGEBRA.md #the-primitives: round(2^16 omega_0),
the key `twist` on every body and every emitter, BUILD.md section 26 item 73) and
the nearest Pythagorean triple of an angle for the twist table (ALGEBRA.md #the-transport, #the-primitives; examples/events/make_universe.py). The loader reads the integers and
checks what integers can check (the table's identities, bound and order).
"""

from __future__ import annotations

import math
from fractions import Fraction

from event_universe.loader.world import TWIST_TRIPLE_BOUND, TWIST_UNIT_SCALE


def twist_triple(k: int, unit: int) -> tuple[int, int, int]:
    """THE NEAREST TRIPLE of the angle k / unit radians (ALGEBRA.md #the-transport, #the-primitives; the generator's procedure): n / m nearest tan(angle / 2) with m at most
    the root of the d bound, the triple (m^2 - n^2, 2 m n, m^2 + n^2) in lowest terms,
    (1, 0, 1) at angle 0. HOST, at the generation; the loader checks the identities,
    the bound and the angles' order."""
    ratio = Fraction(math.tan(k / (2 * unit))).limit_denominator(math.isqrt(TWIST_TRIPLE_BOUND))
    n, m = ratio.numerator, ratio.denominator
    c, s, d = m * m - n * n, 2 * m * n, m * m + n * n
    g = math.gcd(math.gcd(c, s), d)
    return c // g, s // g, d // g


def rotation_twist(cosine_numerator: int, cosine_denominator: int) -> int:
    """THE TWIST "OWN" of a record (ALGEBRA.md #the-primitives): round(2^16 omega_0), omega_0
    the record's rest rotation in radians per interval, cos omega_0 the pair's num / den
    (a matter record's pair) or a / (2 b) of a body's clock [a, b] (2 cos omega); the
    generator's one computation (HOST), an integer the loader reads under `twist`."""
    return round(TWIST_UNIT_SCALE * math.acos(cosine_numerator / cosine_denominator))


def light_twist(wavelength: int) -> int:
    """THE TWIST "OWN" of a light record from its wavelength in Links on light's dispersion
    (ALGEBRA.md #the-primitives): cos omega = (cos(2 pi / lambda) + 2) / 3, round(2^16 omega);
    the retired train's (HISTORY since commit 7)."""
    return round(TWIST_UNIT_SCALE * math.acos((math.cos(2 * math.pi / wavelength) + 2) / 3))


def body_twist(clock: list[int] | tuple[int, int] | None, kind: list[int] | tuple[int, int]) -> int:
    """A body's own record's twist "own" (ALGEBRA.md #the-primitives): its mode's rotation where
    the body is seeded on its mode (`clock` [a, b], 2 cos omega = a / b), else its kind's rest
    rotation on a massive kind (den > num), else 0 (light's kind [1, 1] and a raised pair)."""
    if clock is not None:
        return rotation_twist(int(clock[0]), 2 * int(clock[1]))
    if int(kind[1]) > int(kind[0]):
        return rotation_twist(int(kind[0]), int(kind[1]))
    return 0


def emitter_twist(
    given_pair: list[int] | tuple[int, int] | None, body_clock: list[int] | tuple[int, int] | None
) -> int:
    """A given record's twist "own" (ALGEBRA.md #the-primitives): a massive kind's
    rest rotation from the emitter's own `pair` (a body giving its own family), else the
    emitting body's own rotation where the window writes it (its `clock`), else 0."""
    if given_pair is not None and int(given_pair[1]) > int(given_pair[0]):
        return rotation_twist(int(given_pair[0]), int(given_pair[1]))
    if body_clock is not None:
        return rotation_twist(int(body_clock[0]), 2 * int(body_clock[1]))
    return 0
