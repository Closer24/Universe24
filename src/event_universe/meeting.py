"""The meeting at a Node, the NodeDetectors' loop (ALGEBRA.md #the-click-is-the-meeting, The click writes on the lattice; HIGHLIGHTS.md, the owner's words; the owner's word, the click the heart): a node_detector is where the future met the past, the arriving record's quantum run forward from its root meeting at one Node the node_detector's own transition's quantum read back from the realised click, the click their meeting; a node_detector always receives two quanta, the arriving one and its own, a region node_detector's own quantum implicit in its declared window and whole, and for a record declared a NodeDetector at one Node its record there; from the click the new future goes out, the quantum with the taker to its next meeting (the taker's record changed at its Node and stepped on by Rule3), the hole spreading from the entry Node, the emission's light quantum, and the arriving record's wave with its count at 0, the empty wave, stepped on and never credited. The seven steps in the Node's words (the Boss's sequence with the advisor's and the mathematician's hands): 0, every interval every Node steps every record it holds by Rule3, a bijection, no draw; at the end of a reader's window at the Node named (the declared window's length, or, for a body with a probe, the interval of the probe's lay at its Node: the window bounded by clicks, opened at the body's last write and closed at the probe's absorption, ALGEBRA.md, The pulsed gate), 1, the read, the two records at that Node, the arriving family's level there and the record present, the share their product at resonance (the resonant two-mode act, the two-quadrature form: the arriving level summed over the window against the record's two reference records at the transition's declared resonance, the plane's size over the scale the window's turn at the declared weight, applied once at the window's close as W sub-turns with the carry, turning the two parts' labels into each other, the labels' squares the shares, the Rabi form, `resonance.gathered`, `resonance.window_turn`, `turned_labels`); 2, the draw, the click's read of the board (`node_detector.picked`), once per window, among the alternatives the declaration's table lists for the close (`lists.py`: the emission's at the clock's grain, the probe's, the absorptions', the null window's and the conversion's; the one act, `act.click`); 3, the write at that Node, one whole quantum passing between the two records there (`lists.exchange`, `act.written`): climbing, the arriving record's levels and remainder to 0 (the hole to 0 where the record's booked share at the Node is at most its own quantum; for a dense record, a beam of many quanta per Node, nothing on the board, the quantum passing in the books alone with the deficit printed, the undepleted beam, `take.faced`) and its count in the books down by one; descending, stimulated emission, one quantum given back into the drive (by the count where it is local and whole at the Node, nothing where it is a beam) and its count up by one; the present record's realised part laid at N + 1 at that Node in the direction of the part it leaves turned by the arriving record's phase at the Node, atan2(Y', X) of the window's two sums the close held (the phase passing with the quantum, `resonance.turned_direction`, `take.Item.arrival`), the remainder at the lay's origin, the part it leaves at N - 1 (the absorption); 4, a window with no meeting at a Node whose record reads its own parts, the record laid again in the complement of its outcome set at its whole count (the null window, `lists.null_window`); 5, the emission, at a Node whose record stands in an upper part, drawn at the lifetime's hazard 1 / tau per interval, per window while a window stands and per interval in the dark at the now (the beat's current of a one-part record at one Node being 0, named): one whole quantum passing from that record to the light family's record at the same Node, the upper part to N - 1, the lower to N + 1, light's record up by one whole quantum laid as a source in time at that Node over the emission's lifetime at the transition's declared resonance from the phase phi_e - phi_g, the two parts' directions read before the lay (`lists.emission`, `emission.start_of`, `emission.emitted_quantum`); 6, after the write the Node and its neighbours step by Rule3, nothing written at any other Node, no front; 7, the click line (`node_detector.reported`, the one click line kind of every reader), the window, the reader, the family and the parts, never a Node, the Node written standing in the LATTICE `lay` and `face` lines beside it. The record declared a NodeDetector is one Node by the world's declaration (its six Link factors 0, `cut`, so that it stays, held by its declaration as the node_detector's region is), its books the reader's own and at no Node; the Node knows no click. The region NodeDetectors' clicks at the credit's window close through the same act (`closed`, `lists.region`)."""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import credit, digits, flux, lists, node
from event_universe.act import Alternative, click
from event_universe.core.ports import arrival
from event_universe.node_detector import (
    NodeBooks,
    arriving,
    body_label,
    clock_advanced,
    dark,
    own_clock,
    read_families,
    sourcing,
)
from event_universe.records import Booking, Record
from event_universe.resonance import gathered, hopped, window_pair, window_turn
from event_universe.take import Item, faces_presented, relaid

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
    books = NodeBooks(number, row.family, record, row.nodes, row.counts, kind, 0, [], [], 0, [])
    for part, count in enumerate(kind.counts):
        relaid(board, books, part, count, [((1, 0), 1)] * len(books.nodes))


