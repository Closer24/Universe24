"""Run one world N intervals with the run back 10 on a named src; the record compared with a cached record where one is named; the tallies of the derivation (takes on a line with no write wall, births at a Node whose gap-0 current sums 0). Usage: run_cr2.py <src> <world.json> <intervals> <out.json> [cached.json]"""
import json
import sys

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe import close, take, bodies  # noqa: E402
from event_universe.core.ports import PORTS  # noqa: E402
from event_universe.links import row_current  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.run import record  # noqa: E402

tally = {"takes": 0, "takes_no_write_wall": 0, "takes_im_line": 0, "births_kept": 0, "births_net0": 0, "merger_takes": 0}
_fall = take.fall_of


def fall_of(node, at, walls, r, row):
    got = _fall(node, at, walls, r, row)
    if got[0] is not None:
        tally["takes"] += 1
        if row.lines[got[2]].wwall is None:
            tally["takes_no_write_wall"] += 1
        if got[2] == 1:
            tally["takes_im_line"] += 1
        if row is not node.emitter():
            tally["merger_takes"] += 1
    return got


take.fall_of = fall_of
starts = {}
_click = close.click


def click(node, plane_starts, held, direction=1, frame=None):
    starts["p"] = plane_starts
    return _click(node, plane_starts, held, direction, frame)


_births = close.births


def births(node, kept, c, factors):
    rec0 = node.records().index(node.emitter())
    net = sum((row_current(starts["p"][rec0], port) for port in range(PORTS)), start=0)
    for b in kept:
        tally["births_kept"] += 1
        if int(net[b.at]) == 0:
            tally["births_net0"] += 1
    return _births(node, kept, c, factors)


close.click, close.births = click, births
u, w = load_world(sys.argv[2])
w = dict(w, intervals=int(sys.argv[3]))
found = record(u, w, 10, lambda line: None)
with open(sys.argv[4], "w", encoding="utf-8") as out:
    json.dump(found, out, default=str)
summary = {"world": sys.argv[2], "intervals": sys.argv[3], "counts": found.get("counts"), "run_back": found.get("run_back"), "max_bits": max(int(r["max bits"]) for r in found["rows"]), "tally": tally}
if len(sys.argv) > 5:
    cached = json.load(open(sys.argv[5]))
    same = {k: found.get(k) == cached.get(k) for k in sorted(set(found) | set(cached))}
    summary["against_cached"] = {"keys_equal": same, "all_equal": all(same.values())}
    if not all(same.values()):
        lb, lc = found.get("log", []), cached.get("log", [])
        first = next((k for k, (a, b) in enumerate(zip(lb, lc)) if a != b), None)
        summary["first_apart_log_entry"] = None if first is None else {"index": first, "found": lb[first], "cached": lc[first]}
        summary["log_lengths"] = [len(lb), len(lc)]
print(json.dumps(summary, default=str))
