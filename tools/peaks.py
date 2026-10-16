"""The step's partial sums measured beside a run (ENGINE.md, The amplitude bound): Rule3's flux line adds its terms in one order (`core/rule3.flux_total`), the free term w (2 a_now - a_before), then the Node's own terms w (2 a_now - a_before) - D_i a_now, then the Links' sum SUM_j R_ij (m_ij - a_now), then the remainder r, the whole total; this tool re-forms the four at every Node, line and interval of a world from the step's own inputs (the rule of the record's read, `node.rule_of`; the Links' sum gathered as the step gathers it, `flux.gathered_line`, `flux.gathered_plane`) before the board steps, and keeps the largest size of each over the run, beside the largest level reached, the world's amplitude bound A, the Link unit G and the engine's room B(A), the largest of the five partial rooms at A over the world's families and the loader's three pace points (`rule3.rule_total_bound`). Nothing here is the step: the board steps by `Lattice.step` as in a run, and the readings are the tool's. Usage: `PYTHONPATH=src python tools/peaks.py [--intervals N] <world>.json` prints one JSON object."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import flux, meeting, node
from event_universe.core.rule3 import flux_total, rule_total_bound
from event_universe.features.read import edge_of
from event_universe.lattice import Lattice
from event_universe.loader.derived import PLANE
from event_universe.plane import NO_FACE
from event_universe.records import record_slice
from event_universe.twist import faces_presented
from event_universe.world_files import load_world

FORWARD = 1


class Largest:
    """The largest sizes over a run of the four partial sums and of the levels."""

    def __init__(self) -> None:
        self.free_term, self.own_terms, self.link_sum, self.total, self.level = 0, 0, 0, 0, 0

    def widen(self, rule: Any, link_sum: Any, level: Any, other: Any, remainder: Any) -> None:
        """The four partial sums of Rule3's flux line at every Node, in the order the step adds them (`flux_total`), against the largest so far."""
        free_term = flux_total(0, 0, rule.wall, level, other)
        own_terms = flux_total(0, rule.mass, rule.wall, level, other)
        total = flux_total(link_sum, rule.mass, rule.wall, level, other) + remainder
        for name, found in (
            ("free_term", free_term),
            ("own_terms", own_terms),
            ("link_sum", link_sum),
            ("total", total),
            ("level", level),
        ):
            setattr(self, name, max(getattr(self, name), int(np.abs(np.asarray(found)).max())))

    def as_dict(self) -> dict[str, int]:
        return {
            "largest level": self.level,
            "free term": self.free_term,
            "own terms": self.own_terms,
            "link sum": self.link_sum,
            "total": self.total,
        }


def measured(board: Lattice, index: int, largest: Largest) -> None:
    """One family's lines before the board steps: every record's rule from its own read (as `flux.step_records` reads it), its Links' pairs where it is turned or folded, the faces the click act presents at this interval, and the Links' sum of every line gathered as the step gathers it."""
    family, state = board.families[index], board.states[index]
    gamma, unit = board.world.node_clock, board.unit
    faces = faces_presented(board, index)
    for record in range(family.records):
        content, factors = meeting.read_with_cuts(board, index, FORWARD, record)
        rule = node.rule_of(family, gamma, content, factors, unit)
        pairs = flux.pairs_of(
            index,
            board.families,
            board.states,
            FORWARD,
            board.wrap,
            gamma,
            content,
            factors,
            record,
            board.amplitude,
        )
        span = record_slice(family, record)
        lines = state.lines[span]
        if not family.plane or pairs is None:
            for number, line in enumerate(lines, span.start):
                fill = family.rest if number == span.start and not family.plane else 0
                link_sum, level, other = flux.gathered_line(
                    line, rule, board.wrap, fill, faces.get(number, NO_FACE), FORWARD
                )
                largest.widen(rule, link_sum, level, other, line.remainder)
            continue
        for start in range(0, len(lines), PLANE):
            re, im = lines[start], lines[start + 1]
            here = faces.get(span.start + start, NO_FACE), faces.get(span.start + start + 1, NO_FACE)
            now, other = (re.now, im.now), (re.before, im.before)
            sums = flux.gathered_plane(
                rule, board.wrap, now, other, (re.remainder, im.remainder), here, pairs, FORWARD
            )
            for part, line in enumerate((re, im)):
                largest.widen(rule, sums[part], now[part], other[part], line.remainder)


def room(board: Lattice) -> int:
    """B(A): the largest of the five partial rooms at the world's amplitude bound over its families and the loader's three pace points, the vacuum's, the frozen clock's and the hill's edge (`rule3.rule_total_bound`, the plain line's rooms)."""
    gamma, unit, bound = board.world.node_clock, board.unit, board.world.amplitude_bound
    found = 0
    for family in board.families:
        num, den = family.pair
        edge = edge_of(family.pair, gamma)
        for clock, pace in ((gamma, gamma), (0, 0), (edge, edge)):
            found = max(found, int(rule_total_bound(num, den, gamma, clock, pace, bound, unit)))
    return found


def peaks(world: Path, intervals: int | None) -> dict[str, Any]:
    """The world run for `intervals` intervals (all of its own when None), the four partial sums measured before every step."""
    board, largest = Lattice(load_world(world)), Largest()
    ticks = min(intervals or board.world.intervals, board.world.intervals)
    started, run = time.perf_counter(), 0
    for _ in range(ticks):
        for index in range(len(board.families)):
            if board.states[index].lines:
                measured(board, index, largest)
        board.step()
        run += 1
        if board.ended is not None:
            break
    return {
        "world": world.name,
        "shape": list(board.shape),
        "intervals": run,
        "A": int(board.world.amplitude_bound),
        "G": int(board.unit),
        **largest.as_dict(),
        "B(A)": room(board),
        "seconds": round(time.perf_counter() - started, 1),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split(":")[0])
    parser.add_argument("world", type=Path, help="the world file, with its mode file beside it")
    parser.add_argument(
        "--intervals", type=int, default=None, help="the intervals to run, all of the world's by default"
    )
    args = parser.parse_args(argv)
    print(json.dumps(peaks(args.world, args.intervals)))


if __name__ == "__main__":
    main()