def laid_whole(board: Lattice) -> None:
    """The packets laid whole at this interval's end (`loader/packets.py`, `WholePacket`, a packet the world's schedule lays at an interval of the run): each its count of whole quanta laid at its Node through the one act with one alternative and no draw (`act.click`, `emission.emitted_quantum`, `laid_by_count` at the family's massless pair [den, den], A^2 = count T div 2 on the record's first line), the record's count in the books up by the count and one lay line for the host's tool; the experimenter's lay in time, from outside the Node as every lay is, before the records at Nodes read their arrivals."""
    for whole in board.world.wholes:
        if whole.interval == board.interval:
            den = board.families[whole.family].pair[1]
            items = [Item(whole.family, None, None, whole.count, (whole.at,), (den, den))]
            click(board, None, [Alternative(1, partial(list, items))])


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


def carries(board: Lattice, books: NodeBooks, total: int) -> bool:
    """Whether the body's number for its next draw carries `total` (the reader's ruling of 2026-10-20, (iii)): the number left within the interval, or the board read now where the interval holds none (`digits.read_of`, read and never written, so the draw after it reads the same number), at or above the total; the emission's draw alone asks it (`meeting.emission_drawn`), every other draw below its total refused by name (`features/click.drawn_from`)."""
    if books.left is not None:
        return books.left >= total
    reads = digits.reads_of(board, read_families(books), board.mask(books.nodes))
    return digits.read_of(board, reads, body_label(board, books))[0] >= total


def emission_drawn(board: Lattice, books: NodeBooks, grain: int) -> bool:
    """The emission's draw at the clock's grain, `grain` intervals (ALGEBRA.md, The click writes on the lattice (j), the fifth act, and the emission's clock): for each rate out of the part the record stands in, one click over the emission's alternatives (`lists.emission`: one list per direction the board holds at the hazard's weight over the span, the smaller of the grain and the lifetime, and nothing at the rest), the body's own read of the board; the first emission drawn is taken, its quantum laid and its line written by the act; returns whether one was. The exact dark (the reader's re-ruling of 2026-10-20, the law's sentence): a body whose read finds every digit at the lay's origin at its emission's draw does not draw (`digits.at_origin` over what the body reads, `digits.reads_of`, `node_detector.read_families`), nor where its number, read or left within the interval, stands below the emission row's total (`carries`, the reader's (iii) of 2026-10-20: the remainders at the body do not carry the draw, the budget's own count the measure of nothing to read); its emission falls at its window's close, the detector's declared when (`NodeBooks.deferred`, `emission_fell`); where the body's lines carry the total the emission's hazard is read from the board. The refusals by name stay for every other draw at the origin or below its total (an absorption, a probe, a second draw of one interval)."""
    for rate in books.declared.rates:
        if rate.leaves == books.part:
            if digits.at_origin(
                board, digits.reads_of(board, read_families(books), board.mask(books.nodes))
            ):
                books.deferred = True  # nothing to read: no draw, the emission at the window's close
                return False
            alternatives = lists.emission(board, books, rate, min(grain, rate.lifetime))
            if not carries(board, books, sum(a.weight for a in alternatives)):
                books.deferred = True  # the read below the row's total carries no hazard: no draw
                return False
            pick = click(board, books, alternatives)
            if pick < len(alternatives) - 1:
                return True
    return False


