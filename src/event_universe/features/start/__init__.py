"""The start (ALGEBRA.md #the-generator (g), the start): a held family's rest under its own line at the paces its reads give it, its own level among the content (Every row reads the content, [the paces](#the-paces)), with the sum's sources per proper volume and per proper interval (The write per proper volume and per proper interval): the static condition of the row's own step and write, (6 (den - num) p_0^2 + 6 num p_i^2) a = num p_i^2 S_6(a) + 3 den Gamma^2 sigma with p_0 the clock and p_i = p_0^2 / Gamma the Node's pace at the content c the row reads (its own level among it; the composed paces, core/paces.py), sigma the source scaled by the write's factor at the same paces (`paces.write_factor`, two proper-interval powers on a count, one on a Wronskian, no tension at the start so the three axes' paces are the Node's), 6 den a = num S_6(a) + 3 den sigma where the content is 0, at a fine unit derived from the width, the division act iterated from nothing until the levels repeat (its first repeat its fixed point, the sources of either sign or both), the levels the nearest integers by the division act, the remainder at the half wall, the division's origin (the write's remainder starts at half its wall too); the Link unit cancels from the rest, so it is the same at every G."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import NO_READ, Reads, coefficients, rule3

Pair = tuple[int, int]
SignReads = tuple[tuple[int, int], ...]  # a holder of the sign's reads of the content holders
Sourced = tuple[np.ndarray, Pair, int, int, SignReads]  # counts, pair, level weight, rest, reads


class RestCollapses(ValueError):
    """The rest's refusal by name where the content reaches the Link's zero at a Node under the row's own level, the row's pace rounded to 0, a frozen clock (ALGEBRA.md #the-paces, Every row reads the content; The paces compose: under the composed paces no finite count within the width's reach meets it); the generator reads it to widen a body's first lay or to refuse the body (tools/pixel_mode.py)."""


@dataclass(frozen=True)
class FieldAtRest:
    """The held field at rest: the levels (the nearest integers), the fine levels at the unit, the unit, the iterations to the repeat, the level's remainder at the half wall and the row's own content the paces were read at."""

    levels: np.ndarray
    fine: np.ndarray
    unit: int
    iterations: int
    remainder: int
    content: np.ndarray  # the row's own level its paces were read at: the levels where the rest settled, one off at a rounding tie


def division(numerator: object, wall: object, value: object) -> np.ndarray:
    """Rule3's division act on a value: (numerator x value) div wall, the remainder not kept (ALGEBRA.md #the-four-acts)."""
    return np.asarray(rule3(NO_READ, NO_READ, numerator, wall, value, 0, 0)[0])


def arrivals(a: np.ndarray, wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The six arrivals as Rule3 reads them, the two of each axis summed: the wrap on a periodic axis, 0 beyond a face, the Node itself on a folded axis (core/ports.py)."""
    return tuple(arrival(a, axis, 1, wrap) + arrival(a, axis, -1, wrap) for axis in range(3))


def unit_of(counts: np.ndarray, pair: Pair, level_weight: int, width: int, gamma: int) -> int:
    """The fine unit, derived from the width and never written: the largest unit at which num p_i^2 S_6 of the rest stays inside the host's width, or inside the file's where the host's leaves none (so that a file wider than the host lays the same levels, the rest's own fixed point within the roundings' floor, and only widens the room), p_i^2 at most Gamma^2 under the guard, the rest's bound the larger of the counts and the tent of the whole source over the longest extent (half of 3 x the source total over the level weight times the extent); refused by name where the width leaves no unit."""
    tent = int(division(3 * int(np.abs(counts).sum()) * (max(counts.shape) + 1), 2 * level_weight, 1))
    largest = max(int(np.abs(counts).max()), tent + 1)
    bound = 2 * 2 * abs(pair[0]) * 6 * largest * gamma * gamma
    unit = int(division(1, bound, min(width, MAX_WORK_INT))) or int(division(1, bound, width))
    if unit < 1:
        raise ValueError(
            f"the width {width} leaves no fine unit for the rest of the pair {list(pair)} under a source of "
            f"{int(np.abs(counts).sum())} at Gamma = {gamma} (ALGEBRA.md #the-bound)"
        )
    return unit


def settled(
    fine: np.ndarray, reads: Reads, divisor: Any, source: Any, wrap: Wrap, iterations: int
) -> tuple[np.ndarray, int]:
    """The line at fixed paces, b <- (SUM over the three axes of read x the two arrivals + source) div divisor, iterated by the division act to its fixed point, the first state the act returns unchanged; where the act cycles (the floors of a line at the massless pair can swing between two states), the cycle's elementwise highest state is a floor of the line, from which the act, monotone in the levels, only rises to a fixed point, so the iteration goes on from it; refused by name where it cycles again."""

    def act(state: np.ndarray) -> np.ndarray:
        return np.asarray(rule3(reads, arrivals(state, wrap), 0, divisor, state, 0, source)[0])

    seen: set[int] = set()
    resolved = 0
    while True:
        iterations += 1
        after = act(fine)
        if np.array_equal(after, fine):
            return fine, iterations
        key = hash(after.tobytes())
        if key in seen:  # a cycle, or a hash's collision: collect it within the states seen
            highest, state, length = after, act(after), 1
            while not np.array_equal(state, after) and length < len(seen):
                highest, state, length = np.maximum(highest, state), act(state), length + 1
            if np.array_equal(state, after):
                if resolved:
                    raise ValueError(
                        f"the rest does not settle: the line cycles again after {iterations} iterations"
                    )
                iterations += length
                fine, seen, resolved = highest, set(), resolved + 1
                continue
        seen.add(key)
        fine = after


def scaled_source(source: np.ndarray, clock: Any, pace: Any, gamma: int, intervals: int) -> np.ndarray:
    """The rest's source scaled as the write scales it, per proper volume and per proper interval at the Node's paces (`paces.write_factor`): the three axes' paces the Node's pace p_i, no tension standing at the start, the clock p_0, `intervals` proper-interval powers (2 on a count, 1 on a Wronskian); the product in Python's integers, exact beyond the width, back in the source's kind (the scaled source never above the source in a hollow)."""
    wide = np.asarray(source, dtype=object)
    found = paces.write_factor(wide, pace, pace, pace, clock, gamma, intervals)
    return np.asarray(found).astype(source.dtype)


def rest(
    counts: np.ndarray,
    pair: Pair,
    wrap: Wrap,
    level_weight: int,
    width: int,
    wall: int,
    gamma: int,
    others: np.ndarray | int = 0,
    intervals: int = 2,
) -> FieldAtRest:
    """The rest by the line itself at the row's own paces: the fine levels b <- (num p_i^2 S_6(b) + Gamma^2 x 3 den x (count x unit div E_s) x the write's factor) div (6 (den - num) p_0^2 + 6 num p_i^2), E_s the row's level weight, the paces from the content the row reads, `others` the other holders' levels and the row's own level b div unit among them (Every row reads the content), the source scaled per proper volume and per proper interval at those paces as the write scales it, `intervals` the proper-interval powers of the source's kind, 2 on a count and 1 on a Wronskian (`paces.write_factor`; The write per proper volume and per proper interval), by Rule3's division act from nothing, the line at the paces of the row's own level as last rounded iterated to its fixed point and the paces re-read from it until the levels repeat the content they were read at (a repeat of an earlier state a rounding tie, the content then one unit off at that Node), the remainder at the half of `wall`, the wall of the rule the row steps by; the sources of either sign or both (the iteration converges wherever the board has a sink); refused by name where a board periodic on its every axis at [1, 1] with no Node beyond it gives the sources no sink, where the level weight is below 1, and where the content reaches the Link's zero at a Node, the row's own pace rounded to 0, the rest collapsing (a frozen clock, ALGEBRA.md #the-paces)."""
    num, den = pair
    if level_weight < 1:
        raise ValueError(f"the start's level weight is from 1, got {level_weight}")
    long = [axis for axis in range(len(counts.shape)) if counts.shape[axis] > 1]
    closed = all(wrap[axis] for axis in long) and wrap.beyond is None
    if num == den and closed and bool(counts.any()):
        raise ValueError(
            f"the sum's rest needs a sink: a board periodic on every axis at [1, 1] has no rest under the "
            f"source total {int(counts.sum())}"
        )
    unit = unit_of(counts, pair, level_weight, width, gamma)
    source = division(3 * den * unit, level_weight, counts) * gamma * gamma
    half = int(division(1, 2, unit))
    fine, own, iterations, seen = np.zeros_like(counts), np.zeros_like(counts), 0, set()
    while True:  # the outer pass: the paces from the row's own level as last rounded
        content = others + own
        clock, pace = paces.node_paces(gamma, content)
        if bool((pace <= 0).any()):
            raise RestCollapses(
                f"the rest of the pair {list(pair)} collapses: the content reaches the Link's zero "
                f"{paces.frozen_content(gamma)} at a Node after {iterations} iterations, the row's own pace "
                "rounded to 0 (a frozen clock; ALGEBRA.md #the-paces, Every row reads the content)"
            )
        reads = (num * pace * pace,) * 3
        divisor = 6 * (den - num) * clock * clock + 6 * num * pace * pace
        scaled = scaled_source(source, clock, pace, gamma, intervals)
        fine, iterations = settled(fine, reads, divisor, scaled, wrap, iterations)
        rounded = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half)[0])
        if np.array_equal(rounded, own) or (key := rounded.tobytes()) in seen:
            break  # the levels repeat the content they were read at, or an earlier state: a rounding tie
        seen.add(key)
        own = rounded
    levels = rounded
    return FieldAtRest(levels, fine, unit, iterations, int(division(1, 2, wall - 1)), own)


