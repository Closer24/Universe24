"""G4 (drafter G): on world_pair_3, where the driven carry ties 135 times (all on the light, all 27 clocks at
once, ticks 29, 76, 91, 138, 365), how the states under the three tie rules differ: every gear array of
every train compared, after ticks 28, 29, 30, 100 and 400, under the head's rule (up) against down and even
(monkeypatching tick.py's carry name only; the unwind's move read with the fine tooth modulo its teeth).
argv: none.
"""
import sys
from pathlib import Path

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src', S + '/t24']
sys.set_int_max_str_digits(0)
import numpy as np  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe import tick as T, clock as CL, unwind as UW, click as CK, unspring as UNSPRING  # noqa: E402
from event_universe.core import acts  # noqa: E402
from event_universe.trains import HAND  # noqa: E402

orig_carry = acts.carry
RULE = ['up']


def obj(x):
    return np.asarray(x, dtype=object)


def tick_carry(total, teeth, fine, *going):
    if going:
        return orig_carry(total, teeth, fine, *going)
    m = acts.mid(teeth)
    u = total + m
    q0 = u // teeth
    s = u - teeth * q0
    tie = (obj(teeth) % 2 == 0) & (obj(s) == 0)
    q = q0 if RULE[0] == 'up' else (q0 - tie * (obj(q0) % 2) if RULE[0] == 'even' else q0 - tie)
    return q, u - teeth * q


def move_kept(clock, rec, k, at, count):
    gears = clock.hands()[rec].gears
    teeth = UW.at_clock(gears[k].teeth, at)
    q, _unmoved = orig_carry(count * teeth, teeth, int(gears[k].fine[at]) % teeth, 1)
    UW.advance(clock, rec, at, tuple(q if j == HAND * k else 0 for j in range(HAND * len(gears))))


T.carry = tick_carry
UW.move = CK.move = UNSPRING.move = move_kept


def run(rule, marks):
    RULE[0] = rule
    calibre, piece = read_piece(Path(S + '/t24/tests/worlds/world_pair_3.json'))
    clock = CL.Clock(calibre, piece)
    found = {}
    for t in range(1, max(marks) + 1):
        clock.tick()
        if t in marks:
            found[t] = [[(g.now.copy(), g.before.copy(), g.fine.copy(), None if g.dfine is None else g.dfine.copy())
                         for g in r.gears] for r in clock.trains_]
            found[t, 'names'] = [(r.size, r.ratio, r is clock.unsprung()) for r in clock.trains_]
            found[t, 'slack'] = clock.slack.copy()
            found[t, 'teeth'] = [[g.teeth for g in r.gears] for r in clock.trains_]
    return found


marks = [28, 29, 30, 100, 400]
runs = {rule: run(rule, marks) for rule in ('up', 'down', 'even')}
for other in ('down', 'even'):
    print(f'up against {other}:')
    for t in marks:
        a, b = runs['up'][t], runs[other][t]
        names = runs['up'][t, 'names']
        diffs = []
        for k, (ra, rb) in enumerate(zip(a, b, strict=True)):
            for g, (ga, gb) in enumerate(zip(ra, rb, strict=True)):
                for slot, (xa, xb) in zip(('now', 'before', 'fine', 'dfine'), zip(ga, gb, strict=True), strict=True):
                    if xa is None:
                        continue
                    d = obj(xb) - obj(xa)
                    if np.any(d != 0):
                        vals = sorted({int(v) for v in d.flat})
                        w = runs['up'][t, 'teeth'][k][g]
                        wv = sorted({int(v) for v in obj(w).flat}) if np.ndim(w) else [int(w)]
                        size, ratio, light = names[k]
                        label = 'the light' if light else f'train size {size}'
                        diffs.append(f'{label} gear {g} {slot}: {int(np.count_nonzero(d != 0))} clocks, differences'
                                     f' {vals if len(vals) <= 3 else str(len(vals)) + " values"}'
                                     + (f' (teeth {wv[0]})' if slot == 'fine' and len(wv) == 1 else ''))
        sl = obj(runs[other][t, 'slack']) - obj(runs['up'][t, 'slack'])
        if np.any(sl != 0):
            diffs.append(f'slack: {int(np.count_nonzero(sl != 0))} clocks')
        print(f'  after tick {t}: ' + ('; '.join(diffs) if diffs else 'every array equal'))
