"""Term 13, the frozen clock, measured on the edge (the Boss's code writer, writer A, 2026-10-30, the night's PLAN A3; the
fourth text of term 5, section 6, asks it, and NOT_CLOSED 7 takes it): on the well world as B2b re-laid it under the books'
form, a test clock at every Node-clock, its beat read at the lump's crests and in the void against the teeth W the act reads
there; whole numbers and Rule3's carry alone, the trains read off the world's files by their shapes, no train declared here.

Clock: a clock's beat goes as the root of its spring over its teeth, so N^2 = rest / W: a clock in a deeper 00 slot beats
slower, and it stops only where W grows without bound.
Algebra: the hand on its spring, W (a+ - 2 a + b) = -2 g a on the edge, beats at 4 sin^2(omega / 2) = 2 g / W, so its period
squared goes as W, the lattice's own departure at the second order -(g / 6) (W - rest) / (W rest) of N^2; N^2 = (T_rest / T)^2
from the zero crossings, each placed within its round by Rule3's carry, t = n + |a_n| / (|a_n| + |a_n+1|); rest / W from the
engine's own dial at the clock's row (step.dials), time's mean over the same rounds; every quotient by the carry.
Board: the well world's three files (examples/tensor24-well) through the loader and the engine's act at push 1; the crests
where the light's first part is largest in magnitude, the void where the light's rows are 0 at both slots; the test clock on
the one-row train that is no square (the pulse, whose own lay is left out): laid alike at every Node-clock at its turning
point, a = b = A, its own spring (g; x, x, 1, 1) on the value plan at g = rest div 100, its row's grip at rest 0 (a site-local
clock, as the held hand's rows are; the ii slots' read still lands on its Spokes and is stated), and every term of the push
that reads its row at the factor 0 (a test clock whose momenta and stretches the metric does not feel); the reference the
same files at push 0 with the metric's gears out, W = rest at every Node-clock.
Clicks: n/a: the beat is no click; the clicks would read it as proper time, a deeper clock counting fewer of its beats
between two of its clicks.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/frozen_edge/probe.py; its output is probe.txt beside it.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT.joinpath("src")))

from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import contract, step  # noqa: E402
from tensor24.engine.state import Plan, State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

HERE = Path(__file__).resolve().parent
WORLD = ROOT.joinpath("examples", "tensor24-well")
SPRING = 100  # the clock's spring g = rest div SPRING: 2 g / W about 1 / 50, a beat of about 44 rounds at rest
SWINGS = (10**12, 10)  # the clock's swing: strides far above a notch, and about one count a round (G2's term 13, item 1)
ROUNDS = 300  # about seven beats
FINE = 10**9  # a crossing placed within its round in billionths
PARTS = 10**8  # N^2 = 1 in hundredths of a part per million


def files():
    """The world's three files, read by their paths."""
    universe = json.loads(WORLD.joinpath("universe.json").read_text(encoding="utf-8"))
    shape = json.loads(WORLD.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    setting = json.loads(WORLD.joinpath("setting.json").read_text(encoding="utf-8"))
    return universe, shape, setting


def world(universe, shape, gears):
    """The files loaded on the engine: the held trains, the layout and the state; no departure of the lay."""
    made = main.made(loading.star(len(shape)))
    held, laid = loading.load(universe, {"version": 1, "gears": gears}, sites_of(shape), *made)
    assert not laid, laid
    return held, main.layout(universe, shape, held), State(*held.state)


def trains_of(held):
    """The light (two rows, no square), the square and the one-row train that is no square, by their shapes alone."""
    trains = held.trains
    square = [t for t in range(len(trains)) if trains[t].square]
    light = [t for t in range(len(trains)) if not trains[t].square and trains[t].rows() == 2]
    one = [t for t in range(len(trains)) if not trains[t].square and trains[t].rows() == 1]
    (square,), (light,), (one,) = square, light, one
    return light, square, one


def clocked(layout, rows, row, g):
    """The layout with the test clock on the row: its own spring (g; x, x, 1, 1) on the value plan, which pushes it by -2 g x,
    its grip at rest 0 on every Mesh, and every term of the push that reads one of its planes at the factor 0."""
    grip = layout.grip.copy()
    grip[row] = 0 * grip[row]
    leg = np.array([row], dtype=np.intp)
    spring = contract.pushes(np.array([g], dtype=object), (leg, leg, 0 * leg - 1, 0 * leg - 1))
    plan = Plan(*(np.concatenate((x, y), axis=-1) for x, y in zip(layout.plan, spring, strict=True)))
    _, one = carry(layout.push.legs[0].astype(object), rows, 0)
    _, two = carry(layout.push.legs[1].astype(object), rows, 0)
    deaf = [int(x != row and y != row) for x, y in zip(one.tolist(), two.tolist(), strict=True)]
    push = layout.push._replace(factor=layout.push.factor * np.array(deaf, dtype=object))
    return layout._replace(grip=grip, plan=plan, push=push)


def run(layout, s, row, base, rounds):
    """The rounds on the engine's act: per Node-clock the clock's zero crossings, the first, the last and their count, each
    placed within its round in billionths; per round the clock's teeth W as the act reads them and the 00 slot; the clock's
    largest stride, and the least and the most grip its Spokes hold (the ii slots' read)."""
    sites = s.a.shape[1]
    first, last, count = [None] * sites, [None] * sites, [0] * sites
    teeth, slot, stride, grips = [], [], 0, []
    before = s.a[row].tolist()
    for n in range(rounds):
        s = step.tick(layout, s)
        now = s.a[row].tolist()
        for x in range(sites):
            p, c = before[x], now[x]
            if (p > 0 and c <= 0) or (p < 0 and c >= 0):
                q, _ = carry(abs(p) * FINE, abs(p) + abs(c), 0)
                first[x] = n * FINE + q if first[x] is None else first[x]
                last[x], count[x] = n * FINE + q, count[x] + 1
        wa, _ = step.dials(layout, s)
        teeth.append(wa[row].tolist())
        slot.append(s.a[base].tolist())
        stride = max(stride, max(abs(v) for v in (s.a[row] - s.b[row]).tolist()))
        held = step.grips(layout, s)[row]
        grips.extend((int(held.min()), int(held.max())))
        before = now
    return first, last, count, teeth, slot, stride, (min(grips), max(grips))


def window(first, last, x, series):
    """The sum of a series over the rounds of the clock's window at a Node-clock, its first crossing's round to its last's, and
    the rounds."""
    lo, _ = carry(first[x], FINE, 0)
    hi, _ = carry(last[x], FINE, 0)
    values = [series[r][x] for r in range(lo, hi + 1)]
    return sum(values), len(values)


def decimal(value, places):
    """A whole count in units of 10^-places, written with its point: whole numbers alone."""
    sign, value = ("-" if value < 0 else ""), abs(value)
    whole, part = carry(value, 10**places, 0)
    return f"{sign}{whole}.{str(part).rjust(places, '0')}"


def measured(universe, shape, setting, swing, say):
    """The clock at one swing: the reference at W = rest, then the well world at push 1; N^2 by the beat against rest / W."""
    held, _, _ = world(universe, shape, [])
    light, square, one = trains_of(held)
    row, base = int(held.trains.first[one]), int(held.trains.first[square])
    rows, sites = int(held.trains.size.sum()), sites_of(shape)
    hand = [[one, 0, x, swing, swing, 0] for x in range(sites)]
    world_gears = [g for g in setting["gears"] if g[0] != one]
    flat = json.loads(json.dumps(universe))
    flat["chosen"]["push"] = 0
    runs = {}
    for name, u, gears in (
        ("rest", flat, [g for g in world_gears if g[0] != square] + hand),
        ("well", universe, world_gears + hand),
    ):
        held, layout, s = world(u, shape, gears)
        rest = int(layout.gearing.rest[0, 0])
        g, _ = carry(rest, SPRING, 0)
        runs[name] = run(clocked(layout, rows, row, g), s, row, base, ROUNDS)
    first, last, count, *_ = runs["rest"]
    halves = {(last[x] - first[x], count[x] - 1) for x in range(sites)}
    ((span, beats),) = halves  # the reference beats alike at every Node-clock
    half, _ = carry(span, beats, 0)
    say(
        f"  the swing {swing}: at W = rest (push 0, the metric's gears out) the clock's half beat {decimal(half, 9)} rounds,"
        f" over {beats} half beats, alike at all {sites} Node-clocks"
    )
    first, last, count, teeth, slot, stride, (low, high) = runs["well"]
    a, b = held.state[:2]
    light_rows = range(int(held.trains.first[light]), int(held.trains.first[light]) + held.trains[light].rows())
    peak = max(abs(v) for v in a[light_rows[0]].tolist())
    classes = {
        "the crests": [x for x in range(sites) if abs(a[light_rows[0], x]) == peak],
        "the void": [x for x in range(sites) if not any(a[r, x] or b[r, x] for r in light_rows)],
        "every Node-clock": list(range(sites)),
    }
    means = {}
    for name, xs in classes.items():
        n2, rw, ratio, own, c00 = [], [], [], [], []
        for x in xs:
            w, n = window(first, last, x, teeth)
            c, _ = window(first, last, x, slot)
            num, den = (span * (count[x] - 1)) ** 2, (beats * (last[x] - first[x])) ** 2
            n2.append(carry(PARTS * num, den, 0)[0])
            rw.append(carry(PARTS * rest * n, w, 0)[0])
            ratio.append(carry(PARTS * num * w, den * rest * n, 0)[0])
            own.append(-carry(PARTS * g * (w - rest * n), 6 * w * rest, 0)[0])
            c00.append(carry(c, n, 0)[0])
        mean = [carry(sum(v), len(v), 0)[0] for v in (n2, rw, ratio, own, c00)]
        means[name] = mean
        say(
            f"    {name} ({len(xs)}): the 00 slot {mean[4]} in time's mean; rest / W {decimal(mean[1], 2)} ppm; N^2 by the beat"
            f" {decimal(mean[0], 2)} ppm (least {decimal(min(n2), 2)}, most {decimal(max(n2), 2)}); N^2 / (rest / W) less 1"
            f" {decimal(mean[2] - PARTS, 2)} ppm (least"
            f" {decimal(min(ratio) - PARTS, 2)}, most {decimal(max(ratio) - PARTS, 2)}), the lattice oscillator's own"
            f" second order -(g / 6) (W - rest) / (W rest) {decimal(mean[3], 2)} ppm"
        )
    crest, void = means["the crests"], means["the void"]
    say(
        f"    the crests against the void: N^2 by the beat {decimal(carry(PARTS * crest[0], void[0], 0)[0], 2)} ppm, W_void / W_crest"
        f" {decimal(carry(PARTS * crest[1], void[1], 0)[0], 2)} ppm; the clock's largest stride {stride} counts a round; the"
        f" grips its Spokes hold, the ii slots' read, {low} to {high} against its spring 2 g = {2 * g}"
    )


def main_():
    out = []

    def say(line):
        print(line, flush=True)
        out.append(line)

    universe, shape, setting = files()
    held, layout, _ = world(universe, shape, setting["gears"])
    say(
        f"term 13 on the edge: the well world {shape} at push {universe['chosen']['push']} and notch {universe['chosen']['notch']},"
        f" the rest teeth {int(layout.gearing.rest[0, 0])}, the clock's read k0 = {int(layout.clock.factor.max())}; the test"
        f" clock at every Node-clock on its own spring g = rest div {SPRING}, Mesh-less and read by no push, {ROUNDS} rounds"
    )
    for swing in SWINGS:
        measured(universe, shape, setting, swing, say)
    HERE.joinpath("probe.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main_()
