"""The one act of the click (ALGEBRA.md, The click writes on the lattice; the owner's word: one generic act at the Node, operated by the NodeDetector): a click is one draw among its alternatives by the reader's read of the board (`click`, `node_detector.picked`, the lower index on a tie, no draw where one alternative stands), the drawn alternative's list built where it is drawn (the place drawn inside it by the same read, the hole's Node by the inflows booked, the lay's Node by the record's share, a region's quantum to its region and boundary Node; the rows of the table, `lists.py`), the Node's act for every Item of the list (`written`: a spread record taken by the face, one value presented at one Port for two intervals so that Rule3 writes the level, or given whole quanta by the lay, `emission.emitted_quantum`; a record declared a NodeDetector laid part by part at its new count, `parted`, the piece's momentum and the source's recoil booked on its line and written nowhere, `twist.recoiled`; the erasing front begun where a spread record's count reaches 0) and the click's line after the write (`node_detector.reported`, the one click line kind of every reader, or the conversion line), a list that moves no count writing its line only where its re-lay changed a level (the null window). The Node knows no click and keeps no memory of one; the books are the readers' and stand at no Node."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING

from event_universe import credit, front
from event_universe.emission import emitted_quantum
from event_universe.loader.derived import count_wall
from event_universe.loader.keys import Node
from event_universe.node_detector import NodeBooks, picked, reported
from event_universe.reports import LOST_TO_SOURCE, LOST_TO_TAKER, NO_SIDE, PAID_AT_EMISSION
from event_universe.resonance import turned_direction
from event_universe.twist import (
    Item,
    Phase,
    books_named,
    faced,
    levels_at,
    recoiled,
    relaid,
    scaled,
)

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Levels = list[tuple[int, int, int, int]]  # a list's parts' levels at their Nodes, read about a write


@dataclass(frozen=True)
class Line:
    """The click's line after the act, the one click line kind of every reader (`node_detector.reported`): the parts realised and left, (after, before), the families exchanged, (taken from, given to), None where none, and the count moved, 1 for a click and 0 for the null window's re-lay, whose line is written only where a level moved; `into`, the families out of a record converted whole, makes it the conversion line at the Node the records out were laid at (`reports.conversion`)."""

    parts: tuple[int, int] = (0, 0)
    exchanged: tuple[int | None, int | None] = (None, None)
    count: int = 1


@dataclass(frozen=True)
class Alternative:
    """One alternative of a click's draw: its weight, its list built where it is drawn (the place drawn inside it by the reader's own read of the board, after the click's draw and before its write), its line and the reader whose line it is (None for nothing, and for the region NodeDetectors' credit, whose line per quantum stands in the list's building)."""

    weight: int
    items: Callable[[], list[Item]]
    line: Line | None = None
    books: NodeBooks | None = None


def click(board: Lattice, books: NodeBooks | None, alternatives: list[Alternative]) -> int:
    """The one click act: the draw among the alternatives by their weights by the reader's read of the board (`node_detector.picked`: one draw where more than one alternative stands, the lower index on a tie, the number left carried in the reader's books within the interval; none for one alternative, which needs no reader: the lay by the schedule and the regions' credit), then the drawn alternative's list built, written (`written`) and its line after the write (`lined`); returns the index drawn."""
    pick = 0
    if len(alternatives) > 1:
        assert books is not None  # a draw among alternatives is a body's read of the board
        pick = picked(board, books, [alternative.weight for alternative in alternatives])
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
    reported(board, books, line.parts, line.exchanged, line.count)


