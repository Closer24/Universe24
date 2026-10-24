"""The board reads itself (ALGEBRA.md, The board reads itself, the owner's word of 2026-10-24, the fold; beside Matter's birth from light, whose clause "a birth at every Node by the rule alone with no draw" this module enters): on a world that declares nothing (`World.seed`, `loader/seed.seed_of`) the torus is the law's own region, every Node of it, the way the open faces' layer is the board's own region `face` (loader/world.layer_of), and no NodeDetector object stands per Node: at the end of every interval, after the readers' acts, the board reads its seed family's share at every Node once (`Lattice.share_of`, one vectorised reading of the record, the count the record's share) and, Node by Node in the lattice's x-major order, where two whole quanta stand, the floor of the share over the record's unit W_rec at or above 2, the gapless meeting is there and the pair is born: the two quanta taken from the record at that Node by the hole there, every line of the seed's record at the Node to the Node's own level before, twice, the drift stopped and the level kept (`stopped_at`; the Boss's ruling of 2026-10-24 on the bound-click hand's measurement, ALGEBRA.md, The board reads itself, the dated sentence: the quantum is the drift, the write stops it; the write to (0, 0), to 2026-10-24, kept by name: against the sea's drifted level, a gauge, it made light at the six Links and spent the sea to zero) through the one lay act (`lay.laid`, logged for the run back; the owner's word of 2026-10-24, 04:2x UTC, everything local: the new clause beside the undepleted beam's), the Node's own quanta paying, and the heaviest conjugate pair whose two walls fit within the two quanta's own energy, the light's share read at that Node, laid there at the senses -1 and 1 (`act.born_table` over `conversion.birth_of`'s tables, the law's sentence of 2026-10-24, the owner's word of 05:2x UTC; the former clause, the lightest within the top's threshold, 2026-10-23 to 2026-10-24), and where no pair's walls fit the Node is no meeting, its light standing untaken and no whether drawn, one meeting per Node per interval, the Node's one write; where one whole quantum stands with a share above it, the second quantum is the click's whether, the remainder below one quantum drawn against the unit by the Node's read of itself and its Links (the owner's word of 2026-10-24, 04:2x UTC, everything local: `digits.read_of` over every family of quanta at the Node and its six neighbours, one Link, as a body detector reads at its Nodes and within one Link, Rule3's kept remainders as the digits of one number, `features/click.drawn_from`, one read per Node that draws), and where that read finds every digit at the lay's origin the Node does not draw, the floor alone (the exact dark's precedent, `digits.at_origin`); a Node whose clock is frozen is not read and births nothing, every other Node read as itself; no count summed over the board caps or orders the births (the former cap, the books' count of the seed family read as the share summed over the lattice, was the one non-local act of the folded world, found by the architect's tile test of 2026-10-24, two slabs with skewed clocks equal to the bit before the meeting and apart at it; removed the same day): every Node with two whole quanta births, its own hole paying, the meetings read once before any write so that no Node's hole enters another's reading, and the family's count in the books is afterwards a reading of the board, the share summed (`credit.count_of`), never an act's input; each birth writes the click's line (`reports.credit`, the reader the Node's x-major index, an integer, since the board names no detector and the Node is the write's place) and the birth line beside it (`reports.birth_line`); every lay logged in the books at its interval for the run back as every act's lay is."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, NamedTuple, cast

import numpy as np

from event_universe import credit, records, share, swap, take
from event_universe.act import born_items, born_table, click
from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, arrival
from event_universe.core.rule3 import division_forward
from event_universe.digits import at_origin, frame_of, read_of
from event_universe.features.click import drawn_from
from event_universe.lay import laid
from event_universe.loader.derived import count_wall
from event_universe.loader.keys import Node
from event_universe.readings import momentum_of
from event_universe.reports import READINGS, birth_line, point_of, refused_line
from event_universe.reports import credit as credit_line

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Table = tuple[tuple[int, int], ...]


def child_of(board: Lattice, index: int, share: int, whole: int) -> Table | None:
    """The list two quanta of the seed family make at one Node: the heaviest exact list whose summed walls fit within the two quanta's own energy (N children, one record each, 2026-10-24), two `whole`-ths of the share `share` read at the Node (`act.born_table`, the law's sentence of 2026-10-24; None where no pair's walls fit there)."""
    return born_table(board.families, index, board.world.quantum_action, 2 * share, max(whole, 2))


