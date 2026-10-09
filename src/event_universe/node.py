"""The Node: every family's NodeState over the lattice, a flat list of lines of dimension one and the law's numbers and nothing else, and the interval's acts on it as pure functions of whole-board arrays, each a call of Rule3 (core/rule3.py) with every neighbour read through a Port (core/ports.py), one Link's reach for every act (ALGEBRA.md #the-interval, the dependency radius): the read, the content at the Node into the composed clock and the Node's pace, the clock twice, with each Link's own factor from its tension (#the-paces; the guard once at load), Rule3 on every line (#the-line, #the-direction), the readings of the lines at the interval's start (the currents and the tension's part at the Node, features/currents; the form and the Wronskian about the step; the count is the record's share, #the-count-is-the-records-share) and the one write per held line (#the-primitives, the row "the held write"). The step knows no family, no dimension and no name: it receives lines with their coefficients, their sources and their readers (the loader's grouping, loader/derived.py)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import AXES, PORTS, Wrap, arrival
from event_universe.core.rule3 import coefficients, rule3
from event_universe.features import currents, phase
from event_universe.features.click import presented
from event_universe.features.held_write import held_write
from event_universe.features.read import (
    axis_paces,
    content_of,
    link_factors,
    link_tensions,
    paces_guard,
    plain,
)
from event_universe.loader.derived import PLANE, FamilyRule, row_of, turns, weight_of
from event_universe.plane import (
    NO_FACE,
    Angles,
    Faces,
    Phases,
    Rule,
    fold_guard,
    link_guard,
    link_levels,
    link_pairs,
    link_wall,
    odd_links,
    phase_links,
    step_plane,
)
from event_universe.records import (  # the lines, their readings and their states, the Node's own
    Booking as Booking,
)
from event_universe.records import Families as Families
from event_universe.records import NodeState as NodeState
from event_universe.records import Record as Record
from event_universe.records import Rulers as Rulers
from event_universe.records import Sourcing as Sourcing
from event_universe.records import States as States
from event_universe.records import empty_record as empty_record
from event_universe.records import empty_state as empty_state
from event_universe.records import form as form
from event_universe.records import full as full
from event_universe.records import largest as largest
from event_universe.records import level_at as level_at
from event_universe.records import phase_lines as phase_lines
from event_universe.records import record_slice as record_slice
from event_universe.records import row_levels as row_levels
from event_universe.records import rows_total as rows_total
from event_universe.records import rulers_write_factor as rulers_write_factor
from event_universe.records import well as well
from event_universe.records import write_origins as write_origins
from event_universe.records import write_sources as write_sources
from event_universe.records import wronskian as wronskian
from event_universe.records import zeros as zeros

Factors = tuple[Any, ...]  # the factor Q_ij of a Node's six Links in Port order, in the unit G^2


def ports(a: np.ndarray, wrap: Wrap, fill: int = 0) -> tuple[np.ndarray, ...]:
    """The six arrivals of an array in Port order [+X, -X, +Y, -Y, +Z, -Z]: the neighbour's level through each Port, `fill` beyond a face that does not wrap (0, or the row's rest for the massless row holding the content: the vacuum beyond the face is the same vacuum, ALGEBRA.md #what-is-open, item 22), the Node itself on a folded axis."""
    return tuple(arrival(a, axis, side, wrap, fill) for axis in range(3) for side in (1, -1))


