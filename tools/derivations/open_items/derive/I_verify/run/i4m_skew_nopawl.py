"""I4 (drafter I): the charge Q* on the head's engine (t24 worktree), with runtime monkeypatches only.

Run: python -I i4_head.py <world file> <ticks> <variant> [rewind]
  variant: head  - the engine unpatched
           fix1  - the triple read with the pawl alone (the mutant 'the sweep not turned at the turnover')
           fix2  - the turnover alone (the mutant 'the pawl dropped from the triple')
           fix12 - both: the act this draft derives
  rewind : also run <ticks> forward and <ticks> back on a fresh clock and compare every gear bit for bit

The two patches (no file of the engine is changed):
  fix1: meshes_of reads the odd gear's Mesh sum with the far end's pawl, odd = s (o_x + f o_y), as
        meshes.offsets reads the count, n = K_x - f K_y; skewed reads the flow gears' Mesh sum with the
        near end's pawl sign, m = e_x 3 R s (V_x + V_y)  (e_x = 1 - 2 pawl bit, f = e_x e_y).
  fix2: Clock.reverse writes a hand's two slots exchanged through K^(1 - c), c its coupling (the power the
        Meshes read the pawl at): the coupled hands exchanged with no K, the pawl's flip carrying it;
        the light (c = 0) as on the head.

The budget, per tick and coupled hand, every term computed from its own formula in exact Fractions:
  Q* = -SUM_x e lam Im(conj(a) P),  lam = 1 / (X mr^2),  P = w (now - before) + fine - mid(w)
  the step:     Q*_mid - Q*_start = SUM_x [ I(x) + Rt(x) + Rc(x) ]
                I  = -e lam X SUM_j g_j Im(conj(a) m_j exact)    (the exact Mesh currents into x)
                Rt = -e lam X SUM_j g_j Im(conj(a) (m_j - m_j exact))   (the turns' rounding)
                Rc = -e lam Im(conj(v) rho')                      (the carry's rounding)
                A  = SUM_x I(x): 0 exactly where the current is antisymmetric
  the turnover: at a turned Node-clock the hand ends at its held pre-state mirrored, so
                Q*_turn - Q*_mid = SUM_turned [ proper(x) - (I + Rt + Rc)(x) ],
                proper = e lam E_held                    with the sweep turned with the pawl (fix2),
                proper = -2 q_held - e lam E_held        on the head (the framed charge reversed),
                E_held = Im(conj(now - before) (fine - mid)) of the held hand
  the click:    C = Q*_click - Q*_turn (measured), with the fittings and unspringings counted
  the rates:    B = Q*_next start - Q*_click = -SUM_x e (lam_next - lam) Im(conj(a) P)
"""
import sys
from fractions import Fraction as Fr
from pathlib import Path

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src']
import numpy as np  # noqa: E402
from event_universe import hands, readings  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.core import acts  # noqa: E402
from event_universe.core.acts import mid  # noqa: E402
from event_universe.core.spokes import AXES, SPOKE_SIDES, SPOKES, across  # noqa: E402
from event_universe.meshes import Mesh, coupling_of, mesh_teeth, odd_sum  # noqa: E402
from event_universe.regulation import rest_rate_of  # noqa: E402
from event_universe.trains import HAND, Gear  # noqa: E402

world, ticks, variant = sys.argv[1], int(sys.argv[2]), sys.argv[3]
REWIND = 'rewind' in sys.argv[4:]
FIX1 = variant in ('fix1', 'fix12')
FIX2 = variant in ('fix2', 'fix12')
assert variant in ('head', 'fix1', 'fix2', 'fix12')
EPS = {}


# ---------------------------------------------------------------- the patches
def meshes_of_fix(factors, pawl_signs, offset_pairs, odd):
    """fix1: the odd gear's Mesh sum read with the far end's pawl, s (o_x + f o_y)."""
    return [
        Mesh(factors[spoke], pawl_signs[spoke], *offset_pairs[spoke],
             SPOKE_SIDES[spoke][1] * (odd[axis] + pawl_signs[spoke] * across(odd[axis], spoke)))
        for spoke, (axis, _side) in enumerate(SPOKE_SIDES)
    ]


