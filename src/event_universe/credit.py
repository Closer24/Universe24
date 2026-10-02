"""The credit, the click written on the GameBoard (features/click; ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision of 2026-10-02: after a click the paths are cancelled on the GameBoard, not in the clicks' books, Rule3 kept): where the world declares the `instrument` (its window in intervals, its seed, its generator's multiplier and increment, `loader/instrument.py`) the instrument keeps the books of a window from the detectors' reports, the inflow through each boundary Node's front Ports summed over the window per family and region and, for a family of several parts, the joint share J per combination of the sides' ports accumulated from the parts' sums (the same numbers the click and parts lines carry), and at the window's end draws with its declared generator and writes its click at one Node, the loop's act from outside the Node as the lay and the receding face are, forward only; the record's count goes down by one per credited quantum, the run's accounting in the output, and at 0 the record is uncreditable, whatever its levels still show. The books are the instrument's and stand at no Node; the Node knows no click and no family of clicks; a world without the key keeps empty books and runs as before bit for bit."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from event_universe import growth, node, share
from event_universe.features.click import drawn, taken
from event_universe.loader.derived import count_wall
from event_universe.loader.instrument import Instrument, Ports, ports_of
from event_universe.loader.keys import Node
from event_universe.reports import PORT_NAMES, credit

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard

Intake = dict[Node, int]  # per boundary Node of a region, at the file's coordinates, the window's inflow
Joints = dict[
    tuple[int, ...], int
]  # per combination of the sides' ports (0 the +, 1 the -) the window's J
Sums = dict[str, list[list[int]]]  # per region the parts' level sums [now, before] of one interval


@dataclass
class Books:
    """The instrument's books: its declaration (None where the world declares none), the intervals elapsed in the window, the generator's state, the record's count per family of quanta, the count left to credit, the window's inflows per family and region per boundary Node, the window's joint shares per family of several parts, and the sides, the regions declaring a pattern with their two ports, in the file's order."""

    declaration: Instrument | None
    elapsed: int
    state: int
    counts: dict[int, int]
    intake: dict[tuple[int, str], Intake]
    joints: dict[int, Joints]
    sides: list[tuple[str, Ports]]

    def window_of(self, tick: int) -> list[int]:
        """The window closing at `tick`, [first, last], the declaration's length of intervals."""
        assert self.declaration is not None
        return [tick - self.declaration.window + 1, tick]

    @classmethod
    def of(cls, board: GameBoard) -> Books:
        """The books at the start: every family of quanta's count its laid share in whole quanta (the books' origin read as a count), the generator at the declared seed, every other book empty."""
        found = board.world.instrument
        counts = {index: counted(board, index, board.laid[index]) for index in board.order}
        sides = [(r.name, ports_of(r.basis, r.pattern)) for r in board.world.detectors if r.pattern]
        return cls(found, 0, found.seed if found is not None else 0, counts, {}, {}, sides)


def counted(board: GameBoard, index: int, total: int | None) -> int:
    """A share in the current's units as whole quanta, (total + W_c div 2) div W_c by the division act (`share.quanta_of`), 0 where it is not read: the reading of the record's count."""
    wall = count_wall(board.families[index], board.world.quantum_action)
    return 0 if total is None else int(share.quanta_of(np.array([total], dtype=object), wall, object)[0])


def instrument_nodes(board: GameBoard) -> np.ndarray:
    """The instrument's Nodes: the union of the declared regions (every detector with its own positions, the faces' layer and the bodies' detectors aside, `Detector.declared`), whose boundary is where the reports are read, so that what moves between two regions of one screen is not seen twice."""
    found = np.zeros(board.shape, dtype=bool)
    for detector in board.detectors:
        if detector.declared and detector.nodes is not None:
            found |= detector.nodes
    return found


def booked(board: GameBoard, index: int, name: str, came: np.ndarray) -> None:
    """The book of a window's inflows: per family and declared region the inflow through each boundary Node's front Ports (`reports.entering`) summed over the window's intervals, the Node at the file's coordinates; the shares of the draw of the one Node the click is written at; nothing where the world declares no instrument."""
    if board.credit.declaration is None:
        return
    book = board.credit.intake.setdefault((index, name), {})
    for at in np.argwhere(came != 0):
        key = growth.declared(at, board.offset)
        book[key[0], key[1], key[2]] = book.get((key[0], key[1], key[2]), 0) + int(came[tuple(at)])


