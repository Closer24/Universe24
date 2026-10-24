"""The share (ALGEBRA.md #the-count-is-the-records-share; #the-conserved-form): the count is the record's weighted share at every Node, a reading of the record and no line of its own, in the current's units, e_i = [w (now_i^2 + before_i^2) - S_i now_i before_i - now_i SUM over the six Ports of R_ij before_j] div (2 p_i^2 G^2) at the paces of the read, the conserved form's term at the Node with the Node's weight 1 / p_i^2, p_i = p_0^2 / Gamma the Node's pace, the composed clock twice (The clock is the Node's, the tension is the Link's; The paces compose), over the vacuum's 2 G^2, G the run's Link unit (3 den (now^2 + before^2) - num now S_6(before) in the vacuum, exactly), Rule3's integers exact at any size; in quanta over the wall W_c = 3 den T, (e + W_c div 2) div W_c by the division act, the unit every book and every body's declaration is read in. Its change over one step of Rule3 is exactly SUM_j Q_ij F_ij / G^2, the six currents at the pair the step started from (features/currents) each weighted by its Link's factor, SUM_j F_ij with no tension, less Rule3's remainder term, so nothing is kept at a Node beside the record. A frozen Node, its pace rounded to 0 at a content at or beyond the Link's zero (`paces.frozen_content`, beyond the width's reach of any body), has no share: the readers report it as not read and its well D div T as its content reading (`frozen`)."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, division_forward, form_term
from event_universe.features.read import READS, read_again
from event_universe.loader.derived import FamilyRule, quanta_records
from event_universe.readings import ports
from event_universe.records import Record, wronskian

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


def frozen(gamma: int, content: Any) -> Any:
    """Where a Node is frozen: its pace p_0^2 / Gamma rounds to 0, the content at or beyond `paces.frozen_content(gamma)` (about (Gamma div 2) ln(2 Gamma), beyond the width's reach of any body under the composed paces, ALGEBRA.md #the-paces, The paces compose), every one of its six coefficients 0 with it, so the Node is cut from its six neighbours and its share is not a number (the advisor; ALGEBRA.md #the-count-is-the-records-share, the frozen Node); a Link whose factor is 0 closes alone and its Nodes keep their shares; a reading never stops a run."""
    return paces.link_pace_of(gamma, content) == 0


def over_pace(numerator: Any, gamma: int, content: Any, unit: int, halves: int = 1) -> np.ndarray:
    """A Node term over the Node's pace squared and the Link unit squared, numerator div (2 p_i^2 G^2) by Rule3's division act, the weight 1 / p_i^2 of the conserved form (`paces.link_pace_of`), the wall `halves` times that for a numerator carried doubled (the frame's term of `share`, 2): at a frozen Node the wall is 0 and the division has no value, so the act divides there by the wall 1 and every reader reports the Node as frozen, not read (`frozen`), never the number."""
    pace = paces.link_pace_of(gamma, content)
    squares = pace * pace
    wall = halves * 2 * squares * unit * unit + (squares == 0)
    return np.asarray(division_forward(numerator, wall, 0)[0])


def share(
    pair: tuple[int, int],
    record: Record,
    wrap: Wrap,
    gamma: int,
    content: Any = 0,
    factors: tuple[Any, ...] | None = None,
    unit: int = 1,
    nodes: np.ndarray | None = None,
    as_read: Record | None = None,
) -> np.ndarray:
    """One level pair's weighted share at every Node in the current's units: the conserved form's term at the Node, w (now^2 + before^2) - S now before less now x SUM over the six Ports of R_ij x the neighbour's before by the read act, over 2 p_i^2 G^2 by the division act (`over_pace`); Rule3's integers at the paces of the read (the Node's content and its Links' factors, None no tension), exact at any size in Python's integers, computed at the Nodes `nodes` names (a mask; None: every Node where the pair holds a level, the term being 0 at a Node whose two levels are 0 whatever its neighbours hold) and 0 at every other Node. Under the rotation the share reads the level pair as the step reads it (ALGEBRA.md, The share's change is the currents; the mathematician's line, #1793 comment 5981866600 K3; the advisor's breaker; two hands): `as_read`, the line as the step reads it (the sign's phase stands on the Links, features/phase), stands in the Node term's cross product S now x before and in the Link term's six arrivals alike, the squares now^2 and before^2 as they stand: the plain form's term less now x S x (u - before) at the Node, the arrivals read from u, exact in the integers, the form of the pair so read the flat form the step conserves; None, the plain read, the level before itself, bit for bit where no family reads the sign (the plain read of a pair under the sign is no conserved form)."""
    num, den = pair
    at = (record.now != 0) | (record.before != 0) if nodes is None else nodes
    if (
        nodes is None and as_read is None
    ):  # the frame's term stands at a Node at 0 beside a Node that is not
        beside = ports(np.asarray(at, dtype=np.int64), wrap)
        at = at | np.logical_or.reduce([np.asarray(value) != 0 for value in beside])
    read = record if as_read is None else as_read
    now, before = record.now[at].astype(object), record.before[at].astype(object)
    clock, pace = paces.node_paces(gamma, paces.at_nodes(content, at))
    links = None if factors is None else tuple(paces.at_nodes(factor, at) for factor in factors)
    reads, self_coefficient, wall = coefficients(num, den, gamma, clock, pace, links, unit)
    arrived = tuple(value[at].astype(object) for value in ports(read.before, wrap))
    link = sum(read * arrival for read, arrival in zip(reads, arrived, strict=True))  # the Links' sum
    turn = self_coefficient * (read.before[at].astype(object) - before)  # the cross product's turn
    found = form_term(self_coefficient, wall, now, before) - now * (link + turn)
    halves = 1
    if (
        as_read is None
    ):  # the frame's term: the Links' products shared half and half between a Link's two ends
        arrived_now = tuple(value[at].astype(object) for value in ports(record.now, wrap))
        present = tuple(value[at] for value in ports(np.ones(record.now.shape, dtype=object), wrap))
        shared = sum(  # a Link to a Node beyond the board gives its whole term to its one Node on it
            read * (before - b_j) * (now + n_j) * on
            for read, b_j, n_j, on in zip(reads, arrived, arrived_now, present, strict=True)
        )
        found, halves = found + found - shared, 2
    everywhere = np.zeros(record.now.shape, dtype=object)
    everywhere[at] = over_pace(found, gamma, paces.at_nodes(content, at), unit, halves)
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
    as_read: Sequence[Record] | None = None,
) -> np.ndarray:
    """A family's share at every Node, its level pairs' shares summed (the form of (re, im) is the sum of the two forms), at the paces of the read, computed at the Nodes `nodes` names (`share`; None: where a level stands) and 0 elsewhere; `as_read`, the lines as the step reads them under the sign, one per line of `records` in their order (`share`), None the plain read; `weights`, one integer per line multiplying its share (None: every line at 1), the covector's form of a holder under the Lorentz form, (-3, 1, 1, 1) over its time line and its three odd lines in thirds of the time line's unit, the time line's energy negative (covector.weights)."""
    total: Any = 0
    lines = list(records)
    reads = [None] * len(lines) if as_read is None else list(as_read)
    for record, read in zip(lines, reads, strict=True):
        total = total + share(family.pair, record, wrap, gamma, content, factors, unit, nodes, read)
    return np.asarray(total)


