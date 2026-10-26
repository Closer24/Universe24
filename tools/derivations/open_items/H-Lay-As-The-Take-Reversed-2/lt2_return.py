"""The cycle seed's return read from a record's Node lines (H-Lay-As-The-Take-Reversed-2): the intervals at which every Node's X equals the first interval's (the return), the births per interval and the count of intervals with births, the nearest return by the count of Nodes differing. Integers only. Usage: lt2_return.py <record.json>"""
import json
import sys

sys.set_int_max_str_digits(0)


def main(argv):
    d = json.load(open(argv[1]))
    nodes = d["nodes"]
    first = [int(x) for x in nodes[0]["X"]]
    returns, nearest = [], (len(first) + 1, None)
    for line in nodes[1:]:
        xs = [int(x) for x in line["X"]]
        differing = sum(a != b for a, b in zip(xs, first, strict=True))
        if differing == 0:
            returns.append(int(line["i"]))
        elif differing < nearest[0]:
            nearest = (differing, int(line["i"]))
    births = [e for e in d["log"] if e["event"] == "birth"]
    by_interval = {}
    for e in births:
        by_interval[int(e["i"])] = by_interval.get(int(e["i"]), 0) + 1
    print(json.dumps({
        "record": argv[1],
        "intervals": len(nodes),
        "returns (every Node's X equal to the interval 1's)": returns,
        "nearest otherwise (nodes differing, interval)": list(nearest),
        "births": len(births),
        "intervals with births": len(by_interval),
        "births by interval": sorted(by_interval.items()),
        "counts": d["counts"],
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
