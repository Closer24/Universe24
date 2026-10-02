"""The Node: every family's NodeState over the GameBoard, a flat list of lines of dimension one and the law's numbers and nothing else, and the interval's acts on it as pure functions of whole-board arrays, each a call of Rule3 (core/rule3.py) with every neighbour read through a Port (core/ports.py), one Link's reach for every act (ALGEBRA.md #the-interval, the dependency radius): the read, the content at the Node into the composed clock and the Node's pace, the clock twice, with each Link's own factor from its tension (#the-paces; the guard once at load), Rule3 on every line (#the-line, #the-direction), the readings of the lines at the interval's start (the currents and the tension's part at the Node, features/currents; the form and the Wronskian about the step; the count is the record's share, #the-count-is-the-records-share) and the one write per held line (#the-primitives, the row "the hold"). The step knows no family, no dimension and no name: it receives lines with their coefficients, their sources and their readers (the loader's grouping, loader/derived.py)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import PORTS, coefficients, division_forward, rule3
from event_universe.features import currents, rotation
from event_universe.features.hold import hold
from event_universe.features.read import axis_paces, content_of, guard, link_factors, link_tensions
from event_universe.loader.derived import FamilyRule, row_of, turns
from event_universe.records import (  # the lines, their readings and their states, the Node's own
    Booking as Booking,
)
from event_universe.records import (
    Families as Families,
)
from event_universe.records import (
    NodeState as NodeState,
)
from event_universe.records import (
    Record as Record,
)
from event_universe.records import (
    Rulers as Rulers,
)
from event_universe.records import (
    Sourcing as Sourcing,
)
from event_universe.records import (
    States as States,
)
from event_universe.records import (
    empty_record as empty_record,
)
from event_universe.records import (
    empty_state as empty_state,
)
from event_universe.records import (
    form as form,
)
from event_universe.records import (
    full as full,
)
from event_universe.records import (
    largest as largest,
)
from event_universe.records import (
    level_at as level_at,
)
from event_universe.records import (
    light_record as light_record,
)
from event_universe.records import (
    record_slice as record_slice,
)
from event_universe.records import (
    row_levels as row_levels,
)
from event_universe.records import (
    turned_by as turned_by,
)
from event_universe.records import (
    well as well,
)
from event_universe.records import (
    write_origins as write_origins,
)
from event_universe.records import (
    write_sources as write_sources,
)
from event_universe.records import (
    written as written,
)
from event_universe.records import (
    wronskian as wronskian,
)
from event_universe.records import (
    zeros as zeros,
)

Rule = tuple[tuple[Any, ...], Any, Any]  # Rule3's integers at every Node: the six Ports' R_ij, S, w
Factors = tuple[Any, ...]  # the factor Q_ij of a Node's six Links in Port order, in the unit G^2
Angles = tuple[Any, tuple[Any, Any, Any]]  # the turn's numerators at every Node: the time's, each axis's


def ports(a: np.ndarray, wrap: Wrap, fill: int = 0) -> tuple[np.ndarray, ...]:
    """The six arrivals of an array in Port order [+X, -X, +Y, -Y, +Z, -Z]: the neighbour's level through each Port, `fill` beyond a face that does not wrap (0, or the row's rest for the massless row holding the content: the vacuum beyond the face is the same vacuum, ALGEBRA.md #what-is-open, item 22), the Node itself on a folded axis."""
    return tuple(arrival(a, axis, side, wrap, fill) for axis in range(3) for side in (1, -1))


def read_lines(
    index: int, families: Families, states: States, direction: int, record: int = 0
) -> tuple[Any, list[Any]]:
    """The lines a record's read takes at the interval's start in `direction` (ALGEBRA.md #the-paces, Every row reads the content): the content c = SUM over its reads of the holders acting on the pace of (weight x the read family's time line at the level the step in `direction` starts from, `level_at`), a held row of the content reading its own level among them and a holder of the sign read as the sum of every row but the record's own (`row_levels`, `derived.row_of`), and per read row carrying axis lines its weight and its three axis lines at the same level; the integer 0 and no axis lines where it reads nothing (the plain rule at Gamma); a holder declaring the rotation enters no pace (`turning`)."""
    reads = [r for r in families[index].reads if not families[r.family].rotation]
    own = row_of(families, index, record)
    content = content_of(
        [
            (r.weight, row_levels(families[r.family], states[r.family].lines, 0, direction, own))
            for r in reads
        ]
    )
    rows = [r for r in reads if families[r.family].axes]
    return content, [
        (r.weight, [level_at(states[r.family].lines[1 + a], direction) for a in range(3)]) for r in rows
    ]


