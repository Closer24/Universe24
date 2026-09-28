"""The recoil into the body's record's phase (ALGEBRA.md #the-primitives, the row "the recoil"): at the close the body's own record turns by delta k = sigma_a x (k_q div M) per Link along each axis with a tally, k_q the quantum's wave number in the twist's unit (the generator's reading `wave_number` of the mode, no key), M the body's count, the division one act of the write per axis (features/write, the fifth instance, the angle's remainder carried at the body; Rule3's carried division when none is handed), the taker +1 and the giver -1; at every Node of the body the record's two time levels (now, before) turn by the table's triple of delta k x the Node's offset from the body's centre, the rotation act of the transport on the pair (now, quad) with quad = (cos omega_b now - before) / sin omega_b, 2 cos omega_b = a / b the mode's clock and sin omega_b = isqrt(4 b^2 - a^2) / (2 b), two of Rule3's read acts to the nearest unit over the wall 2 sin d (no remainder kept: d changes with the angle, as the transport's); the momentum n is a reading of the record's current and no level; no wall L, no store, nothing declared."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from math import isqrt

from event_universe.core.register import Declaration
from event_universe.core.rule3 import THE_ADVANCE, Key, carried, rule3

TAKING = 1
GIVING = -1

# the word of ALGEBRA.md #the-primitives for this primitive
THE_WORD = (
    "from the rule ALGEBRA.md #the-line and the click, the angle's remainder of the division on the body"
)
Triple = tuple[int, int, int]
Counts = tuple[tuple[Key, int], ...]
Levels = tuple[tuple[Key, int, int], ...]
# the write's line (features/write): (act, wall, coefficient, the counts per key, values, carries) ->
# per key (key, now, before), the remainders written back into the two dicts
WriteLine = Callable[[str, int, int, Counts, dict[Key, int], dict[Key, int]], Levels]


@dataclass(frozen=True)
class RecoilTerm:
    """The click's declaration: the quantum's wave number k_q in the twist's unit, the body's count M, the body's mode clock [a, b] (2 cos omega_b = a / b), the sense (a taking +1, a giving -1) and the twist table's reading, the triple of an angle in the twist's unit along an axis (refused by name beyond the table)."""

    wave_number: int
    quanta: int
    clock: tuple[int, int]
    sense: int
    triple_of: Callable[[int, int], Triple]


@dataclass(frozen=True)
class RecoilStart:
    """What the click booked: the tally per axis; the record's two levels at the body's Nodes in one order and, per axis, each Node's offset from the body's centre; the write's line the loop hands (features/write; None: the folder's carried division)."""

    tally: tuple[int, int, int]
    levels: tuple[tuple[int, ...], tuple[int, ...]]
    offsets: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]
    write: WriteLine | None = None


@dataclass(frozen=True)
class RecoilOwn:
    """The body's remainders of the angle's division per axis: the value and the carry of every carried division by its key, the axis."""

    values: Mapping[Key, int]
    carries: Mapping[Key, int]


@dataclass(frozen=True)
class RecoilWrites:
    """The record's two levels at the body's Nodes after the turn, the turn delta k per axis (the phase per Link, in the twist's unit) and the body's remainders after."""

    levels: tuple[tuple[int, ...], tuple[int, ...]]
    turn: tuple[int, int, int]
    own: RecoilOwn


def sign_of(value: int) -> int:
    """sigma: -1, 0 or 1, the direction of travel and never the size (ALGEBRA.md #the-primitives)."""
    return (value > 0) - (value < 0)


def carried_line(
    act: str,
    wall: int,
    coefficient: int,
    counts: Counts,
    values: dict[Key, int],
    carries: dict[Key, int],
) -> Levels:
    """The write's line by Rule3's carried division alone, per key (coefficient x count + r) div wall with the remainder at the key: the folder's own when the loop hands no write, the same arithmetic features/write wraps."""
    return tuple(
        (key, *carried(act, key, coefficient * count, wall, values, carries)) for key, count in counts
    )


def sine_of(clock: tuple[int, int]) -> int:
    """2 b sin omega_b as the integer square root of 4 b^2 - a^2 from the mode's clock [a, b] (2 cos omega_b = a / b), from 1 on a rotation; refused by name where the clock is no rotation (b from 1, |a| below 2 b)."""
    a, b = clock
    if b < 1 or not -2 * b < a < 2 * b:
        raise ValueError(f"the recoil's clock [{a}, {b}] is no rotation: b from 1 and |a| below 2 b")
    return isqrt(4 * b * b - a * a)


