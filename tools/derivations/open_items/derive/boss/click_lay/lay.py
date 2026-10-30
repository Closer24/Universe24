"""The click world's lay, examples/tensor24-click/setting.json and its universe's key (the Boss's code writer,
2026-10-30, the night's PLAN.md B3, FRAMES.md 6 and NOT_CLOSED 29): whole numbers by the act itself, Rule3's carry the
one division, no float, no circular function, no root, no rounding; the universe and the piece read from their files,
no train declared here (the held train and the two tied trains read off the loader's flags by character, the giver
the first tied train in the file's order).

Clock: the held hand (A1, A2) at (1, 0) at every Node-clock, its before (0, -1) a quarter turn back, every edge tooth
at the dial's middle, s = 0, the format's default (the room exists only for a held tooth born there); the giver, the
first (T1, T2) hand, laid as a line hand at its turning point, a = b = (A, 0, 0) on its first row at every Node-clock;
the taker, the second, at 0; light and the metric at 0.
Algebra: f = rest div Gamma, the tied spring 2 hold f; the edge moves a count only where a gear's momentum reaches half
a count a round, and a tied hand inside the room moves at most about 0.7 of a count a round (A omega with hold A^2 below
Gamma div 4 and omega^2 = 2 hold / Gamma), so a taker at rest is moved by the hands' tie only where the tie is a large
part of the tied spring (at a tenth of it the taker's push stays in its tooth: no count moves and no click falls,
measured below); the room, hold (|x_giver|^2 + |x_taker|^2) below Gamma div 4 at the held hand, read over the whole run
on the act; the key the nearest odd whole to the seventh of the largest swing of the giver's course of S (its passing,
the two-round energy change) over its first beat, read off the act at the key 1, where the click is S itself, so that
about seven keys pass in a beat.
Board: a cube of 3, every Node-clock laid alike, so the Meshes pull nothing between like sites and one Node-clock's
run is every site's (the run tool's record and ledger read every site: click_lay/measure.py).
Clicks: the giver's and the taker's lines, their q summing to 0 at every round and site (the pair's books, inside the
room); the held train clicks nowhere while its quarter turn is exact (NOT_CLOSED 29).

Run: .venv/bin/python tools/derivations/open_items/derive/boss/click_lay/lay.py; it writes the setting beside the
universe and the piece under examples/tensor24-click/, the key into the universe, and lay.txt beside itself.
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

WORLD = ROOT.joinpath("examples", "tensor24-click")
A = 40  # the giver's turning point: hold A^2 = 1600 of the room's Gamma div 4 = 2500
TICKS = 5000  # past ten tied beats (the physicist's rule)
SEVENTH = 7  # about seven keys pass in a beat
ONE = [1, 1, 1]  # one Node-clock: every site of the cube is laid alike
SEARCH = 1000  # the rounds the lone giver is run for its beat


def files():
    universe = json.loads(WORLD.joinpath("universe.json").read_text(encoding="utf-8"))
    shape = json.loads(WORLD.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
    return universe, shape


def world(universe, shape, gears):
    """The loaded files on the engine: the held trains, the layout and the state; no departure of the lay."""
    made = main.made(loading.star(len(shape)))
    held, laid = loading.load(universe, {"version": 1, "gears": gears}, sites_of(shape), *made)
    assert not laid, laid
    return held, main.layout(universe, shape, held), State(*held.state)


def by_character(held):
    """The held train and the two tied trains by the loader's own flags, the tied in the file's order: the giver first."""
    (hand,) = [t for t in range(len(held.trains)) if held.trains.held[t]]
    giver, taker = [t for t in range(len(held.trains)) if held.trains.tied[t]]
    return hand, giver, taker


def gears_of(hand, giver, sites):
    """The lay: the held hand (1, 0) now and (0, -1) before, the giver a = b = (A, 0, 0), at every Node-clock."""
    turning = [[hand, 0, x, 1, 0, 0] for x in range(sites)] + [[hand, 1, x, 0, -1, 0] for x in range(sites)]
    return turning + [[giver, 0, x, A, A, 0] for x in range(sites)]


def squares(s, held, train):
    """A train's counts squared and summed at the one Node-clock."""
    first = int(held.trains.first[train])
    return sum(int(v) ** 2 for v in s.a[first : first + held.trains[train].rows(), 0].tolist())


