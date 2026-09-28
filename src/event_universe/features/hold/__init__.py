"""The hold: a body's writes into a held family at its Nodes, the count a source into the field's line ((count + r) div the row's divisor E_s added at the time part each interval, the remainder carried), the vector and tensor parts factor x count x n_a (x n_b) div (E_s W) (div (E_s W^2)) with the remainder carried, at a body in the law's form per Node with the count declared there, the dipole sigma (D x e_j)_i div its divisor at the six neighbours, every division one act of the write (features/write, the line the loop hands in the start; Rule3's carried division per key when none is handed) (ALGEBRA.md #the-primitives the rows "the hold" and "the write", ALGEBRA.md #the-interval, #the-four-acts)."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

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
from event_universe.core.schema import Integer, ListOf, ObjectOf, OneOf, Schema

COUNT_WORDS = ("content", "sign")
TIME_PART: Key = (0,)  # the time part's key on the body's remainders, the source's carried division
TENSOR_AXES = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
Vector = tuple[int, int, int]
Counts = tuple[tuple[Key, int], ...]
Levels = tuple[tuple[Key, int, int], ...]
# the write's line (features/write): (act, wall, coefficient, the counts per key, values, carries) ->
# per key (key, now, before), the remainders written back into the two dicts
WriteLine = Callable[[str, int, int, Counts, dict[Key, int], dict[Key, int]], Levels]


@dataclass(frozen=True)
class HoldTerm:
    """The held family's row: the count word (content or sign), the parts per group (the time part, the vector, the tensor), the factor per group, the dipole's vector (spin, moment or None) and its divisor, and the source's divisor E_s."""

    count: str
    parts: tuple[int, ...]
    factors: tuple[int, ...]
    dipole: str | None
    dipole_divisor: int
    divisor: int


@dataclass(frozen=True)
class HoldStart:
    """The interval's reading for one body: the act, the body's count (s or Q), its momentum n now, its wall W, its dipole vector (the spin or the moment) or None."""

    act: str
    count: int
    momentum: Vector
    wall: int
    vector: Vector | None
    nodes: tuple[tuple[Key, int], ...] = ()  # a body in the law's form: per Node its key and its count
    write: WriteLine | None = (
        None  # the write's line the loop hands (features/write); None: `carried_line`
    )


@dataclass(frozen=True)
class HoldOwn:
    """The body's remainders of the hold: the value and the carry of every carried division by its key, a part's index or ("d", i, j, sigma) for a dipole's term."""

    values: Mapping[Key, int]
    carries: Mapping[Key, int]


@dataclass(frozen=True)
class HoldWrites:
    """The writes of one act: the time part's increment of this interval ((count + r) div E_s at the advance, the one subtracted at the inverse, 0 at the load and at a rewrite), per part (its index, the Node's key at a body in the law's form or None for the whole body, now, before), per dipole term ((i, j, sigma), now, before), and the body's remainders after."""

    time_level: int
    parts: tuple[tuple[int, Key | None, int, int], ...]
    dipoles: tuple[tuple[Vector, int, int], ...]
    own: HoldOwn
    node_levels: tuple[tuple[Key, int], ...] = ()  # the time part's increment per Node of the law's form


# (D x e_j)_i for the axis j, per (i, the component k of D, the sign): D x e_x = (0, D_z, -D_y),
# D x e_y = (-D_z, 0, D_x), D x e_z = (D_y, -D_x, 0) (ALGEBRA.md #the-interval)
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
    if term.divisor < 1:
        raise ValueError(f"the hold's divisor E_s is from 1, got {term.divisor}")


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


def booking(factor: int, count: int, momentum: Vector, axes: tuple[int, ...]) -> int:
    """The part's numerator, the booking of the count's level and the momentum's level per axis with the declared held factor, a reading with declared coefficients (ALGEBRA.md #the-four-acts); its wall the row's divisor E_s times the declared W to the power of the momentum factors."""
    found = factor * count
    for axis in axes:
        found *= momentum[axis]
    return found


