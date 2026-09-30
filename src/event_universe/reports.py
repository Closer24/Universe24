"""The detectors' clicks and the books (ALGEBRA.md #the-counts-line, #readings-and-measurements; the advisor's ruling, #1515 comment 5909238819): a detector is a group of Nodes declared in the file, its click a whole quantum's entry into the group through one of its boundary Ports, the one measurement, with its family, its axis and its side; a hop between two of its Nodes is no click, and the rise of its summed count is a reading of its book and no click; a body's Nodes, where its family's count stands about its declared Nodes, are derived when a report needs them and never kept; the books are a GameBoard reading."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import division_forward
from event_universe.node import NodeState


@dataclass(frozen=True)
class Detector:
    """A detector: its name, its declared Nodes (None: the Nodes of the body it names, derived each interval) and that body's number."""

    name: str
    nodes: np.ndarray | None
    body: int | None


def standing(declared: np.ndarray, count: np.ndarray, wrap: Wrap) -> np.ndarray:
    """A body's Nodes as a report needs them (ALGEBRA.md #what-a-body-is (c)): the Nodes where its family's count stands, connected through the Links to its declared Nodes; the declared Nodes themselves where the count stands on none of them; derived from the count and kept nowhere."""
    region = declared & (count != 0)
    if not bool(region.any()):
        return declared
    while True:
        grown = region.copy()
        for axis in range(3):
            for side in (1, -1):
                grown |= arrival(region, axis, side, wrap, False)
        grown &= count != 0
        if np.array_equal(grown, region):
            return np.asarray(region, dtype=bool)
        region = grown


def clicks(
    detector: Detector,
    nodes: np.ndarray,
    through: tuple[Any, ...],
    remainder: np.ndarray,
    count: np.ndarray,
    wall: int,
    wrap: Wrap,
    family: str,
    tick: int,
) -> list[dict[str, object]]:
    """The clicks, the one measurement (ALGEBRA.md #the-counts-line: a click has a family and an axis; the advisor's ruling, #1515 comment 5909238819): a whole quantum's entry into the detector through one of its boundary Ports, at every Port of its Nodes leading in from a Node outside them (none beyond an open face), the quanta the inward current carries into the Node's remainder, (r + F_p) div W_c where that is above 0, one division per Port in the order [+X, -X, +Y, -Y, +Z, -Z], r the Node's remainder before the line; one `click` line per quantum with the Node it entered, the Port's axis and side and the detector's count after; a hop between two of its Nodes is no click; nothing is handed over."""
    held = int(count[nodes].sum())
    line = {"event": "click", "tick": tick, "family": family, "detector": detector.name}
    found: list[dict[str, object]] = []
    for port, (axis, side) in enumerate((a, s) for a in range(3) for s in (1, -1)):
        outer = nodes & ~arrival(nodes, axis, side, wrap, True)
        crossed = np.asarray(division_forward(remainder + np.asarray(through[port]), wall, 0)[0])
        for at in np.argwhere(outer & (crossed > 0)):
            node = [int(i) for i in at]
            for _ in range(int(crossed[tuple(at)])):
                found.append(
                    {**line, "node": node, "axis": [axis, side], "count": held, "body": detector.body}
                )
    return found


def book(
    state: NodeState, wall: int, laid: tuple[int, int], reports: int, pace: int
) -> dict[str, int | bool]:
    """The books of a family of quanta (a GameBoard diagnostic): the count's sum, the remainders' sum, SUM (W_c c + r) against its laid value (the line conserves it to the bit), the clicks reported, the sense's SUM (W_c k + r) against its laid value, and the least Link pace of the final state; `laid` is the two laid totals."""
    assert state.count is not None and state.count_remainder is not None
    assert state.sense is not None and state.sense_remainder is not None
    total = int((wall * state.count.astype(object) + state.count_remainder).sum())
    sense = int((wall * state.sense.astype(object) + state.sense_remainder).sum())
    return {
        "count": int(state.count.sum()),
        "remainders": int(state.count_remainder.sum(dtype=object)),
        "total": total,
        "reports": reports,
        "balanced": total == laid[0],
        "sense": int(state.sense.sum()),
        "sense_balanced": sense == laid[1],
        "pace": pace,
    }
