"""The credit's books (features/click; ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision: after a click the paths are cancelled on the lattice, not in the clicks' books, Rule3 kept): where the world declares the `draw` (its window in intervals, its seed, its generator's multiplier and increment, `loader/draw.py`) the credit keeps the books of a window from the node_detectors' reports, the conserved form's own current through each boundary Node's front Ports, the plain current times the Link's factor Q_ij in the unit G^2 (`reports.weighted`; ALGEBRA.md #the-click-is-the-meeting, the credit's booking), summed over the window per family and region and, for a family of several parts, the joint share J per combination of the sides' ports accumulated from the parts' sums (the same numbers the click and parts lines carry), and counts the window (`counted_windows`); at the window's end the region NodeDetectors draw with the declared generator and write their click at one Node through the one act (`lists.region`, `act.click`, `meeting.closed`), the loop's act from outside the Node as the lay and the receding face are, forward only; the record's count goes down by one per credited quantum, the run's accounting in the output, and at 0 the record is uncreditable, whatever its levels still show. The books are the credit's and stand at no Node; the Node knows no click and no family of clicks; a world without the key keeps empty books and runs as before bit for bit."""

from __future__ import annotations

import itertools
from collections.abc import Sequence
from dataclasses import dataclass, field
from math import gcd
from typing import TYPE_CHECKING

import numpy as np

from event_universe import growth, share
from event_universe.core import paces
from event_universe.core.ports import PORTS
from event_universe.core.rule3 import division_forward
from event_universe.emission import Emitter, Source, packet_unit, registered
from event_universe.features.click import Face
from event_universe.front import Front
from event_universe.loader.derived import count_wall
from event_universe.loader.draw import BACK, Draw, Ports, ports_of
from event_universe.loader.keys import Node
from event_universe.loader.packets import axes_waves
from event_universe.node_detector import NodeBooks, Passage, Weighed, books_of
from event_universe.reports import PORT_NAMES, weighted

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Intake = dict[
    Node, list[int]
]  # per boundary Node of a region, at the file's coordinates, the window's inflow per Port
Joints = dict[
    tuple[int, ...], int
]  # per combination of the sides' ports (0 the +, 1 the -) the window's J
Sums = dict[
    str, list[list[int]]
]  # per region the record's lines' level sums [now, before] of one interval
Levels = list[
    list[list[int]]
]  # per side, in the sides' order, the lines' sums [now, before] of one interval
Terms = list[tuple[int, tuple[int, ...]]]  # the amplitude's terms: the sign and the part each side reads
Clock = list[
    int
]  # a node_detector's own clock: its proper time in whole intervals and the remainder carried


