"""cl1's driver over the ENGINE's Node (engine-5.0-test 5e94fd4b6; the symmetric ride, interval.run; the close, close.click): the engine's
writer run.record with two readings from outside and the flagged lay bound (lay_cl1.lay_world in place of seed.lay_world: the `at` lay's
`sense` and `charge` fields; absent, the engine's path bit for bit, checked by the last states' hashes against `python -m event_universe.run`).
The readings (no act, no Node reads them): at every interval each body's centroid in milli Links (thousandths of a Link), the body's Nodes
those nearer its seed centre on the torus along the axis the two centres differ in; its weight re_now^2 + im_now^2 over the planes with a
gap (the engine's packets_of weight), its Wronskian summed, and the sign level's extreme. Integers only.
Usage: python run_cl1.py <world.json> <out.json> [back N]; the out carries the engine's record plus "centroids" and "last_hash"."""
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
from event_universe.rows import PLANE, POTENTIAL

import lay_cl1

THOUSAND = 1000


def bodies_of(world: dict[str, Any]) -> list[tuple[int, ...]]:
    """The seed centres of the `at` lays onto planes with a gap, in the file's order (the gap-0 row is row 0 in the kit's universes)."""
    return [tuple(int(x) for x in lay["centre"]) for lay in world.get("seed", []) if lay.get("lay") == "at" and int(lay.get("row", 0)) != 0]


def torus_distance(a: int, b: int, cube: int) -> int:
    return min(abs(a - b), cube - abs(a - b))


def masks_of(node: Node, centres: list[tuple[int, ...]]) -> tuple[int, list[Any]]:
    """The axis the first two centres differ in and, per body, the mask of the Nodes nearer its centre along that axis (a tie to neither)."""
    axis = next((a for a in range(3) if centres[0][a] != centres[1][a]), 2)
    idx = np.indices(node.shape)[axis]
    dist = [np.vectorize(lambda z, c=c[axis]: torus_distance(int(z), c, node.cube), otypes=[object])(idx) for c in centres[:2]]
    return axis, [dist[0] < dist[1], dist[1] < dist[0]]


def centroid_reading(node: Node, axis: int, masks: list[Any]) -> dict[str, Any]:
    """Per body: the weight's centroid per axis in milli Links, the weight total, W summed, the credits' count so far; the sign level's extreme."""
    weight = None
    w_total = None
    for r in node.records():
        if r.gap == 0:
            continue
        re, im = r.lines
        w = re.now * re.now + im.now * im.now
        weight = w if weight is None else weight + w
        ww = wronskian(re, im)
        w_total = ww if w_total is None else w_total + ww
    idx = np.indices(node.shape)
    found: dict[str, Any] = {"i": node.interval, "axis": axis, "bodies": []}
    for m in masks:
        ws = [int(x) for x in np.where(m, weight, 0).reshape(-1)]
        total = sum(ws)
        centre = [sum(w * int(x) for w, x in zip(ws, idx[a].reshape(-1))) * THOUSAND // total if total else None for a in range(3)]
        found["bodies"].append({"centroid_milli": centre, "weight": total, "W": int(sum(int(x) for x in np.where(m, w_total, 0).reshape(-1)))})
    phi = node.row(POTENTIAL).lines[0].now
    found["sign_level_min_max"] = [min(int(x) for x in phi.reshape(-1)), max(int(x) for x in phi.reshape(-1))]
    return found


class Cl1Node(Node):
    """The engine's Node with the reading from outside after every step."""

    def __init__(self, universe: dict[str, Any], world: dict[str, Any]) -> None:
        super().__init__(universe, world)
        self.centres = bodies_of(world)
        self.axis, self.masks = masks_of(self, self.centres) if len(self.centres) >= 2 else (2, [])
        self.centroids: list[dict[str, Any]] = []
        if self.masks:
            self.centroids.append(centroid_reading(self, self.axis, self.masks))

    def step(self) -> None:
        super().step()
        if self.masks:
            self.centroids.append(centroid_reading(self, self.axis, self.masks))


def record(universe: dict[str, Any], world: dict[str, Any], back: int, out: Any) -> dict[str, Any]:
    """run.record with the Node above and the two readings added."""
    node = Cl1Node(universe, world)
    intervals = int(world["intervals"])
    t0 = time.monotonic_ns()
    rows, nodes, hashes = run.forward(node, intervals, back, out)
    kept_log = list(node.log)
    returned = run.run_back(node, hashes) if back else None
    if returned:
        out(json.dumps({"run back": returned}))
    counts = {k: str(v) for k, v in node.counts.items()}
    out(json.dumps({"counts": counts, "last_hash": hashes[-1] if hashes else None, "seconds": (time.monotonic_ns() - t0) // (THOUSAND ** 3)}))
    return {
        "world": world, "universe": universe, "den": node.den, "cube": node.cube, "intervals": intervals,
        "T": node.T, "gamma": node.gamma, "G": node.G, "counts": counts, "turns": node.turns, "rows": rows,
        "run_back": returned, "log": kept_log, "centroids": node.centroids, "last_hash": hashes[-1] if hashes else None,
        "census": list(node.census()),
    }


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    seed.lay_world = lay_cl1.lay_world  # the flag: the copy's lay in place of the engine's (absent fields: the same path)
    node_module.seed.lay_world = lay_cl1.lay_world
    found = record(universe, world, back, lambda line: print(line, flush=True))
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(found, f)


if __name__ == "__main__":
    main(sys.argv)
