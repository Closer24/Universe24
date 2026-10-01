"""The share (ALGEBRA.md #the-count-is-the-records-share): the count is the record's weighted share at every Node, a reading of the record and no line of its own, in the current's units, e_i = 3 [w (now_i^2 + before_i^2) - S_i now_i before_i] div (SUM over the six Ports of p_a(i, j)^2) - num now_i S_6(before)_i at the paces of the read, the conserved form's Node term over twice the mean of the six Links' paces squared (2 SUM_a p_a^2 where each axis's two Links share a pace), Rule3's integers exact at any size; in quanta over the wall W_c = 3 den T, (e + W_c div 2) div W_c by the division act, the unit every book and every body's declaration is read in. Its change over one step of Rule3 is exactly SUM_j F_ij, the six currents at the pair the step started from (features/currents), plus the paces' anisotropy term and Rule3's remainder term, so nothing is kept at a Node beside the record. A frozen Node, every Link pace 0, has no share: the readers report it as not read and its well D div T as its content reading (`frozen`)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap
from event_universe.core.rule3 import NO_READ, coefficients, form_term, link_paces, rule3
from event_universe.loader.derived import FamilyRule
from event_universe.node import Record, ports


def squared_paces(gamma: int, links: tuple[Any, ...]) -> Any:
    """The sum of the six Links' paces squared at every Node, SUM over the Ports of p_a(i, j)^2 with p_a(i, j) = Gamma - 2 c_i - t_a(i, j), 2 SUM_a p_a^2 where each axis's two Links share a pace (ALGEBRA.md #the-paces)."""
    squares: Any = 0
    for pace in link_paces(gamma, links):
        squares = squares + pace * pace
    return squares


def frozen(gamma: int, links: tuple[Any, ...]) -> Any:
    """Where a Node is frozen: every one of its six Links at the pace 0, SUM of their squares 0, the content exactly Gamma div 2 with no tension, so the Node is cut from its six neighbours and its share is not a number (the advisor, #1563 comment 5923771616; ALGEBRA.md #the-count-is-the-records-share, the frozen Node); a Node with an open Link keeps its share; a reading never stops a run."""
    return squared_paces(gamma, links) == 0


def over_paces(numerator: Any, gamma: int, links: tuple[Any, ...]) -> np.ndarray:
    """A Node term over the Links' paces squared, 3 x numerator div (SUM over the six Ports of p_a(i, j)^2) by Rule3's division act: numerator div 2 p^2 where the six paces are one; at a frozen Node the wall is 0 and the division has no value, so the act divides there by the wall 1 and every reader reports the Node as frozen, not read (`frozen`), never the number."""
    squares = squared_paces(gamma, links)
    wall = squares + (squares == 0)
    return np.asarray(rule3(NO_READ, NO_READ, 3, wall, numerator, 0, 0)[0])


def share(
    pair: tuple[int, int],
    record: Record,
    wrap: Wrap,
    gamma: int,
    content: Any = 0,
    links: tuple[Any, ...] | None = None,
) -> np.ndarray:
    """One level pair's weighted share at every Node in the current's units: the conserved form's Node term w (now^2 + before^2) - S now before over the Links' paces squared (`over_paces`), less the plain Link term num now S_6(before) by the read act; Rule3's integers at the paces of the read (the Node's content and its six Links' contents, None no tension), exact at any size."""
    num, den = pair
    now, before = record.now.astype(object), record.before.astype(object)
    reads, self_coefficient, wall = coefficients(num, den, gamma, content, links, True)
    weighted = over_paces(
        form_term(self_coefficient, wall, now, before),
        gamma,
        link_contents_of(content, links, len(reads)),
    )
    arrived = tuple(value.astype(object) for value in ports(record.before, wrap))
    link = rule3((num * now,) * len(reads), arrived, 0, 1, 0, 0, 0)[0]
    return np.asarray(weighted - link)


def link_contents_of(content: Any, links: tuple[Any, ...] | None, count: int) -> tuple[Any, ...]:
    """The six Links' contents as the rule reads them: `links` as given, or the Node's content twice on every Link where none is given (no tension)."""
    return (content + content,) * count if links is None else links


def family_share(
    family: FamilyRule,
    records: Iterable[Record],
    wrap: Wrap,
    gamma: int,
    content: Any = 0,
    links: tuple[Any, ...] | None = None,
) -> np.ndarray:
    """A family's share at every Node, its level pairs' shares summed (the form of (re, im) is the sum of the two forms), at the paces of the read."""
    total: Any = 0
    for record in records:
        total = total + share(family.pair, record, wrap, gamma, content, links)
    return np.asarray(total)


def quanta_of(share_now: Any, wall: int, kind: type) -> np.ndarray:
    """A share in quanta at every Node, (share + W_c div 2) div W_c by Rule3's division act, W_c div 2 the rounding's origin: the reading of a share as whole quanta, in the run's kind of integers (the share itself is summed in Python's integers, exact beyond the width)."""
    origin = rule3(NO_READ, NO_READ, 1, 2, wall, 0, 0)[0]
    quanta, _remainder = rule3(NO_READ, NO_READ, 1, wall, 0, 0, np.asarray(share_now) + origin)
    return np.asarray(quanta, dtype=kind)
