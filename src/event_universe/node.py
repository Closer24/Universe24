"""The Node: every family's NodeState over the GameBoard, the law's numbers and nothing else, and the interval's acts on it as pure functions of whole-board arrays, each a call of Rule3 (core/rule3.py) with every neighbour read through a Port (core/ports.py): the signed read (ALGEBRA.md #the-paces), Rule3 on the levels (#the-line, #the-direction), the count's line with its lay (#the-counts-line), the well (the record's form per interval, #the-primitives) and the hold (#the-primitives, the row "the hold")."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import ISOTROPIC, NO_READ, coefficients, form_term, rule3
from event_universe.features import counts_line
from event_universe.features import signed_read as signed
from event_universe.features.hold import components, diagonal, hold
from event_universe.features.write import carried
from event_universe.loader.derived import BY_PLAIN, CONTENT, FamilyRule

Rule = tuple[tuple[Any, Any, Any], Any, Any]  # Rule3's integers at every Node: (R_x, R_y, R_z), S, w


@dataclass(frozen=True)
class Record:
    """One level pair over the GameBoard: the level now, the level before and the remainder r at every Node."""

    now: np.ndarray
    before: np.ndarray
    remainder: np.ndarray


@dataclass
class NodeState:
    """A family's NodeState at every Node: its two levels and remainder (a family of quanta), its count and the count's remainder (laid at the first act), the remainder of its well; its parts, each a level pair with its remainder, and the hold's carry (a held family)."""

    levels: Record | None
    count: np.ndarray | None
    count_remainder: np.ndarray | None
    well_remainder: np.ndarray | None
    parts: list[Record]
    carry: np.ndarray | None


def zeros(shape: tuple[int, int, int]) -> np.ndarray:
    """An integer array of zeros over the GameBoard."""
    return np.zeros(shape, dtype=np.int64)


def empty_record(shape: tuple[int, int, int]) -> Record:
    """A level pair at 0 with the remainder 0 at every Node."""
    return Record(zeros(shape), zeros(shape), zeros(shape))


def empty_state(family: FamilyRule, shape: tuple[int, int, int]) -> NodeState:
    """A family's NodeState before its start: its levels at 0 where it carries quanta, its parts at 0 where it is held."""
    quanta = family.quanta
    parts = [empty_record(shape) for _ in range(components(family.parts))] if family.held else []
    return NodeState(
        empty_record(shape) if quanta else None,
        None,
        None,
        zeros(shape) if quanta else None,
        parts,
        zeros(shape) if family.held else None,
    )


