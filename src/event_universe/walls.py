"""The held rows' walls and sources at the start (ALGEBRA.md, The write per proper volume and per proper interval, the clause of 2026-10-22; the law of one Node, 2026-10-23: every held row's write at the carried factor, the wall fixed per Node for the run): a row's fixed walls at a Node with no level, read by the growth and the run back for a grown layer, and whether anything sources a holder of the sign at the start."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe import records
from event_universe.loader.derived import readers_of

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Rulers = dict[
    records.Sourcing, records.Rulers
]  # the rulers per source record, as the lattice holds them


def sourced(board: Lattice, index: int) -> bool:
    """Whether anything sources a held row at the start: a reader's laid record with a Wronskian other than 0 at a Node for the holder of the sign (a real record sources none of it, so the holder keeps its laid record, light)."""
    return any(
        bool(np.asarray(records.wronskian(board.record(reader), board.families[reader].plane)).any())
        for reader in readers_of(board.families, index)
    )
