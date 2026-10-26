"""Beneath Rule3 (H-Node-Beneath-Rule3-1): the slot exchange with the mirror, the direction -1 and the lay as compositions of the one forward carried division with its quotient laid on a slot, on random lines: (a) the quarter turn Q is Rule3's step with no Links and the own weight 0 (the mass 2 w): (a, y, r) -> (-y, a, r); (b) the negation of a level is the move of -2 a (the division of -2 a w at the wall, the quotient laid); (c) the mirror of the remainder is the forward division of the numerator w - 1 - 2 r (the quotient 0, the remainder w - 1 - r); (d) the exchange X = mirror o negate_now o Q; (e) the division at -1 is mirror o division(+1) o mirror on the remainder with the quotient the same; so every act is the one forward division with its quotient laid. Usage: one_act_nl1.py <core dir> <count>."""

import importlib.util
import json
import random
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("core_nl1", Path(sys.argv[1]) / "core_nl1.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
count = int(sys.argv[2])
rng = random.Random(3)
found = {"quarter_turn": 0, "negation_is_move": 0, "mirror_is_division": 0, "exchange_is_composition": 0, "direction_is_composition": 0, "count": count}
for _ in range(count):
    w = rng.randint(2, 1 << 60)
    r = rng.randint(0, w - 1)
    a, y = rng.randint(-(1 << 40), 1 << 40), rng.randint(-(1 << 40), 1 << 40)
    q = core.step(a, y, r, 0, w, 0, [0] * 6, [0] * 6, 1)
    found["quarter_turn"] += q == (-y, a, r)
    neg = core.move(q[0], -(q[0] + q[0]), w, q[2])
    found["negation_is_move"] += neg == (y, r)
    mir = core.divide(w - 1 - 2 * r, w, r, 1)
    found["mirror_is_division"] += mir == (0, w - 1 - r)
    found["exchange_is_composition"] += (neg[0], q[1], mir[1]) == core.exchange(a, y, r, w)
    t = rng.randint(-(1 << 100), 1 << 100)
    back = core.divide(t, w, r, -1)
    m1 = core.divide(w - 1 - 2 * r, w, r, 1)[1]
    fwd = core.divide(t, w, m1, 1)
    m2 = core.divide(w - 1 - 2 * fwd[1], w, fwd[1], 1)[1]
    found["direction_is_composition"] += back == (fwd[0], m2)
print(json.dumps(found))
