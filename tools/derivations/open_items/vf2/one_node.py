"""vf2's reading of the BH-S1 one-Node world: the 3-cube centre fed to the frozen content (paces.frozen_content at Gamma), 100 intervals; at every interval X at the centre, the proper count, the six factors at the centre and the neighbours' matching Ports, the frozen count, the clicks at the centre, the transient; then the run back 100 of 100 on a deep copy. Usage: one_node.py <world_node.json> <intervals>."""

from __future__ import annotations

import copy
import json
import sys

import numpy as np

from event_universe import readings
from event_universe.core import paces
from event_universe.features import volume
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER
from event_universe.take import frame_nodes

sys.set_int_max_str_digits(0)
universe, world = load_world(sys.argv[1])
n_intervals = int(sys.argv[2])
node = Node(universe, world)
centre = (1, 1, 1)
frozen_content = paces.frozen_content(node.gamma)
carrier = node.row(CARRIER).lines[0]
level = int(np.asarray(volume.volume_of(node.gamma, np.array([frozen_content], dtype=object)), dtype=object).reshape(-1)[0])
carrier.now[centre] = level
carrier.before[centre] = level
node.ride_walls()
fed = [[int(a[centre]) for a in (line.now, line.before, line.rem)] for line in node.all_lines()]
fed_wr = [int(line.wr[centre]) for line in node.all_lines() if line.wr is not None]
proper0 = int(node.proper[centre])
print(json.dumps({"gamma": node.gamma, "frozen content": frozen_content, "X fed": level, "lines": len(node.all_lines()), "proper at start": proper0}))
kept = copy.deepcopy(node)
x_values = set()
proper_values = set()
factor_values = set()
neighbour_factor_values = set()
frozen_counts = set()
lines_equal = 0
wr_equal = 0
turned_ever = 0
for _ in range(n_intervals):
    node.step()
    lines = node.all_lines()
    now = [[int(a[centre]) for a in (line.now, line.before, line.rem)] for line in lines]
    lines_equal += now == fed
    wr_equal += [int(line.wr[centre]) for line in lines if line.wr is not None] == fed_wr
    x_values.add(int(carrier.now[centre]))
    proper_values.add(int(node.proper[centre]))
    turned_ever += bool(node.turned[centre])
    content = node.content()
    mask = np.asarray(readings.frozen_of(node, content), dtype=bool)
    frozen_counts.add(int(mask.sum()))
    factors = node.link_factors(None, mask)
    factor_values.update(int(f[centre]) for f in factors)
    neighbour_factor_values.update(int(factors[port ^ 1][nb]) for port, nb in enumerate(frame_nodes(node, centre)[1:]))
clicks = [e for e in node.log if tuple(e["node"]) == centre and e["event"] in ("birth", "credit")]
ends = [e for e in node.log if e["event"] == "birth" and centre in (tuple(e["minus"]), tuple(e["plus"]))]
summary = {
    "intervals": n_intervals,
    "X at the centre (set over the intervals)": sorted(x_values),
    "proper at the centre (set)": sorted(proper_values),
    "proper at start": proper0,
    "lines equal to the fed at every interval": lines_equal,
    "write remainders equal": wr_equal,
    "six factors at the centre (set)": sorted(factor_values),
    "neighbours' matching Port factors (set)": sorted(neighbour_factor_values),
    "frozen count (set)": sorted(frozen_counts),
    "turned at the centre ever": turned_ever,
    "clicks at the centre": len(clicks),
    "births with a child at the centre": len(ends),
    "clicks on the board (log length)": len(node.log),
    "births on the board": sum(e["event"] == "birth" for e in node.log),
    "max transient": node.max_transient,
    "census": list(node.census()),
    "counts": {k: str(v) for k, v in node.counts.items()},
}
print(json.dumps(summary))
hashes = []
back = kept
for _ in range(n_intervals):
    hashes.append(back.state_hash())
    back.step()
exact = 0
for k in range(n_intervals):
    back.step_back()
    exact += back.state_hash() == hashes[n_intervals - 1 - k]
print(json.dumps({"run back": {"intervals": n_intervals, "exact": exact}}))
