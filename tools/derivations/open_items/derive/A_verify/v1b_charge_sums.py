"""V1 (verifier A, independent of the draft's p1): where the coupled hands' charge moves in a tick.

Read-only harness on the head's engine. Per tick and coupled hand T it reads the plain charge
Q = SUM_x W(x), W = n3 b12 - n12 b3, at five moments:
  start, after the driven carry (before the stopped clocks' restore), after the restore,
  after the turnover, after the click.
So the step proper, the restore (BH-S1), the turnover and the click are each measured alone.

It also tests the exact per-site identity of the step (integers, no rounding hidden):
  D(x) = Im(conj(a) P) with P = w (a - a_before) + fine - mid(w)   (the step's exact momentum)
  D_after - D_start = X Im(conj(a) pull) + Im(conj(v) rho_after)     (v = a_after - a, rho = fine' - mid(w'))
and the charges a conserved current would need:
  Q_frame = SUM eps W              (eps = 1 - 2 * pawl bit: the neighbour is read conjugated across a pawl wall)
  Q_star  = -SUM eps D / (X mr^2)  (the step's grips carry mr(x)^2 at x, so only S_j = grip_j / mr^2 is symmetric)
with the step's own residual split into the turn's part (pull) and the carry's part (rho), exactly.
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

world, ticks = sys.argv[1], int(sys.argv[2])
calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + world))
clock = Clock(calibre, piece)
G = clock.full_rate
coupled = [k for k, h in enumerate(clock.hands()) if coupling_of(h) == 1]
row_of = {id(h): k for k, h in enumerate(clock.hands())}


def W(gears):
    n3, n12, b3, b12 = gears[0].now, gears[1].now, gears[0].before, gears[1].before
    return n3 * b12 - n12 * b3


def total(arr, weight=None):
    if weight is None:
        return sum(int(v) for v in np.asarray(arr).flat)
    return sum((Fraction(int(v)) * weight[i] for i, v in np.ndenumerate(arr)), Fraction(0))


def plain(clk):
    return {k: total(W(clk.hands()[k].gears)) for k in coupled}


def frame(clk, eps):
    return {k: total(eps * W(clk.hands()[k].gears)) for k in coupled}


stage = {}
rows = []
orig_carry, orig_turnover, orig_click, orig_run = T.Tick.carry, T.Tick.turnover, T.Tick.click, T.run


def carry(self):
    clk = self.clock
    eps = 1 - 2 * np.asarray(self.ratchet.gears[0].fine, dtype=object)
    stage['eps'] = eps
    X = np.asarray(self.stretch_now, dtype=object)
    mr = np.asarray(self.mesh_rate, dtype=object) * np.ones(clk.size, dtype=object)
    w_side = readings.mean_teeth(clk, self.regulator.gears[0])
    lam = {i: (Fraction(1, int(X[i]) * int(mr[i]) ** 2) if int(mr[i]) else Fraction(0))
           for i in np.ndindex(clk.size)}
    stage['lam'] = lam
    pre = {}
    for k in coupled:
        t = self.where[id(clk.hands()[k])]
        gears = self.trains[t]
        a = self.starts[t]
        P0 = [w_side * (g.now - g.before) + g.fine - mid(w_side) for g in gears]
        pre[k] = (a, P0, list(self.impelled[t]), list(self.pull[t]), t)
    stage['frame_start'] = frame(clk, eps)
    orig_set = clk.set_trains
    caught = {}

    def set_trains(out):
        orig_set(out)
        caught['plain'] = plain(clk)
        caught['frame'] = frame(clk, eps)
        caught['gears'] = {k: [(g.now.copy(), g.fine.copy(), g.teeth) for g in clk.hands()[k].gears] for k in coupled}

    clk.set_trains = set_trains
    orig_carry(self)
    del clk.set_trains
    stage['mid_plain'], stage['mid_frame'] = caught['plain'], caught['frame']
    stage['restored_plain'], stage['restored_frame'] = plain(clk), frame(clk, eps)
    stopped = np.asarray(self.stopped, dtype=bool)
    stage['stopped'] = int(stopped.sum())
    ident = {}
    for k in coupled:
        a, P0, P1, pull, t = pre[k]
        (n3, f3, w3), (n12, f12, w12) = caught['gears'][k]
        v = [n3 - a[0], n12 - a[1]]
        rho = [f3 - mid(w3), f12 - mid(w12)]
        ok_p = all(bool(np.all(P1[g] == [w3, w12][g] * v[g] + rho[g])) for g in range(2))
        D0 = a[0] * P0[1] - a[1] * P0[0]
        D1 = n3 * P1[1] - n12 * P1[0]
        Rpull = X * (a[0] * pull[1] - a[1] * pull[0])
        Rcarry = v[0] * rho[1] - v[1] * rho[0]
        live = ~stopped
        ok_id = bool(np.all((D1 - D0 - Rpull - Rcarry)[live] == 0))
        w_ref = int(clk.teeth) * G
        scale = Fraction(G ** 3, w_ref)   # 1 at the vacuum: X = mr = G, w = teeth G
        lam_l = {i: (lam[i] if live[i] else Fraction(0)) for i in lam}
        e_lam = {i: eps[i] * lam_l[i] * scale for i in lam}
        d_star = -(total(D1, e_lam) - total(D0, e_lam))
        r_pull = -total(Rpull, e_lam)
        r_carry = -total(Rcarry, e_lam)
        r_pull_plain = -total(Rpull * live, {i: Fraction(1, int(w_side[i]) if np.ndim(w_side) else int(w_side)) for i in lam})
        ident[k] = dict(ok_p=ok_p, ok_id=ok_id, d_star=d_star, r_pull=r_pull, r_carry=r_carry,
                        r_pull_plain=r_pull_plain,
                        abs_carry=sum(abs(int(x)) for x in np.asarray(Rcarry[live]).flat) / w_ref)
    stage['ident'] = ident


def turnover(self):
    orig_turnover(self)
    stage['turned'] = int(np.asarray(self.top).sum())
    stage['turn_plain'], stage['turn_frame'] = plain(self.clock), frame(self.clock, stage['eps'])


def click(self):
    orig_click(self)
    stage['click_plain'] = plain(self.clock)


def run(clk, going):
    start = plain(clk)
    orig_run(clk, going)
    if going != 1:
        return
    rows.append((clk.ticks, start, dict(stage)))


T.Tick.carry, T.Tick.turnover, T.Tick.click, T.run = carry, turnover, click, run
for _ in range(ticks):
    clock.tick()

e = clock.A * clock.B
print(f"{world}, {ticks} ticks, e = A B = {e}; coupled hands {coupled}")
agg = {k: dict(nz_step=0, nz_restore=0, nz_turn=0, nz_click=0, nz_total=0, max_step=0, max_restore=0,
               max_turn=0, max_click=0, max_total=0, nz_frame_step=0, max_frame_step=0,
               max_star=0, max_star_carry=0, max_star_pull=0, max_pull_plain=0, ok_p=0, ok_id=0,
               nz_step_quiet=0, max_step_quiet=0, quiet=0) for k in coupled}
for tk, start, st in rows:
    for k in coupled:
        A_ = agg[k]
        d_step = st['mid_plain'][k] - start[k]
        d_res = st['restored_plain'][k] - st['mid_plain'][k]
        d_turn = st['turn_plain'][k] - st['restored_plain'][k]
        d_click = st['click_plain'][k] - st['turn_plain'][k]
        d_tot = st['click_plain'][k] - start[k]
        d_fs = st['mid_frame'][k] - st['frame_start'][k]
        idn = st['ident'][k]
        A_['ok_p'] += idn['ok_p']
        A_['ok_id'] += idn['ok_id']
        for name, d in (('step', d_step), ('restore', d_res), ('turn', d_turn), ('click', d_click), ('total', d_tot),
                        ('frame_step', d_fs)):
            A_['nz_' + name] += int(d != 0)
            A_['max_' + name] = max(A_['max_' + name], abs(d))
        A_['max_star'] = max(A_['max_star'], abs(float(idn['d_star'])))
        A_['max_star_carry'] = max(A_['max_star_carry'], abs(float(idn['r_carry'])))
        A_['max_star_pull'] = max(A_['max_star_pull'], abs(float(idn['r_pull'])))
        A_['max_pull_plain'] = max(A_['max_pull_plain'], abs(float(idn['r_pull_plain'])))
        if st['stopped'] == 0 and st['turned'] == 0:
            A_['quiet'] += 1
            A_['nz_step_quiet'] += int(d_step != 0)
            A_['max_step_quiet'] = max(A_['max_step_quiet'], abs(d_step))
print("per tick: turned clocks, stopped clocks:", [(tk, st['turned'], st['stopped']) for tk, _s, st in rows][:12], '...')
print("ticks with turned clocks:", sum(1 for _t, _s, st in rows if st['turned']),
      " with stopped clocks:", sum(1 for _t, _s, st in rows if st['stopped']))
for k in coupled:
    A_ = agg[k]
    print(f"hand {k}:")
    print(f"  plain charge, ticks changed / largest |change| (sweep units):")
    for name in ('step', 'restore', 'turn', 'click', 'total'):
        print(f"    {name:8s}: {A_['nz_' + name]:3d} / {A_['max_' + name]}")
    print(f"    the step on ticks with no turned and no stopped clock: {A_['nz_step_quiet']} of {A_['quiet']}, largest {A_['max_step_quiet']}")
    print(f"  frame charge SUM eps W, the step alone: {A_['nz_frame_step']} ticks changed, largest {A_['max_frame_step']}")
    print(f"  the step's exact identities: P' = w' v + rho' at {A_['ok_p']} of {len(rows)} ticks;"
          f" D' - D = X Im(conj a pull) + Im(conj v rho') at every live clock: {A_['ok_id']} of {len(rows)}")
    print(f"  Q_star (eps, 1/(X mr^2), vacuum units), the step's own change: largest {A_['max_star']:.1f};"
          f" its turn part {A_['max_star_pull']:.1f}, its carry part {A_['max_star_carry']:.1f}")
    print(f"  the turn's part with no weights (plain, over w): largest {A_['max_pull_plain']:.1f}")
for k in coupled:
    ss = sum(st['mid_plain'][k] - start[k] for _t, start, st in rows)
    tt = sum(st['turn_plain'][k] - st['restored_plain'][k] for _t, start, st in rows)
    cc = sum(st['click_plain'][k] - st['turn_plain'][k] for _t, start, st in rows)
    print(f"hand {k}: over the run the step's plain changes sum to {ss}, the turnover's to {tt}, the click's to {cc}; net {ss + tt + cc}")
print("first ticks, hand by hand (tick: step, restore, turn, click | star step = pull + carry):")
for tk, start, st in rows[:8]:
    parts = []
    for k in coupled:
        idn = st['ident'][k]
        parts.append(f"h{k}: {st['mid_plain'][k] - start[k]}, {st['restored_plain'][k] - st['mid_plain'][k]},"
                     f" {st['turn_plain'][k] - st['restored_plain'][k]}, {st['click_plain'][k] - st['turn_plain'][k]}"
                     f" | {float(idn['d_star']):.1f} = {float(idn['r_pull']):.1f} + {float(idn['r_carry']):.1f}")
    print(f"  {tk}: " + "; ".join(parts))
