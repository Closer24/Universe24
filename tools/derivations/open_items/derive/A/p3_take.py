"""P3, the take (the payer's unwind at one Node-clock by a due), the head's against the formula F3.

The head (unspring.fall_of, going 1): the gear of the largest now^2 - before^2, the first on a tie (R7), its now
moved toward its before by the least count s at which the window's wind falls by the due (rule3.least_at, a root
search by comparisons), None (the stop) where the full move to the before pays less.

F3, in the three operations (no gear chosen by index, no search):
  N(z)   the window's exact wind numerator, SUM over the clock and its six neighbours and the gears of
         (2 own - shared) X  (hands.wind before its carry by M = 4 Gamma^3 G^2), a quadratic in the gear's notch;
  G_k    = (N(n_k + 1) - N(n_k - 1)) div 2, the wind's pull on gear k (exact: the central difference of a quadratic);
  a      = (N(n_k + 1) + N(n_k - 1) - 2 N(n_k)) div 2, its curvature (the same for both gears of a hand);
  u_k    = -sgn(G_k) [G_k G_k >= G_l G_l]  (the steepest gear, both where tied: the unit move, free of the gears' order);
  P      = -SUM_k u_k G_k (the pull along u), phi = P - a SUM_k u_k u_k the unit's fall;
  s      = (D M + phi - 1) div phi, the linear count (one carry), and the ladder of carries
           s -> ceil(D M / (P - a |u|^2 s)) from ceil(D M / P) to its fixed point, the least count;
  zero   where the fall at the top s_v = (P + a |u|^2) div (2 a |u|^2) is below D M: the payer cannot pay (the stop
         as the quotient's zero, nothing written).
Read at every head's take on the chart: the gear chosen, the count, the stop, and F3's exact window fall (the wind
with its carries) and the remainder it leaves, r' = r + fall - D.

argv: the head's worktree, the world file, the ticks.
"""
import sys
WT = sys.argv[1]
sys.path[:0] = [WT + '/src', WT]
from collections import Counter
import numpy as np
from tests.laws import world_of
from event_universe import unspring as U, bobs as B, hands
from event_universe.clock import Clock
from event_universe.core.rule3 import wind_weight
from event_universe.trains import Gear
from event_universe.unwind import window_clocks
from event_universe.hands import spoke_places, products


def sgn(n):
    d = n * n + 1
    return n // d - (-n) // d


def numerator(clock, gears, r, window):
    """hands.wind's exact numerator summed over the window, before its carry: SUM (o + o - s) X."""
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


def window_wind(clock, gears, r, window):
    return sum(int(v) for v in hands.wind(clock, gears, r, window))


stats = Counter()
extremes = Counter()
orig = U.fall_of


