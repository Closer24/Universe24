"""Read one record of the engine's own writer and print the band's readings and the animation's table.

Integers only: every mean is a quotient with its remainder, never a ratio in decimals.
Usage: python read_band.py <record.json> <table.tsv> [summary.json]
The table's columns, one row per interval (the animation's own data, for the Reader):
  i content_min content_mean_q content_mean_rem content_max x_min x_max frozen turned births credits refused
"""

import json
import sys
from collections import Counter


sys.set_int_max_str_digits(1000000)  # a record past the law's width carries integers the reader's
# own default refuses to parse: the finding of the cycle lay at the count 2,500,000, named in the report


def mean_of(values: list[int], n: int) -> tuple[int, int]:
    """The mean as the law reads one: the quotient and the remainder of the sum over the count."""
    total = sum(values)
    return total // n, total % n


def read(path: str) -> dict:
    with open(path) as handle:
        return json.load(handle)


def main() -> int:
    record = read(sys.argv[1])
    lines = record["nodes"]
    gamma = int(record["gamma"])
    nodes = int(record["cube"]) ** 3
    births = Counter()
    credits = Counter()
    refused = Counter()
    causes = Counter()
    birth_nodes = {}
    for event in record["log"]:
        kind = event.get("event")
        i = int(event.get("i", 0))
        if kind == "birth":
            births[i] += 1
            birth_nodes.setdefault(i, set()).add(tuple(event.get("node") or ()))
        elif kind == "credit":
            credits[i] += 1
        elif kind == "refused":
            refused[i] += 1
            causes[str(event.get("cause"))] += 1
    rows = []
    seed_x = None
    tops = []
    frozen_lines = []
    at_gamma = []
    at_seed = []
    content_top = (0, 0)
    for line in lines:
        i = int(line["i"])
        content = [int(c) for c in line["content"]]
        xs = [int(x) for x in line["X"]]
        turned = len(line["turned"])
        frozen = len(line["frozen"])
        if seed_x is None:
            seed_x = tuple(xs)
        mq, mr = mean_of(content, nodes)
        rows.append(
            (i, min(content), mq, mr, max(content), min(xs), max(xs), frozen, turned,
             births.get(i, 0), credits.get(i, 0), refused.get(i, 0))
        )
        if max(content) > content_top[0]:
            content_top = (max(content), i)
        if turned == nodes:
            tops.append(i)
        if frozen:
            frozen_lines.append((i, frozen))
        if min(xs) == max(xs) == gamma:
            at_gamma.append(i)
        if tuple(xs) == seed_x and i > 1:
            at_seed.append(i)
    with open(sys.argv[2], "w") as handle:
        handle.write(
            "i\tcontent_min\tcontent_mean_q\tcontent_mean_rem\tcontent_max\tx_min\tx_max\t"
            "frozen\tturned\tbirths\tcredits\trefused\n"
        )
        for row in rows:
            handle.write("\t".join(str(v) for v in row) + "\n")
    marks = record.get("rows", [])
    bits = max((int(m.get("max bits", 0)) for m in marks), default=0)
    transient = max((int(m.get("max transient bits", 0)) for m in marks), default=0)
    alike = sum(1 for line in lines if len(set(int(c) for c in line["content"])) == 1)
    summary = {
        "record": sys.argv[1],
        "intervals": int(record["intervals"]),
        "nodes": nodes,
        "gamma": gamma,
        "seed X": seed_x[0] if seed_x else None,
        "content top (value, interval)": list(content_top),
        "frozen lines (interval, count)": frozen_lines[:40],
        "frozen lines total": len(frozen_lines),
        "tops (every Node turned at once)": tops[:40],
        "tops total": len(tops),
        "at the resolution at every Node": at_gamma[:40],
        "at the seed's own first state": at_seed[:40],
        "alike intervals of all": [alike, len(lines)],
        "births total": sum(births.values()),
        "birth intervals": sorted(births)[:20],
        "nodes bearing per birth interval": {str(k): len(v) for k, v in sorted(birth_nodes.items())[:20]},
        "credits total": sum(credits.values()),
        "refused by cause": dict(causes),
        "max bits (marks)": bits,
        "max transient bits (marks)": transient,
        "run back": record.get("run_back"),
        "counts": record.get("counts"),
    }
    text = json.dumps(summary, indent=1)
    if len(sys.argv) > 3:
        with open(sys.argv[3], "w") as handle:
            handle.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
