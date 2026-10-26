"""The band's scan on the fifth form (the cycle lay): the record run from the seed through the engine's
own writer (event_universe.run.record) at each count, and read for the first birth round's count of
Nodes, the board's likeness (the spread 0 at every interval), the content reached and the frozen Nodes.
Integers only. Usage: python scan_counts.py <universe.json> <intervals> <out.json> <count> [<count> ..]"""
from __future__ import annotations
import json
import sys

from event_universe.run import record

DIGITS = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]


def one(universe: dict, n: int, intervals: int) -> dict:
    world = {
        "universe": "universe_ga2.json",
        "shape": [4, 4, 4],
        "intervals": intervals,
        "seed": [{"lay": "wave", "row": 0, "quanta": n, "p1": DIGITS, "cz": 1, "mirror": 0}],
    }
    rec = record(universe, world, 0, lambda _s: None)
    births: dict[int, int] = {}
    for ev in rec["log"]:
        if ev.get("event") == "birth":
            births[int(ev["i"])] = births.get(int(ev["i"]), 0) + 1
    alike = 0
    content = 0
    frozen = 0
    bits = 0
    for line in rec["nodes"]:
        xs = [int(x) for x in line["X"]]
        alike += int(min(xs) == max(xs))
        content = max(content, max(int(c) for c in line["content"]))
        frozen = max(frozen, len(line["frozen"]))
        bits = max(bits, max(abs(x) for x in xs).bit_length())
    return {
        "count": n,
        "births": sorted(births.items()),
        "births total": sum(births.values()),
        "first round nodes": (sorted(births.items())[0][1] if births else 0),
        "alike intervals": alike,
        "of": len(rec["nodes"]),
        "content max": content,
        "frozen max": frozen,
        "bits max": bits,
        "body clicks": rec["counts"]["body_clicks"],
        "refused lay": rec["counts"]["refused_lay"],
    }


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    universe = json.load(open(argv[1]))
    intervals = int(argv[2])
    out = argv[3]
    found = []
    for text in argv[4:]:
        row = one(universe, int(text), intervals)
        found.append(row)
        print(json.dumps(row), flush=True)
    json.dump(found, open(out, "w"))


if __name__ == "__main__":
    main(sys.argv)
