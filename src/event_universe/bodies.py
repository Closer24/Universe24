"""The bodies' ledgers and their givings (ALGEBRA.md #what-a-body-is, #the-primitives, the row "the giving"): a body is a ledger and no state of the law, its Nodes following its family's count; the giving is the count's line's click at its shell, each quantum that crosses an outer Port converted at the Node it enters with the written levels scaled so their form lays exactly one count."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

import numpy as np

from event_universe import node
from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import NO_READ, division_forward, rule3
from event_universe.features.write import carried
from event_universe.loader.derived import FamilyRule
from event_universe.loader.world import Node


@dataclass
class Body:
    """A body's ledger: its number, its family, its Nodes (a mask over the GameBoard), its declared count and its clock's last total."""

    number: int
    family: int
    nodes: np.ndarray
    declared: int
    total: int

    def corner(self) -> list[int]:
        """The lower corner of the body's Nodes, the Node its click names."""
        return [int(low) for low in np.argwhere(self.nodes).min(axis=0)]


def as_node(found: np.ndarray) -> Node:
    """A Node's address from an index row."""
    return int(found[0]), int(found[1]), int(found[2])


def following(nodes: np.ndarray, count: np.ndarray, wrap: Wrap) -> np.ndarray:
    """The body's Nodes are where its count stands (ALGEBRA.md #what-a-body-is (c)): within one Link of its Nodes, the Nodes where its family's count is not 0, the Nodes kept where it stands nowhere; the line alone moves them."""
    region = nodes.copy()
    for axis in range(3):
        for side in (1, -1):
            region |= arrival(nodes, axis, side, wrap[axis], False)
    standing = region & (count != 0)
    return standing if bool(standing.any()) else nodes


def crossings(
    nodes: np.ndarray, through: tuple[Any, ...], remainder: np.ndarray, wall: int, wrap: Wrap
) -> list[tuple[Node, Node, int, int, int]]:
    """The giving is the line's click at the shell (ALGEBRA.md #the-counts-line, the free record): at every outer Port of a body's Nodes (a Port to a Node outside them, none beyond an open face), the quanta the outward current carries out of the Node's remainder, -((r + F_p) div W_c) where that is above 0, one division per Port in the order [+X, -X, +Y, -Y, +Z, -Z]; each crossing as (the shell Node, the Node entered, the axis, the side, its quanta)."""
    addresses = np.arange(nodes.size).reshape(nodes.shape)
    found, port = [], 0
    for axis in range(3):
        for side in (1, -1):
            outer = nodes & ~arrival(nodes, axis, side, wrap[axis], True)
            entered = arrival(addresses, axis, side, wrap[axis])
            crossed = np.asarray(division_forward(remainder + np.asarray(through[port]), wall, 0)[0])
            port += 1
            for at in (as_node(row) for row in np.argwhere(outer & (crossed < 0))):
                there = as_node(np.array(np.unravel_index(int(entered[at]), nodes.shape)))
                found.append((at, there, axis, side, int(-crossed[at])))
    return found


def scaled(
    levels: tuple[np.ndarray, np.ndarray], amplitude: int, scale: int
) -> tuple[np.ndarray, np.ndarray]:
    """The two levels at the amplitude `scale`: (level x scale) div amplitude at every Node by Rule3's division act, the remainder not kept (the scale is the act's choice, no step of the law)."""
    now, before = (
        np.asarray(rule3(NO_READ, NO_READ, scale, amplitude, level, 0, 0)[0], dtype=np.int64)
        for level in levels
    )
    return now, before


def one_quantum(
    family: FamilyRule,
    levels: tuple[np.ndarray, np.ndarray],
    action: int,
    wrap: Wrap,
    bound: int,
    label: str,
    paces: tuple[int, Any, tuple[Any, ...]],
) -> tuple[np.ndarray, np.ndarray]:
    """The count is the record's form (ALGEBRA.md #the-counts-line, the lay and the wall): the written levels scaled so that their own form, laid by the lay's act over the board at the family's paces (Gamma, the content, the axis contents), is exactly one count: the amplitude bracketed from the written one by halving while the lay reaches one and doubling while it does not (up to A), then bisected to the least amplitude that reaches one; refused by name where the write is zero, where no amplitude up to A lays a count, or where the least that lays any lays more than one."""
    amplitude = int(max(int(np.abs(levels[0]).max()), int(np.abs(levels[1]).max())))
    if amplitude == 0:
        raise ValueError(
            f"{label}: the written levels are zero at every Node, and no scale lays one count"
        )
    gamma, content, axis = paces

    def count(scale: int) -> int:
        now, before = scaled(levels, amplitude, scale)
        record = node.Record(now, before, node.zeros(now.shape))
        return int(node.lay(family, (record,), action, wrap, gamma, content, axis)[0].sum())

    def half(value: int) -> int:
        return int(rule3(NO_READ, NO_READ, 1, 2, value, 0, 0)[0])

    low, high = amplitude, amplitude
    if count(amplitude) >= 1:
        while low > 0 and count(low) >= 1:
            high, low = low, half(low)
    else:
        while count(high) < 1:
            if high > bound:
                raise ValueError(
                    f"{label}: the written form lays no count at any amplitude up to A = {bound}"
                )
            low, high = high, 2 * high
    while high - low > 1:
        middle = half(low + high)
        low, high = (low, middle) if count(middle) >= 1 else (middle, high)
    if count(high) != 1 or high > bound:
        raise ValueError(
            f"{label}: the written form lays {count(high)} counts at the least amplitude {high} that lays any "
            f"(A = {bound}): no scale lays exactly one (ALGEBRA.md #the-counts-line, the lay and the wall)"
        )
    return scaled(levels, amplitude, high)


def converted(
    own: node.NodeState,
    other: node.NodeState,
    given: FamilyRule,
    there: Node,
    action: int,
    wrap: Wrap,
    bound: int,
    label: str,
    paces: tuple[int, Any, tuple[Any, ...]],
) -> None:
    """One quantum converted at the Node it entered (ALGEBRA.md #the-primitives, the row "the giving"): the body's family's count there -1, the given family's +1, and the given family's two levels there gain the body's family's two levels there scaled so their form lays exactly one count at the given family's paces (`one_quantum`)."""
    assert own.count is not None and other.count is not None
    assert own.levels is not None and other.levels is not None
    port = np.zeros(own.count.shape, dtype=bool)
    port[there] = True
    written = one_quantum(
        given,
        (np.where(port, own.levels.now, 0), np.where(port, own.levels.before, 0)),
        action,
        wrap,
        bound,
        label,
        paces,
    )
    own.count[there] -= 1
    other.count[there] += 1
    now, before = (carried(level, 1, 0)[0] for level in written)
    other.levels = replace(other.levels, now=other.levels.now + now, before=other.levels.before + before)
