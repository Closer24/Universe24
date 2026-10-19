"""The meeting at a Node, the NodeDetectors' loop (ALGEBRA.md #the-click-is-the-meeting, The click writes on the lattice; HIGHLIGHTS.md, the owner's words; the owner's word, the click the heart): a node_detector is where the future met the past, the arriving record's quantum run forward from its root meeting at one Node the node_detector's own transition's quantum read back from the realised click, the click their meeting; a node_detector always receives two quanta, the arriving one and its own, a region node_detector's own quantum implicit in its declared window and whole, and for a record declared a NodeDetector at one Node its record there; from the click the new future goes out, the quantum with the taker to its next meeting (the taker's record changed at its Node and stepped on by Rule3), the hole spreading from the entry Node, the emission's light quantum, and the arriving record's wave with its count at 0, the empty wave, stepped on and never credited. The seven steps in the Node's words (the Boss's sequence with the advisor's and the mathematician's hands): 0, every interval every Node steps every record it holds by Rule3, a bijection, no draw; at the end of a reader's window at the Node named (the declared window's length, or, for a body with a probe, the interval of the probe's lay at its Node: the window bounded by clicks, opened at the body's last write and closed at the probe's absorption, ALGEBRA.md, The pulsed gate), 1, the read, the two records at that Node, the arriving family's level there and the record present, the share their product at resonance (the resonant two-mode act, the two-quadrature form: the arriving level summed over the window against the record's two reference records at the transition's declared resonance, the plane's size over the scale the window's turn at the declared weight, applied once at the window's close as W sub-turns with the carry, turning the two parts' labels into each other, the labels' squares the shares, the Rabi form, `resonance.gathered`, `resonance.window_turn`, `turned_labels`); 2, the draw, with the declared seed and generator, once per window, among the alternatives the declaration's table lists for the close (`lists.py`: the emission's at the clock's grain, the probe's, the absorptions', the null window's and the conversion's; the one act, `act.click`); 3, the write at that Node, one whole quantum passing between the two records there (`lists.exchange`, `act.written`): climbing, the arriving record's levels and remainder to 0 (the hole to 0 where the record's booked share at the Node is at most its own quantum; for a dense record, a beam of many quanta per Node, nothing on the board, the quantum passing in the books alone with the deficit printed, the undepleted beam, `twist.faced`) and its count in the books down by one; descending, stimulated emission, one quantum given back into the drive (by the count where it is local and whole at the Node, nothing where it is a beam) and its count up by one; the present record's realised part laid at N + 1 at that Node in the direction of the part it leaves turned by the arriving record's phase at the Node, atan2(Y', X) of the window's two sums the close held (the phase passing with the quantum, `resonance.turned_direction`, `twist.Item.arrival`), the remainder at the lay's origin, the part it leaves at N - 1 (the absorption); 4, a window with no meeting at a Node whose record reads its own parts, the record laid again in the complement of its outcome set at its whole count (the null window, `lists.null_window`); 5, the emission, at a Node whose record stands in an upper part, drawn at the lifetime's hazard 1 / tau per interval, per window while a window stands and per interval in the dark at the now (the beat's current of a one-part record at one Node being 0, named): one whole quantum passing from that record to the light family's record at the same Node, the upper part to N - 1, the lower to N + 1, light's record up by one whole quantum laid as a source in time at that Node over the emission's lifetime at the transition's declared resonance from the phase phi_e - phi_g, the two parts' directions read before the lay (`lists.emission`, `emission.start_of`, `emission.emitted_quantum`); 6, after the write the Node and its neighbours step by Rule3, nothing written at any other Node, no front; 7, the click line (`node_detector.reported`, the one click line kind of every reader), the window, the reader, the family and the parts, never a Node, the Node written standing in the LATTICE `lay` and `face` lines beside it. The record declared a NodeDetector is one Node by the world's declaration (its six Link factors 0, `cut`, so that it stays, held by its declaration as the node_detector's region is), its books the reader's own and at no Node; the Node knows no click. The region NodeDetectors' clicks at the credit's window close through the same act (`closed`, `lists.region`)."""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import flux, lists, node
from event_universe.act import Alternative, click
from event_universe.core.ports import arrival
from event_universe.loader.draw import Draw
from event_universe.loader.keys import Node
from event_universe.node_detector import NodeBooks, arriving, clock_advanced, dark, own_clock, sourcing
from event_universe.records import Booking, Record
from event_universe.resonance import gathered, hopped, window_pair, window_turn
from event_universe.twist import Item, faces_presented, relaid

if TYPE_CHECKING:
    from event_universe.lattice import Lattice
from event_universe.core import paces


