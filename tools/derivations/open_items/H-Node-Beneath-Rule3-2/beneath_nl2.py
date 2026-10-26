"""The identities beneath Rule3, checked on random integers (H-Node-Beneath-Rule3-2): (1) the direction is the sign on the total and the quotient, divide(t, w, r, -1) = (-q, r2) with (q, r2) = divide(-t, w, r, 1), and both equal rule3.carried_division; (2) the mirror is the remainder of the complement, w - 1 - r = divide(-1 - r, w, 0)[1] = divide(-1 - 2 r, w, r)[1]; (3) the lay is the division of an exact multiple of the wall with the level carried in the numerator, divide(w (a + c), w, r) = (a + c, r); (4) the write is one division with the level carried in the numerator, divide(ww a + n, ww, wr) = (a + q, wr2) with (q, wr2) = divide(n, ww, wr); (5) the backward act is the ceiling's reading of the one number: N = w a - r with 0 <= r < w gives divide(N + w - 1, w, 0) = (a, w - 1 - r), the mirror the shift w - 1 between the floor's and the ceiling's reading; (6) X R X = R^-1 on a line: the step at -1 equals the slot exchange, the step at +1, the slot exchange (CA-S1). Counts of 20,000 each.

Usage: PYTHONPATH=<worktree>/src python beneath_nl2.py
"""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path

from event_universe.core.rule3 import carried_division, mirrored

spec = importlib.util.spec_from_file_location("core_nl2", Path(__file__).with_name("core_nl2.py"))
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

random.seed(2)
N = 20000
held = {k: 0 for k in ("direction", "mirror", "lay", "write", "ceiling", "xrx")}
for _ in range(N):
    w = random.randint(1, 1 << 60)
    r = random.randint(0, w - 1)
    t = random.randint(-(1 << 90), 1 << 90)
    q, r2 = core.divide(-t, w, r, 1)
    back = core.divide(t, w, r, -1)
    held["direction"] += back == (-q, r2) == carried_division(t, w, r, -1) and core.divide(t, w, r, 1) == carried_division(t, w, r, 1)
    held["mirror"] += core.mirror(r, w, 1) == w - 1 - r == core.divide(-1 - r, w, 0)[1] == core.divide(-1 - 2 * r, w, r)[1] == mirrored(r, w, 1)
    a, c = random.randint(-(1 << 60), 1 << 60), random.randint(-(1 << 40), 1 << 40)
    held["lay"] += core.divide(w * (a + c), w, r, 1) == (core.lay(a, c), r)
    n = random.randint(-(1 << 90), 1 << 90)
    held["write"] += core.divide(w * a + n, w, r, 1) == core.write(a, r, n, w, 1)
    held["ceiling"] += core.divide(w * a - r + w - 1, w, 0, 1) == (a, w - 1 - r)
    # a line (now, before, r) stepped forward with own S, wall w, flux f (the Links' part read once)
    now, before = random.randint(-(1 << 50), 1 << 50), random.randint(-(1 << 50), 1 << 50)
    own, flux = random.randint(-(1 << 61), 1 << 61), random.randint(-(1 << 90), 1 << 90)
    nxt, _start, r_next = core.rotate(now, before, r, own, w, flux, 1)
    # the step at -1 from (now slot = nxt, before slot = now, r_next): the pairs reversed, the same flux
    prev, _s, r_prev = core.rotate(now, nxt, r_next, own, w, flux, -1)
    # X R X: exchange, step at +1 on the exchanged slots, exchange back
    x_now, x_before, x_rem = core.exchange(nxt, now, r_next, w, 1)
    y_lead, y_start, y_rem = core.rotate(x_now, x_before, x_rem, own, w, flux, 1)
    z_now, z_before, z_rem = core.exchange(y_lead, y_start, y_rem, w, 1)
    held["xrx"] += (prev, r_prev) == (before, r) and (z_now, z_before, z_rem) == (now, before, r)
print(json.dumps({"of": N, **held}))
