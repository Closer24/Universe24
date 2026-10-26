"""The flagged record (HT2_HELICITY=1: the twist h logged at every meeting that passes close.meet, as a `helicity` line) against the reader's helicity from the Node lines and against the head's record: the births' and credits' lines equal event for event with the helicity lines struck, the helicity lines matched to the births by (i, minus, plus, row) and their sign against the reader's h_sign, N of M; integers only.

Usage: python flag_compare.py <flagged record.json> <head record.json> <reader out.json>
"""

import json
import sys

sys.set_int_max_str_digits(0)

flagged, head, reader = (json.load(open(p, encoding="utf-8")) for p in sys.argv[1:4])
hel = [e for e in flagged["log"] if e["event"] == "helicity"]
rest = [e for e in flagged["log"] if e["event"] != "helicity"]
head_log = head["log"]
same_events = sum(1 for a, b in zip(rest, head_log) if a == b)
print(json.dumps({"flagged log lines": len(flagged["log"]), "helicity lines (meetings passing the twist)": len(hel), "other lines": len(rest), "head log lines": len(head_log), "lines equal event for event": [same_events, max(len(rest), len(head_log))], "counts equal": flagged["counts"] == head["counts"], "run back": [flagged.get("run_back"), head.get("run_back")]}))
births = reader["births_detail"]
matched = agree = 0
rest_births = 0
for b in births:
    if "axis" not in b:
        continue
    found = [h for h in hel if int(h["i"]) == b["i"] and h["minus"] == b["minus"] and h["plus"] == b["plus"] and int(h["row"]) == b["taken_row"]]
    if not found:
        continue
    matched += 1
    h = found[-1]
    rest_births += bool(h["rest"])
    agree += int(h["sign"]) == b["h_sign"] and int(h["axis"]) == b["axis"]
print(json.dumps({"births": sum(1 for b in births if "axis" in b), "births matched to a helicity line": matched, "helicity sign and axis equal to the reader's (the Node line's twist)": agree, "rest births among them": rest_births, "helicity lines by sign (+, -)": [sum(int(h["sign"]) > 0 for h in hel), sum(int(h["sign"]) < 0 for h in hel)], "twist bits max": max((abs(int(h["twist"])).bit_length() for h in hel), default=0)}))
