"""The Link's pairs of a plane under the rotation, which the step reads on a two-part record's two lines as one (flux.step_plane) with the Peierls phase on every Link and none on the time Link, the temporal gauge (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; features/phase, the mathematician's repaired form of item (g), the advisor's second, the two hands' item (i)): every Link's phase in the fold form, each Link's read a pair (X^c, X^s) in the Link unit, the sign's from the sign holder's odd lines, the Link's angle theta with tan(theta / 2) = n / (4 Gamma) rebooked as the exact tangent half-angle triple with one rounding per part (`sign_pairs`; the two hands' lines of 2026-10-09), folded with the Link's phase pair (c, s) = X e^(i (Phi_i - Phi_j)), the pair of Rule3 lines at the fixed angle theta_0 = 1 / Gamma the holder's time level difference across the Link iterates (`phase_links`, the pair at the Node owning the +a Link at the size of the Link's count, read with the count's sign and conjugated through the -a Port, the pair at -n the conjugate of the pair at +n, 2026-10-21; features/phase.fold, one rounding into the Link unit), gravity's from the flux holder's odd lines (ALGEBRA.md, The clock family on the Ports; `odd_links`, `fold_pairs`), the pairs composed where a plane reads several, the product pair rounded once (`link_pairs`), and the faces the click act presents among a line's arrivals (features/click): the two lines stepped against the plain level before, every Link's pair on the two arrivals in Rule3's one division per part at the wall unchanged, the time turn gone by the exact gauge identity b_i = z_i e^(i Phi_i) (the mathematician's item 5), the bookings the form and the Wronskian are read from the plain pair, every number the same in either direction; the pairs are read plane by plane by the step (flux.step_family)."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import AXES, SIDES, Wrap, arrival
from event_universe.features.click import Face
from event_universe.features.phase import fold, rotation_unit, signed_read, signed_rounded
from event_universe.features.read import content_of
from event_universe.loader.derived import FamilyRule
from event_universe.records import NodeState, Record, level_at

Offset = tuple[
    int, int, int
]  # the layers grown before the origin on each axis, the file's coordinates to the board's
Angles = tuple[
    Any, tuple[Any, Any, Any]
]  # the sign's levels a record reads at every Node: the time level (the phase act's potential) and each axis's odd level
Phases = tuple[
    tuple[Any, Any], ...
]  # the phase pair (c, s) read through each of the six Ports, in Port order
Faces = tuple[list[Face], Offset]  # the faces presented to a line at this step, with the board's offset
NO_FACE: Faces = ([], (0, 0, 0))


def link_levels(
    levels: tuple[Any, Any, Any], wrap: Wrap, ends: tuple[int, int] = (1, 1)
) -> tuple[Any, ...]:
    """An odd line's level along each of a Node's six Links in Port order, the two ends weighed by the holder's declared pair `ends` (the owner's weight and the far end's, `FamilyRule.link_read`, the Port consuming the two integers blindly) with the direction's sign: own L_a(i) + far L_a(i + a) through the +a Port and -(own L_a(i - a) + far L_a(i)) through the -a Port, so that the Link read from its other end is the same size with the opposite sign, n_ji = -n_ij exactly (ALGEBRA.md #the-rows-against-nature (b2), Peierls' coupling); at (-1, -1), the sign holder's read since 2026-10-21, the two ends' sum with the sign opposite to the time line's, the hop's phase of Peierls' p - q A under the band's convention omega(k + theta), so that a co-moving reader reads 1 / gamma_s as row (b2) states (0.987, 0.958, 0.919 at beta_s = 0.150, 0.286, 0.395 against the law's 0.989, 0.958, 0.919); at (-2, 0), the Lorentz form's (covector.py), minus twice the +a Link's own line, the line the Link's own flux sources; (1, 1), the two ends' sum with the time line's own sign, is history, the shipped read until 2026-10-21, under which the co-moving reader read gamma_s (1 + beta_s^2), 1.031, 1.130, 1.254 at the same three beta_s; the default (1, 1) is the flux holder's fold's read (`odd_links`, V_ij = V_a(i) + V_a(j), gravity's turn + along the current, ALGEBRA.md, The clock family on the Ports), which the sign holder's pair never reaches: the sign holder's Links read `FamilyRule.link_read` alone."""
    own, far = ends
    found: list[Any] = []
    for axis, level in enumerate(levels):
        found += [
            own * level + far * arrival(level, axis, 1, wrap),
            -(own * arrival(level, axis, -1, wrap) + far * level),
        ]
    return tuple(found)


def link_wall(gamma: int) -> int:
    """The Link's wall, tan(theta_a / 2) = (L_a(i) + L_a(j)) / (4 Gamma): the clock doubled for the tangent half-angle, once per end of the Link, the two ends summed (`SIDES`; ALGEBRA.md, The sign holder rotates the two-part record)."""
    return SIDES * 2 * gamma


def link_guard(numerator: Any, wall: int, name: str, axis: int) -> None:
    """The Link's guard at load (the one place the loader bounds the sign's Link turn, as it bounds a pace): the tangent half-angle at most 1 at every Node, |n_ij| <= 4 Gamma on the Link of `axis`, a quarter turn per Link, within which the sign's pair stays at its extreme X 2^(1/2) (`derived.turned_room`); refused by name beyond it, naming the Node. The time level is guarded by nothing: the phase line's circle wraps (the advisor's second, item (1))."""
    size = np.abs(np.asarray(numerator))
    high = int(size.max()) if size.ndim else int(size)
    if high > wall:
        node = np.unravel_index(int(size.argmax()), size.shape) if size.ndim else ()
        raise ValueError(
            f"the turn of {name!r} by the odd line of the axis {axis} is {high} over {wall} at the Node "
            f"{tuple(int(i) for i in node)} at load, a tangent half-angle above 1 (more than a quarter turn), "
            "beyond the room the amplitude bound derives for a turned level (ENGINE.md, the amplitude bound); "
            "the run is refused: raise the holder's level weight"
        )


def frame_signs(frame: Any, wrap: Wrap) -> tuple[Any, ...]:
    """The sign each of a Node's six Ports reads its neighbour's plane with, in Port order (ALGEBRA.md, The swap at the top, the frame clause; the bijection hand's derivation M25): `frame` the Node's phase row's remainder at the wall 2, 0 at a record in the frame it was born in and 1 at a record time-reversed an odd number of times by the swap at the top (the remainder complemented at the swap like every remainder); +1 through a Port whose two ends stand in one frame, -1 where they differ, so that the Link reads its two ends in one frame: the neighbour's plane value conjugated and its K negated across such a Link (node.phase_counts, flux.turned_link_fluxes, `phase_links`); +1 beyond a face (the fill 0 against 0, where the pair is 0 too)."""
    own = np.asarray(frame, dtype=object)
    found: list[Any] = []
    for axis in range(AXES):
        for sigma in (1, -1):
            other = arrival(own, axis, sigma, wrap, fill=0)
            beyond = arrival(np.ones_like(own), axis, sigma, wrap) == 0
            found.append(np.where(beyond | (other == own), 1, -1))
    return tuple(found)


def phase_links(lines: list[Record], wrap: Wrap) -> Phases:
    """The phase pair (c, s) a Node reads through each of its six Ports in Port order (features/phase, `read`; the mathematician's item (g)): through the +a Port the pair of the Node's own +a Link, the cosine and the sine line of the axis among `lines` (the six phase lines of one row of the sign, cosine and sine per axis, then the three count lines), (X cos theta, X sin theta) at theta = |SUM_t n_ij| theta_0 with the sine signed by the Link's count (features/phase `signed_read`: the pair at -n the conjugate of the pair at +n, so that the cube's 48 map the remainders as they map the levels, 2026-10-21); through the -a Port the pair of the Link (i - a, i), the neighbour's at its +a Link, read conjugated, (c, -s), so that the pair read from the two ends is exact by direction (K Hermitian, the count exact), and read unconjugated, (c, s), where the Link's two ends stand in different frames (`frame_signs` on the row's phase row, the last of `lines`: the count K_i - (-1)^(b_i xor b_j) K_j is the same from both ends of such a Link, the two ends reading one frame, ALGEBRA.md, The swap at the top, the frame clause); (0, 0) beyond a face, where the arrival is 0 too."""
    found: list[tuple[Any, Any]] = []
    signs = frame_signs(lines[3 * AXES].remainder, wrap)
    for axis in range(AXES):
        c, s, n = lines[2 * axis], lines[2 * axis + 1], lines[2 * AXES + axis]
        cosine, sine = signed_read(
            ((c.now, c.before, c.remainder), (s.now, s.before, s.remainder)), n.now
        )
        found.append((cosine, sine))
        found.append(
            (arrival(cosine, axis, -1, wrap), -signs[2 * axis + 1] * arrival(sine, axis, -1, wrap))
        )
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
    turn = rotation_unit(*pair, gamma)
    even = tuple(2 * num * factor for factor in factors)  # X_ij, the Link quantity in the Link unit
    odd = tuple(signed_rounded(6 * x * turn * link, square) for x, link in zip(even, links, strict=True))
    return even, odd


def sign_pairs(
    pair: tuple[int, int], gamma: int, factors: tuple[Any, ...], links: tuple[Any, ...]
) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    """The sign's pair on each Link in Port order, in the Link unit (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; the two hands' lines of 2026-10-09, the advisor's (a) and (1), the mathematician's (a)): the Link's angle theta with tan(theta / 2) = n / W at the Link's wall W = 4 Gamma (features/rotation.link_wall), n = n_ij the sign holder's odd line along the Link, the two ends' sum with the direction's sign (`link_levels`), is the exact tangent half-angle triple (W^2 - n^2, 2 W n, W^2 + n^2) rebooked in the Link's unit X_ij = 2 num Q_ij with one rounding each: X^c = rounded(X_ij (W^2 - n^2), W^2 + n^2) and X^s = sgn(n) rounded(X_ij 2 W |n|, W^2 + n^2) (features/phase.signed_rounded, the sign attached after), X^c even in n and X^s odd in n, so that X^c_ji = X^c_ij and X^s_ji = -X^s_ij exactly (K = D M Hermitian, the count exact by Theorem 3) and the pair's magnitude is X_ij to the rounding; no shear and no time turn: the Link turn is the phase pair (`step_plane`, `phase_links`)."""
    num, wall = pair[0], link_wall(gamma)
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
    phases: Phases | None = None,
    amplitude: int = 0,
) -> tuple[tuple[Any, ...], tuple[Any, ...]] | None:
    """Each Link's read as a pair (R^c_ij, R^s_ij) = p_i^2 (X^c_ij, X^s_ij) in Port order, the even read and the odd read of a folded plane (`step_plane`): gravity's pair from the flux holder's odd lines along the Links (`flux`, `odd_links`; `fold_pairs`), the sign's from the sign holder's odd lines (`sign`, `link_levels` of the odd levels; `sign_pairs`) folded with the Link's phase pair (c, s) at the amplitude X (`phases`, `phase_links`; `amplitude`, features/phase.amplitude): ((X^c c - X^s s) div X, (X^s c + X^c s) div X), the hop's pair X e^(i (Phi_i - Phi_j)) inside the sign's one coefficient rounding (features/phase.fold, rounded half up on the magnitude with the sign after, so that the pair read from the two ends is exact by direction; the mathematician's item (g)), and where a plane reads the flux holder too the two pairs multiplied, the product pair rounded once into the Link unit X_ij (((X^c_s X_ij - X^s_s X^s_g) div X_ij, (X^s_s X_ij + X^c_s X^s_g) div X_ij), the same integers in either order, and each alone bit for bit its own pair, the division by X_ij exact then), a Link the world cuts (X_ij = 0) staying at the pair (0, 0); None where the plane reads neither, the plain reads R_ij (ALGEBRA.md, The clock family on the Ports; the two hands' (b) of 2026-10-09)."""
    if flux is None and sign is None:
        return None
    if sign is not None:
        evens, odds = sign_pairs(pair, gamma, factors, sign)
        if phases is not None:  # the sign's pair times the Link's phase pair, one rounding into X_ij
            phased = [
                fold(c, s, hop[0], hop[1], amplitude)
                for c, s, hop in zip(evens, odds, phases, strict=True)
            ]
            evens, odds = tuple(f[0] for f in phased), tuple(f[1] for f in phased)
    if sign is None:
        assert flux is not None
        evens, odds = fold_pairs(pair, gamma, factors, flux)
    elif flux is not None:
        gravity = fold_pairs(pair, gamma, factors, flux)
        folded = []
        for cosine, sine, even, odd in zip(evens, odds, *gravity, strict=True):
            unit = even + (even == 0)  # the Link unit X_ij, 1 on a cut Link where every part is 0
            folded.append(fold(cosine, sine, even, odd, unit))
        evens, odds = tuple(f[0] for f in folded), tuple(f[1] for f in folded)
    pace = paces.link_pace_of(gamma, content)
    square = pace * pace
    return tuple(square * x for x in evens), tuple(square * x for x in odds)


