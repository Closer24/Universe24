"""hp2 (H-Horizon-Pair-At-The-Turn-2): one world run N intervals on a named src (FR2_RELEASE from the environment), the close's own letter read at every Node that ever froze and at its six neighbours at every interval from the first freeze on: for every record, the standing share against the unit (meet's `standing`), the frozen mask, the taken row's current and twist on the six Links (meet's refusals by name), and the carrier's own Link term SUM_j R_j (m_j - now) on its time line against the write's numerator over its write wall (the letter's Link term at the horizon); the refusals and meetings counted per interval. Integers only. Usage: hp2_probe.py <src> <world.json> <intervals> <back> <out.jsonl> [feed_now feed_before]"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe import close, readings  # noqa: E402
from event_universe.core import paces, rule3  # noqa: E402
from event_universe.core.ports import PORTS  # noqa: E402
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
out.write(json.dumps({"head": True, "src": sys.argv[1], "world": world_path, "intervals": n, "shape": [int(s) for s in node.shape], "gamma": int(node.gamma), "frozen content": int(paces.frozen_content(node.gamma)), "T": int(node.T), "A": int(node.A), "B": int(node.B), "units": [int(u) for u in node.units]}) + "\n")

ever: set = set()
watch: set = set()
probe: dict = {}
meet0 = close.meet


def meet_probe(nd, rec, start, sh, rules, frozen):
    unit = nd.units[rec]
    if watch:
        rows = {}
        for at in sorted(watch):
            share = int(sh[at])
            rows[str(list(at))] = [share, int(share >= unit), int(frozen[at])]
        probe.setdefault("records", {})[str(rec)] = {"unit": int(unit), "shares": rows}
    return meet0(nd, rec, start, sh, rules, frozen)


close.meet = meet_probe
carried0 = node.carried


def carried_probe(lines, r, numerators, direction, top, kept):
    if watch and direction == 1:
        at = [lines[0].now]
        arr = node.arrivals(at, r, None)[0]
        link_term = arr - sum(r.reaches) * at[0]
        rows = {}
        for w_ in sorted(watch):
            q_num = int(numerators[0][w_])
            rows[str(list(w_))] = {
                "link_term": int(link_term[w_]),
                "link_term_div_w": int(link_term[w_]) // int(r.wall) if np.ndim(r.wall) == 0 else int(link_term[w_]) // int(r.wall[w_]),
                "reaches": [int(x[w_]) if np.ndim(x) else int(x) for x in r.reaches],
                "wall": int(r.wall) if np.ndim(r.wall) == 0 else int(r.wall[w_]),
                "mass": int(r.mass) if np.ndim(r.mass) == 0 else int(r.mass[w_]),
                "write_num": q_num,
                "write_q": q_num // int(lines[0].wwall),
                "X_now": int(lines[0].now[w_]),
                "X_before": int(lines[0].before[w_]),
                "neighbours_X": [int(lines[0].now[j]) for j in frame_nodes(node, w_)[1:]],
            }
        probe["carrier"] = rows
    return carried0(lines, r, numerators, direction, top, kept)


node.carried = carried_probe
hashes = []
seen = 0
last_counts = {k: int(v) for k, v in node.counts.items()}
for k in range(n):
    if k >= n - back:
        hashes.append(node.state_bytes())
    probe = {}
    node.step()
    carrier = node.row(CARRIER).lines[0]
    c = node.content()
    pace = np.asarray(paces.link_pace_of(node.gamma, c), dtype=object)
    frozen_now = [tuple(int(x) for x in w_) for w_ in zip(*np.nonzero(pace == 0))] if np.ndim(pace) else []
    new = [f for f in frozen_now if f not in ever]
    ever |= set(frozen_now)
    for f in new:
        watch |= set(frame_nodes(node, f))
    clicks = [{kk: v for kk, v in e.items() if kk != "frame"} for e in node.log[seen:] if e.get("event") in ("birth", "credit")]
    seen = len(node.log)
    counts = {k_: int(v) for k_, v in node.counts.items()}
    delta = {k_: counts[k_] - last_counts.get(k_, 0) for k_ in counts if counts[k_] != last_counts.get(k_, 0)}
    last_counts = counts
    line = {
        "i": int(node.interval),
        "frozen": [list(f) for f in frozen_now],
        "turned": [[int(x) for x in w_] for w_ in zip(*np.nonzero(node.turned))],
        "ever": len(ever),
        "watch": len(watch),
        "content_watch": {str(list(w_)): int(c[w_]) for w_ in sorted(watch)},
        "X_watch": {str(list(w_)): int(carrier.now[w_]) for w_ in sorted(watch)},
        "board_content_sum": int(sum(int(x) for x in c.reshape(-1))),
        "clicks": clicks,
        "counts_delta": delta,
        "probe": probe,
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
