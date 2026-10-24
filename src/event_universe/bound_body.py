"""The bound body's click is the Node's act (ALGEBRA.md, The board reads itself, the dated clause on the owner's sentence of 2026-10-24, 16:45 UTC, in his words of the point 10, the Node alone must understand it is in a bound body and click, and that must happen by itself): a record standing at a Node at a whole quantum of its own unit through one period of its beat is a bound body; its window one period; at the close the Node reads the light at it and its six Ports, the floor of the share over the record's unit, the remainder the whether (divided by the unit once), the hole the board's own; the credit the record's. Here the period (`period_of`), the records the Nodes can be in (`body_records`) and the bodies whose window closes with the click met (`bodies_closing`); the hole, the quantum into the record and the credit in `meeting_board.closed`."""

from __future__ import annotations

from functools import cache
from math import gcd
from typing import TYPE_CHECKING

import numpy as np

from event_universe import registry, share
from event_universe.core.rule3 import division_forward
from event_universe.digits import at_origin, frame_of, read_of
from event_universe.features.click import Refused, drawn_from
from event_universe.loader.keys import Node
from event_universe.reports import REFUSED_ORIGIN

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


@cache
def period_of(pair: tuple[int, int]) -> int:
    """One period of a record's beat in whole intervals, from its rotation alone (ALGEBRA.md, The board reads itself, the bound body's clause of 2026-10-24, the owner's sentence of 16:45 UTC: a record standing at a Node at a whole quantum of its own unit through one period of its beat is a bound body, its window one period): the rotation cos omega = num / den turns the record's lines by omega per interval, and the period is the first count of intervals P at which the turn completes, read on the integers by the Chebyshev recurrence of the sine's sign, S_0 = 0, S_1 = 1, S_(t+1) = 2 num S_t - den^2 S_(t-1) (the sign of sin(t omega), the pair reduced by their gcd at every step so the integers stay small), P the first t with S_(t-1) < 0 <= S_t, computed once per pair (`functools.cache`: a number of the pair alone, asked at every close for every record); the trial's ceiling of 2 pi over omega bit for bit, no transcendental function; the massless pair never turns and is no body, P = 0."""
    num, den = pair
    if num == den:
        return 0
    before, now, count = 0, 1, 1
    while True:
        before, now, count = now, 2 * num * now - den * den * before, count + 1
        common = gcd(abs(before), abs(now)) or 1
        before, now = (
            int(division_forward(before, common, 0)[0]),
            int(division_forward(now, common, 0)[0]),
        )  # the pair reduced, the signs kept (the floor exact: common divides both)
        if before < 0 <= now:
            return count


def body_records(board: Lattice) -> list[tuple[int, int]]:
    """The records of the charged families standing on the board, (family, record) in order, each with its standing count over the Nodes made at first sight (`Lattice.standing`, zeros): the bodies the Nodes can be in."""
    found = []
    for k in board.order:
        if share.charged(board.families[k]):
            for r in registry.quanta_records(board.families, board.states, k):
                board.standing.setdefault((k, r), np.zeros(board.shape, dtype=np.int64))
                found.append((k, r))
    return found


def bodies_closing(
    board: Lattice,
    light: np.ndarray,
    frozen: np.ndarray,
    born: set[Node],
    refusals: list[tuple[Node, str, int, int]],
) -> list[tuple[int, int, Node, int]]:
    """The bound bodies whose window closes at this close and whose click is met, read on the interval's start as every meeting is (ALGEBRA.md, The board reads itself, the bound body's clause of 2026-10-24 on the owner's sentence of 16:45 UTC): a record of a charged family standing at a Node at a whole quantum of its own unit (`share.family_share` of the record over its unit, the Node not frozen) through one period of its beat (`period_of`, the count kept per record at every Node, `Lattice.standing`, reset where it stops standing) is a bound body there; at the period's close the Node reads the light at it and its six Ports, the floor of the seed family's share at the Node over the record's unit, one whole quantum met, else the remainder the whether drawn by the digits' read of the Node and its six Links divided by the unit once (`read_of`, `drawn_from`); the read's refusals by name are logged lines; a Node the seed births at this close is the birth's. Returns (family, record, Node, the record's unit) per click met; the hole and the credit follow in `closed`."""
    found: list[tuple[int, int, Node, int]] = []
    gamma, unit = board.world.node_clock, board.unit
    for k, r in body_records(board):
        period = period_of(board.families[k].pair)
        if period == 0:
            continue
        unit_k = board.credit.units[k]
        if (
            int(np.asarray(board.share_of(k)[0], dtype=object).max()) < unit_k
        ):  # the family's share, read once per interval and given again: no record of it stands at a whole quantum anywhere, nothing to read
            board.standing[(k, r)] = np.zeros(board.shape, dtype=np.int64)
            continue
        content, factors = board.read(k, 1, r)
        own = share.family_share(board.families[k], board.lines_of(k, r), gamma, content, factors, unit)
        standing = np.where(
            (np.asarray(own, dtype=object) >= unit_k) & ~frozen, board.standing[(k, r)] + 1, 0
        )
        closing = standing >= period
        board.standing[(k, r)] = np.where(closing, 0, standing).astype(np.int64)
        for where in zip(*np.nonzero(closing), strict=True):
            at = (int(where[0]), int(where[1]), int(where[2]))
            if at in born:
                continue
            whole, rest = division_forward(int(light[at]), unit_k, 0)
            met = whole >= 1
            if not met and rest > 0:
                label = f"the body {[k, r]} at {list(at)}'s read of itself and its Links at the interval {board.interval}"
                reads = [
                    (index, frame_of(at, board.shape, board.world.periodic)) for index in board.order
                ]
                if at_origin(board, reads):
                    refusals.append((at, REFUSED_ORIGIN, board.half_wall(k), board.half_wall(k)))
                    continue
                try:
                    number = read_of(board, reads, label)
                    met = drawn_from(number, [rest, unit_k - rest], label, True)[0] == 0
                except Refused as named:
                    refusals.append((at, named.cause, named.amount, named.bound))
                    continue
            if met:
                found.append((k, r, at, unit_k))
    return found
