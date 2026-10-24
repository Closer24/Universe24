"""The credit's books (features/click; ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision: after a click the paths are cancelled on the lattice, not in the clicks' books, Rule3 kept): where the world declares the `draw` (its window in intervals, `loader/draw.py`) the credit keeps the books of a window from the node_detectors' reports, the conserved form's own current through each boundary Node's front Ports, the plain current times the Link's factor Q_ij in the unit G^2 (`reports.weighted`; ALGEBRA.md #the-click-is-the-meeting, the credit's booking), summed over the window per family and region and, for a family of several parts, each declared side's own second moments of the parts' sums over its region (`credit.moments_booked`, the same numbers the parts lines carry; nothing joint in the books, the owner's word of 2026-10-20), and counts the window (`counted_windows`); at the window's end the region NodeDetectors draw by the click's read of the board (`digits.read_of`, `node_detector.credit_draw`) and write their click at one Node through the one act (`lists.region`, `act.click`, `meeting.closed`), the loop's act from outside the Node as the lay and the receding face are, forward only; the record's count goes down by one per credited quantum, the run's accounting in the output, and at 0 the record is uncreditable, whatever its levels still show. The books are the credit's and stand at no Node; the Node knows no click and no family of clicks; a world without the key keeps empty books and runs as before bit for bit."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from event_universe import share
from event_universe.loader.derived import count_wall
from event_universe.loader.keys import Node

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


@dataclass
class Books:
    """The credit's books: its declaration (None where the world declares none), the intervals elapsed in the window, the record's count per family of quanta, the count left to credit, the window's inflows per family and region per boundary Node in the unit G^2 (`booked`), the sides' own second moments per family of several parts (`moments`), the sides, the regions declaring a pattern with their two ports, in the file's order, the records at Nodes declared NodeDetectors with their own books (`node_detector.NodeBooks`), the log the inverse presents again, the sources in time, the unit of one quantum of each record, W_rec, read once at the books' origin (`record_unit`), each declared region's own clock per family it reads (`Clock`, the proper time carried over the board's intervals, `clocked_regions`), the count of the windows closed, the node_detectors' event clock, and per family the deficit, the quanta taken from its record and written nowhere (`deficits`, the undepleted beam, `take.below_quantum`; the board's share exceeds the books' count by it, printed in the books' line, `Lattice.books`), and per family the share its windows left unabsorbed (`unabsorbed`, keyed by the family of quanta as the counts are, one record per family in every shipped world, an account to be split by record where a world declares several records of one family; in the readers' labels' unit: the count's share at the record's first draw, down by every null window's shares, dropped when a quantum passes into or out of the record, so that a later reader's draw reads its share conditionally on the earlier windows' nulls, `lists.absorption`, `act.written`; ALGEBRA.md, The click writes on the lattice (7), the mathematician's line) with the denominator each unabsorbed share is kept in (`unabsorbed_units`, the closing bodies' norms' least common multiple at the draw that wrote it, read in another closing set's denominator by the division act, `unabsorbed_in`; ALGEBRA.md, The absorption, the draw (b)); Part F, the piece's p_a per axis read at the close from the arriving record's momentum terms and share at the region's Nodes, scaled to one count (`node_detector.piece_momentum`), into the credit line; Part G (both hands' lines of 2026-10-10, the click with two receivers), the emitters' book per light family (`emitters`, `emission.Emitter`: per emitting body the quanta it gave that still stand in the record and whether the recoil was booked at the lay, kept after the Source's span is spent until its count reaches 0; the file's lays register nothing), the weights of the one draw of the piece's source at a click (`take.recoiled`); the click's plan, C7: per record the remainder of the credit's division carried into the next window (`remainders`, `quanta_through`), L759's row 12, kept in the books for the next window, nature's counter having no window edge, and signed since 2026-10-21 (the owner's word: the floor and the remainder's draw), the remainder below one quantum where the close's draw credited none and the remainder less the unit, the quantum owed, where it did (`whether`), so that over the run the counts sum to the inflow's whole quanta within one; C4: per family and region the record's passage over the window, its momentum terms and its share at the region summed, the piece's two sums (`passages`, `node_detector.Passage`, booked beside the inflow in `booked`); the click's read of the board: per record and side (None for a record of one part) the number the read left after the close's last draw (`left`, `node_detector.credit_draw`, emptied at the close, `meeting.closed`) and the bias bound of its first draw, booked on the side's or the region's line (`bias`, `features/click.bias_bound`, emptied with it), nothing of it across windows and no seed."""

    counts: dict[int, int]
    units: dict[int, int] = field(default_factory=dict)
    deficits: dict[int, int] = field(default_factory=dict)
    lays: dict[int, list[dict[str, object]]] = field(default_factory=dict)
    births: dict[int, tuple[int, tuple[Node, ...]]] = field(default_factory=dict)

    @classmethod
    def of(cls, board: Lattice) -> Books:
        """The books at the start: every family of quanta's unit of one quantum from its own rotation (`record_unit`, held through the run; the click's plan, C1) and its count its laid share in that unit (`counted`, the books' origin read as a count; a record with no count at the origin named among `empty`, its unit set at its first lay), the emitters' book holding the file's lay for every family laid with a count, `Emitter(None, count, False)` (Part H, the hands' SHOULD: a laid light beside an emitter is drawn between the body and the lay by their counts, `take.drawn_emitter`; the lay drawn is the file's, no receiver, the lay with the recoil lost to the lay), every other book empty."""
        units = {index: record_unit(board, index) for index in board.order}
        counts = {i: counted(*share.count_read(board, i, board.laid[i], units[i])) for i in board.order}
        books = cls(counts, units)
        books.births = {  # the births' book: the records laid at the start, born at the interval 0
            index: (0, support_of(board, index)) for index in board.order if counts[index] > 0
        }
        return books


def born(board: Lattice, index: int, was: int) -> None:
    """The births' book at the write step (ALGEBRA.md, The births' book, the owner's word of 2026-10-20): an act's lay that raised a record's count from 0 (`was`, the count before the lay) books the family's birth, the interval and the lay's Nodes at the file's coordinates (`support_of` after the lay: a directed packet's whole section and not the item's one Node, the reader's W4), for every kind of lay alike (the lay by the count, the directed packet, the source in time at its first increment; the file's lay at the start enters at the books' start with the interval 0); the run back of the click that runs back stops there (`meeting_back.birth_of`) and the record's light cone is the birth's cone (`support_of`). Where a record of several parts read at declared sides is given a quantum while its birth stands in the book, before the window's close, it is refused by name: one birth, one root; the write's books of the family's former record are emptied at the new birth (`Books.written`, `scale`, `taken`, `alike`, `reference`: the new record unwritten, no port realised), and in the cone's reach the board as it stood at the birth is kept once as the record's reference (`Books.reference`, the cone's assertions' frame for a record born during the run, as frame 0 is for a record laid at the start; ALGEBRA.md, The births' book, the born record's reference, 2026-10-20); the births standing at a count of 0 are dropped at the window's close (`meeting.closed`)."""
    books = board.credit
    if was <= 0 < books.counts.get(index, 0):
        books.births[index] = (
            board.interval,
            support_of(board, index),
        )  # the whole lay's Nodes, a section too


def counted(total: int | None, unit: int) -> int:
    """A share in the current's units as whole quanta of the record's own unit, (total + W_rec div 2) div W_rec by the division act (`share.quanta_of`; `record_unit`, C1), 0 where it is not read: the reading of the record's count."""
    return 0 if total is None else int(share.quanta_of(np.array([total], dtype=object), unit, object)[0])


def count_of(board: Lattice, index: int) -> int | None:
    """The record's count read from the board (ALGEBRA.md, The count on the board, the owner's word of 2026-10-20): (n S + scale W div 2) div (scale W) by the one division act (`counted`, `share.quanta_of`), n the record's parts, S its share over the board in the current's units (`Lattice.total_share`), W its unit W_rec (`Books.units`, `record_unit`) and scale the written coefficients' norm (`scale_of`, n before any write, so a record of one part reads S over W as it always did, bit for bit); None where the family holds no share to read; equal to the books' count at the lay and at every window's close before the acts (`meeting.closed`), the books' count moving at the act and the board's following at one Link per interval behind the erasing front, the difference the empty wave's share, a diagnostic."""
    total, unit = share.count_read(board, index, board.total_share(index)[0], board.credit.units[index])
    if total is None:
        return None
    return counted(total, unit)


def record_unit(board: Lattice, index: int) -> int:
    """The unit of one quantum of a record, W_rec, from the record's own rotation and not from a reading (the click's plan, C1; the count's line, Q = count x W_c sin omega for a monochromatic record; nature: E = h nu, one count of light carries the form of its own frequency): W_rec = (the largest x with x^2 <= W_c^2 (den^2 - num_r^2) div den^2) with (num_r, den) the record's rotation, W_c = 3 den T; a family with a gap at its rest rotation, W_c sin omega_0, the count's wall of the record's unit (`loader/derived.count_wall`); a massless family laid as a packet at the wave [p, q] (the family's first packet; a family laid at several waves takes the first's) at the rotation of that wave, den cos omega = (num_l (den cos k + 2 den)) div (3 den_l) by the division act, the band's line with the transverse wave numbers 0, den cos k by the rotation act's integer search, the unit then W_c sin omega through the one form of a born quantum's (`emission.packet_unit`, `features/click.wave_cosine`, `emission.born_unit`; 4242 and 5414 of 6000 at k = pi / 4; the generator reads a packet's count in the same unit, tools/pixel_mode.py); W_c, the massless wall, for a massless family laid by no packet, until a record empty at the origin is first laid, when its unit becomes the lay's own, W_c sin Omega for a quantum given at Omega (`emission.emitted_quantum`); held through the run (a face removes one quantum's share with one count). What moves against the reading of the share over the count: a massless packet's count is its share over W_c sin omega, one count at pi / 4 the amplitude 110 on two_photons' packet, and the beams' counts by 1 / sin omega."""
    return count_wall(board.families[index], board.world.quantum_action)


def support_of(board: Lattice, index: int) -> tuple[Node, ...]:
    """The Nodes a family's record stands on, at the file's coordinates: every Node where a line of the family holds a level other than 0, now or before; at the start the lay's Nodes, S_0, the root of the record's light cone for a record laid at the start (`Books.births`, the interval 0, `Books.of`, `born`; ALGEBRA.md, The meeting's reading, the run back's reach; The births' book)."""
    found = np.zeros(board.shape, dtype=bool)
    for line in board.states[index].lines:
        found |= np.asarray((line.now != 0) | (line.before != 0))
    return tuple((int(at[0]), int(at[1]), int(at[2])) for at in np.argwhere(found))
