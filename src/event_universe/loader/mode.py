"""The body's mode as the loader reads it (ALGEBRA.md #the-primitives, the recoil's row): the period P_body by the one-Node rule from the mode's clock pair, never declared; the mode file's check comes here when the tool writes it."""

from __future__ import annotations

from collections.abc import Mapping

from event_universe.core.rule3 import NO_READ, rule3

Levels = tuple[tuple[int, ...], tuple[int, ...]]


def period_by_the_rule(a: int, b: int) -> int:
    """The period by the one-Node Rule3 with the pair, b c_next + r' = a c_now - b c_before + r from (c_before, c_now) = (2 b, a) at the pair's own unit b, each interval one call of rule3: the first t with a negative c before it, c_t >= 0 and 4 b c_t^2 >= (2 b + a) c_before_0^2, the nearest integer to 2 pi / omega with no pi. The horizon is the pair's own: the sequence itself counts the first quarter turn (the first negative c) and a turn is four quarters, so a clock not back within four quarters, each an interval longer than the first for the rounding, is refused by name; no number of the loader's own (ALGEBRA.md #the-generator, #the-primitives the recoil's row: P_body never declared)."""
    if b < 1 or not -2 * b < a < 2 * b:
        raise ValueError(f"the clock [{a}, {b}] is no rotation: b from 1 and |a| below 2 b")
    before, now, carry = 2 * b * b, a * b, 0
    start = before
    quarter = 1 if now < 0 else 0  # the interval of the first negative c, the first quarter turn
    t = 0
    while quarter == 0 or t < 4 * (quarter + 1):
        t += 1
        if quarter and now >= 0 and 4 * b * now * now >= (2 * b + a) * start * start:
            return t
        before, (now, carry) = now, rule3(NO_READ, NO_READ, a, b, now, before, carry)
        if now < 0 and quarter == 0:
            quarter = t + 1
    raise ValueError(
        f"the clock [{a}, {b}] is not back within {t} intervals, four quarter turns of its first ({quarter} intervals) and one interval each"
    )


def moving_levels(
    moving: object, clock: tuple[int, int] | None, count: int, label: str, bound: int
) -> Levels | None:
    """A moving body's two levels from the mode file's `moving` entry, `now` and `before` (ALGEBRA.md #the-generator (e)), each one integer per Node in x-major order, not all zero, within the amplitude bound and the clock's denominator; None where the entry carries no levels (a resting body's are its profile); every defect refused by name."""
    if not isinstance(moving, Mapping) or "now" not in moving:
        return None
    found: list[tuple[int, ...]] = []
    for word in ("now", "before"):
        values = moving.get(word)
        if (
            not isinstance(values, list)
            or len(values) != count
            or any(type(v) is not int for v in values)
        ):
            raise ValueError(
                f"{label}.moving.{word} must be {count} integers, one per Node in x-major order"
            )
        level = tuple(int(v) for v in values)
        amplitude = max(abs(v) for v in level)
        if amplitude == 0:
            raise ValueError(f"{label}.moving.{word} must not be all zero")
        if amplitude > bound:
            raise ValueError(
                f"{label}.moving.{word}'s amplitude {amplitude} is above the amplitude bound {bound}"
            )
        if clock is None or clock[1] < amplitude:
            raise ValueError(
                f"{label}.moving.{word} needs the clock [a, b] beside it with b at least {amplitude}"
            )
        found.append(level)
    return found[0], found[1]
