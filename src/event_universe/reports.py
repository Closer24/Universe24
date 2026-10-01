"""The detectors' reports and the bodies' Nodes (ALGEBRA.md #the-count-is-the-records-share, #readings-and-measurements; the owner's words of 2026-09-30, no click names a Node, the detector a declared instrument): a detector is a region of Nodes declared in the file, a declared instrument that reads the currents through its boundary; its click is its report of one interval, the net current into the region through the instrument's front boundary Ports, in the current's units, with the region's name and the family and never a Node; the credit of quanta to detectors is the host's reading by the shares. A body's Nodes, where its family's share stands about its declared Nodes, are derived when a report needs them and never kept."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap, arrival

PORTS = tuple((axis, side) for axis in range(3) for side in (1, -1))  # [+X, -X, +Y, -Y, +Z, -Z]


@dataclass(frozen=True)
class Detector:
    """A detector: its name, its declared Nodes (None: the Nodes of the body it names, derived each interval) and that body's number."""

    name: str
    nodes: np.ndarray | None
    body: int | None


def standing(declared: np.ndarray, present: np.ndarray, wrap: Wrap) -> np.ndarray:
    """A body's Nodes as a report needs them (ALGEBRA.md #what-a-body-is (c)): the Nodes where its family's share stands in quanta (`present`), connected through the Links to its declared Nodes; the declared Nodes themselves where it stands on none of them; derived and kept nowhere."""
    region = declared & present
    if not bool(region.any()):
        return declared
    while True:
        grown = region.copy()
        for axis in range(3):
            for side in (1, -1):
                grown |= arrival(region, axis, side, wrap, False)
        grown &= present
        if np.array_equal(grown, region):
            return np.asarray(region, dtype=bool)
        region = grown


def front(
    nodes: np.ndarray, wrap: Wrap, instrument: np.ndarray, declared: np.ndarray
) -> list[np.ndarray]:
    """Per Port, the Nodes of the region at which that Port is a front boundary Port of the instrument: it leads in from a Node of the declared board outside the instrument (`declared`, the file's own Nodes; the layers a receding face has grown lie beyond the declared board, and what leaves into them has left the world), so a Port between two regions, a Port toward the grown layers and a Port beyond a face are no front."""
    return [
        nodes & ~arrival(instrument, axis, side, wrap, True) & arrival(declared, axis, side, wrap, False)
        for axis, side in PORTS
    ]


def inflow(
    nodes: np.ndarray,
    through: tuple[Any, ...],
    wrap: Wrap,
    instrument: np.ndarray,
    declared: np.ndarray,
) -> int:
    """A detector's report of one interval, its click (ALGEBRA.md #the-count-is-the-records-share, #the-click-ends-nothing; the owner's words of 2026-09-30, no click names a Node, the detector a declared instrument): the currents through the instrument's front boundary Ports at the region's Nodes (`front`), inward positive, summed in integers with their signs, the density that entered the region from the declared board (the advisor's correction, #1515 comment 5912958018: the front Links only, net; the transverse Links inside the instrument and the Links toward a receding face's grown layers not counted); the host's reading for the credit by the shares. `instrument` is the union of the declared regions (a body's detector and the faces' layer their own Nodes), so that what passes between the regions of one screen is not seen twice; nothing is handed over and no line names a Node."""
    facing = front(nodes, wrap, instrument, declared)
    seen: Any = 0
    for port in range(len(PORTS)):
        seen = seen + np.where(facing[port], np.asarray(through[port]), 0)
    return int(np.asarray(seen).sum(dtype=object))
