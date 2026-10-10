"""The click's momentum and its items (the engine V2, Parts F and G; ALGEBRA.md, The click's algebra beyond the law, The lattice momentum, The click's momentum on the board): a click's items and the re-lay that keeps each Node's own direction, the taker's lines twisted to the piece's momentum by a bisection on the phase line to the quarter turn's cap (`twisted`, `quarter_turn`, `folded_lines`), the piece's source folded back by the same twist and drawn among the emitters by the quanta each holds (`folded_source`, `recoiled`, `drawn_emitter`), the loss booked by name (`unpaid`), the board's momentum per family (`fan_momentum`) and the faces presented and reported; meeting.py writes the click with them."""

from __future__ import annotations

import itertools
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from event_universe import node
from event_universe.core.ports import AXES, run_offsets
from event_universe.core.rule3 import division_forward
from event_universe.emission import Emitter
from event_universe.features import phase
from event_universe.features.click import Face, laid_pairs, standing
from event_universe.lay import laid
from event_universe.lay import written as lay_written
from event_universe.loader.derived import quanta_records
from event_universe.loader.keys import Node
from event_universe.node_detector import (
    NodeBooks,
)
from event_universe.plane import Faces
from event_universe.reports import (
    BODY,
    LOST_TO_DECLARATION,
    LOST_TO_LAY,
    LOST_TO_REGION,
    LOST_TO_SOURCE,
    LOST_TO_TAKER,
    PAID_AT_EMISSION,
    THE_LAY,
    UNPAID_BY_REGION,
    face,
)

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


def relaid(
    board: Lattice,
    books: NodeBooks,
    part: int,
    count: int,
    phase: tuple[int, int] | None,
    sense: int,
) -> None:
    """The lay of one part of the record over the NodeDetector's Nodes through the one act (features/click, `standing`, `laid_pairs`; `lay.laid`): at every Node of the region the part's lines move to the levels of its share of `count` quanta, A_i^2 = A^2 weight_i / total in the counts' proportion, standing in the direction `phase` and the sense `sense`, the change from what stands handed to the act with no weights (a record at its Node is laid as built, named) and the remainder at the division's origin at every Node of the region, the lay lines the write step's; the count's own lines alone, the other parts untouched. Part H (both hands' lines of 2026-10-10 on the whole trial, MUST 1: the null window's re-lay keeps the fold): where `phase` is None the re-lay keeps each Node's own direction, the pair (re, im) standing at that Node on the part's two lines setting the direction of its new levels (`own_direction`), so that a phase gradient across the region, the write's twist of the taker (`twisted`) and the source's fold (`folded_source`), survives the re-lay to the lay's rounding and the lattice momentum it carries is not discarded unbooked; the acts the same lay act's, the count's share laid as before; one direction at every Node where `phase` names one (the click's write, the part entered in the leaving part's direction turned by the arrival)."""
    family, action = board.families[books.index], board.world.quantum_action
    first = node.record_slice(family, books.record).start + part * family.width
    total, at = sum(books.weights), board.mask(books.nodes)
    levels: list[tuple[np.ndarray, np.ndarray]] = []
    for here, weight in zip(books.nodes, books.weights, strict=True):
        share = (weight, total)
        if books.declared.conversions:
            pairs = laid_pairs(
                count, action, family.pair, books.declared.sense, family.plane, family.laid, share
            )
        else:
            direction = phase if phase is not None else own_direction(board, books, part, here)
            (re, im), (re_before, im_before) = standing(
                count, action, family.pair, direction, sense, share
            )
            pairs = [(re, re_before), (im, im_before)]
        levels = levels or [
            (node.zeros(board.shape, object), node.zeros(board.shape, object)) for _ in pairs
        ]
        where = tuple(np.add(here, board.offset))
        for (now, before), (nows, befores) in zip(pairs, levels, strict=True):
            nows[where], befores[where] = now, before
    origin = board.half_wall(
        books.index
    )  # a fresh lay of the part: every Node of the region at the origin
    for number, (nows, befores) in enumerate(levels):
        line = board.states[books.index].lines[first + number]
        changes = (np.where(at, nows - line.now, 0), np.where(at, befores - line.before, 0))
        laid(board, books.index, first + number, changes, None, origin, at)


