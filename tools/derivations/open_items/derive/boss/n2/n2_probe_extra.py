"""N2 probe, extra checks: the head's own act under the moving clock, the 00 row's collision at the probe's teeth,
and a longer first-order run. Whole numbers only."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
from n2_lib import (  # noqa: E402
    FAMILIES,
    MATTER,
    ROWS,
    S00,
    Carry,
    State,
    carry,
    gradient_part,
    join,
    lay,
    layout,
    mirror_first,
    mirror_head,
    notch,
    potential,
    rate_part,
    run,
    same,
    spring,
    step,
    terms,
    tick_first,
    tick_head,
)

OUT = []


def say(*xs):
    line = " ".join(str(x) for x in xs)
    print(line)
    OUT.append(line)


SHAPE, REST, GRIP, DRIVE_M, DRIVE_G = (3, 4, 5), 3000, 500, 7, 100
NOW = join(
    terms(spring(210, FAMILIES)), terms(notch(5000)), terms(potential(1)), terms(gradient_part(1))
)
RATE, NONE = terms(rate_part(1)), terms([])
Lm = layout(SHAPE, REST, REST, GRIP, DRIVE_M, DRIVE_G, clock="every")
Lf = layout(SHAPE, REST, REST, GRIP, DRIVE_M, DRIVE_G, clock="others")

# 1. the head's own act, no term 5 at all, the clock moving: its G1 limit, not N2's
for seed in (16, 17):
    states, k, rows = run(tick_head, mirror_head, Lm, lay(Carry(seed), Lm), 300, NOW, NONE, parity=False)
    say(
        f"head's act with no term 5, the clock moving, lay {seed}: the run back departs at round back {k}"
    )

# 2. the 00 row reading its own count as teeth: two post-kick states one count apart drift to one state
n = Lm.nb.shape[1]
a = np.zeros((ROWS, n), dtype=object)
p = np.zeros((ROWS, n), dtype=object)
p[S00, 0] = 5 * REST  # p = (R + x) k at x = 0, k = 5
s1, s2 = State(a, p, 0 * a, 0 * a), State(a.copy(), p.copy(), 0 * a, 0 * a)
s2.a[S00, 0] = 1


def drift(L_, s_):
    w = step.weight(L_.gearing, L_.clock, s_.a)
    q, _ = carry(s_.b, w, 0)
    return s_.a + q


d1, d2 = drift(Lm, s1), drift(Lm, s2)
say(
    f"00 row reading itself (rest {REST}): 00 counts 0 and 1 with p = {5 * REST} both drift to "
    f"{d1[S00, 0]} and {d2[S00, 0]}; whole states equal after the drift: {np.array_equal(d1, d2)}"
)
d1, d2 = drift(Lf, s1), drift(Lf, s2)
say(f"00 row at rest teeth: the same two drift to {d1[S00, 0]} and {d2[S00, 0]}")

# 3. a longer first-order run with the clock moving
states, k, rows = run(tick_first, mirror_first, Lf, lay(Carry(26), Lf, first=True), 800, NOW, RATE)
w = [step.weight(Lf.gearing, Lf.clock, st.a)[MATTER[0]] for st in states]
falls = sum(int((w[t + 1] < w[t]).sum()) for t in range(len(w) - 1))
rises = sum(int((w[t + 1] > w[t]).sum()) for t in range(len(w) - 1))
say(
    f"first-order form, 800 rounds, the clock moving ({rises} site-rounds rising, {falls} falling, W in "
    f"[{min(min(x) for x in w)}, {max(max(x) for x in w)}]): forth and back bit for bit: {k is None}; "
    f"the state moved: {not same(states[-1], states[0])}"
)

(Path(__file__).resolve().parent / "n2_results_extra.txt").write_text(
    "\n".join(OUT) + "\n", encoding="utf-8"
)