def skewed_fix(meshes_, rest_rate, flow_gears, full_rate):
    """fix1: the flow gears' Mesh sum read with the near end's pawl sign, e_x 3 R s (V_x + V_y)."""
    w2 = full_rate * full_rate
    found = []
    for spoke, (axis, _side) in enumerate(SPOKE_SIDES):
        skew = (w2, AXES * rest_rate * odd_sum(flow_gears[axis], spoke))
        at = meshes_[spoke]
        found.append(Mesh(at.factor, at.pawl, at.cosine, at.sine, at.odd, skew))
    return found


orig_standard_rate = T.Tick.standard_rate


def standard_rate(self):
    EPS['e'] = 1 - 2 * np.asarray(self.ratchet.gears[0].fine, dtype=object)
    orig_standard_rate(self)


def reverse_fix(self, top, held):
    """fix2: Clock.reverse with a hand's slots exchanged through K^(1 - c)."""
    for r, train, held_train in zip(self.trains_, self.trains(), held, strict=True):
        signs = hands.signs(r.size)
        if r.size == HAND and r.ratio is not None:
            signs = [1, (-1) ** (1 - coupling_of(r))]
        nows, befores, fines = acts.reverse(held_train, signs)
        drives = [None if h.dfine is None else acts.mirror(h.dfine, h.dteeth, 1) for h in held_train]
        fines = fines if r.teeth is None else [acts.flip(h.fine, h.teeth, 1) for h in held_train]
        reversed_gears = [
            Gear(n, b, fine, h.teeth, d, h.dteeth)
            for n, b, fine, h, d in zip(nows, befores, fines, held_train, drives, strict=True)
        ]
        self.restore(train, reversed_gears, top)


T.Tick.standard_rate = standard_rate
if FIX1:
    T.meshes_of = meshes_of_fix
    T.skewed = skewed_fix
if FIX2:
    Clock.reverse = reverse_fix


def new_clock():
    calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + world))
    return Clock(calibre, piece)


# ---------------------------------------------------------------- the rewind
def snapshot(clk):
    gears = [[(g.now.copy(), g.before.copy(), np.asarray(g.fine).copy(), np.asarray(g.teeth).copy(),
               None if g.dfine is None else np.asarray(g.dfine).copy()) for g in r.gears] for r in clk.trains_]
    return gears, clk.slack.copy(), clk.dial.copy(), clk.clicks.copy(), clk.ticks, len(clk.log)


def same(s1, s2):
    g1, *rest1 = s1
    g2, *rest2 = s2
    for t1, t2 in zip(g1, g2, strict=True):
        for a, b in zip(t1, t2, strict=True):
            for x, y in zip(a, b, strict=True):
                if (x is None) != (y is None):
                    return False
                if x is not None and not np.array_equal(np.asarray(x, dtype=object), np.asarray(y, dtype=object)):
                    return False
    for x, y in zip(rest1, rest2, strict=True):
        if not np.array_equal(np.asarray(x, dtype=object), np.asarray(y, dtype=object)):
            return False
    return True


if REWIND:
    clk = new_clock()
    first = snapshot(clk)
    marks = [first]
    for _ in range(ticks):
        clk.tick()
        marks.append(snapshot(clk))
    back_ok = 0
    for k in range(ticks):
        clk.tick(-1)
        back_ok += int(same(snapshot(clk), marks[ticks - 1 - k]))
    turns = clk.counts['turns']
    print(f"REWIND {world} {variant}: {ticks} ticks forward and back, the state equal to the forward run's at "
          f"{back_ok} of {ticks} ticks, the start bit for bit: {same(snapshot(clk), first)}")
    sys.exit(0)


# ---------------------------------------------------------------- the budget
clock = new_clock()
G = clock.full_rate
coupled = [k for k, h in enumerate(clock.hands()) if coupling_of(h) == 1]
SCALE = Fr(clock.standard_length)
rows = []
cur = {}


def im_cb(p, q):
    return p[0] * q[1] - p[1] * q[0]


def gearP(g, w):
    return [w * (g[0].now - g[0].before) + g[0].fine - mid(w), w * (g[1].now - g[1].before) + g[1].fine - mid(w)]