@dataclass
class Books:
    """The credit's books: its declaration (None where the world declares none), the intervals elapsed in the window, the generator's state, the record's count per family of quanta, the count left to credit, the window's inflows per family and region per boundary Node in the unit G^2 (`booked`), the window's joint shares per family of several parts, the sides, the regions declaring a pattern with their two ports, in the file's order, the records at Nodes declared NodeDetectors with their own books (`node_detector.NodeBooks`), the erasing fronts begun where a record's count reached 0 (`Front`, the family, the click's Node and its interval), the faces the click act presents, per interval (features/click, `Face`), the log the inverse presents again, the sources in time, the unit of one quantum of each record, W_rec, read once at the books' origin (`record_unit`), the records that held no count at the origin, whose unit is set at their first lay to the lay's own share and held from there (the advisor's word; `emission.emitted_quantum`), each declared region's own clock per family it reads (`Clock`, the proper time carried over the board's intervals, `clocked_regions`), the count of the windows closed, the node_detectors' event clock, and per family the deficit, the quanta taken from its record and written nowhere (`deficits`, the undepleted beam, `twist.faced`; the board's share exceeds the books' count by it, printed in the books' line, `Lattice.books`), and per family the share its windows left unabsorbed (`unabsorbed`, keyed by the family of quanta as the counts are, one record per family in every shipped world, an account to be split by record where a world declares several records of one family; in the readers' labels' unit: the count's share at the record's first draw, down by every null window's shares, dropped when a quantum passes into or out of the record, so that a later reader's draw reads its share conditionally on the earlier windows' nulls, `lists.absorption`, `act.written`; ALGEBRA.md, The click writes on the lattice (7), the mathematician's line) with the denominator each unabsorbed share is kept in (`unabsorbed_units`, the closing bodies' norms' least common multiple at the draw that wrote it, read in another closing set's denominator by the division act, `unabsorbed_in`; ALGEBRA.md, The absorption, the draw (b)); Part F, the piece's p_a per axis read at the close from the arriving record's momentum terms and share at the region's Nodes, scaled to one count (`node_detector.piece_momentum`), into the credit line; Part G (both hands' lines of 2026-10-10, the click with two receivers), the emitters' book per light family (`emitters`, `emission.Emitter`: per emitting body the quanta it gave that still stand in the record and whether the recoil was paid at the lay, kept after the Source's span is spent until its count reaches 0; the file's lays register nothing), the weights of the one draw of the piece's source at a click (`twist.recoiled`); the click's plan, C7: per record the remainder of the credit's division carried into the next window (`remainders`, `quanta_through`), L759's row 12, kept in the books for the next window, nature's counter having no window edge; C4: per family and region the record's passage over the window, its momentum terms and its share at the region summed, the piece's two sums (`passages`, `node_detector.Passage`, booked beside the inflow in `booked`)."""

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
    remainders: dict[int, int] = field(default_factory=dict)
    passages: dict[tuple[int, str], Passage] = field(default_factory=dict)
    states: dict[str, int] = field(default_factory=dict)
    conditioning: dict[int, list[int]] = field(default_factory=dict)
    levels: dict[int, list[Levels]] = field(default_factory=dict)
    lays: dict[int, list[dict[str, object]]] = field(default_factory=dict)

    @property
    def runs_back(self) -> bool:
        """Whether the world's draw declares the meeting that runs back, `meeting: back` (`loader/draw.py`; `meeting_back`): the sides then draw each at its own place with its own state (`states`, per side, begun at its first draw of the window from the declared seed, its name and the window's number, `features/click.hashed`, and cleared at the close), the partner on the record's parts re-weighted by what the first port read (`conditioning`, per family the integers lambda_k, `conditioned`), its share from the window's parts sums kept per interval (`levels`, per family, `joined`), and the lays the acts wrote stand in the log per interval for the run back to cross (`lays`, the lay lines as `reports.lay` writes them, `lay.written`, `meeting_back.crossed`); every one empty on the root's worlds, which run as built."""
        return self.declaration is not None and self.declaration.meeting == BACK

    def unabsorbed_in(self, drive: int, norms: list[int]) -> tuple[int, int]:
        """The one denominator of the bodies closing a drive's interval and the record's unabsorbed share read in it (ALGEBRA.md, The absorption, the draw (b); `lists.absorption`): the denominator the least common multiple of the bodies' norms, each the sum of its labels' squares, by the division act, so that each body's transfer share scales to it exactly; the unabsorbed share the count's at the record's first draw, and a share left by an earlier draw in another denominator (`unabsorbed_units`) brought to this one by the division act and kept in it from here; a body with no labels, its norm 0, has no transfer and cannot close, refused by name."""
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
        """The record's windows' account ends as a quantum passes into or out of it (`act.written`): its unabsorbed share and the denominator it is kept in dropped, to begin again at the count left."""
        self.unabsorbed.pop(family, None)
        self.unabsorbed_units.pop(family, None)

    def window_of(self, interval: int) -> list[int]:
        """The window closing at `interval`, [first, last], the declaration's length of intervals."""
        assert self.declaration is not None
        return [interval - self.declaration.window + 1, interval]

    @classmethod
    def of(cls, board: Lattice) -> Books:
        """The books at the start: every family of quanta's unit of one quantum from its own rotation (`record_unit`, held through the run; the click's plan, C1) and its count its laid share in that unit (`counted`, the books' origin read as a count; a record with no count at the origin named among `empty`, its unit set at its first lay), the generator at the declared seed, the emitters' book holding the file's lay for every family laid with a count, `Emitter(None, count, False)` (Part H, the hands' SHOULD: a laid light beside an emitter is drawn between the body and the lay by their counts, `twist.drawn_emitter`; the lay drawn is the file's, no receiver, `THE_LAY` with `LOST_TO_LAY`), every other book empty."""
        found = board.world.draw
        units = {index: record_unit(board, index) for index in board.order}
        counts = {index: counted(board, index, board.laid[index], units[index]) for index in board.order}
        sides = [
            (r.name, ports_of(r.axis or r.basis, r.pattern))
            for r in board.world.node_detectors
            if r.pattern
        ]  # a side's setting its `axis` for planes or its `basis` for real lines
        bodies = books_of(board)
        emitters: dict[int, list[Emitter]] = {}
        for index in board.order:  # Part H (the hands' SHOULD): the file's lay in the emitters' draw
            if counts[index] > 0:
                registered(emitters, index, None, False, counts[index])
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
            emitters=emitters,
        )


