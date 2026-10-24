"""The board reads itself (ALGEBRA.md, The board reads itself, the owner's word of 2026-10-24, the fold; beside Matter's birth from light, whose clause "a birth at every Node by the rule alone with no draw" this module enters): on a world that declares nothing (`World.seed`, `loader/seed.seed_of`) the torus is the law's own region, every Node of it, the way the open faces' layer is the board's own region `face` (loader/world.layer_of), and no NodeDetector object stands per Node: at the end of every interval, after the readers' acts, the board reads its seed family's share at every Node once (`Lattice.share_of`, one vectorised reading of the record, the count the record's share) and, Node by Node in the lattice's x-major order, where two whole quanta stand, the floor of the share over the record's unit W_rec at or above 2, the gapless meeting is there and the pair is born: the two quanta taken from the record at that Node by the hole there, every line of the seed's record at the Node to the state of a Node with no level through the one lay act (`lay.laid`, logged for the run back; the owner's word of 2026-10-24, 04:2x UTC, everything local: the new clause beside the undepleted beam's, ALGEBRA.md, The board reads itself, the old kept by name), the Node's own quanta paying, and the heaviest conjugate pair whose two walls fit within the two quanta's own energy, the light's share read at that Node, laid there at the senses -1 and 1 (`act.born_table` over `conversion.birth_of`'s tables, the law's sentence of 2026-10-24, the owner's word of 05:2x UTC; the former clause, the lightest within the top's threshold, 2026-10-23 to 2026-10-24), and where no pair's walls fit the Node is no meeting, its light standing untaken and no whether drawn, one meeting per Node per interval, the Node's one write; where one whole quantum stands with a share above it, the second quantum is the click's whether, the remainder below one quantum drawn against the unit by the Node's read of itself and its Links (the owner's word of 2026-10-24, 04:2x UTC, everything local: `digits.read_of` over every family of quanta at the Node and its six neighbours, one Link, as a body detector reads at its Nodes and within one Link, Rule3's kept remainders as the digits of one number, `features/click.drawn_from`, one read per Node that draws), and where that read finds every digit at the lay's origin the Node does not draw, the floor alone (the exact dark's precedent, `digits.at_origin`); a Node whose clock is frozen is not read and births nothing, every other Node read as itself; no count summed over the board caps or orders the births (the former cap, the books' count of the seed family read as the share summed over the lattice, was the one non-local act of the folded world, found by the architect's tile test of 2026-10-24, two slabs with skewed clocks equal to the bit before the meeting and apart at it; removed the same day): every Node with two whole quanta births, its own hole paying, the meetings read once before any write so that no Node's hole enters another's reading, and the family's count in the books is afterwards a reading of the board, the share summed (`credit.count_of`), never an act's input; each birth writes the click's line (`reports.credit`, the reader the Node's x-major index, an integer, since the board names no detector and the Node is the write's place) and the birth line beside it (`reports.birth_line`); every lay logged in the books at its interval for the run back as every act's lay is."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

import numpy as np

from event_universe import credit, records, swap
from event_universe.act import born_items, born_table, click
from event_universe.core.paces import sine_den
from event_universe.core.rule3 import division_forward
from event_universe.digits import at_origin, frame_of, read_of
from event_universe.features.click import drawn_from
from event_universe.lay import laid
from event_universe.loader.keys import Node
from event_universe.readings import momentum_of
from event_universe.reports import READINGS, birth_line, point_of
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
    """The board's own close at the end of an interval: every meeting read and every whether drawn from the state the interval STARTED from (`begun`, the lines and the phase lines the step read, `swap.kept`: the law's rule that every act reads the interval's start, so the click's read is the step's own one Link and no second read of the neighbours after the step; the Node and its six Ports, nothing of the board's labels), then the pairs born and the lines written on the state the step left, every face read before any write (`act.click`, one act for every pair of the close), so that the order in which the Nodes are taken enters no number (the owner's rule of 2026-10-24: any Nodes in any order give the same board; the branch digit-order) (the module's sentence)."""
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
                    number, moduli = read_of(board, reads, label)
                    meet = drawn_from(number, [rest, unit - rest], label, moduli)[0] == 0
            if meet:
                born.append((at, table))
    finally:
        for state, (lines, phases) in zip(board.states, stepped, strict=True):
            state.lines, state.phases = lines, phases  # the write on the state the step left
    for at, _table in born:
        board.closes[at] += 1  # the Node's own close counted, the click's view's `windows`
    readings = {
        at: readings_at(board, begun, index, 0, at) for at, _table in born
    }  # the click's view read on the state the step left, before the hole (2026-10-24)
    items = []
    for at, table in born:  # every hole at its own Node, then one click act for every list born
        here = board.mask((at,))  # the hole: the seed's record at this Node to 0, the two quanta paying
        for number in range(span.start, span.stop):
            line = board.states[index].lines[number]
            change = (np.where(here, -line.now, 0), np.where(here, -line.before, 0))
            laid(board, index, number, change, None, None, here)
        items.extend(born_items(board.families, table, (at,)))  # one record per child (2026-10-24)
    click(board, items)
    for at, table in born:
        if board.output is not None:
            names = [board.families[out].name for out, _sense in table]
            seed = board.families[index].name
            place = int(np.ravel_multi_index(at, board.shape))
            window = [board.interval, board.interval]
            found, clock = readings[at]
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
                    fan=clock.fan,
                    recoil=clock.recoil,
                    readings=found,
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
                )
            )
    counted = credit.count_of(
        board, index
    )  # the family's count a reading of the board, never an act's input
    if counted is not None:
        books.counts[index] = counted


class Clock(NamedTuple):
    """The credit line's former keys read at the board's own click (the click's view, 2026-10-24; `reports.MOMENTUM`, `FAN`, `RECOIL`, `PROPER`, `WINDOWS`): the piece's p_a per axis, the record's P_a over the board, the recoil -p, the taker's own clock at the close in whole intervals, its count of its own closes."""

    momentum: list[int]
    fan: list[int]
    recoil: list[int]
    proper: int
    windows: int


def readings_at(
    board: Lattice, begun: swap.Kept, index: int, record: int, at: Node
) -> tuple[dict[str, object], Clock]:
    """The click's view at the credited Node, the six readings of the credit line (`reports.READINGS`; ALGEBRA.md, Readings and measurements, the click's view, 2026-10-24): the point, the credited record's cosine read from its lines' three levels around the step at the Node, the level before and the level now at the interval's start (`begun`) and the level the step left, as the reduced pair (num, den) (`reports.point_of`; one pair where every line reads the same, else the lines' pairs in order; None at a level now 0: a Node credited again reads no point, its level taken to 0 by the hole at its last close and standing so at the interval's start, the reading refused by name and no number, the beat None with it); the kind, the rank of the lines credited, the record's lines per part (one a real line, two a plane); the sense, the Wronskian's sign at the Node (0 for real lines); the support, the shell Node the credit left through, the hole's own Node here; the beat, W_rec of the point read, the quantum's own wall 3 T den sin omega = W_c sin omega, 3 T times the integer sine of the pair (`paces.sine_den`, `derived.count_wall` at the pair read; 0 at the uniform mode's double root, None where no point or a mode beyond the band); the identity, the record's family and index; and the credit line's former keys read here and no longer constants (the clicks derivation of 2026-10-24, sections 1a, 2 (v), 4 (a)): the momentum, the piece's p_a per axis read at the close from the record's lattice momentum terms at the credited Node over its share there, scaled to one credited count, p_a = P_a(region) x W_rec div (num x W(region)), one division (ALGEBRA.md, The lattice momentum, Part F; `readings.momentum_of`), the region the one Node: the unit the key carries is that formula's and not T sin k_a per Link, for a plane wave of the massless point's record the reading 2 T sin k / sin omega per quantum, the two-Link sum over the quantum's own sine (2 T exactly at k = 2 pi / 3 on the 3-cube, where sin k = sin omega: 73,512,000 / 1,021 = 72,000 at den 1,021, measured), and at one Node of a record that is no plane wave the ratio of the Node's two Link currents to its share there, which the law bounds by nothing (the hole seed at den 1,021: 0 at the hole, whose inflow is symmetric; 12.4 T along the one axis to the hole at its six neighbours at the close 3, opposite in sign across the hole; 20.1 T at the twelve edge Nodes at 4; 1.24 T at the eight corners at 5), with the fan, the record's P_a over the board at the close, and the recoil, -p owed to the giver (Part G; on the uniform seed every one 0 exactly, a reading and not null); the proper, the credited Node's own composed clock at the close in whole intervals, the Node's clock p_0 summed over the intervals since the start over Gamma (ALGEBRA.md, The paces compose; The clock near matter, the pace e^(-U) = (Gamma / X)^(1 / 4) at the Node; `Lattice.proper_count`), with the windows, the Node's count of its own closes (`Lattice.closes`). Readings and no act: nothing of the board moves here."""
    family = board.families[index]
    span = records.record_slice(family, record)
    where = (int(at[0]), int(at[1]), int(at[2]))
    points = [
        point_of(int(start.before[where]), int(start.now[where]), int(left.now[where]))
        for start, left in zip(begun[0][index][span], board.states[index].lines[span], strict=True)
    ]
    point: object = points[0] if all(found == points[0] for found in points) else points
    wronskian = records.wronskian(board.lines_of(index, record), family.plane)
    value = int(np.asarray(wronskian, dtype=object)[where]) if family.plane else 0
    beat = None
    if isinstance(point, tuple) and abs(point[0]) <= point[1]:
        beat = int(sine_den(abs(point[0]), point[1], 3 * board.world.quantum_action))
    found = (
        list(point) if isinstance(point, tuple) else point,
        family.width,
        0 if value == 0 else (1 if value > 0 else -1),
        list(where),
        beat,
        [index, record],
    )
    lines = board.lines_of(index, record)  # the state the step left
    num, unit, gamma = family.pair[0], board.credit.units[index], board.world.node_clock
    fan = list(momentum_of(num, lines, board.wrap))
    here = board.mask((where,))
    share = int(board.share_of(index, 1, here)[0][where])  # the record's share at the credited Node
    piece = [
        int(division_forward(term * unit, num * share, 0)[0]) if share else 0
        for term in momentum_of(num, lines, board.wrap, here)
    ]  # p_a = P_a(region) x W_rec div (num x W(region)), one division, Part F
    proper = int(division_forward(int(board.proper_count[where]), gamma, 0)[0])
    clock = Clock(piece, fan, [-term for term in piece], proper, int(board.closes[where]))
    return dict(zip(READINGS, found, strict=True)), clock
