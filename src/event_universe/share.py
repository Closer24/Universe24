"""The share (ALGEBRA.md #the-count-is-the-records-share; #the-conserved-form): the count is the record's weighted share at every Node, a reading of the record and no line of its own, in the current's units, e_i = [w (now_i^2 + before_i^2) - S_i now_i before_i - now_i SUM over the six Ports of R_ij before_j] div (2 p_i^2 G^2) at the paces of the read, the conserved form's term at the Node with the Node's weight 1 / p_i^2, p_i = p_0^2 / Gamma the Node's pace, the composed clock twice (The clock is the Node's, the tension is the Link's; The paces compose), over the vacuum's 2 G^2, G the run's Link unit (3 den (now^2 + before^2) - num now S_6(before) in the vacuum, exactly), Rule3's integers exact at any size; in quanta over the wall W_c = 3 den T, (e + W_c div 2) div W_c by the division act, the unit every book and every body's declaration is read in. Its change over one step of Rule3 is exactly SUM_j Q_ij F_ij / G^2, the six currents at the pair the step started from (features/currents) each weighted by its Link's factor, SUM_j F_ij with no tension, less Rule3's remainder term, so nothing is kept at a Node beside the record. A frozen Node, its pace rounded to 0 at a content at or beyond the Link's zero (`paces.frozen_content`, beyond the width's reach of any body), has no share: the readers report it as not read and its well D div T as its content reading (`frozen`)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import NO_READ, coefficients, form_term, rule3
from event_universe.loader.derived import FamilyRule
from event_universe.node import Record, ports


def frozen(gamma: int, content: Any) -> Any:
    """Where a Node is frozen: its pace p_0^2 / Gamma rounds to 0, the content at or beyond `paces.frozen_content(gamma)` (about (Gamma div 2) ln(2 Gamma), beyond the width's reach of any body under the composed paces, ALGEBRA.md #the-paces, The paces compose), every one of its six coefficients 0 with it, so the Node is cut from its six neighbours and its share is not a number (the advisor; ALGEBRA.md #the-count-is-the-records-share, the frozen Node); a Link whose factor is 0 closes alone and its Nodes keep their shares; a reading never stops a run."""
    return paces.link_pace_of(gamma, content) == 0


def over_pace(numerator: Any, gamma: int, content: Any, unit: int) -> np.ndarray:
    """A Node term over the Node's pace squared and the Link unit squared, numerator div (2 p_i^2 G^2) by Rule3's division act, the weight 1 / p_i^2 of the conserved form (`paces.link_pace_of`): at a frozen Node the wall is 0 and the division has no value, so the act divides there by the wall 1 and every reader reports the Node as frozen, not read (`frozen`), never the number."""
    pace = paces.link_pace_of(gamma, content)
    squares = pace * pace
    wall = 2 * squares * unit * unit + (squares == 0)
    return np.asarray(rule3(NO_READ, NO_READ, 1, wall, numerator, 0, 0)[0])


def share(
    pair: tuple[int, int],
    record: Record,
    wrap: Wrap,
    gamma: int,
    content: Any = 0,
    factors: tuple[Any, ...] | None = None,
    unit: int = 1,
    nodes: np.ndarray | None = None,
) -> np.ndarray:
    """One level pair's weighted share at every Node in the current's units: the conserved form's term at the Node, w (now^2 + before^2) - S now before less now x SUM over the six Ports of R_ij x the neighbour's before by the read act, over 2 p_i^2 G^2 by the division act (`over_pace`); Rule3's integers at the paces of the read (the Node's content and its Links' factors, None no tension), exact at any size in Python's integers, computed at the Nodes `nodes` names (a mask; None: every Node where the pair holds a level, the term being 0 at a Node whose two levels are 0 whatever its neighbours hold) and 0 at every other Node."""
    num, den = pair
    at = (record.now != 0) | (record.before != 0) if nodes is None else nodes
    now, before = record.now[at].astype(object), record.before[at].astype(object)
    clock, pace = paces.node_paces(gamma, paces.at_nodes(content, at))
    links = None if factors is None else tuple(paces.at_nodes(factor, at) for factor in factors)
    reads, self_coefficient, wall = coefficients(num, den, gamma, clock, pace, links, unit)
    arrived = tuple(value[at].astype(object) for value in ports(record.before, wrap))
    link = rule3(reads, arrived, 0, 1, 0, 0, 0)[0]
    found = form_term(self_coefficient, wall, now, before) - now * link
    everywhere = np.zeros(record.now.shape, dtype=object)
    everywhere[at] = over_pace(found, gamma, paces.at_nodes(content, at), unit)
    return everywhere


def family_share(
    family: FamilyRule,
    records: Iterable[Record],
    wrap: Wrap,
    gamma: int,
    content: Any = 0,
    factors: tuple[Any, ...] | None = None,
    unit: int = 1,
    nodes: np.ndarray | None = None,
) -> np.ndarray:
    """A family's share at every Node, its level pairs' shares summed (the form of (re, im) is the sum of the two forms), at the paces of the read, computed at the Nodes `nodes` names (`share`; None: where a level stands) and 0 elsewhere."""
    total: Any = 0
    for record in records:
        total = total + share(family.pair, record, wrap, gamma, content, factors, unit, nodes)
    return np.asarray(total)


def quanta_of(share_now: Any, wall: int, kind: type) -> np.ndarray:
    """A share in quanta at every Node, (share + W_c div 2) div W_c by Rule3's division act, W_c div 2 the rounding's origin: the reading of a share as whole quanta, in the run's kind of integers (the share itself is summed in Python's integers, exact beyond the width)."""
    origin = rule3(NO_READ, NO_READ, 1, 2, wall, 0, 0)[0]
    quanta, _remainder = rule3(NO_READ, NO_READ, 1, wall, 0, 0, np.asarray(share_now) + origin)
    return np.asarray(quanta, dtype=kind)
