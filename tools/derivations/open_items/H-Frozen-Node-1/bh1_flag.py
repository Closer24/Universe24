"""bh1's flag (2026-10-25): the form of the frozen Node under test in this COPY of the engine; FORM None is the engine bit for bit (every mask all False, every call the engine's own)."""
from __future__ import annotations

from typing import Any

import numpy as np

FORM: str | None = None  # None | "horizon" | "identity" | "write" | "horizon+identity" | "horizon+write"


def horizon() -> bool:
    """A Link with a frozen end is read at the wall (the horizon widened to the frozen Node's six Links)."""
    return FORM is not None and "horizon" in FORM


def identity() -> bool:
    """A frozen Node's state stands: no act changes it (the frozen mask kept in the frame as the turned mask is)."""
    return FORM is not None and "identity" in FORM


def write_stops() -> bool:
    """The carrier's write is refused at a frozen Node (the numerator 0 there); the step is the letter's."""
    return FORM is not None and "write" in FORM


def mask(found: Any, shape: tuple[int, ...]) -> Any:
    """The frozen mask under a form; all False without one (the engine's path)."""
    return np.asarray(found, dtype=bool) if FORM is not None else np.zeros(shape, dtype=bool)


def swap(node: Any, held: Any, frozen: Any) -> Any:
    """The swap at the top with its trigger off at the frozen Nodes under the identity form; node.swap bit for bit otherwise (its body repeated here with the one mask)."""
    if not identity():
        return node.swap(held)
    from event_universe import readings
    from event_universe.rows import CARRIER

    k = node.rows_.index(node.row(CARRIER))
    x0, x1, x2 = held[k][0].before, held[k][0].now, node.row(CARRIER).lines[0].now
    peak = np.vectorize(
        lambda a, b, c: (int(a) <= int(b) and int(c) <= int(b) and (int(a) < int(b) or int(c) < int(b))),
        otypes=[bool],
    )
    xf = readings.floor(node)
    below = np.vectorize(lambda a, c: int(a) < xf or int(c) < xf, otypes=[bool])
    top = (peak(x0, x1, x2) | below(x0, x2)) & ~np.asarray(frozen, dtype=bool)
    node.turned = top
    if top.any():
        node.counts["turns"] += int(top.sum())
        node.turns.append((node.interval, int(top.sum())))
        node.exchange(top, held)
    return top
