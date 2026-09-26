"""The carried division, Rule3's division act with the remainder kept between intervals: forward the act, backward the direction -1, and the five acts a body's writer names (ALGEBRA.md 9.91 (3), 9.50 (8), 9.119 item 1)."""

from __future__ import annotations

from event_universe.core.rule3 import rule3

THE_LOAD = "the load"
THE_ADVANCE = "the advance"
THE_REWRITE = "the rewrite"
THE_INVERSE = "the inverse"
THE_UNHOLD = "the unhold"
ACTS = (THE_LOAD, THE_ADVANCE, THE_REWRITE, THE_INVERSE, THE_UNHOLD)
NO_READ = (0, 0, 0)
Key = tuple[object, ...]


def division_forward(numerator: int, wall: int, carry: int) -> tuple[int, int]:
    """Rule3's division act forward: (numerator + carry) div wall and the remainder, the line with no read and the numerator as the self coefficient on the level 1 (ALGEBRA.md 9.91 (3))."""
    return rule3(NO_READ, NO_READ, numerator, wall, 1, 0, carry, 1)


def division_back(numerator: int, wall: int, value: int, carry: int) -> tuple[int, int]:
    """The carried division one interval back by Rule3's direction -1: the carry before from (value, carry), then the value before from that carry as the ceiling form, exact while the carry stays below the wall (ALGEBRA.md 9.50 (8), 9.91 (3))."""
    _, carry_before = rule3(NO_READ, NO_READ, numerator, wall, 1, value, carry, -1)
    value_before, _ = rule3(NO_READ, NO_READ, numerator, wall, 1, 0, carry_before, -1)
    return value_before, carry_before


def carried(
    act: str, key: Key, numerator: int, wall: int, values: dict[Key, int], carries: dict[Key, int]
) -> tuple[int, int]:
    """One carried division by its act on the body's remainders: forward the value of this interval and the last one's (the first value twice at the load), back the state stepped back with the value before it, a rewrite the standing value twice (ALGEBRA.md 9.91 (3))."""
    if act == THE_INVERSE:
        value, carry = division_back(numerator, wall, values.get(key, 0), carries.get(key, 0))
        values[key], carries[key] = value, carry
        before, _ = division_back(numerator, wall, value, carry)
        return value, before
    if act in (THE_ADVANCE, THE_LOAD):
        previous = values.get(key)
        value, carry = division_forward(numerator, wall, carries.get(key, 0))
        values[key], carries[key] = value, carry
        return value, value if previous is None else previous
    value = values.get(key, 0)
    return value, value
