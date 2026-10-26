"""RW-T1 measured: carried_division(t, w, r, -1) == (q, w - 1 - r'') with (q, r'') = carried_division(t, w, w - 1 - r, +1), on the head's own division (no flag), and the inverse exact: the forward division then the backward on its remainder returns (q, r). Usage: division_mirror_test.py <src> [count]"""
import random
import sys

sys.path.insert(0, sys.argv[1])
from event_universe.core.rule3 import carried_division as cd, mirrored  # noqa: E402

n = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
random.seed(3)
mirror_same = inverse_exact = 0
for _ in range(n):
    w = random.randint(1, 10**6)
    r = random.randint(0, w - 1)
    t = random.randint(-(10**12), 10**12)
    q, r2 = cd(t, w, r, 1)
    b, r3 = cd(t, w, r2, -1)
    inverse_exact += (q == b) and (r3 == r)
    qm, rm = cd(t, w, mirrored(r2, w, 1), 1)
    mirror_same += (b, r3) == (qm, mirrored(rm, w, 1))
print({"triples": n, "inverse exact": inverse_exact, "the act at -1 the act at +1 under the mirror": mirror_same})