def turned(
    levels: tuple[int, int], triple: Triple, clock: tuple[int, int], sine: int
) -> tuple[int, int]:
    """The record's two time levels at one Node turned by the triple (C, S, d): (now, quad) rotated with quad = (cos omega_b now - before) / sin omega_b and before' = cos omega_b now' - sin omega_b quad', as two of Rule3's read acts to the nearest unit over the wall 2 sin d with the load sin d, sin = 2 b sin omega_b and a = 2 b cos omega_b the clock's integers: now' = ((C sin - S a) now + 2 b S before) / (sin d), before' = (-2 b S now + (C sin + S a) before) / (sin d), the determinant one (ALGEBRA.md #the-transport, the recoil's row)."""
    now, before = levels
    cosine, sinus, d = triple
    a, b = clock
    wall = sine * d
    now_after, _ = rule3(
        (2 * (cosine * sine - sinus * a), 4 * b * sinus, 0), (now, before, 0), 0, 2 * wall, 0, 0, wall
    )
    before_after, _ = rule3(
        (-4 * b * sinus, 2 * (cosine * sine + sinus * a), 0), (now, before, 0), 0, 2 * wall, 0, 0, wall
    )
    return int(now_after), int(before_after)


def check(term: RecoilTerm, start: RecoilStart) -> None:
    """The refusals by name: the wave number from 0, the count from 1, the sense +1 or -1, the two levels and the three offsets over the same Nodes."""
    if term.wave_number < 0 or term.quanta < 1:
        raise ValueError(
            f"the recoil needs a wave number from 0 and a count from 1, got k_q = {term.wave_number}, M = {term.quanta}"
        )
    if term.sense not in (TAKING, GIVING):
        raise ValueError(f"the recoil's sense is +1 (a taking) or -1 (a giving), got {term.sense}")
    nodes = len(start.levels[0])
    if len(start.levels[1]) != nodes or any(len(axis) != nodes for axis in start.offsets):
        raise ValueError(
            f"the recoil's levels and offsets are over the body's Nodes alike, got {nodes}, {len(start.levels[1])} and {[len(axis) for axis in start.offsets]}"
        )


def apply(term: RecoilTerm, start: RecoilStart, own: RecoilOwn) -> RecoilWrites:
    """The primitive: per axis with a tally, delta k = (sense x sigma_a x k_q + r) div M by one act of the write's line at the advance (the axis its key, the angle's remainder carried), then at every Node of the body the two levels turned by the table's triple of delta k x the Node's offset along that axis; nothing on an axis without a tally, nothing at the centre (the angle 0, the identity) (ALGEBRA.md #the-primitives, the rows "the recoil" and "the write", #the-transport)."""
    check(term, start)
    sine = sine_of(term.clock)
    values, carries = dict(own.values), dict(own.carries)
    line = start.write if start.write is not None else carried_line
    now, before = list(start.levels[0]), list(start.levels[1])
    turn = [0, 0, 0]
    for axis in range(3):
        sign = term.sense * sign_of(start.tally[axis])
        if sign == 0:
            continue
        counts: Counts = (((axis,), sign * term.wave_number),)
        ((_, delta, _),) = line(THE_ADVANCE, term.quanta, 1, counts, values, carries)
        turn[axis] = delta
        if delta == 0:
            continue
        for index, offset in enumerate(start.offsets[axis]):
            if offset == 0:
                continue
            triple = term.triple_of(delta * offset, axis)
            now[index], before[index] = turned((now[index], before[index]), triple, term.clock, sine)
    return RecoilWrites(
        (tuple(now), tuple(before)), (turn[0], turn[1], turn[2]), RecoilOwn(values, carries)
    )


DECLARATION = Declaration(
    name="the recoil",
    place="(iv)",
    reads=(
        "the click's tally (sigma_a, the direction of travel)",
        "the quantum's wave number k_q",
        "the body's count M",
        "the body's mode clock",
        "the twist table",
        "the giving's outward tally with the opposite sign",
    ),
    writes=("a family's level at a Node", "a body's remainders"),
    function=apply,
    section=THE_WORD
    + " (ALGEBRA.md #the-primitives); ALGEBRA.md #the-primitives, the row 'the recoil'; ALGEBRA.md #the-transport, #the-interval",
    word="after the step",
)