def read_lines(
    index: int, families: Families, states: States, direction: int, record: int = 0
) -> tuple[Any, list[Any]]:
    """The lines a record's read takes at the interval's start in `direction` (ALGEBRA.md #the-paces, Every row reads the content): the content c = SUM over its reads of the holders acting on the pace of (weight x the read family's time line at the level the step in `direction` starts from, `level_at`), a held row of the content reading its own level among them and a holder of the sign read as the sum of every row but the record's own (`row_levels`, `derived.row_of`), and per read row carrying axis lines its weight and its three axis lines at the same level; the integer 0 and no axis lines where it reads nothing (the plain rule at Gamma); a holder declaring the rotation enters no pace (`turning`)."""
    reads = [r for r in families[index].reads if not families[r.family].rotation]
    own = row_of(families, index, record)
    levels = [
        plain(
            row_levels(families[r.family], states[r.family].lines, 0, direction, own),
            families[r.family].wronskian,
        )
        for r in reads
    ]  # a holder of the sign's level, every row but the reader's own, as the plain read takes it: its size
    content = content_of([(r.weight, level) for r, level in zip(reads, levels, strict=True)])
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
    cut: Factors | None = None,
) -> tuple[Any, Factors]:
    """The read of a record of a family at the interval's start (ALGEBRA.md #the-paces, Every row reads the content; The clock is the Node's, the tension is the Link's; #the-interval, the dependency radius): the content at every Node (`read_lines`, every sign row but the record's own) and the factor of each of its six Links, Q_ij from the Link's tension, the read rows' axis lines at its two ends, (weight x (aa_i + aa_j) + 1) div 2, the neighbour's line read through the Port the arrival is read through, one number per Link read the same from both ends, booked once per Link in the unit G^2 (features/read, `link_tensions`, `link_factors`); the integer 0 at the Node and G^2 on every Link where it reads nothing (the plain rule at Gamma); `cut`, per Port the mask of the Links the world declares at the factor 0, the six Links of a body that is a NodeDetector, read 0 from both ends so that its record stays at its Node (ALGEBRA.md, The click writes on the lattice; the frozen Link, the world's declaration as the node_detector's region is); no floor, no clamp and no guard in the interval; the same levels read back, so the inverse reads the same paces."""
    if not any(not families[r.family].rotation for r in families[index].reads):
        factors: Factors = (unit * unit,) * PORTS
        content: Any = 0
    else:
        content, axes = read_lines(index, families, states, direction, record)
        factors = link_factors(gamma, unit, link_tensions(axes, wrap))
    if cut is not None:
        factors = tuple(np.where(mask, 0, factor) for mask, factor in zip(cut, factors, strict=True))
    return content, factors


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
    index: int, families: Families, states: States, direction: int, record: int = 0
) -> Angles | None:
    """The sign's levels a turned record reads (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; features/phase): from every holder it reads that declares the rotation, the time level SUM of (weight x the holder's time line summed over every row but the record's own, `row_levels`), the potential whose difference across each Link iterates the Link's phase pair (`phased`, n_ij = L(i) - L(j); no clock scaling: the angle per act is theta_0 = 1 / Gamma and the field the count of acts, the mathematician's item (g)), and each axis's SUM of (weight x the holder's odd line a over the same rows) as it is, at every Node, at the level the step in `direction` starts from (the same number read back, so the inverse is explicit); None where the family's record is not turned (`derived.turns`: a one-part family, or every holder acting on the pace)."""
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
        for line in range(1 + AXES)  # the time line and the three axis lines
    ]
    return levels[0], (levels[1], levels[2], levels[3])


def sign_holder(index: int, families: Families) -> int:
    """The one holder of the sign under the rotation a turned family reads, whose phase lines its records read (`phased`, `step_records`); the energy line's holder (`derived.energy_line`); refused by name where a family reads more than one (the Link's phase is one pair per Link, one holder's)."""
    holders = [r.family for r in families[index].reads if families[r.family].rotation]
    if len(holders) != 1:
        raise ValueError(
            f"{families[index].name!r} reads {len(holders)} holders under the rotation, and the Link's phase "
            "is one pair per Link, one holder's: a plane reads one holder of the sign under the rotation"
        )
    return holders[0]


def phased(
    index: int, families: Families, states: States, direction: int, wrap: Wrap, gamma: int
) -> list[list[Record]]:
    """The phase act of one interval on a holder of the sign under the rotation (features/phase, `iterate`; the mathematician's item (g) and the two hands' item (i); ALGEBRA.md, The sign holder rotates the two-part record): for every row of the sign beyond the free row, the row's reader's potential L at every Node, the holder's time level summed over every row but that row (`row_levels`, at the weight the reader reads with, `weight_of`; No record reads its own write of the sign), read at the interval's start (the level now, the state as the interval begins, in either direction), and on each axis the Link's count n_ij = L(i) - L(i + a), the potential's difference across the Node's +a Link, 0 beyond a face (`arrival`), by which the Link's cosine and sine lines take |n_ij| rotation acts in n's sense (the pair then at X e^(i SUM_t n_ij theta_0), the temporal gauge's Link phase), forward; at `direction` -1 the same acts back, bit for bit, the inverse's act once every line stands at the interval's start again (`Lattice.step_inverse`); one Link's reach, the two ends. Returns the rows' phase lines after the act, the state untouched."""
    family, state = families[index], states[index]
    readers = {
        row_of(families, reader, record): (reader, record)
        for reader, other in enumerate(families)
        if turns(families, reader) and weight_of(index, other)
        for record in range(other.records)
    }
    found: list[list[Record]] = []
    for row, lines in enumerate(state.phases):
        if row == 0 or row not in readers:
            found.append(list(lines))
            continue
        reader = families[readers[row][0]]
        potential = weight_of(index, reader) * row_levels(family, state.lines, 0, 1, row)
        turned: list[Record] = []
        for axis in range(AXES):
            neighbour = arrival(potential, axis, 1, wrap)
            beyond = (
                arrival(np.ones_like(np.asarray(potential)), axis, 1, wrap) == 0
            )  # the Link beyond a face
            count = np.where(beyond, 0, potential - neighbour)
            cosine, sine = lines[2 * axis], lines[2 * axis + 1]
            pair = phase.iterate(
                ((cosine.now, cosine.before, cosine.remainder), (sine.now, sine.before, sine.remainder)),
                count,
                gamma,
                direction,
            )
            turned += [Record(*(np.asarray(a) for a in line)) for line in pair]
        found.append(turned)
    return found


