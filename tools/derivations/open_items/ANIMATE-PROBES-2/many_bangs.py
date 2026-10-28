"""Animate's probe of the many bangs from the clocks (the owner's word of 2026-10-28, 12:1x UTC: "derive it yourself,
through the logic of the clocks and the tensors"). Built on draft C's harness (course.py) and drives (drives.py): the
one big bang world (tests/worlds/world_bang.json on universe_bang.json) with draft C's derived push (vol0: general
relativity's A1 volume equation in the head's gauge, no typed form, no clamp), run on a source tree.

Variants (each changes one thing, named; everything else is the tree's own):
  base      draft C's vol0 as built: law 4's two triggers (the top and the floor X_f), BH-S1's restore of every gear
            at a stopped Node-clock
  nofloor   law 4's floor clause struck: the turnover only at the time gear's weak maximum
  weakmin   notick, with law 4's bottom as the top's mirror, the time gear's weak minimum (X0 >= X1 <= X2, one
            strict), in place of the floor (the Boss's candidate, #2187 6468487676)
  fallmin   weakmin with the bottom entered from above only (X0 > X1 <= X2)
  carry     law 11 at the time gear: the turnover is the event of the horizon's dial, the load's whole turn at the
            stopped load L_c (Rule3's own zero of the Mesh rate), read at the tick's start as the quotient
            load div L_c; no weak maximum, no floor, and BH-S1 struck everywhere (no restore, no mask on the Mesh
            factors, on the dial or on the click)
  carry_nof2  carry, with the Mesh factor read from the tension unclipped (the bound F2 struck)
  notick    nofloor, and BH-S1's restore struck: no gear of a stopped clock is restored; law 4 reads the time gear
            of a clock with no tick (mesh rate 0 at the tick's start) as held, X2 = X1 (the clock has no tick on the
            board, the owner's asynchronous board), and nothing else
Readings, per tick and per bang (a bang is the course from one bottom at rest to the next):
  the stretch X (least and largest over the board), the whole-board turnovers, the local turnovers, the floor's
  firings, the births, the books per click phase, the state hash per bottom (is any bottom's state a repeat of an
  earlier one?), the retrace (after each top, X at top + k against X at top - 2 - k), the rewind (n ticks forward
  and n back from a tick, the state bit for bit).
The audit, on every variant: how often each bound the engine still holds changes a value in the run (a load below 0
read at 0; a tension below 0 or above Gamma read at the edge; a Mesh factor zeroed by a stopped end; the dial held at
a stopped clock; the end teeth's fallback; the draw's room capped at the modulus; the coupling min(spring, 1)).
Usage: python -I many_bangs.py <root> <variant> <quanta> <ticks> [<rewind n> <rewind from> ...]
"""

import hashlib
import json
import os
import sys
import time

root, variant, quanta, ticks = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
rewinds = [(int(sys.argv[i]), int(sys.argv[i + 1])) for i in range(5, len(sys.argv) - 1, 2)]
here = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path[:0] = [root + "/src", root, here]

import drives  # noqa: E402
import numpy as np  # noqa: E402

from event_universe import click, hands, readings  # noqa: E402
from event_universe import clock as C  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.features import stretch as stretch_feature  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
from tests.laws import run_back_exact, state_of, world_of  # noqa: E402

FIRED = {"floor": 0}
from event_universe.core.rates import stopped_load as rates_stopped_load  # noqa: E402


