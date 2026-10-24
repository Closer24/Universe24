"""The click's read of the board (ALGEBRA.md, The click's read of the board; the owner's words: the board is deterministic, the click is the only instrument that reads it, and the new draw is built from the remainders and Rule3 only; the owner's rule of 2026-10-24: the click reads the Node and its six neighbours only, nothing of the board's labels, so the digits stand in the Node's own frame, the Node first and then its six Ports in the Port order, `frame_of`, and a roll of the torus or a cut into tiles changes no draw; the branch digit-order): at a detector's draw Rule3's kept remainders of the records the detector reads, one per line per Node in [0, w), at the detector's Nodes (a region detector its region's Nodes, a body detector the body's Nodes) are read as the digits of one number, read and never written (`digits_of`, the one realisation of the order `loader/draw.DIGIT_ORDER`, one declared constant; `read_of`, the number by `features/click.read_number`), and every draw of the close is one division act on it (`features/click.drawn_from`, called by `node_detector.credit_draw`, `node_detector.picked` and `node_detector.drawn_node`). A record's lines laid alike carry one remainder at every Node, equal before the write and complementary after it; the read takes each Node's distinct digits once (the reader's D2 of 2026-10-20: a remainder equal to an earlier line's at the same Node of the record, or w less it, is a copy and enters neither the number nor its bits). A remainder lies on the digits' lattice, F = gcd(w, D_i, R_ij) at the Node, and on a turned plane gcd(w, D_i, R_ij, R^c_ij, R^s_ij), the Link pairs the step reads (2026-10-21, the reader's ruling on issue #2169), every one on w div 2 + F Z (`lattice_of`), so the digit is the remainder's index on its lattice, r div F, one of w div F values, in the base w div F + 1, one above the count so that no total built of the wall's primes divides the base and every digit enters the draw's residue (the remainders themselves as digits in the base w would leave the residue on a total T dividing w to the last remainder alone, confined to the classes of gcd(F, T): the conversion's draw at the weights [span, rate - span] one outcome for ever); the read is refused by name where every digit lies on the lattice of the exact vacuum paces, three values each, and where every digit stands at the lay's origin, nothing read; no generator, no seed and no number of the run born outside the world file and Rule3."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from math import gcd
from typing import TYPE_CHECKING, Any, cast

import numpy as np

from event_universe import flux, node, registry
from event_universe.core.ports import AXES
from event_universe.core.rule3 import Rule, division_forward, wall_of
from event_universe.features.click import read_number
from event_universe.features.read import READS, read_again

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Node = tuple[int, int, int]
Frame = Sequence[
    Node
]  # the Nodes a read takes, in the reader's own order: the Node first, then its six Ports
Reads = Sequence[
    tuple[int, Frame]
]  # what a reader reads: each family at the Nodes of its frame, in the frame's order
VACUUM_VALUES = AXES  # the exact vacuum paces' count of values per digit, the axes' count (ALGEBRA.md, The click's read of the board: at the vacuum paces the six Ports' reaches and the mass sum to SIDES w, the massless point's mass 0, so each reach is w div AXES, the digit lattice F = gcd(w, 0, w div AXES) = w div AXES and the digit has AXES values, three; the clause of 2026-10-24, a digit lattice at or above w div 3, three values or fewer, is the exact vacuum paces' and the read is refused there), the law's own count from the Ports' names and no number of the engine


def frame_of(at: Node, shape: tuple[int, int, int], periodic: Sequence[bool]) -> list[Node]:
    """The Node's own frame for its read: the Node first, then its six Ports in the Port order the law gives the Links (+x, -x, +y, -y, +z, -z; core/ports), each the Node beyond that Port with the torus's wrap, left out beyond an open face: nothing of the board's labels, so the same frame at every Node and under every roll."""
    found = [at]
    for axis in range(len(shape)):
        for side in (1, -1):
            there = list(at)
            there[axis] += side
            if 0 <= there[axis] < shape[axis]:
                found.append((there[0], there[1], there[2]))
            elif periodic[axis]:
                there[axis] = int(division_forward(there[axis], shape[axis], 0)[1])  # the wrap, an index
                found.append((there[0], there[1], there[2]))
    return found


