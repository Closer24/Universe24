"""The share (ALGEBRA.md #the-count-is-the-records-share): the count is the record's weighted share at every Node, a reading of the record and no line of its own, in the current's units, e_i = 3 [w (now_i^2 + before_i^2) - S_i now_i before_i] div (2 SUM_a p_a^2) - num now_i S_6(before)_i at the paces of the read, Rule3's integers exact at any size; in quanta over the wall W_c = 3 den T, (e + W_c div 2) div W_c by the division act, the unit every book and every body's declaration is read in. Its change over one step of Rule3 is exactly SUM_j F_ij, the six currents at the pair the step started from (features/currents), so nothing is kept at a Node beside the record."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap
from event_universe.core.rule3 import ISOTROPIC, NO_READ, coefficients, form_term, link_paces, rule3
from event_universe.loader.derived import FamilyRule
from event_universe.node import Record, axis_sums


def squared_paces(gamma: int, content: Any, axis: tuple[Any, ...]) -> Any:
    """The sum of the three Link paces' squares at every Node, SUM_a p_a^2 with p_a = Gamma - 2 c - t_a (ALGEBRA.md #the-paces)."""
    paces = link_paces(gamma, content, axis)
    return paces[0] * paces[0] + paces[1] * paces[1] + paces[2] * paces[2]


def over_paces(numerator: Any, gamma: int, content: Any, axis: tuple[Any, ...]) -> np.ndarray:
    """A Node term over the Link's pace squared, 3 x numerator div (2 SUM_a p_a^2) by Rule3's division act: numerator div 2 p^2 where the three paces are one."""
    return np.asarray(
        rule3(NO_READ, NO_READ, len(axis), 2 * squared_paces(gamma, content, axis), numerator, 0, 0)[0]
    )


def share(
    pair: tuple[int, int],
    record: Record,
    wrap: Wrap,
    gamma: int,
    content: Any = 0,
    axis: tuple[Any, ...] = ISOTROPIC,
) -> np.ndarray:
    """One level pair's weighted share at every Node in the current's units: the conserved form's Node term w (now^2 + before^2) - S now before over the Link's pace squared (`over_paces`), less the plain Link term num now S_6(before) by the read act; Rule3's integers at the paces of the read, exact at any size."""
    num, den = pair
    now, before = record.now.astype(object), record.before.astype(object)
    _reads, self_coefficient, wall = coefficients(num, den, gamma, content, axis, True)
    weighted = over_paces(form_term(self_coefficient, wall, now, before), gamma, content, axis)
    sums = tuple(value.astype(object) for value in axis_sums(record.before, wrap))
    link = rule3((num * now,) * 3, sums, 0, 1, 0, 0, 0)[0]
    return np.asarray(weighted - link)


def family_share(
    family: FamilyRule,
    records: Iterable[Record],
    wrap: Wrap,
    gamma: int,
    content: Any = 0,
    axis: tuple[Any, ...] = ISOTROPIC,
) -> np.ndarray:
    """A family's share at every Node, its level pairs' shares summed (the form of (re, im) is the sum of the two forms), at the paces of the read."""
    total: Any = 0
    for record in records:
        total = total + share(family.pair, record, wrap, gamma, content, axis)
    return np.asarray(total)


def quanta_of(share_now: Any, wall: int, kind: type) -> np.ndarray:
    """A share in quanta at every Node, (share + W_c div 2) div W_c by Rule3's division act, W_c div 2 the rounding's origin: the reading of a share as whole quanta, in the run's kind of integers (the share itself is summed in Python's integers, exact beyond the width)."""
    origin = rule3(NO_READ, NO_READ, 1, 2, wall, 0, 0)[0]
    quanta, _remainder = rule3(NO_READ, NO_READ, 1, wall, 0, 0, np.asarray(share_now) + origin)
    return np.asarray(quanta, dtype=kind)
