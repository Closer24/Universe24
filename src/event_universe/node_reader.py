"""The reader's region (ALGEBRA.md, The NodeReader is one declaration kind for every experiment; the mathematician's 299 with the advisor's second, #1572, two hands): what a reader declared over a connected region (two Nodes or more with Nodes alone, one Node or more with a record of its own, the relation seen from its two ends) reads and books without writing a level: its books (`NodeBooks`, `books_of`), the lay's amplitudes in the weights' proportion and the record's norm, the arriving record's level projected on the reader's normalised mode (`arriving`), the window's inflow booked per Node (`booked_inflow`, `booked_inflows`), the dark and the reader's own clock over the region (`dark`, `own_clock`), the outcome's draw and the one Node a write is laid at, the taking's by the inflow booked and the giving's by the record's share (`picked`, `drawn_node`, `hole_node`), and the click line that names no Node (`reported`); the writes themselves stay in `meeting.py`."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import node
from event_universe.core import paces
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import division_fixed_point, division_forward
from event_universe.features.click import drawn, spread, squared
from event_universe.loader.derived import count_wall, row_of
from event_universe.loader.instrument import Generator, Instrument, NodeReaderDeclaration
from event_universe.loader.keys import Node
from event_universe.loader.world import BodyRow
from event_universe.reports import BODY, credit, entering, front
from event_universe.resonance import Reference, references_of, scale_of

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard

Currents = dict[int, Any]


@dataclass
class NodeBooks:
    """The books of a record declared a reader over a region (ALGEBRA.md, The NodeReader is one declaration kind for every experiment): the declaration's number among the world's `bodies`, the record's family and its record number, its Nodes with the lay's weights (the weights' proportion), its declaration, the part carrying the count, the counts per part, the labels, the intervals elapsed in the window, the generator's state, the two reference records per transition, the windows closed and its own clock; `amplitudes` the lay's amplitude of one quantum at each Node, isqrt(A^2 w_i div SUM w), `norm` the record's amplitude over the region, isqrt(SUM A_i^2), the mode's norm, and `intake` per arriving family the window's inflow through each Node's front Ports, the taking's draw weights."""

    number: int
    index: int
    record: int
    nodes: tuple[Node, ...]
    weights: tuple[int, ...]
    declared: NodeReaderDeclaration
    part: int
    counts: list[int]
    labels: list[int]
    elapsed: int
    state: int
    references: list[Reference]
    windows: int = 0
    clock: list[int] = field(default_factory=lambda: [0, 0])
    amplitudes: tuple[int, ...] = ()
    norm: int = 1
    intake: dict[int, list[int]] = field(default_factory=dict)


def books_of(board: GameBoard) -> list[NodeBooks]:
    """The books of every record declared an instrument at a Node, in the world's order: its number among `bodies`, its family and record, its one Node, its declaration, the part carrying the count, the counts per part, the labels at their counts in the count's units, the window begun and the generator at the declared seed; the scale of its reference records from the declared window, or from the run's intervals where its window is bounded by a probe's lays (no window longer than the run; one interval the least)."""
    found = []
    for number, (record, row) in enumerate(board.laid_rows()):
        if not isinstance(row, BodyRow) or row.instrument is None or row.instrument.draw is None:
            continue
        parted = list(row.instrument.counts)
        wall = count_wall(board.families[row.family], board.world.quantum_action)
        part = max(range(len(parted)), key=lambda k: parted[k])
        labels = [count * wall for count in parted]
        draw = row.instrument.draw
        longest = draw.window if isinstance(draw, Instrument) else max(board.world.ticks, 1)
        scale = scale_of(board.world.width, board.world.amplitude_bound, longest)
        seed = draw.seed
        references = references_of(scale, row.instrument.transitions)
        square, total = (
            squared(1, board.world.quantum_action, board.families[row.family].pair),
            sum(row.counts),
        )
        amplitudes = tuple(spread(square, (weight, total)) for weight in row.counts)
        norm = max(division_fixed_point(sum(a * a for a in amplitudes)), 1)
        found.append(
            NodeBooks(
                number,
                row.family,
                record,
                row.nodes,
                row.counts,
                row.instrument,
                part,
                parted,
                labels,
                0,
                seed,
                references,
                amplitudes=amplitudes,
                norm=norm,
            )
        )
    return found


def arriving(board: GameBoard, books: NodeBooks, drive: int, direction: int = 1) -> int:
    """The arriving record's level read into the reader's resonant turn: its level at each of the reader's Nodes, the level now (`direction` 1) or the level before (-1), projected on the reader's own normalised mode, SUM_i d_i A_i div A with A_i the lay's amplitude of one quantum at the Node and A = isqrt(SUM A_i^2) (`NodeBooks.amplitudes`, `norm`), rounded half up by the division act: the meeting is bilinear in the two records at each Node and the region's turn is the sum of the Nodes' meetings over the record's norm, the drive's level itself at one Node and (SUM_i d_i) / sqrt(n) over n Nodes in the equal lay (the mathematician's 299 section 2 with the advisor's second, #1572 comment 5969972693, two hands: the level sum over-weights by sqrt(n), the boundary inflow is quadratic in the drive and turns no phase); a drive whose phase runs along the region carries the form factor of a body of that size. A holder of the sign's time level is summed over every row but the record's own (`node.row_levels`, light), a family of quanta's first line's level otherwise."""
    family, lines = board.families[drive], board.states[drive].lines
    if family.wronskian:
        own = row_of(board.families, books.index, books.record)
        levels = np.asarray(node.row_levels(family, lines, 0, direction, own))
    else:
        levels = lines[0].now if direction == 1 else lines[0].before
    total = sum(
        int(levels[tuple(np.add(at, board.offset))]) * amplitude
        for at, amplitude in zip(books.nodes, books.amplitudes, strict=True)
    )
    half = division_forward(books.norm, 2, 0)[0]
    size = int(division_forward(abs(total), books.norm, half)[0])
    return size if total >= 0 else -size


def booked_inflow(board: GameBoard, books: NodeBooks, drive: int, came: Any) -> None:
    """The reader's book of a window's inflows per Node (ALGEBRA.md, The NodeReader is one declaration kind for every experiment; the mathematician's 299 section 3 with the advisor's second, two hands, one rule for the one kind): the arriving family's current through each of the reader's Nodes' front Ports this interval (`reports.entering`, the same read as the credit's `booked`) added to the window's sum at that Node, the weights the taking's Node is drawn by at the close, the Node the quantum entered through; emptied at the window's close (`jumped`)."""
    book = books.intake.setdefault(drive, [0] * len(books.nodes))
    for index, at in enumerate(books.nodes):
        book[index] += int(came[tuple(np.add(at, board.offset))])


def dark(board: GameBoard, books: NodeBooks) -> bool:
    """A reader with no arriving record at its Nodes this interval: both levels, now and before, of every family its transitions name sum to 0 over the region at every Node, so no window stands and the giving\'s grain is the interval."""
    turning = {t.drive for t in books.declared.transitions if t.leaves != t.enters}
    for drive in sorted(turning):
        family, lines = board.families[drive], board.states[drive].lines
        own = row_of(board.families, books.index, books.record)
        for side in (1, -1):
            if family.wronskian:
                levels = np.asarray(node.row_levels(family, lines, 0, side, own))
            else:
                levels = lines[0].now if side == 1 else lines[0].before
            if any(int(levels[tuple(np.add(at, board.offset))]) for at in books.nodes):
                return False
    return True


def own_clock(board: GameBoard, books: NodeBooks) -> int:
    """The reader's own clock, the composed clock p_0 under its record's read of the content (`paces.clock_of`) at each of its Nodes, their mean by the division act with the half carry (as a region's clock is read, `credit.clocked`): Gamma in the vacuum and below it in a well, the number the turn per proper interval and the dark's hazard read."""
    gamma = board.world.node_clock
    content = board.read(books.index, 1, books.record)[0]
    clocks = [
        int(
            paces.clock_of(
                gamma,
                int(np.asarray(content)[tuple(np.add(at, board.offset))])
                if np.ndim(content)
                else int(content),
            )
        )
        for at in books.nodes
    ]
    count = len(clocks)
    return int(division_forward(sum(clocks), count, division_forward(count, 2, 0)[0])[0])


def picked(
    board: GameBoard, state: int, generator: Generator | None, weights: list[int], outcomes: int
) -> tuple[int, int]:
    """The draw of the one click act, the outcome alone: with more than one outcome, one draw by the weights with the generator (its state carried in the books), the lower index on a tie; one outcome, no draw and the state kept. The Node of the realised write is drawn after it, for that write alone (the advisor's 5969944547 (a), the mathematician's 299 section 5, two hands: one draw per click, none for a candidate not realised)."""
    pick, modulus = 0, board.world.width + 1
    if outcomes > 1:
        assert generator is not None  # a draw among outcomes is the declared generator's
        pick, state = drawn(state, generator.multiplier, generator.increment, modulus, weights)
    return pick, state


def drawn_node(board: GameBoard, books: NodeBooks, weights: list[int]) -> Node:
    """The one Node of the region a write is laid at, drawn by `weights` over the reader's Nodes with its own generator (features/click, `drawn`; ALGEBRA.md, The NodeReader is one declaration kind for every experiment: the write of a click is at one Node of the region, the share at a Node a GameBoard reading and no measurement); the lay's weights where every weight is 0."""
    assert books.declared.draw is not None
    found = weights if sum(weights) > 0 else list(books.weights)
    pick, books.state = drawn(
        books.state,
        books.declared.draw.multiplier,
        books.declared.draw.increment,
        board.world.width + 1,
        found,
    )
    return books.nodes[pick]


def hole_node(board: GameBoard, books: NodeBooks, drive: int) -> Node:
    """The taking's Node: drawn by the arriving record's inflow booked through each of the reader's Nodes' front Ports over the window (`booked_inflow`, floored at 0), the Node the quantum entered through, as the credit draws it for a reader of the field's record, one rule for the one kind (the mathematician's 299 section 3, the advisor's 5969944547 (c), two hands); the lay's weights where nothing entered; the hole's two faces written there; drawn after the outcome, for the realised write alone."""
    booked = books.intake.get(drive, [0] * len(books.nodes))
    return drawn_node(board, books, [max(int(weight), 0) for weight in booked])


def reported(
    board: GameBoard,
    books: NodeBooks,
    parts: tuple[int, int],
    exchanged: tuple[int | None, int | None],
    count: int = 1,
) -> None:
    """The click line of a record's click (`reports.credit`, the one click line kind of every reader; ALGEBRA.md, The NodeReader is one declaration kind for every experiment: never a Node): the reader `body n` by its number, the `parts` realised and left by their declared names (`realised` the part after, `before` the part before), the families `exchanged`, the one taken from and the one given to (None where none), the count moved, 1 for a click and 0 for the null window's write, the count left in the books of the family exchanged (None where none), the window's intervals [first, last], the body's own proper time at the close and the index of the window closed (its books' clock and windows); labelled the node_reader's where a `quantum` passed and a diagnostic for the null window's write; the Node written stands in the `lay` and `face` lines beside it and here nowhere."""
    if board.observer is None:
        return
    names, families = books.declared.names, board.families
    window = [board.tick - books.elapsed + 1, board.tick]
    taken, light = (families[k].name if k is not None else None for k in exchanged)
    moved = next((k for k in exchanged if k is not None), None)
    left = board.credit.counts[moved] if moved is not None else None
    name, reader, own = families[books.index].name, f"{BODY} {books.number}", books.clock[0]
    after, before = names[parts[0]], names[parts[1]]
    line = credit(
        board.tick,
        name,
        reader,
        window,
        own,
        books.windows,
        after,
        None,
        count,
        left,
        before,
        taken,
        light,
    )
    board.observer(line)


def booked_inflows(board: GameBoard, currents: Currents, wrap: Wrap, own: np.ndarray) -> None:
    """Every reader's own book of this interval: for each family its transitions name among `currents`, the inflow entering through its Nodes' front Ports (`reports.front` on the region, `entering`), added to its book per Node (`booked_inflow`); the credit's rule for a reader with Nodes alone, here for a reader with a record of its own."""
    for books in board.credit.bodies:
        drives = sorted({t.drive for t in books.declared.transitions if t.drive in currents})
        if drives:
            region = board.mask(books.nodes)
            facing = front(region, wrap, region, own)
            for drive in drives:
                booked_inflow(board, books, drive, entering(facing, currents[drive]))