def fold_guard(pair: tuple[int, int], gamma: int, links: tuple[Any, ...], name: str) -> None:
    """The fold's guard at load, as the Link's (`link_guard`): the fold's tangent at most 1 on every Link, 6 K |V_ij| <= Gamma^2, within which a folded arrival's part stays within twice the level (`derived.FOLD_REACH`); refused by name beyond it, naming the Port."""
    turn = rotation_unit(*pair, gamma)
    for port, link in enumerate(links):
        high = int(np.abs(np.asarray(6 * turn * link)).max())
        if high > gamma * gamma:
            raise ValueError(
                f"the fold of {name!r} on the Port {port} is {high} over {gamma * gamma} at load, a tangent "
                "above 1 (the odd line's level along the Link beyond the room the amplitude bound derives for a "
                "folded arrival); the run is refused: raise the holder's level weight"
            )


def turned_room(pair: tuple[int, int], gamma: int, unit: int) -> int:
    """The room of a turned plane's six arrivals under the sign's pair with the Link's phase, in the Link unit: the largest |X^c| + |X^s| over every Link level n the guard admits, |n| <= 4 Gamma (`node.guarded`), read from the sign's pair as the run books it (`plane.sign_pairs` at the vacuum's factor G^2, X_ij = 2 num G^2 the Link quantity), one evaluation per n at load and no root, plus one for the fold with the phase pair (features/phase.fold, the one rounding per part): the sign's pair's magnitude is X to the rounding and the phase pair's X_phase to the walk's bound (the advisor: 1.9 x 10^-7 of X_phase at 2^35, taken as X_phase exactly, a Link weight), so the product pair's two parts' sum reaches X 2^(1/2) at the angle pi / 4, which the sweep over n passes at the tangent half-angle 2^(1/2) - 1, and no more, under FOLD_REACH's 2 X (the advisor's second of 2026-10-09: the shears' reach 2 on the arrivals becomes 2^(1/2)); |X^c re_j - X^s im_j| <= (|X^c| + |X^s|) A at the level A."""
    levels = np.arange(
        link_wall(gamma) + 1
    )  # n from 0 through 4 Gamma, the sign's part even and odd in n
    even, odd = sign_pairs(pair, gamma, (unit * unit,), (levels,))
    return int((np.abs(even[0]) + np.abs(odd[0])).max()) + 1
