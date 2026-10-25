"""un1's record runner (vf2's form): the engine's own forward and run back (event_universe.run) from whichever src PYTHONPATH names,
the state hash at the end of the forward run, the counts, the turns, the log's digest and length, the rows' digest (milliseconds
apart), the Node lines' digest, the max transient and the census; one JSON line printed and one JSON file written.
Usage: runner.py <world.json> <out.json> <back>"""

from __future__ import annotations

import hashlib
import json
import os
import sys

from event_universe import rows as rows_module
from event_universe.loader.world import load_world
from event_universe.node import Node
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


def digest(x: object) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, default=str).encode()).hexdigest()[:16]


births = [e for e in kept_log if e["event"] == "birth"]
credits = [e for e in kept_log if e["event"] == "credit"]
signs = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
summary = {
    "world": os.path.basename(sys.argv[1]),
    "flag": os.environ.get("UN1_FREE", ""),
    "src": [p for p in sys.path if "src" in p][:1],
    "free_in_module": bool(getattr(rows_module, "FREE", False)),
    "state_hash": state_hash[:16],
    "census": list(census),
    "max_transient": max_transient,
    "counts": counts,
    "turns_total": sum(n for _i, n in node.turns),
    "log_lines": len(kept_log),
    "log_digest": digest(kept_log),
    "rows_digest": digest([{k: v for k, v in row.items() if k != "milliseconds"} for row in rows]),
    "nodes_digest": digest(nodes),
    "run_back": returned,
    "births": len(births),
    "credits": len(credits),
    "charge_at_births": sum(signs),
    "zero_senses": signs.count(0),
    "taken_ge_booked": sum(1 for b in births if b["taken"] >= b["booked"]),
    "units": [str(u) for u in node.units],
    "unit_gap0": str(node.unit_gap0),
}
with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump(summary, f)
print(json.dumps(summary))
