"""The step, Rule3 in flux form (ALGEBRA.md #the-line, #the-interval): every line of every record is stepped by the law's line w (a_next - 2 a_now + a_before) + r' - r = SUM over the Node's six Links of R_ij (m_ij - a_now) - D_i a_now, the Links' sum gathered Link by Link (`link_fluxes`): per axis every interior Link is visited once by slices, its one difference a_far - a_near read once and multiplied by each end's own reach R_ij into that end's sum (two values where the two ends' paces differ, the pairing, both carried and neither averaged); a wall (an open face, an inner face, a Node beyond the board) is a Link to the fill, 0 for quanta and the held row's rest on its first line, as core/ports.arrival reads it; a periodic axis adds the Link from the last layer to the first; an axis of extent one is a Link from the Node to itself, its flux 0; a turned or folded plane is the one complex line, the record sent the neighbour's pair and the Port reading it turned by the Link's pair, R_ij m_ij = (R^c_ij + i R^s_ij) z_j (`turned_link_fluxes`, ALGEBRA.md, The flux form on a turned or folded Link); at a Node named by a click's face the arrival through the face's Port is the value the click act computes from the Node's whole total (features/click `presented`, `face_differences`), a Node's act in a Link's place; the division is Rule3's (`core/rule3.rule3`, the mass D_i the Node's, the wall w the family's, the terms added in the order the engine's bound is derived for). The bound's partial sums (`rule3.partial_rooms`) are read outside the step. The held write, the lays, the growth, the detector's acts and the phase act are outside the step and the engine's own (lattice.py)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, cast

import numpy as np

from event_universe import node, records
from event_universe.core.ports import AXES, Wrap
from event_universe.core.rule3 import Rule, division_forward, rule3
from event_universe.frames import frames_of
from event_universe.loader.derived import PLANE, row_of
from event_universe.plane import link_levels, link_pairs, odd_links, phase_links
from event_universe.readings import at, slices
from event_universe.records import Booking, Record, record_slice

Pairs = tuple[tuple[Any, ...], tuple[Any, ...]]  # a turned plane's reads per Port, (R^c_ij, R^s_ij)


def link_fluxes(level: np.ndarray, reaches: tuple[Any, ...], wrap: Wrap) -> np.ndarray:
    """SUM over the Node's six Links of R_ij (m_ij - a_i) at every Node, gathered Link by Link: per axis every interior Link once, the near end reading the far level through its +a Port and the far end the near level through its -a Port, the Link's one difference with each end's own reach (two values where the paces differ, the pairing); on a periodic axis the Link from the last layer to the first; on an open axis the two wall Links to the fill; on an axis of extent one the Node is its own neighbour through both Ports and the Link's flux is 0; a Node beyond the board reads the fill and is read as the fill (`seen`)."""
    kind = np.result_type(
        level, *(np.asarray(reach) for reach in reaches)
    )  # the level's kind, or Python's integers where a reach is one
    flux = np.zeros(level.shape, dtype=kind)
    for axis in range(AXES):
        plus, minus = reaches[2 * axis], reaches[2 * axis + 1]
        if level.shape[axis] == 1:
            continue
        lo, hi, first, last = slices(axis)
        for near, far in ((lo, hi), (last, first)):
            difference = level[far] - level[near]  # the Link's one difference, a_far - a_near
            flux[near] += at(plus, near) * difference
            flux[far] -= at(minus, far) * difference
    return flux


def turned_link_fluxes(
    levels: tuple[np.ndarray, np.ndarray],
    reaches: tuple[Any, ...],
    pairs: Pairs,
    wrap: Wrap,
    frames: tuple[Any, ...] | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """The complex flux line's Link sum on a turned or folded plane, z = re + i im, SUM over the six Links of [(R^c_ij + i R^s_ij) z_j - R_ij z_now] at every Node, its two real parts (ALGEBRA.md #the-line, The flux form on a turned or folded Link; `plane.link_pairs`, the pair (R^c, R^s) = p_i^2 (X^c, X^s) per Port, the plain reach R_ij = p_i^2 X_ij): the record sent on a turned Link is the neighbour's pair and the Port reads it turned by the Link's pair, R_ij m_ij the pair product, the far end reading the conjugate pair at its own pace (X^s_ji = -X^s_ij exactly, `plane.sign_pairs`, `plane.fold_pairs`); beyond a face and at a Node beyond the board the pair sent is (0, 0); on an axis of extent one the Node's own pair through both Ports, whose odd parts cancel (the two Ports carry the odd level with opposite signs, `plane.link_levels`), the self-Link's term 2 (R^c - R) z. Gathered Link by Link as `link_fluxes` gathers a plain line's. `frames`, per Port the sign the Node reads its neighbour's plane with (plane.frame_signs): -1 across a Link whose two ends stand in different frames (one end time-reversed by the swap at the top, the other not), where the neighbour's value is read conjugated, im_j -> -im_j, so that the Link reads its two ends in one frame (ALGEBRA.md, The swap at the top, the frame clause); None every Port at +1."""
    evens, odds = pairs
    re_level, im_level = levels
    kind = np.result_type(re_level, *(np.asarray(x) for x in (*reaches, *evens, *odds)))
    flux_re, flux_im = np.zeros(re_level.shape, dtype=kind), np.zeros(re_level.shape, dtype=kind)

    def add(where: tuple[Any, ...], port: int, re_j: Any, im_j: Any) -> None:
        c, s, r = at(evens[port], where), at(odds[port], where), at(reaches[port], where)
        if frames is not None:
            im_j = at(frames[port], where) * im_j
        flux_re[where] += c * re_j - s * im_j - r * re_level[where]
        flux_im[where] += s * re_j + c * im_j - r * im_level[where]

    for axis in range(AXES):
        plus, minus = 2 * axis, 2 * axis + 1
        if re_level.shape[axis] == 1:
            whole = (slice(None),) * AXES
            add(whole, plus, re_level, im_level)
            add(whole, minus, re_level, im_level)
            continue
        lo, hi, first, last = slices(axis)
        for near, far in ((lo, hi), (last, first)):
            add(near, plus, re_level[far], im_level[far])
            add(far, minus, re_level[near], im_level[near])
    return flux_re, flux_im


def gathered_line(record: Record, rule: Rule, wrap: Wrap, direction: int) -> tuple[np.ndarray, Any, Any]:
    """The Links' sum of one plain line, SUM over the six Links of R_ij (m_ij - a_now) at every Node, gathered Link by Link (`link_fluxes`) from the level the step starts from, with the faces the click act presents (`face_differences`); returned with that level and the other level, (now, before) forward and (before, now) backward."""
    level, other = (record.now, record.before) if direction == 1 else (record.before, record.now)
    flux = link_fluxes(level, rule.reaches, wrap)
    return flux, level, other


