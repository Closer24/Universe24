"""G2 (drafter G): the three tie rules on the one gear of Rule3's leapfrog, pure integers (python3 -I), no
engine. A gear holds (b, n, r): its notch before, its notch now and its fine tooth at teeth w; its stride is
P = w (n - b) + r - mid, mid = w div 2 (the engine's acts.mid). One step with an odd force F(n) = -D n:
    p = P + F(n),  v = q(p),  (b, n, r) -> (n, n + v, p - w v + mid)
the driven carry of tick.py:266 at fixed teeth, with the quotient q chosen by the tie rule:
    up    q(p) = (p + mid) div w            (the head's; r in [0, w))
    even  the exact tie p = (k + 1/2) w sent to the even quotient (r in [0, w], 0 and w only at even v)
    down  the exact tie sent down              (r in [1, w] at even w)
At odd w the three are one rule (no tie exists). The maps tested on every canonical state of a box:
    C  negation of the gear (the hand's K on its twelve gear, the charge conjugation):
       C_mirror (-b, -n, (2 mid - r) mod w)  the head's (acts.mirror)
       C_raw    (-b, -n, 2 mid - r)          unreduced, about mid
       C_flip   (-b, -n, w - 1 - r)          the former flip (acts.flip), about mid - 1/2
       C_up1    (-b, -n, w + 1 - r)          about mid + 1/2
    T  the turnover (slots exchanged):
       T_mirror (n, b, (2 mid - r) mod w)    the head's
       T_raw    (n, b, 2 mid - r)
       T_flip   (n, b, w - 1 - r)
       T_up1    (n, b, w + 1 - r)
       T_carried now' = b, P' = -P, re-carried under the rule (the mirror with its carry kept in the
                 stride, in the before slot)
Counted: C S = S C (the commuting symmetry), T an involution, the retrace S T = T S^-1, T S T = S^-1,
and the mathematician's log-free test: M = T at the weak top (b <= n >= n+, one strict) else S, images
hit twice.
Part 2: a hand of two such gears turned by the rotation act (F = -(2 w - 2 K) n per gear, cos = K / w),
the charge W = n3 b12 - n12 b3; a K-symmetric pair seed, hand A and hand B = K A (the twelve gear
negated about mid), the net charge W_A + W_B over the steps under each rule, on many random seeds.
"""
import random
from collections import Counter

R = 7  # the box of notches: b, n in [-R, R]
D = 3


def mid_of(w):
    return w // 2


def q_of(rule, p, w):
    m = mid_of(w)
    q0, s = divmod(p + m, w)
    tie = (w % 2 == 0) and s == 0
    if rule == 'up' or not tie:
        return q0
    if rule == 'even':
        return q0 - (q0 % 2)
    return q0 - 1  # down


def canonical(rule, b, n, r, w):
    m = mid_of(w)
    P = w * (n - b) + r - m
    v = q_of(rule, P, w)
    return v == n - b and P - w * v + m == r


def states(rule, w):
    for b in range(-R, R + 1):
        for n in range(-R, R + 1):
            for r in range(0, w + 1):
                if canonical(rule, b, n, r, w):
                    yield (b, n, r)


def step(rule, x, w, F=lambda n: -D * n):
    b, n, r = x
    m = mid_of(w)
    p = w * (n - b) + r - m + F(n)
    v = q_of(rule, p, w)
    return (n, n + v, p - w * v + m)


def unstep(rule, y, w, F=lambda n: -D * n):
    """S^-1: from (n, n+, r+) the stride p, then P = p - F(n), then (b, r) re-carried."""
    n, n1, r1 = y
    m = mid_of(w)
    p = w * (n1 - n) + r1 - m
    P = p - F(n)
    v = q_of(rule, P, w)
    return (n - v, n, P - w * v + m)


def C_maps(w):
    m = mid_of(w)
    return {
        'C_mirror': lambda x: (-x[0], -x[1], (2 * m - x[2]) % w),
        'C_raw': lambda x: (-x[0], -x[1], 2 * m - x[2]),
        'C_flip': lambda x: (-x[0], -x[1], w - 1 - x[2]),
        'C_up1': lambda x: (-x[0], -x[1], w + 1 - x[2]),
    }


def T_maps(rule, w):
    m = mid_of(w)

    def carried(x):
        b, n, r = x
        P = w * (n - b) + r - m
        P2 = -P
        v = q_of(rule, P2, w)
        return (b - v, b, P2 - w * v + m)

    return {
        'T_mirror': lambda x: (x[1], x[0], (2 * m - x[2]) % w),
        'T_raw': lambda x: (x[1], x[0], 2 * m - x[2]),
        'T_flip': lambda x: (x[1], x[0], w - 1 - x[2]),
        'T_up1': lambda x: (x[1], x[0], w + 1 - x[2]),
        'T_carried': carried,
    }


def stride(x, w):
    return w * (x[1] - x[0]) + x[2] - mid_of(w)