def turnover_law4(self, held, going=1, top=None):
    """clock.turnover with the variant's trigger: the weak maximum alone (nofloor), and for notick the time gear of a
    clock with no tick read as held. Backward exactly the tree's."""
    if going == -1:
        if top.any():
            self.reverse(top, held)
        return top
    k = self.trains_.index(self.train(REGULATOR))
    x0, x1, x2 = held[k][0].before, held[k][0].now, self.train(REGULATOR).gears[0].now
    if variant in ("notick", "weakmin", "fallmin"):
        no_tick = readings.stopped_of(self, stretch_feature.load_of(self.full_rate, x1))
        x2 = np.where(no_tick, x1, x2)
    if variant in ("carry", "carry_nof2"):
        horizon = rates_stopped_load(self.full_rate)
        turns = np.asarray(stretch_feature.load_of(self.full_rate, x1), dtype=object) // horizon
        top = turns >= 1
        self.turned_over = top
        if top.any():
            self.counts["turns"] += int(top.sum())
            self.turnovers.append((self.ticks, int(top.sum())))
            self.reverse(top, held)
        return top
    xf = readings.bottom(self)
    floor = (x0 < xf) | (x2 < xf)
    FIRED["floor"] += int(floor.sum())
    top = (x0 <= x1) & (x2 <= x1) & ((x0 < x1) | (x2 < x1))
    if variant == "base":
        top = top | floor
    if variant in ("weakmin", "fallmin"):
        bottom = (x0 >= x1) & (x2 >= x1) & ((x0 > x1) | (x2 > x1))
        if variant == "fallmin":
            bottom = (x0 > x1) & (x2 >= x1)
        FIRED["weakmin"] = FIRED.get("weakmin", 0) + int(bottom.sum())
        top = top | bottom
    self.turned_over = top
    if top.any():
        self.counts["turns"] += int(top.sum())
        self.turnovers.append((self.ticks, int(top.sum())))
        self.reverse(top, held)
    return top


drives.install(T, "vol0")
C.Clock.turnover = turnover_law4

AUDIT = {
    "load below 0 read at 0": 0,
    "tension below 0 read at 0": 0,
    "tension above Gamma read at Gamma": 0,
    "Mesh factor zeroed by a stopped end": 0,
    "dial held at a stopped clock": 0,
    "end teeth's fallback": 0,
    "draw's room capped at the modulus": 0,
}
from event_universe import draw as D  # noqa: E402
from event_universe import meshes as M  # noqa: E402
from event_universe.core.rule3 import carries as carries_act  # noqa: E402
from event_universe.core.spokes import SPOKE_SIDES  # noqa: E402

_rates_of = readings.rates_of


def rates_of_audited(clock, c):
    AUDIT["load below 0 read at 0"] += int((np.asarray(c, dtype=object) < 0).sum())
    return _rates_of(clock, c)


readings.rates_of = rates_of_audited
_factors = M.factors


def factors_audited(clock, axis_notches=None, stopped=None):
    notches = (
        [gear.now for gear in clock.train(REGULATOR).gears[1:4]]
        if axis_notches is None
        else axis_notches
    )
    for spoke, (axis, _side) in enumerate(SPOKE_SIDES):
        t = carries_act(M.even(notches[axis], spoke) + 1, M.SIDES)
        AUDIT["tension below 0 read at 0"] += int((np.asarray(t) < 0).sum())
        AUDIT["tension above Gamma read at Gamma"] += int((np.asarray(t) > clock.full_rate).sum())
    if variant in ("carry", "carry_nof2"):
        stopped = None
    if variant == "carry_nof2":
        found = []
        for spoke, (axis, _side) in enumerate(SPOKE_SIDES):
            t = carries_act(M.even(notches[axis], spoke) + 1, M.SIDES)
            found.append(M.mesh_factor(clock.full_rate, clock.G, t))
        return tuple(found)
    found = _factors(clock, axis_notches, stopped)
    if stopped is not None and np.asarray(stopped).any():
        free = _factors(clock, axis_notches, None)
        AUDIT["Mesh factor zeroed by a stopped end"] += sum(
            int((np.asarray(a) != np.asarray(b)).sum()) for a, b in zip(found, free, strict=True)
        )
    return found


M.factors = factors_audited
T.factors = factors_audited
_end_teeth = T.Tick.end_teeth


def end_teeth_audited(self, time_gear):
    w = readings.mean_teeth(self.clock, time_gear)
    AUDIT["end teeth's fallback"] += int((np.asarray(w) <= 0).sum())
    return _end_teeth(self, time_gear)


