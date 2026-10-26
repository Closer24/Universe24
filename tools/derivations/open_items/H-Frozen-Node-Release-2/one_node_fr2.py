"""fr2: the one-Node test of the frozen Node's release on a named src (the flag FR2_RELEASE from the environment): the 3-cube of tests/worlds/world_node.json with its centre fed to the frozen content (X(3,793) = 4,268,834,097), its before slot fed to X at the content `before` (the same content: a standing Node; a lower content: a Node that rose into the horizon in its last interval), the light at the centre four times the sea's; N intervals forward; per interval at the centre: the content, X's bits, the velocity X_now - X_before, the clock's increment, turned, frozen, the frozen count on the board, the max transient and the state's bits; the clicks at the centre; then the run back of N compared by the state's hash. Integers only. Usage: one_node_fr2.py <src> <world.json> <content> <before content> <intervals> <back> <out.json>"""
import copy
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.core import paces  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

world_path, content, before, n, back = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
universe, world = load_world(world_path)
node = Node(universe, world)
CENTRE = tuple(int(s) // 2 for s in node.shape)


def level_at(c):
    return int(np.asarray(volume.volume_of(node.gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0])


carrier = node.row(CARRIER).lines[0]
carrier.now[CENTRE] = level_at(content)
carrier.before[CENTRE] = level_at(before)
node.ride_walls()
light = node.emitter().lines[0]
light.now[CENTRE] = 4 * int(light.now[CENTRE])
frozen_content = paces.frozen_content(node.gamma)
kept = copy.deepcopy(node)
states = []
rows = []
max_state_bits = 0
for k in range(n):
    states.append(node.state_bytes())
    proper = int(node.proper[CENTRE])
    node.step()
    carrier = node.row(CARRIER).lines[0]  # the rows are set anew each interval
    c = node.content()
    pace = np.asarray(paces.link_pace_of(node.gamma, c), dtype=object)
    census = node.census()
    max_state_bits = max(max_state_bits, census[1])
    rows.append(
        {
            "i": node.interval,
            "content": int(c[CENTRE]),
            "X bits": abs(int(carrier.now[CENTRE])).bit_length(),
            "velocity": int(carrier.now[CENTRE]) - int(carrier.before[CENTRE]),
            "clock increment": int(node.proper[CENTRE]) - proper,
            "turned": bool(node.turned[CENTRE]),
            "frozen": bool(pace[CENTRE] == 0),
            "frozen count": int((pace == 0).sum()),
            "max content": int(max(int(x) for x in c.reshape(-1))),
            "max transient": int(node.max_transient),
            "state bits": int(census[1]),
        }
    )
clicks = [e for e in node.log if tuple(e["node"]) == CENTRE and e["event"] in ("birth", "credit")]
back_ok = 0
for k in range(back):
    node.step_back()
    back_ok += node.state_bytes() == states[n - 1 - k]
out = {
    "src": sys.argv[1], "world": world_path, "content": content, "before": before, "intervals": n,
    "X fed": level_at(content), "X before fed": level_at(before), "frozen content": frozen_content,
    "clicks at centre": len(clicks), "first clicks": clicks[:5],
    "max transient": int(node.max_transient), "max state bits": max_state_bits,
    "run back": [back_ok, back], "counts": {k: int(v) for k, v in node.counts.items()},
    "first frozen interval": next((r["i"] for r in rows if r["frozen"]), None),
    "first unfrozen after": next((r["i"] for r in rows if r["turned"]), None),
    "turned intervals": [r["i"] for r in rows if r["turned"]][:50],
    "frozen intervals count": sum(1 for r in rows if r["frozen"]),
    "clock increments sum": sum(r["clock increment"] for r in rows),
    "course": rows[:30] + rows[30::max(1, n // 40)],
}
json.dump(out, open(sys.argv[7], "w"), default=str, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "course"}, default=str)[:3000])
print("course head", json.dumps(rows[:8], default=str))