def levels_at(
    board: Lattice, books: NodeBooks, part: int, here: Node | None = None
) -> tuple[int, int, int, int]:
    """A part's levels at one Node of the reader, (re_now, im_now, re_before, im_before), read from its two lines; the reader's first Node where none is named: the click's write lays the part in one direction at every Node of the region and the first Node carries that phase, a twisted part (`twisted`, `folded_source`) standing at each Node in its own (Part H, MUST 1, `own_direction`)."""
    family, state = board.families[books.index], board.states[books.index]
    first = node.record_slice(family, books.record).start + part * family.width
    at = tuple(np.add(books.nodes[0] if here is None else here, board.offset))
    re, im = state.lines[first], state.lines[first + 1 if family.plane else first]
    return int(re.now[at]), int(im.now[at]), int(re.before[at]), int(im.before[at])


def own_direction(board: Lattice, books: NodeBooks, part: int, here: Node) -> tuple[int, int]:
    """The direction a part stands in at one Node of the reader, the pair (re, im) of its levels now there (`levels_at`), the direction of the null window's re-lay at that Node (Part H, MUST 1: the re-lay keeps each Node's own direction, so the fold survives it); the first Node's where the part stands at 0 there (nothing of its own to keep)."""
    re, im = levels_at(board, books, part, here)[:2]
    return (re, im) if (re, im) != (0, 0) else levels_at(board, books, part)[:2]


@dataclass(frozen=True)
class Item:
    """One entry of a click's list (the mathematician's hand with the advisor's second, two hands; the owner's word, one generic implementation the node_detector operates): the record by its family and, for a record declared a NodeDetector at one Node, its number among `bodies` (None for a record spread over the board), the part (None for every line of a spread record, no line alone), the change of its count, +1, -1 or 0 (the null window moves no count), the Nodes written at, the file's coordinates, and for a spread record given whole quanta the form of its lay (`emission.emitted_quantum`): the pair its lay stands at where the list names one (the conversion's records out at their family's massless pair [den, den], the lay by the count at one Node, the two hands) with, for a plane, the sense of its lay as the conversion's table declares it (0 for real lines; `emission.laid_by_count`), else the resonance and the span of a source in time (the emission's, the transition's declared resonance and the lifetime, the mathematician's hand with the advisor's second); the absorption's items carry the arriving record's phase at the close, (X, Y'), `arrival`, by which the entered part's direction is turned (`parted`), and the light's item the two parts' (re, im) at the Node, `levels`, the excited and the ground part's, the born source's phase phi_e - phi_g (`emission.start_of`); Part G: the light's item names the body whose click gives it (`emitter`, the emitters' book, `emission.registered`) and the entering item of an absorption names the piece's family (`drive`, the source's draw, `recoiled`)."""

    family: int
    body: int | None
    part: int | None
    delta: int
    nodes: tuple[Node, ...]
    pair: tuple[int, int] | None = None
    resonance: tuple[int, int] | None = None
    span: int = 0
    sense: int = 0
    width: int | None = None  # the open board's packet's Nodes across; None for the source in time
    direction: tuple[int, int] | None = None  # the packet's drawn direction, the axis and its sense
    arrival: tuple[int, int] | None = None
    levels: tuple[tuple[int, int], tuple[int, int]] | None = None
    momentum: tuple[int, int, int] | None = (
        None  # Part F: the piece's p_a per axis the entering part must carry
    )
    drive: int | None = None  # Part G: the family of the piece the entering part takes, its source drawn
    emitter: int | None = (
        None  # Part G: the body whose click's list gives this light quantum, by its number; None the file's
    )


Lists = list[list[Item]]  # the outcomes of one click, each the list written where it is drawn


Phase = tuple[tuple[int, int], int]  # a part's direction (re, im) and its sense, its Wronskian's sign


def books_named(board: Lattice, body: int) -> NodeBooks:
    """The books of the record declared a NodeDetector numbered `body` among the world's `bodies`."""
    return next(books for books in board.credit.bodies if books.number == body)


