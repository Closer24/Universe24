"""The Links' readings, each a function of arrays at every Node alike and every read across a Link through core/ports.across (the owner's word of 2026-10-25: the Link's act in one place): the two ends' sums even and odd, the centred gradient, the plane's Wronskian and current, the stress's diagonal parts and their trace, a line's current on a Link, its net transverse current and its twist."""

from __future__ import annotations

from typing import Any

from event_universe.core.paces import rounded
from event_universe.core.ports import AXES, PORT_SIDES, across, wrap
from event_universe.core.rule3 import remainder
from event_universe.rows import Line, zeros


def cross(x_i: Any, y_i: Any, x_j: Any, y_j: Any) -> Any:
    """The one bilinear of the law (fd2, U1): x_i y_j - y_i x_j, the 2 x 2 determinant of two readings (x, y) at two places (i, j), odd under the exchange of the places and of the readings; the Wronskian, the current across a Link, the plane's sign current, the twist, the lattice momentum's change, the children's and the credit's senses, the decoder's order of rationals."""
    return x_i * y_j - y_i * x_j


def turn_pair(re: Any, im: Any, c: Any, s: Any, scale: Any) -> tuple[Any, Any]:
    """The pair (re, im) turned by the pair (c, s) over the scale, one rounding half up per part (fd2, U2): the phase pair over the amplitude X, the odd tangent triple over its wall, the decoder's solve."""
    return rounded(c * re - s * im, scale), rounded(s * re + c * im, scale)


class Link:
    """The Link's record at one Port for the interval, read once from its two ends and the same from both (X2's link(i, j)): the factor Q_ij from the two ends' tensions, the frame sign f_ij, the Link's phase pair (cos, sin) over X from the two ends' centred counts, and the odd part n_ij of the shape-4 row's odd line on the Link's axis for the tangent triple; every act reads these and recomputes none."""

    __slots__ = ("factor", "frame", "cosine", "sine", "odd")

    def __init__(self, factor: Any, frame: Any, cosine: Any, sine: Any, odd: Any) -> None:
        self.factor, self.frame, self.cosine, self.sine, self.odd = factor, frame, cosine, sine, odd


def links_of(
    factors: tuple[Any, ...], frames: list[Any], phases: list[tuple[Any, Any]], odd_lines: list[Any]
) -> list[Link]:
    """The six Links' records from the interval's readings: the factors, the frame signs, the phase pairs and, per Port, the odd line of its axis summed over the two ends with the Port's sign (the one Link read of an odd part)."""
    found = []
    for port, (axis, _side) in enumerate(PORT_SIDES):
        _even, (n,), _f = link(port, odd=(odd_lines[axis],))
        found.append(Link(factors[port], frames[port], phases[port][0], phases[port][1], n))
    return found


def link(
    port: int, even: tuple[Any, ...] = (), odd: tuple[Any, ...] = (), frame_bits: Any = None
) -> tuple[list[Any], list[Any], Any]:
    """The Link's numbers at one Port, read the same from both ends: for each `even` array the two ends' sum (symmetric), for each `odd` array the two ends' sum signed by the Port's side (antisymmetric: the other end reads the negative), and the frame sign f_ij = 1 where the two ends' frame bits agree and -1 where they differ, the parity of the Link's even part (fd2, U5)."""
    _axis, side = PORT_SIDES[port]
    evens = [a + across(a, port) for a in even]
    odds = [side * (a + across(a, port)) for a in odd]
    f = None if frame_bits is None else 1 - 2 * remainder(frame_bits + across(frame_bits, port), 2)
    return evens, odds, f


def gradient(a: Any, axis: int) -> Any:
    """The centred difference of a row's line along an axis, a(i + a) - a(i - a), read through the Link's one read at the two Ports of the axis."""
    return across(a, 2 * axis) - across(a, 2 * axis + 1)


def wronskian(re: Line, im: Line) -> Any:
    """The plane's bilinear W = re_now im_before - im_now re_before at every Node (the charge density, the sign's source)."""
    return cross(re.now, im.now, re.before, im.before)


def plane_current(re: Line, im: Line, frames: list[Any]) -> list[Any]:
    """The plane's sign current on each axis, J_a = Im(conj z (z(i + a) - z(i - a))) from the levels now, the neighbours' im read in the Node's frame; the three odd lines' source."""
    found = []
    for a in range(AXES):
        fp, fm = frames[2 * a], frames[2 * a + 1]
        dz_re = gradient(re.now, a)
        dz_im = fp * across(im.now, 2 * a) - fm * across(im.now, 2 * a + 1)
        found.append(cross(re.now, im.now, dz_re, dz_im))
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
    return cross(line.now, line.before, across(line.now, port), across(line.before, port))


def net_current(line: Line, axis: int) -> Any:
    """A line's net transverse current at every Node along an axis, u_b(k) = F(k, k - b) - F(k, k + b): the current into the Node from the -b Link less the current out along the +b Link, read from the Node's own two Links of that axis."""
    return link_current(line, 2 * axis + 1) - link_current(line, 2 * axis)


def twist(line: Line, axis: int) -> Any:
    """The twist of a line's transverse current along the +axis Link of every Node (PA2's form, the owner's sentence 4): h(k, k + e_a) = u_b(k) u_c(k + e_a) - u_c(k) u_b(k + e_a) with (a, b, c) cyclic, the cross product of the two ends' transverse currents read at each end from its own Links; a pseudoscalar of the unoriented Link, the handedness of the born pair."""
    a, b, c = axis, wrap(axis + 1, AXES), wrap(axis + 2, AXES)
    ub, uc = net_current(line, b), net_current(line, c)
    return cross(ub, uc, across(ub, 2 * a), across(uc, 2 * a))
