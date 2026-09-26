"""The hold: a body's writes into a held family at its Nodes, the count whole at the time part, the vector and tensor parts factor x count x n_a (x n_b) div W (div W^2) with the remainder carried, the dipole sigma (D x e_j)_i div its divisor at the six neighbours, every division Rule3's division act (ALGEBRA.md 9.117 the row "the hold", 9.91 (3), 9.119 item 2); the read from the rule, the write a load."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from event_universe.core.register import Declaration
from event_universe.core.rule3 import (
    ACTS,
    THE_ADVANCE,
    THE_INVERSE,
    THE_LOAD,
    THE_UNHOLD,
    Key,
    carried,
    division_back,
)
from event_universe.core.rule3 import (
    THE_REWRITE as THE_REWRITE,
)

COUNT_WORDS = ("content", "sign")
TENSOR_AXES = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
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


def booking(factor: int, count: int, momentum: Vector, axes: tuple[int, ...]) -> int:
    """The part's numerator, the booking of the count's level and the momentum's level per axis with the declared held factor, a reading with declared coefficients (ALGEBRA.md 9.119 item 1 (e)); its wall the declared W to the power of the momentum factors."""
    found = factor * count
    for axis in axes:
        found *= momentum[axis]
    return found


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
            part = index + k
            if start.act != THE_UNHOLD:
                now, before = carried(
                    start.act,
                    (part,),
                    booking(term.factors[group], start.count, start.momentum, axes),
                    start.wall ** len(axes),
                    values,
                    carries,
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
                    amount = (
                        sigma * sign * start.vector[component]
                    )  # the unit coefficient times the moment's level
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