def qdens(e, lam_, a3, a12, P3, P12):
    return -e * lam_ * (a3 * P12 - a12 * P3)


def site_ints(x):
    return x if isinstance(x, (int, np.integer)) else x


orig_carry, orig_turnover, orig_click = T.Tick.carry, T.Tick.turnover, T.Tick.click


def carry(self):
    clk = self.clock
    e = 1 - 2 * np.asarray(self.ratchet.gears[0].fine, dtype=object)
    X = np.asarray(self.stretch_now, dtype=object) * np.ones(clk.size, dtype=object)
    mr = np.asarray(self.mesh_rate, dtype=object) * np.ones(clk.size, dtype=object)
    stopped = np.asarray(self.stopped, dtype=bool)
    assert not stopped.any(), "a stopped Node-clock: the budget reads none"
    lam = {i: Fr(1, int(X[i]) * int(mr[i]) ** 2) for i in np.ndindex(clk.size)}
    w_side = readings.mean_teeth(clk, self.regulator.gears[0])
    if 'click' in cur:                              # the rates' term of the tick before
        prev = dict(cur)
        bnext = Fr(0)
        qnext = Fr(0)
        for k in coupled:
            g = clk.hands()[k].gears
            P = gearP(g, w_side)
            for i in np.ndindex(clk.size):
                d = qdens(int(e[i]), lam[i], int(g[0].now[i]), int(g[1].now[i]), int(P[0][i]), int(P[1][i]))
                qnext += d
                bnext += -int(e[i]) * (lam[i] - prev['lam'][i]) * (int(g[0].now[i]) * int(P[1][i]) - int(g[1].now[i]) * int(P[0][i]))
            same_teeth = bool(np.all(np.asarray(g[0].teeth) == w_side))
            prev['teeth_kept'] = prev.get('teeth_kept', True) and same_teeth
        prev['next'] = qnext
        prev['B_formula'] = bnext
        rows.append(prev)
    cur.clear()
    cur.update(lam=lam, e=e, tick=clk.ticks)
    per = {}
    for k in coupled:
        r = clk.hands()[k]
        t = self.where[id(r)]
        gears = self.trains[t]
        a = self.starts[t]
        P0 = gearP(gears, w_side)
        gearing = readings.gearing_of(clk, r, self.load, self.factors)
        rot = coupling_of(r) * rest_rate_of(clk, r.ratio)
        turn = T.skewed(self.meshes_at[coupling_of(r)], rot, self.flow_gears, G)
        I = {}
        Rt = {}
        total_pull = [0, 0]
        for j in range(SPOKES):
            m = clk.offset_pull([across(x, j) for x in a], j, turn)
            total_pull = [total_pull[0] + gearing.grips[j] * m[0], total_pull[1] + gearing.grips[j] * m[1]]
            at = turn[j]
            y3, y12 = across(a[0], j), across(a[1], j)
            wl, (w2, mm) = mesh_teeth(G), at.skew
            for i in np.ndindex(clk.size):
                odd = int(at.odd[i]) if np.ndim(at.odd) else int(at.odd)
                ms = int(mm[i]) if np.ndim(mm) else int(mm)
                g3, g12 = wl * w2 - odd * ms, wl * ms + odd * w2
                nn = g3 * g3 + g12 * g12
                ut = (Fr(g3 * g3 - g12 * g12, nn), Fr(2 * g3 * g12, nn))
                c = int(at.cosine[i]) if np.ndim(at.cosine) else int(at.cosine)
                s = int(at.sine[i]) if np.ndim(at.sine) else int(at.sine)
                f = int(at.pawl[i]) if np.ndim(at.pawl) else int(at.pawl)
                seen = (Fr(int(y3[i])), Fr(f * int(y12[i])))
                uo = (Fr(c) / SCALE, Fr(s) / SCALE)
                z = (uo[0] * seen[0] - uo[1] * seen[1], uo[0] * seen[1] + uo[1] * seen[0])
                ex = (ut[0] * z[0] - ut[1] * z[1], ut[0] * z[1] + ut[1] * z[0])
                gj = int(gearing.grips[j][i]) if np.ndim(gearing.grips[j]) else int(gearing.grips[j])
                ai = (int(a[0][i]), int(a[1][i]))
                coef = -int(e[i]) * lam[i] * int(X[i]) * gj
                I[i] = I.get(i, Fr(0)) + coef * im_cb(ai, ex)
                Rt[i] = Rt.get(i, Fr(0)) + coef * im_cb(ai, (int(m[0][i]) - ex[0], int(m[1][i]) - ex[1]))
        pull_ok = all(bool(np.all(total_pull[g] - (gearing.teeth + gearing.teeth - gearing.hold) * a[g] == self.pull[t][g]))
                      for g in range(2))
        per[k] = dict(t=t, a=[x.copy() for x in a], b=[g.before.copy() for g in gears],
                      fine=[np.asarray(g.fine).copy() for g in gears], w=w_side, P0=P0,
                      Pimp=[np.asarray(p).copy() for p in self.impelled[t]], I=I, Rt=Rt, pull_ok=pull_ok)
    cur['per'] = per
    orig_set = clk.set_trains

    def set_trains(out):
        orig_set(out)
        for k in coupled:
            g = clk.hands()[k].gears
            per[k]['new'] = [(g[0].now.copy(), np.asarray(g[0].fine).copy(), np.asarray(g[0].teeth).copy()),
                             (g[1].now.copy(), np.asarray(g[1].fine).copy(), np.asarray(g[1].teeth).copy())]

    clk.set_trains = set_trains
    orig_carry(self)
    del clk.set_trains
    qs = qm = Fr(0)
    for k in coupled:
        d = per[k]
        (n3, f3, w3), (n12, f12, w12) = d['new']
        Rc = {}
        carry_ok = True
        for i in np.ndindex(clk.size):
            a3, a12 = int(d['a'][0][i]), int(d['a'][1][i])
            v = (int(n3[i]) - a3, int(n12[i]) - a12)
            ww3, ww12 = (int(w3[i]) if np.ndim(w3) else int(w3)), (int(w12[i]) if np.ndim(w12) else int(w12))
            rho = (int(f3[i]) - mid(ww3), int(f12[i]) - mid(ww12))
            Pimp = (int(d['Pimp'][0][i]), int(d['Pimp'][1][i]))
            carry_ok = carry_ok and Pimp == (ww3 * v[0] + rho[0], ww12 * v[1] + rho[1])
            Rc[i] = -int(e[i]) * lam[i] * im_cb(v, rho)
            P0 = (int(d['P0'][0][i]), int(d['P0'][1][i]))
            qs += qdens(int(e[i]), lam[i], a3, a12, P0[0], P0[1])
            qm += qdens(int(e[i]), lam[i], int(n3[i]), int(n12[i]), Pimp[0], Pimp[1])
            d.setdefault('qheld', {})[i] = qdens(int(e[i]), lam[i], a3, a12, P0[0], P0[1])
            b3, b12 = int(d['b'][0][i]), int(d['b'][1][i])
            wsi = int(d['w'][i]) if np.ndim(d['w']) else int(d['w'])
            rh = (int(d['fine'][0][i]) - mid(wsi), int(d['fine'][1][i]) - mid(wsi))
            d.setdefault('Eheld', {})[i] = im_cb((a3 - b3, a12 - b12), rh)
            d.setdefault('edge', {})[i] = (wsi % 2 == 0) and (int(d['fine'][0][i]) == 0 or int(d['fine'][1][i]) == 0)
        d['Rc'] = Rc
        d['carry_ok'] = carry_ok
    cur['q_start'] = qs
    cur['q_mid'] = qm