def guarded(index: int, families: Families, states: States, gamma: int, wrap: Wrap, unit: int) -> None:
    """The guard once at load (ALGEBRA.md #the-paces, The guard): every record's read of the initial state checked as squares, the content below the Link's zero (the lower side, a frozen clock refused by name) and p^2 (den + num) <= 2 den Gamma^2 at every Node on the clock, on the Node's pace and on each Link's pace p_i^2 Q_ij / G^2, refused by name outside; a family that reads nothing stands at Gamma, inside; no act of the interval reads it (features/read). A turned record's Links alike (`plane.link_guard`): each Link's two ends' sum n_ij of the sign's odd lines within 4 Gamma, a tangent half-angle at most 1, the guard on n the fold's Link keeps (`plane.sign_pairs`); the time level is guarded by nothing, the phase line's circle wrapping (features/phase); one holder of the sign under the rotation per turned family (`sign_holder`)."""
    for record in range(families[index].records):
        if families[index].reads:
            content, factors = read(index, families, states, 1, wrap, gamma, unit, record)
            paces_guard(families[index].pair, gamma, unit, content, factors, families[index].name)
        links = odd_links(index, families, states, 1, wrap)
        if links is not None:  # a folded record's fold at every Link within the tangent 1
            fold_guard(families[index].pair, gamma, links, families[index].name)
        angles = turning(index, families, states, 1, record)
        if angles is not None:  # a turned record's Links at both ends
            sign_holder(index, families)
            for a in range(3):
                for side in (1, -1):
                    link = angles[1][a] + arrival(angles[1][a], a, side, wrap)
                    link_guard(link, link_wall(gamma), families[index].name, a)


def least_pace(index: int, families: Families, states: States, gamma: int, wrap: Wrap, unit: int) -> int:
    """The least Node pace p_i = p_0^2 / Gamma of a family's records over the lattice as it stands, 0 at a frozen Node, a lattice diagnostic for the report and no act of the law (the Links' factors beside it are read by no report)."""
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


def step(
    record: Record, rule: Rule, wrap: Wrap, direction: int = 1, fill: int = 0, faces: Faces = NO_FACE
) -> Record:
    """Rule3 on one line (ALGEBRA.md #the-line, #the-direction): forward from (now, before, r) to (next, now, r'), backward from (next, now, r') to (now, before, r), the six arrivals through the Ports of the level the step starts from, each under its Port's read, `fill` read beyond a face (the row's rest), and where the click act presents a face at a Node its value in the place of that Port's arrival (features/click, `presented`), forward computed and kept, backward the kept one."""
    reads, self_coefficient, wall = rule
    level, other = (record.now, record.before) if direction == 1 else (record.before, record.now)
    arrived = ports(level, wrap, fill)
    if faces[0]:
        arrived = presented(
            arrived, reads, self_coefficient, wall, level, other, record.remainder, *faces, direction
        )
    found, remainder = rule3(
        reads, arrived, self_coefficient, wall, level, other, record.remainder, direction
    )
    if direction == 1:
        return Record(np.asarray(found), record.now, np.asarray(remainder))
    return Record(record.before, np.asarray(found), np.asarray(remainder))