def emission_fell(board: Lattice, books: NodeBooks) -> bool:
    """The deferred emission at the window's close (the reader's re-ruling of 2026-10-20, (c) for the exact dark): where an emission's draw of the window found every digit at the lay's origin (`NodeBooks.deferred`, `emission_drawn`) and the window's draws gave none, the emission of the first rate out of the part the record stands in falls at the close without a draw, one alternative (`lists.emission` with `deferred`: the first declared direction, the body's Node of the largest share, the reading `reports.NO_DRAW` on its line), the act's lay and line as a drawn emission's; returns whether one fell."""
    rates = [rate for rate in books.declared.rates if rate.leaves == books.part]
    if not books.deferred or not rates:
        return False
    click(board, books, lists.emission(board, books, rates[0], rates[0].lifetime, deferred=True))
    return True


def absorptions_drawn(board: Lattice, closing: list[NodeBooks]) -> set[int]:
    """The absorptions drawn at the windows' end, one draw at a time per arriving family over every closing record's outcomes into it (ALGEBRA.md, The click writes on the lattice (f); `lists.absorption`): while the arriving record's count stands in the books, the records not done reading it close with one click, the first closing record's read of the board, the drawn record done for the window; nothing drawn ends the family's draws at this close, its unabsorbed share booked by the row; returns the records done."""
    done: set[int] = set()
    pairs = [(b, t) for b in closing for t in b.declared.transitions if t.leaves == b.part]
    for drive in sorted({t.drive for _books, t in pairs}):
        while board.credit.counts[drive] > 0:
            outcomes = [(b, t) for b, t in pairs if b.number not in done and t.drive == drive]
            if not outcomes:
                break
            first, alternatives = closing[0], lists.absorption(board, drive, outcomes)
            pick = click(board, first, alternatives)
            if pick == len(outcomes):
                break
            done.add(outcomes[pick][0].number)
    return done


def absorbing(board: Lattice, books: NodeBooks) -> bool:
    """Whether an absorption's or a probe's draw falls due for the body at this close (ALGEBRA.md, What a body reads, the reader's G2 of 2026-10-20: one draw per body per interval, the absorption at the window's end and the emission at the clock's grain on different intervals where both fall due): a transition out of its part by a drive whose count stands in the books (`lists.absorption`)."""
    return any(
        t.leaves == books.part and board.credit.counts[t.drive] > 0 for t in books.declared.transitions
    )


def closed(board: Lattice) -> None:
    """The region NodeDetectors' clicks at the credit's window's close (`credit.counted_windows`; ALGEBRA.md #the-click-is-the-meeting): first the count on the board of every record the sides read at this close against the books' count, refused by name where the board's share lies more than half a quantum and the walk since the lay from the books' count while no front of the record stands (ALGEBRA.md, The count on the board, 2026-10-20; `credit.count_held`, `Lattice.count`), then per family of quanta its list from the window's books through the one act (`lists.region`, one alternative and no draw of its own, the places drawn inside it by the credit's read of the board; for a record of several parts the sides' draws in the order of their closes with the run back, the write at the birth and the run forward between them, `lists.readings`, `meeting_back`), then the window's books emptied, the inflows, the sides' moments, the passages and the numbers the reads left, and the births of the records whose count reached 0 (the write's books, the coefficients, the scale, the realised ports and the reference, stand until the next birth, so the count on the board reads the erased wave over its scale, `credit.born`), the count beginning again."""
    books = board.credit
    for index, moments in books.moments.items():  # the records the sides read at this close
        standing = books.counts.get(index, 0) > 0 and not any(f.family == index for f in books.fronts)
        if standing and any(credit.standing(m) for m in moments.values()):
            if not credit.count_held(board, index):
                raise RuntimeError(
                    f"the record's count on the board, {board.count(index)}, differs from the books' count "
                    f"{books.counts[index]} at the close {board.interval}: the board's share moved against the "
                    "books' by more than the walk; the books' line names the deficit"
                )
    for index in board.order:
        found = lists.region(board, index)
        if found is not None:
            click(board, None, [found])
    books.intake.clear()
    books.moments.clear()
    for index in [index for index in books.births if books.counts.get(index, 0) <= 0]:
        books.births.pop(
            index
        )  # a record gone: its next quantum a new birth (`credit.born` resets the write's books)
    books.passages.clear()
    books.left.clear()
    books.bias.clear()


