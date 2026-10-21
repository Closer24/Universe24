"""The click's read of the board (ALGEBRA.md, The click's read of the board; the owner's words: the board is deterministic, the click is the only instrument that reads it, and the new draw is built from the remainders and Rule3 only): at a detector's draw Rule3's kept remainders of the records the detector reads, one per line per Node in [0, w), at the detector's Nodes (a region detector its region's Nodes, a body detector the body's Nodes) are read as the digits of one number, read and never written (`digits_of`, the one realisation of the order `loader/draw.DIGIT_ORDER`, one declared constant; `read_of`, the number by `features/click.read_number`), and every draw of the close is one division act on it (`features/click.drawn_from`, called by `node_detector.credit_draw`, `node_detector.picked` and `node_detector.drawn_node`). A record's lines laid alike carry one remainder at every Node, equal before the write and complementary after it; the read takes each Node's distinct digits once (the reader's D2 of 2026-10-20: a remainder equal to an earlier line's at the same Node of the record, or w less it, is a copy and enters neither the number nor its bits). A remainder lies on the digits' lattice, F = gcd(w, D_i, R_ij) at the Node, and on a turned plane gcd(w, D_i, R_ij, R^c_ij, R^s_ij), the Link pairs the step reads (2026-10-21, the reader's ruling on issue #2169), every one on w div 2 + F Z (`lattice_of`), so the digit is the remainder's index on its lattice, r div F, one of w div F values, in the base w div F + 1, one above the count so that no total built of the wall's primes divides the base and every digit enters the draw's residue (the remainders themselves as digits in the base w would leave the residue on a total T dividing w to the last remainder alone, confined to the classes of gcd(F, T): the conversion's draw at the weights [span, rate - span] one outcome for ever); the read is refused by name where every digit lies on the lattice of the exact vacuum paces, three values each, and where every digit stands at the lay's origin, nothing read; no generator, no seed and no number of the run born outside the world file and Rule3."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from math import gcd
from typing import TYPE_CHECKING

import numpy as np

from event_universe import flux, node
from event_universe.core.rule3 import Rule, division_forward, wall_of
from event_universe.features.click import read_number
from event_universe.features.front import ball
from event_universe.loader.derived import quanta_records

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Reads = Sequence[tuple[int, np.ndarray]]  # what a detector reads: each family with the mask of its Nodes


def digits_of(
    board: Lattice, index: int, at: np.ndarray
) -> Iterator[tuple[int, int, int, tuple[int, int]]]:
    """One family's digits at the Nodes the mask `at` names, in the order `loader/draw.DIGIT_ORDER`, the one realisation of that order: every record of quanta of the family in its order (`loader/derived.quanta_records`; a holder of the sign its one record, light's free row, `Lattice.lines_of`), the digits' lattice F at the Nodes from Rule3's integers of the record's read and, where the record is turned or folded, the Link pairs its step reads (`lattice_of`, `flux.pairs_of` at the same read, None for a plain record), then every line of the record in the declared order and each line's kept remainder at the Nodes in the lattice's index order; per digit the remainder, its Node's F, the family's wall w and its place, the record and the Node's index in the lattice's order (the copies' comparison, `read_of`), Python's integers, the arrays read and never written."""
    family, gamma, unit = board.families[index], board.world.node_clock, board.unit
    wall = wall_of(family.pair[1], gamma, unit)
    for record in quanta_records(board.families, index):
        content, factors = board.read(index, 1, record)
        rule = node.rule_of(family, gamma, content, factors, unit)
        families, states, amplitude = board.families, board.states, board.amplitude
        pairs = flux.pairs_of(
            index, families, states, 1, board.wrap, gamma, content, factors, record, amplitude
        )
        lattice = lattice_of(rule, at, pairs)
        for line in board.lines_of(index, record):
            kept = [int(remainder) for remainder in np.asarray(line.remainder)[at]]
            for place, (remainder, found) in enumerate(zip(kept, lattice, strict=True)):
                yield remainder, found, int(wall), (record, place)


def reads_of(board: Lattice, families: Sequence[int], at: np.ndarray) -> list[tuple[int, np.ndarray]]:
    """What a body reads (ALGEBRA.md, What a body reads, the reader's G2 of 2026-10-20): each of `families` (its drives, then its own record, `node_detector.read_families`) at the body's Nodes `at` and at the Nodes within one Link of them (`features/front.ball`, the Link metric with the wrap) where that family's record stands off the lay's origin, a remainder other than w div 2 on one of its lines: the light standing beside the body and the well's region the body's own record fills; a record at the origin beside the body adds no digit (a constant digit carries no entropy), each Node's distinct digits once (`read_of`), the digits of this interval alone; no key, no number, nothing at the Node."""
    centres = [(int(a), int(b), int(c)) for a, b, c in np.argwhere(at)]
    near = ball(board.shape, centres, 1, board.world.periodic)
    found = []
    for index in families:
        half, standing = board.half_wall(index), np.zeros(board.shape, dtype=bool)
        for record in quanta_records(board.families, index):
            for line in board.lines_of(index, record):
                standing |= np.asarray(line.remainder) != half
        found.append((index, at | (near & standing)))
    return found


