"""The body's language on the click (the model owner, 2026-09-28; HIGHLIGHTS lines 7 and 28): the recoil written into the body's own record and told as one event line beside the click, so that action and reaction stand on one line and the books carry the turns per body."""

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
    writes: RecoilWrites,
) -> None:
    """The recoil's writes into the body's own record's two levels at its Nodes and the angle's remainders at the body, the turn booked per body (`recoil_turns`, a GAMEBOARD book) and written as the `recoil` event line: the body, the sense (+1 the taker, -1 the giver), the record, the click's tally per axis and the turn per axis (the phase per Link, in the twist's unit)."""
    live = block.own
    if live is None:
        return
    live.now[block.mask] = np.asarray(writes.levels[0], dtype=np.int64)
    live.before[block.mask] = np.asarray(writes.levels[1], dtype=np.int64)
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
            }
        )
