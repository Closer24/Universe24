"""Probe: count the draw's outputs (c, room) on a world, with the digits sorted (the head) or in their read order."""
import json, sys
from collections import Counter
import event_universe.draw as draw
import event_universe.bobs as bobs
import event_universe.click as click
import event_universe.run as run

seen = []
orig = draw.vernier
def wrapped(clock, at, gearings, winding):
    out = orig(clock, at, gearings, winding)
    if out is not None:
        seen.append(out)
    return out
bobs.vernier = wrapped
click.vernier = wrapped

world, out_path, label = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    run.main(["run", world, out_path])
except SystemExit:
    pass
n = len(seen)
low = sum(1 for c, r in seen if 2 * c < r)
oct_ = Counter(min(7, (8 * c) // r) for c, r in seen if r > 0)
bits = Counter(r.bit_length() for c, r in seen)
print(json.dumps({"label": label, "draws": n, "c below half the room": low,
                  "fraction below half (thousandths)": (1000 * low) // n if n else None,
                  "octiles": [oct_.get(k, 0) for k in range(8)],
                  "room bits (most common)": bits.most_common(3)}))
