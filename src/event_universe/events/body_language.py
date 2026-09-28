"""The body's language on the click (the model owner, 2026-09-28; HIGHLIGHTS lines 7 and 28): the recoil told as one event line beside the click, so that action and reaction stand on one line and the books carry the turns per body; the levels the loop wrote are the loop's, at its one site."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe.features.recoil import RecoilWrites

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation
    from event_universe.events.records import Block


def recoil(
    simulation: DetectorLawSimulation,
    block: Block,
    number: int,
    sense: int,
    identity: int,
    tally: tuple[int, int, int],
    before: tuple[np.ndarray, np.ndarray],
    writes: RecoilWrites,
) -> None:
    """The recoil's angle remainders written at the body under the recoil's key, the turn booked per body (`recoil_turns`, a GAMEBOARD book) and the `recoil` event line: the body, the sense (+1 the taker, -1 the giver), the record, the click's tally per axis, the turn per axis (the phase per Link, in the twist's unit) and the record's two levels at the body's Nodes before the turn (`levels_before`, the host's copy: the click keeps the click, and the reversible row undoes the turn from it)."""
    for stored, written in (
        (block.hold_value, writes.own.values),
        (block.hold_carry, writes.own.carries),
    ):
        for key, value in written.items():
            stored[("recoil", *key)] = value
    book = simulation.recoil_turns.setdefault(number, [0, 0, 0])
    for axis in range(3):
        book[axis] += writes.turn[axis]
    if simulation.record is not None:
        simulation.record(
            {
                "event": "recoil",
                "tick": simulation.tick,
                "measured": number,
                "sense": sense,
                "record": identity,
                "tally": list(tally),
                "turn": list(writes.turn),
                "levels_before": [[int(v) for v in level] for level in before],
            }
        )
