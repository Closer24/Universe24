"""The plane's step under the rotation, Rule3 on a two-part record's two lines as one with the Peierls phase on every Link and on the time Link (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; The turn per proper interval; features/rotation): every Link's phase in the fold form, each Link's read a pair (X^c, X^s) in the Link unit, the sign's from the sign holder's odd lines, the Link's angle theta with tan(theta / 2) = n / (4 Gamma) rebooked as the exact tangent half-angle triple with one rounding per part (`sign_pairs`; the two hands' lines of 2026-10-09, the advisor's (a) and (1), the mathematician's (a)), gravity's from the flux holder's odd lines (ALGEBRA.md, The clock family on the Ports; `odd_links`, `fold_pairs`), the two composed where a plane reads both, the product pair rounded once (features/phase.fold; `link_pairs`), and the faces the click act presents among a line's arrivals (features/click): the two lines stepped against the level before turned by the previous interval's time angle and the result turned by this one's, the time turn the one shear that remains (`step_plane`), each Link's pair on the two arrivals in Rule3's one division per part at the wall unchanged, the bookings the form and the Wronskian are read from, every number the same in either direction; the Node's own act, called by node.py line by line."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import AXES, Wrap, arrival
from event_universe.core.rule3 import rule3
from event_universe.features import rotation
from event_universe.features.click import Face, presented
from event_universe.features.phase import fold, signed_rounded
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


def link_levels(levels: tuple[Any, Any, Any], wrap: Wrap) -> tuple[Any, ...]:
    """An odd line's level along each of a Node's six Links in Port order, the two ends' sum with the direction's sign: L_a(i) + L_a(i + a) through the +a Port and -(L_a(i - a) + L_a(i)) through the -a Port, so that the Link read from its other end is the same size with the opposite sign, n_ji = -n_ij exactly (ALGEBRA.md #the-rows-against-nature (b2), Peierls' coupling; the sign holder's odd lines and the flux holder's alike)."""
    found: list[Any] = []
    for axis, level in enumerate(levels):
        found += [level + arrival(level, axis, 1, wrap), -(level + arrival(level, axis, -1, wrap))]
    return tuple(found)


def odd_links(
    index: int, families: tuple[FamilyRule, ...], states: list[NodeState], direction: int, wrap: Wrap
) -> tuple[Any, ...] | None:
    """The flux holder's odd line's level along each of a Node's six Links in Port order, V_ij = V_a(i) + V_a(j) through the +a Port and -(V_a(i - a) + V_a(i)) through the -a Port (`link_levels`, V_ji = -V_ij exactly), SUM over the holders the family reads that carry the flux's odd lines of weight x the line after its tension lines, at the level the step in `direction` starts from (ALGEBRA.md, The clock family on the Ports); None where the family is no plane or reads no such holder (`derived.folds`)."""
    reads = [r for r in families[index].reads if families[r.family].flux]
    if not (families[index].plane and reads):
        return None
    levels = []
    for axis in range(AXES):
        lines = [(r.weight, states[r.family].lines[1 + AXES + axis]) for r in reads]
        levels.append(content_of([(weight, level_at(line, direction)) for weight, line in lines]))
    return link_levels((levels[0], levels[1], levels[2]), wrap)


def fold_pairs(
    pair: tuple[int, int], gamma: int, factors: tuple[Any, ...], links: tuple[Any, ...]
) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """Gravity's pair on each Link in Port order, in the Link unit (ALGEBRA.md, The clock family on the Ports; the two hands' joint line of 2026-10-09): the Link quantity X_ij = 2 num Q_ij keeps its even part X^c = X_ij and takes the odd part X^s_ij = sgn(V_ij) rounded(6 X_ij K |V_ij| / Gamma^2), the angle 12 omega_0 V_ij of the two ends' sum V_ij over 2 Gamma with K = omega_0 Gamma the family's rotation to the unit (`paces.rotation_unit`), one rounding per Link per interval on the size with the sign attached after (features/phase.signed_rounded), so that X^s_ji = -X^s_ij exactly; 0 on a Link the world cuts and on every Link of a massless family (K = 0)."""
    num, square = pair[0], gamma * gamma
    turn = paces.rotation_unit(*pair, gamma)
    even = tuple(2 * num * factor for factor in factors)  # X_ij, the Link quantity in the Link unit
    odd = tuple(signed_rounded(6 * x * turn * link, square) for x, link in zip(even, links, strict=True))
    return even, odd


def sign_pairs(
    pair: tuple[int, int], gamma: int, factors: tuple[Any, ...], links: tuple[Any, ...]
) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """The sign's pair on each Link in Port order, in the Link unit (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; the two hands' lines of 2026-10-09, the advisor's (a) and (1), the mathematician's (a)): the Link's angle theta with tan(theta / 2) = n / W at the Link's wall W = 4 Gamma (features/rotation.link_wall), n = n_ij the sign holder's odd line along the Link, the two ends' sum with the direction's sign (`link_levels`), is the exact tangent half-angle triple (W^2 - n^2, 2 W n, W^2 + n^2) rebooked in the Link's unit X_ij = 2 num Q_ij with one rounding each: X^c = rounded(X_ij (W^2 - n^2), W^2 + n^2) and X^s = sgn(n) rounded(X_ij 2 W |n|, W^2 + n^2) (features/phase.signed_rounded, the sign attached after), X^c even in n and X^s odd in n, so that X^c_ji = X^c_ij and X^s_ji = -X^s_ij exactly (K = D M Hermitian, the count exact by Theorem 3) and the pair's magnitude is X_ij to the rounding; the three shears of the Link turn replaced, the time turn's shear kept (`step_plane`)."""
    num, wall = pair[0], rotation.link_wall(gamma)
    even, odd = [], []
    for factor, link in zip(factors, links, strict=True):
        x, circle = 2 * num * factor, wall * wall + link * link  # X_ij and the triple's hypotenuse
        even.append(paces.rounded(x * (wall * wall - link * link), circle))
        odd.append(signed_rounded(x * 2 * wall * link, circle))
    return tuple(even), tuple(odd)


def link_pairs(
    pair: tuple[int, int],
    gamma: int,
    content: Any,
    factors: tuple[Any, ...],
    flux: tuple[Any, ...] | None,
    sign: tuple[Any, ...] | None,
) -> tuple[tuple[Any, ...], tuple[Any, ...]] | None:
    """Each Link's read as a pair (R^c_ij, R^s_ij) = p_i^2 (X^c_ij, X^s_ij) in Port order, the even read and the odd read of a folded plane (`step_plane`): gravity's pair from the flux holder's odd lines along the Links (`flux`, `odd_links`; `fold_pairs`), the sign's from the sign holder's (`sign`, `link_levels` of the turn's odd levels; `sign_pairs`), and where a plane reads both the two pairs multiplied, the product pair rounded once into the Link unit X_ij (features/phase.fold: ((X^c_s X_ij - X^s_s X^s_g) div X_ij, (X^s_s X_ij + X^c_s X^s_g) div X_ij), rounded half up on the magnitude with the sign after, the same integers in either order, and each alone bit for bit its own pair, the division by X_ij exact then), a Link the world cuts (X_ij = 0) staying at the pair (0, 0); None where the plane reads neither, the plain reads R_ij (ALGEBRA.md, The clock family on the Ports; the two hands' (b) of 2026-10-09)."""
    if flux is None and sign is None:
        return None
    if sign is None:
        assert flux is not None
        evens, odds = fold_pairs(pair, gamma, factors, flux)
    elif flux is None:
        evens, odds = sign_pairs(pair, gamma, factors, sign)
    else:
        turned, gravity = sign_pairs(pair, gamma, factors, sign), fold_pairs(pair, gamma, factors, flux)
        folded = []
        for cosine, sine, even, odd in zip(*turned, *gravity, strict=True):
            unit = even + (even == 0)  # the Link unit X_ij, 1 on a cut Link where every part is 0
            folded.append(fold(cosine, sine, even, odd, unit))
        evens, odds = tuple(f[0] for f in folded), tuple(f[1] for f in folded)
    pace = paces.link_pace_of(gamma, content)
    square = pace * pace
    return tuple(square * x for x in evens), tuple(square * x for x in odds)


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
    pairs: tuple[tuple[Any, ...], tuple[Any, ...]] | None = None,
) -> tuple[list[Record], Booking]:
    """Rule3 on a plane's two lines under the rotation (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; The turn per proper interval; features/rotation): with z = re + i im and theta_t the angle of the interval t with tan(theta_t / 2) = (L_t p_0 div Gamma) / (2 Gamma), L_t the holder's time level at the Node at that interval's start and p_0 the turned family's clock then (exactly 2 arctan of that tangent half-angle, (L / Gamma) (p_0 / Gamma) to the third order), the turn is the Peierls phase of the time Link as the Links' pairs are of the space Links (`link_pairs`): e^(i theta_t) z_next + e^(-i theta_(t-1)) z_before = (S z_now + SUM over the Ports of R_ij (e^(i theta_a) z_(+a) or e^(-i theta_a) z_(-a))) / w, the level before under the previous interval's angle and the level next under this one's (the mathematician's hand, the owner's word: the Wronskian conserved under the rotation exactly for any level in time; a static level, theta_(t-1) = theta_t, the turn by the level now bit for bit); the law's row 9 of its conventions table, one convention, the engine's, the sign the declared bit (ALGEBRA.md, The conventions and the units; The sign holder rotates the two-part record); the tangent half-angles (L p_0 div Gamma) / (2 Gamma) on the time Link, by three shears, the one shear that remains (the two hands' lines of 2026-10-09; the next step replaces it), and on the Link ij n_ij / (4 Gamma), n_ij = L_a(i) + L_a(j), in the fold form, the turn against the sense of the record of positive Wronskian, which then rotates faster by theta. Forward the lines arrive with the level before turned already, u = e^(-i theta_(t-1)) z_before (`turned_before` at the previous interval's angle), Rule3 steps re and im with one rule and their own remainders against u, each neighbour's pair arriving plain through its Port and read by the Link's pair, and the result v is turned by this interval's angle, z_next = e^(-i theta_t) v; backward v = e^(i theta_t) z_next undoes that turn, Rule3 at -1 gives u and the remainders back, bit for bit, and the lines returned hold u as the level before, the inverse's first stage: `turned_before` at -1 turns it back to z_before once the previous interval's angle is read again from the held rows at that interval's start, which the inverse reaches after their write back and their step back. Returns the two lines and the booking (first, second) the form and the Wronskian are read from, D = form(first, second) = |z_now|^2 - v . u and W = wronskian(second) = Im(conj(v) z_now), the bookings read from the un-turned levels u and v and never from z_before, the same numbers in either direction. Under the fold (`pairs`, each Port's even read R^c_ij = p_i^2 X^c_ij and odd read R^s_ij = p_i^2 X^s_ij, `link_pairs`; None the plain reads) each arrival z_j enters as (X^c + i X^s) z_j: the re part's numerator SUM (R^c_ij re_j - R^s_ij im_j) and the im part's SUM (R^c_ij im_j + R^s_ij re_j), twelve reads on twelve arrivals in Rule3's one division per part at the wall w unchanged, the same reads read back (ALGEBRA.md, The clock family on the Ports; the two hands' (a) of 2026-10-09); `angles` None where no holder turns the record, no turn of the levels."""
    reads, self_coefficient, wall = rule
    now = (level_at(re, direction), level_at(im, direction))
    before = (re.before, im.before)  # u forward (`turned_before`); v = e^(i theta_t) z_next backward
    arrived = tuple(
        tuple(arrival(level, axis, side, wrap) for axis in range(AXES) for side in (1, -1))
        for level in now
    )
    if angles is None:
        other = before if direction == 1 else (re.now, im.now)
    else:
        half = rotation.turn_wall(gamma)  # the time turn's wall, tan(theta / 2) = n / (2 Gamma)
        other = before if direction == 1 else rotation.turned(re.now, im.now, -angles[0], half, -1)
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
    folded = (  # each Link's pair on the two arrivals: X^c re_j - X^s im_j on re, X^c im_j + X^s re_j on im
        ((reads, arrived[0]), (reads, arrived[1]))
        if pairs is None
        else (
            (pairs[0] + tuple(-x for x in pairs[1]), arrived[0] + arrived[1]),
            (pairs[0] + pairs[1], arrived[1] + arrived[0]),
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