def read_with_cuts(board: Lattice, index: int, direction: int, record: int) -> tuple[Any, node.Factors]:
    """A record's read at the interval's start in `direction` (`node.read`, every sign row but the record's own), the Links the world cuts at 0 among its factors (`cut`)."""
    gamma, unit, cuts = board.world.node_clock, board.unit, cut(board, index)
    return node.read(
        index, board.families, board.states, direction, board.wrap, gamma, unit, record, cuts
    )


def stepped(board: Lattice, index: int, direction: int) -> tuple[list[Record], list[Booking]]:
    """Every record of a family stepped by Rule3 in flux form in `direction` with the rule of its own read (`flux.step_records`), the Links the world cuts at 0 among its factors (`cut`) and the faces the click act presents at this interval among its arrivals (`faces_presented`)."""
    gamma, unit, cuts = board.world.node_clock, board.unit, cut(board, index)
    faces = faces_presented(board, index)
    return flux.step_records(
        index,
        board.families,
        board.states,
        board.wrap,
        gamma,
        unit,
        direction,
        cuts,
        faces,
        board.amplitude,
    )


def cut(board: Lattice, index: int) -> node.Factors | None:
    """The Links the world declares at the factor 0 for a family, per Port the mask of the Nodes whose Port faces them (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment: its outer Links cut and its inner Links open): the boundary Links of every region over which a record of the family is laid in its parts, the Links with one end in the region and one outside, read 0 from both ends; the Links between two Nodes of one region stay at G^2, so that the record's uniform mode rotates at cos omega_0 = num / den whatever the region's size; None where the family has no such record."""
    regions = [
        board.mask(row.nodes)
        for row in board.world.bodies
        if row.family == index and row.detector is not None
    ]
    if not regions:
        return None
    found = []
    for axis in range(3):
        for side in (1, -1):
            mask = np.zeros(board.shape, dtype=bool)
            for at in regions:
                mask |= at ^ arrival(at, axis, side, board.wrap, False)
            found.append(mask)
    return tuple(found)


def laid_record(board: Lattice, number: int, record: int) -> None:
    """A record laid in its parts at its one Node at the start (`loader/node_detector_declaration.py`, `parts`): every part at its declared count, the one carrying the count as the standing record of the pair in the direction (1, 0) and the sense +1, the others 0 there; the books not yet made, so a passing book names the declaration."""
    row = board.world.bodies[number]
    kind = row.detector
    assert kind is not None
    books = NodeBooks(number, row.family, record, row.nodes, row.counts, kind, 0, [], [], 0, 0, [])
    for part, count in enumerate(kind.counts):
        relaid(board, books, part, count, [((1, 0), 1)] * len(books.nodes))


def laid_whole(board: Lattice) -> None:
    """The packets laid whole at this interval's end (`loader/packets.py`, `WholePacket`: the probe of the pulsed gate, the two hands): each its count of whole quanta laid at its Node through the one act with one alternative and no draw (`act.click`, `emission.emitted_quantum`, `laid_by_count` at the family's massless pair [den, den], A^2 = count T div 2 on the record's first line), the record's count in the books up by the count and one lay line for the host's tool; the experimenter's lay in time, from outside the Node as every lay is, before the records at Nodes read their arrivals."""
    for whole in board.world.wholes:
        if whole.interval == board.interval:
            den = board.families[whole.family].pair[1]
            items = [Item(whole.family, None, None, whole.count, (whole.at,), (den, den))]
            click(board, board.credit, None, [Alternative(1, partial(list, items))])


def turned_labels(board: Lattice, books: NodeBooks) -> None:
    """The resonant two-mode act at the window's close, once per window (ALGEBRA.md, The two-mode line; The click writes on the lattice (b), the share at resonance; item 50, the two-quadrature form, two hands): for every transition out of the part the record stands in, the window's turn (`resonance.window_turn`, the plane's size over the scale) scaled to the record's own proper interval by its clock (`paces.turn_factor`, one rounding half up: the window's angle theta_W in units of the phase line's theta_0 = 1 / Gamma) turns the two parts' labels into each other by one hop with the phase line's pair at that angle (`resonance.window_pair`, `resonance.hopped`: (C u - S v + r_u) div X and (S u + C v + r_v) div X, the remainders carried in the books (`NodeBooks.carried`) between windows and cleared with the labels at the re-lay), the plane's size over the wall read once and not a turn per interval, no shear; the labels' squares are the parts' population after the window; the window's draw reads each transition's own transfer share, kept in the books (`NodeBooks.shares`): the pair as it stood before the window's turns hopped by that transition's turn alone (no remainder carried: a read for the share, not the books' write), its entered label squared, sin^2 of the turn, the Rabi form, the record's share at the body (`lists.absorption`, `lists.probe`), the composed label squared itself where one transition alone feeds the part; the complement outcome at the close, none takes, is the null window (`lists.null_window`, the record re-laid in its part at its count, the labels' coherence ended); every transition's two sums then begin again, the reference records running on."""
    gamma, clock = board.world.node_clock, own_clock(board, books)
    before, books.shares = list(books.labels), {}
    if len(books.carried) != len(books.labels):
        books.carried = [0 for _label in books.labels]
    for transition, reference in zip(books.declared.transitions, books.references, strict=True):
        leaves, enters = transition.leaves, transition.enters
        if leaves == books.part and leaves != enters:  # the probe's turns nothing
            turn = int(paces.turn_factor(window_turn(reference, transition.weight), clock, gamma))
            pair = window_pair(turn, gamma, board.amplitude)
            own = hopped(before[leaves], before[enters], *pair)
            remainders = (books.carried[leaves], books.carried[enters])
            u, v, books.carried[leaves], books.carried[enters] = hopped(
                books.labels[leaves], books.labels[enters], *pair, remainders
            )
            books.labels[leaves], books.labels[enters], books.shares[transition] = u, v, own[1] ** 2
        reference.closed()


