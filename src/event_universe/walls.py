"""The held rows' walls and sources at the start (ALGEBRA.md, The write per proper volume and per proper interval, the clause of 2026-10-22; the law of one Node, 2026-10-23: every held row's write at the carried factor, the wall fixed per Node for the run): a row's fixed walls at a Node with no level, read by the growth and the run back for a grown layer, and whether anything sources a holder of the sign at the start."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import records
from event_universe.bookings import sources_of
from event_universe.core import paces
from event_universe.loader.derived import readers_of

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Rulers = dict[
    records.Sourcing, records.Rulers
]  # the rulers per source record, as the lattice holds them


def vacuum_walls(board: Lattice, index: int) -> list[int]:
    """A held row's fixed walls at a Node with no level, one integer per line: the walls per Node of the carried factor (`records.walls_at`) at the rulers every source reads at the rest, the clock from the content of the holders it reads at their rests (the fill beyond a face, the level the volume's reading gives the rest's volume) and the pace along every axis the Node's pace under no tension; the walls a layer grown beyond a receding face is born with (growth.resize), the same the start gives every Node standing at the rest."""
    gamma = board.world.node_clock
    rulers: Rulers = {}
    for source in sources_of(board.families, board.order):
        reads = [r for r in board.families[source[0]].reads if not board.families[r.family].rotation]
        if not reads:
            rulers[source] = (gamma, (gamma, gamma, gamma))
            continue
        content: Any = np.full(
            (1, 1, 1), sum(r.weight * board.families[r.family].rest for r in reads), dtype=board.kind
        )
        clock, pace = paces.node_paces(gamma, content)
        axis = paces.axis_pace(pace, gamma, 0, 0)
        rulers[source] = (clock, (axis, axis, axis))
    found = records.walls_at(index, board.families, board.writes[index], rulers, gamma)
    return [int(np.asarray(wall, dtype=object).reshape(-1)[0]) for wall in found]


def sourced(board: Lattice, index: int) -> bool:
    """Whether anything sources a held row at the start: a reader's laid record with a Wronskian other than 0 at a Node for the holder of the sign (a real record sources none of it, so the holder keeps its laid record, light)."""
    return any(
        bool(np.asarray(records.wronskian(board.record(reader), board.families[reader].plane)).any())
        for reader in readers_of(board.families, index)
    )
