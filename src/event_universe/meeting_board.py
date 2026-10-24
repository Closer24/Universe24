"""The board reads itself (ALGEBRA.md, The board reads itself, the owner's word of 2026-10-24, the fold; beside Matter's birth from light, whose clause "a birth at every Node by the rule alone with no draw" this module enters): on a world that declares nothing (`World.seed`, `loader/seed.seed_of`) the torus is the law's own region, every Node of it, the way the open faces' layer is the board's own region `face` (loader/world.layer_of), and no NodeDetector object stands per Node: at the end of every interval, after the readers' acts, the board reads its seed family's share at every Node once (`Lattice.share_of`, one vectorised reading of the record, the count the record's share) and, Node by Node in the lattice's x-major order, where two whole quanta stand, the floor of the share over the record's unit W_rec at or above 2, the gapless meeting is there and the pair is born: the two quanta taken from the record at that Node by the hole there, every line of the seed's record at the Node to the Node's own level before, twice, the drift stopped and the level kept (`stopped_at`; the Boss's ruling of 2026-10-24 on the bound-click hand's measurement, ALGEBRA.md, The board reads itself, the dated sentence: the quantum is the drift, the write stops it; the write to (0, 0), to 2026-10-24, kept by name: against the sea's drifted level, a gauge, it made light at the six Links and spent the sea to zero) through the one lay act (`lay.laid`, logged for the run back; the owner's word of 2026-10-24, 04:2x UTC, everything local: the new clause beside the undepleted beam's), the Node's own quanta paying, and the heaviest conjugate pair whose two walls fit within the two quanta's own energy, the light's share read at that Node, laid there at the senses -1 and 1 (`act.born_table` over `conversion.birth_of`'s tables, the law's sentence of 2026-10-24, the owner's word of 05:2x UTC; the former clause, the lightest within the top's threshold, 2026-10-23 to 2026-10-24), and where no pair's walls fit the Node is no meeting, its light standing untaken and no whether drawn, one meeting per Node per interval, the Node's one write; where one whole quantum stands with a share above it, the second quantum is the click's whether, the remainder below one quantum drawn against the unit by the Node's read of itself and its Links (the owner's word of 2026-10-24, 04:2x UTC, everything local: `digits.read_of` over every family of quanta at the Node and its six neighbours, one Link, as a body detector reads at its Nodes and within one Link, Rule3's kept remainders as the digits of one number, `features/click.drawn_from`, one read per Node that draws), and where that read finds every digit at the lay's origin the Node does not draw, the floor alone (the exact dark's precedent, `digits.at_origin`); a Node whose clock is frozen is not read and births nothing, every other Node read as itself; no count summed over the board caps or orders the births (the former cap, the books' count of the seed family read as the share summed over the lattice, was the one non-local act of the folded world, found by the architect's tile test of 2026-10-24, two slabs with skewed clocks equal to the bit before the meeting and apart at it; removed the same day): every Node with two whole quanta births, its own hole paying, the meetings read once before any write so that no Node's hole enters another's reading, and the family's count in the books is afterwards a reading of the board, the share summed (`credit.count_of`), never an act's input; each birth writes the click's line (`reports.credit`, the reader the Node's x-major index, an integer, since the board names no detector and the Node is the write's place) and the birth line beside it (`reports.birth_line`); every lay logged in the books at its interval for the run back as every act's lay is."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, cast

import numpy as np

from event_universe import credit, records, swap, take
from event_universe.act import affordable, born_items, click
from event_universe.bound_body import bodies_closing
from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, arrival
from event_universe.core.rule3 import division_forward
from event_universe.digits import at_origin, frame_of, read_of
from event_universe.features.click import Refused, drawn_from
from event_universe.hole import Take, moved, take_of, walls_of
from event_universe.lay import laid
from event_universe.loader.keys import Node
from event_universe.readings import momentum_of
from event_universe.reports import (
    READINGS,
    REFUSED_LAY,
    REFUSED_ORIGIN,
    REFUSED_STOP,
    TAKE_KEYS,
    birth_line,
    point_of,
    refused_line,
)
from event_universe.reports import credit as credit_line
from event_universe.take import Item

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Table = tuple[tuple[int, int], ...]


def child_of(board: Lattice, index: int, share: int, whole: int) -> tuple[Table, ...]:
    """The lists two quanta of the seed family can afford at one Node (the birth's selector, 2026-10-24, 13:xx UTC): the lifts' conjugate pairs whose summed walls fit within the two quanta's own energy, two `whole`-ths of the share `share` read at the Node (`act.affordable`, lightest first; the former clause, the heaviest of them, `act.born_table`, kept by name); empty where no lift's walls fit there, the Node then no meeting."""
    return affordable(board.families, index, board.world.quantum_action, 2 * share, max(whole, 2))


def drawn_among(tables: tuple[Table, ...], left: int | None) -> Table | None:
    """The pick among the affordable lists at a meeting Node, the birth's selector (ALGEBRA.md, Matter's birth from light, the lifts' draw within the energy, 2026-10-24, 13:xx UTC, the pick from the quotient since 16:0x UTC on the Boss's order; The board reads itself; The click's read of the board, one Link and one number): one list is a certain draw and reads nothing (one alternative needs no reader); several are drawn at equal weights from `left`, THE QUOTIENT of the number the Node read by the unit, the read's one division act at every close (the remainder the whether where one whole quantum stands with a share above it, `features/click.drawn_from` in `closed`; the number div the unit where two or more whole quanta stand), the list at the quotient's residue modulo the candidates' count, one division act (`division_forward`; equal weights, so the residue is the index, the lower index on a tie as `drawn_from` places a residue on cumulative weights); None, nothing born at that Node this interval and its light standing, where no quotient stands: the read refused at the lay's origin, or the number below the unit (the quotient 0), the read's own refusals and nothing forced. The former pick (13:xx UTC to 16:0x UTC), from the number itself through the bias clause's moduli, kept by name: on the family-less board the untouched rows' constant digits stand after bases divisible by three, and the number's residue modulo three was one point of the three at 160 of 163 fresh reads (`digits.py`, the frozen pick named); the quotient's division by the unit mixes every digit."""
    if len(tables) == 1:
        return tables[0]
    if not left:
        return None
    return tables[int(division_forward(left, len(tables), 0)[1])]


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
    refusals: list[
        tuple[Node, str, int, int]
    ] = []  # the reads refused by name: logged lines, never a crash
    try:
        shares, frozen = board.share_of(index)
        born: list[tuple[Node, Table]] = []
        for at, whole, rest in meetings(board, index, shares, frozen):
            tables = child_of(board, index, int(shares[at]), whole)
            if not tables:  # no lift's walls within the two quanta's energy there: no meeting
                continue
            meet, left = whole >= 2, None
            label = (
                f"the Node {list(at)}'s read of itself and its Links at the interval {board.interval}"
            )
            if (
                not meet and rest > 0
            ):  # one whole quantum and a share above it: the second is the whether
                region = frame_of(at, board.shape, board.world.periodic)  # the Node, then its six Ports
                reads = [(family, region) for family in board.order]
                if at_origin(
                    board, reads
                ):  # every digit at the lay's origin: nothing to read, nothing born, a logged line
                    refusals.append((at, REFUSED_ORIGIN, board.half_wall(index), board.half_wall(index)))
                else:
                    try:
                        number = read_of(board, reads, label)  # one Link and one number (2026-10-24)
                        drawn, left = drawn_from(number, [rest, unit - rest], label, True)
                        meet = (
                            drawn == 0
                        )  # the number divided by the unit once: the remainder the whether, the quotient `left` the pick's
                    except (
                        Refused
                    ) as named:  # the read's or the draw's refusal by name: a logged line (2026-10-24)
                        refusals.append((at, named.cause, named.amount, named.bound))
            elif (
                meet and len(tables) > 1
            ):  # two or more whole quanta and several lifts: the number divided by the unit once, the quotient the pick's
                reads = [
                    (family, frame_of(at, board.shape, board.world.periodic)) for family in board.order
                ]
                if at_origin(board, reads):  # the Node does not draw: nothing born, its light standing
                    refusals.append((at, REFUSED_ORIGIN, board.half_wall(index), board.half_wall(index)))
                    continue
                try:
                    left = int(division_forward(read_of(board, reads, label), unit, 0)[0])
                except Refused as named:  # the read refused by name: a logged line, nothing born
                    refusals.append((at, named.cause, named.amount, named.bound))
                    continue
            table = drawn_among(tables, left) if meet else None
            if table is not None:
                born.append((at, table))
        bodies = bodies_closing(board, shares, frozen, {at for at, _table in born}, refusals)
    finally:
        for state, (lines, phases) in zip(board.states, stepped, strict=True):
            state.lines, state.phases = lines, phases  # the write on the state the step left
    takes: list[tuple[Node, Table, Take]] = []
    for at, table in born:  # every face read before any write, on the state the write acts on
        found = take_of(board, index, span, at, walls_of(board, table))
        refusal = refused_by(board, at, table, found)
        if refusal is not None:  # nothing born, nothing taken, the light standing
            refusals.append((at, *refusal))
            continue
        takes.append((at, table, found))
    clicks: list[
        tuple[int, int, Node, Take]
    ] = []  # the bound bodies' clicks: the light taken by the records' units, one take per Node
    at_node: dict[Node, list[tuple[int, int, int]]] = {}
    for k, r, at, unit_k in bodies:
        at_node.setdefault(at, []).append((k, r, unit_k))
    for at, standing in sorted(at_node.items()):  # every face read before any write
        found = take_of(board, index, span, at, sum(unit_k for _k, _r, unit_k in standing))
        if (
            found.taken < found.walls
        ):  # the full stop cannot pay the records' units summed: refused by name, the light standing
            refusals.append((at, REFUSED_STOP, found.taken, found.walls))
            continue
        clicks.extend((k, r, at, found) for k, r, _unit_k in standing)
    for at, _table, _take in takes:
        board.closes[at] += 1  # the Node's own close counted, the click's view's `windows`
    clicks.sort(
        key=lambda found: (found[2], found[0], found[1])
    )  # the emission order: the Node, then the record
    body_readings = {}
    for k, r, at, _found in clicks:
        board.closes[at] += (
            1  # the body's own close counted at its Node, each record's credit reading the count as it stands
        )
        body_readings[(k, r, at)] = readings_at(board, begun, k, r, at)
    readings = {
        at: readings_at(board, begun, index, 0, at) for at, _table, _take in takes
    }  # the click's view read before the hole (2026-10-24): the levels at the interval's start, the point's level after the Node's own step
    lines = list(board.states[index].lines[span])
    targets = (
        [moved(lines, at, found.levels) for at, _table, found in takes]
        + [moved(lines, at, found.levels) for at, found in holes_of(clicks)]
    )  # every hole's lines read before any hole is written: the before kept, the now moved toward it by the take's levels
    items = []
    for (at, table, _found), target in zip(
        takes, targets[: len(takes)], strict=True
    ):  # every hole at its own Node, then the click act
        here = board.mask((at,))
        for number, line, after in zip(range(span.start, span.stop), lines, target, strict=True):
            change = (np.where(here, after.now - line.now, 0), np.where(here, 0, 0))
            laid(board, index, number, change, None, None, here)
        items.extend(born_items(board.families, table, (at,)))  # one record per child (2026-10-24)
    for (at, _found), target in zip(
        holes_of(clicks), targets[len(takes) :], strict=True
    ):  # the bodies' click: the light holed once at the Node by the records' units summed
        here = board.mask((at,))
        for number, line, after in zip(range(span.start, span.stop), lines, target, strict=True):
            change = (np.where(here, after.now - line.now, 0), np.where(here, 0, 0))
            laid(board, index, number, change, None, None, here)
    for k, r, at, _found in clicks:  # the quantum into each record by the click act
        sense = int(
            np.sign(int(np.asarray(records.wronskian(board.lines_of(k, r), True), dtype=object)[at]))
        )
        den = board.families[k].pair[1]
        items.append(Item(k, 1, (at,), (den, den), sense=sense, record=r))
    click(board, items)
    if (
        board.output is not None
    ):  # the close's lines after its lays, Node by Node in the x-major order (the slabs runner's order of the board's lines, 2026-10-24): a refused Node its one line, a born Node its credit and its birth
        closes: dict[Node, list[dict[str, object]]] = {}
        for at, cause, amount, bound in refusals:
            closes[at] = [refused_line(board.interval, family.name, at, cause, amount, bound)]
        for at, table, found in takes:
            names = [board.families[out].name for out, _sense in table]
            seed = board.families[index].name
            place = int(np.ravel_multi_index(at, board.shape))
            window = [board.interval, board.interval]
            readings_found, clock = readings[at]
            children = born_items(board.families, table, (at,))
            closes[at] = [
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
                ),
                birth_line(
                    board.interval,
                    seed,
                    names,
                    [sense for _out, sense in table],
                    (at,),
                    [child.record for child in children],
                    [list(board.families[child.family].pair) for child in children],
                    (found.taken, found.walls, found.excess, found.step),
                ),
            ]
        for (
            k,
            r,
            at,
            found,
        ) in clicks:  # the credit the record's: its identity, proper, windows, point, kind, sense, support, beat and momentum
            readings_found, clock = body_readings[(k, r, at)]
            closes.setdefault(at, []).append(
                credit_line(
                    board.interval,
                    family.name,
                    int(np.ravel_multi_index(at, board.shape)),
                    [board.interval, board.interval],
                    clock.proper,
                    clock.windows,
                    board.families[k].name,
                    None,
                    1,
                    None,
                    None,
                    family.name,
                    board.families[k].name,
                    momentum=clock.momentum,
                    readings={
                        **readings_found,
                        **dict(
                            zip(
                                TAKE_KEYS,
                                (found.taken, found.walls, found.excess, found.step),
                                strict=True,
                            )
                        ),
                    },  # the body's take named on its credit as the birth's is on its line
                )
            )
        for at in sorted(closes):
            for entry in closes[at]:
                board.output(entry)
    counted = credit.count_of(
        board, index
    )  # the family's count a reading of the board, never an act's input
    if counted is not None:
        books.counts[index] = counted


def holes_of(clicks: list[tuple[int, int, Node, Take]]) -> list[tuple[Node, Take]]:
    """The bodies' holes, one per Node in the x-major order: a Node's clicks share its one take, their units summed, so its hole is written once."""
    found: dict[Node, Take] = {}
    for _k, _r, at, taken in clicks:
        found.setdefault(at, taken)
    return sorted(found.items())


def refused_by(board: Lattice, at: Node, table: Table, found: Take) -> tuple[str, int, int] | None:
    """The close's refusal by name at a born Node, or None where the hole is written (ALGEBRA.md, The board reads itself, the hole's clause of 2026-10-24): the cause "lay" where a child's lay would be refused, the child family's share at the Node already above its unit by `take.below_quantum`'s own comparison on the state the write acts on (the Boss's default of 2026-10-24: a close whose children's lay would be refused births nothing and takes nothing, so that the books equal the board's charge by construction), with the share and the unit; the cause "stop" where the full stop would take less than the children's walls, with the take and the walls."""
    for child in born_items(board.families, table, (at,)):
        if at not in take.below_quantum(board, child):
            standing = int(board.share_of(child.family, 1, board.mask((at,)))[0][at])
            return REFUSED_LAY, standing, board.credit.units[child.family]
    if found.taken < found.walls:
        return REFUSED_STOP, found.taken, found.walls
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
