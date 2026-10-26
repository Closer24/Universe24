"""vf12: the taken line re-derived by this hand's own code at every take's moment (the line with the largest now^2 - before^2 at the take's Node, the first where equal, read from the taken row's levels before the engine's take_at runs), compared with the line the engine returns and logs; the merger's order (both ends pre-read by fall_of before either take_at writes); the takes per line; the run back exact. The engine's close.take_at, bodies.take_at and close.fall_of are wrapped by name (take.py's own functions untouched). Integers only.
Usage: python replay_takes.py <worktree> pair|merger|cycle [cycle folder]"""

from __future__ import annotations

import copy
import json
import sys
from collections import Counter

sys.set_int_max_str_digits(0)
W = sys.argv[1]
sys.path.insert(0, W)
from event_universe import bodies, close, take  # noqa: E402
from event_universe.rows import CARRIER, PLANE  # noqa: E402
from tests.laws import node_of, run_back_exact  # noqa: E402

trace: list[tuple] = []
order: list[tuple] = []
mismatch: list[tuple] = []
orig_take_at, orig_fall_of = take.take_at, take.fall_of


def my_line(node, at, rec):
    row = node.records()[rec]
    gaps = [int(line.now[at]) ** 2 - int(line.before[at]) ** 2 for line in row.lines]
    best = gaps[0]
    for g in gaps:
        if g > best:
            best = g
    k = 0
    while gaps[k] != best:
        k += 1
    return k, gaps


def take_at_w(node, at, walls, rule, cause, rec=None):
    taken = node.records().index(node.row(PLANE, gap=0)) if rec is None else rec
    k, gaps = my_line(node, at, taken)
    got = orig_take_at(node, at, walls, rule, cause, rec)
    order.append(("take", node.interval, tuple(at), taken, k, got is not None))
    if got is not None:
        if got[4] != k:
            mismatch.append(("take", node.interval, tuple(at), taken, k, got[4], gaps))
        trace.append((node.interval, tuple(at), taken, k))
    return got


def fall_of_w(node, at, walls, r, row):
    rec = node.records().index(row)
    k, gaps = my_line(node, at, rec)
    got = orig_fall_of(node, at, walls, r, row)
    if got[2] != k:
        mismatch.append(("pre-read", node.interval, tuple(at), rec, k, got[2], gaps))
    order.append(("read", node.interval, tuple(at), rec, k, got[0] is not None))
    return got


close.take_at = take_at_w
bodies.take_at = take_at_w
close.fall_of = fall_of_w


def logged(node):
    rec0 = node.records().index(node.row(PLANE, gap=0))
    found = []
    for e in node.log:
        if e["event"] not in ("birth", "credit"):
            continue
        rec = e.get("taken_row", rec0)
        for t in e.get("takes", [e]):
            found.append((e["i"], tuple(t["node"]), rec, t["taken_line"]))
    return found


def merger_order(node):
    """For every merger (a birth with two takes): the two pre-reads precede both takes in the call order."""
    verdicts = []
    for e in node.log:
        if e["event"] != "birth" or "takes" not in e:
            continue
        i, ends = e["i"], [tuple(t["node"]) for t in e["takes"]]
        rec = e["taken_row"]
        reads = [n for n, o in enumerate(order) if o[0] == "read" and o[1] == i and o[2] in ends and o[3] == rec]
        takes = [n for n, o in enumerate(order) if o[0] == "take" and o[1] == i and o[2] in ends and o[3] == rec]
        ok = len(reads) >= 2 and len(takes) >= 2 and max(reads[:2]) < min(takes)
        verdicts.append((i, ends, e["taken_line"], reads[:2], takes[:2], ok))
    return verdicts


def report(name, node, kept, back):
    mine, theirs = Counter(trace), Counter(logged(node))
    lines = Counter(k for _, _, _, k in trace)
    print(name, "| takes traced", sum(mine.values()), "| takes logged", sum(theirs.values()), "| equal as multisets", mine == theirs, "| mismatches of the line (mine against the engine's)", len(mismatch), mismatch[:3])
    print("  takes per line (line: count)", dict(sorted(lines.items())), "| births", node.counts["births"], "| credits", node.counts["body_clicks"], "| laid back", node.counts["laid_back"], "| stops", node.counts["refused_stop"])
    stops = [e for e in node.log if e["event"] == "refused" and e["cause"] == "stop"]
    print("  stops logged", len(stops), "| at intervals", sorted({e["i"] for e in stops})[:12])
    births = [e for e in node.log if e["event"] == "birth"]
    print("  births", len(births), "| charge at every birth (W_children summed 0):", all(sum(int(x) for x in e["W_children"]) == 0 for e in births) if births else "no birth", "| taken at or above booked", sum(1 for e in births if int(e["taken"]) >= int(e["booked"])), "of", len(births))
    mo = merger_order(node)
    print("  mergers", len(mo), "| both ends read before either written", all(v[5] for v in mo), mo[:3])
    print("  run back exact from the seed:", run_back_exact(kept, back), "of", back)


