"""The engine run with the twist read at every interval (H-Helicity-From-The-Twist-1): a reader, no act, nothing of the state changed.

The world is run by the engine's own writer (event_universe.run: Node, forward, run_back, the record as run.record builds it); the
writer's Node line is wrapped so that, after every step, the twist of every record on every +axis Link (links.row_twist, the act
the close reads at close.py meet: `twists = [row_twist(start, axis) ...]`, `start` the record's lines at the interval's start) is
read from the state and its sign kept per record, per axis, per Node. The state after the step of interval i is the start of
interval i + 1, the state the close of i + 1 reads; the seed's state is read as the start of interval 1. The record is written as
the writer writes it (the log, the counts, the run back) beside the twists' file: {"interval i": {record k: [sign arrays per axis]}}.
Integers only. Usage: python twist_run.py <world.json> <record_out.json> <twists_out.json> [back N]
"""

from __future__ import annotations

import json
import sys

from event_universe import run as engine
from event_universe.core.ports import AXES
from event_universe.links import row_twist
from event_universe.loader.world import load_world


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


def twists_of(node: engine.Node) -> list[list[list[int]]]:
    """The sign of every record's twist on every +axis Link at the state the Node holds (the record's lines as the Node holds them)."""
    return [[[sign(int(x)) for x in row_twist(row.lines, axis).reshape(-1)] for axis in range(AXES)] for row in node.records()]


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    _, world_path, out_path, twists_path, *rest = argv
    back = int(rest[rest.index("back") + 1]) if "back" in rest else 0
    universe, world = load_world(world_path)
    node = engine.Node(universe, world)
    intervals = int(world["intervals"])
    kept: dict[str, list[list[list[int]]]] = {"0": twists_of(node)}
    original = engine.node_lines

    def hooked(n: engine.Node) -> dict:
        line = original(n)
        kept[str(n.interval)] = twists_of(n)
        return line

    engine.node_lines = hooked
    rows, nodes, hashes = engine.forward(node, intervals, back, lambda line: print(line, flush=True))
    kept_log = list(node.log)
    returned = engine.run_back(node, hashes) if back else None
    print(json.dumps({"run back": returned}), flush=True)
    counts = {k: str(v) for k, v in node.counts.items()}
    print(json.dumps({"counts": counts}), flush=True)
    found = {
        "world": world,
        "universe": universe,
        "den": node.den,
        "cube": node.cube,
        "intervals": intervals,
        "gapped": [(str(r.pair[0]), str(engine.sine_den(r.pair[0], node.den))) for r in node.gapped if r.pair],
        "planes": [str(r.pair[0]) for r in node.records() if r.pair],
        "T": node.T,
        "gamma": node.gamma,
        "G": node.G,
        "counts": counts,
        "turns": node.turns,
        "rows": rows,
        "nodes": nodes,
        "run_back": returned,
        "log": kept_log,
    }
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(found, out)
    records = node.records()
    with open(twists_path, "w", encoding="utf-8") as out:
        json.dump(
            {
                "records": [{"index": k, "shape": r.shape, "pair": [str(x) for x in r.pair] if r.pair else None, "emitter": r is node.emitter()} for k, r in enumerate(records)],
                "cube": node.cube,
                "twists": kept,
            },
            out,
        )


if __name__ == "__main__":
    main(sys.argv)
