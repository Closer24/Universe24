"""The take, the act's readings and items (the law's word for the act its contents serve, the module so named on 2026-10-21, twist.py until then; the engine V2, Parts F and G; ALGEBRA.md, The click's algebra beyond the law, The lattice momentum, The click's momentum on the board; the owner's rule, at the Nodes Rule3 only): the taker's part re-laid at each Node's own direction (`relaid`, `levels_at`), the click's items (`Item`, `Phase`, `books_named`), the hole's faces (`faced`, `faces_presented`, `faces_reported`), the piece's momentum readings (`fan_momentum`, `scaled`) and the piece's source drawn among the emitters by the quanta each holds and named with the recoil it owes, -p_a as integers on the credit line and written nowhere (`recoiled`, `drawn_emitter`), the loss booked by name (`unpaid`); the write moves the count by one and writes nothing for the piece's momentum, the recoil of a body held at declared Nodes being the declaration's; meeting.py writes the click with them."""

from __future__ import annotations

import itertools
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from event_universe import readings, records
from event_universe.core.rule3 import division_forward
from event_universe.emission import Emitter
from event_universe.features.click import Face, standing
from event_universe.lay import laid
from event_universe.loader.derived import quanta_records
from event_universe.loader.keys import Node
from event_universe.node_detector import (
    NodeBooks,
)
from event_universe.plane import Faces
from event_universe.reports import (
    BODY,
    BOOKED_AT_EMISSION,
    LOST_TO_LAY,
    LOST_TO_REGION,
    LOST_TO_SOURCE,
    THE_LAY,
    UNPAID_BY_REGION,
    face,
)

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


