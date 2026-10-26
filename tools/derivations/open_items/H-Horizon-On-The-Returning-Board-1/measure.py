"""The measure of one record for the horizon on a returning board (sb1): the frozen Nodes per interval, the content and volume course, the exact return by the state's hash, the bangs, the births, the credits, the run back, the width. Reads the record's JSON written by event_universe.run; the gates come from the engine's own decoder beside it."""
import hashlib
import json
import sys

from event_universe.core import paces


def state_hash(line):
    text = json.dumps([int(x) for x in line["X"]], separators=(",", ":"))
    return hashlib.sha256(text.encode("ascii")).hexdigest()[:16]


def main(path):
    r = json.load(open(path))
    gamma = int(r["universe"]["integers"]["node_clock"])
    frozen_mark = paces.certified(gamma)
    lines = r["nodes"]
    print("record", path)
    print("cube", r.get("cube"), "intervals", r.get("intervals"), "gamma", gamma)
    lay = [e for e in r["log"] if e.get("event") == "lay"]
    for e in lay[:2]:
        print("lay", {k: e[k] for k in ("quanta", "amplitude", "share", "unit", "nodes") if k in e})
    first_frozen, frozen_counts, releases = None, [], []
    xs_max, xmax_at = 0, None
    cmax = 0
    for line in lines:
        i = int(line["i"])
        nfrozen = len(line.get("frozen", []))
        if nfrozen:
            frozen_counts.append((i, nfrozen))
            if first_frozen is None:
                first_frozen = (i, nfrozen)
        elif first_frozen is not None and not releases:
            releases.append(i)
        top = max(int(x) for x in line["X"])
        if top > xs_max:
            xs_max, xmax_at = top, i
    print("X max", xs_max, "at the interval", xmax_at, "bits", xs_max.bit_length())
    print("the frozen mark (content)", frozen_mark)
    print("frozen intervals", len(frozen_counts), "first", first_frozen, "released at", releases[:1])
    print("frozen per interval (first ten)", frozen_counts[:10])
    rows = r["rows"]
    cmax = max(int(x["content min/mean/max"][2]) for x in rows)
    print("content max in the rows", cmax, "frozen mark", frozen_mark, "reached" if cmax >= frozen_mark else "not reached")
    # the tops and the exact returns from the Node lines, as board.py reads them
    means = [(int(l["i"]), sum(int(x) for x in l["X"]) // len(l["X"]), len(l["turned"]), len(l["X"])) for l in lines]
    tops = [i for i, _m, t, n in means if t == n and n]
    bottoms = [
        (means[k][0], means[k][1], all(int(x) == gamma for x in lines[k]["X"]))
        for k in range(1, len(means) - 1)
        if means[k][1] <= means[k - 1][1] and means[k][1] < means[k + 1][1]
    ]
    exact = [i for i, _m, at in bottoms if at]
    print("tops (whole board turned)", tops[:10], "count", len(tops))
    print("bottoms", bottoms[:6], "exact returns", exact[:10], "count", len(exact))
    # the state's hash: the board's volumes at every interval, the first pair against every later pair
    hashes = [state_hash(l) for l in lines]
    first = hashes[0]
    same = [int(lines[k]["i"]) for k in range(1, len(hashes)) if hashes[k] == first]
    print("the first interval's volume hash repeats at", same[:10], "count", len(same))
    births = [e for e in r["log"] if e.get("event") == "birth"]
    credits = [e for e in r["log"] if e.get("event") == "credit"]
    print("births in the log", len(births), "credits in the log", len(credits), "run back", r.get("run_back"))
    print("counts", {k: r["counts"][k] for k in ("births", "body_clicks", "turns") if k in r.get("counts", {})})


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
        print("-" * 40)
