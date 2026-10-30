"""The well world measured for examples/README.md (the Boss's code writer, 2026-10-30, the night's PLAN.md B2b): the laid
world run its ticks on the engine's own act, the same act the run tool turns, and the same files at push 0 with the metric
standing at 0 for the pulse's reference; whole numbers and Rule3's carry alone, the trains read off the files by their
shapes (lay.py's helpers), no train declared here.

Clock: the 00 slot's well and the ii slots' grips where the lump is, and the pulse slowed by the well.
Algebra: time's means over the second half of the rounds by Rule3's carry; W = rest + k0 c00, N^2 = rest / W in parts per
million; the pulse's centroid along x weighted by its counts squared, each site taken at its image nearest the last
round's centroid on the ring, in hundredths of a Mesh, and its bend in thousandths.
Board: the crests where the mode f = c(x) + c(y) + c(z) is 6 in magnitude (x, y and z all multiples of 6 or all 3
more), the void where f = 0; the pulse's rows through the crests where |c(y) + c(z)| = 4 and through the void where
c(y) + c(z) = 0.
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


def mean(values):
    q, _ = carry(sum(values), len(values), 0)
    return q


def per(num, den, unit):
    q, _ = carry(num * unit, den, 0)
    return q


def centroid(pulse, rows, shape, last):
    """The pulse's centroid along x in hundredths of a Mesh over the given (y, z) rows, weighted by its counts squared,
    each x at its image nearest the last centroid (hundredths) on the ring."""
    sx, _, _ = shape
    weight, moment = 0, 0
    for x in range(sx):
        w = sum(int(pulse[lay.site_of(shape, x, y, z)]) ** 2 for y, z in rows)
        k, _ = carry(last - 100 * x + 50 * sx, 100 * sx, 0)
        weight, moment = weight + w, moment + w * (100 * x + 100 * sx * k)
    q, _ = carry(moment, weight, 0)
    return q


def course(universe, shape, gears, rows_of, ticks):
    """The world run its ticks: per round the state, handed to the reader; the pulse's centroids by row set at every round."""
    held, layout, s = lay.world(universe, shape, gears)
    light, square, pulse = lay.trains_of(held)
    at = int(held.trains[pulse].first)
    last = {name: centroid(s.a[at], rows, shape, 0) for name, rows in rows_of.items()}
    tracks = {name: [] for name in rows_of}
    states = []
    for _ in range(ticks):
        s = step.tick(layout, s)
        for name, rows in rows_of.items():
            last[name] = centroid(s.a[at], rows, shape, last[name])
            tracks[name].append(last[name])
        states.append(s)
    return held, layout, states, tracks


def main_():
    out = []

    def say(line):
        print(line, flush=True)
        out.append(line)

    universe = json.loads(lay.WORLD.joinpath("universe.json").read_text(encoding="utf-8"))
    shape = json.loads(lay.WORLD.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    setting = json.loads(lay.WORLD.joinpath("setting.json").read_text(encoding="utf-8"))
    sx, sy, sz = shape
    f, cy, cz = lay.board(shape), lay.mode(sy), lay.mode(sz)
    crests = [x for x in f if f[x] * f[x] == 36]
    void = [x for x in f if not f[x]]
    every = [(y, z) for y in range(sy) for z in range(sz)]
    rows_of = {
        "all": every,
        "crests": [(y, z) for y, z in every if (cy[y] + cz[z]) ** 2 == 16],
        "void": [(y, z) for y, z in every if not cy[y] + cz[z]],
    }
    ticks = setting["ticks"]
    held, layout, states, tracks = course(universe, shape, setting["gears"], rows_of, ticks)
    light, square, pulse = lay.trains_of(held)
    base, rest = int(held.trains[square].first), int(layout.gearing.rest[0, 0])
    k0 = int(layout.clock.factor.max())
    half = states[ticks - lay.WINDOW :]
    c00 = [mean([int(s.a[base, x]) for s in half]) for x in range(len(f))]
    crest00, void00, board00 = mean([c00[x] for x in crests]), mean([c00[x] for x in void]), mean(c00)
    along = [c00[lay.site_of(shape, x, 0, 0)] for x in range(lay.PERIOD)]
    say(
        f"the well world {shape} at push {universe['chosen']['push']} and notch {universe['chosen']['notch']}, {ticks} rounds; the clock's read k0 = {k0},"
        f" the rest teeth {rest}; time's means over rounds {ticks - lay.WINDOW + 1}..{ticks}:"
    )
    say(
        f"1. the 00 slot: {crest00} at the {len(crests)} crests, {void00} at the {len(void)} sites of the void, the board's mean {board00};"
        f" W = rest + k0 c00, N^2 = rest / W {per(rest, rest + k0 * crest00, 10**6)} ppm at the crests and {per(rest, rest + k0 * void00, 10**6)}"
        f" in the void (10^6 at the loader's rest); along x through (y, z) = (0, 0): {along}"
    )
    ii = {name: base + 1 + len(shape) + i for i, name in enumerate(("xx", "yy", "zz"))}
    slots = {
        name: (mean([mean([int(s.a[r, x]) for s in half]) for x in crests]), mean([mean([int(s.a[r, x]) for s in half]) for x in void]))
        for name, r in ii.items()
    }
    end = states[-1]
    grip = int(layout.grip[0, 0])
    xs = [lay.site_of(shape, x, 0, 0) for x in range(sx)]
    after = [carry(x + 1, sx, 0)[1] for x in range(sx)]  # each x Mesh's far end, around the ring
    xgrips = [grip + int(end.a[ii["xx"], xs[x]]) + int(end.a[ii["xx"], xs[after[x]]]) for x in range(sx)]
    say(
        f"2. the ii slots (crests, void): {slots}; the x Meshes' grips g + c_xx + c_xx' through (y, z) = (0, 0) at the last round"
        f" {min(xgrips)} to {max(xgrips)} of {grip}"
    )
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
        strides[name] = max(int(abs(s.a[first : first + rows] - s.b[first : first + rows]).max()) for s in states)
    say(f"4. the largest stride a round over the run, by train: {strides} (the 00 push resolves none below half a count a round)")
    # the pulse's reference: the same files at push 0, the metric standing at 0 (its gears taken out)
    flat = json.loads(json.dumps(universe))
    flat["chosen"]["push"] = 0
    bare = [g for g in setting["gears"] if g[0] != square]
    _, _, _, still = course(flat, shape, bare, rows_of, ticks)
    moved, ref = tracks["all"][-1] - tracks["all"][0], still["all"][-1] - still["all"][0]
    bend = (tracks["crests"][-1] - tracks["void"][-1]) - (still["crests"][-1] - still["void"][-1])
    say(
        f"5. the pulse's centroid along x over the {ticks - 1} rounds from the first, in hundredths of a Mesh: {moved} at push"
        f" {universe['chosen']['push']} against {ref} at push 0 with the metric at 0, a lag of {ref - moved}; the bend between its rows through"
        f" the crests and through the void at the last round, less the same at push 0, {bend} hundredths"
    )
    HERE.joinpath("measure.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main_()
