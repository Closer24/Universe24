"""The hold: a body's writes into a held family at its Nodes, the count whole at the time part, the vector and tensor parts factor x count x n_a (x n_b) div W (div W^2) with the remainder carried, the dipole sigma (D x e_j)_i div its divisor at the six neighbours, every division Rule3's division act (ALGEBRA.md 9.117 the row "the hold", 9.91 (3), 9.119 item 2); the read from the rule, the write a load."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.rule3 import rule3

THE_LOAD = "the load"
THE_ADVANCE = "the advance"
THE_REWRITE = "the rewrite"
THE_INVERSE = "the inverse"
THE_UNHOLD = "the unhold"
ACTS = (THE_LOAD, THE_ADVANCE, THE_REWRITE, THE_INVERSE, THE_UNHOLD)
COUNT_WORDS = ("content", "sign")
NO_READ = (0, 0, 0)
TENSOR_AXES = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
Key = tuple[object, ...]
Vector = tuple[int, int, int]


@dataclass(frozen=True)
class HoldTerm:
    """The held family's row: the count word (content or sign), the parts per group (the time part, the vector, the tensor), the factor per group, the dipole's vector (spin, moment or None) and its divisor."""

    count: str
    parts: tuple[int, ...]
    factors: tuple[int, ...]
    dipole: str | None
    dipole_divisor: int


@dataclass(frozen=True)
class HoldStart:
    """The interval's reading for one body: the act, the body's count (s or Q), its momentum n now, its wall W, its dipole vector (the spin or the moment) or None."""

    act: str
    count: int
    momentum: Vector
    wall: int
    vector: Vector | None


@dataclass(frozen=True)
class HoldOwn:
    """The body's remainders of the hold: the value and the carry of every carried division by its key, a part's index or ("d", i, j, sigma) for a dipole's term."""

    values: Mapping[Key, int]
    carries: Mapping[Key, int]


@dataclass(frozen=True)
class HoldWrites:
    """The writes of one act: the time part's level, per part (its index, now, before), per dipole term ((i, j, sigma), now, before), and the body's remainders after."""

    time_level: int
    parts: tuple[tuple[int, int, int], ...]
    dipoles: tuple[tuple[Vector, int, int], ...]
    own: HoldOwn


def division_forward(numerator: int, wall: int, carry: int) -> tuple[int, int]:
    """Rule3's division act forward: (numerator + carry) div wall and the remainder, the line with no read, the self coefficient the numerator on the level 1 (ALGEBRA.md 9.91 (3))."""
    return rule3(NO_READ, NO_READ, numerator, wall, 1, 0, carry, 1)


def division_back(numerator: int, wall: int, value: int, carry: int) -> tuple[int, int]:
    """The carried division one interval back by Rule3's direction -1: the carry before from (value, carry), then the value before from that carry, exact while the carry stays below the wall (ALGEBRA.md 9.50 (8), 9.91 (3))."""
    _, carry_before = rule3(NO_READ, NO_READ, numerator, wall, 1, value, carry, -1)
    value_before, _ = rule3(NO_READ, NO_READ, numerator, wall, 1, 0, carry_before, -1)
    return value_before, carry_before


# (D x e_j)_i for the axis j, per (i, the component k of D, the sign): D x e_x = (0, D_z, -D_y),
# D x e_y = (-D_z, 0, D_x), D x e_z = (D_y, -D_x, 0) (ALGEBRA.md 9.91 (3))
CROSS_TERMS: tuple[tuple[tuple[int, int, int], ...], ...] = (
    ((1, 2, 1), (2, 1, -1)),
    ((0, 2, -1), (2, 0, 1)),
    ((0, 1, 1), (1, 0, -1)),
)


def check(term: HoldTerm, start: HoldStart) -> None:
    """The refusals by name: the count word, the act, the parts and factors group for group, the wall and the dipole's divisor from 1."""
    if term.count not in COUNT_WORDS:
        raise ValueError(f"the hold's count word is {term.count!r}: one of {list(COUNT_WORDS)}")
    if start.act not in ACTS:
        raise ValueError(f"the hold's act is one of {list(ACTS)}, got {start.act!r}")
    if len(term.parts) != len(term.factors) or not term.parts:
        raise ValueError(
            f"the hold's parts {list(term.parts)} and factors {list(term.factors)} go group for group"
        )
    if start.wall < 1 or term.dipole_divisor < 1:
        raise ValueError(
            f"the hold's wall W = {start.wall} and the dipole's divisor {term.dipole_divisor} are from 1"
        )


def carried(
    act: str, key: Key, numerator: int, wall: int, values: dict[Key, int], carries: dict[Key, int]
) -> tuple[int, int]:
    """One carried division by its act: forward the value of this interval and the last one's (the first value twice at the load), back the state stepped back with the value before it, a rewrite the standing value twice (ALGEBRA.md 9.91 (3))."""
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


def apply(term: HoldTerm, start: HoldStart, own: HoldOwn) -> HoldWrites:
    """The primitive at (iv) for one body and one held family: the count at the time part, every part beyond it by its carried division, the dipole's terms at the six neighbours (ALGEBRA.md 9.117 the row "the hold")."""
    check(term, start)
    values, carries = dict(own.values), dict(own.carries)
    parts: list[tuple[int, int, int]] = []
    index = 0
    for group, count in enumerate(term.parts):
        for k in range(count):
            if group == 0:
                continue
            axes = (k,) if group == 1 else TENSOR_AXES[k]
            numerator = term.factors[group] * start.count
            for axis in axes:
                numerator *= start.momentum[axis]
            part = index + k
            if start.act != THE_UNHOLD:
                now, before = carried(
                    start.act, (part,), numerator, start.wall ** len(axes), values, carries
                )
                parts.append((part, now, before))
        index += count
    dipoles: list[tuple[Vector, int, int]] = []
    if (
        term.dipole is not None
        and len(term.parts) >= 2
        and start.vector is not None
        and any(start.vector)
    ):
        for j in range(3):
            for sigma in (1, -1):
                for i, component, sign in CROSS_TERMS[j]:
                    amount = sigma * sign * start.vector[component]
                    if amount == 0:
                        continue
                    key: Key = ("d", i, j, sigma)
                    if start.act in (THE_ADVANCE, THE_LOAD):
                        now, before = carried(
                            THE_ADVANCE, key, amount, term.dipole_divisor, values, carries
                        )
                    elif start.act == THE_INVERSE:
                        now = values.get(key, 0)
                        before, _ = division_back(amount, term.dipole_divisor, now, carries.get(key, 0))
                    elif start.act == THE_UNHOLD:
                        now = values.get(key, 0)
                        carried(THE_INVERSE, key, amount, term.dipole_divisor, values, carries)
                        before = 0
                    else:
                        continue
                    dipoles.append(((i, j, sigma), now, before))
    return HoldWrites(start.count, tuple(parts), tuple(dipoles), HoldOwn(values, carries))


DECLARATION = Declaration(
    "the hold",
    "(iv)",
    (
        "a body's content M_k",
        "P_0 and P_k",
        "the wall W",
        "a body's momentum n",
        "the held factors",
        "the dipole",
    ),
    ("a family's level at a Node", "a body's remainders"),
    1,
    apply,
    "9.45 (2); 9.91 (3); 9.111 item 3; 9.117 item 3; 9.119 item 2, the row 'the hold'",
    word="the right side",
)


def bind(loop: Any) -> Callable[..., object]:
    """The loop's method `_hold`, whose divisions `apply` gives bit for bit, until the loop calls `apply`."""
    return loop._method("_hold")  # type: ignore[no-any-return]