def relaid(board: Lattice, books: NodeBooks, part: int, count: int, phases: Sequence[Phase]) -> None:
    """The lay of one part of the record over the NodeDetector's Nodes through the one act (features/click, `standing`, `laid_pairs`; `lay.laid`): at every Node of the region the part's lines move to the levels of its share of `count` quanta, A_i^2 = A^2 weight_i / total in the counts' proportion, each Node standing in its own direction and sense, `phases` one per Node of the region in the books' order (the click's plan, C3: the recoil per Node, `act.leaving_phase` read per Node and not at the first Node), the change from what stands handed to the act with no weights (a record at its Node is laid as built, named) and the remainder at the division's origin at every Node of the region, the lay lines the write step's; the count's own lines alone, the other parts untouched. Part H (both hands' lines of 2026-10-10 on the whole trial, MUST 1: the null window's re-lay keeps each Node's own direction) and C3 (every re-lay, the exchange's too): each Node's direction is the pair (re, im) standing at that Node on the part's two lines, turned by the arrival for the part a quantum enters (`act.parted`), so that a phase gradient across the region survives the re-lay to the lay's rounding, the emission's re-lay among them, and the lattice momentum the record carries is not discarded unbooked; the acts the same lay act's, the count's share laid as before; the part a quantum enters stands at each Node in the leaving part's direction there turned by the arrival (`act.parted`)."""
    family, action = board.families[books.index], board.world.quantum_action
    first = records.record_slice(family, books.record).start + part * family.width
    total, at = sum(books.weights), board.mask(books.nodes)
    levels: list[tuple[np.ndarray, np.ndarray]] = []
    for here, weight, (direction, sense) in zip(books.nodes, books.weights, phases, strict=True):
        share = (weight, total)
        (re, im), (re_before, im_before) = standing(count, action, family.pair, direction, sense, share)
        pairs = [(re, re_before), (im, im_before)]
        levels = levels or [
            (records.zeros(board.shape, object), records.zeros(board.shape, object)) for _ in pairs
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
    """A part's levels at one Node of the reader, (re_now, im_now, re_before, im_before), read from its two lines; the reader's first Node where none is named: the click's write lays each Node in its own direction (C3), a part standing at each Node in its own (Part H, MUST 1; `act.leaving_phase` reads every Node)."""
    family, state = board.families[books.index], board.states[books.index]
    first = records.record_slice(family, books.record).start + part * family.width
    at = tuple(np.add(books.nodes[0] if here is None else here, board.offset))
    re, im = state.lines[first], state.lines[first + 1 if family.plane else first]
    return int(re.now[at]), int(im.now[at]), int(re.before[at]), int(im.before[at])


@dataclass(frozen=True)
class Item:
    """One entry of a click's list (the mathematician's hand with the advisor's second, two hands; the owner's word, one generic implementation the node_detector operates): the record by its family and, for a record declared a NodeDetector at one Node, its number among `bodies` (None for a record spread over the board), the part (None for every line of a spread record, no line alone), the change of its count, +1, -1 or 0 (the null window moves no count), the Nodes written at, the file's coordinates, and for a spread record given whole quanta the form of its lay (`emission.emitted_quantum`): the pair its lay stands at where the list names one (a record laid whole at its declared interval at its family's massless pair [den, den], the lay by the count at one Node, `meeting.laid_whole`; the conversion's records out until 2026-10-20; the two hands) with, for a plane, the sense of its lay (0 for real lines; the conversion's table declared it until 2026-10-20; `emission.laid_by_count`), else the resonance and the span of a source in time (the emission's, the transition's declared resonance and the lifetime, the mathematician's hand with the advisor's second); the absorption's items carry the arriving record's phase at the close, (X, Y'), `arrival`, by which the entered part's direction is turned (`parted`), and the light's item the two parts' (re, im) at the Node, `levels`, the excited and the ground part's, the born source's phase phi_e - phi_g (`emission.start_of`); Part G: the light's item names the body whose click gives it (`emitter`, the emitters' book, `emission.registered`) and the entering item of an absorption names the piece's family (`drive`, the source's draw, `recoiled`); the click's plan, C6: a spread record taken names per Node the Ports the quantum entered it by, the face's set (`ports`, from the window's inflow booked per Port, `node_detector.arrival_ports`)."""

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
    ports: tuple[tuple[int, ...], ...] = ()  # C6 (i): per Node named, the Ports the quantum entered by


Phase = tuple[tuple[int, int], int]  # a part's direction (re, im) and its sense, its Wronskian's sign


def books_named(board: Lattice, body: int) -> NodeBooks:
    """The books of the record declared a NodeDetector numbered `body` among the world's `bodies`."""
    return next(books for books in board.credit.bodies if books.number == body)


def faced(board: Lattice, item: Item) -> list[tuple[Node, tuple[int, ...]]]:
    """The one comparison of the absorption and the emission at a spread record's Nodes (features/click, `Face`; ALGEBRA.md, The click writes on the lattice (b) and (d), the undepleted beam): at each Node named the record's booked share, the share the credit reads there (`Lattice.share_of`, the conserved form's density at the Node, `share.share`, read at the click from the levels the next step reads), against the record's own quantum W_rec (`credit.Books.units`); the Nodes where it is at most W_rec, the record there local and whole, are returned with their Ports (a Node whose face set is empty, an arrival two-sided on every axis, is not among them: the quantum is taken in the books and the levels stand, the deficit path below, with the reading `NO_SIDE` on the credit line; the click's plan, C6, the cold reader's fix of 2026-10-18), the Nodes the click writes, and for an absorption the hole to 0 is booked there: for every line of the record one face at the next two intervals on the Ports the quantum entered the Node by, the item's set for that Node (`Item.ports`; the click's plan, C6 (i)), so that Rule3 writes the level 0 and then the level before 0 with its own remainder (the mathematician's hand; the front erasing what spread beyond the Node where the count reaches 0); at a Node where the share is above W_rec a record of many quanta per Node is a beam, nature's undepleted beam, exact as the count per Node grows: no face, no lay and no front there, the levels standing (a one-Node lay into a beam would be the same point defect the hole of a dense record was), the quantum passing in the books alone (`written`: the count and the deficit); nothing assigned at any Node."""
    lines = range(board.families[item.family].record)
    intervals = (board.interval + 1, board.interval + 2)
    unit = board.credit.units[item.family]
    shares = board.share_of(item.family, 1, board.mask(item.nodes))[0]
    nodes = [(int(n[0]), int(n[1]), int(n[2])) for n in item.nodes]
    named = zip(nodes, item.ports or ((),) * len(nodes), strict=True)
    sided = not item.ports  # no face set named: a lay, or a record taken whole
    whole = [
        (n, p) for n, p in named if int(shares[tuple(np.add(n, board.offset))]) <= unit and (sided or p)
    ]
    for (at, ports), line, interval in itertools.product(
        whole if item.delta < 0 else [], lines, intervals
    ):
        board.credit.faces.setdefault(interval, []).append(Face(item.family, line, at, ports, interval))
    return whole


def fan_momentum(board: Lattice, index: int) -> tuple[int, int, int]:
    """A family's lattice momentum P_a over the board in T's unit (Part F, Task 5; the two hands' lines of 2026-10-09 (c)): every record of the family read at the weight num (`readings.momentum_of`) and the sum over num once by the division act, rounded half up on the magnitude with the sign after (kind D), the same unit as the piece's p_a (`node_detector.piece_momentum`) so that the credit line's two integers differ by the erasure's deficit; the fan's P before the erasure starts, read at the click's interval."""
    weight = board.families[index].pair[0]
    found = [0, 0, 0]
    for record in quanta_records(board.families, index):
        read = readings.momentum_of(weight, board.lines_of(index, record), board.wrap)
        found = [a + b for a, b in zip(found, read, strict=True)]
    signed = scaled(found, weight)
    return signed[0], signed[1], signed[2]


def scaled(found: Sequence[int], weight: int) -> list[int]:
    """A lattice momentum reading per axis brought from the current's unit to T's unit, the piece's (`node_detector.piece_momentum`): each over the weight num once by the division act, rounded half up on the magnitude with the sign after (kind D); the fan's reading (`fan_momentum`) and the packet's P at birth (`act.written`) are read in it."""
    half = division_forward(weight, 2, 0)[0]
    sizes = [int(division_forward(abs(int(value)), weight, half)[0]) for value in found]
    return [size if value >= 0 else -size for size, value in zip(sizes, found, strict=True)]


def recoiled(
    board: Lattice, family: int, momentum: Sequence[int], pick: Callable[[list[int]], int]
) -> tuple[str, list[int], str]:
    """The piece's source at a click and the recoil it owes (Part G, both hands' lines of 2026-10-10, the attribution: -p is one body's, whole, Bothe-Geiger 1925 refuting a split among sources; ALGEBRA.md, The click's algebra beyond the law: the write moves the count and writes nothing for the piece's momentum, the recoil of a body held at declared Nodes the declaration's): among the light family's emitters with outstanding quanta in the record (`credit.Books.emitters`, `emission.Emitter`) one is drawn by those counts through `pick`, the click's own read of the board as the Node is drawn (the body's for a record's click, `parted`; the credit's for a region's, `lists.credited_node`; one emitter, weight 1, no draw), one taken from its outstanding count, and the recoil it owes, -p_a per axis as integers, is booked on the credit line and written nowhere, the source's part standing as laid: `LOST_TO_SOURCE` the reading; where the recoil was booked at the lay (the directed packet's emission line, `act.written`) `BOOKED_AT_EMISSION` is read; where no emitter stands for the family the piece is the file's lay's, no receiver, `THE_LAY` with `LOST_TO_LAY`. Returns the source's name (`body n` by its number in the world's order, or the lay), the recoil owed per axis and the reading for `lost`."""
    owed = [-int(value) for value in momentum]
    emitter = drawn_emitter(board, family, pick)
    if emitter is None or emitter.body is None:  # the file's lay, drawn or alone: no receiver
        return THE_LAY, owed, LOST_TO_LAY
    return f"{BODY} {emitter.body}", owed, BOOKED_AT_EMISSION if emitter.booked else LOST_TO_SOURCE


def drawn_emitter(board: Lattice, family: int, pick: Callable[[list[int]], int]) -> Emitter | None:
    """The piece's source drawn among the light family's emitters with outstanding quanta in the record by those counts through `pick` (one emitter, no draw; `recoiled`), one of the close's later draws through the same number the click read, the quotient left after the Node's draw (ALGEBRA.md, The click's read of the board, beside The click's algebra beyond the law: the source drawn and named with the recoil it owes, written nowhere), one taken from its outstanding count; the file's lay stands among them as its own entry with the laid count (`credit.Books.of`, body None, Part H), so a laid light beside an emitter is drawn between the body and the lay by their counts; None where no entry stands."""
    standing = [e for e in board.credit.emitters.get(family, []) if e.outstanding > 0]
    if not standing:
        return None
    emitter = standing[pick([e.outstanding for e in standing]) if len(standing) > 1 else 0]
    emitter.outstanding -= 1
    return emitter


def unpaid(board: Lattice, family: int, pick: Callable[[list[int]], int]) -> tuple[str, str, str]:
    """A region taker's reading of the piece's source (Part H, MUST 5, both hands' lines of 2026-10-10 on the whole trial): a declared region (the two slits' screens, bell's sides) has no part of its own, so the piece's P is lost to the region; the source is drawn and named (`drawn_emitter`, its outstanding count down by one as at a body's click) and no recoil is booked to it: returns the source's name (`body n` or the lay), the recoil's one word `UNPAID_BY_REGION` and the reading `LOST_TO_REGION` for `lost`. OPEN by name: the region's +p (a region's record of the taken piece's momentum, which no declared screen carries)."""
    emitter = drawn_emitter(board, family, pick)
    name = THE_LAY if emitter is None or emitter.body is None else f"{BODY} {emitter.body}"
    return name, UNPAID_BY_REGION, LOST_TO_REGION


def faces_presented(board: Lattice, index: int) -> dict[int, Faces]:
    """The faces presented to a family's lines at this interval's step, per line, with the board's offset (the layers grown before the origin), forward and back alike (`flux.step_records`)."""
    found: dict[int, Faces] = {}
    for presented in board.credit.faces.get(board.interval, []):
        if presented.family == index:
            found.setdefault(presented.line, ([], board.offset))[0].append(presented)
    return found


def faces_reported(board: Lattice) -> None:
    """The faces presented at this interval's step, one `face` line each (`reports.face`): the family, the line, the Node, the Ports and the value Rule3 read through them, written after the step computed them, for the host's tool, which presents them again on the way back from the lines and not from the books' log (`tools/back_in_time.py`)."""
    if board.output is None:
        return
    for found in board.credit.faces.get(board.interval, []):
        assert found.value is not None  # computed at this interval's step
        name, at = board.families[found.family].name, list(found.at)
        board.output(face(board.interval, name, found.line, at, list(found.ports), found.value))