def fall_of(clock, at, windings, r, hand, going=1):
    got = orig(clock, at, windings, r, hand, going)
    if going != 1 or windings <= 0:
        return got
    count, fall, k = got
    window = window_clocks(clock, at)
    gears = hand.gears
    N0 = numerator(clock, gears, r, window)
    G, A = [], []
    for kk in range(len(gears)):
        up = [1 if j == kk else 0 for j in range(len(gears))]
        dn = [-1 if j == kk else 0 for j in range(len(gears))]
        Np, Nm = numerator(clock, moved(gears, at, up), r, window), numerator(clock, moved(gears, at, dn), r, window)
        G.append((Np - Nm) // 2)
        A.append((Np + Nm - 2 * N0) // 2)
    a = A[0]
    stats["takes read (the head's fall_of at going 1, a due > 0)"] += 1
    stats["  the curvature a the same on both gears"] += int(all(x == a for x in A))
    steep = [1 if G[kk] * G[kk] >= G[1 - kk] * G[1 - kk] else 0 for kk in range(2)]
    u = [-sgn(G[kk]) * steep[kk] for kk in range(2)]
    unit2 = sum(x * x for x in u)
    M = 2 * wind_weight(clock.full_rate, clock.G)
    D = windings  # the due in wind units, as the head reads it (the slack already taken off)
    pull = sum(abs(G[kk]) * steep[kk] for kk in range(2))
    a2v = a * unit2
    sv = (pull + a2v) // (a2v + a2v) if a2v > 0 else 0  # the top of the fall, the nearest whole count to the vertex
    payable = unit2 > 0 and pull > a2v and sv * pull - a2v * sv * sv >= D * M  # F3's zero read at the whole top
    head_paid = count is not None
    stats["  the head pays (no stop)"] += int(head_paid)
    stats["  F3 pays (f_max >= the due)"] += int(payable)
    stats["  both pay"] += int(head_paid and payable)
    stats["  the head stops where F3 pays"] += int(payable and not head_paid)
    stats["  F3 stops where the head pays"] += int(head_paid and not payable)
    nz = [kk for kk in range(2) if u[kk] != 0]
    tie = steep[0] and steep[1]
    stats["  F3's unit on both gears (a tie)"] += int(tie)
    if not tie and nz:
        stats["  F3's steepest gear equals the head's gear (R7's largest now^2 - before^2)"] += int(nz[0] == k)
    gk = hand.gears[k]
    head_gear_empty = int(gk.now[at]) == int(gk.before[at])
    stats["  the head's gear has now = before (no direction: the stop by R7's choice)"] += int(head_gear_empty)
    if not payable:
        return got
    phi = -sum(u[kk] * G[kk] for kk in range(2)) - a * unit2
    s = (D * M + phi - 1) // phi
    # the ladder of carries: s -> ceil(D M / (P - a |u|^2 s)), from the linear count to its fixed point
    a2, Dp, sk, steps = a * unit2, D * M, (D * M + pull - 1) // pull, 0
    while True:
        den = pull - a2 * sk
        if den <= 0 or steps > 100000:  # past the vertex: no whole count pays
            sk = None
            break
        nxt = (Dp + den - 1) // den
        if nxt == sk:
            break
        sk, steps = nxt, steps + 1
    if sk is None:
        stats["  the ladder passes the vertex (no whole count pays the due)"] += 1
        return got
    extremes["largest count of carries the ladder takes past the first"] = max(
        extremes["largest count of carries the ladder takes past the first"], steps)
    stats[f"  the ladder's carries past the first: {min(steps, 4)}{'+' if steps >= 4 else ''}"] += 1
    s_fixed = sk
    f_fixed = s_fixed * pull - a2 * s_fixed * s_fixed
    stats["  the ladder's fixed point pays the due on the exact numerator"] += int(f_fixed >= Dp)
    stats["  the ladder's fixed point is the least count on the exact numerator"] += int(
        f_fixed >= Dp and (s_fixed - 1) * pull - a2 * (s_fixed - 1) ** 2 < Dp)
    d = [s * u[kk] for kk in range(2)]
    base = window_wind(clock, gears, r, window)
    f3_fall = base - window_wind(clock, moved(gears, at, d), r, window)
    rem = f3_fall - D  # the remainder's change r' - r
    extremes["largest F3 count s"] = max(extremes["largest F3 count s"], s)
    unit_fall = phi // M + 1
    stats["  F3: the exact fall at its count >= the due (no debt)"] += int(f3_fall >= D)
    stats["  F3: the remainder's change below one unit's fall (phi div M + 1)"] += int(-unit_fall <= rem < unit_fall)
    curv = (a2 * s * s) // M + 2
    stats["  F3: the remainder's change within its proved bound [-(a |u|^2 s^2 div M) - 2, phi div M + 2)"] += int(
        -curv <= rem < phi // M + 2)
    base_fp = window_wind(clock, moved(gears, at, [s_fixed * u[kk] for kk in range(2)]), r, window)
    rem_fp = (base - base_fp) - D
    stats["  the ladder's fixed point: the exact fall (with the carries) >= the due"] += int(rem_fp >= 0)
    if head_paid:
        same_move = (not tie) and nz and nz[0] == k
        if same_move:
            t_head = (1 if int(gk.before[at]) > int(gk.now[at]) else -1)
            stats["  same gear: the head's direction (toward before) = F3's (-sgn G)"] += int(t_head == u[k])
            stats["  same gear and direction: the head's least count = F3's linear count"] += int(t_head == u[k] and count == s)
            stats["  same gear and direction: the head's least count = the ladder's fixed point"] += int(t_head == u[k] and count == s_fixed)
            if t_head == u[k] and count != s:
                extremes["  largest |head count - F3 count| where they differ"] = max(
                    extremes["  largest |head count - F3 count| where they differ"], abs(count - s))
    return got


U.fall_of = fall_of
B.fall_of = fall_of
calibre, piece = world_of(sys.argv[2])
clock = Clock(calibre, piece)
for _ in range(int(sys.argv[3])):
    clock.tick()
print(sys.argv[2], sys.argv[3], "ticks; births", clock.counts["births"], "chimes", clock.counts["body_clicks"],
      "stops", clock.counts["refused_stop"])
for k in stats:
    print(f"  {k}: {stats[k]}")
for k in extremes:
    print(f"  {k}: {extremes[k]}")
