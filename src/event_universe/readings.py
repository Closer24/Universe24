"""The readings of a record's lines at every Node, one Link's reach each (ALGEBRA.md #the-count-is-the-records-share, #readings-and-measurements; features/currents): the six arrivals in Port order (`ports`), the currents through the Ports (`currents_of`; a turned record's the flux line's own with the Link's pair, `turned_currents_of`, `Turned`), the tension's part, the shear's part and the axis sources (`stresses_of`, `off_diagonals_of`, `axis_sources_of`), the sign's current (`sense_current_of`), the lattice momentum per axis (`momentum_of`); readings alone, no level written."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import numpy as np

from event_universe.core.ports import AXES, arrival
from event_universe.features import currents
from event_universe.records import Record

Part = Callable[
    [int, tuple[currents.Neighbours, currents.Neighbours, currents.Neighbours]], currents.Vector
]  # a reading of one level's neighbours per axis or axis pair, the tension's or the shear's


def framed(arrived: tuple[np.ndarray, ...], frames: Sequence[Any] | None) -> tuple[np.ndarray, ...]:
    """The six arrivals of a plane's im line read in the Node's frame: each multiplied by its Port's frame sign (plane.frame_signs, -1 across a Link whose two ends stand in different frames under the swap at the top, the neighbour's value read conjugated so that the Link reads its two ends in one frame, ALGEBRA.md, The swap at the top, the frame clause); as they are where `frames` is None."""
    if frames is None:
        return arrived
    return tuple(sign * level for sign, level in zip(frames, arrived, strict=True))


def at(value: Any, where: tuple[Any, ...]) -> Any:
    """A coefficient at a slice or a Node of the board: the slice where it is an array over the Nodes, itself where it is one integer (a family reading nothing has one reach per Port for every Node)."""
    return value[where] if np.ndim(value) else value


def slices(
    axis: int,
) -> tuple[tuple[slice, ...], tuple[slice, ...], tuple[slice, ...], tuple[slice, ...]]:
    """The four slices of an axis: every Node but the last (the near end of every Link toward +a), every Node but the first (the far end), the first layer and the last layer (the two faces)."""
    lo = [slice(None)] * AXES
    hi, first, last = list(lo), list(lo), list(lo)
    lo[axis], hi[axis] = slice(None, -1), slice(1, None)
    first[axis], last[axis] = slice(0, 1), slice(-1, None)
    return tuple(lo), tuple(hi), tuple(first), tuple(last)


def ports(a: np.ndarray) -> tuple[np.ndarray, ...]:
    """The six arrivals of an array in Port order [+X, -X, +Y, -Y, +Z, -Z]: the neighbour's level through each Port of the torus, the Node itself on a folded axis."""
    return tuple(arrival(a, axis, side) for axis in range(3) for side in (1, -1))


def sense_current_of(lines: Sequence[Record], frames: Sequence[Any] | None = None) -> currents.Vector:
    """The sign's current of a two-part record at every Node on each axis, the Node's two a-Links' Wronskian currents summed, a reading of its planes' lines at the interval's start: J_a(i) = Im(conj(z_i) (z_(i+a) - z_(i-a))) = re_i (im_(+a) - im_(-a)) - im_i (re_(+a) - re_(-a)) = (G_(i, i-a) - G_(i, i+a)) / num, the net of the conserved current G_ij = num (im_i re_j - re_i im_j) through the Node's two a-Ports from the levels now, every plane's added, one Link's reach, unhalved (the mathematician's (L2) and the advisor's (c) of 2026-10-09: the mean of the two Links taken by the doubled wall of the odd lines' write, `loader.derived.held_write_of`, 2 E_s T, as Part A takes the flux's), odd under the sense exactly (a record and its conjugate give opposite currents, where the momentum density P_a = (F_(+a) - F_(-a)) / num, quadratic in each real line, gave the same), even under the time reversal; the source of the holder of the sign's odd lines under the rotation, J_a = (6 den / num) W v on a plane record, so that the odd level over the time level is 3 (den / num) v = v / c_s^2 and the magnetic over the electric force on a co-moving reader is 1 / gamma (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; the owner's word on the two hands); `frames`, per Port the sign the Node reads its neighbour's im part with (plane.frame_signs, -1 across a Link whose two ends stand in different frames under the swap at the top, the neighbour read conjugated: the Link reads its two ends in one frame), None every Port at +1."""
    found: list[Any] = [0, 0, 0]
    for re_line, im_line in zip(lines[0::2], lines[1::2], strict=True):
        re_at, im_at = ports(re_line.now), framed(ports(im_line.now), frames)
        for axis in range(3):
            plus, minus = 2 * axis, 2 * axis + 1
            found[axis] = (
                found[axis]
                + re_line.now * (im_at[plus] - im_at[minus])
                - im_line.now * (re_at[plus] - re_at[minus])
            )
    return np.asarray(found[0]), np.asarray(found[1]), np.asarray(found[2])


