"""The live world's lay, examples/tensor24-live/setting.json (the Boss's code writer, 2026-10-31, on both readings of
main b1a50bb33: no script wrote this setting, and its pulse's before slot was set one round back by a typed speed):
whole numbers by the act itself, Rule3's carry the one division, no float, no circular function, no root, no search,
no table, no rounding; the universe and the piece read from their files, no train declared here (the board's wave read
off the loaded trains by character, the one train that is no square).

Clock: the first part of the board's wave a pulse along z, the bump the setting held, 2^28 (64 - d^2)^2 at the distance d from its
centre below 8, its peak 2^40 counts (far above one notch), laid at rest (its before its now), so that the act alone
sets how it moves: it splits into two halves that run apart along z; the metric standing at 0.
Algebra: the pulse's halves read on the board as the place and the count of its largest count on either side of its
laid centre, and its squares' mean distance from that centre around the ring, in hundredths of a Mesh.
Board: 3 by 3 by 40, the pulse alike at every x and y.
Clicks: n/a: no vertex is laid in the live world.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/live_lay/lay.py; it writes the setting beside the
universe and the piece under examples/tensor24-live/, and lay.txt beside itself.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT.joinpath("src")))

from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

WORLD = ROOT.joinpath("examples", "tensor24-live")
SCALE, REACH, CENTRE = 1 << 28, 8, 10  # the bump SCALE (REACH^2 - d^2)^2 about z = CENTRE, its peak 2^40
TICKS = 100  # the setting's ticks
SPAN = 20  # the account's windows of rounds


def site_of(shape, x, y, z):
    _, sy, sz = shape
    return (x * sy + y) * sz + z


def away(v, centre, side, half):
    """v's distance from the centre around a ring of the side, within [-half, side - half), by Rule3's carry."""
    _, u = carry(v - centre + half, side, 0)
    return u - half


def bump(z, sz):
    """The pulse along z: SCALE (REACH^2 - d^2)^2 at the distance d from the centre below REACH, 0 elsewhere."""
    d = away(z, CENTRE, sz, REACH)
    return int(-REACH < d < REACH) * SCALE * (REACH * REACH - d * d) ** 2


def world(universe, shape, gears):
    """The loaded files on the engine: the held trains, the layout and the state; no departure of the lay."""
    made = main.made(loading.star(len(shape)))
    held, laid = loading.load(universe, {"version": 1, "gears": gears}, sites_of(shape), *made)
    assert not laid, laid
    return held, main.layout(universe, shape, held), State(*held.state)


def halves(row, shape):
    """The pulse along z through (x, y) = (0, 0): the place and the count of its largest count on either side of its laid
    centre (around the ring within half its side), and its squares' mean distance from that centre in hundredths."""
    _, _, sz = shape
    half, _ = carry(sz, 2, 0)
    line = [int(row[site_of(shape, 0, 0, z)]) for z in range(sz)]
    d = [away(z, CENTRE, sz, half) for z in range(sz)]
    ahead = max((line[z], z) for z in range(sz) if d[z] > 0)
    behind = max((line[z], z) for z in range(sz) if d[z] < 0)
    weight = sum(v * v for v in line)
    moment = sum(line[z] * line[z] * abs(d[z]) for z in range(sz))
    return (behind[1], behind[0]), (ahead[1], ahead[0]), carry(100 * moment, weight, 0)[0]


def lay():
    out = []

    def say(line):
        print(line, flush=True)
        out.append(line)

    universe = json.loads(WORLD.joinpath("universe.json").read_text(encoding="utf-8"))
    shape = json.loads(WORLD.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    sx, sy, sz = shape
    held, _, _ = world(universe, shape, [])
    (light,) = [t for t in range(len(held.trains)) if not held.trains[t].square]
    gears = [
        [light, 0, site_of(shape, x, y, z), bump(z, sz), bump(z, sz), 0]
        for x in range(sx)
        for y in range(sy)
        for z in range(sz)
        if bump(z, sz)
    ]
    say(
        f"the board {shape}, {sites_of(shape)} Node-clocks; the board's wave train {light} by character; the pulse along z, 2^28 (64 - d^2)^2"
        f" about z = {CENTRE}, its peak {bump(CENTRE, sz)}, alike at every x and y: {[carry(bump(z, sz), SCALE, 0)[0] for z in range(sz)]}"
        f" times 2^28, at rest (its before its now): {len(gears)} gears; ticks {TICKS}"
    )
    held, layout, start = world(universe, shape, gears)
    first = int(held.trains[light].first)
    s, reads = start, [(0, halves(start.a[first], shape))]
    for n in range(1, TICKS + 1):
        s = step.tick(layout, s)
        if not carry(n, SPAN, 0)[1]:
            reads.append((n, halves(s.a[first], shape)))
    back = s
    for _ in range(TICKS):
        back = step.untick(layout, back)
    exact = all(np.array_equal(x, y) for x, y in zip(back, start, strict=True))
    say(
        f"1. the run, {TICKS} rounds on the act, by windows of {SPAN} rounds (round, ((z, count) of its largest count behind its"
        f" laid centre, the same ahead of it, its squares' mean distance from the centre in hundredths of a Mesh)): {reads};"
        f" the run back exact: {exact}"
    )
    WORLD.joinpath("setting.json").write_text(
        '{"version": 1, "ticks": ' + str(TICKS) + ', "gears": [\n' + ",\n".join("  " + json.dumps(g) for g in gears) + "\n]}\n",
        encoding="utf-8",
    )
    say(f"the setting written: {len(gears)} gears, ticks {TICKS}")
    Path(__file__).with_name("lay.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    lay()
