"""Q2, Q4, Q8 on the records: for every take and lay of a record (the credit and birth lines), the slot moved, the sign of the move
(toward = sign(before - now) of the taken line), whether the move is the full one (levels == |now - before|, the now slot set to its
own past: the first component of Rule3 at -1 at that Node), the trigger's sign at a credit (the sign of re_now - re_before at the
close, the crossing's direction), the Node turned (the swap's exchange, the Node's own time reversal) or not, and at a turned credit
whether the frame at the close is the start's record exchanged and conjugated bit for bit (re_now == re_start_before,
re_before == re_start_now, im_now == -im_start_before, im_before == -im_start_now). Q4: the Wronskian of the credit's frame under the
slot exchange X (W -> -W) and under the swap's X K (W kept); the births' two children's W summing to 0.
Usage: python ca1_q2_records.py <record.json> [...]; integers only."""
import json, sys
from collections import Counter

sys.set_int_max_str_digits(0)

for path in sys.argv[1:]:
    d = json.load(open(path))
    log = d["log"]
    credits = [e for e in log if e["event"] == "credit"]
    births = [e for e in log if e["event"] == "birth"]
    c = Counter()
    for e in credits:
        now, before, levels = e["taker"]
        toward = 1 if before > now else -1 if before < now else 0
        c["take on the now slot"] += 1
        c["toward +1 (now below its past)" if toward > 0 else "toward -1 (now above its past)"] += 1
        c["full move (now set to before)"] += levels == abs(now - before)
        c["partial move"] += levels < abs(now - before)
        c["laid back (no current)"] += "laid_back" in e
        c["turned Node"] += bool(e.get("turned"))
        f = e.get("frame", {})
        if "re_now" in f:
            cross = (f["re_now"] > 0) - (f["re_now"] < 0) - ((f["re_before"] > 0) - (f["re_before"] < 0))
            c["trigger sign +" if cross > 0 else "trigger sign -" if cross < 0 else "trigger sign 0"] += 1
            w = f["re_now"] * f["im_before"] - f["re_before"] * f["im_now"]
            wx = f["re_before"] * f["im_now"] - f["re_now"] * f["im_before"]
            wxk = f["re_before"] * (-f["im_now"]) - f["re_now"] * (-f["im_before"])
            c["W != 0"] += w != 0
            c["W flips under X"] += (w != 0) and wx == -w
            c["W kept under X K (the swap)"] += wxk == w
            c["sense == sign W"] += e["sense"] == ((w > 0) - (w < 0))
            if e.get("turned"):
                ex = (f["re_now"] == f["re_start_before"] and f["re_before"] == f["re_start_now"]
                      and f["im_now"] == -f["im_start_before"] and f["im_before"] == -f["im_start_now"])
                c["turned: frame == start exchanged and conjugated"] += ex
                c["turned: frame differs (a write or a kick between)"] += not ex
            else:
                c["not turned: re_now == re_stepped"] += f["re_now"] == f["re_stepped"]
                c["not turned: re_now != re_stepped (a write between)"] += f["re_now"] != f["re_stepped"]
    b = Counter()
    for e in births:
        b["birth: take on the now slot of the taken line"] += 1
        b["lay re on now (A) at both ends"] += 1
        b["lay im on before (sense B) at both ends"] += 1
        wm, wp = e["W_children"]
        b["children W opposite, sum 0"] += wm + wp == 0 and wm < 0 < wp
        b["taken == booked"] += e["taken"] == e["booked"]
        b["taken >= booked"] += e["taken"] >= e["booked"]
        tk = e["taker"]
        if isinstance(tk[0], list):
            for now, before, levels in tk:
                b["merger end: full move"] += levels == abs(now - before)
        else:
            now, before, levels = tk
            b["birth take: full move"] += levels == abs(now - before)
            b["birth take: partial move"] += levels < abs(now - before)
    print(path.split('/')[-1], "credits", len(credits), "births", len(births), "turns", d.get("counts", {}).get("turns"))
    for k, v in sorted(c.items()):
        print("  ", k, v)
    for k, v in sorted(b.items()):
        print("  ", k, v)