def counted(board: Lattice, index: int, total: int | None, unit: int) -> int:
    """A share in the current's units as whole quanta of the record's own unit, (total + W_rec div 2) div W_rec by the division act (`share.quanta_of`; `record_unit`, C1), 0 where it is not read: the reading of the record's count."""
    return 0 if total is None else int(share.quanta_of(np.array([total], dtype=object), unit, object)[0])


def record_unit(board: Lattice, index: int) -> int:
    """The unit of one quantum of a record, W_rec, from the record's own rotation and not from a reading (the click's plan, C1; the count's line, Q = count x W_c sin omega for a monochromatic record; nature: E = h nu, one count of light carries the form of its own frequency): W_rec = (the largest x with x^2 <= W_c^2 (den^2 - num_r^2) div den^2) with (num_r, den) the record's rotation, W_c = 3 den T; a family with a gap at its rest rotation, W_c sin omega_0, the count's wall of the record's unit (`loader/derived.count_wall`); a massless family laid as a packet at the wave [p, q] (the family's first packet; a family laid at several waves takes the first's) at the rotation of that wave, den cos omega = (num_l (den cos k + 2 den)) div (3 den_l) by the division act, the band's line with the transverse wave numbers 0, den cos k by the rotation act's integer search, the unit then W_c sin omega through the one form of a born quantum's (`emission.packet_unit`, `features/click.wave_cosine`, `emission.born_unit`; 4242 and 5414 of 6000 at k = pi / 4; the generator reads a packet's count in the same unit, tools/pixel_mode.py); W_c, the massless wall, for a massless family laid by no packet, until a record empty at the origin is first laid, when its unit becomes the lay's own, W_c sin Omega for a quantum given at Omega (`emission.emitted_quantum`); held through the run (a face removes one quantum's share with one count). What moves against the reading of the share over the count: a massless packet's count is its share over W_c sin omega and no longer over W_c, one count at pi / 4 the amplitude 110 and not 165 on two_photons' packet, and the beams' counts by 1 / sin omega."""
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


def quanta_through(books: Books, index: int, inflow: int, link_unit: int) -> int:
    """The clicks a window's inflow is worth in the record's own unit, the remainder carried (the click's plan, C7; L759's row 12: the remainder kept in the books for the next window): the inflow booked in the unit G^2 of the Link's factor (`booked`, `reports.weighted`), G the run's Link unit `link_unit`, with the record's carried remainder added, over one quantum's unit W_rec G^2, (inflow + r + W_rec G^2 div 2) div W_rec G^2 by the division act (`record_unit`), one division at the window's close and no rounding per Link, the division's own remainder less the half unit carried per record into the next window (`Books.remainders`, per record and never per detector, so that no share is dropped at a window's edge and the windows' count differs from the dropped-remainder count by at most one per window), the share's own rounding, the count the plain formula reads where no tension stood (ALGEBRA.md #the-click-is-the-meeting, the credit's booking); the cap by the count is the credit's (`lists.region`), and the remainder advances as computed also where the clicks are capped by the count or the count stands at 0, the excess consumed as main dropped it."""
    unit = books.units[index] * link_unit * link_unit
    half = int(division_forward(unit, 2, 0)[0])
    through, rest = division_forward(inflow + books.remainders.get(index, 0), unit, half)
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


