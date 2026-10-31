"""The click world measured from outside (the Boss's code writer, 2026-10-30, the night's PLAN.md B3): the record and
the ledger the run tool wrote for examples/tensor24-click read line by line, and the 24 turns of the files' lay run on
the engine's own act; whole numbers and Rule3's carry alone, the trains read off the loader's flags by character, no
train declared here.

Clock: the held hand's quarter turn, |k|^2 at every Node-clock and round; the tied hands' squares summed at the held
hand, inside the room or not, every round; the giver's and the taker's clicks.
Algebra: the room hold (|x_giver|^2 + |x_taker|^2) below Gamma div 4; the pair's books, the q of the click lines summed
over the trains at every round and Node-clock; the taker's course, its q summed over the rounds; the largest count over
the run, read at 10^9 from outside (no runaway).
Board: the cube of 3 the record holds, every Node-clock read; the 24 on the same cube, the lay turned under the twisted
action (a negated row's counts negated and its edge tooth flipped to -1 - s, the drive's tooth to T_d - 1 - r_d, the
click tooth kept) and its sites moved, run its rounds and compared with the run turned, clicks and state.
Clicks: the click lines as the record holds them.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/click_lay/measure.py <record .jsonl> [turned rounds];
the ledger is read beside the record; its output is measure.txt beside this file.
"""

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import lay  # noqa: E402

from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import kinds, step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402

LARGE = 10**9  # the runaway's mark, read from outside


def lines_of(path):
    with path.open(encoding="utf-8") as held:
        for line in held:
            yield json.loads(line)


def turn_of(m, held):
    """The rows' turn for the cube's turn m: each train's kinds' matrices block by block, its parts alike."""
    acting = kinds.kinds(m[None, :, :])
    rows = int(held.trains.size.sum())
    turn = np.zeros((rows, rows), dtype=object)
    for t in range(len(held.trains)):
        train = held.trains[t]
        blocks = [kinds.square(acting)[0]] if train.square else [acting[k][0] for k in train.kinds]
        offset = 0
        for block in blocks:
            d = block.shape[0]
            for part in range(train.part):
                at = train.first + (offset + np.arange(d)) * train.part + part
                turn[np.ix_(at, at)] = block
            offset += d
    return turn


def turned(m, turn, layout, s, shape):
    """The state turned: the sites moved by m, the rows by the turn, a negated row's two teeth flipped, the click tooth kept."""
    xyz, sides = np.indices(shape).reshape(len(shape), -1), np.array(shape)[:, None]
    _, moved = carry(np.array(m.tolist(), dtype=np.intp) @ xyz, sides, 0)
    site = np.ravel_multi_index(tuple(moved), shape)
    teeth = np.broadcast_to(layout.gearing.drive, s.a.shape)
    there = State(*(np.empty_like(x) for x in s))
    there.a[:, site], there.b[:, site] = turn @ s.a, turn @ s.b
    flipped, _ = carry(turn @ (s.r + s.r + 1) - 1, 2, 0)
    there.r[:, site] = flipped
    drive, _ = carry(turn @ (s.rd + s.rd + 1 - teeth) + teeth - 1, 2, 0)
    there.rd[:, site] = drive
    there.k[:, site] = s.k
    return there, site


def the_24(say, universe, shape, setting, rounds):
    """Every turn of the 24 on the lay: the run of the turned lay against the run turned, clicks and state, each round."""
    held, layout, s0 = lay.world(universe, shape, setting["gears"])
    states, clicks = [s0], []
    for _ in range(rounds):
        s, q = step.act(layout, states[-1])
        states.append(s)
        clicks.append(q)
    matrix, weight = kinds.turns(loading.star(len(shape)))
    alike = 0
    for m in [x for x, w in zip(matrix, weight, strict=True) if w]:
        turn = turn_of(m, held)
        s, site = turned(m, turn, layout, s0, shape)
        same = True
        for n in range(rounds):
            s, q = step.act(layout, s)
            there, _ = turned(m, turn, layout, states[n + 1], shape)
            same = same and all(np.array_equal(x, y) for x, y in zip(s, there, strict=True))
            same = same and np.array_equal(q[:, site], clicks[n])
        alike += same
    say(
        f"5. the 24: the lay turned under the twisted action and its sites moved, run {rounds} rounds on the cube against the run turned,"
        f" the state and every train's clicks at every Node-clock and round: alike at {alike} of 24 turns"
    )