def turnover(self):
    orig_turnover(self)
    clk = self.clock
    top = np.asarray(self.top, dtype=bool)
    e1 = 1 - 2 * np.asarray(self.ratchet.gears[0].fine, dtype=object)
    lam, e = cur['lam'], cur['e']
    qt = Fr(0)
    proper_bad = edges = turned = 0
    for k in coupled:
        d = cur['per'][k]
        g = clk.hands()[k].gears
        w = np.asarray(g[0].teeth, dtype=object) * np.ones(clk.size, dtype=object)
        P = gearP(g, w)
        for i in np.ndindex(clk.size):
            q = qdens(int(e1[i]), lam[i], int(g[0].now[i]), int(g[1].now[i]), int(P[0][i]), int(P[1][i]))
            qt += q
            if top[i]:
                turned += 1
                proper = q - d['qheld'][i]
                ee = int(e[i]) * lam[i] * d['Eheld'][i]
                want = ee if FIX2 else -2 * d['qheld'][i] - ee
                if proper != want:
                    if d['edge'][i]:
                        edges += 1
                    else:
                        proper_bad += 1
            elif e1[i] != e[i]:
                proper_bad += 1
    cur['q_turn'] = qt
    cur['turned'] = int(top.sum())
    cur['turn_checks'] = (turned, proper_bad, edges)
    cur['top'] = top.copy()


