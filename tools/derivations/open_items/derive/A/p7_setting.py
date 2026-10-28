"""P7, the setting's lay (formulas S1 to S5) against the head's assembly/setting.py.

S1  the setting is data: for each Node-clock and train the file names the gears' integers, and the lay is the one
    advance act, a sum over the entries (order-free):  n_k(x) += N_k(x),  b_k(x) += B_k(x).
S2  the rest turn where the file names a rest at a sense: one Gaussian product and one carry per part,
    N = SUM over the entries of z_now (pinion + i sigma s)  (s the pair's third integer, pinion^2 + s^2 = rim^2),
    V = W now - (W div rim) N + mid(W),  before = now - V div W,  fine = V mod W   (DAVID-AMPLITUDES.md section 3).
S3  a moving entry names its before notches too (data); the dispersion's closed forms leave the engine.
S4  the wave: z_now = A i^p, z_before = i z_now, i^p by p products by i (an exchange and a sign), no table.
S5  quanta are read, never set: q(x) = E(x) div w_c, the click's own quotient on the laid state.
Read here, for every committed world:
  (a) the head's laid state (every gear's now, before and fine) taken as the file's data and laid by S1 on a clock
      with no setting: the state bit for bit, and five ticks of both runs bit for bit (the state's hash);
  (b) S2 against the head's rest lays at every Node-clock they touched (the before and the fine tooth);
  (c) S4 against the head's cycle lay (the quarter table) at every Node-clock;
  (d) the head's angle_of (three pairs composed in their sorted order, two odd roundings) against the one exact
      Gaussian product rounded once (commutative, so free of the axes' order);
  (e) the file's `quanta` against the quotient read on the laid state;
  (f) the setting's searches and roots (least_at, largest_below) the head runs, counted.

argv: the head's worktree.
"""
import sys
WT = sys.argv[1]
sys.path[:0] = [WT + '/src', WT]
import itertools
import random
from collections import Counter
import numpy as np
from tests.laws import world_of
from event_universe import run as RUN
from event_universe.assembly import setting as SET, cycle as CYC
from event_universe.core import rule3, acts
from event_universe.core.rates import sine_rim, rounded
from event_universe.clock import Clock
from event_universe import hands
from event_universe.meshes import offset_pair

stats = Counter()
WORLDS = ["world_hole.json", "world_nature.json", "world_bang.json", "world_node.json", "world_sea.json",
          "world_sea_3.json", "world_pair_3.json", "world_plasma.json", "world_plasma_3.json", "world_universe.json",
          "world_universe_3.json", "world_ga2.json", "world_packet.json", "world_bodies.json",
          "world_emission.json", "world_emission_one.json", "world_polarization.json"]

# (f) count the setting's searches and roots
counts = Counter()
import event_universe  # noqa: E402
_orig_fns = {"least_at": rule3.least_at, "largest_below": rule3.largest_below}
for modname, mod in list(sys.modules.items()):
    if not modname.startswith("event_universe"):
        continue
    for name, fn in _orig_fns.items():
        if getattr(mod, name, None) is fn:
            def wrapped(*args, _orig=fn, _name=name, **kw):
                counts[_name] += 1
                return _orig(*args, **kw)
            setattr(mod, name, wrapped)


def snapshot(clock):
    return [[(g.now.copy(), g.before.copy(), g.fine.copy(), None if g.dfine is None else g.dfine.copy())
             for g in tr.gears] for tr in clock.trains_]


def equal(a, b):
    for ta, tb in zip(a, b):
        for ga, gb in zip(ta, tb):
            for xa, xb in zip(ga, gb):
                if xa is None and xb is None:
                    continue
                if xa is None or xb is None or not np.array_equal(np.asarray(xa), np.asarray(xb)):
                    return False
    return True