def apply(term: HoldTerm, start: HoldStart, own: HoldOwn) -> HoldWrites:
    """The primitive at (iv) for one body and one held family: the count a source at the time part (its carried division over E_s this interval's increment), every part beyond it by its carried division, the dipole's terms at the six neighbours, every division one act of the write's line (ALGEBRA.md #the-primitives the rows "the hold" and "the write")."""
    check(term, start)
    values, carries = dict(own.values), dict(own.carries)
    line = start.write if start.write is not None else carried_line
    increments = time_increments(
        start.act, ((TIME_PART, start.count), *start.nodes), term.divisor, values, carries, line
    )
    time_level = increments[TIME_PART]
    node_levels = tuple((key, increments[key]) for key, _ in start.nodes)
    parts: list[tuple[int, Key | None, int, int]] = []
    index = 0
    # the vector and tensor parts over the row's divisor E_s as the time part, the source one tensor at
    # one scale (ALGEBRA.md the row "the hold"): at a body in the law's form per Node with the count
    # declared there, else the whole body's count at every Node
    sources: tuple[tuple[Key | None, int], ...] = (
        tuple((key, count) for key, count in start.nodes) if start.nodes else ((None, start.count),)
    )
    for group, count in enumerate(term.parts):
        if group > 0 and start.act != THE_UNHOLD:
            entries: list[tuple[int, Key | None, Key, int]] = []
            for k in range(count):
                axes = (k,) if group == 1 else TENSOR_AXES[k]
                for node, source in sources:
                    key = (index + k,) if node is None else (index + k, *node[1:])
                    numerator = booking(term.factors[group], source, start.momentum, axes)
                    entries.append((index + k, node, key, numerator))
            wall = term.divisor * start.wall ** (1 if group == 1 else 2)  # E_s W^(the group's axes)
            written = line(
                start.act, wall, 1, tuple((key, n) for _, _, key, n in entries), values, carries
            )
            parts.extend(
                (part, node, now, before)
                for (part, node, _, _), (_, now, before) in zip(entries, written, strict=True)
            )
        index += count
    dipoles: list[tuple[Vector, int, int]] = []
    if (
        term.dipole is not None
        and len(term.parts) >= 2
        and start.vector is not None
        and any(start.vector)
    ):
        terms: list[tuple[Vector, Key, int]] = []
        for j in range(3):
            for sigma in (1, -1):
                for i, component, sign in CROSS_TERMS[j]:
                    amount = (
                        sigma * sign * start.vector[component]
                    )  # the unit coefficient times the moment's level
                    if amount != 0:
                        terms.append(((i, j, sigma), ("d", i, j, sigma), amount))
        counts = tuple((key, amount) for _, key, amount in terms)
        if start.act in (THE_ADVANCE, THE_LOAD):
            written = line(THE_ADVANCE, term.dipole_divisor, 1, counts, values, carries)
            dipoles.extend(
                (term_key, now, before)
                for (term_key, _, _), (_, now, before) in zip(terms, written, strict=True)
            )
        elif start.act == THE_INVERSE:
            for term_key, key, amount in terms:
                now = values.get(key, 0)
                before, _ = division_back(amount, term.dipole_divisor, now, carries.get(key, 0))
                dipoles.append((term_key, now, before))
        elif start.act == THE_UNHOLD:
            standing = [values.get(key, 0) for _, key, _ in terms]
            line(THE_INVERSE, term.dipole_divisor, 1, counts, values, carries)
            dipoles.extend(
                (term_key, now, 0) for (term_key, _, _), now in zip(terms, standing, strict=True)
            )
    return HoldWrites(time_level, tuple(parts), tuple(dipoles), HoldOwn(values, carries), node_levels)


def time_increments(
    act: str,
    counts: Counts,
    divisor: int,
    values: dict[Key, int],
    carries: dict[Key, int],
    line: WriteLine,
) -> dict[Key, int]:
    """The time part's increment per source under its key by one act of the write's line: (count + r) div E_s by the carried division at the advance, the one subtracted at the inverse (the store stepped back), 0 at the load (the store's first division, no increment written: the rest holds the sources) and at a rewrite."""
    if act == THE_INVERSE:
        standing = {key: values.get(key, 0) for key, _ in counts}
        line(THE_INVERSE, divisor, 1, counts, values, carries)
        return standing
    if act == THE_ADVANCE:
        return {key: now for key, now, _ in line(THE_ADVANCE, divisor, 1, counts, values, carries)}
    if act == THE_LOAD:
        line(THE_LOAD, divisor, 1, counts, values, carries)
    return {key: 0 for key, _ in counts}


DECLARATION = Declaration(
    name="the hold",
    place="(iv)",
    reads=(
        "a body's content M_k",
        "the row's divisor E_s",
        "P_0 and P_k",
        "the wall W",
        "a body's momentum n",
        "the held factors",
        "the dipole",
    ),
    writes=("a family's level at a Node", "a body's remainders"),
    function=apply,
    section="ALGEBRA.md #the-counts-line, #the-interval, #the-primitives, #the-four-acts, the row 'the hold'",
    word="the right side",
    schema=Schema(
        {
            "a family's entry": ObjectOf(
                {
                    "held": ObjectOf(
                        {
                            "count": OneOf(("content", "sign")),
                            "factors": ListOf(Integer(least=1)),
                            "divisor": Integer(least=1),
                            "dipole": OneOf(("spin", "moment")),
                            "dipole_div": Integer(least=1),
                        },
                        frozenset({"dipole", "dipole_div"}),
                    )
                },
                frozenset({"held"}),
            )
        }
    ),
)
