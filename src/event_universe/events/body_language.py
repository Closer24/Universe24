"""The body's language on the click (the model owner, 2026-09-28; HIGHLIGHTS lines 7 and 28): the recoil written into the body and told as one event line beside the click, so that action and reaction stand on one line and the books carry the kicks per body."""

from __future__ import annotations

from typing import TYPE_CHECKING

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
    before: tuple[int, int, int],
    writes: RecoilWrites,
) -> None:
    """The recoil's writes into the body's two levels of momentum and its stores on the wall, the kick booked per body (`recoil_kicks`, a GAMEBOARD book) and written as the `recoil` event line: the body, the sense (+1 the taker, -1 the giver), the record, the click's tally per axis and the kick per axis."""
    kick = [kicked - old for kicked, old in zip(writes.momentum, before, strict=True)]
    for axis, (kicked, rest) in enumerate(zip(writes.momentum, writes.remainders, strict=True)):
        block.momentum_before[axis] += kick[axis]
        block.momentum[axis], block.hold_value[("recoil", axis)] = kicked, rest
    book = simulation.recoil_kicks.setdefault(number, [0, 0, 0])
    for axis in range(3):
        book[axis] += kick[axis]
    if simulation.record is not None:
        simulation.record(
            {
                "event": "recoil",
                "tick": simulation.tick,
                "measured": number,
                "sense": sense,
                "record": identity,
                "tally": list(tally),
                "kick": kick,
            }
        )
