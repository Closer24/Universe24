"""tc2's record runner: a world run n intervals on a named src (the flag TC2_CHORD_COUNT from the environment), every take read at
merger.fall_of (the head's least-root count and the chord count both computed at every call, the one the run names returned), then
`back` intervals back (the run back bit for bit by state_of). Written: the counts (takes, where the two counts agree, where the chord
exceeds, the pays of each: fall(s) >= walls, taken against booked over every take and birth, the births and credits, the children's
Wronskian odd under the slot exchange from the log), the state's hash at n, and the record (the log) for the moment reader.
Usage: tc2_record.py <src> <world.json> <n> <back> <out.json>. Integers only."""
import hashlib, json, os, sys, collections
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))), "tests"))
sys.set_int_max_str_digits(0)
from event_universe import merger as merger_mod
from event_universe.core import rule3
from event_universe.loader.world import load_world
from event_universe.node import Node
from laws import state_of

src, world_path, n, back, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
flag = os.environ.get("TC2_CHORD_COUNT", "")
universe, world = load_world(world_path)
node = Node(universe, dict(world, intervals=n))
orig = merger_mod.fall_of
takes = []


def both(node_, at, walls, r, row):
    if flag:
        os.environ.pop("TC2_CHORD_COUNT")
    head = orig(node_, at, walls, r, row)
    os.environ["TC2_CHORD_COUNT"] = "1"
    chord = orig(node_, at, walls, r, row)
    if flag:
        os.environ["TC2_CHORD_COUNT"] = flag
    else:
        os.environ.pop("TC2_CHORD_COUNT")
    return head, chord


def wrapped(node_, at, walls, r, row):
    head, chord = both(node_, at, walls, r, row)
    got = chord if flag else head
    if walls > 0 and head[0] is not None:
        line = row.lines[head[2]]
        now, before = int(line.now[at]), int(line.before[at])
        takes.append(dict(i=node_.interval, at=list(at), walls=walls, s_head=head[0], f_head=head[1], s_chord=chord[0], f_chord=chord[1],
                          dist=abs(now - before), now=now, before=before))
    return got


merger_mod.fall_of = wrapped
kept = []
for _ in range(n):
    kept.append(state_of(node))
    node.step()
end = hashlib.sha256(state_of(node).encode()).hexdigest()[:16]
log = [dict(e) for e in node.log]
counts = {k: int(v) for k, v in node.counts.items()}
returned = sum(state_of(node) == kept[n - 1 - k] for k in range(back) if not node.step_back())
c = collections.Counter()
for t in takes:
    c["takes"] += 1
    c["agree"] += t["s_head"] == t["s_chord"]
    c["chord_above"] += t["s_chord"] > t["s_head"]
    c["chord_below"] += t["s_chord"] < t["s_head"]
    c["head_pays"] += t["f_head"] >= t["walls"]
    c["chord_pays"] += t["f_chord"] >= t["walls"]
    c["chord_within_dist"] += 1 <= t["s_chord"] <= t["dist"]
    c["chord_full_move"] += t["s_chord"] == t["dist"]
    c["head_full_move"] += t["s_head"] == t["dist"]
    c["surplus_head"] += t["f_head"] - t["walls"]
    c["surplus_chord"] += t["f_chord"] - t["walls"]
    c["levels_head"] += t["s_head"]
    c["levels_chord"] += t["s_chord"]
births = [e for e in log if e["event"] == "birth"]
credits = [e for e in log if e["event"] == "credit"]
odd = 0
for e in births:
    a, b = e["amplitude"]
    for stood, sense, w_end in zip(e["stood"], (-1, 1), e["W_children"], strict=True):
        rn, rb, inn, ib = stood
        rn2, ib2 = rn + sense * a, ib + b
        w_now = rn2 * ib2 - inn * rb
        rn_x, rb_x, in_x, ib_x = rb, rn + sense * a, ib, inn + b  # the slots exchanged then the lay on the other slot
        w_x = rn_x * ib_x - in_x * rb_x
        odd += w_now == w_end and w_x == -w_now and w_now != 0
tb = [(int(e["taken"]), int(e["booked"])) for e in births + credits if "booked" in e]
res = dict(src=src, flag=flag, world=os.path.basename(world_path), n=n, hash=end, counts=counts, births=len(births), credits=len(credits),
           run_back=returned, of=back, takes=dict(c), W_children_odd_under_exchange=odd, of_children=2 * len(births),
           taken_ge_booked=sum(1 for a, b in tb if a >= b), taken_eq_booked=sum(1 for a, b in tb if a == b), of_takes_logged=len(tb),
           taken_sum=sum(a for a, _ in tb), booked_sum=sum(b for _, b in tb), log_entries=len(log))
json.dump(dict(res, log=log, cube=int(world["shape"][0]), den=int(universe["integers"]["den"])), open(out, "w"), default=str)
open(out.replace(".json", "_takes.jsonl"), "w").write("\n".join(json.dumps(t) for t in takes) + "\n")
print(json.dumps(res, default=str))
