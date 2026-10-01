"""The Node: every family's NodeState over the GameBoard, a flat list of lines of dimension one and the law's numbers and nothing else, and the interval's acts on it as pure functions of whole-board arrays, each a call of Rule3 (core/rule3.py) with every neighbour read through a Port (core/ports.py): the read (ALGEBRA.md #the-paces; the guard once at load), Rule3 on every line (#the-line, #the-direction), the readings of the lines (the currents and the tension, features/currents; the form and the Wronskian; the count is the record's share, #the-count-is-the-records-share) and the one write per held line (#the-primitives, the row "the hold"). The step knows no family, no dimension and no name: it receives lines with their coefficients, their sources and their readers (the loader's grouping, loader/derived.py)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import (
    ISOTROPIC,
    NO_READ,
    coefficients,
    link_paces,
    rule3,
)
from event_universe.features import currents
from event_universe.features.hold import hold
from event_universe.features.read import axis_content, content_of, guard
from event_universe.features.write import carried
from event_universe.loader.derived import FamilyRule, HeldWrite, readers_of, weight_of

Rule = tuple[tuple[Any, Any, Any], Any, Any]  # Rule3's integers at every Node: (R_x, R_y, R_z), S, w


@dataclass(frozen=True)
class Record:
    """One line of dimension one over the GameBoard: the level now, the level before and the remainder r at every Node."""

    now: np.ndarray
    before: np.ndarray
    remainder: np.ndarray


@dataclass
class NodeState:
    """A family's NodeState at every Node, the law's numbers and nothing else (ALGEBRA.md #the-postulates): its lines, each a record of dimension one (two levels and Rule3's remainder), one shape for every family, and per held line the one remainder of its write. A family of quanta's lines are its record, one line (dimension 1) or two (a plane, re and im); a held row's lines are its sources' count, the time line and, where the tensions source it, the three axis lines; the holder of the sign's one line is its record, light. Its count, currents, tension, form and Wronskian are readings of the lines (share.py, features/currents, `form`, `wronskian`) and stand nowhere."""

    lines: list[Record]
    write_remainders: list[np.ndarray]


def zeros(shape: tuple[int, int, int], kind: type) -> np.ndarray:
    """An array of zeros over the GameBoard, of the run's kind of integers (the loader's choice by the file's width, `World.kind`)."""
    return np.zeros(shape, dtype=kind)


def full(shape: tuple[int, int, int], value: Any, kind: type) -> np.ndarray:
    """An array over the GameBoard at one value, of the run's kind of integers."""
    return np.full(shape, value, dtype=kind)


def empty_record(shape: tuple[int, int, int], kind: type) -> Record:
    """A line at 0 with the remainder 0 at every Node."""
    return Record(zeros(shape, kind), zeros(shape, kind), zeros(shape, kind))


def write_origins(walls: Sequence[int], shape: tuple[int, int, int], kind: type) -> list[np.ndarray]:
    """A held family's write remainders at a Node with no level, one per held line at half its wall, the division's origin (ALGEBRA.md #the-primitives, a family's write is one act; the start's origin, features/start)."""
    return [full(shape, rule3(NO_READ, NO_READ, 1, 2, wall, 0, 0)[0], kind) for wall in walls]


def empty_state(
    family: FamilyRule, shape: tuple[int, int, int], walls: Sequence[int], kind: type
) -> NodeState:
    """A family's NodeState before its start, the state of a Node with no level: its lines at 0, as many as the loader derives for it (`FamilyRule.lines`), and where it is held one write remainder per line at the origin (`walls` the write's wall per line)."""
    lines = [empty_record(shape, kind) for _ in range(family.lines)]
    return NodeState(lines, write_origins(walls, shape, kind) if family.held else [])


def ports(a: np.ndarray, wrap: Wrap, fill: int = 0) -> tuple[np.ndarray, ...]:
    """The six arrivals of an array in Port order [+X, -X, +Y, -Y, +Z, -Z]: the neighbour's level through each Port, `fill` beyond a face that does not wrap (0, or the row's rest for the massless row holding the content: the vacuum beyond the face is the same vacuum, ALGEBRA.md #what-is-open, item 22), the Node itself on a folded axis."""
    return tuple(arrival(a, axis, side, wrap, fill) for axis in range(3) for side in (1, -1))


def axis_sums(a: np.ndarray, wrap: Wrap, fill: int = 0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The two arrivals of each axis summed, the three sums Rule3 reads, `fill` beyond a face."""
    arrived = ports(a, wrap, fill)
    x, y, z = (arrived[2 * axis] + arrived[2 * axis + 1] for axis in range(3))
    return x, y, z


def read(
    index: int,
    families: tuple[FamilyRule, ...],
    states: list[NodeState],
    level: str,
) -> tuple[Any, tuple[Any, Any, Any]]:
    """The read of a family at the interval's start (ALGEBRA.md #the-paces): the content c = SUM over its reads of (weight x the read family's time line at `level`, "now" forward and "before" backward) and the axis contents t_a = SUM over the reads of (weight x the read family's axis line a + 1) div 2, one division per read per axis rounded at the read; the integer 0 where it reads nothing (the plain rule at Gamma); no floor, no clamp and no guard in the interval (features/read)."""
    reads = families[index].reads
    content = content_of([(r.weight, getattr(states[r.family].lines[0], level)) for r in reads])
    axis = []
    for a in range(3):
        found = [
            (r.weight, getattr(states[r.family].lines[1 + a], level))
            for r in reads
            if families[r.family].axes
        ]
        axis.append(axis_content(found))
    return content, (axis[0], axis[1], axis[2])


def guarded(index: int, families: tuple[FamilyRule, ...], states: list[NodeState], gamma: int) -> None:
    """The guard once at load (ALGEBRA.md #the-paces, the guard): the family's read of the initial state checked as squares, 0 < p and p^2 (den + num) <= 2 den Gamma^2 at every Node, refused by name outside; a family that reads nothing stands at Gamma, inside; no act of the interval reads it (features/read)."""
    if families[index].reads:
        content, axis = read(index, families, states, "now")
        guard(families[index].pair, gamma, content, axis, families[index].name)


def least_pace(index: int, families: tuple[FamilyRule, ...], states: list[NodeState], gamma: int) -> int:
    """The least Link pace Gamma - 2 c - t_a of a family over the GameBoard as it stands, a GameBoard diagnostic for the report and no act of the law."""
    content, axis = read(index, families, states, "now")
    return min(int(np.min(pace)) for pace in link_paces(gamma, content, axis))


def quanta_rule(family: FamilyRule, gamma: int, content: Any, axis: tuple[Any, ...] = ISOTROPIC) -> Rule:
    """Rule3's integers for a family of quanta at every Node from its pair and the paces (ALGEBRA.md #the-line)."""
    num, den = family.pair
    return coefficients(num, den, gamma, content, axis, True)


def part_rule(family: FamilyRule) -> Rule:
    """Rule3's integers for a held row of the content's lines: the plain rule of the row's pair at the pace 1 and the wall 3 den, its reads num and its self coefficient 0, with or without a gap (ALGEBRA.md #the-line; #the-primitives, the row "the hold")."""
    num, den = family.pair
    return coefficients(num, den, 1, 0, ISOTROPIC, False)


def rule_of(family: FamilyRule, gamma: int, content: Any, axis: tuple[Any, ...] = ISOTROPIC) -> Rule:
    """The rule every line of a family steps by: a family of quanta's at the paces of its read (the holder of the sign included, its line its record), a holder of the content's the plain rule at the pace 1 (ALGEBRA.md #the-interval)."""
    return quanta_rule(family, gamma, content, axis) if family.quanta else part_rule(family)


def step(record: Record, rule: Rule, wrap: Wrap, direction: int = 1, fill: int = 0) -> Record:
    """Rule3 on one line (ALGEBRA.md #the-line, #the-direction): forward from (now, before, r) to (next, now, r'), backward from (next, now, r') to (now, before, r), the six reads through the Ports of the level the step starts from, `fill` read beyond a face (the row's rest)."""
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


def currents_of(weight: int, lines: Sequence[Record], wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The currents of a record at every Node, a reading of its lines (ALGEBRA.md #the-count-is-the-records-share; features/currents): through each of the six Ports F_ij = num (now_i before_j - before_i now_j) into the Node from its neighbour, every line's currents added, at the lines as they stand (the pair the step started from, read before Rule3 acts, so that the share's change over the step is exactly their sum); what a detector reads at its boundary."""
    found: list[Any] = [0] * 6
    for record in lines:
        here = currents.Levels(record.now, record.before)
        now, before = ports(record.now, wrap), ports(record.before, wrap)
        for port in range(6):
            there = currents.Levels(now[port], before[port])
            found[port] = found[port] + currents.current(weight, here, there)
    return tuple(np.asarray(value) for value in found)


def stresses_of(weight: int, lines: Sequence[Record], wrap: Wrap) -> currents.Vector:
    """The tension on each axis at every Node from a record's levels now, every line's tensions added, a reading of the lines into the held rows' axis lines (features/currents; ALGEBRA.md #the-primitives, the row "the hold")."""
    tensions: currents.Vector = (0, 0, 0)
    for record in lines:
        found = currents.stress(weight, axis_differences(record.now, wrap))
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


def form(begun: Sequence[Record], stepped: Sequence[Record]) -> Any:
    """The record's form at every Node over one interval, D_i = now^2 - next x before from the three levels around the step summed over its lines (`begun` holds (now, before) at the interval's start, `stepped` holds next as its `now`): the source of the rows that hold the content."""
    total: Any = 0
    for before, after in zip(begun, stepped, strict=True):
        total = total + (before.now * before.now - after.now * before.before)
    return total


def wronskian(lines: Sequence[Record]) -> Any:
    """The Wronskian of a record's two lines at every Node, W_i = re_now im_before - im_now re_before, the booking of the rotation sense, the charge density: the source of the row that holds the sign; the integer 0 for a record of one line, which has no plane."""
    if len(lines) < 2:
        return 0
    return lines[0].now * lines[1].before - lines[1].now * lines[0].before


def well(booking: Any, action: int) -> np.ndarray:
    """A reading, the well of one interval (ALGEBRA.md #the-primitives, the rows "the hold" and "the source"; row (u), a body's well is gravity's source as a number): a booking of the record at every Node (its form D_i, or its Wronskian W_i) in quanta, booking div T by the division act, no remainder kept; the run writes the booking itself through the one wall of the held line."""
    return np.asarray(carried(booking, action, 0)[0])


def write_sources(
    held: int,
    families: tuple[FamilyRule, ...],
    bookings: dict[int, Any],
    stresses: dict[int, currents.Vector],
    write: HeldWrite,
) -> list[Any]:
    """The numerators of a held family's one write per line at every Node (ALGEBRA.md #the-primitives, the row "the hold"; the integer 0 where nothing sources a line): for the time line SUM over the sourcing families (its readers, by the hold's reciprocity) of w x q, q the booking of each that the row's sources name, the form D for a row sourced by the form and the Wronskian W for the holder of the sign (`bookings`); for each axis line SUM over the sources of w x factor x T_aa, the tension of each times its factor of the common wall (`HeldWrite`, one wall per line)."""
    time: Any = 0
    for index in readers_of(families, held):
        time = time + weight_of(held, families[index]) * bookings.get(index, 0)
    found = [time]
    for axis in range(len(write.walls) - 1):
        total: Any = 0
        for index, stress in stresses.items():
            total = total + weight_of(held, families[index]) * write.factors.get(index, 0) * stress[axis]
        found.append(total)
    return found


def held_write(
    lines: Sequence[Record],
    numerators: Sequence[Any],
    walls: Sequence[int],
    remainders: Sequence[np.ndarray],
    direction: int = 1,
) -> tuple[list[Record], list[np.ndarray]]:
    """A held family's one write per line (ALGEBRA.md #the-primitives, the row "the hold"), its lines already stepped by Rule3 in the interval's second act, with or without a gap: each line's level gains (numerator + r) div wall by the write's carried division (features/hold) with the one remainder kept at the Node; backward the increments taken off and the remainders stepped back, exact; returns the lines and the remainders after."""
    written, after = [], []
    for line, numerator, wall, remainder in zip(lines, numerators, walls, remainders, strict=True):
        level, kept = hold(line.now, numerator, wall, remainder, direction)
        written.append(replace(line, now=np.asarray(level)))
        after.append(np.asarray(kept))
    return written, after


def largest(record: Record) -> int:
    """The largest size of a line's newest level, read against the amplitude bound A."""
    return int(np.abs(record.now).max())