def read(
    index: int,
    families: Families,
    states: States,
    direction: int,
    wrap: Wrap,
    gamma: int,
    unit: int,
    record: int = 0,
) -> tuple[Any, Factors]:
    """The read of a record of a family at the interval's start (ALGEBRA.md #the-paces, Every row reads the content; The clock is the Node's, the tension is the Link's; #the-interval, the dependency radius): the content at every Node (`read_lines`, every sign row but the record's own) and the factor of each of its six Links, Q_ij from the Link's tension, the read rows' axis lines at its two ends, (weight x (aa_i + aa_j) + 1) div 2, the neighbour's line read through the Port the arrival is read through, one number per Link read the same from both ends, booked once per Link in the unit G^2 (features/read, `link_tensions`, `link_factors`); the integer 0 at the Node and G^2 on every Link where it reads nothing (the plain rule at Gamma); no floor, no clamp and no guard in the interval; the same levels read back, so the inverse reads the same paces."""
    if not any(not families[r.family].rotation for r in families[index].reads):
        return 0, (unit * unit,) * PORTS
    content, axes = read_lines(index, families, states, direction, record)
    return content, link_factors(gamma, unit, link_tensions(axes, wrap))


def rulers(
    index: int,
    families: Families,
    states: States,
    direction: int,
    wrap: Wrap,
    gamma: int,
    record: int = 0,
) -> Rulers:
    """The paces a record's read gives it at every Node for the write's factor (ALGEBRA.md, The write per proper volume and per proper interval; The paces compose): the clock p_0 from its content and its pace along each axis, p_a = p_i (q_(+a) + q_(-a)) / (2 Gamma), the Node's pace p_i = p_0^2 / Gamma times the mean of its two a-Links' factors from their tensions, one reading per axis through its two Ports (`features/read`, `axis_paces`), the ruler h_a = p_0 / p_a; Gamma on the clock and on every axis where the family reads nothing (every factor 1 at the vacuum's paces); read at the level the step in `direction` starts from, the same numbers read back."""
    if not any(not families[r.family].rotation for r in families[index].reads):
        return gamma, (gamma, gamma, gamma)
    content, axes = read_lines(index, families, states, direction, record)
    clock, pace = paces.node_paces(gamma, content)
    return clock, axis_paces(gamma, pace, link_tensions(axes, wrap))


def turning(
    index: int, families: Families, states: States, direction: int, gamma: int, record: int = 0
) -> Angles | None:
    """The angles a turned record reads (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; The turn per proper interval): from every holder it reads that declares the rotation, the time angle's numerator SUM of (weight x the holder's time line summed over every row but the record's own, `row_levels`) scaled by the turned family's own clock, p_0 / Gamma from the content it reads (`turned_by`, the angle per proper interval), and each axis's SUM of (weight x the holder's odd line a over the same rows) as it is, at every Node, at the level the step in `direction` starts from (the same number read back, so the inverse is explicit); None where the family's record is not turned (`derived.turns`: a one-part family, or every holder acting on the pace)."""
    if not turns(families, index):
        return None
    reads = [r for r in families[index].reads if families[r.family].rotation]
    own = row_of(families, index, record)
    levels = [
        content_of(
            [
                (r.weight, row_levels(families[r.family], states[r.family].lines, line, direction, own))
                for r in reads
            ]
        )
        for line in range(1 + 3)
    ]
    clock = paces.clock_of(gamma, read_lines(index, families, states, direction, record)[0])
    return turned_by(levels[0], clock, gamma), (levels[1], levels[2], levels[3])


def guarded(index: int, families: Families, states: States, gamma: int, wrap: Wrap, unit: int) -> None:
    """The guard once at load (ALGEBRA.md #the-paces, The guard): every record's read of the initial state checked as squares, the content below the Link's zero (the lower side, a frozen clock refused by name) and p^2 (den + num) <= 2 den Gamma^2 at every Node on the clock, on the Node's pace and on each Link's pace p_i^2 Q_ij / G^2, refused by name outside; a family that reads nothing stands at Gamma, inside; no act of the interval reads it (features/read). A turned record's angles alike (features/rotation, `guard`): the time angle's numerator within 2 Gamma and each Link's two ends' sum within 4 Gamma, a tangent half-angle at most 1."""
    for record in range(families[index].records):
        if families[index].reads:
            content, factors = read(index, families, states, 1, wrap, gamma, unit, record)
            guard(families[index].pair, gamma, unit, content, factors, families[index].name)
        angles = turning(index, families, states, 1, gamma, record)
        if angles is not None:
            time, links = angles
            rotation.guard(time, 2 * gamma, families[index].name, None)
            for a in range(3):
                for side in (1, -1):
                    link = links[a] + arrival(links[a], a, side, wrap)
                    rotation.guard(link, 2 * 2 * gamma, families[index].name, a)


