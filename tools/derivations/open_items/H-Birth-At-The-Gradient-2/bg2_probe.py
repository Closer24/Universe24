"""bg2 (H-Birth-At-The-Gradient-2): one world run N intervals on a named src (FR2_RELEASE and BG2_FORM from the environment), read at every interval: the frozen Nodes, the turned count, the board's content sum, the Nodes that ever froze and their six neighbours (the watch) with their content, X and Link pace, the clicks (births with their Nodes, taken row, children's W, the taken row's share at both ends), the counts' change per interval, and the form's own counters (close.BG2: meetings at a gradient, the twist and the sense that would have stood, the number drawn, the gradient births). Integers only. Usage: bg2_probe.py <src> <world.json> <intervals> <back> <out.jsonl> [feed_now feed_before]"""
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
out = open(sys.argv[5], "w", encoding="utf-8")
out.write(json.dumps({"head": True, "src": sys.argv[1], "world": world_path, "intervals": n, "shape": [int(s) for s in node.shape], "gamma": int(node.gamma), "frozen content": int(paces.frozen_content(node.gamma)), "T": int(node.T), "A": int(node.A), "B": int(node.B), "units": [int(u) for u in node.units], "BG2_FORM": bool(getattr(close, "BG2_FORM", False))}) + "\n")
ever: set = set()
watch: set = set()
hashes = []
seen = 0
last_counts = {k: int(v) for k, v in node.counts.items()}
bg2 = getattr(close, "BG2", None)
for k in range(n):
    if k >= n - back:
        hashes.append(node.state_bytes())
    if bg2 is not None:
        for key in bg2:
            bg2[key] = [] if key == "born" else 0
    node.step()
    carrier = node.row(CARRIER).lines[0]
    c = node.content()
    pace = np.asarray(paces.link_pace_of(node.gamma, c), dtype=object)
    frozen_now = [tuple(int(x) for x in w_) for w_ in zip(*np.nonzero(pace == 0))] if np.ndim(pace) else []
    new = [f for f in frozen_now if f not in ever]
    ever |= set(frozen_now)
    for f in new:
        watch |= set(frame_nodes(node, f))
    clicks = []
    for e in node.log[seen:]:
        if e.get("event") in ("birth", "credit"):
            e2 = {kk: v for kk, v in e.items() if kk not in ("frame", "stood", "taker", "dP_take", "dP_lay")}
            if e.get("event") == "birth":
                mn, pl = tuple(e["minus"]), tuple(e["plus"])
                e2["content_minus_plus"] = [int(c[mn]), int(c[pl])]
                e2["pace_minus_plus"] = [int(pace[mn]), int(pace[pl])]
                e2["X_minus_plus"] = [int(carrier.now[mn]), int(carrier.now[pl])]
                e2["dist_frozen_minus_plus"] = [min([sum(min(abs(a - b), s - abs(a - b)) for a, b, s in zip(w_, f, node.shape)) for f in ever] or [-1]) for w_ in (mn, pl)]
            clicks.append(e2)
    seen = len(node.log)
    counts = {k_: int(v) for k_, v in node.counts.items()}
    delta = {k_: counts[k_] - last_counts.get(k_, 0) for k_ in counts if counts[k_] != last_counts.get(k_, 0)}
    last_counts = counts
    line = {
        "i": int(node.interval),
        "frozen": [list(f) for f in frozen_now],
        "turned": int(node.turned.sum()) if np.ndim(node.turned) else int(node.turned),
        "ever": len(ever),
        "watch": len(watch),
        "content_watch": {str(list(w_)): int(c[w_]) for w_ in sorted(watch)},
        "pace_watch": {str(list(w_)): int(pace[w_]) for w_ in sorted(watch)},
        "X_watch": {str(list(w_)): int(carrier.now[w_]) for w_ in sorted(watch)},
        "board_content_sum": int(sum(int(x) for x in c.reshape(-1))),
        "distinct_pace": int(len(set(int(x) for x in pace.reshape(-1)))),
        "clicks": clicks,
        "counts_delta": delta,
        "bg2": None if bg2 is None else {kk: (v if kk != "born" else list(v)) for kk, v in bg2.items()},
        "max transient": int(node.max_transient),
        "state bits": int(node.census()[1]),
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