def joined(board: Lattice, index: int, sums: Sums) -> None:
    """The book of the meeting (ALGEBRA.md #the-click-is-the-meeting, the one form): per combination of the sides' ports the joint share J accumulated over the window on both members of the level pair from the sides' parts sums of one interval, J += (SUM_k c_k PROD_sides now_k)^2 + (SUM_k c_k PROD_sides before_k)^2, c_k the product over the sides of e_k at their ports, as the reader `tools/bell_gate.py` reads the same sums; nothing where the world declares no draw or no side. For a record of plane parts (the spin branch, 2026-10-19) a part's sum is its pair (re, im) on its two lines, the product over the sides a plane's product and the square the pair's norm, J += |SUM_k c_k PROD_sides psi^s_k|^2 per member: the spinor amplitude's share under the detectors' declared axes (`loader/draw.settings_of_the_law`), the real-line form the same with im at 0. The pair's amplitude is built from the record's sign under exchange, the family's declaration (`FamilyRule.exchange`, the key `exchange`; ALGEBRA.md, Spin, closed for the paper as a route, The family's sign under exchange, 2026-10-19), read here and by the lists' factor and by nothing at the Node: the symmetric record, and a family declaring no sign, SUM_k over the same part k at every side, the form as it stood; the antisymmetric record SUM_{k != l} sign(l - k) e^L_k psi^L_k e^R_l psi^R_l over the ordered pairs of parts across two sides, the determinant of the two sides' parts, equal at two parts to the symmetric form with the crossed pattern [[0, 1], [-1, 0]] on one side term by term (e^L_0 e^R_1 - e^L_1 e^R_0), so the singlet's numbers come out with the plain identity pattern on both detectors; more than two sides refused by name, a third quantum's determinant being a third side's declaration the law has not made."""
    books = board.credit
    if books.declaration is None or not books.sides:
        return
    family = board.families[index]
    parts, width = family.parts, family.width  # the lines per part: one for a real line, two for a plane
    levels = [sums.get(name, [[0, 0]] * (parts * width)) for name, _ports in books.sides]
    joint = books.joints.setdefault(index, {})
    if family.exchange < 0 and len(books.sides) != 2:
        raise ValueError(
            f"{family.name!r} declares the antisymmetric sign under exchange and the world declares "
            f"{len(books.sides)} sides: the pair's amplitude is the determinant of two sides' parts, and a third "
            "side's determinant is a declaration the law has not made (ALGEBRA.md, Spin, closed for the paper "
            "as a route)"
        )
    terms = terms_of(family.exchange, parts, len(books.sides))
    for key in itertools.product(range(len(PORT_NAMES)), repeat=len(books.sides)):
        readers = [
            (ports[port], found)
            for (_name, ports), port, found in zip(books.sides, key, levels, strict=True)
        ]
        total = sum(squared(terms, readers, member, width, family.plane) for member in range(2))
        joint[key] = joint.get(key, 0) + total
    if (
        books.runs_back
    ):  # the window's sums kept per interval: the partner's re-weighted share reads them
        books.levels.setdefault(index, []).append(levels)


def terms_of(exchange: int, parts: int, sides: int) -> Terms:
    """The amplitude's terms as (the sign, the part each side reads): the record's sign under exchange, the family's declaration, read by the click alone (ALGEBRA.md, Spin, closed for the paper as a route); the symmetric record and a family declaring no sign SUM_k over the same part at every side; the antisymmetric record SUM_{k != l} sign(l - k) over the ordered pairs across the two sides, the determinant, so that two sides reading the same part cancel exactly and the sign, and not a detector's pattern, carries the pair."""
    if exchange >= 0:
        return [(1, (k,) * sides) for k in range(parts)]
    return [(1 if k < m else -1, (k, m)) for k in range(parts) for m in range(parts) if k != m]


def squared(
    terms: Terms,
    readers: Sequence[tuple[Sequence[int], Sequence[Sequence[int]]]],
    member: int,
    width: int,
    plane: bool,
) -> int:
    """The norm squared of the amplitude at one member of the level pair (`joined`, the one form; the partner's re-weighted share of the meeting that runs back reads its one side by it, `reweighted_share`): SUM over the terms of the sign times the product over the readers of e_k psi_k, each reader its coefficient per part and its lines' sums [now, before] of the interval, a part's sum its pair (re, im) on its two lines for a plane and (re, 0) for a real line, the product a plane's product; the sum's norm, real^2 + imaginary^2, an integer."""
    real, imaginary = 0, 0
    for sign, which in terms:
        product = (sign, 0)
        for (coefficients, found), k in zip(readers, which, strict=True):
            factor = coefficients[k]
            re = factor * found[k * width][member]
            im = factor * found[k * width + 1][member] if plane else 0
            product = (product[0] * re - product[1] * im, product[0] * im + product[1] * re)
        real, imaginary = real + product[0], imaginary + product[1]
    return real * real + imaginary * imaginary


