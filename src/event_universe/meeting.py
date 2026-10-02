"""The meeting at a Node (ALGEBRA.md #the-click-is-the-meeting, The click writes on the GameBoard; HIGHLIGHTS.md, the owner's words of 2026-10-02 and 2026-10-03; the owner's word of 03:15 Israel, 2026-10-03, the click the heart): a detector is where the future met the past, the arriving record's quantum run forward from its root meeting at one Node the detector's own transition's quantum read back from the realised click, the click their meeting; a detector always receives two quanta, the arriving one and its own, a region detector's own quantum implicit in its declared window and whole, and for a record declared an instrument at one Node its record there; from the click the new future goes out, the quantum with the taker to its next meeting (the taker's record changed at its Node and stepped on by Rule3), the hole spreading from the entry Node, the giving's light quantum, and the arriving record's wave with its count at 0, the empty wave, stepped on and never credited. The seven steps in the Node's words (the Boss's sequence of 2026-10-03 with the advisor's and the mathematician's hands): 0, every interval every Node steps every record it holds by Rule3, a bijection, no draw; at the end of an instrument's window at the Node named, 1, the read, the two records at that Node, the arriving family's level there and the record present, the share their product at resonance (the two-mode line: the arriving level read into the record's phase at the transition's declared weight, the turn per proper interval, turning the two parts' labels into each other, the labels' squares the shares, the Rabi form); 2, the draw, with the declared seed and generator, once per window; 3, the write at that Node, one whole quantum passing between the two records there: the arriving record's levels and remainder to 0 (the hole) and its count in the books down by one, the present record's realised part laid at N + 1 at that Node in the direction of the part it leaves (the phase passing with the quantum), the remainder at the lay's origin, the part it leaves at N - 1 (the taking); 4, a window with no meeting at a Node whose record reads its own parts, the record laid again in the complement of its outcome set at its whole count (the null window, one function); 5, the giving, at a Node whose record stands in an upper part, drawn per window at the declared floor (the beat's current of a one-part record at one Node being 0, named): one whole quantum passing from that record to the light family's record at the same Node, the upper part to N - 1, the lower to N + 1, light's record up by one whole quantum laid at the born rotation, the resonance omega_e - omega_g (`features/click.born`); 6, after the write the Node and its neighbours step by Rule3, nothing written at any other Node, no front; 7, the jump line, the window, the instrument, the family and the parts, the Node a GameBoard diagnostic beside it. The record declared an instrument is one Node by the world's declaration (its six Link factors 0, `cut`, so that it stays, held by its declaration as the detector's region is), its books the instrument's own and at no Node; the Node knows no click."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import node
from event_universe.core import paces
from event_universe.core.ports import arrival
from event_universe.core.rule3 import division_forward
from event_universe.features import rotation
from event_universe.features.click import born, drawn, hole, standing
from event_universe.loader.derived import count_wall, row_of
from event_universe.loader.instrument import NodeInstrument, Rate, Transition
from event_universe.loader.keys import Node
from event_universe.loader.world import BodyRow
from event_universe.reports import jump

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
    """Every record of a family stepped by Rule3 in `direction` with the rule of its own read (`node.step_records`), the Links the world cuts at 0 among its factors (`cut`)."""
    gamma, unit, cuts = board.world.node_clock, board.unit, cut(board, index)
    return node.step_records(
        index, board.families, board.states, board.wrap, gamma, unit, direction, cuts
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
    """The lay of one part of the record at the instrument's one Node (features/click, `standing`; the owner's word of 2026-10-03, the body is at a Node; the mathematician's 174 (a) and (b)): the part's two lines at the Node set to the levels of `count` quanta of the family's pair standing there in the direction `phase` and the sense given, the level before the level now turned by the rest rotation, the remainder at the lay's origin, the half wall of the rule the record steps by; every other Node as it stands."""
    family, state = board.families[books.index], board.states[books.index]
    gamma, unit = board.world.node_clock, board.unit
    (re, im), (re_before, im_before) = standing(
        count, board.world.quantum_action, family.pair, phase, sense
    )
    origin = division_forward(node.rule_of(family, gamma, 0, None, unit)[2], 2, 0)[0]
    first, at = (
        node.record_slice(family, books.record).start + part * family.width,
        board.mask((books.at,)),
    )
    for number, (now, before) in zip(
        (first, first + 1), ((re, re_before), (im, im_before)), strict=True
    ):
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
    re, im = state.lines[first], state.lines[first + 1]
    return int(re.now[at]), int(im.now[at]), int(re.before[at]), int(im.before[at])


def exchanged(board: GameBoard, books: NodeBooks, leaves: int, enters: int) -> None:
    """The body's own half of the exchange at its Node (ALGEBRA.md, The click writes on the GameBoard (j), the jump; the advisor's clause 4 with the mathematician's 174): one quantum of the record's count moves from the part `leaves` to the part `enters`; the part it enters is laid at its new count in the direction of the part it leaves (the phase passes with the quantum), in that part's sense (the sign of its Wronskian), and the part it leaves is laid at its new count in its own direction; the books' part the one carrying the count, the labels' coherence ended, every part at its count in the count's units."""
    re, im, re_before, im_before = levels_at(board, books, leaves)
    sense = 1 if re * im_before - im * re_before >= 0 else -1
    books.counts[leaves] -= 1
    books.counts[enters] += 1
    relaid(board, books, enters, books.counts[enters], (re, im), sense)
    relaid(board, books, leaves, books.counts[leaves], (re, im), sense)
    books.part = max(range(len(books.counts)), key=lambda k: books.counts[k])
    wall = count_wall(board.families[books.index], board.world.quantum_action)
    books.labels = [count * wall for count in books.counts]


def node_draw(board: GameBoard, books: NodeBooks, weights: list[int]) -> int:
    """One draw of a record's own instrument by its declared generator (features/click, `drawn`), its state kept in its books."""
    assert books.declared.draw is not None
    found = books.declared.draw
    pick, books.state = drawn(
        books.state, found.multiplier, found.increment, board.world.width + 1, weights
    )
    return pick


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


