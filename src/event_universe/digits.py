"""The click's read of the board, one Link and one number (ALGEBRA.md, The click's read of the board, the dated sentence of 2026-10-24 on the builder's sentence posted on #2187, measured on the toy at the dens 1,021 and 1,105; the owner's words: the board is deterministic, the click is the only instrument that reads it, and the draw is built from the remainders and Rule3 only; the owner's word of 2026-10-24, keep the laws: the Node steps simply with Rule3 and the click produces everything, so nothing of this read enters the Node's step): at its close a Node reads, for every line of every record of quanta in the records' order, its own remainder as its index on its own lattice (F_i = gcd(w, D_i, R_ik, R^c_ik, R^s_ik) over its six Ports) and each neighbour's remainder as its index on the Link's lattice (F_ij = gcd(w, R_ji, R^c_ji, R^s_ji), the Link's own terms as the neighbour steps across it, a multiple of the neighbour's own F_j, so the coarse index, the floor of the fine one over the two lattices' ratio; `lattice_of`, the Port back across the Link by `ports_of` and `opposite`); a remainder equal to an earlier line's at the same Node of the record, or w less it, is a copy and enters nothing (the reader's D2 of 2026-10-20); the digits of the Node and its six Links, of every line and record, in the order of their values, one number in the mixed radix of the bases w div F + 1 (`read_of`, `features/click.read_number`; the builder's all-sorted composition of 2026-10-24, the sentence (A)'s order, the Node's digit first and the Link digits sorted per line in the records' order, kept by name); the number is divided by the unit once (`features/click.drawn_from`, called by `meeting_board.closed`), the remainder the whether where one is asked (against the rest and the unit less it) and the quotient the close's later draws'; refused where every digit stands at the lay's origin (`at_origin`, `read_of`) and where the number is below the unit (`drawn_from`); no Port order, no last base, and no digit erased from the pick, since no base is 0 modulo den and so no place value is 0 modulo the unit. The read reaches one Link by construction (a halo of one Link suffices: the two tiles with skewed clocks run the board bit for bit through the drawn whethers, tests/test_two_tiles_with_skewed_clocks_run_the_board.py) and is one function of the Node's read and the set of its six Links' reads (the board is the cube's 48, tests/test_the_board_is_the_cube_48.py). Kept by name, the read to 2026-10-24: the digits of the Node and its six Ports in the Port order (+x, -x, +y, -y, +z, -z; the owner's rule of 2026-10-24 that the click reads the Node and its six neighbours only and nothing of the board's labels, `frame_of`), each on its own Node's lattice F_j over that Node's six Ports, two Links from the drawing Node, with the read's two moduli, the bases less one and the last base, booked as the draw's bias bound; its three defects measured on the toy at den 1,021: the Port order a label the cube's 48 does not keep (the sea plus one at the origin breaks at the interval 4 under 40 of 47 elements), the two-Link reach parting the two tiles with one-Link halos at the closes 11 and 21 (the halo's own lattice takes the tile's wrap), and the frozen place values (a base 0 modulo 3 erasing every digit before it from a pick among three, the pick one point of the three at 160 of 163 fresh reads). A remainder lies on its lattice w div 2 + F Z since every term of its walk is a multiple of F (2026-10-21, the reader's ruling on issue #2169), so the digit is the remainder's index on its lattice, r div F, one of w div F values, in the base w div F + 1, one above the count so that no total built of the wall's primes divides the base; the read is refused by name as well where every digit lies on the lattice of the exact vacuum paces, three values each (the clause of 2026-10-24); no generator, no seed and no number of the run born outside the world file and Rule3; the arrays read and never written, so the run back and the inverse stand as they are."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from math import gcd
from typing import TYPE_CHECKING, Any, cast

import numpy as np

from event_universe import flux, node, registry
from event_universe.core.ports import AXES, PORT_SIDES
from event_universe.core.rule3 import Rule, division_forward, wall_of
from event_universe.features.click import read_number
from event_universe.features.read import READS, read_again

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Node = tuple[int, int, int]
Frame = Sequence[
    Node
]  # the Nodes a read takes: the Node first, then the Nodes beyond its Ports (`frame_of`)
Reads = Sequence[tuple[int, Frame]]  # what a reader reads: each family at the Nodes of its frame
VACUUM_VALUES = AXES  # the exact vacuum paces' count of values per digit, the axes' count (ALGEBRA.md, The click's read of the board: at the vacuum paces the six Ports' reaches and the mass sum to SIDES w, the massless point's mass 0, so each reach is w div AXES, the digit lattice F = gcd(w, 0, w div AXES) = w div AXES and the digit has AXES values, three; the clause of 2026-10-24, a digit lattice at or above w div 3, three values or fewer, is the exact vacuum paces' and the read is refused there), the law's own count from the Ports' names and no number of the engine


def ported(
    at: Node, shape: tuple[int, int, int], periodic: Sequence[bool]
) -> Iterator[tuple[int, Node]]:
    """Each Port of the Node with the Node beyond it: the six Ports in the order the law gives the Links (+x, -x, +y, -y, +z, -z; core/ports `PORT_SIDES`), the Node beyond each with the torus's wrap, none beyond an open face."""
    for port, (axis, side) in enumerate(PORT_SIDES):
        there = list(at)
        there[axis] += side
        if 0 <= there[axis] < shape[axis]:
            yield port, (there[0], there[1], there[2])
        elif periodic[axis]:
            there[axis] = int(division_forward(there[axis], shape[axis], 0)[1])  # the wrap, an index
            yield port, (there[0], there[1], there[2])


