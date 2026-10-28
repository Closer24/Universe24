"""Toy reading: the click events per bang (Animate; the owner's word of 2026-10-28, 15:0x UTC, on law 10's missing part:
"think in clocks and the tensor"). It runs many_bangs.py's set-up (beside it, on draft C's tree at 33d9ecaa) and counts
the log's events in each bang (a bang runs from one bottom of the largest X to the next), the refusals by their cause.
Settings by environment variable: VARIANT (dial or dial_nof2), QUANTA, TICKS, TWIN (1 by default, empty for the A1
calibre), READ, TENSION and CONE as in many_bangs.py. A refusal by name ends the run and the counts to it are printed.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("TREE", "/tmp/reader/t24")
QUANTA, TICKS = int(os.environ.get("QUANTA", "5000000")), int(os.environ.get("TICKS", "494"))
sys.argv = [
    os.path.join(HERE, "many_bangs.py"),
    ROOT,
    os.environ.get("VARIANT", "dial"),
    str(QUANTA),
    "0",
]
os.environ.setdefault("READ", "step")
os.environ.setdefault("TWIN", "1")
sys.path[:0] = [ROOT + "/src", ROOT, HERE]
exec(open(os.path.join(HERE, "many_bangs.py")).read().split("click.click = booked")[0])  # noqa: S102

clock = make_clock()  # noqa: F821
xs = []
refused = None
for _ in range(TICKS):
    try:
        clock.tick()
    except ValueError as err:
        refused = (clock.ticks, str(err))
        break
    xs.append(int(clock.train(REGULATOR).gears[0].now.max()))  # noqa: F821
if refused:
    print("refused at tick", refused[0], refused[1])
bottoms = [0] + [t + 1 for t in range(1, len(xs) - 1) if xs[t - 1] > xs[t] <= xs[t + 1]]
counts = {}
for e in clock.log:
    bang = sum(1 for b in bottoms if b < e["i"])
    key = e["event"] if e["event"] != "refused" else "refused:" + str(e.get("cause"))
    counts.setdefault(bang, {})
    counts[bang][key] = counts[bang].get(key, 0) + 1
print(f"quanta {QUANTA}, ticks {TICKS}, bottoms at {bottoms}")
for bang in sorted(counts):
    print(f"  bang {bang}: {dict(sorted(counts[bang].items()))}")
print(
    "splits in all:", sum(c.get("split", 0) for c in counts.values()), "births:", clock.counts["births"]
)
