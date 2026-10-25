"""The reference frames of a turned record's read through its Ports (ALGEBRA.md, The stress is the Links', 2026-10-23; `readings.framed`, `plane.frame_signs`): the sign a turned record reads its neighbour's plane with through each of its six Ports, from the phase row's remainder of the record's own row on the holder of the sign, None for a record that is not turned; one reading the step (`flux.step_records`), the held write's sources (`Lattice.held_write`) and the board's readings (`board_readings`) share."""

from __future__ import annotations

from typing import Any

from event_universe import node, records
from event_universe.core.ports import Wrap
from event_universe.loader.derived import row_of, turns
from event_universe.plane import frame_signs


def frames_of(
    index: int, families: records.Families, states: records.States, wrap: Wrap, record: int = 0
) -> tuple[Any, ...] | None:
    """The sign a turned record reads its neighbour's plane with through each of its six Ports, in Port order (plane.frame_signs on the phase row's remainder of the record's own row of its holder of the sign: +1 where the Link's two ends stand in one frame, -1 where one end is time-reversed by the swap at the top and the other not, so that the Link reads its two ends in one frame, ALGEBRA.md, The swap at the top, the frame clause); None for a record that is not turned."""
    if not turns(families, index):
        return None
    row = row_of(families, index, record)
    assert row is not None
    frame = states[node.sign_holder(index, families)].phases[row][node.PHI].remainder
    return frame_signs(frame, wrap)
