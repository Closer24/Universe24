"""The mesh world's lay, examples/tensor24-mesh/setting.json (the Boss's code writer, 2026-10-30, the night's PLAN.md
B5, FRAMES.md 7; its pulse laid at rest on 2026-10-31, as no typed pair may set its speed): whole numbers by the act
itself, Rule3's carry the one division, no float, no circular function, no root, no search, no table, no rounding;
the universe and the piece read from their files, no train declared here (the board's wave, the held train and the
tied train read off the loader's flags by character).

Clock: the first part of the board's wave a pulse along x, the well world's pulse form, laid at rest (its before its
now), so that the act alone sets how it moves: it splits into two halves that run apart along the ring; the held hand
(A1, A2) at rest at (1, 0) at every Node-clock, its before its now (no angle aimed: its own spring, CHOSEN in the
universe file, turns it as the act will), and every edge tooth at the dial's middle, s = 0; the tied hand (T1, T2) at rest; the gradient vertex at the universe's
CHOSEN mesh couples the difference of the board's wave to the tied hand's T1 rows and back.
Algebra: the room, hold |x_tied|^2 below Gamma div 4 at the held hand, read over the whole run on the act; the
squares of the board's wave summed against the same run at mesh 0 (the wave's own dispersion on the ring apart); the tied hand moves a count
only where its momentum reaches half a count a round.
Board: a ring along x, one Node-clock across y and z.
Clicks: n/a: the Mesh leg's wind is counted by no click (NOT_CLOSED 4); the held hand clicks nowhere inside the room.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/mesh_lay/lay.py; it writes the setting beside the
universe and the piece under examples/tensor24-mesh/, and lay.txt beside itself.
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

WORLD = ROOT.joinpath("examples", "tensor24-mesh")
PULSE, HALF, CENTRE = 500, 4, 20  # the pulse's peak, half-width and centre along x
SCAN = ((200000, 125), (240000, 125), (350000, 125), (250000, 250))  # the window about the file's mesh: (mesh, rounds)
TICKS = 125  # the setting's ticks: inside the room at the file's mesh, measured below


def bump(x, sx):
    """The pulse along x, (HALF^2 - u^2)^2 scaled to the peak, u the distance from the centre around the ring."""
    _, u = carry(x - CENTRE + HALF, sx, 0)
    u = u - HALF
    inside = int(-HALF < u < HALF)
    q, _ = carry(PULSE * (HALF * HALF - u * u) ** 2, HALF**4, 0)
    return inside * q


def world(universe, shape, gears):
    made = main.made(loading.star(len(shape)))
    held, laid = loading.load(universe, {"version": 1, "gears": gears}, sites_of(shape), *made)
    assert not laid, laid
    return held, main.layout(universe, shape, held), State(*held.state)


def by_character(held):
    """The board's wave (no square, not held, not tied), the held train and the tied train, by the loader's flags."""
    trains = range(len(held.trains))
    (light,) = [t for t in trains if held.trains.matter[t] and held.trains.gripped[t] and not held.trains.tied[t]]
    (hand,) = [t for t in trains if held.trains.held[t]]
    (tied,) = [t for t in trains if held.trains.tied[t]]
    return light, hand, tied


def gears_of(held, shape):
    light, hand, _ = by_character(held)
    sx = shape[0]
    sites = sites_of(shape)
    resting = [[hand, 0, x, 1, 1, 0] for x in range(sites)]  # the held hand at rest: before = now
    still = [[light, 0, x, bump(x, sx), bump(x, sx), 0] for x in range(sx) if bump(x, sx)]  # at rest: before = now
    return resting + still


def run(universe, shape, gears, ticks):
    """The run on the act: the squares of the board's wave by round, the tied hand's room and moves, |k|^2, the clicks, the run back."""
    held, layout, s0 = world(universe, shape, gears)
    light, hand, tied = by_character(held)
    lf, hf, tf = (int(held.trains.first[t]) for t in (light, hand, tied))
    rows = held.trains[tied].rows()
    hold, room = universe["chosen"]["hold"], carry(universe["integers"]["full_rate"], 4, 0)[0]
    seen = {"squares": [], "most": 0, "out": None, "moved": set(), "k": set(), "clicks": 0, "largest": 0}
    s = s0
    for n in range(1, ticks + 1):
        s, clicks = step.act(layout, s)
        seen["squares"].append(int((s.a[lf : lf + held.trains[light].rows()] ** 2).sum()))
        total = hold * int((s.a[tf : tf + rows] ** 2).sum(axis=0).max())
        seen["most"] = max(seen["most"], total)
        seen["out"] = n if seen["out"] is None and total >= room else seen["out"]
        seen["moved"] |= {int(x) for x in np.nonzero((s.a[tf : tf + rows] != 0).any(axis=0))[0]}
        seen["k"] |= {int(v) for v in (s.a[hf] ** 2 + s.a[hf + 1] ** 2).tolist()}
        seen["clicks"] += int((clicks != 0).sum())
        seen["largest"] = max(seen["largest"], int(abs(s.a).max()))
        if seen["largest"] > 10**9:
            break
    return seen, room, s, layout, s0


def lay():
    out = []

    def say(line):
        print(line, flush=True)
        out.append(line)

    universe = json.loads(WORLD.joinpath("universe.json").read_text(encoding="utf-8"))
    shape = json.loads(WORLD.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    ticks = TICKS
    held, layout, _ = world(universe, shape, [])
    light, hand, tied = by_character(held)
    integers, chosen = universe["integers"], universe["chosen"]
    rest, grip = int(layout.gearing.rest[0, 0]), int(layout.grip[0, 0])
    f, _ = carry(rest, integers["full_rate"], 0)
    room, _ = carry(integers["full_rate"], 4, 0)
    say(
        f"the board {shape}, {sites_of(shape)} Node-clocks along x; den {integers['den']}, Gamma {integers['full_rate']}: rest {rest}, the"
        f" grip {grip}, f = rest div Gamma {f}; the board's wave train {light}, the held train {hand} and the tied train {tied} by character; hold"
        f" {chosen['hold']} (the tied spring 2 hold f = {2 * chosen['hold'] * f}), tie 0, push 0, notch 0, mesh {chosen['mesh']}"
        f" (its ground state needs mesh^2 below grip x 2 hold f / 2 = {grip * chosen['hold'] * f}); the room hold |x_tied|^2 below Gamma"
        f" div 4 = {room}"
    )
    gears = gears_of(held, shape)
    say(
        f"1. the lay: the held hand at rest at (1, 0) at every Node-clock, its before its now, every edge tooth s = 0; the first part of the board's wave the pulse"
        f" {[bump(x, shape[0]) for x in range(CENTRE - HALF, CENTRE + HALF + 1)]} about x = {CENTRE}, at rest, its before its now, so"
        f" that the act alone sets how it moves; the tied hand at rest: {len(gears)} gears; ticks {ticks}"
    )
    flat = json.loads(json.dumps(universe))
    flat["chosen"]["mesh"] = 0
    still, _, _, _, _ = run(flat, shape, gears, ticks)
    seen, _, end, layout_, start = run(universe, shape, gears, ticks)
    back = end
    for _ in range(ticks):
        back = step.untick(layout_, back)
    exact = all(np.array_equal(x, y) for x, y in zip(back, start, strict=True))
    first = still["squares"][0]
    gap = max(abs(a - b) for a, b in zip(seen["squares"], still["squares"], strict=True))
    say(
        f"2. the run at the file's strengths, {ticks} rounds on the act: hold |x_tied|^2 at most {seen['most']} against the room's {room}"
        f" (inside it for every round: {seen['out'] is None}); the tied hand moved at {len(seen['moved'])} Node-clocks, where the pulse"
        f" passed; the held hand's |k|^2 {sorted(seen['k'])}; {seen['clicks']} clicks (the Mesh leg's wind is counted by no click); the"
        f" largest count {seen['largest']}; the squares of the board's wave summed {first} at the first round, within {min(seen['squares'])} and"
        f" {max(seen['squares'])} over the run against {min(still['squares'])} and {max(still['squares'])} at mesh 0 (the wave's own"
        f" dispersion on the ring), the two runs apart by {gap} at most, {carry(1000 * gap, first, 0)[0]} permille of the first;"
        f" the run back exact: {exact}"
    )
    for mesh, rounds in SCAN:
        other = json.loads(json.dumps(universe))
        other["chosen"]["mesh"] = mesh
        found, _, _, _, _ = run(other, shape, gears, rounds)
        say(
            f"3. the window about the file's mesh, mesh {mesh} for {rounds} rounds: hold |x_tied|^2 at most {found['most']}, first out of the room at round"
            f" {found['out']}, the tied hand moved at {len(found['moved'])} Node-clocks, the held hand's |k|^2 within"
            f" {min(found['k'])} and {max(found['k'])}, {found['clicks']} clicks, the largest count {found['largest']}"
        )
    WORLD.joinpath("setting.json").write_text(
        '{"version": 1, "ticks": ' + str(ticks) + ', "gears": [\n' + ",\n".join("  " + json.dumps(g) for g in gears) + "\n]}\n",
        encoding="utf-8",
    )
    say(f"the setting written: {len(gears)} gears, ticks {ticks}")
    Path(__file__).with_name("lay.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    lay()
