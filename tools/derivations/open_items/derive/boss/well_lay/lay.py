"""The well world's lay, examples/tensor24-well/setting.json, in whole numbers by a polynomial lump and the act itself
(the Boss's code writer, 2026-10-30; laid again on 2026-10-31 with no mode of the ring, on both readings of main
b1a50bb33, #2187 6536864716): no float, no circular function and no construction that finds one, no root, no search,
no table, no rounding; Rule3's carry the one division; the universe and the piece read from their files, no train
declared here.

Clock: the first part of the board's wave laid at rest (now = before, the tooth 0) as one lump, the polynomial bump the pulse
already uses turned round its centre in the three axes, and its second part at 0; the lump spreads, as it is no
mode; the metric's slots laid at the time's mean of a first run from 0, so that the metric starts near the mean the
lump gives it and not at 0 (the Node-clock has no damping).
Algebra: the lump is PEAK (H^2 - r^2)^2 div H^4 where r^2 = u_x^2 + u_y^2 + u_z^2 is below H^2, u each axis's
distance from the lump's centre around its ring (Rule3's carry), and 0 elsewhere; it is no mode of the board's pull,
so the act moves it as it will, and the account reads what the act does with it, on the board.
Board: 18 by 6 by 6; the lump about (0, 0, 0), its peak 12000 and H 3; a pulse of 500 along x about x = 9, alike at
every y and z, at rest, its before slot its now, so that the act alone sets how it moves; the metric's 00, xx, yy and zz
slots, read from the shape, at the mean of the first run's last 64 rounds (Rule3's carry).
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
PEAK, H = 12000, 3  # the lump's peak at its centre and its half-width, so that it stands inside the board's 6 across
LUMP = (0, 0, 0)  # the lump's centre
PULSE, HALF = 500, 4  # the pulse's peak and half-width
CENTRE = 9  # the pulse's centre along x, the ring's far side from the lump
TICKS = 128  # the setting's ticks, and the first run's rounds
WINDOW = 64  # the first run's last rounds, over which the metric's slots are averaged
SPAN = 16  # the account's windows of rounds


def site_of(shape, x, y, z):
    _, sy, sz = shape
    return (x * sy + y) * sz + z


def away(v, centre, side, half):
    """v's distance from the centre around a ring of the side, within [-half, side - half), by Rule3's carry."""
    _, u = carry(v - centre + half, side, 0)
    return u - half


def reach(shape, x, y, z):
    """r^2, the squared distance of (x, y, z) from the lump's centre, each axis around its ring."""
    return sum(away(v, c, side, H) ** 2 for v, c, side in zip((x, y, z), LUMP, shape, strict=True))


def board(shape):
    """The lump at every site: PEAK (H^2 - r^2)^2 div H^4 where r^2 is below H^2, and 0 elsewhere."""
    sx, sy, sz = shape
    f = {}
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                r2 = reach(shape, x, y, z)
                q, _ = carry(PEAK * (H * H - r2) ** 2, H**4, 0)
                f[site_of(shape, x, y, z)] = int(r2 < H * H) * q
    return f


def bump(x, sx):
    """The pulse along x, (HALF^2 - u^2)^2 scaled to the peak, u the distance from the centre around the ring."""
    _, u = carry(x - CENTRE + HALF, sx, 0)
    u = u - HALF
    inside = int(-HALF < u < HALF)
    q, _ = carry(PULSE * (HALF * HALF - u * u) ** 2, HALF**4, 0)
    return inside * q


def sigma(layout, s):
    """Every gear's momentum in whole turns of the rest dial, as the stress reads sigma_in: the centred split of
    M = 2 (W(a) + W(b)) (a - b) + s at the dial 4 rest (step.split at 2 rest and the senses)."""
    wa, wb = step.dials(layout, s)
    senses = step.halves(layout)
    q, _ = step.split(senses * (wa + wb) * (s.a - s.b) + s.r, senses * layout.gearing.rest, senses)
    return q


