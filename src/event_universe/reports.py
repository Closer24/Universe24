"""The detectors' reports and the bodies' Nodes (ALGEBRA.md #the-count-is-the-records-share, #readings-and-measurements; the owner's words of 2026-09-30, no click names a Node, the detector a declared instrument): a detector is a region of Nodes declared in the file, a declared instrument that reads the currents through its boundary; its click is its report of one interval, the net current into the region through the instrument's front boundary Ports, in the current's units, with the region's name and the family and never a Node; the credit of quanta to detectors is the host's reading by the shares. A body's Nodes, where its family's share stands about its declared Nodes, are derived when a report needs them and never kept. The output's words live here and nowhere else in the engine (ENGINE.md, the output): the click line, labelled the measurement, the field line, labelled a GameBoard reading, and the run's end."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.ports import Wrap, arrival

PORTS = tuple((axis, side) for axis in range(3) for side in (1, -1))  # [+X, -X, +Y, -Y, +Z, -Z]


MEASUREMENT, DIAGNOSTIC = (
    "DETECTOR",
    "GAMEBOARD",
)  # the labels of the output's lines (ALGEBRA.md #readings-and-measurements)
CLICK, FIELD = (
    "click",
    "field",
)  # the output's two lines: the detector's report and the GameBoard reading
OUTPUT = (
    "event",
    "label",
    "tick",
    "family",
    "detector",
    "inflow",
    "reading",
)  # the lines' keys, in their order
END = ("interval", "axis", "side", "largest")  # the keys of the run's lawful end at a receding face
BOOKS = ("share", "quanta", "drift", "pace")  # the keys of a family's books, a GameBoard diagnostic


@dataclass(frozen=True)
class Detector:
    """A detector: its name, its Nodes (None: the Nodes of the body it names, derived each interval), that body's number, and whether it is a region of the declared instrument (the faces' layer and a body's detector are not: each reads its own boundary and takes no field line)."""

    name: str
    nodes: np.ndarray | None
    body: int | None
    declared: bool


def click(tick: int, family: str, detector: str, inflow: int) -> dict[str, object]:
    """The click line, the measurement: the detector's report of one interval, the net current into its region through the instrument's front boundary Ports in the current's units (undivided; N over W_c is the host's reading), with the region's name and the family and never a Node, labelled DETECTOR."""
    return dict(zip(OUTPUT, (CLICK, MEASUREMENT, tick, family, detector, inflow), strict=False))


def field(tick: int, family: str, detector: str, reading: int | None) -> dict[str, object]:
    """The field line, a GameBoard reading labelled so and no measurement: the family's density over the region this interval."""
    line = dict(zip(OUTPUT, (FIELD, DIAGNOSTIC, tick, family, detector), strict=False))
    line[OUTPUT[-1]] = reading
    return line


def book(share: int, quanta: int, drift: int, pace: int) -> dict[str, int]:
    """A family's books, a GameBoard diagnostic: its share summed over the GameBoard in the current's units, the same in quanta over W_c, the share's drift from the one the world started with and the least Link pace of the final state."""
    return dict(zip(BOOKS, (share, quanta, drift, pace), strict=True))


def end(interval: int, axis: str, side: str, largest: int) -> dict[str, object]:
    """The lawful end, named: the front stands on the layer before the receding face of an axis grown to its largest size after this interval, and the next interval would reflect it."""
    return dict(zip(END, (interval, axis, side, largest), strict=True))


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