def frame_of(at: Node, shape: tuple[int, int, int], periodic: Sequence[bool]) -> list[Node]:
    """The Node's own frame for its read: the Node first, then the Nodes beyond its six Ports (`ported`), nothing of the board's labels, so the same frame at every Node and under every roll; the order the neighbours are listed in enters no number since 2026-10-24 (`read_of`: the Link digits in the order of their values)."""
    return [at, *(there for _port, there in ported(at, shape, periodic))]


def ports_of(at: Frame, shape: tuple[int, int, int], periodic: Sequence[bool]) -> list[int]:
    """The Port of each neighbour in the frame `at` (the Node first), by the Node's own Ports (`ported`): each neighbour matched to the Node beyond a Port, each Port taken once, in the frame's order (on a torus of extent two the two Ports of an axis reach one Node, and both Links' terms are read); a Node beyond none of the Ports is refused by name."""
    left = list(ported(at[0], shape, periodic))
    found = []
    for there in at[1:]:
        match = next((pair for pair in left if pair[1] == tuple(there)), None)
        if match is None:
            raise ValueError(
                f"the click's read at {list(at[0])} names the Node {list(there)} beyond none of its Ports"
            )
        left.remove(match)
        found.append(match[0])
    return found


def opposite(port: int) -> int:
    """The Port back across a Link: the same axis, the other side (core/ports `PORT_SIDES`)."""
    axis, side = PORT_SIDES[port]
    return PORT_SIDES.index((axis, -side))


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


def rule_and_pairs(board: Lattice, index: int, record: int) -> tuple[Rule, flux.Pairs | None]:
    """Rule3's integers of one record's read and its Link pairs where it is turned or folded, as the step reads them (`ruled`; `flux.pairs_of` at the same read, None for a plain record), made once per interval and given again."""
    content, factors = board.read(index, 1, record)
    rule = ruled(board, index, record, content, factors)
    families, states, gamma, amplitude = (
        board.families,
        board.states,
        board.world.node_clock,
        board.amplitude,
    )
    pairs = flux.pairs_of(index, families, states, 1, gamma, content, factors, record, amplitude)
    return rule, pairs


