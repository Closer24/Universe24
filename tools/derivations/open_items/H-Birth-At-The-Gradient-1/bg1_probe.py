"""bg1 (H-Birth-At-The-Gradient-1): one world run N intervals on a named src (FR2_RELEASE and BG1_FORM from the environment), read per interval: the frozen Nodes, the hovering set (every Node ever frozen and its six neighbours) with its content, the board's content sum, every click (birth, credit, gradient meeting) with its Node's Link distance from the ever-frozen set, the counts' change, the bits; the children of every birth followed on their record's share at their Nodes for 60 intervals (the course). Integers only. Usage: bg1_probe.py <src> <world.json> <intervals> <back> <out.jsonl> [feed_now feed_before]"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe import close  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402
from event_universe.take import frame_nodes  # noqa: E402

world_path, n, back = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
universe, world = load_world(world_path)
world = dict(world, intervals=n)
node = Node(universe, world)
if len(sys.argv) > 7:
    centre = tuple(s // 2 for s in node.shape)
    car = node.row(CARRIER).lines[0]
    car.now[centre], car.before[centre] = int(sys.argv[6]), int(sys.argv[7])
    node.start_content, node.start_x = node.content(), car.now
shape = [int(s) for s in node.shape]
out = open(sys.argv[5], "w", encoding="utf-8")
out.write(json.dumps({"head": True, "src": sys.argv[1], "world": world_path, "intervals": n, "shape": shape, "gamma": int(node.gamma), "frozen content": int(paces.frozen_content(node.gamma)), "units": [int(u) for u in node.units]}) + "\n")


def distance(a, frozen_set):
    """The least Link distance on the torus from a Node to a set (the sum over the axes of the wrapped difference)."""
    best = None
    for f in frozen_set:
        d = sum(min(abs(x - y), s - abs(x - y)) for x, y, s in zip(a, f, shape))
        best = d if best is None or d < best else best
    return best


ever: set = set()
watch: set = set()
course: dict = {}
shares: dict = {}
meet0 = close.meet


def meet_probe(nd, rec, start, sh, rules, frozen):
    for key in list(course):
        s, where, since = key
        if s == rec:
            shares.setdefault(str(key), []).append([int(nd.interval), int(sh[where])])
    return meet0(nd, rec, start, sh, rules, frozen)


close.meet = meet_probe
hashes = []
seen = 0
last_counts = {k: int(v) for k, v in node.counts.items()}
for k in range(n):
    if k >= n - back:
        hashes.append(node.state_bytes())
    node.step()
    c = node.content()
    pace = np.asarray(paces.link_pace_of(node.gamma, c), dtype=object)
    frozen_now = [tuple(int(x) for x in w_) for w_ in zip(*np.nonzero(pace == 0))] if np.ndim(pace) else []
    new = [f for f in frozen_now if f not in ever]
    ever |= set(frozen_now)
    for f in new:
        watch |= set(frame_nodes(node, f))
    clicks = []
    for e in node.log[seen:]:
        if e.get("event") in ("birth", "credit", "gradient"):
            e2 = {kk: v for kk, v in e.items() if kk != "frame"}
            e2["distance_from_frozen"] = distance(tuple(e["node"]), ever) if ever else None
            if e.get("event") == "birth":
                e2["content_minus_plus"] = [int(c[tuple(e["minus"])]), int(c[tuple(e["plus"])])]
                for end in ("minus", "plus"):
                    course[(int(e["line_pair"]), tuple(e[end]), int(node.interval))] = True
            clicks.append(e2)
    seen = len(node.log)
    for key in list(course):
        if node.interval - key[2] > 60:
            del course[key]
    counts = {k_: int(v) for k_, v in node.counts.items()}
    delta = {k_: counts[k_] - last_counts.get(k_, 0) for k_ in counts if counts[k_] != last_counts.get(k_, 0)}
    last_counts = counts
    line = {
        "i": int(node.interval),
        "frozen": [list(f) for f in frozen_now],
        "ever": len(ever),
        "content_watch": {str(list(w_)): int(c[w_]) for w_ in sorted(watch)},
        "board_content_sum": int(sum(int(x) for x in c.reshape(-1))),
        "clicks": clicks,
        "counts_delta": delta,
        "max transient": int(node.max_transient),
        "state bits": int(node.census()[1]),
    }
    out.write(json.dumps(line, default=str) + "\n")
    out.flush()
ok = 0
for k in range(back):
    node.step_back()
    ok += node.state_bytes() == hashes[back - 1 - k]
out.write(json.dumps({"tail": True, "run back": [ok, back], "counts": {k: str(v) for k, v in node.counts.items()}, "max transient": int(node.max_transient), "course": shares}) + "\n")
out.close()
print(json.dumps({"run back": [ok, back], "counts": {k: str(v) for k, v in node.counts.items()}}))