def currents_of(
    weight: int,
    lines: Sequence[Record],
    frames: Sequence[Any] | None = None,
    horizon: Sequence[Any] | None = None,
) -> tuple[np.ndarray, ...]:
    """The currents of a record at every Node, a reading of its lines (ALGEBRA.md #the-count-is-the-records-share; features/currents): through each of the six Ports F_ij = num (now_i before_j - before_i now_j) into the Node from its neighbour, every line's currents added, at the lines as they stand (the pair the step started from, read before Rule3 acts, so that the share's change over the step is exactly their sum); what a node_detector reads at its boundary; `weights`, one integer per line multiplying that line's currents (None: every line at 1), the covector's form of a holder under the Lorentz form, (-3, 1, 1, 1) over its time line and its three odd lines in thirds of the time line's unit (covector.weights); `turned`, the pairs a turned record's step reads with the unit of its booking (`Turned`, None for a plain record, whose currents are bit for bit the plain bilinear's): the record's currents are then the flux line's own with the Link's pair (`turned_currents_of`; ALGEBRA.md, The share's change is the currents, the clause of 2026-10-21), since the plain bilinear of a turned pair turns at the difference of the two Nodes' angles, the gauge's oscillation of zero mean, and books nothing; `frames`, the Port signs a turned plane's im lines (every second line) read their neighbours with (`framed`), None every Port at +1; `horizon`, per Port the mask of the Links at the wall (board_readings.horizon_ports), through which the current reads 0 as the step moves nothing across them (ALGEBRA.md, The horizon, 2026-10-23), None no such Link."""
    found: list[Any] = [0] * 6
    for number, record in enumerate(lines):
        here = currents.Levels(record.now, record.before)
        signs = frames if number & 1 else None
        now, before = framed(ports(record.now), signs), framed(ports(record.before), signs)
        for port in range(6):
            there = currents.Levels(now[port], before[port])
            found[port] = found[port] + currents.current(weight, here, there)
    if horizon is not None:  # a Link at the wall reads nothing: its current 0 (ALGEBRA.md, The horizon)
        found = [np.where(at, 0, value) for at, value in zip(horizon, found, strict=True)]
    return tuple(np.asarray(value) for value in found)


def momentum_of(
    weight: int, lines: Sequence[Record], at: np.ndarray | None = None
) -> tuple[int, int, int]:
    """A record's lattice momentum per axis, a reading of its lines (Part F, features/currents `momentum`; the two hands' lines of 2026-10-09): every line's antisymmetric sum of its two Link currents along the axis, added, in the current's unit at the weight num, over the board (`at` None) or over the Nodes a mask names (Part F2: the per-Node terms before their sum at a region's Nodes, `currents.momentum_terms`, the piece's P_a at the region the credit books at a window's close, `node_detector.piece_momentum`); what the write must give the taker."""
    found = []
    for axis in range(AXES):
        total = 0
        for r in lines:
            terms = currents.momentum_terms(r.now, r.before, axis, weight)
            total += int((terms if at is None else terms[at]).sum(dtype=object))
        found.append(total)
    return int(found[0]), int(found[1]), int(found[2])


def stresses_of(
    weight: int,
    lines: Sequence[Record],
    part: Part = currents.stress,
    frames: Sequence[Any] | None = None,
) -> currents.Vector:
    """The tension's part at every Node on each axis from a record's levels now as they stand at the interval's start, weight x h_a(i) with h_a(i) = now_(i-a) now_(i+a) - now_i^2, every line's parts added, a reading of the lines into the held rows' axis lines, one Link's reach (features/currents; ALGEBRA.md #the-primitives, the row "the held write", The tension); `part` the reading of one line's neighbours summed over the lines, the tension's (features/currents `stress`) or, through `off_diagonals_of`, the shear's, one body for the two; `frames`, the Port signs a turned plane's im lines (every second line) read their neighbours with (`framed`)."""
    tensions: currents.Vector = (0, 0, 0)
    for number, record in enumerate(lines):
        found = part(weight, axis_neighbours(record.now, frames if number & 1 else None))
        tensions = (tensions[0] + found[0], tensions[1] + found[1], tensions[2] + found[2])
    return tuple(np.asarray(value) for value in tensions)  # type: ignore[return-value]


def axis_sources_of(
    weight: int, lines: Sequence[Record], frames: Sequence[Any] | None = None
) -> tuple[Any, ...]:
    """The axis sources of a record at every Node, six readings of its lines at the interval's start, nine where a held row of the world declares the shear, one Link's reach: the tension's part on each axis (`stresses_of`, into the held rows' tension lines), then the count's flux along each axis, the current through the -a Port less the current through the +a Port, F_(i, i-a) - F_(i, i+a) (`currents_of`, the pair the step starts from), the axis's two Links' flux summed unhalved into the flux holder's odd lines (ALGEBRA.md, The clock family on the Ports), then, with `off_diagonal`, the shear's part on each axis pair xy, yz, zx (`off_diagonals_of`, into the shear lines); a holder takes the readings its lines name, by position (`records.write_sources`)."""
    through = currents_of(weight, lines, frames=frames)
    fluxes = [through[2 * axis + 1] - through[2 * axis] for axis in range(AXES)]
    return (*stresses_of(weight, lines, currents.stress, frames), *fluxes)


def axis_neighbours(
    now: np.ndarray, frames: Sequence[Any] | None = None
) -> tuple[currents.Neighbours, currents.Neighbours, currents.Neighbours]:
    """The level now at every Node and at its two neighbours along each axis, through the +a and the -a Port, the tension's reads (ALGEBRA.md #the-primitives, the row "the held write", The tension); `frames` the Port signs a plane's im line reads with (`framed`)."""
    arrived = framed(ports(now), frames)
    found = [currents.Neighbours(now, arrived[2 * axis], arrived[2 * axis + 1]) for axis in range(3)]
    return found[0], found[1], found[2]
