"""The Node: every family's NodeState over the GameBoard, a flat list of lines of dimension one and the law's numbers and nothing else, and the interval's acts on it as pure functions of whole-board arrays, each a call of Rule3 (core/rule3.py) with every neighbour read through a Port (core/ports.py), one Link's reach for every act (ALGEBRA.md #the-interval, the dependency radius): the read, the content at the Node and of each of its six Links, the Node's twice with the Link's own tension (#the-paces; the guard once at load), Rule3 on every line (#the-line, #the-direction), the readings of the lines at the interval's start (the currents and the tension's part at the Node, features/currents; the form and the Wronskian about the step; the count is the record's share, #the-count-is-the-records-share) and the one write per held line (#the-primitives, the row "the hold"). The step knows no family, no dimension and no name: it receives lines with their coefficients, their sources and their readers (the loader's grouping, loader/derived.py)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import NO_READ, coefficients, division_forward, link_paces, rule3
from event_universe.features import currents, rotation
from event_universe.features.hold import hold
from event_universe.features.read import content_of, guard, link_contents
from event_universe.features.write import carried
from event_universe.loader.derived import FamilyRule, HeldWrite, readers_of, turns, weight_of

Rule = tuple[tuple[Any, ...], Any, Any]  # Rule3's integers at every Node: the six Ports' R_ij, S, w
Links = tuple[Any, ...]  # the content of a Node's six Links in Port order, 2 c_i + t_a(i, j)
Angles = tuple[Any, tuple[Any, Any, Any]]  # the turn's numerators at every Node: the time's, each axis's


@dataclass(frozen=True)
class Record:
    """One line of dimension one over the GameBoard: the level now, the level before and the remainder r at every Node."""

    now: np.ndarray
    before: np.ndarray
    remainder: np.ndarray


Booking = tuple[list[Record], list[Record]]  # the lines the form and the Wronskian are read from


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


def level_at(record: Record, direction: int) -> np.ndarray:
    """The level a step in `direction` starts from: the level now forward (+1), the level before backward (-1), the one the state after the interval still holds (ALGEBRA.md #the-direction)."""
    return record.now if direction == 1 else record.before


def read(
    index: int,
    families: tuple[FamilyRule, ...],
    states: list[NodeState],
    direction: int,
    wrap: Wrap,
) -> tuple[Any, Links]:
    """The read of a family at the interval's start (ALGEBRA.md #the-paces; #the-interval, the dependency radius): the content c = SUM over its reads of the holders acting on the pace of (weight x the read family's time line at the level the step in `direction` starts from, `level_at`), and the content of each of its six Links, 2 c_i + t_a(i, j), the Node's content twice and the Link's own tension from the read rows' axis lines at its two ends, (weight x (aa_i + aa_j) + 1) div 2, the neighbour's line read through the Port the arrival is read through, one division per read per Link rounded at the read, one number per Link read the same from both ends (features/read, `link_contents`); the integer 0 at the Node and on every Link where it reads nothing (the plain rule at Gamma); a holder declaring the rotation enters no pace (`turning`); no floor, no clamp and no guard in the interval; the same levels read back, so the inverse reads the same paces."""
    reads = [r for r in families[index].reads if not families[r.family].rotation]
    if not reads:
        return 0, NO_READ
    content = content_of([(r.weight, level_at(states[r.family].lines[0], direction)) for r in reads])
    axes = [
        (r.weight, [level_at(states[r.family].lines[1 + a], direction) for a in range(3)])
        for r in reads
        if families[r.family].axes
    ]
    return content, link_contents(content, axes, wrap)


def turning(
    index: int, families: tuple[FamilyRule, ...], states: list[NodeState], direction: int
) -> Angles | None:
    """The angles a turned record reads (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record): from every holder it reads that declares the rotation, the time angle's numerator SUM of (weight x the holder's time line) and each axis's SUM of (weight x the holder's odd line a) at every Node, at the level the step in `direction` starts from (the same number read back, so the inverse is explicit); None where the family's record is not turned (`derived.turns`: a one-part family, or every holder acting on the pace)."""
    if not turns(families, index):
        return None
    reads = [r for r in families[index].reads if families[r.family].rotation]
    time = content_of([(r.weight, level_at(states[r.family].lines[0], direction)) for r in reads])
    axis = [
        content_of([(r.weight, level_at(states[r.family].lines[1 + a], direction)) for r in reads])
        for a in range(3)
    ]
    return time, (axis[0], axis[1], axis[2])


def guarded(
    index: int, families: tuple[FamilyRule, ...], states: list[NodeState], gamma: int, wrap: Wrap
) -> None:
    """The guard once at load (ALGEBRA.md #the-paces, the guard): the family's read of the initial state checked as squares, 0 < p and p^2 (den + num) <= 2 den Gamma^2 at every Node on the clock and on the six Links, refused by name outside; a family that reads nothing stands at Gamma, inside; no act of the interval reads it (features/read). A turned record's angles alike (features/rotation, `guard`): the time angle's numerator within 2 Gamma and each Link's two ends' sum within 4 Gamma, a tangent half-angle at most 1."""
    if families[index].reads:
        content, links = read(index, families, states, 1, wrap)
        guard(families[index].pair, gamma, content, links, families[index].name)
    angles = turning(index, families, states, 1)
    if angles is not None:
        time, links = angles
        rotation.guard(time, 2 * gamma, families[index].name, None)
        for a in range(3):
            for side in (1, -1):
                link = links[a] + arrival(links[a], a, side, wrap)
                rotation.guard(link, 2 * 2 * gamma, families[index].name, a)


def least_pace(
    index: int, families: tuple[FamilyRule, ...], states: list[NodeState], gamma: int, wrap: Wrap
) -> int:
    """The least Link pace Gamma - 2 c_i - t_a(i, j) of a family over the GameBoard's Links as it stands, a GameBoard diagnostic for the report and no act of the law."""
    _content, links = read(index, families, states, 1, wrap)
    return min(int(np.min(pace)) for pace in link_paces(gamma, links))


def quanta_rule(family: FamilyRule, gamma: int, content: Any, links: Links | None = None) -> Rule:
    """Rule3's integers for a family of quanta at every Node from its pair and the paces, the clock's from the Node's content and each Link's from the Link's content (ALGEBRA.md #the-line; None a uniform level)."""
    num, den = family.pair
    return coefficients(num, den, gamma, content, links, True)


def part_rule(family: FamilyRule) -> Rule:
    """Rule3's integers for a held row of the content's lines: the plain rule of the row's pair at the pace 1 and the wall 3 den, its reads num and its self coefficient 0, with or without a gap (ALGEBRA.md #the-line; #the-primitives, the row "the hold")."""
    num, den = family.pair
    return coefficients(num, den, 1, 0, None, False)


def rule_of(family: FamilyRule, gamma: int, content: Any, links: Links | None = None) -> Rule:
    """The rule every line of a family steps by: a family of quanta's at the paces of its read (the holder of the sign included, its line its record), a holder of the content's the plain rule at the pace 1 (ALGEBRA.md #the-interval)."""
    return quanta_rule(family, gamma, content, links) if family.quanta else part_rule(family)


def step(record: Record, rule: Rule, wrap: Wrap, direction: int = 1, fill: int = 0) -> Record:
    """Rule3 on one line (ALGEBRA.md #the-line, #the-direction): forward from (now, before, r) to (next, now, r'), backward from (next, now, r') to (now, before, r), the six arrivals through the Ports of the level the step starts from, each under its Port's read, `fill` read beyond a face (the row's rest)."""
    reads, self_coefficient, wall = rule
    if direction == 1:
        arrived = ports(record.now, wrap, fill)
        nxt, remainder = rule3(
            reads, arrived, self_coefficient, wall, record.now, record.before, record.remainder
        )
        return Record(np.asarray(nxt), record.now, np.asarray(remainder))
    arrived = ports(record.before, wrap, fill)
    back, remainder = rule3(
        reads, arrived, self_coefficient, wall, record.before, record.now, record.remainder, -1
    )
    return Record(record.before, np.asarray(back), np.asarray(remainder))


def turned_ports(
    now: tuple[Any, Any], links: tuple[Any, Any, Any], wall: int, wrap: Wrap
) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """The six arrivals of a plane's two lines with the phase on the Link, in Port order (ALGEBRA.md #the-rows-against-nature (b2), Peierls' coupling): the pair arriving through the +a Port turned by the angle with tan(theta_a / 2) = (L_a(i) + L_a(i + a)) / wall, the Link's odd level the mean of its two ends' over Gamma at the wall 4 Gamma, and the pair through the -a Port turned by the opposite angle of its own Link, (L_a(i - a) + L_a(i)); the re arrivals and the im arrivals, each under its Port's read (features/rotation)."""
    re, im = [], []
    for axis, level in enumerate(links):
        ahead, behind = level + arrival(level, axis, 1, wrap), level + arrival(level, axis, -1, wrap)
        plus = rotation.turned(
            arrival(now[0], axis, 1, wrap), arrival(now[1], axis, 1, wrap), ahead, wall
        )
        minus = rotation.turned(
            arrival(now[0], axis, -1, wrap), arrival(now[1], axis, -1, wrap), -behind, wall
        )
        re += [plus[0], minus[0]]
        im += [plus[1], minus[1]]
    return tuple(re), tuple(im)


def step_plane(
    re: Record, im: Record, rule: Rule, wrap: Wrap, angles: Angles, gamma: int, direction: int = 1
) -> tuple[list[Record], Booking]:
    """Rule3 on a plane's two lines under the rotation (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; features/rotation): with z = re + i im and theta the angle with tan(theta / 2) = L / (2 Gamma), L the holder's time level at the Node (exactly theta = 2 arctan(L / (2 Gamma)), L / Gamma to the third order), the equation the engine implements is e^(i theta) z_next + e^(-i theta) z_before = (S z_now + SUM over the Ports of R_ij (e^(i theta_a) z_(+a) or e^(-i theta_a) z_(-a))) / w; the law's line as written is e^(-i theta) z_next + e^(i theta) z_before = the same right side, the opposite sign of theta, and ALGEBRA.md states both (the engine's convention the declared bit, the two differing by the sign of theta alone); the tangent half-angles L / (2 Gamma) and, on the Link ij, (L_a(i) + L_a(j)) / (4 Gamma) (`turned_ports`), the turn against the sense of the record of positive Wronskian, which then rotates faster by theta: forward the level before is turned, u = e^(-i theta) z_before, Rule3 steps re and im with one rule and their own remainders against u, each neighbour's pair arriving turned through its Port, and the result v is turned the same way, z_next = e^(-i theta) v; backward v = e^(i theta) z_next undoes the turn, Rule3 at -1 gives u and the remainders back and e^(i theta) u the level before, bit for bit. Returns the two lines and the booking (first, second) the form and the Wronskian are read from, D = form(first, second) = |z_now|^2 - v . u and W = wronskian(second) = Im(conj(v) z_now), the bookings carrying the angle (the step's levels before the turn), the same numbers in either direction."""
    reads, self_coefficient, wall = rule
    time, links = angles
    half = 2 * gamma  # the time turn's wall, tan(theta / 2) = L / (2 Gamma); the Link's twice it
    now = (level_at(re, direction), level_at(im, direction))
    other = (re.before, im.before) if direction == 1 else (re.now, im.now)
    arrived = turned_ports(now, links, 2 * half, wrap)
    turned_other = rotation.turned(other[0], other[1], -time, half, direction)
    stepped = []
    for part, (record, through) in enumerate(zip((re, im), arrived, strict=True)):
        level, remainder = rule3(
            reads,
            through,
            self_coefficient,
            wall,
            now[part],
            turned_other[part],
            record.remainder,
            direction,
        )
        stepped.append((np.asarray(level), np.asarray(remainder)))
    out = rotation.turned(stepped[0][0], stepped[1][0], -time, half, direction)
    u, v = (
        (turned_other, [s[0] for s in stepped])
        if direction == 1
        else ([s[0] for s in stepped], turned_other)
    )
    lines = [
        Record(np.asarray(out[part]), record.now, stepped[part][1])
        if direction == 1
        else Record(record.before, np.asarray(out[part]), stepped[part][1])
        for part, record in enumerate((re, im))
    ]
    first = [Record(now[part], np.asarray(u[part]), lines[part].remainder) for part in range(2)]
    second = [Record(np.asarray(v[part]), now[part], lines[part].remainder) for part in range(2)]
    return lines, (first, second)


def step_family(
    index: int,
    families: tuple[FamilyRule, ...],
    states: list[NodeState],
    rule: Rule,
    wrap: Wrap,
    gamma: int,
    direction: int = 1,
) -> tuple[list[Record], Booking]:
    """Every line of a family stepped by Rule3 in `direction` with its rule (ALGEBRA.md #the-interval): line by line (`step`), the time line of a holder of the content reading its rest beyond every face, or, where the family's record is turned (`turning`), each part's plane as one (`step_plane`); with the lines, the booking (first, second) the form D = form(first, second) and the Wronskian W = wronskian(second) are read from, the lines the step started from and the lines it left for a plain step, the step's levels before the turn for a turned one."""
    family, state = families[index], states[index]
    angles = turning(index, families, states, direction)
    if angles is None:
        found = [
            step(record, rule, wrap, direction, family.rest if number == 0 else 0)
            for number, record in enumerate(state.lines)
        ]
        return found, ((state.lines, found) if direction == 1 else (found, state.lines))
    lines: list[Record] = []
    first: list[Record] = []
    second: list[Record] = []
    for start in range(0, family.lines, family.width):
        planes = state.lines[start], state.lines[start + 1]
        found, (begun, left) = step_plane(*planes, rule, wrap, angles, gamma, direction)
        lines, first, second = lines + found, first + begun, second + left
    return lines, (first, second)


def sense_current_of(lines: Sequence[Record], wrap: Wrap) -> currents.Vector:
    """The sign's current of a two-part record at every Node on each axis, the mean of the Node's two a-Links' Wronskian currents, a reading of its planes' lines at the interval's start: J_a(i) = Im(conj(z_i) (z_(i+a) - z_(i-a))) = re_i (im_(+a) - im_(-a)) - im_i (re_(+a) - re_(-a)) = (G_(i, i-a) - G_(i, i+a)) / num, the net of the conserved current G_ij = num (im_i re_j - re_i im_j) through the Node's two a-Ports from the levels now, every plane's added, one Link's reach, and the source its mean over the two Links, (J_a + 1) div 2 by the division act rounded as the read rounds the Link's tension (`features/read`, `link_tension`), as the tension on an axis is the mean of its two Links' stresses (ALGEBRA.md #the-primitives, The tension); odd under the sense within that rounding unit (a record and its conjugate give opposite currents, where the momentum density P_a = (F_(+a) - F_(-a)) / num, quadratic in each real line, gave the same), even under the time reversal; the source of the holder of the sign's odd lines under the rotation at the wall den T, J_a = (6 den / num) W v on a plane record, so that the magnetic over the electric force on a co-moving reader is 1 / gamma where J_a unhalved doubled the magnetic term (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; the owner's word of 2026-10-01, 17:17, on the two hands, the mathematician's #1572 comment 5932451234 and the advisor's 5932831736 and 5933191332)."""
    found: list[Any] = [0, 0, 0]
    for re_line, im_line in zip(lines[0::2], lines[1::2], strict=True):
        re_at, im_at = ports(re_line.now, wrap), ports(im_line.now, wrap)
        for axis in range(3):
            plus, minus = 2 * axis, 2 * axis + 1
            found[axis] = (
                found[axis]
                + re_line.now * (im_at[plus] - im_at[minus])
                - im_line.now * (re_at[plus] - re_at[minus])
            )
    x, y, z = (division_forward(current, currents.AXIS_PORTS, 1)[0] for current in found)
    return np.asarray(x), np.asarray(y), np.asarray(z)


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
    """The tension's part at every Node on each axis from a record's levels now as they stand at the interval's start, weight x h_a(i) with h_a(i) = now_(i-a) now_(i+a) - now_i^2, every line's parts added, a reading of the lines into the held rows' axis lines, one Link's reach (features/currents; ALGEBRA.md #the-primitives, the row "the hold", The tension)."""
    tensions: currents.Vector = (0, 0, 0)
    for record in lines:
        found = currents.stress(weight, axis_neighbours(record.now, wrap))
        tensions = (tensions[0] + found[0], tensions[1] + found[1], tensions[2] + found[2])
    return tuple(np.asarray(value) for value in tensions)  # type: ignore[return-value]


def axis_neighbours(
    now: np.ndarray, wrap: Wrap
) -> tuple[currents.Neighbours, currents.Neighbours, currents.Neighbours]:
    """The level now at every Node and at its two neighbours along each axis, through the +a and the -a Port, the tension's reads (ALGEBRA.md #the-primitives, the row "the hold", The tension)."""
    arrived = ports(now, wrap)
    found = [currents.Neighbours(now, arrived[2 * axis], arrived[2 * axis + 1]) for axis in range(3)]
    return found[0], found[1], found[2]


def form(begun: Sequence[Record], stepped: Sequence[Record]) -> Any:
    """The record's form at every Node over one interval, D_i = now^2 - next x before from the three levels around the step summed over its lines (`begun` holds (now, before) at the interval's start, `stepped` holds next as its `now`): the source of the rows that hold the content."""
    total: Any = 0
    for before, after in zip(begun, stepped, strict=True):
        total = total + (before.now * before.now - after.now * before.before)
    return total


def wronskian(lines: Sequence[Record], plane: bool) -> Any:
    """The Wronskian of a plane's two lines at every Node, W_i = re_now im_before - im_now re_before, the booking of the rotation sense, the charge density, summed over the record's planes: the source of the row that holds the sign; the integer 0 for a record of real lines (one line, or the pair family's two never summed at a Node), which has no plane (ALGEBRA.md #a-familys-declaration)."""
    if not plane:
        return 0
    total: Any = 0
    for re, im in zip(lines[0::2], lines[1::2], strict=True):
        total = total + (re.now * im.before - im.now * re.before)
    return total


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
    """The numerators of a held family's one write per line at every Node (ALGEBRA.md #the-primitives, the row "the hold"; the integer 0 where nothing sources a line): for the time line SUM over the sourcing families (its readers, by the hold's reciprocity) of w x q, q the booking of each that the row's sources name, the form D for a row sourced by the form and the Wronskian W for the holder of the sign (`bookings`); for each axis line SUM over the sources of w x factor x the axis booking of each, its tension's part for a row of the content and its sign current, the mean of its two a-Links' Wronskian currents J_a / 2, for the holder of the sign under the rotation (`stresses`, the readers' vectors), times its factor of the common wall (`HeldWrite`, one wall per line)."""
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
