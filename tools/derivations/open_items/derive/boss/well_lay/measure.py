"""The well world measured for examples/README.md (the Boss's code writer, 2026-10-30, the night's PLAN.md B2b; read
again on 2026-10-31 on the lump at rest, which spreads): the laid world run its ticks on the engine's own act, the same
act the run tool turns, and the same files at push 0 with the metric standing at 0 for the pulse's reference; whole
numbers and Rule3's carry alone, the trains read off the files by their shapes (lay.py's helpers), no train declared
here. Every line is a board reading of a lump that spreads, not of a standing well.

Clock: the 00 slot where the lump is and where it is not, the ii slots, the 00 row's own cone, and the pulse through
the well.
Algebra: term 5's sign read from 0 (the metric's gears taken out): the 00 slot's mean over the lump's laid support
against the void's at the first rounds; time's means over the second half of the rounds by Rule3's carry; W = rest +
k0 c00, N^2 = rest / W in parts per million; the pulse's halves read as its squares' mean distance from its laid
centre around the ring, in hundredths of a Mesh, at push 1 against push 0.
Board: the lump's laid support where its count is not 0, its centre (0, 0, 0), the void where it is 0.
Clicks: n/a: no vertex is laid in the well world.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/well_lay/measure.py; its output is measure.txt beside it.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import lay  # noqa: E402

from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

SIGN = (1, 2, 4, 8, 16)  # the first rounds at which term 5's sign is read from 0


def mean(values):
    q, _ = carry(sum(values), len(values), 0)
    return q


def per(num, den, unit):
    q, _ = carry(num * unit, den, 0)
    return q


def apart(pulse, shape):
    """The pulse's squares' mean distance from its laid centre along x, around the ring within half its side, in
    hundredths of a Mesh: how far its two halves have run apart."""
    sx, sy, sz = shape
    weight, moment = 0, 0
    for x in range(sx):
        w = sum(int(pulse[lay.site_of(shape, x, y, z)]) ** 2 for y in range(sy) for z in range(sz))
        u = lay.away(x, lay.CENTRE, sx, carry(sx, 2, 0)[0])
        weight, moment = weight + w, moment + w * abs(u)
    return carry(100 * moment, weight, 0)[0]


def course(universe, shape, gears, ticks):
    """The world run its ticks: per round the state."""
    held, layout, s = lay.world(universe, shape, gears)
    states = [s]
    for _ in range(ticks):
        s = step.tick(layout, s)
        states.append(s)
    return held, layout, states


def main_():
    out = []

    def say(line):
        print(line, flush=True)
        out.append(line)

    universe = json.loads(lay.WORLD.joinpath("universe.json").read_text(encoding="utf-8"))
    shape = json.loads(lay.WORLD.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    setting = json.loads(lay.WORLD.joinpath("setting.json").read_text(encoding="utf-8"))
    sx, _, _ = shape
    f = lay.board(shape)
    support = [x for x in f if f[x]]
    void = [x for x in f if not f[x]]
    centre = lay.site_of(shape, *lay.LUMP)
    ticks = setting["ticks"]
    held, layout, states = course(universe, shape, setting["gears"], ticks)
    light, square, pulse = lay.trains_of(held)
    base, rest = int(held.trains[square].first), int(layout.gearing.rest[0, 0])
    k0 = int(layout.clock.factor.max())
    # 0. term 5's sign from 0: the same files with the metric's gears taken out
    bare = [g for g in setting["gears"] if g[0] != square]
    _, _, fresh = course(universe, shape, bare, SIGN[-1])
    marks = [(n, mean([int(fresh[n].a[base, x]) for x in support]), mean([int(fresh[n].a[base, x]) for x in void])) for n in SIGN]
    say(
        f"the well world {shape} at push {universe['chosen']['push']} and notch {universe['chosen']['notch']}, {ticks} rounds;"
        f" the clock's read k0 = {k0}, the rest teeth {rest}; the lump's laid support {len(support)} Node-clocks, the void {len(void)}"
    )
    say(
        f"0. term 5's sign, read from 0 with the metric's gears taken out: (round, the 00 slot's mean over the lump's laid"
        f" support, over the void): {marks} (the clock deeper where the lump's matter moves, before its waves spread it)"
    )
    half = states[ticks - lay.WINDOW + 1 :]
    c00 = [mean([int(s.a[base, x]) for s in half]) for x in range(len(f))]
    at, inside, outside = c00[centre], mean([c00[x] for x in support]), mean([c00[x] for x in void])
    along = [c00[lay.site_of(shape, x, 0, 0)] for x in range(sx)]
    say(
        f"1. the depth, time's means over rounds {ticks - lay.WINDOW + 1}..{ticks}: the 00 slot {at} at the lump's centre,"
        f" {inside} over its laid support, {outside} over the void, {min(c00)}..{max(c00)} over the board; N^2 = rest / W"
        f" {per(rest, rest + k0 * at, 10**6)} ppm at the centre and {per(rest, rest + k0 * outside, 10**6)} over the void"
        f" (10^6 at the loader's rest); along x through (y, z) = (0, 0): {along}"
    )
    ii = {name: base + 1 + len(shape) + i for i, name in enumerate(("xx", "yy", "zz"))}
    slots = {
        name: (mean([mean([int(s.a[r, x]) for s in half]) for x in support]), mean([mean([int(s.a[r, x]) for s in half]) for x in void]))
        for name, r in ii.items()
    }
    say(f"2. the ii slots (the lump's laid support, the void), time's means: {slots}")
    end = states[-1]
    wa, _ = step.dials(layout, end)
    others = [int(v) for r in range(wa.shape[0]) if r != base for v in wa[r].tolist()]
    say(
        f"3. the second cone: at the last round every other row's dial reads {min(others)} to {max(others)} where the 00 row's reads"
        f" {sorted(set(int(v) for v in wa[base].tolist()))}, W / rest {per(min(others), rest, 10**6)} to {per(max(others), rest, 10**6)} ppm"
    )
    groups = {"light": light, "the metric": square, "the pulse": pulse}
    strides = {}
    for name, t in groups.items():
        first, rows = int(held.trains[t].first), held.trains[t].rows()
        strides[name] = max(int(abs(s.a[first : first + rows] - s.b[first : first + rows]).max()) for s in states[1:])
    say(f"4. the largest stride a round over the run, by train: {strides} (the 00 push resolves none below half a count a round)")
    # the pulse's reference: the same files at push 0, the metric standing at 0 (its gears taken out)
    flat = json.loads(json.dumps(universe))
    flat["chosen"]["push"] = 0
    _, _, still = course(flat, shape, bare, ticks)
    first = int(held.trains[pulse].first)
    runs = [(n, apart(states[n].a[first], shape), apart(still[n].a[first], shape)) for n in range(0, ticks + 1, lay.SPAN)]
    say(
        f"5. the pulse through the well, laid at rest: its two halves run apart and meet again around the ring, (round, its"
        f" squares' mean distance from its laid centre in hundredths of a Mesh at push {universe['chosen']['push']}, the"
        f" same at push 0 with the metric at 0): {runs}"
    )
    HERE.joinpath("measure.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main_()