def board_share(
    board: Lattice, index: int, direction: int = 1, at: Any = None
) -> tuple[np.ndarray, np.ndarray]:
    """A family of quanta's share at every Node of a board and its frozen Nodes (`Lattice.share_of`): each record's share at the paces of its own read in `direction` (`family_share` on the records' lines, `board.read`), summed over the records, and the frozen mask, a Node frozen where any record's read freezes it; computed at the Nodes `at` names, or over the whole board where `at` is None, and then read once per interval on the records as they stand and given again to every reader of the same records (features/read READS under the key `share`, the very record objects held, a record never written in place; the architect's second round of 2026-10-24): the same integers, read once."""
    family, gamma = board.families[index], board.world.node_clock
    key = (
        board_share,
        index,
        direction,
        gamma,
    )  # the reading named by its own function, as node.read_key names the records' reads
    taken = (board.families, board.states, *(line for state in board.states for line in state.lines))
    if at is None and (kept := read_again(key, taken)) is not None:
        return kept[0], kept[1][0]
    found: Any = 0
    cold = np.zeros(board.shape, dtype=bool)
    for record in quanta_records(board.families, index):
        content, factors = board.read(index, direction, record)
        lines = board.lines_of(index, record)
        found = found + family_share(family, lines, board.wrap, gamma, content, factors, board.unit, at)
        cold |= np.broadcast_to(frozen(gamma, content), board.shape)
    if at is None:
        READS[key] = (taken, (np.asarray(found), [cold]))
    return np.asarray(found), cold