def main_(record, rounds):
    out = []

    def say(line):
        print(line, flush=True)
        out.append(line)

    universe, shape = lay.files()
    setting = json.loads(lay.WORLD.joinpath("setting.json").read_text(encoding="utf-8"))
    held, layout, _ = lay.world(universe, shape, setting["gears"])
    hand, giver, taker = lay.by_character(held)
    hold, gamma = universe["chosen"]["hold"], universe["integers"]["full_rate"]
    room, _ = carry(gamma, 4, 0)
    lines = list(lines_of(record))
    header, end = lines[0], lines[-1]
    taps = [x for x in lines if x["kind"] == "click"]
    say(
        f"the click world's record {record.name}: {header['sides']} Node-clocks, {end['rounds']} rounds, {len(taps)} click lines; the run"
        f" back exact: {end['exact']} (undone {end['undone']})"
    )
    books, by_train, held_rounds = {}, {}, []
    for x in taps:
        books[x["round"], x["site"]] = books.get((x["round"], x["site"]), 0) + x["q"]
        by_train[x["train"]] = by_train.get(x["train"], 0) + x["q"]
        if x["train"] == hand:
            held_rounds.append(x["round"])
    open_ = [place for place, q in books.items() if q]
    say(
        f"1. the pair's books: the q of the click lines summed over the trains at every round and Node-clock where any clicked:"
        f" {len(books)} places, {len(open_)} not 0; the q summed by train over the run {by_train} (the giver {giver}, the taker {taker})"
    )
    largest, squares_k, envelope, courses = 0, set(), {}, {}
    taker_q = {}
    for x in taps:
        if x["train"] == taker:
            taker_q[x["round"], x["site"]] = x["q"]
    pair = {}
    for x in lines_of(record.with_name(f"{record.stem}.ledger{record.suffix}")):
        count = x["count"]
        largest = max(largest, max(abs(v) for v in count))
        if x["train"] == hand:
            squares_k.add(sum(v * v for v in count))
        if x["train"] in (giver, taker):
            key = x["round"], x["site"]
            pair[key] = pair.get(key, 0) + hold * sum(v * v for v in count)
    for (n, site), total in pair.items():
        envelope[site] = max(envelope.get(site, 0), total)
    most = max(pair.values())
    named = [f"round {n}: |k|^2 there" for n in sorted(set(held_rounds))]
    say(
        f"2. the held train's click lines: {len(held_rounds)} {named[:5]}; the held hand's |k|^2 over every Node-clock and round"
        f" {sorted(squares_k)}; the largest count over the run {largest} (below {LARGE}: no runaway)"
    )
    sites = sorted({site for _, site in pair})
    say(
        f"3. the room: hold (|x_giver|^2 + |x_taker|^2) at the held hand at most {most} over every round and Node-clock against Gamma div 4 ="
        f" {room}, the same at every Node-clock: {len(set(envelope.values())) == 1} ({len(sites)} Node-clocks)"
    )
    for (n, site), q in sorted(taker_q.items()):
        courses.setdefault(site, []).append((n, q))
    course, marks = 0, []
    for n, q in courses.get(0, []):
        course += q
        marks.append((n, course))
    alike = len({tuple(v) for v in courses.values()}) == 1
    say(
        f"4. the taker's course in keys at Node-clock 0, (round, course) at each of its clicks, the first and the last ten: {marks[:10]} ..."
        f" {marks[-10:]}; its click lines alike at every Node-clock: {alike}"
    )
    the_24(say, universe, shape, setting, rounds)
    HERE.joinpath("measure.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main_(Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 100)
