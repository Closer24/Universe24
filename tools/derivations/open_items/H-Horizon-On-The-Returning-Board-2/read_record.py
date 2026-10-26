"""The measures of one record from its own Node lines (no engine import): the course of the volume and the content, the first freeze and the release, the turns, the alike intervals, and the return of the whole board's volume to its first line."""

import json
import sys


def main(path: str) -> None:
    d = json.load(open(path))
    lines = d["nodes"]
    print(f"record {path}: cube {d['cube']}, intervals {d['intervals']}, Gamma {d['gamma']}, lines {len(lines)}")
    print(f"counts: {d['counts']}")
    print(f"run back: {d['run_back']}")
    first = tuple(lines[0]["X"])
    tops, alike, frozen_at, turned_at = [], 0, [], []
    xmax, cmax, at_max = 0, 0, 0
    for line in lines:
        xs, cs = line["X"], line["content"]
        if len(set(xs)) == 1:
            alike += 1
        if max(xs) > xmax:
            xmax, cmax, at_max = max(xs), max(cs), line["i"]
        if line["frozen"]:
            frozen_at.append((line["i"], len(line["frozen"])))
        if line["turned"]:
            turned_at.append((line["i"], len(line["turned"])))
    print(f"alike intervals (one volume at every Node): {alike} of {len(lines)}")
    print(f"the volume's max {xmax} at the interval {at_max}, the content there {cmax}")
    print(f"the frozen lines (interval, Nodes): {frozen_at[:12]} ... count {len(frozen_at)}")
    print(f"the turned lines (interval, Nodes): {turned_at[:12]} ... count {len(turned_at)}")
    if len(frozen_at) > 1:
        runs = [b[0] - a[0] for a, b in zip(frozen_at, frozen_at[1:])]
        print(f"the least gap between two frozen lines: {min(runs)} (1 would be two in a row)")
    back = [line["i"] for line in lines[1:] if tuple(line["X"]) == first]
    print(f"the intervals whose whole board equals the first line's volumes: {back[:10]}")
    near = [(line["i"], max(line["X"])) for line in lines if line["i"] > at_max and max(line["X"]) <= first[0] * 2]
    print(f"the first lines back below twice the seed's volume after the top: {near[:5]}")
    for line in lines:
        if line["i"] in (1, at_max, at_max + 1, len(lines)):
            print(f"  i {line['i']}: X {line['X'][0]} content {line['content'][0]} turned {len(line['turned'])} frozen {len(line['frozen'])} held {len(line['held']) if isinstance(line['held'], list) else line['held']}")


if __name__ == "__main__":
    main(sys.argv[1])