def step_family(
    index: int,
    families: Families,
    states: States,
    rule: Rule,
    wrap: Wrap,
    gamma: int,
    direction: int = 1,
    record: int = 0,
    faces: Mapping[int, Faces] | None = None,
    pairs: tuple[Factors, Factors] | None = None,
) -> tuple[list[Record], Booking]:
    """Every line of one record of a family stepped by Rule3 in `direction` with its rule (ALGEBRA.md #the-interval): line by line (`step`), the time line of a holder of the content reading its rest beyond every face, or, where the family's record is turned or folded (`pairs`, each Link's read as the pair (R^c, R^s) from the sign holder's odd lines with the Link's phase pair and the flux holder's odd lines, `plane.link_pairs`, the caller's, as `step_records` computes it from the record's read; ALGEBRA.md, The clock family on the Ports; features/phase), each part's plane as one (`step_plane`), every line with the faces the click act presents to it at this step (`faces`, per line number); with the lines, the booking (first, second) the form D = form(first, second) and the Wronskian W = wronskian(second) are read from, the lines the step started from and the lines it left."""
    family, state = families[index], states[index]
    span = record_slice(family, record)
    own = state.lines[span]
    faced = dict(faces or {})
    if pairs is None:
        found = [
            step(
                line,
                rule,
                wrap,
                direction,
                family.rest if number == 0 else 0,
                faced.get(number, NO_FACE),
            )
            for number, line in enumerate(own, span.start)
        ]
        return found, ((own, found) if direction == 1 else (found, own))
    lines: list[Record] = []
    first: list[Record] = []
    second: list[Record] = []
    for start in range(0, len(own), PLANE):  # plane by plane, each its two lines, re and im
        pair = own[start], own[start + 1]
        at = faced.get(span.start + start, NO_FACE), faced.get(span.start + start + 1, NO_FACE)
        found, (begun, left) = step_plane(*pair, rule, wrap, gamma, direction, at, pairs)
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
    cut: Factors | None = None,
    faces: Mapping[int, Faces] | None = None,
    amplitude: int = 0,
) -> tuple[list[Record], list[Booking]]:
    """Every record of a family stepped by Rule3 in `direction`, each with the rule of its own read (`read`, `rule_of`: the content and the six Links' factors from the held rows' levels the step starts from, every sign row but the record's own, the Links the world cuts at 0, `cut`), its Links' pairs (`turning`, the sign's odd levels, every sign row but the record's own; `plane.odd_links`, the flux holder's; the record's row's phase lines as they stand after the interval's phase act, read through the six Ports, `plane.phase_links`, at the amplitude X, `amplitude`, features/phase.amplitude; `plane.link_pairs`, the pair (R^c, R^s) per Port; `step_family`), the faces the click act presents at this step among its arrivals (`faces`, per line); the lines in the records' order and one booking per record, the lines its form and its Wronskian are read from."""
    lines: list[Record] = []
    bookings: list[Booking] = []
    for record in range(families[index].records):
        content, factors = read(index, families, states, direction, wrap, gamma, unit, record, cut)
        rule = rule_of(families[index], gamma, content, factors, unit)
        angles = turning(index, families, states, direction, record)
        flux = odd_links(index, families, states, direction, wrap)  # the fold, a folded plane's
        sign = None if angles is None else link_levels(angles[1], wrap)  # the sign's Link levels n_ij
        phases: Phases | None = None
        if angles is not None:  # the record's row's phase pairs, the Link's hop through each Port
            row = row_of(families, index, record)
            assert row is not None
            if amplitude < 1:
                raise ValueError(
                    f"{families[index].name!r} reads the sign's phase lines and the step was given no amplitude X "
                    "for the fold: the caller passes features/phase.amplitude of the width"
                )
            phases = phase_links(states[sign_holder(index, families)].phases[row], wrap)
        pairs = link_pairs(families[index].pair, gamma, content, factors, flux, sign, phases, amplitude)
        found, booking = step_family(
            index, families, states, rule, wrap, gamma, direction, record, faces, pairs
        )
        lines, bookings = lines + found, bookings + [booking]
    return lines, bookings


def sense_current_of(lines: Sequence[Record], wrap: Wrap) -> currents.Vector:
    """The sign's current of a two-part record at every Node on each axis, the Node's two a-Links' Wronskian currents summed, a reading of its planes' lines at the interval's start: J_a(i) = Im(conj(z_i) (z_(i+a) - z_(i-a))) = re_i (im_(+a) - im_(-a)) - im_i (re_(+a) - re_(-a)) = (G_(i, i-a) - G_(i, i+a)) / num, the net of the conserved current G_ij = num (im_i re_j - re_i im_j) through the Node's two a-Ports from the levels now, every plane's added, one Link's reach, unhalved (the mathematician's (L2) and the advisor's (c) of 2026-10-09: the halving (J_a + 1) div 2 retired, half a unit of current per Node per interval, the mean of the two Links taken instead by the doubled wall of the odd lines' write, `loader.derived.held_write_of`, 2 E_s T, as Part A takes the flux's), odd under the sense exactly (a record and its conjugate give opposite currents, where the momentum density P_a = (F_(+a) - F_(-a)) / num, quadratic in each real line, gave the same), even under the time reversal; the source of the holder of the sign's odd lines under the rotation, J_a = (6 den / num) W v on a plane record, so that the odd level over the time level is 3 (den / num) v = v / c_s^2 and the magnetic over the electric force on a co-moving reader is 1 / gamma (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; the owner's word on the two hands)."""
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
    return np.asarray(found[0]), np.asarray(found[1]), np.asarray(found[2])


