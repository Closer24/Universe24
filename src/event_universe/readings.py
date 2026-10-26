"""The Node's readings at an interval's start, each a function of the Node's state at every Node alike: the content (the carrier's level), the (cos, sin) pair at a count along the one orbit, the swap's floor; the Link's readings are links.py's (the former link_factors, frames, centred_count and link_phases kept by name) and the records' share is gram.share."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import paces
from event_universe.core.rule3 import remainder
from event_universe.features import phase, volume
from event_universe.rows import CARRIER

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
    """The integer (cos, sin) pair at the count n along the one orbit from the seed (features/phase): the orbit a table built as far as the counts reach and stored to the half turn H alone, the first count where the cosine stops falling (254,469 at Gamma 1,000, 81 pi Gamma to the integer), every count beyond read by the orbit's own symmetry, the pair at 2 H - n with the sine negated, modulo the full turn 2 H (the Boss's word of 2026-10-26, 11:33 UTC, 6414995372, under the owner's delegation of 08:3x: the table of the heavy quartet legs' beat reached 12,581,080 pairs and killed the run; the walked orbit beyond H kept by name, the mirror's read differing from it by the rounding of each step alone)."""
    n = int(n)
    s = 1 if n >= 0 else -1
    n = abs(n)
    while node.orbit_half is None and len(node.orbit) <= n:
        c, sn = node.orbit_lines[-1]
        c, sn = phase.act(c, node.gamma, 1), phase.act(sn, node.gamma, 1)
        if int(c[0]) >= node.orbit[-1][0] and len(node.orbit) > 1:
            node.orbit_half = len(node.orbit) - 1
            break
        node.orbit_lines = [(c, sn)]
        node.orbit.append((int(c[0]), int(sn[0])))
    if node.orbit_half is not None and n > node.orbit_half:
        n = remainder(n, node.orbit_half + node.orbit_half)
        if n > node.orbit_half:
            n, s = node.orbit_half + node.orbit_half - n, -s
    c_, sn_ = node.orbit[n]
    return c_, s * sn_


def floor(node: Node) -> int:
    """The carrier's level at the content -Gamma, the swap's floor."""
    return int(
        np.asarray(
            volume.volume_of(node.gamma, np.array([-node.gamma], dtype=object)), dtype=object
        ).reshape(-1)[0]
    )
