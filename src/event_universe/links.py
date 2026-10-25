"""The Links' readings, each a function of arrays at every Node alike and every read across a Link through core/ports.across (the owner's word of 2026-10-25: the Link's act in one place): the two ends' sums even and odd, the centred gradient, the plane's Wronskian and current, the stress's diagonal parts and their trace, a line's current on a Link, its net transverse current and its twist."""

from __future__ import annotations

from typing import Any

from event_universe.core.ports import AXES, PORT_SIDES, across, wrap
from event_universe.rows import Line, zeros


def link(
    port: int, even: tuple[Any, ...] = (), odd: tuple[Any, ...] = (), frame_bits: Any = None
) -> tuple[list[Any], list[Any], Any]:
    """The Link's numbers at one Port, read the same from both ends: for each `even` array the two ends' sum (symmetric), for each `odd` array the two ends' sum signed by the Port's side (antisymmetric: the other end reads the negative), and the frame sign f_ij = 1 where the two ends' frame bits agree and -1 where they differ (from `frame_bits`)."""
    _axis, side = PORT_SIDES[port]
    evens = [a + across(a, port) for a in even]
    odds = [side * (a + across(a, port)) for a in odd]
    f = None if frame_bits is None else 1 - 2 * (frame_bits ^ across(frame_bits, port))
    return evens, odds, f


def gradient(a: Any, axis: int) -> Any:
    """The centred difference of a row's line along an axis, a(i + a) - a(i - a), read through the Link's one read at the two Ports of the axis."""
    return across(a, 2 * axis) - across(a, 2 * axis + 1)


def wronskian(re: Line, im: Line) -> Any:
    """The plane's bilinear W = re_now im_before - im_now re_before at every Node (the charge density, the sign's source)."""
    return re.now * im.before - im.now * re.before


def plane_current(re: Line, im: Line, frames: list[Any]) -> list[Any]:
    """The plane's sign current on each axis, J_a = Im(conj z (z(i + a) - z(i - a))) from the levels now, the neighbours' im read in the Node's frame; the three odd lines' source."""
    found = []
    for a in range(AXES):
        fp, fm = frames[2 * a], frames[2 * a + 1]
        dz_re = gradient(re.now, a)
        dz_im = fp * across(im.now, 2 * a) - fm * across(im.now, 2 * a + 1)
        found.append(re.now * dz_im - im.now * dz_re)
    return found


def stress_parts(lines: list[tuple[Any, int]], shape: tuple[int, ...]) -> list[Any]:
    """The stress tensor's three diagonal parts from the rows' levels, one act on every line alike: SUM over lines of weight x (gradient along the axis)^2; `lines` holds (levels, weight) pairs."""
    parts = [zeros(shape) for _ in range(AXES)]
    for levels, num in lines:
        for a in range(AXES):
            d = gradient(levels, a)
            parts[a] = parts[a] + num * d * d
    return parts


def tensor_parts(parts: list[Any]) -> tuple[Any, list[Any]]:
    """A tensor's trace and its traceless diagonal parts: trace = SUM_a parts_a; traceless_a = 3 parts_a - trace (the stress's trace is the time line's, the axis lines traceless)."""
    trace = parts[0] + parts[1] + parts[2]
    return trace, [AXES * part - trace for part in parts]


def link_current(line: Line, port: int) -> Any:
    """The line's own current on the Link at the Port, F_ij = now_i before_j - before_i now_j: odd under the exchange of the ends (the other end reads -F), read at the interval's start; the + child of a Link birth goes to the end the current flows into."""
    return line.now * across(line.before, port) - line.before * across(line.now, port)


def net_current(line: Line, axis: int) -> Any:
    """A line's net transverse current at every Node along an axis, u_b(k) = F(k, k - b) - F(k, k + b): the current into the Node from the -b Link less the current out along the +b Link, read from the Node's own two Links of that axis."""
    return link_current(line, 2 * axis + 1) - link_current(line, 2 * axis)


def twist(line: Line, axis: int) -> Any:
    """The twist of a line's transverse current along the +axis Link of every Node (PA2's form, the owner's sentence 4): h(k, k + e_a) = u_b(k) u_c(k + e_a) - u_c(k) u_b(k + e_a) with (a, b, c) cyclic, the cross product of the two ends' transverse currents read at each end from its own Links; a pseudoscalar of the unoriented Link, the handedness of the born pair."""
    a, b, c = axis, wrap(axis + 1, AXES), wrap(axis + 2, AXES)
    ub, uc = net_current(line, b), net_current(line, c)
    return ub * across(uc, 2 * a) - uc * across(ub, 2 * a)
