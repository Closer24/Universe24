"""Q1: where the direction sits in Rule3's algebra, measured on one line (the toy harness's functions, src/event_universe/core/rule3.py).
R: the step forward, (now, before, r) -> (next, now, r'); R(-1): the same function with the other slot and the direction -1.
X: the exchange of the two slots with the remainder mirrored, (now, before, r) -> (before, now, w - 1 - r).
Measured: (a) n forward then n back bit for bit; (b) X R X == R(-1) bit for bit (the time reversal of Rule3 is the slot exchange
conjugated by the mirror, both at once); (c) the slot exchange alone (no mirror) against R(-1): the mismatches counted, and
where they fall (r == 0 against r > 0); (d) at the wall 1 (no remainder) the slot exchange alone is R(-1) exactly: the
asymmetric piece is the remainder's interval [0, w) and nothing else; (e) the sign of the quotient at -1 is forced by (b).
Integers only; the random levels within 2^40, the walls within 2^30."""
import random, sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else 'src')
from event_universe.core.rule3 import carried_division, rule3, mirrored

rng = random.Random(24)
N = 20000
BITS_L, BITS_W = 40, 30

def step(flux, mass, wall, now, before, rem, d):
    return rule3(flux, mass, wall, now, before, rem, d)

def x_of(now, before, rem, wall):
    return before, now, mirrored(rem, wall, 1)

a_ok = b_ok = c_ok = c_bad_r0 = c_bad_rpos = d_ok = e_ok = 0
for _ in range(N):
    wall = rng.randrange(1, 1 << BITS_W)
    mass = rng.randrange(0, 2 * wall + 1)
    now, before = (rng.randrange(-(1 << BITS_L), 1 << BITS_L) for _ in range(2))
    rem = rng.randrange(0, wall)
    flux = rng.randrange(-(1 << BITS_L), 1 << BITS_L) * rng.randrange(1, 1 << 8)
    # (a) forward n = 8 steps on a fixed flux, then back 8: bit for bit
    n = 8
    kept = [(now, before, rem)]
    a, b, r = now, before, rem
    for _ in range(n):
        z, r = step(flux, mass, wall, a, b, r, 1)
        a, b = z, a
        kept.append((a, b, r))
    back_ok = True
    for k in range(n):
        z, r = step(flux, mass, wall, b, a, r, -1)   # (now=b, other=a=next) -> (before, r)
        a, b = b, z
        back_ok = back_ok and (a, b, r) == kept[n - 1 - k]
    a_ok += back_ok
    # (b) X R X == R(-1): from the post-state (next, now, r')
    z, r2 = step(flux, mass, wall, now, before, rem, 1)
    post = (z, now, r2)
    xb, xa, xr = x_of(*post, wall)             # (now, next, w-1-r')
    y, yr = step(flux, mass, wall, xb, xa, xr, 1)   # R forward on the exchanged slots: other = next
    xrx = x_of(y, xb, yr, wall)                # (xb=now, y, w-1-yr) -> exchanged: (now?..)
    # X R X (post) = X(y, xb, yr) = (xb, y, w-1-yr): the record (now, before, r)
    got = (xb, y, mirrored(yr, wall, 1))
    want = (now, before, rem)
    b_ok += got == want
    # the engine's own R(-1)
    zb, rb = step(flux, mass, wall, post[1], post[0], post[2], -1)
    e_ok += (post[1], zb, rb) == want
    # (c) the slot exchange alone, no mirror
    y2, yr2 = step(flux, mass, wall, post[1], post[0], post[2], 1)
    if (post[1], y2, yr2) == want:
        c_ok += 1
    elif rem == 0:
        c_bad_r0 += 1
    else:
        c_bad_rpos += 1
    # (d) the wall 1: the exchange alone is the inverse
    z1, r1 = step(flux, mass, 1, now, before, 0, 1)
    y1, yr1 = step(flux, mass, 1, now, z1, 0, 1)
    d_ok += (now, y1, yr1) == want[:2] + (0,)
print(f"(a) forward 8 back 8 bit for bit: {a_ok} of {N}")
print(f"(b) X R X == R(-1), the exchange conjugated by the mirror: {b_ok} of {N}")
print(f"(e) the engine's R(-1) == the inverse: {e_ok} of {N}")
print(f"(c) the exchange alone (no mirror) == R(-1): {c_ok} of {N}; off at r == 0: {c_bad_r0}, off at r > 0: {c_bad_rpos}")
print(f"(d) at the wall 1 (no remainder) the exchange alone == R(-1): {d_ok} of {N}")