def step_line(record: Record, rule: Rule, wrap: Wrap, direction: int = 1) -> Record:
    """Rule3 on one plain line in the law's flux form (ALGEBRA.md #the-line, #the-direction): the Links' sum gathered (`gathered_line`), the division Rule3's (`core/rule3.rule3`); forward from (now, before, r) to (next, now, r'), backward from (next, now, r') to (now, before, r)."""
    flux, level, other = gathered_line(record, rule, wrap, direction)
    found, remainder = rule3(flux, rule.mass, rule.wall, level, other, record.remainder, direction)
    if direction == 1:
        return Record(np.asarray(found), record.now, np.asarray(remainder))
    return Record(record.before, np.asarray(found), np.asarray(remainder))


def step_momentum(
    own: Sequence[Record],
    rule: Rule,
    wrap: Wrap,
    direction: int,
    volumes: tuple[Any, Any, Any],
) -> list[Record]:
    """The three tension lines of a held row of the content stepped as the shear's momentum at the volume's wall (ALGEBRA.md, The shear's momentum is carried at the volume's wall, a hypothesis under its own name, 2026-10-23; the symmetry hand's derivation read cold by the reader): Rule3's line on the traceless part of the line's own three Link terms with its wall 3 w split across the interval, the wall of the pair the act enters 3 w (X_now + X_ahead) on the level stepped to and on the remainder's range, the wall the velocity carried in was born under, 3 w (X_now + X_behind), on that velocity, and the one volume of the start, 2 X_now, on the Links' term and the mass, `volumes` the Node's own time line (X_behind, X_now, X_ahead) in `direction` (forward X_before, X_now, X_next after the time line's step and write; backward X_next, X_now, X_before after the time line's inverse), so that the shear's momentum (X / Gamma) T_a' in the board's interval is what the Links' traceless terms move and the shear's velocity falls as the volume grows, nature's -3 H sigma in proper time with the weight the volume's exponent d + 1 in the board's interval and no number typed; with the half wall's move (3 w (X_ahead - X_behind)) / 2 in the numerator, so that the rest's remainder at half the wall born under stands at half the wall entered (the law's birth at the half wall carried across the wall's change: the momentum less half the wall is what the flux moves, the floor a rounding to the nearest, no bias as the wall grows), one carried division per line (`core/rule3.division_forward`, the remainder Python's integer in [0, 3 w (X_now + X_ahead))), a bijection at every Node-interval whether the volume grows or shrinks (the incoming remainder's range is the incoming level's coefficient), the inverse the same function at -1 with every remainder complemented at its own wall, the wall it was born under (the forward act on the swapped pair; `records.complement`, the mirror of The cube's symmetry), and the law's own `step_traceless` bit for bit where the time line stands (X_behind = X_now = X_ahead), the remainder 2 X times the law's."""
    behind, now, ahead = (np.asarray(volume, dtype=object) for volume in volumes)
    gathered = [gathered_line(line, rule, wrap, direction) for line in own]
    total: Any = sum(np.asarray(flux, dtype=object) for flux, _level, _other in gathered)
    wall3, mass3 = AXES * rule.wall, AXES * rule.mass
    entered, born = (
        wall3 * (now + ahead),
        wall3 * (now + behind),
    )  # the wall entered, the wall the carry was born under
    rest = division_forward(
        entered - born, 2, 0
    )[
        0
    ]  # the half wall's move: the rest's remainder from half the wall born under to half the wall entered (3 w even)
    found = []
    for line, (flux, level, other) in zip(own, gathered, strict=True):
        kind = line.now.dtype
        traceless = AXES * np.asarray(flux, dtype=object) - total
        level, other = np.asarray(level, dtype=object), np.asarray(other, dtype=object)
        numerator = (
            entered * level + born * (level - other) + (now + now) * (traceless - mass3 * level) + rest
        )
        remainder = np.asarray(line.remainder, dtype=object)
        carry = (
            remainder if direction == 1 else born - 1 - remainder
        )  # backward every remainder complemented at its own wall
        stepped, carried = division_forward(numerator, entered, carry)
        kept = carried if direction == 1 else entered - 1 - carried
        stepped = np.asarray(stepped, dtype=kind)
        found.append(
            Record(stepped, line.now, kept) if direction == 1 else Record(line.before, stepped, kept)
        )
    return found


