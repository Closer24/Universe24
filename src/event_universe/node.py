"""The Node: every family's NodeState over the GameBoard, the law's numbers and nothing else, and the interval's acts on it as pure functions of whole-board arrays, each a call of Rule3 (core/rule3.py) with every neighbour read through a Port (core/ports.py): the signed read (ALGEBRA.md #the-paces), Rule3 on the record's two level pairs (#the-line, #the-direction), the count's line and the sense's line with their lay from the weighted share (#the-counts-line), the well and the Wronskian's quanta (the record's form and its sense per interval, #the-primitives) and the hold with its time, vector and tensor parts (#the-primitives, the row "the hold")."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

import numpy as np

from event_universe import flow
from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import (
    ISOTROPIC,
    NO_READ,
    coefficients,
    form_term,
    link_paces,
    rule3,
)
from event_universe.features import counts_line
from event_universe.features import signed_read as signed
from event_universe.features.hold import components, diagonal, hold
from event_universe.features.write import carried
from event_universe.loader.derived import BY_PLAIN, BY_SIGN, FamilyRule

Rule = tuple[tuple[Any, Any, Any], Any, Any]  # Rule3's integers at every Node: (R_x, R_y, R_z), S, w


@dataclass(frozen=True)
class Record:
    """One level pair over the GameBoard: the level now, the level before and the remainder r at every Node."""

    now: np.ndarray
    before: np.ndarray
    remainder: np.ndarray


@dataclass
class NodeState:
    """A family's NodeState at every Node. A family of quanta: its record's level pair with the remainder and its second level pair (the rotation sense, 0 on a real record), its count and the count's remainder and its sense (the booked Wronskian) and the sense's remainder (laid at the first act), the remainders of its well and of its Wronskian's quanta. A held family: its parts, each a level pair with its remainder, the hold's carry of the time part, and per family that sources it the carries of its vector and tensor parts."""

    levels: Record | None
    count: np.ndarray | None
    count_remainder: np.ndarray | None
    well_remainder: np.ndarray | None
    parts: list[Record]
    carry: np.ndarray | None
    second: Record | None = None
    sense: np.ndarray | None = None
    sense_remainder: np.ndarray | None = None
    wronskian_remainder: np.ndarray | None = None
    flows: dict[int, list[np.ndarray]] = field(default_factory=dict)


def zeros(shape: tuple[int, int, int]) -> np.ndarray:
    """An integer array of zeros over the GameBoard."""
    return np.zeros(shape, dtype=np.int64)


def empty_record(shape: tuple[int, int, int]) -> Record:
    """A level pair at 0 with the remainder 0 at every Node."""
    return Record(zeros(shape), zeros(shape), zeros(shape))


def empty_state(family: FamilyRule, shape: tuple[int, int, int]) -> NodeState:
    """A family's NodeState before its start: its two level pairs at 0 where it carries quanta, its parts at 0 where it is held."""
    quanta = family.quanta
    parts = [empty_record(shape) for _ in range(components(family.parts))] if family.held else []
    return NodeState(
        empty_record(shape) if quanta else None,
        None,
        None,
        zeros(shape) if quanta else None,
        parts,
        zeros(shape) if family.held else None,
        empty_record(shape) if quanta else None,
        None,
        None,
        zeros(shape) if quanta else None,
    )


