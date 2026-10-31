"""A hand per quantum, measured on the act in whole numbers (writer C for the Boss, 2026-10-30; Big Pic's hand per
quantum for Pauli, on the owner's word to him, "Try a hand per quantum"): on a cube of 3 with the example universe's
integers, two whole-speed hands of one kind, T1 at one part (three gears a site), X and Y, each on its own spring and
with no tie between them, against one hand Z laid as their sum at every gear and site; then X and Y tied, against
themselves untied. The world's trains stand in the universe file beside the probe, universe.json (the three hands and
the metric family at the example's integers, every train's pinion at den, the seed's), read through the loader, and the
hands are the trains the loader finds no square, in the file's order (the audit of main b1a50bb33, F6 part one: they
stood declared in code before, the metric found by its kinds' count).

Clock: a hand is a train of gears, and a quantum per hand is one train laid by the files, which the loader accepts in
any number of one whole-speed kind. The push on a gear is linear in the hands (the pull, the spring, the kick at T_d = 1),
so from a common lay the momenta add after one round, N_x + N_y = N_z at every gear and site, exactly; the split of
the momentum into a count and a tooth is Rule3's carry, whose floor parts the summed hand from the pair by at most one
count a round, so over the rounds the two part by the act's rounding alone, measured here to the teeth.
Algebra: N = 2 (D (a - b) + 2 (F + J)) + s, D = 2 W at the standing clock; J = -2 f x on a hand's own spring, and
-g y on x and -g x on y under the tie g x . y, both through the T1 x T1 -> A1 table read from the star (the dot
product); P = 2 D (a - b) + s is the momentum a gear keeps on its edge, N exactly after the split; the gaps
P_z - P_x - P_y and a_z - a_x - a_y per gear over 1,000 rounds; with the tie, (N_x + N_y) tied less untied is
4 (J_tie,x + J_tie,y) = -4 g (x + y) at every gear and site, the tie's push and nothing else.
Board: the cube of 3, the metric family at 0 (push 0, notch 0, so W is the rest teeth everywhere and the clock
stands); X and Y drawn by a fixed recurrence in [-1000, 1000] counts with strides in [-30, 30] a round, Z their sum,
every edge tooth 0; the spring f = rest div 800 (a beat of about 126 rounds), the tie g = f div 10.
Clicks: n/a: the probe reads the board from outside. No half-speed kind stands in kinds.py tonight (its five kinds
are the whole-speed ones), so no half-speed quantum is laid as a hand here, and the determinant and permanent weighing
of Big Pic's reading is not built.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/hand_per_quantum/probe.py; its output is probe.txt beside it.
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
from tensor24.engine.state import Plan, State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

SHAPE = [3, 3, 3]
ROUNDS = 1000
CHECKPOINTS = (1, 10, 100, 1000)
HERE = Path(__file__).resolve().parent
UNIVERSE = json.loads(HERE.joinpath("universe.json").read_text(encoding="utf-8"))  # the hands and the metric family
UNIT = -1  # the unit, the readings' last row, as contract.pushes lays it


def recurrence(seed):
    """Whole numbers from a fixed recurrence, each step one carry: no random module."""
    v = seed
    while True:
        _, v = carry(v * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)
        yield v


def drawn(src, low, high):
    """A whole number in [low, high] from the recurrence's high bits, by two carries."""
    top, _ = carry(next(src), 1 << 33, 0)
    _, x = carry(top, high - low + 1, 0)
    return low + x


def hands(held):
    """The three hands by the loader's flags: the trains that are not the four-vector's square, in the file's order, X, Y and
    Z = X + Y."""
    x, y, z = [t for t in range(len(held.trains)) if not int(held.trains.square[t])]
    return x, y, z


def table(made):
    """The 24's table of T1 with T1 onto A1, derived from the star: its nonzero entries (entry, j, i)."""
    kinds, tables, _ = made
    labels = [name.upper() for name in kinds._fields]
    t = tables[(labels.index("T1"), labels.index("T1"), labels.index("A1"))][0]
    return [(int(t[j, i]), int(j), int(i)) for j, i in np.argwhere(t)]


def rows(held, h):
    """The rows of hand h, its train's."""
    train = held.trains[h]
    return list(range(train.first, train.first + train.rows()))


def potential(held, made, f, g):
    """V = f SUM over the hands of H . H + g X . Y, as whole factors on their legs: the springs, and the tie where g is not 0."""
    entries = table(made)
    X, Y, Z = hands(held)
    own = [(f * e, (rows(held, h)[j], rows(held, h)[i])) for h in (X, Y, Z) for e, j, i in entries]
    tie = [(g * e, (rows(held, X)[j], rows(held, Y)[i])) for e, j, i in entries] if g else []
    return own, tie


def plan(monomials):
    """J's terms from one potential: each monomial pushes every leg by minus its factor times its other legs, the unit standing for each leg it lacks of three."""
    terms = []
    for factor, legs in monomials:
        for p, leg in enumerate(legs):
            terms.append(((*legs[:p], *legs[p + 1 :], UNIT, UNIT, UNIT)[:3], -factor, leg))
    readings, factor, target = zip(*terms, strict=True)
    return Plan(
        np.array(list(zip(*readings, strict=True)), dtype=np.intp),
        np.array(factor, dtype=object),
        np.array(target, dtype=np.intp),
    )


