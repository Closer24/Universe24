"""Verifier's engine check of the springs' weight 2d in the derived push (integers from the engine; ratios as floats):
a pure A1 course of one massive hand at rest at every Node-clock (the fourth form, `sea`, its sense 1), no light and
no other train; the push X ((d + 1) G + vw V) with vw = 2d = 6 (the draft), and vw = 3, 4, 9; the first integral of
(V) + continuity, E = X'^2 / 16 - (kappa / 6) X^2 F, read along the course as E / ((kappa / 6) X0^2 F0) at windows.
The verifier's lattice analysis: a mass mode at the lattice frequency w0 dilutes so that E is kept only with the
weight (2/3)(2 + cos w0) per V, about 1.44 (vw about 4.3) at the heavy row (cos w0 = pinion / rim = 0.162), and 2
(vw = 6) only in the continuum (w0 -> 0).
Usage: python -I e_mass.py ENGINE_ROOT ROW_PINION QUANTA TICKS [noclick]"""
import sys, json
from fractions import Fraction
root, pinion, quanta, ticks = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
sys.path[:0] = [root + "/src", root]
from tests.laws import world_of  # noqa: E402
from event_universe import tick as T, click  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
calibre, piece = world_of("world_bang.json")
calibre, piece = json.loads(json.dumps(calibre)), json.loads(json.dumps(piece))
rim = calibre["integers"]["den"]
calibre["rows"] = [{"shape": 2, "pair": [pinion, rim]}]
piece["seed"] = [{"lay": "sea", "row": 1, "quanta": quanta, "sense": 1}]
GAMMA, KEY = 1000, 36000
if len(sys.argv) > 5 and sys.argv[5] == 'noclick':
    click.click = lambda *a, **k: None   # the clicks struck: the A1 course of GR's two halves alone
    print('the clicks struck (no chime moves wind out of the hand)')
print(f"row cos w0 = pinion / rim = {pinion / rim:.6f}; (2/3)(2 + cos w0) = {(2 / 3) * (2 + pinion / rim):.4f} per V (the draft: 2)")
for vw in (6, 4, 3, 9):
    T.VERIFY.update(mode="derived", sign=1, gw=4, vw=vw, spring=False, restore=True, log=[])
    c = Clock(calibre, piece)
    xs = [int(c.train(REGULATOR).gears[0].now.min())]
    alike = True
    for _ in range(ticks):
        c.tick()
        x = c.train(REGULATOR).gears[0].now
        alike &= int(x.min()) == int(x.max())
        xs.append(int(x.min()))
    forms = [row["forms"] for row in T.VERIFY["log"]]
    norm = Fraction(xs[0] ** 2 * forms[0], 2 * GAMMA * KEY)
    out = []
    for t in range(1, len(xs) - 1):
        xd = Fraction(xs[t + 1] - xs[t - 1], 2)
        e = xd * xd / 16 - Fraction(xs[t] ** 2 * forms[t], 2 * GAMMA * KEY)
        out.append((t, float(e / norm)))
    wins = []
    for lo, hi in ((5, 50), (50, 100), (100, 150), (150, 200), (200, 300), (300, 400)):
        win = [r for t, r in out if lo <= t < hi]
        if win:
            wins.append(f"[{lo},{hi}) {sum(win) / len(win):+.3f}")
    print(f"vw {vw}: board alike {alike}; X {xs[0]} -> {xs[-1]}; births {c.counts['births']}, chimes {c.counts['body_clicks']};"
          f" E ratio by window: " + "  ".join(wins))
