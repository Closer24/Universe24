"""mg1: an engine record (python -m event_universe.run) read for the merger at rest: the rest meetings, the mergers landed (a gapped row taken, the light born) with the interval, the Nodes, the charge summed from the rest meeting of the same Link, taken against booked per end; the heavy stops' fall over wall in thousandths by interval (first and last); the births from light by interval.
Usage: python read_three.py <record.json> [<record.json> ...]"""
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
    print("record:", path.split("/")[-1], "run back:", r["run_back"], "births:", r["counts"]["births"], "body_clicks:", r["counts"]["body_clicks"], "rest_met:", r["counts"].get("rest_met", 0), "refused_stop:", r["counts"]["refused_stop"])
    rest = [e for e in log if e["event"] == "rest_meet"]
    births = [e for e in log if e["event"] == "birth"]
    mergers = [e for e in births if e.get("taken_row", light) != light and e["line_pair"] == light]
    plain = [e for e in births if e.get("taken_row", light) == light]
    print("  births from light:", len(plain), "at", sorted(Counter(e["i"] for e in plain).items())[:14])
    print("  rest meetings:", len(rest), "at", sorted(Counter(e["i"] for e in rest).items())[:16])
    by_key = {}
    for e in rest:
        by_key[(e["i"], e["row"], frozenset((tuple(e["node"]), tuple(e["link"]))))] = e["charges"]
    print("  mergers:", len(mergers))
    for e in mergers:
        w = by_key.get((e["i"], e["taken_row"], frozenset((tuple(e["minus"]), tuple(e["plus"])))))
        ends = [(t["taken"] - t["booked"]) * THOUSAND // t["booked"] for t in e.get("takes", []) if t["booked"] > 0]
        print(f"    i {e['i']} row {e['taken_row']} minus {e['minus']} plus {e['plus']} charges {w} sum {None if w is None else w[0] + w[1]} W_children {e['W_children']} (taken - booked) over booked per end (thousandths) {ends} exact_lay {e.get('exact_lay')}")
    stops = [e for e in log if e["event"] == "refused" and e["cause"] == "stop" and e.get("row", light) != light and e.get("walls", 0) > 0]
    ratios = Counter()
    for e in stops:
        ratios[e["fall"] * THOUSAND // e["walls"]] += 1
    print("  heavy stops with a wall above 0:", len(stops), "fall over wall (thousandths) min", min(ratios) if ratios else None, "max", max(ratios) if ratios else None, "at or above 900:", sum(v for k, v in ratios.items() if k >= 900), "below 0:", sum(v for k, v in ratios.items() if k < 0))
    credits = [e for e in log if e["event"] == "credit"]
    print("  credits:", len(credits), "by row", dict(Counter(e["line"] for e in credits)))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
