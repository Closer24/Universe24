"""The credit's books (features/click; ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision: after a click the paths are cancelled on the lattice, not in the clicks' books, Rule3 kept): where the world declares the `draw` (its window in intervals, `loader/draw.py`) the credit keeps the books of a window from the node_detectors' reports, the conserved form's own current through each boundary Node's front Ports, the plain current times the Link's factor Q_ij in the unit G^2 (`reports.weighted`; ALGEBRA.md #the-click-is-the-meeting, the credit's booking), summed over the window per family and region and, for a family of several parts, each declared side's own second moments of the parts' sums over its region (`credit.moments_booked`, the same numbers the parts lines carry; nothing joint in the books, the owner's word of 2026-10-20), and counts the window (`counted_windows`); at the window's end the region NodeDetectors draw by the click's read of the board (`digits.read_of`, `node_detector.credit_draw`) and write their click at one Node through the one act (`lists.region`, `act.click`, `meeting.closed`), the loop's act from outside the Node as the lay and the receding face are, forward only; the record's count goes down by one per credited quantum, the run's accounting in the output, and at 0 the record is uncreditable, whatever its levels still show. The books are the credit's and stand at no Node; the Node knows no click and no family of clicks; a world without the key keeps empty books and runs as before bit for bit."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from math import gcd
from typing import TYPE_CHECKING

import numpy as np

from event_universe import growth, meeting_back, share
from event_universe.core import paces
from event_universe.core.ports import PORTS
from event_universe.core.rule3 import division_forward
from event_universe.emission import Emitter, Source, packet_unit, registered
from event_universe.features.click import Face
from event_universe.front import Front
from event_universe.loader.derived import FamilyRule, count_wall
from event_universe.loader.draw import CONE, Draw, Gauss, Pattern, Ports, norm, ports_of, reduced_write
from event_universe.loader.keys import Node
from event_universe.loader.packets import axes_waves
from event_universe.node_detector import NodeBooks, Passage, Weighed, books_of
from event_universe.records import NodeState
from event_universe.reports import weighted

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Intake = dict[
    Node, list[int]
]  # per boundary Node of a region, at the file's coordinates, the window's inflow per Port
Levels = list[
    list[list[int]]
]  # per side, in the sides' order, the lines' sums [now, before] of one interval
Terms = list[tuple[int, tuple[int, ...]]]  # the amplitude's terms: the sign and the part each side reads
Clock = list[
    int
]  # a node_detector's own clock: its proper time in whole intervals and the remainder carried


@dataclass
class Books:
    """The credit's books: its declaration (None where the world declares none), the intervals elapsed in the window, the record's count per family of quanta, the count left to credit, the window's inflows per family and region per boundary Node in the unit G^2 (`booked`), the sides' own second moments per family of several parts (`moments`), the sides, the regions declaring a pattern with their two ports, in the file's order, the records at Nodes declared NodeDetectors with their own books (`node_detector.NodeBooks`), the erasing fronts begun where a record's count reached 0 (`Front`, the family, the click's Node and its interval), the faces the click act presents, per interval (features/click, `Face`), the log the inverse presents again, the sources in time, the unit of one quantum of each record, W_rec, read once at the books' origin (`record_unit`), the records that held no count at the origin, whose unit is set at their first lay to the lay's own share and held from there (the advisor's word; `emission.emitted_quantum`), each declared region's own clock per family it reads (`Clock`, the proper time carried over the board's intervals, `clocked_regions`), the count of the windows closed, the node_detectors' event clock, and per family the deficit, the quanta taken from its record and written nowhere (`deficits`, the undepleted beam, `twist.faced`; the board's share exceeds the books' count by it, printed in the books' line, `Lattice.books`), and per family the share its windows left unabsorbed (`unabsorbed`, keyed by the family of quanta as the counts are, one record per family in every shipped world, an account to be split by record where a world declares several records of one family; in the readers' labels' unit: the count's share at the record's first draw, down by every null window's shares, dropped when a quantum passes into or out of the record, so that a later reader's draw reads its share conditionally on the earlier windows' nulls, `lists.absorption`, `act.written`; ALGEBRA.md, The click writes on the lattice (7), the mathematician's line) with the denominator each unabsorbed share is kept in (`unabsorbed_units`, the closing bodies' norms' least common multiple at the draw that wrote it, read in another closing set's denominator by the division act, `unabsorbed_in`; ALGEBRA.md, The absorption, the draw (b)); Part F, the piece's p_a per axis read at the close from the arriving record's momentum terms and share at the region's Nodes, scaled to one count (`node_detector.piece_momentum`), into the credit line; Part G (both hands' lines of 2026-10-10, the click with two receivers), the emitters' book per light family (`emitters`, `emission.Emitter`: per emitting body the quanta it gave that still stand in the record and whether the recoil was booked at the lay, kept after the Source's span is spent until its count reaches 0; the file's lays register nothing), the weights of the one draw of the piece's source at a click (`twist.recoiled`); the click's plan, C7: per record the remainder of the credit's division carried into the next window (`remainders`, `quanta_through`), L759's row 12, kept in the books for the next window, nature's counter having no window edge; C4: per family and region the record's passage over the window, its momentum terms and its share at the region summed, the piece's two sums (`passages`, `node_detector.Passage`, booked beside the inflow in `booked`); the click's read of the board: per record and side (None for a record of one part) the number the read left after the close's last draw (`left`, `node_detector.credit_draw`, emptied at the close, `meeting.closed`) and the bias bound of its first draw, booked on the side's or the region's line (`bias`, `features/click.bias_bound`, emptied with it), nothing of it across windows and no seed."""

    declaration: Draw | None
    elapsed: int
    counts: dict[int, int]
    intake: dict[tuple[int, str], Intake]
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
    remainders: dict[int, int] = field(default_factory=dict)
    passages: dict[tuple[int, str], Passage] = field(default_factory=dict)
    left: dict[tuple[int, str | None], int] = field(default_factory=dict)
    bias: dict[tuple[int, str | None], list[int]] = field(default_factory=dict)
    lays: dict[int, list[dict[str, object]]] = field(default_factory=dict)
    support: tuple[Node, ...] = ()
    reference: dict[int, list[NodeState]] = field(default_factory=dict)
    cone: dict[int, int] = field(default_factory=dict)
    births: dict[int, tuple[int, tuple[Node, ...]]] = field(default_factory=dict)
    birth: int = 0
    moments: dict[int, dict[str, list[list[Gauss]]]] = field(default_factory=dict)
    patterns: dict[str, Pattern] = field(default_factory=dict)
    written: dict[int, list[Gauss]] = field(default_factory=dict)
    scale: dict[int, int] = field(default_factory=dict)
    taken: dict[int, dict[str, tuple[int, tuple[Node, tuple[int, ...]] | None, bool]]] = field(
        default_factory=dict
    )  # per record and side: the realised port, the credited Node with its Ports, whether the sequence is settled
    alike: dict[int, bool] = field(default_factory=dict)
    weights: dict[tuple[int, str], list[int]] = field(default_factory=dict)
    regrown: list[NodeState] = field(default_factory=list)
    stepped: dict[int, int] = field(default_factory=dict)

    @property
    def reads_sides(self) -> bool:
        """Whether the world holds a record of several parts read at declared sides, the click that writes at the record's birth (ALGEBRA.md, The click is the meeting of the future with the past; the owner's word of 2026-10-20; `meeting_back`, `lists.readings`): the sides then draw each at its own place by its own read of the board (`left`, per record and side, the number left of the side's read at its first draw of the close, `node_detector.credit_draw`, emptied at the close), in the order of their closes, each on its own second moments with the Gram of the sides after it (`moments`, `patterns`, `weights`), the realised ports kept per record and side until the family's next birth (`taken`: the port, the credited Node and whether the sequence it was drawn in is settled by the count's write; a side clicks again on a settled record with the same port and writes nothing, the reader's ruling of 2026-10-20, precision one), the write's coefficients, scale and likeness per record (`written`, `scale`, `alike`), and the lays the acts wrote stand in the log per interval for the run back to cross (`lays`, the lay lines as `reports.lay` writes them, `lay.written`, `meeting_back.crossed`); every one empty on a world with no such record, which runs as built, byte for byte."""
        return self.declaration is not None and bool(self.sides)

    @property
    def reach(self) -> str | None:
        """The run back's reach where the click runs back (ALGEBRA.md, The meeting's reading, the run back's reach; the owner's word of 2026-10-19; `loader/draw.REACHES`): the draw's declared word, `board` or `cone`, and the record's light cone, `cone`, where the draw declares none; None on a world with no record of several parts at declared sides. The books hold the births' book (`births`, per family the birth's interval and its Nodes at the file's coordinates, `support_of`, `born`), the birth and the Nodes of the record being run (`birth`, `support`, S_0 at the file's coordinates, the cone's root), and in the cone the reference per record (`reference`, every family's NodeState as the board stood at the record's birth: frame 0 for a record laid at the start, kept once at the books' start, the board at the birth for a record born during the run, kept once at the write step, `meeting_back.frame_of`, `born`; ALGEBRA.md, The births' book, the born record's reference, 2026-10-20) and the cone's volume per interval, |G(t)| the Nodes within t - t_b + 1 Links of S_0 (`cone`, written by the run back and forward, `cone.stepped_alone`), the look's header's words; and, through the reading alone, the cone stepped alone's own books (the owner's word of 2026-10-20): frame 0 regrown to the board's shape (`regrown`, resized with the growths the run back pops and the run forward finds anew, `cone.grown_at`) and the Node-steps per interval (`stepped`, the box with its ring in the cone's reach, the whole board's volume in the board's reach, the header's `cone_stepped`)."""
        if not self.reads_sides:
            return None
        assert self.declaration is not None
        return self.declaration.reach or CONE

    def unabsorbed_in(self, drive: int, norms: list[int]) -> tuple[int, int]:
        """The one denominator of the bodies closing a drive's interval and the record's unabsorbed share read in it (ALGEBRA.md, The absorption, the draw (b); `lists.absorption`): the denominator the least common multiple of the bodies' norms, each the sum of its labels' squares, by the division act, so that each body's transfer share scales to it exactly; the unabsorbed share the count's at the record's first draw, and a share left by an earlier draw in another denominator (`unabsorbed_units`) brought to this one by the division act and kept in it from here; a body with no labels, its norm 0, has no transfer and cannot close, refused by name."""
        if min(norms) <= 0:
            raise ValueError("a body closing a drive's interval holds labels: its norm is above 0")
        unit = norms[0]
        for other in norms[1:]:
            unit = int(division_forward(unit * other, gcd(unit, other), 0)[0])
        kept = self.unabsorbed.setdefault(drive, self.counts[drive] * unit)
        born = self.unabsorbed_units.setdefault(drive, unit)
        self.unabsorbed[drive] = share = int(division_forward(kept * unit, born, 0)[0])
        self.unabsorbed_units[drive] = unit
        return unit, share

    def account_ended(self, family: int) -> None:
        """The record's windows' account ends as a quantum passes into or out of it (`act.written`): its unabsorbed share and the denominator it is kept in dropped, to begin again at the count left."""
        self.unabsorbed.pop(family, None)
        self.unabsorbed_units.pop(family, None)

    def window_of(self, interval: int) -> list[int]:
        """The window closing at `interval`, [first, last], the declaration's length of intervals."""
        assert self.declaration is not None and self.declaration.window is not None  # the world's window
        return [interval - self.declaration.window + 1, interval]

    @classmethod
    def of(cls, board: Lattice) -> Books:
        """The books at the start: every family of quanta's unit of one quantum from its own rotation (`record_unit`, held through the run; the click's plan, C1) and its count its laid share in that unit (`counted`, the books' origin read as a count; a record with no count at the origin named among `empty`, its unit set at its first lay), the emitters' book holding the file's lay for every family laid with a count, `Emitter(None, count, False)` (Part H, the hands' SHOULD: a laid light beside an emitter is drawn between the body and the lay by their counts, `twist.drawn_emitter`; the lay drawn is the file's, no receiver, `THE_LAY` with `LOST_TO_LAY`), every other book empty."""
        found = board.world.draw
        units = {index: record_unit(board, index) for index in board.order}
        counts = {index: counted(board, index, board.laid[index], units[index]) for index in board.order}
        sides = [
            (r.name, ports_of(r.axis or r.basis, r.pattern, r.turn))
            for r in board.world.node_detectors
            if r.pattern
        ]  # a side's setting its `axis` for planes or its `basis` for real lines
        patterns = {r.name: r.pattern for r in board.world.node_detectors if r.pattern}
        bodies = books_of(board)
        emitters: dict[int, list[Emitter]] = {}
        for index in board.order:  # Part H (the hands' SHOULD): the file's lay in the emitters' draw
            if counts[index] > 0:
                registered(emitters, index, None, False, counts[index])
        books = cls(
            found,
            0,
            counts,
            {},
            sides,
            bodies,
            [],
            {},
            [],
            units,
            {index for index in board.order if counts[index] <= 0},
            emitters=emitters,
            patterns=patterns,
        )
        books.births = {  # the births' book: the records laid at the start, born at the interval 0
            index: (0, support_of(board, index)) for index in board.order if counts[index] > 0
        }
        books.support = tuple(sorted({at for _t, nodes in books.births.values() for at in nodes}))
        if books.reach == CONE:  # frame 0, the reference of every record laid at the start, kept once
            books.reference = dict.fromkeys(books.births, meeting_back.frame_of(board))
        return books


def born(board: Lattice, index: int, was: int) -> None:
    """The births' book at the write step (ALGEBRA.md, The births' book, the owner's word of 2026-10-20): an act's lay that raised a record's count from 0 (`was`, the count before the lay) books the family's birth, the interval and the lay's Nodes at the file's coordinates (`support_of` after the lay: a directed packet's whole section and not the item's one Node, the reader's W4), for every kind of lay alike (the lay by the count, the directed packet, the source in time at its first increment; the file's lay at the start enters at the books' start with the interval 0); the run back of the click that runs back stops there (`meeting_back.birth_of`) and the record's light cone is the birth's cone (`support_of`). Where a record of several parts read at declared sides is given a quantum while its birth stands in the book, before the window's close, it is refused by name: one birth, one root; the write's books of the family's former record are emptied at the new birth (`Books.written`, `scale`, `taken`, `alike`, `reference`: the new record unwritten, no port realised), and in the cone's reach the board as it stood at the birth is kept once as the record's reference (`Books.reference`, the cone's assertions' frame for a record born during the run, as frame 0 is for a record laid at the start; ALGEBRA.md, The births' book, the born record's reference, 2026-10-20); the births standing at a count of 0 are dropped at the window's close (`meeting.closed`)."""
    books, family = board.credit, board.families[index]
    if index in books.births and books.reads_sides and family.parts > 1:
        raise RuntimeError(
            f"the record of {family.name!r} was born twice, at the intervals {books.births[index][0]} and "
            f"{board.interval}: the click that writes at the birth reads one birth per record; lay the second quantum "
            "after the window's close or in a record of its own"
        )
    if was <= 0 < books.counts.get(index, 0):
        for book in (books.written, books.scale, books.taken, books.alike, books.reference):
            book.pop(index, None)  # a new birth: unwritten, no port realised, no reference
        books.births[index] = (
            board.interval,
            support_of(board, index),
        )  # the whole lay's Nodes, a section too
        if (
            books.reach == CONE and family.parts > 1
        ):  # the born record's reference, the board at its birth
            books.reference[index] = meeting_back.frame_of(board)


def counted(board: Lattice, index: int, total: int | None, unit: int) -> int:
    """A share in the current's units as whole quanta of the record's own unit, (total + W_rec div 2) div W_rec by the division act (`share.quanta_of`; `record_unit`, C1), 0 where it is not read: the reading of the record's count."""
    return 0 if total is None else int(share.quanta_of(np.array([total], dtype=object), unit, object)[0])


def standing(moments: Sequence[Sequence[Gauss]]) -> bool:
    """Whether a side's second moments hold a number other than 0, the beam arrived in its window (`moments_booked`; the pairs read by their numbers, a pair (0, 0) standing for nothing)."""
    return any(entry != (0, 0) for row in moments for entry in row)


def scale_of(board: Lattice, index: int) -> int:
    """The record's scale, the norm's square of the coefficients standing on its parts, SUM_k w_k^2 with w_k the cumulative coefficient the clicks wrote on the part k at the birth (`Books.written`, `meeting_back.realised`), the parts' count n before any write (every w_k 1): the parts alike at the birth, the record's share over the board after the writes is the unwritten share times the scale over n (ALGEBRA.md, The count on the board, 2026-10-20)."""
    return sum(norm(w) for w in board.credit.written.get(index, [(1, 0)] * board.families[index].parts))


def count_of(board: Lattice, index: int) -> int | None:
    """The record's count read from the board (ALGEBRA.md, The count on the board, the owner's word of 2026-10-20): (n S + scale W div 2) div (scale W) by the one division act (`counted`, `share.quanta_of`), n the record's parts, S its share over the board in the current's units (`Lattice.total_share`), W its unit W_rec (`Books.units`, `record_unit`) and scale the written coefficients' norm (`scale_of`, n before any write, so a record of one part reads S over W as it always did, bit for bit); None where the family holds no share to read; equal to the books' count at the lay and at every window's close before the acts (`meeting.closed`), the books' count moving at the act and the board's following at one Link per interval behind the erasing front, the difference the empty wave's share, a diagnostic."""
    total = board.total_share(index)[0]
    if total is None:
        return None
    unit = board.credit.units[index] * scale_of(board, index)
    return counted(board, index, total * board.families[index].parts, unit)


def record_unit(board: Lattice, index: int) -> int:
    """The unit of one quantum of a record, W_rec, from the record's own rotation and not from a reading (the click's plan, C1; the count's line, Q = count x W_c sin omega for a monochromatic record; nature: E = h nu, one count of light carries the form of its own frequency): W_rec = (the largest x with x^2 <= W_c^2 (den^2 - num_r^2) div den^2) with (num_r, den) the record's rotation, W_c = 3 den T; a family with a gap at its rest rotation, W_c sin omega_0, the count's wall of the record's unit (`loader/derived.count_wall`); a massless family laid as a packet at the wave [p, q] (the family's first packet; a family laid at several waves takes the first's) at the rotation of that wave, den cos omega = (num_l (den cos k + 2 den)) div (3 den_l) by the division act, the band's line with the transverse wave numbers 0, den cos k by the rotation act's integer search, the unit then W_c sin omega through the one form of a born quantum's (`emission.packet_unit`, `features/click.wave_cosine`, `emission.born_unit`; 4242 and 5414 of 6000 at k = pi / 4; the generator reads a packet's count in the same unit, tools/pixel_mode.py); W_c, the massless wall, for a massless family laid by no packet, until a record empty at the origin is first laid, when its unit becomes the lay's own, W_c sin Omega for a quantum given at Omega (`emission.emitted_quantum`); held through the run (a face removes one quantum's share with one count). What moves against the reading of the share over the count: a massless packet's count is its share over W_c sin omega, one count at pi / 4 the amplitude 110 on two_photons' packet, and the beams' counts by 1 / sin omega."""
    family, action = board.families[index], board.world.quantum_action
    wall = count_wall(family, action)
    packets = [p for p in board.world.packets if p.family == index]
    if family.pair[0] != family.pair[1] or not packets:
        return wall
    units = {packet_unit(wall, family.pair, axes_waves(p)) for p in packets}
    if len(units) > 1:  # one record, one unit: packets at waves of different units are refused by name
        raise ValueError(
            f"{family.name}: its packets are laid at waves of different units {sorted(units)}; a family's "
            "record has one unit (C1), and its packets one wave's cosine"
        )
    return units.pop()


def reduced(board: Lattice, index: int, coefficients: Sequence[Gauss]) -> list[Gauss]:
    """The coefficients the click writes on the record's parts (the reader's ruling of 2026-10-20; ALGEBRA.md, The click is the meeting of the future with the past: at the root it writes): the realised port's integers over the record's surviving parts, a part surviving while its cumulative coefficient in the books is other than 0 (`Books.written`, every part before any write; the books' word and no reading of the board's levels), divided by their greatest common divisor, the direction's least integers, so the write is the realised term's direction among the parts and never its magnitude alone; one value on every surviving part (a scaling, a global sign included) is the identity, 1 on every part, the port realised all the same (`loader/draw.reduced_write`, the one arithmetic, read at load by the bound gate too)."""
    return reduced_write(board.credit.written.get(index, [(1, 0)] * len(coefficients)), coefficients)


def count_held(board: Lattice, index: int) -> bool:
    """Whether the record's share on the board agrees with the books' count (ALGEBRA.md, The count on the board, the owner's word of 2026-10-20; the check at every close, `meeting.closed`): 2 |n S - c scale W| <= scale W + 2 n |S - S_lay|, the books' count c within half a quantum of the board's reading (`count_of`, the same n, W and scale) and the walk since the lay, the share's drift the books' line prints (`Lattice.laid`, S_lay the share at the start), exact integers and no division; the walk's term 0 for a record born during the run, whose birth's share is the books' count's; True where the family holds no share to read."""
    books, family = board.credit, board.families[index]
    total, laid = board.total_share(index)[0], board.laid[index]
    if total is None:
        return True
    born_later = books.births.get(index, (0,))[0] > 0
    walk = 0 if born_later or laid is None else abs(total - laid)
    unit = books.units[index] * scale_of(board, index)
    return 2 * abs(family.parts * total - books.counts[index] * unit) <= unit + 2 * family.parts * walk


def quanta_rounded(books: Books, index: int, inflow: int, link_unit: int, parts: int, scale: int) -> int:
    """The whole quanta a side's window brought in, the count's rounding with nothing carried: the side's gate (ALGEBRA.md, The meeting's reading, the reader's F4 of 2026-10-20: a side draws where a whole quantum has come through its window, the count's rounding over its region and its window; a share below it is no click), the remainder left to `quanta_through`. The count reads a record of n parts from its share S over the board as n S over scale W_rec (`count_of`); a side reads one of the record's beams, its inflow I in the unit G^2 summed over the parts' lines and taken in the quantum of one part, so (n n I + scale W_rec G^2 div 2) div (scale W_rec G^2) by the division act, `scale` the written coefficients' norm standing while the window was booked (`scale_of` before the close's writes, n before any write), the same reading before and after a write (the singlet's two beams, half the record each, read 0.997 and 1.001 at the sides and round to one each; after the first side's write the second side's beam reads the same; a background at a tenth of the signal rounds to 0)."""
    unit = books.units[index] * link_unit * link_unit * scale
    half = int(division_forward(unit, 2, 0)[0])
    return int(division_forward(inflow * parts * parts, unit, half)[0])


def quanta_through(books: Books, index: int, inflow: int, link_unit: int, parts: int = 1) -> int:
    """The clicks a window's inflow is worth in the record's own unit, the remainder carried (the click's plan, C7; L759's row 12: the remainder kept in the books for the next window): the inflow booked in the unit G^2 of the Link's factor (`booked`, `reports.weighted`), G the run's Link unit `link_unit`, with the record's carried remainder added, over one quantum's unit W_rec G^2, (inflow + r + W_rec G^2 div 2) div W_rec G^2 by the division act (`record_unit`), one division at the window's close and no rounding per Link, the division's own remainder less the half unit carried per record into the next window (`Books.remainders`, per record and never per detector, so that no share is dropped at a window's edge and the windows' count differs from the dropped-remainder count by at most one per window), the share's own rounding, the count the plain formula reads where no tension stood (ALGEBRA.md #the-click-is-the-meeting, the credit's booking); the cap by the count is the credit's (`lists.region`), and the remainder advances as computed also where the clicks are capped by the count or the count stands at 0, the excess consumed as main dropped it."""
    scale = sum(norm(w) for w in books.written.get(index, [(1, 0)] * parts))  # n before any write
    unit = books.units[index] * link_unit * link_unit * scale
    half = int(division_forward(unit, 2, 0)[0])
    through, rest = division_forward(inflow * parts + books.remainders.get(index, 0), unit, half)
    books.remainders[index] = int(rest) - half
    return int(through)


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


def parts_of(family: FamilyRule, count: int) -> list[int]:
    """The part of every line of a family's records by the line's number, `count` lines: the records laid out alike, parts times width lines each (`records.record_slice`), each part a block of `width` lines within its record; an enumeration of the blocks, no division."""
    found: list[int] = []
    while len(found) < count:
        found += [part for part in range(family.parts) for _i in range(family.width)]
    return found[:count]


def positions_of(family: FamilyRule, count: int) -> list[int]:
    """The position of every line within its part, 0 the real line or a plane's cosine line, 1 a plane's sine line (`parts_of`, the same enumeration): the plane's two lines the Gaussian write turns together."""
    found: list[int] = []
    while len(found) < count:
        found += [i for _part in range(family.parts) for i in range(family.width)]
    return found[:count]


def moments_booked(board: Lattice, index: int, sums: Mapping[str, Sequence[Sequence[int]]]) -> None:
    """The book of a side's own read of a record of several parts (ALGEBRA.md, The meeting's reading; The meeting's identity, the Gram theorem; the owner's word of 2026-10-20): per side the second moments of its own region's parts' sums over the window on both members of the level pair, M_kl += SUM_member sigma_k sigma_l (a plane part's sum its pair (re, im) on its two lines, the product the pair's real inner product re_k re_l + im_k im_l), from the parts' sums of one interval as the `parts` lines carry them (`credit.Books.moments`, per family per side an n x n matrix of integers); nothing of another side enters a side's book: a side's weights at the close are the quadratic form of its coefficients on its own M with the Gram of the sides unrealised (`side_weights`)."""
    books, family = board.credit, board.families[index]
    parts, width = family.parts, family.width
    book = books.moments.setdefault(index, {})
    for name, _ports in books.sides:
        found = sums.get(name)
        if found is None:
            continue
        moments = book.setdefault(name, [[(0, 0)] * parts for _k in range(parts)])
        for member in range(2):
            for k in range(parts):
                for m in range(parts):
                    re_k, re_m = found[k * width][member], found[m * width][member]
                    im_k, im_m = (
                        (found[k * width + 1][member], found[m * width + 1][member])
                        if family.plane
                        else (0, 0)
                    )
                    was = moments[k][
                        m
                    ]  # psi_k conj(psi_m): Hermitian, the imaginary part 0 on real lines
                    moments[k][m] = (
                        was[0] + re_k * re_m + im_k * im_m,
                        was[1] + im_k * re_m - re_k * im_m,
                    )


def booked(
    board: Lattice,
    index: int,
    name: str,
    nodes: np.ndarray,
    facing: Sequence[np.ndarray],
    weighed: Weighed,
) -> None:
    """The book of a window's inflows: per family and declared region the conserved form's own current through each boundary Node's front Ports, per Port, each record's plain current times its Link's factor Q_ij in the unit G^2 (`reports.weighted` on the family's read `weighed` through the region's front `facing`, per Port and Node; ALGEBRA.md #the-click-is-the-meeting, the credit's booking: the Link's factor squared the one weight, no rounding per Link) summed over the window's intervals, the Node at the file's coordinates; the Ports' sums the shares of the draw of the one Node the click is written at and, over the regions, of the window's count (`quanta_through`), the Ports the hole's face set (`node_detector.arrival_ports`); beside it the family's passage through the region's Nodes, its momentum terms and its share there from the same read, summed over the window, the piece's two sums (`node_detector.Passage`, C4); nothing where the world declares no draw."""
    if board.credit.declaration is None:
        return
    board.credit.passages.setdefault((index, name), Passage()).booked(nodes, weighed[index])
    book = board.credit.intake.setdefault((index, name), {})
    for port, through in enumerate(weighted(facing, weighed[index])):
        for at in np.argwhere(through != 0):
            key = growth.declared(at, board.offset)
            book.setdefault((key[0], key[1], key[2]), [0] * PORTS)[port] += int(through[tuple(at)])


def support_of(board: Lattice, index: int) -> tuple[Node, ...]:
    """The Nodes a family's record stands on, at the file's coordinates: every Node where a line of the family holds a level other than 0, now or before; at the start the lay's Nodes, S_0, the root of the record's light cone for a record laid at the start (`Books.births`, the interval 0, `Books.of`, `born`; ALGEBRA.md, The meeting's reading, the run back's reach; The births' book)."""
    found = np.zeros(board.shape, dtype=bool)
    for line in board.states[index].lines:
        found |= np.asarray((line.now != 0) | (line.before != 0))
    return tuple(
        (int(at[0]) - board.offset[0], int(at[1]) - board.offset[1], int(at[2]) - board.offset[2])
        for at in np.argwhere(found)
    )


def terms_of(exchange: int, parts: int, sides: int) -> Terms:
    """The amplitude's terms as (the sign, the part each side reads): the record's sign under exchange, the family's declaration, read by the click alone (ALGEBRA.md, Spin, closed for the paper as a route); the symmetric record and a family declaring no sign SUM_k over the same part at every side; the antisymmetric record SUM_{k != l} sign(l - k) over the ordered pairs across the two sides, the determinant, so that two sides reading the same part cancel exactly and the sign, and not a detector's pattern, carries the pair."""
    if exchange >= 0:
        return [(1, (k,) * sides) for k in range(parts)]
    return [(1 if k < m else -1, (k, m)) for k in range(parts) for m in range(parts) if k != m]


def counted_windows(board: Lattice) -> bool:
    """The window's count at the end of an interval: where the world declares the draw, the node_detectors' own clocks advanced (`clocked_regions`), one more interval elapsed, and at the window's length the window counted among the closed and the count beginning again; returns whether the window closed at this interval, the region NodeDetectors' clicks then the act's (`meeting.closed`, `lists.region`)."""
    books = board.credit
    if books.declaration is None:
        return False
    assert books.declaration.window is not None  # the world's draw declares its window
    clocked_regions(board)
    books.elapsed += 1
    if books.elapsed < books.declaration.window:
        return False
    books.windows += 1
    books.elapsed = 0
    return True