def given(board: GameBoard, books: NodeBooks, rate: Rate) -> None:
    """The giving click at the instrument's Node (ALGEBRA.md, The click writes on the GameBoard (j), the fifth act; the advisor's clause 5; the mathematician's 174 (c), two hands): one whole quantum of light laid on the row of the family named at the instrument's Node, the levels of one quantum at the born rotation, the resonance omega_L = omega_e - omega_g of the two parts' pairs (`born`; the parts of one pair, whose rotation is 0, laid by the count alone, the two levels alike, and the share's difference T (sin omega_L - sin omega_e + sin omega_g) then 0), added to the row's first line (the free row, light's), its remainder at the lay's origin, the row's count in the books up by one; the record's quantum moved from the excited part to the lower (`exchanged`); one jump line."""
    light, state = board.families[rate.light], board.states[rate.light]
    gamma, unit, at = board.world.node_clock, board.unit, board.mask((books.at,))
    pair = born(
        board.families[books.index].pair, board.families[books.index].pair
    )  # one pair, the parts'
    (level, _im), (before, _im_before) = standing(1, board.world.quantum_action, pair, (1, 0), 1)
    origin = division_forward(node.rule_of(light, gamma, 0, None, unit)[2], 2, 0)[0]
    line = state.lines[0]
    state.lines[0] = node.Record(
        line.now + np.where(at, level, 0),
        line.before + np.where(at, before, 0),
        np.where(at, origin, line.remainder),
    )
    board.credit.counts[rate.light] += 1
    exchanged(board, books, rate.leaves, rate.enters)
    reported(board, books, rate.enters, rate.leaves, None, rate.light)


def taking(board: GameBoard, books: NodeBooks, transition: Transition) -> None:
    """The taking click at the instrument's Node, the exchange (the owner's word of 2026-10-03; ALGEBRA.md, The click writes on the GameBoard (b), (d) and (j)): the arriving record's levels and remainder at the Node set to 0 on every line of its record (`hole`, as the detector's write) and its count in the books down by one; the record's quantum moved from the part it stands in to the part the transition enters (`exchanged`); one jump line."""
    family, state, at = (
        board.families[transition.drive],
        board.states[transition.drive],
        board.mask((books.at,)),
    )
    for number, line in enumerate(state.lines[: family.record]):
        now, before, remainder = hole([line.now, line.before, line.remainder], at)
        state.lines[number] = node.Record(now, before, remainder)
    board.credit.counts[transition.drive] -= 1
    exchanged(board, books, transition.leaves, transition.enters)
    reported(board, books, transition.enters, transition.leaves, transition.drive, None)


