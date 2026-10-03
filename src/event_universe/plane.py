"""The plane's step under the rotation, Rule3 on a two-part record's two lines as one with the Peierls phase on every Link and on the time Link (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; The turn per proper interval; features/rotation), and the faces an instrument presents among a line's arrivals (features/click): the arrivals turned through the Ports (`turned_ports`), the two lines stepped against the level before turned by the previous interval's angle and the result turned by this one's (`step_plane`), the bookings the form and the Wronskian are read from, every number the same in either direction; the Node's own act, called by node.py line by line."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import rule3
from event_universe.features import rotation
from event_universe.features.click import Face, presented
from event_universe.records import Booking, Record, level_at

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


def step_plane(
    re: Record,
    im: Record,
    rule: Rule,
    wrap: Wrap,
    angles: Angles,
    gamma: int,
    direction: int = 1,
    faces: tuple[Faces, Faces] = (NO_FACE, NO_FACE),
) -> tuple[list[Record], Booking]:
    """Rule3 on a plane's two lines under the rotation (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; The turn per proper interval; features/rotation): with z = re + i im and theta_t the angle of the interval t with tan(theta_t / 2) = (L_t p_0 div Gamma) / (2 Gamma), L_t the holder's time level at the Node at that interval's start and p_0 the turned family's clock then (exactly 2 arctan of that tangent half-angle, (L / Gamma) (p_0 / Gamma) to the third order), the turn is the Peierls phase of the time Link as it is of the space Links (`turned_ports`): e^(i theta_t) z_next + e^(-i theta_(t-1)) z_before = (S z_now + SUM over the Ports of R_ij (e^(i theta_a) z_(+a) or e^(-i theta_a) z_(-a))) / w, the level before under the previous interval's angle and the level next under this one's (the mathematician's 118 B and 119, the owner's word of 2026-10-02, 08:35: the Wronskian conserved under the rotation exactly for any level in time; a static level, theta_(t-1) = theta_t, the turn by the level now bit for bit); the law's line as written has the opposite sign of theta, e^(-i theta_t) z_next + e^(i theta_(t-1)) z_before = the same right side, and ALGEBRA.md states both (the engine's convention the declared bit, the two differing by the sign of theta alone); the tangent half-angles (L p_0 div Gamma) / (2 Gamma) and, on the Link ij, (L_a(i) + L_a(j)) / (4 Gamma), the turn against the sense of the record of positive Wronskian, which then rotates faster by theta. Forward the lines arrive with the level before turned already, u = e^(-i theta_(t-1)) z_before (`turned_before` at the previous interval's angle), Rule3 steps re and im with one rule and their own remainders against u, each neighbour's pair arriving turned through its Port, and the result v is turned by this interval's angle, z_next = e^(-i theta_t) v; backward v = e^(i theta_t) z_next undoes that turn, Rule3 at -1 gives u and the remainders back, bit for bit, and the lines returned hold u as the level before, the inverse's first stage: `turned_before` at -1 turns it back to z_before once the previous interval's angle is read again from the held rows at that interval's start, which the inverse reaches after their write back and their step back. Returns the two lines and the booking (first, second) the form and the Wronskian are read from, D = form(first, second) = |z_now|^2 - v . u and W = wronskian(second) = Im(conj(v) z_now), the bookings read from the un-turned levels u and v and never from z_before, the same numbers in either direction."""
    reads, self_coefficient, wall = rule
    time, links = angles
    half = 2 * gamma  # the time turn's wall, tan(theta / 2) = n / (2 Gamma); the Link's twice it
    now = (level_at(re, direction), level_at(im, direction))
    arrived = turned_ports(now, links, 2 * half, wrap)
    before = (re.before, im.before)  # u forward (`turned_before`); v = e^(i theta_t) z_next backward
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
    stepped = [
        rule3(reads, at, self_coefficient, wall, now[part], other[part], record.remainder, direction)
        for part, (record, at) in enumerate(zip((re, im), arrived, strict=True))
    ]
    levels, remainders = ([np.asarray(found[i]) for found in stepped] for i in (0, 1))
    u, v = (other, levels) if direction == 1 else (levels, other)
    out = rotation.turned(levels[0], levels[1], -time, half) if direction == 1 else levels
    lines = [
        Record(np.asarray(out[part]), record.now, remainders[part])
        if direction == 1
        else Record(record.before, out[part], remainders[part])
        for part, record in enumerate((re, im))
    ]
    first = [Record(now[part], np.asarray(u[part]), remainders[part]) for part in range(2)]
    second = [Record(np.asarray(v[part]), now[part], remainders[part]) for part in range(2)]
    return lines, (first, second)
