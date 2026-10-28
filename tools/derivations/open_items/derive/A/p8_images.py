"""P8, the 24 (and the 48) on the running engine with the take F3 in place of the head's (R7's gear and the
least_at search): the head's own images test (tests/test_the_board.py: the chiral setting run from each of its 48
images, the regulator's time gear and the unsprung hand's first gear compared through the image, and every
fitting mapped, a reflection's with its two fitted hands exchanged), run once on the head as it is and once with
F3 patched in (a probe's monkeypatch; no file changed).

F3 at going +1 (a take): the steepest unit of the payer at the Node-clock (both gears where tied), the least count
by the ladder of carries, the zero where its integer vertex cannot pay.  At going -1 (the unspringing's light
advanced by a due): the steepest ascent and the backward ladder.  The move's sign is F3's own (-sgn G or +sgn G).

argv: the head's worktree, the ticks (14 as the head's test), 'head' or 'f3', the world (the chiral setting, world_nature.json, by default).
"""
import sys
WT = sys.argv[1]
sys.path[:0] = [WT + '/src', WT]
import itertools
from collections import Counter
import numpy as np
from tests.laws import world_of
from event_universe import unspring as U, bobs as B, hands
from event_universe.clock import Clock
from event_universe.core.rule3 import wind_weight
from event_universe.core.spokes import AXES
from event_universe.trains import Gear, HAND, REGULATOR
from event_universe.unwind import window_clocks, move, push_of, recoil
from event_universe.hands import spoke_places, products

TICKS = int(sys.argv[2])
MODE = sys.argv[3]
stats = Counter()


def sgn(n):
    d = n * n + 1
    return n // d - (-n) // d


def numerator(clock, gears, r, window):
    places = [tuple(np.array(w) for w in zip(*window))]
    places += [tuple(table[(slice(None), *places[0])]) for table in spoke_places(clock.size)]
    at = lambda a: a[places[0]] if np.ndim(a) else a
    beyond = lambda a, spoke: a[places[1 + spoke]]
    x = clock.start_stretch[places[0]]
    full_n, full_b = [g.now for g in gears], [g.before for g in gears]
    nows, befores = [at(n) for n in full_n], [at(b) for b in full_b]
    zero = np.zeros(len(window), dtype=object)
    gripped = [zero.copy() for _ in gears]
    shared = [zero.copy() for _ in gears]
    for spoke, grip in enumerate(r.grips):
        b_j = [beyond(b, spoke) for b in full_b]
        n_j = [beyond(n, spoke) for n in full_n]
        here = at(grip)
        gripped = [v + here * bj for v, bj in zip(gripped, b_j)]
        parts = products([b - bj for b, bj in zip(befores, b_j)], [n + nj for n, nj in zip(nows, n_j)])
        shared = [s + here * p for s, p in zip(shared, parts)]
    own = [at(r.teeth) * (nn + bb) - at(r.hold) * nb - nr for nn, bb, nb, nr in
           zip(products(nows, nows), products(befores, befores), products(nows, befores), products(nows, gripped))]
    return int(sum(int(v) for o, s in zip(own, shared) for v in ((o + o - s) * x)))


def moved(gears, at, d):
    out = []
    for g, dk in zip(gears, d):
        n = g.now.copy()
        n[at] = n[at] + dk
        out.append(Gear(n, g.before, g.fine, g.teeth))
    return out


def wwind(clock, gears, r, window):
    return sum(int(v) for v in hands.wind(clock, gears, r, window))


SIGNED = {}  # the last F3 move per (clock, Node-clock, going): the gear and its signed count


