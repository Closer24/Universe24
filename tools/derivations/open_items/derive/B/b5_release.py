"""Probe B5: the release's advance and its recoil as one act of every hand alike, weighed by the hand's own integers,
with no clock.unsprung() identity (R14); against the head bit for bit.

The generic act (installed at run time in place of tick.Tick.advances; no file edited), forward and backward alike:
  u_h = pinion_h div rim_h                    the hand's own Rule3 quotient: 1 where the pinion fills a whole rim
  c_h = 1 - u_h                               the coupling, the head's coupling_of = min(rim - pinion, 1) exactly
  R   = X SUM_h c_h (three_h F12_h - twelve_h F3_h)   (the head's release, every hand alike)
  rho = rounded(R, W+)                        (the head's odd rounding at the end teeth)
  q_h, r_dh = carry(u_h rho, key, r_dh)       on every hand's first gear (a gapped hand's drive remainder kept in a
                                              side table: its carry of 0 leaves it, counted)
  a_h0 += q_h                                 (the advance; as a kick it is W+ q_h before the gear's carry, identity I2)
  P_a  = SUM_h 2 pinion_h q_h (a_h0(x - e_a) - a_h0(x + e_a))   the push, a_h0 the first gear's start notch
  flow gear a: drive(-P_a p0^2) at every clock (the head's recoil, merged into the regulator's flow drive: I3)
Modes:
  lockstep WORLD TICKS [SEED_JSON]   the generic act against the head, every tick bit for bit, and its rewind of 20.
  identities                          I1 c_h = coupling_of over every calibre's rows and random pairs; I2 the advance
                                      after the carry equals the kick W+ q before it (random integers of both signs);
                                      I3 two drives at one teeth equal one drive of their sum (random), both goings."""

import json
import random
import sys

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
import hashlib  # noqa: E402

import bcommon as B  # noqa: E402
from bcommon import np  # noqa: E402
from event_universe import meshes  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.core import rates  # noqa: E402
from event_universe.core.acts import carry, mid  # noqa: E402
from event_universe.core.spokes import AXES, across, spoke_of  # noqa: E402
from event_universe.trains import REGULATOR, zeros  # noqa: E402
from tests.laws import run_back_exact  # noqa: E402

HEAD_ADV = T.Tick.advances
SIDE = {}
TALLY = {"gapped drive remainders moved": 0, "hands read": 0}


def advances(self):
    clock = self.clock
    time_gear = clock.train(REGULATOR).gears[0]
    rho = rates.rounded(self.release, self.end_teeth(time_gear))
    push = [zeros(clock.size) for _ in range(AXES)]
    for h in clock.hands():
        pinion, rim = h.ratio
        u = pinion // rim
        gear = h.gears[0]
        if gear.dteeth is None:
            key = (id(clock), id(h))
            SIDE.setdefault(key, zeros(clock.size) + mid(clock.key))
            teeth, fine = clock.key, SIDE[key]
        else:
            teeth, fine = gear.dteeth, gear.dfine
        q, new_fine = carry(u * rho, teeth, fine, self.going)
        TALLY["hands read"] += 1
        if gear.dteeth is None:
            TALLY["gapped drive remainders moved"] += B.n(new_fine != fine)
            SIDE[(id(clock), id(h))] = new_fine
        else:
            gear.dfine = new_fine
        notches = gear.now
        gear.now = notches + self.going * q
        if self.going == 1:
            T.advanced_on(clock, gear, notches)
        b = self.starts[self.where[id(h)]][0]  # the first gear's start notch, read alike in both goings
        for a in range(AXES):
            push[a] = push[a] + (pinion + pinion) * q * (across(b, spoke_of(a, 1)) - across(b, spoke_of(a, 0)))
    rate2 = clock.start_rate * clock.start_rate
    for a, flow in enumerate(clock.train(REGULATOR).gears[1 + AXES: 1 + AXES + AXES]):
        clock.drive(flow, -push[a] * rate2, self.going)


def digest(clock):
    return hashlib.sha256(B.state(clock).encode()).hexdigest()


def lockstep(world, ticks, seed):
    changes = {"seed": seed} if seed else {}
    a, b = B.make(world, **changes), B.make(world, **changes)
    differ, first = 0, None
    for t in range(ticks):
        T.Tick.advances = HEAD_ADV
        a.tick()
        T.Tick.advances = advances
        b.tick()
        T.Tick.advances = HEAD_ADV
        if digest(a) != digest(b):
            differ += 1
            first = t + 1 if first is None else first
    same_log = [str(e) for e in a.log] == [str(e) for e in b.log]
    T.Tick.advances = advances
    rewind = run_back_exact(B.make(world, **changes), min(20, ticks))
    T.Tick.advances = HEAD_ADV
    print(json.dumps({"mode": "lockstep", "world": world, "seed": seed or "file", "ticks": ticks,
                      "ticks whose state differs": differ, "first tick differing": first, "logs equal": same_log,
                      "laid head / generic": [a.counts["laid"], b.counts["laid"]],
                      "laid_nodes head / generic": [a.counts["laid_nodes"], b.counts["laid_nodes"]],
                      "rewind exact (generic)": rewind, **TALLY}), flush=True)


def identities():
    rng = random.Random(24)
    # I1: the coupling as the pinion's carry at the rim
    rows = []
    for name in ("universe_toy.json", "universe_bang.json", "universe_middle.json", "universe_ga2.json"):
        import json as _j

        cal = _j.load(open(B.S + "/t24/tests/worlds/" + name))
        rim = int(cal["integers"]["den"])
        rows += [(rim, rim)] + [tuple(int(x) for x in r["pair"]) for r in cal["rows"] if r.get("pair")]
    rows += [(p, d) for d in (rng.randrange(1, 10**18) for _ in range(20000)) for p in (rng.randrange(0, d + 1),)]
    rows += [(d, d) for d in (rng.randrange(1, 10**18) for _ in range(1000))]
    i1 = sum(1 - p // d == min(d - p, 1) for p, d in rows)
    # I2: an advance of q notches after the carry at W is the kick W q before it
    i2 = 0
    for _ in range(100000):
        w = rng.randrange(1, 10**30)
        p, q = rng.randrange(-10**34, 10**34), rng.randrange(-10**6, 10**6)
        v0, r0 = carry(p, w, mid(w))
        v1, r1 = carry(p + w * q, w, mid(w))
        i2 += (v1 == v0 + q) and (r1 == r0)
    # I3: two drives at one teeth with the remainder carried equal one drive of the sum, at +1 and at -1
    i3 = 0
    for _ in range(100000):
        t = rng.randrange(1, 10**25)
        r = rng.randrange(0, t)
        n1, n2 = rng.randrange(-10**30, 10**30), rng.randrange(-10**30, 10**30)
        g = rng.choice((1, -1))
        q1, r1 = carry(n1, t, r, g)
        q2, r2 = carry(n2, t, r1, g)
        q, rr = carry(n1 + n2, t, r, g)
        i3 += (q1 + q2 == q) and (r2 == rr)
    print(json.dumps({"mode": "identities", "I1 pairs": len(rows), "I1 holds": i1, "I2 draws": 100000, "I2 holds": i2,
                      "I3 draws": 100000, "I3 holds": i3}), flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "identities":
        identities()
    else:
        lockstep(sys.argv[2], int(sys.argv[3]), json.loads(sys.argv[4]) if len(sys.argv) > 4 else None)