def meetings(
    board: Lattice, index: int, shares: np.ndarray, frozen: np.ndarray
) -> list[tuple[Node, int, int]]:
    """Every Node, in the engine's x-major order (a convention of the file's coordinates and no sentence of the law), with a share of the seed family at or above one quantum and its own clock not frozen: the Node, the whole quanta standing there (the floor of the share over the unit) and the remainder below the next."""
    unit, found = board.credit.units[index], []
    for at in np.ndindex(*board.shape):
        value = int(shares[at])
        if value < unit or bool(frozen[at]):
            continue
        whole, rest = division_forward(value, unit, 0)
        found.append(((int(at[0]), int(at[1]), int(at[2])), int(whole), int(rest)))
    return found


def closed(board: Lattice, begun: swap.Kept) -> None:
    """The board's own close at the end of an interval: every meeting read and every whether drawn from the state the interval STARTED from (`begun`, the lines and the phase lines the step read, `swap.kept`: the law's rule that every act reads the interval's start, so the click's read is the step's own one Link and no second read of the neighbours after the step; the Node and its six Ports, nothing of the board's labels), then the pairs born and the lines written on the state the step left, every face read before any write (every hole's target, the Node's own level before, read before any hole is written, `stopped_at`; `act.click`, one act for every pair of the close), so that the order in which the Nodes are taken enters no number (the owner's rule of 2026-10-24: any Nodes in any order give the same board; the branch digit-order) (the module's sentence)."""
    index = board.world.seed
    if index is None:
        return
    books = board.credit
    unit, family = books.units[index], board.families[index]
    span = records.record_slice(family, 0)
    stepped = [(state.lines, state.phases) for state in board.states]
    for state, lines, phases in zip(board.states, begun[0], begun[2], strict=True):
        state.lines, state.phases = lines, phases  # the read on the interval's start
    try:
        shares, frozen = board.share_of(index)
        born: list[tuple[Node, Table]] = []
        for at, whole, rest in meetings(board, index, shares, frozen):
            table = child_of(board, index, int(shares[at]), whole)
            if table is None:  # no list's walls within the two quanta's energy there: nothing born
                continue
            meet = whole >= 2
            if (
                not meet and rest > 0
            ):  # one whole quantum and a share above it: the second is the whether
                label = f"the Node {list(at)}'s read of itself and its Links at the interval {board.interval}"
                region = frame_of(at, board.shape, board.world.periodic)  # the Node, then its six Ports
                reads = [(family, region) for family in board.order]
                if not at_origin(board, reads):
                    number = read_of(board, reads, label)  # one Link and one number (2026-10-24)
                    meet = (
                        drawn_from(number, [rest, unit - rest], label, True)[0] == 0
                    )  # the number divided by the unit once: the remainder the whether, the quotient the close's later draws' (kept for the pick where main's selector asks none)
            if meet:
                born.append((at, table))
    finally:
        for state, (lines, phases) in zip(board.states, stepped, strict=True):
            state.lines, state.phases = lines, phases  # the write on the state the step left
    takes: list[tuple[Node, Table, Take]] = []
    for at, table in born:  # every face read before any write, on the state the write acts on
        found = take_of(board, index, span, at, walls_of(board, table))
        refusal = refused_by(board, at, table, found)
        if refusal is not None:  # nothing born, nothing taken, the light standing
            if board.output is not None:
                board.output(refused_line(board.interval, family.name, at, *refusal))
            continue
        takes.append((at, table, found))
    for at, _table, _take in takes:
        board.closes[at] += 1  # the Node's own close counted, the click's view's `windows`
    readings = {
        at: readings_at(board, begun, index, 0, at) for at, _table, _take in takes
    }  # the click's view read before the hole (2026-10-24): the levels at the interval's start, the point's level after the Node's own step
    lines = list(board.states[index].lines[span])
    targets = [
        moved(lines, at, found.levels) for at, _table, found in takes
    ]  # every hole's lines read before any hole is written: the before kept, the now moved toward it by the take's levels
    items = []
    for (at, table, _found), target in zip(
        takes, targets, strict=True
    ):  # every hole at its own Node, then the click act
        here = board.mask((at,))
        for number, line, after in zip(range(span.start, span.stop), lines, target, strict=True):
            change = (np.where(here, after.now - line.now, 0), np.where(here, 0, 0))
            laid(board, index, number, change, None, None, here)
        items.extend(born_items(board.families, table, (at,)))  # one record per child (2026-10-24)
    click(board, items)
    for at, table, found in takes:
        if board.output is not None:
            names = [board.families[out].name for out, _sense in table]
            seed = board.families[index].name
            place = int(np.ravel_multi_index(at, board.shape))
            window = [board.interval, board.interval]
            readings_found, clock = readings[at]
            board.output(
                credit_line(
                    board.interval,
                    seed,
                    place,
                    window,
                    clock.proper,
                    clock.windows,
                    names[0],
                    None,
                    1,
                    None,
                    None,
                    seed,
                    names[0],
                    momentum=clock.momentum,
                    readings=readings_found,
                )
            )
            children = born_items(board.families, table, (at,))
            board.output(
                birth_line(
                    board.interval,
                    seed,
                    names,
                    [sense for _out, sense in table],
                    (at,),
                    [child.record for child in children],
                    [list(board.families[child.family].pair) for child in children],
                    (found.taken, found.walls, found.excess, found.step),
                )
            )
    counted = credit.count_of(
        board, index
    )  # the family's count a reading of the board, never an act's input
    if counted is not None:
        books.counts[index] = counted