def written(board: Lattice, items: list[Item]) -> None:
    """The write step of the act, the one swappable step, item by item (ALGEBRA.md, The click writes on the lattice, the undepleted beam; the two hands' line at the owner's word for the simple solution): a spread record's quantum is taken or given at the Nodes named through one comparison, `faced`, the record's booked share at the Node against its own quantum W_rec; where the record is local and whole there the absorption is the hole to 0 by the face (every line of the record whatever their number) and the emission the lay of one whole quantum (`emitted_quantum`), and where the record is a beam, many quanta per Node, nothing is written on the board: the quantum passes in the books alone, the count moved by the item's change as for every item and the family's deficit, the board's share over the books' count in quanta, moved against it (`credit.Books.deficits`, up by one for an absorption written at no Node named, down by one for an emission not laid, the deficit's condition the complement of the lay's: an emission naming several Nodes with a beam among them lays nothing and moves the deficit, though no shipped list names several Nodes for an emission; printed in the books' line), and a quantum passing into or out of a spread record ends its windows' account, its unabsorbed share and its denominator dropped from the credit's books to begin again at the count left (`credit.Books.account_ended`, `lists.absorption`); a record declared a NodeDetector at one Node laid part by part at its new count (`parted`), the direction and sense of the part its quantum leaves read first and passed to the part it enters (the phase passes with the quantum), its books' part the one carrying the count and its labels' coherence ended; where a spread record's count reaches 0 its erasing front begins from every Node faced, with the Ports faced there (`front.started`), and a record whose count stays at one or more has no front; every lay of the step is the one lay act's, which writes every line a lay changed at a Node, levels or remainder, as one `lay` line with the levels before and after (`lay.written`, `reports.lay`), the diagnostic the host's tool crosses the lay from (the mathematician's hand: the face's part crossed by Rule3's inverse, the lay's part from its line). Part G (both hands' lines of 2026-10-10, the emission's write): the recoil is booked at the act whose draw fixes the direction; a directed packet laid here (`emission.laid_packet`, the direction the emission's own draw) carries its lattice momentum at birth, and the emitting body's books take its negative as the recoil owed, in T's unit (`scaled`), with the two readings for the emission's own credit line, `PAID_AT_EMISSION` and `LOST_TO_SOURCE`: booked on this line and written nowhere, the body's part standing as laid (ALGEBRA.md, The click's algebra beyond the law; the recoil of a body held at declared Nodes is the declaration's); the source in time books none here, the whole recoil the click's. The standing origin (C6, 2026-10-19): where the hole's Node is booked and not faced (`NO_SIDE`, a two-sided arrival or a Port set whose read coefficients sum above the wall), its one-Node share stands and spreads behind the front at the count 0, carried by the deficit book and within B1's one half of a quantum, the consequence named."""
    phases = {i.body: leaving_phase(board, i) for i in items if i.body is not None and i.delta < 0}
    touched: list[NodeBooks] = []
    holes: dict[int, list[tuple[Node, tuple[int, ...]]]] = {}
    recoils: list[tuple[int, int, tuple[int, int, int]]] = []
    unsided = False  # C6: a hole's Node with an empty face set, the quantum booked and not faced
    for item in items:
        if item.body is not None:
            parted(board, books := books_named(board, item.body), item, phases.get(item.body))
            touched += [books] if books not in touched else []
            continue
        whole, was = faced(board, item), board.credit.counts[item.family]
        drawn = list(zip(item.nodes, item.ports or ((),) * len(item.nodes), strict=True))
        unwritten = not whole if item.delta < 0 else len(whole) < len(item.nodes)
        if item.delta > 0 and not unwritten:
            born = emitted_quantum(board, item)
            if born is not None and item.emitter is not None:
                recoils.append((item.family, item.emitter, born))
        else:
            board.credit.counts[item.family] += item.delta
        board.credit.account_ended(item.family)
        if item.delta > 0 and not unwritten:  # a lay that raised the count: the births' book
            credit.born(board, item.family, was)
        if item.delta < 0:  # the front from every drawn Node, faced or not (C6, the re-fix)
            holes.setdefault(item.family, []).extend(drawn)
        if unwritten:  # the undepleted beam, or no Node with a side: the quantum in the books alone
            board.credit.deficits[item.family] = board.credit.deficits.get(item.family, 0) - item.delta
        unsided |= item.delta < 0 and bool(item.ports) and not all(item.ports)  # any Node without a side
    for books in touched:
        books.lost = [*(books.lost or []), NO_SIDE] if unsided else books.lost
        books.part = max(range(len(books.counts)), key=lambda k: books.counts[k])
        wall = count_wall(board.families[books.index], board.world.quantum_action)
        books.labels = [count * wall for count in books.counts]
        books.carried = [
            0 for _count in books.counts
        ]  # the labels re-laid: the hop's remainders with them
    for light, number, born in recoils:  # the packet's recoil at the lay: the giver's owed, booked
        giver = books_named(board, number)
        giver.recoil = scaled([-value for value in born], board.families[light].pair[0])
        giver.lost = [*(giver.lost or []), PAID_AT_EMISSION, LOST_TO_SOURCE]
    for family, absorbed in sorted(holes.items()):
        if board.credit.counts[family] <= 0 and absorbed:  # the count at 0: its front from every Node
            front.started(board, family, absorbed)