def digits_of(
    board: Lattice, index: int, at: Frame
) -> Iterator[tuple[int, int, int, list[int], list[int]]]:
    """One family's reads at the Nodes of the frame `at` (the Node first, then its neighbours): for every record of quanta of the family in its order (`registry.quanta_records`; a holder of the sign its one record, light's free row, `Lattice.lines_of`) and every line of the record in the declared order, the record, the line, the family's wall w, the line's kept remainders at the frame's Nodes and the lattices they are read on (`lattice_of`: the Node's own F_i first, then each neighbour's Link lattice F_ij at the Port the frame names, `ports_of`), Python's integers, the arrays read and never written."""
    family, gamma, unit = board.families[index], board.world.node_clock, board.unit
    wall = int(wall_of(family.pair[1], gamma, unit))
    ports = ports_of(at, board.shape, board.world.periodic)
    for record in registry.quanta_records(board.families, board.states, index):
        rule, pairs = rule_and_pairs(board, index, record)
        lattice = lattice_of(rule, at, pairs, ports)
        for number, line in enumerate(board.lines_of(index, record)):
            yield record, number, wall, picked(line.remainder, at), lattice


def at_origin(board: Lattice, reads: Reads) -> bool:
    """Whether every digit the read would take stands at the lay's origin w div 2 (the digits of `digits_of` over `reads`, each family at its Nodes): the condition `read_of` refuses on, read here without a refusal for the emission's draw alone (ALGEBRA.md, the exact dark: a body whose read finds every digit at the lay's origin at its emission's draw does not draw; The board reads itself: no draw where the Node's read finds every digit at the origin). A digit is its line's remainder at the Node over a lattice F, and the origin's digit is the remainder w div 2 whatever F, so the remainders alone are read here, the same records and the same Nodes as `digits_of` (every record of quanta of the family, every line of it, the frame's Nodes), and no rule, Link pair or lattice is made for a comparison that reads none of them (the economy of 2026-10-24, every answer the same)."""
    return all(
        int(remainder) == board.half_wall(index)
        for index, at in reads
        for record in registry.quanta_records(board.families, board.states, index)
        for line in board.lines_of(index, record)
        for remainder in picked(line.remainder, at)
    )


def lattice_of(rule: Rule, at: Frame, pairs: flux.Pairs | None, ports: Sequence[int]) -> list[int]:
    """The lattices of a Node's read, in the frame's order (ALGEBRA.md, The click's read of the board, the sentence of 2026-10-24): the Node's own first, F_i = gcd(w, D_i, R_ik over its six Ports, and R^c_ik, R^s_ik where the record is turned or folded) from Rule3's integers at the Node (`node.rule_of`) and the Link pairs the step reads (`pairs`, `flux.pairs_of`, (R^c, R^s) = p_i^2 (X^c, X^s) per Port; None for a plain record, the plain reaches alone); then, for each neighbour j at the Port `ports` names, the Link's lattice F_ij = gcd(w, R_ji, R^c_ji, R^s_ji), the Link's own terms as the neighbour steps across it, Rule3's integers at the neighbour at the Port back toward the Node (`opposite`), a multiple of the neighbour's own lattice F_j (a gcd over fewer of F_j's terms), so that the neighbour's remainder's coarse index, r div F_ij, is the floor of its fine index over the two lattices' ratio; Euclid's gcd on the line's coefficients (kind D in the acts table), the arrays read at one Node each and never written."""
    wall, here = int(rule.wall), (at[0],)
    own = (
        (rule.mass, *rule.reaches) if pairs is None else (rule.mass, *rule.reaches, *pairs[0], *pairs[1])
    )
    found = [gcd(wall, *(picked(value, here)[0] for value in own))]
    for there, port in zip(at[1:], ports, strict=True):
        back = opposite(port)  # the Port back across the Link, the neighbour's own toward the Node
        terms = (
            (rule.reaches[back],)
            if pairs is None
            else (rule.reaches[back], pairs[0][back], pairs[1][back])
        )
        found.append(gcd(wall, *(picked(value, (there,))[0] for value in terms)))
    return found


