"""A world run n intervals on a named src (the flag from the environment), the state's hash, the counts, the clicks' conservations (taken against booked, every take; the senses' sum; dP_take and dP_lay summed), the run back n of n. Usage: run_hash.py <src> <world name under tests/worlds> <n> [back m]"""
import hashlib, json, os, sys
sys.set_int_max_str_digits(0)
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))), "tests"))
from laws import node_of, state_of
node = node_of(sys.argv[2]); n = int(sys.argv[3]); back = int(sys.argv[sys.argv.index("back") + 1]) if "back" in sys.argv else n
kept = []
for _ in range(n):
    kept.append(state_of(node)); node.step()
end = hashlib.sha256(state_of(node).encode()).hexdigest()[:16]
births = [e for e in node.log if e["event"] == "birth"]
credits = [e for e in node.log if e["event"] == "credit"]
cons = dict(taken=0, booked=0, dP_take=[0, 0, 0], dP_lay=[0, 0, 0], senses=0, W=0, takes=0, taken_below_booked=0, remainder_negative=0, remainder_min=0)
for e in births + credits:
    booked = int(e.get("booked", e["taken"] if e["event"] == "credit" else 0))
    cons["taken"] += int(e["taken"]); cons["booked"] += booked; cons["takes"] += 1
    cons["taken_below_booked"] += int(e["taken"]) < booked
    rem = int(e.get("remainder", 0)); cons["remainder_negative"] += rem < 0; cons["remainder_min"] = min(cons["remainder_min"], rem)
    for a in range(3):
        cons["dP_take"][a] += int(e["dP_take"][a]); cons["dP_lay"][a] += int(e.get("dP_lay", [0, 0, 0])[a])
    if e["event"] == "birth":
        cons["senses"] += sum(e["senses"]); cons["W"] += sum(e["W_children"])
cons["taken_minus_booked"] = cons["taken"] - cons["booked"]
ran = sum(state_of(node) == kept[n - 1 - k] for k in range(back) if not node.step_back())
bits = max((int(abs(int(v))).bit_length() for e in node.log for v in (e.get("taken", 0), e.get("booked", 0))), default=0)
print(json.dumps(dict(src=sys.argv[1], world=sys.argv[2], flag=os.environ.get("TC1_DIVISION_COUNT", ""), hash=end, births=len(births), credits=len(credits),
      counts={k: int(v) for k, v in node.counts.items()}, run_back=ran, of=back, cons=cons, log_bits=bits)))