T.Tick.end_teeth = end_teeth_audited


def min_audited(a, b, *rest):
    if not rest and a > b:
        AUDIT["draw's room capped at the modulus"] += 1
    return min(a, b, *rest)


D.min = min_audited
_rate_readings = T.Tick.rate_readings


def rate_readings_audited(self):
    _rate_readings(self)
    if variant in ("carry", "carry_nof2"):
        self.clock.dial = self.clock.dial + self.going * np.where(self.stopped, self.rate, 0)
        self.stopped = np.zeros(self.clock.size, dtype=bool)
        self.still = self.top | self.stopped
    else:
        AUDIT["dial held at a stopped clock"] += int(np.asarray(self.stopped).sum())


T.Tick.rate_readings = rate_readings_audited
if variant in ("carry", "carry_nof2"):
    from event_universe import click as K  # noqa: E402

    _stopped_of = readings.stopped_of
    K.readings = type("R", (), {})()
    for name in dir(readings):
        if not name.startswith("__"):
            setattr(K.readings, name, getattr(readings, name))
    K.readings.stopped_of = lambda clock, c: np.zeros(clock.size, dtype=bool)
    drives.NO_RESTORE.add("vol0")
if variant in ("notick", "weakmin", "fallmin"):
    drives.NO_RESTORE.add("vol0")

calibre, piece = world_of("world_bang.json")
piece = json.loads(json.dumps(piece))
piece["seed"][0]["quanta"] = quanta

books = []
clicked = click.click


def board(clock):
    reads = [readings.gearing_of(clock, r, clock.start_load, clock.start_factors) for r in clock.hands()]
    return sum(
        int(hands.wind(clock, r.gears, g).sum()) for r, g in zip(clock.hands(), reads, strict=True)
    )


def booked(clock, starts, held, going=1, note=None):
    if going != 1:
        return clicked(clock, starts, held, going, note)
    wind, slack, log_from = board(clock), int(clock.slack.sum()), len(clock.log)
    clicked(clock, starts, held, going, note)
    new = clock.log[log_from:]
    chimes = sum(int(e["booked"]) for e in new if e["event"] == "credit")
    after = board(clock)
    books.append(wind - after == chimes + int(clock.slack.sum()) - slack)


def make_clock():
    found = Clock(calibre, piece)
    if hasattr(drives, "PREPARE") and "vol0" in drives.PREPARE:
        drives.PREPARE["vol0"](found)
    return found


def short(clock):
    return hashlib.sha256(state_of(clock).encode()).hexdigest()[:16]


def short_without_dial(clock):
    """The state's hash with the dial (the count of each clock's own rate, a reading of its proper time) left out."""
    from event_universe import run as R

    arrays = [a for a in R.state(clock) if a is not clock.dial]
    text = " ".join(str(int(v)) for a in arrays for v in a.reshape(-1))
    return hashlib.sha256(text.encode()).hexdigest()[:16]


click.click = booked
t0 = time.time()
clock = make_clock()
size = int(np.prod(clock.size))
gear = clock.train(REGULATOR).gears[0]
X_seed = int(gear.now.min())
rows = []  # (tick, X least, X largest, turned, births so far, stopped clocks at the start)
whole, local = [], 0
near = {
    0: short(clock)
}  # the state hash at every tick whose largest X is within 20 seeds of the seed's stretch
refused = None
for at in range(1, ticks + 1):
    try:
        g = clock.train(REGULATOR).gears[0]
        stopped = readings.stopped_of(clock, stretch_feature.load_of(clock.full_rate, g.now))
        clock.tick()
        X = clock.train(REGULATOR).gears[0].now
        turned = int(clock.turned_over.sum())
        if turned == size:
            whole.append(at)
        elif turned:
            local += turned
        rows.append((at, int(X.min()), int(X.max()), turned, clock.counts["births"], int(stopped.sum())))
        if int(X.max()) <= 20 * X_seed:
            near[at] = short(clock)

    except ValueError as err:
        refused = (at, str(err))
        break