def null_window(board: GameBoard, books: NodeBooks) -> None:
    """The window with no click (the owner's words of 2026-10-02, "Yes, both of them", and of 2026-10-03, "I approve the four things"; the mathematician's 148; the advisor's clause 8): the record's own reading of itself written at its one Node, the record laid again in the complement of its outcome set, the part it stands in, at its whole count, in that part's own direction and sense (the levels of what stands there within the lay's rounding, the remainder at the lay's origin), the parts' counts unchanged, and the labels' coherence ended, every part at its count in the count's units; one function, the act's one place."""
    re, im, re_before, im_before = levels_at(board, books, books.part)
    sense = 1 if re * im_before - im * re_before >= 0 else -1
    relaid(board, books, books.part, books.counts[books.part], (re, im), sense)
    wall = count_wall(board.families[books.index], board.world.quantum_action)
    books.labels = [count * wall for count in books.counts]


def reported(
    board: GameBoard, books: NodeBooks, realised: int, left: int, taken: int | None, light: int | None
) -> None:
    """The jump line of a record's click (`reports.jump`): the part realised and the part left by name, the family taken from or the family given to, the window, the one Node beside as a GameBoard diagnostic."""
    names, window = (
        books.declared.names,
        board.credit.window_of(board.tick) if False else [board.tick - books.elapsed, board.tick],
    )
    if board.observer is not None:
        families = board.families
        board.observer(
            jump(
                board.tick,
                families[books.index].name,
                books.number,
                window,
                names[realised],
                names[left],
                families[taken].name if taken is not None else None,
                families[light].name if light is not None else None,
                list(books.at),
            )
        )


def gave(board: GameBoard, books: NodeBooks) -> bool:
    """The giving drawn at a record's window's end (ALGEBRA.md, The click writes on the GameBoard (j), the fifth act): for the givings out of the part the record stands in, the weights the window against the lifetime's rest in the labels' unit (the count's measure squared, so that the generator's low bits, which cycle, decide nothing), the quantum given on the first drawn; True where one was."""
    assert books.declared.draw is not None
    window = books.declared.draw.window
    wall = count_wall(board.families[books.index], board.world.quantum_action)
    unit = wall * wall
    for rate in books.declared.rates:
        if rate.leaves == books.part:
            span = window if window <= rate.lifetime else rate.lifetime
            if node_draw(board, books, [span * unit, (rate.lifetime - span) * unit]) == 0:
                given(board, books, rate)
                return True
    return False


def took(board: GameBoard, closing: list[NodeBooks]) -> set[int]:
    """The takings drawn at the windows' end, one draw at a time per arriving family over every closing record's outcomes into it (ALGEBRA.md, The click writes on the GameBoard (f): the credit draws once over all the instruments that read one record, so one quantum is one click, and a record of several quanta is drawn from quantum by quantum as the detector's credit draws N; the paper's S.57): the outcomes the transitions out of the parts the records stand in, each weighted by its record's label squared (the two-mode line's share), and the outcome that none takes weighted by the rest of the count's unit; the draw with the first closing record's generator; the record drawn takes (`taking`) and takes no more this window, the draw repeated while the arriving record's count stands above 0 in the books and a record has not taken, until none takes; returns the records' numbers that took."""
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
            pick = node_draw(board, closing[0], [*weights, rest if rest > 0 else 0])
            if pick >= len(outcomes):
                break
            books, transition = outcomes[pick]
            taking(board, books, transition)
            done.add(books.number)
    return done


def jumped(board: GameBoard) -> None:
    """The records at Nodes that are instruments at the end of an interval: each turned by the records arriving at its Node (`turned_labels`), one more interval elapsed, and at the windows' length the draws and the writes, the givings first record by record (`gave`), then the takings in one draw per arriving family over the records closing together (`took`), then the null window's write for every closing record that neither gave nor took (`null_window`), each window beginning again."""
    for books in board.credit.bodies:
        turned_labels(board, books)
        books.elapsed += 1
    closing = [
        books
        for books in board.credit.bodies
        if books.declared.draw is not None and books.elapsed == books.declared.draw.window
    ]
    quiet = [books for books in closing if not gave(board, books)]
    done = took(board, quiet)
    for books in quiet:
        if books.number not in done:
            null_window(board, books)
    for books in closing:
        books.elapsed = 0