def at_origin(board: Lattice, reads: Reads) -> bool:
    """Whether every digit the read would take stands at the lay's origin w div 2 (the digits of `digits_of` over `reads`, each family at its Nodes): the condition `read_of` refuses on, read here without a refusal for the emission's draw alone (ALGEBRA.md, the exact dark: a body whose read finds every digit at the lay's origin at its emission's draw does not draw; its emission falls at its window's close; where light stands at the body the emission's hazard is read from the board; `meeting.emission_drawn`)."""
    return all(
        remainder == board.half_wall(index)
        for index, at in reads
        for remainder, _found, _wall, _place in digits_of(board, index, at)
    )


def lattice_of(rule: Rule, at: np.ndarray, pairs: flux.Pairs | None = None) -> list[int]:
    """The digits' lattice at the Nodes `at` names, in the lattice's index order: F = gcd(w, D_i, R_ij over the six Ports) from Rule3's integers at the Node (`node.rule_of`) and, where the record is turned or folded, the Link pairs' R^c_ij and R^s_ij over the six Ports beside them (`pairs`, the pairs the step reads, `flux.pairs_of`, (R^c, R^s) = p_i^2 (X^c, X^s) per Port; None for a plain record, the plain reaches alone), Euclid's gcd on the line's coefficients once (kind D in the acts table); the law's line gives r' = r + S_t (mod w) with S_t a sum of multiples of the line's terms and the mass, the plain reaches on a plain line and the pairs' products on a turned one (ALGEBRA.md, The flux form on a turned or folded Link; the reader's ruling of 2026-10-21 on issue #2169: the plain reaches alone gave the hydrogen electron w div 9, nine values, where its remainders walk on w div 2 + T Z, T = p_i^2 at the vacuum paces, 9,216,000 values per digit), and every line is born at w div 2, so a digit lies on w div 2 + F Z and takes w div F values: w div 3 for light at the exact vacuum paces (every R_ij = w div 3 and D_i = 0 at p_0 = p_i = Gamma with no tension: three values, the lattice the read is refused on, `read_of`), 2 Gamma^2 G^2 gcd(num, 3 den) for any plain pair there, and 3,072,000 = 2 num G^2 on the shipped universes' content 60, 108,000,000 values per digit."""
    read = (
        (rule.mass, *rule.reaches) if pairs is None else (rule.mass, *rule.reaches, *pairs[0], *pairs[1])
    )
    terms = [np.broadcast_to(np.asarray(value), at.shape)[at] for value in read]
    return [gcd(int(rule.wall), *(int(term[k]) for term in terms)) for k in range(int(at.sum()))]


def read_of(board: Lattice, reads: Reads, label: str) -> tuple[int, tuple[int, int]]:
    """The click's read of the board, one integer (ALGEBRA.md, The click's read of the board): the remainders of the records of every family in `reads` in that order, each at the Nodes its mask names (a region detector the record it reads at its region; a body detector the arriving records, its transitions' drives, first and its own record after, at its Nodes and within one Link where each stands, `reads_of`), each family's in the order `DIGIT_ORDER` (`digits_of`, the remainder with its Node's lattice F and the family's wall), each read as its index on the lattice, r div F (one division act per digit), as one number in the mixed radix of the bases w div F + 1 (`features/click.read_number`; the base one above the digit's count of values, so that a total T of the wall's primes never divides it and every digit enters the residue); a remainder equal to an earlier line's at the same Node of the record, or w less it, is a copy and enters neither the number nor its bits (the reader's D2 of 2026-10-20: a record's lines laid alike carry one remainder at every Node, equal before the write and complementary after it; the read takes each Node's distinct digits once; a record whose lines differ keeps every digit), one comparison per later line and no act; returned with the number's two moduli for its first draw, the gcd of the bases less one after the first digit's (the residue modulo a factor of it the digits' plain sum) and the last digit's base (modulo a factor of it the last digit alone; `features/click.drawn_from`, the reader's D4); read at the draw's moment, the close before that click's write, and never written, so the run back and the inverse stand as they are. Refused by name, `label` naming the detector and the interval: every remainder at the lay's origin w div 2 (the records untouched at the Nodes read, or an exactly periodic standing record returned to its origin: nothing to read), and every digit on the lattice of the exact vacuum paces, at most three values each (3 F at or above w: light's remainders at p_0 = p_i = Gamma with no tension; a record read for its digits reads a content, the shipped universes' 60)."""
    digits, bases, origin, coarse = [], [], True, True
    for index, at in reads:
        half, earlier = board.half_wall(index), dict[tuple[int, int], list[int]]()
        for remainder, found, wall, place in digits_of(board, index, at):
            origin = origin and remainder == half
            coarse = coarse and 3 * found >= wall
            standing = earlier.setdefault(place, [])
            copied = any(remainder in (kept, wall - kept) for kept in standing)
            standing.append(remainder)
            if copied:  # an earlier line's remainder at the Node, or w less it: a copy, read once
                continue
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
    summed = gcd(*(base - 1 for base in bases[1:])) if len(bases) > 1 else 1  # the plain sum's modulus
    return read_number(digits, bases), (summed, bases[-1])