def gathered_plane(
    rule: Rule,
    wrap: Wrap,
    now: tuple[Any, Any],
    pairs: Pairs,
    frames: tuple[Any, ...] | None = None,
) -> list[np.ndarray]:
    """The Links' sum of a turned or folded plane's one complex line, SUM over the six Links of [(R^c_ij + i R^s_ij) z_j - R_ij z_now], its two real parts gathered Link by Link (`turned_link_fluxes`, `frames` the sign each Port reads its neighbour's im part with, the two ends read in one frame), with the faces the click act presents on each part's own arrivals (`face_differences`: a re arrival's difference enters the re part by R^c and the im part by R^s, an im arrival's the re part by -R^s and the im part by R^c, the im arrival's difference read with the Port's frame sign)."""
    return list(turned_link_fluxes(now, rule.reaches, pairs, wrap, frames))


def step_plane(
    re: Record,
    im: Record,
    rule: Rule,
    wrap: Wrap,
    direction: int,
    pairs: Pairs | None,
    frames: tuple[Any, ...] | None = None,
) -> tuple[list[Record], Booking]:
    """A plane's two lines by Rule3's flux line (ALGEBRA.md #the-line, The flux form on a turned or folded Link): at no turn (`pairs` None) each line a plain line (`step_line`); turned or folded, the one complex line w (z_next - 2 z_now + z_before) + (r' - r) = SUM over the six Links of [(R^c_ij + i R^s_ij) z_j - R_ij z_now] - D_i z_now, its two real parts gathered (`gathered_plane`, with `frames` the sign each Port reads its neighbour's im part with, plane.frame_signs) and each divided by Rule3 with its own remainder (`core/rule3.rule3`); the bookings (first, second) the form and the Wronskian are read from: first the pair the step started from with the level it left behind, second the level it wrote with the pair it started from (ALGEBRA.md #the-interval)."""
    now = (re.now, im.now) if direction == 1 else (re.before, im.before)
    other = (re.before, im.before) if direction == 1 else (re.now, im.now)
    if pairs is None:
        found = [step_line(record, rule, wrap, direction) for record in (re, im)]
    else:
        remainders = (re.remainder, im.remainder)
        fluxes = gathered_plane(rule, wrap, now, pairs, frames)
        stepped = [
            rule3(fluxes[part], rule.mass, rule.wall, now[part], other[part], remainder, direction)
            for part, remainder in enumerate(remainders)
        ]
        found = [
            Record(np.asarray(level), record.now, np.asarray(remainder))
            if direction == 1
            else Record(record.before, np.asarray(level), np.asarray(remainder))
            for record, (level, remainder) in zip((re, im), stepped, strict=True)
        ]
    levels = [line.now if direction == 1 else line.before for line in found]
    remainders_found = [line.remainder for line in found]
    u, v = (other, levels) if direction == 1 else (levels, other)
    first = [Record(now[part], np.asarray(u[part]), remainders_found[part]) for part in range(PLANE)]
    second = [Record(np.asarray(v[part]), now[part], remainders_found[part]) for part in range(PLANE)]
    return found, (first, second)


