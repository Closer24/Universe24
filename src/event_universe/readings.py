"""The readings of a record's lines at every Node, one Link's reach each (ALGEBRA.md #the-count-is-the-records-share, #readings-and-measurements; features/currents): the six arrivals in Port order (`ports`), the currents through the Ports (`currents_of`), the tension's part, the shear's part and the axis sources (`stresses_of`, `off_diagonals_of`, `axis_sources_of`), the sign's current (`sense_current_of`), the lattice momentum per axis (`momentum_of`); readings alone, no level written."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import numpy as np

from event_universe.core.ports import AXES, Wrap, arrival
from event_universe.features import currents
from event_universe.records import Record

Part = Callable[
    [int, tuple[currents.Neighbours, currents.Neighbours, currents.Neighbours]], currents.Vector
]  # a reading of one level's neighbours per axis or axis pair, the tension's or the shear's


def ports(a: np.ndarray, wrap: Wrap, fill: int = 0) -> tuple[np.ndarray, ...]:
    """The six arrivals of an array in Port order [+X, -X, +Y, -Y, +Z, -Z]: the neighbour's level through each Port, `fill` beyond a face that does not wrap (0, or the row's rest for the massless row holding the content: the vacuum beyond the face is the same vacuum, ALGEBRA.md #what-is-open, item 22), the Node itself on a folded axis."""
    return tuple(arrival(a, axis, side, wrap, fill) for axis in range(3) for side in (1, -1))


def sense_current_of(lines: Sequence[Record], wrap: Wrap) -> currents.Vector:
    """The sign's current of a two-part record at every Node on each axis, the Node's two a-Links' Wronskian currents summed, a reading of its planes' lines at the interval's start: J_a(i) = Im(conj(z_i) (z_(i+a) - z_(i-a))) = re_i (im_(+a) - im_(-a)) - im_i (re_(+a) - re_(-a)) = (G_(i, i-a) - G_(i, i+a)) / num, the net of the conserved current G_ij = num (im_i re_j - re_i im_j) through the Node's two a-Ports from the levels now, every plane's added, one Link's reach, unhalved (the mathematician's (L2) and the advisor's (c) of 2026-10-09: the mean of the two Links taken by the doubled wall of the odd lines' write, `loader.derived.held_write_of`, 2 E_s T, as Part A takes the flux's), odd under the sense exactly (a record and its conjugate give opposite currents, where the momentum density P_a = (F_(+a) - F_(-a)) / num, quadratic in each real line, gave the same), even under the time reversal; the source of the holder of the sign's odd lines under the rotation, J_a = (6 den / num) W v on a plane record, so that the odd level over the time level is 3 (den / num) v = v / c_s^2 and the magnetic over the electric force on a co-moving reader is 1 / gamma (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; the owner's word on the two hands)."""
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


def currents_of(
    weight: int, lines: Sequence[Record], wrap: Wrap, weights: Sequence[int] | None = None
) -> tuple[np.ndarray, ...]:
    """The currents of a record at every Node, a reading of its lines (ALGEBRA.md #the-count-is-the-records-share; features/currents): through each of the six Ports F_ij = num (now_i before_j - before_i now_j) into the Node from its neighbour, every line's currents added, at the lines as they stand (the pair the step started from, read before Rule3 acts, so that the share's change over the step is exactly their sum); what a node_detector reads at its boundary; `weights`, one integer per line multiplying that line's currents (None: every line at 1), the covector's form of a holder under the Lorentz form, (-3, 1, 1, 1) over its time line and its three odd lines in thirds of the time line's unit (covector.weights)."""
    found: list[Any] = [0] * 6
    scales = [1] * len(lines) if weights is None else list(weights)
    for record, scale in zip(lines, scales, strict=True):
        here = currents.Levels(record.now, record.before)
        now, before = ports(record.now, wrap), ports(record.before, wrap)
        for port in range(6):
            there = currents.Levels(now[port], before[port])
            found[port] = found[port] + currents.current(weight * scale, here, there)
    return tuple(np.asarray(value) for value in found)


