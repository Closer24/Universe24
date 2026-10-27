"""The file's one reader (R6 of the readings' map, 2026-10-26, under the owner's word of 12:2x UTC): what the Node reads of the two files at its content before it adds, each a function of the Node's state at every Node alike: the content (the carrier's level), the two paces, the frozen mask, the (cos, sin) pair at a count along the one orbit, the swap's floor, Rule3's integers at a pair and at a row (the former node.rule, node.rule_of and node.content kept by name) and the mean wall of the carrier's two levels (the former Interval.mean_wall); the Link's readings are links.py's and the records' share is gram.share."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import paces, rule3
from event_universe.core.ports import PORTS
from event_universe.core.rule3 import half, remainder
from event_universe.features import phase, volume
from event_universe.rows import CARRIER, QUARTET, Line, Row

if TYPE_CHECKING:
    from event_universe.node import Node


def paces_of(node: Node, content: Any) -> tuple[Any, Any]:
    """The Node's two paces from its content, the clock p_0 and the Link's pace p_i (X2: paces(content)), one reading; the carried pair of the interval where one stands (the blind build)."""
    found = getattr(node, "paces_now", None)
    if found is not None:
        return found
    return paces.clock_of(node.gamma, content), paces.link_pace_of(node.gamma, content)


def carried_paces(node: Node, content: Any, direction: int) -> tuple[Any, Any]:
    """The blind build of the toy's carried paces: the clock N(c) = q_0 Gamma^2 + r_0 and the Link pace p_0^2 = q Gamma + r, each one carried division of the Node with its remainder kept per Node across intervals, advanced once per interval forward and inverted once backward (acts.divide at -1 with the same numerator)."""
    from event_universe.core import acts
    g = node.gamma
    numerator = np.asarray(paces.numerator_of(g, content), dtype=object)
    p0, node.carry0 = acts.divide(numerator, g * g, node.carry0, direction)
    pi, node.carry1 = acts.divide(p0 * p0, g, node.carry1, direction)
    node.paces_now = (p0, pi)
    return node.paces_now


def frozen_of(node: Node, content: Any) -> Any:
    """The frozen mask from the content (BH-S1): the Nodes whose Link pace reads 0 at the interval's start, one reading for the interval, the close and the writer."""
    pace = np.asarray(paces_of(node, content)[1], dtype=object)
    return pace == 0 if np.ndim(pace) else np.zeros(node.shape, dtype=bool)


def content(node: Node) -> Any:
    """The content at every Node, the level of the carrier's time line."""
    return np.asarray(volume.level_of(node.gamma, node.row(CARRIER).lines[0].now), dtype=object)


def pair_angle(node: Node, n: Any) -> tuple[int, int]:
    """The integer (cos, sin) pair at the count n along the one orbit from the seed (features/phase): the orbit a table built as far as the counts reach and stored to the half turn H alone, the first count where the cosine stops falling (3,142 at Gamma 1,000, pi Gamma to the integer; 254,469, the deepest cosine over 400,000 counts, the former docstring's number, H-Confirm-Build-25), every count beyond read by the orbit's own symmetry, the pair at 2 H - n with the sine negated, modulo the full turn 2 H (the Boss's word of 2026-10-26, 11:33 UTC, 6414995372, under the owner's delegation of 08:3x: the table of the heavy quartet legs' beat reached 12,581,080 pairs and killed the run; the walked orbit beyond H kept by name, the mirror's read differing from it by the rounding of each step alone)."""
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


def scale(shape: int, gamma: Any) -> Any:
    """The row's scale on the rule and the walls (the former gram.scale kept by name, a reading of the row's shape alone): 2 x 6 Gamma for the quartet, so that the term's coefficient R / (2 Gamma) summed over the six Ports enters as the integer SUM_j R_j (SR-S3, sr1's form); 1 for every other shape."""
    return (PORTS + PORTS) * gamma if shape == QUARTET else 1


def rule(node: Node, pair: tuple[int, int], c: Any, factors: tuple[Any, ...]) -> rule3.Rule:
    """Rule3's integers of a pair at the Node's paces from the content, in the carrier's unit (PM-S1)."""
    clock, pace = paces_of(node, c)
    return rule3.rule_integers(pair[0], pair[1], node.gamma, clock, pace, factors, node.G)


def rule_of(node: Node, r: Row, c: Any, factors: tuple[Any, ...]) -> rule3.Rule:
    """A row's rule: Rule3's integers at its pair and the Node's paces scaled by the row's scale (gram.scale: 1 but for the quartet), or, for the row with its own wall, no Links and the own weight 2 w (next = 2 now - before + the write inside the division)."""
    if r.wall is not None:
        return rule3.Rule(tuple(0 for _ in range(PORTS)), r.wall + r.wall, r.wall, 0)
    assert r.pair is not None
    return rule3.scaled(rule(node, r.pair, c, factors), scale(r.shape, node.gamma))


def mean_wall(node: Node, line: Line) -> Any:
    """The mean wall (w div 2)(X_before + X_now) of the carrier's time line as given: the rows' own before the carrier's act for the kick and the lays, the act's at its end for the riding lines' divisions."""
    return half(node.w) * (line.before + line.now)


def floor(node: Node) -> int:
    """The carrier's level at the content -Gamma, the swap's floor."""
    return int(
        np.asarray(
            volume.volume_of(node.gamma, np.array([-node.gamma], dtype=object)), dtype=object
        ).reshape(-1)[0]
    )
