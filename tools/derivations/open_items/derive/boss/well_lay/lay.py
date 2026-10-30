"""The well world's lay, examples/tensor24-well/setting.json, in whole numbers by the lattice's own modes and the act
itself (the Boss's code writer, 2026-10-30): no float, no circular function, no root, no rounding; Rule3's carry the
one division; the universe and the piece read from their files, no train declared here.

Clock: the light's first part laid at rest (now = before, the tooth 0) on the ring's whole standing mode, the second
part the act's own state a quarter beat later (a, b and the edge's tooth), so that the two parts' squares,
momenta squared and gradients squared, summed, stand nearly still in time: a steady source for the metric; the metric's slots laid at the time's
mean of a first run from 0, so that the well stands rather than swinging about its rest (the Node-clock has no
damping).
Algebra: the ring's whole mode is the sequence whose second difference is minus itself, c(x + 1) = c(x) - c(x - 1)
from (2, 1): 2, 1, -1, -2, -1, 1, closing on a ring whose side is a multiple of 6 (the only whole modes of a ring
are this one, the one whose second difference is minus twice itself, 1, 0, -1, 0, the constant and the alternating
one); the board's mode f = c(x) + c(y) + c(z), the three axes alike, is an eigenvector of the board's pull, so it
stands; the quarter beat is read off the act as the count of rounds at which the crest's count has crossed 0.
Board: 18 by 6 by 6; the light's two parts at the amplitude 2000 f; a pulse of 500 along x, alike at every y and z,
its before slot one round back at about 20 / 49 Meshes a round; the metric's 00, xx, yy and zz slots at the mean of
the first run's last 64 rounds (Rule3's carry).
Clicks: n/a: the lay is written from outside; the setting's ticks 128.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/well_lay/lay.py; it writes the setting beside the
universe and the piece under examples/tensor24-well/, and lay.txt beside itself: the account of every lay number.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT.joinpath("src")))

from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

WORLD = ROOT.joinpath("examples", "tensor24-well")
AMPLITUDE = 2000  # the light's first part at rest: a = b = AMPLITUDE f
PULSE, HALF = 500, 4  # the pulse's peak and half-width
CENTRE = 9  # the pulse's centre along x
NUM, DEN = 20, 49  # the pulse's speed, about 20 / 49 Meshes a round, as the live world has it
TICKS = 128  # the setting's ticks, and the first run's rounds
WINDOW = 64  # the first run's last rounds, over which the metric's slots are averaged
SLOTS = (0, 4, 5, 6)  # the square train's components laid at their mean: 00, xx, yy, zz
PERIOD = 6  # the ring's whole mode closes on a side that is a multiple of 6


def mode(side):
    """The ring's whole standing mode, the second difference minus itself: 2, 1, -1, -2, -1, 1 around the ring."""
    _, left = carry(side, PERIOD, 0)
    assert left == 0, side
    values = [2, 1]
    for _ in range(side - 2):
        values.append(values[-1] - values[-2])
    assert values[-1] - values[-2] == values[0] and values[0] - values[-1] == values[1], (
        values
    )  # the ring closes
    return values


def site_of(shape, x, y, z):
    _, sy, sz = shape
    return (x * sy + y) * sz + z


def board(shape):
    """The board's mode f = c(x) + c(y) + c(z) at every site, the three axes alike."""
    sx, sy, sz = shape
    cx, cy, cz = mode(sx), mode(sy), mode(sz)
    f = {}
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                f[site_of(shape, x, y, z)] = cx[x] + cy[y] + cz[z]
    return f


def bump(x, sx):
    """The pulse along x, (HALF^2 - u^2)^2 scaled to the peak, u the distance from the centre around the ring."""
    _, u = carry(x - CENTRE + HALF, sx, 0)
    u = u - HALF
    inside = int(-HALF < u < HALF)
    q, _ = carry(PULSE * (HALF * HALF - u * u) ** 2, HALF**4, 0)
    return inside * q


def world(universe, shape, gears):
    """The loaded files on the engine: the held trains, the layout and the state; no departure of the lay."""
    sites = sites_of(shape)
    made = main.made(loading.star(len(shape)))
    held, laid = loading.load(universe, {"version": 1, "gears": gears}, sites, *made)
    assert not laid, laid
    return held, main.layout(universe, shape, held), State(*held.state)


def trains_of(held):
    """The light (two parts, no square), the square and the pulse (one part, no square) by their shapes alone."""
    square = [t for t in range(len(held.trains)) if held.trains[t].square]
    light = [
        t for t in range(len(held.trains)) if not held.trains[t].square and held.trains[t].rows() == 2
    ]
    pulse = [
        t for t in range(len(held.trains)) if not held.trains[t].square and held.trains[t].rows() == 1
    ]
    (square,), (light,), (pulse,) = square, light, pulse
    return light, square, pulse


