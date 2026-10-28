"""G7 (drafter G): a world against its antiworld under one tie rule (monkeypatching only).

The antiworld is the world's seed under C, applied to the clock after the setting and before the first tick:
every matter hand (coupling 1) by K, its twelve gear negated; the light (coupling 0) negated whole, both
gears, since the release's advance on the light is odd under K; every negated gear's fine tooth and drive
fine tooth reflected about mid, r -> w - r (the stride P -> -P exactly); the regulator, the offset train
(all at rest at the start) and the ratchet as they are. If the head were C-covariant but for the tie, then
by Theorem 3 the antiworld under (a) would carry exactly the negated charges of the world under (c), and
under (b) the world and the antiworld would carry exactly opposite charges at every tick.

argv: world ticks rule urule [image] [noskew] (noskew: a diagnosis, the flow gears' skew turn of the
hands, meshes.skewed, struck in both runs; rule and urule each up, even or down: the driven carry's tie and
the impulse's u's tie; image 'twelve' (default: K on the matter, the light whole) or 'three' (-K on every
hand: its three gear negated, which exchanges the fitted pair (A, iB) and (-A, iB) and keeps the light's
release on its three gear and its turns covariant)). Prints per tick the coupled hands' plain charges of the world and of the antiworld, and
their sum (0 at every tick where the pair is exactly C-symmetric).
"""
import sys
from pathlib import Path

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src', S + '/t24']
sys.set_int_max_str_digits(0)
import numpy as np  # noqa: E402
from collections import Counter  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe import tick as T, clock as CL, unwind as UW, click as CK, unspring as UNSPRING, hands  # noqa: E402
from event_universe.core import acts, rates  # noqa: E402
from event_universe.meshes import coupling_of  # noqa: E402
from event_universe.trains import HAND  # noqa: E402

world, ticks, rule, urule = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
image = sys.argv[5] if len(sys.argv) > 5 else 'twelve'
skew_off = len(sys.argv) > 6 and sys.argv[6] == 'noskew'  # a diagnosis only: the flow gears' skew turn struck
orig_carry, orig_rounded, orig_impulse = acts.carry, rates.rounded, T.Tick.impulse
D = [None]


def obj(x):
    return np.asarray(x, dtype=object)


def pick(q0, tie, which):
    if which == 'up':
        return q0
    if which == 'even':
        return q0 - tie * (obj(q0) % 2)
    return q0 - tie


def tick_carry(total, teeth, fine, *going):
    if going:
        return orig_carry(total, teeth, fine, *going)
    m = acts.mid(teeth)
    u = total + m
    q0 = u // teeth
    tie = (obj(teeth) % 2 == 0) & (obj(u - teeth * q0) == 0)
    q = pick(q0, tie, rule)
    return q, u - teeth * q


def rounded_v(numerator, teeth):
    out = orig_rounded(numerator, teeth)
    if D[0] is not None and np.size(obj(teeth)) and bool(np.all(obj(teeth) == obj(D[0]))):
        tie = ((obj(numerator) - 1) % obj(teeth)) == (obj(teeth) // 2)
        if np.any(tie):
            out = obj(out) - tie if urule == 'down' else (obj(out) - tie * (obj(out) % 2) if urule == 'even' else out)
    return out


def impulse_v(self):
    D[0] = (self.clock.teeth + self.clock.teeth) * self.stretch_now
    try:
        return orig_impulse(self)
    finally:
        D[0] = None


def move_kept(clock, rec, k, at, count):
    gears = clock.hands()[rec].gears
    teeth = UW.at_clock(gears[k].teeth, at)
    q, _unmoved = orig_carry(count * teeth, teeth, int(gears[k].fine[at]) % teeth, 1)
    UW.advance(clock, rec, at, tuple(q if j == HAND * k else 0 for j in range(HAND * len(gears))))


T.carry = tick_carry
rates.rounded = rounded_v
if skew_off:
    T.skewed = lambda meshes, rotation, flow_gears, full_rate: meshes
T.Tick.impulse = impulse_v
UW.move = CK.move = UNSPRING.move = move_kept


def negate(gear):
    w = gear.teeth
    gear.now, gear.before = -obj(gear.now), -obj(gear.before)
    gear.fine = obj(w) - obj(gear.fine)
    if gear.dfine is not None:
        gear.dfine = obj(gear.dteeth) - obj(gear.dfine)


def conjugate(clock):
    for r in clock.hands():
        if image == 'three':
            negate(r.gears[0])
        elif coupling_of(r) == 0:
            for g in r.gears:
                negate(g)
        else:
            negate(r.gears[1])


def run(anti):
    calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + world))
    clock = CL.Clock(calibre, piece)
    if anti:
        conjugate(clock)
    coupled = [k for k, r in enumerate(clock.hands()) if coupling_of(r) == 1]
    series = []
    for _ in range(ticks):
        clock.tick()
        series.append([sum(int(x) for x in obj(hands.sweep(clock.hands()[k].gears)).flat) for k in coupled])
    births = Counter((e['line_pair'], e['i']) for e in clock.log if e['event'] == 'birth' and 'takes' not in e)
    chimes = Counter((e['line'], e['sense']) for e in clock.log if e['event'] == 'credit')
    return coupled, series, births, chimes


coupled, w_series, w_births, w_chimes = run(False)
_c, a_series, a_births, a_chimes = run(True)
print(f'{world}, {ticks} ticks, the driven carry {rule}, the impulse u {urule}, the image {image}'
      f'{", the skew struck (a diagnosis)" if skew_off else ""}; coupled hands {coupled}')
first = None
for t, (w, a) in enumerate(zip(w_series, a_series, strict=True), start=1):
    s = [x + y for x, y in zip(w, a, strict=True)]
    if first is None and any(s):
        first = t
    print(f'  tick {t:3d}: world {w}; antiworld {a}; sum {s}')
print(f'the first tick where the antiworld is not the world negated: {first}')
print(f'births (hand, tick): world {sorted(w_births.items())}; antiworld {sorted(a_births.items())}')
print(f'chimes (hand, sense): world {sorted(w_chimes.items())}; antiworld {sorted(a_chimes.items())}')
print(f'the coupled charge at the end: world {sum(w_series[-1])}, antiworld {sum(a_series[-1])}, their sum {sum(w_series[-1]) + sum(a_series[-1])}')
