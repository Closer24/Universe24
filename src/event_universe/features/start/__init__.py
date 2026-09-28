"""The start (ALGEBRA.md #the-generator, the (g) row, THE START; #the-stable-body): a held family's levels around the bodies under its own line at the pace 1, the line's exact rest under the hold to the nearest integer: on a chain in one pass in integers, on a box a guess refined on the exact residual and certified in whole integers by the exit-time bound; the clamp iterated from nothing by the division act, monotone to its fixed point, is the same rest on a small board and the reference; the loop starts every held family from it, never from zeros (the transient rings); the generator reads it from here."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, replace
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import arrival
from event_universe.core.register import Declaration
from event_universe.core.rule3 import rule3

NO_READ = (0, 0, 0)  # the line with no read
PORTS, SIGNS, TERMS = 6, 2, 2  # a Node's six Ports; a level's two signs; the line's two terms
Wrap = tuple[bool, bool, bool]
Pair = tuple[int, int]
PERIODIC: Wrap = (True, True, True)


@dataclass(frozen=True)
class FieldAtRest:
    """The held field at rest around the body under its family's pair: the levels (the nearest integers), the fine levels at the derived unit, the unit, the iterations to the repeat and the cycle's length, 1 at a fixed point (ALGEBRA.md #the-generator (g)). THE REST OF THE REMAINDERS (`remainder`, `carries`): the level's remainder at the half wall (the division act's unbiased origin) and the hold's carries over the source Nodes, j E_s div N for the j-th of N: a steady source stream from the first interval (at 0 the first units arrive together after E_s div count intervals while the faces drain from the first, and the second-order rule keeps the deficit as a velocity of the whole field)"""

    levels: np.ndarray
    fine: np.ndarray
    unit: int
    iterations: int
    cycle: int
    remainder: int = 0
    carries: np.ndarray | None = None


def check_counts(counts: np.ndarray, gamma: int) -> None:
    """The refusals by name: the counts an int64 array of nonnegative integers below Gamma, at least one nonzero (ALGEBRA.md #the-paces, the guard's lower side)."""
    if counts.dtype != np.int64 or counts.size == 0 or not counts.any():
        raise ValueError("the counts are an int64 array (integers only), not zero everywhere: no body")
    low, high = int(counts.min()), int(counts.max())
    if low < 0 or high >= gamma:
        raise ValueError(f"a count {low if low < 0 else high}: the counts stay in [0, Gamma = {gamma})")


def division(numerator_coefficient: Any, wall: Any, level: np.ndarray) -> np.ndarray:
    """Rule3's division act on a level: (coefficient x level) div wall, the line with no read, the coefficient as the self coefficient and the remainder not kept (ALGEBRA.md #the-four-acts)."""
    return np.asarray(rule3(NO_READ, NO_READ, numerator_coefficient, wall, level, 0, 0)[0])


def axis_arrivals(a: np.ndarray, axis: int, wrap: Wrap) -> np.ndarray:
    """The two neighbours' levels summed along one axis at every Node, each read through its Port (core/ports.py `arrival`): the row itself twice on an axis of one layer, 0 beyond a closed face (the receive of ALGEBRA.md #the-line)."""
    return np.asarray(arrival(a, axis, 1, wrap[axis]) + arrival(a, axis, -1, wrap[axis]))


def arrivals(a: np.ndarray, wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The six arrivals as Rule3 reads them, one sum per axis."""
    return tuple(axis_arrivals(a, axis, wrap) for axis in range(3))


def field_unit(counts: np.ndarray, num: int, reach: int = 0) -> int:
    """The field's fine unit, derived and never written: the largest scale of the levels at which num S_6 stays inside the integer width with room, the width div (2 x 6 num x the largest level's size), the largest level the largest count or the rest's own bound `reach` where the rest rises above the counts (the sum's tent)."""
    largest = max(int(np.abs(counts).max()), reach)
    return int(division(1, SIGNS * PORTS * num * largest, np.array(MAX_WORK_INT, dtype=object)))


def field_at_rest(counts: np.ndarray, pair: Pair, wrap: Wrap = PERIODIC) -> FieldAtRest:
    """The held family's field at rest under its own line at the pace 1 (ALGEBRA.md #the-line; #the-generator (g)): a stands where 6 den a = num S_6(a), so from nothing b <- num S_6(b) div (6 den) by Rule3's division act on the levels at the fine unit (the counts times the unit at the body's Nodes, rewritten each time: the hold); the map is monotone from nothing, so the levels rise to a fixed point, the stop at its first repeat (exact, no tolerance); the fixed point is below the line's own by less than one fine unit per Node, so the levels, the nearest integers by the division act, are the rest within one unit."""
    check_counts(counts, 1 + int(counts.max()))
    num, den = pair
    if num < 1 or den < num:
        raise ValueError(f"the field's pair [{num}, {den}] has num from 1 and den from num")
    unit = field_unit(counts, num)
    hold = counts > 0
    fine = np.zeros(counts.shape, dtype=np.int64)
    seen: dict[bytes, int] = {}
    step = 0
    key = hashlib.sha256(fine.tobytes()).digest()
    while key not in seen:
        seen[key] = step
        fine = np.asarray(rule3((num, num, num), arrivals(fine, wrap), 0, 6 * den, fine, 0, 0, 1)[0])
        fine[hold] = counts[hold] * unit
        step += 1
        key = hashlib.sha256(fine.tobytes()).digest()
    half = int(division(1, 2, np.array(unit, dtype=object)))
    levels = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half, 1)[0])
    return FieldAtRest(levels, fine, unit, step, step - seen[key])


def chain_axis(counts: np.ndarray) -> int | None:
    """The one axis of extent above one where the other two are folded (a chain), else None."""
    long = [axis for axis in range(3) if counts.shape[axis] > 1]
    return long[0] if len(long) == 1 else None


def chain_rest(counts: np.ndarray, pair: Pair, wrap: Wrap) -> FieldAtRest:
    """The rest on a chain in one pass (ALGEBRA.md #the-generator, THE START): the fixed point of the clamp's map, 6 den b_i = num (b_(i-1) + b_(i+1) + 4 b_i) between the bodies' Nodes with the counts times the unit at them and 0 beyond an open face, solved exactly in integers segment by segment (the tridiagonal line of the same map: the segment's determinants p_k = d p_(k-1) - num^2 p_(k-2) with d = 6 den - 4 num, the Node's value the division act N_i div p_s with N_i = L num^i p_(s-i) + R num^(s+1-i) p_(i-1) from the two ends L and R), the levels then the nearest integers by the division act; the clamp's fixed point, bit for bit."""
    check_counts(np.abs(counts), 1 + int(np.abs(counts).max()))  # a signed family's counts by size
    num, den = pair
    if num < 1 or den < num:
        raise ValueError(f"the field's pair [{num}, {den}] has num from 1 and den from num")
    axis = chain_axis(counts)
    if axis is None:
        raise ValueError("the one-pass rest is the chain's: two axes of extent one")
    unit = field_unit(counts, num)
    line = np.moveaxis(counts, axis, 0).reshape(-1)
    extent = int(line.shape[0])
    bodies = [i for i, c in enumerate(line) if c != 0]
    diagonal = 6 * den - 4 * num
    fine_values = [int(c) * unit for c in line]  # the counts times the unit at the bodies, 0 between

    def solve(nodes: list[int], left: int, right: int) -> None:
        """One free segment between two known values: the determinants' recurrence, then one exact division per Node by the division act."""
        size = len(nodes)
        if size == 0:
            return
        determinants = [1, diagonal]
        powers = [1]
        for _ in range(size + 1):
            determinants.append(diagonal * determinants[-1] - num * num * determinants[-2])
            powers.append(powers[-1] * num)
        for k, node in enumerate(nodes):
            i = k + 1
            numerator = (
                left * powers[i] * determinants[size - i]
                + right * powers[size + 1 - i] * determinants[i - 1]
            )
            fine_values[node] = int(division(numerator, determinants[size], np.array(1, dtype=object)))

    if wrap[axis]:
        for index, start in enumerate(bodies):
            end = bodies[index + 1] if index + 1 < len(bodies) else bodies[0]
            gap = end - start if end > start else end - start + extent
            nodes = []
            for step in range(1, gap):
                node = start + step
                nodes.append(node - extent if node >= extent else node)
            solve(nodes, fine_values[start], fine_values[end])
    else:
        solve(list(range(0, bodies[0])), 0, fine_values[bodies[0]])
        for start, end in zip(bodies, bodies[1:], strict=False):
            solve(list(range(start + 1, end)), fine_values[start], fine_values[end])
        solve(list(range(bodies[-1] + 1, extent)), fine_values[bodies[-1]], 0)
    fine = np.array(fine_values, dtype=np.int64).reshape(np.moveaxis(counts, axis, 0).shape)
    fine = np.moveaxis(fine, 0, axis)
    half = int(division(1, 2, np.array(unit, dtype=object)))
    levels = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half, 1)[0])
    return FieldAtRest(levels, fine, unit, 1, 1)


