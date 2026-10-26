"""hr2 (H-Horizon-Radiates-2): one world run N intervals on a named src (the flag FR2_RELEASE from the environment), a reading per interval streamed as a JSON line as it comes: the frozen set, the turned among the Nodes that ever froze, the content and X at every Node that ever froze, the sum of content over the horizon's neighbourhood (every Node that ever froze and its six neighbours) against the rest of the board, the credits and births of the interval with their Node, their distance in Links from the nearest Node that ever froze (the torus), their levels, beat, proper and content, the max transient and state bits; then the run back of `back` by the state's hash; the final JSON with the counts and the whole click log (births and credits). Integers only. Usage: hr2_stream.py <src> <world.json> <intervals> <back> <out.jsonl> <final.json> [fed content] [fed before content]"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.core import paces  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

src, world_path, n, back, out_path, final_path = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6]
universe, world = load_world(world_path)
node = Node(universe, world)
shape = tuple(int(s) for s in node.shape)
cube = shape[0]
fed = None
if len(sys.argv) > 8:
    content_fed, before_fed = int(sys.argv[7]), int(sys.argv[8])
    centre = tuple(s // 2 for s in shape)

    def level_at(c):
        return int(np.asarray(volume.volume_of(node.gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0])

    carrier = node.row(CARRIER).lines[0]
    carrier.now[centre] = level_at(content_fed)
    carrier.before[centre] = level_at(before_fed)
    node.ride_walls()
    light = node.emitter().lines[0]
    light.now[centre] = 4 * int(light.now[centre])
    fed = {"centre": list(centre), "content": content_fed, "before": before_fed, "X": level_at(content_fed), "X before": level_at(before_fed)}


def at(i):
    return (i // (cube * cube), (i // cube) % cube, i % cube)


def index(p):
    return p[0] * cube * cube + p[1] * cube + p[2]


def dist(a, b):
    return sum(min((x - y) % cube, (y - x) % cube) for x, y in zip(a, b))


def neighbours(i):
    p = at(i)
    out = set()
    for ax in range(3):
        for d in (-1, 1):
            q = list(p)
            q[ax] = (q[ax] + d) % cube
            out.add(index(tuple(q)))
    return out


ever = []  # the Nodes that ever froze, in order of first freeze
ever_set = set()
hood = set()  # ever frozen and their six neighbours
first_freeze = {}
hashes = []
log_seen = 0
frozen_content = paces.frozen_content(node.gamma)
t0 = time.monotonic_ns()
out = open(out_path, "w", encoding="utf-8")
max_transient = 0
max_state = 0
for t in range(n):
    if back and t >= n - back:
        hashes.append(node.state_hash())
    node.step()
    i = node.interval
    carrier = node.row(CARRIER).lines[0]
    c = node.content()
    cflat = [int(x) for x in np.asarray(c, dtype=object).reshape(-1)]
    xflat = [int(x) for x in np.asarray(carrier.now, dtype=object).reshape(-1)]
    pace = [int(p) for p in np.asarray(paces.link_pace_of(node.gamma, c), dtype=object).reshape(-1)]
    frozen = [k for k, p in enumerate(pace) if p == 0]
    for k in frozen:
        if k not in ever_set:
            ever_set.add(k)
            ever.append(k)
            first_freeze[k] = i
            hood.add(k)
            hood |= neighbours(k)
    turned_flat = node.turned.reshape(-1).tolist()
    new_log = node.log[log_seen:]
    log_seen = len(node.log)
    clicks = []
    for e in new_log:
        if e.get("event") not in ("birth", "credit"):
            continue
        p = tuple(int(v) for v in e["node"])
        d = min((dist(p, at(k)) for k in ever), default=None)
        clicks.append({"event": e["event"], "node": list(p), "index": index(p), "dist": d, "levels": int(e.get("levels", 0)), "beat": int(e.get("beat", 0)) if e["event"] == "credit" else None, "proper": int(e.get("proper", 0)), "content": int(e.get("content", 0)), "sense": e.get("sense"), "line": e.get("line", e.get("line_pair")), "turned": e.get("turned")})
    census = node.census()
    max_transient = max(max_transient, int(node.max_transient))
    max_state = max(max_state, int(census[1]))
    line = {
        "i": i,
        "frozen": frozen,
        "turned_ever": [k for k in ever if turned_flat[k]],
        "content_ever": {str(k): cflat[k] for k in ever},
        "X_ever": {str(k): xflat[k] for k in ever},
        "hood_size": len(hood),
        "hood_content_sum": sum(cflat[k] for k in hood),
        "rest_content_sum": sum(cflat[k] for k in range(len(cflat)) if k not in hood),
        "board_content_sum": sum(cflat),
        "max_content": max(cflat),
        "clicks": clicks,
        "credits": sum(1 for e in clicks if e["event"] == "credit"),
        "births": sum(1 for e in clicks if e["event"] == "birth"),
        "max_transient_bits": int(node.max_transient),
        "state_bits": int(census[1]),
        "ms": (time.monotonic_ns() - t0) // 1000000,
    }
    if fed is not None:
        ci = index(tuple(fed["centre"]))
        line["centre"] = {"content": cflat[ci], "X": xflat[ci], "X_before": int(carrier.before.reshape(-1)[ci]), "turned": bool(turned_flat[ci]), "frozen": pace[ci] == 0, "proper": int(node.proper.reshape(-1)[ci])}
        line["centre_neighbours_content"] = [cflat[k] for k in sorted(neighbours(ci))]
    out.write(json.dumps(line, default=str) + "\n")
    if i % 50 == 0 or i == n:
        out.flush()
out.close()
exact = 0
for k in range(len(hashes)):
    node.step_back()
    exact += node.state_hash() == hashes[len(hashes) - 1 - k]
final = {
    "src": src, "world": world_path, "intervals": n, "fed": fed, "frozen content": frozen_content, "cube": cube,
    "ever frozen": [{"index": k, "node": list(at(k)), "first freeze": first_freeze[k]} for k in ever],
    "hood": sorted(hood), "run back": [exact, len(hashes)],
    "counts": {k: int(v) for k, v in node.counts.items()}, "turns": len(node.turns) if isinstance(node.turns, list) else int(node.turns),
    "max transient bits": max_transient, "max state bits": max_state,
    "ms": (time.monotonic_ns() - t0) // 1000000,
    "clicks": [e for e in node.log if e.get("event") in ("birth", "credit")],
}
json.dump(final, open(final_path, "w"), default=str)
print(json.dumps({k: v for k, v in final.items() if k != "clicks"}, default=str)[:3000])
