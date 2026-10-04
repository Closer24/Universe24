"""The conversion, the fifth list of the one click act (ALGEBRA.md, A family's declaration, item 5, The conversion's table and rate; The click is the meeting, what the click's picture derives of the conversions; the two hands, the advisor's (c), the mathematician's hand, and their agreement on the one-Node lay; the owner's word, build and run tonight): a record declared whole at one Node with its table and rate (`loader/node_detector_declaration.py`, `Conversion`, a body's `conversion` with its own `node_detector`) is laid by the engine at the start over every line of its record by the invariant 2 A^2 sin omega = T (features/click, `laid_pairs`; `meeting.relaid`), cut and held at its Node as the parted record is, and at every window's end its conversion is drawn by the one act (`meeting.click_act`), the record's own generator: the record whole at -1 at its Node, its hole its lay at the count 0, and each family out at +1 there, one whole quantum laid by the count at its family's massless pair on every laid line of its record alike, a plane's two lines per plane with the sense the table declares for it (`emission.emitted_quantum`, the one lay function of a spread record given whole quanta, `Item.pair` and `Item.sense`; the mathematician's hand), the weights the window against the rate's rest in intervals (the rate the intervals per expected conversion, the declared floor, as the emission's); the act writes one lay line per line the write changed (`meeting.written`), every line of the record in and every laid line of each record out, so that the back-in-time tool crosses the write from the lines as it crosses the absorption and the emission; one conversion line (`reports.conversion`). A record converted whole has one part, named by its family, and no emission, absorption or null window, so its conversion is drawn after the records' clicks of the interval (`Lattice.step`, `meeting.jumped`), its window read as they left it; the rotations' sum and the sines' difference at the Node are the reader's to book from the levels (the world `examples/events/neutron_conversion/`)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe.loader.draw import Draw
from event_universe.meeting import Item, written
from event_universe.node_detector import NodeBooks, drawn_node, picked, share_weights
from event_universe.reports import conversion

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


def converted(board: Lattice, books: NodeBooks) -> bool:
    """The conversion drawn at a record's window's end: while the record's count stands, for each conversion its declaration names, one draw of the act between the conversion's list (the record whole at -1, each family out at +1 by the count at its massless pair, a plane at the sense the table declares) and nothing, at the weights [window, rate - window] (the window capped at the rate), the record's own generator; the first conversion drawn is taken, its records out laid at the one Node of the region drawn by the record's share at the body's Nodes as the board holds it at the close (`share_weights`, `drawn_node`; the file's lay weights enter no draw), its line written, and the window ends; returns whether one was drawn."""
    assert isinstance(books.declared.draw, Draw)  # a record converted whole declares its window
    window = books.declared.draw.window
    for table in books.declared.conversions:
        if books.counts[books.part] <= 0:
            return False
        span = window if window <= table.rate else table.rate
        weights = [span, table.rate - span]
        pick, books.state = picked(board, books.state, books.declared.draw, weights, 2)
        if (
            pick == 0
        ):  # realised: the records out at one Node of the region drawn now, by the record's own share
            items = [Item(books.index, books.number, books.part, -1, books.nodes)]
            laid_at = drawn_node(board, books, share_weights(board, books))
            for out, sense in zip(table.outs, table.senses, strict=True):
                den = board.families[out].pair[1]
                items.append(Item(out, None, None, 1, (laid_at,), (den, den), sense=sense))
            written(board, items)
            if board.output is not None:
                name, *into = [board.families[i].name for i in (books.index, *table.outs)]
                over, at = [board.interval - window + 1, board.interval], list(laid_at)
                board.output(conversion(board.interval, name, books.number, over, into, at))
            return True
    return False


def drawn_conversions(board: Lattice) -> None:
    """The conversions at the end of an interval, after the jumps (`meeting.jumped`, which begins a closing window again, its intervals elapsed 0): every record converted whole whose window closed at this interval has its conversion drawn (`converted`)."""
    for books in board.credit.bodies:
        if books.declared.conversions and books.elapsed == 0:
            converted(board, books)
