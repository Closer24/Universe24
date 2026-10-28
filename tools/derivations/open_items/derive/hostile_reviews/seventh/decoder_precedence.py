"""Row 15's precedence at the head (823690afc) against its own docstring: "shown where every whole click's books close and
the wind agrees at every round with a click; not shown where either fails at a part read; not read where the ledger's
lines are read at no round with a click, or at some alone".

usage: python3 -I decoder_precedence.py <worktree> <scratch folder>

Two records with one click whose books open: beside a click that lacks a field (the books read at a part), and beside
a ledger read at some rounds alone (the wind read at a part). The docstring reads both NOT SHOWN.
"""

import json
import sys
from pathlib import Path

WT, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(WT / "src"))
from tensor24.decoder import books, records  # noqa: E402

SCRATCH.mkdir(parents=True, exist_ok=True)
H = {"kind": "header", "record": "tensor24", "major": 1, "minor": 0}
E = {"kind": "end", "rounds": 1, "digest": "", "undone": 0, "exact": 1}


def hold(t, w, k=(0, 0)):
    return {"train": t, "windings": list(w), "kept": list(k)}


def click(r, s, taken, laid):
    return {"kind": "whole", "round": r, "site": s, "count": r, "train": 1, "taken": taken, "laid": laid, "ends": []}


def ledger(r, held):
    return [{"round": r, "at": a, "train": t, "wind": v} for t, pair in held.items() for a, v in zip(("step", "clicks"), pair)]


def read(lines):
    p = SCRATCH / "r.jsonl"
    p.write_text("".join(json.dumps(x) + "\n" for x in lines), encoding="utf-8")
    return records.read(str(p))[0]


opened = click(1, 1, [hold(1, (7, 4), (3, 3))], [hold(0, (0, 4))])  # 3 windings taken, 4 laid: the books open by 1
lacking = {k: v for k, v in click(1, 0, [hold(1, (7, 4), (3, 2))], [hold(0, (0, 4))]).items() if k != "taken"}
both = read([H, lacking, opened, E])
v = books.row_15(both, ledger(1, {0: (0, 8), 1: (10, 2)}))
print(f"a click that lacks its taken, and a click whose books open:\n    docstring: NOT SHOWN\n    head:      {v['kind']}: {v['cause']}")
two = read([H, opened, {**opened, "round": 1 + 1, "count": 1 + 1}, E])
v = books.row_15(two, ledger(1, {0: (0, 4), 1: (10, 6)}))
print(f"two clicks whose books open, the ledger read at round 1 alone and agreeing:\n    docstring: NOT SHOWN\n    head:      {v['kind']}: {v['cause']}")
