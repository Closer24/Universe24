"""Q1: where the direction sits in Rule3's algebra (hand ca2). Random lines at the toy's wall: the step at +1 then at -1 bit for bit;
the step at -1 against the step at +1 on the slot-exchanged line with the remainder mirrored (w - 1 - r) and the quotient's sign kept;
the slot exchange alone (no mirror); the mirror alone (no exchange). Then the Node: the 3-cube world stepped n forward and n back
(tests/laws.py run_back_exact). Integers only. Prediction written before the run: exchange + mirror equal 20000 of 20000; exchange alone
equal only where w divides the backward numerator; mirror alone never the inverse; the Node 20 of 20."""
import random, sys, os
sys.path.insert(0, os.environ["PYTHONPATH"])
sys.path.insert(0, os.path.join(os.environ["PYTHONPATH"], "..", "tests"))
from event_universe.core.rule3 import carried_division, flux_total, rule3, mirrored
from laws import node_of, run_back_exact

random.seed(2)
den, gamma = 1021, 1000
w = 6 * den * gamma * gamma
N = 20000
back_ok = exch_mirror_ok = exch_only_ok = mirror_only_ok = 0
for _ in range(N):
    now, before = random.randint(-10**6, 10**6), random.randint(-10**6, 10**6)
    r = random.randint(0, w - 1)
    mass = random.randint(0, w)
    flux = random.randint(-w * 10, w * 10)
    nxt, r2 = rule3(flux, mass, w, now, before, r, 1)
    # the step at -1 from (now, next, r2): the same function, the other slot the next
    b1, r1 = rule3(flux, mass, w, now, nxt, r2, -1)
    back_ok += (b1, r1) == (before, r)
    # the slot exchange with the mirror: the step at +1 on (now, other = next) with the remainder mirrored, the quotient kept,
    # the remainder it leaves mirrored back
    q, rr = rule3(flux, mass, w, now, nxt, mirrored(r2, w, 1), 1)
    exch_mirror_ok += (q, mirrored(rr, w, 1)) == (before, r)
    # the exchange alone
    q, rr = rule3(flux, mass, w, now, nxt, r2, 1)
    exch_only_ok += (q, rr) == (before, r)
    # the mirror alone (no exchange: the before slot still read as the other)
    q, rr = rule3(flux, mass, w, now, before, mirrored(r2, w, 1), 1)
    mirror_only_ok += (q, mirrored(rr, w, 1)) == (before, r)
print("lines", N, "back_bit_for_bit", back_ok, "exchange_and_mirror_equal_back", exch_mirror_ok,
      "exchange_alone_equal_back", exch_only_ok, "mirror_alone_equal_back", mirror_only_ok)
# the identity under the exchange + mirror is the ones' complement commuting with the floor: floor((w-1-u)/w) = -floor(u/w)
ident = sum(((w - 1 - u) // w) == -(u // w) for u in (random.randint(-10**12, 10**12) for _ in range(N)))
print("complement_commutes_with_floor", ident, "of", N)
node = node_of("world_node.json")
n = 20
print("node_3cube_run_back", run_back_exact(node, n), "of", n)
