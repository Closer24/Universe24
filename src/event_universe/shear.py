"""The shear's momentum at the lattice (ALGEBRA.md, The shear's momentum is carried at the volume's wall, a proposal under its own name, 2026-10-23; the symmetry hand's derivation from the cube's group of 48 read cold by the reader): the three tension lines of a held row of the content step as the shear's momentum at the volume's wall (flux.step_momentum) after the time line's step and write forward and after the time line's inverse backward, the one order of the acts inside the interval the hypothesis names; this module holds the loop's three calls (the write split around the step, `written`; the step itself, `stepped`; the inverse, `inverted`) and the start's birth of the remainders at half the volume's wall (`born`), reading the board's own records and nothing of the board."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import flux, meeting, node, records, take
from event_universe.core.ports import AXES
from event_universe.core.rule3 import wall_of
from event_universe.plane import NO_FACE

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


def carried(family: Any) -> bool:
    """Whether a held row carries its tension lines as the shear's momentum: a holder of the content with its axis lines under the trace (every such row, the law of one Node)."""
    return bool(family.axes and not family.wronskian)


def shear_lines(family: Any) -> list[int]:
    """The positions of a held row's tension lines among its lines, three per record after its time line."""
    return [
        records.record_slice(family, record).start + 1 + a
        for record in range(family.records)
        for a in range(AXES)
    ]


def written(
    board: Lattice,
    index: int,
    numerators: list[Any],
    walls: list[Any],
    direction: int,
    begun: list[list[records.Record]] | None,
) -> tuple[list[records.Record], list[np.ndarray]]:
    """(ALGEBRA.md, The shear's momentum is carried at the volume's wall; features/held_write) The held write of a row carrying the shear's momentum, in the direction's order: forward the time line's write, the tension lines' step (`stepped`, reading the time line after its step and write), the tension lines' write; backward the tension lines' write back and the time line's write back, the tension lines' step back left to `inverted` after the time line's step back (node.held_write_at on each part with its own numerators, walls and remainders)."""
    family, state = board.families[index], board.states[index]
    if not carried(family):  # a row without the shear's momentum: the one write of every line at once
        return node.held_write_at(state.lines, numerators, walls, state.write_remainders, direction)
    lines, kept = list(state.lines), list(state.write_remainders)
    shear = shear_lines(family)
    time = [number for number in range(len(lines)) if number not in shear]
    for part in (time, shear) if direction == 1 else (shear, time):
        found, carried_out = node.held_write_at(
            [lines[n] for n in part],
            [numerators[n] for n in part],
            [walls[n] for n in part],
            [kept[n] for n in part],
            direction,
        )
        for n, line, carry in zip(part, found, carried_out, strict=True):
            lines[n], kept[n] = line, carry
        state.lines, state.write_remainders = lines, kept
        if direction == 1 and part is time:
            assert begun is not None
            stepped(board, index, 1, begun)
            lines, kept = list(state.lines), list(state.write_remainders)
    return lines, kept


def stepped(board: Lattice, index: int, direction: int, begun: list[list[records.Record]]) -> None:
    """(ALGEBRA.md, The shear's momentum is carried at the volume's wall; features/held_write) The three tension lines of one held row stepped as the shear's momentum (flux.step_momentum): the rule of the row's own read at the interval's start (`begun`, the lines the direction starts from), the Node's own three volumes in the direction, forward (X_before, X_now, X_next) with X_next the time line after its step and its write, backward (X_next, X_now, X_before) with X_before the time line's inverse's output (the reversibility hand's Theorem 1: every numerator a function of the post-state in that order), the faces the click act presents and the Links the world cuts."""
    family, gamma, unit = board.families[index], board.world.node_clock, board.unit
    started = [replace(s, lines=lines) for s, lines in zip(board.states, begun, strict=True)]
    faces, cuts = take.faces_presented(board, index), meeting.cut(board, index)
    lines = list(board.states[index].lines)
    for record in range(family.records):
        content, factors = node.read(
            index, board.families, started, direction, board.wrap, gamma, unit, record, cuts
        )
        rule = node.rule_of(family, gamma, content, factors, unit)
        first = records.record_slice(family, record).start
        time_begun, time_now = begun[index][first], lines[first]
        volumes = (
            (time_begun.before, time_begun.now, time_now.now)
            if direction == 1
            else (time_begun.now, time_begun.before, time_now.before)
        )
        faces_of = [faces.get(first + 1 + a, NO_FACE) for a in range(AXES)]
        lines[first + 1 : first + 1 + AXES] = flux.step_momentum(
            lines[first + 1 : first + 1 + AXES], rule, board.wrap, direction, faces_of, volumes
        )
    board.states[index].lines = lines


def inverted(board: Lattice, ended: list[list[records.Record]]) -> None:
    """The tension lines' inverse of every row carrying the shear's momentum, after the time line's (`ended` the post-state the inverse started from), each line read against the amplitude bound."""
    for index in board.held:
        if carried(board.families[index]):
            stepped(board, index, -1, ended)
            family = board.families[index]
            for number, line in enumerate(board.states[index].lines):
                board.bounded(family.name, line, number == 0 and family.motion_volume)


def born(board: Lattice, family: Any, lines: list[records.Record]) -> None:
    """(ALGEBRA.md, The shear's momentum is carried at the volume's wall; features/held_write) The tension lines' remainders born at half the volume's wall, 3 w X_0 (half of 3 w (X_0 + X_0)), Python's integers, X_0 the time line's volume at the start."""
    if carried(family):
        half = (
            3 * wall_of(family.pair[1], board.world.node_clock, board.unit) * records.exact(lines[0].now)
        )
        for number in range(1, 1 + AXES):
            lines[number] = replace(lines[number], remainder=np.asarray(half, dtype=object))