def momentum_of(
    weight: int, lines: Sequence[Record], wrap: Wrap, at: np.ndarray | None = None
) -> tuple[int, int, int]:
    """A record's lattice momentum per axis, a reading of its lines (Part F, features/currents `momentum`; the two hands' lines of 2026-10-09): every line's antisymmetric sum of its two Link currents along the axis, added, in the current's unit at the weight num, over the board (`at` None) or over the Nodes a mask names (Part F2: the per-Node terms before their sum at a region's Nodes, `currents.momentum_terms`, the piece's P_a at the region the credit books at a window's close, `node_detector.piece_momentum`); what the write must give the taker."""
    found = []
    for axis in range(AXES):
        total = 0
        for r in lines:
            terms = currents.momentum_terms(r.now, r.before, axis, wrap, weight)
            total += int((terms if at is None else terms[at]).sum(dtype=object))
        found.append(total)
    return int(found[0]), int(found[1]), int(found[2])


def stresses_of(
    weight: int, lines: Sequence[Record], wrap: Wrap, part: Part = currents.stress
) -> currents.Vector:
    """The tension's part at every Node on each axis from a record's levels now as they stand at the interval's start, weight x h_a(i) with h_a(i) = now_(i-a) now_(i+a) - now_i^2, every line's parts added, a reading of the lines into the held rows' axis lines, one Link's reach (features/currents; ALGEBRA.md #the-primitives, the row "the held write", The tension); `part` the reading of one line's neighbours summed over the lines, the tension's (features/currents `stress`) or, through `off_diagonals_of`, the shear's, one body for the two."""
    tensions: currents.Vector = (0, 0, 0)
    for record in lines:
        found = part(weight, axis_neighbours(record.now, wrap))
        tensions = (tensions[0] + found[0], tensions[1] + found[1], tensions[2] + found[2])
    return tuple(np.asarray(value) for value in tensions)  # type: ignore[return-value]


def off_diagonals_of(weight: int, lines: Sequence[Record], wrap: Wrap) -> currents.Vector:
    """The shear's part at every Node on each axis pair, xy, yz, zx, from a record's levels now as they stand at the interval's start, weight x D_a now_i x D_b now_i with D_a now_i = now_(i+a) - now_(i-a), the product of the Node's own two axis differences, every line's parts added, a reading of the lines into the held rows' shear lines, one Link's reach and the same interval (features/currents `off_diagonal`; ALGEBRA.md, The tension, the off-diagonal booking G_ab met in the mean at the Link's two ends) (one body with `stresses_of`, the shear's part in the tension's place)."""
    return stresses_of(weight, lines, wrap, currents.off_diagonal)


def axis_sources_of(
    weight: int, lines: Sequence[Record], wrap: Wrap, off_diagonal: bool = False
) -> tuple[Any, ...]:
    """The axis sources of a record at every Node, six readings of its lines at the interval's start, nine where a held row of the world declares the shear, one Link's reach: the tension's part on each axis (`stresses_of`, into the held rows' tension lines), then the count's flux along each axis, the current through the -a Port less the current through the +a Port, F_(i, i-a) - F_(i, i+a) (`currents_of`, the pair the step starts from), the axis's two Links' flux summed unhalved into the flux holder's odd lines (ALGEBRA.md, The clock family on the Ports), then, with `off_diagonal`, the shear's part on each axis pair xy, yz, zx (`off_diagonals_of`, into the shear lines); a holder takes the readings its lines name, by position (`records.write_sources`)."""
    through = currents_of(weight, lines, wrap)
    fluxes = [through[2 * axis + 1] - through[2 * axis] for axis in range(AXES)]
    off = off_diagonals_of(weight, lines, wrap) if off_diagonal else ()
    return (*stresses_of(weight, lines, wrap), *fluxes, *off)


def axis_neighbours(
    now: np.ndarray, wrap: Wrap
) -> tuple[currents.Neighbours, currents.Neighbours, currents.Neighbours]:
    """The level now at every Node and at its two neighbours along each axis, through the +a and the -a Port, the tension's reads (ALGEBRA.md #the-primitives, the row "the held write", The tension)."""
    arrived = ports(now, wrap)
    found = [currents.Neighbours(now, arrived[2 * axis], arrived[2 * axis + 1]) for axis in range(3)]
    return found[0], found[1], found[2]
