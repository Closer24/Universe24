"""The order test on stage 7a's full act: random schedules that bring every Node-clock to the same count equal the
synchronous pass bit for bit, J on, the drive at T_d > 1, rates parted and one clock stopped; then the whole run back.

Usage: PYTHONPATH=<worktree>/src:<worktree> python -P order_full_act.py
"""

import numpy as np

from tensor24.engine import step
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests.test_the_tensor24_act import varied, world

COUNT = 6


def run(seed, schedules=8):
    rng = np.random.default_rng(seed)
    layout = varied(rng, alike=True)  # W+ = W: one layout over many rounds keeps r within [0, W)
    layout = layout._replace(gearing=layout.gearing._replace(drive=layout.gearing.drive + 1))  # every T_d >= 2
    rate = layout.rate.copy()
    rate[0, 4] = 0  # a stopped clock
    layout = layout._replace(rate=rate)
    s0 = world(rng, layout)
    s0 = s0._replace(rd=s0.rd % layout.gearing.drive, c=0 * s0.c, tn=0 * s0.tn)
    n = layout.nb.shape[1]
    sync, _ = rounds(step.tick, layout, s0, [np.ones((1, n), dtype=object)] * COUNT)
    alike = back = 0
    for _ in range(schedules):
        s, outs = s0, []
        while (s.c < COUNT).any():
            mask = rng.integers(0, 2, (1, n)).astype(object) * (s.c < COUNT)
            s, o = step.tick(layout, s, mask)
            outs.append(o)
        alike += all(np.array_equal(x, y) for x, y in zip(s, sync, strict=True))
        back += all(np.array_equal(x, y) for x, y in zip(rewind(step.untick, layout, s, outs), s0, strict=True))
    return alike, back, schedules, int(np.array([x != 0 for x in sync.rd.flat]).sum())


for seed in range(4):
    alike, back, total, moved = run(seed)
    print(f"seed {seed}: {alike} of {total} random schedules equal the synchronous pass at count {COUNT}; {back} of {total} run back exactly; drive teeth not 0 at the end: {moved}")
