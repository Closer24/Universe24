"""Verifier's detail of e_mass.py's vw = 6 course: X_t, the forms F_t, K, G, V at (0,0,0), the sweep-like invariant
J = W+ Im(conj(a) a+) of the massive hand, and E ratio, ticks 0..T. Usage: python -I e_mass_detail.py <root> <pinion> <quanta> <t> <vw>"""
import sys, json
from fractions import Fraction
root, pinion, quanta, ticks, vw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
sys.path[:0] = [root + "/src", root]
from tests.laws import world_of  # noqa: E402
from event_universe import tick as T, click  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
click.click = lambda *a, **k: None
calibre, piece = world_of("world_bang.json")
calibre, piece = json.loads(json.dumps(calibre)), json.loads(json.dumps(piece))
rim = calibre["integers"]["den"]
calibre["rows"] = [{"shape": 2, "pair": [pinion, rim]}]
piece["seed"] = [{"lay": "sea", "row": 1, "quanta": quanta, "sense": 1}]
T.VERIFY.update(mode="derived", sign=1, gw=4, vw=vw, spring=False, restore=True, log=[])
c = Clock(calibre, piece)
hand = [r for r in c.hands() if r.ratio[0] == pinion][0]
w = c.teeth
xs, J = [int(c.train(REGULATOR).gears[0].now.min())], []
for t in range(ticks):
    g = hand.gears
    a3, a12 = int(g[0].now.flat[0]), int(g[1].now.flat[0])
    c.tick()
    b3, b12 = int(g[0].now.flat[0]) if False else int(hand.gears[0].now.flat[0]), int(hand.gears[1].now.flat[0])
    x0, x1 = xs[-1], int(c.train(REGULATOR).gears[0].now.min())
    J.append((x0 + x1) * (a3 * b12 - a12 * b3))     # W+ Im(conj(a) a+) up to w/2
    xs.append(x1)
log = T.VERIFY["log"]
norm = Fraction(xs[0] ** 2 * log[0]["forms"], 2 * 1000 * 36000)
for t in range(0, ticks - 1):
    r = log[t]
    e = (Fraction(xs[t + 1] - (xs[t - 1] if t else xs[0]), 2) ** 2 / 16 - Fraction(xs[t] ** 2 * r["forms"], 2 * 1000 * 36000)) / norm
    if t < 12 or t % 25 == 0:
        print(f"t {t}: X {xs[t]} F {r['forms']} K {r['kin']} G {(r['pot'] - r['spr']) // w} V {r['spr'] // w} rate {r['rate']} J {J[t]} E/norm {float(e):+.3f}")