def emission_drawn(board: Lattice, books: NodeBooks, grain: int) -> bool:
    """The emission's draw at the clock's grain, `grain` intervals (ALGEBRA.md, The click writes on the lattice (j), the fifth act, and the emission's clock): for each rate out of the part the record stands in, one click over the emission's alternatives (`lists.emission`: one list per direction the board holds at the hazard's weight over the span, the smaller of the grain and the lifetime, and nothing at the rest), the record's own generator; the first emission drawn is taken, its quantum laid and its line written by the act; returns whether one was."""
    for rate in books.declared.rates:
        if rate.leaves == books.part:
            alternatives = lists.emission(board, books, rate, min(grain, rate.lifetime))
            pick = click(board, books, books.declared.draw, alternatives)
            if pick < len(alternatives) - 1:
                return True
    return False


def absorptions_drawn(board: Lattice, closing: list[NodeBooks]) -> set[int]:
    """The absorptions drawn at the windows' end, one draw at a time per arriving family over every closing record's outcomes into it (ALGEBRA.md, The click writes on the lattice (f); `lists.absorption`): while the arriving record's count stands in the books, the records not done reading it close with one click, the first closing record's generator, the drawn record done for the window; nothing drawn ends the family's draws at this close, its unabsorbed share booked by the row; returns the records done."""
    done: set[int] = set()
    pairs = [(b, t) for b in closing for t in b.declared.transitions if t.leaves == b.part]
    for drive in sorted({t.drive for _books, t in pairs}):
        while board.credit.counts[drive] > 0:
            outcomes = [(b, t) for b, t in pairs if b.number not in done and t.drive == drive]
            if not outcomes:
                break
            first, alternatives = closing[0], lists.absorption(board, drive, outcomes)
            pick = click(board, first, first.declared.draw, alternatives)
            if pick == len(outcomes):
                break
            done.add(outcomes[pick][0].number)
    return done


def conversion_drawn(board: Lattice, books: NodeBooks) -> bool:
    """The conversion drawn at a record's window's end (`lists.conversion`): while the record's count stands, for each conversion its declaration names one click between the conversion's list and nothing at the weights [the window capped at the rate, the rate less it], the record's own generator; the first conversion drawn is taken, its records out laid and its line written by the act; returns whether one was."""
    assert isinstance(books.declared.draw, Draw)  # a record converted whole declares its window
    window = books.declared.draw.window
    for table in books.declared.conversions:
        if books.counts[books.part] <= 0:
            return False
        span = window if window <= table.rate else table.rate
        alternatives = lists.conversion(board, books, table, span)
        pick = click(board, books, books.declared.draw, alternatives)
        if pick == 0:
            return True
    return False


def probe_arrived(books: NodeBooks, laid: set[tuple[int, Node]]) -> bool:
    """Whether a probe arrived at the body this interval: a lay at its Node (`laid_whole`, the world's schedule) of the family of one of its transitions of a part into itself; the window's close at the declared interval, no level read (ALGEBRA.md, The pulsed gate: the window bounded by the lays' schedule; the two hands)."""
    return any(
        t.leaves == t.enters and (t.drive, at) in laid
        for t in books.declared.transitions
        for at in books.nodes
    )


