"""The Node: every family's NodeState over the GameBoard, the law's numbers and nothing else, and the interval's acts on it as pure functions of whole-board arrays, each a call of Rule3 (core/rule3.py) with every neighbour read through a Port (core/ports.py): the signed read (ALGEBRA.md #the-paces; the guard once at load), Rule3 on every record (#the-line, #the-direction), the currents and the tension read from the record (features/currents; the count is the record's share, #the-count-is-the-records-share), the well and the Wronskian's quanta (the record's form and its sense per interval, #the-primitives) and the hold with its time, vector and tensor parts (#the-primitives, the row "the hold")."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

import numpy as np

from event_universe import flow
from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import (
    ISOTROPIC,
    coefficients,
    link_paces,
    rule3,
)
from event_universe.features import currents
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
    """A family's NodeState at every Node, the law's numbers and nothing else. A family of quanta: its record's level pair with the remainder and its second level pair (the rotation sense, 0 on a real record), the remainders of its well and of its Wronskian's quanta; its count and its sense are readings of the record (share.py, features/currents) and stand nowhere. A held family: its parts, each a level pair with its remainder, the hold's carry of the time part, and per family that sources it the carries of its vector and tensor parts. A family of quanta that holds a row (the holder of the sign, its quanta light) keeps its record as its time part alone, `levels` None (`record_of`)."""

    levels: Record | None
    well_remainder: np.ndarray | None
    parts: list[Record]
    carry: np.ndarray | None
    second: Record | None = None
    wronskian_remainder: np.ndarray | None = None
    flows: dict[int, list[np.ndarray]] = field(default_factory=dict)


def zeros(shape: tuple[int, int, int]) -> np.ndarray:
    """An integer array of zeros over the GameBoard."""
    return np.zeros(shape, dtype=np.int64)


def empty_record(shape: tuple[int, int, int]) -> Record:
    """A level pair at 0 with the remainder 0 at every Node."""
    return Record(zeros(shape), zeros(shape), zeros(shape))


def empty_state(family: FamilyRule, shape: tuple[int, int, int]) -> NodeState:
    """A family's NodeState before its start: its two level pairs at 0 where it carries quanta, its parts at 0 where it is held, its time part the real pair itself where it does both (the holder of the sign, its quanta light: `parts[0] is levels`)."""
    quanta = family.quanta
    parts = [empty_record(shape) for _ in range(components(family.parts))] if family.held else []
    levels = parts[0] if parts and quanta else empty_record(shape) if quanta else None
    return NodeState(
        levels,
        zeros(shape) if quanta else None,
        parts,
        zeros(shape) if family.held else None,
        empty_record(shape) if quanta else None,
        zeros(shape) if quanta else None,
    )


def records(state: NodeState) -> list[Record]:
    """Every level pair of a NodeState in one order: the real pair and the second of a family of quanta, then a held family's parts, after the time part where that part is the real pair itself."""
    own = [r for r in (state.levels, state.second) if r is not None]
    return own + list(state.parts[1:] if state.levels is not None and state.parts else state.parts)


def with_records(state: NodeState, found: list[Record]) -> None:
    """Every level pair of the NodeState replaced in the order of `records`, the time part of a held family of quanta its real pair."""
    found = list(found)
    if state.levels is not None:
        state.levels = found.pop(0)
    if state.second is not None:
        state.second = found.pop(0)
    state.parts = ([state.levels] if state.levels is not None and state.parts else []) + found


def with_parts(state: NodeState, parts: list[Record]) -> None:
    """A held family's parts replaced after the hold, its time part the real pair where it carries quanta."""
    state.parts = parts
    if state.levels is not None:
        state.levels = parts[0]


def ports(a: np.ndarray, wrap: Wrap, fill: int = 0) -> tuple[np.ndarray, ...]:
    """The six arrivals of an array in Port order [+X, -X, +Y, -Y, +Z, -Z]: the neighbour's level through each Port, `fill` beyond a face that does not wrap (0, or the row's rest for the massless row holding the content: the vacuum beyond the face is the same vacuum, ALGEBRA.md #what-is-open, item 22), the Node itself on a folded axis."""
    return tuple(arrival(a, axis, side, wrap, fill) for axis in range(3) for side in (1, -1))


