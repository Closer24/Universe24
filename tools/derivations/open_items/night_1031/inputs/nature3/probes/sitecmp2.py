"""NATURE3: the test's lay against the shipped lay site by site, two ways: (q) the click world's content alone (each
line's train, q and its sides' partners and q), and (k) the whole line with its teeth (board fields carried for the
checks), a board check. For each, the first round apart by site, and one site's lines alike counted from both records'
sides. Whole numbers only; no division.

Usage: python3 -I sitecmp2.py <shipped record .jsonl> <test record .jsonl> <site to count>
"""

import json
import sys
from pathlib import Path


def lines(path, teeth):
    out = {}
    for t in Path(path).read_text(encoding="utf-8").splitlines():
        e = json.loads(t)
        if e.get("kind") != "click":
            continue
        sides = tuple(tuple(s) if teeth else (s[0], s[1]) for s in e.get("sides", []))
        across = tuple(tuple(s) if teeth else (s[0], s[1], s[2]) for s in e.get("across", []))
        out[(e["round"], e["site"], e["train"])] = (e["q"], sides, across)
    return out


site = int(sys.argv[3])
for name, teeth in (("(q) the click world's content", False), ("(k) the whole line with its teeth, a board check", True)):
    a, b = lines(sys.argv[1], teeth), lines(sys.argv[2], teeth)
    first = {}
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            first.setdefault(k[1], k[0])
    rounds = {}
    for x, r in first.items():
        rounds.setdefault(r, []).append(x)
    at_a = [k for k in a if k[1] == site]
    at_b = [k for k in b if k[1] == site]
    same = [k for k in at_b if a.get(k) == b[k]]
    print(f"{name}: sites apart {len(first)} of 27; first round apart: "
          + "; ".join(f"round {r}: sites {sorted(xs)}" for r, xs in sorted(rounds.items())))
    print(f"  site {site}: {len(same)} lines alike, of {len(at_b)} test lines and {len(at_a)} shipped lines")
