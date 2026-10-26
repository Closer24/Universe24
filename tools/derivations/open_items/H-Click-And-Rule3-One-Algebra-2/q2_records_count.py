"""Q2 on the published records (examples/records/*.json, the head's record of the hole 60, the chiral 60 and the bodies): from the log
alone, every take (a birth's or a credit's; a merger's two under `takes`): the slot moved is the now slot by the lay act's `line=` form
(taken_now_was and taker [now, before, levels]); the move's sign t = sign(before - now); the crossing's side at the credits from the
frame (re_before, re_now): down (before > 0 >= now), up (before < 0 <= now), none; the children's lays (re on now, im on before, two per
birth); the senses' and the Wronskians' sums over the births (the charge). Usage: q2_records_count.py <record.json>..."""
import json, sys, collections


def sign(x):
    return (x > 0) * 1 - (x < 0) * 1


for path in sys.argv[1:]:
    d = json.load(open(path))
    c = collections.Counter()
    for e in d["log"]:
        ev = e["event"]
        if ev == "refused":
            c["refused_" + e["cause"]] += 1
            continue
        c[ev] += 1
        takes = e.get("takes") or [e]
        for t in takes:
            tk = t.get("taker")
            if tk is None:
                c["takes_without_taker"] += 1
                continue
            if isinstance(tk[0], list):
                continue
            now, before, levels = tk
            c["takes"] += 1
            c["slot_moved_now"] += 1
            c["t_up" if before > now else "t_down"] += 1
            c["full_fall"] += levels == abs(now - before)
            c["levels_sum"] += levels
        if ev == "credit":
            f = e["frame"]
            if isinstance(f, str):
                f = json.loads(f.replace("'", '"').replace("True", "true").replace("False", "false"))
            b, n = int(f["re_before"]), int(f["re_now"])
            side = "cross_down" if (b > 0 >= n) else ("cross_up" if (b < 0 <= n) else "cross_none")
            c[side] += 1
            st = int(f.get("re_stepped", n))
            side2 = "step_down" if (n > 0 >= st) else ("step_up" if (n < 0 <= st) else "step_none")
            c[side2] += 1
            c["laid_back"] += "laid_back" in e
        if ev == "birth":
            c["child_lays_re_now"] += 2
            c["child_lays_im_before"] += 2
            c["W_children_sum"] += sum(e["W_children"])
            c["senses_sum"] += sum(e["senses"])
            c["W_pairs_opposite"] += sign(e["W_children"][0]) == -sign(e["W_children"][1]) != 0
    print(json.dumps(dict(record=path.split("/")[-1], intervals=d.get("intervals"), cube=d.get("cube"), run_back=d.get("run_back"), counts=dict(c))))
