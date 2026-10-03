"""The start (ALGEBRA.md #the-generator (g), the start; #what-a-body-is, the four lines (a) and (c)): a held family's rest under its own line at the paces its reads give it, its own level among the content (Every row reads the content, [the paces](#the-paces)), with the sum's sources per proper volume and per proper interval (The write per proper volume and per proper interval): the static condition of the row's own step and write, (6 (den - num) p_0^2 + 6 num p_i^2) a = num p_i^2 S_6(a) + 3 den Gamma^2 sigma with p_0 the clock and p_i = p_0^2 / Gamma the Node's pace at the content c the row reads (its own level among it; the composed paces, core/paces.py), sigma the source scaled by the write's factor at the same paces (`paces.write_factor`, two proper-interval powers on a count, one on a Wronskian, no tension at the start so the three axes' paces are the Node's), 6 den a = num S_6(a) + 3 den sigma where the content is 0, at a fine unit derived from the width, the division act iterated from nothing until the levels repeat the state they were read at, the first state the act returns unchanged, and then refined to the line within one fine unit at every Node by the scaled residual (`refined`: the floored iteration's stop lies below the line by up to one fine unit over 1 - rho in the board's lowest mode, rho the row's Jacobi factor, 137 fine units on the open 25-cube at the massless pair; the advisor's finding and remedy, #1563 comments 5958624379 and 5959617991), the paces re-read until the levels repeat the state they were read at, its fixed point, or an earlier state one unit off at most, a rounding tie (a return to an earlier state further off, a cycle, refused by name; the sources of either sign or both), the levels the nearest integers by the division act, the remainder at the half wall, the division's origin (the write's remainder starts at half its wall too); the Link unit cancels from the rest, so it is the same at every G. The engine's start sources every held row by the form of the laid records, the quantity the hold writes each interval (`held_rests`): the lay and the rest iterated to the fixed point where the sources return themselves, under the one rule of the repeat (`returned`); the generator sources its rests by a count in quanta over the row's level weight, the seed of its own lay (tools/pixel_mode.py)."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import NO_READ, Reads, coefficients, rule3

Pair = tuple[int, int]
SignReads = tuple[
    tuple[int, int], ...
]  # a held row's reads of the content holders by position, weighted
# a row's source: its booking, its pair, the booking's wall (the row's level weight E_s on a count in
# quanta, the write's wall E_s T on the hold's booking), its rest and its reads
Sourced = tuple[np.ndarray, Pair, int, int, SignReads]
Booked = Callable[[Sequence[np.ndarray]], tuple[list[Sourced], list[Sourced]]]


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


def tent_of(counts: np.ndarray, divisor: int) -> int:
    """A bound on a rest's levels from its source alone, the tent: the larger of the source over its wall at one Node and the parabola a source spread flat over the longest extent would raise, half of 3 x the source total over the wall times the extent, each plus one (ALGEBRA.md #the-bound). It is the bound of a chain or a slab, whose rest grows with the extent, and loose by 2 (L + 1) for a point source on a board with no folded axis, whose rest peaks near 0.76 of its source over the wall (the mathematician's 249 with the advisor's second, #1572 comments 5968344874 and 5968375224, two hands)."""
    tent = int(division(3 * int(np.abs(counts).sum()) * (max(counts.shape) + 1), 2 * divisor, 1))
    return max(int(division(1, divisor, int(np.abs(counts).max()))) + 1, tent + 1)


def source_bound(counts: np.ndarray, divisor: int) -> int:
    """A bound on a rest's levels on a board open on every axis of more than one Node, the source total over its wall plus one, no number of the engine in it: on the cubic lattice the rest of a point source peaks at 3 G(0) of its source over the wall, G(0) the lattice Green's function at the origin, 0.2527 (Watson's integral), below one third; a screened row (num below den), a face read as 0 and a sink lower it; so the rest of any source at the vacuum's paces stands below the sum of its sources over the wall (the mathematician's 249 with the advisor's second, two hands). On a board with a folded axis the rest is a chain's or a slab's and grows with the extent, and the tent is its bound (`tent_of`)."""
    return int(division(1, divisor, int(np.abs(counts).sum()))) + 1


