"""the questions 2, 4 and 8 (hand ca2): a world run n intervals forward in the engine with every take read (take.fall_of wrapped, no src edited),
then n back (the run back). At every take (fall_of called from take_at): the taken line's (now, before, rem) at the Node, the move's
sign t = sign(before - now), the levels s, the pull Y = S before + SUM_j R_j before_j (Rule3's numerator read at the before slot), and
Rule3 at -1 on the taken line at that Node from the pair (a_now, a_next) = (before, now) with the remainder rem: a_{-2}. Counted:
takes; the slot moved (the now slot, by the lay act's `line=` form); t up / down; the crossing of the taken line (before * now < 0,
one of them 0); takes where now + t s == a_{-2} (the take equal to Rule3 at -1 bit for bit); where sign(a_{-2} - now) == t; where
s == |now - before| (the full fall: the line sent to now == before, the slot exchange's fixed line). The children's lays: re on now,
im on before (close.child_at), counted from the log. Then, on the state at the end of the forward run, the time reversal of the frame
(every line's two slots exchanged): the conserved form's term, the Wronskian W = re_now im_before - im_now re_before, the Link current
F = now_i before_j - before_i now_j, the lattice momentum P_a, the count (share-like now^2 + before^2): counts of Nodes/Links where
each flips sign exactly, stays, or neither. Usage: q8_takes.py <world.json> <n> <out.txt>. Integers only."""
import sys, os, json, collections
sys.path.insert(0, os.environ["PYTHONPATH"])
sys.path.insert(0, os.path.join(os.environ["PYTHONPATH"], "..", "tests"))
import numpy as np
from event_universe import take as take_mod
from event_universe.core import rule3
from event_universe.core.ports import AXES, PORTS, port_of
from event_universe.rows import PLANE
from laws import node_of, state_of

world, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
node = node_of(world)
orig = take_mod.fall_of
takes = []


def sign(x):
    return (x > 0) * 1 - (x < 0) * 1


def wrapped(node, at, walls, r, row):
    got = orig(node, at, walls, r, row)
    if sys._getframe(1).f_code.co_name != "take_at" or got[0] is None:
        return got
    levels, fall, k = got
    line = row.lines[k]
    now, before, rem = int(line.now[at]), int(line.before[at]), int(line.rem[at])
    w, own = int(r.wall), take_mod.at_node(r.self_coefficient, at)
    mass = take_mod.at_node(r.mass, at)
    reached, flux = 0, 0
    for port, reach in enumerate(r.reaches):
        j = take_mod.neighbour(node, at, port)
        rj = take_mod.at_node(reach, at)
        reached += rj * int(line.before[j])
        flux += rj * (int(line.before[j]) - before)
    pull = own * before + reached
    a_m2, r_m2 = rule3.rule3(flux, mass, w, before, now, rem, -1)
    t = sign(before - now)
    takes.append(dict(i=node.interval, at=list(at), k=k, now=now, before=before, rem=rem, levels=levels, t=t, pull=pull,
                      a_m2=a_m2, r_m2=r_m2, moved=now + t * levels, dist=abs(now - before), rec=node.records().index(row)))
    return got


take_mod.fall_of = wrapped
kept = []
for _ in range(n):
    kept.append(state_of(node))
    node.step()
# the time reversal of the frame on the end state: every line's two slots exchanged; each quantity on the frame and on its image
flips = collections.Counter()
for rec, row in enumerate(node.records()):
    if row.shape != PLANE:
        continue
    re, im = row.lines
    num = row.pair[0]
    rn, rb, inn, ib = (np.asarray(x, dtype=object) for x in (re.now, re.before, im.now, im.before))
    w = int(re.wall) if np.ndim(re.wall) == 0 else int(np.asarray(re.wall).reshape(-1)[0])
    for at in np.ndindex(*node.shape):
        a, b, c_, d = int(rn[at]), int(rb[at]), int(inn[at]), int(ib[at])
        W, W_T = a * d - c_ * b, b * c_ - d * a
        form, form_T = w * (a * a + b * b), w * (b * b + a * a)
        flips["W_flips_sign"] += W_T == -W and W != 0
        flips["W_zero"] += W == 0
        flips["form_same"] += form_T == form
    for ax in range(AXES):
        un, ub = np.roll(rn, -1, axis=ax), np.roll(rb, -1, axis=ax)
        P = P_T = 0
        for at in np.ndindex(*node.shape):
            a, b, a2, b2 = int(rn[at]), int(rb[at]), int(un[at]), int(ub[at])
            F, F_T = num * (a * b2 - b * a2), num * (b * a2 - a * b2)
            flips["F_flips_sign"] += F_T == -F and F != 0
            flips["F_zero"] += F == 0
            P += (num + num) * (a2 * b - a * b2)
            P_T += (num + num) * (b2 * a - b * a2)
        flips["P_axis_flips_sign"] += P_T == -P and P != 0
        flips["P_axis_zero"] += P == 0
back = sum(state_of(node) == kept[n - 1 - k] for k in range(n) if not node.step_back())
c = collections.Counter()
for t_ in takes:
    c["takes"] += 1
    c["slot_moved_now"] += 1
    c["t_up" if t_["t"] > 0 else "t_down"] += 1
    nb = t_["now"] * t_["before"]
    c["crossing" if nb < 0 else ("touch" if nb == 0 else "no_crossing")] += 1
    c["equal_rule3_minus1"] += t_["moved"] == t_["a_m2"]
    c["sign_agrees_rule3_minus1"] += sign(t_["a_m2"] - t_["now"]) == t_["t"]
    c["full_fall_now_eq_before"] += t_["levels"] == t_["dist"]
    c["a_m2_between_now_and_before"] += min(t_["now"], t_["before"]) <= t_["a_m2"] <= max(t_["now"], t_["before"])
births = [e for e in node.log if e["event"] == "birth"]
credits = [e for e in node.log if e["event"] == "credit"]
c["births"], c["credits"] = len(births), len(credits)
c["child_lays_re_now"] = 2 * len(births)
c["child_lays_im_before"] = 2 * len(births)
c["W_children_sum"] = sum(sum(b["W_children"]) for b in births)
c["senses_sum"] = sum(sum(b["senses"]) for b in births)
c["laid_back"] = sum(1 for e in credits if "laid_back" in e)
res = dict(world=world, n=n, run_back=back, of=n, counts=dict(c), flips=dict(flips), node_counts={k: int(v) for k, v in node.counts.items()})
open(out, "w").write(json.dumps(res) + "\n")
open(out.replace(".txt", "_takes.jsonl"), "w").write("\n".join(json.dumps(t) for t in takes) + "\n")
print(json.dumps(res))
