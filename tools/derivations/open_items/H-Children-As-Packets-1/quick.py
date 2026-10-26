import json, sys, time
sys.path.insert(0, sys.argv[1]); sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
u, w = load_world(sys.argv[2]); n = int(sys.argv[3]); w = dict(w, intervals=n)
node = Node(u, w); hashes = []
t0 = time.time()
for _ in range(n):
    node.step(); hashes.append(node.state_hash())
t1 = time.time()
births = [e for e in node.log if e["event"] == "birth"]
for e in births[:4]:
    print({k: e[k] for k in ("i","node","minus","plus","dP_take","dP_lay","W_children","booked","taken") if k in e}, e.get("waves"), e.get("dP_lay_ends"), e.get("moment_ends"), e.get("amplitude_packets"))
back = int(sys.argv[4]); exact = 0
for k in range(back):
    node.run(-1); exact += (node.state_hash() == hashes[len(hashes)-2-k]) if len(hashes)-2-k >= 0 else 0
print("births", len(births), "counts", {k:int(v) for k,v in node.counts.items()}, "run_back", exact, "of", back, "secs", int(t1-t0))