class Take(NamedTuple):
    """The exact take at a born Node (ALGEBRA.md, The board reads itself, the hole's clause of 2026-10-24): the levels the Node's now is moved toward its before, the frame's seven shares' fall in the current's units (the taken), the children's walls summed (what the birth books), the take's remainder (the taken less the walls, below the last level's step where the hole is written; negative where the full stop cannot pay and the close is refused) and the last level's step (the fall's increment at the last level moved, 0 at a refused close)."""

    levels: int
    taken: int
    walls: int
    excess: int
    step: int


def walls_of(board: Lattice, table: Table) -> int:
    """What the birth books: the children's walls summed, SUM over the children of count_wall(child), 2 x 3 T sqrt(den^2 - num^2) for the pair of a point (`loader/derived.count_wall`, the record's unit W_rec; `act.list_walls` orders the lists by it), the amount the hole takes (the hole's clause of 2026-10-24)."""
    return sum(count_wall(board.families[out], board.world.quantum_action) for out, _sense in table)


def moved(lines: list[records.Record], at: Node, levels: int) -> list[records.Record]:
    """Every line of the seed's record with its now at the Node moved `levels` levels toward its before, the before kept, and no other Node touched (the hole's clause of 2026-10-24: the Node's before is kept and its now is moved toward its before, one level at a time); a line at its before already stands."""
    found = []
    for line in lines:
        now, before = int(line.now[at]), int(line.before[at])
        toward = 0 if now == before else (1 if before > now else -1)
        after = line.now.copy()
        after[at] = now + toward * min(levels, abs(now - before))
        found.append(replace(line, now=after))
    return found


def frame_shares(board: Lattice, index: int, lines: list[records.Record], at: Node) -> int:
    """The shares of the Node and its six neighbours summed, read by the share's own form (`share.family_share`, the conserved form's term at each Node over the Node's pace, the Links' products shared half and half) on the lines given, at the paces of the seed record's read on the state the write acts on, in the current's units."""
    family, gamma = board.families[index], board.world.node_clock
    content, factors = board.read(index, 1, 0)
    nodes = board.mask(tuple(frame_of(at, board.shape, board.world.periodic)))
    found = share.family_share(family, lines, gamma, content, factors, board.unit, nodes)
    return int(np.asarray(found, dtype=object).sum())


