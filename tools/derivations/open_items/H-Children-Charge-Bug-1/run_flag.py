"""A record run on a given src (the head's or the flagged copy's): the world stepped n intervals, the state's hash at the end
(node.state_hash), the births and the credits, the counts, the run back `back` intervals by the hash, taken against booked at every
take, the census (integers, bits), and per birth the children's own Wronskian (sense A B for the child's lay, 0 for the exact lay)
against the log's W_children (the record's W at the Node after the lay).
Usage: run_flag.py <src path> <world.json> <n> <back>; the flag CC1_LIGHT_EXACT read from the environment by the copy alone."""
import json, os, sys, time
sys.path.insert(0, sys.argv[1])
from event_universe.core import rule3
from event_universe.loader.world import load_world
from event_universe.node import Node
sys.set_int_max_str_digits(0)
universe, world = load_world(sys.argv[2])
n, back = int(sys.argv[3]), int(sys.argv[4])
node = Node(universe, {**world, "intervals": n})
t0 = time.monotonic_ns()
hashes, bits = [], 0
for t in range(n):
    if t >= n - back:
        hashes.append(node.state_hash())
    node.step()
    bits = max(bits, node.census()[1])
end = node.state_hash()[:16]
ms = (time.monotonic_ns() - t0) // 1000000
A, B = (int(x) for x in rule3.balanced_pair(rule3.half(node.T)))
births = [e for e in node.log if e["event"] == "birth"]
credits = [e for e in node.log if e["event"] == "credit"]
takes_ok = takes = ex_s1 = 0
for e in births + credits:
    for t_ in e.get("takes") or [e]:
        takes += 1
        takes_ok += int(t_["taken"]) >= int(t_["booked"])
        ex_s1 += "remainder_was" not in t_ or int(t_["taken"]) + int(t_["remainder_was"]) - int(t_["remainder"]) == int(t_["booked"])
own_rows, own_sum, after_sum, own_zero, after_zero, exact = [], 0, 0, 0, 0, 0
for b in births:
    ex = b.get("exact_lay") or [None, None]
    own = [0 if ex[end_] is not None else sense * A * B for end_, sense in ((0, -1), (1, 1))]
    exact += sum(x is not None for x in ex)
    own_rows.append(own)
    own_sum += sum(own); after_sum += sum(b["W_children"])
    own_zero += sum(own) == 0; after_zero += sum(b["W_children"]) == 0
counts = {k: int(v) for k, v in node.counts.items()}
back_exact = 0
for k in range(len(hashes)):
    node.step_back()
    back_exact += node.state_hash() == hashes[len(hashes) - 1 - k]
print(json.dumps(dict(src=sys.argv[1], flag=os.environ.get("CC1_LIGHT_EXACT", ""), world=os.path.basename(sys.argv[2]), n=n,
      hash=end, births=len(births), credits=len(credits), exact_lays=exact, births_own_W_zero=own_zero,
      births_after_W_zero=after_zero, SUM_W_own=own_sum, SUM_W_after=after_sum, W_own=own_rows,
      takes=takes, taken_ge_booked=takes_ok, ex_s1_taken_plus_owed_equals_booked=ex_s1, births_log=births, taken=counts["taken"], booked=counts["booked"], counts=counts,
      integers=node.census()[0], bits=bits, run_back=back_exact, of=back, milliseconds=ms)))
