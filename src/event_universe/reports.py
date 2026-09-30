"""The detectors' clicks and the books (ALGEBRA.md #the-counts-line, #readings-and-measurements; the owner's word of 2026-09-30, no click names a Node): a detector is a region of Nodes declared in the file, a declared instrument that reads the currents through its boundary; its click is a whole quantum's entry into the region through its boundary Ports, the one measurement, reported with the region's name, the family and the Ports crossed and never a Node; a hop between two of its Nodes is no click, and the rise of its summed count is a reading of its book and no click; a body's Nodes, where its family's count stands about its declared Nodes, are derived when a report needs them and never kept; the books are a GameBoard reading."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap, arrival
from event_universe.core.rule3 import division_forward
from event_universe.node import NodeState

PORTS = tuple((axis, side) for axis in range(3) for side in (1, -1))  # [+X, -X, +Y, -Y, +Z, -Z]


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


def entered(
    nodes: np.ndarray, through: tuple[Any, ...], wrap: Wrap, instrument: np.ndarray
) -> list[np.ndarray]:
    """Per Port, the Nodes of the region at which that Port is a boundary Port of the instrument (it leads in from a Node outside the instrument, the union of the declared regions, none beyond an open face) carrying a current into the region this interval; a Port between two regions of one instrument is no boundary, so a quantum moving from one region to the next is no entry and no click."""
    return [
        nodes & ~arrival(instrument, axis, side, wrap, True) & (np.asarray(through[port]) > 0)
        for port, (axis, side) in enumerate(PORTS)
    ]


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
    instrument: np.ndarray,
) -> tuple[list[dict[str, object]], int]:
    """The clicks, the one measurement, and what the detector saw (ALGEBRA.md #the-counts-line, #the-click-ends-nothing; the owner's words of 2026-09-30, no click names a Node, the detector a declared instrument): at every Node of the region the currents entering it through the region's boundary Ports (`entered`) are summed, and (r + SUM F_p) div W_c where that is above 0, r the Node's remainder before the line, is the whole quanta that entered the region there; one `click` line per quantum with the region's name, the family, the Ports crossed as [axis, side] (one, or two where a corner of the region is crossed in one interval) and the region's count after; a hop between two of its Nodes is no click, no line names a Node, and nothing is handed over. Beside the clicks, the region's inflow this interval, the inward currents through the instrument's boundary Ports at its Nodes summed in integers, the amplitudes the instrument saw at its boundary (its `seen` line of the interval, the host's reading for the credit by the shares); `instrument` is the union of the declared regions (a body's detector and the faces' layer their own Nodes), so that what passes between the regions of one screen is neither seen twice nor clicked twice."""
    held = int(count[nodes].sum())
    line = {"event": "click", "tick": tick, "family": family, "detector": detector.name}
    inward = entered(nodes, through, wrap, instrument)
    total = np.zeros(nodes.shape, dtype=np.int64)
    for port in range(len(PORTS)):
        total = total + np.where(inward[port], np.asarray(through[port]), 0)
    crossed = np.asarray(division_forward(remainder + total, wall, 0)[0])
    found: list[dict[str, object]] = []
    for at in np.argwhere(crossed > 0):
        where = tuple(at)
        ports = [list(PORTS[port]) for port in range(len(PORTS)) if inward[port][where]]
        for _ in range(int(crossed[where])):
            found.append({**line, "ports": ports, "count": held, "body": detector.body})
    return found, int(total.sum(dtype=object))


def book(
    state: NodeState, wall: int, laid: tuple[int, int], reports: int, pace: int
) -> dict[str, int | bool]:
    """The books of a family (a GameBoard diagnostic): the count's sum, the remainders' sum, SUM (W_c c + r) against its laid value (the line conserves it to the bit), the clicks reported, the sense's SUM (W_c k + r) against its laid value (0 and balanced on a real record, which carries no sense), and the least Link pace of the final state; `laid` is the two laid totals."""
    assert state.count is not None and state.count_remainder is not None
    total = int((wall * state.count.astype(object) + state.count_remainder).sum())
    sense, sense_total = 0, laid[1]
    if state.sense is not None and state.sense_remainder is not None:
        sense = int(state.sense.sum())
        sense_total = int((wall * state.sense.astype(object) + state.sense_remainder).sum())
    return {
        "count": int(state.count.sum()),
        "remainders": int(state.count_remainder.sum(dtype=object)),
        "total": total,
        "reports": reports,
        "balanced": total == laid[0],
        "sense": sense,
        "sense_balanced": sense_total == laid[1],
        "pace": pace,
    }
