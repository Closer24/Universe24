"""The one reader of the Link (H-Readings-One-Reader-2): every reading of a Link is the Link's one read at a Port, the pair (x_i, x_j) of one array at the two ends, combined one way: linear, x_i + sign x_j (the even sum at +1: the tension, the frame bits' parity; the difference at -1: the count K_i - f K_j, the gradient; the odd part: the sum signed by the Port's side), or bilinear, F_ij = x_i y_j - y_i x_j (the current of a line, the twist of two net currents). The Link's record (the factor, the frame, the phase pair, the odd part, the fold) and its turn of a row's lines are named readings of `read`; no act recomputes any of them. Imports through the engine's core, links (Link, turn_pair) and readings (pair_angle) alone."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.paces import rounded
from event_universe.core.ports import AXES, PORT_SIDES, PORTS, SIDES, across, port_of, wrap
from event_universe.core.rule3 import half, link_factor, odd
from event_universe.links import Link, turn_pair
from event_universe.readings import pair_angle


def read(x: Any, port: int, y: Any = None, sign: int = 1) -> Any:
    """The Link's one read at a Port: x_i + sign x_j (y None), or the bilinear x_i y_j - y_i x_j."""
    x_j = across(x, port)
    if y is None:
        return x + sign * x_j
    return x * across(y, port) - y * x_j


def even(x: Any, port: int) -> Any:
    """The even reading, the two ends' sum (the same from both ends)."""
    return read(x, port)


def odd_part(x: Any, port: int) -> Any:
    """The odd reading, the two ends' sum signed by the Port's side (the other end reads the negative)."""
    return PORT_SIDES[port][1] * read(x, port)


def frame(bits: Any, port: int) -> Any:
    """The frame sign f_ij = 1 - 2 parity of the two ends' frame bits' sum."""
    parity = odd(read(bits, port))
    return 1 - parity - parity


def count(k: Any, f: Any, port: int) -> Any:
    """The Link's count n_ij = K_i - f_ij K_j, the difference read with the frame."""
    return read(k, port, sign=-f)


def gradient(a: Any, axis: int) -> Any:
    """The centred difference a(i + a) - a(i - a): the two Ports' differences read."""
    return read(a, port_of(axis, 1), sign=-1) - read(a, port_of(axis, 0), sign=-1)


def current(now: Any, before: Any, port: int) -> Any:
    """A line's current on the Link, F_ij = now_i before_j - before_i now_j."""
    return read(now, port, before)


def net_current(now: Any, before: Any, axis: int) -> Any:
    """A line's net transverse current along an axis, F(k, k - b) - F(k, k + b)."""
    return current(now, before, port_of(axis, 1)) - current(now, before, port_of(axis, 0))


def twist(nows: list[Any], befores: list[Any], axis: int) -> Any:
    """The twist along the +axis Link: the cross of the two transverse net currents at the two ends."""
    b, c = wrap(axis + 1, AXES), wrap(axis - 1, AXES)
    ub = sum((net_current(n, bf, b) for n, bf in zip(nows, befores, strict=True)), start=0)
    uc = sum((net_current(n, bf, c) for n, bf in zip(nows, befores, strict=True)), start=0)
    return read(ub, port_of(axis, 0), uc)


def factor(gamma: int, unit: int, levels: list[Any], port: int, frozen: Any = None) -> Any:
    """The Link's factor from the two ends' tensions' mean rounded half up, 0 at a frozen end."""
    t = rounded(even(levels[PORT_SIDES[port][0]], port), SIDES)
    q = np.vectorize(lambda tt: int(link_factor(gamma, unit, min(int(tt), gamma))), otypes=[object])
    if frozen is None:
        return q(t)
    return np.where(frozen | across(frozen, port), 0, q(t))


def phases(node: Any, k: Any, f: Any, port: int) -> tuple[Any, Any]:
    """The Link's phase pair (cos, sin) over X at the Link's count."""
    pairs = np.vectorize(lambda m: pair_angle(node, m), otypes=[object, object])(count(k, f, port))
    return pairs[0], pairs[1]


def fold(flux_line: Any, rotation: int, gamma: int, port: int) -> tuple[Any, Any, Any]:
    """The flux lines' fold triple at the record's rest rotation, the identity at the rotation 0 or the flux 0."""
    m = half(PORTS) * rotation * odd_part(flux_line, port)
    w2 = gamma * gamma
    return w2 * w2 - m * m, (w2 + w2) * m, w2 * w2 + m * m


def record(
    node: Any,
    factors: tuple[Any, ...],
    frames: list[Any],
    k: Any,
    odd_lines: list[Any],
    coupling: int,
    rotation: int = 0,
    flux_lines: list[Any] | None = None,
) -> list[Link]:
    """The six Links' records at a coupling, each one Link read per part: the factor, the frame sign to the coupling, the phase pair at the count times the coupling, the odd part of the odd line times the coupling, the fold of the flux line at the rotation."""
    found = []
    for port, (axis, _side) in enumerate(PORT_SIDES):
        f = frames[port] ** coupling
        cosine, sine = phases(node, k * coupling, frames[port], port)
        n = odd_part(odd_lines[axis] * coupling, port)
        at = (1, 0, 1) if flux_lines is None else fold(flux_lines[axis], rotation, node.gamma, port)
        found.append(Link(factors[port], f, cosine, sine, n, at))
    return found


def turn(xs: list[Any], at: Link, scale: Any, gamma: int, plane: int) -> list[Any]:
    """A row's lines turned by the Link's record: the phase pair over X, then the odd line's tangent triple at the wall 4 Gamma times the fold triple, one odd rounding per part."""
    wl = (gamma + gamma) + (gamma + gamma)
    tc, ts, tw = wl * wl - at.odd * at.odd, (wl + wl) * at.odd, wl * wl + at.odd * at.odd
    fc, fs, fw = at.fold
    tc, ts, tw = tc * fc - ts * fs, ts * fc + tc * fs, tw * fw
    found: list[Any] = []
    for re_j, im_j in zip(xs[0::plane], xs[1::plane], strict=True):
        a_re, a_im = turn_pair(re_j, im_j, at.cosine, at.sine, scale)
        found += turn_pair(a_re, a_im, tc, ts, tw)
    return found