def settled_rows(
    rows: Sequence[Sourced], wrap: Wrap, width: int, gamma: int, unit: int
) -> list[FieldAtRest]:
    """Every holder of the content at its rest under its sources, each reading its own level and the other holders' among the content (Every row reads the content, ALGEBRA.md #the-paces): the rows' rests taken in turn, each at the others' levels as last found with their rests and its own rest among them (`rest`), until every row's levels repeat (or the rows together repeat an earlier state: a rounding tie, the first repeat the start), the remainder of each at the half wall of the rule the row steps by, w = 6 den Gamma^2 G^2; the engine's start and the generator share it."""
    levels = [np.zeros_like(row[0]) for row in rows]
    fields: list[FieldAtRest] = []
    seen: set[bytes] = set()
    while (key := b"".join(level.tobytes() for level in levels)) not in seen:
        seen.add(key)
        fields, moved = [], False
        for number, (counts, pair, level_weight, own_rest, _reads) in enumerate(rows):
            others: Any = own_rest
            for other, (level, row) in enumerate(zip(levels, rows, strict=True)):
                if other != number:
                    others = others + level + row[3]
            wall = coefficients(pair[0], pair[1], gamma, gamma, gamma, None, unit)[2]
            field = rest(counts, pair, wrap, level_weight, width, wall, gamma, others)
            moved = moved or not np.array_equal(field.levels, levels[number])
            levels[number] = field.levels
            fields.append(field)
        if not moved:
            break
    return fields


def held_rests(
    holders: Sequence[Sourced], signs: Sequence[Sourced], wrap: Wrap, width: int, gamma: int, unit: int
) -> list[FieldAtRest]:
    """Every held row at its rest, the engine's start (ALGEBRA.md #the-generator (g), the start): the holders of the content together, each its own level and the others' among its content (`settled_rows`), then each holder of the sign at the rest of its line under the content it reads, its reads naming the content holders by their position with their weights, the rests among the levels, its Wronskian source carrying one proper-interval power where a count carries two; the fields in the holders' order and then the signs'."""
    fields = settled_rows(holders, wrap, width, gamma, unit)
    for counts, pair, level_weight, own_rest, reads in signs:
        content: Any = own_rest
        for position, weight in reads:
            content = content + weight * (fields[position].levels + holders[position][3])
        wall = coefficients(pair[0], pair[1], gamma, gamma, gamma, None, unit)[2]
        fields.append(rest(counts, pair, wrap, level_weight, width, wall, gamma, content, 1))
    return fields
