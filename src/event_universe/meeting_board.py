"""The board reads itself (ALGEBRA.md, The board reads itself, the owner's word of 2026-10-24, the fold; beside Matter's birth from light, whose clause "a birth at every Node by the rule alone with no draw" this module enters): on a world that declares nothing (`World.seed`, `loader/seed.seed_of`) the torus is the law's own region, every Node of it, the way the open faces' layer is the board's own region `face` (loader/world.layer_of), and no NodeDetector object stands per Node: at the end of every interval, after the readers' acts, the board reads its seed family's share at every Node once (`Lattice.share_of`, one vectorised reading of the record, the count the record's share) and, Node by Node in the lattice's x-major order, where two whole quanta stand, the floor of the share over the record's unit W_rec at or above 2, the gapless meeting is there and the pair is born: the two quanta taken from the record at that Node by the hole there, every line of the seed's record at the Node to the state of a Node with no level through the one lay act (`lay.laid`, logged for the run back; the owner's word of 2026-10-24, 04:2x UTC, everything local: the new clause beside the undepleted beam's, ALGEBRA.md, The board reads itself, the old kept by name), the Node's own quanta paying, and the heaviest conjugate pair whose two walls fit within the two quanta's own energy, the light's share read at that Node, laid there at the senses -1 and 1 (`act.born_table` over `conversion.birth_of`'s tables, the law's sentence of 2026-10-24, the owner's word of 05:2x UTC; the former clause, the lightest within the top's threshold, 2026-10-23 to 2026-10-24), and where no pair's walls fit the Node is no meeting, its light standing untaken and no whether drawn, one meeting per Node per interval, the Node's one write; where one whole quantum stands with a share above it, the second quantum is the click's whether, the remainder below one quantum drawn against the unit by the Node's read of itself and its Links (the owner's word of 2026-10-24, 04:2x UTC, everything local: `digits.read_of` over every family of quanta at the Node and its six neighbours, one Link, as a body detector reads at its Nodes and within one Link, Rule3's kept remainders as the digits of one number, `features/click.drawn_from`, one read per Node that draws), and where that read finds every digit at the lay's origin the Node does not draw, the floor alone (the exact dark's precedent, `digits.at_origin`); a Node whose clock is frozen is not read and births nothing, every other Node read as itself; no count summed over the board caps or orders the births (the former cap, the books' count of the seed family read as the share summed over the lattice, was the one non-local act of the folded world, found by the architect's tile test of 2026-10-24, two slabs with skewed clocks equal to the bit before the meeting and apart at it; removed the same day): every Node with two whole quanta births, its own hole paying, the meetings read once before any write so that no Node's hole enters another's reading, and the family's count in the books is afterwards a reading of the board, the share summed (`credit.count_of`), never an act's input; each birth writes the click's line (`reports.credit`, the reader the Node's x-major index, an integer, since the board names no detector and the Node is the write's place) and the birth line beside it (`reports.birth_line`); every lay logged in the books at its interval for the run back as every act's lay is."""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

import numpy as np

from event_universe import credit, records
from event_universe.act import Alternative, born_table, click
from event_universe.core.rule3 import division_forward
from event_universe.digits import at_origin, read_of
from event_universe.features.click import drawn_from
from event_universe.features.front import ball
from event_universe.lay import laid
from event_universe.loader.keys import Node
from event_universe.reports import birth_line
from event_universe.reports import credit as credit_line
from event_universe.take import Item

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Table = tuple[tuple[int, int], ...]


def child_of(board: Lattice, index: int, share: int, whole: int) -> Table | None:
    """The pair two quanta of the seed family make at one Node: the heaviest conjugate pair whose two walls fit within the two quanta's own energy, two `whole`-ths of the share `share` read at the Node (`act.born_table`, the law's sentence of 2026-10-24; None where no pair's walls fit there)."""
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


def closed(board: Lattice) -> None:
    """The board's own close at the end of an interval: the meetings read, the whether drawn, the pairs born, the lines written (the module's sentence)."""
    index = board.world.seed
    if index is None:
        return
    books = board.credit
    shares, frozen = board.share_of(index)
    unit, family = books.units[index], board.families[index]
    span = records.record_slice(family, 0)
    for at, whole, rest in meetings(board, index, shares, frozen):
        table = child_of(board, index, int(shares[at]), whole)
        if table is None:  # no pair's walls within the two quanta's energy there: nothing born
            continue
        meet = whole >= 2
        if not meet and rest > 0:  # one whole quantum and a share above it: the second is the whether
            label = (
                f"the Node {list(at)}'s read of itself and its Links at the interval {board.interval}"
            )
            region = ball(board.shape, [at], 1, board.world.periodic)  # the Node and its six neighbours
            reads = [(family, region) for family in board.order]
            if not at_origin(board, reads):
                number, moduli = read_of(board, reads, label)
                meet = drawn_from(number, [rest, unit - rest], label, moduli)[0] == 0
        if not meet:
            continue
        here = board.mask((at,))  # the hole: the seed's record at this Node to 0, the two quanta paying
        for number in range(span.start, span.stop):
            line = board.states[index].lines[number]
            change = (np.where(here, -line.now, 0), np.where(here, -line.before, 0))
            laid(board, index, number, change, None, None, here)
        items = []
        for out, sense in table:
            den = board.families[out].pair[1]
            items.append(Item(out, None, None, 1, (at,), (den, den), sense=sense))
        click(board, None, [Alternative(1, partial(list, items))])
        if board.output is not None:
            names = [board.families[out].name for out, _sense in table]
            seed = board.families[index].name
            place = int(np.ravel_multi_index(at, board.shape))
            window = [board.interval, board.interval]
            board.output(
                credit_line(
                    board.interval,
                    seed,
                    place,
                    window,
                    0,
                    0,
                    names[0],
                    None,
                    1,
                    None,
                    None,
                    seed,
                    names[0],
                )
            )
            board.output(
                birth_line(board.interval, seed, names, [sense for _out, sense in table], (at,))
            )
    counted = credit.count_of(
        board, index
    )  # the family's count a reading of the board, never an act's input
    if counted is not None:
        books.counts[index] = counted
