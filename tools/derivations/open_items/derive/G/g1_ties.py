"""G1 (drafter G): the exact ties of every carry with a mid rounding on the head's engine, and the
matter against antimatter read, under a tie rule installed at run time (monkeypatching only; no file of
the repository or the worktree is changed).

argv: world ticks rule back [mirror]
  rule   head  the engine untouched but for counting wrappers
         up    the driven carry re-spelt here as half up (must equal head bit for bit)
         even  the driven carry's exact tie sent to the even quotient (Animate's candidate)
         down  the driven carry's exact tie sent down
  back   ticks rewound at the end, each compared with the forward state's hash (run.state_hash)
  mirror mod    the head's turnover mirror r -> (2 mid - r) mod W on every gear (default)
         exact  on the driven gears the turnover reverses the stride exactly, P -> -P, and re-carries it
                under the rule in force (the carry kept in the stride, in the before slot)

Sites counted (S1 to S7), each an exact tie of its own rounding:
  S1 the driven carry, tick.py:266, v = (p + mid W) div W: tie where W is even and p + mid W = 0 mod W
  S2 the impulse's u = rounded(2 p + 1, 2 t X), tick.py:231-232: half up in p, tie where 2 p = t X mod 2 t X
  S3 the tension, meshes.factors, t = (n_i + n_j + 1) div 2: tie where n_i + n_j is odd
  S4 the carried carries (Rule3's turn of the regulator and the ratchet, clock.turn; every drive,
     clock.drive and tick.py's own): their remainder is kept, so no tie is chosen; counted is the
     remainder landing at 0 at even teeth, the one point where the mirror misses -P
  S5 the setting's rest lay, assembly/setting.py:213, carry(total, w, mid w): tie as S1
  S6 the turnover: the turned driven gears whose fine tooth stands at 0 (or at W under a variant),
     where the head's mirror misses -P
  S7 the mesh factor's rounding, rule3.mesh_factor: read once over every tension 0..Gamma
"""
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src', S + '/t24']
sys.set_int_max_str_digits(0)
import numpy as np  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe.assembly import setting as SET  # noqa: E402
from event_universe import tick as T, readings, hands, run as RUN, unwind as UW, click as CK  # noqa: E402
from event_universe import unspring as UNSPRING, clock as CL, symmetries as SYM  # noqa: E402
from event_universe.core import acts, rates, rule3  # noqa: E402
from event_universe.core.spokes import AXES, SPOKES, SPOKE_SIDES, across  # noqa: E402
from event_universe.meshes import coupling_of  # noqa: E402
from event_universe.reckoner import Chart  # noqa: E402
from event_universe.trains import REGULATOR, OFFSET, HAND  # noqa: E402

world, ticks, rule, back = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
mirror_kind = sys.argv[5] if len(sys.argv) > 5 else 'mod'
digest_on = (sys.argv[6] if len(sys.argv) > 6 else 'digest') == 'digest'
urule = sys.argv[7] if len(sys.argv) > 7 else 'head'
skew_off = len(sys.argv) > 8 and sys.argv[8] == 'noskew'  # a diagnosis only: the flow gears' skew turn struck
assert rule in ('head', 'up', 'even', 'down') and mirror_kind in ('mod', 'exact') and urule in ('head', 'even', 'down')

C = Counter()          # every count of the run
TICK = Counter()       # the counts of the tick under way
orig_carry = acts.carry
orig_mid = acts.mid


def obj(x):
    return np.asarray(x, dtype=object)


def nz(x):
    return int(np.count_nonzero(obj(x).astype(bool)))


