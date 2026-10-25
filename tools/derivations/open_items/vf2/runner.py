"""vf2's record runner: the engine's own forward and run back (event_universe.run), the state hash at the end of the forward run, the counts, the turns, the rows (without milliseconds), the log, the Node lines, the max transient and the census, and the gates' output; one JSON out. Usage: runner.py <world.json> <out.json> <back>."""

from __future__ import annotations

import json
import sys

from event_universe.gates import gates
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.core.paces import sine_den
from event_universe.run import forward, run_back

sys.set_int_max_str_digits(0)
universe, world = load_world(sys.argv[1])
back = int(sys.argv[3])
node = Node(universe, world)
intervals = int(world["intervals"])
rows, nodes, hashes = forward(node, intervals, back, lambda line: None)
state_hash = node.state_hash()
census = node.census()
max_transient = node.max_transient
kept_log = list(node.log)
returned = run_back(node, hashes)
counts = {k: str(v) for k, v in node.counts.items()}
record = {
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
record = json.loads(json.dumps(record))
found = gates(record)
out = {
    "state_hash": state_hash,
    "census": list(census),
    "max_transient": max_transient,
    "counts": counts,
    "turns": record["turns"],
    "rows": [{k: v for k, v in row.items() if k != "milliseconds"} for row in record["rows"]],
    "nodes": record["nodes"],
    "log": record["log"],
    "run_back": returned,
    "gates": found,
}
with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump(out, f)
print(sys.argv[1], state_hash, counts, returned, "transient", max_transient, "census", census)
