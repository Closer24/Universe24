"""ws1's driver: the engine's writer (run.forward, run.run_back) over the Node of whichever event_universe PYTHONPATH names (src: the engine;
src_ws1: the instrumented copy, whose reading acts not: the state hash must be equal), with cl1's flagged lay bound (lay_ws1.lay_world;
the fields absent: the engine's path). Readings from outside at every interval: the board's W of the planes with a gap and, where the
world lays two or more `at` packets with a gap, W per body over cl1's half-board masks (the Nodes nearer each body's centre along the axis
the centres differ in). Integers only. Usage: python run_ws1.py <world.json> <out.json> [back N]"""
from __future__ import annotations

import json
import sys
import time
from typing import Any

import numpy as np

from event_universe import node as node_module
from event_universe import run, seed
from event_universe.links import wronskian
from event_universe.loader.world import load_world
from event_universe.node import Node

import lay_ws1


def bodies_of(world: dict[str, Any]) -> list[tuple[int, ...]]:
    return [tuple(int(x) for x in lay["centre"]) for lay in world.get("seed", []) if lay.get("lay") == "at" and int(lay.get("row", 0)) != 0]


def torus_distance(a: int, b: int, cube: int) -> int:
    return min(abs(a - b), cube - abs(a - b))


def masks_of(node: Node, centres: list[tuple[int, ...]]) -> tuple[int, list[Any]]:
    axis = next((a for a in range(3) if centres[0][a] != centres[1][a]), 2)
    idx = np.indices(node.shape)[axis]
    dist = [np.vectorize(lambda z, c=c[axis]: torus_distance(int(z), c, node.cube), otypes=[object])(idx) for c in centres[:2]]
    return axis, [dist[0] < dist[1], dist[1] < dist[0]]


def w_reading(node: Node, masks: list[Any]) -> list[int]:
    """[interval, W of the planes with a gap over the board, W of every plane over the board, W per body over each half mask...]."""
    total_gap = None
    total_all = None
    for r in node.records():
        ww = wronskian(*r.lines)
        total_all = ww if total_all is None else total_all + ww
        if r.gap:
            total_gap = ww if total_gap is None else total_gap + ww
    found = [node.interval, int(sum(int(x) for x in total_gap.reshape(-1))), int(sum(int(x) for x in total_all.reshape(-1)))]
    for m in masks:
        found.append(int(sum(int(x) for x in np.where(m, total_gap, 0).reshape(-1))))
    return found


class Ws1Node(Node):
    def __init__(self, universe: dict[str, Any], world: dict[str, Any]) -> None:
        super().__init__(universe, world)
        self.centres = bodies_of(world)
        self.axis, self.masks = masks_of(self, self.centres) if len(self.centres) >= 2 else (2, [])
        self.wread: list[list[int]] = [w_reading(self, self.masks)]

    def step(self) -> None:
        super().step()
        self.wread.append(w_reading(self, self.masks))


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    seed.lay_world = lay_ws1.lay_world
    node_module.seed.lay_world = lay_ws1.lay_world
    t0 = time.monotonic_ns()
    node = Ws1Node(universe, world)
    intervals = int(world["intervals"])
    rows, _nodes, hashes = run.forward(node, intervals, back, lambda s: None)
    end_hash = node.state_hash()
    kept_log = list(node.log)
    returned = run.run_back(node, hashes) if back else None
    counts = {k: int(v) for k, v in node.counts.items()}
    found = {
        "world": argv[1], "intervals": intervals, "cube": node.cube, "counts": counts, "turns": node.turns,
        "run_back": returned, "end_hash": end_hash, "census": list(node.census()),
        "seconds": (time.monotonic_ns() - t0) // (1000 ** 3),
        "wcounts": getattr(node, "wcounts", None), "wlog": getattr(node, "wlog", None), "wread": node.wread,
        "lays": [e for e in kept_log if e["event"] == "lay"],
        "births": [[e["i"], e["line_pair"], e["W_children"], e["amplitude"]] for e in kept_log if e["event"] == "birth"],
        "credits": [[e["i"], e["line"], e["sense"], e["turned"]] for e in kept_log if e["event"] == "credit"],
    }
    print(json.dumps({k: found[k] for k in ("world", "intervals", "counts", "run_back", "end_hash", "census", "seconds", "wcounts")}))
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(found, f)


if __name__ == "__main__":
    main(sys.argv)
