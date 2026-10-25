"""vf2's chiral seed to N intervals at the 54-bit den: the frozen mask read after every interval (readings.frozen_of on the content, the mask of the next interval's start), every Node's first freeze logged with the interval, its content, whether any of its six neighbours froze earlier, and the neighbours' contents; the count at the marks; unfreezes counted; the max transient and the census; the run back over the last `back` intervals. Usage: frozen_8000.py <world.json> <out.json> <back>."""

from __future__ import annotations

import json
import sys
import time

import numpy as np

from event_universe import readings
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.take import frame_nodes

sys.set_int_max_str_digits(0)
universe, world = load_world(sys.argv[1])
back = int(sys.argv[3])
node = Node(universe, world)
intervals = int(world["intervals"])
marks = {7129, 7200, 7600, 8000, 2400, 4000, 6000}
first_frozen: dict[tuple[int, ...], dict] = {}
count_at: dict[int, int] = {}
unfreezes = 0
previous = np.zeros(node.shape, dtype=bool)
hashes = []
t0 = time.monotonic_ns()
for t in range(intervals):
    if t >= intervals - back:
        hashes.append(node.state_hash())
    node.step()
    content = node.content()
    mask = np.asarray(readings.frozen_of(node, content), dtype=bool)
    unfreezes += int((previous & ~mask).sum())
    new = mask & ~previous
    if new.any():
        for at in zip(*np.nonzero(new), strict=True):
            at = tuple(int(a) for a in at)
            neighbours = frame_nodes(node, at)[1:]
            earlier = [
                (list(n), first_frozen[n]["interval"]) for n in neighbours if n in first_frozen
            ]
            first_frozen[at] = {
                "interval": node.interval,
                "content": int(content[at]),
                "neighbours frozen earlier": earlier,
                "neighbours' contents": [int(content[n]) for n in neighbours],
                "neighbours frozen at this interval": [list(n) for n in neighbours if mask[n]],
                "count after": int(mask.sum()),
            }
    previous = mask
    if node.interval in marks or node.interval % 1000 == 0:
        count_at[node.interval] = int(mask.sum())
        print(
            json.dumps(
                {
                    "interval": node.interval,
                    "frozen count": int(mask.sum()),
                    "max transient": node.max_transient,
                    "census": list(node.census()),
                    "seconds": (time.monotonic_ns() - t0) // 10**9,
                }
            ),
            flush=True,
        )
    if first_frozen and len(first_frozen) == 1 and node.interval % 100 == 0:
        at = next(iter(first_frozen))
        print(json.dumps({"interval": node.interval, "first frozen node": list(at), "content": int(content[at])}), flush=True)
final_mask = previous
census = node.census()
max_transient = node.max_transient
exact = 0
for k in range(len(hashes)):
    node.step_back()
    exact += node.state_hash() == hashes[len(hashes) - 1 - k]
out = {
    "intervals": intervals,
    "first frozen": {str(list(k)): v for k, v in sorted(first_frozen.items(), key=lambda kv: kv[1]["interval"])},
    "count at marks": count_at,
    "final frozen count": int(final_mask.sum()),
    "unfreezes": unfreezes,
    "max transient": max_transient,
    "census": list(census),
    "counts": {k: str(v) for k, v in node.counts.items()},
    "run back": {"intervals": len(hashes), "exact": exact},
}
with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "first frozen"}))
