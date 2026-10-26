"""The loader's refusals by name on both engines: a universe with two planes at one pair, one with no plane but the emitter; the hash of world_node at 20. Usage: refusals.py <src>"""
import sys, copy, json
sys.path.insert(0, sys.argv[1]); sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
u, w = load_world("tests/worlds/world_node.json")
print("shape", w.get("shape"), "rows", [(r.get("shape"), r.get("pair"), r.get("wall")) for r in u["rows"]])
def attempt(name, uu):
    try:
        Node(uu, w); print(name, "ACCEPTED")
    except Exception as e:
        print(name, "REFUSED:", str(e)[:100])
den = int(u["integers"]["den"])
planes = [r for r in u["rows"] if r.get("shape") == 2]
gapped = [r for r in planes if tuple(r["pair"]) != (den, den)]
u2 = copy.deepcopy(u); u2["rows"].append(copy.deepcopy(gapped[0])); attempt("two planes at one pair", u2)
u3 = copy.deepcopy(u); u3["rows"] = [r for r in u3["rows"] if not (r.get("shape") == 2 and tuple(r["pair"]) != (den, den))]; attempt("no plane but the emitter", u3)
u4 = copy.deepcopy(u); u4["rows"] = [r for r in u4["rows"] if not (r.get("shape") == 2 and tuple(r["pair"]) == (den, den))]; attempt("no emitter", u4)
n = Node(u, w)
for _ in range(20): n.step()
print("world_node 20 hash", n.state_hash())
