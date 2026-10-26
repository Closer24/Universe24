"""The one-Node identity of 1637d151d: the former merger.rise_of (3d7729581, least_at on the rise) against take.fall_of at -1 (the division iterated from above), transcribed on the same integers (now, before, pull, x, w, weight, walls) over random draws at the records' magnitudes; the count equal of N."""
import random, sys
sys.path.insert(0, sys.argv[1] + "/src")
from event_universe.core.rule3 import least_at, quotient

def former(now, before, pull, x, w, weight, wall):
    u = 1 if now > before else -1
    def rise(d):
        moved = now + u * d
        return int(quotient(x * (w * (moved * moved - now * now) + u * d * pull), weight))
    high = least_at(lambda d: rise(d) >= wall)
    return u * high, rise(high)

def folded(now, before, pull, x, w, weight, walls):
    direction = -1
    t = 1 if now > before else -1
    def fall(s):
        moved = now + t * s
        return int(quotient(direction * x * (w * (now * now - moved * moved) - t * s * pull), weight))
    price = -t * direction * ((w + w) * now + pull) * x
    s = -quotient(-walls * weight, price) if price > 0 else -quotient(price, x * w) - quotient(-walls * weight, x * w)
    while s > 1 and fall(s - 1) >= walls:
        s -= max(1, quotient(s * (price + x * w * s) - walls * weight, price + x * w * (s + s)))
    return t * s, fall(s)

random.seed(int(sys.argv[2]))
equal = total = 0
first = None
for _ in range(int(sys.argv[3])):
    bits = random.choice((8, 20, 40, 70))
    now = random.randint(-(1 << bits), 1 << bits)
    before = now if random.randrange(10) == 0 else random.randint(-(1 << bits), 1 << bits)
    pull = random.randint(-(1 << (bits + 10)), 1 << (bits + 10))
    x = random.randint(1, 1 << 12)
    w = random.randint(1, 1 << 20)
    weight = random.randint(1, 1 << 24)
    walls = random.randint(1, 1 << (2 * bits + 8))
    a, b = former(now, before, pull, x, w, weight, walls), folded(now, before, pull, x, w, weight, walls)
    total += 1
    if a == b:
        equal += 1
    elif first is None:
        first = (now, before, pull, x, w, weight, walls, a, b)
print("equal", equal, "of", total, "first apart", first)