# ---------------------------------------------------------------- the tie rules at the driven carry
def q_rule(p, w, which):
    """The driven carry's quotient and fine tooth under a tie rule: v and fine with p + mid = w v + fine;
    head/up: fine in [0, w); even: the exact tie to the even v (fine = w where it rounds down); down:
    the exact tie down (fine = w)."""
    m = orig_mid(w)
    u = p + m
    q0 = u // w
    s = u - w * q0
    tie = (obj(w) % 2 == 0) & (obj(s) == 0)
    if which == 'up':
        q = q0
    elif which == 'even':
        q = q0 - tie * (obj(q0) % 2)
    else:
        q = q0 - tie
    if np.ndim(q) == 0 and np.ndim(p) == 0 and np.ndim(w) == 0:
        q = int(q)
    return q, u - w * q, tie


DRIVEN_ORDER = []      # the (train name, gear) of each driven carry in a tick, in the tick's order
call_index = [0]


def tick_carry(total, teeth, fine, *going):
    """tick.py's own carry name: the drive carries (four arguments, a carried fine tooth) counted as S4,
    the driven carry (three arguments, the mid tooth) counted as S1 and carried under the rule."""
    if going:
        out = orig_carry(total, teeth, fine, *going)
        C['S4 drive (tick.py) carries'] += np.size(obj(out[1]))
        C['S4 drive (tick.py) remainder at 0, even teeth'] += nz((obj(out[1]) == 0) & (obj(teeth) % 2 == 0))
        return out
    m = orig_mid(teeth)
    assert bool(np.all(obj(fine) == obj(m))), 'a three-argument carry in tick.py off the mid tooth'
    name = DRIVEN_ORDER[call_index[0] % len(DRIVEN_ORDER)] if DRIVEN_ORDER else '?'
    call_index[0] += 1
    which = 'up' if rule == 'head' else rule
    q, f, tie = q_rule(total, teeth, which)
    n_tie = nz(tie)
    C['S1 driven carries'] += np.size(obj(f))
    C['S1 driven carries, odd teeth'] += nz(obj(teeth) % 2 == 1) * (np.size(obj(f)) if np.ndim(teeth) == 0 else 1)
    C['S1 ties'] += n_tie
    C[f'S1 ties on {name}'] += n_tie
    TICK['S1'] += n_tie
    if n_tie:
        p_t = obj(total)[obj(tie).astype(bool)] if np.ndim(total) else [total]
        C['S1 tie strides positive'] += sum(1 for x in np.asarray(p_t).flat if int(x) > 0)
        C['S1 tie strides negative'] += sum(1 for x in np.asarray(p_t).flat if int(x) < 0)
    if rule == 'head':
        out = orig_carry(total, teeth, fine)
        assert bool(np.all(obj(out[0]) == obj(q))) and bool(np.all(obj(out[1]) == obj(f)))
        return out
    return q, f


T.carry = tick_carry

orig_tick_carry_method = T.Tick.carry


def tick_carry_method(self):
    DRIVEN_ORDER.clear()
    for r in self.driven:
        nm = name_of(self.clock, r)
        DRIVEN_ORDER.extend([nm] * len(self.trains[self.where[id(r)]]))
    call_index[0] = 0
    return orig_tick_carry_method(self)


T.Tick.carry = tick_carry_method


def name_of(clock, r):
    if r in clock.hands():
        k = clock.hands().index(r)
        return f'hand {k}' + (' (light)' if r is clock.unsprung() else '')
    if r is clock.train(OFFSET):
        return 'offset'
    if r.weight is not None:
        return 'held field'
    return f'train size {r.size}'


# ---------------------------------------------------------------- S2, the impulse's odd rounding u
orig_rounded = rates.rounded
IN_IMPULSE = [None]
U_ORDER = []
u_index = [0]
U_TIES = []


