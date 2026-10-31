"""NATURE3: a test's lay against the shipped lay, site by site (a board check of the record against two lays): for each
site, the first round at which its click lines (train, q, sides' partners and q, across) differ, and the lines alike
at one site; whether the takers pass a quantum; across sides written. Whole numbers only; no division.

Usage: python3 -I sitecmp.py <shipped record .jsonl> <test record .jsonl> <site to count>
"""

import json
import sys
from pathlib import Path


def lines(path):
    out = {}
    for t in Path(path).read_text(encoding="utf-8").splitlines():
        e = json.loads(t)
        if e.get("kind") == "click":
            out[(e["round"], e["site"], e["train"])] = (
                e["q"], tuple((s[0], s[1]) for s in e.get("sides", [])), tuple((s[0], s[1], s[2]) for s in e.get("across", [])))
    return out


a, b = lines(sys.argv[1]), lines(sys.argv[2])
count_site = int(sys.argv[3])
keys = set(a) | set(b)
first_apart = {}
for r, x, t in sorted(keys):
    if a.get((r, x, t)) != b.get((r, x, t)):
        first_apart.setdefault(x, r)
sites = sorted({x for _, x, _ in keys})
alike_none = [x for x in sites if x not in first_apart]
order = sorted(first_apart.items(), key=lambda kv: (kv[1], kv[0]))
print(f"sites: {len(sites)}; sites whose lines differ: {len(first_apart)}; alike throughout: {alike_none}")
print("first round apart, by site: " + " ".join(f"{x}:{r}" for x, r in sorted(first_apart.items())))
at = [k for k in b if k[1] == count_site]
same = [k for k in at if a.get(k) == b[k]]
print(f"site {count_site}: {len(same)} of {len(at)} test lines alike with the shipped record's")
passing_takers = sorted({k for k, v in b.items() if k[2] == 4 and any(s[1] != 0 for s in v[1])})
print(f"taker lines (train 4) passing a quantum in the test record: {len(passing_takers)}; across sides written:"
      f" {sum(len(v[2]) for v in b.values())}")
