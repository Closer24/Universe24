"""Term 6's frame on the engine's act through the real loader (the Boss's code writer, 2026-10-30; the night's PLAN.md B2,
FRAMES.md 6): the Mesh-less held hand (A1, A2) at (1, 0) with its edge tooth at the dial's middle, s = 0, the format's
default, on a cube of 3 with Meshes and on a cube of 4, a tied (T1, T2) hand beside it, light beside both, for ten tied
beats; whole numbers and Rule3's carry alone, the runaway read from outside at 10^9 (the coupling family's physicist's
rule: every board claim past ten beats, the stability at the zone corner).

Clock: the held hand turns a quarter a round at every Node-clock by its own spring 2 rest with |k|^2 = 1 and no grip on
its Meshes; the tied hand swings by the held hand's square at the beat the loader's plan lays; light, untied, stands.
Algebra: the loader's plans (plans.holding, plans.tying) at hold 1, f = rest div Gamma = 6000 at den 1, Gamma 1000; the
beat read as whole rounds between the giver's upward zero crossings against G3's relaxation period Gamma / (hold A) + 4 A.
Board: a cube of 3 (27 Node-clocks) and a cube of 4 (64, the checkerboard's board): the quarter turn, |k|^2, the largest
count, the period, light's standing, the run back by the act on the mirrored state; the no: the held tooth at the edge's
end, s = -D, where the turn bends at round 1 for any tied matter (the mathematician's 3b); the physicist's q6b and q11
(a tied hand at rest within one count at every site; a checkerboard of a tied hand at A = 2) rerun on the Mesh-less held
train, where his found runaways at rounds 196 to 510.
Clicks: n/a: the key 1 at every train, its clicks counted, pushing nothing.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/g3_frame/probe.py [steps]; its output is probe.txt beside
it (one step at a time with its number as the argument, each writing probe_<step>.txt, then with no argument the
whole gathered from those files in order; a step whose file is absent is run).
"""

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

GAMMA = 1000
BOUND = 10**9  # a count past it is a runaway, read from outside
BEATS = 10
LIGHT, SQUARE, HAND, GIVER, TAKER = range(5)
LEAN = 2  # the lean universe's trains stand two places earlier


def universe(den, hold, tie, lean=False):
    """The click world's shape: light, the square, the held hand (A1, A2), two tied (T1, T2) hands; every pinion den, the seed's; lean: light and the square at 0 left out (the same act on the held and tied rows, faster)."""
    trains = () if lean else (("light", ["A1"], 2), ("metric", ["A1", "T1", "A1", "E", "T2"], 1))
    trains += (("held", ["A1", "A2"], 1), ("giver", ["T1", "T2"], 1), ("taker", ["T1", "T2"], 1))
    return {
        "version": 1,
        "integers": {"den": den, "full_rate": GAMMA, "width": 128},
        "chosen": {"key": 1, "push": 0, "notch": 0, "hold": hold, "tie": tie, "mesh": 0},
        "trains": [{"name": n, "kinds": k, "part": p, "pinion": den} for n, k, p in trains],
    }


def world(u, shape, gears):
    """The files loaded on the engine: the trains, the layout and the state."""
    made = main.made(loading.star(len(shape)))
    held, laid = loading.load(u, {"version": 1, "ticks": 0, "gears": gears}, sites_of(shape), *made)
    assert not laid, laid
    return held, main.layout(u, shape, held), State(*held.state)


def rows(held, t):
    train = held.trains[t]
    return list(range(train.first, train.first + train.rows()))


def held_lay(sites, re, im, tooth=0, hand=HAND):
    """The held hand at (re, im) now and turned back one round before, before = (im, -re), at every site; its edge tooth."""
    return [[hand, 0, x, re, im, tooth] for x in range(sites)] + [[hand, 1, x, im, -re, tooth] for x in range(sites)]


def period(seq):
    """The span between the first and the last upward zero crossing over the crossings counted, as (span, count)."""
    found = [t for t in range(1, len(seq)) if seq[t - 1] < 0 <= seq[t]]
    return (found[-1] - found[0], len(found) - 1) if len(found) > 1 else (0, 0)


def thousandths(num, den):
    """num / den in thousandths by one carry; den at least 1."""
    q, _ = carry(num * 1000, den, 0)
    return q


def run(laid, s, held, rounds, watch, hand=HAND):
    """The act for rounds, read from outside each round: the watched readings, the largest count, the round a runaway shows (0: none)."""
    re, im = rows(held, hand)
    top, bent, out = 0, 0, []
    for t in range(1, rounds + 1):
        s, _ = step.act(laid, s)
        k2 = s.a[re] * s.a[re] + s.a[im] * s.a[im]
        bent = bent or (t if (k2 != 1).any() else 0)
        top = max(top, max(abs(int(v)) for v in s.a.flat))
        out.append(watch(s))
        if top > BOUND:
            return s, out, top, bent, t
    return s, out, top, bent, 0