def faced(board: Lattice, item: Item) -> list[Node]:
    """The one comparison of the absorption and the emission at a spread record's Nodes (features/click, `Face`; ALGEBRA.md, The click writes on the lattice (b) and (d), the undepleted beam): at each Node named the record's booked share, the share the credit reads there (`Lattice.share_of`, the conserved form's density at the Node, `share.share`, read at the click from the levels the next step reads), against the record's own quantum W_rec (`credit.Books.units`); the Nodes where it is at most W_rec, the record there local and whole, are returned, the Nodes the click writes, and for an absorption the hole to 0 is booked there: for every line of the record one face at the next two intervals, the first Port preferred, so that Rule3 writes the level 0 and then the level before 0 with its own remainder (the mathematician's hand; the front erasing what spread beyond the Node where the count reaches 0); at a Node where the share is above W_rec a record of many quanta per Node is a beam, nature's undepleted beam, exact as the count per Node grows: no face, no lay and no front there, the levels standing (a one-Node lay into a beam would be the same point defect the hole of a dense record was), the quantum passing in the books alone (`written`: the count and the deficit); nothing assigned at any Node."""
    lines = range(board.families[item.family].record)
    intervals = (board.interval + 1, board.interval + 2)
    unit = board.credit.units[item.family]
    shares = board.share_of(item.family, 1, board.mask(item.nodes))[0]
    nodes = [(int(n[0]), int(n[1]), int(n[2])) for n in item.nodes]
    whole = [n for n in nodes if int(shares[tuple(np.add(n, board.offset))]) <= unit]
    for node_at, line, interval in itertools.product(whole if item.delta < 0 else [], lines, intervals):
        board.credit.faces.setdefault(interval, []).append(Face(item.family, line, node_at, 0, interval))
    return whole


def fan_momentum(board: Lattice, index: int) -> tuple[int, int, int]:
    """A family's lattice momentum P_a over the board in T's unit (Part F, Task 5; the two hands' lines of 2026-10-09 (c)): every record of the family read at the weight num (`node.momentum_of`) and the sum over num once by the division act, rounded half up on the magnitude with the sign after (kind D), the same unit as the piece's p_a (`node_detector.piece_momentum`) so that the credit line's two integers differ by the erasure's deficit; the fan's P before the erasure starts, read at the click's interval."""
    weight = board.families[index].pair[0]
    found = [0, 0, 0]
    for record in quanta_records(board.families, index):
        read = node.momentum_of(weight, board.lines_of(index, record), board.wrap)
        found = [a + b for a, b in zip(found, read, strict=True)]
    signed = scaled(found, weight)
    return signed[0], signed[1], signed[2]


def scaled(found: Sequence[int], weight: int) -> list[int]:
    """A lattice momentum reading per axis brought from the current's unit to T's unit, the piece's (`node_detector.piece_momentum`): each over the weight num once by the division act, rounded half up on the magnitude with the sign after (kind D); the fan's reading (`fan_momentum`), the packet's P at birth and the source's reach (`written`, `folded_source`) are read in it."""
    half = division_forward(weight, 2, 0)[0]
    sizes = [int(division_forward(abs(int(value)), weight, half)[0]) for value in found]
    return [size if value >= 0 else -size for size, value in zip(sizes, found, strict=True)]


