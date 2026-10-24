"""The board reads itself (ALGEBRA.md, The board reads itself, the owner's word of 2026-10-24, the fold; beside Matter's birth from light, whose clause "a birth at every Node by the rule alone with no draw" this module enters): on a world that declares nothing (`World.seed`, `loader/derived.seed_of`) the torus is the law's own region, every Node of it, the way the open faces' layer is the board's own region `face` (loader/world.layer_of), and no NodeDetector object stands per Node: at the end of every interval, after the readers' acts, the board reads its seed family's share at every Node once (`Lattice.share_of`, one vectorised reading of the record, the count the record's share) and, Node by Node in the lattice's x-major order, where two whole quanta stand, the floor of the share over the record's unit W_rec at or above 2, the gapless meeting is there and the pair is born: the two quanta taken from the record at that Node by the law's one write (`act.written`: the hole where the record is local and whole there, the books alone where it is a beam, the undepleted beam, the deficit printed) and the lightest conjugate pair within the threshold laid at that Node at the senses -1 and 1 (`conversion.birth_of`, the threshold of `act.born_pair`, the two quanta's two walls carrying the pair's two walls), one meeting per Node per interval, the Node's one write; where one whole quantum stands with a share above it, the second quantum is the click's whether, the remainder below one quantum drawn against the unit by the click's read of the board (`digits.read_of` over every family of quanta at every Node of the board, Rule3's kept remainders as the digits of one number, `features/click.drawn_from`, the first draw of the close reading the board and every later draw one division act on the number left, as the regions' credit draws), and where that read finds every digit at the lay's origin the board does not draw, the floor alone (the exact dark's precedent, `digits.at_origin`); the count the board pays with is the books' count of the seed family, the lay's count less the quanta taken (ALGEBRA.md, The count on the board: the board's reading of the share walks with the paces, the walk, and the books' count is the count the law conserves), and the births leave the seed's record standing, a close birthing while the count after the pair stays above 0, so that a world seeded with N quanta of light births at most (N - 1) div 2 pairs (the record's count at 0 would begin its erasing front from the drawn Nodes, the law's clause for a spent record, `front.started`, and the board's own light is never spent: measured on the 5-cube with the count spent, the front erased the uniform light and the step's cost rose from 0.3 to 400 seconds per interval), and a close whose count pays for fewer meetings than Nodes carry them writes the first in the lattice's order (the lower index on a tie, the uniform board's read of itself finding every digit at the origin); each birth writes the click's line (`reports.credit`, the reader the Node's x-major index, an integer, since the board names no detector and the Node is the write's place) and the birth line beside it (`reports.birth_line`); every lay logged in the books at its interval for the run back as every act's lay is."""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

import numpy as np

from event_universe import conversion
from event_universe.act import Alternative, click
from event_universe.core.rule3 import division_forward
from event_universe.digits import at_origin, read_of
from event_universe.features.click import drawn_from
from event_universe.loader.derived import count_wall
from event_universe.loader.keys import Node
from event_universe.reports import birth_line
from event_universe.reports import credit as credit_line
from event_universe.take import Item

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Table = tuple[tuple[int, int], ...]


def child_of(board: Lattice, index: int) -> Table | None:
    """The pair two quanta of the seed family make at one Node: the lightest conjugate pair within the threshold (`conversion.birth_of`, the threshold of `act.born_pair`), None where the universe declares none."""
    action = board.world.quantum_action
    carried = 2 * count_wall(board.families[index], action)
    for table in conversion.birth_of(board.families, index):
        if 2 * count_wall(board.families[table[0][0]], action) <= carried:
            return table
    return None


def meetings(board: Lattice, index: int, shares: np.ndarray) -> list[tuple[Node, int, int]]:
    """Every Node in the lattice's order with a share of the seed family at or above one quantum: the Node, the whole quanta standing there (the floor of the share over the unit) and the remainder below the next."""
    unit, found = board.credit.units[index], []
    for at in np.ndindex(*board.shape):
        value = int(shares[at])
        if value < unit:
            continue
        whole, rest = division_forward(value, unit, 0)
        found.append(((int(at[0]), int(at[1]), int(at[2])), int(whole), int(rest)))
    return found


def closed(board: Lattice) -> None:
    """The board's own close at the end of an interval: the meetings read, the whether drawn, the pairs born, the lines written (the module's sentence)."""
    index = board.world.seed
    if index is None:
        return
    books, table = board.credit, child_of(board, index)
    if table is None:
        return
    shares, frozen = board.share_of(index)
    if frozen.any():
        return  # a frozen Node: the share is not read over the board, nothing is born
    unit, left = (
        books.units[index],
        books.counts[index],
    )  # the books' count: the lay's less the quanta taken
    label = f"the board's own read of {board.families[index].name!r} at the interval {board.interval}"
    region = np.ones(board.shape, dtype=bool)
    number: int | None = None
    moduli: tuple[int, int] | None = None
    read = False
    for at, whole, rest in meetings(board, index, shares):
        if left < 3:
            break  # the seed's last quantum stands: a spent record's front would erase the board's own light
        meet = whole >= 2
        if not meet and rest > 0:  # one whole quantum and a share above it: the second is the whether
            if not read:
                reads = [(family, region) for family in board.order]
                read = True
                if not at_origin(board, reads):
                    number, moduli = read_of(board, reads, label)
            if number is not None:
                pick, number = drawn_from(number, [rest, unit - rest], label, moduli)
                moduli, meet = None, pick == 0
        if not meet:
            continue
        items = [Item(index, None, None, -1, (at,)), Item(index, None, None, -1, (at,))]
        for out, sense in table:
            den = board.families[out].pair[1]
            items.append(Item(out, None, None, 1, (at,), (den, den), sense=sense))
        click(board, None, [Alternative(1, partial(list, items))])
        left -= 2
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
                    left,
                    None,
                    seed,
                    names[0],
                )
            )
            board.output(
                birth_line(board.interval, seed, names, [sense for _out, sense in table], (at,))
            )
