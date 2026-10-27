"""The file's one reader (R6 of the readings' map, 2026-10-26, under the owner's word of 12:2x UTC): what the Node reads of the two files at its content before it adds, each a function of the Node's state at every Node alike: the content (the carrier's level), the two paces, the frozen mask, the (cos, sin) pair at a count along the one orbit, the swap's floor, Rule3's integers at a pair and at a row (the former node.rule, node.rule_of and node.content kept by name) and the mean wall of the carrier's two levels (the former Interval.mean_wall); the Link's readings are links.py's and the records' share is gram.share."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import rates, rule3
from event_universe.core.rule3 import remainder
from event_universe.core.spokes import SPOKES
from event_universe.features import standard, stretch
from event_universe.trains import REGULATOR, Gear, Train

if TYPE_CHECKING:
    from event_universe.clock import Clock


def rates_of(node: Clock, content: Any) -> tuple[Any, Any]:
    """The Node's two paces from its content, the clock p_0 and the Link's pace p_i (X2: paces(content)), one reading."""
    return rates.rate_of(node.full_rate, content), rates.mesh_rate_of(node.full_rate, content)


def stopped_of(node: Clock, content: Any) -> Any:
    """The frozen mask from the content (BH-S1): the Nodes whose Link pace reads 0 at the interval's start, one reading for the interval, the close and the writer."""
    pace = np.asarray(rates_of(node, content)[1], dtype=object)
    return pace == 0 if np.ndim(pace) else np.zeros(node.size, dtype=bool)


def load(node: Clock) -> Any:
    """The content at every Node, the level of the carrier's time line."""
    return np.asarray(stretch.load_of(node.full_rate, node.train(REGULATOR).gears[0].now), dtype=object)


def standard_angle(node: Clock, n: Any) -> tuple[int, int]:
    """The integer (cos, sin) pair at the count n along the one orbit from the seed (features/phase): the orbit a table built as far as the counts reach and stored to the half turn H alone, the first count where the cosine stops falling (3,142 at Gamma 1,000, pi Gamma to the integer; 254,469, the deepest cosine over 400,000 counts, the former docstring's number, H-Confirm-Build-25), every count beyond read by the orbit's own symmetry, the pair at 2 H - n with the sine negated, modulo the full turn 2 H (the Boss's word of 2026-10-26, 11:33 UTC, 6414995372, under the owner's delegation of 08:3x: the table of the heavy quartet legs' beat reached 12,581,080 pairs and killed the run; the walked orbit beyond H kept by name, the mirror's read differing from it by the rounding of each step alone)."""
    n = int(n)
    s = 1 if n >= 0 else -1
    n = abs(n)
    while node.circuit_half is None and len(node.circuit) <= n:
        c, sn = node.circuit_gears[-1]
        c, sn = standard.act(c, node.full_rate, 1), standard.act(sn, node.full_rate, 1)
        if int(c[0]) >= node.circuit[-1][0] and len(node.circuit) > 1:
            node.circuit_half = len(node.circuit) - 1
            break
        node.circuit_gears = [(c, sn)]
        node.circuit.append((int(c[0]), int(sn[0])))
    if node.circuit_half is not None and n > node.circuit_half:
        n = remainder(n, node.circuit_half + node.circuit_half)
        if n > node.circuit_half:
            n, s = node.circuit_half + node.circuit_half - n, -s
    c_, sn_ = node.circuit[n]
    return c_, s * sn_


def gearing(node: Clock, pair: tuple[int, int], c: Any, factors: tuple[Any, ...]) -> rule3.Gearing:
    """Rule3's integers of a pair at the Node's paces from the content, in the carrier's unit (PM-S1)."""
    clock, pace = rates_of(node, c)
    return rule3.gearing(pair[0], pair[1], node.full_rate, clock, pace, factors, node.G)


def gearing_of(node: Clock, r: Train, c: Any, factors: tuple[Any, ...]) -> rule3.Gearing:
    """A row's rule: Rule3's integers at its pair and the Node's paces, or, for the row with its own wall, no Links and the own weight 2 w (next = 2 now - before + the write inside the division)."""
    if r.teeth is not None:
        return rule3.Gearing(tuple(0 for _ in range(SPOKES)), r.teeth + r.teeth, r.teeth, 0)
    assert r.ratio is not None
    return gearing(node, r.ratio, c, factors)


def mean_teeth(node: Clock, line: Gear) -> Any:
    """The mean wall (w div 2)(X_before + X_now) of the carrier's time line as given: the rows' own before the carrier's act for the kick and the lays, the act's at its end for the riding lines' divisions."""
    return rule3.mean_teeth_of(node.teeth, line.before, line.now)


def bottom(node: Clock) -> int:
    """The carrier's level at the content -Gamma, the swap's floor."""
    return int(
        np.asarray(
            stretch.stretch_of(node.full_rate, np.array([-node.full_rate], dtype=object)), dtype=object
        ).reshape(-1)[0]
    )
