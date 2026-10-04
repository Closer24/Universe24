"""The erasing front, the loop's act beside the receding face (the owner's word, "it starts erasing at the speed of light"; the mathematician's hand with the advisor's second, two hands; ALGEBRA.md, The click writes on the GameBoard; features/front): when a record's count reaches 0 in the books, from every Node written in that draw, at every interval t after it the loop presents the face (features/click, `Face`) to that record alone on the shell of Nodes at Link-metric distance exactly t from the Node, one shell per interval from the interval after the click, the shells one interval behind the causal bound and inside the click's light cone (`features/front.shell`, the periodic axes wrapped as the receding face handles them), at each shell Node's inward Port, the one whose neighbour on the inner shell is already erased, for the next two intervals, so that Rule3 writes 0 for the level now and then for the level before and the Node's free step keeps (0, 0) with its remainder below one read coefficient, its inner neighbours at 0 since the shell before, its outer since the shell after (the world's `erasure` L above 1 the taper: the last L shells before the reach faced each interval at the fractions (L - 1) / L down to 1 / L of Rule3's own level and then 0, the hard hole's kink at the taker's neighbours, about half a quantum of the local amplitude's share for the intervals until the front erased it, written down shell by shell instead; the owner's word of 2026-10-04, the mathematician's hand with the advisor's first); the ball of distance at most t is empty of the record, the past going out from the click at the causal bound, what stands beyond the ball holds the whole NodeState bit for bit as the run without the front holds it (the dependency radius one Link, the front invisible ahead of itself), and the inverse presents the same faces, so the back-in-time gate reads MATCH across every erasure interval; every other record untouched, a record whose count stays above 0 after a click has no front, nothing in the Node, nothing assigned at any Node; one erasure line per front per interval while its shell holds a Node, a GameBoard diagnostic beside the click line for the host's tool (the shell's Nodes and the levels standing there, the faces' take), and one last line with no Node where the shell leaves the declared board, the front's end. The fronts stand in the credit's books and at no Node. **The restoring front, the hole's local form** (ALGEBRA.md, The click writes on the GameBoard (6); the two hands' line): where the record's count stays at one or more after the taking, the same front from the hole's Node carries the other target: the hole's content written back among the record's Nodes by the one division act (`lay.division_act`) in proportion to a snapshot of the record's |levels| at the click (`Restoring.weights`, a read of the record and no write), the leftover units at the heaviest, each share written through the one lay act (`lay.laid`) when the front reaches its Node and never before, one Link per interval, one interval behind the causal bound as the erasure is; the hole's content is its two faces' own change of the record's two sums, read from the faces' kicks R_face (value - arrival) (`features/click.Hole.kicks`, `content_of`), so that the velocity sum is restored within the remainders' units for every hole, the hole to 0 and the partial hole alike; what the front leaves is a constant uniform level of the record, no form and no share; a Node the wave has left by the time the front arrives still receives its share, a few units in an empty region, harmless and named; the front ends when every share is written or its shell leaves the board."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.ports import arrival
from event_universe.core.rule3 import division_forward
from event_universe.features.click import Face, Hole
from event_universe.features.front import shell
from event_universe.lay import division_act, laid
from event_universe.loader.keys import Node
from event_universe.reports import erasure

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard


Snapshot = dict[Node, int]  # the record's |levels| at its Nodes at the click, the file's coordinates
Schedule = dict[Node, tuple[int, int]]  # per Node the share of the hole's content, (now, before)


@dataclass
class Restoring:
    """The restoring front's books: per line of the record the holes at its Node (one per hole written there, their faces' kicks the hole's content, `features/click.Hole`), the snapshot of the record's |now| + |before| at its other Nodes at the click (`Snapshot`, the file's coordinates; a read of the record and no write) and, once the two faces have been presented, the schedule (`Schedule`): per line the share of the hole's content at every Node by the one division act, each written when the front reaches its Node and popped then, so the front ends when none is left."""

    holes: list[list[Hole]]
    weights: list[Snapshot]
    shares: list[Schedule] | None = None


def on_board(board: GameBoard, node: Node) -> tuple[int, int, int]:
    """A Node declared at the file's coordinates on the GameBoard as grown, by the offset of the layers grown before the origin."""
    return (
        int(node[0]) + board.offset[0],
        int(node[1]) + board.offset[1],
        int(node[2]) + board.offset[2],
    )


def declared(board: GameBoard, here: Any) -> Node:
    """A Node of the GameBoard as grown at the file's coordinates, the offset taken back."""
    return (
        int(here[0]) - board.offset[0],
        int(here[1]) - board.offset[1],
        int(here[2]) - board.offset[2],
    )


@dataclass(frozen=True)
class Front:
    """A front in the credit's books: the record's family, the click's Node (the file's coordinates), the click's interval and its target, None for the erasing front (the count at 0, the faces to 0 shell by shell) or the restoring front's books (`Restoring`, the count at one or more)."""

    family: int
    origin: Node
    since: int
    restoring: Restoring | None = None


def started(board: GameBoard, index: int, nodes: list[Node]) -> None:
    """A record's count at 0 in the books: a front begun at this interval from every Node written in the draw, kept in the books (`credit.Books.fronts`)."""
    board.credit.fronts.extend(Front(index, at, board.tick) for at in nodes)


def restoring(board: GameBoard, index: int, holes: dict[Node, list[list[Hole]]]) -> None:
    """A record's count at one or more after its taking: a restoring front begun at this interval from every hole's Node (`holes`: per Node the holes written there, each one `Hole` per line of the record), with the snapshot of the record's |now| + |before| at every Node but the holes' per line, the weights of the division act (ALGEBRA.md, The restoring front, the hole's local form: the weights a snapshot at the click, the schedule fixed then)."""
    lines = board.families[index].record
    taken = board.mask(tuple(holes))
    weights = []
    for line in range(lines):
        record = board.states[index].lines[line]
        sizes = np.where(taken, 0, np.abs(record.now) + np.abs(record.before))
        weights.append({declared(board, h): int(sizes[tuple(h)]) for h in np.argwhere(sizes != 0)})
    for at, written in holes.items():
        books = Restoring([[hole[line] for hole in written] for line in range(lines)], weights)
        board.credit.fronts.append(Front(index, at, board.tick, books))


def content_of(holes: list[Hole], wall: int) -> tuple[int, int]:
    """The hole's content, its change of the record's two sums after its two faces, read from the faces' kicks k_1 and k_2 (each R_face (value - arrival), the face's change of the velocity invariant w (SUM now - SUM before) + SUM r, exact; summed over the holes written at the Node): the level sum moved by (2 k_1 + k_2) div w, the first kick a velocity carried one interval further, and the before sum by k_1 div w, each half up, so that the velocity sum is restored within the remainders' units once every share is written; a hole to 0 reads about (now_i, before_i), a partial hole what its faces took. The velocity's drift over the restoration's delay stays as the constant uniform level the law names, no form and no share: written back locally, shell by shell, it would be a step whose kinks carry form as its square."""
    first = sum(hole.kicks[0] for hole in holes)
    second = sum(hole.kicks[1] for hole in holes)
    half = division_forward(wall, 2, 0)[0]
    return (
        int(division_forward(2 * first + second, wall, half)[0]),
        int(division_forward(first, wall, half)[0]),
    )


def divided(change: int, weights: list[int]) -> list[int]:
    """A change standing at the hole's Node divided back among the record's other Nodes by the one division act (`lay.division_act`): the Node first at the weight 0 and the others at their weights, the others' shares summing to -change exactly, the leftover one unit each at the heaviest."""
    hole = np.array([change, *([0] * len(weights))], dtype=object)
    return [int(share) for share in division_act(hole, np.array([0, *weights], dtype=object))[1:]]


def scheduled(board: GameBoard, front: Front) -> list[Schedule]:
    """The restoring front's schedule, once its hole's two faces have been presented: per line the hole's content (`content_of`) divided back among the record's other Nodes by the one division act in proportion to their |levels| at the click (`divided`, the snapshot's weights, the leftover one unit each at the heaviest), the shares at those Nodes the schedule, the hole's Node the faces' and no share; no schedule where the record stands nowhere else."""
    assert front.restoring is not None
    wall = 2 * board.half_wall(front.family)
    found: list[Schedule] = []
    for holes, weights in zip(front.restoring.holes, front.restoring.weights, strict=True):
        nodes, sizes = list(weights), list(weights.values())
        level, before = content_of(holes, wall) if nodes else (0, 0)
        shares = zip(nodes, divided(level, sizes), divided(before, sizes), strict=True)
        found.append({at: (n, b) for at, n, b in shares if n or b})
    return found


def inward(mask: np.ndarray, inner: np.ndarray, board: GameBoard) -> np.ndarray:
    """Per shell Node the first Port in Port order whose neighbour lies on the inner shell (the arrival of the inner shell's mask through that Port), 0 where none does."""
    found = np.full(board.shape, -1, dtype=object)
    for port, (axis, side) in enumerate((a, s) for a in range(3) for s in (1, -1)):
        there = (
            mask & (found < 0) & np.asarray(arrival(inner, axis, side, board.wrap, False), dtype=bool)
        )
        found[there] = port
    return np.where(found < 0, 0, found)


def advanced_fronts(board: GameBoard) -> None:
    """Every front one shell further at the end of an interval: the faces of the record's every line at the shell at the Link-metric distance of the intervals since the click, the shell wrapped on the periodic axes and read at the file's coordinates by the offset of the layers grown before the origin; at L = 1 (`World.erasure`, the file's `erasure`, 1 as built) the two faces to 0 at each shell Node's inward Port for the next two intervals, as built, bit for bit; above 1 the taper (ALGEBRA.md, The click writes on the GameBoard (6), the front writes to 0 over L shells): at every interval the shells within the last L before the reach d are faced for the next interval alone, each on the board as it stands then (a layer grown beside a tapering shell is faced with it, where a booking made at the reach would have missed it), the shell at distance s at the fraction (L - (d - s + 1)) / L of Rule3's own level while that is above 0 (`Face.fraction`) and at 0 for its two faces after, so that its pair reaches (0, 0) as its outer neighbour's level now does and the free step keeps it there, and the hole's own Node faced to 0 through the first shell's taper, its two faces of the taking having left it at (0, 0) beside tapered neighbours; a front ends when its new shell and, above L = 1, its tapering shells lie beyond the board; one erasure line per front while a shell of it holds a Node, with the record's share standing on it and the record's unit, the faces' take in quanta. A restoring front (`Front.restoring`) writes its shares instead (`restored`), the shell at the distance of the intervals since the click less one, once its hole's two faces have been presented."""
    kept = []
    for front in board.credit.fronts:
        distance = board.tick - front.since
        if distance == 0:  # the click's own interval: the first shell at the interval after the click
            kept.append(front)
        elif (restored if front.restoring is not None else erased)(board, front, distance):
            kept.append(front)
    board.credit.fronts = kept


def erased(board: GameBoard, front: Front, distance: int) -> bool:
    """The erasing front's interval (the body of the loop's act as built, bit for bit): the shell at `distance` faced to 0 for the next two intervals at L = 1, the taper above 1, one erasure line while a shell holds a Node and one last line where the shell leaves the board; whether the front goes on."""
    index, origin = front.family, front.origin
    taper = board.world.erasure
    where = on_board(board, origin)
    mask = shell(board.shape, where, distance, board.world.periodic)
    family, unit = board.families[index], board.credit.units[index]
    holds = bool(mask.any())
    if taper == 1:
        if holds:
            faced(board, index, family.record, where, distance, [board.tick + 1, board.tick + 2], None)
    else:
        for s in range(max(1, distance - taper), distance + 1):
            reached = distance - s + 1  # the intervals since the reach passed the shell s
            fraction = (taper - reached, taper) if reached < taper else None
            holds |= faced(board, index, family.record, where, s, [board.tick + 1], fraction)
        if 2 <= distance <= taper:  # the hole's Node kept at 0 while its first shell tapers
            for line in range(family.record):
                board.credit.faces.setdefault(board.tick + 1, []).append(
                    Face(index, line, (origin[0], origin[1], origin[2]), 0, board.tick + 1)
                )
    if not holds:  # the shells beyond the declared board: the front ends, one line
        if board.output is not None:
            board.output(erasure(board.tick, family.name, list(origin), distance, 0, 0, unit))
        return False
    standing = int(board.share_of(index, 1, mask)[0].sum(dtype=object)) if bool(mask.any()) else 0
    if board.output is not None:
        board.output(
            erasure(board.tick, family.name, list(origin), distance, int(mask.sum()), standing, unit)
        )
    return True


def restored(board: GameBoard, front: Front, distance: int) -> bool:
    """The restoring front's interval: nothing until the hole's two faces have been presented (the content read from them, `scheduled`, once), then the shares of the shell at `distance` less one, one interval behind the causal bound as the erasure is, written through the one lay act (`lay.laid`, no weights: the shares are the division act's own, the remainders as they stand) and popped from the schedule; whether a share is left to write and the shell still holds a Node."""
    books = front.restoring
    assert books is not None
    if distance < 2:
        return True
    if books.shares is None:
        books.shares = scheduled(board, front)
    mask = shell(board.shape, on_board(board, front.origin), distance - 1, board.world.periodic)
    for line, shares in enumerate(books.shares):
        reached = [node for node in shares if mask[on_board(board, node)]]
        if not reached:
            continue
        now, before = (np.zeros(board.shape, dtype=object) for _ in range(2))
        for node in reached:
            now[on_board(board, node)], before[on_board(board, node)] = shares.pop(node)
        origin = None  # the remainders as they stand: the shares change a standing record
        laid(board, front.family, line, (now, before), None, origin, board.mask(tuple(reached)))
    return bool(mask.any()) and any(books.shares)


def faced(
    board: GameBoard,
    index: int,
    lines: int,
    at: tuple[int, int, int],
    distance: int,
    ticks: list[int],
    fraction: tuple[int, int] | None,
) -> bool:
    """The faces of a record's lines at the shell at `distance` from the click's Node `at` (the board's coordinates), one per Node and line at each tick named, at the Node's inward Port (the first whose neighbour lies on the inner shell), at the taper's fraction or the target 0 (None); whether the shell holds a Node on the board (a shell beyond it books none)."""
    mask = shell(board.shape, at, distance, board.world.periodic)
    if not bool(mask.any()):
        return False
    ports = inward(mask, shell(board.shape, at, distance - 1, board.world.periodic), board)
    for here in np.argwhere(mask):
        node_at = declared(board, here)
        port = int(ports[tuple(here)])
        for line in range(lines):
            for tick in ticks:
                board.credit.faces.setdefault(tick, []).append(
                    Face(index, line, node_at, port, tick, fraction=fraction)
                )
    return True
