"""The start's rests, the fixed point of the lay and the rest (ALGEBRA.md #the-generator (g), the start; #what-a-body-is, (a) and (c); features/start): a held row's content from the content holders at the weights its reads name (`read_content`), every holder of the content at its rest under its sources, the rows' rests taken in turn until they repeat (`settled_rows`), and every held row at its rest under the sources the laid records write at those rests, the engine's start (`held_rests`, `Lattice.start`); the rest of one row is features/start `rest`."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import wall_of
from event_universe.features.start import FieldAtRest, SignReads, Sourced, rest, returned

Booked = Callable[[Sequence[np.ndarray]], tuple[list[Sourced], list[Sourced]]]


def read_content(
    reads: SignReads, levels: Sequence[np.ndarray], rests: Sequence[int], own: int | None
) -> tuple[Any, int]:
    """A held row's content at the start from the content holders by position at the weights its reads name (ALGEBRA.md, every family reads the holders its declaration names, at the weights it names): the sum of weight x (the holder's level with its rest) over its reads, the row's own level left out and its weight returned apart (`own` its position among the holders, None for a holder of the sign, which stands outside them and reads none of itself), for the rest to iterate (`rest`); 0 and 0 where it reads nothing."""
    content: Any = 0
    weight = 0
    for position, read in reads:
        content = content + read * rests[position]
        if position == own:
            weight += read
        else:
            content = content + read * levels[position]
    return content, weight


def settled_rows(
    rows: Sequence[Sourced],
    wrap: Wrap,
    width: int,
    gamma: int,
    unit: int,
    seeds: Sequence[FieldAtRest] = (),
    carried: bool = False,
) -> list[FieldAtRest]:
    """Every holder of the content at its rest under its sources, each reading the holders its declaration names at their weights, its own level among them where it names itself (`read_content`; ALGEBRA.md #the-paces): the rows' rests taken in turn, each at the others' levels as last found with their rests (`rest`), until every row's levels repeat the state the pass began from, or the rows together repeat an earlier state one unit off at most, a rounding tie, a return further off refused by name as a cycle (`returned`, the one rule), the remainder of each at the half wall of the rule the row steps by, w = 6 den Gamma^2 G^2; each pass seeds every row's rest with its rest of the pass before (`seeds` those of an earlier call, none in the first), the fixed point the same and reached from nearer; the engine's start and the generator share it; `carried` the world's `uniform: carried`, the rest of a massless row on a board with no sink its zero-mean part (`rest`)."""
    levels = [np.zeros_like(row[0]) for row in rows]
    fields: list[FieldAtRest] = list(seeds)
    seen: dict[bytes, int] = {}
    rests = [own_rest for _counts, _pair, _divisor, own_rest, _reads in rows]
    while True:
        began, fields, before = list(levels), [], fields
        for number, (counts, pair, divisor, _own_rest, reads) in enumerate(rows):
            others, own_weight = read_content(reads, levels, rests, number)
            wall = wall_of(pair[1], gamma, unit)
            seed = before[number] if number < len(before) else None
            field = rest(
                counts,
                pair,
                wrap,
                divisor,
                width,
                wall,
                gamma,
                others,
                intervals=paces.COUNT_POWER,
                own_weight=own_weight,
                seed=seed,
                carried=carried,
            )
            levels[number] = field.levels
            fields.append(field)
        if returned(
            levels,
            began,
            seen,
            f"the holders of the content, the pairs {[list(row[1]) for row in rows]},",
        ):
            return fields


def held_rests(
    booked: Booked,
    seed: Sequence[np.ndarray],
    wrap: Wrap,
    width: int,
    gamma: int,
    unit: int,
    carried: bool = False,
) -> list[FieldAtRest]:
    """Every held row at its rest under the sources the laid records write at those rests, the engine's start (ALGEBRA.md #the-generator (g), the start; #what-a-body-is, (a) the body stands where the sources return themselves and (c) the well, D_i div T each interval, is the record's quanta as the fields' source): the lay and the rest iterated to the fixed point. `booked` books every held row's source at the held rows' levels it is given, the holders of the content first and then the holders of the sign, each the booking the held write's write takes at those paces (the form of every laid record for a row of the content and its Wronskian for the holder of the sign, scaled per proper volume and per proper interval at the sourcing family's paces, over the write's wall E_s T); the holders of the content rest together under it (`settled_rows`), then each holder of the sign at the rest of its line under the content it reads, its reads naming the content holders by their position with their weights, the rests among the levels and none of its own level (`read_content`), its Wronskian source carrying one proper-interval power where a count carries two; the levels found are booked again until they repeat the state they were booked at, the fixed point, or an earlier state two units off at most at every Node, a rounding tie of the composed map, one unit per division act, the rest's and the booking's (`returned`, the one rule), a return further off refused by name as a cycle; `seed` the levels the first booking reads, nothing (0 at every Node) in the engine, never the result; `carried` the world's `uniform: carried`, every massless row's rest on a board with no sink its zero-mean part, the holders' and the signs' alike (`rest`); the fields in the holders' order and then the signs'."""
    levels, fields = list(seed), list[FieldAtRest]()
    seen: dict[bytes, int] = {}
    while True:
        holders, signs = booked(levels)
        before, fields = (
            fields,
            settled_rows(holders, wrap, width, gamma, unit, fields[: len(holders)], carried),
        )
        rests = [own_rest for _counts, _pair, _divisor, own_rest, _reads in holders]
        for number, (counts, pair, divisor, _own_rest, reads) in enumerate(signs, len(holders)):
            content, own_weight = read_content(reads, [field.levels for field in fields], rests, None)
            wall = wall_of(pair[1], gamma, unit)
            seeded = before[number] if number < len(before) else None
            fields.append(
                rest(
                    counts,
                    pair,
                    wrap,
                    divisor,
                    width,
                    wall,
                    gamma,
                    content,
                    intervals=paces.WRONSKIAN_POWER,
                    own_weight=own_weight,
                    seed=seeded,
                    carried=carried,
                )
            )
        found = [field.levels for field in fields]
        name = f"the lay and the rest of {len(holders)} holders and {len(signs)} signs"
        if returned(
            found, levels, seen, name, 2
        ):  # two division acts composed: the rest's and the booking's
            return fields
        levels = found
