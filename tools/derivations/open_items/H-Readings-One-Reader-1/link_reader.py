"""The one reader of the Link (H-Readings-One-Reader-1): every reading of a Link at a Port is a reading of ONE record, read once per interval per Link and the same from both ends up to the side's sign: the two ends' even sum e(a) = a_i + a_j, the two ends' odd sum o(a) = side (a_i + a_j) (the other end reads -o), the frame parity f = 1 - 2 odd(b_i + b_j), and the one cross F(x, y) = x_i y_j - y_i x_j (the other end reads -F). The factor, the frame, the phase pair, the fold, the twist, the current, the flux and the gradient are named readings of these four; nothing here is a new arithmetic: each line is the engine's own form, so the proof is bit for bit by construction and the count of lines is the measure."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.paces import odd_rounded, rounded
from event_universe.core.ports import AXES, SIDES, across, port_of, wrap
from event_universe.core.ports import PORT_SIDES
from event_universe.core.rule3 import half, link_factor, odd
from event_universe.links import Link
from event_universe.rows import PLANE


def even(a: Any, port: int) -> Any:
    """The Link's even sum, a_i + a_j, the same from both ends."""
    return a + across(a, port)


def odd_sum(a: Any, port: int) -> Any:
    """The Link's odd sum, side (a_i + a_j): the other end reads the negative."""
    return PORT_SIDES[port][1] * even(a, port)


def frame(bits: Any, port: int) -> Any:
    """The frame sign f_ij = 1 - 2 odd(b_i + b_j), the parity of the Link's even part."""
    parity = odd(even(bits, port))
    return 1 - parity - parity


def cross(x_i: Any, y_i: Any, x_j: Any, y_j: Any) -> Any:
    """The one bilinear, x_i y_j - y_i x_j."""
    return x_i * y_j - y_i * x_j


def current(now: Any, before: Any, port: int) -> Any:
    """A line's current on the Link, F_ij = now_i before_j - before_i now_j (the other end reads -F)."""
    return cross(now, before, across(now, port), across(before, port))


def gradient(a: Any, axis: int) -> Any:
    """The centred difference along an axis, the + Port's arrival less the - Port's."""
    return across(a, port_of(axis, 0)) - across(a, port_of(axis, 1))


def net_current(now: Any, before: Any, axis: int) -> Any:
    """A line's net transverse current along an axis, F(k, k - b) - F(k, k + b)."""
    return current(now, before, port_of(axis, 1)) - current(now, before, port_of(axis, 0))


def twist(pairs: list[tuple[Any, Any]], axis: int) -> Any:
    """The twist along the + axis Link: the cross of the two ends' net transverse currents on the other two axes."""
    b, c = wrap(axis + 1, AXES), wrap(axis - 1, AXES)
    ub = sum((net_current(n, bf, b) for n, bf in pairs), start=0)
    uc = sum((net_current(n, bf, c) for n, bf in pairs), start=0)
    return cross(ub, uc, across(ub, port_of(axis, 0)), across(uc, port_of(axis, 0)))


def factor(gamma: Any, unit: Any, level: Any, port: int, frozen: Any = None) -> Any:
    """The Link's factor Q_ij: the tension the mean of the two ends' levels rounded half up, read at the wall at or past Gamma; 0 where either end is frozen."""
    t = rounded(even(level, port), SIDES)
    q = np.vectorize(lambda tt: int(link_factor(gamma, unit, min(int(tt), gamma))), otypes=[object])(t)
    return q if frozen is None else np.where(frozen | across(frozen, port), 0, q)


def phase(node: Any, count: Any, f: Any, port: int) -> tuple[Any, Any]:
    """The Link's count n_ij = K_i - f_ij K_j and its (cos, sin) pair along the one orbit."""
    from event_universe.readings import pair_angle

    n = count - f * across(count, port)
    pairs = np.vectorize(lambda m: pair_angle(node, m), otypes=[object, object])(n)
    return pairs[0], pairs[1]


def triple(wall: Any, m: Any) -> tuple[Any, Any, Any]:
    """The tangent triple (W^2 - m^2, 2 W m, W^2 + m^2) of an odd part m over the wall W."""
    return wall * wall - m * m, (wall + wall) * m, wall * wall + m * m


def fold(flux_axis: Any, rotation: Any, gamma: Any, port: int) -> tuple[Any, Any, Any]:
    """The flux lines' fold at a Link: the odd sum of the axis's flux line times 3 K as the tangent triple over Gamma^2."""
    return triple(gamma * gamma, half(SIDES * AXES) * rotation * odd_sum(flux_axis, port))


def read_link(
    node: Any,
    port: int,
    level: Any,
    frozen: Any,
    bits: Any,
    count: Any,
    odd_axis: Any,
    flux_axis: Any,
    rotation: Any,
    coupling: int = 1,
) -> Link:
    """The one reader: the Link's record at a Port for an interval, every part from the four readings at the coupling (0: the identity turn by arithmetic)."""
    f = frame(bits, port) ** coupling
    c, s = phase(node, count * coupling, f, port)
    return Link(
        factor(node.gamma, node.G, level, port, frozen),
        f,
        c,
        s,
        odd_sum(odd_axis * coupling, port),
        fold(flux_axis, rotation, node.gamma, port),
    )


def turn_pair(re: Any, im: Any, c: Any, s: Any, scale: Any) -> tuple[Any, Any]:
    """The pair turned by (c, s) over the scale, one odd rounding per part."""
    return odd_rounded(c * re - s * im, scale), odd_rounded(s * re + c * im, scale)


def turned(xs: list[Any], at: Link, scale: Any, gamma: Any) -> list[Any]:
    """A row's lines turned by the Link's record: the phase pair over X, then the odd line's tangent triple at the wall 4 Gamma multiplied by the fold."""
    tc, ts, tw = triple((SIDES + SIDES) * gamma, at.odd)
    fc, fs, fw = at.fold
    tc, ts, tw = tc * fc - ts * fs, ts * fc + tc * fs, tw * fw
    found: list[Any] = []
    for re_j, im_j in zip(xs[0::PLANE], xs[1::PLANE], strict=True):
        found += turn_pair(*turn_pair(re_j, im_j, at.cosine, at.sine, scale), tc, ts, tw)
    return found
