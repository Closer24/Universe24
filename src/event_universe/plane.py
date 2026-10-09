"""The plane's step under the rotation, Rule3 on a two-part record's two lines as one with the Peierls phase on every Link and on the time Link (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; The turn per proper interval; features/rotation), under gravity's fold, each Link's read a pair (X^c, X^s) in the Link unit from the flux holder's odd lines (ALGEBRA.md, The clock family on the Ports; `odd_links`, `fold_reads`), and the faces the click act presents among a line's arrivals (features/click): the arrivals turned through the Ports (`turned_ports`), the two lines stepped against the level before turned by the previous interval's angle and the result turned by this one's (`step_plane`), the odd part of each read on the other line's arrival in Rule3's one division per part, the bookings the form and the Wronskian are read from, every number the same in either direction; the Node's own act, called by node.py line by line."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import AXES, Wrap, arrival
from event_universe.core.rule3 import rule3
from event_universe.features import rotation
from event_universe.features.click import Face, presented
from event_universe.features.read import content_of
from event_universe.loader.derived import FamilyRule
from event_universe.records import Booking, NodeState, Record, level_at

Rule = tuple[tuple[Any, ...], Any, Any]  # Rule3's integers at every Node: the six Ports' R_ij, S, w
Offset = tuple[
    int, int, int
]  # the layers grown before the origin on each axis, the file's coordinates to the board's
Angles = tuple[Any, tuple[Any, Any, Any]]  # the turn's numerators at every Node: the time's, each axis's
Faces = tuple[list[Face], Offset]  # the faces presented to a line at this step, with the board's offset
NO_FACE: Faces = ([], (0, 0, 0))


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


def odd_links(
    index: int, families: tuple[FamilyRule, ...], states: list[NodeState], direction: int, wrap: Wrap
) -> tuple[Any, ...] | None:
    """The odd line's level along each of a Node's six Links in Port order, V_ij = V_a(i) + V_a(j) through the +a Port and -(V_a(i - a) + V_a(i)) through the -a Port, the two ends' sum with the direction's sign so that V_ji = -V_ij exactly, as the sign's odd lines are read (`turned_ports`), SUM over the holders the family reads that carry the flux's odd lines of weight x the line after its tension lines, at the level the step in `direction` starts from (ALGEBRA.md, The clock family on the Ports); None where the family is no plane or reads no such holder (`derived.folds`)."""
    reads = [r for r in families[index].reads if families[r.family].flux]
    if not (families[index].plane and reads):
        return None
    found: list[Any] = []
    for axis in range(AXES):
        lines = [(r.weight, states[r.family].lines[1 + AXES + axis]) for r in reads]
        level = content_of([(weight, level_at(line, direction)) for weight, line in lines])
        found += [level + arrival(level, axis, 1, wrap), -(level + arrival(level, axis, -1, wrap))]
    return tuple(found)


def fold_reads(
    pair: tuple[int, int], gamma: int, content: Any, factors: tuple[Any, ...], links: tuple[Any, ...]
) -> tuple[Any, ...]:
    """The odd part of each Link's read in Port order (ALGEBRA.md, The clock family on the Ports; the two hands' joint line of 2026-10-09): the Link quantity X_ij = 2 num Q_ij keeps its even part X^c = X_ij, the read R_ij = p_i^2 X_ij as it is, and takes the odd part X^s_ij = sgn(V_ij) rounded(6 X_ij K |V_ij| / Gamma^2), the angle 12 omega_0 V_ij of the two ends' sum V_ij over 2 Gamma with K = omega_0 Gamma the family's rotation to the unit (`paces.rotation_unit`), one rounding per Link per interval (`paces.rounded`) on the size with the sign attached after, so that X^s_ji = -X^s_ij exactly; the odd read p_i^2 X^s_ij, 0 on a Link the world cuts and on every Link of a massless family (K = 0)."""
    num, square = pair[0], gamma * gamma
    pace = paces.link_pace_of(gamma, content)
    turn = paces.rotation_unit(*pair, gamma)
    found = []
    for factor, link in zip(factors, links, strict=True):
        even = 2 * num * factor  # X_ij, the Link quantity in the Link unit, R_ij = p_i^2 X_ij
        size = paces.rounded(6 * even * turn * np.abs(link), square)
        found.append(pace * pace * np.sign(link) * size)
    return tuple(found)


def fold_guard(pair: tuple[int, int], gamma: int, links: tuple[Any, ...], name: str) -> None:
    """The fold's guard at load, as the turn's (`rotation.turn_guard`): the fold's tangent at most 1 on every Link, 6 K |V_ij| <= Gamma^2, within which a folded arrival's part stays within twice the level (`derived.FOLD_REACH`); refused by name beyond it, naming the Port."""
    turn = paces.rotation_unit(*pair, gamma)
    for port, link in enumerate(links):
        high = int(np.abs(np.asarray(6 * turn * link)).max())
        if high > gamma * gamma:
            raise ValueError(
                f"the fold of {name!r} on the Port {port} is {high} over {gamma * gamma} at load, a tangent "
                "above 1 (the odd line's level along the Link beyond the room the amplitude bound derives for a "
                "folded arrival); the run is refused: raise the holder's level weight"
            )


def step_plane(
    re: Record,
    im: Record,
    rule: Rule,
    wrap: Wrap,
    angles: Angles | None,
    gamma: int,
    direction: int = 1,
    faces: tuple[Faces, Faces] = (NO_FACE, NO_FACE),
    odd: tuple[Any, ...] | None = None,
) -> tuple[list[Record], Booking]:
    """Rule3 on a plane's two lines under the rotation (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; The turn per proper interval; features/rotation): with z = re + i im and theta_t the angle of the interval t with tan(theta_t / 2) = (L_t p_0 div Gamma) / (2 Gamma), L_t the holder's time level at the Node at that interval's start and p_0 the turned family's clock then (exactly 2 arctan of that tangent half-angle, (L / Gamma) (p_0 / Gamma) to the third order), the turn is the Peierls phase of the time Link as it is of the space Links (`turned_ports`): e^(i theta_t) z_next + e^(-i theta_(t-1)) z_before = (S z_now + SUM over the Ports of R_ij (e^(i theta_a) z_(+a) or e^(-i theta_a) z_(-a))) / w, the level before under the previous interval's angle and the level next under this one's (the mathematician's hand, the owner's word: the Wronskian conserved under the rotation exactly for any level in time; a static level, theta_(t-1) = theta_t, the turn by the level now bit for bit); the law's row 9 of its conventions table, one convention, the engine's, the sign the declared bit (ALGEBRA.md, The conventions and the units; The sign holder rotates the two-part record); the tangent half-angles (L p_0 div Gamma) / (2 Gamma) and, on the Link ij, (L_a(i) + L_a(j)) / (4 Gamma), the turn against the sense of the record of positive Wronskian, which then rotates faster by theta. Forward the lines arrive with the level before turned already, u = e^(-i theta_(t-1)) z_before (`turned_before` at the previous interval's angle), Rule3 steps re and im with one rule and their own remainders against u, each neighbour's pair arriving turned through its Port, and the result v is turned by this interval's angle, z_next = e^(-i theta_t) v; backward v = e^(i theta_t) z_next undoes that turn, Rule3 at -1 gives u and the remainders back, bit for bit, and the lines returned hold u as the level before, the inverse's first stage: `turned_before` at -1 turns it back to z_before once the previous interval's angle is read again from the held rows at that interval's start, which the inverse reaches after their write back and their step back. Returns the two lines and the booking (first, second) the form and the Wronskian are read from, D = form(first, second) = |z_now|^2 - v . u and W = wronskian(second) = Im(conj(v) z_now), the bookings read from the un-turned levels u and v and never from z_before, the same numbers in either direction. Under gravity's fold (`odd`, the odd read p_i^2 X^s_ij per Port, `fold_reads`; None no fold) each arrival z_j enters as (X^c + i X^s) z_j: the re part's numerator SUM (R_ij re_j - R^s_ij im_j) and the im part's SUM (R_ij im_j + R^s_ij re_j), twelve reads on twelve arrivals in Rule3's one division per part at the wall w unchanged, the same reads read back (ALGEBRA.md, The clock family on the Ports); `angles` None where no holder turns the record, the plain arrivals and no turn of the levels."""
    reads, self_coefficient, wall = rule
    now = (level_at(re, direction), level_at(im, direction))
    before = (re.before, im.before)  # u forward (`turned_before`); v = e^(i theta_t) z_next backward
    if angles is None:
        arrived = tuple(
            tuple(arrival(level, axis, side, wrap) for axis in range(AXES) for side in (1, -1))
            for level in now
        )
        other = before if direction == 1 else (re.now, im.now)
    else:
        time, links = angles
        half = rotation.turn_wall(gamma)  # the time turn's wall, tan(theta / 2) = n / (2 Gamma)
        arrived = turned_ports(now, links, rotation.link_wall(gamma), wrap)
        other = before if direction == 1 else rotation.turned(re.now, im.now, -time, half, -1)
    if faces[0][0] or faces[1][0]:  # the faces presented to each part's line
        faced = [
            presented(
                at,
                reads,
                self_coefficient,
                wall,
                now[k],
                other[k],
                (re, im)[k].remainder,
                *faces[k],
                direction,
            )
            if faces[k][0]
            else at
            for k, at in enumerate(arrived)
        ]
        arrived = (faced[0], faced[1])
    folded = (  # the odd part of each read on the other line's arrival: -X^s im_j on re, +X^s re_j on im
        ((reads, arrived[0]), (reads, arrived[1]))
        if odd is None
        else (
            (reads + tuple(-x for x in odd), arrived[0] + arrived[1]),
            (reads + odd, arrived[1] + arrived[0]),
        )
    )
    stepped = [
        rule3(read, at, self_coefficient, wall, now[part], other[part], record.remainder, direction)
        for part, (record, (read, at)) in enumerate(zip((re, im), folded, strict=True))
    ]
    levels, remainders = ([np.asarray(found[i]) for found in stepped] for i in (0, 1))
    u, v = (other, levels) if direction == 1 else (levels, other)
    out: Any = levels  # z_next = e^(-i theta_t) v forward under the rotation, the levels otherwise
    if direction == 1 and angles is not None:
        out = rotation.turned(levels[0], levels[1], -angles[0], rotation.turn_wall(gamma))
    lines = [
        Record(np.asarray(out[part]), record.now, remainders[part])
        if direction == 1
        else Record(record.before, out[part], remainders[part])
        for part, record in enumerate((re, im))
    ]
    first = [Record(now[part], np.asarray(u[part]), remainders[part]) for part in range(2)]
    second = [Record(np.asarray(v[part]), now[part], remainders[part]) for part in range(2)]
    return lines, (first, second)