def world(universe, shape, gears):
    """The loaded files on the engine: the held trains, the layout and the state; no departure of the lay."""
    sites = sites_of(shape)
    made = main.made(loading.star(len(shape)))
    held, laid = loading.load(universe, {"version": 1, "gears": gears}, sites, *made)
    assert not laid, laid
    return held, main.layout(universe, shape, held), State(*held.state)


def trains_of(held):
    """The board's wave (two parts, no square), the square and the pulse (one part, no square) by their shapes alone."""
    square = [t for t in range(len(held.trains)) if held.trains[t].square]
    light = [
        t for t in range(len(held.trains)) if not held.trains[t].square and held.trains[t].rows() == 2
    ]
    pulse = [
        t for t in range(len(held.trains)) if not held.trains[t].square and held.trains[t].rows() == 1
    ]
    (square,), (light,), (pulse,) = square, light, pulse
    return light, square, pulse


def spread(shape, row, weights):
    """A part's squares read on the board: their sum, the permille of them within the lump's laid support, their mean r^2
    from the lump's centre in hundredths (each axis around its ring, within half its side), and the permille of those on
    the lump's +x side among those on its two sides (500 where it moves neither way; the planes through the centre and its
    far side apart)."""
    sx, sy, sz = shape
    total, inside, moment, plus, minus = 0, 0, 0, 0, 0
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                w = int(row[site_of(shape, x, y, z)]) ** 2
                u = [away(v, c, side, carry(side, 2, 0)[0]) for v, c, side in zip((x, y, z), LUMP, shape, strict=True)]
                far = -carry(sx, 2, 0)[0]
                total += w
                inside += w * int(weights[site_of(shape, x, y, z)] != 0)
                moment += w * sum(v * v for v in u)
                plus += w * int(u[0] > 0)
                minus += w * int(far < u[0] < 0)
    return (
        total,
        carry(1000 * inside, total, 0)[0],
        carry(100 * moment, total, 0)[0],
        carry(1000 * plus, plus + minus, 0)[0],
    )