def currents_of(weight: int, lines: Sequence[Record], wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The currents of a record at every Node, a reading of its lines (ALGEBRA.md #the-count-is-the-records-share; features/currents): through each of the six Ports F_ij = num (now_i before_j - before_i now_j) into the Node from its neighbour, every line's currents added, at the lines as they stand (the pair the step started from, read before Rule3 acts, so that the share's change over the step is exactly their sum); what a node_detector reads at its boundary."""
    found: list[Any] = [0] * 6
    for record in lines:
        here = currents.Levels(record.now, record.before)
        now, before = ports(record.now, wrap), ports(record.before, wrap)
        for port in range(6):
            there = currents.Levels(now[port], before[port])
            found[port] = found[port] + currents.current(weight, here, there)
    return tuple(np.asarray(value) for value in found)


def stresses_of(weight: int, lines: Sequence[Record], wrap: Wrap) -> currents.Vector:
    """The tension's part at every Node on each axis from a record's levels now as they stand at the interval's start, weight x h_a(i) with h_a(i) = now_(i-a) now_(i+a) - now_i^2, every line's parts added, a reading of the lines into the held rows' axis lines, one Link's reach (features/currents; ALGEBRA.md #the-primitives, the row "the held write", The tension)."""
    tensions: currents.Vector = (0, 0, 0)
    for record in lines:
        found = currents.stress(weight, axis_neighbours(record.now, wrap))
        tensions = (tensions[0] + found[0], tensions[1] + found[1], tensions[2] + found[2])
    return tuple(np.asarray(value) for value in tensions)  # type: ignore[return-value]


def axis_sources_of(weight: int, lines: Sequence[Record], wrap: Wrap) -> tuple[Any, ...]:
    """The axis sources of a record at every Node, six readings of its lines at the interval's start, one Link's reach: the tension's part on each axis (`stresses_of`, into the held rows' tension lines), then the count's flux along each axis, the current through the -a Port less the current through the +a Port, F_(i, i-a) - F_(i, i+a) (`currents_of`, the pair the step starts from), the axis's two Links' flux summed unhalved into the flux holder's odd lines (ALGEBRA.md, The clock family on the Ports; a holder without them reads the first three, `write_sources`)."""
    through = currents_of(weight, lines, wrap)
    fluxes = [through[2 * axis + 1] - through[2 * axis] for axis in range(AXES)]
    return (*stresses_of(weight, lines, wrap), *fluxes)


def axis_neighbours(
    now: np.ndarray, wrap: Wrap
) -> tuple[currents.Neighbours, currents.Neighbours, currents.Neighbours]:
    """The level now at every Node and at its two neighbours along each axis, through the +a and the -a Port, the tension's reads (ALGEBRA.md #the-primitives, the row "the held write", The tension)."""
    arrived = ports(now, wrap)
    found = [currents.Neighbours(now, arrived[2 * axis], arrived[2 * axis + 1]) for axis in range(3)]
    return found[0], found[1], found[2]


def held_write_at(
    lines: Sequence[Record],
    numerators: Sequence[Any],
    walls: Sequence[int],
    remainders: Sequence[np.ndarray],
    direction: int = 1,
) -> tuple[list[Record], list[np.ndarray]]:
    """A held family's one write per line (ALGEBRA.md #the-primitives, the row "the held write"), its lines already stepped by Rule3 in the interval's second act, with or without a gap: each line's level gains (numerator + r) div wall by the write's carried division (features/held_write) with the one remainder kept at the Node; backward the increments taken off and the remainders stepped back, exact; returns the lines and the remainders after."""
    found, after = [], []
    for line, numerator, wall, remainder in zip(lines, numerators, walls, remainders, strict=True):
        level, kept = held_write(line.now, numerator, wall, remainder, direction)
        found.append(replace(line, now=np.asarray(level)))
        after.append(np.asarray(kept))
    return found, after