def world(seed=6):
    """The hands laid by the loader on the cube: X and Y drawn, Z their sum at every gear and site, the metric at 0, every edge tooth 0; the loaded trains, the layout as the loader lays it (its plan the notch's, empty at 0), and the state."""
    held_universe = UNIVERSE
    sites = sites_of(SHAPE)
    made = main.made(loading.star(len(SHAPE)))
    empty, found = loading.load(held_universe, {"version": 1, "gears": []}, sites, *made)
    assert not found, found
    X, Y, Z = hands(empty)
    src = recurrence(seed)
    drawn_hands = {}
    for h in (X, Y):
        for component in range(empty.trains[h].rows()):
            for x in range(sites):
                a = drawn(src, -1000, 1000)
                drawn_hands[(h, component, x)] = (a, a - drawn(src, -30, 30))
    gears = [[h, c, x, a, b, 0] for (h, c, x), (a, b) in drawn_hands.items()]
    gears += [
        [Z, c, x, drawn_hands[(X, c, x)][0] + drawn_hands[(Y, c, x)][0], drawn_hands[(X, c, x)][1] + drawn_hands[(Y, c, x)][1], 0]
        for c in range(empty.trains[Z].rows())
        for x in range(sites)
    ]
    held, found = loading.load(held_universe, {"version": 1, "gears": gears}, sites, *made)
    assert not found, found
    return held, made, main.layout(held_universe, SHAPE, held), State(*held.state)


def momentum(layout, s):
    """Every gear's momentum on its edge, P = 2 D (a - b) + s with D = W(a) + W(b), in the tooth's unit."""
    wa, wb = step.dials(layout, s)
    return step.halves(layout) * (wa + wb) * (s.a - s.b) + s.r


def biggest(values):
    """The largest absolute whole number among the values."""
    found = 0
    for v in values:
        v = -v if v < 0 else v
        found = v if v > found else found
    return found


def gaps(held, layout, s):
    """Per component of the hands, the largest gap over the sites between Z and X + Y: of the momentum (the tooth's unit) and of the count."""
    p = momentum(layout, s)
    rx, ry, rz = (rows(held, h) for h in hands(held))
    gap_p = p[rz] - p[rx] - p[ry]
    gap_a = s.a[rz] - s.a[rx] - s.a[ry]
    return [biggest(row) for row in gap_p.tolist()], [biggest(row) for row in gap_a.tolist()]


def report():
    out = []

    def say(line):
        print(line)
        out.append(line)

    held, made, laid, s0 = world()
    rest = int(np.broadcast_to(laid.gearing.rest, s0.a.shape)[0, 0])
    f, _ = carry(rest, 800, 0)
    g, _ = carry(f, 10, 0)
    own, tie = potential(held, made, f, g)
    springs = laid._replace(plan=plan(own))
    tied = laid._replace(plan=plan(own + tie))
    rx, ry, rz = (rows(held, h) for h in hands(held))
    sites = s0.a.shape[1]
    gears = len(rz) * sites
    say(
        f"A hand per quantum on the act: the cube of {SHAPE}, the example universe's integers, three T1 hands of one part"
        f" (X, Y and Z = X + Y) and the metric family at 0; the rest teeth {rest}, the spring f {f}, the tie g {g};"
        f" {ROUNDS} rounds"
    )
    # 1. one round from the common lay, no tie: the momenta add exactly
    s1, _ = step.act(springs, s0)
    p1 = momentum(springs, s1)
    exact = int((p1[rz] == p1[rx] + p1[ry]).sum())
    gap_p, gap_a = gaps(held, springs, s1)
    say(
        f"1. after one round from the common lay, no tie: the momenta add, P_z = P_x + P_y, exactly at {exact} of {gears} gears"
        f" (the counts' gap after the split, per component, {gap_a} counts; the momentum's {gap_p})"
    )
    # 2. over the rounds: the largest gap per gear between Z and X + Y, in counts and to the teeth
    big_p, big_a, seen = [0] * len(rz), [0] * len(rz), []
    s = s0
    for t in range(1, ROUNDS + 1):
        s, _ = step.act(springs, s)
        gap_p, gap_a = gaps(held, springs, s)
        big_p = [u if u > v else v for u, v in zip(gap_p, big_p, strict=True)]
        big_a = [u if u > v else v for u, v in zip(gap_a, big_a, strict=True)]
        if t in CHECKPOINTS:
            seen.append((t, biggest(gap_a), biggest(gap_p)))
    teeth = [carry(v, rest, 0)[0] for v in big_p]
    say(
        f"2. over {ROUNDS} rounds the largest gap per gear between the summed hand and the pair: in counts, per component,"
        f" {big_a}; in the tooth's unit {big_p}, which is {teeth} teeth (a count is 4 W = {4 * rest} of the tooth's unit, the"
        f" dial 2 D at the standing clock); at the rounds {[t for t, _, _ in seen]} the largest gaps were {[a for _, a, _ in seen]} counts"
        f" and {[p for _, _, p in seen]} in the tooth's unit"
    )
    # 3. the tie between X and Y: one round from the common lay, the difference against the untied pair
    s1t, _ = step.act(tied, s0)
    p1t = momentum(tied, s1t)
    difference = (p1t[rx] + p1t[ry]) - (p1[rx] + p1[ry])
    _, j_tie = step.sources(laid._replace(plan=plan(tie)), s0.a)
    senses = step.halves(springs)
    pushed = senses * senses * (j_tie[rx] + j_tie[ry])
    closed = -senses * senses * g * (s0.a[rx] + s0.a[ry])
    alike = int((difference == pushed).sum())
    form = int((difference == closed).sum())
    standing = int((p1t[rz] == p1[rz]).sum())
    say(
        f"3. with the tie g between X and Y, one round from the common lay: the pair's momenta less the untied pair's equal"
        f" 4 (J_tie,x + J_tie,y), the tie's push through the kick, exactly at {alike} of {gears} gears, and -4 g (x + y) at"
        f" {form} of {gears}; Z, untied, unchanged at {standing} of {gears}"
    )
    Path(__file__).with_name("probe.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    report()