def unit_from_bound(largest_level: int, pair: Pair, width: int, gamma: int) -> int:
    """The fine unit under a bound on the rest's levels, derived from the width and never written: the largest unit at which num p_i^2 S_6 of a rest within `largest_level` stays inside the host's width, or inside the file's where the host's leaves none (so that a file wider than the host lays the same levels, the rest's own fixed point within the roundings' floor, and only widens the room), p_i^2 at most Gamma^2 under the guard; 0 where the width leaves no unit."""
    bound = 2 * 2 * abs(pair[0]) * 6 * largest_level * gamma * gamma
    return int(division(1, bound, min(width, MAX_WORK_INT))) or int(division(1, bound, width))


def unit_of(
    counts: np.ndarray, pair: Pair, divisor: int, width: int, gamma: int, wrap: Wrap | None = None
) -> int:
    """The fine unit of a row's rest: under the tent where the tent leaves a unit (`tent_of`, every shipped world bit for bit), else, on a board open on every axis of more than one Node (no wrap and no fold there, `wrap` the board's), under the source's own bound (`source_bound`, the room the tent over-bounds by 2 (L + 1), which held the Node clock of the atom's world at a fiftieth of its reach); a periodic axis folds the images of the source onto it and the rest is a slab's, a chain's or the gap's uniform mode, above the bound by 3 to 19 times on the tubes the mathematician solved (260, #1572 comment 5968797010), so the tent stays there; refused by name where both leave none."""
    unit = unit_from_bound(tent_of(counts, divisor), pair, width, gamma)
    long = [axis for axis in range(len(counts.shape)) if counts.shape[axis] > 1]
    open_board = wrap is not None and len(long) == 3 and not any(wrap[axis] for axis in long)
    if not unit and open_board:
        unit = unit_from_bound(source_bound(counts, divisor), pair, width, gamma)
    if unit < 1:
        raise ValueError(
            f"the width {width} leaves no fine unit for the rest of the pair {list(pair)} under a source of "
            f"{int(np.abs(counts).sum())} at Gamma = {gamma} (ALGEBRA.md #the-bound)"
        )
    return unit


def settled(
    fine: np.ndarray, reads: Reads, divisor: Any, source: Any, wrap: Wrap, iterations: int
) -> tuple[np.ndarray, int]:
    """The line at fixed paces, b <- (SUM over the three axes of read x the two arrivals + source) div divisor, iterated by the division act to its fixed point, the first state the act returns unchanged (the line's residual then in [0, divisor) at every Node, the state below the line by up to the bound `bound_of` in the lowest mode, which `refined` takes off); where the act cycles (the floors of a line at the massless pair can swing between two states), the cycle's elementwise highest state is a floor of the line, from which the act, monotone in the levels, only rises to a fixed point, so the iteration goes on from it; refused by name where it cycles again."""

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