# THE FAST LANE'S SIZES, every one from the machine's width (the owner's rule: no number of its own): two halves' product times the Nodes' partial sum, and a ratio's half times a vector's half shifted up by the halves' excess over the fixed point, each below 2^ROOM (the sign bit out); the right side's scale, the unit's growth and the margin's room come from the certificate and the GameBoard, inside `box_rest`.
WIDTH = MAX_WORK_INT.bit_length()  # the machine's integer width
ROOM = WIDTH - 1  # the bits below the sign
NODES_BITS = int(division(1, 3, np.array(WIDTH, dtype=object)))  # the lane's Nodes bound, a third
HALF_BITS = (ROOM - NODES_BITS) >> 1  # a vector's low half: two halves' product times the Nodes fits
VECTOR_BITS = HALF_BITS << 1  # the lane's vectors below 2^VECTOR_BITS, their halves below 2^HALF_BITS
RATIO_BITS = (WIDTH + 1) >> 1  # a ratio's fixed point: half the width
RATIO_HALF_BITS = (ROOM + RATIO_BITS - VECTOR_BITS) >> 1  # a ratio's low half: the shifted product fits
STOP, FLOORS = 1 << VECTOR_BITS, 3  # a sweep stops below 2^-VECTOR_BITS; three floors an update