def read_of(board: Lattice, reads: Reads, label: str) -> int:
    """The click's read of the board, one Link and one number (ALGEBRA.md, The click's read of the board, the sentence of 2026-10-24): for every family in `reads` in that order, every record of quanta in the records' order and every line of it in the declared order (`digits_of`), the Node's own remainder as its index on the Node's own lattice F_i and each neighbour's remainder as its index on the Link's lattice F_ij (`lattice_of`), r div F, one division act per digit, in the base w div F + 1 (one above the digit's count of values, so that a total built of the wall's primes never divides the base and every digit enters the residue); a remainder equal to an earlier line's at the same Node of the record, or w less it, is a copy and enters nothing (the reader's D2 of 2026-10-20: a record's lines laid alike carry one remainder at every Node, equal before the write and complementary after it; one comparison per later line and no act); the digits of the Node and its six Links, of every line and record, in the order of their values (the digit, and the base where two digits are equal: the pair is the digit's read, two equal pairs exchangeable, so the number is one function of the multiset of the read's digits and no Port order, no lines' order and no records' order enters it; the builder's all-sorted line of 2026-10-24, measured on the toy: the tiles equal through 120, the 48 at every interval, 0 refused, the picks spread; the sentence (A) of 2026-10-24 15:0x, the Node's digit first and the six Link digits sorted per line in the records' order, kept by name with its numbers, the tiles through 120 to 150 and the pick 5, 4, 4 at the three-way reads), all as one number in the mixed radix of the bases (`features/click.read_number`); read at the draw's moment, the close before that click's write, and never written, so the run back and the inverse stand as they are. The number is divided by the unit once by the caller (`features/click.drawn_from`: the remainder the whether, the quotient the close's later draws'). Refused by name, `label` naming the Node and the interval: every remainder at the lay's origin w div 2 (the records untouched at the Nodes read, or an exactly periodic standing record returned to its origin: nothing to read), and every digit on the lattice of the exact vacuum paces, three values or fewer each (w div F at or below `VACUUM_VALUES`, the lattice F at or above w div 3: the massless point's remainders at p_0 = p_i = Gamma with no tension; a record read for its digits reads a content, the shipped universes' 60)."""
    taken: list[tuple[int, int]] = []
    origin, coarse = True, True
    for index, at in reads:
        half, earlier = board.half_wall(index), dict[tuple[int, int], list[int]]()
        for record, _line, wall, kept, lattice in digits_of(board, index, at):
            for place, (remainder, found) in enumerate(zip(kept, lattice, strict=True)):
                values = int(division_forward(wall, found, 0)[0])  # w div F, the digit's count of values
                origin = origin and remainder == half
                coarse = coarse and values <= VACUUM_VALUES  # the exact vacuum paces, refused by name
                standing = earlier.setdefault((record, place), [])
                copied = any(remainder in (seen, wall - seen) for seen in standing)
                standing.append(remainder)
                if copied:  # an earlier line's remainder at the Node, or w less it: a copy, read once
                    continue
                digit = int(division_forward(remainder, found, 0)[0])  # the index on the lattice
                taken.append((digit, values + 1))  # the base one above w div F
    taken.sort()  # every digit of the Node and its six Links, of every line and record, in the order of their values: the one composition line (2026-10-24)
    digits, bases = [digit for digit, _base in taken], [base for _digit, base in taken]
    if origin:
        raise RuntimeError(
            f"the click's read of the board at {label} finds every digit at the lay's origin w div 2: the "
            "records stand untouched at the Nodes read, nothing to read; a draw asked there is refused"
        )
    if coarse:
        raise RuntimeError(
            f"the click's read of the board at {label} finds every digit on the lattice of the exact vacuum "
            "paces, three values or fewer each (the lattice F at or above w div 3: the massless point's remainders "
            "at p_0 = p_i = Gamma with no tension; ALGEBRA.md, The click's read of the board); the number cannot "
            "spread over the unit, so the read is refused: a record read for its digits reads a content, the "
            "paces off the exact band"
        )
    return read_number(digits, bases)