def bound_of(fine: np.ndarray, wrap: Wrap, reads: Reads, divisor: Any) -> int:
    """The floored iteration's largest miss in fine units, K, a bound of the line's inverse on the unit source (the advisor's finding, #1563 comment 5958624379: the first state the act returns unchanged lies below the line by up to one fine unit over 1 - rho, rho the row's Jacobi factor on the board's lowest mode, (num / den) cos(pi / (n + 1)) on an open n-cube): along the longest open or closed axis of n Nodes, 3 ((n + 2) div 2)^2 + 1, at or above the top 3 (n + 1)^2 / 4 of the parabola 3 x (n + 1 - x), which the massless line at the vacuum's paces returns at or above the unit source at every Node (at every pace the six reads sum to at most the divisor, 6 num p_i^2 <= 6 (den - num) p_0^2 + 6 num p_i^2, so the inverse's row sums are at most that line's, and a face or an inner face read as 0 only lowers them); where every axis of more than one Node wraps, the pair's gap alone is the sink, W div (W - 6 R) + 1 at the Node where it is largest (den over den - num at the vacuum); the smaller where both hold; where neither holds and an inner face is the sink (`Wrap.beyond`), the longest axis's parabola, the face a wall somewhere along it; refused by name where no face at all bounds it (a massless row on a board wrapping on every axis needs a sink, which `rest` refuses before)."""
    open_axes = [n for axis, n in enumerate(fine.shape) if n > 1 and not wrap[axis]]
    longest = max(open_axes if open_axes or wrap.beyond is None else fine.shape, default=0) + 1
    half = int(division(1, 2, longest + 1))  # (n + 2) div 2, at or above (n + 1) / 2
    bounds = [3 * half * half + 1] if longest > 1 else []
    gap = divisor - 2 * sum(reads)  # W - 6 R at every Node, 6 (den - num) p_0^2
    if bool((gap > 0).all()):
        bounds.append(int(division(divisor, gap, 1).max()) + 1)
    if not bounds:
        raise ValueError(
            "the rest's miss has no bound: a massless row on a board that wraps on every axis of more than one "
            "Node is sunk by an inner face alone (ALGEBRA.md, The start)"
        )
    return min(bounds)


Correction = tuple[np.ndarray, int]  # a refinement's correction and the scale F it stands at


def refined(
    fine: np.ndarray,
    reads: Reads,
    divisor: Any,
    source: Any,
    wrap: Wrap,
    largest: int,
    unit: int,
    iterations: int,
    seed: Correction | None = None,
) -> tuple[np.ndarray, int, Correction | None]:
    """The rest refined to its line within one level at every Node, the law's rest, by the scaled residual where the stop can miss it, within one fine unit where it is refined (the law's rest is the static solution of the row's line, ALGEBRA.md, The start; the advisor's finding and remedy, #1563 comments 5958624379 and 5959617991, the mathematician's 172 beside it: the floored iteration stops below the line by up to K fine units, `bound_of`, in the board's lowest mode, 137 on the open 25-cube at the massless pair, 9 levels at the row's unit 15 there): the line's residual is read exactly in integers at the stop, rho = SUM over the Ports of read x arrival + source - divisor x b, in [0, divisor) at every Node, the same line is solved for the correction with F rho as its source by the same act to its own stop (`settled` from nothing), delta within K of F times the miss, and the correction is added rounded half up, b + (delta + F div 2) div F; F a power of two, the least at or above 2 K the width admits for the round, else the largest it admits (the act's numerator at most 6 R (2 F B + K) + F |rho| inside half the width's largest integer, B the miss's bound in fine units, K before the first round and 1 + K div F after a round at F), the rounds repeated while F is below 2 K, after which the miss lies in [-1 / 2, 1 / 2 + K / F), within one fine unit; one round on the 25-cube and three on the chain of 128 at the width 63, each round's passes about ln(F K) over 1 - rho from nothing (a Richardson refinement in integers, nothing of the law, every number the width's and the board's); the first round's correction is returned with its scale and seeds the first round of the next call (`seed`, the pass before's correction brought to this round's scale: the floored stop lies the same K below the line at every pass, so the correction barely moves and the act from it stops in a fraction of the passes, the same fixed-point property at the stop whatever the start); refused by name where the width leaves no room for a round. Nothing is refined where the stop is the line itself (the residual 0 at every Node) or where the stop's miss cannot reach half a level, 2 K at or below the unit: the fine levels then lie within half a level of the line and the levels, rounded half up, within one level of it, the law's rest at the stop's own cost (a small body's rest has a large unit, the look's chains and the tests' chain bodies, whose lays stand as before; the 25-cube's bodies, the unit 15 against K 508, and the chain of 128 at the unit 306 against K 12,676 are refined)."""
    found: Correction | None = None
    bound = miss = 0
    six = 2 * sum(int(np.asarray(read).max()) for read in reads)  # 6 R at the largest pace
    while True:
        total = rule3(reads, arrivals(fine, wrap), 0, 1, fine, 0, source)[0]  # the numerator, the wall 1
        residual = np.asarray(total, dtype=object) - np.asarray(divisor, dtype=object) * fine
        residual = residual.astype(fine.dtype)  # within the divisor, the fine levels' kind
        if not residual.any():  # the stop is the line itself: nothing to refine, no bound needed
            return fine, iterations, found
        if not bound:
            bound = miss = bound_of(fine, wrap, reads, divisor)
            if (
                2 * bound <= unit
            ):  # the miss within half a level: the levels within one level of the line
                return fine, iterations, found
        room = int(division(1, 2, largest)) - six * bound
        scales = int(division(1, 2 * six * miss + int(np.abs(residual).max()), room)) if room > 0 else 0
        if scales < 2:
            raise ValueError(
                f"the width {largest} leaves no room for the rest's correction at the miss {miss} with the "
                f"bound {bound} over the six reads {six} (ALGEBRA.md, The start)"
            )
        scale = 1 << min(
            scales.bit_length() - 1, (2 * bound - 1).bit_length()
        )  # the least at 2 K or above
        start = np.zeros_like(fine) if seed is None else division(scale, seed[1], seed[0])
        delta, iterations = settled(start, reads, divisor, scale * residual, wrap, iterations)
        fine = fine + division(1, scale, delta + int(division(1, 2, scale)))
        found, seed = found or (delta, scale), None  # the later rounds correct another residual
        if scale >= 2 * bound:
            return fine, iterations, found
        miss = 1 + int(division(1, scale, bound))


