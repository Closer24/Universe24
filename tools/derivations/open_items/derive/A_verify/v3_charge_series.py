"""V3 (verifier A): the step's conserved charge Q* through the tick's acts, against the plain sweep.

Q*(state; eps, lam) = -SUM_x eps(x) G^3 / (w_ref X(x) mr(x)^2) Im(conj(a) P),  P = w (a - a_before) + fine - mid(w)
(vacuum sweep units: at X = mr = G, w = w_ref, Q* = SUM eps W less the fine tooth's term).
Per tick and coupled hand: Q* at the start; after the step proper (same eps, lam); after the turnover with the
turned pawls (eps after) and the old lam; after the click; and the next start (the background's lam moved).
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
from event_universe.core.acts import mid  # noqa: E402
from event_universe.meshes import coupling_of  # noqa: E402
from event_universe.trains import REGULATOR, ratchet_of  # noqa: E402

world, ticks = sys.argv[1], int(sys.argv[2])
calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + world))
clock = Clock(calibre, piece)
G = clock.full_rate
w_ref = int(clock.teeth) * G
coupled = [k for k, h in enumerate(clock.hands()) if coupling_of(h) == 1]


def eps_of(clk):
    return 1 - 2 * np.asarray(ratchet_of(clk.trains_).gears[0].fine, dtype=object)


def weights(clk):
    load = readings.load(clk)
    mr = np.asarray(readings.rates_of(clk, load)[1], dtype=object) * np.ones(clk.size, dtype=object)
    X = np.asarray(clk.train(REGULATOR).gears[0].now, dtype=object)
    return {i: (Fraction(G ** 3, w_ref * int(X[i]) * int(mr[i]) ** 2) if int(mr[i]) else Fraction(0))
            for i in np.ndindex(clk.size)}


def qstar(clk, k, eps, lam):
    w = readings.mean_teeth(clk, clk.train(REGULATOR).gears[0])
    g3, g12 = clk.hands()[k].gears
    P3 = w * (g3.now - g3.before) + g3.fine - mid(w)
    P12 = w * (g12.now - g12.before) + g12.fine - mid(w)
    D = g3.now * P12 - g12.now * P3
    return -sum((Fraction(int(eps[i] * D[i])) * lam[i] for i in lam), Fraction(0))


def plainq(clk, k):
    g3, g12 = clk.hands()[k].gears
    return int(sum(int(v) for v in (g3.now * g12.before - g12.now * g3.before).flat))


series = []
cur = {}
orig_carry, orig_turnover, orig_click, orig_run = T.Tick.carry, T.Tick.turnover, T.Tick.click, T.run


def carry(self):
    clk = self.clock
    cur['eps'], cur['lam'] = eps_of(clk), weights(clk)
    cur['start'] = {k: qstar(clk, k, cur['eps'], cur['lam']) for k in coupled}
    orig_set = clk.set_trains

    def set_trains(out):
        orig_set(out)
        cur['step'] = {k: qstar(clk, k, cur['eps'], cur['lam']) for k in coupled}

    clk.set_trains = set_trains
    orig_carry(self)
    del clk.set_trains


def turnover(self):
    orig_turnover(self)
    cur['turned'] = int(np.asarray(self.top).sum())
    cur['eps_after'] = eps_of(self.clock)
    cur['turn'] = {k: qstar(self.clock, k, cur['eps_after'], cur['lam']) for k in coupled}
    cur['turn_noflip'] = {k: qstar(self.clock, k, cur['eps'], cur['lam']) for k in coupled}


def click(self):
    orig_click(self)
    cur['click'] = {k: qstar(self.clock, k, cur['eps_after'], cur['lam']) for k in coupled}


def run(clk, going):
    p0 = {k: plainq(clk, k) for k in coupled}
    orig_run(clk, going)
    cur['plain'] = {k: plainq(clk, k) - p0[k] for k in coupled}
    series.append(dict(cur))


T.Tick.carry, T.Tick.turnover, T.Tick.click, T.run = carry, turnover, click, run
for _ in range(ticks):
    clock.tick()

print(f"{world}, {ticks} ticks, e = {clock.A * clock.B}: Q* (vacuum sweep units) per act, largest |change| and ticks changed")
for k in coupled:
    d = {n: [] for n in ('step', 'turn (pawls flipped)', 'turn (pawls not flipped)', 'click', 'background', 'tick', 'plain tick')}
    for t, row in enumerate(series):
        d['step'].append(row['step'][k] - row['start'][k])
        d['turn (pawls flipped)'].append(row['turn'][k] - row['step'][k])
        d['turn (pawls not flipped)'].append(row['turn_noflip'][k] - row['step'][k])
        d['click'].append(row['click'][k] - row['turn'][k])
        if t + 1 < len(series):
            d['background'].append(series[t + 1]['start'][k] - row['click'][k])
            d['tick'].append(series[t + 1]['start'][k] - row['start'][k])
        d['plain tick'].append(Fraction(row['plain'][k]))
    print(f"hand {k}: Q* at the first start {float(series[0]['start'][k]):.1f}, at the last start {float(series[-1]['start'][k]):.1f}")
    for n, vals in d.items():
        big = max((abs(v) for v in vals), default=0)
        print(f"  {n:26s}: largest {float(big):12.1f}, ticks changed {sum(1 for v in vals if v != 0):3d} of {len(vals)},"
              f" summed {float(sum(vals, Fraction(0))):12.1f}")