def text(universe):
    """The universe file in the examples' own layout: the version, the integers, the chosen, a train a line."""
    trains = ",\n".join("    " + json.dumps(t) for t in universe["trains"])
    head = [f'  "{k}": {json.dumps(universe[k])},' for k in ("version", "integers", "chosen")]
    return "{\n" + "\n".join(head) + '\n  "trains": [\n' + trains + "\n  ]\n}\n"


def lay():
    out = []

    def say(line):
        print(line, flush=True)
        out.append(line)

    universe, shape = files()
    sites = sites_of(shape)
    held, layout, _ = world(universe, shape, [])
    hand, giver, taker = by_character(held)
    rest, gamma = int(layout.gearing.rest[0, 0]), universe["integers"]["full_rate"]
    f, _ = carry(rest, gamma, 0)
    hold, tie = universe["chosen"]["hold"], universe["chosen"]["tie"]
    room, _ = carry(gamma, 4, 0)
    say(
        f"the board {shape}, {sites} Node-clocks laid alike; den {universe['integers']['den']}, Gamma {gamma}: rest {rest}, f = rest div Gamma"
        f" {f}; the held train {hand} (A1, A2) by character, the tied trains {giver} (the giver) and {taker} (the taker); hold {hold}, the"
        f" tied spring 2 hold f = {2 * hold * f}, the hands' tie {tie} ({carry(1000 * tie, 2 * hold * f, 0)[0]} permille of it, the pair's"
        f" stiffness {2 * hold * f - tie} positive); the room hold (|x_giver|^2 + |x_taker|^2) below Gamma div 4 = {room}"
    )
    gears = gears_of(hand, giver, sites)
    say(
        f"1. the held hand (1, 0) at every Node-clock, its before (0, -1) a quarter turn back, every edge tooth at the dial's middle s = 0;"
        f" the giver a line hand at its turning point, a = b = ({A}, 0, 0): hold A^2 = {hold * A * A} of the room's {room}; the taker,"
        f" light and the metric at 0: {len(gears)} gears"
    )
    # 2. the beat: the giver alone (the hands' tie at 0), the rounds between its count's first and third sign changes
    lone = json.loads(json.dumps(universe))
    lone["chosen"]["tie"] = 0
    turns, last = [], [A]

    def beat(n, held_, s, clicks):
        count = int(s.a[int(held_.trains.first[giver]), 0])
        if (count > 0) != (last[0] > 0):
            turns.append(n)
        last[0] = count

    run_one(lone, gears_of(hand, giver, 1), SEARCH, beat)
    period = turns[2] - turns[0]
    say(f"2. the giver alone (the hands' tie at 0): its count changes sign at rounds {turns[:4]}, a beat of {period} rounds")
    # 3. the key: the act at the key 1, where the click is S, over the first beat with the hands' tie on
    one = json.loads(json.dumps(universe))
    one["chosen"]["key"] = 1
    course, swing = [0], [0]

    def wind(n, held_, s, clicks):
        course[0] += int(clicks[giver, 0])
        swing[0] = max(swing[0], abs(course[0]))

    run_one(one, gears_of(hand, giver, 1), period, wind)
    near, _ = carry(2 * swing[0] + SEVENTH, 2 * SEVENTH, 0)  # the nearest whole to the seventh
    _, odd = carry(near, 2, 0)
    key = near + (1 - odd) * (1 if SEVENTH * near <= swing[0] else -1)
    say(
        f"3. the act at the key 1 over the first beat, rounds 1..{period} (the window): the giver's course of S swings to {swing[0]} at most;"
        f" the key CHOSEN as the nearest odd whole to its seventh, {key}, so that about seven keys pass in a beat (twice the one-round key, S"
        f" counting each round's energy change twice; a chosen unit of wind below the quantum, Planck's key being NOT_CLOSED 3)"
    )
    universe["chosen"]["key"] = key
    # 4. the room over the whole run, at the key: the tied hands' squares at the held hand, |k|^2, the clicks
    seen = {"most": 0, "at": 0, "k": set(), "held": 0, "books": 0, "taker": 0, "course": [0, 0], "windows": []}
    window = [0, None]

    def watch(n, held_, s, clicks):
        total = hold * (squares(s, held_, giver) + squares(s, held_, taker))
        if total > seen["most"]:
            seen["most"], seen["at"] = total, n
        seen["k"].add(squares(s, held_, hand))
        seen["held"] += int(clicks[hand, 0] != 0)
        seen["books"] += int(int(clicks[giver, 0]) + int(clicks[taker, 0]) != 0)
        seen["course"] = [seen["course"][0] + int(clicks[giver, 0]), seen["course"][1] + int(clicks[taker, 0])]
        seen["taker"] = max(seen["taker"], abs(int(s.a[int(held_.trains.first[taker]), 0])))
        window[0] = max(window[0], total)
        window[1] = total if window[1] is None else min(window[1], total)
        _, place = carry(n, period, 0)
        if not place:
            seen["windows"].append((window[1], window[0]))
            window[0], window[1] = 0, None

    run_one(universe, gears_of(hand, giver, 1), TICKS, watch)
    say(
        f"4. the run at the key {key} for its {TICKS} rounds, on one Node-clock (every site of the cube alike): the tied hands' squares"
        f" summed at the held hand, hold (|x_giver|^2 + |x_taker|^2), at most {seen['most']} (round {seen['at']}) against the room's {room},"
        f" so the run stays inside the room for every round, the energy moving between the giver and the taker included (the lay's own"
        f" {hold * A * A} the most); by beats of {period} rounds (least, most): {seen['windows']}; the held hand's |k|^2 {sorted(seen['k'])};"
        f" the held train's clicks {seen['held']}; rounds where the giver's and the taker's q do not sum to 0: {seen['books']}; their"
        f" courses in keys {seen['course']}; the taker's largest count {seen['taker']}"
    )
    # 5. the tie the plan first named, a tenth of the tied spring: the taker's push stays in its tooth
    tenth = json.loads(json.dumps(universe))
    tenth["chosen"]["tie"], tenth["chosen"]["key"] = carry(2 * hold * f, 10, 0)[0], 1
    still = {"taker": 0, "tooth": 0, "clicks": 0}

    def quiet(n, held_, s, clicks):
        first = int(held_.trains.first[taker])
        still["taker"] = max(still["taker"], abs(int(s.a[first, 0])))
        still["tooth"] = max(still["tooth"], abs(int(s.r[first, 0])))
        still["clicks"] += sum(int(int(clicks[t, 0]) != 0) for t in range(len(held_.trains)))

    run_one(tenth, gears_of(hand, giver, 1), TICKS, quiet)
    dial = 2 * rest
    say(
        f"5. the no, the hands' tie at a tenth of the tied spring ({tenth['chosen']['tie']}) at the key 1 for {TICKS} rounds: the taker's largest"
        f" count {still['taker']}, its tooth at most {still['tooth']} of the dial's half {dial} (its push lives in the tooth, below the half count"
        f" a round that moves a count), and {still['clicks']} clicks: no exchange, no click"
    )
    WORLD.joinpath("universe.json").write_text(text(universe), encoding="utf-8")
    WORLD.joinpath("setting.json").write_text(
        '{"version": 1, "ticks": '
        + str(TICKS)
        + ', "gears": [\n'
        + ",\n".join("  " + json.dumps(g) for g in gears)
        + "\n]}\n",
        encoding="utf-8",
    )
    say(f"the setting written: {len(gears)} gears, ticks {TICKS}; the universe's key {key}")
    Path(__file__).with_name("lay.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


def run_one(universe, gears, rounds, reader):
    """The world laid by the gears on one Node-clock for the rounds, each round's state and clicks handed to the reader."""
    held, layout, s = world(universe, ONE, gears)
    for n in range(1, rounds + 1):
        s, clicks = step.act(layout, s)
        reader(n, held, s, clicks)


if __name__ == "__main__":
    lay()