def rounded_wrapped(numerator, teeth):
    out = orig_rounded(numerator, teeth)
    d = IN_IMPULSE[0]
    if d is not None and np.size(obj(teeth)) and bool(np.all(obj(teeth) == obj(d))):
        n = obj(numerator)
        name = U_ORDER[u_index[0]] if u_index[0] < len(U_ORDER) else '?'
        u_index[0] += 1
        C['S2 u roundings'] += np.size(n)
        tie = ((n - 1) % obj(teeth)) == (obj(teeth) // 2)
        k = nz(tie)
        C['S2 u ties (2p = tX mod 2tX)'] += k
        TICK['S2'] += k
        if k:
            C[f'S2 u ties on {name}'] += k
            idx = list(zip(*np.nonzero(np.asarray(tie, dtype=bool)))) if np.ndim(tie) else [()]
            for at in idx:
                nv = int(n[at]) if np.ndim(n) else int(n)
                uv = int(obj(out)[at]) if np.ndim(out) else int(out)
                U_TIES.append((T_NOW[0], name, at, (nv - 1) // 2, uv))
            if urule == 'even':
                out = obj(out) - tie * (obj(out) % 2)
            elif urule == 'down':
                out = obj(out) - tie
    return out


T_NOW = [0]


rates.rounded = rounded_wrapped
orig_impulse = T.Tick.impulse


def impulse_wrapped(self):
    IN_IMPULSE[0] = (self.clock.teeth + self.clock.teeth) * self.stretch_now
    U_ORDER.clear()
    for r in self.driven:
        nm = name_of(self.clock, r)
        ng = len(self.trains[self.where[id(r)]])
        U_ORDER.extend([f'{nm} gear {g} in' for g in range(ng)] + [f'{nm} gear {g} out' for g in range(ng)])
    u_index[0] = 0
    T_NOW[0] = self.clock.ticks
    try:
        return orig_impulse(self)
    finally:
        IN_IMPULSE[0] = None


T.Tick.impulse = impulse_wrapped

# ---------------------------------------------------------------- S3, the tension's mean
orig_factors = T.factors


def factors_wrapped(clock, axis_notches=None, stopped=None):
    notches = (
        [g.now for g in clock.train(REGULATOR).gears[1:1 + AXES]] if axis_notches is None else axis_notches
    )
    for spoke, (axis, _side) in enumerate(SPOKE_SIDES):
        e = obj(notches[axis]) + obj(across(notches[axis], spoke))
        odd = (e % 2) == 1
        t = (e + 1) // 2
        live = odd & (t >= 0) & (t <= clock.full_rate)
        C['S3 tension means'] += np.size(e)
        C['S3 tension ties (n_i + n_j odd)'] += nz(odd)
        C['S3 tension ties inside 0..Gamma'] += nz(live)
        TICK['S3'] += nz(live)
    return orig_factors(clock, axis_notches, stopped)


T.factors = factors_wrapped
if skew_off:
    T.skewed = lambda meshes, rotation, flow_gears, full_rate: meshes


# ---------------------------------------------------------------- S4, the carried carries via acts.carry
def acts_carry_wrapped(total, teeth, fine, going=1):
    out = orig_carry(total, teeth, fine, going)
    caller = sys._getframe(1).f_code.co_name
    if caller in ('turn', 'drive'):
        r = obj(out[1])
        two = np.ndim(teeth) == 0 and int(teeth) == 2
        label = f'S4 {caller}' + (' (the ratchet, two teeth: its pawl bit)' if two else '')
        C[f'{label} carries'] += np.size(r)
        k = nz((r == 0) & (obj(teeth) % 2 == 0))
        C[f'{label} remainder at 0, even teeth'] += k
        if not two:
            TICK['S4'] += k
    return out


acts.carry = acts_carry_wrapped


# ---------------------------------------------------------------- the unwind's move under a variant
def move_kept(clock, rec, k, at, count):
    """unwind.move with the fine tooth read modulo its teeth: the head's move exactly where the fine
    tooth is in [0, W) (q = count), and the same move where a variant leaves it at W."""
    gears = clock.hands()[rec].gears
    teeth = UW.at_clock(gears[k].teeth, at)
    q, _unmoved = orig_carry(count * teeth, teeth, int(gears[k].fine[at]) % teeth, 1)
    UW.advance(clock, rec, at, tuple(q if j == HAND * k else 0 for j in range(HAND * len(gears))))


if rule in ('even', 'down'):
    UW.move = CK.move = UNSPRING.move = move_kept

# ---------------------------------------------------------------- S5, the setting's rest lay
orig_set_carry = SET.carry


def set_carry_wrapped(total, teeth, fine, *going):
    out = orig_set_carry(total, teeth, fine, *going)
    if not going:
        m = orig_mid(teeth)
        tie = (obj(teeth) % 2 == 0) & ((obj(total) + obj(m)) % obj(teeth) == 0)
        C['S5 setting carries'] += np.size(obj(out[1]))
        C['S5 setting ties'] += nz(tie)
    return out


SET.carry = set_carry_wrapped

# ---------------------------------------------------------------- S6, the turnover
orig_reverse = CL.Clock.reverse


def reverse_wrapped(self, top, held):
    topb = np.asarray(top, dtype=bool)
    for r, held_train in zip(self.trains_, held, strict=True):
        driven = r.teeth is None and r.size != REGULATOR
        signs = hands.signs(r.size)
        for g, s in zip(held_train, signs, strict=True):
            f, w = obj(g.fine)[topb], obj(g.teeth if np.ndim(g.teeth) == 0 else obj(g.teeth)[topb])
            if driven and s > 0:
                C['S6 turned driven gears (mirrored once)'] += np.size(f)
                k0 = nz((f == 0) & (w % 2 == 0))
                kw = nz(f == w)
                C['S6 turned driven gears at fine 0 (the mirror misses -P by W)'] += k0
                C['S6 turned driven gears at fine W (a variant tie)'] += kw
                TICK['S6'] += k0 + kw
            if g.dfine is not None:
                C['S6 turned drive fine teeth'] += np.size(obj(g.dfine)[topb])
                C['S6 turned drive fine teeth at 0'] += nz(obj(g.dfine)[topb] == 0)
            if not driven and r.teeth is None:
                C['S6 turned regulator gears'] += np.size(f)
                C['S6 turned regulator gears at fine 0'] += nz(f == 0)
    if mirror_kind == 'exact':
        return reverse_exact(self, top, held)
    return orig_reverse(self, top, held)


def reverse_exact(self, top, held):
    """The turnover with the driven gears' stride reversed exactly and re-carried under the rule:
    now' = s before, P' = -s P read at the held teeth (for s = 1; the K-negated gear keeps P), then
    before' = now' - v(P'), fine' = P' - W v(P') + mid; every other gear as the head turns it."""
    orig_reverse(self, top, held)
    topb = np.asarray(top, dtype=bool)
    which = 'up' if rule == 'head' else rule
    for r, train, held_train in zip(self.trains_, self.trains(), held, strict=True):
        if not (r.teeth is None and r.size != REGULATOR):
            continue
        for g, h, s in zip(train, held_train, hands.signs(r.size), strict=True):
            if s < 0:
                continue
            w = h.teeth
            P = w * (h.now - h.before) + h.fine - orig_mid(w)
            P2 = -P
            v, f, _tie = q_rule(P2, w, which)
            now2 = h.before
            g.now = np.where(topb, now2, g.now)
            g.before = np.where(topb, now2 - v, g.before)
            g.fine = np.where(topb, f, g.fine)


CL.Clock.reverse = reverse_wrapped


# ---------------------------------------------------------------- readings
def sweeps(clock):
    return [hands.sweep(r.gears) for r in clock.hands()]


def plain_charges(clock):
    return [sum(int(x) for x in obj(w).flat) for w in sweeps(clock)]


def q_star(clock):
    """Draft A's verifier's Q* per hand at the tick's end: -SUM eps D / (X mr^2) in vacuum units, D =
    Im(conj(a) P), P = W (now - before) + fine - mid(W) at the regulator's mean teeth, eps = 1 - 2 pawl
    bit, the stopped clocks left out."""
    g0 = clock.train(REGULATOR).gears[0]
    X = obj(g0.now)
    load = readings.load(clock)
    mr = obj(rates.mesh_rate_of(clock.full_rate, np.maximum(obj(load), 0))) * np.ones(clock.size, dtype=object)
    eps = 1 - 2 * obj(clock.ratchet_fine())
    G = clock.full_rate
    found = []
    for r in clock.hands():
        a3, a12 = r.gears[0], r.gears[1]
        w = a3.teeth
        P3 = w * (a3.now - a3.before) + a3.fine - orig_mid(w)
        P12 = w * (a12.now - a12.before) + a12.fine - orig_mid(w)
        D = obj(a3.now) * obj(P12) - obj(a12.now) * obj(P3)
        tot = Fraction(0)
        for i in np.ndindex(clock.size):
            if int(mr[i]):
                tot += Fraction(int(eps[i]) * int(D[i]), int(X[i]) * int(mr[i]) ** 2)
        found.append(-tot * Fraction(G * G, int(clock.teeth)))
    return found


def ratchet_fine(self):
    return T.ratchet_of(self.trains_).gears[0].fine


CL.Clock.ratchet_fine = ratchet_fine

# ---------------------------------------------------------------- the run
calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + world))
t0 = time.time()
clock = CL.Clock(calibre, piece)
hand_names = [name_of(clock, r) for r in clock.hands()]
couplings = [coupling_of(r) for r in clock.hands()]
print(f'{world}, {ticks} ticks, rule {rule}, mirror {mirror_kind}, back {back}, the impulse rounding u at its tie: {urule}'
      + (', the skew struck (a diagnosis)' if skew_off else ''))
print(f'hands (acts order): {hand_names}; couplings {couplings}; teeth t = {clock.teeth} (t even: {clock.teeth % 2 == 0})')
print(f'setting: S5 carries {C["S5 setting carries"]}, ties {C["S5 setting ties"]}')
q0 = plain_charges(clock)
print(f'tick 0: plain charges {q0}; Q* (floor) {[x.numerator // x.denominator for x in q_star(clock)]}')

hashes = []
per_tick = []
import hashlib  # noqa: E402
digest = hashlib.sha256()
last_line = None
for t in range(ticks):
    TICK.clear()
    if back and t >= ticks - back:
        hashes.append(RUN.state_hash(clock))
    log_from = len(clock.log)
    clock.tick()
    new = clock.log[log_from:]
    if digest_on:
        digest.update(RUN.state_hash(clock).encode())
    births = [e for e in new if e['event'] == 'birth']
    pairs = sum(1 for e in births if 'takes' not in e)
    mergers = sum(1 for e in births if 'takes' in e)
    chimes = [e for e in new if e['event'] == 'credit']
    ch_plus = sum(1 for e in chimes if e['sense'] > 0)
    ch_minus = sum(1 for e in chimes if e['sense'] < 0)
    turned = int(np.asarray(clock.turned_over).sum())
    qs = plain_charges(clock)
    X = sorted({int(x) for x in obj(clock.train(REGULATOR).gears[0].now).flat})
    row = (clock.ticks, turned, pairs, mergers, ch_plus, ch_minus, TICK['S1'], TICK['S2'], TICK['S3'],
           TICK['S4'], TICK['S6'], tuple(qs))
    per_tick.append(row)
    line = (turned, pairs, mergers, ch_plus, ch_minus, TICK['S1'], TICK['S2'], TICK['S3'], TICK['S4'],
            TICK['S6'], tuple(qs))
    if line != last_line or clock.ticks in (1, ticks):
        xs = X if len(X) <= 3 else f'{len(X)} values {X[0]}..{X[-1]}'
        print(f'  tick {clock.ticks:3d}: X {xs}; turned {turned}; births {pairs} pairs, {mergers} mergers;'
              f' chimes +{ch_plus} -{ch_minus}; ties S1 {TICK["S1"]} S2 {TICK["S2"]} S3 {TICK["S3"]}'
              f' S4 {TICK["S4"]} S6 {TICK["S6"]}; plain charges {list(qs)}')
    last_line = line

elapsed = time.time() - t0
final_hash = RUN.state_hash(clock)
print(f'forward done in {elapsed:.0f} s; the final state hash {final_hash}')
if digest_on:
    print(f'the digest of the {ticks} per-tick state hashes: {digest.hexdigest()}')
print(f'S2 ties (tick, rounding, clock, p, the head\'s u): {U_TIES}')
print('counts:')
for k in sorted(C):
    print(f'  {k}: {C[k]}')

# the matter against antimatter, from the log
log = clock.log
births = [e for e in log if e['event'] == 'birth']
pairs = [e for e in births if 'takes' not in e]
mergers = [e for e in births if 'takes' in e]
by_hand = Counter()
for e in pairs:
    s = e['line_pair']
    plus_hand = e.get('plus_hand', s)
    by_hand[(hand_names[s], -1)] += 1
    by_hand[(hand_names[plus_hand], 1)] += 1
print(f'fittings: {len(pairs)} pairs, {len(mergers)} unspringings (mergers)')
print(f'  fitted hands by hand and sense: {sorted(by_hand.items())}')
print(f'  fittings per tick: {sorted(Counter(e["i"] for e in pairs).items())}')
print(f'  unspringings per tick: {sorted(Counter(e["i"] for e in mergers).items())}')
m_sign = Counter()
m_ends = Counter()
m_net = 0
for e in mergers:
    ws = []
    for t in e['takes']:
        n3, b3, n12, b12 = (int(x) for x in t['taken_levels'])
        ws.append(n3 * b12 - n12 * b3)
        m_ends[(hand_names[t.get('hand', e['taken_row'])], int(np.sign(ws[-1])))] += 1
    m_net += sum(ws)
    m_sign[(hand_names[e['taken_row']], int(np.sign(sum(ws))))] += 1
print(f'  unspringings by the unwound hand and the sign of the sweep they unwound (W_x + W_y): {sorted(m_sign.items())}')
print(f'  unspringings\' ends by hand and the sign of the sweep unwound there: {sorted(m_ends.items())}; the net sweep unwound {m_net}')
chimes = [e for e in log if e['event'] == 'credit']
ch = Counter((hand_names[e['line']], e['sense']) for e in chimes)
print(f'chimes by hand and sense: {sorted(ch.items())}')
qf = plain_charges(clock)
print(f'plain charges at the end (the head\'s sweep summed per hand): {qf}; their total {sum(qf)}')
print(f'  coupled total SUM c_T Q_T: {sum(c * q for c, q in zip(couplings, qf))}')
qs_end = q_star(clock)
print(f'Q* at the end per hand (vacuum units, the floor of the exact rational): {[x.numerator // x.denominator for x in qs_end]}')
print(f'  coupled total SUM c_T Q*_T (floor): {(lambda v: v.numerator // v.denominator)(sum((c * q for c, q in zip(couplings, qs_end)), Fraction(0)))}')
run = {
    'den': clock.rim, 'universe': calibre, 'gamma': clock.full_rate, 'G': clock.G, 'T': clock.key,
    'planes': [str(r.ratio[0]) for r in clock.hands() if r.ratio], 'log': log, 'cube': clock.cube,
    'rows': [], 'intervals': ticks, 'nodes': [],
}
chart = Chart(run)
for f in (SYM.matter_against_antimatter, SYM.one_twist, SYM.baryon_number):
    print(f'reckoner: {f(chart)}')
print(f'counts of the clock: {dict(clock.counts)}')

if back:
    exact = 0
    first_bad = None
    for k in range(len(hashes)):
        clock.tick(-1)
        ok = RUN.state_hash(clock) == hashes[len(hashes) - 1 - k]
        exact += ok
        if not ok and first_bad is None:
            first_bad = clock.ticks
    print(f'the rewind: {exact} of {len(hashes)} exact' + ('' if first_bad is None else f'; first missed at tick {first_bad}'))
print(f'done in {time.time() - t0:.0f} s')