def picked(value: Any, nodes: Frame) -> list[int]:
    """An integer per Node of the frame in the frame's order, from an array over the board or one integer for every Node."""
    array = np.asarray(value)
    return [int(array[node]) if array.ndim else int(array) for node in nodes]


def ruled(board: Lattice, index: int, record: int, content: Any, factors: node.Factors) -> Rule:
    """Rule3's integers of one record's read (`node.rule_of`), made once per interval on the very read and given again at every Node's frame of the close (features/read READS, `read_again`, keyed as `flux.pairs_of` is, the content and the factors the memoized read returned held by identity: the board's own read asks every record's rule at every meeting Node; the architect's economy of 2026-10-24)."""
    gamma, unit = board.world.node_clock, board.unit
    key = (ruled, index, record, gamma, unit)
    taken = (board.families, content, *(() if factors is None else tuple(factors)))
    if (kept := read_again(key, taken)) is not None:
        return cast(Rule, kept[0])
    rule = node.rule_of(board.families[index], gamma, content, factors, unit)
    READS[key] = (taken, (rule, []))
    return rule


def digits_of(board: Lattice, index: int, at: Frame) -> Iterator[tuple[int, int, int, tuple[int, int]]]:
    """One family's digits at the Nodes of the frame `at` in the frame's order (the reader's own: the Node first, then its six Ports in the Port order, `frame_of`; the lines outer in the record's declared order): every record of quanta of the family in its order (`loader/derived.quanta_records`; a holder of the sign its one record, light's free row, `Lattice.lines_of`), the digits' lattice F at the Nodes from Rule3's integers of the record's read and, where the record is turned or folded, the Link pairs its step reads (`lattice_of`, `flux.pairs_of` at the same read, None for a plain record), then every line of the record in the declared order and each line's kept remainder at the Nodes in the lattice's index order; per digit the remainder, its Node's F, the family's wall w and its place, the record and the Node's index in the lattice's order (the copies' comparison, `read_of`), Python's integers, the arrays read and never written."""
    family, gamma, unit = board.families[index], board.world.node_clock, board.unit
    wall = wall_of(family.pair[1], gamma, unit)
    for record in registry.quanta_records(board.families, board.states, index):
        content, factors = board.read(index, 1, record)
        rule = ruled(board, index, record, content, factors)
        families, states, amplitude = board.families, board.states, board.amplitude
        pairs = flux.pairs_of(
            index, families, states, 1, board.wrap, gamma, content, factors, record, amplitude
        )
        lattice = lattice_of(rule, at, pairs)
        for line in board.lines_of(index, record):
            kept = picked(line.remainder, at)
            for place, (remainder, found) in enumerate(zip(kept, lattice, strict=True)):
                yield remainder, found, int(wall), (record, place)


def at_origin(board: Lattice, reads: Reads) -> bool:
    """Whether every digit the read would take stands at the lay's origin w div 2 (the digits of `digits_of` over `reads`, each family at its Nodes): the condition `read_of` refuses on, read here without a refusal for the emission's draw alone (ALGEBRA.md, the exact dark: a body whose read finds every digit at the lay's origin at its emission's draw does not draw; The board reads itself: no draw where the Node's read finds every digit at the origin). A digit is its line's remainder at the Node over the lattice F, and the origin's digit is the remainder w div 2 whatever F, so the remainders alone are read here, the same records and the same Nodes as `digits_of` (every record of quanta of the family, `loader/derived.quanta_records`, every line of it, the frame's Nodes), and no rule, Link pair or lattice is made for a comparison that reads none of them (the economy of 2026-10-24, every answer the same)."""
    return all(
        int(remainder) == board.half_wall(index)
        for index, at in reads
        for record in registry.quanta_records(board.families, board.states, index)
        for line in board.lines_of(index, record)
        for remainder in picked(line.remainder, at)
    )


