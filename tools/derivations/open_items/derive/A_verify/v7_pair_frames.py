"""V7 (verifier A): the head's fitted pairs in the step's own conserved form.

For every fitting the head lays: its two ends' pawl frames eps (1 - 2 * the ratchet's fine bit) and lapse weights
lam = w / (X mr^2) (vacuum units), the pair's plain charge W_minus + W_plus (0 by F1) and its Q* share
eps_minus lam_minus W_minus + eps_plus lam_plus W_plus, which the step keeps (v1, v3, v6).
Also the coupled hands' plain charge per tick on this world (is the bang's 'kept' trivially empty matter?).
argv: world file, ticks.
"""
import sys
from fractions import Fraction
from pathlib import Path

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src']
import numpy as np  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe import tick as T, readings  # noqa: E402
from event_universe.meshes import coupling_of  # noqa: E402
from event_universe.trains import REGULATOR, ratchet_of  # noqa: E402

world, ticks = sys.argv[1], int(sys.argv[2])
calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + world))
clock = Clock(calibre, piece)
G = clock.full_rate
w_ref = int(clock.teeth) * G
coupled = [k for k, h in enumerate(clock.hands()) if coupling_of(h) == 1]
rows, nonzero_sites = [], []
orig_click = T.Tick.click


def click(self):
    clk = self.clock
    eps = 1 - 2 * np.asarray(ratchet_of(clk.trains_).gears[0].fine, dtype=object)
    load = readings.load(clk)
    mr = np.asarray(readings.rates_of(clk, load)[1], dtype=object) * np.ones(clk.size, dtype=object)
    X = np.asarray(clk.train(REGULATOR).gears[0].now, dtype=object)
    w = readings.mean_teeth(clk, clk.train(REGULATOR).gears[0])
    w = w * np.ones(clk.size, dtype=object)
    nonzero_sites.append((clk.ticks, {k: int(sum(1 for v in (clk.hands()[k].gears[0].now != 0).flat if v)
                                         + sum(1 for v in (clk.hands()[k].gears[1].now != 0).flat if v)) for k in coupled}))
    log_from = len(clk.log)
    orig_click(self)
    for e in clk.log[log_from:]:
        if e.get("event") != "birth" or "takes" in e:
            continue
        s = e["line_pair"]
        g = clk.hands()[s].gears
        out = []
        for where in (tuple(e["minus"]), tuple(e["plus"])):
            Wv = int(g[0].now[where]) * int(g[1].before[where]) - int(g[1].now[where]) * int(g[0].before[where])
            lam = Fraction(int(w[where]) * G ** 3, w_ref * int(X[where]) * int(mr[where]) ** 2)
            out.append((int(eps[where]), lam, Wv))
        plain = out[0][2] + out[1][2]
        star = sum(ep * lam * Wv for ep, lam, Wv in out)
        rows.append((clk.ticks, s, out[0][0] != out[1][0], plain, star, [float(o[1]) for o in out]))


T.Tick.click = click
for _ in range(ticks):
    clock.tick()
e_unit = clock.A * clock.B
print(f"{world}, {ticks} ticks: fittings {len(rows)}")
print(f"  laid across a pawl wall (eps differs at the two ends): {sum(1 for r in rows if r[2])}")
print(f"  plain charge of the pair 0: {sum(1 for r in rows if r[3] == 0)}; Q* share of the pair 0: {sum(1 for r in rows if r[4] == 0)}")
big = sorted(rows, key=lambda r: -abs(r[4]))[:5]
for tk, s, wall, plain, star, lams in big:
    print(f"    tick {tk}, train {s}: wall {wall}, plain {plain}, Q* share {float(star):.1f} ({float(star) / e_unit:.3f} e),"
          f" lam at the ends {lams[0]:.4f}, {lams[1]:.4f}")
first = [t for t, nz in nonzero_sites if any(nz.values())]
print(f"  the coupled hands' first tick with a nonzero notch now (before the click): {first[0] if first else None}")
