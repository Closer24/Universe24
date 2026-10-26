"""The hand H-Six-Metric-Lines-3: one world run as the writer runs it (run.record's loop) with the ten lines read: the record's hash (the log, the counts, the turns, the Node lines), the births and the credits, the gates SHOWN, the run back of the last `back` intervals, the bits and the count per Node, the six lines' board sums and their largest magnitude per line at the end, the Nodes where the flux is 0 and the six lines are 0. `python run_y3.py <world.json> <intervals> <back> <out.json>`; the engine on PYTHONPATH decides (the head, the copy with Y3_METRIC unset, or set)."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

sys.set_int_max_str_digits(0)

from event_universe import run as writer  # noqa: E402
from event_universe.core.ports import AXES, PORTS  # noqa: E402
from event_universe.gates import gates, kind_of  # noqa: E402
from event_universe.links import row_current  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402


def ints(a):
    return [int(x) for x in a.reshape(-1)]


def six_lines(node: Node) -> dict:
    lines = node.row(CARRIER).lines
    found = {}
    for k, line in enumerate(lines):
        nows = ints(line.now)
        found[f"line {k}"] = {
            "sum now": sum(nows),
            "max abs now": max(abs(x) for x in nows),
            "nonzero nodes": sum(1 for x in nows if x != 0),
            "max abs rem": max(abs(x) for x in ints(line.rem)),
            "wr max": max(ints(line.wr)) if line.wr is not None else None,
        }
    flux_zero = None
    rows = node.records()
    net = [0] * AXES
    for r in rows:
        for a in range(AXES):
            net[a] = net[a] + r.pair[0] * (row_current(r.lines, 2 * a + 1) - row_current(r.lines, 2 * a))
    zero_flux = [all(int(net[a].reshape(-1)[i]) == 0 for a in range(AXES)) for i in range(net[0].size)]
    six_zero = [
        all(int(lines[k].now.reshape(-1)[i]) == 0 and int(lines[k].before.reshape(-1)[i]) == 0 for k in range(1 + AXES, 1 + 3 * AXES))
        for i in range(net[0].size)
    ]
    found["nodes with the level flux 0"] = sum(zero_flux)
    found["nodes with the six lines 0"] = sum(six_zero)
    found["nodes with the flux 0 and the six lines not 0"] = sum(1 for z, s in zip(zero_flux, six_zero) if z and not s)
    return found


def main(argv):
    world_path, intervals, back, out = argv[1], int(argv[2]), int(argv[3]), argv[4]
    universe, world = load_world(world_path)
    world = dict(world, intervals=intervals)
    t0 = time.time()
    node = Node(universe, world)
    rows, nodes, hashes = writer.forward(node, intervals, back, lambda line: None)
    end_hash = node.state_hash()
    census = node.census()
    six = six_lines(node)
    kept_log = list(node.log)
    returned = writer.run_back(node, hashes) if back else None
    counts = {k: str(v) for k, v in node.counts.items()}
    record = {
        "world": world,
        "universe": universe,
        "den": node.den,
        "cube": node.cube,
        "intervals": intervals,
        "gapped": [(str(r.pair[0]), str(writer.sine_den(r.pair[0], node.den))) for r in node.gapped if r.pair],
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
    record = json.loads(json.dumps(record))
    timeless = {k: v for k, v in record.items() if k != "rows"}
    timeless["rows"] = [{k: v for k, v in row.items() if k != "milliseconds"} for row in record["rows"]]
    record_hash = hashlib.sha256(json.dumps(timeless, sort_keys=True).encode()).hexdigest()
    found = gates(record)
    kinds = {int(k[:2]): kind_of(v["verdict"]) for k, v in found.items() if k[:2].strip().isdigit()}
    shown = sorted(n for n, kind in kinds.items() if kind.startswith("SHOWN"))
    births = [e for e in kept_log if e["event"] == "birth"]
    credits = [e for e in kept_log if e["event"] == "credit"]
    senses = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
    summary = {
        "world": Path(world_path).name,
        "intervals": intervals,
        "state hash at the end": end_hash,
        "record hash": record_hash,
        "births": len(births),
        "credits": len(credits),
        "laid back": sum(1 for c in credits if "laid_back" in c),
        "turns": node.counts["turns"],
        "senses summed over the births": sum(senses),
        "taken at or above booked": all(b["taken"] >= b["booked"] for b in births),
        "run back": returned,
        "integers per node": census[0],
        "max bits of the state": census[1],
        "max transient bits": node.max_transient,
        "integers per node constant over the rows": len({row["integers"] for row in rows}) == 1,
        "gates SHOWN": shown,
        "gate 1": found["1 recurring bangs"]["verdict"],
        "gate 46": found["46 the bangs recurring with the same gates"]["verdict"],
        "six lines at the end": six,
        "seconds": round(time.time() - t0, 1),
    }
    Path(out).write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "six lines at the end"}))
    print(json.dumps(six))


if __name__ == "__main__":
    main(sys.argv)