def take_of(board: Lattice, index: int, span: slice, at: Node, walls: int) -> Take:
    """The exact take, the hole as the write that takes what the birth books and nothing else (ALGEBRA.md, The board reads itself, the hole's clause of 2026-10-24, the builder's derivation on #2187): at the born Node the seed record's before is kept and its now is moved toward its before, one level at a time (`moved`), until the shares of the Node and its six neighbours, read by the share's own form on the state the write acts on (`frame_shares`), have fallen by the children's walls summed (`walls`); the first such level is the take's, the fall the taken, the fall less the walls the excess, below the last level's step, and the last level's step named with it; where the full stop (the now at the before) would take less than the walls, the Take carries the full stop's fall below the walls and the caller refuses the close by name (`refused_by`), nothing born and the light standing. The comparisons run level by level on the engine's own share function and no algebraic form is assumed (the builder's integer root of the quadratic, the same level, kept by name); the arrays are read and never written here, the hole written by the caller through the one lay act. Kept by name with their numbers, the forms before this one: the write to (0, 0), which against the sea's drifted level made light at the six Links, 7.68 quanta at the first close of the 3-cube, and spent the sea to exactly zero; the Node's own level before twice (`stopped_at`, the sentence of 2026-10-24 15:0x), which took 1.6 to 2.7 W_c for two booked at 1.526, the Links' part of the share following the level; the exact take's excess 0.0002 to 0.04 W_c per birth on the builder's three boards."""
    lines = list(board.states[index].lines[span])
    base = frame_shares(board, index, lines, at)
    distance = max(abs(int(line.now[at]) - int(line.before[at])) for line in lines)
    full = base - frame_shares(board, index, moved(lines, at, distance), at)
    if full < walls:
        return Take(distance, full, walls, full - walls, 0)
    previous = 0
    for levels in range(1, distance):
        taken = base - frame_shares(board, index, moved(lines, at, levels), at)
        if taken >= walls:
            return Take(levels, taken, walls, taken - walls, taken - previous)
        previous = taken
    return Take(distance, full, walls, full - walls, full - previous)


def refused_by(board: Lattice, at: Node, table: Table, found: Take) -> tuple[str, int, int] | None:
    """The close's refusal by name at a born Node, or None where the hole is written (ALGEBRA.md, The board reads itself, the hole's clause of 2026-10-24): the cause "lay" where a child's lay would be refused, the child family's share at the Node already above its unit by `take.below_quantum`'s own comparison on the state the write acts on (the Boss's default of 2026-10-24: a close whose children's lay would be refused births nothing and takes nothing, so that the books equal the board's charge by construction), with the share and the unit; the cause "stop" where the full stop would take less than the children's walls, with the take and the walls."""
    for child in born_items(board.families, table, (at,)):
        if at not in take.below_quantum(board, child):
            standing = int(board.share_of(child.family, 1, board.mask((at,)))[0][at])
            return "lay", standing, board.credit.units[child.family]
    if found.taken < found.walls:
        return "stop", found.taken, found.walls
    return None


def stopped_at(board: Lattice, index: int, number: int, at: Node) -> tuple[int, int]:
    """The hole's target on one line of the seed's record: the Node's own level before, twice (ALGEBRA.md, The board reads itself, the dated sentence of 2026-10-24 on the Boss's ruling over the bound-click hand's measurement: the quantum is the drift, the write stops it; The uniform seed is a lay: the massless uniform mode is a double root whose quantum is the drift now - before, the level itself a gauge). The write reads nothing but the Node's own two levels and keeps the level the Node had before this interval's drift: on the uniform sea it takes exactly the drift's quantum and moves nothing on the Links (the Link's product (n_i - n_j)(b_i - b_j) has the before-difference 0 there); between two holes written in one close the Link keeps its product at equal drift; at the seed it is the seed's own origin, (0, 0) at the Node whose level before is 0, so a hole at any later close on a uniform frame is the seed's kink exactly. Kept by name with their numbers (the forms measured before this one, 2026-10-24): the write to (0, 0), which against the sea's drifted level, a gauge no act reads, made light of the level squared at the six Links, 7.68 quanta at the first close of the 3-cube where the books took two, and spent the sea to zero within five closes; the six Ports' mean of both levels, which keeps the frame's own drift, the sea's quantum, and took 0.58 quanta at that close and nothing on a board at two whole quanta per Node, 1,227 births in 60 intervals on the 3-cube; and the six Ports' mean of the level before, twice, which took 2.09 at that close and made light at the Link between two adjacent holes each written to its own frame, 10 to 172 quanta per close at the 5-cube's closes 5 to 10, 405 births in 60 intervals, where this write makes none (131 births, the light never below 48 quanta)."""
    line = board.states[index].lines[number]
    level = int(line.before[at])
    return level, level


