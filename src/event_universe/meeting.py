"""The meeting at a Node (ALGEBRA.md #the-click-is-the-meeting, The click writes on the GameBoard; HIGHLIGHTS.md, the owner's words of 2026-10-02 and 2026-10-03; the owner's word of 03:15 Israel, 2026-10-03, the click the heart): a detector is where the future met the past, the arriving record's quantum run forward from its root meeting at one Node the detector's own transition's quantum read back from the realised click, the click their meeting; a detector always receives two quanta, the arriving one and its own, a region detector's own quantum implicit in its declared window and whole, and for a record declared an instrument at one Node its record there; from the click the new future goes out, the quantum with the taker to its next meeting (the taker's record changed at its Node and stepped on by Rule3), the hole spreading from the entry Node, the giving's light quantum, and the arriving record's wave with its count at 0, the empty wave, stepped on and never credited. The seven steps in the Node's words (the Boss's sequence of 2026-10-03 with the advisor's and the mathematician's hands): 0, every interval every Node steps every record it holds by Rule3, a bijection, no draw; at the end of an instrument's window at the Node named (the declared window's length, or, for a body with a probe, the tick of the probe's lay at its Node: the window bounded by clicks, opened at the body's last write and closed at the probe's taking, ALGEBRA.md, The pulsed gate), 1, the read, the two records at that Node, the arriving family's level there and the record present, the share their product at resonance (the resonant two-mode act, the two-quadrature form: the arriving level summed over the window against the record's two reference records at the transition's declared resonance, the plane's size over the scale the window's turn at the declared weight, applied once at the window's close as W sub-turns with the carry, turning the two parts' labels into each other, the labels' squares the shares, the Rabi form, `resonance.gathered`, `resonance.window_turn`, `turned_labels`); 2, the draw, with the declared seed and generator, once per window; 3, the write at that Node, one whole quantum passing between the two records there: the arriving record's levels and remainder to 0 (the hole; for a dense record, whose share at the Node exceeds its own quantum, its two levels scaled so that one quantum's share leaves and the phase stands, the hole of a dense record, `faced`) and its count in the books down by one, the present record's realised part laid at N + 1 at that Node in the direction of the part it leaves (the phase passing with the quantum), the remainder at the lay's origin, the part it leaves at N - 1 (the taking); 4, a window with no meeting at a Node whose record reads its own parts, the record laid again in the complement of its outcome set at its whole count (the null window, one function); 5, the giving, at a Node whose record stands in an upper part, drawn at the lifetime's hazard 1 / tau per interval, per window while a window stands and per interval in the dark at the now (the beat's current of a one-part record at one Node being 0, named): one whole quantum passing from that record to the light family's record at the same Node, the upper part to N - 1, the lower to N + 1, light's record up by one whole quantum laid as a source in time at that Node over the giving's lifetime at the transition's declared resonance (`giving.given_quantum`); 6, after the write the Node and its neighbours step by Rule3, nothing written at any other Node, no front; 7, the click line (`reports.credit`, the one click line kind of every reader), the window, the reader, the family and the parts, never a Node, the Node written standing in the GAMEBOARD `lay` and `face` lines beside it. The record declared an instrument is one Node by the world's declaration (its six Link factors 0, `cut`, so that it stays, held by its declaration as the detector's region is), its books the instrument's own and at no Node; the Node knows no click."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import front, node
from event_universe.core import paces
from event_universe.core.ports import arrival
from event_universe.core.rule3 import division_forward
from event_universe.features.click import Face, Hole, drawn, laid_pairs, standing
from event_universe.giving import given_lines, given_quantum, levels_of
from event_universe.loader.derived import count_wall, row_of
from event_universe.loader.instrument import Generator, Instrument, NodeInstrument
from event_universe.loader.keys import Node
from event_universe.loader.world import BodyRow
from event_universe.plane import Faces
from event_universe.reports import MEASURED, credit, face, lay
from event_universe.resonance import Reference, gathered, references_of, scale_of, sheared, window_turn

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard


@dataclass
class NodeBooks:
    """The books of a record declared a reader over a region (ALGEBRA.md, The NodeReader is one declaration kind for every experiment): the declaration's number among the world's `measured`, the record's family and its record number, its Nodes with the lay's weights (the counts' proportion), its declaration, the part carrying the count, the counts per part, the labels, the intervals elapsed in the window, the generator's state, the two reference records per transition, the windows closed and its own clock."""

    number: int
    index: int
    record: int
    nodes: tuple[Node, ...]
    weights: tuple[int, ...]
    declared: NodeInstrument
    part: int
    counts: list[int]
    labels: list[int]
    elapsed: int
    state: int
    references: list[Reference]
    windows: int = 0
    clock: list[int] = field(default_factory=lambda: [0, 0])


def books_of(board: GameBoard) -> list[NodeBooks]:
    """The books of every record declared an instrument at a Node, in the world's order: its number among `measured`, its family and record, its one Node, its declaration, the part carrying the count, the counts per part, the labels at their counts in the count's units, the window begun and the generator at the declared seed; the scale of its reference records from the declared window, or from the run's intervals where its window is bounded by a probe's lays (no window longer than the run; one interval the least)."""
    found = []
    for number, (record, row) in enumerate(board.laid_rows()):
        if not isinstance(row, BodyRow) or row.instrument is None or row.instrument.draw is None:
            continue
        parted = list(row.instrument.counts)
        wall = count_wall(board.families[row.family], board.world.quantum_action)
        part = max(range(len(parted)), key=lambda k: parted[k])
        labels = [count * wall for count in parted]
        draw = row.instrument.draw
        longest = draw.window if isinstance(draw, Instrument) else max(board.world.ticks, 1)
        scale = scale_of(board.world.width, board.world.amplitude_bound, longest)
        seed = draw.seed
        references = references_of(scale, row.instrument.transitions)
        found.append(
            NodeBooks(
                number,
                row.family,
                record,
                row.nodes,
                row.counts,
                row.instrument,
                part,
                parted,
                labels,
                0,
                seed,
                references,
            )
        )
    return found


def read(board: GameBoard, index: int, direction: int, record: int) -> tuple[Any, node.Factors]:
    """A record's read at the interval's start in `direction` (`node.read`, every sign row but the record's own), the Links the world cuts at 0 among its factors (`cut`)."""
    gamma, unit, cuts = board.world.node_clock, board.unit, cut(board, index)
    return node.read(
        index, board.families, board.states, direction, board.wrap, gamma, unit, record, cuts
    )


def stepped(
    board: GameBoard, index: int, direction: int
) -> tuple[list[node.Record], list[node.Booking]]:
    """Every record of a family stepped by Rule3 in `direction` with the rule of its own read (`node.step_records`), the Links the world cuts at 0 among its factors (`cut`) and the faces the instrument presents at this interval among its arrivals (`faces_of`)."""
    gamma, unit, cuts = board.world.node_clock, board.unit, cut(board, index)
    faces = faces_of(board, index)
    return node.step_records(
        index, board.families, board.states, board.wrap, gamma, unit, direction, cuts, faces
    )


def cut(board: GameBoard, index: int) -> node.Factors | None:
    """The Links the world declares at the factor 0 for a family, per Port the mask of the Nodes whose Port faces them (ALGEBRA.md, The NodeReader is one declaration kind for every experiment: its outer Links cut and its inner Links open): the boundary Links of every region over which a record of the family is laid in its parts, the Links with one end in the region and one outside, read 0 from both ends; the Links between two Nodes of one region stay at G^2, so that the record's uniform mode rotates at cos omega_0 = num / den whatever the region's size; None where the family has no such record."""
    regions = [
        board.mask(row.nodes)
        for row in board.world.bodies
        if row.family == index and row.instrument is not None
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


def relaid(
    board: GameBoard, books: NodeBooks, part: int, count: int, phase: tuple[int, int], sense: int
) -> None:
    """The lay of one part of the record over the reader\'s Nodes (features/click, `standing`, `laid_pairs`): at every Node of the region the part\'s two lines set to the levels of its share of `count` quanta, A_i^2 = A^2 weight_i / total in the counts\' proportion, standing in the direction `phase` and the sense `sense`, the remainder at the lay\'s origin; the count\'s own lines alone, the other parts untouched."""
    family, state = board.families[books.index], board.states[books.index]
    gamma, unit, action = board.world.node_clock, board.unit, board.world.quantum_action
    origin = division_forward(node.rule_of(family, gamma, 0, None, unit)[2], 2, 0)[0]
    first = node.record_slice(family, books.record).start + part * family.width
    total = sum(books.weights)
    for here, weight in zip(books.nodes, books.weights, strict=True):
        share = (weight, total)
        if books.declared.conversions:
            pairs = laid_pairs(
                count, action, family.pair, books.declared.sense, family.plane, family.laid, share
            )
        else:
            (re, im), (re_before, im_before) = standing(count, action, family.pair, phase, sense, share)
            pairs = [(re, re_before), (im, im_before)]
        at = board.mask((here,))
        for number, (now, before) in zip(range(first, first + len(pairs)), pairs, strict=True):
            line = state.lines[number]
            state.lines[number] = node.Record(
                np.where(at, now, line.now),
                np.where(at, before, line.before),
                np.where(at, origin, line.remainder),
            )


def laid_record(board: GameBoard, number: int, record: int) -> None:
    """A record laid in its parts at its one Node at the start (`loader/instrument.py`, `parts`): every part at its declared count, the one carrying the count as the standing record of the pair in the direction (1, 0) and the sense +1, the others 0 there; the books not yet made, so a passing book names the declaration."""
    row = board.world.bodies[number]
    assert row.instrument is not None
    books = NodeBooks(
        number, row.family, record, row.nodes, row.counts, row.instrument, 0, [], [], 0, 0, []
    )
    for part, count in enumerate(row.instrument.counts):
        relaid(board, books, part, count, (1, 0), 1)


def levels_at(board: GameBoard, books: NodeBooks, part: int) -> tuple[int, int, int, int]:
    """A part's levels at the reader's first Node, (re_now, im_now, re_before, im_before), read from its two lines: the lay stands in one direction at every Node of the region, so the first Node carries the part's phase."""
    family, state = board.families[books.index], board.states[books.index]
    first = node.record_slice(family, books.record).start + part * family.width
    at = tuple(np.add(books.nodes[0], board.offset))
    re, im = state.lines[first], state.lines[first + 1 if family.plane else first]
    return int(re.now[at]), int(im.now[at]), int(re.before[at]), int(im.before[at])


def arriving(board: GameBoard, books: NodeBooks, drive: int, direction: int = 1) -> int:
    """The arriving record's level summed over the reader's Nodes, the level now (`direction` 1) or the level before (-1): a holder of the sign's time level summed over every row but the record's own (`node.row_levels`, light), a family of quanta's first line's level otherwise; the window's sums are over all the region's Nodes."""
    family, lines = board.families[drive], board.states[drive].lines
    if family.wronskian:
        own = row_of(board.families, books.index, books.record)
        levels = np.asarray(node.row_levels(family, lines, 0, direction, own))
    else:
        levels = lines[0].now if direction == 1 else lines[0].before
    return sum(int(levels[tuple(np.add(at, board.offset))]) for at in books.nodes)


def dark(board: GameBoard, books: NodeBooks) -> bool:
    """A reader with no arriving record at its Nodes this interval: both levels, now and before, of every family its transitions name sum to 0 over the region at every Node, so no window stands and the giving\'s grain is the interval."""
    turning = {t.drive for t in books.declared.transitions if t.leaves != t.enters}
    for drive in sorted(turning):
        family, lines = board.families[drive], board.states[drive].lines
        own = row_of(board.families, books.index, books.record)
        for side in (1, -1):
            if family.wronskian:
                levels = np.asarray(node.row_levels(family, lines, 0, side, own))
            else:
                levels = lines[0].now if side == 1 else lines[0].before
            if any(int(levels[tuple(np.add(at, board.offset))]) for at in books.nodes):
                return False
    return True


def own_clock(board: GameBoard, books: NodeBooks) -> int:
    """The reader's own clock, the composed clock p_0 under its record's read of the content (`paces.clock_of`) at each of its Nodes, their mean by the division act with the half carry (as a region's clock is read, `credit.clocked`): Gamma in the vacuum and below it in a well, the number the turn per proper interval and the dark's hazard read."""
    gamma = board.world.node_clock
    content = board.read(books.index, 1, books.record)[0]
    clocks = [
        int(
            paces.clock_of(
                gamma,
                int(np.asarray(content)[tuple(np.add(at, board.offset))])
                if np.ndim(content)
                else int(content),
            )
        )
        for at in books.nodes
    ]
    count = len(clocks)
    return int(division_forward(sum(clocks), count, division_forward(count, 2, 0)[0])[0])


def clocked(board: GameBoard, books: NodeBooks) -> None:
    """The body's own clock, one interval (the advisor's derivation of 2026-10-03, #1572 comment 5966657866, the clock composed from the paces, with the mathematician's second; the two hands' click line of the pulsed gate, 5967698811 and 5967783614): its clock p_0 at its Node (`own_clock`) added to the carried remainder and divided once by Gamma, the whole intervals to its proper time and the remainder kept, as the credit keeps a region's (`credit.clocked`); the board's tick in the vacuum, slower in a well."""
    whole, rest = division_forward(books.clock[1] + own_clock(board, books), board.world.node_clock, 0)
    books.clock[0], books.clock[1] = books.clock[0] + int(whole), int(rest)


def laid_whole(board: GameBoard) -> None:
    """The messages laid whole at this interval's end (`loader/messages.py`, `WholeMessage`: the probe of the pulsed gate, the two hands of 2026-10-03, #1572 comments 5967698811 and 5967783614): each its count of whole quanta laid at its Node through the one act with one outcome and no draw (`click`, `given_quantum`, `laid_by_count` at the family's massless pair [den, den], A^2 = count T div 2 on the record's first line), the record's count in the books up by the count and one lay line for the host's tool; the experimenter's lay in time, from outside the Node as every lay is, before the records at Nodes read their arrivals."""
    for whole in board.world.wholes:
        if whole.tick == board.tick:
            den = board.families[whole.family].pair[1]
            items = [Item(whole.family, None, None, whole.count, (whole.at,), (den, den))]
            click(board, 0, None, [1], [items])


def hazard_weights(span: int, lifetime: int, clock: int, gamma: int, unit: int) -> list[int]:
    """The dark's draw between the giving and nothing over `span` board intervals at the lifetime tau, a proper time (the mathematician's 235, #1572 comment 5966769056, with the advisor's second, 5966780505, two hands): the hazard 1 / tau per proper interval, the body's proper intervals per board tick p_0 / Gamma, so the giving's weight is span x p_0 x unit div Gamma by the division act (half up) against the rest of tau x unit, [span x unit, (tau - span) x unit] exactly in the vacuum where p_0 = Gamma, and in a well the body gives slower by p_0 / Gamma."""
    given = int(division_forward(span * clock * unit, gamma, division_forward(gamma, 2, 0)[0])[0])
    return [given, lifetime * unit - given]


def turned_labels(board: GameBoard, books: NodeBooks) -> None:
    """The resonant two-mode act at the window's close, once per window (ALGEBRA.md, The two-mode line; The click writes on the GameBoard (b), the share at resonance; item 50, the two-quadrature form, two hands): for every transition out of the part the record stands in, the window's turn (`resonance.window_turn`, the plane's size over the scale) scaled by the record's own clock (`node.turned_by`, the tangent half-angle over 2 Gamma) turns the two parts' labels into each other by the engine's own three shears (features/rotation) as W equal sub-turns with the carry (`resonance.sheared`, W the window's intervals, so the angles add as the proper intervals' did), the plane's size over the wall read once and not a turn per interval; the labels' squares are the parts' shares the window's draw reads, sin^2 of the turn, the Rabi form; the complement outcome at the close, none takes, is the null window (`null_window`, the record re-laid in its part at its count, the labels' coherence ended); every transition's two sums then begin again, the reference records running on."""
    gamma, clock = board.world.node_clock, own_clock(board, books)
    for transition, reference in zip(books.declared.transitions, books.references, strict=True):
        if (
            transition.leaves == books.part and transition.leaves != transition.enters
        ):  # the probe's turns nothing
            turn = int(node.turned_by(window_turn(reference, transition.weight), clock, gamma))
            u, v = books.labels[transition.leaves], books.labels[transition.enters]
            u, v = sheared(u, v, turn, books.elapsed, gamma)
            books.labels[transition.leaves], books.labels[transition.enters] = u, v
        reference.in_phase, reference.quadrature = 0, 0


@dataclass(frozen=True)
class Item:
    """One entry of a click's list (the mathematician's 192 with the advisor's second, #1572 comment 5963391333, two hands; the owner's word of 2026-10-03, 03:22 Israel, one generic implementation the detector operates): the record by its family and, for a record declared an instrument at one Node, its number among `measured` (None for a record spread over the board), the part (None for every line of a spread record, no line alone), the change of its count, +1, -1 or 0 (the null window moves no count), the Nodes written at, the file's coordinates, and for a spread record given whole quanta the form of its lay (`giving.given_quantum`): the pair its lay stands at where the list names one (the conversion's records out at their family's massless pair [den, den], the lay by the count at one Node, the two hands of 2026-10-03, #1572 comments 5964520368 and 5964754600) with, for a plane, the sense of its lay as the conversion's table declares it (0 for real lines; `giving.laid_by_count`), else the resonance and the span of a source in time (the giving's, the transition's declared resonance and the lifetime, the mathematician's 213 (B) and 220 with the advisor's second, #1572 comments 5965054791 and 5965303134, #1563 comment 5965316267)."""

    family: int
    measured: int | None
    part: int | None
    delta: int
    nodes: tuple[Node, ...]
    pair: tuple[int, int] | None = None
    resonance: tuple[int, int] | None = None
    span: int = 0
    sense: int = 0
    width: int | None = (
        None  # the open board's packet: its Nodes across (`giving.laid_packet`), None for the source in time
    )
    direction: tuple[int, int] | None = None  # the packet's drawn direction, the axis and its sense


Lists = list[list[Item]]  # the outcomes of one click, each the list written where it is drawn
Phase = tuple[tuple[int, int], int]  # a part's direction (re, im) and its sense, its Wronskian's sign


def click(
    board: GameBoard, state: int, generator: Generator | None, weights: list[int], outcomes: Lists
) -> tuple[int, int]:
    """The one click act, the detector's, of every list alike (the owner's words of 2026-10-03, 03:22 and 03:24 Israel; the mathematician's 192 and 197, the advisor's second, two hands): with more than one outcome, one draw by the weights with the generator from `state` (features/click, `drawn`, the modulus 2^width; with one outcome no draw and the state untouched), then the drawn outcome's list written (`written`); returns the outcome's index and the generator's state after. The five lists through it: the region detector's credit (the arriving record at the Nodes drawn, -1), the taking (the arriving record -1, the present record's part entered +1 and left -1), the giving (the part left -1, the part entered +1, light's record +1), the null window (the part the record stands in at 0) and the conversion (the record whole at -1 at its Node and records of other families out at +1 there, each one whole quantum laid by the count at its family's massless pair, declared in a world's table and rate and drawn at the rate, src/event_universe/conversion.py); no family name and no branch on a record's lines or dimension anywhere in it."""
    pick, modulus = 0, board.world.width + 1
    if len(outcomes) > 1:
        assert generator is not None  # a draw among outcomes is the declared generator's
        pick, state = drawn(state, generator.multiplier, generator.increment, modulus, weights)
    written(board, outcomes[pick])
    return pick, state


def written(board: GameBoard, items: list[Item]) -> None:
    """The write step of the act, the one swappable step, item by item: a spread record's quantum taken by the face at every Node named (`faced`, every line of the record whatever their number) or given by the lay of one whole quantum there (`given_quantum`), its count in the credit's books moved; a record declared an instrument at one Node laid part by part at its new count (`parted`), the direction and sense of the part its quantum leaves read first and passed to the part it enters (the phase passes with the quantum), its books' part the one carrying the count and its labels' coherence ended; where a spread record's count reaches 0 its erasing front begins from every Node of its items (`front.started`); every line a lay changed at a Node, levels or remainder, written as one `lay` line with the levels before and after (`laid_lines`, `levels_of`, `reports.lay`), the diagnostic the host's tool crosses the lay from (the mathematician's 195: the face's part crossed by Rule3's inverse, the lay's part from its line)."""
    leaving = [item for item in items if item.measured is not None and item.delta < 0]
    phases = {item.measured: leaving_phase(board, item) for item in leaving}
    laid = [
        (i.family, line, at)
        for i in items
        if i.direction is None  # a packet writes its own lay lines at every Node it lays
        for line in laid_lines(board, i)
        for at in i.nodes
    ]
    before = [levels_of(board, *entry) for entry in laid]
    touched: list[NodeBooks] = []
    for item in items:
        if item.measured is None:
            (faced if item.delta < 0 else given_quantum)(board, item)
            continue
        parted(board, books := books_named(board, item.measured), item, phases.get(item.measured))
        touched += [books] if books not in touched else []
    for books in touched:
        books.part = max(range(len(books.counts)), key=lambda k: books.counts[k])
        wall = count_wall(board.families[books.index], board.world.quantum_action)
        books.labels = [count * wall for count in books.counts]
    for family in sorted({i.family for i in items if i.measured is None and i.delta < 0}):
        if board.credit.counts[family] <= 0:  # the count at 0: its front from every Node written
            front.started(board, family, [at for i in items if i.family == family for at in i.nodes])
    for (index, line, at), was in zip(laid, before, strict=True):
        now = levels_of(board, index, line, at)
        if now != was and board.observer is not None:
            board.observer(lay(board.tick, board.families[index].name, line, list(at), was, now))


def laid_lines(board: GameBoard, item: Item) -> list[int]:
    """The lines of a record an item lays at its Nodes: the lines of the part of a record declared an instrument at one Node (`parted`), the lines of a spread record given whole quanta (`given_quantum`, `giving.given_lines`: every laid line of one part of its first record, a plane's two lines per plane, a holder of the sign's time line alone), none for a quantum taken by the face."""
    if item.measured is None:
        return given_lines(board.families[item.family]) if item.delta > 0 else []
    assert item.part is not None
    family, books = board.families[item.family], books_named(board, item.measured)
    first = node.record_slice(family, books.record).start + item.part * family.width
    return list(range(first, first + family.width))


def books_named(board: GameBoard, measured: int) -> NodeBooks:
    """The books of the record declared an instrument numbered `measured` among the world's `measured`."""
    return next(books for books in board.credit.bodies if books.number == measured)


def leaving_phase(board: GameBoard, item: Item) -> Phase:
    """The direction (re, im) and the sense (the sign of the Wronskian) of the part a quantum leaves, read at the Node before any lay of the list."""
    assert item.part is not None
    re, im, re_before, im_before = levels_at(board, books_named(board, item.measured or 0), item.part)
    return (re, im), 1 if re * im_before - im * re_before >= 0 else -1


def faced(board: GameBoard, item: Item) -> None:
    """A spread record's quantum taken at the Nodes named, the face (features/click, `Face`; ALGEBRA.md, The click writes on the GameBoard (b) and (d), and the hole of a dense record): for every line of the record and every Node, one face at the next two intervals, the first Port preferred, so that Rule3 writes the level 0 and then the level before 0 with its own remainder where the record's booked share at the Node, O + C / 2, is at most its own quantum (237, 239, the mathematician's 266; the front erasing what spread beyond the Node), and otherwise (a dense record, the Zeno drive at 3.5 quanta per Node or the ion's drive at 55) each face writes its level by the booking identity, one `Hole` per line and Node shared by its two faces carrying the record's unit from the books in the form's own units at the Node, W_rec x 2 p_i^2 G^2 (the share's weight, `share.over_pace`, p_i the Node's Link pace under the record's read), the first face removing one quantum or the most one write can and recording exactly what left, the second the rest the same way (`features/click.rest_of`; the mathematician's 265 and 266 correcting 244, with 237 and the advisor's second); the record's count in the credit's books down by the item's change; nothing assigned at any Node."""
    lines, ticks = range(board.families[item.family].record), (board.tick + 1, board.tick + 2)
    unit, gamma, link = board.credit.units[item.family], board.world.node_clock, board.unit
    content = board.read(item.family, 1, 0)[0]
    for at, line in itertools.product(item.nodes, lines):
        node_at, here = (int(at[0]), int(at[1]), int(at[2])), tuple(np.add(at, board.offset))
        pace = int(paces.link_pace_of(gamma, np.asarray(content)[here] if np.ndim(content) else content))
        hole = Hole(unit * 2 * pace * pace * link * link)  # W_rec in the form's own units at the Node
        for tick in ticks:
            found = Face(item.family, line, node_at, 0, tick, None, hole, tick == ticks[1])
            board.credit.faces.setdefault(tick, []).append(found)
    board.credit.counts[item.family] += item.delta


def parted(board: GameBoard, books: NodeBooks, item: Item, phase: Phase | None) -> None:
    """One part of a record declared an instrument at one Node laid at its new count (`relaid`): in the direction and sense of the part the quantum leaves where the list names one (the phase passes with the quantum), in its own otherwise (a part laid again at its count, the null window)."""
    assert item.part is not None and item.nodes == books.nodes
    books.counts[item.part] += item.delta
    (re, im), sense = phase if phase is not None else leaving_phase(board, item)
    relaid(board, books, item.part, books.counts[item.part], (re, im), sense)


def faces_of(board: GameBoard, index: int) -> dict[int, Faces]:
    """The faces presented to a family's lines at this interval's step, per line, with the board's offset (the layers grown before the origin), forward and back alike (`node.step_records`)."""
    found: dict[int, Faces] = {}
    for presented in board.credit.faces.get(board.tick, []):
        if presented.family == index:
            found.setdefault(presented.line, ([], board.offset))[0].append(presented)
    return found


def faces_reported(board: GameBoard) -> None:
    """The faces presented at this interval's step, one `face` line each (`reports.face`): the family, the line, the Node, the Port and the value Rule3 read there, written after the step computed them, for the host's tool, which presents them again on the way back from the lines and not from the books' log (`tools/back_in_time.py`)."""
    if board.observer is None:
        return
    for found in board.credit.faces.get(board.tick, []):
        assert found.value is not None  # computed at this interval's step
        name, at = board.families[found.family].name, list(found.at)
        board.observer(face(board.tick, name, found.line, at, found.port, found.value))


def drawn_node(board: GameBoard, books: NodeBooks, weights: list[int]) -> Node:
    """The one Node of the region a write is laid at, drawn by `weights` over the reader's Nodes with its own generator (features/click, `drawn`; ALGEBRA.md, The NodeReader is one declaration kind for every experiment: the write of a click is at one Node of the region, the share at a Node a GameBoard reading and no measurement); the lay's weights where every weight is 0."""
    assert books.declared.draw is not None
    found = weights if sum(weights) > 0 else list(books.weights)
    pick, books.state = drawn(
        books.state,
        books.declared.draw.multiplier,
        books.declared.draw.increment,
        board.world.width + 1,
        found,
    )
    return books.nodes[pick]


def hole_node(board: GameBoard, books: NodeBooks, drive: int) -> Node:
    """The taking's Node: drawn by the arriving record's share at the reader's Nodes at the window's close (`GameBoard.share_of`, floored at 0, a reading used as the draw's weight), the hole's two faces written there."""
    shares = board.share_of(drive)[0]
    weights = [max(int(shares[tuple(np.add(at, board.offset))]), 0) for at in books.nodes]
    return drawn_node(board, books, weights)


def exchange(books: NodeBooks, leaves: int, enters: int) -> list[Item]:
    """The record's own half of a click's list: one quantum of its count from the part `leaves` to the part `enters` at its Node."""
    return [
        Item(books.index, books.number, part, delta, books.nodes)
        for part, delta in ((enters, 1), (leaves, -1))
    ]


def null_window(board: GameBoard, books: NodeBooks) -> None:
    """The window with no click (the owner's words of 2026-10-02, "Yes, both of them", and of 2026-10-03, "I approve the four things"; the mathematician's 148; the advisor's clause 8): the record's own reading of itself written at its one Node, the one list of the act with the part it stands in at the change 0 (`click`): the record laid again in the complement of its outcome set, the part it stands in, at its whole count, in that part's own direction and sense (the levels of what stands there within the lay's rounding, the remainder at the lay's origin), the parts' counts unchanged, and the labels' coherence ended; where the re-lay changed a level, a write outside Rule3, one click line labelled GAMEBOARD, the `lay` lines beside it carrying the levels before and after at the Node for the host's tool (a null window that changes nothing writes none); one function, the act's one place."""
    before = levels_at(board, books, books.part)
    click(board, books.state, None, [1], [[Item(books.index, books.number, books.part, 0, books.nodes)]])
    if levels_at(board, books, books.part) != before:  # a level changed: its line, the lay lines beside
        reported(board, books, (books.part, books.part), (None, None), False)


def reported(
    board: GameBoard,
    books: NodeBooks,
    parts: tuple[int, int],
    exchanged: tuple[int | None, int | None],
    quantum: bool = True,
) -> None:
    """The click line of a record's click (`reports.credit`, the one click line kind of every reader; ALGEBRA.md, The NodeReader is one declaration kind for every experiment: never a Node): the reader `measured n` by its number, the `parts` realised and left by their declared names (`realised` the part after, `before` the part before), the families `exchanged`, the one taken from and the one given to (None where none), the count moved, 1 for a click and 0 for the null window's write, the count left in the books of the family exchanged (None where none), the window's intervals [first, last], the body's own proper time at the close and the index of the window closed (its books' clock and windows); labelled the detector's where a `quantum` passed and a diagnostic for the null window's write; the Node written stands in the `lay` and `face` lines beside it and here nowhere."""
    if board.observer is None:
        return
    names, families = books.declared.names, board.families
    window = [board.tick - books.elapsed + 1, board.tick]
    taken, light = (families[k].name if k is not None else None for k in exchanged)
    moved = next((k for k in exchanged if k is not None), None)
    left = board.credit.counts[moved] if moved is not None else None
    name, reader, own = families[books.index].name, f"{MEASURED} {books.number}", books.clock[0]
    after, before = names[parts[0]], names[parts[1]]
    line = credit(
        board.tick,
        name,
        reader,
        window,
        own,
        books.windows,
        after,
        None,
        int(quantum),
        left,
        before,
        taken,
        light,
        quantum,
    )
    board.observer(line)


def gave(board: GameBoard, books: NodeBooks, grain: int) -> bool:
    """The giving drawn at the clock's grain, `grain` intervals (ALGEBRA.md, The click writes on the GameBoard (j), the fifth act, and the giving's clock; the advisor's clause 5; the mathematician's 174 (c) and 223 (a), #1572 comment 5965727937, with the advisor's second 5965918924 (a), the per-interval draw at the now of 224 (2)(a), 5966081562, and his second 5966129376, two hands): for the givings out of the part the record stands in, one draw of the act between the giving's list (the part at N - 1 and the lower at N + 1 at its Node, light's record at +1 there, laid as a source in time over the lifetime at the transition's declared resonance, `giving.given_quantum`; `click`) and nothing, the weights [span x p_0 x unit div Gamma, the rest of tau x unit] in the labels' unit (`hazard_weights`) with span the smaller of the grain and the lifetime tau and p_0 the body's own clock at its Node (`own_clock`), the lifetime's hazard 1 / tau per proper interval, [span x unit, (tau - span) x unit] in the vacuum (the beat's current of a one-part record at one Node is 0, so the hazard alone is the rate): the window at its close while a window stands, the one interval in the dark (`dark`), at the now and not a booked waiting time (a booked variate writes a future, which the click's line does not: the click implements the now, the mathematician's 208); the record's own generator; the first giving drawn is taken; one click line. Where the body stands in the open board and its rate declares a `width`, the given quantum is laid as a packet along a drawn direction, one list per direction the board holds, each at the giving's weight, the direction's draw the click's one draw with the record's own generator, an assumption by name (`giving.laid_packet`; the mathematician's 224 (1) and 229 with the advisor's seconds, two hands); inside a guide, or with no width declared, the source in time as built."""
    assert books.declared.draw is not None
    unit = count_wall(board.families[books.index], board.world.quantum_action) ** 2
    clock = own_clock(board, books)
    for rate in books.declared.rates:
        if rate.leaves == books.part:
            span = grain if grain <= rate.lifetime else rate.lifetime
            items = exchange(books, rate.leaves, rate.enters)
            laid_at = drawn_node(
                board, books, list(books.weights)
            )  # the giving's Node by the record's share
            given = Item(rate.light, None, None, 1, (laid_at,), None, rate.resonance, rate.lifetime)
            outcomes = [
                items + [replace(given, width=rate.width, direction=direction)]
                for direction in (rate.directions or (None,))
            ]
            giving, rest = hazard_weights(span, rate.lifetime, clock, board.world.node_clock, unit)
            weights = [giving] * len(outcomes) + [len(outcomes) * rest]
            pick, books.state = click(board, books.state, books.declared.draw, weights, [*outcomes, []])
            if pick < len(outcomes):
                reported(board, books, (rate.enters, rate.leaves), (None, rate.light))
                return True
    return False


def took(board: GameBoard, closing: list[NodeBooks]) -> set[int]:
    """The takings drawn at the windows' end, one draw at a time per arriving family over every closing record's outcomes into it (ALGEBRA.md, The click writes on the GameBoard (f): the credit draws once over all the instruments that read one record, one quantum one click; the owner's word of 2026-10-03): the outcomes the transitions out of the part each record stands in reading that family, each weighted by its label squared, the two-mode line's share, and the outcome that none takes weighted by the rest of the count's unit; the first closing record's generator; none while the arriving record's count stands at 0 in the books; the taking's list the drawn outcome's (the arriving record at -1 at that Node, the record's part entered at +1 and left at -1; `click`); a record that took is done for the window; returns the records done."""
    done: set[int] = set()
    drives = sorted(
        {t.drive for books in closing for t in books.declared.transitions if t.leaves == books.part}
    )
    for drive in drives:
        while board.credit.counts[drive] > 0:
            outcomes = [
                (books, transition)
                for books in closing
                if books.number not in done
                for transition in books.declared.transitions
                if transition.leaves == books.part and transition.drive == drive
            ]
            if not outcomes:
                break
            weights = [books.labels[transition.enters] ** 2 for books, transition in outcomes]
            unit = max(sum(label * label for label in books.labels) for books, _transition in outcomes)
            rest = unit - sum(weights)
            lists = [
                [
                    Item(drive, None, None, -1, (hole_node(board, books, drive),)),
                    *exchange(books, t.leaves, t.enters),
                ]
                for books, t in outcomes
            ]
            first, weighted = closing[0], [*weights, rest if rest > 0 else 0]
            pick, first.state = click(board, first.state, first.declared.draw, weighted, [*lists, []])
            if pick >= len(outcomes):
                break
            books, transition = outcomes[pick]
            reported(board, books, (transition.enters, transition.leaves), (drive, None))
            done.add(books.number)
    return done


def probe_arrived(books: NodeBooks, laid: set[tuple[int, Node]]) -> bool:
    """Whether a probe arrived at the body this interval: a lay at its Node (`laid_whole`, the world's schedule) of the family of one of its transitions of a part into itself; the window's close at the declared tick, no level read (ALGEBRA.md, The pulsed gate: the window bounded by the lays' schedule; the two hands of 2026-10-03, #1572 comment 5967913000)."""
    return any(
        t.leaves == t.enters and (t.drive, at) in laid
        for t in books.declared.transitions
        for at in books.nodes
    )


def probe_click(board: GameBoard, books: NodeBooks) -> None:
    """The click at a probe's arrival, the body's window's close (ALGEBRA.md, The pulsed gate; the two hands of 2026-10-03, #1572 comments 5967783614 and 5967913000): one draw of the act over the transitions out of the part the body stands in whose family's count stands, each at its entered part's label squared as the shears carried the labels from the part the body stood in (the two-mode line's shares, cos^2 and sin^2 of the half window's turn): the probe's own, the transition of the part into itself, re-lays the body whole in that part, its list the part at the change 0 and no write on the probe's record (taken and given back at one tick and one Node, the fluorescence by name the probe's own wave continuing from that Node); a drive's takes the drive's quantum and exchanges the parts as every taking does (the hole, the count down by one); the rest of the labels' unit is the null window, the body whole in its part (`null_window`); one click line for a click, `taken` the family read and `given` the probe's where it was given back; the body's own generator."""
    outcomes = [
        t
        for t in books.declared.transitions
        if t.leaves == books.part and board.credit.counts[t.drive] > 0
    ]
    lists: Lists = []
    for t in outcomes:
        if t.leaves == t.enters:
            lists.append([Item(books.index, books.number, t.leaves, 0, books.nodes)])
        else:
            at = (hole_node(board, books, t.drive),)
            lists.append([Item(t.drive, None, None, -1, at), *exchange(books, t.leaves, t.enters)])
    weights = [books.labels[t.enters] ** 2 for t in outcomes]
    rest = sum(label * label for label in books.labels) - sum(weights)
    weighted = [*weights, rest if rest > 0 else 0]
    pick, books.state = click(board, books.state, books.declared.draw, weighted, [*lists, []])
    if pick < len(outcomes):
        taken = outcomes[pick]
        light = taken.drive if taken.leaves == taken.enters else None
        reported(board, books, (taken.enters, taken.leaves), (taken.drive, light))
    elif len(books.counts) > 1:  # a record of one part reads none
        null_window(board, books)


def jumped(board: GameBoard) -> None:
    """The records at Nodes that are instruments at the end of an interval: first the messages the world lays whole at this tick (`laid_whole`, the probe's lay at the body's Node by the schedule); then each record gathers the records arriving at its Node into its window's sums (`resonance.gathered`, the arriving level per drive family read once, `arriving`), one more interval elapsed and its own clock advanced (`clocked`); the window closes at its declared length, or, for a body with a probe among its transitions, at the tick of the probe's lay at its Node (`probe_arrived`: the window bounded by clicks, opened at the body's last write and closed at the probe's taking, no level read; ALGEBRA.md, The pulsed gate, the two hands of 2026-10-03); at the close the window's turn of the labels (`turned_labels`, once per window, as W sub-turns with the carry) and the body's windows counted, then the draws and the writes, the givings first record by record (`gave`: at the window's close while a window stands, the grain the window's length, at every interval in the dark, `dark`, the lifetime's hazard 1 / tau per interval either way), then at a probe's close the body's own one draw over its outcomes (`probe_click`), at a declared window's the takings in one draw per arriving family over the records that gave none (`took`), then the null window of every record of several parts that neither gave nor took (`null_window`; a record of one part reads no part of itself and has none; a record converted whole is drawn after the records' clicks, src/event_universe/conversion.py), every write the one act's (`click`); the windows begun again."""
    laid_whole(board)
    laid = {(whole.family, whole.at) for whole in board.world.wholes if whole.tick == board.tick}
    for books in board.credit.bodies:
        drives = {transition.drive for transition in books.declared.transitions}
        levels = {drive: arriving(board, books, drive) for drive in drives}
        gathered(books.references, books.declared.transitions, levels)
        books.elapsed += 1
        clocked(board, books)
    closing = [
        b
        for b in board.credit.bodies
        if b.declared.draw is not None
        and (
            probe_arrived(b, laid)
            or (isinstance(b.declared.draw, Instrument) and b.elapsed == b.declared.draw.window)
        )
    ]
    for books in closing:
        turned_labels(board, books)
        books.windows += 1
    closed, given = {books.number for books in closing}, set()
    for books in board.credit.bodies:
        if books.declared.draw is None:
            continue
        grain = 1 if dark(board, books) else books.elapsed if books.number in closed else 0
        if grain and gave(board, books, grain):
            given.add(books.number)
    quiet = [books for books in closing if books.number not in given]
    read = {books.number for books in quiet if probe_arrived(books, laid)}
    for books in quiet:
        if books.number in read:
            probe_click(board, books)
    done = took(board, [books for books in quiet if books.number not in read])
    for books in quiet:
        if books.number not in read | done and len(books.counts) > 1:  # a record of one part reads none
            null_window(board, books)
    for books in closing:
        books.elapsed = 0