def axis_sums(a: np.ndarray, wrap: Wrap, fill: int = 0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The two arrivals of each axis summed, the three sums Rule3 reads, `fill` beyond a face."""
    arrived = ports(a, wrap, fill)
    x, y, z = (arrived[2 * axis] + arrived[2 * axis + 1] for axis in range(3))
    return x, y, z


def sense_sign(state: NodeState, shape: tuple[int, int, int]) -> np.ndarray:
    """The reader's q at every Node: the sign of its own rotation sense there, the Wronskian of its two level pairs read from the record (0 where it has none; ALGEBRA.md #the-paces, the sign is the rotation sense)."""
    if state.levels is None or state.second is None:
        return zeros(shape)
    return np.asarray(np.sign(wronskian(state.levels, state.second)), dtype=np.int64)


def read_terms(
    index: int,
    families: tuple[FamilyRule, ...],
    states: list[NodeState],
    gamma: int,
    level: str,
    shape: tuple[int, int, int],
) -> tuple[signed.SignedReadTerm, signed.SignedReadStart]:
    """The read's declaration and start for a family (ALGEBRA.md #the-paces): its reads, its q (`sense_sign`), its pair and Gamma; the read families' time parts at `level` ("now" forward at the interval's start, "before" backward) and the axis contents t_a = SUM over the reads of (weight x by x the read family's aa part + 1) div 2, one division per read per axis rounded at the read."""
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
    return term, signed.SignedReadStart(shape, arguments, (axis[0], axis[1], axis[2]))


def signed_read(
    index: int,
    families: tuple[FamilyRule, ...],
    states: list[NodeState],
    gamma: int,
    level: str,
    shape: tuple[int, int, int],
) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    """The signed read (ALGEBRA.md #the-paces): the content c = SUM over the family's reads of (weight x by x the read family's time part) and the axis contents, no floor, no clamp and no guard in the interval (features/signed_read)."""
    writes = signed.apply(*read_terms(index, families, states, gamma, level, shape))
    assert writes.axis_contents is not None
    return writes.content, writes.axis_contents


def guarded(
    index: int,
    families: tuple[FamilyRule, ...],
    states: list[NodeState],
    gamma: int,
    shape: tuple[int, int, int],
) -> None:
    """The guard once at load (ALGEBRA.md #the-paces, the guard): the family's read of the initial state checked as squares, 0 < p and p^2 (den + num) <= 2 den Gamma^2 at every Node, refused by name outside; no act of the interval reads it (features/signed_read)."""
    term, start = read_terms(index, families, states, gamma, "now", shape)
    signed.guard(term, signed.apply(term, start), signed.SignedReadOwn(index, families[index].name))


def least_pace(
    index: int,
    families: tuple[FamilyRule, ...],
    states: list[NodeState],
    gamma: int,
    shape: tuple[int, int, int],
) -> int:
    """The least Link pace Gamma - 2 c - t_a of a family over the GameBoard as it stands, a GameBoard diagnostic for the report and no act of the law."""
    content, axis = signed_read(index, families, states, gamma, "now", shape)
    return min(int(np.min(pace)) for pace in link_paces(gamma, content, axis))


def quanta_rule(family: FamilyRule, gamma: int, content: Any, axis: tuple[Any, ...] = ISOTROPIC) -> Rule:
    """Rule3's integers for a family of quanta at every Node from its pair and the paces (ALGEBRA.md #the-line)."""
    num, den = family.pair
    return coefficients(num, den, gamma, content, axis, True)


def part_rule(family: FamilyRule) -> Rule:
    """Rule3's integers for a held family's parts: the plain rule of the row's pair at the pace 1 and the wall 3 den, its reads num and its self coefficient 0, with or without a gap (ALGEBRA.md #the-line; #the-primitives, the row "the hold")."""
    num, den = family.pair
    return coefficients(num, den, 1, 0, ISOTROPIC, False)


def rule_of(family: FamilyRule, gamma: int, content: Any, axis: tuple[Any, ...] = ISOTROPIC) -> Rule:
    """The rule every record of a family steps by: a family of quanta's at the paces of its read (the holder of the sign included, its time part its record), a holder of the content's the plain rule at the pace 1 (ALGEBRA.md #the-interval)."""
    return quanta_rule(family, gamma, content, axis) if family.quanta else part_rule(family)


def step(record: Record, rule: Rule, wrap: Wrap, direction: int = 1, fill: int = 0) -> Record:
    """Rule3 on a level pair (ALGEBRA.md #the-line, #the-direction): forward from (now, before, r) to (next, now, r'), backward from (next, now, r') to (now, before, r), the six reads through the Ports of the level the step starts from, `fill` read beyond a face (the row's rest)."""
    reads, self_coefficient, wall = rule
    if direction == 1:
        sums = axis_sums(record.now, wrap, fill)
        nxt, remainder = rule3(
            reads, sums, self_coefficient, wall, record.now, record.before, record.remainder
        )
        return Record(np.asarray(nxt), record.now, np.asarray(remainder))
    sums = axis_sums(record.before, wrap, fill)
    back, remainder = rule3(
        reads, sums, self_coefficient, wall, record.before, record.now, record.remainder, -1
    )
    return Record(record.before, np.asarray(back), np.asarray(remainder))


def currents_of(family: FamilyRule, state: NodeState, wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The currents of a family of quanta at every Node, a reading of its record (ALGEBRA.md #the-count-is-the-records-share; features/currents): through each of the six Ports F_ij = num (now_i before_j - before_i now_j) into the Node from its neighbour, both level pairs' currents added, at the level pairs as they stand (the pair the step started from, read before Rule3 acts, so that the share's change over the step is exactly their sum); what a detector reads at its boundary."""
    assert state.levels is not None
    found: list[Any] = [0] * 6
    for record in (state.levels, state.second):
        if record is None:
            continue
        here = currents.Levels(record.now, record.before)
        now, before = ports(record.now, wrap), ports(record.before, wrap)
        for port in range(6):
            there = currents.Levels(now[port], before[port])
            found[port] = found[port] + currents.current(family.pair[0], here, there)
    return tuple(np.asarray(value) for value in found)


def stresses_of(family: FamilyRule, state: NodeState, wrap: Wrap) -> currents.Vector:
    """The tension on each axis at every Node from a family of quanta's levels now, both level pairs' tensions added, a reading of the record into the held rows' paces (features/currents; ALGEBRA.md #the-primitives, the row "the hold")."""
    assert state.levels is not None
    tensions: currents.Vector = (0, 0, 0)
    for record in (state.levels, state.second):
        if record is None:
            continue
        found = currents.stress(family.pair[0], axis_differences(record.now, wrap))
        tensions = (tensions[0] + found[0], tensions[1] + found[1], tensions[2] + found[2])
    return tuple(np.asarray(value) for value in tensions)  # type: ignore[return-value]


def axis_differences(
    now: np.ndarray, wrap: Wrap
) -> tuple[currents.Differences, currents.Differences, currents.Differences]:
    """The level's difference across each axis's two Ports at every Node, D_a = the +a arrival minus the -a arrival, with the neighbours' own differences brought through the axis's two Ports, the tension's reads (ALGEBRA.md #the-primitives, the row "the hold", the tension)."""
    arrived = ports(now, wrap)
    found = []
    for axis in range(3):
        d = arrived[2 * axis] - arrived[2 * axis + 1]
        plus, minus = arrival(d, axis, 1, wrap), arrival(d, axis, -1, wrap)
        found.append(currents.Differences(now, d, plus, minus))
    return found[0], found[1], found[2]


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
    direction: int = 1,
    flows: dict[int, flow.Flow] | None = None,
) -> tuple[list[Record], np.ndarray, dict[int, list[np.ndarray]]]:
    """A held family's hold (ALGEBRA.md #the-primitives, the row "the hold"), its parts already stepped by Rule3 in the interval's second act, with or without a gap: the hold (features/hold) at its time part, (source + r) div E_s added with the carry kept at the Node, and at its tensor parts from every sourcing family's flow (`flow.flow_hold`); backward the holds' increments taken off and the carries stepped back."""
    assert state.carry is not None and family.divisor is not None
    parts, carry = list(state.parts), state.carry
    carries = dict(state.flows)
    time, carry = hold(parts[0].now, source_now, family.divisor, carry, direction)
    parts[0] = replace(parts[0], now=np.asarray(time))
    if len(family.parts) > 1:
        levels = [part.now for part in parts]
        for index, current in (flows or {}).items():
            levels, carries[index] = flow.flow_hold(family, levels, current, carries[index], direction)
        parts = [replace(part, now=level) for part, level in zip(parts, levels, strict=True)]
    return parts, np.asarray(carry), carries


def largest(record: Record) -> int:
    """The largest size of a level pair's newest level, read against the amplitude bound A."""
    return int(np.abs(record.now).max())
