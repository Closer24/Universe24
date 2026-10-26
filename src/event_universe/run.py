"""The writer: the world's intervals run, a reader's row at every twelfth and two early marks, then N intervals run back and compared bit for bit by the state's hash (the arrow's reading on the record); the record is the two files, the constants, the counts, the turns, the rows, the run back and the log as the run left it. Usage: `python -m event_universe.run <world.json> <out.json> [back N]`; the record carries a Node line per interval (X, content, turned, frozen, the Links held at the wall) for the page."""

from __future__ import annotations

import json
import sys
import time
from collections.abc import Callable
from typing import Any

import numpy as np

from event_universe import gram, readings
from event_universe.core import paces
from event_universe.core.paces import sine_den
from event_universe.core.ports import AXES, SIDES, port_of
from event_universe.decoder import THOUSAND
from event_universe.links import link_current
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, POTENTIAL, zeros

MARKS = 12  # the reader's rows: one at every twelfth of the run
EARLY = (60, 24)  # and two early marks, at the sixtieth and the twenty-fourth


def ints(a: Any) -> list[int]:
    """An array's values as Python integers."""
    return [int(x) for x in a.reshape(-1)]


def packets_of(node: Node) -> dict[str, Any]:
    """The reader's view of every plane with a gap: its weight's centroid in thousandths of a Link, its Nodes with levels, its energy's bits."""
    found = {}
    for rec, row in enumerate(node.records()):
        if row is node.emitter():
            continue
        nows = [line.now for line in row.lines]
        weight = gram.form(gram.gram(row.shape), nows, nows)
        total = sum(ints(weight))
        if total == 0:
            continue
        idx = np.indices(node.shape)
        centre = [
            sum(w * x for w, x in zip(ints(weight), ints(idx[a]), strict=True)) * THOUSAND // total
            for a in range(len(node.shape))
        ]
        found[f"plane {rec}"] = {
            "centroid (thousandths of a Link)": centre,
            "nodes with levels": sum(1 for x in ints(weight) if x > 0),
            "energy bits": total.bit_length(),
        }
    return found


