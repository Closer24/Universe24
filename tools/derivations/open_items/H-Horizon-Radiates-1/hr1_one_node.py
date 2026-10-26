"""hr1: the fed one-Node world (tests/worlds/world_node.json, the 3-cube) on a named src (FR2_RELEASE from the environment): the centre fed to the frozen content, its before slot to the content `before` (the same: standing; lower: risen into the horizon), the light at the centre four times the sea's; N intervals streamed one JSON line per interval: the content and X at the centre and its six neighbours, turned, frozen, the clicks of the interval (births, credits, no frame); then the run back compared by the state's hash. Integers only. Usage: hr1_one_node.py <src> <world.json> <before offset> <intervals> <back> <out.jsonl>"""
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

world_path, offset, n, back = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
universe, world = load_world(world_path)
node = Node(universe, world)
CENTRE = tuple(int(s) // 2 for s in node.shape)
frozen = int(paces.frozen_content(node.gamma))
content, before = frozen, frozen - offset


def level_at(c):
    return int(np.asarray(volume.volume_of(node.gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0])


carrier = node.row(CARRIER).lines[0]
carrier.now[CENTRE] = level_at(content)
carrier.before[CENTRE] = level_at(before)
node.ride_walls()
light = node.emitter().lines[0]
light.now[CENTRE] = 4 * int(light.now[CENTRE])
cube = int(node.shape[0])
cx, cy, cz = CENTRE
nb = [((cx + d) % cube, cy, cz) for d in (1, -1)] + [(cx, (cy + d) % cube, cz) for d in (1, -1)] + [(cx, cy, (cz + d) % cube) for d in (1, -1)]
out = open(sys.argv[6], "w", encoding="utf-8")
out.write(json.dumps({"head": True, "world": world_path, "content": content, "before": before, "frozen content": frozen, "centre": list(CENTRE), "neighbours": [list(p) for p in nb], "X fed": level_at(content), "X before fed": level_at(before)}) + "\n")
hashes = []
seen = 0
for k in range(n):
    if k >= n - back:
        hashes.append(node.state_bytes())
    proper = int(node.proper[CENTRE])
    node.step()
    carrier = node.row(CARRIER).lines[0]
    c = node.content()
    pace = np.asarray(paces.link_pace_of(node.gamma, c), dtype=object)
    clicks = [{kk: v for kk, v in e.items() if kk != "frame"} for e in node.log[seen:] if e.get("event") in ("birth", "credit")]
    seen = len(node.log)
    line = {
        "i": int(node.interval), "content": int(c[CENTRE]), "X": int(carrier.now[CENTRE]), "Xb": int(carrier.before[CENTRE]),
        "clock increment": int(node.proper[CENTRE]) - proper, "turned": bool(node.turned[CENTRE]), "frozen": bool(pace[CENTRE] == 0),
        "frozen count": int((pace == 0).sum()), "neighbours content": [int(c[p]) for p in nb], "board content": [int(x) for x in c.reshape(-1).tolist()],
        "clicks": clicks, "max transient": int(node.max_transient), "state bits": int(node.census()[1]),
    }
    out.write(json.dumps(line, default=str) + "\n")
    out.flush()
ok = 0
for k in range(back):
    node.step_back()
    ok += node.state_bytes() == hashes[back - 1 - k]
out.write(json.dumps({"tail": True, "run back": [ok, back], "counts": {k: str(v) for k, v in node.counts.items()}, "max transient": int(node.max_transient)}) + "\n")
out.close()
print(json.dumps({"run back": [ok, back], "counts": {k: str(v) for k, v in node.counts.items()}}))