def joined(board: GameBoard, index: int, sums: Sums) -> None:
    """The book of the meeting (ALGEBRA.md #the-click-is-the-meeting, the one form): per combination of the sides' ports the joint share J accumulated over the window on both members of the level pair from the sides' parts sums of one interval, J += (SUM_k c_k PROD_sides now_k)^2 + (SUM_k c_k PROD_sides before_k)^2, c_k the product over the sides of e_k at their ports, as the reader `tools/bell_gate.py` reads the same sums; nothing where the world declares no instrument or no side."""
    books = board.credit
    if books.declaration is None or not books.sides:
        return
    parts = board.families[index].parts
    levels = [sums.get(name, [[0, 0]] * parts) for name, _ports in books.sides]
    joint = books.joints.setdefault(index, {})
    for key in itertools.product(range(len(PORT_NAMES)), repeat=len(books.sides)):
        total = 0
        for member in range(2):
            term = 0
            for k in range(parts):
                product = 1
                for (_name, ports), port, found in zip(books.sides, key, levels, strict=True):
                    product *= ports[port][k] * found[k][member]
                term += product
            total += term * term
        joint[key] = joint.get(key, 0) + total


def draw(board: GameBoard, weights: list[int]) -> int:
    """One draw of the instrument by its declared generator (features/click, `drawn`): the index drawn among the weights, the generator's state kept in the books, the modulus the width's own, 2^width."""
    books = board.credit
    assert books.declaration is not None
    found = books.declaration
    pick, books.state = drawn(
        books.state, found.multiplier, found.increment, board.world.width + 1, weights
    )
    return pick


def windowed(board: GameBoard) -> None:
    """The window's count at the end of an interval: where the world declares the instrument, one more interval elapsed, and at the window's length the instrument's draw and its click written (`credited`), the count beginning again."""
    books = board.credit
    if books.declaration is None:
        return
    books.elapsed += 1
    if books.elapsed == books.declaration.window:
        credited(board)
        books.elapsed = 0


def credited(board: GameBoard) -> None:
    """The click written on the GameBoard at a window's end, per family of quanta from the window's books, then the books emptied: for a record of several parts the one draw through the root over the combinations of the sides' ports by the joint shares J (as the reader draws its combination), then at each side's one arrival Node the write (`written`) with the port realised and the parts it reads with a coefficient other than 0 named as kept in the result, the record's count down by one; for a record of one part the regions' window inflows floored at 0 are the shares, N = (their sum + W_c div 2) div W_c whole quanta, at most the count left, each drawn to a region by the shares and written at one Node of it; a record whose count stands at 0 is uncreditable and nothing draws from it, whatever its levels still show (the empty wave, a diagnostic); the draw and the write are the instrument's and no act of Rule3."""
    books = board.credit
    names = [detector.name for detector in board.detectors if detector.declared]
    for index in board.order:
        family = board.families[index]
        intake = {name: books.intake.pop((index, name), {}) for name in names}
        if family.parts > 1:
            joint = books.joints.pop(index, {})
            if sum(joint.values()) <= 0 or books.counts[index] <= 0 or not books.sides:
                continue
            keys = sorted(joint)
            combination = keys[draw(board, [joint[key] for key in keys])]
            for (name, ports), port in zip(books.sides, combination, strict=True):
                kept = [k for k, coefficient in enumerate(ports[port]) if coefficient != 0]
                written(board, index, name, intake[name], PORT_NAMES[port], kept)
            books.counts[index] -= 1
            continue
        shares = [max(sum(intake[name].values()), 0) for name in names]
        if sum(shares) <= 0:
            continue
        for _ in range(min(counted(board, index, sum(shares)), books.counts[index])):
            name = names[draw(board, shares)]
            written(board, index, name, intake[name], None, [0])
            books.counts[index] -= 1


def written(
    board: GameBoard, index: int, name: str, book: Intake, realised: str | None, kept: list[int]
) -> None:
    """The write of one click at one Node (features/click, `taken`): among the region's boundary Nodes the one the credited quantum entered through, drawn by the window's inflows per Node floored at 0 (none where nothing entered: no write); there every line of the record, the parts kept and the parts the realised port reads with 0 alike, is set to 0 in its three arrays, the hole, exactly as the receding face removes a share; nothing is written at any other Node, the hole spreading by Rule3 alone; one credit line, its result the window, the region, the port realised and the parts kept, the count moved 1 and the record's count left, with the one Node at the file's coordinates beside it as a GameBoard diagnostic (the owner's word of 2026-10-02: the detector gives no result for one Node)."""
    nodes = list(book)
    weights = [max(book[at], 0) for at in nodes]
    if sum(weights) <= 0:
        return
    at = nodes[draw(board, weights)]
    mask, family, state = board.mask((at,)), board.families[index], board.states[index]
    for number, line in enumerate(state.lines[: family.record]):
        now, before, remainder = taken([line.now, line.before, line.remainder], mask)
        state.lines[number] = node.Record(now, before, remainder)
    left, window = board.credit.counts[index] - 1, board.credit.window_of(board.tick)
    if board.observer is not None:
        board.observer(credit(board.tick, family.name, name, window, realised, kept, 1, left, list(at)))