def ports(a: np.ndarray, wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The six arrivals of an array in Port order [+X, -X, +Y, -Y, +Z, -Z]: the neighbour's level through each Port, 0 beyond a face that does not wrap, the Node itself on a folded axis."""
    return tuple(arrival(a, axis, side, wrap[axis]) for axis in range(3) for side in (1, -1))


def axis_sums(a: np.ndarray, wrap: Wrap) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The two arrivals of each axis summed, the three sums Rule3 reads."""
    arrived = ports(a, wrap)
    x, y, z = (arrived[2 * axis] + arrived[2 * axis + 1] for axis in range(3))
    return x, y, z


def signed_read(
    index: int,
    families: tuple[FamilyRule, ...],
    states: list[NodeState],
    gamma: int,
    level: str,
    tick: int,
    shape: tuple[int, int, int],
) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    """THE SIGNED READ (ALGEBRA.md #the-paces): the content c = SUM over the family's reads of (weight x by x the read family's time part) and the axis contents t_a = SUM over the reads of (weight x by x the read family's aa part + 1) div 2, one division per read per axis rounded at the read, from the parts' `level` ("now" forward at the interval's start, "before" backward); no floor and no clamp, and the guard 0 < p <= P ends the run by name (features/signed_read)."""
    family = families[index]
    reads = tuple((read.family, read.weight, read.by) for read in family.reads)
    arguments = {read.family: getattr(states[read.family].parts[0], level) for read in family.reads}
    axis = [zeros(shape), zeros(shape), zeros(shape)]
    for read in family.reads:
        tensor = diagonal(families[read.family].parts)
        factor = read.weight if read.by == BY_PLAIN else -family.sign * read.weight
        for a, part in enumerate(tensor or ()):
            axis[a] += carried(factor * getattr(states[read.family].parts[part], level), 2, 1)[0]
    term = signed.SignedReadTerm(reads, family.sign, family.pair, gamma)
    start = signed.SignedReadStart(shape, arguments, (axis[0], axis[1], axis[2]))
    writes = signed.apply(term, start, signed.SignedReadOwn(index, family.name, tick))
    return writes.content, (axis[0], axis[1], axis[2])


def quanta_rule(family: FamilyRule, gamma: int, content: Any, axis: tuple[Any, ...] = ISOTROPIC) -> Rule:
    """Rule3's integers for a family of quanta at every Node from its pair and the paces (ALGEBRA.md #the-line)."""
    num, den = family.pair
    return coefficients(num, den, gamma, content, axis, True)


def part_rule(family: FamilyRule) -> Rule:
    """Rule3's integers for a held family's parts: the plain rule of the row's pair at the pace 1 and the wall 3 den (ALGEBRA.md #the-line)."""
    num, den = family.pair
    return coefficients(num, den, 1, 0, ISOTROPIC, False)


def step(record: Record, rule: Rule, wrap: Wrap, direction: int = 1) -> Record:
    """RULE3 ON A LEVEL PAIR (ALGEBRA.md #the-line, #the-direction): forward from (now, before, r) to (next, now, r'), backward from (next, now, r') to (now, before, r), the six reads through the Ports of the level the step starts from."""
    reads, self_coefficient, wall = rule
    if direction == 1:
        sums = axis_sums(record.now, wrap)
        nxt, remainder = rule3(
            reads, sums, self_coefficient, wall, record.now, record.before, record.remainder
        )
        return Record(np.asarray(nxt), record.now, np.asarray(remainder))
    sums = axis_sums(record.before, wrap)
    back, remainder = rule3(
        reads, sums, self_coefficient, wall, record.before, record.now, record.remainder, -1
    )
    return Record(record.before, np.asarray(back), np.asarray(remainder))


def count_wall(family: FamilyRule, action: int) -> int:
    """THE COUNT'S WALL W_c = 3 den T, the family's plain wall times the universe's quantum action (ALGEBRA.md #the-counts-line, the lay and the wall)."""
    return 3 * family.pair[1] * action


def share(family: FamilyRule, record: Record, wrap: Wrap) -> np.ndarray:
    """The form's share at every Node in the current's units, E_i / 2 = 3 den (now^2 + before^2) - num now S_6(before) (ALGEBRA.md #the-counts-line): the form's Node term at the plain wall less the Link term by the read act."""
    num, den = family.pair
    sums = axis_sums(record.before, wrap)
    link = rule3((num * record.now,) * 3, sums, 0, 1, 0, 0, 0)[0]
    return np.asarray(form_term(0, 3 * den, record.now, record.before) - link)


def lay(family: FamilyRule, record: Record, action: int, wrap: Wrap) -> tuple[np.ndarray, np.ndarray]:
    """THE LAY, once at the first act (ALGEBRA.md #the-counts-line): W_c c + r = E_i / 2 + W_c div 2 at every Node by Rule3's division act, W_c div 2 the remainder's origin."""
    wall = count_wall(family, action)
    origin = rule3(NO_READ, NO_READ, 1, 2, wall, 0, 0)[0]  # W_c div 2, the division act
    counts, remainder = rule3(NO_READ, NO_READ, 1, wall, 0, 0, share(family, record, wrap) + origin)
    return np.asarray(counts, dtype=np.int64), np.asarray(remainder, dtype=np.int64)


def count_line(
    family: FamilyRule, state: NodeState, action: int, amplitude: int, wrap: Wrap, direction: int = 1
) -> counts_line.CountWrites:
    """THE COUNT'S LINE on the family's count (ALGEBRA.md #the-counts-line): the six currents F_ij = num (now_i before_j - before_i now_j) through the Ports from the family's levels as the step left them, the count and its remainder moved forward or back by the line's division act (features/counts_line)."""
    assert state.levels is not None and state.count is not None and state.count_remainder is not None
    levels = state.levels
    now, before = ports(levels.now, wrap), ports(levels.before, wrap)
    links = tuple(counts_line.Levels(now[port], before[port]) for port in range(6))
    term = counts_line.CountTerm(
        count_wall(family, action), family.pair[0], amplitude, int(state.count.max())
    )
    here = counts_line.Levels(levels.now, levels.before)
    start = counts_line.CountStart(state.count, state.count_remainder, here, links, direction)
    return counts_line.apply(term, start)


def well(
    before: Record, after: Record, remainder: np.ndarray, action: int, direction: int = 1
) -> tuple[np.ndarray, np.ndarray]:
    """THE WELL of one interval (ALGEBRA.md #the-primitives, the rows "the hold" and "the source"): the record's form at every Node D_i = now^2 - next x before from the three levels around the step, its quanta (D_i + r) div T by the write's carried division with the remainder kept at the Node; backward the same quanta and the remainder before them. `before` holds (now, before) at the interval's start and `after` holds next as its `now`."""
    form = before.now * before.now - after.now * before.before
    quanta, carried_out = carried(form, action, remainder, direction)
    return np.asarray(quanta), np.asarray(carried_out)


def source(
    held: FamilyRule,
    families: tuple[FamilyRule, ...],
    wells: dict[int, np.ndarray],
    shape: tuple[int, int, int],
) -> np.ndarray:
    """The hold's source at every Node for a held family: SUM over the families whose bodies source it of their well, at the weight 1 for a holder of the content and by the sourcing family's sign q for a holder of the sign (ALGEBRA.md #the-primitives, the row "the hold")."""
    total = zeros(shape)
    for index, quanta in wells.items():
        weight = 1 if held.held == CONTENT else families[index].sign
        total = total + weight * quanta
    return total


def held_step(
    family: FamilyRule, state: NodeState, source_now: np.ndarray, wrap: Wrap, direction: int = 1
) -> tuple[list[Record], np.ndarray]:
    """A held family's interval: forward its parts by the plain rule, then THE HOLD (features/hold) at its time part, (source + r) div E_s added with the carry kept at the Node; backward the hold's increment taken off and the carry stepped back, then the parts back (ALGEBRA.md #the-primitives, the row "the hold")."""
    assert state.carry is not None and family.divisor is not None
    rule = part_rule(family)
    parts, carry = list(state.parts), state.carry
    if direction == 1:
        parts = [step(part, rule, wrap) for part in parts]
    time, carry = hold(parts[0].now, source_now, family.divisor, carry, direction)
    parts[0] = replace(parts[0], now=np.asarray(time))
    if direction == -1:
        parts = [step(part, rule, wrap, -1) for part in parts]
    return parts, np.asarray(carry)


def scaled(
    levels: tuple[np.ndarray, np.ndarray], amplitude: int, scale: int
) -> tuple[np.ndarray, np.ndarray]:
    """The two levels at the amplitude `scale`: (level x scale) div amplitude at every Node by Rule3's division act, the remainder not kept (the scale is the act's choice, no step of the law)."""
    now, before = (
        np.asarray(rule3(NO_READ, NO_READ, scale, amplitude, level, 0, 0)[0], dtype=np.int64)
        for level in levels
    )
    return now, before


def one_quantum(
    family: FamilyRule,
    levels: tuple[np.ndarray, np.ndarray],
    action: int,
    wrap: Wrap,
    bound: int,
    label: str,
) -> tuple[np.ndarray, np.ndarray]:
    """THE COUNT IS THE RECORD'S FORM (ALGEBRA.md #the-counts-line, the lay and the wall): the written levels scaled so that their own form, laid by the lay's act over the board, is exactly one count: the amplitude bracketed from the written one by halving while the lay reaches one and doubling while it does not (up to A), then bisected to the least amplitude that reaches one; refused by name where the write is zero, where no amplitude up to A lays a count, or where the least that lays any lays more than one."""
    amplitude = int(max(int(np.abs(levels[0]).max()), int(np.abs(levels[1]).max())))
    if amplitude == 0:
        raise ValueError(
            f"{label}: the written levels are zero at every Node, and no scale lays one count"
        )

    def count(scale: int) -> int:
        now, before = scaled(levels, amplitude, scale)
        return int(lay(family, Record(now, before, zeros(now.shape)), action, wrap)[0].sum())

    def half(value: int) -> int:
        return int(rule3(NO_READ, NO_READ, 1, 2, value, 0, 0)[0])

    low, high = amplitude, amplitude
    if count(amplitude) >= 1:
        while low > 0 and count(low) >= 1:
            high, low = low, half(low)
    else:
        while count(high) < 1:
            if high > bound:
                raise ValueError(
                    f"{label}: the written form lays no count at any amplitude up to A = {bound}"
                )
            low, high = high, 2 * high
    while high - low > 1:
        middle = half(low + high)
        low, high = (low, middle) if count(middle) >= 1 else (middle, high)
    if count(high) != 1 or high > bound:
        raise ValueError(
            f"{label}: the written form lays {count(high)} counts at the least amplitude {high} that lays any "
            f"(A = {bound}): no scale lays exactly one (ALGEBRA.md #the-counts-line, the lay and the wall)"
        )
    return scaled(levels, amplitude, high)


def largest(record: Record) -> int:
    """The largest size of a level pair's newest level, read against the amplitude bound A."""
    return int(np.abs(record.now).max())
