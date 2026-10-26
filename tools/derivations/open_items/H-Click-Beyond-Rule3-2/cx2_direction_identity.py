"""H-Click-Beyond-Rule3-2, the one-Node test of (B): the merger's rise (merger.rise_of's quadratic, the count moved away from the before) is the birth's fall (take.fall_of's quadratic, the count moved toward the before) read at the direction -1: with F(s, sigma) = x (w (now^2 - (now + sigma t s)^2) - sigma t s pull), t toward the before, the fall is F(s, +1) div weight (the floor) and the rise is -(F(d, -1) div weight) read by the ceiling (the floor's mirror, RW-S1): rise(d) + ceil(F(d, -1) / weight) = 0 on random lines, the division at -1 of NL-S1. The two formulas are copied from take.py:54-56 and merger.py:245-247 verbatim through rule3.quotient. Integers only."""
import json
import random
import sys

from event_universe.core.rule3 import quotient

random.seed(24)
N = 20000
held = short = 0
for _ in range(N):
    now, before = random.randint(-10**9, 10**9), random.randint(-10**9, 10**9)
    if now == before:
        continue
    w, x, weight = random.randint(1, 10**12), random.randint(1, 10**9), random.randint(1, 10**15)
    pull, s = random.randint(-10**15, 10**15), random.randint(0, 10**6)
    t = 1 if before > now else -1
    u = -t

    def fall(s, sigma=1):
        moved = now + sigma * t * s
        return int(quotient(x * (w * (now * now - moved * moved) - sigma * t * s * pull), weight))

    def rise(d):
        moved = now + u * d
        return int(quotient(x * (w * (moved * moved - now * now) + u * d * pull), weight))

    numerator = x * (w * (now * now - (now - t * s) ** 2) + t * s * pull)
    ceiling = -int(quotient(-numerator, weight))
    held += rise(s) + ceiling == 0
    short += rise(s) + fall(s, -1) == 0
print(json.dumps({"lines": N, "rise_is_fall_at_minus_one_by_the_ceiling": held, "rise_is_fall_at_minus_one_by_the_floor": short}))