def sizes(vector: np.ndarray) -> int:
    """The largest size in a vector, as a Python integer."""
    if vector.dtype == object:
        return int(max(abs(int(v)) for v in vector.ravel()))
    return int(np.abs(vector).max())


def halves(vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """A machine-integer vector as its high and low halves, v = high x 2^HALF_BITS + low with 0 <= low < 2^HALF_BITS."""
    high = vector >> HALF_BITS
    return high, vector - (high << HALF_BITS)


def exact_dot(a: np.ndarray, b: np.ndarray) -> int:
    """The product of two vectors, exact: in Python integers, or by the halves' partial sums for machine integers below 2^VECTOR_BITS on at most 2^NODES_BITS Nodes."""
    if a.dtype == object or b.dtype == object:
        return int(np.dot(a.astype(object).ravel(), b.astype(object).ravel()))
    a1, a0 = halves(a.ravel())
    b1, b0 = halves(b.ravel())
    top = int(np.dot(a1, b1))
    middle = int(np.dot(a1, b0)) + int(np.dot(a0, b1))
    return (top << VECTOR_BITS) + (middle << HALF_BITS) + int(np.dot(a0, b0))


def scaled(vector: np.ndarray, ratio: int) -> np.ndarray:
    """floor(vector x ratio / 2^RATIO_BITS), the ratio at its fixed point: in Python integers, or for machine integers by the halves of both (four products inside the width, the three floors within three units of the one)."""
    if vector.dtype == object:
        return np.asarray((ratio * vector) >> RATIO_BITS)
    high = ratio >> RATIO_HALF_BITS
    low = ratio - (high << RATIO_HALF_BITS)
    v1, v0 = halves(vector)
    top = (high * v1) << (RATIO_HALF_BITS + HALF_BITS - RATIO_BITS)
    middle = ((high * v0) >> (RATIO_BITS - RATIO_HALF_BITS)) + ((low * v1) >> (RATIO_BITS - HALF_BITS))
    return np.asarray(top + middle + ((low * v0) >> RATIO_BITS))


def line_solver(counts: np.ndarray, pair: Pair, wrap: Wrap) -> tuple[Any, np.ndarray]:
    """The line on the free Nodes, A = 6 den I - num S_6 with the bodies' Nodes and the space beyond an open face held out, solved by conjugate gradients in whole integers (the matrix is symmetric and positive): the products exact, the two ratios of a sweep at a fixed point of RATIO_BITS, the vectors in the machine's integers while they stay below 2^VECTOR_BITS (the fast lane, the right side scaled into its band) and in Python integers otherwise; with the free Nodes' mask. The guess is the solver's, the certificate the integers' (ALGEBRA.md #the-generator, THE START)."""
    num, den = pair
    free = counts == 0
    held = ~free
    cap = int(np.count_nonzero(free)) + 1  # the gradients end within the free Nodes' count, exactly
    bound = 1 << VECTOR_BITS
    # |A v| <= 2 x 6 den |v| (the two terms, the six Ports), a sign's room for a sum of two
    room = int(division(1, SIGNS * TERMS * PORTS * den, np.array(MAX_WORK_INT, dtype=object)))
    fast_lane = counts.size <= 1 << NODES_BITS and bound <= room

    def apply(vector: np.ndarray) -> np.ndarray:
        """A on a vector that is 0 at the bodies' Nodes, 0 kept there, in the vector's own integers."""
        total = np.zeros(vector.shape, dtype=vector.dtype)
        for summed in arrivals(vector, wrap):
            total = total + summed
        out = np.asarray(6 * den * vector - num * total)
        out[held] = 0
        return out

    def sweep_lane(right_side: np.ndarray, narrow: bool) -> np.ndarray | None:
        """One run of the gradients; None where the fast lane would leave its bounds."""
        r = right_side.copy()
        r[held] = 0
        if narrow:
            r = r.astype(np.int64)
        x = np.zeros(counts.shape, dtype=r.dtype)
        p = r.copy()
        rr = exact_dot(r, r)
        floor = sizes(r)
        for sweep in range(cap):
            if rr == 0:
                break
            if narrow and (sizes(p) >= bound or sizes(x) >= bound):
                return None
            ap = apply(p)
            pap = exact_dot(p, ap)
            if pap <= 0:
                break
            alpha = int(division(1, pap, np.array(rr << RATIO_BITS, dtype=object)))
            if narrow and alpha >= 1 << (2 * RATIO_HALF_BITS):
                return None
            x = x + scaled(p, alpha)
            r = r - scaled(ap, alpha)
            if narrow and sizes(r) >= bound:
                return None
            rr_next = exact_dot(r, r)
            size = sizes(r)
            if size <= FLOORS * (sweep + 1) + 1 or size * STOP <= floor:
                break  # the floors' own drift (three units a sweep, one at the start), or a round's worth of the right side
            beta = int(division(1, rr, np.array(rr_next << RATIO_BITS, dtype=object)))
            if narrow and beta >= 1 << (2 * RATIO_HALF_BITS):
                return None
            p = r + scaled(p, beta)
            rr = rr_next
        return x.astype(object)

    def solve(right_side: np.ndarray, bound_bits: int) -> np.ndarray:
        """x with A x = the right side on the free Nodes, to the floors' accuracy; the right side is 0 at the bodies. The fast lane takes the right side scaled by a power of two so that its rise by the inverse's bound (bound_bits, the certificate's) stays below half the lane, one bit lower on every bail; Python integers where the lane cannot hold it."""
        size = sizes(right_side)
        if fast_lane and size > 0:
            shift = VECTOR_BITS - 1 - bound_bits - size.bit_length()
            while (size << shift if shift >= 0 else size >> -shift) >= 1:
                side = right_side << shift if shift >= 0 else right_side >> -shift
                found = sweep_lane(np.asarray(side), True)
                if found is not None:
                    return np.asarray(division(1, 1 << shift, found) if shift >= 0 else found << -shift)
                shift -= 1
        return np.asarray(sweep_lane(right_side, False))

    return solve, free.ravel()


def solved(
    counts: np.ndarray, solver: Any, free: np.ndarray, right: np.ndarray, bound_bits: int
) -> np.ndarray:
    """The line solved for a right side given on the free Nodes, the inverse's bound in bits for the lane's scale; a whole-board array, 0 at the bodies."""
    side = np.zeros(counts.shape, dtype=object)
    side.ravel()[free] = np.asarray(right, dtype=object)
    return np.asarray(solver(side, bound_bits))


def residual(fine: np.ndarray, pair: Pair, wrap: Wrap, free: np.ndarray) -> np.ndarray:
    """The line's exact residual at the free Nodes, 6 den b - num S_6(b) in whole integers (the bodies' values and the 0 beyond an open face read through the Ports as Rule3 reads them)."""
    num, den = pair
    total = np.zeros(fine.shape, dtype=object)
    for summed in arrivals(fine, wrap):
        total = total + summed
    return np.asarray((6 * den * fine - num * total).ravel()[free], dtype=object)


def certified(
    fine: np.ndarray, unit: int, half: int, margin: int, free: np.ndarray
) -> tuple[np.ndarray, bool]:
    """The levels by the division act, and whether every free Node's value stands at least the margin away from the nearest half between two levels: then the nearest integers of the line's exact rest are these, whatever the guess was."""
    levels = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half, 1)[0])
    below = np.asarray(fine - (levels * unit - half)).ravel()[free]
    above = np.asarray((levels * unit + half) - fine).ravel()[free]
    closed = bool((below >= margin).all() and (above > margin).all())
    return levels, closed


