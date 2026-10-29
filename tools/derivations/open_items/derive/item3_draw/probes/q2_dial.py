"""Q2 against David's item 11: the draw read from the clock's own dial, (k, ph') = carry(ph, Gamma, rate), the engine's
tensor24.engine.step.beat. Over the ticks, at the beats (where a gear can step, so where a click can happen), with the
rate not coprime to Gamma, with the rate moved by the count, and two successive draws read together. Exact integers."""
import math
from collections import Counter
from fractions import Fraction

import numpy as np

from tensor24.algebra.carry import carry
from tensor24.engine.step import beat


def run(ph0, rate_of, gamma, ticks):
    """The dial run by the engine's own beat (fire = 1): per tick (k, ph after), the rate read from the beat count."""
    ph, n, out = np.array([[ph0]], dtype=object), 0, []
    for _ in range(ticks):
        k, ph = beat(ph, np.array([[rate_of(n)]], dtype=object), gamma, 1)
        n += int(k[0, 0])
        out.append((int(k[0, 0]), int(ph[0, 0])))
    return out


def up(c, room):  # equal parts (1, 1): up where c (1 + 1) < room, the pick's first bracket
    t, _ = carry(c * 2, room, 0)
    return t < 1


print("(1) Over the ticks: the dial's phase over one full period Gamma (every tick, beat or not)")
for gamma, rate in [(12, 5), (12, 7), (12, 4), (12, 6), (1000, 999), (1000, 375)]:
    seen = Counter(ph for _, ph in run(0, lambda n: rate, gamma, gamma))
    g = math.gcd(rate, gamma)
    print(f"  Gamma {gamma:4d} rate {rate:3d} gcd {g:3d}: residues visited {len(seen):4d} of {gamma}, "
          f"each {sorted(set(seen.values()))} times; uniform on [0, Gamma) {len(seen) == gamma}")

print("\n(2) At the beats (k = 1, the only ticks where a gear steps and a click can happen): the phase after the beat")
print("    is the beat carry's remainder, ph' = ph + rate - Gamma, so it lies in [0, rate); between beats it moves by")
print("    -Gamma modulo rate: a rotation on [0, rate)")
for gamma, rate in [(12, 5), (12, 7), (1000, 375), (1000, 999), (1000, 600), (12, 12)]:
    beats = [ph for k, ph in run(0, lambda n: rate, gamma, 50 * gamma) if k]
    seen = Counter(beats)
    step_ok = all((beats[i + 1] - beats[i] + gamma) % rate == 0 for i in range(len(beats) - 1)) if rate else True
    upf = Fraction(sum(up(c, gamma) for c in beats), len(beats))
    upr = Fraction(sum(up(c, rate) for c in beats), len(beats))
    print(f"  Gamma {gamma:4d} rate {rate:4d}: {len(beats):5d} beats, phases in [{min(beats)}, {max(beats)}], "
          f"{len(seen)} distinct, step -Gamma mod rate {step_ok}; P(up) on room Gamma {float(upf):.4f}, "
          f"on room rate {float(upr):.4f}")

print("\n(3) The rate not coprime to Gamma, read over the ticks with room Gamma: the up odds for equal parts per start")
for gamma, rate in [(12, 4), (12, 6), (12, 8), (12, 5)]:
    odds = sorted({Fraction(sum(up(ph, gamma) for _, ph in run(p0, lambda n: rate, gamma, gamma)), gamma)
                   for p0 in range(gamma)})
    print(f"  Gamma {gamma} rate {rate} (gcd {math.gcd(rate, gamma)}): P(up) over a period, by start phase: {[str(o) for o in odds]}")

print("\n(4) The rate moved by the count (stage 7b: the count moves the rate), three laws of the rate by the beat count n")
gamma = 1000
for name, rate_of in [("rate 700 - 37 (n mod 5)", lambda n: 700 - 37 * (n % 5)),
                      ("rate falling 999 - n (n < 400)", lambda n: 999 - min(n, 400)),
                      ("rate = Gamma (1 - 1/Gamma)^n, by carries", None)]:
    if rate_of is None:
        def rate_of(n, g=gamma):
            p = g
            for _ in range(n):
                p, _ = carry(p * (g - 1), g, 0)  # one unit of load: p (1 - 1/Gamma), its quotient kept
            return p
        memo = {}
        rate_of = (lambda f: (lambda n: memo.setdefault(n, f(n))))(rate_of)
    trace = run(0, rate_of, gamma, 3000)
    beats = [(i, ph) for i, (k, ph) in enumerate(trace) if k]
    n_list = list(range(len(beats)))
    inside = all(ph < rate_of(n) for n, (_, ph) in zip(n_list, beats))
    upf = Fraction(sum(up(ph, gamma) for _, ph in beats), len(beats))
    print(f"  {name:42s}: {len(beats)} beats, every post-beat phase below that beat's rate {inside}, "
          f"P(up) on room Gamma {float(upf):.4f}")

print("\n(5) Two successive draws from the dial at the beats: the pair (c_n, c_n+1) over every start phase,")
print("    Gamma 1000, rate 377 (coprime, gcd 1), room rate: are the two whethers independent?")
gamma, rate = 1000, 377
pairs = Counter()
for p0 in range(rate):  # a uniform post-beat phase on [0, rate)
    a = p0
    _, b = carry(a - gamma, rate, 0)
    pairs[(up(a, rate), up(b, rate))] += 1
tot = sum(pairs.values())
pu = Fraction(sum(v for (x, _), v in pairs.items() if x), tot)
print(f"  P(up) = {pu}; P(up, then up) = {Fraction(pairs[(True, True)], tot)} against P(up)^2 = {pu * pu}; "
      f"joint support {len(pairs)} of 4 outcome pairs over {tot} starts, (c_n, c_n+1) on {tot} of {rate * rate} pairs")
