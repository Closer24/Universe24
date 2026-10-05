"""The meeting at a Node (ALGEBRA.md #the-click-is-the-meeting, The click writes on the lattice; HIGHLIGHTS.md, the owner's words; the owner's word, the click the heart): a node_detector is where the future met the past, the arriving record's quantum run forward from its root meeting at one Node the node_detector's own transition's quantum read back from the realised click, the click their meeting; a node_detector always receives two quanta, the arriving one and its own, a region node_detector's own quantum implicit in its declared window and whole, and for a record declared a NodeDetector at one Node its record there; from the click the new future goes out, the quantum with the taker to its next meeting (the taker's record changed at its Node and stepped on by Rule3), the hole spreading from the entry Node, the emission's light quantum, and the arriving record's wave with its count at 0, the empty wave, stepped on and never credited. The seven steps in the Node's words (the Boss's sequence with the advisor's and the mathematician's hands): 0, every interval every Node steps every record it holds by Rule3, a bijection, no draw; at the end of an reader's window at the Node named (the declared window's length, or, for a body with a probe, the interval of the probe's lay at its Node: the window bounded by clicks, opened at the body's last write and closed at the probe's absorption, ALGEBRA.md, The pulsed gate), 1, the read, the two records at that Node, the arriving family's level there and the record present, the share their product at resonance (the resonant two-mode act, the two-quadrature form: the arriving level summed over the window against the record's two reference records at the transition's declared resonance, the plane's size over the scale the window's turn at the declared weight, applied once at the window's close as W sub-turns with the carry, turning the two parts' labels into each other, the labels' squares the shares, the Rabi form, `resonance.gathered`, `resonance.window_turn`, `turned_labels`); 2, the draw, with the declared seed and generator, once per window; 3, the write at that Node, one whole quantum passing between the two records there, the drive's item carrying the sign of the transition's direction in the body's declared order of parts (`exchange`): climbing, the arriving record's levels and remainder to 0 (the hole to 0 where the record's booked share at the Node is at most its own quantum; for a dense record, a beam of many quanta per Node, nothing on the board, the quantum passing in the books alone with the deficit printed, the undepleted beam, `faced`) and its count in the books down by one; descending, stimulated emission, one quantum given back into the drive (by the count where it is local and whole at the Node, nothing where it is a beam) and its count up by one; the present record's realised part laid at N + 1 at that Node in the direction of the part it leaves turned by the arriving record's phase at the Node, atan2(Y', X) of the window's two sums the close held (the phase passing with the quantum, `resonance.turned_direction`, `Item.arrival`), the remainder at the lay's origin, the part it leaves at N - 1 (the absorption); 4, a window with no meeting at a Node whose record reads its own parts, the record laid again in the complement of its outcome set at its whole count (the null window, one function); 5, the emission, at a Node whose record stands in an upper part, drawn at the lifetime's hazard 1 / tau per interval, per window while a window stands and per interval in the dark at the now (the beat's current of a one-part record at one Node being 0, named): one whole quantum passing from that record to the light family's record at the same Node, the upper part to N - 1, the lower to N + 1, light's record up by one whole quantum laid as a source in time at that Node over the emission's lifetime at the transition's declared resonance from the phase phi_e - phi_g, the two parts' directions read before the lay (`Item.levels`, `emission.start_of`, `emission.emitted_quantum`); 6, after the write the Node and its neighbours step by Rule3, nothing written at any other Node, no front; 7, the click line (`reports.credit`, the one click line kind of every reader), the window, the reader, the family and the parts, never a Node, the Node written standing in the LATTICE `lay` and `face` lines beside it. The record declared a NodeDetector is one Node by the world's declaration (its six Link factors 0, `cut`, so that it stays, held by its declaration as the node_detector's region is), its books the reader's own and at no Node; the Node knows no click."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import front, node
from event_universe.core.ports import arrival
from event_universe.core.rule3 import division_forward
from event_universe.emission import emitted_quantum
from event_universe.features.click import Face, laid_pairs, standing
from event_universe.lay import laid
from event_universe.loader.derived import count_wall
from event_universe.loader.draw import Draw, Generator
from event_universe.loader.keys import Node
from event_universe.node_detector import (
    NodeBooks,
    arriving,
    clock_advanced,
    dark,
    drawn_node,
    hole_node,
    own_clock,
    picked,
    reported,
    share_weights,
)
from event_universe.plane import Faces
from event_universe.reports import face
from event_universe.resonance import arrival_of, gathered, sheared, turned_direction, window_turn

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


def read_with_cuts(board: Lattice, index: int, direction: int, record: int) -> tuple[Any, node.Factors]:
    """A record's read at the interval's start in `direction` (`node.read`, every sign row but the record's own), the Links the world cuts at 0 among its factors (`cut`)."""
    gamma, unit, cuts = board.world.node_clock, board.unit, cut(board, index)
    return node.read(
        index, board.families, board.states, direction, board.wrap, gamma, unit, record, cuts
    )


def stepped(board: Lattice, index: int, direction: int) -> tuple[list[node.Record], list[node.Booking]]:
    """Every record of a family stepped by Rule3 in `direction` with the rule of its own read (`node.step_records`), the Links the world cuts at 0 among its factors (`cut`) and the faces the click act presents at this interval among its arrivals (`faces_presented`)."""
    gamma, unit, cuts = board.world.node_clock, board.unit, cut(board, index)
    faces = faces_presented(board, index)
    return node.step_records(
        index, board.families, board.states, board.wrap, gamma, unit, direction, cuts, faces
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


def relaid(
    board: Lattice, books: NodeBooks, part: int, count: int, phase: tuple[int, int], sense: int
) -> None:
    """The lay of one part of the record over the NodeDetector's Nodes through the one act (features/click, `standing`, `laid_pairs`; `lay.laid`): at every Node of the region the part's lines move to the levels of its share of `count` quanta, A_i^2 = A^2 weight_i / total in the counts' proportion, standing in the direction `phase` and the sense `sense`, the change from what stands handed to the act with no weights (a record at its Node is laid as built, named) and the remainder at the division's origin at every Node of the region, the lay lines the write step's; the count's own lines alone, the other parts untouched."""
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
            (re, im), (re_before, im_before) = standing(count, action, family.pair, phase, sense, share)
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


def laid_record(board: Lattice, number: int, record: int) -> None:
    """A record laid in its parts at its one Node at the start (`loader/node_detector_declaration.py`, `parts`): every part at its declared count, the one carrying the count as the standing record of the pair in the direction (1, 0) and the sense +1, the others 0 there; the books not yet made, so a passing book names the declaration."""
    row = board.world.bodies[number]
    kind = row.detector
    assert kind is not None
    books = NodeBooks(number, row.family, record, row.nodes, row.counts, kind, 0, [], [], 0, 0, [])
    for part, count in enumerate(kind.counts):
        relaid(board, books, part, count, (1, 0), 1)


def levels_at(board: Lattice, books: NodeBooks, part: int) -> tuple[int, int, int, int]:
    """A part's levels at the reader's first Node, (re_now, im_now, re_before, im_before), read from its two lines: the lay stands in one direction at every Node of the region, so the first Node carries the part's phase."""
    family, state = board.families[books.index], board.states[books.index]
    first = node.record_slice(family, books.record).start + part * family.width
    at = tuple(np.add(books.nodes[0], board.offset))
    re, im = state.lines[first], state.lines[first + 1 if family.plane else first]
    return int(re.now[at]), int(im.now[at]), int(re.before[at]), int(im.before[at])


def laid_whole(board: Lattice) -> None:
    """The packets laid whole at this interval's end (`loader/packets.py`, `WholePacket`: the probe of the pulsed gate, the two hands): each its count of whole quanta laid at its Node through the one act with one outcome and no draw (`click`, `emitted_quantum`, `laid_by_count` at the family's massless pair [den, den], A^2 = count T div 2 on the record's first line), the record's count in the books up by the count and one lay line for the host's tool; the experimenter's lay in time, from outside the Node as every lay is, before the records at Nodes read their arrivals."""
    for whole in board.world.wholes:
        if whole.interval == board.interval:
            den = board.families[whole.family].pair[1]
            items = [Item(whole.family, None, None, whole.count, (whole.at,), (den, den))]
            click_act(board, 0, None, [1], [items])


def hazard_weights(span: int, lifetime: int, clock: int, gamma: int, unit: int) -> list[int]:
    """The dark's draw between the emission and nothing over `span` board intervals at the lifetime tau, a proper time (the mathematician's hand with the advisor's second, two hands): the hazard 1 / tau per proper interval, the body's proper intervals per board interval p_0 / Gamma, so the emission's weight is span x p_0 x unit div Gamma by the division act (half up) against the rest of tau x unit, [span x unit, (tau - span) x unit] exactly in the vacuum where p_0 = Gamma, and in a well the body gives slower by p_0 / Gamma."""
    emitted = int(division_forward(span * clock * unit, gamma, division_forward(gamma, 2, 0)[0])[0])
    return [emitted, lifetime * unit - emitted]


def turned_labels(board: Lattice, books: NodeBooks) -> None:
    """The resonant two-mode act at the window's close, once per window (ALGEBRA.md, The two-mode line; The click writes on the lattice (b), the share at resonance; item 50, the two-quadrature form, two hands): for every transition out of the part the record stands in, the window's turn (`resonance.window_turn`, the plane's size over the scale) scaled by the record's own clock (`node.turned_by`, the tangent half-angle over 2 Gamma) turns the two parts' labels into each other by the engine's own three shears (features/rotation) as W equal sub-turns with the carry (`resonance.sheared`, W the window's intervals, so the angles add as the proper intervals' did), the plane's size over the wall read once and not a turn per interval; the labels' squares are the parts' population after the window; the window's draw reads each transition's own transfer share, kept in the books (`NodeBooks.shares`): the pair as it stood before the window's turns sheared by that transition's turn alone, its entered label squared, sin^2 of the turn, the Rabi form, the record's share at the body (`absorbed`, `probe_click`), the composed label squared itself where one transition alone feeds the part; the complement outcome at the close, none takes, is the null window (`null_window`, the record re-laid in its part at its count, the labels' coherence ended); every transition's two sums then begin again, the reference records running on."""
    gamma, clock = board.world.node_clock, own_clock(board, books)
    before, books.shares = list(books.labels), {}
    for transition, reference in zip(books.declared.transitions, books.references, strict=True):
        leaves, enters = transition.leaves, transition.enters
        if leaves == books.part and leaves != enters:  # the probe's turns nothing
            turn = int(node.turned_by(window_turn(reference, transition.weight), clock, gamma))
            own = sheared(before[leaves], before[enters], turn, books.elapsed, gamma)
            u, v = sheared(books.labels[leaves], books.labels[enters], turn, books.elapsed, gamma)
            books.labels[leaves], books.labels[enters], books.shares[transition] = u, v, own[1] ** 2
        reference.closed()


@dataclass(frozen=True)
class Item:
    """One entry of a click's list (the mathematician's hand with the advisor's second, two hands; the owner's word, one generic implementation the node_detector operates): the record by its family and, for a record declared a NodeDetector at one Node, its number among `bodies` (None for a record spread over the board), the part (None for every line of a spread record, no line alone), the change of its count, +1, -1 or 0 (the null window moves no count), the Nodes written at, the file's coordinates, and for a spread record given whole quanta the form of its lay (`emission.emitted_quantum`): the pair its lay stands at where the list names one (the conversion's records out at their family's massless pair [den, den], the lay by the count at one Node, the two hands) with, for a plane, the sense of its lay as the conversion's table declares it (0 for real lines; `emission.laid_by_count`), else the resonance and the span of a source in time (the emission's, the transition's declared resonance and the lifetime, the mathematician's hand with the advisor's second); the absorption's items carry the arriving record's phase at the close, (X, Y'), `arrival`, by which the entered part's direction is turned (`parted`), and the light's item the two parts' (re, im) at the Node, `levels`, the excited and the ground part's, the born source's phase phi_e - phi_g (`emission.start_of`)."""

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


Lists = list[list[Item]]  # the outcomes of one click, each the list written where it is drawn
Phase = tuple[tuple[int, int], int]  # a part's direction (re, im) and its sense, its Wronskian's sign


def click_act(
    board: Lattice, state: int, generator: Generator | None, weights: list[int], outcomes: Lists
) -> tuple[int, int]:
    """The one click act, the node_detector's, of every list alike (the owner's words; the mathematician's hand, the advisor's second, two hands): the outcome drawn (`picked`) and its list written (`written`)."""
    pick, state = picked(board, state, generator, weights, len(outcomes))
    written(board, outcomes[pick])
    return pick, state


def written(board: Lattice, items: list[Item]) -> None:
    """The write step of the act, the one swappable step, item by item (ALGEBRA.md, The click writes on the lattice, the undepleted beam; the two hands' line at the owner's word for the simple solution): a spread record's quantum is taken or given at the Nodes named through one comparison, `faced`, the record's booked share at the Node against its own quantum W_rec; where the record is local and whole there the absorption is the hole to 0 by the face (every line of the record whatever their number) and the emission the lay of one whole quantum (`emitted_quantum`), and where the record is a beam, many quanta per Node, nothing is written on the board: the quantum passes in the books alone, the count moved by the item's change as for every item and the family's deficit, the board's share over the books' count in quanta, moved against it (`credit.Books.deficits`, up by one for an absorption written at no Node named, down by one for an emission not laid, the deficit's condition the complement of the lay's: an emission naming several Nodes with a beam among them lays nothing and moves the deficit, though no shipped list names several Nodes for an emission; printed in the books' line), and a quantum passing into or out of a spread record ends its windows' account, its unabsorbed share and its denominator dropped from the credit's books to begin again at the count left (`credit.Books.account_ended`, `absorbed`); a record declared a NodeDetector at one Node laid part by part at its new count (`parted`), the direction and sense of the part its quantum leaves read first and passed to the part it enters (the phase passes with the quantum), its books' part the one carrying the count and its labels' coherence ended; where a spread record's count reaches 0 its erasing front begins from every Node faced (`front.started`), and a record whose count stays at one or more has no front; every lay of the step is the one lay act's, which writes every line a lay changed at a Node, levels or remainder, as one `lay` line with the levels before and after (`lay.written`, `reports.lay`), the diagnostic the host's tool crosses the lay from (the mathematician's hand: the face's part crossed by Rule3's inverse, the lay's part from its line)."""
    phases = {i.body: leaving_phase(board, i) for i in items if i.body is not None and i.delta < 0}
    touched: list[NodeBooks] = []
    holes: dict[int, list[Node]] = {}
    for item in items:
        if item.body is not None:
            parted(board, books := books_named(board, item.body), item, phases.get(item.body))
            touched += [books] if books not in touched else []
            continue
        whole = faced(board, item)
        unwritten = not whole if item.delta < 0 else len(whole) < len(item.nodes)
        if item.delta > 0 and not unwritten:
            emitted_quantum(board, item)
        else:
            board.credit.counts[item.family] += item.delta
        board.credit.account_ended(item.family)
        if item.delta < 0:
            holes.setdefault(item.family, []).extend(whole)
        if unwritten:  # the undepleted beam: the quantum in the books alone
            board.credit.deficits[item.family] = board.credit.deficits.get(item.family, 0) - item.delta
    for books in touched:
        books.part = max(range(len(books.counts)), key=lambda k: books.counts[k])
        wall = count_wall(board.families[books.index], board.world.quantum_action)
        books.labels = [count * wall for count in books.counts]
    for family, absorbed in sorted(holes.items()):
        if board.credit.counts[family] <= 0 and absorbed:  # the count at 0: its front from every Node
            front.started(board, family, absorbed)


def books_named(board: Lattice, body: int) -> NodeBooks:
    """The books of the record declared a NodeDetector numbered `body` among the world's `bodies`."""
    return next(books for books in board.credit.bodies if books.number == body)


def leaving_phase(board: Lattice, item: Item) -> Phase:
    """The direction (re, im) and the sense (the sign of the Wronskian) of the part a quantum leaves, read at the Node before any lay of the list."""
    assert item.part is not None
    re, im, re_before, im_before = levels_at(board, books_named(board, item.body or 0), item.part)
    return (re, im), 1 if re * im_before - im * re_before >= 0 else -1


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


def parted(board: Lattice, books: NodeBooks, item: Item, phase: Phase | None) -> None:
    """One part of a record declared a NodeDetector at one Node laid at its new count (`relaid`): in the sense of the part the quantum leaves where the list names one, the entered part's direction the leaving part's turned by the arriving record's phase at the Node, atan2(Y', X) of the two sums the close held (`Item.arrival`, `resonance.turned_direction`; ALGEBRA.md, The two-mode line, row 16: the phase passes with the quantum, the product's phase phi_part = phi_left + phi_L), unturned where no arrival stands (the emission's items); in its own direction and sense otherwise (a part laid again at its count, the null window)."""
    assert item.part is not None and item.nodes == books.nodes
    books.counts[item.part] += item.delta
    (re, im), sense = phase if phase is not None else leaving_phase(board, item)
    direction = (re, im) if item.arrival is None else turned_direction(re, im, *item.arrival)
    relaid(board, books, item.part, books.counts[item.part], direction, sense)


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


def exchange(
    board: Lattice, books: NodeBooks, leaves: int, enters: int, drive: int | None = None
) -> list[Item]:
    """The record's own half of a click's list, one quantum of its count from the part `leaves` to the part `enters` at its Node, and before it, for a transition by a `drive`, the drive's item at the Node the drive's inflow draws (`hole_node`): the drive's quantum taken, -1, where the transition climbs, the part entered above the part left in the body's declared order of parts (the first part the lowest, `loader/node_detector_declaration.parts_of`), and given back, +1, where it descends, stimulated emission, by the count at the drive's own pair where the drive is local and whole at the Node and nothing where it is a beam (`written`, `faced`, the undepleted beam; the two hands' line); both items carry the arriving record's phase the close held for the transition, (X, Y') (`resonance.arrival_of`), None for an emission, which names no drive."""
    arrival = arrival_of(books.declared.transitions, books.references, (leaves, enters, drive))
    entering = Item(books.index, books.number, enters, 1, books.nodes, arrival=arrival)
    parts = [entering, replace(entering, part=leaves, delta=-1, arrival=None)]
    if drive is None:
        return parts
    sign = -1 if enters > leaves else 1
    pair = board.families[drive].pair if sign > 0 else None
    return [Item(drive, None, None, sign, (hole_node(board, books, drive),), pair), *parts]


def null_window(board: Lattice, books: NodeBooks) -> None:
    """The window with no click (the owner's words, "Yes, both of them" and "I approve the four things"; the mathematician's hand; the advisor's clause 8): the record's own reading of itself written at its one Node, the one list of the act with the part it stands in at the change 0 (`click`): the record laid again in the complement of its outcome set, the part it stands in, at its whole count, in that part's own direction and sense (the levels of what stands there within the lay's rounding, the remainder at the lay's origin), the parts' counts unchanged, and the labels' coherence ended; where the re-lay changed a level, a write outside Rule3, one click line labelled LATTICE, the `lay` lines beside it carrying the levels before and after at the Node for the host's tool (a null window that changes nothing writes none); one function, the act's one place."""
    before = levels_at(board, books, books.part)
    item = Item(books.index, books.number, books.part, 0, books.nodes)
    click_act(board, books.state, None, [1], [[item]])
    if levels_at(board, books, books.part) != before:  # a level changed: its line, the lay lines beside
        reported(board, books, (books.part, books.part), (None, None), 0)


def emitted(board: Lattice, books: NodeBooks, grain: int) -> bool:
    """The emission drawn at the clock's grain, `grain` intervals (ALGEBRA.md, The click writes on the lattice (j), the fifth act, and the emission's clock; the advisor's clause 5; the mathematician's hand with the advisor's seconds, two hands): for the emissions out of the part the record stands in, one draw of the act between the emission's list (the part at N - 1 and the lower at N + 1 at its Node, light's record at +1 there, laid as a source in time over the lifetime at the transition's declared resonance, `emission.emitted_quantum`; `click`) and nothing, the weights [span x p_0 x unit div Gamma, the rest of tau x unit] in the labels' unit (`hazard_weights`) with span the smaller of the grain and the lifetime tau (the grain the window's lit intervals at its close, `NodeBooks.lit`, the dark ones drawn at their own grain 1 as they pass, `jumped`) and p_0 the body's own clock at its Node (`own_clock`), the lifetime's hazard 1 / tau per proper interval, [span x unit, (tau - span) x unit] in the vacuum (the beat's current of a one-part record at one Node is 0, so the hazard alone is the rate): the window at its close while a window stands, the one interval in the dark (`dark`), at the now and not a booked waiting time (a booked variate writes a future, which the click's line does not: the click implements the now, the mathematician's hand); the record's own generator; the first emission drawn is taken, its quantum laid at the one Node of the body's region drawn by the record's share at the body's Nodes as the board holds it at the close (`share_weights`, `drawn_node`; the file's lay weights enter no draw); one click line. Where the body stands in the open board and its rate declares a `width`, the emitted quantum is laid as a packet along a drawn direction, one list per direction the board holds, each at the emission's weight, the direction's draw the click's one draw with the record's own generator, an assumption by name (`emission.laid_packet`; the mathematician's hand with the advisor's seconds, two hands); inside a guide, or with no width declared, the source in time as built; the light's item carries the two parts' (re, im) at the Node read before the lay (`levels_at`, `Item.levels`), the source begun at the phase phi_e - phi_g (`emission.start_of`)."""
    assert books.declared.draw is not None
    unit = count_wall(board.families[books.index], board.world.quantum_action) ** 2
    clock = own_clock(board, books)
    for rate in books.declared.rates:
        if rate.leaves == books.part:
            span, directions = min(grain, rate.lifetime), rate.directions or (None,)
            emission, rest = hazard_weights(span, rate.lifetime, clock, board.world.node_clock, unit)
            weights = [emission] * len(directions) + [len(directions) * rest]
            pick, books.state = picked(board, books.state, books.declared.draw, weights, len(weights))
            if pick < len(directions):
                laid_at = drawn_node(board, books, share_weights(board, books))
                e, g = (levels_at(board, books, p)[:2] for p in (rate.leaves, rate.enters))
                lit = Item(rate.light, None, None, 1, (laid_at,), None, rate.resonance, rate.lifetime)
                light = replace(lit, width=rate.width, direction=directions[pick], levels=(e, g))
                written(board, exchange(board, books, rate.leaves, rate.enters) + [light])
                reported(board, books, (rate.enters, rate.leaves), (None, rate.light))
                return True
    return False


def absorbed(board: Lattice, closing: list[NodeBooks]) -> set[int]:
    """The absorptions drawn at the windows' end, one draw at a time per arriving family over every closing record's outcomes into it (ALGEBRA.md, The click writes on the lattice (f): the credit draws once over all the NodeDetectors that read one record, one quantum one click; the owner's word): the outcomes the transitions out of the part each record stands in reading that family, each weighted by its transition's own transfer share (`turned_labels`, `NodeBooks.shares`: the two-mode line's share of the record read at the body, nothing of another drive's transfer, never the composed label of a part several drives feed), the weights of the closing bodies brought to one denominator, the least common multiple of their norms, each body's entered label squared scaled by the denominator over its own norm (ALGEBRA.md, The absorption, the draw (b): bodies of different counts read by their own transfer shares, a body of one count as before; `credit.Books.unabsorbed_in`), and the outcome that none takes weighted by the rest of the record's unabsorbed share (`credit.Books.unabsorbed`, the one quantity of the record's books the draw reads: the record's count in that denominator at its first draw, read in a later closing set's denominator by the division act, down by the weights of every window drawn null, dropped when a quantum passes into or out of the record, `written`; the rest the smaller of the unabsorbed share and the denominator less the weights drawn, floored at 0; where the weights sum above the denominator the rest is 0 and the quantum goes to one of the bodies in the proportion of their weights, (a)), so that where the readers of one record close at different intervals the later reader's share is read conditionally on the earlier windows' nulls, s_B over (1 - the sum of the earlier readers' shares) in the labels' unit, capped at the unit, the realised frequencies the one draw's, P(B) = s_B, and the count conserved, an absorption ending the record for every later reader (ALGEBRA.md, The click writes on the lattice (7), the mathematician's line; readers closing together, and a record of many quanta while its unabsorbed share stands above the unit, drawn bit for bit as before); the first closing record's generator; none while the arriving record's count stands at 0 in the books; the drawn outcome's list (`exchange`: the drive at -1 at that Node where the transition climbs in the declared order of parts and at +1, given back, where it descends, the record's part entered at +1 and left at -1); a record that took or gave back is done for the window; returns the records done."""
    done: set[int] = set()
    pairs = [(b, t) for b in closing for t in b.declared.transitions if t.leaves == b.part]
    for drive in sorted({t.drive for _books, t in pairs}):
        while board.credit.counts[drive] > 0:
            outcomes = [(b, t) for b, t in pairs if b.number not in done and t.drive == drive]
            if not outcomes:
                break
            norms = [sum(label * label for label in books.labels) for books, _transition in outcomes]
            unit, unabsorbed = board.credit.unabsorbed_in(drive, norms)
            scaled = zip(outcomes, norms, strict=True)
            weights = [b.shares[t] * division_forward(unit, norm, 0)[0] for (b, t), norm in scaled]
            first, weighted = closing[0], [*weights, max(min(unabsorbed, unit) - sum(weights), 0)]
            pick, first.state = picked(
                board, first.state, first.declared.draw, weighted, len(outcomes) + 1
            )
            if pick >= len(outcomes):
                board.credit.unabsorbed[drive] = unabsorbed - sum(weights)
                break
            books, transition = outcomes[pick]
            parts, up = (transition.enters, transition.leaves), transition.enters > transition.leaves
            written(board, exchange(board, books, transition.leaves, transition.enters, drive))
            reported(board, books, parts, (drive, None) if up else (None, drive))
            done.add(books.number)
    return done


def probe_arrived(books: NodeBooks, laid: set[tuple[int, Node]]) -> bool:
    """Whether a probe arrived at the body this interval: a lay at its Node (`laid_whole`, the world's schedule) of the family of one of its transitions of a part into itself; the window's close at the declared interval, no level read (ALGEBRA.md, The pulsed gate: the window bounded by the lays' schedule; the two hands)."""
    return any(
        t.leaves == t.enters and (t.drive, at) in laid
        for t in books.declared.transitions
        for at in books.nodes
    )


def probe_click(board: Lattice, books: NodeBooks) -> None:
    """The click at a probe's arrival, the body's window's close (ALGEBRA.md, The pulsed gate; the two hands): one draw of the act over the transitions out of the part the body stands in whose family's count stands, each turn at its own transfer share (`turned_labels`, `NodeBooks.shares`, the record's share at the body) and the probe's own at the part's label squared as the turns left it (the two-mode line's shares, sin^2 and cos^2 of the half window's turn): the probe's own, the transition of the part into itself, re-lays the body whole in that part, its list the part at the change 0 and no write on the probe's record (taken and given back at one interval and one Node, the fluorescence by name the probe's own wave continuing from that Node); a drive's takes the drive's quantum and exchanges the parts as every absorption does (the hole, the count down by one); the rest of the labels' unit is the null window, the body whole in its part (`null_window`); one click line for a click, `absorbed` the family read and `emitted` the probe's where it was given back; the body's own generator."""
    outcomes = [
        t
        for t in books.declared.transitions
        if t.leaves == books.part and board.credit.counts[t.drive] > 0
    ]
    weights = [books.shares.get(t, books.labels[t.enters] ** 2) for t in outcomes]
    rest = sum(label * label for label in books.labels) - sum(weights)
    weighted = [*weights, rest if rest > 0 else 0]
    pick, books.state = picked(board, books.state, books.declared.draw, weighted, len(outcomes) + 1)
    if pick < len(outcomes):
        absorbed = outcomes[pick]
        if absorbed.leaves == absorbed.enters:
            written(board, [Item(books.index, books.number, absorbed.leaves, 0, books.nodes)])
        else:
            written(board, exchange(board, books, absorbed.leaves, absorbed.enters, absorbed.drive))
        up, down = absorbed.enters >= absorbed.leaves, absorbed.enters <= absorbed.leaves
        traded = (absorbed.drive if up else None, absorbed.drive if down else None)
        reported(board, books, (absorbed.enters, absorbed.leaves), traded)
    elif len(books.counts) > 1:  # a record of one part reads none
        null_window(board, books)


def jumped(board: Lattice) -> None:
    """The records at Nodes that are NodeDetectors at the end of an interval: first the packets the world lays whole at this interval (`laid_whole`, the probe's lay at the body's Node by the schedule); then each record gathers the records arriving at its Node into its window's sums (`resonance.gathered`, the arriving level per drive family read once, `arriving`), one more interval elapsed and its own clock advanced (`node_detector.clock_advanced`); the window closes at its declared length, or, for a body with a probe among its transitions, at the interval of the probe's lay at its Node (`probe_arrived`: the window bounded by clicks, opened at the body's last write and closed at the probe's absorption, no level read; ALGEBRA.md, The pulsed gate, the two hands); at the close the window's turn of the labels (`turned_labels`, once per window, as W sub-turns with the carry) and the body's windows counted, then the draws and the writes, the emissions first record by record (`emitted`: at the window's close while a window stands, the grain the count of the window's lit intervals, `NodeBooks.lit`, at every interval in the dark, `dark`, the grain 1, the lifetime's hazard 1 / tau per interval either way; a dark interval at the window's close draws twice, the interval at its own grain and then, where none was given, the window's lit intervals at theirs, so every interval of the window enters exactly one draw's span and the summed hazard over a window is W / tau whatever its dark intervals, ALGEBRA.md, The dark; a window with no dark interval the length itself, bit for bit), then at a probe's close the body's own one draw over its outcomes (`probe_click`), at a declared window's the absorptions in one draw per arriving family over the records that gave none (`absorbed`), then the null window of every record of several parts that neither gave nor took (`null_window`; a record of one part reads no part of itself and has none; a record converted whole is drawn after the records' clicks, src/event_universe/conversion.py), every write the one act's (`click`); the windows begun again."""
    laid_whole(board)
    laid = {(whole.family, whole.at) for whole in board.world.wholes if whole.interval == board.interval}
    for books in board.credit.bodies:
        levels = {t.drive: arriving(board, books, t.drive) for t in books.declared.transitions}
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
    closed, lit_numbers = {books.number for books in closing}, set()
    for books in board.credit.bodies:
        if books.declared.draw is None:
            continue
        lit = not dark(board, books)
        books.lit += lit
        spans = ([] if lit else [1]) + ([books.lit] if books.number in closed and books.lit else [])
        if any(emitted(board, books, span) for span in spans):
            lit_numbers.add(books.number)
    quiet = [books for books in closing if books.number not in lit_numbers]
    read = {books.number for books in quiet if probe_arrived(books, laid)}
    for books in quiet:
        if books.number in read:
            probe_click(board, books)
    done = absorbed(board, [books for books in quiet if books.number not in read])
    for books in quiet:
        if books.number not in read | done and len(books.counts) > 1:  # a record of one part reads none
            null_window(board, books)
    for books in closing:
        books.elapsed, books.lit, books.intake = 0, 0, {}