def jumped(board: Lattice) -> None:
    """The records at Nodes that are NodeDetectors at the end of an interval: first the packets the world lays whole at this interval (`laid_whole`, the probe's lay at the body's Node by the schedule); then each record gathers the records arriving at its Node into its window's sums (`resonance.gathered`, the arriving level per drive family read once, `arriving`), one more interval elapsed and its own clock advanced (`node_detector.clock_advanced`); the window closes at its declared length; at the close the window's turn of the labels (`turned_labels`, once per window, as W sub-turns with the carry) and the body's windows counted, then the draws and the writes, every one the one act's over the table's rows (`act.click`, `lists.py`): the emissions first record by record (`emission_drawn`: at the window's close while a window stands, the grain the count of the window's lit intervals, `NodeBooks.lit`, at every interval in the dark, `dark`, the grain 1, the lifetime's hazard 1 / tau per interval either way; one draw per body per interval (ALGEBRA.md, What a body reads, the reader's G2 of 2026-10-20): a dark interval at the window's close draws once over the interval and the window's lit intervals together, so every interval of the window enters exactly one draw's span and the summed hazard over a window is W / tau whatever its dark intervals, ALGEBRA.md, The dark; a window with no dark interval the length itself, bit for bit; where an absorption falls due at the close too (`absorbing`), the absorption draws at the window's end and the emission's span is carried to the next interval (`NodeBooks.due`), dropped where the body left its part, the acts' order the declared one; a body whose read found every digit at the lay's origin at an emission's draw of the window gives at the close where the draws gave none, `emission_fell`), then the absorptions in one draw per arriving family over the records that gave none (`absorptions_drawn`), then the null window of every record of several parts that neither gave nor took (`lists.null_window`; a record of one part reads no part of itself and has none); the windows begun again. A body standing in a part it gives from (a rate out of it) counts its window from its lay, its emission's when, lit or dark; a taker's window opens at its first lit interval (C2)."""
    laid_whole(board)
    own = {b.number: sourcing(board, b) for b in board.credit.bodies}  # C5: read once per body
    for books in board.credit.bodies:
        books.left, books.bias = None, None  # the click's read of the board: one per body per interval
        levels = {
            t.drive: 0 if t.drive in own[books.number] else arriving(board, books, t.drive)
            for t in books.declared.transitions
        }
        gathered(books.references, books.declared.transitions, levels)
        draw = books.declared.draw
        timed = (
            draw is not None and draw.window is not None
        )  # C2: a window opens at the first lit interval
        gives = any(rate.leaves == books.part for rate in books.declared.rates)  # an emitter's when
        books.elapsed += (
            1 if books.elapsed or not timed or gives or not dark(board, books, own[books.number]) else 0
        )
        clock_advanced(board, books)
    closing = [
        b
        for b in board.credit.bodies
        if b.declared.draw is not None
        and b.declared.draw.window is not None
        and b.elapsed == b.declared.draw.window
    ]
    for books in closing:
        turned_labels(board, books)
        books.windows += 1
    ended, lit_numbers = {books.number for books in closing}, set()
    for books in board.credit.bodies:
        if books.declared.draw is None:
            continue
        lit, closes = not dark(board, books, own[books.number]), books.number in ended
        books.lit += lit
        span = books.due + (0 if lit else 1) + (books.lit if closes else 0)  # one draw, G2
        books.due, given = 0, False
        if span and closes and absorbing(board, books):
            books.due = (
                span  # the absorption at the window's end; the emission's draw at the next interval
            )
        elif span:
            given = emission_drawn(board, books, span)
        if not given and closes and books.deferred:
            given = emission_fell(board, books)  # E1: the deferred emission falls at the close
        if given:
            lit_numbers.add(books.number)
    quiet = [books for books in closing if books.number not in lit_numbers]
    done = absorptions_drawn(board, quiet)
    for books in quiet:
        if books.number in done:
            books.due = 0  # the body left its part at the close: the carried span was that part's
        elif len(books.counts) > 1:  # a record of one part reads none
            click(board, books, lists.null_window(board, books))
    for books in closing:
        books.elapsed, books.lit, books.intake, books.passages = 0, 0, {}, {}
        books.deferred = False