def reading(node: Node, maxbits: int) -> dict[str, Any]:
    """The reader's row at an interval: the board's numbers read from outside (no Node reads them)."""
    metric, potential, emitter = node.row(CARRIER), node.row(POTENTIAL), node.emitter().lines[0]
    records = node.records()
    cs, vs = ints(node.content()), ints(metric.lines[0].now)
    energy = sum(x * x for r in records for line in r.lines for x in ints(line.now))
    odd_max = max(abs(x) for line in potential.lines[1:] for x in ints(line.now))
    emitter_v = max(abs(a - b) for a, b in zip(ints(emitter.now), ints(emitter.before), strict=True))
    total = zeros(node.shape)
    charges = [gram.charge(r.shape, r.lines) for r in records]
    for w in charges:
        total = total + w
    n, _bits = node.census()
    tens = [x for line in metric.lines[1:] for x in ints(line.now)]
    counts = node.counts
    return {
        "i": node.interval,
        "packets (reader)": packets_of(node),
        "content min/mean/max": [min(cs), sum(cs) // len(cs), max(cs)],
        "volume mean": sum(vs) // len(vs),
        "births": counts["births"],
        "body_clicks": counts["body_clicks"],
        "refused": sum(v for k, v in counts.items() if k.startswith("refused_")),
        "refused_lay": counts["refused_lay"],
        "refused_orientation": counts["refused_orientation"],
        "turns": counts["turns"],
        "integers": n,
        "max bits": maxbits,
        "max transient bits": node.max_transient,
        "sign level max": max(abs(x) for x in ints(potential.lines[0].now)),
        "planes energy bits": energy.bit_length(),
        "links at the wall": sum(1 for f in node.link_factors()[0::SIDES] for x in ints(f) if x == 0),
        "tension min/max": [min(tens), max(tens)],
        "odd max bits": odd_max.bit_length(),
        "link count max": node.count_max,
        "orbit table": len(node.orbit),
        "gap-0 W abs max": max(abs(x) for x in ints(charges[records.index(node.emitter())])),
        "W total": sum(ints(total)),
        "W abs sum": sum(abs(x) for w in charges for x in ints(w)),
        "gap-0 velocity max": emitter_v,
    }


def node_lines(node: Node) -> dict[str, Any]:
    """The record's Node and Link line at an interval, every Node by its index in the board's order: the carrier's level X, the content, the turned Nodes, the frozen Nodes (the Link pace 0), the Links held at the wall (the factor 0) as [Node, axis] pairs, and every Link's current of the gap-0 line, F_ij from the Node along each axis (the sign the direction, the size the flow); the page draws the board from these and nothing else."""
    carrier = node.row(CARRIER).lines[0]
    content = node.content()
    pace = paces.link_pace_of(node.gamma, content)
    factors = node.link_factors(None, readings.frozen_of(node, content))
    held = [
        [i, axis]
        for axis in range(AXES)
        for i, f in enumerate(ints(factors[port_of(axis, 0)]))
        if f == 0
    ]
    emitter = node.emitter().lines[0]
    return {
        "i": node.interval,
        "X": ints(carrier.now),
        "content": ints(content),
        "turned": [i for i, t in enumerate(node.turned.reshape(-1).tolist()) if t],
        "frozen": [i for i, p in enumerate(ints(pace)) if p == 0],
        "held": held,
        "current": [ints(link_current(emitter, port_of(axis, 0))) for axis in range(AXES)],
    }


def run_back(node: Node, hashes: list[str]) -> dict[str, int]:
    """The run back: as many intervals back as states were kept, each compared with the kept state's hash."""
    exact = 0
    for k in range(len(hashes)):
        node.step_back()
        exact += node.state_hash() == hashes[len(hashes) - 1 - k]
    return {"intervals": len(hashes), "exact": exact}


def forward(
    node: Node, intervals: int, back: int, out: Callable[[str], Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """The intervals run forward: the reader's rows at the marks written as they come, a Node line at every interval, the last `back` states' hashes kept for the run back."""
    t0 = time.monotonic_ns()
    marks = (
        {1, intervals}
        | {(k * intervals) // MARKS for k in range(1, MARKS)}
        | {intervals // e for e in EARLY}
    )
    rows: list[dict[str, Any]] = []
    nodes: list[dict[str, Any]] = []
    hashes = []
    maxbits = 0
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(node.state_hash())
        node.step()
        maxbits = max(maxbits, node.census()[1])
        nodes.append(node_lines(node))
        if node.interval in marks:
            rows.append(
                dict(
                    reading(node, maxbits),
                    milliseconds=(time.monotonic_ns() - t0) // (THOUSAND * THOUSAND),
                )
            )
            out(json.dumps(rows[-1]))
    return rows, nodes, hashes


def record(
    universe: dict[str, Any], world: dict[str, Any], back: int = 0, out: Callable[[str], Any] = print
) -> dict[str, Any]:
    """The world's intervals run (`forward`), then `back` intervals run back and compared by the state's hash (`run_back`); the record returned."""
    node = Node(universe, world)
    intervals = int(world["intervals"])
    rows, nodes, hashes = forward(node, intervals, back, out)
    kept_log = list(node.log)
    returned = run_back(node, hashes) if back else None
    if returned:
        out(json.dumps({"run back": returned}))
    counts = {k: str(v) for k, v in node.counts.items()}
    out(json.dumps({"counts": counts}))
    return {
        "world": world,
        "universe": universe,
        "den": node.den,
        "cube": node.cube,
        "intervals": intervals,
        "gapped": [(str(r.pair[0]), str(sine_den(r.pair[0], node.den))) for r in node.gapped if r.pair],
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


def main(argv: list[str]) -> None:
    """The writer from the command line: the world file, the output file, `back N` for the run back."""
    sys.set_int_max_str_digits(0)
    _, world_path, out_path, *_rest = argv
    universe, world = load_world(world_path)
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    found = record(universe, world, back, lambda line: print(line, flush=True))
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(found, out)


if __name__ == "__main__":
    main(sys.argv)