def step_family(
    index: int,
    families: records.Families,
    states: records.States,
    rule: Rule,
    wrap: Wrap,
    gamma: int,
    direction: int = 1,
    record: int = 0,
    pairs: Pairs | None = None,
    frames: tuple[Any, ...] | None = None,
) -> tuple[list[Record], Booking]:
    """Every line of one record of a family stepped in `direction` with its rule (ALGEBRA.md #the-interval): line by line in the law's flux form (`step_line`, the time line of a holder of the content reading its rest beyond every face), a plane plane by plane (`step_plane`: at no turn two plain lines, turned or folded the one complex line with the pairs `pairs`, each Link's read the pair (R^c, R^s), `plane.link_pairs`, and `frames` the sign each Port reads its neighbour's im part with, `frames_of`); every line with the faces the click act presents to it at this step; with the lines, the booking (first, second) the form and the Wronskian are read from."""
    family, state = families[index], states[index]
    span = record_slice(family, record)
    own = state.lines[span]
    if not family.plane:
        traced = (
            family.axes and not family.wronskian
        )  # a holder of the content's tension lines: the shear's momentum
        found = [
            step_line(line, rule, wrap, direction)
            if not (traced and 1 <= number - span.start <= AXES)
            else line
            for number, line in enumerate(own, span.start)
        ]
        return (
            found,
            ((own, found) if direction == 1 else (found, own)),
        )  # the tension lines untouched here: the lattice steps them after the time line's interval (step_momentum)
    lines: list[Record] = []
    first: list[Record] = []
    second: list[Record] = []
    for start in range(0, len(own), PLANE):  # plane by plane, each its two lines, re and im
        pair = own[start], own[start + 1]
        found, (begun, left) = step_plane(*pair, rule, wrap, direction, pairs, frames)
        lines, first, second = lines + found, first + begun, second + left
    return lines, (first, second)


