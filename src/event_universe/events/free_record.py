"""THE FREE RECORD'S QUANTUM (ALGEBRA.md #the-counts-line, the free record; the model owner's word of 2026-09-29 on #1495, finding 10): a given record is laid with one quantum from its form at its birth, its two levels scaled so the count its form lays over the board is exactly one, by the generator's own act (tools/pixel_mode.py `scaled_record`): the scale bracketed by halving and doubling, then bisected, integers alone; each scaled level (level x k) div A by Rule3's division act, A the written record's own amplitude and k the new one, so no number of the engine enters; refused by name where no scale lays exactly one quantum."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from event_universe.core.rule3 import NO_READ, rule3

Laid = Callable[[np.ndarray, np.ndarray], int]


def scaled_levels(
    now: np.ndarray, before: np.ndarray, amplitude: int, scale: int
) -> tuple[np.ndarray, np.ndarray]:
    """The two levels at the amplitude `scale`: (level x scale) div amplitude at every Node by Rule3's division act (the scale the coefficient on the level, the amplitude the wall), the remainder not kept (the scale is the generator's choice, not a step of the law)."""
    return (
        np.asarray(rule3(NO_READ, NO_READ, scale, amplitude, now, 0, 0)[0], dtype=np.int64),
        np.asarray(rule3(NO_READ, NO_READ, scale, amplitude, before, 0, 0)[0], dtype=np.int64),
    )


def scaled_to_one_quantum(
    now: np.ndarray, before: np.ndarray, laid: Laid, bound: int, label: str
) -> tuple[np.ndarray, np.ndarray]:
    """The record's two levels scaled so that `laid`, the count its form lays over the board (the loop's lay, core.rule3 and the count's line alone), is exactly one quantum: the new amplitude k bracketed from the record's own amplitude by halving (while the lay reaches one) and doubling (while it does not, up to the amplitude bound A), then bisected to the least k whose lay reaches one; refused by name where the written record is zero, where no amplitude up to A lays a quantum, or where the least such amplitude lays more than one."""
    amplitude = int(max(int(np.abs(now).max()), int(np.abs(before).max())))
    if amplitude == 0:
        raise ValueError(
            f"{label}: the written record is zero at every Node, and no scale lays one quantum"
        )

    def count(scale: int) -> int:
        return laid(*scaled_levels(now, before, amplitude, scale))

    low, high = amplitude, amplitude
    if count(amplitude) >= 1:
        while low > 0 and count(low) >= 1:
            high, low = low, low // 2
    else:
        while count(high) < 1:
            if high > bound:
                raise ValueError(
                    f"{label}: the given record's form lays no quantum at any amplitude up to the bound "
                    f"A = {bound} (ALGEBRA.md #the-counts-line, the free record)"
                )
            low, high = high, 2 * high
    while high - low > 1:
        middle = (low + high) // 2
        if count(middle) >= 1:
            high = middle
        else:
            low = middle
    found = count(high)
    if found != 1:
        raise ValueError(
            f"{label}: the given record's form lays {found} quanta at the least amplitude {high} that lays "
            "any, never exactly one: no scale gives the record one quantum (ALGEBRA.md #the-counts-line, "
            "the free record)"
        )
    if high > bound:
        raise ValueError(
            f"{label}: the given record's amplitude {high} for one quantum is above the bound A = {bound}"
        )
    return scaled_levels(now, before, amplitude, high)