def click(self):
    clk = self.clock
    log_from = len(clk.log)
    orig_click(self)
    lam = cur['lam']
    e1 = 1 - 2 * np.asarray(self.ratchet.gears[0].fine, dtype=object)
    qc = Fr(0)
    for k in coupled:
        g = clk.hands()[k].gears
        w = np.asarray(g[0].teeth, dtype=object) * np.ones(clk.size, dtype=object)
        P = gearP(g, w)
        for i in np.ndindex(clk.size):
            qc += qdens(int(e1[i]), lam[i], int(g[0].now[i]), int(g[1].now[i]), int(P[0][i]), int(P[1][i]))
    cur['q_click'] = qc
    ev = [x.get('event') for x in clk.log[log_from:]]
    cur['births'] = ev.count('birth')
    cur['events'] = len(ev)
    cur['click'] = True


T.Tick.carry, T.Tick.turnover, T.Tick.click = carry, turnover, click
for _ in range(ticks + 1):
    clock.tick()

vac = Fr(G ** 3, int(clock.teeth) * G)        # vacuum sweep units: lam X ... at X = mr = G, w = teeth G -> 1


def v(x):
    return (x * vac).__floor__()


print(f"I4 {world}, {ticks} ticks, variant {variant}; coupled hands {coupled}; Q* in vacuum sweep units")
agg = dict(step_id=0, A_nz=0, A_max=Fr(0), Rt=Fr(0), Rc=Fr(0), turn_id=0, turned=0, proper_bad=0, edges=0,
           C=Fr(0), C_nz=0, B=Fr(0), B_id=0, pull_ok=0, carry_ok=0, teeth_kept=0, inflow=Fr(0), proper=Fr(0),
           tick_id=0, births=0)
total = Fr(0)
for row in rows[:ticks]:
    per = row['per']
    Itot = sum((sum(d['I'].values(), Fr(0)) for d in per.values()), Fr(0))
    Rt = sum((sum(d['Rt'].values(), Fr(0)) for d in per.values()), Fr(0))
    Rc = sum((sum(d['Rc'].values(), Fr(0)) for d in per.values()), Fr(0))
    step_change = row['q_mid'] - row['q_start']
    agg['step_id'] += int(step_change != Itot + Rt + Rc)
    agg['A_nz'] += int(Itot != 0)
    agg['A_max'] = max(agg['A_max'], abs(Itot))
    agg['Rt'] += Rt
    agg['Rc'] += Rc
    top = row['top']
    lost = Fr(0)
    prop = Fr(0)
    for d in per.values():
        for i in d['I']:
            if top[i]:
                lost += d['I'][i] + d['Rt'][i] + d['Rc'][i]
                ee = int(row['e'][i]) * row['lam'][i] * d['Eheld'][i]
                prop += ee if FIX2 else -2 * d['qheld'][i] - ee
    turn_change = row['q_turn'] - row['q_mid']
    turned, bad, edges = row['turn_checks']
    agg['turned'] += turned
    agg['proper_bad'] += bad
    agg['edges'] += edges
    agg['turn_id'] += int(edges == 0 and turn_change != prop - lost)
    agg['inflow'] += -lost
    agg['proper'] += prop
    C = row['q_click'] - row['q_turn']
    agg['C'] += C
    agg['C_nz'] += int(C != 0)
    agg['births'] += row['births']
    B = row['next'] - row['q_click']
    agg['B'] += B
    agg['B_id'] += int(B != row['B_formula'])
    agg['pull_ok'] += int(all(d['pull_ok'] for d in per.values()))
    agg['carry_ok'] += int(all(d['carry_ok'] for d in per.values()))
    agg['teeth_kept'] += int(row.get('teeth_kept', True))
    tick_change = row['next'] - row['q_start']
    agg['tick_id'] += int(tick_change != step_change + turn_change + C + B)
    total += tick_change