def folded_source(
    board: Lattice, giver: NodeBooks, wanted: tuple[int, int, int]
) -> tuple[list[int], str | None]:
    """The source's fold (Part G, both hands' lines of 2026-10-10, the click with two receivers, theorem from the pair rule with the source as partner: at a click the write conserves P with two receivers, the taker's part folded by +p_a and the piece's source's part by -p_a, both at the click's tick by the same twist, n_a from the same bisection, kind S): the giver's part, the one carrying its count, folded by `wanted` through `twisted` on its own books, the same function the taker's write runs, written through the one lay act (`lay.written`, one `lay` line per Node changed) so that the host's tool crosses it on the way back; the fold is the body's and runs through no erasing front (the source's Nodes are the body's, not the light's). Returns the recoil given and its reading: `wanted` itself and None where the quarter turn carries it (the deposit equal to it to the fold's roundings, the hands' bound 2 c T (M - 1) / M for a count c on M Nodes along the axis); where the quarter turn falls short, the reach as read on the giver's own record lines before and after (`node.momentum_of`, `scaled`) with `LOST_TO_SOURCE`, the remainder `wanted` less it; a region of one Node along the axis folds none, `LOST_TO_DECLARATION`. OPEN by name (both hands): the shipped two-Node atoms at count 1 carry 0.71 of a pi / 4 piece; the one-Node write; the dipole."""
    weight, lines = board.families[giver.index].pair[0], board.lines_of(giver.index, giver.record)
    before = node.momentum_of(weight, lines, board.wrap)
    _twist, short = twisted(board, giver, giver.part, wanted)
    if short is None:
        return list(wanted), None
    after = node.momentum_of(weight, board.lines_of(giver.index, giver.record), board.wrap)
    reach = scaled([a - b for a, b in zip(after, before, strict=True)], weight)
    return reach, LOST_TO_SOURCE if short == LOST_TO_TAKER else short


def recoiled(
    board: Lattice, family: int, momentum: Sequence[int], pick: Callable[[list[int]], int]
) -> tuple[str, list[int], str | None]:
    """The piece's source at a click and its fold (Part G, both hands' lines of 2026-10-10, the click with two receivers, the attribution: -p is one body's, whole, Bothe-Geiger 1925 refuting a split among sources): among the light family's emitters with outstanding quanta in the record (`credit.Books.emitters`, `emission.Emitter`) one is drawn by those counts through `pick`, the click's own generator as the Node is drawn (the body's for a record's click, `parted`; the credit's for a region's, `credit.click_node`; one emitter, weight 1, no draw), one taken from its outstanding count, and its part folded by -p_a at the click's tick by the same twist (`folded_source`); where its recoil was paid at the lay (the directed packet) nothing more is folded and `PAID_AT_EMISSION` is read; where no emitter stands for the family the piece is the file's lay's, no receiver, `THE_LAY` with -p_a as integers and `LOST_TO_LAY`. Returns the source's name (`body n` by its number in the world's order, or the lay), the recoil per axis and the reading for `lost` (None where the source carries it). OPEN by name (both hands): the per-source share at the taker's region (one record per source), the fan's remainder on a board uneven about the source, the front's delay."""
    owed = [-int(value) for value in momentum]
    emitter = drawn_emitter(board, family, pick)
    if emitter is None or emitter.body is None:  # the file's lay, drawn or alone: no receiver
        return THE_LAY, owed, LOST_TO_LAY
    name = f"{BODY} {emitter.body}"
    if emitter.paid:
        return name, owed, PAID_AT_EMISSION
    given, short = folded_source(board, books_named(board, emitter.body), (owed[0], owed[1], owed[2]))
    return name, given, short


def drawn_emitter(board: Lattice, family: int, pick: Callable[[list[int]], int]) -> Emitter | None:
    """The piece's source drawn among the light family's emitters with outstanding quanta in the record by those counts through `pick` (one emitter, no draw; `recoiled`), one taken from its outstanding count; the file's lay stands among them as its own entry with the laid count (`credit.Books.of`, body None, Part H), so a laid light beside an emitter is drawn between the body and the lay by their counts; None where no entry stands."""
    standing = [e for e in board.credit.emitters.get(family, []) if e.outstanding > 0]
    if not standing:
        return None
    emitter = standing[pick([e.outstanding for e in standing]) if len(standing) > 1 else 0]
    emitter.outstanding -= 1
    return emitter