def returned(
    found: Sequence[np.ndarray],
    own: Sequence[np.ndarray],
    seen: dict[bytes, int],
    name: str,
    acts: int = 1,
) -> bool:
    """The one rule of a repeat for every iteration of the start, the levels re-read against the state they were read at: True at the fixed point (the levels repeat the state) and at a rounding tie (an earlier state returns, one unit off at most per division act composed in the map, `acts`, at every Node of every row: the rest's own division alone in `rest`, the rest's and the booking's of the form over its wall in `held_rests`, so two units there, PR #1614's rule generalised to the composed map and no criterion of its own); an earlier state returning further off, a cycle of two states or more, is no rest and is refused by name with the passes made, the cycle's length and the two levels at the Node (about a deep enough source the self-read's swing is not damped); a new state is recorded in `seen` by its pass and False returned."""
    if all(np.array_equal(a, b) for a, b in zip(found, own, strict=True)):
        return True
    if (key := b"".join(level.tobytes() for level in found)) in seen:
        offs = [np.abs(a - b) for a, b in zip(found, own, strict=True)]
        row = max(range(len(offs)), key=lambda number: int(offs[number].max()))
        node = np.unravel_index(int(offs[row].argmax()), offs[row].shape)
        if int(offs[row][node]) <= acts:
            return True
        raise ValueError(
            f"{name} finds no fixed point: the levels re-read return to an earlier state after {len(seen)} "
            f"passes, a cycle of length {len(seen) - seen[key]}, {int(own[row][node])} and "
            f"{int(found[row][node])} at the Node {[int(index) for index in node]} of the row {row}"
        )
    seen[key] = len(seen)
    return False


def scaled_source(source: np.ndarray, clock: Any, pace: Any, gamma: int, intervals: int) -> np.ndarray:
    """The rest's source scaled as the write scales it, per proper volume and per proper interval at the Node's paces (`paces.write_factor`, one rounding, the product exact beyond the width): the three axes' paces the Node's pace p_i, no tension standing at the start, the clock p_0, `intervals` proper-interval powers (2 on a count, 1 on a Wronskian); back in the source's kind (the scaled source never above the source in a hollow)."""
    return np.asarray(paces.write_factor(source, pace, pace, pace, clock, gamma, intervals))


