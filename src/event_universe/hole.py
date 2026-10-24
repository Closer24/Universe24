"""The hole is the write that takes what the birth books and nothing else: the exact take (ALGEBRA.md, The board reads itself, the hole's clause of 2026-10-24 on the builder's derivation, the one-Link form of the fall ruled 17:1x UTC; the module split from meeting_board.py the same day for the files' bound): at a born Node the seed record's before is kept and its now moved toward its before one level at a time (`moved`) until the frame's seven shares, read exactly on the Node's own term and its six Links' terms over their walls (`taken_at`), have fallen by the children's walls summed (`walls_of`); `take_of` the level search, the Take its levels, the taken, the walls, the excess below the last level's step and the step; the caller (`meeting_board.closed`) refuses the close by name where the full stop cannot pay and writes the hole through the one lay act; every face read before any write."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, NamedTuple

import numpy as np

from event_universe import node, records
from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.digits import frame_of, opposite, ports_of
from event_universe.loader.derived import count_wall
from event_universe.loader.keys import Node

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Table = tuple[tuple[int, int], ...]


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


def taken_at(board: Lattice, index: int, span: slice, at: Node, levels: int) -> tuple[int, int]:
    """The fall of the frame's seven shares when the seed record's now at the Node moves `levels` levels toward its before (`moved`), read exactly on the Node's own term and its six Links' terms over their walls, no neighbour's floor (ALGEBRA.md, The board reads itself, the hole's clause, the one-Link form ruled 2026-10-24, 17:1x UTC): the share's own form at a Node k is N_k div W_k with W_k = 4 p_k^2 G^2 (`share.share`, the frame's term, `share.over_pace`; 1 at a frozen Node) and N_k = 2 (w (n_k^2 + b_k^2) - S_k n_k b_k) - 2 n_k SUM_j R_kj b_j - SUM_j R_kj (b_k - b_j)(n_k + n_j); when the Node's now moves, only its own term and its six Links' products move, in its numerator and in each neighbour's, so the frame's exact fall is the Node's change over W_i plus each Link's change over its two ends' walls, summed over the record's lines as one rational with the common denominator D = W_i PROD_j W_j, returned as (numerator, D): nothing of a neighbour's other Links enters, so the fall is one Link's reading and bit-equal in every slab. Kept by name with its finding: the per-Node floors' form of this afternoon (the seven shares each floored, `share.family_share` on the moved lines), which carried the neighbours' two-Link remainders N_j mod W_j into the fall and parted the slabs runner's lines by a unit or two in the logged taken, excess and step (the 5-cube by two slabs: 142669080 against 142669081 at the interval 5), the arrays equal."""
    family, gamma, unit = board.families[index], board.world.node_clock, board.unit
    content, factors = board.read(index, 1, 0)
    rule = node.rule_of(family, gamma, content, factors, unit)
    squares = np.asarray(paces.link_pace_of(gamma, content), dtype=object)
    squares = squares * squares
    frame = frame_of(at, board.shape, board.world.periodic)
    ports = ports_of(frame, board.shape, board.world.periodic)
    walls = []
    for k in frame:  # W_k = 4 p_k^2 G^2, the frame's term's wall (share.over_pace with the halves 2), 1 at a frozen Node
        twice = int(squares[k]) + int(squares[k])
        walls.append((twice + twice) * unit * unit + int(twice == 0))
    common, cofactors = 1, []
    for wall in walls:
        common *= wall
    for number, _wall in enumerate(walls):  # D over W_k as the product of the other walls, no division
        cofactor = 1
        for other, wall in enumerate(walls):
            cofactor *= 1 if other == number else wall
        cofactors.append(cofactor)
    wall_w, own = int(rule.wall), int(np.asarray(rule.self_coefficient, dtype=object)[at])
    numerator = 0
    for line in board.states[index].lines[span]:
        now, before = int(line.now[at]), int(line.before[at])
        toward = 0 if now == before else (1 if before > now else -1)
        after = now + toward * min(levels, abs(now - before))
        shift = after - now
        reach_sum = 0
        node_change = 2 * (wall_w * (after * after - now * now) - own * before * shift)
        for there, port in zip(frame[1:], ports, strict=True):
            reach_out = int(np.asarray(rule.reaches[port], dtype=object)[at])
            reach_back = int(np.asarray(rule.reaches[opposite(port)], dtype=object)[there])
            b_j = int(line.before[there])
            reach_sum += reach_out * b_j
            node_change -= reach_out * (before - b_j) * shift
            link_change = (
                -reach_back * (b_j - before) * shift
            )  # the neighbour's numerator, its one term that moves
            numerator -= link_change * cofactors[1 + ports.index(port)]
        node_change -= 2 * shift * reach_sum
        numerator -= node_change * cofactors[0]
    return numerator, common


def take_of(board: Lattice, index: int, span: slice, at: Node, walls: int) -> Take:
    """The exact take, the hole as the write that takes what the birth books and nothing else (ALGEBRA.md, The board reads itself, the hole's clause of 2026-10-24, the builder's derivation on #2187; the one-Link form ruled 17:1x UTC): at the born Node the seed record's before is kept and its now is moved toward its before, one level at a time (`moved`), until the frame's seven shares, read exactly on the Node's own term and its six Links' terms over their walls (`taken_at`), have fallen by the children's walls summed (`walls`); the first such level is the take's, the fall in the current's units (the exact numerator over the common denominator, one division act, kind D) the taken, the fall less the walls the excess, below the last level's step, and the last level's step named with it; where the full stop (the now at the before) would take less than the walls, the Take carries the full stop's fall below the walls and the caller refuses the close by name (`refused_by`), nothing born and the light standing. The comparisons run level by level and the level search stands as it was; the arrays are read and never written here, the hole written by the caller through the one lay act. Kept by name with their numbers, the forms before this one: the write to (0, 0), which against the sea's drifted level made light at the six Links, 7.68 quanta at the first close of the 3-cube, and spent the sea to exactly zero; the Node's own level before twice (`stopped_at`, the sentence of 2026-10-24 15:0x), which took 1.6 to 2.7 W_c for two booked at 1.526, the Links' part of the share following the level; the exact take's excess 0.0002 to 0.04 W_c per birth on the builder's three boards."""
    lines = list(board.states[index].lines[span])
    distance = max(abs(int(line.now[at]) - int(line.before[at])) for line in lines)

    def fallen(levels: int) -> int:
        numerator, common = taken_at(board, index, span, at, levels)
        return int(division_forward(numerator, common, 0)[0])  # the fall in the current's units, once

    full = fallen(distance)
    if full < walls:
        return Take(distance, full, walls, full - walls, 0)
    previous = 0
    for levels in range(1, distance):
        taken = fallen(levels)
        if taken >= walls:
            return Take(levels, taken, walls, taken - walls, taken - previous)
        previous = taken
    return Take(distance, full, walls, full - walls, full - previous)