def marginal_of(joint: Joints, side: int) -> list[int]:
    """One side's marginal from the credit's joint shares (the meeting that runs back, the first side's weights; ALGEBRA.md, The click is the meeting of the future with the past): per port of the side the sum of J over the other sides' ports, the books' integers as they stand at the close, no new act and no new reading; for parts laid alike it equals the side's parts' shares credited alone and never the coherent one-side sum."""
    return [
        sum(share for key, share in joint.items() if key[side] == port)
        for port in range(len(PORT_NAMES))
    ]


def conditioned(board: Lattice, index: int, first: int, port: int) -> list[int]:
    """The re-weighting of the partner's parts by what the first side's port read of them, the credit's reading through the root and never a write (ALGEBRA.md, The click is the meeting of the future with the past, the re-weighting lambda_k = e_k(port_A) a_k; the owner's word of 2026-10-19): from the amplitude's own terms (`terms_of`), per term the sign times the first side's coefficient on the part it reads, added on the part the partner reads, so that lambda_k = e^A_k(p) for the symmetric record and the undeclared and lambda_l = SUM_k sign(l - k) e^A_k(p) for the antisymmetric (at two parts lambda_0 = -e^A_1(p), lambda_1 = e^A_0(p), the determinant's conditional), SUM_l e^B_l(q) lambda_l psi^B_l then the amplitude at the realised p; the part's lay weight a_k is 1, the one lay act laying every part of a record alike (`Lattice.lay`); integers, carried in the books (`Books.conditioning`); two sides, the partner the other."""
    family, books = board.families[index], board.credit
    assert len(books.sides) == 2  # the loader admits the meeting that runs back on two sides
    partner, coefficients = 1 - first, books.sides[first][1][port]
    lambdas = [0] * family.parts
    for sign, which in terms_of(family.exchange, family.parts, len(books.sides)):
        lambdas[which[partner]] += sign * coefficients[which[first]]
    return lambdas


def reweighted_share(board: Lattice, index: int, side: int, lambdas: Sequence[int]) -> list[int]:
    """The partner's share at each of its ports under the conditioning, its own one-side sum with the parts re-weighted (ALGEBRA.md, The click is the meeting of the future with the past: the partner's click meets the re-weighted record): S(q) = SUM over the window's intervals and both members of |SUM_k e_k(q) lambda_k psi_k|^2 from the window's parts sums the books kept (`Books.levels`, `joined`), the plane product and the norm as `squared` forms them, an integer per port; with the parts stepping alike, S(q) / SUM S = J(p, q) / SUM_q J(p, q) exactly, the first side's factor common to the ports and cancelling, so the two readings give the one joint distribution (tests/test_the_meeting_back.py)."""
    family, books = board.families[index], board.credit
    terms = terms_of(0, family.parts, 1)  # one side: the sum over its parts
    ports = books.sides[side][1]
    found = []
    for port in range(len(PORT_NAMES)):
        weights = [e * weight for e, weight in zip(ports[port], lambdas, strict=True)]
        found.append(
            sum(
                squared(terms, [(weights, levels[side])], member, family.width, family.plane)
                for levels in books.levels.get(index, [])
                for member in range(2)
            )
        )
    return found


def counted_windows(board: Lattice) -> bool:
    """The window's count at the end of an interval: where the world declares the draw, the node_detectors' own clocks advanced (`clocked_regions`), one more interval elapsed, and at the window's length the window counted among the closed and the count beginning again; returns whether the window closed at this interval, the region NodeDetectors' clicks then the act's (`meeting.closed`, `lists.region`)."""
    books = board.credit
    if books.declaration is None:
        return False
    clocked_regions(board)
    books.elapsed += 1
    if books.elapsed < books.declaration.window:
        return False
    books.windows += 1
    books.elapsed = 0
    return True