def part1():
    print('part 1: one gear, F = -3 n, notches in [-7, 7]; failures counted over the canonical states')
    for w in range(8, 16):
        for rule in ('up', 'even', 'down'):
            xs = list(states(rule, w))
            sx = set(xs)
            cs = []
            for name, C in C_maps(w).items():
                fail = sum(1 for x in xs if not (C(x) in sx and step(rule, C(x), w) == C(step(rule, x, w))))
                rest = C((0, 0, mid_of(w)))
                cs.append(f'{name} {fail}' + ('' if rest == (0, 0, mid_of(w)) else ' (rest not fixed)'))
            ts = []
            for name, Tm in T_maps(rule, w).items():
                inv = sum(1 for x in xs if Tm(Tm(x)) != x)
                closed = sum(1 for x in xs if Tm(x) not in sx)
                retr = sum(1 for x in xs if Tm(x) in sx and step(rule, Tm(x), w) != Tm(unstep(rule, x, w)))
                tst = sum(1 for x in xs if Tm(x) in sx and Tm(step(rule, Tm(x), w)) != unstep(rule, x, w))
                neg = sum(1 for x in xs if stride(Tm(x), w) != -stride(x, w))
                images = Counter()
                for x in xs:
                    nxt = step(rule, x, w)
                    top = x[0] <= x[1] and nxt[1] <= x[1] and (x[0] < x[1] or nxt[1] < x[1])
                    images[Tm(x) if top else nxt] += 1
                twice = sum(1 for v in images.values() if v > 1)
                ts.append(f'{name}: inv {inv} closed {closed} retrace {retr} TST {tst} P->-P {neg} M twice {twice}')
            print(f'w {w:2d} {rule:4s} ({len(xs)} states): ' + '; '.join(cs))
            for t in ts:
                print(f'          {t}')


def hand_step(rule, h, w, K):
    """A hand (three, twelve), each gear (b, n, r) turned by the rotation act F = -(2 w - 2 K) n."""
    F = lambda n: -(2 * w - 2 * K) * n  # noqa: E731
    return tuple(step(rule, g, w, F) for g in h)


def charge(h):
    (b3, n3, _r3), (b12, n12, _r12) = h
    return n3 * b12 - n12 * b3


def conj(h, w):
    """K: the twelve gear negated about mid (r -> 2 mid - r, unreduced), the three gear kept."""
    (g3, (b, n, r)) = h
    return (g3, (-b, -n, 2 * mid_of(w) - r))


def neg(h, w):
    """C: every gear of the hand negated about mid (r -> 2 mid - r, unreduced), the hand's half turn."""
    return tuple((-b, -n, 2 * mid_of(w) - r) for (b, n, r) in h)


def part2(trials=400, steps=400):
    print()
    print(f'part 2: the hand pair A and B = K A (the twelve gear negated about mid), each turned by the rotation'
          f' act; {trials} random seeds, {steps} steps each; the net charge W_A + W_B per step')
    rng = random.Random(24)
    for w in (8, 10, 12, 14, 16, 20, 9, 11):
        sign_first, sign_last, sign_mean = Counter(), Counter(), Counter()
        flips = conj_thm = zero_even = ties_seen = 0
        for _ in range(trials):
            K = rng.randint(1, w - 1)
            amp = rng.randint(3, 40)
            n3, n12 = rng.randint(-amp, amp), rng.randint(-amp, amp)
            b3, b12 = rng.randint(-amp, amp), rng.randint(-amp, amp)
            m = mid_of(w)
            A = ((b3, n3, m), (b12, n12, m))
            B = conj(A, w)
            nets = {}
            for rule, (a0, b0) in (('up', (A, B)), ('even', (A, B)), ('down', (A, B)), ('up on -seed', (neg(A, w), neg(B, w)))):
                a, bb = a0, b0
                series = []
                for _t in range(steps):
                    r_ = 'up' if rule.startswith('up') else rule
                    a, bb = hand_step(r_, a, w, K), hand_step(r_, bb, w, K)
                    series.append(charge(a) + charge(bb))
                nets[rule] = series
            up = nets['up']
            first = next((x for x in up if x), 0)
            sign_first[(first > 0) - (first < 0)] += 1
            sign_last[(up[-1] > 0) - (up[-1] < 0)] += 1
            total = sum(up)
            sign_mean[(total > 0) - (total < 0)] += 1
            flips += all(x == -y for x, y in zip(up, nets['down'], strict=True))
            conj_thm += nets['down'] == nets['up on -seed']
            zero_even += all(x == 0 for x in nets['even'])
            ties_seen += any(up)
        print(f'  w {w:2d}: seeds with a nonzero net under up {ties_seen} of {trials}; the sign (-1, 0, 1) of the'
              f' first nonzero net {dict(sorted(sign_first.items()))}, of the last {dict(sorted(sign_last.items()))},'
              f' of the run\'s sum {dict(sorted(sign_mean.items()))}; down = -up at every step on {flips}; down on the'
              f' seed = up on the negated seed on {conj_thm}; even 0 at every step on {zero_even}')


def part3():
    print()
    print('part 3: the no-go at even teeth, p in [-60, 60]: oddness q(-p) = -q(p) and the one-notch shift'
          ' q(p + w) = q(p) + 1, failures per rule; and an advance of whole notches on the notch now (the'
          ' release, the unwind move) at every canonical state of the box: states it leaves non-canonical')
    for w in range(8, 16):
        parts = []
        for rule in ('up', 'even', 'down'):
            odd = sum(1 for p in range(-60, 61) if q_of(rule, -p, w) != -q_of(rule, p, w))
            shift = sum(1 for p in range(-60, 61) if q_of(rule, p + w, w) != q_of(rule, p, w) + 1)
            xs = list(states(rule, w))
            bad = sum(1 for (b, n, r) in xs for c in (1, 2, 3, -1) if not canonical(rule, b, n + c, r, w))
            parts.append(f'{rule}: odd {odd}, shift {shift}, advance {bad} of {4 * len(xs)}')
        print(f'  w {w:2d}: ' + '; '.join(parts))


part1()
part2()
part3()
