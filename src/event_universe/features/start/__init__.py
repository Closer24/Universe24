"""The start (ALGEBRA.md #the-generator, the (g) row, THE START; #the-stable-body): a held family's levels around the bodies under its own line at the pace 1, the line's exact rest under the hold to the nearest integer: on a chain in one pass in integers, on a box a guess refined on the exact residual and certified in whole integers by the exit-time bound; the clamp iterated from nothing by the division act, monotone to its fixed point, is the same rest on a small board and the reference; the loop starts every held family from it, never from zeros (the transient rings); the generator reads it from here."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import arrival
from event_universe.core.register import Declaration
from event_universe.core.rule3 import rule3

NO_READ = (0, 0, 0)  # the line with no read
Wrap = tuple[bool, bool, bool]
Pair = tuple[int, int]
PERIODIC: Wrap = (True, True, True)


@dataclass(frozen=True)
class FieldAtRest:
    """The held field at rest around the body under its family's pair: the levels (the nearest integers), the fine levels at the derived unit, the unit, the iterations to the repeat and the cycle's length, 1 at a fixed point (ALGEBRA.md #the-generator (g))."""

    levels: np.ndarray
    fine: np.ndarray
    unit: int
    iterations: int
    cycle: int


def check_counts(counts: np.ndarray, gamma: int) -> None:
    """The refusals by name: the counts an int64 array of nonnegative integers below Gamma, at least one nonzero (ALGEBRA.md #the-paces, the guard's lower side)."""
    if counts.dtype != np.int64 or counts.size == 0 or not counts.any():
        raise ValueError("the counts are an int64 array (integers only), not zero everywhere: no body")
    low, high = int(counts.min()), int(counts.max())
    if low < 0 or high >= gamma:
        raise ValueError(
            f"a count {low if low < 0 else high}: the counts stay in [0, Gamma) with Gamma = {gamma}"
        )


def division(numerator_coefficient: Any, wall: Any, level: np.ndarray) -> np.ndarray:
    """Rule3's division act on a level: (coefficient x level) div wall, the line with no read, the coefficient as the self coefficient and the remainder not kept (ALGEBRA.md #the-four-acts)."""
    return np.asarray(rule3(NO_READ, NO_READ, numerator_coefficient, wall, level, 0, 0)[0])


def axis_arrivals(a: np.ndarray, axis: int, wrap: Wrap) -> np.ndarray:
    """The two neighbours' levels summed along one axis at every Node, each read through its Port (core/ports.py `arrival`): the row itself twice on an axis of one layer, 0 beyond a closed face (the receive of ALGEBRA.md #the-line)."""
    return np.asarray(arrival(a, axis, 1, wrap[axis]) + arrival(a, axis, -1, wrap[axis]))


def arrivals(a: np.ndarray, wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The six arrivals as Rule3 reads them, one sum per axis."""
    return tuple(axis_arrivals(a, axis, wrap) for axis in range(3))


def field_unit(counts: np.ndarray, num: int) -> int:
    """The field's fine unit, derived and never written: the largest scale of the levels at which num S_6 stays inside the integer width with room, the width div (2 x 6 num x the largest count's size)."""
    return int(
        division(1, 2 * 6 * num * int(np.abs(counts).max()), np.array(MAX_WORK_INT, dtype=object))
    )


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
    check_counts(
        np.abs(counts), 1 + int(np.abs(counts).max())
    )  # a signed family's counts by their sizes
    num, den = pair
    if num < 1 or den < num:
        raise ValueError(f"the field's pair [{num}, {den}] has num from 1 and den from num")
    axis = chain_axis(counts)
    if axis is None:
        raise ValueError("the one-pass rest is the chain's: two axes of extent one")
    unit = field_unit(counts, num)
    line = np.moveaxis(counts, axis, 0).reshape(-1)
    extent = int(line.shape[0])
    clamped = [int(c) * unit for c in line]
    bodies = [i for i, c in enumerate(line) if c != 0]
    diagonal = 6 * den - 4 * num
    fine_values = [0] * extent
    for i in bodies:
        fine_values[i] = clamped[i]

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


LIFT = 1 << (6 * 8)  # the right side lifted before a solve, so the floors fall far below it
ROUNDS = 8  # refinements on the exact residual per precision
PRECISION_STEP = 1 << (4 * 8)  # the fine unit's growth where the certificate does not close
PRECISIONS = 2  # the fine unit's growths, one, before a value within the margin of a half rounds up
MARGIN_ROOM = 1 << (
    4 * 4
)  # the rounds end once the margin is 2^16 below a half: only a half is left uncertified
SWEEPS = 8  # the conjugate gradients' cap, times the extents' sum
STOP = 1 << (
    4 * 8 + 8
)  # a sweep stops once the residual is below the right side's 2^-40: a round's worth
VECTOR_BITS = (
    4 * 8 + 8
)  # the fast lane's vectors stay below 2^40, so their halves' products fit the width
HALF_BITS = 4 * 4 + 4  # a vector's low half: 20 bits
RATIO_BITS = 4 * 8  # the fixed point of a ratio between two of the solver's products: 32 bits
RATIO_HALF_BITS = 3 * 8 + 1  # a ratio's low half: 25 bits, its high half then below 2^25
BAND = 1 << (3 * 8 + 6)  # the right side's first band in the fast lane, 2^30; shrunk by a byte on a bail
NODES_BOUND = 1 << (
    4 * 4 + 4
)  # the fast lane's Nodes bound, 2^20: the partial sums of a product fit the width


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
    """The product of two vectors, exact: in Python integers, or by the halves' partial sums for machine integers below 2^VECTOR_BITS on at most NODES_BOUND Nodes."""
    if a.dtype == object or b.dtype == object:
        return int(np.dot(a.astype(object).ravel(), b.astype(object).ravel()))
    a1, a0 = halves(a.ravel())
    b1, b0 = halves(b.ravel())
    top = int(np.dot(a1, b1))
    middle = int(np.dot(a1, b0)) + int(np.dot(a0, b1))
    return (top << (2 * HALF_BITS)) + (middle << HALF_BITS) + int(np.dot(a0, b0))


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
    cap = SWEEPS * int(sum(counts.shape))
    bound = 1 << VECTOR_BITS
    room = int(
        division(1, 4 * 6 * den, np.array(MAX_WORK_INT, dtype=object))
    )  # |v| with A v inside the width
    fast_lane = counts.size <= NODES_BOUND and bound <= room

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
            alpha = (rr << RATIO_BITS) // pap
            if narrow and alpha >= 1 << (2 * RATIO_HALF_BITS):
                return None
            x = x + scaled(p, alpha)
            r = r - scaled(ap, alpha)
            if narrow and sizes(r) >= bound:
                return None
            rr_next = exact_dot(r, r)
            size = sizes(r)
            if size <= 3 * sweep + 4 or size * STOP <= floor:
                break  # the floors' own drift (three units a sweep), or a round's worth of the right side
            beta = (rr_next << RATIO_BITS) // rr
            if narrow and beta >= 1 << (2 * RATIO_HALF_BITS):
                return None
            p = r + scaled(p, beta)
            rr = rr_next
        return x.astype(object)

    def solve(right_side: np.ndarray) -> np.ndarray:
        """x with A x = the right side on the free Nodes, to the floors' accuracy; the right side is 0 at the bodies: the fast lane on the right side scaled into its band, shrunk by a byte on every bail, else Python integers."""
        size = sizes(right_side)
        if fast_lane and size > 0:
            shift = 0
            while (size >> shift) > BAND:
                shift += 1
            while (size >> shift) >= 1 << 8:
                found = sweep_lane(np.asarray(right_side >> shift), True)
                if found is not None:
                    return np.asarray(found << shift)
                shift += 8
        return np.asarray(sweep_lane(right_side, False))

    return solve, free.ravel()


def solved(counts: np.ndarray, solver: Any, free: np.ndarray, right: np.ndarray) -> np.ndarray:
    """The line solved for a right side given on the free Nodes: a small right side lifted by a power of two first and the solution taken down by the division act; a whole-board array, 0 at the bodies."""
    size = sizes(right)
    up = 0
    if size > 0:
        while (size << up) <= BAND >> 1:
            up += 1
    side = np.zeros(counts.shape, dtype=object)
    side.ravel()[free] = np.asarray(right, dtype=object) << up
    return np.asarray(division(1, 1 << up, solver(side)))


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


def box_rest(counts: np.ndarray, pair: Pair, wrap: Wrap) -> FieldAtRest:
    """The rest on a box (ALGEBRA.md #the-generator, THE START): the line's exact rest to the nearest integer, certified in integers. The guess is the solver's; each round the exact residual R of the whole-integer field is solved back and taken off; the certificate is the exit-time bound: T solves the same line with 6 den x the lift on the right side, its own exact residual rho makes ||A^-1|| <= ||T|| / (6 den x lift - ||rho||), so the field stands within margin = ||A^-1|| ||R|| of the exact rest; where every free Node is farther than the margin from a half, the levels are the exact rest's nearest integers. Where the certificate does not close, the unit grows once and the rounds repeat; a value still within the margin of a half then rounds up, the half's own side under the division act (the margin added before the act). The cost is the load's."""
    check_counts(
        np.abs(counts), 1 + int(np.abs(counts).max())
    )  # a signed family's counts by their sizes
    num, den = pair
    if num < 1 or den < num:
        raise ValueError(f"the field's pair [{num}, {den}] has num from 1 and den from num")
    solver, free = line_solver(counts, pair, wrap)
    lifted = np.zeros(counts.shape, dtype=object)
    lifted[...] = 6 * den * LIFT
    exit_time = solved(counts, solver, free, lifted.ravel()[free])
    rho = residual(exit_time, pair, wrap, free) - 6 * den * LIFT
    bound_wall = 6 * den * LIFT - sizes(rho)
    if bound_wall <= 0:
        raise ValueError(
            "the exit-time bound did not close: the line's solver is off by more than its lift"
        )
    bound_top = sizes(exit_time.ravel()[free])
    unit = field_unit(counts, num)
    fine = np.zeros(counts.shape, dtype=object)
    fine[...] = counts.astype(object) * unit
    fine = fine + solved(counts, solver, free, -residual(fine, pair, wrap, free))
    rounds = 0
    for precision in range(PRECISIONS):
        if precision > 0:
            unit *= PRECISION_STEP
            fine = fine * PRECISION_STEP
        half = int(division(1, 2, np.array(unit, dtype=object)))
        floor = None
        for _ in range(ROUNDS):
            rounds += 1
            worst = residual(fine, pair, wrap, free)
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
            if margin * MARGIN_ROOM <= half:
                break  # only a half is left uncertified
            fine = fine + solved(counts, solver, free, -worst)
    levels = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half + margin, 1)[0])
    return FieldAtRest(levels.astype(np.int64), fine, unit, rounds, 1)


def rest(counts: np.ndarray, pair: Pair, wrap: Wrap = PERIODIC) -> FieldAtRest:
    """The start's rest of a held family on the counts: the chain's one pass where the region is a chain, the box's certified rest elsewhere (ALGEBRA.md #the-generator, THE START)."""
    return (
        chain_rest(counts, pair, wrap)
        if chain_axis(counts) is not None
        else box_rest(counts, pair, wrap)
    )


DECLARATION = Declaration(
    name="the start",
    place="any",
    reads=("a body's counts at its Nodes", "a family's pair", "the faces"),
    writes=("a family's level at a Node",),
    function=rest,
    section="ALGEBRA.md #the-generator, #the-stable-body",
    word="any",
)
