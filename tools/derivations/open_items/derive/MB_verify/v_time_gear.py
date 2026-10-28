"""Verifier's probe (MB_verify): T S T = S^-1 for the time gear's step, pure integers, every state of a box.

The step S (clock.drive with acts.carry, the fine tooth kept; the regulator's own hold 2 w, so on the A1 course the
own carry is exact and the drive alone carries a remainder):
    (b, n, r) -> (n, 2 n - b + q, r'),   q, r' = divmod(N + r, w)          r in [0, w)
The same map as draft G's 'up' rule (g2_toy.py: P = w (n - b) + r - mid, v = (P + F + mid) div w), since
(w (n - b) + r + F) div w = n - b + (r + F) div w: the half-up re-carry of a stride that holds r - mid IS the floor
carry of the push with the tooth kept. Checked here (part 0).
Turnovers T (slots exchanged, the tooth turned):
    flip      (n, b, w - 1 - r)
    mirror    (n, b, (2 mid - r) mod w)        the head's acts.mirror on the drive's tooth (tst_time_gear's 'mirror')
    raw       (n, b, 2 mid - r)                unreduced (the tooth w at r = 0, even w: off the dial)
    carried   (n - (2 mid - r) div w, b, (2 mid - r) mod w)   draft G's T_carried (the carry kept in the before slot)
    kept      (n, b, r)                         mutant
Counted: T T = id (involution) and S T S = T (i.e. T S T = S^-1 for an involution; written S(T(S(s))) = T(s)).
For the mirror the failures are split by (r == 0, r' == 0).
"""
from collections import Counter


def mid(w):
    return w // 2


def S(s, N, w):
    b, n, r = s
    q, r2 = divmod(N + r, w)
    return (n, 2 * n - b + q, r2)


def S_G_up(s, F, w):
    """Draft G's 'up' step (g2_toy.step with q_of 'up'), the force F given."""
    b, n, r = s
    m = mid(w)
    p = w * (n - b) + r - m + F
    v = (p + m) // w
    return (n, n + v, p - w * v + m)


def T_rules(w):
    m = mid(w)
    return {
        "flip": lambda s: (s[1], s[0], w - 1 - s[2]),
        "mirror": lambda s: (s[1], s[0], (2 * m - s[2]) % w),
        "raw": lambda s: (s[1], s[0], 2 * m - s[2]),
        "carried": lambda s: (s[1] - (2 * m - s[2]) // w, s[0], (2 * m - s[2]) % w),
        "kept (mutant)": lambda s: (s[1], s[0], s[2]),
    }


def box(w, R):
    for b in range(-R, R + 1):
        for n in range(-R, R + 1):
            for r in range(w):
                yield (b, n, r)


def main():
    out = []
    p = out.append
    p("0. the time gear's floor carry with the kept tooth equals draft G's half-up 'up' step")
    diff = sum(
        1
        for w in range(2, 17)
        for s in box(w, 3)
        for N in range(-3 * w, 3 * w + 1)
        if S(s, N, w) != S_G_up(s, N, w)
    )
    p(f"   states x pushes compared at w = 2..16: differences {diff}")
    p("1. every rule, w = 2..16, b, n in [-2, 2], r in [0, w), N in [-3 w, 3 w]")
    p("   w  rule           states  TT!=id  STS!=T  mirror's fails by (r=0, r'=0)")
    for w in range(2, 17):
        for name, T in T_rules(w).items():
            cnt = inv = ret = 0
            split = Counter()
            for s in box(w, 2):
                if T(T(s)) != s:
                    inv += 1
                for N in range(-3 * w, 3 * w + 1):
                    cnt += 1
                    s1 = S(s, N, w)
                    if S(T(s1), N, w) != T(s):
                        ret += 1
                        split[(s[2] == 0, s1[2] == 0)] += 1
            extra = ""
            if name == "mirror":
                one = sum(1 for s in box(w, 2) for N in range(-3 * w, 3 * w + 1) if (s[2] == 0) != (S(s, N, w)[2] == 0))
                both = sum(1 for s in box(w, 2) for N in range(-3 * w, 3 * w + 1) if s[2] == 0 and S(s, N, w)[2] == 0)
                extra = f"{dict(split)}; exactly-one-zero cases {one}, both-zero cases {both}"
            p(f"  {w:3d}  {name:13s} {cnt:6d}  {inv:6d}  {ret:6d}  {extra}")
    p("2. draft G's box: b, n in [-7, 7], r in [0, 8), w = 8 (1,800 states), force F(n) = -3 n")
    w = 8
    for name, T in T_rules(w).items():
        states = list(box(w, 7))
        inv = sum(1 for s in states if T(T(s)) != s)
        ret = sum(1 for s in states if S(T(S(s, -3 * s[1], w)), -3 * s[1], w) != T(s))

        def ST(x):
            return S(T(x), -3 * T(x)[1], w)

        tst = sum(1 for s in states if ST(ST(s)) != s)
        p(f"   {name:13s} states {len(states)}  TT!=id {inv}  retrace S T S != T {ret}  T S T != S^-1 ((S T)^2 != id) {tst}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
