"""The lay (ALGEBRA.md #the-counts-line, the lay and the wall; #the-paces, the sign is the rotation sense): every family's count and sense laid once at the first act from the weighted share of its two level pairs and from the Wronskian's share at the paces of the read, by Rule3's division act at the count's wall W_c, exact in integers of any size."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.ports import Wrap
from event_universe.core.rule3 import ISOTROPIC, NO_READ, coefficients, form_term, link_paces, rule3
from event_universe.loader.derived import FamilyRule, count_wall
from event_universe.node import Record, axis_sums, wronskian


def squared_paces(gamma: int, content: Any, axis: tuple[Any, ...]) -> Any:
    """The sum of the three Link paces' squares at every Node, SUM_a p_a^2 with p_a = Gamma - 2 c - t_a (ALGEBRA.md #the-paces)."""
    paces = link_paces(gamma, content, axis)
    return paces[0] * paces[0] + paces[1] * paces[1] + paces[2] * paces[2]


def over_paces(numerator: Any, gamma: int, content: Any, axis: tuple[Any, ...]) -> np.ndarray:
    """A Node term over the Link's pace squared, 3 x numerator div (2 SUM_a p_a^2) by Rule3's division act: numerator div 2 p^2 where the three paces are one (ALGEBRA.md #the-counts-line, the lay and the wall)."""
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
    """The weighted share at every Node in the current's units (ALGEBRA.md #the-counts-line, the lay and the wall): the conserved form's Node term w (now^2 + before^2) - S now before over the Link's pace squared (`over_paces`), less the plain Link term num now S_6(before) by the read act; Rule3's integers at the paces of the read, exact at any size."""
    num, den = pair
    now, before = record.now.astype(object), record.before.astype(object)
    _reads, self_coefficient, wall = coefficients(num, den, gamma, content, axis, True)
    weighted = over_paces(form_term(self_coefficient, wall, now, before), gamma, content, axis)
    sums = tuple(value.astype(object) for value in axis_sums(record.before, wrap))
    link = rule3((num * now,) * 3, sums, 0, 1, 0, 0, 0)[0]
    return np.asarray(weighted - link)


def sense_share(
    pair: tuple[int, int],
    record: Record,
    second: Record,
    gamma: int,
    content: Any = 0,
    axis: tuple[Any, ...] = ISOTROPIC,
) -> np.ndarray:
    """The sense's share at every Node in the current's units (ALGEBRA.md #the-paces, the sign is the rotation sense): the Wronskian of the two level pairs W_i = re_now im_before - im_now re_before times the rule's wall w over the Link's pace squared (`over_paces`), whose change over one interval is exactly the sense's current."""
    num, den = pair
    _reads, _self, wall = coefficients(num, den, gamma, content, axis, True)
    return over_paces(wall * wronskian(record, second).astype(object), gamma, content, axis)


def laid(share_now: np.ndarray, wall: int) -> tuple[np.ndarray, np.ndarray]:
    """W_c c + r = share + W_c div 2 at every Node by Rule3's division act, W_c div 2 the remainder's origin (ALGEBRA.md #the-counts-line, the lay and the wall)."""
    origin = rule3(NO_READ, NO_READ, 1, 2, wall, 0, 0)[0]  # W_c div 2, the division act
    counts, remainder = rule3(NO_READ, NO_READ, 1, wall, 0, 0, share_now + origin)
    return np.asarray(counts, dtype=np.int64), np.asarray(remainder, dtype=np.int64)


def lay(
    family: FamilyRule,
    records: tuple[Record, ...],
    action: int,
    wrap: Wrap,
    gamma: int,
    content: Any = 0,
    axis: tuple[Any, ...] = ISOTROPIC,
) -> tuple[np.ndarray, np.ndarray]:
    """The lay, once at the first act (ALGEBRA.md #the-counts-line): the count from the weighted share of the record's level pairs summed (the form of (re, im) is the sum of the two forms), at the paces of the read."""
    total = sum(share(family.pair, record, wrap, gamma, content, axis) for record in records)
    return laid(np.asarray(total), count_wall(family, action))


def lay_sense(
    family: FamilyRule,
    record: Record,
    second: Record,
    action: int,
    gamma: int,
    content: Any = 0,
    axis: tuple[Any, ...] = ISOTROPIC,
) -> tuple[np.ndarray, np.ndarray]:
    """The sense's lay, once at the first act beside the count's: the sense from the sense's share at the count's wall W_c."""
    return laid(
        sense_share(family.pair, record, second, gamma, content, axis), count_wall(family, action)
    )
