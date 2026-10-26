"""The 3-cube at 20 intervals: the head's src against the flagged copy with the flag empty (bit for bit by state_of) and with the flag set.
Usage: run_flag_3cube.py <src path> <world> <n>; prints the state's hash, the counts, the run back."""
import hashlib, json, os, sys
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))), "tests"))
from laws import node_of, state_of
node = node_of(sys.argv[2]); n = int(sys.argv[3])
kept = []
for _ in range(n):
    kept.append(state_of(node)); node.step()
end = hashlib.sha256(state_of(node).encode()).hexdigest()[:16]
births = [e for e in node.log if e["event"] == "birth"]
credits = [e for e in node.log if e["event"] == "credit"]
cons = dict(taken=0, booked=0, dP_take=[0, 0, 0], dP_lay=[0, 0, 0], senses=0, W=0, takes=0)
for e in births + credits:
    cons["taken"] += int(e["taken"]); cons["booked"] += int(e.get("booked", e["taken"] if e["event"] == "credit" else 0))
    cons["takes"] += 1
    for a in range(3):
        cons["dP_take"][a] += int(e["dP_take"][a]); cons["dP_lay"][a] += int(e.get("dP_lay", [0, 0, 0])[a])
    if e["event"] == "birth":
        cons["senses"] += sum(e["senses"]); cons["W"] += sum(e["W_children"])
cons["taken_minus_booked"] = cons["taken"] - cons["booked"]
back = sum(state_of(node) == kept[n - 1 - k] for k in range(n) if not node.step_back())
print(json.dumps(dict(src=sys.argv[1], flag=os.environ.get("CA2_EVEN_LAY", ""), hash=end, births=len(births),
      W_children=[b["W_children"] for b in births][:6], senses_sum=sum(sum(b["senses"]) for b in births),
      refused_sense=int(node.counts["refused_sense"]), run_back=back, of=n, cons=cons)))