def closed(board: Lattice) -> None:
    """The region NodeDetectors' clicks at the credit's window's close (`credit.counted_windows`; ALGEBRA.md #the-click-is-the-meeting): per family of quanta its list from the window's books through the one act (`lists.region`, one alternative and no draw of its own, the places drawn inside it with the credit's generator; where the meeting runs back the two readings in the time's order with the run back and forward between them, `lists.readings`, `meeting_back`), then the window's books emptied, the inflows, the joint shares, the passages and the back run's own (the sides' states, the parts' sums per interval and the conditioning), the count beginning again."""
    books = board.credit
    for index in board.order:
        found = lists.region(board, index)
        if found is not None:
            click(board, books, None, [found])
    books.intake.clear()
    books.joints.clear()
    books.passages.clear()
    books.states.clear()
    books.levels.clear()
    books.conditioning.clear()


def jumped(board: Lattice) -> None:
    """The records at Nodes that are NodeDetectors at the end of an interval: first the packets the world lays whole at this interval (`laid_whole`, the probe's lay at the body's Node by the schedule); then each record gathers the records arriving at its Node into its window's sums (`resonance.gathered`, the arriving level per drive family read once, `arriving`), one more interval elapsed and its own clock advanced (`node_detector.clock_advanced`); the window closes at its declared length, or, for a body with a probe among its transitions, at the interval of the probe's lay at its Node (`probe_arrived`: the window bounded by clicks, opened at the body's last write and closed at the probe's absorption, no level read; ALGEBRA.md, The pulsed gate, the two hands); at the close the window's turn of the labels (`turned_labels`, once per window, as W sub-turns with the carry) and the body's windows counted, then the draws and the writes, every one the one act's over the table's rows (`act.click`, `lists.py`): the emissions first record by record (`emission_drawn`: at the window's close while a window stands, the grain the count of the window's lit intervals, `NodeBooks.lit`, at every interval in the dark, `dark`, the grain 1, the lifetime's hazard 1 / tau per interval either way; a dark interval at the window's close draws twice, the interval at its own grain and then, where none was given, the window's lit intervals at theirs, so every interval of the window enters exactly one draw's span and the summed hazard over a window is W / tau whatever its dark intervals, ALGEBRA.md, The dark; a window with no dark interval the length itself, bit for bit), then at a probe's close the body's own one draw over its outcomes (`lists.probe`), at a declared window's the absorptions in one draw per arriving family over the records that gave none (`absorptions_drawn`), then the null window of every record of several parts that neither gave nor took (`lists.null_window`; a record of one part reads no part of itself and has none); the windows begun again; last, after the records' clicks, the conversion of every record converted whole whose window closed at this interval (`conversion_drawn`, its window read as the clicks left it)."""
    laid_whole(board)
    laid = {(whole.family, whole.at) for whole in board.world.wholes if whole.interval == board.interval}
    own = {b.number: sourcing(board, b) for b in board.credit.bodies}  # C5: read once per body
    for books in board.credit.bodies:
        levels = {
            t.drive: 0 if t.drive in own[books.number] else arriving(board, books, t.drive)
            for t in books.declared.transitions
        }
        gathered(books.references, books.declared.transitions, levels)
        timed = isinstance(
            books.declared.draw, Draw
        )  # C2: a declared window opens at the first lit interval
        books.elapsed += (
            1 if books.elapsed or not timed or not dark(board, books, own[books.number]) else 0
        )
        clock_advanced(board, books)
    closing = [
        b
        for b in board.credit.bodies
        if b.declared.draw is not None
        and (
            probe_arrived(b, laid)
            or (isinstance(b.declared.draw, Draw) and b.elapsed == b.declared.draw.window)
        )
    ]
    for books in closing:
        turned_labels(board, books)
        books.windows += 1
    ended, lit_numbers = {books.number for books in closing}, set()
    for books in board.credit.bodies:
        if books.declared.draw is None:
            continue
        lit = not dark(board, books, own[books.number])
        books.lit += lit
        spans = ([] if lit else [1]) + ([books.lit] if books.number in ended and books.lit else [])
        if any(emission_drawn(board, books, span) for span in spans):
            lit_numbers.add(books.number)
    quiet = [books for books in closing if books.number not in lit_numbers]
    read = {books.number for books in quiet if probe_arrived(books, laid)}
    for books in quiet:
        if books.number in read:
            click(board, books, books.declared.draw, lists.probe(board, books))
    done = absorptions_drawn(board, [books for books in quiet if books.number not in read])
    for books in quiet:
        if books.number not in read | done and len(books.counts) > 1:  # a record of one part reads none
            click(board, books, books.declared.draw, lists.null_window(board, books))
    for books in closing:
        books.elapsed, books.lit, books.intake, books.passages = 0, 0, {}, {}
    for (
        books
    ) in board.credit.bodies:  # the conversions after the records' clicks, the window as they left it
        if books.declared.conversions and books.elapsed == 0:
            conversion_drawn(board, books)