def least_pace(index: int, families: Families, states: States, gamma: int, wrap: Wrap, unit: int) -> int:
    """The least Node pace p_i = p_0^2 / Gamma of a family's records over the GameBoard as it stands, 0 at a frozen Node, a GameBoard diagnostic for the report and no act of the law (the Links' factors beside it are read by no report)."""
    return min(
        int(
            np.min(
                paces.link_pace_of(gamma, read(index, families, states, 1, wrap, gamma, unit, record)[0])
            )
        )
        for record in range(families[index].records)
    )


def rule_of(
    family: FamilyRule, gamma: int, content: Any, factors: Factors | None = None, unit: int = 1
) -> Rule:
    """The rule every line of a family steps by, Rule3's integers at every Node from its pair and the paces of its read, the clock and the Node's pace from the Node's content (`paces.node_paces`, The paces compose) and each Link's factor (ALGEBRA.md #the-line; #the-interval): a family of quanta's (the holder of the sign included, its line its record) and a held row's alike, the row's own level among the content it reads (Every row reads the content); None no tension, G^2 on every Link."""
    num, den = family.pair
    clock, pace = paces.node_paces(gamma, content)
    return coefficients(num, den, gamma, clock, pace, factors, unit)


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
    families: Families,
    states: States,
    rule: Rule,
    wrap: Wrap,
    gamma: int,
    direction: int = 1,
    record: int = 0,
) -> tuple[list[Record], Booking]:
    """Every line of one record of a family stepped by Rule3 in `direction` with its rule (ALGEBRA.md #the-interval): line by line (`step`), the time line of a holder of the content reading its rest beyond every face, or, where the family's record is turned (`turning`, the angles every sign row's but the record's own), each part's plane as one (`step_plane`); with the lines, the booking (first, second) the form D = form(first, second) and the Wronskian W = wronskian(second) are read from, the lines the step started from and the lines it left for a plain step, the step's levels before the turn for a turned one."""
    family, state = families[index], states[index]
    span = record_slice(family, record)
    own = state.lines[span]
    angles = turning(index, families, states, direction, gamma, record)
    if angles is None:
        found = [
            step(line, rule, wrap, direction, family.rest if number == 0 else 0)
            for number, line in enumerate(own, span.start)
        ]
        return found, ((own, found) if direction == 1 else (found, own))
    lines: list[Record] = []
    first: list[Record] = []
    second: list[Record] = []
    for start in range(0, len(own), family.width):
        planes = own[start], own[start + 1]
        found, (begun, left) = step_plane(*planes, rule, wrap, angles, gamma, direction)
        lines, first, second = lines + found, first + begun, second + left
    return lines, (first, second)


def step_records(
    index: int,
    families: Families,
    states: States,
    wrap: Wrap,
    gamma: int,
    unit: int,
    direction: int = 1,
) -> tuple[list[Record], list[Booking]]:
    """Every record of a family stepped by Rule3 in `direction`, each with the rule of its own read (`read`, `rule_of`: the content and the six Links' factors from the held rows' levels the step starts from, every sign row but the record's own) and its own angles (`step_family`); the lines in the records' order and one booking per record, the lines its form and its Wronskian are read from."""
    lines: list[Record] = []
    bookings: list[Booking] = []
    for record in range(families[index].records):
        content, factors = read(index, families, states, direction, wrap, gamma, unit, record)
        rule = rule_of(families[index], gamma, content, factors, unit)
        found, booking = step_family(index, families, states, rule, wrap, gamma, direction, record)
        lines, bookings = lines + found, bookings + [booking]
    return lines, bookings


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


def held_write(
    lines: Sequence[Record],
    numerators: Sequence[Any],
    walls: Sequence[int],
    remainders: Sequence[np.ndarray],
    direction: int = 1,
) -> tuple[list[Record], list[np.ndarray]]:
    """A held family's one write per line (ALGEBRA.md #the-primitives, the row "the hold"), its lines already stepped by Rule3 in the interval's second act, with or without a gap: each line's level gains (numerator + r) div wall by the write's carried division (features/hold) with the one remainder kept at the Node; backward the increments taken off and the remainders stepped back, exact; returns the lines and the remainders after."""
    found, after = [], []
    for line, numerator, wall, remainder in zip(lines, numerators, walls, remainders, strict=True):
        level, kept = hold(line.now, numerator, wall, remainder, direction)
        found.append(replace(line, now=np.asarray(level)))
        after.append(np.asarray(kept))
    return found, after
