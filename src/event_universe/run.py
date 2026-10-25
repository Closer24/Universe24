"""The writer: the world's intervals run, a reader's row at every twelfth and two early marks, then N intervals run back and compared bit for bit by the state's hash (the arrow's reading on the record); the record is the two files, the constants, the counts, the turns, the rows, the run back and the log as the run left it. Usage: `python -m event_universe.run <world.json> <out.json> [back N]`."""

from __future__ import annotations

import json
import sys
import time
from collections.abc import Callable
from typing import Any

import numpy as np

from event_universe.core.paces import sine_den
from event_universe.links import wronskian
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE, POTENTIAL, zeros

MARKS = 12  # the reader's rows: one at every twelfth of the run
EARLY = (60, 24)  # and two early marks, at the sixtieth and the twenty-fourth
THOUSAND = 1000  # a centroid in thousandths of a Link, a clock in milliseconds


def ints(a: Any) -> list[int]:
    """An array's values as Python integers."""
    return [int(x) for x in a.reshape(-1)]


def packets_of(node: Node) -> dict[str, Any]:
    """The reader's view of every plane with a gap: its weight's centroid in thousandths of a Link, its Nodes with levels, its energy's bits."""
    found = {}
    for rec, row in enumerate(node.records()):
        if row.gap == 0:
            continue
        re, im = row.lines
        weight = re.now * re.now + im.now * im.now
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
    metric, potential, massless = node.row(CARRIER), node.row(POTENTIAL), node.row(PLANE, gap=0).lines[0]
    planes = [r.lines for r in node.records()]
    cs, vs = ints(node.content()), ints(metric.lines[0].now)
    energy = sum(x * x for rec in planes for line in rec for x in ints(line.now))
    odd_max = max(abs(x) for line in potential.lines[1:] for x in ints(line.now))
    light_v = max(abs(a - b) for a, b in zip(ints(massless.now), ints(massless.before), strict=True))
    total = zeros(node.shape)
    for re, im in planes:
        total = total + wronskian(re, im)
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
        "links at the wall": sum(1 for f in node.link_factors()[0::2] for x in ints(f) if x == 0),
        "tension min/max": [min(tens), max(tens)],
        "odd max bits": odd_max.bit_length(),
        "link count max": node.count_max,
        "orbit table": len(node.orbit),
        "massless W abs max": max(abs(x) for x in ints(wronskian(*node.row(PLANE, gap=0).lines))),
        "W total": sum(ints(total)),
        "W abs sum": sum(abs(x) for re, im in planes for x in ints(wronskian(re, im))),
        "light velocity max": light_v,
    }


def record(
    universe: dict[str, Any], world: dict[str, Any], back: int = 0, out: Callable[[str], Any] = print
) -> dict[str, Any]:
    """The world's intervals run with the reader's rows written as they come, then `back` intervals run back and compared by the state's hash; the record returned."""
    node = Node(universe, world)
    intervals = int(world["intervals"])
    t0 = time.monotonic_ns()
    marks = (
        {1, intervals}
        | {(k * intervals) // MARKS for k in range(1, MARKS)}
        | {intervals // e for e in EARLY}
    )
    rows: list[dict[str, Any]] = []
    hashes = []
    maxbits = 0
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(node.state_hash())
        node.step()
        maxbits = max(maxbits, node.census()[1])
        if node.interval in marks:
            rows.append(
                dict(
                    reading(node, maxbits),
                    milliseconds=(time.monotonic_ns() - t0) // (THOUSAND * THOUSAND),
                )
            )
            out(json.dumps(rows[-1]))
    kept_log = list(node.log)
    run_back = None
    if back:
        exact = 0
        for k in range(back):
            node.step_back()
            exact += node.state_hash() == hashes[back - 1 - k]
        run_back = {"intervals": back, "exact": exact}
        out(json.dumps({"run back": run_back}))
    counts = {k: str(v) for k, v in node.counts.items()}
    out(json.dumps({"counts": counts}))
    return {
        "world": world,
        "universe": universe,
        "den": node.den,
        "cube": node.cube,
        "intervals": intervals,
        "lifts": [
            (None, str(r.pair[0]), str(sine_den(r.pair[0], node.den))) for r in node.lifts if r.pair
        ],
        "planes": [str(r.pair[0]) for r in node.records() if r.pair],
        "T": node.T,
        "gamma": node.gamma,
        "G": node.G,
        "counts": counts,
        "turns": node.turns,
        "rows": rows,
        "run_back": run_back,
        "log": kept_log,
    }


def main(argv: list[str]) -> None:
    """The writer from the command line: the world file, the output file, `back N` for the run back."""
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    found = record(universe, world, back, lambda line: print(line, flush=True))
    with open(argv[2], "w", encoding="utf-8") as out:
        json.dump(found, out)


if __name__ == "__main__":
    main(sys.argv)
