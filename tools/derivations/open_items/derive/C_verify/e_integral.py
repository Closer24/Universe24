"""Verifier's engine check of claim 1 (integers read from the engine; the ratio printed as a float): on the pure A1
course (the bang world with the light alone, so no fitting breaks the sameness), the first integral of GR's volume
equation (V) with continuity, E = X'^2 / 16 - (kappa / 6) X^2 F (kappa = 3 / (Gamma key), X' the centred difference),
read along the engine's own course; GR's (V) + continuity hold iff E stays constant. E / ((kappa / 6) X0^2 F0) is
printed: the seed at rest gives -1 in the continuum. Run for the derived push, its mutations (G weight 3 or 5, the
V weight irrelevant here: the light has no spring), and the head's typed form.
Usage: python -I e_integral.py ENGINE_ROOT QUANTA TICKS"""
import sys, json
from fractions import Fraction
root, quanta, ticks = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.path[:0] = [root + "/src", root]
from tests.laws import world_of  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
calibre, piece = world_of("world_bang.json")
calibre, piece = json.loads(json.dumps(calibre)), json.loads(json.dumps(piece))
calibre["rows"] = []
piece["seed"][0]["quanta"] = quanta
GAMMA, KEY = 1000, 36000

def course(**v):
    T.VERIFY.update(dict(mode="derived", sign=1, gw=4, vw=6, spring=False, restore=True), **v, log=[])
    c = Clock(calibre, piece)
    xs = [int(c.train(REGULATOR).gears[0].now.min())]
    for _ in range(ticks):
        c.tick()
        x = c.train(REGULATOR).gears[0].now
        assert int(x.min()) == int(x.max()), "the board lost its sameness"
        xs.append(int(x.min()))
    forms = [row["forms"] for row in T.VERIFY["log"]]   # forms at each tick's start, tick 1..ticks
    return xs, forms

for label, v in (("derived push (4 G + 6 V)", {}), ("mutation: 3 G", {"gw": 3}), ("mutation: 5 G", {"gw": 5}),
                 ("head's typed form (E10, F1) with its spring", {"mode": "head", "spring": True})):
    xs, forms = course(**v)
    norm = Fraction(xs[0] ** 2 * forms[0], 2 * GAMMA * KEY)     # (kappa / 6) X0^2 F0
    out = []
    for t in range(1, len(xs) - 1):
        xd = Fraction(xs[t + 1] - xs[t - 1], 2)
        e = xd * xd / 16 - Fraction(xs[t] ** 2 * forms[t], 2 * GAMMA * KEY)
        out.append((t, xs[t], float(e / norm)))
    picks = [o for o in out if o[0] in (1, 2, 3, 5, 10, 20, 40, 80, 120, 160, 200, 300, 400, 600, 800) or o is out[-1]]
    print(label + ":  " + "  ".join(f"t{t} X{x}: {r:+.3f}" for t, x, r in picks))
    for lo, hi in ((5, 30), (30, 60), (60, 90), (90, 120), (120, 200), (200, 400)):
        win = [r for t, x, r in out if lo <= t < hi]
        if win:
            print(f"    t in [{lo}, {hi}): E ratio mean {sum(win) / len(win):+.3f}, least {min(win):+.3f}, largest {max(win):+.3f}")
