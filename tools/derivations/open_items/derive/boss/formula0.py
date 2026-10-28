"""Tensor24's cut 0, the Boss's check: the main formula against the head's step, gear by gear, at every node-clock.
Driven trains: p+ = p + s F, with p = W (a - a-) + (r - mid W) and p+ = W+ (a+ - a) + (r+ - mid W+), F the pull (the six Meshes' grips times
the neighbour carried across the Mesh less the gear, less the spring times the gear, with Pauli's term) and K the kicks (the offset's lead, the
held field's masses). The regulator: Rule3's turn T a+ = hold a - T a- + sum_j grip_j a_j, then the drive of its numerators."""
import sys
from collections import Counter
import numpy as np
sys.path[:0] = [sys.argv[1] + '/src', sys.argv[1]]
from tests.laws import world_of
from event_universe import tick as T, readings
from event_universe.clock import Clock
from event_universe.core.acts import carry, mid
from event_universe.core.rule3 import held_numerator
from event_universe.core.spokes import AXES
from event_universe.regulation import tensor_parts

stats = Counter()
orig_impulse, orig_carry = T.Tick.impulse, T.Tick.carry

def impulse(self):
    pre = {}
    for r in self.driven:
        k = self.where[id(r)]
        pre[k] = [(g.now.copy(), g.before.copy(), g.fine.copy()) for g in self.trains[k]]
    w_side = readings.mean_teeth(self.clock, self.regulator.gears[0])
    orig_impulse(self)
    s = self.stretch_now
    self._probe = {"w": w_side, "pre": pre}
    for r in self.driven:
        k = self.where[id(r)]
        kind = "offset" if r is self.offset else "held" if r.weight is not None else "hand"
        for i, (now, before, fine) in enumerate(pre[k]):
            p = w_side * (now - before) + fine - mid(w_side)
            K = self.impelled[k][i] - (p + self.going * s * self.pull[k][i])
            nz = int((K != 0).sum())
            stats[f"(i) {kind} gears, sites with a kick K != 0"] += nz
            stats[f"(i) {kind} gears, sites read"] += K.size
            if nz:
                unit = self.going * self.clock.teeth * s
                q = K // unit
                stats[f"(i) {kind} gears, kick sites where K = going T s q (q a whole carry)"] += int(((K == unit * q) & (K != 0)).sum())

def carry_(self):
    reg_k = self.where[id(self.regulator)]
    g_pre = [(g.now.copy(), g.before.copy(), g.fine.copy(), None if g.dfine is None else g.dfine.copy()) for g in self.trains[reg_k]]
    # the regulator's numerators as tick.carry builds them
    p02, (trace, traceless) = self.rate * self.rate, tensor_parts(self.stress[:AXES])
    clk = self.clock
    drive = held_numerator(clk.trace, self.stretch_now, self.forms, trace, self.rate, clk.rim, clk.full_rate)
    hold = self.stretch_now * self.trains[reg_k][0].dteeth
    numerators = [np.minimum(np.maximum(drive, -hold), hold)] + [part * p02 for part in (*traceless, *self.stress[AXES:])]
    gearing = readings.gearing_of(clk, self.regulator, self.load, self.factors)
    starts = {k: [a.copy() for a in v] for k, v in self.starts.items()}
    impelled = {k: [p.copy() for p in v] for k, v in self.impelled.items()}
    unsprung_k = self.where[id(clk.unsprung())]
    orig_carry(self)
    stopped = self.stopped
    # (iv) the regulator: the turn, then the drive
    for i, (now, before, fine, dfine) in enumerate(g_pre):
        total = gearing.hold * now - gearing.teeth * before + sum(
            grip * np.roll(now, 0) * 0 for grip in ()) + clk.pulls([now], gearing, None)[0] if False else None
    turned = clk.turn([type(self.trains[reg_k][0])(n, b, f, self.trains[reg_k][0].teeth, d, self.trains[reg_k][j].dteeth) for j, (n, b, f, d) in enumerate(g_pre)], gearing, None, 1, None, None)
    for j, (gear_t, gear_out, n_j) in enumerate(zip(turned, self.out[reg_k], numerators)):
        q, _ = carry(n_j, gear_t.dteeth, g_pre[j][3])
        ok = (gear_out.now == gear_t.now + q) | stopped
        stats["(iv) regulator gears, sites where now = turn + drive"] += int(ok.sum())
        stats["(iv) regulator gears, sites read"] += ok.size
    # (iii) the driven trains' carry
    w_div = self.end_teeth(self.out[reg_k][0])
    for r in self.driven:
        k = self.where[id(r)]
        for i, (a, p, gear) in enumerate(zip(starts[k], impelled[k], self.out[k])):
            v, fine = carry(p, w_div, mid(w_div))
            ok = ((gear.now == a + v) & (gear.fine == fine)) | stopped
            name = "unsprung gear 0 (the release drives it)" if (k == unsprung_k and i == 0) else "driven gears"
            stats[f"(iii) {name}, sites where a+ = a + carry(p + s F, W+)"] += int(ok.sum())
            stats[f"(iii) {name}, sites read"] += ok.size
            # the identity p+ = p + s F in its remainder form, W+ (a+ - a) + (r+ - mid W+) = p'
            lhs = w_div * (gear.now - a) + gear.fine - mid(w_div)
            stats[f"(iii) {name}, sites where W+ (a+ - a) + (r+ - mid W+) = p + s F + K"] += int(((lhs == p) | stopped).sum())

T.Tick.impulse, T.Tick.carry = impulse, carry_
calibre, piece = world_of(sys.argv[2])
clock = Clock(calibre, piece)
for _ in range(int(sys.argv[3])):
    clock.tick()
print(sys.argv[2], sys.argv[3], "ticks")
for k in sorted(stats):
    print(f"  {k}: {stats[k]}")