def pairs_of(
    index: int,
    families: records.Families,
    states: records.States,
    direction: int,
    wrap: Wrap,
    gamma: int,
    content: Any,
    factors: node.Factors,
    record: int,
    amplitude: int,
) -> tuple[tuple[Any, ...], tuple[Any, ...]] | None:
    """A record's Link pairs where it is turned or folded (`node.turning`, the sign's odd levels along the Links, `plane.link_levels`; `plane.odd_links`, the flux holder's; the record's row's phase lines through the six Ports at the amplitude X, `plane.phase_links`; `plane.link_pairs`, the pair (R^c, R^s) per Port), None for a plain record; made once per interval on the very records and given again (features/read `READS`, `read_again`: the step asks once per record, the board's own read at every meeting Node for every record, 2026-10-24)."""
    from event_universe.features.read import (
        READS,  # the reading made once per interval on the very records (the architect's economy of 2026-10-24): the Link pairs are asked by the step once and by the board's own read at every meeting Node for every record
        read_again,
    )

    key = (pairs_of, index, record, direction, gamma, amplitude)
    taken = (
        *states[index].lines,
        *(line for held, family in enumerate(families) if family.held for line in states[held].lines),
        *(
            line
            for held, family in enumerate(families)
            if family.held
            for row in states[held].phases
            for line in row
        ),
        content,
        *(() if factors is None else tuple(factors)),
    )
    if (kept := read_again(key, taken)) is not None:
        return cast(Pairs | None, kept[0])
    angles = node.turning(index, families, states, direction, record)
    flux = odd_links(index, families, states, direction, wrap)  # the fold, a folded plane's
    sign = (  # the sign's Link levels n_ij, the two ends weighed as the holder declares (`link_read`)
        None
        if angles is None
        else link_levels(angles[1], wrap, families[node.sign_holder(index, families)].link_read)
    )
    phases = None
    if angles is not None:  # the record's row's phase pairs, the Link's hop through each Port
        row = row_of(families, index, record)
        assert row is not None
        if amplitude < 1:
            raise ValueError(
                f"{families[index].name!r} reads the sign's phase lines and the step was given no amplitude X "
                "for the fold: the caller passes features/phase.amplitude of the width"
            )
        phases = phase_links(states[node.sign_holder(index, families)].phases[row], wrap)
    found = link_pairs(families[index].pair, gamma, content, factors, flux, sign, phases, amplitude)
    READS[key] = (taken, (found, []))
    return found


def step_records(
    index: int,
    families: records.Families,
    states: records.States,
    wrap: Wrap,
    gamma: int,
    unit: int,
    direction: int = 1,
    amplitude: int = 0,
) -> tuple[list[Record], list[Booking]]:
    """Every record of a family stepped in `direction`, each with the rule of its own read (`node.read`, `node.rule_of`: the content and the six Links' factors from the held rows' levels the step starts from, every sign row but the record's own), its Links' pairs where the record is turned or folded (`node.turning`, `plane.odd_links`, `plane.phase_links`, `plane.link_pairs`), the faces the click act presents at this step among its arrivals (`faces`, per line); the lines in the records' order and one booking per record, the lines its form and its Wronskian are read from."""
    lines: list[Record] = []
    bookings: list[Booking] = []
    for record in range(families[index].records):
        content, factors = node.read(index, families, states, direction, wrap, gamma, unit, record)
        rule = node.rule_of(families[index], gamma, content, factors, unit)
        pairs = pairs_of(
            index, families, states, direction, wrap, gamma, content, factors, record, amplitude
        )
        frames = frames_of(index, families, states, wrap, record)
        found, booking = step_family(
            index, families, states, rule, wrap, gamma, direction, record, pairs, frames
        )
        lines, bookings = lines + found, bookings + [booking]
    return lines, bookings
