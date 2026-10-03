"""The meeting at a Node (ALGEBRA.md #the-click-is-the-meeting, The click writes on the GameBoard; HIGHLIGHTS.md, the owner's words; the owner's word, the click the heart): a node_reader is where the future met the past, the arriving record's quantum run forward from its root meeting at one Node the node_reader's own transition's quantum read back from the realised click, the click their meeting; a node_reader always receives two quanta, the arriving one and its own, a region node_reader's own quantum implicit in its declared window and whole, and for a record declared an instrument at one Node its record there; from the click the new future goes out, the quantum with the taker to its next meeting (the taker's record changed at its Node and stepped on by Rule3), the hole spreading from the entry Node, the giving's light quantum, and the arriving record's wave with its count at 0, the empty wave, stepped on and never credited. The seven steps in the Node's words (the Boss's sequence with the advisor's and the mathematician's hands): 0, every interval every Node steps every record it holds by Rule3, a bijection, no draw; at the end of an instrument's window at the Node named (the declared window's length, or, for a body with a probe, the tick of the probe's lay at its Node: the window bounded by clicks, opened at the body's last write and closed at the probe's taking, ALGEBRA.md, The pulsed gate), 1, the read, the two records at that Node, the arriving family's level there and the record present, the share their product at resonance (the resonant two-mode act, the two-quadrature form: the arriving level summed over the window against the record's two reference records at the transition's declared resonance, the plane's size over the scale the window's turn at the declared weight, applied once at the window's close as W sub-turns with the carry, turning the two parts' labels into each other, the labels' squares the shares, the Rabi form, `resonance.gathered`, `resonance.window_turn`, `turned_labels`); 2, the draw, with the declared seed and generator, once per window; 3, the write at that Node, one whole quantum passing between the two records there: the arriving record's levels and remainder to 0 (the hole; for a dense record, whose share at the Node exceeds its own quantum, its two levels scaled so that one quantum's share leaves and the phase stands, the hole of a dense record, `faced`) and its count in the books down by one, the present record's realised part laid at N + 1 at that Node in the direction of the part it leaves (the phase passing with the quantum), the remainder at the lay's origin, the part it leaves at N - 1 (the taking); 4, a window with no meeting at a Node whose record reads its own parts, the record laid again in the complement of its outcome set at its whole count (the null window, one function); 5, the giving, at a Node whose record stands in an upper part, drawn at the lifetime's hazard 1 / tau per interval, per window while a window stands and per interval in the dark at the now (the beat's current of a one-part record at one Node being 0, named): one whole quantum passing from that record to the light family's record at the same Node, the upper part to N - 1, the lower to N + 1, light's record up by one whole quantum laid as a source in time at that Node over the giving's lifetime at the transition's declared resonance (`giving.given_quantum`); 6, after the write the Node and its neighbours step by Rule3, nothing written at any other Node, no front; 7, the click line (`reports.credit`, the one click line kind of every reader), the window, the reader, the family and the parts, never a Node, the Node written standing in the GAMEBOARD `lay` and `face` lines beside it. The record declared an instrument is one Node by the world's declaration (its six Link factors 0, `cut`, so that it stays, held by its declaration as the node_reader's region is), its books the instrument's own and at no Node; the Node knows no click."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import front, node
from event_universe.core import paces
from event_universe.core.ports import arrival
from event_universe.core.rule3 import division_forward
from event_universe.features.click import Face, Hole, laid_pairs, standing
from event_universe.giving import given_lines, given_quantum, line_levels_at
from event_universe.loader.derived import count_wall
from event_universe.loader.draw import Draw, Generator
from event_universe.loader.keys import Node
from event_universe.node_reader import (
    NodeBooks,
    arriving,
    clock_advanced,
    dark,
    drawn_node,
    hole_node,
    own_clock,
    picked,
    reported,
)
from event_universe.plane import Faces
from event_universe.reports import face, lay
from event_universe.resonance import gathered, sheared, window_turn

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard


def read_with_cuts(
    board: GameBoard, index: int, direction: int, record: int
) -> tuple[Any, node.Factors]:
    """A record's read at the interval's start in `direction` (`node.read`, every sign row but the record's own), the Links the world cuts at 0 among its factors (`cut`)."""
    gamma, unit, cuts = board.world.node_clock, board.unit, cut(board, index)
    return node.read(
        index, board.families, board.states, direction, board.wrap, gamma, unit, record, cuts
    )


def stepped(
    board: GameBoard, index: int, direction: int
) -> tuple[list[node.Record], list[node.Booking]]:
    """Every record of a family stepped by Rule3 in `direction` with the rule of its own read (`node.step_records`), the Links the world cuts at 0 among its factors (`cut`) and the faces the instrument presents at this interval among its arrivals (`faces_presented`)."""
    gamma, unit, cuts = board.world.node_clock, board.unit, cut(board, index)
    faces = faces_presented(board, index)
    return node.step_records(
        index, board.families, board.states, board.wrap, gamma, unit, direction, cuts, faces
    )


def cut(board: GameBoard, index: int) -> node.Factors | None:
    """The Links the world declares at the factor 0 for a family, per Port the mask of the Nodes whose Port faces them (ALGEBRA.md, The NodeReader is one declaration kind for every experiment: its outer Links cut and its inner Links open): the boundary Links of every region over which a record of the family is laid in its parts, the Links with one end in the region and one outside, read 0 from both ends; the Links between two Nodes of one region stay at G^2, so that the record's uniform mode rotates at cos omega_0 = num / den whatever the region's size; None where the family has no such record."""
    regions = [
        board.mask(row.nodes)
        for row in board.world.bodies
        if row.family == index and row.reader is not None
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
    """A record laid in its parts at its one Node at the start (`loader/node_reader_declaration.py`, `parts`): every part at its declared count, the one carrying the count as the standing record of the pair in the direction (1, 0) and the sense +1, the others 0 there; the books not yet made, so a passing book names the declaration."""
    row = board.world.bodies[number]
    assert row.reader is not None
    books = NodeBooks(number, row.family, record, row.nodes, row.counts, row.reader, 0, [], [], 0, 0, [])
    for part, count in enumerate(row.reader.counts):
        relaid(board, books, part, count, (1, 0), 1)


def levels_at(board: GameBoard, books: NodeBooks, part: int) -> tuple[int, int, int, int]:
    """A part's levels at the reader's first Node, (re_now, im_now, re_before, im_before), read from its two lines: the lay stands in one direction at every Node of the region, so the first Node carries the part's phase."""
    family, state = board.families[books.index], board.states[books.index]
    first = node.record_slice(family, books.record).start + part * family.width
    at = tuple(np.add(books.nodes[0], board.offset))
    re, im = state.lines[first], state.lines[first + 1 if family.plane else first]
    return int(re.now[at]), int(im.now[at]), int(re.before[at]), int(im.before[at])


def laid_whole(board: GameBoard) -> None:
    """The messages laid whole at this interval's end (`loader/messages.py`, `WholeMessage`: the probe of the pulsed gate, the two hands): each its count of whole quanta laid at its Node through the one act with one outcome and no draw (`click`, `given_quantum`, `laid_by_count` at the family's massless pair [den, den], A^2 = count T div 2 on the record's first line), the record's count in the books up by the count and one lay line for the host's tool; the experimenter's lay in time, from outside the Node as every lay is, before the records at Nodes read their arrivals."""
    for whole in board.world.wholes:
        if whole.tick == board.tick:
            den = board.families[whole.family].pair[1]
            items = [Item(whole.family, None, None, whole.count, (whole.at,), (den, den))]
            click_act(board, 0, None, [1], [items])


def hazard_weights(span: int, lifetime: int, clock: int, gamma: int, unit: int) -> list[int]:
    """The dark's draw between the giving and nothing over `span` board intervals at the lifetime tau, a proper time (the mathematician's hand with the advisor's second, two hands): the hazard 1 / tau per proper interval, the body's proper intervals per board tick p_0 / Gamma, so the giving's weight is span x p_0 x unit div Gamma by the division act (half up) against the rest of tau x unit, [span x unit, (tau - span) x unit] exactly in the vacuum where p_0 = Gamma, and in a well the body gives slower by p_0 / Gamma."""
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
    """One entry of a click's list (the mathematician's hand with the advisor's second, two hands; the owner's word, one generic implementation the node_reader operates): the record by its family and, for a record declared an instrument at one Node, its number among `bodies` (None for a record spread over the board), the part (None for every line of a spread record, no line alone), the change of its count, +1, -1 or 0 (the null window moves no count), the Nodes written at, the file's coordinates, and for a spread record given whole quanta the form of its lay (`giving.given_quantum`): the pair its lay stands at where the list names one (the conversion's records out at their family's massless pair [den, den], the lay by the count at one Node, the two hands) with, for a plane, the sense of its lay as the conversion's table declares it (0 for real lines; `giving.laid_by_count`), else the resonance and the span of a source in time (the giving's, the transition's declared resonance and the lifetime, the mathematician's hand with the advisor's second)."""

    family: int
    body: int | None
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


def click_act(
    board: GameBoard, state: int, generator: Generator | None, weights: list[int], outcomes: Lists
) -> tuple[int, int]:
    """The one click act, the node_reader's, of every list alike (the owner's words; the mathematician's hand, the advisor's second, two hands): the outcome drawn (`picked`) and its list written (`written`)."""
    pick, state = picked(board, state, generator, weights, len(outcomes))
    written(board, outcomes[pick])
    return pick, state


def written(board: GameBoard, items: list[Item]) -> None:
    """The write step of the act, the one swappable step, item by item: a spread record's quantum taken by the face at every Node named (`faced`, every line of the record whatever their number) or given by the lay of one whole quantum there (`given_quantum`), its count in the credit's books moved; a record declared an instrument at one Node laid part by part at its new count (`parted`), the direction and sense of the part its quantum leaves read first and passed to the part it enters (the phase passes with the quantum), its books' part the one carrying the count and its labels' coherence ended; where a spread record's count reaches 0 its erasing front begins from every Node of its items (`front.started`); every line a lay changed at a Node, levels or remainder, written as one `lay` line with the levels before and after (`laid_lines`, `line_levels_at`, `reports.lay`), the diagnostic the host's tool crosses the lay from (the mathematician's hand: the face's part crossed by Rule3's inverse, the lay's part from its line)."""
    leaving = [item for item in items if item.body is not None and item.delta < 0]
    phases = {item.body: leaving_phase(board, item) for item in leaving}
    laid = [
        (i.family, line, at)
        for i in items
        if i.direction is None  # a packet writes its own lay lines at every Node it lays
        for line in laid_lines(board, i)
        for at in i.nodes
    ]
    before = [line_levels_at(board, *entry) for entry in laid]
    touched: list[NodeBooks] = []
    for item in items:
        if item.body is None:
            (faced if item.delta < 0 else given_quantum)(board, item)
            continue
        parted(board, books := books_named(board, item.body), item, phases.get(item.body))
        touched += [books] if books not in touched else []
    for books in touched:
        books.part = max(range(len(books.counts)), key=lambda k: books.counts[k])
        wall = count_wall(board.families[books.index], board.world.quantum_action)
        books.labels = [count * wall for count in books.counts]
    for family in sorted({i.family for i in items if i.body is None and i.delta < 0}):
        if board.credit.counts[family] <= 0:  # the count at 0: its front from every Node written
            front.started(board, family, [at for i in items if i.family == family for at in i.nodes])
    for (index, line, at), was in zip(laid, before, strict=True):
        now = line_levels_at(board, index, line, at)
        if now != was and board.output is not None:
            board.output(lay(board.tick, board.families[index].name, line, list(at), was, now))


def laid_lines(board: GameBoard, item: Item) -> list[int]:
    """The lines of a record an item lays at its Nodes: the lines of the part of a record declared an instrument at one Node (`parted`), the lines of a spread record given whole quanta (`given_quantum`, `giving.given_lines`: every laid line of one part of its first record, a plane's two lines per plane, a holder of the sign's time line alone), none for a quantum taken by the face."""
    if item.body is None:
        return given_lines(board.families[item.family]) if item.delta > 0 else []
    assert item.part is not None
    family, books = board.families[item.family], books_named(board, item.body)
    first = node.record_slice(family, books.record).start + item.part * family.width
    return list(range(first, first + family.width))


def books_named(board: GameBoard, body: int) -> NodeBooks:
    """The books of the record declared an instrument numbered `body` among the world's `bodies`."""
    return next(books for books in board.credit.bodies if books.number == body)


def leaving_phase(board: GameBoard, item: Item) -> Phase:
    """The direction (re, im) and the sense (the sign of the Wronskian) of the part a quantum leaves, read at the Node before any lay of the list."""
    assert item.part is not None
    re, im, re_before, im_before = levels_at(board, books_named(board, item.body or 0), item.part)
    return (re, im), 1 if re * im_before - im * re_before >= 0 else -1


def faced(board: GameBoard, item: Item) -> None:
    """A spread record's quantum taken at the Nodes named, the face (features/click, `Face`; ALGEBRA.md, The click writes on the GameBoard (b) and (d), and the hole of a dense record): for every line of the record and every Node, one face at the next two intervals, the first Port preferred, so that Rule3 writes the level 0 and then the level before 0 with its own remainder where the record's booked share at the Node, O + C / 2, is at most its own quantum (the mathematician's hand; the front erasing what spread beyond the Node), and otherwise (a dense record, the Zeno drive at 3.5 quanta per Node or the ion's drive at 55) each face writes its level by the booking identity, one `Hole` per line and Node shared by its two faces carrying the record's unit from the books in the form's own units at the Node, W_rec x 2 p_i^2 G^2 (the share's weight, `share.over_pace`, p_i the Node's Link pace under the record's read), the first face removing one quantum or the most one write can and recording exactly what left, the second the rest the same way (`features/click.rest_of`; the mathematician's hand with the advisor's second); the record's count in the credit's books down by the item's change; nothing assigned at any Node."""
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


def faces_presented(board: GameBoard, index: int) -> dict[int, Faces]:
    """The faces presented to a family's lines at this interval's step, per line, with the board's offset (the layers grown before the origin), forward and back alike (`node.step_records`)."""
    found: dict[int, Faces] = {}
    for presented in board.credit.faces.get(board.tick, []):
        if presented.family == index:
            found.setdefault(presented.line, ([], board.offset))[0].append(presented)
    return found


def faces_reported(board: GameBoard) -> None:
    """The faces presented at this interval's step, one `face` line each (`reports.face`): the family, the line, the Node, the Port and the value Rule3 read there, written after the step computed them, for the host's tool, which presents them again on the way back from the lines and not from the books' log (`tools/back_in_time.py`)."""
    if board.output is None:
        return
    for found in board.credit.faces.get(board.tick, []):
        assert found.value is not None  # computed at this interval's step
        name, at = board.families[found.family].name, list(found.at)
        board.output(face(board.tick, name, found.line, at, found.port, found.value))


def exchange(books: NodeBooks, leaves: int, enters: int) -> list[Item]:
    """The record's own half of a click's list: one quantum of its count from the part `leaves` to the part `enters` at its Node."""
    return [
        Item(books.index, books.number, part, delta, books.nodes)
        for part, delta in ((enters, 1), (leaves, -1))
    ]


def null_window(board: GameBoard, books: NodeBooks) -> None:
    """The window with no click (the owner's words, "Yes, both of them" and "I approve the four things"; the mathematician's hand; the advisor's clause 8): the record's own reading of itself written at its one Node, the one list of the act with the part it stands in at the change 0 (`click`): the record laid again in the complement of its outcome set, the part it stands in, at its whole count, in that part's own direction and sense (the levels of what stands there within the lay's rounding, the remainder at the lay's origin), the parts' counts unchanged, and the labels' coherence ended; where the re-lay changed a level, a write outside Rule3, one click line labelled GAMEBOARD, the `lay` lines beside it carrying the levels before and after at the Node for the host's tool (a null window that changes nothing writes none); one function, the act's one place."""
    before = levels_at(board, books, books.part)
    click_act(
        board, books.state, None, [1], [[Item(books.index, books.number, books.part, 0, books.nodes)]]
    )
    if levels_at(board, books, books.part) != before:  # a level changed: its line, the lay lines beside
        reported(board, books, (books.part, books.part), (None, None), 0)


def gave(board: GameBoard, books: NodeBooks, grain: int) -> bool:
    """The giving drawn at the clock's grain, `grain` intervals (ALGEBRA.md, The click writes on the GameBoard (j), the fifth act, and the giving's clock; the advisor's clause 5; the mathematician's hand with the advisor's seconds, two hands): for the givings out of the part the record stands in, one draw of the act between the giving's list (the part at N - 1 and the lower at N + 1 at its Node, light's record at +1 there, laid as a source in time over the lifetime at the transition's declared resonance, `giving.given_quantum`; `click`) and nothing, the weights [span x p_0 x unit div Gamma, the rest of tau x unit] in the labels' unit (`hazard_weights`) with span the smaller of the grain and the lifetime tau and p_0 the body's own clock at its Node (`own_clock`), the lifetime's hazard 1 / tau per proper interval, [span x unit, (tau - span) x unit] in the vacuum (the beat's current of a one-part record at one Node is 0, so the hazard alone is the rate): the window at its close while a window stands, the one interval in the dark (`dark`), at the now and not a booked waiting time (a booked variate writes a future, which the click's line does not: the click implements the now, the mathematician's hand); the record's own generator; the first giving drawn is taken; one click line. Where the body stands in the open board and its rate declares a `width`, the given quantum is laid as a packet along a drawn direction, one list per direction the board holds, each at the giving's weight, the direction's draw the click's one draw with the record's own generator, an assumption by name (`giving.laid_packet`; the mathematician's hand with the advisor's seconds, two hands); inside a guide, or with no width declared, the source in time as built."""
    assert books.declared.draw is not None
    unit = count_wall(board.families[books.index], board.world.quantum_action) ** 2
    clock = own_clock(board, books)
    for rate in books.declared.rates:
        if rate.leaves == books.part:
            span = grain if grain <= rate.lifetime else rate.lifetime
            directions = rate.directions or (None,)
            giving, rest = hazard_weights(span, rate.lifetime, clock, board.world.node_clock, unit)
            weights = [giving] * len(directions) + [len(directions) * rest]
            pick, books.state = picked(
                board, books.state, books.declared.draw, weights, len(directions) + 1
            )
            if pick < len(directions):
                laid_at = drawn_node(board, books, list(books.weights))
                given = Item(rate.light, None, None, 1, (laid_at,), None, rate.resonance, rate.lifetime)
                items = exchange(books, rate.leaves, rate.enters)
                written(board, items + [replace(given, width=rate.width, direction=directions[pick])])
                reported(board, books, (rate.enters, rate.leaves), (None, rate.light))
                return True
    return False


def took(board: GameBoard, closing: list[NodeBooks]) -> set[int]:
    """The takings drawn at the windows' end, one draw at a time per arriving family over every closing record's outcomes into it (ALGEBRA.md, The click writes on the GameBoard (f): the credit draws once over all the instruments that read one record, one quantum one click; the owner's word): the outcomes the transitions out of the part each record stands in reading that family, each weighted by its label squared, the two-mode line's share, and the outcome that none takes weighted by the rest of the count's unit; the first closing record's generator; none while the arriving record's count stands at 0 in the books; the taking's list the drawn outcome's (the arriving record at -1 at that Node, the record's part entered at +1 and left at -1; `click`); a record that took is done for the window; returns the records done."""
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
            first, weighted = closing[0], [*weights, rest if rest > 0 else 0]
            pick, first.state = picked(
                board, first.state, first.declared.draw, weighted, len(outcomes) + 1
            )
            if pick >= len(outcomes):
                break
            books, transition = outcomes[pick]
            hole = Item(drive, None, None, -1, (hole_node(board, books, drive),))
            written(board, [hole, *exchange(books, transition.leaves, transition.enters)])
            reported(board, books, (transition.enters, transition.leaves), (drive, None))
            done.add(books.number)
    return done


def probe_arrived(books: NodeBooks, laid: set[tuple[int, Node]]) -> bool:
    """Whether a probe arrived at the body this interval: a lay at its Node (`laid_whole`, the world's schedule) of the family of one of its transitions of a part into itself; the window's close at the declared tick, no level read (ALGEBRA.md, The pulsed gate: the window bounded by the lays' schedule; the two hands)."""
    return any(
        t.leaves == t.enters and (t.drive, at) in laid
        for t in books.declared.transitions
        for at in books.nodes
    )


def probe_click(board: GameBoard, books: NodeBooks) -> None:
    """The click at a probe's arrival, the body's window's close (ALGEBRA.md, The pulsed gate; the two hands): one draw of the act over the transitions out of the part the body stands in whose family's count stands, each at its entered part's label squared as the shears carried the labels from the part the body stood in (the two-mode line's shares, cos^2 and sin^2 of the half window's turn): the probe's own, the transition of the part into itself, re-lays the body whole in that part, its list the part at the change 0 and no write on the probe's record (taken and given back at one tick and one Node, the fluorescence by name the probe's own wave continuing from that Node); a drive's takes the drive's quantum and exchanges the parts as every taking does (the hole, the count down by one); the rest of the labels' unit is the null window, the body whole in its part (`null_window`); one click line for a click, `taken` the family read and `given` the probe's where it was given back; the body's own generator."""
    outcomes = [
        t
        for t in books.declared.transitions
        if t.leaves == books.part and board.credit.counts[t.drive] > 0
    ]
    weights = [books.labels[t.enters] ** 2 for t in outcomes]
    rest = sum(label * label for label in books.labels) - sum(weights)
    weighted = [*weights, rest if rest > 0 else 0]
    pick, books.state = picked(board, books.state, books.declared.draw, weighted, len(outcomes) + 1)
    if pick < len(outcomes):
        taken = outcomes[pick]
        if taken.leaves == taken.enters:
            written(board, [Item(books.index, books.number, taken.leaves, 0, books.nodes)])
        else:
            at = (hole_node(board, books, taken.drive),)
            written(
                board,
                [Item(taken.drive, None, None, -1, at), *exchange(books, taken.leaves, taken.enters)],
            )
        light = taken.drive if taken.leaves == taken.enters else None
        reported(board, books, (taken.enters, taken.leaves), (taken.drive, light))
    elif len(books.counts) > 1:  # a record of one part reads none
        null_window(board, books)


def jumped(board: GameBoard) -> None:
    """The records at Nodes that are instruments at the end of an interval: first the messages the world lays whole at this tick (`laid_whole`, the probe's lay at the body's Node by the schedule); then each record gathers the records arriving at its Node into its window's sums (`resonance.gathered`, the arriving level per drive family read once, `arriving`), one more interval elapsed and its own clock advanced (`node_reader.clock_advanced`); the window closes at its declared length, or, for a body with a probe among its transitions, at the tick of the probe's lay at its Node (`probe_arrived`: the window bounded by clicks, opened at the body's last write and closed at the probe's taking, no level read; ALGEBRA.md, The pulsed gate, the two hands); at the close the window's turn of the labels (`turned_labels`, once per window, as W sub-turns with the carry) and the body's windows counted, then the draws and the writes, the givings first record by record (`gave`: at the window's close while a window stands, the grain the window's length, at every interval in the dark, `dark`, the lifetime's hazard 1 / tau per interval either way), then at a probe's close the body's own one draw over its outcomes (`probe_click`), at a declared window's the takings in one draw per arriving family over the records that gave none (`took`), then the null window of every record of several parts that neither gave nor took (`null_window`; a record of one part reads no part of itself and has none; a record converted whole is drawn after the records' clicks, src/event_universe/conversion.py), every write the one act's (`click`); the windows begun again."""
    laid_whole(board)
    laid = {(whole.family, whole.at) for whole in board.world.wholes if whole.tick == board.tick}
    for books in board.credit.bodies:
        drives = {transition.drive for transition in books.declared.transitions}
        levels = {drive: arriving(board, books, drive) for drive in drives}
        gathered(books.references, books.declared.transitions, levels)
        books.elapsed += 1
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
        books.intake = {}