def unpaid(board: Lattice, family: int, pick: Callable[[list[int]], int]) -> tuple[str, str, str]:
    """A region taker's reading of the piece's source (Part H, MUST 5, both hands' lines of 2026-10-10 on the whole trial): a declared region (the two slits' screens, bell's sides) has no part of its own to twist, so it takes no +p and the law's two receivers are not there to pay; folding the source by -p alone would break the law, so the source is drawn and named (`drawn_emitter`, its outstanding count down by one as at a body's click) and nothing is folded: returns the source's name (`body n` or the lay), the recoil's one word `UNPAID_BY_REGION` and the reading `LOST_TO_REGION` for `lost`. OPEN by name: the region's +p (a region's record of the taken piece's momentum, which no declared screen carries)."""
    emitter = drawn_emitter(board, family, pick)
    name = THE_LAY if emitter is None or emitter.body is None else f"{BODY} {emitter.body}"
    return name, UNPAID_BY_REGION, LOST_TO_REGION


def quarter_turn(board: Lattice) -> int:
    """The count of phase-line acts to the quarter turn, the largest n with the cosine line at or above 0, found by bisection on the phase line as `paces.rotation_unit` finds the rest rotation (kind S): the sine line rises over [0, n] and the fold at n gives the taker the most momentum its lay can carry."""
    gamma = board.world.node_clock
    low, high, pair = 0, 2 * gamma, phase.seed(board.amplitude, gamma)
    while high - low > 1:
        middle = int(division_forward(low + high, 2, 0)[0])
        probe = phase.iterate(pair, middle - low, gamma)
        if int(phase.read(probe)[0]) >= 0:
            low, pair = middle, probe
        else:
            high = middle
    return low


def folded_lines(
    board: Lattice,
    lines: tuple[node.Record, node.Record],
    at: np.ndarray,
    offsets: np.ndarray,
    count: int,
) -> tuple[node.Record, node.Record]:
    """A part's two lines folded at every Node of the region by the phase pair at the angle x n theta_0, x the Node's offset along the axis from the region's lowest Node and n = `count` (signed): at each Node (re, im) now and before each multiplied by the pair (c, s) at x n acts and rounded once into the Link's unit (`phase.fold`, `signed_rounded`, the engine's one rounding half up on the magnitude with the sign after), the remainders as they stand; the levels elsewhere untouched. The pairs at the distinct offsets carried from the seed (`phase.iterate`), one per offset."""
    re_line, im_line = lines
    gamma, amplitude = board.world.node_clock, board.amplitude
    re_now, im_now = re_line.now.copy(), im_line.now.copy()
    re_before, im_before = re_line.before.copy(), im_line.before.copy()
    for offset in sorted({int(x) for x in offsets[at]}):
        c, s = phase.read(phase.iterate(phase.seed(amplitude, gamma), offset * count, gamma))
        here = at & (offsets == offset)
        for now, before in ((re_now, im_now), (re_before, im_before)):
            re_folded, im_folded = phase.fold(
                now[here].astype(object), before[here].astype(object), c, s, amplitude
            )
            now[here], before[here] = re_folded, im_folded
    return node.Record(re_now, re_before, re_line.remainder), node.Record(
        im_now, im_before, im_line.remainder
    )


@dataclass(frozen=True)
class Probe:
    """The twist's probe (Part F): a part's two lines standing at the region `at` with the Nodes' offsets along one axis, read once; `gained` the lattice momentum along the axis the fold at a signed count of acts would add, the folded copy's reading less the standing lines' (`folded_lines`, `node.momentum_of`), the exact reading in place of M rho sin delta."""

    board: Lattice
    weight: int
    lines: tuple[node.Record, node.Record]
    at: np.ndarray
    offsets: np.ndarray
    axis: int

    def gained(self, count: int) -> int:
        standing = node.momentum_of(self.weight, list(self.lines), self.board.wrap)[self.axis]
        folded = folded_lines(self.board, self.lines, self.at, self.offsets, count)
        return node.momentum_of(self.weight, list(folded), self.board.wrap)[self.axis] - standing


