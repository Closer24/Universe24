"""NATURE1's second reader: per edge kind (the two trains an edge joins, in-site or across), the books edge by edge,
and on a record with across sides the chain of first clicks by site. Whole numbers only; no division at all.

Usage: python -I edges_front.py <tree> <record .jsonl> <label>
"""

import json
import sys
from pathlib import Path

TREE = Path(sys.argv[1])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)


def main():
    rows = [json.loads(t) for t in Path(sys.argv[2]).read_text(encoding="utf-8").splitlines() if t.strip()]
    head = rows[0]
    clicks = [e for e in rows if e.get("kind") == "click"]
    dial = head.get("dial", 0)
    labels = {}
    trains = head.get("trains", [])
    for t in trains if isinstance(trains, list) else []:
        labels[t.get("index")] = t.get("label")
    keys = sorted({t.get("key") for t in trains if isinstance(t, dict)}) if isinstance(trains, list) else []
    print(f"== {sys.argv[3]}: dial {dial}, train keys {keys}, dial = 3 x key: {[3 * k == dial for k in keys]}")
    at = {(e["round"], e["site"], e["train"]): e for e in clicks}
    kinds = {}
    for e in clicks:
        for u, q, kb, ka in e.get("sides", []):
            far = at.get((e["round"], e["site"], u))
            mate = [s for s in (far or {}).get("sides", []) if s[0] == e["train"]]
            ok = len(mate) == 1 and mate[0][1] == -q and mate[0][2] + kb == dial - 1 and mate[0][3] + ka == dial - 1
            key = ("in-site", min(e["train"], u), max(e["train"], u))
            held = kinds.setdefault(key, [0, 0, 0, 0])
            held[0] += 1
            held[1] += 0 if ok else 1
            held[2] += abs(q)
            held[3] += 1 if q else 0
        for u, y, q, kb, ka in e.get("across", []):
            far = at.get((e["round"], y, u))
            mate = [s for s in (far or {}).get("across", []) if s[0] == e["train"] and s[1] == e["site"]]
            ok = len(mate) == 1 and mate[0][2] == -q and mate[0][3] + kb == dial - 1 and mate[0][4] + ka == dial - 1
            key = ("across", min(e["train"], u), max(e["train"], u))
            held = kinds.setdefault(key, [0, 0, 0, 0])
            held[0] += 1
            held[1] += 0 if ok else 1
            held[2] += abs(q)
            held[3] += 1 if q else 0
    for (where, t, u), (n, bad, quanta, landed) in sorted(kinds.items()):
        print(f"edge {where} ({t} {labels.get(t)}, {u} {labels.get(u)}): {n} sides read from both ends,"
              f" {bad} without their mate, {landed} with q not 0, {quanta} quanta counted at both ends")
    # the chain of first clicks by site, where across sides are written
    if any(e.get("across") for e in clicks):
        first = {}
        for e in sorted(clicks, key=lambda e: e["round"]):
            first.setdefault(e["site"], e["round"])
        sites = sorted(first)
        print(f"sites with lines: {len(sites)}, from {sites[0]} to {sites[-1]}; sites with none:"
              f" {sorted(set(range(sites[0], sites[-1] + 1)) - set(sites))[:10]}")
        print("first round by site: " + " ".join(f"{x}:{first[x]}" for x in sites))
        steps = {}
        for x, y in zip(sites, sites[1:]):
            if y == x + 1:
                d = first[y] - first[x]
                steps[d] = steps.get(d, 0) + 1
        print(f"first-round differences between neighbouring site indices (a board geometry, read as a check of the"
              f" record against the board): {dict(sorted(steps.items()))}")
        across_first = {}
        for e in sorted(clicks, key=lambda e: e["round"]):
            if e.get("across"):
                across_first.setdefault(e["site"], e["round"])
        same = sum(1 for x in across_first if across_first[x] == first[x])
        print(f"sites whose first line carries an across side: {same} of {len(first)}")


main()
