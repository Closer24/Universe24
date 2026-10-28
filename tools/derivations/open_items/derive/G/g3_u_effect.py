"""G3 (drafter G): where the impulse's three exact ties of u on nature go (tick 3, the light's three gear,
u_in at the clocks (1,1,1), (1,1,4), (2,0,4)), read-only on the head's engine (monkeypatching only).

The head's u = rounded(2 p + 1, 2 t X) sends the tie p = (k + 1/2) t X up; the variant sends it down. This
probe runs nature to tick 3 under each, and at the tie clocks reads: the forms and the regulator's time
gear's drive against its hold (the clamp), the stress's parts, the clock's turnover at the tick, and every
state array at the tick's end. argv: none.
"""
import sys
from pathlib import Path

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src', S + '/t24']
sys.set_int_max_str_digits(0)
import numpy as np  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe import tick as T, run as RUN, clock as CL  # noqa: E402
from event_universe.core import rates  # noqa: E402
from event_universe.core.rule3 import held_numerator  # noqa: E402
from event_universe.regulation import tensor_parts  # noqa: E402
from event_universe.core.spokes import AXES  # noqa: E402

TIES = [(1, 1, 1), (1, 1, 4), (2, 0, 4)]
orig_rounded = rates.rounded
orig_impulse = T.Tick.impulse
orig_carry = T.Tick.carry
STATE = {'mode': 'head', 'd': None}
READ = {}


def obj(x):
    return np.asarray(x, dtype=object)


def rounded_v(numerator, teeth):
    out = orig_rounded(numerator, teeth)
    d = STATE['d']
    if d is not None and np.size(obj(teeth)) and bool(np.all(obj(teeth) == obj(d))):
        n = obj(numerator)
        tie = ((n - 1) % obj(teeth)) == (obj(teeth) // 2)
        if np.any(tie):
            READ.setdefault('ties', []).append([tuple(int(i) for i in at) for at in zip(*np.nonzero(np.asarray(tie, dtype=bool)))])
            if STATE['mode'] == 'down':
                out = obj(out) - tie
    return out


def impulse_v(self):
    STATE['d'] = (self.clock.teeth + self.clock.teeth) * self.stretch_now
    try:
        orig_impulse(self)
    finally:
        STATE['d'] = None
    if self.clock.ticks == 3:
        READ['forms'] = [int(self.forms[at]) for at in TIES]
        READ['stress'] = [[int(s[at]) for s in self.stress] for at in TIES]


def carry_v(self):
    if self.clock.ticks == 3:
        clk = self.clock
        k = self.where[id(self.regulator)]
        trace, _traceless = tensor_parts(self.stress[:AXES])
        drive = held_numerator(clk.trace, self.stretch_now, self.forms, trace, self.rate, clk.rim, clk.full_rate)
        hold = self.stretch_now * self.trains[k][0].dteeth
        READ['drive'] = [int(obj(drive)[at]) for at in TIES]
        READ['hold'] = [int(obj(hold)[at]) if np.ndim(hold) else int(hold) for at in TIES]
        READ['stopped'] = [bool(np.asarray(self.stopped)[at]) for at in TIES]
    return orig_carry(self)


rates.rounded = rounded_v
T.Tick.impulse = impulse_v
T.Tick.carry = carry_v

found = {}
for mode in ('head', 'down'):
    STATE['mode'] = mode
    READ.clear()
    calibre, piece = read_piece(Path(S + '/t24/tests/worlds/world_nature.json'))
    clock = CL.Clock(calibre, piece)
    for _ in range(3):
        clock.tick()
    READ['turned'] = [bool(np.asarray(clock.turned_over)[at]) for at in TIES]
    READ['hash'] = RUN.state_hash(clock)
    READ['state'] = RUN.state_text(clock)
    found[mode] = dict(READ)
    print(f'mode {mode}: ties at {READ.get("ties")}; turned at the tie clocks {READ["turned"]}; stopped {READ.get("stopped")}')
    print(f'  forms at the tie clocks {READ.get("forms")}')
    print(f'  the time gear drive {READ.get("drive")}')
    print(f'  its hold            {READ.get("hold")}')
    print(f'  clamped: {[abs(d) >= h for d, h in zip(READ.get("drive", []), READ.get("hold", []))]}')
    print(f'  stress parts at the tie clocks {READ.get("stress")}')
    print(f'  state hash at the end of tick 3: {READ["hash"]}')
h, d = found['head'], found['down']
print(f'forms differ: {h["forms"] != d["forms"]}; drive differs: {h["drive"] != d["drive"]};'
      f' stress differs: {h["stress"] != d["stress"]}; state differs: {h["state"] != d["state"]}')