def lay():
    out = []

    def say(line):
        print(line, flush=True)
        out.append(line)

    universe = json.loads(WORLD.joinpath("universe.json").read_text(encoding="utf-8"))
    shape = json.loads(WORLD.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    sx, sy, sz = shape
    sites = sites_of(shape)
    slots = (0, *(1 + len(shape) + i for i in range(len(shape))))  # the square's 00 and ii slots, read from the shape
    f = board(shape)
    centre = site_of(shape, *LUMP)
    by_reach = sorted({(reach(shape, x, y, z), f[site_of(shape, x, y, z)]) for x in range(sx) for y in range(sy) for z in range(sz) if f[site_of(shape, x, y, z)]})
    say(
        f"the board {shape}, {sites} Node-clocks; the lump {PEAK} (H^2 - r^2)^2 div H^4 at H = {H} about {LUMP}, by r^2:"
        f" {by_reach}"
    )
    held, _, _ = world(universe, shape, [])
    light, square, pulse = trains_of(held)
    first = int(held.trains[light].first)
    # 1. the first part of the board's wave at rest on the lump: a = b, the tooth 0; its second part at 0
    rest = [[light, 0, x, f[x], f[x], 0] for x in range(sites) if f[x]]
    say(
        f"1. the first part of the board's wave at rest on the lump, a = b and the tooth 0, at {len(rest)} Node-clocks; its second part at 0"
    )
    # 2. the pulse along x, alike at every y and z, at rest: its before its now
    still = []
    for x in range(sx):
        now = bump(x, sx)
        still.extend([pulse, 0, site_of(shape, x, y, z), now, now, 0] for y in range(sy) for z in range(sz) if now)
    say(
        f"2. the pulse along x at rest, its before its now, so that the act alone sets how it moves: now"
        f" {[bump(x, sx) for x in range(sx)]}; {len(still)} Node-clocks"
    )
    # 3. the first run from 0 under the universe's push and notch: the metric's slots at the mean of the last rounds
    held, layout, s = world(universe, shape, rest + still)
    base = int(held.trains[square].first)
    sums = {c: [0] * sites for c in slots}
    board_sum = []  # the board's 00 sum by round: the notch's beat
    for r in range(1, TICKS + 1):
        s = step.tick(layout, s)
        board_sum.append(int(s.a[base].sum()))
        if r > TICKS - WINDOW:
            for c in slots:
                row = s.a[base + c]
                sums[c] = [sums[c][x] + int(row[x]) for x in range(sites)]
    means = {c: [carry(sums[c][x], WINDOW, 0)[0] for x in range(sites)] for c in slots}
    well = [
        [square, c, x, means[c][x], means[c][x], 0] for c in slots for x in range(sites) if means[c][x]
    ]
    turns = [r + 1 for r in range(1, TICKS - 1) if (board_sum[r] - board_sum[r - 1]) * (board_sum[r + 1] - board_sum[r]) < 0]
    say(
        f"3. the first run from 0, {TICKS} rounds at push {universe['chosen']['push']} and notch {universe['chosen']['notch']}:"
        f" the metric's components {slots} (read from the shape) at the mean of rounds {TICKS - WINDOW + 1}..{TICKS} (Rule3's"
        f" carry), the 00 slot's mean {means[0][centre]} at the lump's centre and {min(means[0])}..{max(means[0])} over the board;"
        f" {len(well)} Node-clocks; the board's 00 sum turning at rounds {turns} (the notch's beat)"
    )
    gears = rest + still + well
    WORLD.joinpath("setting.json").write_text(
        '{"version": 1, "ticks": '
        + str(TICKS)
        + ', "gears": [\n'
        + ",\n".join("  " + json.dumps(g) for g in gears)
        + "\n]}\n",
        encoding="utf-8",
    )
    # 4. the account: the laid world run its ticks, the lump and the pulse read on the board by windows of rounds
    held, layout, s = world(universe, shape, gears)
    at = int(held.trains[pulse].first)
    ii = [base + 1 + len(shape) + i for i in range(len(shape))]
    matter = [r for r in range(int(held.trains.size.sum())) if not base <= r < base + held.trains[square].rows()]
    kinetic, si = {"matter": 0, "ii": 0}, sigma(layout, s)
    read = [(0, int(s.a[first, centre]), spread(shape, s.a[first], f))]
    line = [int(s.a[at, site_of(shape, x, 0, 0)]) for x in range(sx)]
    profiles = [(0, line)]
    for n in range(1, TICKS + 1):
        s = step.tick(layout, s)
        so = sigma(layout, s)
        kinetic["matter"] += int((si[matter] * so[matter]).sum())
        kinetic["ii"] += int((si[ii] * so[ii]).sum())
        si = so
        if not carry(n, SPAN, 0)[1]:
            read.append((n, int(s.a[first, centre]), spread(shape, s.a[first], f)))
            profiles.append((n, [int(s.a[at, site_of(shape, x, 0, 0)]) for x in range(sx)]))
    say(
        f"4. the laid world, {TICKS} rounds: the lump by windows of {SPAN} rounds, (round, its centre's count, (its squares summed,"
        f" the permille of them within its laid support, their mean r^2 in hundredths, the permille of those on its +x side"
        f" among its two sides)): {read}"
    )
    say(
        f"5. the pulse along x through (y, z) = (0, 0), by windows of {SPAN} rounds (round, its counts at x = 0 to {sx - 1}):"
        f" {profiles}"
    )
    share, _ = carry(10**6 * kinetic["ii"], kinetic["matter"], 0)
    say(
        f"6. the price of the books' form as built (plans.pushing): the 00 push reads the momenta of every row the push does not"
        f" land on, the matter and the square's 0i and jk rows, and leaves out the square's 00 and ii rows, whose stride the stress"
        f" reads before the push's own kick; so the metric's own kinetic share of the books, its self-stress (OPEN, G2), is not"
        f" paid into the 00 slot: over the laid world's {TICKS} rounds sigma_in sigma_out summed over the board, the ii rows' {kinetic['ii']}"
        f" against the matter's {kinetic['matter']}, {share} ppm"
    )
    say(f"the setting written: {len(gears)} gears, ticks {TICKS}")
    Path(__file__).with_name("lay.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    lay()
