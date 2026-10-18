"""The one act of the click (ALGEBRA.md, The click writes on the lattice; the owner's word: one generic act at the Node, operated by the NodeDetector): a click is one draw among its alternatives by the declared generator (`click`, the lower index on a tie, no draw where one alternative stands), the drawn alternative's list built where it is drawn (the place drawn inside it with the reader's own generator, the hole's Node by the inflows booked, the lay's Node by the record's share, a region's quantum to its region and boundary Node; the rows of the table, `lists.py`), the Node's act for every Item of the list (`written`: a spread record taken by the face, one value presented at one Port for two intervals so that Rule3 writes the level, or given whole quanta by the lay, `emission.emitted_quantum`; a record declared a NodeDetector laid part by part at its new count, `parted`, the taker's twist and the source's fold the same lay write, `twist.twisted`, `twist.folded_source`; the erasing front begun where a spread record's count reaches 0) and the click's line after the write (`node_detector.reported`, the one click line kind of every reader, or the conversion line), a list that moves no count writing its line only where its re-lay changed a level (the null window). The Node knows no click and keeps no memory of one; the books are the readers' and stand at no Node."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from event_universe import front
from event_universe.emission import emitted_quantum
from event_universe.loader.derived import count_wall
from event_universe.loader.draw import Draw, Generator
from event_universe.loader.keys import Node
from event_universe.node_detector import NodeBooks, picked, reported
from event_universe.reports import NO_SIDE, PAID_AT_EMISSION, conversion
from event_universe.resonance import turned_direction
from event_universe.twist import (
    Item,
    Phase,
    books_named,
    faced,
    folded_source,
    levels_at,
    recoiled,
    relaid,
    scaled,
    twisted,
)

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Levels = list[tuple[int, int, int, int]]  # a list's parts' levels at their Nodes, read about a write


class Reader(Protocol):
    """A reader whose generator the click draws with: its state kept in its books (`node_detector.NodeBooks`, `credit.Books`), advanced by the click's draw before the drawn list draws its place with the same generator."""

    state: int


@dataclass(frozen=True)
class Line:
    """The click's line after the act, the one click line kind of every reader (`node_detector.reported`): the parts realised and left, (after, before), the families exchanged, (taken from, given to), None where none, and the count moved, 1 for a click and 0 for the null window's re-lay, whose line is written only where a level moved; `into`, the families out of a record converted whole, makes it the conversion line at the Node the records out were laid at (`reports.conversion`)."""

    parts: tuple[int, int] = (0, 0)
    exchanged: tuple[int | None, int | None] = (None, None)
    count: int = 1
    into: tuple[int, ...] | None = None


@dataclass(frozen=True)
class Alternative:
    """One alternative of a click's draw: its weight, its list built where it is drawn (the place drawn inside it with the reader's own generator, after the click's draw and before its write), its line and the reader whose line it is (None for nothing, and for the region NodeDetectors' credit, whose line per quantum stands in the list's building)."""

    weight: int
    items: Callable[[], list[Item]]
    line: Line | None = None
    books: NodeBooks | None = None


def click(
    board: Lattice, reader: Reader, generator: Generator | None, alternatives: list[Alternative]
) -> int:
    """The one click act: the draw among the alternatives by their weights with the generator (`node_detector.picked`: one draw where more than one alternative stands, the lower index on a tie, the state carried in the reader's books and advanced there before the list is built; none for one), then the drawn alternative's list built, written (`written`) and its line after the write (`lined`); returns the index drawn."""
    weights = [alternative.weight for alternative in alternatives]
    pick, reader.state = picked(board, reader.state, generator, weights, len(alternatives))
    chosen = alternatives[pick]
    items = chosen.items()
    quiet = (
        chosen.line is not None and chosen.line.count == 0
    )  # the null window: a line where a level moved
    standing = levels_of(board, items) if quiet else None
    written(board, items)
    if chosen.line is not None and (standing is None or levels_of(board, items) != standing):
        lined(board, chosen, items)
    return pick


def levels_of(board: Lattice, items: list[Item]) -> Levels:
    """The parts' levels at the Nodes of a list's body Items, (re_now, im_now, re_before, im_before) each (`twist.levels_at`), read before and after a write that moves no count: a null window whose re-lay changed no level writes no line."""
    return [
        levels_at(board, books_named(board, item.body), item.part, here)
        for item in items
        if item.body is not None and item.part is not None
        for here in item.nodes
    ]


