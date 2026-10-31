"""NATURE2's label-rule probe: the click world's record against its swapped lay's record (trains 3 and 4, giver and
taker, exchanged in the files with their gears), the second relabelled back (3 <-> 4 in every line's train and every
side's partner), each line's sides put in the other train's order. Lines compared on (round, site, train, q, sides
(u, q, k_before, k_after)) and on (round, site, train, q, sides (u, q)). Whole numbers only; no division.

Usage: python3 -I swapcmp.py <tree> <record .jsonl> <swapped record .jsonl>
"""

import json
import sys
from pathlib import Path

TREE = Path(sys.argv[1])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

SWAP = {3: 4, 4: 3}


def lines(path, swap):
    out = {}
    for t in Path(path).read_text(encoding="utf-8").splitlines():
        e = json.loads(t)
        if e.get("kind") != "click":
            continue
        train = swap.get(e["train"], e["train"])
        sides = sorted([swap.get(s[0], s[0]), s[1], s[2], s[3]] for s in e.get("sides", []))
        out[(e["round"], e["site"], train)] = (e["q"], tuple(tuple(s) for s in sides))
    return out


def main():
    a = lines(sys.argv[2], {})
    b = lines(sys.argv[3], SWAP)
    keys = sorted(set(a) | set(b))
    full = [k for k in keys if a.get(k) == b.get(k)]
    qonly = [k for k in keys if a.get(k) and b.get(k) and a[k][0] == b[k][0]
             and tuple((s[0], s[1]) for s in a[k][1]) == tuple((s[0], s[1]) for s in b[k][1])]
    apart = [k for k in keys if a.get(k) != b.get(k)]
    print(f"lines: {len(a)} and {len(b)} (relabelled); alike with teeth {len(full)} of {len(keys)};"
          f" alike on q and partners {len(qonly)} of {len(keys)}; first apart {apart[:1]}")
    if apart:
        k = apart[0]
        print(f"  at {k}: record {a.get(k)}; swapped, relabelled {b.get(k)}")
    print(f"the label rule: {'SHOWN' if not apart else 'NOT SHOWN'}")
    raw = lines(sys.argv[3], {})
    raw_apart = [k for k in sorted(set(a) | set(raw)) if a.get(k) != raw.get(k)]
    print(f"its no, the swapped record read without the relabelling: {len(raw_apart)} lines apart, first"
          f" {raw_apart[:1]}: {'NOT SHOWN' if raw_apart else 'SHOWN'}")


main()
