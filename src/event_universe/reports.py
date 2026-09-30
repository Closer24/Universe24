"""The detectors' reports and the output lines (ALGEBRA.md #the-counts-line, #readings-and-measurements): a detector is a Node told to report, its report of the quanta a family's count brought across its boundary the one measurement (`gather`); a body's clock, the giving it makes and its total are readings (`click`, `giving`, `block`), and so are the books."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from event_universe.node import NodeState


@dataclass(frozen=True)
class Detector:
    """A detector: its name, its fixed Nodes (None: the Nodes of its body each interval) and the body it names."""

    name: str
    nodes: np.ndarray | None
    body: int | None


def gathers(
    detector: Detector, nodes: np.ndarray, rise: np.ndarray, count: np.ndarray, family: str, tick: int
) -> list[dict[str, object]]:
    """The report, a reading of the count's line (ALGEBRA.md #the-counts-line: the count that arrives at a detector's Node is the detector's click): the rise of a family's count summed over the detector's Nodes this interval, the net inflow across its boundary (a move between its own Nodes cancels), one `gather` line per unit of rise with the detector's count after; nothing is handed over."""
    arrived, held = int(rise[nodes].sum()), int(count[nodes].sum())
    line = {"event": "gather", "tick": tick, "family": family, "detector": detector.name, "count": held}
    return [{**line, "taker": detector.body} for _ in range(max(arrived, 0))]


def clock_lines(
    number: int, family: str, corner: list[int], before: int, total: int, tick: int
) -> list[dict[str, object]]:
    """The body's clock, a reading that fires nothing: a crossing of its total from at most 0 to above 0 is a `click` line, and every interval a `block` line with the total."""
    lines: list[dict[str, object]] = []
    if before <= 0 < total:
        lines.append(
            {"event": "click", "tick": tick, "measured": number, "family": family, "node": corner}
        )
    lines.append({"event": "block", "tick": tick, "measured": number, "corner": corner, "sum": total})
    return lines


def giving_line(
    number: int, family: str, at: tuple[int, int, int], axis: int, side: int, count: int, tick: int
) -> dict[str, object]:
    """One quantum given, a reading of the count's line's click at a body's shell: the shell Node, the Port it crossed as [axis, side] and the body's count after."""
    return {
        "event": "giving",
        "tick": tick,
        "measured": number,
        "family": family,
        "node": list(at),
        "axis": [axis, side],
        "count": count,
    }


def book(
    state: NodeState, wall: int, laid: tuple[int, int], moved: tuple[int, int, int]
) -> dict[str, int | bool]:
    """The books of a family of quanta (a GameBoard diagnostic): the count's sum, the remainders' sum, SUM (W_c c + r) against its laid value moved by the givings alone (the line conserves it to the bit), the quanta given and taken, the reports, and the sense's SUM (W_c k + r) against its laid value (no giving moves it); `laid` is the two laid totals, `moved` the quanta given, taken and reported."""
    assert state.count is not None and state.count_remainder is not None
    assert state.sense is not None and state.sense_remainder is not None
    given, taken, reports = moved
    total = int((wall * state.count.astype(object) + state.count_remainder).sum())
    sense = int((wall * state.sense.astype(object) + state.sense_remainder).sum())
    return {
        "count": int(state.count.sum()),
        "remainders": int(state.count_remainder.sum(dtype=object)),
        "total": total,
        "given": given,
        "taken": taken,
        "reports": reports,
        "balanced": total == laid[0] + wall * (taken - given),
        "sense": int(state.sense.sum()),
        "sense_balanced": sense == laid[1],
    }
