"""STOP1 reader: a train's beat and swing on the board, read from a run's ledger (the counts per round, per Node-clock
and train), a clock fact of the board. For the train and Node-clock named: the sign changes of each of its rows in the
run, the first rounds of the first changes, the rounds per sign change (by Rule3's carry), and the widest swing per
block of rounds. Usage: python -I beats.py <ledger .jsonl> <train> [site=0] [block=500]
Whole numbers only; Rule3's carry the one division.
"""

import json
import sys
from pathlib import Path

LEDGER, TRAIN = Path(sys.argv[1]), int(sys.argv[2])
opts = dict(x.split("=", 1) for x in sys.argv[3:] if "=" in x)
SITE, BLOCK = int(opts.get("site", 0)), int(opts.get("block", 500))
sys.path.insert(0, str(Path(__file__).resolve().parents[1].joinpath("tree", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

rows = None
for text in LEDGER.read_text(encoding="utf-8").splitlines():
    line = json.loads(text)
    if line["site"] != SITE or line["train"] != TRAIN:
        continue
    counts = line["count"]
    if rows is None:
        rows = [[] for _ in counts]
    for r, x in enumerate(counts):
        rows[r].append(int(x))
assert rows is not None, "no line for that train and site"
n = len(rows[0])
print(f"ledger {LEDGER.parent.parent.name}/{LEDGER.parent.name}: train {TRAIN}, site {SITE}, {n} rounds, {len(rows)} rows")
for r, xs in enumerate(rows):
    if not any(xs):
        continue
    changes, last, firsts = 0, 0, []
    for at, x in enumerate(xs, start=1):
        sign = (x > 0) - (x < 0)
        if sign and last and sign != last:
            changes += 1
            if len(firsts) < 6:
                firsts.append(at)
        if sign:
            last = sign
    per, _ = carry(n, changes, 0) if changes else (None, None)
    swings = []
    for lo in range(0, n, BLOCK):
        swings.append(max(abs(x) for x in xs[lo:lo + BLOCK]))
    print(f"  row {r}: {changes} sign changes, the first at rounds {firsts}; rounds per change {per}; "
          f"widest |count| per {BLOCK} rounds {swings}")