def ports(a: np.ndarray, wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The six arrivals of an array in Port order [+X, -X, +Y, -Y, +Z, -Z]: the neighbour's level through each Port, 0 beyond a face that does not wrap, the Node itself on a folded axis."""
    return tuple(arrival(a, axis, side, wrap[axis]) for axis in range(3) for side in (1, -1))


def axis_sums(a: np.ndarray, wrap: Wrap) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The two arrivals of each axis summed, the three sums Rule3 reads."""
    arrived = ports(a, wrap)
    x, y, z = (arrived[2 * axis] + arrived[2 * axis + 1] for axis in range(3))
    return x, y, z


def sense_sign(state: NodeState, shape: tuple[int, int, int]) -> np.ndarray:
    """The reader's q at every Node: the sign of its own sense there, the booked Wronskian of its two level pairs (0 where it has none; ALGEBRA.md #the-paces, the sign is the rotation sense)."""
    return np.sign(state.sense) if state.sense is not None else zeros(shape)


def signed_read(
    index: int,
    families: tuple[FamilyRule, ...],
    states: list[NodeState],
    gamma: int,
    level: str,
    tick: int,
    shape: tuple[int, int, int],
) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    """The signed read (ALGEBRA.md #the-paces): the content c = SUM over the family's reads of (weight x by x the read family's time part) and the axis contents t_a = SUM over the reads of (weight x by x the read family's aa part + 1) div 2, one division per read per axis rounded at the read, from the parts' `level` ("now" forward at the interval's start, "before" backward), a held row with a gap read as the well it laid; by sign the reader's q at the Node (`sense_sign`); no floor and no clamp, and the guard 0 < p <= P ends the run by name (features/signed_read)."""
    family = families[index]
    q = sense_sign(states[index], shape)
    reads = tuple((read.family, read.weight, read.by) for read in family.reads)
    arguments = {read.family: getattr(states[read.family].parts[0], level) for read in family.reads}
    axis = [zeros(shape), zeros(shape), zeros(shape)]
    for read in family.reads:
        tensor = diagonal(families[read.family].parts)
        factor = read.weight if read.by == BY_PLAIN else -q * read.weight
        for a, part in enumerate(tensor or ()):
            axis[a] += carried(factor * getattr(states[read.family].parts[part], level), 2, 1)[0]
    term = signed.SignedReadTerm(reads, q, family.pair, gamma)
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
    """Rule3 on a level pair (ALGEBRA.md #the-line, #the-direction): forward from (now, before, r) to (next, now, r'), backward from (next, now, r') to (now, before, r), the six reads through the Ports of the level the step starts from."""
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
    """The count's wall W_c = 3 den T, the family's plain wall times the universe's quantum action (ALGEBRA.md #the-counts-line, the lay and the wall)."""
    return 3 * family.pair[1] * action


def squared_paces(gamma: int, content: Any, axis: tuple[Any, ...]) -> Any:
    """The sum of the three Link paces' squares at every Node, SUM_a p_a^2 with p_a = Gamma - 2 c - t_a (ALGEBRA.md #the-paces)."""
    paces = link_paces(gamma, content, axis)
    return paces[0] * paces[0] + paces[1] * paces[1] + paces[2] * paces[2]


def over_paces(numerator: Any, gamma: int, content: Any, axis: tuple[Any, ...]) -> np.ndarray:
    """A Node term over the Link's pace squared, 3 x numerator div (2 SUM_a p_a^2) by Rule3's division act: numerator div 2 p^2 where the three paces are one (ALGEBRA.md #the-counts-line, the lay and the wall)."""
    return np.asarray(
        rule3(NO_READ, NO_READ, len(axis), 2 * squared_paces(gamma, content, axis), numerator, 0, 0)[0]
    )


def share(
    pair: tuple[int, int],
    record: Record,
    wrap: Wrap,
    gamma: int,
    content: Any = 0,
    axis: tuple[Any, ...] = ISOTROPIC,
) -> np.ndarray:
    """The weighted share at every Node in the current's units (ALGEBRA.md #the-counts-line, the lay and the wall): the conserved form's Node term w (now^2 + before^2) - S now before over the Link's pace squared (`over_paces`), less the plain Link term num now S_6(before) by the read act; Rule3's integers at the paces of the read, exact at any size."""
    num, den = pair
    now, before = record.now.astype(object), record.before.astype(object)
    _reads, self_coefficient, wall = coefficients(num, den, gamma, content, axis, True)
    weighted = over_paces(form_term(self_coefficient, wall, now, before), gamma, content, axis)
    sums = tuple(value.astype(object) for value in axis_sums(record.before, wrap))
    link = rule3((num * now,) * 3, sums, 0, 1, 0, 0, 0)[0]
    return np.asarray(weighted - link)


def sense_share(
    pair: tuple[int, int],
    record: Record,
    second: Record,
    gamma: int,
    content: Any = 0,
    axis: tuple[Any, ...] = ISOTROPIC,
) -> np.ndarray:
    """The sense's share at every Node in the current's units (ALGEBRA.md #the-paces, the sign is the rotation sense): the Wronskian of the two level pairs W_i = re_now im_before - im_now re_before times the rule's wall w over the Link's pace squared (`over_paces`), whose change over one interval is exactly the sense's current."""
    num, den = pair
    _reads, _self, wall = coefficients(num, den, gamma, content, axis, True)
    return over_paces(wall * wronskian(record, second).astype(object), gamma, content, axis)


def laid(share_now: np.ndarray, wall: int) -> tuple[np.ndarray, np.ndarray]:
    """W_c c + r = share + W_c div 2 at every Node by Rule3's division act, W_c div 2 the remainder's origin (ALGEBRA.md #the-counts-line, the lay and the wall)."""
    origin = rule3(NO_READ, NO_READ, 1, 2, wall, 0, 0)[0]  # W_c div 2, the division act
    counts, remainder = rule3(NO_READ, NO_READ, 1, wall, 0, 0, share_now + origin)
    return np.asarray(counts, dtype=np.int64), np.asarray(remainder, dtype=np.int64)


def lay(
    family: FamilyRule,
    records: tuple[Record, ...],
    action: int,
    wrap: Wrap,
    gamma: int,
    content: Any = 0,
    axis: tuple[Any, ...] = ISOTROPIC,
) -> tuple[np.ndarray, np.ndarray]:
    """The lay, once at the first act (ALGEBRA.md #the-counts-line): the count from the weighted share of the record's level pairs summed (the form of (re, im) is the sum of the two forms), at the paces of the read."""
    total = sum(share(family.pair, record, wrap, gamma, content, axis) for record in records)
    return laid(np.asarray(total), count_wall(family, action))


def lay_sense(
    family: FamilyRule,
    record: Record,
    second: Record,
    action: int,
    gamma: int,
    content: Any = 0,
    axis: tuple[Any, ...] = ISOTROPIC,
) -> tuple[np.ndarray, np.ndarray]:
    """The sense's lay, once at the first act beside the count's: the sense from the sense's share at the count's wall W_c."""
    return laid(
        sense_share(family.pair, record, second, gamma, content, axis), count_wall(family, action)
    )


def count_term(family: FamilyRule, action: int, amplitude: int, most: int) -> counts_line.CountTerm:
    """The count's line's declaration for a family: its wall W_c, the current's weight num, the amplitude bound A and the largest count."""
    return counts_line.CountTerm(count_wall(family, action), family.pair[0], amplitude, most)


def count_line(
    family: FamilyRule, state: NodeState, action: int, amplitude: int, wrap: Wrap, direction: int = 1
) -> counts_line.CountWrites:
    """The count's line on the family's count (ALGEBRA.md #the-counts-line): the six currents F_ij = num (now_i before_j - before_i now_j) through the Ports from the family's two level pairs as the step left them, summed, the count and its remainder moved forward or back by the line's division act (features/counts_line)."""
    assert state.levels is not None and state.count is not None and state.count_remainder is not None

    def pairs(record: Record) -> tuple[counts_line.Levels, tuple[counts_line.Levels, ...]]:
        now, before = ports(record.now, wrap), ports(record.before, wrap)
        links = tuple(counts_line.Levels(now[port], before[port]) for port in range(6))
        return counts_line.Levels(record.now, record.before), links

    here, links = pairs(state.levels)
    second = pairs(state.second) if state.second is not None else None
    term = count_term(family, action, amplitude, int(np.abs(state.count).max()))
    start = counts_line.CountStart(state.count, state.count_remainder, here, links, direction, second)
    return counts_line.apply(term, start)


def sense_line(
    family: FamilyRule, state: NodeState, action: int, amplitude: int, wrap: Wrap, direction: int = 1
) -> counts_line.CountWrites:
    """The sense's line (ALGEBRA.md #the-paces, the sign is the rotation sense): the sense moved by the count's line with the Wronskian's current G_ij = num (im_i re_j - re_i im_j) through each Port at the level pairs the step started from, the change of the sense's share over the interval, forward or back."""
    assert state.levels is not None and state.second is not None
    assert state.sense is not None and state.sense_remainder is not None
    real, turned = state.levels.before, state.second.before
    re_there, im_there = ports(real, wrap), ports(turned, wrap)
    links = tuple(counts_line.Levels(im_there[port], re_there[port]) for port in range(6))
    term = count_term(family, action, amplitude, int(np.abs(state.sense).max()))
    here = counts_line.Levels(turned, real)
    start = counts_line.CountStart(state.sense, state.sense_remainder, here, links, direction)
    return counts_line.apply(term, start)


def form(before: Record, after: Record) -> np.ndarray:
    """The record's form at every Node over one interval, D_i = now^2 - next x before from the three levels around the step (`before` holds (now, before) at the interval's start, `after` holds next as its `now`)."""
    return np.asarray(before.now * before.now - after.now * before.before)


def wronskian(record: Record, second: Record) -> np.ndarray:
    """The Wronskian of a record's two level pairs at every Node, W_i = re_now im_before - im_now re_before, the booking of the rotation sense (0 on a real record)."""
    return np.asarray(record.now * second.before - second.now * record.before)


def well(
    booking: np.ndarray, remainder: np.ndarray, action: int, direction: int = 1
) -> tuple[np.ndarray, np.ndarray]:
    """The well of one interval (ALGEBRA.md #the-primitives, the rows "the hold" and "the source"): a booking of the record at every Node (its form D_i, or its Wronskian W_i), its quanta (booking + r) div T by the write's carried division with the remainder kept at the Node; backward the same quanta and the remainder before them."""
    quanta, carried_out = carried(booking, action, remainder, direction)
    return np.asarray(quanta), np.asarray(carried_out)


def weight_of(held: int, reader: FamilyRule, by: str = BY_PLAIN) -> int:
    """The weight with which a family sources a held family by `by`, the one weight of the pair (ALGEBRA.md #the-primitives, a family's write: whoever reads with w sources with w), 0 where it does not read it so."""
    return sum(read.weight for read in reader.reads if read.family == held and read.by == by)


def source(
    held: int,
    families: tuple[FamilyRule, ...],
    wells: dict[int, np.ndarray],
    turns: dict[int, np.ndarray],
    shape: tuple[int, int, int],
) -> np.ndarray:
    """The hold's source at every Node for a held family: SUM over the families of quanta of their well at the weight with which each sources it by plain, and of their Wronskian's quanta at the weight with which each sources it by sign (ALGEBRA.md #the-primitives, the row "the hold")."""
    total = zeros(shape)
    for index, quanta in wells.items():
        total = total + weight_of(held, families[index]) * quanta
    for index, quanta in turns.items():
        total = total + weight_of(held, families[index], BY_SIGN) * quanta
    return total


def held_step(
    family: FamilyRule,
    state: NodeState,
    source_now: np.ndarray,
    wrap: Wrap,
    direction: int = 1,
    flows: dict[int, flow.Flow] | None = None,
) -> tuple[list[Record], np.ndarray, dict[int, list[np.ndarray]]]:
    """A held family's interval (ALGEBRA.md #the-primitives, the row "the hold"). A row without a gap: forward its parts by the plain rule, then the hold (features/hold) at its time part, (source + r) div E_s added with the carry kept at the Node, and at its vector and tensor parts from every sourcing family's flow (`flow.flow_hold`); backward the holds' increments taken off and the carries stepped back, then the parts back. A row with a gap is not stepped: its time part is the well laid each interval, (source + r) div E_s with its own remainder, the level before kept beside it; backward the level before returns and the remainder steps back (the row keeps one interval of its past, so its inverse is exact where its level stands still)."""
    assert state.carry is not None and family.divisor is not None
    parts, carry = list(state.parts), state.carry
    carries = dict(state.flows)
    if family.gap:
        laid, carry = carried(source_now, family.divisor, carry, direction)
        now = np.asarray(laid) if direction == 1 else parts[0].before
        parts[0] = Record(now, parts[0].now if direction == 1 else parts[0].before, parts[0].remainder)
        return parts, np.asarray(carry), carries
    rule = part_rule(family)
    if direction == 1:
        parts = [step(part, rule, wrap) for part in parts]
    time, carry = hold(parts[0].now, source_now, family.divisor, carry, direction)
    parts[0] = replace(parts[0], now=np.asarray(time))
    if len(family.parts) > 1:
        levels = [part.now for part in parts]
        for index, current in (flows or {}).items():
            levels, carries[index] = flow.flow_hold(family, levels, current, carries[index], direction)
        parts = [replace(part, now=level) for part, level in zip(parts, levels, strict=True)]
    if direction == -1:
        parts = [step(part, rule, wrap, -1) for part in parts]
    return parts, np.asarray(carry), carries


def largest(record: Record) -> int:
    """The largest size of a level pair's newest level, read against the amplitude bound A."""
    return int(np.abs(record.now).max())
