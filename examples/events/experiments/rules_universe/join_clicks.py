"""THE READER OF WORLD (d), THE JOIN AND THE PARTING: the world of `lay_out_join.py` run headless through the engine's own functions with the event lines observed, and the reading of THE CLICK JOINS AND PARTS against the expectation file beside the world: THE COUNTS (GAMEBOARD), each body's held count at its Node every interval, read from the loop's block after the count's line, the first interval a count changes and the interval a count falls under the edge (the smaller dissolved) against `dissolution_intervals`; THE MOVES (GAMEBOARD), the quanta the count's line moved between the two bodies, interval by interval, from the counts' differences (a quantum leaving one and arriving at the other), and the first move's interval against `first_click_interval`; THE RECORDS (HOST), the records alive at the end against `records_at_the_end`; THE LEVELS (GAMEBOARD), the matter level at both Nodes and the support along the run from the declared readings. Nothing here replays a rule; no number of a run enters a test. Run from the repository root: PYTHONPATH=src python examples/events/experiments/rules_universe/join_clicks.py <world.json>; the reading is written beside the world as `<name>.clicks.json`."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from event_universe.core.readings import Readings
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world


def counts_of(simulation: DetectorLawSimulation) -> list[int]:
    """Each body's held count summed over its Nodes, read from the loop's block (GAMEBOARD)."""
    found = []
    for block in simulation.blocks:
        counts = getattr(block, "counts", None)
        if counts is None:
            found.append(sum(int(c) for c in (block.definition.counts or ())))
        else:
            found.append(int(counts.sum()))
    return found


def read(world_path: Path) -> dict[str, Any]:
    """The reading against the expectation file beside the world."""
    blind = json.loads(world_path.with_suffix(".expectation.json").read_text(encoding="utf-8"))["blind"]
    world = load_world(world_path)
    lines: list[dict[str, Any]] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    readings = Readings(world.readings)
    readings.read(simulation)
    counts = [counts_of(simulation)]
    refusal = None
    for _ in range(world.ticks):
        try:
            simulation.step()
        except (RuntimeError, ValueError) as stop:
            refusal = f"at interval {simulation.tick + 1}: {stop}"
            break
        readings.read(simulation)
        counts.append(counts_of(simulation))
    moves = [
        {
            "interval": i,
            "left": counts[i][0] - counts[i - 1][0],
            "right": counts[i][1] - counts[i - 1][1],
        }
        for i in range(1, len(counts))
        if counts[i] != counts[i - 1]
    ]
    edge = int(blind["edge_quanta_per_node"])
    first_move = moves[0]["interval"] if moves else None
    under_edge = next((i for i, c in enumerate(counts) if min(c) < edge), None)
    events: dict[str, int] = {}
    for line in lines:
        events[line.get("event", "?")] = events.get(line.get("event", "?"), 0) + 1
    low, high = blind["dissolution_intervals"]
    report = {
        "world": world_path.name,
        "kind": "WORLD (d), THE CLICK JOINS AND PARTS: the counts, the moves and the records against the expectation",
        "verdict": "LAWFUL" if refusal is None else "REFUSED IN THE RUN",
        "refusal": refusal,
        "ticks_run": simulation.tick,
        "1_the_counts": {
            "label": "GAMEBOARD",
            "start": counts[0],
            "end": counts[-1],
            "every_10": [(i, c) for i, c in enumerate(counts) if i % 10 == 0],
            "edge": edge,
            "under_the_edge_at": under_edge,
            "expected_dissolution_intervals": [low, high],
            "verdict": "MISS"
            if under_edge is None
            else ("MATCH" if low <= under_edge <= high else "MISS"),
        },
        "2_the_moves": {
            "label": "GAMEBOARD",
            "moves": moves[:40],
            "count_of_moves": len(moves),
            "quanta_moved": sum(abs(m["left"]) for m in moves),
            "first_move_interval": first_move,
            "expected_first_click_interval": blind["first_click_interval"],
            "verdict": "MATCH" if first_move == blind["first_click_interval"] else "MISS",
        },
        "3_the_records": {
            "label": "HOST",
            "alive_at_the_end": len(simulation.records),
            "expected": blind["records_at_the_end"],
            "verdict": "MATCH" if len(simulation.records) == blind["records_at_the_end"] else "MISS",
            "event_lines": events,
        },
        "4_the_levels": {
            "label": "GAMEBOARD",
            "readings": {
                r["name"]: [
                    (line["interval"], line.get("level", line.get("support", line.get("total"))))
                    for line in r["lines"]
                ][:12]
                for r in readings.output()
                if r["kind"] in ("level", "support", "total")
            },
        },
    }
    world_path.with_name(f"{world_path.stem}.clicks.json").write_text(
        json.dumps(report, indent=1) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    for argument in sys.argv[1:]:
        report = read(Path(argument).resolve())
        shown = dict(report)
        shown["1_the_counts"] = {k: v for k, v in report["1_the_counts"].items() if k != "every_10"}
        shown["2_the_moves"] = {**report["2_the_moves"], "moves": report["2_the_moves"]["moves"][:8]}
        print(json.dumps(shown, indent=1))


if __name__ == "__main__":
    main()
