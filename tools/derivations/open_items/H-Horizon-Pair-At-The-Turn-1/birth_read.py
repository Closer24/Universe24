"""hp1: the close's own condition for a birth (close.meet) read at every interval's start at the Nodes frozen at that start, the Nodes turned at the previous interval (the released) and their six neighbours: per record the share in the record's unit (standing where share >= unit), the record's current on the three axes at the Node, its twist, its charge; the carrier's X, the content, the frozen and turned masks. Steps the engine under the environment's flags. Usage: birth_read.py <src> <world.json> <intervals> <out.jsonl> [feed_content feed_before] (the 3-cube's centre fed as the one-Node runners feed it)"""
import json, sys
import numpy as np
sys.path.insert(0, sys.argv[1]); sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER
from event_universe import readings, gram
from event_universe.features import volume
from event_universe.core.ports import AXES, port_of
from event_universe.links import row_current, row_twist
u, w = load_world(sys.argv[2]); n = int(sys.argv[3]); w = dict(w, intervals=n); node = Node(u, w)
if len(sys.argv) > 6:
    centre = tuple(x // 2 for x in node.shape); car = node.row(CARRIER).lines[0]
    lv = lambda c: int(np.asarray(volume.volume_of(node.gamma, np.array([c], dtype=object)), dtype=object).reshape(-1)[0])
    car.now[centre] = lv(int(sys.argv[5])); car.before[centre] = lv(int(sys.argv[6])); node.ride_walls()
    light = node.emitter().lines[0]; light.now[centre] = 4 * int(light.now[centre])
cube = node.cube; recs = node.records(); out = open(sys.argv[4], "w")
def nb(at):
    found = []
    for a in range(3):
        for s in (1, -1):
            m = list(at); m[a] = (m[a] + s) % cube; found.append(tuple(m))
    return found
prev_turned = np.zeros(node.shape, dtype=bool); births0 = int(node.counts["births"])
for t in range(1, n + 1):
    x = node.row(CARRIER).lines[0].now
    c = np.asarray(volume.level_of(node.gamma, x), dtype=object)
    frozen = readings.frozen_of(node, c); factors = node.link_factors(None, frozen)
    watch = set(tuple(int(v) for v in p) for p in zip(*np.nonzero(frozen | prev_turned)))
    if watch:
        hood = set(watch)
        for at in list(watch): hood |= set(nb(at))
        shares = []
        for rec, r in enumerate(recs):
            sh = node.share(r.lines, node.rule(r.pair, c, factors)); unit = node.units[rec]
            cur = [node.den * row_current(r.lines, port_of(a, 0)) for a in range(AXES)]
            tw = [row_twist(r.lines, a) for a in range(AXES)]
            ch = gram.charge(r.shape, r.lines) if r is not node.emitter() else None
            shares.append((sh, unit, cur, tw, ch))
        rows = []
        for at in sorted(hood):
            e = {"node": list(at), "X": int(x[at]), "content": int(c[at]), "frozen": bool(frozen[at]), "released": bool(prev_turned[at]), "watched": at in watch, "records": []}
            for rec, (sh, unit, cur, tw, ch) in enumerate(shares):
                e["records"].append({"rec": rec, "share": int(sh[at]), "unit": int(unit), "standing": int(sh[at]) >= int(unit), "current": [int(k[at]) for k in cur], "twist": [int(k[at]) for k in tw], "charge": None if ch is None else int(ch[at])})
            rows.append(e)
        out.write(json.dumps({"i": t, "start": True, "frozen_count": int(frozen.sum()), "released_count": int(prev_turned.sum()), "nodes": rows}) + "\n")
    b0 = int(node.counts["births"]); node.step()
    prev_turned = np.asarray(node.turned, dtype=bool) & frozen
    if int(node.counts["births"]) != b0 or t % 100 == 0:
        out.write(json.dumps({"i": t, "births_so_far": int(node.counts["births"]), "credits": int(node.counts["body_clicks"]), "frozen_count": int(frozen.sum()), "met": int(node.counts["met"]), "max_bits": int(node.max_transient)}) + "\n"); out.flush()
out.close(); print("done", n, dict((k, int(v)) for k, v in node.counts.items()))