def twisted(
    board: Lattice, books: NodeBooks, part: int, momentum: tuple[int, int, int]
) -> tuple[list[int], str | None]:
    """The write's twist (Part F, Task 3; the two hands' lines of 2026-10-09: at a click the write must give the taker the piece's p_a exactly, by a phase gradient delta_a across the taker's Nodes, the whole-record twist e^(i delta x); NO SINE: delta is a count n of phase-line acts found by bisection, the mathematician's 6084261824): after the count entered the part, for each axis with p_a other than 0, the part's two lines folded at every Node of the region by the phase pair at the angle x n_a theta_0 (`folded_lines`; x the Node's offset from the start of the taker's run along the axis, taken around the ring on a periodic axis so a taker straddling the wrap folds by consecutive offsets, `core/ports.run_offsets`, Part F2), n_a the count at which the part's lattice momentum along the axis grew by p_a, found by bisection over [0, the quarter turn] on the probe "the folded lines' P_a less the standing lines' against |p_a|" (`node.momentum_of` on the folded copy, the exact reading in place of M rho sin delta: no overlap division; kind S), the sense of n_a the one whose quarter turn moves P_a with p_a's sign; where the quarter turn itself falls short of |p_a| the taker cannot carry the piece's momentum, "P lost to the taker" is booked and the quarter turn applied; a region of one Node along the axis carries none, nothing folded and "P lost to the declaration" booked; the fold is written through the one lay act (`lay.written`), one `lay` line per Node changed so that the host's tool crosses the twist on the way back (tools/back_in_time, `crossed`) and the inverse through the click is bit for bit; returns n_a per axis for the credit line and what was lost (None where nothing)."""
    family, state = board.families[books.index], board.states[books.index]
    first = node.record_slice(family, books.record).start + part * family.width
    if not family.plane:  # a real line holds no phase to twist
        return [0] * AXES, LOST_TO_DECLARATION if any(momentum) else None
    at = board.mask(books.nodes)
    positions = np.indices(board.shape)
    found, lost = [0] * AXES, None
    quarter = None
    for axis in range(AXES):
        wanted = momentum[axis]
        if wanted == 0:
            continue
        offsets = run_offsets(positions[axis], at, axis, board.wrap[axis])
        if int(offsets[at].max()) == 0:  # one Node along the axis: rho = 0, nothing to fold
            lost = LOST_TO_DECLARATION
            continue
        lines = (state.lines[first], state.lines[first + 1])
        quarter = quarter_turn(board) if quarter is None else quarter
        probe = Probe(board, family.pair[0], lines, at, offsets, axis)
        sense = 1 if probe.gained(quarter) * wanted > 0 else -1
        size = abs(wanted)
        low, high = 0, quarter
        if abs(probe.gained(sense * quarter)) < size:
            lost, low = LOST_TO_TAKER, quarter
        while high - low > 1:
            middle = int(division_forward(low + high, 2, 0)[0])
            if abs(probe.gained(sense * middle)) <= size:
                low = middle
            else:
                high = middle
        count = sense * low
        if low:
            folded = folded_lines(board, lines, at, offsets, count)
            for number, (line, after) in enumerate(zip(lines, folded, strict=True)):
                changes = (
                    np.where(at, after.now.astype(object) - line.now.astype(object), 0),
                    np.where(at, after.before.astype(object) - line.before.astype(object), 0),
                )
                lay_written(board, books.index, first + number, changes, None, at)
        found[axis] = count
    return found, lost


def faces_presented(board: Lattice, index: int) -> dict[int, Faces]:
    """The faces presented to a family's lines at this interval's step, per line, with the board's offset (the layers grown before the origin), forward and back alike (`node.step_records`)."""
    found: dict[int, Faces] = {}
    for presented in board.credit.faces.get(board.interval, []):
        if presented.family == index:
            found.setdefault(presented.line, ([], board.offset))[0].append(presented)
    return found


def faces_reported(board: Lattice) -> None:
    """The faces presented at this interval's step, one `face` line each (`reports.face`): the family, the line, the Node, the Port and the value Rule3 read there, written after the step computed them, for the host's tool, which presents them again on the way back from the lines and not from the books' log (`tools/back_in_time.py`)."""
    if board.output is None:
        return
    for found in board.credit.faces.get(board.interval, []):
        assert found.value is not None  # computed at this interval's step
        name, at = board.families[found.family].name, list(found.at)
        board.output(face(board.interval, name, found.line, at, found.port, found.value))
