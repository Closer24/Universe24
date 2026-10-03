"""The credit, the click written on the GameBoard (features/click; ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision of 2026-10-02: after a click the paths are cancelled on the GameBoard, not in the clicks' books, Rule3 kept): where the world declares the `instrument` (its window in intervals, its seed, its generator's multiplier and increment, `loader/instrument.py`) the instrument keeps the books of a window from the detectors' reports, the inflow through each boundary Node's front Ports summed over the window per family and region and, for a family of several parts, the joint share J per combination of the sides' ports accumulated from the parts' sums (the same numbers the click and parts lines carry), and at the window's end draws with its declared generator and writes its click at one Node, the loop's act from outside the Node as the lay and the receding face are, forward only; the record's count goes down by one per credited quantum, the run's accounting in the output, and at 0 the record is uncreditable, whatever its levels still show. The books are the instrument's and stand at no Node; the Node knows no click and no family of clicks; a world without the key keeps empty books and runs as before bit for bit."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from event_universe import growth, share
from event_universe.body_node import references_over, scale_of_the_width, shares, solved
from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.features.click import Face, drawn
from event_universe.giving import Source
from event_universe.loader.derived import count_wall
from event_universe.loader.instrument import Instrument, Ports, ports_of
from event_universe.loader.keys import Node
from event_universe.meeting import Item, NodeBooks, books_of, click
from event_universe.reports import PORT_NAMES, credit

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard

Front = tuple[
    int, Node, int
]  # a front: the record's family, the click's Node (the file's coordinates), the click's interval
Intake = dict[Node, int]  # per boundary Node of a region, at the file's coordinates, the window's inflow
Joints = dict[
    tuple[int, ...], int
]  # per combination of the sides' ports (0 the +, 1 the -) the window's J
Sums = dict[str, list[list[int]]]  # per region the parts' level sums [now, before] of one interval
Clock = list[int]  # a detector's own clock: its proper time in whole intervals and the remainder carried


@dataclass
class Books:
    """The instrument's books: its declaration (None where the world declares none), the intervals elapsed in the window, the generator's state, the record's count per family of quanta, the count left to credit, the window's inflows per family and region per boundary Node, the window's joint shares per family of several parts, the sides, the regions declaring a pattern with their two ports, in the file's order, the records at Nodes declared instruments with their own books (`meeting.NodeBooks`), the erasing fronts begun where a record's count reached 0 (`Front`, the family, the click's Node and its interval), the faces the instrument presents, per interval (features/click, `Face`), the log the inverse presents again, the sources in time, the unit of one quantum of each record, W_rec, read once at the books' origin (`record_unit`), each declared region's own clock per family it reads (`Clock`, the proper time carried over the board's ticks, `clocked`), the count of the windows closed, the detectors' event clock, and per family and one-Node detector on a bound body the window's level sequence at its Node (`listened`, read at the close by the exact solve, `read_levels`)."""

    declaration: Instrument | None
    elapsed: int
    state: int
    counts: dict[int, int]
    intake: dict[tuple[int, str], Intake]
    joints: dict[int, Joints]
    sides: list[tuple[str, Ports]]
    bodies: list[NodeBooks]
    fronts: list[Front]
    faces: dict[int, list[Face]]
    sources: list[Source]
    units: dict[int, int] = field(default_factory=dict)
    clocks: dict[tuple[int, str], Clock] = field(default_factory=dict)
    windows: int = 0
    sequences: dict[tuple[int, str], list[int]] = field(default_factory=dict)

    def window_of(self, tick: int) -> list[int]:
        """The window closing at `tick`, [first, last], the declaration's length of intervals."""
        assert self.declaration is not None
        return [tick - self.declaration.window + 1, tick]

    @classmethod
    def of(cls, board: GameBoard) -> Books:
        """The books at the start: every family of quanta's count its laid share in whole quanta (the books' origin read as a count), its unit of one quantum from the same two numbers (`record_unit`, held through the run), the generator at the declared seed, every other book empty."""
        found = board.world.instrument
        counts = {index: counted(board, index, board.laid[index]) for index in board.order}
        sides = [(r.name, ports_of(r.basis, r.pattern)) for r in board.world.detectors if r.pattern]
        bodies = books_of(board)
        units = {
            index: record_unit(board, index, board.laid[index], counts[index]) for index in board.order
        }
        return cls(
            found,
            0,
            found.seed if found is not None else 0,
            counts,
            {},
            {},
            sides,
            bodies,
            [],
            {},
            [],
            units,
        )


def counted(board: GameBoard, index: int, total: int | None) -> int:
    """A share in the current's units as whole quanta, (total + W_c div 2) div W_c by the division act (`share.quanta_of`), 0 where it is not read: the reading of the record's count."""
    wall = count_wall(board.families[index], board.world.quantum_action)
    return 0 if total is None else int(share.quanta_of(np.array([total], dtype=object), wall, object)[0])


def record_unit(board: GameBoard, index: int, total: int | None, count: int) -> int:
    """The unit of one quantum of a record, W_rec, read and not declared (the advisor's line of 2026-10-03 with the mathematician's second, #1572 comments 5966657866, 5966769056 and 5966780505, two hands; the count's line, Q(z) = count x W_c sin omega for a monochromatic record): the record's share over the board at the books' origin over its count there, (total + count div 2) div count by the division act, read once and held through the run (a face removes one quantum's share with one count, the ratio unchanged; the roundings' drift moves it not); W_c where the books hold no count or no reading (nothing to credit). For a record laid by share with its count the share over W_c it is W_c within the lay's own rounding; for a born quantum of count 1 at Omega it is W_c sin Omega, the detector counting in the record's own quantum with no transition declared on any region."""
    wall = count_wall(board.families[index], board.world.quantum_action)
    if total is None or count <= 0:
        return wall
    return int(division_forward(total, count, division_forward(count, 2, 0)[0])[0])


def quanta_through(books: Books, index: int, inflow: int) -> int:
    """The clicks a window's inflow is worth in the record's own unit, (inflow + W_rec div 2) div W_rec by the division act (`record_unit`), the share's own rounding; the cap by the count is the credit's."""
    unit = books.units[index]
    return int(division_forward(inflow, unit, division_forward(unit, 2, 0)[0])[0])


def clocked(board: GameBoard) -> None:
    """The detectors' own clocks, one interval (the advisor's derivation of 2026-10-03, #1572 comment 5966657866, the clock composed from the paces, with the mathematician's second: the clock is the Node's, a detector's proper interval per board tick at a Node of content c is p_0(c) / Gamma): per family of quanta and declared region, and per one-Node detector on a bound body alike, p_0 the mean of the region's Nodes' clocks under that family's read of the content, rounded once, (SUM p_0 + n div 2) div n, added to the carried remainder and divided once by Gamma, the whole intervals to the proper time and the remainder kept in the books; at a region in the vacuum p_0 = Gamma and the proper time is the board's tick, in a well it runs slower."""
    books, gamma = board.credit, board.world.node_clock
    if books.declaration is None:
        return
    for index in board.order:
        content = board.read(index, 1, 0)[0]
        clock = paces.clock_of(gamma, content)
        for detector in board.detectors:
            if detector.nodes is None or not (detector.declared or detector.levels):
                continue
            at = detector.nodes
            count = int(at.sum())
            total = int(np.sum(np.broadcast_to(clock, board.shape)[at], dtype=object))
            mean = int(division_forward(total, count, division_forward(count, 2, 0)[0])[0])
            own = books.clocks.setdefault((index, detector.name), [0, 0])
            whole, rest = division_forward(own[1] + mean, gamma, 0)
            own[0], own[1] = own[0] + int(whole), int(rest)


def listened(board: GameBoard) -> None:
    """The one-Node detectors' read of one interval, a read and no write (ALGEBRA.md, line 1 of the generic emitter/detector; the mathematician's 235 with the advisor's second, two hands): per family of quanta the record's first line's level now at the detector's Node (light the sum of its rows, `GameBoard.record`) appended to the window's level sequence in the books, the sequence the exact solve reads at the close (`read_levels`); nothing where the world declares no instrument."""
    books = board.credit
    if books.declaration is None:
        return
    for detector in board.detectors:
        if not detector.levels or detector.nodes is None:
            continue
        for index in board.order:
            level = int(board.record(index)[0].now[detector.nodes][0])
            books.sequences.setdefault((index, detector.name), []).append(level)


def read_levels(board: GameBoard) -> None:
    """The one-Node detectors' draw at the window's close (ALGEBRA.md, line 1 of the generic emitter/detector: the exact solve on the four reference sequences, the Gram determinants exact in Python's integers, the draw once at the window's close by the levels' shares; the mathematician's 235 with the advisor's second, two hands): per family of quanta whose level at the Node was not 0 throughout the window, the reference sequences at the declared pairs over the window at the scale derived from the width (`body_node.references_over`, `body_node.scale_of_the_width`), Cramer's rule on their Gram matrix (`body_node.solved`), the levels' shares as integer weights (`body_node.shares`: (a_n^2 + b_n^2) sin^2(omega_n) over the level's declared weight at the Node, the common factors cancelling) brought into the labels' unit (`in_the_unit`) and one draw of the instrument's generator among them; the credit line names the level realised with its index kept, the count moved 0 (the body's record stands; its re-lay in the realised level is by name) and the record's count as it stands, the detector's proper time and window index beside the board's tick; the sequences begin again."""
    books = board.credit
    for detector in board.detectors:
        if not detector.levels or detector.nodes is None:
            continue
        pairs = tuple(level.pair for level in detector.levels)
        weights = tuple(level.weight for level in detector.levels)
        for index in board.order:
            sequence = books.sequences.pop((index, detector.name), [])
            if not any(sequence):
                continue
            scale = scale_of_the_width(board.world.width)
            found = shares(
                solved(references_over(scale, pairs, len(sequence)), sequence)[1], pairs, weights
            )
            if sum(found) <= 0:
                continue
            unit = count_wall(board.families[index], board.world.quantum_action) ** 2
            pick = draw(board, in_the_unit(found, unit))
            if board.observer is None:
                continue
            name, left = board.families[index].name, books.counts[index]
            proper, window = (
                books.clocks.get((index, detector.name), [0, 0])[0],
                books.window_of(board.tick),
            )
            realised, kept = detector.levels[pick].name, [pick]
            board.observer(
                credit(
                    board.tick,
                    name,
                    detector.name,
                    window,
                    proper,
                    books.windows,
                    realised,
                    kept,
                    0,
                    left,
                )
            )


def in_the_unit(weights: list[int], unit: int) -> list[int]:
    """The levels' shares brought into the labels' unit for the draw, W_c^2 as the giving's draw uses it (`meeting.gave`), (Q_n x unit + total div 2) div total by the division act: the shares' ratios within the rounding of one part in the unit, their total within the width where the generator's state lives (the Gram determinants' squares stand beyond it)."""
    total = sum(weights)
    return [int(division_forward(w * unit, total, division_forward(total, 2, 0)[0])[0]) for w in weights]


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
    """The window's count at the end of an interval: where the world declares the instrument, the detectors' own clocks advanced (`clocked`), the one-Node detectors' level read (`listened`), one more interval elapsed, and at the window's length the instrument's draw and its click written (`credited`) and the one-Node detectors' draw by the exact solve (`read_levels`), the window counted among the closed and the count beginning again."""
    books = board.credit
    if books.declaration is None:
        return
    clocked(board)
    listened(board)
    books.elapsed += 1
    if books.elapsed == books.declaration.window:
        books.windows += 1
        credited(board)
        read_levels(board)
        books.elapsed = 0


def credited(board: GameBoard) -> None:
    """The click written on the GameBoard at a window's end, per family of quanta from the window's books, then the books emptied, the region detector's list of the one act (`meeting.click`, the first of its five lists): for a record of several parts the one draw through the root over the combinations of the sides' ports by the joint shares J (as the reader draws its combination), then at each side's one arrival Node (`written`, the Node drawn by the window's inflows per Node, the port realised and the parts it reads with a coefficient other than 0 named as kept in the credit line) the record at -1 as one item over the Nodes drawn, one quantum; for a record of one part the regions' window inflows floored at 0 are the shares, N = (their sum + W_rec div 2) div W_rec whole quanta in the record's own unit (`quanta_through`, `record_unit`), at most the count left, each drawn to a region by the shares and to one Node of it, one item each; the window's items written by the act in one list, the record's count down by one per quantum and its erasing front begun from every Node written where the count reaches 0; a record whose count stands at 0 is uncreditable and nothing draws from it, whatever its levels still show (the empty wave, a diagnostic, until the front reaches it); the draw and the write are the instrument's and no act of Rule3."""
    books = board.credit
    names = [detector.name for detector in board.detectors if detector.declared]
    for index in board.order:
        family = board.families[index]
        intake = {name: books.intake.pop((index, name), {}) for name in names}
        items: list[Item] = []
        if family.parts > 1:
            joint = books.joints.pop(index, {})
            if sum(joint.values()) <= 0 or books.counts[index] <= 0 or not books.sides:
                continue
            keys = sorted(joint)
            combination = keys[draw(board, [joint[key] for key in keys])]
            nodes: list[Node] = []
            for (name, ports), port in zip(books.sides, combination, strict=True):
                kept = [k for k, coefficient in enumerate(ports[port]) if coefficient != 0]
                nodes += written(board, index, name, intake[name], PORT_NAMES[port], kept, 1)
            items.append(Item(index, None, None, -1, tuple(nodes)))
        else:
            shares = [max(sum(intake[name].values()), 0) for name in names]
            if sum(shares) <= 0:
                continue
            for quantum in range(min(quanta_through(books, index, sum(shares)), books.counts[index])):
                name = names[draw(board, shares)]
                at = written(board, index, name, intake[name], None, [0], quantum + 1)
                items.append(Item(index, None, None, -1, tuple(at)))
        click(board, books.state, None, [1], [items])


def written(
    board: GameBoard,
    index: int,
    name: str,
    book: Intake,
    realised: str | None,
    kept: list[int],
    quantum: int,
) -> list[Node]:
    """The Node of one click at a region and its credit line: among the region's boundary Nodes the one the credited quantum entered through, drawn by the window's inflows per Node floored at 0 (none where nothing entered: no Node, no write); one credit line, its result the window, the detector's own proper time at the close and the index of the window closed (`clocked`, the detector's two clocks beside the board's tick, a diagnostic), the region, the port realised and the parts kept, the count moved 1 and the record's count left after this, the window's `quantum`-th, and no Node (the owner's words of 2026-10-02 and 2026-10-03: the detector gives no result for one Node, and the experiment reads the clicks' file alone); the write itself the act's (`meeting.click`, the face at that Node); returns the Node, none where nothing entered."""
    nodes = list(book)
    weights = [max(book[at], 0) for at in nodes]
    if sum(weights) <= 0:
        return []
    at = nodes[draw(board, weights)]
    books = board.credit
    left, window = books.counts[index] - quantum, books.window_of(board.tick)
    if board.observer is not None:
        family, proper = board.families[index].name, books.clocks.get((index, name), [0, 0])[0]
        board.observer(
            credit(board.tick, family, name, window, proper, books.windows, realised, kept, 1, left)
        )
    return [at]