def lattice_of(rule: Rule, at: Frame, pairs: flux.Pairs | None = None) -> list[int]:
    """The digits' lattice at the Nodes of the frame `at`, in the frame's order: F = gcd(w, D_i, R_ij over the six Ports) from Rule3's integers at the Node (`node.rule_of`) and, where the record is turned or folded, the Link pairs' R^c_ij and R^s_ij over the six Ports beside them (`pairs`, the pairs the step reads, `flux.pairs_of`, (R^c, R^s) = p_i^2 (X^c, X^s) per Port; None for a plain record, the plain reaches alone), Euclid's gcd on the line's coefficients once (kind D in the acts table)."""
    read = (
        (rule.mass, *rule.reaches) if pairs is None else (rule.mass, *rule.reaches, *pairs[0], *pairs[1])
    )
    terms = [picked(value, at) for value in read]
    return [gcd(int(rule.wall), *(term[k] for term in terms)) for k in range(len(at))]


def read_of(board: Lattice, reads: Reads, label: str) -> tuple[int, tuple[int, int]]:
    """The click's read of the board, one integer (ALGEBRA.md, The click's read of the board): the remainders of the records of every family in `reads` in that order, each at the Nodes its mask names (a region detector the record it reads at its region; a body detector the arriving records, its transitions' drives, first and its own record after, at its Nodes and within one Link where each stands, `reads_of`), each family's in its frame's order (`digits_of`, `frame_of`, the remainder with its Node's lattice F and the family's wall), each read as its index on the lattice, r div F (one division act per digit), as one number in the mixed radix of the bases w div F + 1 (`features/click.read_number`; the base one above the digit's count of values, so that a total T of the wall's primes never divides it and every digit enters the residue); a remainder equal to an earlier line's at the same Node of the record, or w less it, is a copy and enters neither the number nor its bits (the reader's D2 of 2026-10-20: a record's lines laid alike carry one remainder at every Node, equal before the write and complementary after it; the read takes each Node's distinct digits once; a record whose lines differ keeps every digit), one comparison per later line and no act; returned with the number's two moduli for its first draw, the gcd of the bases less one after the first digit's (the residue modulo a factor of it the digits' plain sum) and the last digit's base (modulo a factor of it the last digit alone; `features/click.drawn_from`, the reader's D4); read at the draw's moment, the close before that click's write, and never written, so the run back and the inverse stand as they are. Refused by name, `label` naming the detector and the interval: every remainder at the lay's origin w div 2 (the records untouched at the Nodes read, or an exactly periodic standing record returned to its origin: nothing to read), and every digit on the lattice of the exact vacuum paces, three values or fewer each (w div F at or below `VACUUM_VALUES`, the lattice F at or above w div 3: the massless point's remainders at p_0 = p_i = Gamma with no tension; a record read for its digits reads a content, the shipped universes' 60)."""
    digits, bases, origin, coarse = [], [], True, True
    for index, at in reads:
        half, earlier = board.half_wall(index), dict[tuple[int, int], list[int]]()
        for remainder, found, wall, place in digits_of(board, index, at):
            values = int(division_forward(wall, found, 0)[0])  # w div F, the digit's count of values
            origin = origin and remainder == half
            coarse = coarse and values <= VACUUM_VALUES  # the exact vacuum paces, refused by name
            standing = earlier.setdefault(place, [])
            copied = any(remainder in (kept, wall - kept) for kept in standing)
            standing.append(remainder)
            if copied:  # an earlier line's remainder at the Node, or w less it: a copy, read once
                continue
            digits.append(division_forward(remainder, found, 0)[0])  # the index on the lattice
            bases.append(values + 1)  # one above w div F
    if origin:
        raise RuntimeError(
            f"the click's read of the board at {label} finds every digit at the lay's origin w div 2: the "
            "records stand untouched at the Nodes read, nothing to read; a draw asked there is refused"
        )
    if coarse:
        raise RuntimeError(
            f"the click's read of the board at {label} finds every digit on the lattice of the exact vacuum "
            "paces, three values or fewer each (the lattice F = gcd(w, D_i, R_ij) at or above w div 3: the massless "
            "point's remainders at p_0 = p_i = Gamma with no tension; ALGEBRA.md, The click's read of the board); "
            "the number cannot spread over the weights' total, so the read is refused: a record read for its "
            "digits reads a content, the paces off the exact band"
        )
    summed = gcd(*(base - 1 for base in bases[1:])) if len(bases) > 1 else 1  # the plain sum's modulus
    return read_number(digits, bases), (summed, bases[-1])
