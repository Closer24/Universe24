"""Verifier's probe (integers only) against C2 / section 4's 'never below 0 on the A1 course (PROVED)': random and
adversarial board states, one tick forward of the verifier's engine copy (eng/, the derived push, the regulator's
spring 0, written independently of the draft), the first difference X+ - X against X - X- at every Node-clock not
turned over, and the push's numerator N with its parts G = (SUM -a pull - D a a) div T and V = (SUM D a a) div T.
Part A, A1 boards (every Node-clock alike): every train's gears the same at every Node-clock, or the light laid as an
exact quarter-turn plane wave (multiplication by i per Mesh, its wind alike everywhere), the matter hands turned by a
uniform offset (odd gears) and flow (skew) so their Meshes' turn is rounded, the springs as the calibre's, the fine
teeth and drive fine teeth at random or at their extremes (0 and teeth - 1).
Part B, boards not alike (every gear drawn per Node-clock): C2's premise broken.
Usage: python -I a1_adversarial.py ENGINE_ROOT TRIALS_A TRIALS_B SEED"""
import sys, json, random
root, ta, tb, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
sys.path[:0] = [root + "/src", root]
import numpy as np  # noqa: E402
from tests.laws import world_of  # noqa: E402
from event_universe import tick as T, readings  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR, OFFSET, HAND  # noqa: E402
from event_universe.core.acts import mid  # noqa: E402

rng = random.Random(seed)
calibre, piece = world_of("world_bang.json")
piece = json.loads(json.dumps(piece)); piece["seed"][0]["quanta"] = 500
base = Clock(calibre, piece)
SHAPE = base.size
reg = base.train(REGULATOR)
TD = reg.gears[0].dteeth
W = base.teeth

def fine_pick(teeth):
    u = rng.random()
    return 0 if u < 0.25 else (teeth - 1 if u < 0.5 else rng.randrange(teeth))

def quarter_wave(amp3, amp12, k):
    """an exact plane wave on the side-4 torus: z(x) = z0 i^(k . x)"""
    three, twelve = np.zeros(SHAPE, dtype=object), np.zeros(SHAPE, dtype=object)
    for idx in np.ndindex(SHAPE):
        m = (k[0] * idx[0] + k[1] * idx[1] + k[2] * idx[2]) % 4
        a, b = amp3, amp12
        for _ in range(m):
            a, b = -b, a
        three[idx], twelve[idx] = a, b
    return three, twelve

