"""The click's read of the board (ALGEBRA.md, The click's read of the board; the owner's words: the board is deterministic, the click is the only instrument that reads it, and the new draw is built from the remainders and Rule3 only): at a detector's draw Rule3's kept remainders of the records the detector reads, one per line per Node in [0, w), at the detector's Nodes (a region detector its region's Nodes, a body detector the body's Nodes) are read as the digits of one number, read and never written (`digits_of`, the one realisation of the order `loader/draw.DIGIT_ORDER`, one declared constant; `read_of`, the number by `features/click.read_number`), and every draw of the close is one division act on it (`features/click.drawn_from`, called by `node_detector.credit_draw`, `node_detector.picked` and `node_detector.drawn_node`). A remainder lies on the digits' lattice, F = gcd(w, D_i, R_ij) at the Node, every one on w div 2 + F Z (`lattice_of`), so the digit is the remainder's index on its lattice, r div F, one of w div F values, in the base w div F + 1, one above the count so that no total built of the wall's primes divides the base and every digit enters the draw's residue (the remainders themselves as digits in the base w would leave the residue on a total T dividing w to the last remainder alone, confined to the classes of gcd(F, T): the conversion's draw at the weights [span, rate - span] one outcome for ever); the read is refused by name where every digit lies on the lattice of the exact vacuum paces, three values each, and where every digit stands at the lay's origin, nothing read; no generator, no seed and no number of the run born outside the world file and Rule3."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from math import gcd
from typing import TYPE_CHECKING

import numpy as np

from event_universe import node
from event_universe.core.rule3 import Rule, division_forward, wall_of
from event_universe.features.click import read_number
from event_universe.loader.derived import quanta_records

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


def digits_of(board: Lattice, index: int, at: np.ndarray) -> Iterator[tuple[int, int, int]]:
    """One family's digits at the Nodes the mask `at` names, in the order `loader/draw.DIGIT_ORDER`, the one realisation of that order: every record of quanta of the family in its order (`loader/derived.quanta_records`; a holder of the sign its one record, light's free row, `Lattice.lines_of`), the digits' lattice F at the Nodes from Rule3's integers of the record's read (`lattice_of`), then every line of the record in the declared order and each line's kept remainder at the Nodes in the lattice's index order; one triple per digit, the remainder, its Node's F and the family's wall w, Python's integers, the arrays read and never written."""
    family, gamma, unit = board.families[index], board.world.node_clock, board.unit
    wall = wall_of(family.pair[1], gamma, unit)
    for record in quanta_records(board.families, index):
        rule = node.rule_of(family, gamma, *board.read(index, 1, record), unit)
        lattice = lattice_of(rule, at)
        for line in board.lines_of(index, record):
            kept = [int(remainder) for remainder in np.asarray(line.remainder)[at]]
            for remainder, found in zip(kept, lattice, strict=True):
                yield remainder, found, int(wall)


def lattice_of(rule: Rule, at: np.ndarray) -> list[int]:
    """The digits' lattice at the Nodes `at` names, in the lattice's index order: F = gcd(w, D_i, R_ij over the six Ports) from Rule3's integers at the Node (`node.rule_of`), Euclid's gcd on the rule's coefficients once (kind D in the acts table); the law's line gives r' = r + S_t (mod w) with S_t a sum of multiples of the reaches and the mass, and every line is born at w div 2, so a digit lies on w div 2 + F Z and takes w div F values: w div 3 for light at the exact vacuum paces (every R_ij = w div 3 and D_i = 0 at p_0 = p_i = Gamma with no tension: three values, the lattice the read is refused on, `read_of`), 2 Gamma^2 G^2 gcd(num, 3 den) for any pair there, and 3,072,000 = 2 num G^2 on the shipped universes' content 60, 108,000,000 values per digit."""
    terms = [np.broadcast_to(np.asarray(value), at.shape)[at] for value in (rule.mass, *rule.reaches)]
    return [gcd(int(rule.wall), *(int(term[k]) for term in terms)) for k in range(int(at.sum()))]


def read_of(board: Lattice, families: Sequence[int], at: np.ndarray, label: str) -> int:
    """The click's read of the board at the Nodes `at` names, one integer (ALGEBRA.md, The click's read of the board): the remainders of the records of every family in `families` in that order (a region detector the record it reads; a body detector the arriving records, its transitions' drives, first and its own record after), each family's in the order `DIGIT_ORDER` (`digits_of`, the remainder with its Node's lattice F and the family's wall), each read as its index on the lattice, r div F (one division act per digit), as one number in the mixed radix of the bases w div F + 1 (`features/click.read_number`; the base one above the digit's count of values, so that a total T of the wall's primes never divides it and every digit enters the residue); read at the draw's moment, the close before that click's write, and never written, so the run back and the inverse stand as they are. Refused by name, `label` naming the detector and the interval: every remainder at the lay's origin w div 2 (the records untouched at the Nodes read, or an exactly periodic standing record returned to its origin: nothing to read), and every digit on the lattice of the exact vacuum paces, at most three values each (3 F at or above w: light's remainders at p_0 = p_i = Gamma with no tension; a record read for its digits reads a content, the shipped universes' 60)."""
    digits, bases, origin, coarse = [], [], True, True
    for index in families:
        half = board.half_wall(index)
        for remainder, found, wall in digits_of(board, index, at):
            origin = origin and remainder == half
            coarse = coarse and 3 * found >= wall
            digits.append(division_forward(remainder, found, 0)[0])  # the index on the lattice
            bases.append(division_forward(wall, found, 0)[0] + 1)  # one above w div F
    if origin:
        raise RuntimeError(
            f"the click's read of the board at {label} finds every digit at the lay's origin w div 2: the "
            "records stand untouched at the Nodes read, nothing to read; a draw asked there is refused"
        )
    if coarse:
        raise RuntimeError(
            f"the click's read of the board at {label} finds every digit on the lattice of the exact vacuum "
            "paces, at most three values each (gcd(w, D_i, R_ij) at or above w div 3: light's remainders at "
            "p_0 = p_i = Gamma with no tension); the number cannot spread over the weights' total, so the read "
            "is refused: a record read for its digits reads a content, the paces off the exact band"
        )
    return read_number(digits, bases)