class Clock(NamedTuple):
    """The credit line's former keys read at the board's own click (the click's view, 2026-10-24; `reports.MOMENTUM`, `PROPER`, `WINDOWS`): the momentum, the frame's running cosine along each axis with the Link current's sign, [sign_a, num_a, den_a] per axis, None at a level now 0; the taker's own clock at the close in whole intervals; its count of its own closes. The fan and the recoil struck from the line on 2026-10-24: the fan read the record over the whole board and no click reads the board, the recoil was -p, redundant with the momentum."""

    momentum: object
    proper: int
    windows: int


def agreed(found: list[tuple[int, int] | None]) -> object:
    """One reading where every line of the record reads the same at the Node, else the lines' readings in order (the click's view's rule for a record of several lines, the point's and the momentum's): a pair as a list of two integers, None for a line at a level now 0."""
    first = found[0]
    if all(reading == first for reading in found):
        return None if first is None else list(first)
    return [None if reading is None else list(reading) for reading in found]


def readings_at(
    board: Lattice, begun: swap.Kept, index: int, record: int, at: Node
) -> tuple[dict[str, object], Clock]:
    """The click's view at the credited Node, the six readings of the credit line (`reports.READINGS`; ALGEBRA.md, Readings and measurements, the click's view, 2026-10-24): the point, the credited record's cosine read from its lines' three levels around the step at the Node, the level before and the level now at the interval's start (`begun`) and the level the step left, the Node's own step result, as the reduced pair (num, den) (`reports.point_of`; one pair where every line reads the same, else the lines' pairs in order, `agreed`; None at a level now 0: a Node credited again reads no point, its level taken to 0 by the hole at its last close and standing so at the interval's start, the reading refused by name and no number, the beat and the momentum None with it); the kind, the rank of the lines credited, the record's lines per part (one a real line, two a plane); the sense, the Wronskian's sign at the Node (0 for real lines); the support, the shell Node the credit left through, the hole's own Node here; the beat, W_rec of the point read, the quantum's own wall 3 T den sin omega = W_c sin omega, 3 T times the integer sine of the pair (`paces.sine_den`, `derived.count_wall` at the pair read; 0 at the uniform mode's double root, None where no point or a mode beyond the band); the identity, the record's family and index; and the credit line's former keys read here and no longer constants (the clicks derivation of 2026-10-24, sections 1a, 2 (v), 4 (a)): the momentum, the frame's running cosine along each axis, 2 cos k_a = (a_{+a} + a_{-a}) / a_i, with the Link current's sign, p_a = T sin k_a per Link (ALGEBRA.md, The lattice momentum, Part F): per axis [sign_a, num_a, den_a], (num_a, den_a) the reduced pair `point_of` reads along the axis from the Node's level now and its two neighbours' through the +a and -a Ports at the interval's start (`begun`, the frame the click reads, the Node and its six neighbours, the owner's rule of the local law; `core/ports.arrival`, the Node itself on a folded axis; the same convention as the point, den above 0, the lines' pairs in order where they differ, None for a line at a level now 0, the whole key None where the point is None), sign_a in {-1, 0, 1} the sign of the Node's two Link currents' antisymmetric term along the axis, F_(i, i-a) - F_(i, i+a) with F_ij = num (now_i before_j - before_i now_j) (`readings.momentum_of` at the one Node, `features/currents.momentum_terms`), read on the levels at the interval's start like every reading of the click (the owner's rule: every act and every reading of the click reads the Node and its six neighbours at the interval's start, so that the credit line, the record, reads the same on two tiles with skewed clocks, a reading of the neighbours' state after their step being a dependency the law does not grant; the Boss's ruling of 2026-10-24): the direction is the current at the interval's start, 0 where no current flows yet, the direction unread at that click; the cosine even in k, the current carrying the direction; bounded, |p_a| <= T wherever |num_a| <= den_a (a running wave along the axis), and |num_a| > den_a a pair outside the circle, no running wave along the axis, named by the reader as the point names a mode beyond the band (measured at den 1,021 on the 3-cube: the travelling plane wave of the massless record at k = 2 pi / 3 along x reads [1, -1, 2] on x and [0, 1, 1] on y and z on every credit of its step; the uniform sea [0, 1, 1] on every axis; on the hole seed the hole's own first credit [0, 5, 6] on every axis, its inflow symmetric, its six neighbours at the next close [0, 1, 2] on the axis to the hole, cos k = 1 / 2 with the sign 0 (nothing flows at the start, the inflow is the step's), and [0, 25, 26] on the two cross axes, the twelve edge Nodes at the close 4 [0, 714, 713] between two corners, outside the circle, and [0, 1, 2] on the other two axes, the eight corners at 5 [0, 1, 2] on every axis); the fan (the record's P_a over the whole board) and the recoil (-p) struck from the line on 2026-10-24, no click reading the board and the recoil redundant with the momentum; the proper, the credited Node's own composed clock at the close in whole intervals, the Node's clock p_0 summed over the intervals since the start over Gamma (ALGEBRA.md, The paces compose; The clock near matter, the pace e^(-U) = (Gamma / X)^(1 / 4) at the Node; `Lattice.proper_count`), with the windows, the Node's count of its own closes (`Lattice.closes`). Readings and no act: nothing of the board moves here."""
    family = board.families[index]
    span = records.record_slice(family, record)
    where = (int(at[0]), int(at[1]), int(at[2]))
    starts, lefts = begun[0][index][span], board.states[index].lines[span]
    point = agreed(
        [
            point_of(int(start.before[where]), int(start.now[where]), int(left.now[where]))
            for start, left in zip(starts, lefts, strict=True)
        ]
    )
    wronskian = records.wronskian(board.lines_of(index, record), family.plane)
    value = int(np.asarray(wronskian, dtype=object)[where]) if family.plane else 0
    beat = None
    if isinstance(point, list) and all(isinstance(v, int) for v in point) and abs(point[0]) <= point[1]:
        beat = int(sine_den(abs(point[0]), point[1], 3 * board.world.quantum_action))
    found = (
        point,
        family.width,
        0 if value == 0 else (1 if value > 0 else -1),
        list(where),
        beat,
        [index, record],
    )
    num, gamma = family.pair[0], board.world.node_clock
    terms = momentum_of(
        num, starts, board.mask((where,))
    )  # the Node's two Link currents along each axis at the interval's start, the direction
    frame = [
        agreed(
            [
                point_of(
                    int(arrival(start.now, axis, -1)[where]),
                    int(start.now[where]),
                    int(arrival(start.now, axis, 1)[where]),
                )
                for start in starts
            ]
        )
        for axis in range(AXES)
    ]  # the running cosine along each axis at the interval's start, the frame the click reads
    momentum: object = None
    if point is not None:
        momentum = [
            None
            if cosine is None
            else [0 if term == 0 else (1 if term > 0 else -1), *cast(list[object], cosine)]
            for term, cosine in zip(terms, frame, strict=True)
        ]
    proper = int(division_forward(int(board.proper_count[where]), gamma, 0)[0])
    return dict(zip(READINGS, found, strict=True)), Clock(momentum, proper, int(board.closes[where]))
