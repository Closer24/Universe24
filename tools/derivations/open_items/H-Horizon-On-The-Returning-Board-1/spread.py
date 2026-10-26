"""The board's spread and its births per interval (sb1): the lift's own reading of BG-S1 (the neighbours' spread e against 2 over the square root of Gamma, read as thousandths of the mean by one quotient) and the count of Nodes that bore a child at each interval, from the record's log and its Node lines."""
import json
import sys


def main(path):
    r = json.load(open(path))
    lines = r["nodes"]
    births = {}
    for e in r["log"]:
        if e.get("event") == "birth":
            births.setdefault(int(e["i"]), []).append(e.get("node"))
    print("record", path, "cube", r.get("cube"))
    print("the birth intervals and the count of Nodes bearing (first six):",
          [(i, len(set(map(str, v)))) for i, v in sorted(births.items())[:6]])
    out = []
    for line in lines:
        xs = [int(x) for x in line["X"]]
        mean = sum(xs) // len(xs)
        spread = (max(xs) - min(xs)) * 1000 // mean if mean else 0
        out.append((int(line["i"]), mean, spread, len(line.get("frozen", []))))
    marks = [0, 1, 2, 3, 5, 10, 50, 100, 110, 111, 150, 200, 219, 230, 300, 400, 499]
    print("interval | mean X | spread in thousandths of the mean | frozen Nodes")
    for i, mean, spread, fr in out:
        if i in marks:
            print(i, mean, spread, fr)
    print("the largest spread", max(s for _i, _m, s, _f in out), "against the lift's threshold 63 thousandths")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
        print("-" * 30)