def rest(
    counts: np.ndarray,
    pair: Pair,
    wrap: Wrap,
    divisor: int,
    width: int,
    wall: int,
    gamma: int,
    others: np.ndarray | int = 0,
    intervals: int = 2,
    *,
    own_weight: int,
    seed: FieldAtRest | None = None,
) -> FieldAtRest:
    """The rest by the line itself at the row's own paces: the fine levels b <- (num p_i^2 S_6(b) + Gamma^2 x 3 den x (source x unit div divisor) x the write's factor) div (6 (den - num) p_0^2 + 6 num p_i^2), `divisor` the wall of the source's booking (the row's level weight E_s on a count in quanta, the write's wall E_s T on the form the hold books), the paces from the content the row reads, `others` the other holders' weighted levels with their rests and `own_weight` x the row's own level b div unit among them (the weight its declaration names for itself, 0 where it does not read its own level: the holder of the sign), the source scaled per proper volume and per proper interval at those paces as the write scales it, `intervals` the proper-interval powers of the source's kind, 2 on a count and 1 on a Wronskian (`paces.write_factor`; The write per proper volume and per proper interval), by Rule3's division act from nothing, the line at the paces of the row's own level as last rounded iterated to its fixed point and refined to the line within one fine unit at every Node (`settled`, `refined`), and the paces re-read from it until the levels repeat the content they were read at, the fixed point, or repeat an earlier state one unit off at most at every Node, a rounding tie (the content then one unit off at that Node; a return further off refused by name, `returned`), the remainder at the half of `wall`, the wall of the rule the row steps by; `seed` a rest found before under other sources or paces, the fine levels (at this call's unit) and the content the iteration starts from in place of nothing, the same fixed point reached from nearer (the start's passes seed each row with the pass before, `settled_rows`, `held_rests`), none in a first pass; the sources of either sign or both (the iteration converges wherever the board has a sink); refused by name where a board periodic on its every axis at [1, 1] with no Node beyond it gives the sources no sink, where the divisor is below 1, and where the content reaches the Link's zero at a Node, the row's own pace rounded to 0, the rest collapsing (a frozen clock, ALGEBRA.md #the-paces)."""
    num, den = pair
    if divisor < 1:
        raise ValueError(
            f"the start's divisor, the row's level weight or its write's wall, is from 1, got {divisor}"
        )
    long = [axis for axis in range(len(counts.shape)) if counts.shape[axis] > 1]
    closed = all(wrap[axis] for axis in long) and wrap.beyond is None
    if num == den and closed and bool(counts.any()):
        raise ValueError(
            f"the sum's rest needs a sink: a board periodic on every axis at [1, 1] has no rest under the "
            f"source total {int(counts.sum())}"
        )
    unit, largest = unit_of(counts, pair, divisor, width, gamma, wrap), min(width, MAX_WORK_INT)
    source = division(3 * den * unit, divisor, counts) * gamma * gamma
    half = int(division(1, 2, unit))
    fine, own, iterations = np.zeros_like(counts), np.zeros_like(counts), 0
    correction: Correction | None = None  # the pass before's refinement, the seed of the next
    if seed is not None:
        fine, own = division(unit, seed.unit, seed.fine), seed.content.copy()
    seen: dict[bytes, int] = {}  # every state the paces were read from, by its outer pass
    while True:  # the outer pass: the paces from the row's own level as last rounded
        content = others + own_weight * own
        clock, pace = paces.node_paces(gamma, content)
        if bool((pace <= 0).any()):
            raise RestCollapses(
                f"the rest of the pair {list(pair)} collapses: the content reaches the Link's zero "
                f"{paces.frozen_content(gamma)} at a Node after {iterations} iterations, the row's own pace "
                "rounded to 0 (a frozen clock; ALGEBRA.md #the-paces, Every row reads the content)"
            )
        reads = (num * pace * pace,) * 3
        line_wall = 6 * (den - num) * clock * clock + 6 * num * pace * pace
        scaled = scaled_source(source, clock, pace, gamma, intervals)
        fine, iterations = settled(fine, reads, line_wall, scaled, wrap, iterations)
        fine, iterations, correction = refined(
            fine, reads, line_wall, scaled, wrap, largest, unit, iterations, correction
        )
        rounded = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half)[0])
        if returned([rounded], [own], seen, f"the rest of the pair {list(pair)}"):
            break
        own = rounded
    return FieldAtRest(rounded, fine, unit, iterations, int(division(1, 2, wall - 1)), own)


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
) -> list[FieldAtRest]:
    """Every holder of the content at its rest under its sources, each reading the holders its declaration names at their weights, its own level among them where it names itself (`read_content`; ALGEBRA.md #the-paces): the rows' rests taken in turn, each at the others' levels as last found with their rests (`rest`), until every row's levels repeat the state the pass began from, or the rows together repeat an earlier state one unit off at most, a rounding tie, a return further off refused by name as a cycle (`returned`, the one rule), the remainder of each at the half wall of the rule the row steps by, w = 6 den Gamma^2 G^2; each pass seeds every row's rest with its rest of the pass before (`seeds` those of an earlier call, none in the first), the fixed point the same and reached from nearer; the engine's start and the generator share it."""
    levels = [np.zeros_like(row[0]) for row in rows]
    fields: list[FieldAtRest] = list(seeds)
    seen: dict[bytes, int] = {}
    rests = [row[3] for row in rows]
    while True:
        began, fields, before = list(levels), [], fields
        for number, (counts, pair, divisor, _own_rest, reads) in enumerate(rows):
            others, own_weight = read_content(reads, levels, rests, number)
            wall = coefficients(pair[0], pair[1], gamma, gamma, gamma, None, unit)[2]
            seed = before[number] if number < len(before) else None
            field = rest(
                counts, pair, wrap, divisor, width, wall, gamma, others, own_weight=own_weight, seed=seed
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
    booked: Booked, seed: Sequence[np.ndarray], wrap: Wrap, width: int, gamma: int, unit: int
) -> list[FieldAtRest]:
    """Every held row at its rest under the sources the laid records write at those rests, the engine's start (ALGEBRA.md #the-generator (g), the start; #what-a-body-is, (a) the body stands where the sources return themselves and (c) the well, D_i div T each interval, is the record's quanta as the fields' source): the lay and the rest iterated to the fixed point. `booked` books every held row's source at the held rows' levels it is given, the holders of the content first and then the holders of the sign, each the booking the hold's write takes at those paces (the form of every laid record for a row of the content and its Wronskian for the holder of the sign, scaled per proper volume and per proper interval at the sourcing family's paces, over the write's wall E_s T); the holders of the content rest together under it (`settled_rows`), then each holder of the sign at the rest of its line under the content it reads, its reads naming the content holders by their position with their weights, the rests among the levels and none of its own level (`read_content`), its Wronskian source carrying one proper-interval power where a count carries two; the levels found are booked again until they repeat the state they were booked at, the fixed point, or an earlier state two units off at most at every Node, a rounding tie of the composed map, one unit per division act, the rest's and the booking's (`returned`, the one rule), a return further off refused by name as a cycle; `seed` the levels the first booking reads, nothing (0 at every Node) in the engine, never the result; the fields in the holders' order and then the signs'."""
    levels, fields = list(seed), list[FieldAtRest]()
    seen: dict[bytes, int] = {}
    while True:
        holders, signs = booked(levels)
        before, fields = fields, settled_rows(holders, wrap, width, gamma, unit, fields[: len(holders)])
        rests = [holder[3] for holder in holders]
        for number, (counts, pair, divisor, _own_rest, reads) in enumerate(signs, len(holders)):
            content, own_weight = read_content(reads, [field.levels for field in fields], rests, None)
            wall = coefficients(pair[0], pair[1], gamma, gamma, gamma, None, unit)[2]
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
                    1,
                    own_weight=own_weight,
                    seed=seeded,
                )
            )
        found = [field.levels for field in fields]
        name = f"the lay and the rest of {len(holders)} holders and {len(signs)} signs"
        if returned(
            found, levels, seen, name, 1 + 1
        ):  # two division acts composed: the rest's and the booking's
            return fields
        levels = found
