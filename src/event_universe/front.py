"""The erasing front, the loop's act beside the receding face (the owner's word, "it starts erasing at the speed of light"; the mathematician's hand with the advisor's second, two hands; ALGEBRA.md, The click writes on the lattice; features/front): when a record's count reaches 0 in the books, from every Node written in that draw, at every interval t after it the loop presents the face (features/click, `Face`) to that record alone on the shell of Nodes at Link-metric distance exactly t from the Node, one shell per interval from the interval after the click, the shells one interval behind the causal bound and inside the click's light cone (`features/front.shell`, the periodic axes wrapped as the receding face handles them), at each shell Node's inward Port, the one whose neighbour on the inner shell is already erased, for the next two intervals, so that Rule3 writes 0 for the level now and then for the level before and the Node's free step keeps (0, 0) with its remainder below one read coefficient, its inner neighbours at 0 since the shell before, its outer since the shell after (the world's `erasure` L above 1 the taper: the last L shells before the reach faced each interval at the fractions (L - 1) / L down to 1 / L of Rule3's own level and then 0, the hard hole's kink at the taker's neighbours, about half a quantum of the local amplitude's share for the intervals until the front erased it, written down shell by shell instead; the owner's word of 2026-10-04, the mathematician's hand with the advisor's first); the ball of distance at most t is empty of the record, the past going out from the click at the causal bound, what stands beyond the ball holds the whole NodeState bit for bit as the run without the front holds it (the dependency radius one Link, the front invisible ahead of itself), and the inverse presents the same faces, so the back-in-time gate reads MATCH across every erasure interval; every other record untouched, a record whose count stays above 0 after a click has no front, nothing in the Node, nothing assigned at any Node; one erasure line per front per interval while its shell holds a Node, a lattice diagnostic beside the click line for the host's tool (the shell's Nodes and the levels standing there, the faces' take), and one last line with no Node where the shell leaves the declared board, the front's end. The fronts stand in the credit's books and at no Node."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.ports import arrival
from event_universe.features.click import Face
from event_universe.features.front import shell
from event_universe.loader.keys import Node
from event_universe.reports import erasure

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


def on_board(board: Lattice, node: Node) -> tuple[int, int, int]:
    """A Node declared at the file's coordinates on the lattice as grown, by the offset of the layers grown before the origin."""
    return (
        int(node[0]) + board.offset[0],
        int(node[1]) + board.offset[1],
        int(node[2]) + board.offset[2],
    )


def declared(board: Lattice, here: Any) -> Node:
    """A Node of the lattice as grown at the file's coordinates, the offset taken back."""
    return (
        int(here[0]) - board.offset[0],
        int(here[1]) - board.offset[1],
        int(here[2]) - board.offset[2],
    )


@dataclass(frozen=True)
class Front:
    """A front in the credit's books: the record's family, the click's Node (the file's coordinates) and the click's interval; its target is 0, the faces to 0 shell by shell, the count at 0."""

    family: int
    origin: Node
    since: int


def started(board: Lattice, index: int, nodes: list[Node]) -> None:
    """A record's count at 0 in the books: a front begun at this interval from every Node written in the draw, kept in the books (`credit.Books.fronts`)."""
    board.credit.fronts.extend(Front(index, at, board.interval) for at in nodes)


def inward(mask: np.ndarray, inner: np.ndarray, board: Lattice) -> np.ndarray:
    """Per shell Node the first Port in Port order whose neighbour lies on the inner shell (the arrival of the inner shell's mask through that Port), 0 where none does."""
    found = np.full(board.shape, -1, dtype=object)
    for port, (axis, side) in enumerate((a, s) for a in range(3) for s in (1, -1)):
        there = (
            mask & (found < 0) & np.asarray(arrival(inner, axis, side, board.wrap, False), dtype=bool)
        )
        found[there] = port
    return np.where(found < 0, 0, found)