def set_state(clock, alike):
    def val(lo, hi):
        if alike:
            return np.full(SHAPE, rng.randint(lo, hi), dtype=object)
        return np.array([rng.randint(lo, hi) for _ in range(64)], dtype=object).reshape(SHAPE)
    g = clock.train(REGULATOR).gears
    x = rng.choice([1000, 1000, rng.randint(1000, 10**6), rng.randint(10**6, 4 * 10**9)])
    xb = x - rng.randint(-x // 3, x // 3)
    if alike:
        g[0].now[:], g[0].before[:] = x, xb
    else:
        g[0].now[:] = val(max(20, x - x // 4), x + x // 4)
        g[0].before[:] = val(max(20, xb - xb // 4), xb + xb // 4)
    g[0].fine[:] = fine_pick(g[0].teeth) if alike else val(0, g[0].teeth - 1)
    g[0].dfine[:] = fine_pick(TD) if alike else val(0, TD - 1)
    for gear in g[1:4]:   # tensions
        gear.now[:] = gear.before[:] = val(0, rng.choice([0, 0, 50, 400]))
    for gear in g[4:7]:   # flows
        gear.now[:] = gear.before[:] = val(-rng.choice([0, 2, 30]), rng.choice([0, 2, 30]))
    off = clock.train(OFFSET).gears
    off[0].now[:] = off[0].before[:] = 0
    for gear in off[1:]:
        gear.now[:] = gear.before[:] = val(-rng.choice([0, 1, 3, 300]), rng.choice([0, 1, 3, 300]))
    wb = (W // 2) * (np.asarray(g[0].before) + np.asarray(g[0].now))
    for r in clock.trains_:
        if r is clock.train(REGULATOR) or r is clock.train(OFFSET) or r.teeth is not None:
            continue
        amp = rng.choice([1, 30, 3000, 10**5, 10**7])
        if r.size == HAND and alike and rng.random() < 0.5:
            k = [rng.randrange(4) for _ in range(3)]
            n3, n12 = quarter_wave(rng.randint(-amp, amp), rng.randint(-amp, amp), k)
            turn = rng.choice([0, 1, 2, 3])          # the before a turn of quarters back (any of the four)
            b3, b12 = n3, n12
            for _ in range(turn):
                b3, b12 = b12, -b3
            r.gears[0].now[:], r.gears[1].now[:] = n3, n12
            r.gears[0].before[:], r.gears[1].before[:] = b3, b12
        else:
            for gear in r.gears:
                gear.now[:] = val(-amp, amp)
                gear.before[:] = gear.now + val(-amp // 10 - 1, amp // 10 + 1)
        for gear in r.gears:
            gear.teeth = wb
            gear.fine = np.array([fine_pick(int(t)) for t in np.asarray(wb).reshape(-1)], dtype=object).reshape(SHAPE)

BASE = None

def trial(alike):
    global BASE
    if BASE is None:
        BASE = Clock(calibre, piece)
        BASE.saved = [[gear.copy() for gear in train] for train in BASE.trains()]
    clock = BASE
    clock.set_trains([[gear.copy() for gear in train] for train in clock.saved])
    set_state(clock, alike)
    g = clock.train(REGULATOR).gears[0]
    x1, x0 = g.now.copy(), g.before.copy()
    T.VERIFY.update(mode="derived", sign=1, gw=4, vw=6, spring=False, restore=True, log=[])
    try:   # the tick's acts up to the time gear's carry: the readings, the impulse, the carry (no turnover, no click)
        t = T.Tick(clock, 1)
        t.readings(); t.impulse()
        pot, spr = t.v_pot.copy(), t.v_spr.copy()
        t.carry()
    except Exception as e:  # a state the engine refuses
        return None, repr(e)[:80]
    x2 = clock.train(REGULATOR).gears[0].now
    w = clock.teeth
    G = np.array([int(a) // w for a in np.asarray(pot - spr).reshape(-1)], dtype=object)
    Vv = np.array([int(a) // w for a in np.asarray(spr).reshape(-1)], dtype=object)
    N = 4 * G + 6 * Vv
    falls = int((x2 - x1 < x1 - x0).sum())
    return (falls, 64, {"G": G, "V": Vv, "N": N, "X": np.asarray(x1).reshape(-1)}), None

for name, alike, trials in (("A: A1 boards", True, ta), ("B: boards not alike", False, tb)):
    n_falls = n_sites = n_trials_fall = refused = 0
    neg_G = neg_N = 0
    worst = None
    errs = {}
    for _ in range(trials):
        out, err = trial(alike)
        if out is None:
            refused += 1
            errs[err] = errs.get(err, 0) + 1
            continue
        falls, sites, row = out
        n_sites += sites; n_falls += falls; n_trials_fall += falls > 0
        neg_G += int(sum(1 for gg in row["G"] if gg < 0)); neg_N += int(sum(1 for nn in row["N"] if nn < 0))
        for gg, vv, nn, xx in zip(row["G"], row["V"], row["N"], row["X"]):
            if nn < 0 and (worst is None or nn < worst[2]):
                worst = (int(gg), int(vv), int(nn), int(xx))
    print(f"{name}: {trials} trials ({refused} refused by the engine {errs}); Node-clock ticks {n_sites}; the first"
          f" difference fell at {n_falls} ({n_trials_fall} trials); G < 0 at {neg_G}, 4 G + 6 V < 0 at {neg_N} Node-clock"
          f" ticks; the most negative (G, V, 4 G + 6 V, X): {worst}")
