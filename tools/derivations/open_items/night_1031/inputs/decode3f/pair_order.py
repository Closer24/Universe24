"""DECODE3e's R4 with the order of each place's landings (David's word, #2187 6540015705 item 5), read on records of
Big Pic's pair act (bp/pairwhole.py, copied unchanged from origin/bigpic-3clicks 7817d1530: its definitions executed,
its two loops run as written): the third click (the pair's teeth turned) and the first (unturned, no draw). Each
record names its pair events (one line a landing, its pair's index, its place, its setting, its outcome); every R4
part is read back from the record alone, per half. Whole numbers; every division Rule3's carry.
argv: the src, the pairs, the output name."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
text = HERE.joinpath("bp", "pairwhole.py").read_text(encoding="utf-8")
defs = text.split("alice, bob, pair = born(1), born(2), born(3)\nlay =")[0]
space = {"__name__": "pairwhole_defs"}
exec(compile(defs, "pairwhole.py", "exec"), space)
carry, born, turn, click, HALF, SAME = (space[k] for k in ("carry", "born", "turn", "click", "HALF", "SAME"))
PAIRS = int(sys.argv[2])
UNIT, B2 = 1000, 2000 * 2000
N_T = 26  # per half: five 2 x 2 tests, four no-signal tests, the local bound, the pair's limit, two orders
CUT_FW = 9622  # the one-degree chi-square's upper point at 5 / 26 per cent, cited, about 9,622 thousandths
out = []


def run(turned_pair):
    alice, bob, pair = born(1), born(2), born(3)
    lines = []
    for t in range(PAIRS):
        turn(alice), turn(bob)
        if turned_pair:
            turn(pair)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        sa = 2 * click(HALF, pair, 0) - 1
        same = click(SAME[abs(b - a)], pair, 1)
        lines.append((t, "A", a, sa))
        lines.append((t, "B", b, sa * (2 * same - 1)))
    return lines


def th(num, den):
    return None if den == 0 else carry(UNIT * num, den, 0)[0]


def chi2x2(n00, n01, n10, n11):
    n = n00 + n01 + n10 + n11
    den = (n00 + n01) * (n10 + n11) * (n00 + n10) * (n01 + n11)
    return None if den == 0 else carry(UNIT * (n00 * n11 - n01 * n10) * (n00 * n11 - n01 * n10) * n, den, 0)[0]


def order_z2(xs):
    """The lag-1 correlation of a place's outcomes in the pair events' order, mean taken out (Big Pic's form), and its
    z^2 = n r1^2 in thousandths against independent draws."""
    n, s = len(xs), sum(xs)
    num = n * sum(xs[i] * xs[i + 1] for i in range(n - 1)) - s * s
    den = n * sum(v * v for v in xs) - s * s
    if den == 0:
        return None, None
    return carry(UNIT * num, den, 0)[0], carry(UNIT * n * num * num, den * den, 0)[0]


def r4(lines):
    """R4's parts per half, from the record alone: the trials joined by the pair events they name."""
    joined = {}
    for t, place, setting, landing in lines:
        joined.setdefault(t, {})[place] = (setting, landing)
    trials = [(t, v["A"], v["B"]) for t, v in sorted(joined.items()) if set(v) == {"A", "B"}]
    H, _ = carry(len(trials), 2, 0)
    res = []
    for half in (trials[:H], trials[H:H + H]):
        idx_a = {2: 0, 0: 1}  # Big Pic's signs, S = E00 + E01 + E10 - E11 (the minus on sides 0 and height 90)
        idx_b = {1: 0, 3: 1}
        cnt, num = {}, {}
        for _, (a, sa), (b, sb) in half:
            k = (idx_a[a], idx_b[b])
            cnt[k] = cnt.get(k, 0) + 1
            num[k] = num.get(k, 0) + sa * sb
        E = {k: th(num[k], cnt[k]) for k in cnt}
        S = E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)]
        S_lo = S - 1
        var = sum(carry(UNIT * UNIT - E[k] * E[k], cnt[k], 0)[0] for k in cnt)
        m2, _ = carry(CUT_FW * var, UNIT, 0)
        power = m2 < B2 and (B2 - m2) * (B2 - m2) > 4 * B2 * m2
        a_v = "NOT READ" if not power else ("SHOWN" if S_lo > 2000 and (S_lo - 2000) * (S_lo - 2000) > m2 else "NOT SHOWN")
        L = S_lo * S_lo + m2 - 2 * B2
        past = S_lo > 0 and S_lo * S_lo > m2 and L > 0 and L * L > 4 * S_lo * S_lo * m2
        z_ns = []
        for me, far, mine in ((1, 2, idx_a), (2, 1, idx_b)):
            for s_me in (0, 1):
                n0 = n1 = p0 = p1 = 0
                for _, A, Bb in half:
                    own, other = (A, Bb) if me == 1 else (Bb, A)
                    if mine[own[0]] != s_me:
                        continue
                    farset = (idx_b if me == 1 else idx_a)[other[0]]
                    plus = 1 if own[1] > 0 else 0
                    if farset == 0:
                        n0, p0 = n0 + 1, p0 + plus
                    else:
                        n1, p1 = n1 + 1, p1 + plus
                n, P = n0 + n1, p0 + p1
                den = n0 * n1 * P * (n - P)
                z_ns.append(None if den == 0 else carry(UNIT * (p0 * n1 - p1 * n0) * (p0 * n1 - p1 * n0) * n, den, 0)[0])
        mi = []
        sa_set = [idx_a[A[0]] for _, A, _ in half]
        sb_set = [idx_b[Bb[0]] for _, _, Bb in half]
        a_out = [1 if A[1] > 0 else 0 for _, A, _ in half]
        b_out = [1 if Bb[1] > 0 else 0 for _, _, Bb in half]
        for x, y in ((sa_set, sb_set), (sa_set[1:], a_out[:-1]), (sa_set[1:], b_out[:-1]), (sb_set[1:], a_out[:-1]),
                     (sb_set[1:], b_out[:-1])):
            c = [0, 0, 0, 0]
            for u, v in zip(x, y):
                c[u + u + v] += 1
            mi.append(chi2x2(*c))
        r1a, za = order_z2([A[1] for _, A, _ in half])
        r1b, zb = order_z2([Bb[1] for _, _, Bb in half])
        res.append({"S": S, "Var S": var, "(a)": a_v, "past the limit": past, "no signal z^2": z_ns,
                    "2 x 2 z^2": mi, "order": (r1a, za, r1b, zb)})
    return res


out.append(f"R4 on records of Big Pic's pair act, {PAIRS} pair events each, read per half; N_T {N_T}, CUT_FW {CUT_FW}")
for turned, label in ((1, "the third click (the pair's teeth turned)"), (0, "the first click (unturned, no draw)")):
    halves = r4(run(turned))
    for h, part in zip(("first half", "second half"), halves):
        tests = part["no signal z^2"] + part["2 x 2 z^2"]
        rest = "SHOWN" if all(z is not None and z <= CUT_FW for z in tests) else "NOT SHOWN"
        r1a, za, r1b, zb = part["order"]
        order = "SHOWN" if za is not None and zb is not None and za <= CUT_FW and zb <= CUT_FW else "NOT SHOWN"
        out.append(f"  {label}, {h}: S {part['S']} thousandths, Var S {part['Var S']} millionths; (a) {part['(a)']};"
                   f" past the pair's limit {part['past the limit']}; no signal and the 2 x 2 tests {rest}"
                   f" (largest z^2 {max(tests)}); the order: lag-1 A {r1a}, B {r1b} per mille, z^2 {za} and {zb}: {order}")
HERE.joinpath(sys.argv[3]).write_text("\n".join(out) + "\n", encoding="utf-8")