Clock(*world_of(WORLDS[0]))  # one clock first, so that the cached derivations (the standard's) count for none
for world in WORLDS:
    calibre, piece = world_of(world)
    counts.clear()
    head = Clock(calibre, piece)
    with_setting = dict(counts)
    counts.clear()
    bare = Clock(calibre, dict(piece, seed=[]))
    without = dict(counts)
    stats[f"(f) {world}: the setting's own searches (least_at) and roots (largest_below), beyond the bare clock's"] = (
        with_setting.get("least_at", 0) - without.get("least_at", 0),
        with_setting.get("largest_below", 0) - without.get("largest_below", 0))
    data = snapshot(head)
    base = snapshot(bare)
    # S1: the data laid on the bare clock by the one advance act (the notches added, the fine tooth written)
    for tr, td, tb in zip(bare.trains_, data, base):
        for g, (n, b, f, d), (n0, b0, f0, d0) in zip(tr.gears, td, tb):
            g.now = acts.advance(g.now, n - n0)
            g.before = acts.advance(g.before, b - b0)
            g.fine = f.copy()  # the fine tooth as the file names it (born at mid where the file names none)
    stats[f"(a) {world}: S1's lay equal to the head's setting bit for bit"] = int(equal(snapshot(bare), data))
    # the log of the setting is a reading: the bare clock's log holds no `lay` entries
    head_ticks, bare_ticks = Clock(calibre, piece), bare
    same = True
    for _ in range(5):
        head_ticks.tick()
        bare_ticks.tick()
        same = same and equal(snapshot(head_ticks), snapshot(bare_ticks)) and np.array_equal(
            np.asarray(head_ticks.slack), np.asarray(bare_ticks.slack))
    stats[f"(a) {world}: five ticks of the two runs equal bit for bit (every gear and the slack)"] = int(same)
    # (e) the quanta read on the laid state against the file's quanta
    gearings = [SET.readings.gearing(head, h.ratio, SET.readings.load(head), SET.factors(head)) for h in head.hands()]
    named = Counter()
    for entry in piece.get("seed", []):
        if "quanta" in entry:
            named[int(entry["row"])] += int(entry["quanta"])
    for row, n in sorted(named.items()):
        rec = head.hands().index(head.by_index[row])
        hand = head.hands()[rec]
        winds = hands.wind(head, [g for g in hand.gears], gearings[rec])
        q = sum(int(v) // head.windings[rec] for v in winds.flat)  # the click's quotient at every Node-clock, summed
        stats[f"(e) {world}: row {row}: the file's quanta summed {n}; the quotients E(x) div w_c read and summed {q}"] = 1


# (b) S2 against the head's rest lays, the conjugate pair and the one-sense hand, at every Node-clock touched
def rest_by_s2(z3, z12, senses, pinion, s, rim, teeth):
    """S2: N = SUM over the senses of z (pinion + i sigma s); V = W now - (W div rim) N + mid W."""
    n3 = sum(z3 for _ in senses)
    n12 = sum(z12 for _ in senses)
    N3 = sum(z3 * pinion - sg * z12 * s for sg in senses)
    N12 = sum(sg * z3 * s + z12 * pinion for sg in senses)
    out = []
    for now, N in ((n3, N3), (n12, N12)):
        V = teeth * now - (teeth // rim) * N + acts.mid(teeth)
        out.append((now - V // teeth, V % teeth))
    return out


for world in ("world_packet.json", "world_bodies.json", "world_emission_one.json", "world_pair_3.json",
              "world_plasma_3.json", "world_universe_3.json"):
    calibre, piece = world_of(world)
    head = Clock(calibre, piece)
    done = set()
    for entry in piece["seed"]:
        if entry.get("lay") not in ("at", "sea") or int(entry["row"]) == 0 or entry.get("wave"):
            continue
        if int(entry["row"]) in done:  # every Node-clock of a train read once
            continue
        done.add(int(entry["row"]))
        hand = head.by_index[int(entry["row"])]
        rec = head.hands().index(hand)
        pinion, rim = hand.ratio[0], head.rim
        s = sine_rim(pinion, rim)
        sense = int(entry.get("sense", 0))
        senses = (-1, 1) if sense == 0 else (sense,)
        three, twelve = hand.gears
        touched = ok = 0
        for at in np.ndindex(*head.size):
            if int(three.now[at]) == 0 and int(twelve.now[at]) == 0:
                continue
            touched += 1
            per_sense = int(three.now[at]) // len(senses)  # the head lays each sense with the same base
            got = rest_by_s2(per_sense, 0, senses, pinion, s, rim, three.teeth if np.ndim(three.teeth) == 0 else int(np.asarray(three.teeth)[at]))
            want = [(int(three.before[at]), int(three.fine[at])), (int(twelve.before[at]), int(twelve.fine[at]))]
            ok += int(got == want)
        stats[f"(b) {world}: row {entry['row']} Node-clocks the rest lay touched"] += touched
        stats[f"(b) {world}: row {entry['row']} S2 equal to the head (before, fine) bit for bit"] += ok


# S2 is one Gaussian product: covariant under the hand's units on a complex z_now (random draws)
rng = random.Random(28)
bad = 0
for _ in range(2000):
    rim = rng.randint(10 ** 6, 10 ** 9)
    pinion = rng.randint(0, rim)
    s = sine_rim(pinion, rim)
    teeth = 6 * rim * rng.randint(1, 50)
    z3, z12 = rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6)
    sg = rng.choice((-1, 1))
    (b3, f3), (b12, f12) = rest_by_s2(z3, z12, (sg,), pinion, s, rim, teeth)
    (c3, g3), (c12, g12) = rest_by_s2(-z12, z3, (sg,), pinion, s, rim, teeth)  # z -> i z
    # the momentum P = W (now - before) + fine - mid is linear: P(i z) = i P(z) exactly
    P = lambda now, before, fine: teeth * (now - before) + fine - acts.mid(teeth)
    p3, p12 = P(z3, b3, f3), P(z12, b12, f12)
    q3, q12 = P(-z12, c3, g3), P(z3, c12, g12)
    bad += (q3, q12) != (-p12, p3)
stats["(b) S2 under z -> i z on random complex hands: the rest momentum turned exactly (off of 2000)"] = bad

# (c) S4 against the head's cycle lay: z_now = A i^p by products by i, no table
for world in ("world_bang.json", "world_ga2.json"):
    calibre, piece = world_of(world)
    head = Clock(calibre, piece)
    entry = piece["seed"][0]
    digits = [int(v) for v in entry["p1"]] + [int(entry["cz"])]
    light = head.unsprung()
    three, twelve = light.gears
    ok = n = 0
    for at in np.ndindex(*head.size):
        x, y, zc = (v % 4 for v in at)
        p = (digits[4 * x + y] + digits[16] * zc) % 4
        A = None
        z = (1, 0)
        for _ in range(p):
            z = (-z[1], z[0])  # the product by i: an exchange and a sign
        zb = (-z[1], z[0])
        # the amplitude A is the head's search; read it from the laid state (S5: the file names A)
        A = abs(int(three.now[at])) + abs(int(twelve.now[at]))
        got = (A * z[0], A * zb[0], A * z[1], A * zb[1])
        want = (int(three.now[at]), int(three.before[at]), int(twelve.now[at]), int(twelve.before[at]))
        n += 1
        ok += int(got == want)
    stats[f"(c) {world}: S4's i^p by products against the head's quarter table, Node-clocks equal"] = (ok, n)

# (d) angle_of's sorted double rounding against the exact Gaussian product rounded once
rim = 15162856759112389
bad_head = bad_exact = diff = 0
for _ in range(3000):
    pts = []
    for _a in range(3):
        h = rng.randint(-rim // 3, rim // 3)
        pts.append(SET.rim_point(rim, h))
    heads = set()
    for perm in itertools.permutations(pts):
        first, second, third = perm
        t, w = offset_pair(first[0], first[1], second[0], second[1], rim)
        t, w = offset_pair(t, w, third[0], third[1], rim)
        heads.add((int(t), int(w)))
    exacts = set()
    for perm in itertools.permutations(pts):
        re, im = 1, 0
        for c, sn in perm:
            re, im = re * c - im * sn, re * sn + im * c
        exacts.add((int(rounded(re, rim * rim)), int(rounded(im, rim * rim))))
    bad_head += len(heads) > 1
    bad_exact += len(exacts) > 1
    diff += SET.angle_of(rim, pts) not in exacts
stats["(d) the double rounding composed in the 6 orders: draws where the order moves the result (of 3000)"] = bad_head
stats["(d) the exact product rounded once: draws where the order moves the result (of 3000)"] = bad_exact
stats["(d) the head's sorted angle_of differs from the exact product by a tooth (of 3000)"] = diff

print("P7 the setting's lay")
for k in stats:
    print(f"  {k}: {stats[k]}")
