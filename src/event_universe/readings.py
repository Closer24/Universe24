"""The Node's readings at an interval's start, each a function of the Node's state at every Node alike: the content (the carrier's level), the (cos, sin) pair at a count along the one orbit, the Link factors from the two ends' axis parts, the frame signs, the centred count and the Links' phases, the swap's floor; the records' share is gram.share."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import PORT_SIDES, PORTS, across
from event_universe.core.rule3 import link_factor
from event_universe.features import phase, volume
from event_universe.links import link
from event_universe.rows import CARRIER, Line

if TYPE_CHECKING:
    from event_universe.node import Node


def paces_of(node: Node, content: Any) -> tuple[Any, Any]:
    """The Node's two paces from its content, the clock p_0 and the Link's pace p_i (X2: paces(content)), one reading."""
    return paces.clock_of(node.gamma, content), paces.link_pace_of(node.gamma, content)


def frozen_of(node: Node, content: Any) -> Any:
    """The frozen mask from the content (BH-S1): the Nodes whose Link pace reads 0 at the interval's start, one reading for the interval, the close and the writer."""
    pace = np.asarray(paces_of(node, content)[1], dtype=object)
    return pace == 0 if np.ndim(pace) else np.zeros(node.shape, dtype=bool)


def content(node: Node) -> Any:
    """The content at every Node, the level of the carrier's time line."""
    return np.asarray(volume.level_of(node.gamma, node.row(CARRIER).lines[0].now), dtype=object)


def pair_angle(node: Node, n: Any) -> tuple[int, int]:
    """The integer (cos, sin) pair at the count n along the one orbit from the seed (features/phase), the orbit a table built as far as the counts reach."""
    n = int(n)
    s = 1 if n >= 0 else -1
    n = abs(n)
    while len(node.orbit) <= n:
        c, sn = node.orbit_lines[-1]
        c, sn = phase.act(c, node.gamma, 1), phase.act(sn, node.gamma, 1)
        node.orbit_lines = [(c, sn)]
        node.orbit.append((int(c[0]), int(sn[0])))
    c_, sn_ = node.orbit[n]
    return c_, s * sn_


def link_factors(
    node: Node, axis_levels: list[Any] | None = None, frozen: Any = None
) -> tuple[Any, ...]:
    """The Link factor at each Port from the two ends' axis parts of the carrier: the tension the mean of the two ends' levels rounded half up (the one rounding not reached by the remainder's rule: fd1 measured the odd rounding here parts the 48's reflections), a tension at or past Gamma read at the wall, the factor 0 (the horizon); and 0 where either end is frozen, the Link pace 0 at the interval's start (BH-S1: every Link with a frozen end is at the wall, from both ends)."""
    levels = [line.now for line in node.row(CARRIER).lines[1:4]] if axis_levels is None else axis_levels
    found = []
    for port, (axis, _side) in enumerate(PORT_SIDES):
        (summed,), _odd, _f = link(port, even=(levels[axis],))
        t = paces.rounded(summed, 2)
        factor = np.vectorize(
            lambda tt: int(link_factor(node.gamma, node.G, min(int(tt), node.gamma))),
            otypes=[object],
        )
        at_wall = None if frozen is None else frozen | across(frozen, port)
        found.append(factor(t) if at_wall is None else np.where(at_wall, 0, factor(t)))
    return tuple(found)


def frames(node: Node, phi_rem: Any) -> list[Any]:
    """The frame signs per Port: +1 where the two ends' frame bits (the phase row's remainder at the wall 2, complemented at every swap) agree, -1 where they differ; there the neighbour's plane is read conjugated and its count negated."""
    return [link(port, frame_bits=phi_rem)[2] for port in range(PORTS)]


def centred_count(node: Node, cphi: Any, phi: Line) -> Any:
    """The Node's centred count K = 2 (Phi_now - Phi_before) + c from the phase row at the start, twice the trapezoid sum of the clocked potential to the triple's centre."""
    return 2 * (phi.now - phi.before) + cphi


def link_phases(node: Node, frames: list[Any], count: Any) -> list[tuple[Any, Any]]:
    """The Link's count n_ij = K_i - f_ij K_j (the two ends' centred counts; f_ij the frame sign, the neighbour's count negated where the frames differ) and its (cos, sin) pair over X."""
    found = []
    for port in range(PORTS):
        n = count - frames[port] * across(count, port)
        pairs = np.vectorize(lambda m: pair_angle(node, m), otypes=[object, object])(n)
        found.append((pairs[0], pairs[1]))
    return found


def floor(node: Node) -> int:
    """The carrier's level at the content -Gamma, the swap's floor."""
    return int(
        np.asarray(
            volume.volume_of(node.gamma, np.array([-node.gamma], dtype=object)), dtype=object
        ).reshape(-1)[0]
    )
