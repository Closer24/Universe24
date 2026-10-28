"""F7 (head): the one big bang on the head's engine, read for a dark part (draft F; root VI, the owner's
question of 2026-10-28, 13:1x UTC: "Is there a solution for what dark matter is? In fact it does not click").

Read-only on the t24 worktree: its src is imported and nothing in it is changed. The harness wraps the
head's tick.Tick.impulse: before the head's own impulse runs, a line-for-line copy of its loop computes the
regulator's source, the forms, train by train (the gravitating wind), on copies and with no write; after the
head's impulse it asserts that the trains' forms sum to the head's own forms at every Node-clock (the split's
second reading, so it can fail). The click record gives, train by train, the clicks. Integers only.

Usage: python3 -I F7_dark_head.py QUANTA TICKS
"""

import sys

T24 = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/t24"
sys.path[:0] = [T24 + "/src", T24]

import json  # noqa: E402

from tests.laws import world_of  # noqa: E402
from event_universe import hands, readings  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.core import rates  # noqa: E402
from event_universe.core.acts import carry, mid  # noqa: E402
from event_universe.core.rule3 import carries  # noqa: E402
from event_universe.meshes import coupling_of, cross  # noqa: E402
from event_universe.trains import REGULATOR, zeros  # noqa: E402

quanta, ticks = int(sys.argv[1]), int(sys.argv[2])
calibre, piece = world_of("world_bang.json")
piece = json.loads(json.dumps(piece))
piece["seed"][0]["quanta"] = quanta

SPLIT = []  # per tick: {train index: forms summed over the board}, and the held field's least and largest
CHECKS = []
original = T.Tick.impulse


def name_of(clock, r):
    k = clock.trains_.index(r)
    if r.weight is not None:
        return f"{k}: held field (one gear, weight {r.weight})"
    if r is clock.train(T.OFFSET):
        return f"{k}: offset (the potential)"
    kind = {1: "one gear", 2: "hand", 4: "twin hands"}.get(r.size, f"size {r.size}")
    if r.ratio is not None and r.ratio[0] == r.ratio[1]:
        return f"{k}: {kind} at (rim, rim), the light"
    return f"{k}: {kind}, spring {None if r.ratio is None else r.ratio[1] - r.ratio[0]}"


def split_impulse(self):
    clock = self.clock
    d = (clock.teeth + clock.teeth) * self.stretch_now
    w_side = readings.mean_teeth(self.clock, self.regulator.gears[0])
    sweep = zeros(clock.size)
    masses = zeros(clock.size)
    per = {}
    for r in self.driven:
        k = self.where[id(r)]
        p_side = [w_side * (gear.now - gear.before) + gear.fine - mid(w_side) for gear in self.trains[k]]
        p_other = [p + self.going * self.stretch_now * f for p, f in zip(p_side, self.pull[k], strict=True)]
        if r is self.offset:
            for a, (gear, n) in enumerate(zip(self.trains[k], [sweep, *self.lead], strict=True)):
                q, _ = carry(n, gear.dteeth, gear.dfine, self.going)
                p_other[a] = p_other[a] + self.going * clock.teeth * self.stretch_now * q
        if r.weight is not None:
            gear = self.trains[k][0]
            q, _ = carry(r.weight * masses, gear.dteeth, gear.dfine, self.going)
            p_other[0] = p_other[0] + self.going * clock.teeth * self.stretch_now * q
        u_in = [rates.rounded(p + p + 1, d) for p in p_side]
        u_out = [rates.rounded(p + p + 1, d) for p in p_other]
        if r in self.hands:
            velocity = [x + y for x, y in zip(u_in, u_out, strict=True)]
            sweep = sweep + coupling_of(r) * cross(*velocity, *self.starts[k])
        mass = self.train_spring[k] * hands.dot(self.starts[k], self.starts[k])
        masses = masses + carries(mass, self.train_teeth[k])
        pulls = hands.products(self.starts[k], self.pull[k])
        f = zeros(clock.size)
        for product, pull in zip(hands.products(u_in, u_out), pulls, strict=True):
            f = f + product + carries(-pull, self.train_teeth[k])
        per[k] = f
    original(self)
    if self.going == 1:
        total = zeros(clock.size)
        for f in per.values():
            total = total + f
        CHECKS.append(bool((total == self.forms).all()))
        row = {k: int(f.sum()) for k, f in per.items()}
        held = [k for k in per if clock.trains_[k].weight is not None]
        spread = {k: (int(per[k].min()), int(per[k].max())) for k in held}
        SPLIT.append((clock.ticks, row, spread))


