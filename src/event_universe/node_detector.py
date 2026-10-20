"""The reader's region (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment; the mathematician's hand with the advisor's second, two hands): what a reader declared over a connected region (two Nodes or more with Nodes alone, one Node or more with a record of its own, the relation seen from its two ends) reads and books without writing a level: its books (`NodeBooks`, `books_of`), the lay's amplitudes in the weights' proportion and the record's norm, the arriving record's level projected on the reader's normalised mode (`arriving`), the window's inflow booked per Node (`booked_inflow`, `booked_inflows`), the dark and the reader's own clock over the region (`dark`, `own_clock`), the outcome's draw and the one Node a write is laid at, the absorption's by the inflow booked and the emission's and the conversion's by the record's share at the body's Nodes as the board holds it at the close (`picked`, `drawn_node`, `share_weights`, `hole_node`), and the click line that names no Node (`reported`); the writes themselves stay in `meeting.py`."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import node, readings, records, share
from event_universe.core import paces
from event_universe.core.ports import AXES, PORTS, SIDES, Wrap
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.digits import read_of
from event_universe.features.click import drawn_from, spread, squared
from event_universe.loader.derived import count_wall, quanta_records, row_of
from event_universe.loader.keys import Node
from event_universe.loader.node_detector_declaration import NodeDetectorDeclaration, Transition
from event_universe.loader.world import BodyRow
from event_universe.reports import BODY, credit, front, weighted
from event_universe.resonance import Reference, references_of, scale_of

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Read = tuple[
    tuple[np.ndarray, ...], node.Factors, np.ndarray
]  # one record's current through each Port, the factor of each of its six Links and its share at the readers' Nodes
Weighed = dict[
    int, list[Read]
]  # per family of quanta, per record, its read at the pair the step starts from


@dataclass
class Passage:
    """A record's passage through a region over the window (the click's plan, C4, the window-booked piece; Part F2's line, the region's lattice momentum over its share scaled to one count, taken over the window and not at one instant): the record's lattice momentum terms per axis at the region's Nodes (`readings.momentum_of` over the mask, `currents.momentum_terms`, in the unit num of the current's weight) summed over the intervals, and its share there (`Lattice.share_of`) summed, booked each interval beside the inflow from the same read at the pair the step starts from (`weighed_currents`, `booked_inflows`, `credit.booked`) and begun again at the window's close; the piece is their ratio at the close (`piece_momentum`), exact for a monochromatic record and the form-weighted mean for a packet, so that the piece does not depend on where the packet stands when the window closes."""

    momenta: list[int] = field(default_factory=lambda: [0] * AXES)
    share: int = 0

    def booked(self, at: np.ndarray, read: Sequence[Read]) -> None:
        """One interval's terms added at the region's Nodes `at` from the family's records' read at the pair the step starts from, the inflow's own (`weighed_currents`): per axis the current through each Node's -a Port less the current through its +a Port, the term of the lattice momentum (`currents.momentum_terms`, `readings.momentum_of`), and the share there."""
        for through, _factors, shares in read:
            for axis in range(AXES):
                minus, plus = through[2 * axis + 1][at], through[2 * axis][at]
                self.momenta[axis] += int((minus - plus).sum(dtype=object))
            self.share += int(shares[at].sum(dtype=object))


@dataclass
class NodeBooks:
    """The books of a record declared a NodeDetector over a region (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment): the declaration's number among the world's `bodies`, the record's family and its record number, its Nodes with the lay's weights (the weights' proportion), its declaration, the part carrying the count, the counts per part, the labels, the intervals elapsed in the window and the lit ones among them (`lit`, the span of the emission's draw at the window's close, the dark intervals drawn at their own grain as they pass, `meeting.jumped`), the two reference records per transition, the windows closed and its own clock; `amplitudes` the lay's amplitude of one quantum at each Node, (the largest x with x^2 <= A^2 w_i div SUM w), `norm` the record's amplitude over the region, (the largest x with x^2 <= SUM A_i^2), the mode's norm, `intake` per arriving family the window's inflow through each Node's front Ports, per Node and per Port, the conserved form's own current in the unit G^2 (`booked_inflow`), the absorption's Node's draw weights by their sums and the hole's Port set by the Ports (`arrival_ports`), `passages` per arriving family its momentum terms and its share at the region summed over the window, the piece's two sums (`Passage`, C4), and `shares` per transition out of the part, at the window's close, its own transfer share, the weight of its absorption (`meeting.turned_labels`, `lists.absorption`). `carried`, the hop's remainders per label, one per part, kept between windows and cleared with the labels at the re-lay (`resonance.hopped`, Part C); `left`, the number the click's read of the board left after the body's last draw of the interval, None before its first (`picked`, emptied every interval, `meeting.jumped`). Part F (the two hands' lines of 2026-10-09): the last click's four readings for its credit line, `piece` the piece's p_a in T's unit, read at the close from the arriving record's momentum terms and share at the region's Nodes (`piece_momentum`), `fan` the arriving record's P_a over the board at the click, `twist` the write's n_a per axis, `shortfall` what the fold could not give per axis, s_a = |p_a| - gain_a at or above 0 (the click's plan, C3; `twist.twisted`), and `lost` the readings of who lost it; Part G (both hands' lines of 2026-10-10, the click with two receivers): `source`, the piece's source drawn among the light's emitters by their outstanding quanta, and `recoil`, the source's p per axis, the fold given its part by the same twist (`twist.recoiled`), or on the emission's own line the directed packet's recoil paid at the lay (`act.written`)."""

    number: int
    index: int
    record: int
    nodes: tuple[Node, ...]
    weights: tuple[int, ...]
    declared: NodeDetectorDeclaration
    part: int
    counts: list[int]
    labels: list[int]
    elapsed: int
    references: list[Reference]
    windows: int = 0
    lit: int = 0
    clock: list[int] = field(default_factory=lambda: [0, 0])
    amplitudes: tuple[int, ...] = ()
    norm: int = 1
    intake: dict[int, list[list[int]]] = field(default_factory=dict)
    passages: dict[int, Passage] = field(default_factory=dict)
    shares: dict[Transition, int] = field(default_factory=dict)
    carried: list[int] = field(default_factory=list)
    piece: list[int] | None = None
    fan: list[int] | None = None
    twist: list[int] | None = None
    shortfall: list[int] | None = None  # C3: s_a = |p_a| - gain_a per axis, at or above 0
    lost: list[str] | None = None
    source: str | None = None  # Part G: the piece's source, `body n` or the lay (`twist.recoiled`)
    recoil: list[int] | None = (
        None  # Part G: the source's p per axis, the fold given (`twist.folded_source`)
    )
    left: int | None = (
        None  # the click's read of the board: the number left within the interval (`picked`)
    )


def books_of(board: Lattice) -> list[NodeBooks]:
    """The books of every record declared a NodeDetector at a Node, in the world's order: its number among `bodies`, its family and record, its one Node, its declaration, the part carrying the count, the counts per part, the labels at their counts in the count's units and the window begun; the scale of its reference records from the declared window, or from the run's intervals where its window is bounded by a probe's lays (no window longer than the run; one interval the least)."""
    found = []
    for number, (record, row) in enumerate(board.laid_rows()):
        if not isinstance(row, BodyRow) or row.detector is None or row.detector.draw is None:
            continue
        parted = list(row.detector.counts)
        wall = count_wall(board.families[row.family], board.world.quantum_action)
        part = max(range(len(parted)), key=lambda k: parted[k])
        labels = [count * wall for count in parted]
        draw = row.detector.draw
        longest = draw.window if draw.window is not None else max(board.world.intervals, 1)
        scale = scale_of(board.world.width, board.world.amplitude_bound, longest)
        references = references_of(scale, row.detector.transitions)
        square, total = (
            squared(1, board.world.quantum_action, board.families[row.family].pair),
            sum(row.counts),
        )
        amplitudes = tuple(spread(square, (weight, total)) for weight in row.counts)
        norm = max(largest_below(sum(a * a for a in amplitudes)), 1)
        found.append(
            NodeBooks(
                number,
                row.family,
                record,
                row.nodes,
                row.counts,
                row.detector,
                part,
                parted,
                labels,
                0,
                references,
                amplitudes=amplitudes,
                norm=norm,
            )
        )
    return found


def arriving(board: Lattice, books: NodeBooks, drive: int) -> int:
    """The arriving record's level read into the reader's resonant turn: its level at each of the NodeDetector's Nodes, the level now, projected on the reader's own normalised mode, SUM_i d_i A_i div A with A_i the lay's amplitude of one quantum at the Node and A = (the largest x with x^2 <= SUM A_i^2) (`NodeBooks.amplitudes`, `norm`), rounded half up by the division act: the meeting is bilinear in the two records at each Node and the region's turn is the sum of the Nodes' meetings over the record's norm, the drive's level itself at one Node and (SUM_i d_i) / n^(1/2) over n Nodes in the equal lay (the mathematician's hand with the advisor's second, two hands: the level sum over-weights by n^(1/2), the boundary inflow is quadratic in the drive and turns no phase); a drive whose phase runs along the region carries the form factor of a body of that size. A holder of the sign's time level is summed over every row but the record's own (`records.row_levels`, light), a family of quanta's first line's level otherwise."""
    family, lines = board.families[drive], board.states[drive].lines
    if family.wronskian:
        own = row_of(board.families, books.index, books.record)
        levels = np.asarray(records.row_levels(family, lines, 0, 1, own))
    else:
        levels = lines[0].now
    total = sum(
        int(levels[tuple(np.add(at, board.offset))]) * amplitude
        for at, amplitude in zip(books.nodes, books.amplitudes, strict=True)
    )
    half = division_forward(books.norm, 2, 0)[0]
    size = int(division_forward(abs(total), books.norm, half)[0])
    return size if total >= 0 else -size


def booked_inflow(board: Lattice, books: NodeBooks, drive: int, came: Sequence[Any]) -> None:
    """The reader's book of a window's inflows per Node and per Port (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment; the mathematician's hand with the advisor's second, two hands, one rule for the one kind): the arriving family's conserved form's own current through each of the NodeDetector's Nodes' front Ports this interval, the plain current times the Link's factor Q_ij in the unit G^2 (`reports.weighted`, per Port, the same read as the credit's `booked`; ALGEBRA.md #the-click-is-the-meeting, the credit's booking) added to the window's sum at that Node and Port, the sums the weights the absorption's Node is drawn by at the close, over G^2 once (`drawn_weights`), the Node the quantum entered through, and the Ports its face set (`arrival_ports`); emptied at the window's close (`jumped`)."""
    book = books.intake.setdefault(drive, [[0] * PORTS for _at in books.nodes])
    for index, at in enumerate(books.nodes):
        here = tuple(np.add(at, board.offset))
        for port, through in enumerate(came):
            book[index][port] += int(through[here])


def piece_momentum(board: Lattice, index: int, passage: Passage) -> list[int]:
    """The piece's momentum p_a per axis in T's unit, the momentum one credited count of the arriving record deposits (Part F2; both hands' correction of Part F, 2026-10-09, the advisor's 6085442608 and the mathematician's 6085486079: the faces' throughput summed over a window is no momentum, the sin k cancels in it; the piece is the region's lattice momentum over its share, scaled to one count; the click's plan, C4: the ratio booked over the window and not read at one instant): p_a = (SUM_t P_a(region, t) x W_rec + h) div (num x SUM_t Q(region, t)), h = (num x SUM_t Q) div 2, the sums the record's passage through the region over the window (`Passage`: the momentum terms at the region's Nodes and the share there, booked each interval beside the inflow, `readings.momentum_of`, `Lattice.share_of`) and W_rec the unit of one credited count (`credit.Books.units`, `record_unit`), one division at the close, rounded half up on the magnitude with the sign after (kind D in the acts table, as `credit.quanta_through` divides once), exact for a monochromatic record, whose ratio is constant, and the form-weighted mean over the passage for a packet, so that the piece deposited is one count's whatever fraction of the packet stands in the region at the close and whichever unit the record holds: one quantum of action (SUM A^2 sin omega = T) at the wave number k carries 2 T sin k in this normalisation (46,341 at k = pi / 4), a count of W_c carries 2 T sin k / sin omega, and a record whose count holds several packets carries their action's worth at the region's own wave number; the sign that of +k, a piece entering from the +a side carries p_a below 0; 0 where nothing passed."""
    weight = board.families[index].pair[0]
    unit = board.credit.units[index]
    wall = weight * passage.share
    if wall <= 0:
        return [0] * AXES
    half = division_forward(wall, 2, 0)[0]
    found = []
    for value in passage.momenta:
        size = int(division_forward(abs(int(value)) * unit, wall, half)[0])
        found.append(size if value >= 0 else -size)
    return found


def sourcing(board: Lattice, books: NodeBooks) -> set[int]:
    """The families a reader is dark to as their giver (the click's plan, C5, dark to its own source; its reach by the lay's end on 2026-10-19, the atom branch, the cold reader's change (a) with the reader's fix): the families it is giving a source in time to while that source has intervals left (`credit.Books.sources`, `emission.Source.emitter`), and, where its lay of the family has an end (`Rate.ended`, the window rule's property: an open board, the record departing, the wake no light to take back), every light family in which quanta it gave still stand in the record (`credit.Books.emitters`, `emission.Emitter.outstanding`, kept until a click draws the body as the piece's source and the count reaches 0, `twist.drawn_emitter`); where the lay has no end (a periodic board, the quantum circulating as in a cavity) the first line alone, the body released at the span's end; its transitions read none of them, no window, no turn and no hole from a quantum it gave (L780, a quantum from outside; nature: an atom does not absorb the photon it is emitting); on the narrower line alone a body on an open chain read its own train's wake once the source's span was spent and took its own quantum back (chain_detuned, seed 25, 215, a finding by name), and the emitter of a directed packet was lit by it at the lay; a read of the books and of the lay's end, no geometry of the board's axes, symmetric under the 48 by construction."""
    departing = {rate.light for rate in books.declared.rates if rate.ended}
    given = {
        f
        for f, book in board.credit.emitters.items()
        if f in departing and any(e.body == books.number and e.outstanding for e in book)
    }
    return given | {source.family for source in board.credit.sources if source.emitter == books.number}


def dark(board: Lattice, books: NodeBooks, sourced: set[int]) -> bool:
    """A reader with no arriving record at its Nodes this interval: both levels, now and before, of every family its transitions name, its own sources' families `sourced` aside (`sourcing`, read once per body per interval by the caller, C5), sum to 0 over the region at every Node, so no window stands and the emission\'s grain is the interval; a reader naming no drive is never dark, its window its own clock's (the conversion's), and a declared window opens at the first lit interval and closes its length after it, a window bounded by a probe's lays counting from its last close as before (the click's plan, C2, the hybrid window: the detector integrates over the pulse, `meeting.jumped`)."""
    if not books.declared.transitions:
        return False
    turning = {t.drive for t in books.declared.transitions if t.leaves != t.enters} - sourced
    for drive in sorted(turning):
        family, lines = board.families[drive], board.states[drive].lines
        own = row_of(board.families, books.index, books.record)
        for side in (1, -1):
            if family.wronskian:
                levels = np.asarray(records.row_levels(family, lines, 0, side, own))
            else:
                levels = lines[0].now if side == 1 else lines[0].before
            if any(int(levels[tuple(np.add(at, board.offset))]) for at in books.nodes):
                return False
    return True


def own_clock(board: Lattice, books: NodeBooks) -> int:
    """The reader's own clock, the composed clock p_0 under its record's read of the content (`paces.clock_of`) at each of its Nodes, their mean by the division act with the half carry (as a region's clock is read, `credit.clocked_regions`): Gamma in the vacuum and below it in a well, the number the turn per proper interval and the dark's hazard read."""
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


def clock_advanced(board: Lattice, books: NodeBooks) -> None:
    """The body's own clock, one interval (the advisor's derivation, the clock composed from the paces, with the mathematician's second; the two hands' click line of the pulsed gate): its clock p_0 at its Node (`own_clock`) added to the carried remainder and divided once by Gamma, the whole intervals to its proper time and the remainder kept, as the credit keeps a region's (`credit.clocked_regions`); the board's interval in the vacuum, slower in a well."""
    whole, rest = division_forward(books.clock[1] + own_clock(board, books), board.world.node_clock, 0)
    books.clock[0], books.clock[1] = books.clock[0] + int(whole), int(rest)


def picked(board: Lattice, books: NodeBooks, weights: list[int]) -> int:
    """A body's draw, the click's read of the board at the body's Nodes (`digits.read_of`, `features/click.drawn_from`; ALGEBRA.md, The click's read of the board): the body's first draw of the interval reads the digits of the records it reads, the arriving records' (its transitions' drives, in the declared order) first and its own after, at its Nodes, into the number left (`NodeBooks.left`, emptied every interval, `meeting.jumped`), and every draw of the interval is one division act on it, the outcome of the click act (`act.click`), the Node of the write (`drawn_node`) and the piece's source (`act.parted`) alike, the remainder the pick and the quotient the number left; one weight consumes nothing; the lower index on a tie."""
    label = f"the body {books.number} of {board.families[books.index].name!r} at the interval {board.interval}"
    if books.left is None:
        drives = list(dict.fromkeys(t.drive for t in books.declared.transitions))
        books.left = read_of(board, [*drives, books.index], board.mask(books.nodes), label)
    pick, books.left = drawn_from(books.left, weights, label)
    return pick


def credit_draw(board: Lattice, index: int, weights: list[int], side: str | None = None) -> int:
    """The region NodeDetectors' draw of a place, the click's read of the board at the regions' Nodes (`digits.read_of`, `features/click.drawn_from`; ALGEBRA.md, The click's read of the board): a side of a record of several parts (`side`, the region's name) reads the record's digits at its own region at its first draw of the close, before its write, into the number left (`credit.Books.left`, per record and side, emptied at the close, `meeting.closed`), and a record of one part reads its digits at the union of the declared regions' Nodes (`node_detector_nodes`) at the first draw of the close; every later draw of the close is one division act on the number left, the side's port by its own second moments (`lists.readings`), the region by the window's shares, the boundary Node by the inflows per Node and the piece's source by the emitters' counts (`lists.region`, `lists.credited_node`), the remainder the pick and the quotient the number left; one weight consumes nothing."""
    books, family = board.credit, board.families[index]
    label = f"{'the regions' if side is None else f'the side {side!r}'} of {family.name!r} at the interval {board.interval}"
    if (index, side) not in books.left:
        at = (
            node_detector_nodes(board)
            if side is None
            else next(d.nodes for d in board.node_detectors if d.name == side)
        )
        assert at is not None  # a side is a declared region with its Nodes
        books.left[(index, side)] = read_of(board, [index], at, label)
    pick, books.left[(index, side)] = drawn_from(books.left[(index, side)], weights, label)
    return pick


def drawn_node(board: Lattice, books: NodeBooks, weights: list[int]) -> Node:
    """The one Node of the region a write is laid at, drawn by `weights` over the NodeDetector's Nodes by the body's read of the board (`picked`; ALGEBRA.md, The NodeDetector is one declaration kind for every experiment: the write of a click is at one Node of the region, the absorption's by the inflow booked, `hole_node`, the emission's and the conversion's by the record's share at the body's Nodes as the board holds it at the close, `share_weights`, the share at a Node a lattice reading and no measurement); the file's lay weights enter no draw and stand alone where every weight is 0."""
    found = weights if sum(weights) > 0 else list(books.weights)
    return books.nodes[picked(board, books, found)]


def drawn_weights(board: Lattice, inflows: Iterable[int]) -> list[int]:
    """The draw's weights from the books' inflows booked in the unit G^2 (`booked_inflow`, `credit.booked`): each floored at 0 and divided once at the close by G^2 by the division act, the current's units the draw is made in (features/click, `drawn_from`: the pick the residue of the read's number by the weights' total on the cumulative weights, so the weights' ratios realise the draw and their one rounding at the close is part of the realisation), the plain inflows bit for bit where no tension stood and the draw's realisation with them (ALGEBRA.md #the-click-is-the-meeting, the credit's booking: every reading at the vacuum's paces unchanged bit for bit), the law's ratios under tension; one division at the close and none per Link, the count's own division by W_rec G^2 beside it (`credit.quanta_through`)."""
    square = board.unit * board.unit
    return [int(division_forward(max(int(inflow), 0), square, 0)[0]) for inflow in inflows]


def share_weights(board: Lattice, books: NodeBooks) -> list[int]:
    """The emission's and the conversion's draw weights (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment: the emission's whole quantum laid at the Node drawn by its own record's share over its Nodes; the mathematician's words, #1793, A2 of the alignment audit): the record's family's share at each of the body's Nodes as the board holds it at the close, `Lattice.share_of` read once at the body's Nodes in the current's units, a lattice reading and no measurement, each floored at 0 as `drawn_weights` floors the inflows; the file's lay weights enter no draw and stand alone where every share is 0, nothing standing at the Nodes, so that a draw stays possible."""
    found = board.share_of(books.index, 1, board.mask(books.nodes))[0]
    shares = [max(int(found[tuple(np.add(at, board.offset))]), 0) for at in books.nodes]
    return shares if sum(shares) > 0 else list(books.weights)


def arrival_ports(booked: Sequence[int]) -> tuple[int, ...]:
    """The Ports a quantum entered a Node by, read from the window's inflow booked per Port at that Node (the click's plan, C6 (i): nature names no axis; `booked_inflow`, `credit.booked`): per axis the Port of the larger booked inflow, the arrival's side, and both Ports where the two tie with inflow (the quantum came through both, a tied axis; none where the axis carries no inflow), the set within the wall's bound or empty decided by `face_ports`, so the hole's remainder stays below one read coefficient (features/click, `presented`); the set maps to its image under the cube's symmetries and the one value presented on it is the same integer; a set empty on every axis, a standing wave with no side, refuses the hole by name at the step."""
    found = []
    for axis in range(AXES):
        plus, minus = booked[SIDES * axis], booked[SIDES * axis + 1]
        if plus != minus:
            found.append(SIDES * axis if plus > minus else SIDES * axis + 1)
        elif plus > 0:  # a tied axis with inflow: the quantum came through both its Ports
            found.extend((SIDES * axis, SIDES * axis + 1))
    return tuple(found)


def face_ports(board: Lattice, index: int, at: Node, booked: Sequence[int]) -> tuple[int, ...]:
    """The hole's face set at a Node (the click's plan, C6 (i); the cold reader's re-fix of 2026-10-19, the Boss's decision under the owner's word, generic and right): the Ports the quantum entered by (`arrival_ports`, a sided axis's one Port and a tied axis's two) where the set's read coefficients at the Node sum to the wall at most, SUM over the set of R_p <= w, the window in which the face value reaches the target exactly (ALGEBRA.md, The one act as a face at the Node's Ports: one or two sided axes, one tied axis alone or beside a sided one for light's R = w / 3); above the wall (two or three tied axes, four to six Ports) the empty set, the booked path: the quantum taken in the books, the Node not faced and its levels standing, the credit line reading `NO_SIDE` (`act.written`, `lists.credited_node`); the rule's integers the record's own read at the Node (`node.rule_of`), the detector's side and nothing at the Node."""
    ports = arrival_ports(booked)
    content, factors = board.read(index)
    rule = node.rule_of(board.families[index], board.world.node_clock, content, factors, board.unit)
    here = tuple(int(v) for v in np.add(at, board.offset))
    reaches = [int(np.asarray(read)[here]) if np.ndim(read) else int(read) for read in rule.reaches]
    return ports if sum(reaches[p] for p in ports) <= int(rule.wall) else ()


def hole_node(board: Lattice, books: NodeBooks, drive: int) -> tuple[Node, tuple[int, ...]]:
    """The absorption's Node and its face set: the Node drawn by the arriving record's inflow booked through each of the NodeDetector's Nodes' front Ports over the window, the Ports' sums (`booked_inflow`, floored at 0 and over G^2 once, `drawn_weights`), the Node the quantum entered through, as the credit draws it for a reader of the field's record, one rule for the one kind (the mathematician's hand, the advisor's hand, two hands); the lay's weights where nothing entered; the Ports the quantum entered that Node by from the same book (`arrival_ports`), the hole's two faces written there at them; drawn after the outcome, for the realised write alone."""
    booked = books.intake.get(drive, [[0] * PORTS for _at in books.nodes])
    at = drawn_node(board, books, drawn_weights(board, [sum(through) for through in booked]))
    return at, face_ports(board, drive, at, booked[books.nodes.index(at)])


def reported(
    board: Lattice,
    books: NodeBooks,
    parts: tuple[int, int],
    exchanged: tuple[int | None, int | None],
    count: int = 1,
) -> None:
    """The click line of a record's click (`reports.credit`, the one click line kind of every reader; ALGEBRA.md, The NodeDetector is one declaration kind for every experiment: never a Node): the reader `body n` by its number, the `parts` realised and left by their declared names (`realised` the part after, `before` the part before), the families `exchanged`, the one taken from and the one given to (None where none), the count moved, 1 for a click and 0 for the null window's write, the count left in the books of the family exchanged (None where none), the window's intervals [first, last], the body's own proper time at the close and the index of the window closed (its books' clock and windows); labelled the node_detector's where a `quantum` passed and a diagnostic for the null window's write; the Node written stands in the `lay` and `face` lines beside it and here nowhere; Part F: the piece's p_a, the arriving record's P_a over the board, the write's twist n_a and what it could not give, the books' four readings of the click (`NodeBooks.piece`, `fan`, `twist`, `lost`), None each where the click read none; Part G: the piece's source and the source's recoil (`NodeBooks.source`, `recoil`)."""
    if board.output is None:
        return
    names, families = books.declared.names, board.families
    window = [
        board.interval - max(books.elapsed, 1) + 1,
        board.interval,
    ]  # a dark draw: its own interval
    absorbed, light = (families[k].name if k is not None else None for k in exchanged)
    moved = next((k for k in exchanged if k is not None), None)
    left = board.credit.counts[moved] if moved is not None else None
    name, reader, own = families[books.index].name, f"{BODY} {books.number}", books.clock[0]
    after, before = names[parts[0]], names[parts[1]]
    line = credit(
        board.interval,
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
        absorbed,
        light,
        books.piece,
        books.fan,
        books.twist,
        books.shortfall,
        books.lost,
        books.source,
        books.recoil,
    )
    board.output(line)


def node_detector_nodes(board: Lattice) -> np.ndarray:
    """The declared NodeDetectors' Nodes: the union of the declared regions (every node_detector with its own positions, the faces' layer and the bodies' node_detectors aside, `NodeDetector.declared`), the Nodes the credit's bookings read (`Lattice.report`)."""
    found = np.zeros(board.shape, dtype=bool)
    for node_detector in board.node_detectors:
        if node_detector.declared and node_detector.nodes is not None:
            found |= node_detector.nodes
    return found


def weighed_currents(board: Lattice) -> Weighed:
    """Every record of quanta's read for the bookings at the pair the step starts from, once per interval: its current through each Port at every Node (`readings.currents_of`, as `Lattice.currents` reads it, per record) with the factor Q_ij of each of its six Links in the unit G^2 (`Lattice.read`, the record's read with the world's cuts), by which the credit books the conserved form's own current through a region's front Ports (`reports.weighted`, `credit.booked`, `booked_inflows`), and its share at the readers' Nodes, the declared regions' (`node_detector_nodes`) and the bodies' own, at the same read (`share.family_share` with the read's content and factors, as `Lattice.share_of` reads it), the passage's share (`Passage.booked`, the click's plan, C4)."""
    at, gamma = node_detector_nodes(board), board.world.node_clock
    for books in board.credit.bodies:
        at = at | board.mask(books.nodes)
    found: Weighed = {}
    for index in board.order:
        family, found[index] = board.families[index], []
        for record in quanta_records(board.families, index):
            lines = board.lines_of(index, record)
            content, factors = board.read(index, 1, record)
            shares = share.family_share(
                family, lines, board.wrap, gamma, content, factors, board.unit, at
            )
            found[index].append(
                (readings.currents_of(family.pair[0], lines, board.wrap), factors, shares)
            )
    return found


def booked_inflows(board: Lattice, weighed: Weighed, wrap: Wrap, own: np.ndarray) -> None:
    """Every reader's own book of this interval: for each family its transitions name among `weighed` (per record its currents and its Links' factors at the pair the step started from), the conserved form's own current entering through its Nodes' front Ports (`reports.front` on the region, `reports.weighted`, in the unit G^2), added to its book per Node (`booked_inflow`), and the family's passage through the region, its momentum terms and its share there, added to the piece's two sums from the same read (`Passage.booked`, C4); the credit's rule for a NodeDetector with Nodes alone, here for a NodeDetector with a record of its own."""
    for books in board.credit.bodies:
        drives = sorted({t.drive for t in books.declared.transitions if t.drive in weighed})
        if drives:
            region = board.mask(books.nodes)
            facing = front(region, wrap, region, own)
            for drive in drives:
                booked_inflow(board, books, drive, weighted(facing, weighed[drive]))
                books.passages.setdefault(drive, Passage()).booked(region, weighed[drive])
