"""mg1: the walls census on a record run with MG1_LOG_WALLS=1: per interval and per children's record the walls under the two readings (the board's increment, the child's own quantum), the negatives, the distinct values, the standing share at the ends; the stops of the heavy rows with the fall over the wall in thousandths; the mergers landed with taken against booked.
Usage: python read_walls.py <record.json>"""
import json
import sys
from collections import Counter

sys.set_int_max_str_digits(0)
THOUSAND = 1000


def main(path: str) -> None:
    r = json.load(open(path))
    log = r["log"]
    planes = [str(p) for p in r["planes"]]
    light = planes.index(str(r["den"]))
    print("record:", path.split("/")[-1], "run back:", r["run_back"], "counts:", r["counts"])
    walls = [e for e in log if e["event"] == "walls"]
    print("walls lines:", len(walls))
    for i in sorted({e["i"] for e in walls}):
        ws = [e for e in walls if e["i"] == i]
        for s in sorted({e["line_pair"] for e in ws}):
            w = [e for e in ws if e["line_pair"] == s]
            inc = [v for e in w for v in e["increment"]]
            own = [v for e in w for v in e["own"]]
            st = [v for e in w for v in e["standing"]]
            diff = [a - b for a, b in zip(inc, own)]
            print(
                f"  i {i} children's record {s} ({'light' if s == light else 'heavy'}), taken rows {dict(Counter(e['taken_row'] for e in w))}: ends {len(inc)}; increment negative {sum(1 for v in inc if v < 0)}, distinct {len(set(inc))}, min {min(inc)}, max {max(inc)}; own negative {sum(1 for v in own if v < 0)}, distinct {len(set(own))}, values {sorted(set(own))[:4]}; increment - own: zero at {sum(1 for v in diff if v == 0)}, distinct {len(set(diff))}; standing at the ends: zero {sum(1 for v in st if v == 0)}, min {min(st)}, max {max(st)}"
            )
            if any(st):
                # the increment less the own against the standing's sign: the cross term
                c = Counter((v > 0) - (v < 0) for v in diff)
                print(f"    the cross term's sign (increment - own): {dict(c)}")
    stops = [e for e in log if e["event"] == "refused" and e["cause"] == "stop" and e.get("row", light) != light]
    print("heavy stops:", len(stops), "whole-take stops:", sum(1 for e in stops if e.get("whole")))
    for i in sorted({e["i"] for e in stops})[:6]:
        ss = [e for e in stops if e["i"] == i]
        ratios = Counter(e["fall"] * THOUSAND // e["walls"] if e["walls"] > 0 else None for e in ss)
        print(f"  i {i}: stops {len(ss)} by row {dict(Counter(e['row'] for e in ss))}; fall over wall (thousandths: count) {dict(sorted(ratios.items(), key=lambda kv: (kv[0] is None, kv[0])))}")
    births = [e for e in log if e["event"] == "birth"]
    mergers = [e for e in births if e.get("taken_row", light) != light and e["line_pair"] == light]
    print("mergers:", len(mergers), "at", sorted({e["i"] for e in mergers})[:12])
    for i in sorted({e["i"] for e in mergers})[:6]:
        ms = [e for e in mergers if e["i"] == i]
        ends = Counter()
        for e in ms:
            for t in e.get("takes", []):
                ends[(t["taken"] >= t["booked"], (t["taken"] - t["booked"]) * THOUSAND // t["booked"] if t["booked"] else None)] += 1
        nodes = {tuple(e["minus"]) for e in ms} | {tuple(e["plus"]) for e in ms}
        print(f"  i {i}: mergers {len(ms)} by taken row {dict(Counter(e['taken_row'] for e in ms))}; Nodes touched {len(nodes)}; per end (taken >= booked, (taken - booked) over booked in thousandths): {dict(ends)}; W_children {dict(Counter(tuple(e['W_children']) for e in ms))}; booked min {min(e['booked'] for e in ms)} max {max(e['booked'] for e in ms)}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
        print()
