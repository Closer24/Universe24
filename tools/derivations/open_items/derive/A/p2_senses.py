"""P2, the senses at a Mesh as one sign (formula F1), against the head's engagement bit for bit.

F1: at the Mesh (x, y), the sense of the end e is  sigma_e = sgn(h F_(o, e)),  o the other end, with
  F_(x, y) = SUM over the hand's gears (now_x before_y - before_x now_y)   (meshes.mesh_lead, the lead),
  h        = e_xy . (u(x) cross u(y)),  u_b(k) = F(k, k - b) - F(k, k + b)  (meshes.train_twists, the twist),
  sgn(n)   = n div (n n + 1) - (-n) div (n n + 1)   (two Rule3 quotients, no comparison).
The head's engagement (click.engage) puts the + fitted hand at `plus`; F1 must give sigma(plus) = +1 and
sigma(minus) = -1 at every fitting the head lays outside its rest branch, and sigma = 0 at every Mesh the head
jams by name `orientation` (lead 0) or `twist` (h 0).  The rest branch (R2) is counted apart.
Also read here: the charge current J_xy = Im(conj(z_x) z_y) (the same-time bilinear's imaginary part) at the
same Meshes, and whether it could orient them (J != 0).

argv: the head's worktree, the world file, the ticks.
"""
import sys
WT = sys.argv[1]
sys.path[:0] = [WT + '/src', WT]
from collections import Counter
from tests.laws import world_of
from event_universe import click as C
from event_universe.clock import Clock
from event_universe.core.spokes import spoke_of
from event_universe.meshes import train_lead, train_twists, cross
from event_universe.core.spokes import across


def sgn(n):
    """The sign by two Rule3 quotients (floor division), no comparison: n div (n n + 1) - (-n) div (n n + 1)."""
    d = n * n + 1
    return n // d - (-n) // d


stats = Counter()
orig_engage, orig_jammed = C.engage, C.jammed
jams = []


def jammed(clock, at, cause, **numbers):
    jams.append((cause, at, numbers))
    orig_jammed(clock, at, cause, **numbers)


def engage(clock, rec, start, wind, gearings, stopped, other=None):
    jams.clear()
    fits = orig_engage(clock, rec, start, wind, gearings, stopped, other)
    axis_leads = [train_lead(start, spoke_of(a, 0)) for a in range(3)]
    twists = train_twists(start)
    if other is not None:
        q_start = other[2]
        axis_leads = [c + train_lead(q_start, spoke_of(a, 0)) for a, c in enumerate(axis_leads)]
        twists = [t + u for t, u in zip(twists, train_twists(q_start))]
    # the same-time bilinear conj(z_x) z_y's imaginary part on the Mesh along +a, read at x
    nows = [g.now for g in start]
    charge_current = [cross(nows[0], nows[1], across(nows[0], spoke_of(a, 0)), across(nows[1], spoke_of(a, 0)))
                      for a in range(3)]
    for f in fits:
        # find the axis and the +a end of the Mesh holding minus and plus
        found = None
        for a in range(3):
            for x, y in ((f.minus, f.plus), (f.plus, f.minus)):
                j = tuple((x[b] + (1 if b == a else 0)) % clock.cube for b in range(3))
                if j == y:
                    found = (a, x, y)
        a, x, y = found
        F = int(axis_leads[a][x])  # F_(x, y), the lead along +a read at x
        h = int(twists[a][x])
        if F == 0:  # the rest branch (R2): the head's + end by the sweep, the twist not read
            stats["rest-branch engagements (R2, lead 0): F1 gives sigma 0 there"] += int(sgn(h * F) == 0)
            continue
        sig_y, sig_x = sgn(h * F), sgn(-h * F)  # sigma_y = sgn(h F_(x,y)), sigma_x = sgn(h F_(y,x))
        sigma = {x: sig_x, y: sig_y}
        ok = sigma[f.plus] == 1 and sigma[f.minus] == -1
        giver = "uncoupled giver (fittings)" if clock.hands()[rec].spring == 0 else "coupled giver (moving unspringings)"
        stats[f"engagements engage() orients ({giver}), before the lay jam and the stop"] += 1
        stats[f"  [{giver}] F1's senses equal to the head's (+ at plus, - at minus)"] += int(ok)
        stats[f"  [{giver}] sigma_x + sigma_y = 0"] += int(sig_x + sig_y == 0)
        J = int(charge_current[a][x])
        stats[f"  [{giver}] the same-time Im(conj(z_x) z_y) (the charge current) is 0"] += int(J == 0)
        stats[f"  [{giver}] sgn(Im(conj(z_x) z_y)) = sgn(F)"] += int(sgn(J) == sgn(F))
    for cause, at, numbers in jams:
        if cause not in ("orientation", "twist"):
            continue
        y = tuple(numbers["link"])
        a = next(b for b in range(3) if tuple((at[c] + (1 if c == b else 0)) % clock.cube for c in range(3)) == y)
        F, h = int(axis_leads[a][at]), int(twists[a][at])
        stats[f"jams by name `orientation` or `twist`"] += 1
        stats[f"  of them F1 gives sigma = 0 (h F = 0)"] += int(sgn(h * F) == 0)
    return fits


C.engage, C.jammed = engage, jammed
calibre, piece = world_of(sys.argv[2])
clock = Clock(calibre, piece)
for _ in range(int(sys.argv[3])):
    clock.tick()
print(sys.argv[2], sys.argv[3], "ticks; births", clock.counts["births"])
for k in stats:
    print(f"  {k}: {stats[k]}")
# the sign lemma, exhaustive on a range and at the largest integers
bad = sum(1 for n in range(-100000, 100001) if sgn(n) != (n > 0) - (n < 0))
big = [10**40 + 7, -(10**40 + 7), 2**200, -(2**200), 1, -1, 0]
bad += sum(1 for n in big if sgn(n) != (n > 0) - (n < 0))
print(f"  the sign lemma: sgn(n) = n div (n n + 1) - (-n) div (n n + 1) off at {bad} of {200001 + len(big)} integers")