def lined(board: Lattice, chosen: Alternative, items: list[Item]) -> None:
    """The click's line after the write: the one click line kind of every reader (`node_detector.reported`: the parts, the families exchanged and the count), or for a record converted whole the conversion line (`reports.conversion`: the reader by its number, its window, the families out and the one Node the records out were laid at, the first spread Item's, a diagnostic beside the result)."""
    books, line = chosen.books, chosen.line
    assert books is not None and line is not None
    if line.into is None:
        reported(board, books, line.parts, line.exchanged, line.count)
        return
    if board.output is None:
        return
    assert isinstance(books.declared.draw, Draw)  # a record converted whole declares its window
    window = [board.interval - books.declared.draw.window + 1, board.interval]
    name, *into = [board.families[k].name for k in (books.index, *line.into)]
    at = list(next(item.nodes[0] for item in items if item.body is None))
    board.output(conversion(board.interval, name, books.number, window, into, at))


def written(board: Lattice, items: list[Item]) -> None:
    """The write step of the act, the one swappable step, item by item (ALGEBRA.md, The click writes on the lattice, the undepleted beam; the two hands' line at the owner's word for the simple solution): a spread record's quantum is taken or given at the Nodes named through one comparison, `faced`, the record's booked share at the Node against its own quantum W_rec; where the record is local and whole there the absorption is the hole to 0 by the face (every line of the record whatever their number) and the emission the lay of one whole quantum (`emitted_quantum`), and where the record is a beam, many quanta per Node, nothing is written on the board: the quantum passes in the books alone, the count moved by the item's change as for every item and the family's deficit, the board's share over the books' count in quanta, moved against it (`credit.Books.deficits`, up by one for an absorption written at no Node named, down by one for an emission not laid, the deficit's condition the complement of the lay's: an emission naming several Nodes with a beam among them lays nothing and moves the deficit, though no shipped list names several Nodes for an emission; printed in the books' line), and a quantum passing into or out of a spread record ends its windows' account, its unabsorbed share and its denominator dropped from the credit's books to begin again at the count left (`credit.Books.account_ended`, `lists.absorption`); a record declared a NodeDetector at one Node laid part by part at its new count (`parted`), the direction and sense of the part its quantum leaves read first and passed to the part it enters (the phase passes with the quantum), its books' part the one carrying the count and its labels' coherence ended; where a spread record's count reaches 0 its erasing front begins from every Node faced, with the Ports faced there (`front.started`), and a record whose count stays at one or more has no front; every lay of the step is the one lay act's, which writes every line a lay changed at a Node, levels or remainder, as one `lay` line with the levels before and after (`lay.written`, `reports.lay`), the diagnostic the host's tool crosses the lay from (the mathematician's hand: the face's part crossed by Rule3's inverse, the lay's part from its line). Part G (both hands' lines of 2026-10-10, the click with two receivers, the emission's write): the recoil is written at the act whose draw fixes the direction; a directed packet laid here (`emission.laid_packet`, the direction the emission's own draw) carries its lattice momentum at birth, and the emitting body's part, the one carrying its count after the parts are laid, is folded by its negative through the same twist about the lay's Node (`folded_source`; the click's plan, C6 (ii)), the emitter's books taking the recoil paid and its reading for the emission's own credit line (`PAID_AT_EMISSION`, with `LOST_TO_SOURCE` where its quarter turn falls short); the source in time pays none here, the whole recoil the click's."""
    phases = {i.body: leaving_phase(board, i) for i in items if i.body is not None and i.delta < 0}
    touched: list[NodeBooks] = []
    holes: dict[int, list[tuple[Node, tuple[int, ...]]]] = {}
    recoils: list[tuple[int, int, tuple[int, int, int], Node]] = []
    unsided = False  # C6: a hole's Node with an empty face set, the quantum booked and not faced
    for item in items:
        if item.body is not None:
            parted(board, books := books_named(board, item.body), item, phases.get(item.body))
            touched += [books] if books not in touched else []
            continue
        whole = faced(board, item)
        unwritten = not whole if item.delta < 0 else len(whole) < len(item.nodes)
        if item.delta > 0 and not unwritten:
            born = emitted_quantum(board, item)
            if born is not None and item.emitter is not None:
                recoils.append((item.family, item.emitter, born, item.nodes[0]))
        else:
            board.credit.counts[item.family] += item.delta
        board.credit.account_ended(item.family)
        if item.delta < 0:
            holes.setdefault(item.family, []).extend(whole)
        if unwritten:  # the undepleted beam, or a two-sided arrival: the quantum in the books alone
            board.credit.deficits[item.family] = board.credit.deficits.get(item.family, 0) - item.delta
            unsided |= item.delta < 0 and bool(item.ports) and not any(item.ports)
    for books in touched:
        books.lost = [*(books.lost or []), NO_SIDE] if unsided else books.lost
        books.part = max(range(len(books.counts)), key=lambda k: books.counts[k])
        wall = count_wall(board.families[books.index], board.world.quantum_action)
        books.labels = [count * wall for count in books.counts]
        books.carried = [
            0 for _count in books.counts
        ]  # the labels re-laid: the hop's remainders with them
    for light, number, born, origin in recoils:  # the packet's recoil at the lay: the giver folded by -P
        giver = books_named(board, number)
        owed = scaled([-value for value in born], board.families[light].pair[0])
        giver.recoil, short = folded_source(board, giver, (owed[0], owed[1], owed[2]), origin)
        giver.lost = [PAID_AT_EMISSION, *([short] if short is not None else [])]
    for family, absorbed in sorted(holes.items()):
        if board.credit.counts[family] <= 0 and absorbed:  # the count at 0: its front from every Node
            front.started(board, family, absorbed)


