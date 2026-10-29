"""Q3, the waiting times of a quantum that draws "whether" at each beat by the split (the stay and the go).
(1) A fresh uniform c each beat: exact enumeration of every draw sequence; the first go at beat t counted.
(2) The mutant, a periodic whether: c read from the dial at its beats, a rotation on [0, rate) by -Gamma mod rate
    (q2_dial.py, part 2), over every entry phase; the waiting times and the gaps between goes (three-gap theorem).
(3) The board: c from the site's own fine tooth and one Mesh's digit by the sum carry, at each beat of the engine's
    own tick (tensor24.engine.step.tick), the waiting time over 2,000 seeds of the setting, against the geometric law.
Exact integers; floats only to print a ratio."""
import itertools
import sys
from collections import Counter
from fractions import Fraction

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import layout, state, tick  # noqa: E402

from tensor24.algebra.carry import carry  # noqa: E402


def go(c, sizes, room):
    """The split on (stay, go): c (stay + go) = t room + r_t; go where t falls in the go part's bracket."""
    t, _ = carry(c * sum(sizes), room, 0)
    q, _ = carry(t, sizes[0], 0) if False else (None, None)
    return sizes[0] <= t  # t < stay + go always, since c < room


print("(1) Fresh uniform draws, every sequence of 5 beats enumerated (room^5 sequences)")
for room, sizes in [(8, (3, 1)), (8, (2, 1)), (6, (5, 1))]:
    g = sum(go(c, sizes, room) for c in range(room))
    cnt = Counter()
    for seq in itertools.product(range(room), repeat=5):
        first = next((i + 1 for i, c in enumerate(seq) if go(c, sizes, room)), None)
        cnt[first] += 1
    law = all(cnt[t] == (room - g) ** (t - 1) * g * room ** (5 - t) for t in range(1, 6))
    print(f"  room {room}, sizes {sizes}: go count g = {g}, hazard g/room = {Fraction(g, room)} "
          f"(Born {Fraction(sizes[1], sum(sizes))}); first go at t counted (room - g)^(t-1) g room^(5-t) exactly: {law}; "
          f"survivors {cnt[None]} = (room - g)^5 {(room - g) ** 5}")


def waiting_rotation(room, step, sizes, horizon):
    """Every entry phase c0 on [0, room); c_n = c0 + n step mod room; the first beat n >= 1 with a go."""
    taus = Counter()
    for c0 in range(room):
        c = c0
        for n in range(1, horizon + 1):
            if go(c, sizes, room):
                taus[n] += 1
                break
            _, c = carry(c + step, room, 0)
        else:
            taus[None] += 1
    return taus


print("\n(2) The mutant: the dial read at its beats (room = rate, step = -Gamma mod rate), sizes (3, 1)")
for gamma, rate in [(1000, 377), (1000, 999), (1000, 401), (12, 12)]:
    _, step = carry(-gamma, rate, 0)
    sizes = (3, 1)
    g = sum(go(c, sizes, rate) for c in range(rate))
    h = Fraction(g, rate)
    taus = waiting_rotation(rate, step, sizes, 200)
    # the gaps between successive goes along one orbit (the return times)
    c, last, gaps = 0, None, Counter()
    for n in range(4 * rate):
        if go(c, sizes, rate):
            if last is not None:
                gaps[n - last] += 1
            last = n
        _, c = carry(c + step, rate, 0)
    tmax = max(t for t in taus if t is not None) if any(t is not None for t in taus) else None
    mean = Fraction(sum(t * v for t, v in taus.items() if t is not None), rate - taus[None])
    tail = Fraction(sum(v for t, v in taus.items() if t is None or t > 8), rate)
    print(f"  Gamma {gamma} rate {rate} step {step}: hazard of one draw g/room = {h} = {float(h):.4f}; "
          f"waiting times over {rate} entry phases take {len([t for t in taus if t is not None])} values, the longest {tmax}"
          f"{'' if not taus[None] else f', never {taus[None]}'}; mean {float(mean):.3f} (1/h = {float(1 / h):.3f}); "
          f"P(wait > 8) = {float(tail):.4f} against geometric (1-h)^8 = {float((1 - h) ** 8):.4f}; "
          f"gaps between goes along the orbit: {dict(sorted(gaps.items()))}")


def board_waits(seeds, amp, D, grip, W, sizes, beats, shape=(4, 4, 1)):
    lay = layout(shape, W, spring=D, grip=grip)
    n = shape[0] * shape[1] * shape[2]
    mesh = int(lay.nb[0, 0])  # site 0's +x neighbour: the one Mesh whose digit is read
    taus, pairs = Counter(), Counter()
    for seed in range(seeds):
        rng = np.random.default_rng(seed)
        a = [int(x) for x in rng.integers(-amp, amp + 1, n)]
        b = [int(x) for x in rng.integers(-amp, amp + 1, n)]
        r = [int(x) for x in rng.integers(0, W, n)]
        s, first, prev = state(a, b, r), None, None
        for t in range(1, beats + 1):
            s, _ = tick(lay, s)
            _, c = carry(s.r[0, 0] + s.r[0, mesh], W, 0)  # the sum carry: own fine tooth + one Mesh's digit
            now = go(int(c), sizes, W)
            if prev is not None:
                pairs[(prev, now)] += 1
            prev = now
            if now and first is None:
                first = t
        taus[first] += 1
    return taus, pairs


print("\n(3) The board: a 4 x 4 x 1 board, one gear per site, W 64, the full rate (every tick a beat), sizes (3, 1),")
print("    so one fresh uniform draw would have the hazard 16/64 = 1/4 exactly; 2,000 seeds of the setting, 60 beats")
W, sizes, seeds, beats = 64, (3, 1), 2000, 60
h = Fraction(sum(go(c, sizes, W) for c in range(W)), W)
for name, amp, D, grip in [("lively: notches up to 1000, D 1, grip 1", 1000, 1, 1),
                           ("quiet: notches up to 3, D 1, grip 1", 3, 1, 1),
                           ("still: no spring, no grip (push 0)", 1000, 0, 0)]:
    taus, pairs = board_waits(seeds, amp, D, grip, W, sizes, beats)
    bins = list(range(1, 13))
    chi = Fraction(0)
    row = []
    for t in bins:
        e = seeds * h * (1 - h) ** (t - 1)
        chi += (taus[t] - e) ** 2 / e
        row.append(f"{taus[t]}/{float(e):.0f}")
    e_tail = seeds * (1 - h) ** bins[-1]
    o_tail = seeds - sum(taus[t] for t in bins)
    chi += (o_tail - e_tail) ** 2 / e_tail
    gg = pairs[(True, True)] + pairs[(True, False)]
    cond = Fraction(pairs[(True, True)], gg) if gg else None
    print(f"  {name}:")
    print(f"     first go at beats 1..12, observed/geometric: {' '.join(row)}; after 12: {o_tail}/{float(e_tail):.0f};"
          f" never in 60: {taus[None]}")
    print(f"     chi-square over 13 bins (12 degrees of freedom; 21.0 is the 5% line) = {float(chi):.1f}; "
          f"P(go | go the beat before) = {float(cond) if cond is not None else 'none'} against h = {float(h)}")