def f3(clock, at, windings, r, hand, going=1):
    """F3 in the head's return form (count, fall, gear), its signed move kept for the writes below."""
    window = window_clocks(clock, at)
    gears = hand.gears
    N0 = numerator(clock, gears, r, window)
    G, A = [], []
    for k in range(2):
        up = [1 if j == k else 0 for j in range(2)]
        dn = [-1 if j == k else 0 for j in range(2)]
        Np, Nm = numerator(clock, moved(gears, at, up), r, window), numerator(clock, moved(gears, at, dn), r, window)
        G.append((Np - Nm) // 2)
        A.append((Np + Nm - 2 * N0) // 2)
    steep = [1 if G[k] * G[k] >= G[1 - k] * G[1 - k] else 0 for k in range(2)]
    toward = -1 if going == 1 else 1
    u = [toward * sgn(G[k]) * steep[k] for k in range(2)]
    k = 0 if u[0] != 0 else 1
    if windings <= 0 and going == 1:
        SIGNED[(id(clock), at, going)] = (k, 0)  # the remainder alone pays: nothing moves
        return 0, 0, k
    u2 = u[0] * u[0] + u[1] * u[1]
    M = 2 * wind_weight(clock.full_rate, clock.G)
    Dp = windings * M
    a2 = A[0] * u2
    if going == 1:
        P = -(u[0] * G[0] + u[1] * G[1])
        if u2 == 0 or P <= a2:
            return None, 0, k
        sv = (P + a2) // (a2 + a2)
        if sv * P - a2 * sv * sv < Dp:
            return None, sv * P - a2 * sv * sv, k
        s = (Dp + P - 1) // P
        while True:
            den = P - a2 * s
            nxt = (Dp + den - 1) // den
            if nxt == s:
                break
            s = nxt
    else:
        if u2 == 0:
            u, u2, a2 = [1, 0], 1, A[0]
            stats["F3 at -1 from a hand with no pull (the three gear by name)"] += 1
        P = u[0] * G[0] + u[1] * G[1]
        R = lambda s_: s_ * P + a2 * s_ * s_
        s = (Dp + P - 1) // P if P > 0 else 1
        while R(s) < Dp:
            s = s + s
        while True:
            step = (R(s) - Dp) // (R(s) - R(s - 1)) if s > 0 else 0
            if step == 0:
                break
            s = s - step
    if u[0] != 0 and u[1] != 0:
        stats["F3 ties (both gears moved): not written by this probe's head form"] += 1
    d = [s * u[0], s * u[1]]
    base = wwind(clock, gears, r, window)
    after = wwind(clock, moved(gears, at, d), r, window)
    SIGNED[(id(clock), at, going)] = (k, d[k])
    return s, (base - after) if going == 1 else (after - base), k


def unsprung_end(clock, rec, read):
    """The head's unsprung_end with F3's own signed move."""
    where, tallied, notches, fall, k, _slack_was, due, _r = read
    hand = clock.hands()[rec]
    z = hand.gears[k]
    now, before = int(z.now[where]), int(z.before[where])
    _k, signed = SIGNED[(id(clock), where, 1)]
    move(clock, rec, k, where, signed)
    clock.clicks[where] += 1
    slack_was = int(clock.slack[where])
    clock.slack[where] += fall - tallied
    clock.last_push = push_of(clock, [clock.start_gears[rec][k]], where, (signed, 0), hand.ratio[0])
    clock.last_recoil = recoil(clock, where, clock.last_push, int(clock.start_rate[where]), 1)
    return {"node": list(where), "taken": fall, "booked": tallied, "levels": notches, "taken_now_was": now,
            "taker": [now, before, notches], "dP_take": clock.last_push, "taken_line": k,
            "remainder_was": slack_was, "remainder": int(clock.slack[where]), "owed": due, **clock.last_recoil}


def unsprung_notches(clock, s, windings, gearing, exact):
    hand = clock.hands()[s]

    def notches_of(where, sense):
        count, rise, k = f3(clock, where, windings[sense], gearing, hand, -1)
        _k, d = SIGNED[(id(clock), where, -1)]
        slack_was = int(clock.slack[where])
        clock.slack[where] = slack_was - (rise - windings[sense])
        exact.append([k, d, rise, slack_was])
        return tuple(d if j == HAND * k else 0 for j in range(HAND * len(hand.gears)))

    return notches_of


if MODE == "f3":
    U.fall_of, B.fall_of = f3, f3
    U.unsprung_end, U.unsprung_notches = unsprung_end, unsprung_notches
    from event_universe import click as C
    C.unsprung_notches = unsprung_notches

CUBE = 5
IMAGES = [np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
          for pi in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]


def image(m, at):
    return tuple(int(x) % CUBE for x in m @ np.array(at, dtype=int))


def births_of(clock):
    return sorted((e["i"], tuple(e["node"]), e["line_pair"], tuple(e["minus"]), tuple(e["plus"]))
                  for e in clock.log if e["event"] == "birth")


def mapped(births, m, exchanged):
    found = [(i, image(m, at), s, image(m, mi), image(m, pl)) for i, at, s, mi, pl in births]
    return sorted((i, at, s, pl, mi) if exchanged else (i, at, s, mi, pl) for i, at, s, mi, pl in found)


def world_image(piece, m):
    found = dict(piece, shape=[CUBE] * 3, seed=[dict(st) for st in piece["seed"]])
    for st in found["seed"]:
        for key in ("at", "centre"):
            if key in st:
                st[key] = list(image(m, tuple(st[key])))
    return found


def run(calibre, piece):
    clock = Clock(calibre, piece)
    for _ in range(TICKS):
        clock.tick()
    return clock


def same_rows(base, other, m):
    for gb, go in ((base.train(REGULATOR).gears[0], other.train(REGULATOR).gears[0]),
                   (base.unsprung().gears[0], other.unsprung().gears[0])):
        for at in np.ndindex(CUBE, CUBE, CUBE):
            there = image(m, at)
            if int(gb.now[at]) != int(go.now[there]) or int(gb.before[at]) != int(go.before[there]):
                return False
    return True


WORLD = sys.argv[4] if len(sys.argv) > 4 else "world_nature.json"
calibre, piece = world_of(WORLD)
base = run(calibre, world_image(piece, np.eye(3, dtype=int)))
fittings = births_of(base)
alike = Counter()
for m in IMAGES:
    other = run(calibre, world_image(piece, m))
    mm = [[int(v) for v in row] for row in m]
    determinant = (mm[0][0] * (mm[1][1] * mm[2][2] - mm[1][2] * mm[2][1]) - mm[0][1] * (mm[1][0] * mm[2][2] - mm[1][2] * mm[2][0])
                   + mm[0][2] * (mm[1][0] * mm[2][1] - mm[1][1] * mm[2][0]))
    reflection = determinant == -1  # the determinant in integers
    same = same_rows(base, other, m) and births_of(other) == mapped(fittings, m, reflection)
    alike["reflections" if reflection else "rotations"] += int(same)
print(f"P8 {WORLD}, {TICKS} ticks, the engine {'with F3' if MODE == 'f3' else 'as on the head'}:")
print(f"  fittings {base.counts['births']}, chimes {base.counts['body_clicks']}, stops {base.counts['refused_stop']}, "
      f"takes {base.counts['taken'] > 0}")
print(f"  rotations alike: {alike['rotations']} of 24; reflections alike with the fitted hands exchanged: "
      f"{alike['reflections']} of 24")
for k in stats:
    print(f"  {k}: {stats[k]}")