def back(laid, s, start, rounds):
    for _ in range(rounds):
        s = step.untick(laid, s)
    return all(np.array_equal(x, y) for x, y in zip(s, start, strict=True))


def step_1(say):
    """The held hand at (1, 0), s = 0, the giver at rest at A, light at 1000: ten beats on the cube of 3."""
    den, hold = 1, 1  # the room: hold A^2 = 225 below Gamma div 4 = 250
    u = universe(den, hold, 0)
    shape = [3, 3, 3]
    sites = sites_of(shape)
    held, laid, _ = world(u, shape, [])
    rest = int(laid.gearing.rest[0, 0])
    f, _ = carry(rest, GAMMA, 0)
    say(
        f"term 6's frame on the act: den {den}, Gamma {GAMMA}, rest {rest}, f = rest div Gamma {f}, hold {hold}; the cube of 3,"
        f" {sites} Node-clocks; the held hand's rows {rows(held, HAND)}, grips {sorted(set(laid.grip[rows(held, HAND)].ravel().tolist()))},"
        f" the other rows' grips {sorted(set(np.delete(laid.grip, rows(held, HAND), axis=0).ravel().tolist()))}"
    )
    giver, light = rows(held, GIVER)[0], rows(held, LIGHT)[0]
    gears = held_lay(sites, 1, 0) + [[GIVER, 0, x, A, A, 0] for x in range(sites)]
    gears += [[LIGHT, 0, x, 1000, 1000, 0] for x in range(sites)]
    held, laid, start = world(u, shape, gears)
    re, im = rows(held, HAND)
    watch = lambda s: (int(s.a[giver, 0]), int(s.a[light, 0]), tuple(s.a[re, :4].tolist()))  # noqa: E731
    s, out, top, bent, away = run(laid, start, held, ROUNDS, watch)
    turn = all(out[t][2] == out[t + 4][2] for t in range(len(out) - 4))
    span, count = period([g for g, _, _ in out])
    say(
        f"1. the held hand (1, 0) at s = 0, the giver at rest at A = {A} on its first row, light at 1000, {ROUNDS} rounds (ten beats):"
        f" |k|^2 = 1 at every site and round ({'yes' if not bent else 'off at round ' + str(bent)}), the quarter turn exact (k returns every 4 rounds: {turn}),"
        f" the largest count {top} (runaway: {'none' if not away else 'at round ' + str(away)}); the giver's period by zero crossings"
        f" {thousandths(span, count)} thousandths of a round over {count} beats against Gamma / (hold A) + 4 A = {thousandths(BEAT, A)};"
        f" light stands at {sorted(set(l for _, l, _ in out))}; the run back exact: {back(laid, s, start, ROUNDS)}"
    )


def step_2(say):
    """The no: the held tooth at the edge's end, s = -D (the old act's r = 0): the turn bends at once with tied matter."""
    u = universe(1, 1, 0, lean=True)
    shape = [3, 3, 3]
    sites = sites_of(shape)
    held, laid, _ = world(u, shape, [])
    d = 2 * int(laid.gearing.rest[0, 0])
    giver = rows(held, GIVER - LEAN)[0]
    bad = held_lay(sites, 1, 0, tooth=-d, hand=HAND - LEAN) + [[GIVER - LEAN, 0, x, A, A, 0] for x in range(sites)]
    held, laid, start = world(u, shape, bad)
    s, out, top, bent, away = run(laid, start, held, 40, lambda s: int(s.a[giver, 0]), hand=HAND - LEAN)
    say(f"2. the no: the held tooth at the edge's end, s = -D = {-d}, the same giver: the turn bends at round {bent} (|k|^2 off 1), the largest count {top} in 40 rounds")


def step_3(say, side):
    """The physicist's q6b and q11 on the Mesh-less held train: a tied hand at rest within one count at every site."""
    u = universe(1, 1, 0, lean=True)
    shape = [side, side, side]
    sites = sites_of(shape)
    gears = held_lay(sites, 1, 0, hand=HAND - LEAN) + [[GIVER - LEAN, 0, x, 1, 1, 0] for x in range(sites)]
    held, laid, start = world(u, shape, gears)
    giver = rows(held, GIVER - LEAN)[0]
    s, out, top, bent, away = run(laid, start, held, ROUNDS, lambda s: int(s.a[giver, 0]), hand=HAND - LEAN)
    say(
        f"3. the physicist's q6b / q11 on {side}^3 (light and the square at 0 left out): the tied hand at rest at one count at every site, {ROUNDS} rounds:"
        f" |k|^2 = 1 throughout ({'yes' if not bent else 'off at round ' + str(bent)}), the largest count {top}, runaway {'none' if not away else 'at round ' + str(away)}"
        f" (his: runaways at rounds 436 and 263 with the held hand gripped); the run back exact: {back(laid, s, start, ROUNDS)}"
    )


