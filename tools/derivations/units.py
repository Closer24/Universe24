"""The units of count-unit (ALGEBRA.md, the lay by the count and the family's quantum; R8, R162): the family's quantum isqrt(9 T^2 (den^2 - num^2)) = W_c sin omega_0 for a gapped pair and 3 den T for a massless one, and the taker's lay A^2 = isqrt(count^2 T^2 den^2 div (4 laid^2 (den^2 - num^2))) with 2 A^2 sin omega = (count / laid) T per line, by the integer formulas here and by the engine's own functions as the second method.

Usage: `python tools/derivations/units.py` prints them at [4000, 6000] and [2, 3] with T = 32,768 and for light at [6000, 6000].
"""

from __future__ import annotations

import math


def family_quantum(num: int, den: int, action: int) -> int:
    """isqrt(9 T^2 (den^2 - num^2)) for a gapped pair, 3 den T massless."""
    gap = den * den - num * num
    return math.isqrt(9 * action * action * gap) if gap else 3 * den * action


def lay_squared(count: int, laid: int, num: int, den: int, action: int) -> int:
    """A^2 = isqrt(count^2 T^2 den^2 div (4 laid^2 (den^2 - num^2))), the taker's lay of a gapped family."""
    return math.isqrt(
        count * count * action * action * den * den // (4 * laid * laid * (den * den - num * num))
    )


def quanta() -> list[float]:
    """[the matter quantum at [4000, 6000] and T = 32,768, light's at [6000, 6000], A^2 and A at [2, 3] for one count on one line]."""
    squared = lay_squared(1, 1, 2, 3, 32768)
    return [
        family_quantum(4000, 6000, 32768),
        family_quantum(6000, 6000, 32768),
        squared,
        math.isqrt(squared),
    ]


def invariant_per_line() -> list[float]:
    """2 A^2 sin omega over T at [2, 3], one count on one line: 1 to the root's rounding."""
    squared = lay_squared(1, 1, 2, 3, 32768)
    return [2 * squared * math.sqrt(5) / 3 / 32768]


def against_the_engine() -> list[float]:
    """The same four numbers by the engine's own `count_wall` and `click.squared`, the second method; 0 where the engine is not importable here."""
    try:
        from event_universe.features.click import squared
        from event_universe.loader.derived import FamilyRule, count_wall
    except ImportError:
        return [0.0, 0.0, 0.0]

    def family(name: str, pair: tuple[int, int]) -> FamilyRule:
        """A family row holding nothing but its pair, the one field `count_wall` reads."""
        return FamilyRule(name, pair, 1, 1, False, False, False, None, None, 0, ())

    matter, light = family("matter", (4000, 6000)), family("light", (6000, 6000))
    return [count_wall(matter, 32768), count_wall(light, 32768), squared(1, 32768, (2, 3), 1)]


if __name__ == "__main__":
    print("W_c sin omega_0 at [4000, 6000], W_c light, A^2 and A at [2, 3]:", quanta())
    print("2 A^2 sin omega / T:", [round(v, 5) for v in invariant_per_line()])
    print("by the engine:", against_the_engine())
