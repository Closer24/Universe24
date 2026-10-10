"""The credit, the click written on the lattice (features/click; ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision: after a click the paths are cancelled on the lattice, not in the clicks' books, Rule3 kept): where the world declares the `draw` (its window in intervals, its seed, its generator's multiplier and increment, `loader/draw.py`) the credit keeps the books of a window from the node_detectors' reports, the conserved form's own current through each boundary Node's front Ports, the plain current times the Link's factor Q_ij in the unit G^2 (`reports.weighted`; ALGEBRA.md #the-click-is-the-meeting, the credit's booking), summed over the window per family and region and, for a family of several parts, the joint share J per combination of the sides' ports accumulated from the parts' sums (the same numbers the click and parts lines carry), and at the window's end draws with its declared generator and writes its click at one Node, the loop's act from outside the Node as the lay and the receding face are, forward only; the record's count goes down by one per credited quantum, the run's accounting in the output, and at 0 the record is uncreditable, whatever its levels still show. The books are the credit's and stand at no Node; the Node knows no click and no family of clicks; a world without the key keeps empty books and runs as before bit for bit."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from math import gcd
from typing import TYPE_CHECKING

import numpy as np

from event_universe import growth, share
from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.emission import Emitter, Source
from event_universe.features.click import Face, drawn
from event_universe.front import Front
from event_universe.loader.derived import count_wall
from event_universe.loader.draw import Draw, Ports, ports_of
from event_universe.loader.keys import Node
from event_universe.meeting import Item, click_act, fan_momentum, unpaid
from event_universe.node_detector import NodeBooks, books_of, drawn_weights, piece_momentum
from event_universe.reports import PORT_NAMES, credit

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Intake = dict[Node, int]  # per boundary Node of a region, at the file's coordinates, the window's inflow
Joints = dict[
    tuple[int, ...], int
]  # per combination of the sides' ports (0 the +, 1 the -) the window's J
Sums = dict[str, list[list[int]]]  # per region the parts' level sums [now, before] of one interval
Clock = list[
    int
]  # a node_detector's own clock: its proper time in whole intervals and the remainder carried


@dataclass
class Books:
    """The credit's books: its declaration (None where the world declares none), the intervals elapsed in the window, the generator's state, the record's count per family of quanta, the count left to credit, the window's inflows per family and region per boundary Node in the unit G^2 (`booked`), the window's joint shares per family of several parts, the sides, the regions declaring a pattern with their two ports, in the file's order, the records at Nodes declared NodeDetectors with their own books (`meeting.NodeBooks`), the erasing fronts begun where a record's count reached 0 (`Front`, the family, the click's Node and its interval), the faces the click act presents, per interval (features/click, `Face`), the log the inverse presents again, the sources in time, the unit of one quantum of each record, W_rec, read once at the books' origin (`record_unit`), the records that held no count at the origin, whose unit is set at their first lay to the lay's own share and held from there (the advisor's word; `emission.emitted_quantum`), each declared region's own clock per family it reads (`Clock`, the proper time carried over the board's intervals, `clocked_regions`), the count of the windows closed, the node_detectors' event clock, and per family the deficit, the quanta taken from its record and written nowhere (`deficits`, the undepleted beam, `meeting.faced`; the board's share exceeds the books' count by it, printed in the books' line, `Lattice.books`), and per family the share its windows left unabsorbed (`unabsorbed`, keyed by the family of quanta as the counts are, one record per family in every shipped world, an account to be split by record where a world declares several records of one family; in the readers' labels' unit: the count's share at the record's first draw, down by every null window's shares, dropped when a quantum passes into or out of the record, so that a later reader's draw reads its share conditionally on the earlier windows' nulls, `meeting.absorbed`, `meeting.written`; ALGEBRA.md, The click writes on the lattice (7), the mathematician's line) with the denominator each unabsorbed share is kept in (`unabsorbed_units`, the closing bodies' norms' least common multiple at the draw that wrote it, read in another closing set's denominator by the division act, `unabsorbed_in`; ALGEBRA.md, The absorption, the draw (b)); Part F, the piece's p_a per axis read at the close from the arriving record's momentum terms and share at the region's Nodes, scaled to one count (`node_detector.piece_momentum`), into the credit line; Part G (both hands' lines of 2026-10-10, the click with two receivers), the emitters' book per light family (`emitters`, `emission.Emitter`: per emitting body the quanta it gave that still stand in the record and whether the recoil was paid at the lay, kept after the Source's span is spent until its count reaches 0; the file's lays register nothing), the weights of the one draw of the piece's source at a click (`meeting.recoiled`)."""

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
    unabsorbed: dict[int, int] = field(default_factory=dict)
    unabsorbed_units: dict[int, int] = field(default_factory=dict)
    emitters: dict[int, list[Emitter]] = field(default_factory=dict)

    def unabsorbed_in(self, drive: int, norms: list[int]) -> tuple[int, int]:
        """The one denominator of the bodies closing a drive's interval and the record's unabsorbed share read in it (ALGEBRA.md, The absorption, the draw (b); `meeting.absorbed`): the denominator the least common multiple of the bodies' norms, each the sum of its labels' squares, by the division act, so that each body's transfer share scales to it exactly; the unabsorbed share the count's at the record's first draw, and a share left by an earlier draw in another denominator (`unabsorbed_units`) brought to this one by the division act and kept in it from here; a body with no labels, its norm 0, has no transfer and cannot close, refused by name."""
        if min(norms) <= 0:
            raise ValueError("a body closing a drive's interval holds labels: its norm is above 0")
        unit = norms[0]
        for norm in norms[1:]:
            unit = int(division_forward(unit * norm, gcd(unit, norm), 0)[0])
        kept = self.unabsorbed.setdefault(drive, self.counts[drive] * unit)
        born = self.unabsorbed_units.setdefault(drive, unit)
        self.unabsorbed[drive] = share = int(division_forward(kept * unit, born, 0)[0])
        self.unabsorbed_units[drive] = unit
        return unit, share

    def account_ended(self, family: int) -> None:
        """The record's windows' account ends as a quantum passes into or out of it (`meeting.written`): its unabsorbed share and the denominator it is kept in dropped, to begin again at the count left."""
        self.unabsorbed.pop(family, None)
        self.unabsorbed_units.pop(family, None)

    def window_of(self, interval: int) -> list[int]:
        """The window closing at `interval`, [first, last], the declaration's length of intervals."""
        assert self.declaration is not None
        return [interval - self.declaration.window + 1, interval]

    @classmethod
    def of(cls, board: Lattice) -> Books:
        """The books at the start: every family of quanta's count its laid share in whole quanta (the books' origin read as a count), its unit of one quantum from the same two numbers (`record_unit`, held through the run; a record with no count at the origin named among `empty`, its unit set at its first lay), the generator at the declared seed, every other book empty."""
        found = board.world.draw
        counts = {index: counted(board, index, board.laid[index]) for index in board.order}
        sides = [(r.name, ports_of(r.basis, r.pattern)) for r in board.world.node_detectors if r.pattern]
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


def counted(board: Lattice, index: int, total: int | None) -> int:
    """A share in the current's units as whole quanta, (total + W_c div 2) div W_c by the division act (`share.quanta_of`), 0 where it is not read: the reading of the record's count."""
    wall = count_wall(board.families[index], board.world.quantum_action)
    return 0 if total is None else int(share.quanta_of(np.array([total], dtype=object), wall, object)[0])


def record_unit(board: Lattice, index: int, total: int | None, count: int) -> int:
    """The unit of one quantum of a record, W_rec, read and not declared (the advisor's line with the mathematician's second, two hands; the count's line, Q(z) = count x W_c sin omega for a monochromatic record): the record's share over the board at the books' origin over its count there, (total + count div 2) div count by the division act, read once and held through the run (a face removes one quantum's share with one count, the ratio unchanged; the roundings' drift moves it not); W_c where the books hold no count or no reading (nothing to credit), until a record empty at the origin is first laid, when its unit becomes the lay's own, W_c sin Omega for a quantum given at Omega (`emission.emitted_quantum`, `born_unit`), so a born quantum below the half-top energy is credited 1 and not 0. For a record laid by share with its count the share over W_c it is W_c within the lay's own rounding; for a born quantum of count 1 at Omega it is W_c sin Omega, the node_detector counting in the record's own quantum with no transition declared on any region."""
    wall = count_wall(board.families[index], board.world.quantum_action)
    if total is None or count <= 0:
        return wall
    return int(division_forward(total, count, division_forward(count, 2, 0)[0])[0])


def quanta_through(books: Books, index: int, inflow: int, link_unit: int) -> int:
    """The clicks a window's inflow is worth in the record's own unit: the inflow booked in the unit G^2 of the Link's factor (`booked`, `reports.weighted`), G the run's Link unit `link_unit`, over one quantum's unit W_rec G^2, (inflow + W_rec G^2 div 2) div W_rec G^2 by the division act (`record_unit`), one division at the window's close and no rounding per Link, the share's own rounding, the count the plain formula reads where no tension stood (ALGEBRA.md #the-click-is-the-meeting, the credit's booking); the cap by the count is the credit's."""
    unit = books.units[index] * link_unit * link_unit
    return int(division_forward(inflow, unit, division_forward(unit, 2, 0)[0])[0])


def clocked_regions(board: Lattice) -> None:
    """The node_detectors' own clocks, one interval (the advisor's derivation, the clock composed from the paces, with the mathematician's second: the clock is the Node's, a node_detector's proper interval per board interval at a Node of content c is p_0(c) / Gamma): per family of quanta and declared region, p_0 the mean of the region's Nodes' clocks under that family's read of the content, rounded once, (SUM p_0 + n div 2) div n, added to the carried remainder and divided once by Gamma, the whole intervals to the proper time and the remainder kept in the books; at a region in the vacuum p_0 = Gamma and the proper time is the board's interval, in a well it runs slower."""
    books, gamma = board.credit, board.world.node_clock
    if books.declaration is None:
        return
    for index in board.order:
        content = board.read(index, 1, 0)[0]
        clock = paces.clock_of(gamma, content)
        for node_detector in board.node_detectors:
            if not node_detector.declared or node_detector.nodes is None:
                continue
            at = node_detector.nodes
            count = int(at.sum())
            total = int(np.sum(np.broadcast_to(clock, board.shape)[at], dtype=object))
            mean = int(division_forward(total, count, division_forward(count, 2, 0)[0])[0])
            own = books.clocks.setdefault((index, node_detector.name), [0, 0])
            whole, rest = division_forward(own[1] + mean, gamma, 0)
            own[0], own[1] = own[0] + int(whole), int(rest)


def node_detector_nodes(board: Lattice) -> np.ndarray:
    """The declared NodeDetectors' Nodes: the union of the declared regions (every node_detector with its own positions, the faces' layer and the bodies' node_detectors aside, `NodeDetector.declared`), whose boundary is where the reports are read, so that what moves between two regions of one screen is not seen twice."""
    found = np.zeros(board.shape, dtype=bool)
    for node_detector in board.node_detectors:
        if node_detector.declared and node_detector.nodes is not None:
            found |= node_detector.nodes
    return found


def booked(board: Lattice, index: int, name: str, came: np.ndarray) -> None:
    """The book of a window's inflows: per family and declared region the conserved form's own current through each boundary Node's front Ports, each record's plain current times its Link's factor Q_ij in the unit G^2 (`reports.weighted`, `came` per Node; ALGEBRA.md #the-click-is-the-meeting, the credit's booking: the Link's factor squared the one weight, no rounding per Link) summed over the window's intervals, the Node at the file's coordinates; the shares of the draw of the one Node the click is written at and, over the regions, of the window's count (`quanta_through`); nothing where the world declares no draw."""
    if board.credit.declaration is None:
        return
    book = board.credit.intake.setdefault((index, name), {})
    for at in np.argwhere(came != 0):
        key = growth.declared(at, board.offset)
        book[key[0], key[1], key[2]] = book.get((key[0], key[1], key[2]), 0) + int(came[tuple(at)])


def joined(board: Lattice, index: int, sums: Sums) -> None:
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


def draw(board: Lattice, weights: list[int]) -> int:
    """One draw of the NodeDetector by its declared generator (features/click, `drawn`): the index drawn among the weights, the generator's state kept in the books, the modulus the width's own, 2^width."""
    books = board.credit
    assert books.declaration is not None
    found = books.declaration
    pick, books.state = drawn(
        books.state, found.multiplier, found.increment, board.world.width + 1, weights
    )
    return pick


def counted_windows(board: Lattice) -> None:
    """The window's count at the end of an interval: where the world declares the draw, the node_detectors' own clocks advanced (`clocked_regions`), one more interval elapsed, and at the window's length the NodeDetector's draw and its click written (`credited`), the window counted among the closed and the count beginning again."""
    books = board.credit
    if books.declaration is None:
        return
    clocked_regions(board)
    books.elapsed += 1
    if books.elapsed == books.declaration.window:
        books.windows += 1
        credited(board)
        books.elapsed = 0


def credited(board: Lattice) -> None:
    """The click written on the lattice at a window's end, per family of quanta from the window's books, then the books emptied, the region node_detector's list of the one act (`meeting.click_act`, the first of its five lists): for a record of several parts the one draw through the root over the combinations of the sides' ports by the joint shares J (as the reader draws its combination), then at each side's one arrival Node (`click_node`, the Node drawn by the window's inflows per Node, the port realised and the parts it reads with a coefficient other than 0 named as kept in the credit line) the record at -1 as one item over the Nodes drawn, one quantum; for a record of one part the regions' window inflows floored at 0, in the unit G^2 of the booking, give N = (their sum + W_rec G^2 div 2) div W_rec G^2 whole quanta in the record's own unit, one division at the close (`quanta_through`, `record_unit`), at most the count left, each drawn to a region by the shares, the inflows over G^2 once by the division act, the plain inflows bit for bit where no tension stood (`node_detector.drawn_weights`), and to one Node of it, one item each; the window's items written by the act in one list, the record's count down by one per quantum and its erasing front begun from every Node written where the count reaches 0; a record whose count stands at 0 is uncreditable and nothing draws from it, whatever its levels still show (the empty wave, a diagnostic, until the front reaches it); the draw and the write are the NodeDetectors' and no act of Rule3."""
    books = board.credit
    names = [node_detector.name for node_detector in board.node_detectors if node_detector.declared]
    regions = {d.name: d.nodes for d in board.node_detectors if d.declared and d.nodes is not None}
    for index in board.order:
        family = board.families[index]
        intake = {name: books.intake.pop((index, name), {}) for name in names}
        fan = list(fan_momentum(board, index))
        items: list[Item] = []
        if family.parts > 1:
            joint = books.joints.pop(index, {})
            if sum(joint.values()) <= 0 or books.counts[index] <= 0 or not books.sides:
                continue
            keys = sorted(joint)
            combination = keys[draw(board, [joint[key] for key in keys])]
            pieces = [piece_momentum(board, index, regions[name]) for name, _ports in books.sides]
            nodes: list[Node] = []
            for (name, ports), port, piece in zip(books.sides, combination, pieces, strict=True):
                kept = [k for k, coefficient in enumerate(ports[port]) if coefficient != 0]
                nodes += click_node(
                    board, index, name, intake[name], PORT_NAMES[port], kept, 1, piece, fan
                )
            items.append(Item(index, None, None, -1, tuple(nodes)))
        else:
            inflows = [max(sum(intake[name].values()), 0) for name in names]
            shares = drawn_weights(board, inflows)
            if sum(shares) <= 0:
                continue
            through = quanta_through(books, index, sum(inflows), board.unit)
            for quantum in range(min(through, books.counts[index])):
                name = names[draw(board, shares)]
                piece = piece_momentum(board, index, regions[name])
                at = click_node(board, index, name, intake[name], None, [0], quantum + 1, piece, fan)
                items.append(Item(index, None, None, -1, tuple(at)))
        click_act(board, books.state, None, [1], [items])


def click_node(
    board: Lattice,
    index: int,
    name: str,
    book: Intake,
    realised: str | None,
    kept: list[int],
    quantum: int,
    piece: list[int] | None = None,
    fan: list[int] | None = None,
) -> list[Node]:
    """The Node of one click at a region and its credit line: among the region's boundary Nodes the one the credited quantum entered through, drawn by the window's inflows per Node floored at 0 and over G^2 once by the division act (the booked current in the unit G^2, the plain inflows bit for bit where no tension stood, `node_detector.drawn_weights`; none where nothing entered: no Node, no write); one credit line, its result the window, the node_detector's own proper time at the close and the index of the window closed (`clocked_regions`, the node_detector's two clocks beside the board's interval, a diagnostic), the region, the port realised and the parts kept, the count moved 1 and the record's count left after this, the window's `quantum`-th, and no Node (the owner's words: the node_detector gives no result for one Node, and the experiment reads the clicks' file alone), and Part F's two readings, the piece's p_a per axis in T's unit, one count's momentum read at the close from the record's momentum terms and share at the region (`piece`, `node_detector.piece_momentum`) and the record's P_a over the board at the close (`fan`, `fan_momentum`); Part G (both hands' lines of 2026-10-10, the click with two receivers): after the Node, the piece's source drawn among the record's emitters by their outstanding quanta through the same generator (`draw`; one emitter, no draw), its part folded by -p_a at the click's tick by the same twist, and the credit line's `source`, `recoil` and the source's reading in `lost` (`meeting.recoiled` at a body's click); Part H, MUST 5 (both hands' lines of 2026-10-10 on the whole trial): a region taker has no part to twist, so it takes no +p_a of its own, and -p with no +p would break the law, so the region folds no source: the source is drawn and named all the same, its outstanding count down by one, `recoil` reads the one word `UNPAID_BY_REGION` and `lost` the reading `LOST_TO_REGION` (`meeting.unpaid`); OPEN by name: the region's +p, a declared region's record of the momentum it took, which no shipped screen or side carries; the write itself the act's (`meeting.click_act`, the face at that Node); returns the Node, none where nothing entered."""
    nodes = list(book)
    weights = drawn_weights(board, (book[at] for at in nodes))
    if sum(weights) <= 0:
        return []
    at = nodes[draw(board, weights)]
    books = board.credit
    left, window = books.counts[index] - quantum, books.window_of(board.interval)
    source: str | None
    recoil: str | None
    lost: list[str] | None
    source, recoil, lost = None, None, None
    if piece is not None:  # Part H, MUST 5: the region takes no +p and folds no source
        source, recoil, reading = unpaid(board, index, lambda shares: draw(board, shares))
        lost = [reading]
    if board.output is not None:
        family, proper = board.families[index].name, books.clocks.get((index, name), [0, 0])[0]
        proper_window = (window, proper, books.windows)
        board.output(
            credit(
                board.interval,
                family,
                name,
                *proper_window,
                realised,
                kept,
                1,
                left,
                None,
                None,
                None,
                piece,
                fan,
                None,
                lost,
                source,
                recoil,
            )
        )
    return [at]