def quanta_of(share_now: Any, wall: int, kind: type) -> np.ndarray:
    """A share in quanta at every Node, (share + W_c div 2) div W_c by Rule3's division act, W_c div 2 the rounding's origin: the reading of a share as whole quanta, in the run's kind of integers (the share itself is summed in Python's integers, exact beyond the width)."""
    origin = division_forward(wall, 2, 0)[0]
    quanta, _remainder = division_forward(np.asarray(share_now) + origin, wall, 0)
    return np.asarray(quanta, dtype=kind)


def plain_quanta(board: Lattice, index: int) -> tuple[np.ndarray, np.ndarray]:
    """A family's lay in quanta at every Node by the plain term, the lay's own support (ALGEBRA.md, The booking is the frame's, the last clause): the plain form's term at the Node, 0 where the record's two levels are 0 whatever its neighbours hold, the Links' terms at the lay's Nodes alone (`share` with the lines as their own read, `as_read`), in quanta over the record's unit (`quanta_of`) with the mask of its frozen Nodes; what a body's declared Nodes read as its standing (`Lattice.body_nodes`) and the start's count gate reads against the declared count (`lists.gate_count`), the frame's share standing at the Nodes beside the lay too and belonging to the Links, not to a declared Node (tools/frame_of.py reads the standing region the same way)."""
    family, gamma = board.families[index], board.world.node_clock
    found: Any = 0
    cold = np.zeros(board.shape, dtype=bool)
    for record in quanta_records(board.families, index):
        content, factors = board.read(index, 1, record)
        lines = board.lines_of(index, record)
        found = found + family_share(
            family, lines, board.wrap, gamma, content, factors, board.unit, None, lines
        )
        cold |= np.broadcast_to(frozen(gamma, content), board.shape)
    return quanta_of(found, board.credit.units[index], board.kind), cold


def half_action(action: int) -> int:
    """T div 2, the count's unit of a plane record on the board (the cold reader's ruling of 2026-10-22; ALGEBRA.md, The count on the board): one quantum of any plane family in any well carries the Wronskian T / 2, the charge's unit, the sign holder's own read, so a plane record's count is its charge over T / 2 and no reading of its share; one division act."""
    return int(division_forward(action, 2, 0)[0])


def charge_at(board: Lattice, index: int) -> np.ndarray:
    """A plane family's charge density at every Node, the Wronskian re_now im_before - im_now re_before summed over its records' planes (`records.wronskian`, the sign holder's own read, no new reading), signed, in the units of the levels' product."""
    total: Any = 0
    for record in quanta_records(board.families, index):
        total = total + wronskian(board.lines_of(index, record), True)
    return np.asarray(np.broadcast_to(np.asarray(total, dtype=object), board.shape), dtype=object)


def charge_of(board: Lattice, index: int) -> int:
    """A plane family's charge over the board, |SUM over the Nodes of W_i| (`charge_at`): its count of quanta in the unit T / 2 (`half_action`), the one number the count on the board reads for a plane record, free or standing in a well (the ruling of 2026-10-22; measured on the standing electron of examples/events/conserve: constant to four digits over 17 intervals while the share in the free unit beat 1.43 to 1.87)."""
    return abs(int(charge_at(board, index).sum(dtype=object)))


def charged(family: FamilyRule) -> bool:
    """Whether a family's count on the board is its charge (the ruling of 2026-10-22): a plane family at a pair with a rotation, num other than den, whose quantum carries the Wronskian T / 2; a massless plane pair turns not and its Wronskian is 0 by construction, so its count stays the share's, as a family of real lines' does."""
    return family.plane and family.pair[0] != family.pair[1]


def by_charge(board: Lattice, index: int) -> bool:
    """Whether a family's count on the board is read as its charge: a plane family at a pair with a rotation (`charged`) whose record carries a sense, its Wronskian other than 0 over the board (`charge_of`); a plane record laid without its quadrature, its Wronskian 0 at every Node (a packet with no `sense` declared, the clicks world's electron), is neutral, two real lines, and is counted as they are, by its share."""
    return charged(board.families[index]) and charge_of(board, index) > 0


def count_read(board: Lattice, index: int, total: int | None, unit: int) -> tuple[int | None, int]:
    """The total and the unit the count on the board is read from (`credit.counted`): a charged plane record's charge over T div 2 (`by_charge`, `charge_of`, `half_action`, the ruling of 2026-10-22), another record's share `total` over its own unit `unit` (W_rec, `credit.record_unit`)."""
    if by_charge(board, index):
        return charge_of(board, index), half_action(board.world.quantum_action)
    return total, unit
