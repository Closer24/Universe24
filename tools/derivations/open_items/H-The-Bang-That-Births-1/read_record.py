"""Read a record written by event_universe.run and print the bang's own table: per interval the
content (min, mean, max), the volume (min, mean, max), the frozen Nodes, the turns, the births and the
credits, the spread in thousandths, and the returns of the board's volume vector to an earlier one.
Integers only. Usage: python read_record.py <record.json> <table.tsv> [every N]"""
from __future__ import annotations
import json
import sys


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    path, table = argv[1], argv[2]
    every = int(argv[3]) if len(argv) > 3 else 1
    rec = json.load(open(path))
    lines = rec["nodes"]
    log = rec.get("log") or []
    births: dict[int, int] = {}
    credits: dict[int, int] = {}
    refused: dict[str, int] = {}
    refused_first: dict[str, int] = {}
    for ev in log:
        i = int(ev.get("i", 0))
        kind = ev.get("event")
        if kind == "birth":
            births[i] = births.get(i, 0) + 1
        elif kind == "credit":
            credits[i] = credits.get(i, 0) + 1
        elif kind == "refused":
            cause = str(ev.get("cause"))
            refused[cause] = refused.get(cause, 0) + 1
            refused_first.setdefault(cause, i)
    gamma = int(rec["gamma"])
    seen: dict[str, int] = {}
    returns = []
    rows = []
    frozen_lines = []
    bangs = []
    tops = []
    for line in lines:
        i = int(line["i"])
        xs = [int(x) for x in line["X"]]
        cs = [int(c) for c in line["content"]]
        n = len(xs)
        key = ",".join(str(x) for x in xs)
        if key in seen:
            returns.append((i, seen[key]))
        else:
            seen[key] = i
        mean = sum(xs) // n
        bits = max(abs(x) for x in xs).bit_length()
        spread = ((max(xs) - min(xs)) * 1000) // mean if mean else 0
        frozen = len(line["frozen"])
        turned = len(line["turned"])
        held = len(line["held"])
        if frozen:
            frozen_lines.append((i, frozen, held, min(cs), max(cs)))
        if turned:
            tops.append((i, turned))
        if min(xs) == max(xs) == gamma:
            bangs.append(i)
        rows.append(
            (i, min(cs), sum(cs) // n, max(cs), min(xs), mean, max(xs), spread, frozen, turned,
             held, births.get(i, 0), credits.get(i, 0), bits)
        )
    with open(table, "w") as out:
        out.write("i\tc_min\tc_mean\tc_max\tx_min\tx_mean\tx_max\tspread\tfrozen\tturned\theld\tbirths\tcredits\tx_bits\n")
        for r in rows:
            if int(r[0]) % every == 0 or r[8] or r[9] or r[11] or r[12]:
                out.write("\t".join(str(v) for v in r) + "\n")
    alike = sum(1 for r in rows if r[7] == 0)
    print(json.dumps({
        "record": path,
        "intervals": rec["intervals"],
        "counts": rec["counts"],
        "turns": rec["turns"],
        "run_back": rec["run_back"],
        "content max": max(r[3] for r in rows),
        "content max at": max(rows, key=lambda r: r[3])[0],
        "volume max": max(r[6] for r in rows),
        "bits max": max(r[13] for r in rows),
        "bits by interval": [(r[0], r[13]) for r in rows if r[0] % 2 == 0][:24],
        "alike intervals": alike,
        "of": len(rows),
        "frozen lines": frozen_lines[:12],
        "frozen lines count": len(frozen_lines),
        "turn intervals": tops[:12],
        "turn intervals count": len(tops),
        "bangs at the resolution": bangs[:12],
        "bangs count": len(bangs),
        "returns (interval, to)": returns[:12],
        "returns count": len(returns),
        "births total": sum(births.values()),
        "births by interval": sorted(births.items())[:12],
        "credits total": sum(credits.values()),
        "refused by cause": refused,
        "refused first interval": refused_first,
    }))


if __name__ == "__main__":
    main(sys.argv)