print(f"variant {variant}  quanta {quanta}  ticks {ticks}  board {size} Node-clocks")
print("tick: X least..largest [turned over] births stopped-at-start")
for at, lo, hi, turned, b, st in rows:
    print(
        f"  {at}: {lo}..{hi}"
        + (f" [{turned}]" if turned else "")
        + f"  b{b}"
        + (f" s{st}" if st else "")
    )
if refused:
    print(f"refused by name at tick {refused[0]}: {refused[1]}")
    ticks = refused[0] - 1
print(f"whole-board turnovers (tops): {len(whole)} at ticks {whole}")
print(f"local turnovers: {local}; the floor's trigger true at {FIRED['floor']} Node-clock ticks")
if "weakmin" in FIRED:
    print(f"the weak minimum's trigger true at {FIRED['weakmin']} Node-clock ticks")
print(f"births: {clock.counts['births']}; books closed at {sum(books)} of {len(books)} click phases")
X_at = {0: X_seed}
X_at.update({at: hi for at, _lo, hi, *_ in rows})
# a bottom: the first tick of a weak minimum of the largest X (it fell into it and does not fall after it)
bottoms = [(0, near[0])]
for at in range(1, ticks):
    if X_at[at - 1] > X_at[at] <= X_at[at + 1]:
        bottoms.append((at, near.get(at, "far")))
print("bottoms (tick, largest X, state hash):", [(b, X_at[b], h) for b, h in bottoms])
hashes = [h for _, h in bottoms]
print(f"distinct bottom states: {len(set(hashes))} of {len(hashes)}")
# the retrace after each top: X at top + k against X at top - 1 - k, k = 0, 1, ...
# the turnover at the top's tick ends it at the start state exchanged, so the run back reads X at top + k equal to
# X at top - 2 - k; counted until the first difference or the run's end
for top in whole:
    k = 0
    while top + k in X_at and top - 2 - k in X_at and X_at[top + k] == X_at[top - 2 - k]:
        k += 1
    end = (
        "the run's end"
        if top + k not in X_at
        else f"tick {top + k}: {X_at[top + k]} against {X_at.get(top - 2 - k)}"
    )
    print(f"  top {top}: X at top + k equals X at top - 2 - k for {k} ticks; first difference at {end}")
births_seen = 0
for at, _lo, hi, _t, b, _s in rows:
    if b != births_seen:
        print(f"  births at tick {at}: +{b - births_seen} (X {hi})")
        births_seen = b
# per bang: from one bottom to the next, its top, its births, its largest X
edges = [b for b, _ in bottoms] + [ticks]
births_at = {0: 0}
births_at.update({at: b for at, _lo, _hi, _t, b, _s in rows})
print("bangs (from a bottom to the next): start, end, top tick, largest X, births in it")
for s, e in zip(edges, edges[1:], strict=False):
    tops_in = [t for t in whole if s < t <= e]
    largest = max(X_at[t] for t in range(s, e + 1))
    print(f"  {s}..{e}: top {tops_in}, largest X {largest}, births {births_at[e] - births_at[s]}")
print("the bounds the engine still holds, values each changed in the run:")
for name, n in AUDIT.items():
    print(f"  {name}: {n}")
springs = [r.spring for r in clock.hands() if r.spring is not None]
print(
    f"  the coupling min(spring, 1): the hands' springs {sorted(set(springs))} (a cap acts where a spring passes 1)"
)
print("state hash", short(clock), "| without the dial", short_without_dial(clock))
click.click = clicked
for n, frm in rewinds:
    start = make_clock()
    for _ in range(frm):
        start.tick()
    print(f"rewind from tick {frm}: {run_back_exact(start, n)} of {n}")
print(f"seconds {time.time() - t0:.1f}")