def lay():
    out = []

    def say(line):
        print(line)
        out.append(line)

    universe = json.loads(WORLD.joinpath("universe.json").read_text(encoding="utf-8"))
    shape = json.loads(WORLD.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    sx, sy, sz = shape
    sites = sites_of(shape)
    f = board(shape)
    crest = site_of(shape, 0, 0, 0)
    say(
        f"the board {shape}, {sites} Node-clocks; the ring's whole mode along x: {mode(sx)}; f at the crest (0, 0, 0): {f[crest]}"
    )
    held, _, _ = world(universe, shape, [])
    light, square, pulse = trains_of(held)
    first = int(held.trains[light].first)
    # 1. the first part at rest on the mode: a = b = AMPLITUDE f, the tooth 0
    rest = [[light, 0, x, AMPLITUDE * f[x], AMPLITUDE * f[x], 0] for x in range(sites) if f[x]]
    say(
        f"1. the light's first part at rest on the mode, a = b = {AMPLITUDE} f, at {len(rest)} Node-clocks (f = 0 at the rest)"
    )
    # 2. the second part: the act alone, from the first part's lay, until the crest's count has crossed 0
    alone = json.loads(json.dumps(universe))
    alone["chosen"]["push"] = 0
    _, layout, s = world(alone, shape, rest)
    quarter, crests = 0, [int(s.a[first, crest])]
    while s.a[first, crest] > 0:
        s = step.tick(layout, s)
        quarter += 1
        crests.append(int(s.a[first, crest]))
    partner = [[light, 1, x, int(s.a[first, x]), int(s.b[first, x]), int(s.r[first, x])] for x in range(sites)]
    partner = [g for g in partner if g[3] or g[4] or g[5]]
    teeth = sorted({int(v) for v in s.r[first]})
    say(
        f"2. the act alone from that lay: the crest's count by round {crests}; the quarter beat {quarter} rounds;"
        f" the state then, a, b and the edge's tooth, is the second part's lay at {len(partner)} Node-clocks"
        f" (the state's teeth {teeth}, within the edge's dial, the run's promise)"
    )
    # 3. the pulse along x, alike at every y and z, its before one round back at about NUM / DEN Meshes a round
    moving = []
    for x in range(sx):
        now = bump(x, sx)
        before, _ = carry((DEN - NUM) * now + NUM * bump(x + 1, sx), DEN, 0)
        if now or before:
            moving.extend(
                [pulse, 0, site_of(shape, x, y, z), now, before, 0] for y in range(sy) for z in range(sz)
            )
    say(
        f"3. the pulse along x: now {[bump(x, sx) for x in range(sx)]}, its before (({DEN} - {NUM}) now + {NUM} next) div {DEN}; {len(moving)} Node-clocks"
    )
    # 4. the first run from 0 under the universe's push and notch: the metric's slots at the mean of the last rounds
    held, layout, s = world(universe, shape, rest + partner + moving)
    base = int(held.trains[square].first)
    sums = {c: [0] * sites for c in SLOTS}
    for r in range(1, TICKS + 1):
        s = step.tick(layout, s)
        if r > TICKS - WINDOW:
            for c in SLOTS:
                row = s.a[base + c]
                sums[c] = [sums[c][x] + int(row[x]) for x in range(sites)]
    means = {c: [carry(sums[c][x], WINDOW, 0)[0] for x in range(sites)] for c in SLOTS}
    well = [
        [square, c, x, means[c][x], means[c][x], 0] for c in SLOTS for x in range(sites) if means[c][x]
    ]
    say(
        f"4. the first run from 0, {TICKS} rounds at push {universe['chosen']['push']} and notch {universe['chosen']['notch']}:"
        f" the metric's components {SLOTS} at the mean of rounds {TICKS - WINDOW + 1}..{TICKS} (Rule3's carry),"
        f" the 00 slot's mean {means[0][crest]} at the crest and {min(means[0])}..{max(means[0])} over the board; {len(well)} Node-clocks"
    )
    gears = rest + partner + moving + well
    WORLD.joinpath("setting.json").write_text(
        '{"version": 1, "ticks": '
        + str(TICKS)
        + ', "gears": [\n'
        + ",\n".join("  " + json.dumps(g) for g in gears)
        + "\n]}\n",
        encoding="utf-8",
    )
    # 5. the account: the source's steadiness in the laid world, the parts' squares summed at the crest by windows
    held, layout, s = world(universe, shape, gears)
    squares, windows = [], []
    for _ in range(TICKS):
        s = step.tick(layout, s)
        squares.append(int(s.a[first, crest]) ** 2 + int(s.a[first + 1, crest]) ** 2)
        if len(squares) == 16:
            windows.append((min(squares), max(squares)))
            squares = []
    ratio = [carry(1000 * (hi - lo), hi + lo, 0)[0] for lo, hi in windows]
    say(
        f"5. the laid world, {TICKS} rounds: the parts' squares summed at the crest, least and most by windows of 16 rounds:"
        f" {windows}; (most - least) / (most + least) in permille: {ratio}"
    )
    say(f"the setting written: {len(gears)} gears, ticks {TICKS}")
    Path(__file__).with_name("lay.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    lay()
