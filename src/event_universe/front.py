"""The erasing front, the loop's act beside the receding face (the owner's word of 2026-10-03, 03:25 Israel, "it starts erasing at the speed of light"; the mathematician's 182 and 197 with the advisor's second, #1563 comment 5963124874 and #1572 comment 5963391333, two hands; ALGEBRA.md, The click writes on the GameBoard; features/front): when a record's count reaches 0 in the books, from every Node written in that draw, at every interval t after it the loop presents the face (features/click, `Face`) to that record alone on the shell of Nodes at Link-metric distance exactly t from the Node (`features/front.shell`, the periodic axes wrapped as the receding face handles them), at each shell Node's inward Port, the one whose neighbour on the inner shell is already erased, for the next two intervals, so that Rule3 writes 0 for the level now and then for the level before and the Node's free step keeps (0, 0) with its remainder below one read coefficient, its inner neighbours at 0 since the shell before, its outer since the shell after; the ball of distance at most t is empty of the record, the past going out from the click at the causal bound, what stands beyond the ball holds the whole NodeState bit for bit as the run without the front holds it (the dependency radius one Link, the front invisible ahead of itself), and the inverse presents the same faces, so the back-in-time gate reads MATCH across every erasure interval; every other record untouched, a record whose count stays above 0 after a click has no front, nothing in the Node, nothing assigned at any Node; one erasure line per front per interval while its shell holds a Node, a GameBoard diagnostic beside the click line for the host's tool (the shell's Nodes and the levels standing there, the faces' take), and one last line with no Node where the shell leaves the declared board, the front's end. The fronts stand in the credit's books and at no Node."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe.core.ports import arrival
from event_universe.features.click import Face
from event_universe.features.front import shell
from event_universe.loader.keys import Node
from event_universe.reports import erasure

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard


def started(board: GameBoard, index: int, nodes: list[Node]) -> None:
    """A record's count at 0 in the books: a front begun at this interval from every Node written in the draw, kept in the books (`credit.Books.fronts`)."""
    board.credit.fronts.extend((index, at, board.tick) for at in nodes)


def inward(mask: np.ndarray, inner: np.ndarray, board: GameBoard) -> np.ndarray:
    """Per shell Node the first Port in Port order whose neighbour lies on the inner shell (the arrival of the inner shell's mask through that Port), 0 where none does."""
    found = np.full(board.shape, -1, dtype=object)
    for port, (axis, side) in enumerate((a, s) for a in range(3) for s in (1, -1)):
        there = (
            mask & (found < 0) & np.asarray(arrival(inner, axis, side, board.wrap, False), dtype=bool)
        )
        found[there] = port
    return np.where(found < 0, 0, found)


def advanced(board: GameBoard) -> None:
    """Every front one shell further at the end of an interval: the faces of the record's every line at the shell at the Link-metric distance of the intervals since the click, for the next two intervals at each Node's inward Port, the shell wrapped on the periodic axes and read at the file's coordinates by the offset of the layers grown before the origin; a front whose shell lies beyond the board ends; one erasure line per front where the shell holds a Node."""
    kept = []
    for index, origin, since in board.credit.fronts:
        distance = board.tick - since
        if distance == 0:  # the click's own interval: the shell begins at the next
            kept.append((index, origin, since))
            continue
        at = tuple(int(a) + b for a, b in zip(origin, board.offset, strict=True))
        mask = shell(board.shape, (at[0], at[1], at[2]), distance, board.world.periodic)
        family, state = board.families[index], board.states[index]
        if not bool(mask.any()):  # the shell beyond the declared board: the front ends, one line
            if board.observer is not None:
                board.observer(erasure(board.tick, family.name, list(origin), distance, 0, 0))
            continue
        ports = inward(
            mask, shell(board.shape, (at[0], at[1], at[2]), distance - 1, board.world.periodic), board
        )
        standing = sum(
            int(np.abs(line.now[mask]).sum(dtype=object))
            + int(np.abs(line.before[mask]).sum(dtype=object))
            for line in state.lines[: family.record]
        )
        for here in np.argwhere(mask):
            node_at = (
                int(here[0] - board.offset[0]),
                int(here[1] - board.offset[1]),
                int(here[2] - board.offset[2]),
            )
            port = int(ports[tuple(here)])
            for line in range(family.record):
                for tick in (board.tick + 1, board.tick + 2):
                    board.credit.faces.setdefault(tick, []).append(
                        Face(index, line, node_at, port, tick)
                    )
        kept.append((index, origin, since))
        if board.observer is not None:
            board.observer(
                erasure(board.tick, family.name, list(origin), distance, int(mask.sum()), standing)
            )
    board.credit.fronts = kept
