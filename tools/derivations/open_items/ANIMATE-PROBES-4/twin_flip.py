"""Toy reading: the twin hands' wind at single clocks, the up twin's and the down twin's, at every top and bottom
(Animate; the owner's word of 2026-10-28, 15:4x UTC: "that the detector's choice influences its choice in the next
bang"). It runs many_bangs.py's set-up beside it (the twin row, the dial variant read at the step, T = J K) and prints,
at every whole-board top and every bottom, the two twins' wind at four clocks: which twin holds more (the sign of the
spin's z part) is read across the bangs.
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

WATCH = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (2, 1, 3)]


def twin_at(clock, at):
    """The up and down twins' wind at one clock."""
    found = []
    for r in clock.hands():
        if r.twin is not None:
            g = readings.gearing_of(clock, r, clock.start_load, clock.start_factors)  # noqa: F821
            found.append(int(hands.wind(clock, r.gears, g)[at]))  # noqa: F821
    return tuple(found)


clock = make_clock()  # noqa: F821
rows = []
for t in range(1, TICKS + 1):
    clock.tick()
    x = int(clock.train(REGULATOR).gears[0].now.max())  # noqa: F821
    rows.append((t, x, int(clock.turned_over.sum()), [twin_at(clock, at) for at in WATCH]))
for i, (t, x, turned, per) in enumerate(rows):
    before = rows[i - 1][1] if i else None
    after = rows[i + 1][1] if i + 1 < len(rows) else None
    bottom = before is not None and after is not None and before > x <= after
    if turned == 64 or bottom or i == len(rows) - 1:
        label = "top" if turned == 64 else ("bottom" if bottom else "end")
        signs = ["up" if u > d else ("down" if d > u else "even") for u, d in per]
        print(f"tick {t} ({label}): the twin ahead at {WATCH}: {signs}; (up, down) winds {per}")
