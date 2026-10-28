"""V4b (verifier A): the 9 ladder 'offs' of v4 re-read: non-termination at the cap, or a wrong fixed point; and the
ladder's carries against sqrt of the count at the top's own due. Pure integers. python3 -I v4b_ladder.py"""
import random
rng = random.Random(4242)


def cdiv(n, d):
    return (n + d - 1) // d


def least_brute(P, a2, DM):
    top = (P + a2) // (2 * a2)
    if top * P - a2 * top * top < DM:
        return None
    lo, hi = -1, top
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid >= 0 and mid * P - a2 * mid * mid >= DM:
            hi = mid
        else:
            lo = mid
    return hi


def ladder(P, a2, DM, cap):
    s, steps = cdiv(DM, P), 0
    while steps < cap:
        nxt = cdiv(DM, P - a2 * s)
        if nxt == s:
            return s, steps
        s, steps = nxt, steps + 1
    return None, steps


capped = wrong = n = 0
lens = []
for t in range(60000):
    P = rng.choice((rng.randint(1, 10 ** 6), rng.randint(1, 10 ** 30), rng.randint(10 ** 40, 10 ** 60)))
    a2 = rng.choice((rng.randint(1, 10 ** 3), rng.randint(1, max(1, P // 7)), rng.randint(1, max(1, P // 5000))))
    top = (P + a2) // (2 * a2)
    fmax = top * P - a2 * top * top
    if fmax <= 0:
        continue
    kind = t % 3
    DM = rng.randint(1, fmax) if kind == 0 else (fmax - rng.randint(0, max(0, fmax // 10 ** 6)) if kind == 1 else rng.randint(1, max(1, fmax // 100)))
    want = least_brute(P, a2, DM)
    got, steps = ladder(P, a2, DM, 10 ** 6)
    n += 1
    if got is None:
        capped += 1
        lens.append((steps, want))
    elif got != want:
        wrong += 1
print(f"draws {n}: the ladder stopped on a wrong count at {wrong}; still climbing after 10^6 carries at {capped}"
      f" (their least counts: {sorted(w for _s, w in lens)[:9]})")
for k in (4, 6, 8, 10, 12):
    P, a2 = 2 * 10 ** k + 1, 1
    top = (P + a2) // 2
    fmax = top * P - top * top
    s, steps = ladder(P, a2, fmax, 10 ** 8)
    print(f"  at the top's own due, P = 2 10^{k} + 1, a' = 1: the least count {top}, the ladder's carries {steps},"
          f" carries / sqrt(count) = {steps / top ** 0.5:.2f}")
