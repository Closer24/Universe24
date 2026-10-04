"""The credit, the click written on the GameBoard (features/click; ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision: after a click the paths are cancelled on the GameBoard, not in the clicks' books, Rule3 kept): where the world declares the `draw` (its window in intervals, its seed, its generator's multiplier and increment, `loader/draw.py`) the credit keeps the books of a window from the node_readers' reports, the conserved form's own current through each boundary Node's front Ports, the plain current times the Link's factor Q_ij in the unit G^2 (`reports.weighted`; ALGEBRA.md #the-click-is-the-meeting, the credit's booking), summed over the window per family and region and, for a family of several parts, the joint share J per combination of the sides' ports accumulated from the parts' sums (the same numbers the click and parts lines carry), and at the window's end draws with its declared generator and writes its click at one Node, the loop's act from outside the Node as the lay and the receding face are, forward only; the record's count goes down by one per credited quantum, the run's accounting in the output, and at 0 the record is uncreditable, whatever its levels still show. The books are the credit's and stand at no Node; the Node knows no click and no family of clicks; a world without the key keeps empty books and runs as before bit for bit."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from math import gcd
from typing import TYPE_CHECKING

import numpy as np

from event_universe import growth, share
from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.features.click import Face, drawn
from event_universe.front import Front
from event_universe.giving import Source
from event_universe.loader.derived import count_wall
from event_universe.loader.draw import Draw, Ports, ports_of
from event_universe.loader.keys import Node
from event_universe.meeting import Item, click_act
from event_universe.node_reader import NodeBooks, books_of, drawn_weights
from event_universe.reports import PORT_NAMES, credit

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard

Intake = dict[Node, int]  # per boundary Node of a region, at the file's coordinates, the window's inflow
Joints = dict[
    tuple[int, ...], int
]  # per combination of the sides' ports (0 the +, 1 the -) the window's J
Sums = dict[str, list[list[int]]]  # per region the parts' level sums [now, before] of one interval
Clock = list[
    int
]  # a node_reader's own clock: its proper time in whole intervals and the remainder carried


@dataclass
class Books:
    """The credit's books: its declaration (None where the world declares none), the intervals elapsed in the window, the generator's state, the record's count per family of quanta, the count left to credit, the window's inflows per family and region per boundary Node in the unit G^2 (`booked`), the window's joint shares per family of several parts, the sides, the regions declaring a pattern with their two ports, in the file's order, the records at Nodes declared NodeReaders with their own books (`meeting.NodeBooks`), the erasing fronts begun where a record's count reached 0 (`Front`, the family, the click's Node and its interval), the faces the click act presents, per interval (features/click, `Face`), the log the inverse presents again, the sources in time, the unit of one quantum of each record, W_rec, read once at the books' origin (`record_unit`), the records that held no count at the origin, whose unit is set at their first lay to the lay's own share and held from there (the advisor's word; `giving.given_quantum`), each declared region's own clock per family it reads (`Clock`, the proper time carried over the board's ticks, `clocked_regions`), the count of the windows closed, the node_readers' event clock, and per family the deficit, the quanta taken from its record and written nowhere (`deficits`, the undepleted beam, `meeting.faced`; the board's share exceeds the books' count by it, printed in the books' line, `GameBoard.books`), and per family the share its windows left untaken (`untaken`, keyed by the family of quanta as the counts are, one record per family in every shipped world, an account to be split by record where a world declares several records of one family; in the readers' labels' unit: the count's share at the record's first draw, down by every null window's shares, dropped when a quantum passes into or out of the record, so that a later reader's draw reads its share conditionally on the earlier windows' nulls, `meeting.took`, `meeting.written`; ALGEBRA.md, The click writes on the GameBoard (7), the mathematician's line) with the denominator each untaken share is kept in (`untaken_units`, the closing bodies' norms' least common multiple at the draw that wrote it, read in another closing set's denominator by the division act, `untaken_in`; ALGEBRA.md, The taking, the draw (b))."""

    declaration: Draw | None
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
    empty: set[int] = field(default_factory=set)
    clocks: dict[tuple[int, str], Clock] = field(default_factory=dict)
    windows: int = 0
    deficits: dict[int, int] = field(default_factory=dict)
    untaken: dict[int, int] = field(default_factory=dict)
    untaken_units: dict[int, int] = field(default_factory=dict)

    def untaken_in(self, drive: int, norms: list[int]) -> tuple[int, int]:
        """The one denominator of the bodies closing a drive's interval and the record's untaken share read in it (ALGEBRA.md, The taking, the draw (b); `meeting.took`): the denominator the least common multiple of the bodies' norms, each the sum of its labels' squares, by the division act, so that each body's transfer share scales to it exactly; the untaken share the count's at the record's first draw, and a share left by an earlier draw in another denominator (`untaken_units`) brought to this one by the division act and kept in it from here; a body with no labels, its norm 0, has no transfer and cannot close, refused by name."""
        if min(norms) <= 0:
            raise ValueError("a body closing a drive's interval holds labels: its norm is above 0")
        unit = norms[0]
        for norm in norms[1:]:
            unit = int(division_forward(unit * norm, gcd(unit, norm), 0)[0])
        kept = self.untaken.setdefault(drive, self.counts[drive] * unit)
        born = self.untaken_units.setdefault(drive, unit)
        self.untaken[drive] = share = int(division_forward(kept * unit, born, 0)[0])
        self.untaken_units[drive] = unit
        return unit, share

    def account_ended(self, family: int) -> None:
        """The record's windows' account ends as a quantum passes into or out of it (`meeting.written`): its untaken share and the denominator it is kept in dropped, to begin again at the count left."""
        self.untaken.pop(family, None)
        self.untaken_units.pop(family, None)

    def window_of(self, tick: int) -> list[int]:
        """The window closing at `tick`, [first, last], the declaration's length of intervals."""
        assert self.declaration is not None
        return [tick - self.declaration.window + 1, tick]

    @classmethod
    def of(cls, board: GameBoard) -> Books:
        """The books at the start: every family of quanta's count its laid share in whole quanta (the books' origin read as a count), its unit of one quantum from the same two numbers (`record_unit`, held through the run; a record with no count at the origin named among `empty`, its unit set at its first lay), the generator at the declared seed, every other book empty."""
        found = board.world.draw
        counts = {index: counted(board, index, board.laid[index]) for index in board.order}
        sides = [(r.name, ports_of(r.basis, r.pattern)) for r in board.world.node_readers if r.pattern]
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
            {index for index in board.order if counts[index] <= 0},
        )


def counted(board: GameBoard, index: int, total: int | None) -> int:
    """A share in the current's units as whole quanta, (total + W_c div 2) div W_c by the division act (`share.quanta_of`), 0 where it is not read: the reading of the record's count."""
    wall = count_wall(board.families[index], board.world.quantum_action)
    return 0 if total is None else int(share.quanta_of(np.array([total], dtype=object), wall, object)[0])


def record_unit(board: GameBoard, index: int, total: int | None, count: int) -> int:
    """The unit of one quantum of a record, W_rec, read and not declared (the advisor's line with the mathematician's second, two hands; the count's line, Q(z) = count x W_c sin omega for a monochromatic record): the record's share over the board at the books' origin over its count there, (total + count div 2) div count by the division act, read once and held through the run (a face removes one quantum's share with one count, the ratio unchanged; the roundings' drift moves it not); W_c where the books hold no count or no reading (nothing to credit), until a record empty at the origin is first laid, when its unit becomes the lay's own, W_c sin Omega for a quantum given at Omega (`giving.given_quantum`, `born_unit`), so a born quantum below the half-top energy is credited 1 and not 0. For a record laid by share with its count the share over W_c it is W_c within the lay's own rounding; for a born quantum of count 1 at Omega it is W_c sin Omega, the node_reader counting in the record's own quantum with no transition declared on any region."""
    wall = count_wall(board.families[index], board.world.quantum_action)
    if total is None or count <= 0:
        return wall
    return int(division_forward(total, count, division_forward(count, 2, 0)[0])[0])


def quanta_through(books: Books, index: int, inflow: int, link_unit: int) -> int:
    """The clicks a window's inflow is worth in the record's own unit: the inflow booked in the unit G^2 of the Link's factor (`booked`, `reports.weighted`), G the run's Link unit `link_unit`, over one quantum's unit W_rec G^2, (inflow + W_rec G^2 div 2) div W_rec G^2 by the division act (`record_unit`), one division at the window's close and no rounding per Link, the share's own rounding, the count the plain formula reads where no tension stood (ALGEBRA.md #the-click-is-the-meeting, the credit's booking); the cap by the count is the credit's."""
    unit = books.units[index] * link_unit * link_unit
    return int(division_forward(inflow, unit, division_forward(unit, 2, 0)[0])[0])


def clocked_regions(board: GameBoard) -> None:
    """The node_readers' own clocks, one interval (the advisor's derivation, the clock composed from the paces, with the mathematician's second: the clock is the Node's, a node_reader's proper interval per board tick at a Node of content c is p_0(c) / Gamma): per family of quanta and declared region, p_0 the mean of the region's Nodes' clocks under that family's read of the content, rounded once, (SUM p_0 + n div 2) div n, added to the carried remainder and divided once by Gamma, the whole intervals to the proper time and the remainder kept in the books; at a region in the vacuum p_0 = Gamma and the proper time is the board's tick, in a well it runs slower."""
    books, gamma = board.credit, board.world.node_clock
    if books.declaration is None:
        return
    for index in board.order:
        content = board.read(index, 1, 0)[0]
        clock = paces.clock_of(gamma, content)
        for node_reader in board.node_readers:
            if not node_reader.declared or node_reader.nodes is None:
                continue
            at = node_reader.nodes
            count = int(at.sum())
            total = int(np.sum(np.broadcast_to(clock, board.shape)[at], dtype=object))
            mean = int(division_forward(total, count, division_forward(count, 2, 0)[0])[0])
            own = books.clocks.setdefault((index, node_reader.name), [0, 0])
            whole, rest = division_forward(own[1] + mean, gamma, 0)
            own[0], own[1] = own[0] + int(whole), int(rest)


def node_reader_nodes(board: GameBoard) -> np.ndarray:
    """The declared NodeReaders' Nodes: the union of the declared regions (every node_reader with its own positions, the faces' layer and the bodies' node_readers aside, `NodeReader.declared`), whose boundary is where the reports are read, so that what moves between two regions of one screen is not seen twice."""
    found = np.zeros(board.shape, dtype=bool)
    for node_reader in board.node_readers:
        if node_reader.declared and node_reader.nodes is not None:
            found |= node_reader.nodes
    return found


def booked(board: GameBoard, index: int, name: str, came: np.ndarray) -> None:
    """The book of a window's inflows: per family and declared region the conserved form's own current through each boundary Node's front Ports, each record's plain current times its Link's factor Q_ij in the unit G^2 (`reports.weighted`, `came` per Node; ALGEBRA.md #the-click-is-the-meeting, the credit's booking: the Link's factor squared the one weight, no rounding per Link) summed over the window's intervals, the Node at the file's coordinates; the shares of the draw of the one Node the click is written at and, over the regions, of the window's count (`quanta_through`); nothing where the world declares no draw."""
    if board.credit.declaration is None:
        return
    book = board.credit.intake.setdefault((index, name), {})
    for at in np.argwhere(came != 0):
        key = growth.declared(at, board.offset)
        book[key[0], key[1], key[2]] = book.get((key[0], key[1], key[2]), 0) + int(came[tuple(at)])


def joined(board: GameBoard, index: int, sums: Sums) -> None:
    """The book of the meeting (ALGEBRA.md #the-click-is-the-meeting, the one form): per combination of the sides' ports the joint share J accumulated over the window on both members of the level pair from the sides' parts sums of one interval, J += (SUM_k c_k PROD_sides now_k)^2 + (SUM_k c_k PROD_sides before_k)^2, c_k the product over the sides of e_k at their ports, as the reader `tools/bell_gate.py` reads the same sums; nothing where the world declares no draw or no side."""
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
    """One draw of the NodeReader by its declared generator (features/click, `drawn`): the index drawn among the weights, the generator's state kept in the books, the modulus the width's own, 2^width."""
    books = board.credit
    assert books.declaration is not None
    found = books.declaration
    pick, books.state = drawn(
        books.state, found.multiplier, found.increment, board.world.width + 1, weights
    )
    return pick


def counted_windows(board: GameBoard) -> None:
    """The window's count at the end of an interval: where the world declares the draw, the node_readers' own clocks advanced (`clocked_regions`), one more interval elapsed, and at the window's length the NodeReader's draw and its click written (`credited`), the window counted among the closed and the count beginning again."""
    books = board.credit
    if books.declaration is None:
        return
    clocked_regions(board)
    books.elapsed += 1
    if books.elapsed == books.declaration.window:
        books.windows += 1
        credited(board)
        books.elapsed = 0


def credited(board: GameBoard) -> None:
    """The click written on the GameBoard at a window's end, per family of quanta from the window's books, then the books emptied, the region node_reader's list of the one act (`meeting.click_act`, the first of its five lists): for a record of several parts the one draw through the root over the combinations of the sides' ports by the joint shares J (as the reader draws its combination), then at each side's one arrival Node (`click_node`, the Node drawn by the window's inflows per Node, the port realised and the parts it reads with a coefficient other than 0 named as kept in the credit line) the record at -1 as one item over the Nodes drawn, one quantum; for a record of one part the regions' window inflows floored at 0, in the unit G^2 of the booking, give N = (their sum + W_rec G^2 div 2) div W_rec G^2 whole quanta in the record's own unit, one division at the close (`quanta_through`, `record_unit`), at most the count left, each drawn to a region by the shares, the inflows over G^2 once by the division act, the plain inflows bit for bit where no tension stood (`node_reader.drawn_weights`), and to one Node of it, one item each; the window's items written by the act in one list, the record's count down by one per quantum and its erasing front begun from every Node written where the count reaches 0; a record whose count stands at 0 is uncreditable and nothing draws from it, whatever its levels still show (the empty wave, a diagnostic, until the front reaches it); the draw and the write are the NodeReaders' and no act of Rule3."""
    books = board.credit
    names = [node_reader.name for node_reader in board.node_readers if node_reader.declared]
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
                nodes += click_node(board, index, name, intake[name], PORT_NAMES[port], kept, 1)
            items.append(Item(index, None, None, -1, tuple(nodes)))
        else:
            inflows = [max(sum(intake[name].values()), 0) for name in names]
            shares = drawn_weights(board, inflows)
            if sum(shares) <= 0:
                continue
            through = quanta_through(books, index, sum(inflows), board.unit)
            for quantum in range(min(through, books.counts[index])):
                name = names[draw(board, shares)]
                at = click_node(board, index, name, intake[name], None, [0], quantum + 1)
                items.append(Item(index, None, None, -1, tuple(at)))
        click_act(board, books.state, None, [1], [items])


def click_node(
    board: GameBoard,
    index: int,
    name: str,
    book: Intake,
    realised: str | None,
    kept: list[int],
    quantum: int,
) -> list[Node]:
    """The Node of one click at a region and its credit line: among the region's boundary Nodes the one the credited quantum entered through, drawn by the window's inflows per Node floored at 0 and over G^2 once by the division act (the booked current in the unit G^2, the plain inflows bit for bit where no tension stood, `node_reader.drawn_weights`; none where nothing entered: no Node, no write); one credit line, its result the window, the node_reader's own proper time at the close and the index of the window closed (`clocked_regions`, the node_reader's two clocks beside the board's tick, a diagnostic), the region, the port realised and the parts kept, the count moved 1 and the record's count left after this, the window's `quantum`-th, and no Node (the owner's words: the node_reader gives no result for one Node, and the experiment reads the clicks' file alone); the write itself the act's (`meeting.click_act`, the face at that Node); returns the Node, none where nothing entered."""
    nodes = list(book)
    weights = drawn_weights(board, (book[at] for at in nodes))
    if sum(weights) <= 0:
        return []
    at = nodes[draw(board, weights)]
    books = board.credit
    left, window = books.counts[index] - quantum, books.window_of(board.tick)
    if board.output is not None:
        family, proper = board.families[index].name, books.clocks.get((index, name), [0, 0])[0]
        board.output(
            credit(board.tick, family, name, window, proper, books.windows, realised, kept, 1, left)
        )
    return [at]
