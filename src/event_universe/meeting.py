"""The meeting at a Node (ALGEBRA.md #the-click-is-the-meeting, The click writes on the GameBoard; HIGHLIGHTS.md, the owner's words of 2026-10-02 and 2026-10-03; the owner's word of 03:15 Israel, 2026-10-03, the click the heart): a detector is where the future met the past, the arriving record's quantum run forward from its root meeting at one Node the detector's own transition's quantum read back from the realised click, the click their meeting; a detector always receives two quanta, the arriving one and its own, a region detector's own quantum implicit in its declared window and whole, and for a record declared an instrument at one Node its record there; from the click the new future goes out, the quantum with the taker to its next meeting (the taker's record changed at its Node and stepped on by Rule3), the hole spreading from the entry Node, the giving's light quantum, and the arriving record's wave with its count at 0, the empty wave, stepped on and never credited. The seven steps in the Node's words (the Boss's sequence of 2026-10-03 with the advisor's and the mathematician's hands): 0, every interval every Node steps every record it holds by Rule3, a bijection, no draw; at the end of an instrument's window at the Node named, 1, the read, the two records at that Node, the arriving family's level there and the record present, the share their product at resonance (the two-mode line: the arriving level read into the record's phase at the transition's declared weight, the turn per proper interval, turning the two parts' labels into each other, the labels' squares the shares, the Rabi form); 2, the draw, with the declared seed and generator, once per window; 3, the write at that Node, one whole quantum passing between the two records there: the arriving record's levels and remainder to 0 (the hole) and its count in the books down by one, the present record's realised part laid at N + 1 at that Node in the direction of the part it leaves (the phase passing with the quantum), the remainder at the lay's origin, the part it leaves at N - 1 (the taking); 4, a window with no meeting at a Node whose record reads its own parts, the record laid again in the complement of its outcome set at its whole count (the null window, one function); 5, the giving, at a Node whose record stands in an upper part, drawn per window at the declared floor (the beat's current of a one-part record at one Node being 0, named): one whole quantum passing from that record to the light family's record at the same Node, the upper part to N - 1, the lower to N + 1, light's record up by one whole quantum laid as a source in time at that Node over the giving's lifetime at the transition's declared resonance (`giving.given_quantum`); 6, after the write the Node and its neighbours step by Rule3, nothing written at any other Node, no front; 7, the jump line, the window, the instrument, the family and the parts, the Node a GameBoard diagnostic beside it. The record declared an instrument is one Node by the world's declaration (its six Link factors 0, `cut`, so that it stays, held by its declaration as the detector's region is), its books the instrument's own and at no Node; the Node knows no click."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import front, node
from event_universe.core import paces
from event_universe.core.ports import arrival
from event_universe.core.rule3 import division_forward
from event_universe.features import rotation
from event_universe.features.click import Face, drawn, laid_pairs, standing
from event_universe.giving import given_quantum, levels_of
from event_universe.loader.derived import count_wall, row_of
from event_universe.loader.instrument import Instrument, NodeInstrument
from event_universe.loader.keys import Node
from event_universe.loader.world import BodyRow
from event_universe.plane import Faces
from event_universe.reports import face, jump, lay

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard


@dataclass
class NodeBooks:
    """The books of a record at a Node that is an instrument, the instrument's own and at no Node (ALGEBRA.md, The click writes on the GameBoard (j) and (k); the owner's word of 2026-10-03, one thinks of a Node): the declaration's number among the world's `measured`, the record's family and its record number, its one Node at the file's coordinates, its declaration, the part the record stands in as its last write left it (its own transition read back, the past), its count per part, per part the two-mode line's amplitude in the count's units since its last write (the parts' coherence, turned by the arriving records' levels), the intervals elapsed in its window and its generator's state."""

    number: int
    index: int
    record: int
    at: Node
    declared: NodeInstrument
    part: int
    counts: list[int]
    labels: list[int]
    elapsed: int
    state: int