def leaving_phase(board: Lattice, item: Item) -> Phase:
    """The direction (re, im) and the sense (the sign of the Wronskian) of the part a quantum leaves, read at the Node before any lay of the list."""
    assert item.part is not None
    re, im, re_before, im_before = levels_at(board, books_named(board, item.body or 0), item.part)
    return (re, im), 1 if re * im_before - im * re_before >= 0 else -1


def parted(board: Lattice, books: NodeBooks, item: Item, phase: Phase | None) -> None:
    """One part of a record declared a NodeDetector at one Node laid at its new count (`relaid`): in the sense of the part the quantum leaves where the list names one, the entered part's direction the leaving part's turned by the arriving record's phase at the Node, atan2(Y', X) of the two sums the close held (`Item.arrival`, `resonance.turned_direction`; ALGEBRA.md, The two-mode line, row 16: the phase passes with the quantum, the product's phase phi_part = phi_left + phi_L), unturned where no arrival stands (the emission's items); in its own direction and sense otherwise (a part laid again at its count, the null window: Part H, MUST 1, each Node of the region in the direction standing there, so the twist and the source's fold survive the re-lay, `relaid` with no direction named); Part F: where the item carries the piece's momentum and the count enters, the part's lines twisted after the lay about the click's Node, the item's origin (`twisted`, C6 (ii)), the books taking n_a per axis and what was lost for the credit line; Part G (both hands' lines of 2026-10-10, the click with two receivers): after the taker's twist the piece's source is drawn among the light's emitters by the quanta each still holds, through the taker's own generator as its Node is drawn (one emitter, no draw), and the source's part is folded by -p_a at the click's tick by the same twist (`recoiled`), the books taking the source's name, its recoil and its reading in `lost` after the taker's."""
    assert item.part is not None and item.nodes == books.nodes
    books.counts[item.part] += item.delta
    (re, im), sense = phase if phase is not None else leaving_phase(board, item)
    direction: tuple[int, int] | None
    if item.delta == 0:  # the null window and the probe's own: each Node keeps its own direction
        direction = None
    else:
        direction = (re, im) if item.arrival is None else turned_direction(re, im, *item.arrival)
    relaid(board, books, item.part, books.counts[item.part], direction, sense)
    if item.momentum is not None and item.delta > 0:
        assert item.origin is not None  # the click's Node, the fold's origin
        books.twist, short = twisted(board, books, item.part, item.momentum, item.origin)
        readings = [short] if short is not None else []
        if item.drive is not None:

            def pick(weights: list[int]) -> int:
                index, books.state = picked(
                    board, books.state, books.declared.draw, weights, len(weights)
                )
                return index

            books.source, books.recoil, reading = recoiled(
                board, item.drive, item.momentum, pick, item.origin
            )
            readings += [reading] if reading is not None else []
        books.lost = readings or None