def step_4(say):
    """The checkerboard on the tied hand at A = 2 on 4^3, the zone corner: bounded past ten beats."""
    u = universe(1, 1, 0, lean=True)
    shape = [4, 4, 4]
    sites = sites_of(shape)
    xyz = np.indices(shape).reshape(3, -1)
    _, odd = carry(xyz.sum(axis=0), 2, 0)
    gears = held_lay(sites, 1, 0, hand=HAND - LEAN)
    gears += [[GIVER - LEAN, 0, x, 2 - 4 * int(odd[x]), 2 - 4 * int(odd[x]), 0] for x in range(sites)]
    held, laid, start = world(u, shape, gears)
    giver = rows(held, GIVER - LEAN)[0]
    s, out, top, bent, away = run(laid, start, held, ROUNDS, lambda s: int(s.a[giver, 0]), hand=HAND - LEAN)
    say(
        f"4. the checkerboard, the tied hand at +-2 by the site's parity on 4^3, {ROUNDS} rounds: |k|^2 = 1 throughout"
        f" ({'yes' if not bent else 'off at round ' + str(bent)}), the largest count {top}, runaway {'none' if not away else 'at round ' + str(away)}"
        f" (his: the checkerboard on the gripped held hand grew as t + 1 to |k|^2 66,050 in 256 rounds); the run back exact: {back(laid, s, start, ROUNDS)}"
    )


def step_5(say, a=8, tie=1200):
    """The hands' tie at tie = 1200 (a tenth of the tied spring 2 hold f = 12000), the giver at A = 8 so that both hands have room (hold (A^2 + t^2) below Gamma div 4): the taker moves, the pair stays within the room."""
    u = universe(1, 1, tie, lean=True)
    shape = [3, 3, 3]
    sites = sites_of(shape)
    gears = held_lay(sites, 1, 0, hand=HAND - LEAN) + [[GIVER - LEAN, 0, x, a, a, 0] for x in range(sites)]
    held, laid, start = world(u, shape, gears)
    giver, taker = rows(held, GIVER - LEAN)[0], rows(held, TAKER - LEAN)[0]
    d = 2 * int(laid.gearing.rest[0, 0])  # the edge's dial D = W(b) + W(a) at rest
    watch = lambda s: (int(s.a[giver, 0]), int(s.a[taker, 0]), int(s.r[taker, 0]))  # noqa: E731
    s, out, top, bent, away = run(laid, start, held, ROUNDS, watch, hand=HAND - LEAN)
    say(
        f"5. the hands' tie at tie = {tie} beside hold 1, the giver at rest at A = {a}: the taker's first row reaches {max(abs(t) for _, t, _ in out)} from 0"
        f" while its edge tooth swings to {thousandths(max(abs(r) for _, _, r in out), d)} thousandths of the dial D = {d} (the tie's push below a count a round"
        f" lives in the tooth) and the giver's row stays within {max(abs(g) for g, _, _ in out)}, {ROUNDS} rounds; |k|^2 = 1 throughout"
        f" ({'yes' if not bent else 'off at round ' + str(bent)}), the largest count {top}, the run back exact: {back(laid, s, start, ROUNDS)}"
    )


STEPS = {"1": step_1, "2": step_2, "3": lambda say: step_3(say, 3), "4": lambda say: step_3(say, 4), "5": step_4, "6": step_5}
A = 15  # the giver's rest: hold A^2 = 225, below Gamma div 4 = 250, the room
BEAT = GAMMA + 4 * A * A  # G3's relaxation period times A: (Gamma / (hold A) + 4 A) A
ROUNDS, _ = carry(BEATS * (BEAT + A - 1), A, 0)  # ten beats, whole


def main_(argv):
    here = Path(__file__).parent
    for step in argv or STEPS:
        part = here.joinpath(f"probe_{step}.txt")
        if argv or not part.is_file():
            lines = []
            STEPS[step](lambda line: (print(line, flush=True), lines.append(line)))
            part.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if not argv:
        parts = [here.joinpath(f"probe_{step}.txt").read_text(encoding="utf-8") for step in STEPS]
        here.joinpath("probe.txt").write_text("".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main_(sys.argv[1:])