def advanced_fronts(board: Lattice) -> None:
    """Every front one shell further at the end of an interval: the faces of the record's every line at the shell at the Link-metric distance of the intervals since the click, the shell wrapped on the periodic axes and read at the file's coordinates by the offset of the layers grown before the origin; at L = 1 (`World.erasure`, the file's `erasure`, 1 as built) the two faces to 0 at each shell Node's inward Port for the next two intervals, as built, bit for bit; above 1 the taper (ALGEBRA.md, The click writes on the lattice (6), the front writes to 0 over L shells): at every interval the shells within the last L before the reach d are faced for the next interval alone, each on the board as it stands then (a layer grown beside a tapering shell is faced with it, where a booking made at the reach would have missed it), the shell at distance s at the fraction (L - (d - s + 1)) / L of Rule3's own level while that is above 0 (`Face.fraction`) and at 0 for its two faces after, so that its pair reaches (0, 0) as its outer neighbour's level now does and the free step keeps it there, and the hole's own Node faced to 0 through the first shell's taper, its two faces of the absorption having left it at (0, 0) beside tapered neighbours; a front ends when its new shell and, above L = 1, its tapering shells lie beyond the board; one erasure line per front while a shell of it holds a Node, with the record's share standing on it and the record's unit, the faces' take in quanta."""
    kept = []
    for front in board.credit.fronts:
        distance = board.interval - front.since
        if distance == 0:  # the click's own interval: the first shell at the interval after the click
            kept.append(front)
        elif erased(board, front, distance):
            kept.append(front)
    board.credit.fronts = kept


def erased(board: Lattice, front: Front, distance: int) -> bool:
    """The erasing front's interval (the body of the loop's act as built, bit for bit): the shell at `distance` faced to 0 for the next two intervals at L = 1, the taper above 1, one erasure line while a shell holds a Node and one last line where the shell leaves the board; whether the front goes on."""
    index, origin = front.family, front.origin
    taper = board.world.erasure
    where = on_board(board, origin)
    mask = shell(board.shape, where, distance, board.world.periodic)
    family, unit = board.families[index], board.credit.units[index]
    holds = bool(mask.any())
    if taper == 1:
        if holds:
            faced(
                board,
                index,
                family.record,
                where,
                distance,
                [board.interval + 1, board.interval + 2],
                None,
            )
    else:
        for s in range(max(1, distance - taper), distance + 1):
            reached = distance - s + 1  # the intervals since the reach passed the shell s
            fraction = (taper - reached, taper) if reached < taper else None
            holds |= faced(board, index, family.record, where, s, [board.interval + 1], fraction)
        if 2 <= distance <= taper:  # the hole's Node kept at 0 while its first shell tapers
            for line in range(family.record):
                board.credit.faces.setdefault(board.interval + 1, []).append(
                    Face(index, line, (origin[0], origin[1], origin[2]), 0, board.interval + 1)
                )
    if not holds:  # the shells beyond the declared board: the front ends, one line
        if board.output is not None:
            board.output(erasure(board.interval, family.name, list(origin), distance, 0, 0, unit))
        return False
    standing = int(board.share_of(index, 1, mask)[0].sum(dtype=object)) if bool(mask.any()) else 0
    if board.output is not None:
        board.output(
            erasure(board.interval, family.name, list(origin), distance, int(mask.sum()), standing, unit)
        )
    return True


def faced(
    board: Lattice,
    index: int,
    lines: int,
    at: tuple[int, int, int],
    distance: int,
    intervals: list[int],
    fraction: tuple[int, int] | None,
) -> bool:
    """The faces of a record's lines at the shell at `distance` from the click's Node `at` (the board's coordinates), one per Node and line at each interval named, at the Node's inward Port (the first whose neighbour lies on the inner shell), at the taper's fraction or the target 0 (None); whether the shell holds a Node on the board (a shell beyond it books none)."""
    mask = shell(board.shape, at, distance, board.world.periodic)
    if not bool(mask.any()):
        return False
    ports = inward(mask, shell(board.shape, at, distance - 1, board.world.periodic), board)
    for here in np.argwhere(mask):
        node_at = declared(board, here)
        port = int(ports[tuple(here)])
        for line in range(lines):
            for interval in intervals:
                board.credit.faces.setdefault(interval, []).append(
                    Face(index, line, node_at, port, interval, fraction=fraction)
                )
    return True