def pair():
    pair, image = node_of("world_pair_3.json"), node_of("world_pair_3.json")
    re, im = image.row(PLANE, gap=0).lines
    im.now[...], im.before[...], re.now[...], re.before[...] = re.now.copy(), re.before.copy(), 0, 0
    kept = copy.deepcopy(image)
    x_equal = 0
    for _ in range(20):
        pair.step()
        image.step()
        x_equal += bool((pair.row(CARRIER).lines[0].now == image.row(CARRIER).lines[0].now).all())
    c = [[(e["i"], e["node"], e["taken"], e["levels"], e["taker"], e["taken_line"]) for e in n.log if e["event"] == "credit"] for n in (pair, image)]
    print("pair beside its quarter-turned image | X equal at every Node at", x_equal, "of 20 | credits", len(c[0]), len(c[1]), "| equal take for take in (i, node, taken, levels, taker)", [x[:5] for x in c[0]] == [x[:5] for x in c[1]], "| lines on the board", sorted({x[5] for x in c[0]}), "| on the image", sorted({x[5] for x in c[1]}))
    print("  the image's re line at 0 at every credited Node:", all(int(re.now[tuple(x[1])]) == int(re.before[tuple(x[1])]) == 0 for x in c[1]))
    report("image", image, kept, 10)
    print("  run back exact 20:", run_back_exact(copy.deepcopy(kept), 20), "of 20")


def merger():
    node = node_of("world_node.json", shape=[5, 5, 5], seed=[])
    a, b, k = node.A, node.B, 3
    heavy = max(range(len(node.records())), key=lambda r: node.records()[r].gap or 0)
    for at, levels in (((1, 1, 1), (k * a, 0, 0, k * b)), ((2, 1, 1), (k * a, b, 0, -k * b)), ((1, 2, 1), (a, b, 0, 0)), ((2, 1, 2), (b, a, 0, 0))):
        node.lay(heavy, at, levels)
    kept = copy.deepcopy(node)
    for _ in range(20):
        node.step()
    births = [e for e in node.log if e["event"] == "birth"]
    first = births[0]
    refusals = [e for e in node.log if e["event"] == "refused" and e.get("row") == heavy and e["i"] <= first["i"]]
    on_first = [(e["i"], t["taken_line"]) for e in births for t in e.get("takes", [e]) if not t["taken_line"]]
    print("merger board | the first birth at i", first["i"], "| taken_row heavy", first["taken_row"] == heavy, "| taken_line", first["taken_line"], "| heavy-row refusals at or before it", len(refusals), "| births", len(births), "| takes on the first line", on_first)
    report("merger board", node, kept, 10)
    print("  run back exact 20:", run_back_exact(copy.deepcopy(kept), 20), "of 20")


def cycle(folder):
    sys.path.insert(0, folder)
    import cs6_run  # noqa: E402
    from event_universe.loader.world import load_world  # noqa: E402

    universe, world = load_world(folder + "/worlds/empty4_ga2_450.json")
    with open(folder + "/worlds/cycle_m5_m0.json", encoding="utf-8") as f:
        pattern = json.load(f)
    node = cs6_run.Cs6Node(universe, world, pattern)
    phases = node.lay_line["phases"]
    cube = node.cube
    kept = copy.deepcopy(node)
    n = int(world["intervals"])
    for _ in range(n):
        node.step()
    at2 = [(at, k) for i, at, rec, k in trace if i == 2]
    by_line = Counter(k for _, k in at2)
    by_class = Counter((phases[(at[0] * cube + at[1]) * cube + at[2]], k) for at, k in at2)
    print("cycle board (ga2, 4-cube, cycle_m5_m0, no flag) to", n, "| takes at i 2:", len(at2), "at", len({at for at, _ in at2}), "Nodes | by line", dict(by_line), "| by (phase class, line)", dict(sorted(by_class.items())))
    report("cycle board", node, kept, 10)


if __name__ == "__main__":
    {"pair": pair, "merger": merger}.get(sys.argv[2], lambda: cycle(sys.argv[3]))()
