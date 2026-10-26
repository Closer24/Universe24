"""The off birth's flow and charges (H-Helicity-From-The-Twist-1): close.meet's row_current and gram.charge recorded by wrappers on the chiral 60; a reader."""
import json, sys
from event_universe import run as engine
from event_universe.loader.world import load_world
close = sys.modules["event_universe.close"]
seen = {"current": [], "charge": [], "twist": []}
oc, ocg, ot = close.row_current, close.gram.charge, close.row_twist
def rc(lines, port):
    f = oc(lines, port); seen["current"].append((port, [int(x) for x in f.reshape(-1)])); return f
def cg(shape, lines):
    f = ocg(shape, lines); seen["charge"].append([int(x) for x in f.reshape(-1)]); return f
def rt(lines, axis):
    f = ot(lines, axis); seen["twist"].append((axis, [int(x) for x in f.reshape(-1)])); return f
close.row_current, close.gram.charge, close.row_twist = rc, cg, rt
sys.set_int_max_str_digits(0)
universe, world = load_world(sys.argv[1])
node = engine.Node(universe, world)
cube = node.cube
def idx(p): return p[0]*cube*cube + p[1]*cube + p[2]
per = {}
for t in range(int(world["intervals"])):
    for k in seen: seen[k].clear()
    node.step()
    per[node.interval] = {k: list(v) for k, v in seen.items()}
for b in [e for e in node.log if e["event"] == "birth"]:
    i, rec = int(b["i"]), int(b["taken_row"])
    minus, plus, at = b["minus"], b["plus"], b["node"]
    axis = [a for a in range(3) if minus[a] != plus[a]][0]
    lo = minus if (minus[axis] + 1) % cube == plus[axis] else plus
    cur = per[i]["current"][3*rec:3*rec+3]
    tw = per[i]["twist"][3*rec:3*rec+3]
    flow = cur[axis][1][idx(lo)]
    h = tw[axis][1][idx(lo)]
    hi = [(lo[a] + (1 if a == axis else 0)) % cube for a in range(3)]
    ch = per[i]["charge"][rec] if rec < len(per[i]["charge"]) else None
    w = [ch[idx(lo)], ch[idx(hi)]] if ch else None
    into = hi if flow > 0 else lo
    rest = flow == 0 and (w is not None and w[0]*w[1] < 0)
    print(json.dumps({"i": i, "rec": rec, "lo": lo, "hi": hi, "flow sign": (flow>0)-(flow<0), "h sign": (h>0)-(h<0), "charges lo,hi": w, "rest": rest, "node==into": at == into, "plus==hi": plus == hi, "h bits": abs(h).bit_length(), "charges count": len(per[i]["charge"])}))