n = len(rows[:ticks])
print(f"  the head's own pull read back at {agg['pull_ok']} of {n} ticks; the carry P' = w' v + rho' at {agg['carry_ok']} of {n};"
      f" the momentum read with the gear's own teeth at the next start at {agg['teeth_kept']} of {n}")
print(f"  the step: Q*_mid - Q*_start = SUM (I + Rt + Rc) fails at {agg['step_id']} of {n} ticks")
print(f"  the Mesh currents: A = SUM I not 0 at {agg['A_nz']} of {n} ticks, largest |A| {v(agg['A_max'])}")
print(f"  the turnover: {agg['turned']} Node-clock turnovers; the proper term off its formula at {agg['proper_bad']}"
      f" (the mirror's even-teeth edge at {agg['edges']}); the turnover identity fails at {agg['turn_id']} of {n} ticks")
print(f"  the rates: B = -SUM e (lam' - lam) Im(conj(a) P) fails at {agg['B_id']} of {n} ticks")
print(f"  the tick: Q*_next - Q*_start = step + turnover + click + rates fails at {agg['tick_id']} of {n} ticks")
print(f"  over the run (summed): Q* moved {v(total)}; the turns' rounding {v(agg['Rt'])}, the carry's rounding"
      f" {v(agg['Rc'])}; the turnovers' proper term {v(agg['proper'])}, the turned clocks' inflow not taken"
      f" {v(agg['inflow'])}; the click {v(agg['C'])} ({agg['C_nz']} ticks, {agg['births']} births);"
      f" the rates {v(agg['B'])}")
big = dict(Rt=Fr(0), Rc=Fr(0), proper=Fr(0), inflow=Fr(0), C=Fr(0), B=Fr(0), A=Fr(0))
for row in rows[:ticks]:
    per = row['per']
    top = row['top']
    big['A'] = max(big['A'], abs(sum((sum(d['I'].values(), Fr(0)) for d in per.values()), Fr(0))))
    big['Rt'] = max(big['Rt'], abs(sum((sum(d['Rt'].values(), Fr(0)) for d in per.values()), Fr(0))))
    big['Rc'] = max(big['Rc'], abs(sum((sum(d['Rc'].values(), Fr(0)) for d in per.values()), Fr(0))))
    lost = prop = Fr(0)
    for d in per.values():
        for i in d['I']:
            if top[i]:
                lost += d['I'][i] + d['Rt'][i] + d['Rc'][i]
                ee = int(row['e'][i]) * row['lam'][i] * d['Eheld'][i]
                prop += ee if FIX2 else -2 * d['qheld'][i] - ee
    big['proper'] = max(big['proper'], abs(prop))
    big['inflow'] = max(big['inflow'], abs(lost))
    big['C'] = max(big['C'], abs(row['q_click'] - row['q_turn']))
    big['B'] = max(big['B'], abs(row['next'] - row['q_click']))
print("  largest |term| in one tick: " + ', '.join(f"{k} {v(x)}" for k, x in big.items()))
ok = (agg['step_id'] == 0 and agg['tick_id'] == 0 and agg['B_id'] == 0 and agg['turn_id'] == 0 and agg['proper_bad'] == 0
      and agg['pull_ok'] == n and agg['carry_ok'] == n)
crit = ok and agg['A_nz'] == 0 and FIX2
print(f"VERDICT {variant}: the budget closes to the last digit: {ok}; the currents antisymmetric at every tick:"
      f" {agg['A_nz'] == 0}; the turnover keeps the framed charge up to its booked terms: {FIX2 and agg['proper_bad'] == 0};"
      f" PASS as the derived act: {crit}")