def leaving_phase(board: Lattice, item: Item) -> list[Phase]:
    """The direction (re, im) and the sense (the sign of the Wronskian) of the part a quantum leaves at each Node of the body, in the books' order, read before any lay of the list (the click's plan, C3: per Node and not at the first Node, so the re-lay keeps each Node's own direction); a Node with no direction of its own, standing at (0, 0), takes the direction of the first Node that has one, a tie-break of the hole's Port order's kind (the cold reader's line of 2026-10-19)."""
    assert item.part is not None
    books = books_named(board, item.body or 0)
    found = [levels_at(board, books, item.part, here) for here in books.nodes]
    first = next((levels for levels in found if levels[:2] != (0, 0)), found[0])
    return [
        (
            (re, im) if (re, im) != (0, 0) else first[:2],
            1 if re * im_before - im * re_before >= 0 else -1,
        )
        for re, im, re_before, im_before in found
    ]


def parted(board: Lattice, books: NodeBooks, item: Item, phase: list[Phase] | None) -> None:
    """One part of a record declared a NodeDetector at one Node laid at its new count (`relaid`): in the sense of the part the quantum leaves where the list names one, the entered part's direction at each Node the leaving part's own at that Node turned by the arriving record's phase, atan2(Y', X) of the two sums the close held (the click's plan, C3: per Node, so the body's P after an absorption and an emission is gain_in - gain_out, the two kicks of laser cooling) (`Item.arrival`, `resonance.turned_direction`; ALGEBRA.md, The two-mode line, row 16: the phase passes with the quantum, the product's phase phi_part = phi_left + phi_L), unturned where no arrival stands (the emission's items) and for the part the quantum leaves; in its own direction and sense otherwise (a part laid again at its count, the null window: Part H, MUST 1, each Node of the region in the direction standing there, so a phase gradient across the region survives every re-lay, `relaid`); Part F: where the item carries the piece's momentum and the count enters, the piece's P is booked lost to the taker, the part's lines standing as laid (ALGEBRA.md, The click's algebra beyond the law: the write writes nothing for the piece's momentum, the recoil of a body held at declared Nodes the declaration's); Part G (both hands' lines of 2026-10-10): the piece's source is drawn among the light's emitters by the quanta each still holds, through the taker's own read of the board as its Node is drawn (one emitter, no draw), and the recoil it owes is booked (`recoiled`), the books taking the source's name, its recoil and its reading in `lost` after the taker's."""
    assert item.part is not None and item.nodes == books.nodes
    books.counts[item.part] += item.delta
    own = phase if phase is not None else leaving_phase(board, item)
    arrival = (
        item.arrival if item.delta > 0 else None
    )  # the entering part turned; the leaving, the null's own
    phases = [(d if arrival is None else turned_direction(*d, *arrival), s) for d, s in own]
    relaid(board, books, item.part, books.counts[item.part], phases)
    if item.momentum is not None and item.delta > 0:
        readings = [LOST_TO_TAKER] if any(item.momentum) else []  # the piece's P booked, not written
        if item.drive is not None:
            books.source, books.recoil, reading = recoiled(
                board, item.drive, item.momentum, partial(picked, board, books)
            )
            readings.append(reading)
        books.lost = readings or None