def box_rest(counts: np.ndarray, pair: Pair, wrap: Wrap, divisor: int | None = None) -> FieldAtRest:
    """The rest on a box (ALGEBRA.md #the-generator, THE START): the line's exact rest to the nearest integer, certified in integers. The guess is the solver's; each round the exact residual R of the whole-integer field is solved back and taken off; the certificate is the exit-time bound: T solves the same line with 6 den x the lift on the right side, its own exact residual rho makes ||A^-1|| <= ||T|| / (6 den x lift - ||rho||), so the field stands within margin = ||A^-1|| ||R|| of the exact rest; where every free Node is farther than the margin from a half, the levels are the exact rest's nearest integers. Where the certificate does not close, the unit grows once and the rounds repeat; a value still within the margin of a half then rounds up, the half's own side under the division act (the margin added before the act). The cost is the load's. With a divisor the rest is the sum's (the hold's row as a sum, 6 den a - num S_6(a) = 3 den sigma): no Node is clamped, the counts are the weighted sources at the bodies' Nodes, and the line's right side is 3 den x the source x the unit div the divisor at every Node, the residual read against it; the fine unit is derived from the rest's bound as well as the counts (the tent of the whole source over the longest extent, at most half the source total per side times the extent, rises above the counts on a long chain); a board periodic on its every axis at [1, 1] has no sink: under a source total other than 0 it is refused by name, and under the total 0 (a signed family balanced) the rest stands up to a constant, solved with one Node of no source held as the gauge and written at the mean 0."""
    check_counts(np.abs(counts), 1 + int(np.abs(counts).max()))  # a signed family's counts by size
    num, den = pair
    if num < 1 or den < num:
        raise ValueError(f"the field's pair [{num}, {den}] has num from 1 and den from num")
    long = [axis for axis in range(len(wrap)) if counts.shape[axis] > 1]
    closed = divisor is not None and num == den and all(wrap[axis] for axis in long)
    if divisor is not None and (divisor < 1 or (closed and (int(counts.sum()) != 0 or counts.all()))):
        raise ValueError(
            f"the sum's rest needs a divisor from 1 (got {divisor}) and a sink: a board periodic on every axis at [1, 1] rests only under the source total 0 (got {int(counts.sum())}), one Node free"
        )
    clamped = np.zeros(counts.shape, dtype=np.int64) if divisor is not None else counts
    if closed:  # the balanced rest up to a constant: a Node of no source the gauge, the mean taken off
        clamped.ravel()[int(np.flatnonzero(counts.ravel() == 0)[0])] = 1
    solver, free = line_solver(clamped, pair, wrap)
    nodes = int(np.count_nonzero(free))
    ones = np.zeros(counts.shape, dtype=object)
    ones[...] = 6 * den
    # the exit-time field T twice: as it comes, its size the bound's bits; then lifted by the lane's room
    bound_bits = nodes.bit_length()
    rough = solved(counts, solver, free, ones.ravel()[free], bound_bits)
    bound_bits = max(1, sizes(rough.ravel()[free]).bit_length() - (6 * den).bit_length() + 1)
    lift = 1 << max(0, VECTOR_BITS - 1 - bound_bits - (6 * den).bit_length())
    lifted = ones * lift
    exit_time = solved(counts, solver, free, lifted.ravel()[free], bound_bits)
    rho = residual(exit_time, pair, wrap, free) - 6 * den * lift
    bound_wall = 6 * den * lift - sizes(rho)
    if bound_wall <= 0:
        raise ValueError(
            "the exit-time bound did not close: the line's solver is off by more than its lift"
        )
    bound_top = sizes(exit_time.ravel()[free])
    bound_bits = max(1, bound_top.bit_length() - bound_wall.bit_length() + 1)
    room = nodes * nodes  # the margin far below a half: no accidental near-half over the free Nodes
    tent = 3 * int(np.abs(counts).sum()) * (max(counts.shape) + 1)  # the sum's rest above the counts
    reach = 0 if divisor is None else int(division(tent, 2 * divisor, np.array(1, dtype=object))) + 1
    unit = field_unit(counts, num, reach)
    fine = np.zeros(counts.shape, dtype=object)
    fine[...] = clamped.astype(object) * (0 if divisor is not None else unit)  # the gauge Node at 0
    side = np.zeros(counts.shape, dtype=object)
    if divisor is not None:
        side[...] = division(3 * den * unit, divisor, counts.astype(object))
    side = side.ravel()[free]
    fine = fine + solved(counts, solver, free, side - residual(fine, pair, wrap, free), bound_bits)
    fine = fine - division(1, fine.size, np.array(fine.sum() if closed else 0, dtype=object))
    rounds = 0
    grown = False
    while True:
        half = int(division(1, 2, np.array(unit, dtype=object)))
        floor = None
        while True:  # the rounds end by the certificate: it closes, the margin is far below a half, or the residual stops falling
            rounds += 1
            worst = residual(fine, pair, wrap, free) - side
            size = sizes(worst)
            if floor is not None and 2 * size >= floor:
                break  # the residual at the solver's floor: the rest of the way is the unit's
            floor = size
            margin = int(
                division(1, bound_wall, np.array(bound_top * size + bound_wall - 1, dtype=object))
            )
            levels, closed = certified(fine, unit, half, margin, free)
            if closed:
                return FieldAtRest(levels.astype(np.int64), fine, unit, rounds, 1)
            if margin * room <= half:
                break  # only a half is left uncertified
            fine = fine + solved(counts, solver, free, -worst, bound_bits)
        if grown:
            break  # the one growth taken (ALGEBRA.md, THE START): a value within the margin of a half rounds up
        grown = True
        growth = 1 << max(0, (margin * room).bit_length() - half.bit_length() + 1)  # far below a half
        unit *= growth
        fine = fine * growth
    levels = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half + margin, 1)[0])
    return FieldAtRest(levels.astype(np.int64), fine, unit, rounds, 1)


def rest(
    counts: np.ndarray, pair: Pair, wrap: Wrap = PERIODIC, divisor: int | None = None
) -> FieldAtRest:
    """The start's rest of a held family: with a divisor the sum's rest on the weighted sources by the box's certified solve on any board; else on the counts clamped, the chain's one pass where the region is a chain, the box's certified rest elsewhere (ALGEBRA.md #the-generator, THE START)."""
    if divisor is None and chain_axis(counts) is not None:
        return chain_rest(counts, pair, wrap)
    field = box_rest(counts, pair, wrap, divisor)
    if divisor is None:
        return field
    sources, carries = np.flatnonzero(counts.ravel()), np.zeros(counts.shape, dtype=np.int64)
    carries.ravel()[sources] = division(divisor, len(sources), np.arange(len(sources), dtype=np.int64))
    return replace(field, carries=carries, remainder=int(division(1, 2, np.array(3 * pair[1] - 1))))


DECLARATION = Declaration(
    name="the start",
    place="any",
    reads=("a body's counts at its Nodes", "a family's pair", "the faces"),
    writes=("a family's level at a Node",),
    function=rest,
    section="ALGEBRA.md #the-generator, #the-stable-body",
    word="any",
)
