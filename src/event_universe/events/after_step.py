"""The acts after the step, out of the loop's module (the ledger's place (ii), the rows the loop hooks per record): the lifetime's end of a record at its age L, and the write's line the loop hands its callers; each function takes the engine (`DetectorLawSimulation` of `detector_law.py`) and is bound as its method of the same duty, so every caller, test and spy works unchanged."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, cast

from event_universe.core.rule3 import Key
from event_universe.features.lifetime import LifetimeStart, LifetimeTerm, LifetimeWrites
from event_universe.features.write import WriteOwn, WriteStart, WriteTerm, WriteWrites

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def lifetime_stage(loop: DetectorLawSimulation, function: Callable[..., object]) -> None:
    """The lifetime's act (features/lifetime): every free record of a family with a lifetime L whose last quantum was not reported ends on the border `lifetime` at age L, the quanta it still carries handed there on its `gather` line, the record deleted whole at the interval's close."""
    for identity in list(loop.records):
        live = loop.records[identity]
        lifetime = loop.families[live.family].lifetime
        if lifetime is None or live.counts is None or live.reported or loop.lifetime_detector is None:
            continue
        writes = cast(
            LifetimeWrites, function(LifetimeTerm(lifetime), LifetimeStart(live.age, live.reported))
        )
        if writes.ends:
            loop._gather_line(live, loop.lifetime_detector, None, live.content)
            live.reported = True
            loop.dead.append(live.identity)


def write_line(
    loop: DetectorLawSimulation,
    act: str,
    wall: int,
    coefficient: int,
    counts: tuple[tuple[Key, int], ...],
    values: dict[Key, int],
    carries: dict[Key, int],
) -> tuple[tuple[Key, int, int], ...]:
    """The write's line the loop hands the four callers (the hold, the giving, the recoil, THE START), its method `_write_line`: one act of the folder features/write, found by its name at load (`loop.write`), per key (coefficient x count + r) div wall by Rule3's carried division at both levels, the remainders written back into the caller's own (ALGEBRA.md #the-primitives, the row "the write")."""
    term, start, own = WriteTerm(wall, coefficient), WriteStart(act, counts), WriteOwn(values, carries)
    writes = cast(WriteWrites, loop.write(term, start, own))
    values.update(writes.own.values)
    carries.update(writes.own.carries)
    return writes.levels
