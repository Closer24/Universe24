"""NATURE2: causality's no on the click world, keeping the books: a mated pair forged across a Mesh at round 10 between
the takers (train 4) at sites 0 and 1, whose first clicks come at round 82 or later; q 1 and -1, each tooth at the
birth (the dial odd, the birth its own complement, D - 1 = 2 birth). The forged record is written for the guard and
the books (guardread.py), and its causal order per clock printed. Whole numbers only; no division.

Usage: python3 -I nocause_click.py <tree> <record .jsonl> <forged out .jsonl>
"""

import json
import sys
from pathlib import Path

TREE = Path(sys.argv[1])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)


def meets(e):
    found = [(e["site"], s[0]) for s in e.get("sides", []) if s[1] != 0]
    return found + [(s[1], s[0]) for s in e.get("across", []) if s[2] != 0]


def per_clock(clicks):
    first = {}
    for e in sorted(clicks, key=lambda e: e["round"]):
        if meets(e):
            first.setdefault((e["site"], e["train"]), e["round"])
    start = min(first.values())
    partners = {}
    for e in clicks:
        c = (e["site"], e["train"])
        if first.get(c) == e["round"]:
            partners.setdefault(c, set()).update(meets(e))
    late = [c for c in first if first[c] > start]
    uncaused = sorted(c for c in late if not any(first.get(p, first[c]) < first[c] for p in partners.get(c, set())))
    return len(late), uncaused


rows = [json.loads(t) for t in Path(sys.argv[2]).read_text(encoding="utf-8").splitlines() if t.strip()]
head, end = rows[0], rows[-1]
birth = head["birth"]
assert birth + birth == head["dial"] - 1
clicks = [e for e in rows if e.get("kind") == "click"]
late, uncaused = per_clock(clicks)
print(f"the record: {late} later clocks, {len(uncaused)} uncaused: {'SHOWN' if not uncaused else 'NOT SHOWN'}")
at = {(e["round"], e["site"], e["train"]) for e in clicks}
assert (10, 0, 4) not in at or True
fake = []
for site, other, q in ((0, 1, 1), (1, 0, -1)):
    line = [e for e in clicks if (e["round"], e["site"], e["train"]) == (10, site, 4)]
    if line:
        e = dict(line[0])
        e["across"] = list(e.get("across", [])) + [[4, other, q, birth, birth]]
        e["q"] = e["q"] + q
        fake.append(e)
    else:
        fake.append({"kind": "click", "round": 10, "site": site, "train": 4, "q": q, "sides": [],
                     "across": [[4, other, q, birth, birth]]})
keyed = {(e["round"], e["site"], e["train"]): e for e in clicks}
for e in fake:
    keyed[(e["round"], e["site"], e["train"])] = e
forged = sorted(keyed.values(), key=lambda e: (e["round"], e["site"], e["train"]))
late2, uncaused2 = per_clock(forged)
print(f"the forged record (a mated pair across a Mesh at round 10, takers at sites 0 and 1): {late2} later clocks,"
      f" {len(uncaused2)} uncaused {uncaused2}: {'SHOWN' if not uncaused2 else 'NOT SHOWN'}")
Path(sys.argv[3]).write_text("".join(json.dumps(e) + "\n" for e in [head] + forged + [end]), encoding="utf-8")
print(f"written: {Path(sys.argv[3]).name}")
