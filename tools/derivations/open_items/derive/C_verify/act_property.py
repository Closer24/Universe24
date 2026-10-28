"""Verifier's property test of C2's lemma on the engine's own act (clock.act: Rule3's turn with the regulator's real
gearing at its load, then the drive's carry), integers only, on uniform boards (every Node-clock alike, so the grips'
sum cancels), with the fine tooth r and the drive fine tooth r_d drawn at random or at their extremes (0, teeth - 1),
X- above or below X, and the numerator N >= 0 (0, 1, teeth - 1, random up to 10^6 teeth) or N < 0 (-1, random).
Claim: with the spring D_R = 0 and N >= 0, X+ - X >= X - X-. Mutations: N negated; the head's spring D_R kept.
Usage: python -I act_property.py ENGINE_ROOT DRAWS SEED"""
import sys, json, random
root, draws, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.path[:0] = [root + "/src", root]
import numpy as np  # noqa: E402
from tests.laws import world_of  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe import readings  # noqa: E402
from event_universe.core.rule3 import Gearing  # noqa: E402
from event_universe.features import stretch  # noqa: E402
from event_universe.trains import REGULATOR, Gear  # noqa: E402
calibre, piece = world_of("world_bang.json")
piece = json.loads(json.dumps(piece)); piece["seed"][0]["quanta"] = 1
clock = Clock(calibre, piece)
reg = clock.train(REGULATOR)
TD, W = reg.gears[0].dteeth, reg.gears[0].teeth
SH = clock.size
rng = random.Random(seed)
def pick(teeth):
    u = rng.random()
    return 0 if u < 0.3 else (teeth - 1 if u < 0.6 else rng.randrange(teeth))
counts = {}
def tally(name, ok):
    a = counts.setdefault(name, [0, 0]); a[0] += ok; a[1] += 1
for _ in range(draws):
    x = rng.choice([19, 1000, rng.randrange(20, 10**6), rng.randrange(10**6, 5 * 10**9)])
    xb = max(1, x + rng.choice([0, 1, -1, rng.randrange(-x, x + 1)]))
    r, rd = pick(W), pick(TD)
    n_pos = rng.choice([0, 1, TD - 1, TD, rng.randrange(0, 10**6) * TD + rng.randrange(TD)])
    n_neg = rng.choice([-1, -TD, -rng.randrange(1, 10**3) * TD - rng.randrange(TD)])
    load = stretch.load_of(clock.full_rate, np.array([x], dtype=object))
    g = readings.gearing_of(clock, reg, np.full(SH, int(load[0]), dtype=object), clock.start_factors or None)
    g0 = Gearing(g.grips, g.teeth + g.teeth - sum(g.grips), g.teeth, 0)
    for name, gearing, n in (("D_R = 0, N >= 0 (the lemma)", g0, n_pos), ("mutation: N negated", g0, -n_pos if n_pos else n_neg),
                             ("D_R = 0, N < 0", g0, n_neg), ("mutation: the head's spring D_R, N = 0", g, 0)):
        gear = Gear(np.full(SH, x, dtype=object), np.full(SH, xb, dtype=object), np.full(SH, r, dtype=object), W,
                    np.full(SH, rd, dtype=object), TD)
        _, out = clock.act([gear], gearing, None, [np.full(SH, n, dtype=object)], 1)
        xn = out[0].now
        tally(name, bool(((xn - x) >= (x - xb)).all()))
for name, (ok, tot) in counts.items():
    print(f"{name}: the first difference held in {ok} of {tot} draws")
