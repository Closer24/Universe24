"""The swap at the top (ALGEBRA.md, The swap at the top, a hypothesis under its own name, 2026-10-23, the owner's decision; the swap hand's derivation read cold by the reader): the fifth act of the interval, the law's own time symmetry used once at a Node. At the end of every interval each Node reads three levels of its own time line (the held row carrying its volume, features/volume) and nothing else: X0 the level before and X1 the level now it started the interval with, X2 the level now it ends with after the step and the one write. Where X0 <= X1 and X2 <= X1 and not all three are equal (the weak maximum, symmetric in X0 and X2), the Node is at a top and ends the interval at the state it started from with every line's two levels exchanged and every remainder complemented at its wall (w on a plain line, 3 w (X1 + X0) on a tension line carried as the shear's momentum, the write's wall on a write remainder; records.complement), the step's output discarded; everywhere else the interval stands. By Rule3's own identity on the carried division (the inverse on a state is the forward act on the swapped and complemented state, every neighbour's level fixed) this equals the swap of the post-state followed by one more step, and the forward run from it is the run back of the rise. The inverse is the same reading on the undone interval, (Y.before, Z.before, Z.now) with Z the post-state and Y the engine's inverse of it, the same triple read backward; where it holds the pre-state is the swapped and complemented Z: a bijection and an involution, nothing declared, nothing kept. The symmetry of the trigger is what makes the conditional act a bijection (an asymmetric trigger collides at a flat approach); the swap of the post-state in place of the pre-state fires again on the mirror passage and locks the board at its top, and is not the act. A falling rest state is a weak top and stands (its remainder alternating): an empty gapped board stands at the vacuum, The closed lattice has no rest excepted for it by the owner's decision. The phase lines of a holder of the sign under the rotation have no image under the act (the count's reversal is the pair's conjugate and not a swap of the count and 0): a top on such a world is refused by name. The module holds the loop's two calls (`stepped` after the held writes forward, `inverted` after the shear's inverse backward), reading the board's own records and nothing of the board."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import records, shear
from event_universe.core.rule3 import wall_of
from event_universe.loader.derived import turns

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Kept = tuple[
    list[list[records.Record]], list[list[np.ndarray]]
]  # every family's lines and write remainders at one end of the interval


def kept(board: Lattice) -> Kept:
    """Every family's lines and write remainders as they stand, the state one end of the interval holds (the lines are not copied: every act replaces them)."""
    return [s.lines for s in board.states], [list(s.write_remainders) for s in board.states]


def at_top(x0: Any, x1: Any, x2: Any) -> np.ndarray:
    """The trigger at every Node from the time line's three levels: the weak maximum, X0 <= X1 and X2 <= X1 and not X0 = X1 = X2, symmetric in X0 and X2."""
    x0, x1, x2 = (np.asarray(x, dtype=object) for x in (x0, x1, x2))
    return np.asarray((x0 <= x1) & (x2 <= x1) & ((x0 < x1) | (x2 < x1)), dtype=bool)


def swapped(board: Lattice, held: Kept, mask: np.ndarray) -> None:
    """The act where `mask` holds: every line of every family and every write remainder of the state `held` swapped and complemented at its wall, the interval's output kept elsewhere."""
    gamma, unit = board.world.node_clock, board.unit
    for index, family in enumerate(board.families):
        state, lines, remainders = board.states[index], held[0][index], held[1][index]
        wall = wall_of(family.pair[1], gamma, unit)
        times: dict[
            int, records.Record
        ] = {}  # per tension line the row's own time line at the interval's start, the wall of the shear's momentum
        if shear.carried(family):
            for record in range(family.records):
                first = records.record_slice(family, record).start
                for number in shear.shear_lines(family):
                    if first < number <= first + family.width - 1:
                        times[number] = lines[first]
        found = []
        for number, (line, out) in enumerate(zip(lines, state.lines, strict=True)):
            own: Any = wall
            if number in times:  # 3 w (X_now + X_before) of the row's own time line
                time = times[number]
                own = (
                    3
                    * wall
                    * (np.asarray(time.now, dtype=object) + np.asarray(time.before, dtype=object))
                )
            complemented = records.complement(np.asarray(line.remainder, dtype=object), own)
            found.append(
                records.Record(
                    np.asarray(np.where(mask, line.before, out.now), dtype=out.now.dtype),
                    np.asarray(np.where(mask, line.now, out.before), dtype=out.before.dtype),
                    np.asarray(
                        np.where(mask, complemented, np.asarray(out.remainder, dtype=object)),
                        dtype=out.remainder.dtype,
                    ),
                )
            )
        state.lines = found
        if state.write_remainders:
            walls = board.write_walls[index]
            state.write_remainders = [
                np.asarray(
                    np.where(
                        mask,
                        records.complement(np.asarray(r, dtype=object), np.asarray(w, dtype=object)),
                        np.asarray(out, dtype=object),
                    ),
                    dtype=np.asarray(out).dtype,
                )
                for w, r, out in zip(walls, remainders, state.write_remainders, strict=True)
            ]


def acted(board: Lattice, held: Kept, direction: int) -> None:
    """The act of one interval in `direction`: forward (+1) `held` is the pre-state and the triple (X0, X1, X2) is (held.before, held.now, the state's now); backward (-1) `held` is the post-state Z and the state the engine's inverse Y of it, the triple (Y.before, Z.before, Z.now); where the trigger holds, the state becomes `held` swapped and complemented; the swaps logged as (interval, direction, Nodes) for the readings and no act."""
    rows = [i for i in board.held if board.families[i].motion_volume]
    if not rows:
        return
    time_held, time_now = held[0][rows[0]][0], board.states[rows[0]].lines[0]
    if direction == 1:
        mask = at_top(time_held.before, time_held.now, time_now.now)
    else:
        mask = at_top(time_now.before, time_held.before, time_held.now)
    if not mask.any():
        return
    if any(f.rotation for f in board.families) or any(turns(board.families, i) for i in board.order):
        raise ValueError(
            "a Node's time line is at a top on a world with a holder of the sign under the rotation: the phase lines "
            "have no image under the swap at the top (ALGEBRA.md, The swap at the top, what it does not cover), refused by name"
        )
    swapped(board, held, mask)
    board.swaps.append((board.interval, direction, int(mask.sum())))


def stepped(board: Lattice, held: Kept) -> None:
    """The act forward, after the held writes and before the acts from outside the Node (`Lattice.step`)."""
    acted(board, held, 1)


def inverted(board: Lattice, held: Kept) -> None:
    """The act's inverse, after the shear's inverse and before the phase act back (`Lattice.step_inverse`)."""
    acted(board, held, -1)