T.Tick.impulse = split_impulse
clock = Clock(calibre, piece)
names = {k: name_of(clock, r) for k, r in enumerate(clock.trains_)}
size = 1
for n in clock.size:
    size *= n
events_before = len(clock.log)
bangs = []  # the ticks of whole-board turnovers
for _ in range(ticks):
    clock.tick()
    if int(clock.turned_over.sum()) == size:
        bangs.append(clock.ticks)
T.Tick.impulse = original

print(f"the one big bang, {quanta} quanta, {ticks} ticks, the head's engine (t24), the board {clock.size}")
print("trains:", "; ".join(names[k] for k in sorted(names)))
print(f"the split's second reading: the trains' forms sum to the head's forms at every Node-clock at {sum(CHECKS)} of {len(CHECKS)} ticks")
kinds = {}
named = {}
hand_index = [clock.trains_.index(r) for r in clock.hands()]
for e in clock.log[events_before:]:
    kinds[e["event"]] = kinds.get(e["event"], 0) + 1
    if e["event"] in ("birth", "credit"):
        for key in ("line_pair", "taken_row", "line"):
            if key in e:
                tr = hand_index[int(e[key])] if key != "line" else None
                named.setdefault(e["event"], {}).setdefault(key, set()).add(tr if tr is not None else int(e[key]))
print("click record, by event:", dict(sorted(kinds.items())))
print("the hands' train indices the clicks name (births: line_pair, taken_row; credits: the gear 'line' of a hand):",
      {k: {kk: sorted(vv) for kk, vv in v.items()} for k, v in named.items()})
print("births", clock.counts.get("births"), "chimes", clock.counts.get("body_clicks"), "; whole-board turnovers at", bangs[:12], "..." if len(bangs) > 12 else "")
never = [k for k in names if clock.trains_[k] not in clock.hands() and k in SPLIT[0][1]]
cum = {}
for t, row, spread in SPLIT:
    for k, v in row.items():
        cum[k] = cum.get(k, 0) + v
tot = sum(cum.values())
dark = sum(cum[k] for k in never)
print(f"the forms summed over every tick and Node-clock: total {tot}; the trains that never click ({', '.join(names[k] for k in never)}): {dark}")
edges = [0] + bangs + ([ticks] if not bangs or bangs[-1] != ticks else [])
for a, b in list(zip(edges, edges[1:]))[:8]:
    seg = [row for t, row, _ in SPLIT if a < t <= b]
    if seg:
        st = sum(sum(r.values()) for r in seg)
        sd = sum(sum(r[k] for k in never) for r in seg)
        print(f"  ticks {a + 1}..{b}: forms {st}, of which never clicking {sd}")
marks = sorted(set([1, 2, 5, 10, 20, 50, 100, 200, ticks]) & set(range(1, ticks + 1)))
print("tick: forms summed over the board, train by train [the held field's least..largest per Node-clock]")
for t, row, spread in SPLIT:
    if t in marks:
        tot = sum(row.values())
        parts = ", ".join(f"{names[k].split(':')[0]}={v}" for k, v in sorted(row.items()))
        print(f"  {t}: total {tot}; {parts}; held {spread}")
X = clock.train(REGULATOR).gears[0].now
print(f"stretch at the end: {int(X.min())}..{int(X.max())}")