def books_of(board: GameBoard) -> list[NodeBooks]:
    """The books of every record declared an instrument at a Node, in the world's order: its number among `measured`, its family and record, its one Node, its declaration, the part carrying the count, the counts per part, the labels at their counts in the count's units, the window begun and the generator at the declared seed."""
    found = []
    for number, (record, row) in enumerate(board.laid_rows()):
        if not isinstance(row, BodyRow) or row.instrument is None or row.instrument.draw is None:
            continue
        parted = list(row.instrument.counts)
        wall = count_wall(board.families[row.family], board.world.quantum_action)
        part = max(range(len(parted)), key=lambda k: parted[k])
        labels = [count * wall for count in parted]
        at, seed = row.nodes[0], row.instrument.draw.seed
        found.append(
            NodeBooks(number, row.family, record, at, row.instrument, part, parted, labels, 0, seed)
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
    """The Links the world declares at the factor 0 for a family, per Port the mask of the Nodes whose Port faces them (ALGEBRA.md, The click writes on the GameBoard; the owner's word of 2026-10-03): the six Links of every Node at which a record of the family is laid in its parts (`loader/instrument.py`), read 0 from both ends so that the record stays at its Node, held by its declaration as the detector's region is; None where the world declares none."""
    nodes = tuple(
        row.nodes[0] for row in board.world.bodies if row.family == index and row.instrument is not None
    )
    if not nodes:
        return None
    at = board.mask(nodes)
    return tuple(
        at | arrival(at, axis, side, board.wrap, False) for axis in range(3) for side in (1, -1)
    )


def relaid(
    board: GameBoard, books: NodeBooks, part: int, count: int, phase: tuple[int, int], sense: int
) -> None:
    """The lay of one part of the record at the instrument's one Node (features/click, `standing`; the owner's word of 2026-10-03, the body is at a Node; the mathematician's 174 (a) and (b)): the part's two lines at the Node set to the levels of `count` quanta of the family's pair standing there in the direction `phase` and the sense given, the level before the level now turned by the rest rotation, the remainder at the lay's origin, the half wall of the rule the record steps by; every other Node as it stands. A record converted whole (its declaration's `conversions`, src/event_universe/conversion.py) is laid whole instead, every line of its record at the Node by the invariant at its declared sense (features/click, `laid_pairs`, the two hands' lay of 2026-10-03; at the count 0 every line 0, the hole), the phase its lay's own."""
    family, state = board.families[books.index], board.states[books.index]
    gamma, unit, action = board.world.node_clock, board.unit, board.world.quantum_action
    if books.declared.conversions:
        pairs = laid_pairs(count, action, family.pair, books.declared.sense, family.plane, family.laid)
    else:
        (re, im), (re_before, im_before) = standing(count, action, family.pair, phase, sense)
        pairs = [(re, re_before), (im, im_before)]
    origin = division_forward(node.rule_of(family, gamma, 0, None, unit)[2], 2, 0)[0]
    first = node.record_slice(family, books.record).start + part * family.width
    at = board.mask((books.at,))
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
    books = NodeBooks(number, row.family, record, row.nodes[0], row.instrument, 0, [], [], 0, 0)
    for part, count in enumerate(row.instrument.counts):
        relaid(board, books, part, count, (1, 0), 1)


def levels_at(board: GameBoard, books: NodeBooks, part: int) -> tuple[int, int, int, int]:
    """A part's levels at the instrument's Node, (re_now, im_now, re_before, im_before), read from its two lines."""
    family, state = board.families[books.index], board.states[books.index]
    first = node.record_slice(family, books.record).start + part * family.width
    at = tuple(np.add(books.at, board.offset))
    re, im = state.lines[first], state.lines[first + 1 if family.plane else first]
    return int(re.now[at]), int(im.now[at]), int(re.before[at]), int(im.before[at])


def arriving(board: GameBoard, books: NodeBooks, drive: int) -> int:
    """The arriving record's level at the instrument's Node: a holder of the sign's time level summed over every row but the record's own (`node.row_levels`, light), a family of quanta's first line's level now otherwise."""
    family, lines = board.families[drive], board.states[drive].lines
    at = tuple(np.add(books.at, board.offset))
    if family.wronskian:
        own = row_of(board.families, books.index, books.record)
        return int(np.asarray(node.row_levels(family, lines, 0, 1, own))[at])
    return int(lines[0].now[at])


def turned_labels(board: GameBoard, books: NodeBooks) -> None:
    """The two-mode line at the instrument's Node, one interval (ALGEBRA.md, The two-mode line; The click writes on the GameBoard (b), the share at resonance; the advisor's Omega = k_r ell / Gamma): for every transition out of the part the record stands in, the arriving record's level at the Node read into the record's phase at the weight the transition declares, the turn per proper interval (`node.turned_by`, the tangent half-angle over 2 Gamma), turns the two parts' labels into each other by the engine's own three shears (features/rotation), the turn's size added at the resonance the transition declares; the labels' squares are the parts' shares the window's draw reads, sin^2 of the accumulated turn, the Rabi form."""
    gamma = board.world.node_clock
    content = board.read(books.index, 1, books.record)[0]
    at = tuple(np.add(books.at, board.offset))
    clock = paces.clock_of(gamma, int(np.asarray(content)[at]) if np.ndim(content) else int(content))
    for transition in books.declared.transitions:
        if transition.leaves != books.part:
            continue
        level = transition.weight * arriving(board, books, transition.drive)
        turn = int(node.turned_by(level, clock, gamma))
        u, v = books.labels[transition.leaves], books.labels[transition.enters]
        u, v = rotation.turned(u, v, turn if turn >= 0 else -turn, 2 * gamma)
        books.labels[transition.leaves], books.labels[transition.enters] = int(u), int(v)


@dataclass(frozen=True)
class Item:
    """One entry of a click's list (the mathematician's 192 with the advisor's second, #1572 comment 5963391333, two hands; the owner's word of 2026-10-03, 03:22 Israel, one generic implementation the detector operates): the record by its family and, for a record declared an instrument at one Node, its number among `measured` (None for a record spread over the board), the part (None for every line of a spread record, no line alone), the change of its count, +1, -1 or 0 (the null window moves no count), the Nodes written at, the file's coordinates, and for a spread record given whole quanta the form of its lay (`giving.given_quantum`): the pair its lay stands at where the list names one (the conversion's records out at their family's massless pair [den, den], the lay by the count at one Node, the two hands of 2026-10-03, #1572 comments 5964520368 and 5964754600), else the resonance and the span of a source in time (the giving's, the transition's declared resonance and the lifetime, the mathematician's 213 (B) and 220 with the advisor's second, #1572 comments 5965054791 and 5965303134, #1563 comment 5965316267)."""

    family: int
    measured: int | None
    part: int | None
    delta: int
    nodes: tuple[Node, ...]
    pair: tuple[int, int] | None = None
    resonance: tuple[int, int] | None = None
    span: int = 0
    width: int | None = (
        None  # the open board's packet: its Nodes across (`giving.laid_packet`), None for the source in time
    )
    direction: tuple[int, int] | None = None  # the packet's drawn direction, the axis and its sense


Lists = list[list[Item]]  # the outcomes of one click, each the list written where it is drawn
Phase = tuple[tuple[int, int], int]  # a part's direction (re, im) and its sense, its Wronskian's sign


def click(
    board: GameBoard, state: int, generator: Instrument | None, weights: list[int], outcomes: Lists
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
    """The lines of a record an item lays at its Nodes: the lines of the part of a record declared an instrument at one Node (`parted`), the first line of a spread record given whole quanta (`given_quantum`), none for a quantum taken by the face."""
    if item.measured is None:
        return [0] if item.delta > 0 else []
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
    """A spread record's quantum taken at the Nodes named, the face (features/click, `Face`; ALGEBRA.md, The click writes on the GameBoard (b) and (d)): for every line of the record and every Node, one face at the next two intervals, the first Port preferred, so that Rule3 writes the level 0 and then the level before 0 with its own remainder; the record's count in the credit's books down by the item's change; nothing assigned at any Node."""
    lines, ticks = range(board.families[item.family].record), (board.tick + 1, board.tick + 2)
    for at, line, tick in itertools.product(item.nodes, lines, ticks):
        node_at = (int(at[0]), int(at[1]), int(at[2]))
        board.credit.faces.setdefault(tick, []).append(Face(item.family, line, node_at, 0, tick))
    board.credit.counts[item.family] += item.delta


def parted(board: GameBoard, books: NodeBooks, item: Item, phase: Phase | None) -> None:
    """One part of a record declared an instrument at one Node laid at its new count (`relaid`): in the direction and sense of the part the quantum leaves where the list names one (the phase passes with the quantum), in its own otherwise (a part laid again at its count, the null window)."""
    assert item.part is not None and item.nodes == (books.at,)
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


def exchange(books: NodeBooks, leaves: int, enters: int) -> list[Item]:
    """The record's own half of a click's list: one quantum of its count from the part `leaves` to the part `enters` at its Node."""
    return [
        Item(books.index, books.number, part, delta, (books.at,))
        for part, delta in ((enters, 1), (leaves, -1))
    ]


def null_window(board: GameBoard, books: NodeBooks) -> None:
    """The window with no click (the owner's words of 2026-10-02, "Yes, both of them", and of 2026-10-03, "I approve the four things"; the mathematician's 148; the advisor's clause 8): the record's own reading of itself written at its one Node, the one list of the act with the part it stands in at the change 0 (`click`): the record laid again in the complement of its outcome set, the part it stands in, at its whole count, in that part's own direction and sense (the levels of what stands there within the lay's rounding, the remainder at the lay's origin), the parts' counts unchanged, and the labels' coherence ended; where the re-lay changed a level, a write outside Rule3, one jump line labelled GAMEBOARD, the `lay` lines beside it carrying the levels before and after at the Node for the host's tool (a null window that changes nothing writes none); one function, the act's one place."""
    before = levels_at(board, books, books.part)
    click(board, books.state, None, [1], [[Item(books.index, books.number, books.part, 0, (books.at,))]])
    if levels_at(board, books, books.part) != before:  # a level changed: its line, the lay lines beside
        reported(board, books, (books.part, books.part), (None, None), False)


def reported(
    board: GameBoard,
    books: NodeBooks,
    parts: tuple[int, int],
    exchanged: tuple[int | None, int | None],
    quantum: bool = True,
) -> None:
    """The jump line of a record's click (`reports.jump`): the `parts` realised and left by name, the families `exchanged`, the one taken from and the one given to (None where none), the window's intervals [first, last], the one Node beside as a GameBoard diagnostic, labelled the detector's where a `quantum` passed and a diagnostic for the null window's write."""
    if board.observer is None:
        return
    names, families = books.declared.names, board.families
    window = [board.tick - books.elapsed + 1, board.tick]
    taken, light = (families[k].name if k is not None else None for k in exchanged)
    words = (names[parts[0]], names[parts[1]], taken, light)
    name, at = families[books.index].name, list(books.at)
    board.observer(jump(board.tick, name, books.number, window, *words, at, quantum))


def gave(board: GameBoard, books: NodeBooks) -> bool:
    """The giving drawn at a record's window's end (ALGEBRA.md, The click writes on the GameBoard (j), the fifth act; the advisor's clause 5; the mathematician's 174 (c), two hands): for the givings out of the part the record stands in, one draw of the act between the giving's list (the part at N - 1 and the lower at N + 1 at its Node, light's record at +1 there, laid as a source in time over the lifetime at the transition's declared resonance inside a guide, `giving.given_quantum`, or, in the open board, as a packet along a drawn direction, one list per direction the board holds, each at the giving's weight, the direction's draw the click's one draw with the record's own generator, an assumption by name, `giving.laid_packet`; `click`) and nothing, the weights the window against the lifetime's rest in the labels' unit (the declared floor; the beat's current of a one-part record at one Node is 0, so the floor alone is the rate), the record's own generator; the first giving drawn is taken and the window ends; one jump line."""
    assert books.declared.draw is not None
    window = books.declared.draw.window
    unit = count_wall(board.families[books.index], board.world.quantum_action) ** 2
    for rate in books.declared.rates:
        if rate.leaves == books.part:
            span = window if window <= rate.lifetime else rate.lifetime
            items = exchange(books, rate.leaves, rate.enters)
            given = Item(rate.light, None, None, 1, (books.at,), None, rate.resonance, rate.lifetime)
            outcomes = [
                items + [replace(given, width=rate.width, direction=direction)]
                for direction in (rate.directions or (None,))
            ]
            weights = [span * unit] * len(outcomes) + [len(outcomes) * (rate.lifetime - span) * unit]
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
                [Item(drive, None, None, -1, (books.at,)), *exchange(books, t.leaves, t.enters)]
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


def jumped(board: GameBoard) -> None:
    """The records at Nodes that are instruments at the end of an interval: each turned by the records arriving at its Node (`turned_labels`), one more interval elapsed, and at the windows' length the draws and the writes, the givings first record by record (`gave`), then the takings in one draw per arriving family over the records that gave none (`took`), then the null window of every record of several parts that neither gave nor took (`null_window`; a record of one part reads no part of itself and has none; a record converted whole is drawn after the jumps, src/event_universe/conversion.py), every write the one act's (`click`); the windows begun again."""
    for books in board.credit.bodies:
        turned_labels(board, books)
        books.elapsed += 1
    closing = [b for b in board.credit.bodies if b.declared.draw and b.elapsed == b.declared.draw.window]
    quiet = [books for books in closing if not gave(board, books)]
    done = took(board, quiet)
    for books in quiet:
        if books.number not in done and len(books.counts) > 1:  # a record of one part reads none
            null_window(board, books)
    for books in closing:
        books.elapsed = 0
