"""DECODE3f's measurements of its new and changed rules. Whole numbers; every division Rule3's carry; no random module.

It executes the definitions of decode3e.py and pair_order.py (copies of the frozen probes, in this folder) and reads:
A. R3 as the conjunction, gated on (3b): (3d) and the new (3e) (the past-2 table, lags 1 and 2) read only where (3b)
   is read; (3p), the period weighed against the record's length; on carried sides (the HALF mathematician's moving
   families), fair draws, and the circulation's landings W at the click world's dial (THIRD7's form, K = 3).
B. R4 with the new (e): per pair source, at both places, lag-1 and R2's past ladder (1, 2, 4, 8, AMBIG 2) with a power
   gate; each place's outcomes against its own past setting; (c) gated on R3 at both places, each place's passing
   carried; the precedence; on seven pair records (Big Pic's pair act, bp/pairwhole.py, and six forms with no draw).
C. The seed test's (ii): its no in THIRD7's twin; the headers' units; acceptance with section 7's books.
D. The three kinds at ed6a1f225: a place with an edge on two triangles; W from the record (min and c . q); the lone
   edge recomputed exactly.
E. Each clock's own count (its own lines, in the record's order) and D4, on the frozen board records.
F. The conversions' checks on hand-built counts (a test of the checks' logic, never a world).
G. CUT_FW at each N_T, by whole numbers (erf's series and Machin's pi), checked against the cited values.
argv: the output name."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTNAME = sys.argv[1] if len(sys.argv) > 1 else "decode3f.txt"
SRC = HERE.joinpath("decode3e.py")
g = {"__file__": str(SRC), "__name__": "decode3e_defs"}
TEXT = SRC.read_text(encoding="utf-8")
exec(compile(TEXT.split("# ---- the stand-in cases")[0], str(SRC), "exec"), g)


def lift(name):
    """One top-level definition of decode3e.py, by name: from its def to the next top-level line."""
    head = TEXT.index("\ndef " + name + "(") + 1
    body = TEXT[head:].split("\n")
    keep = [body[0]]
    for ln in body[1:]:
        if ln and not ln.startswith((" ", "#")):
            break
        keep.append(ln)
    return "\n".join(keep) + "\n"


exec(compile("EDGES = ((2, 3), (2, 4), (3, 4))\nCYC = (1, -1, 1)\n" + "".join(lift(n) for n in (
    "seed_ii", "by_place", "clock_sum", "whole_circulations", "cen", "triangle", "lines_of", "kinds_read",
    "checks_b_c", "lone_edge", "circulation")), str(SRC), "exec"), g)
carry, th, up, D = g["carry"], g["th"], g["up"], g["D"]
b3_given, d3_given = g["b3_given"], g["d3_given"]
carried_side, fair_side, steady, swing, wide, step = (g[k] for k in ("carried_side", "fair_side", "steady", "swing",
                                                                      "wide", "step"))
ambiguous, circulation, triangle, checks_b_c, lines_of, kinds_read = (g[k] for k in (
    "ambiguous", "circulation", "triangle", "checks_b_c", "lines_of", "kinds_read"))
seed_ii, by_place, EDGES, CYC, clock_sum, cen = (g[k] for k in ("seed_ii", "by_place", "EDGES", "CYC", "clock_sum",
                                                                "cen"))
UNIT, CUT, CUT2, CUT4, FIVE, KMIN, AMBIG, M2 = 1000, 3841, 5991, 9488, 5, 20, 2, 2996
out = []
say = out.append


def tally(d, v):
    d[v] = d.get(v, 0) + 1


def both(names):
    if "NOT SHOWN" in names:
        return "NOT SHOWN"
    if "NOT READ" in names:
        return "NOT READ"
    return "SHOWN"


# ================================================================ G first: the cuts, by whole numbers
SC = 10 ** 60


def atan_inv(x):
    total, k, power, sign = 0, 0, x, 1
    while True:
        t, _ = carry(SC, (k + k + 1) * power, 0)
        if t == 0:
            return total
        total += sign * t
        sign, k, power = -sign, k + 1, power * x * x


PI = 16 * atan_inv(5) - 4 * atan_inv(239)


def tail_within(c, nt):
    """True where P(chi-square on one degree > c / 1,000) <= 5 / (100 nt): erf(s)^2 >= (1 - a)^2 with s^2 = c / 2,000,
    erf(s)^2 = (2 c / pi) T^2, T = SUM (-1)^n (c / 2,000)^n / (n! (2n + 1)); whole numbers throughout."""
    T, fact, sign = 0, 1, 1
    for n in range(160):
        t, _ = carry(SC * c ** n, 2000 ** n * fact * (n + n + 1), 0)
        T += sign * t
        sign, fact = -sign, fact * (n + 1)
    return 2 * c * T * T * (20 * nt) ** 2 >= 1000 * PI * SC * (20 * nt - 1) ** 2


def cut_fw(nt):
    lo, hi = 3000, 20000
    while hi - lo > 1:
        mid, _ = carry(lo + hi, 2, 0)
        if tail_within(mid, nt):
            hi = mid
        else:
            lo = mid
    return hi


CUTS = {nt: cut_fw(nt) for nt in (1, 18, 20, 26, 30, 34)}
say(f"G. CUT_FW, the least whole thousandth c with P(chi-square on one degree > c) <= 5 / N_T per cent, by whole"
    f" numbers: {CUTS} (N_T 1 is the one-test 5 per cent point, cited 3,841)")

# ================================================================ A. R3, the conjunction, gated on (3b)


def e3_half(q, x, dial):
    """(3e), the past-2 table on one half: the rounds split by the landings at the two rounds before; in each class the
    landings against the passing's chances; X^2 = SUM (D O - X)^2 / V on four degrees against 9,488 thousandths."""
    if any(v not in (0, 1) for v in q) or any(v < 0 or v > dial for v in x):
        return ("NOT READ", "not a single, one-way side", None)
    O, X, V, N = [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]
    for r in range(2, len(q)):
        c = q[r - 2] + q[r - 2] + q[r - 1]
        O[c] += q[r]
        X[c] += x[r]
        V[c] += x[r] * (dial - x[r])
        N[c] += 1
    for c in range(4):
        if X[c] < FIVE * dial or N[c] * dial - X[c] < FIVE * dial or V[c] == 0:
            return ("NOT READ", f"past {['00', '01', '10', '11'][c]} expects fewer than five", O)
    X2 = sum(carry(UNIT * (dial * O[c] - X[c]) * (dial * O[c] - X[c]), V[c], 0)[0] for c in range(4))
    return ("SHOWN" if X2 <= CUT4 else "NOT SHOWN", X2, O)


def e3_given(q, x, dial):
    H, _ = carry(len(q), 2, 0)
    hv = [e3_half(q[:H], x[:H], dial), e3_half(q[H:H + H], x[H:H + H], dial)]
    return both([h[0] for h in hv]), hv


def r3(q, x, dial, kmin=KMIN):
    """R3 = (3b) and (3d) and (3e); (3d) and (3e) read only where (3b) is read, with no verdict of their own."""
    if x is None:
        return "NOT READ", {"3b": "NOT READ (no passing)"}
    vb, _ = b3_given(q, x, dial, kmin)
    if vb != "SHOWN":
        return vb, {"3b": vb}
    vd, _ = d3_given(q, x, dial, kmin)
    ve, he = e3_given(q, x, dial)
    return both([vd, ve]), {"3b": vb, "3d": vd, "3e": ve, "3e X^2": [h[1] for h in he]}


def read_r3(name, group, dial=D):
    rows = {"R3": {}, "(3b)": {}, "(3d) where (3b) SHOWN": {}, "(3e) where (3b) SHOWN": {}, "(3d) alone": {},
            "(3e) alone": {}}
    for q, x in group:
        v, parts = r3(q, x, dial)
        tally(rows["R3"], v)
        tally(rows["(3b)"], parts["3b"])
        if "3d" in parts:
            tally(rows["(3d) where (3b) SHOWN"], parts["3d"])
            tally(rows["(3e) where (3b) SHOWN"], parts["3e"])
        if len(group) <= 1000:
            tally(rows["(3d) alone"], d3_given(q, x, dial, KMIN)[0])
            tally(rows["(3e) alone"], e3_given(q, x, dial)[0])
    say(f"  {name}: " + "; ".join(f"{k} {dict(sorted(d.items()))}" for k, d in rows.items() if d))


say("A. R3 = (3b) and (3d) and (3e), gated on (3b); verdict counts:")
say(" A1. carried sides (each the carry with its tooth kept, no turn):")
read_r3("carried steady, 300 a round, halves of 2,000, 20 phases",
        [(carried_side(steady(300, 2000), ph), steady(300, 2000)) for ph in range(0, 1000, 50)])
read_r3("carried steady, 175 a round, halves of 2,000, 20 phases",
        [(carried_side(steady(175, 2000), ph), steady(175, 2000)) for ph in range(0, 1000, 50)])
for nm, xs in (("swing, halves of 2,000", swing(2000)), ("wide, halves of 1,000", wide(1000)),
               ("step, halves of 2,000", step(2000))):
    read_r3(f"carried moving, {nm}, 20 phases", [(carried_side(xs, ph), xs) for ph in range(0, 1000, 50)])


def blocks(xa, la, xb, lb, H):
    one = []
    while len(one) < H:
        one += [xa] * la + [xb] * lb
    return one[:H] + one[:H]


fam2 = []
for xa in (120, 130, 140, 150, 160, 170, 180):
    for xb in (40, 45, 50, 55, 60, 65, 70):
        for la in (20, 30, 40, 50, 60, 80):
            for lb in (20, 30, 40, 50, 60, 80):
                xs = blocks(xa, la, xb, lb, 350)
                for ph in (0, 400):
                    fam2.append((carried_side(xs, ph), xs))
read_r3("the HALF mathematician's two-level carried family at halves of 350, tooth phases 0 and 400 (3,528 records,"
        " his SHOWN example 120 x 50 then 60 x 20 at phase 400 among them)", fam2)
fam3 = []
for hi in (200, 250, 300):
    for mid in (90, 110):
        for lo in (30, 40, 50):
            for lh in (30, 60, 100):
                for lm in (30, 60, 100):
                    for ll in (30, 60, 100):
                        one = []
                        while len(one) < 2000:
                            one += [hi] * lh + [mid] * lm + [lo] * ll
                        xs = one[:2000] + one[:2000]
                        for ph in (0, 600):
                            fam3.append((carried_side(xs, ph), xs))
read_r3("the HALF mathematician's three-level carried family at halves of 2,000, phases 0 and 600 (972 records)", fam3)

say(" A2. fair draws (a stand-in draw at the passing's chance):")
seed = 27182


def fairs(xs, n):
    global seed
    grp = []
    for _ in range(n):
        q, seed = fair_side(seed, xs)
        grp.append((q, xs))
    return grp


for p, H in ((175, 2000), (190, 1000), (300, 2000), (70, 2560), (800, 400)):
    read_r3(f"fair, {p} a round, halves of {H}, 100 draws", fairs(steady(p, H), 100))
for nm, xs in (("swing, halves of 2,000", swing(2000)), ("wide, halves of 1,000", wide(1000)),
               ("step, halves of 2,000", step(2000))):
    read_r3(f"fair moving, {nm}, 100 draws", fairs(xs, 100))

say(" A3. the circulation's landings W (THIRD7's form at K = 3: the palindrome about the birth, the carry of y at 3D),"
    " at the click world's dial, against y over 3D:")
KEY = json.loads(HERE.joinpath("nl", "examples", "tensor24-click", "universe.json").read_text(encoding="utf-8"))[
    "chosen"]["key"]
DIAL3 = 9 * KEY
for a, H, lays in ((86, 2000, 3), (100, 2000, 3), (100, 400000, 2)):
    y = carry(a * DIAL3, UNIT, 0)[0]
    ys = [y] * (H + H)
    for turned in (True, False):
        for j in range(lays if turned else 1):
            Ws = circulation(ys, DIAL3, turned, j)
            v, parts = r3(Ws, ys, DIAL3)
            n_pairs = sum(1 for r in range(1, H + H) if Ws[r - 1] and Ws[r])
            n_trip = sum(1 for r in range(2, H + H) if Ws[r - 2] and Ws[r - 1] and Ws[r])
            say(f"  y {a} thousandths of 3D, halves of {H}, {'turned, lay ' + str(j) if turned else 'carried'}:"
                f" landings {sum(Ws)}, twice in a row {n_pairs}, three in a row {n_trip} (a fresh draw expects pairs x p ="
                f" {n_pairs * a} thousandths); R3 {v}, parts {parts}")
    if H == 400000:
        q, seed = fair_side(seed, [a] * (H + H))
        v, parts = r3(q, [a] * (H + H), D)
        say(f"  a fair stand-in draw at {a} a round, halves of {H}: R3 {v}, parts {parts}")


def matmul(A, B, m):
    return [[carry(sum(A[i][k] * B[k][j] for k in range(len(B))), m, 0)[1] for j in range(len(B[0]))]
            for i in range(len(A))]


def matpow(A, n, m):
    R = [[1 if i == j else 0 for j in range(len(A))] for i in range(len(A))]
    while n:
        n, bit = carry(n, 2, 0)
        if bit:
            R = matmul(R, A, m)
        A = matmul(A, A, m)
    return R


say(" A4. (3p), the period weighed:")
Lm = [[19, 60], [6, 19]]  # A B B A with A: tau += 3 eta, B: eta += 3 tau (THIRD7's L at K = 3)
Nn = 528480
LN = matpow(Lm, Nn, DIAL3)
big = [[19, 60, 19, 60], [6, 19, 6, 19], [0, 0, 1, 0], [0, 0, 0, 1]]  # [[L, L], [0, I]]: its N-th power holds S = L + ... + L^N
SN = matpow(big, Nn, DIAL3)
say(f"  at the click world's dial 3D = {DIAL3}: L^N mod 3D = {LN} (N = {Nn}); S = L + ... + L^N mod 3D ="
    f" {[row[2:] for row in SN[:2]]}, against D = {carry(DIAL3, 3, 0)[0]}; so the round's N-th power moves tau by D y,"
    f" and the period is N where 3 divides y, 3N otherwise")
for a in (86, 100):
    y = carry(a * DIAL3, UNIT, 0)[0]
    say(f"  y at {a} thousandths of 3D = {y}: 3 divides y {carry(y, 3, 0)[1] == 0}; the period"
        f" {Nn if carry(y, 3, 0)[1] == 0 else 3 * Nn} rounds, against the 800,000 rounds read above")


def member_states(y, dial3, rounds, turned=True):
    born, _ = carry(dial3 - 1, 2, 0)
    tau = eta = born
    seen, Ws = {(tau, eta): 0}, []
    for r in range(1, rounds + 1):
        if turned:
            eta = cen(eta - born + 3 * (tau - born), dial3, born) + born
            tau = cen(tau - born + 3 * (eta - born), dial3, born) + born
        n, tau = carry(y, dial3, tau)
        if turned:
            tau = cen(tau - born + 3 * (eta - born), dial3, born) + born
            eta = cen(eta - born + 3 * (tau - born), dial3, born) + born
        Ws.append(n)
        if (tau, eta) in seen:
            return r - seen[(tau, eta)], Ws
        seen[(tau, eta)] = r
    return None, Ws


def p3(Ws, P):
    """(3p): where the stretch holds two periods, NOT SHOWN where its second period repeats its first."""
    if P is None:
        return "NOT READ: no period carried"
    if len(Ws) < P + P:
        return f"the period {P} beyond the record's {len(Ws)} rounds: the readings necessary only"
    return "NOT SHOWN: the landings repeat with the period" if Ws[P:P + P] == Ws[:P] else "SHOWN: no repetition"


PS = {}
for dial3, a in ((3000, 257), (3001, 257)):
    y = carry(a * dial3, UNIT, 0)[0]
    P, _ = member_states(y, dial3, 200000)
    PS[dial3] = P
    Ws = circulation([y] * 4000, dial3, True, 0)
    say(f"  the stand-in dial 3D = {dial3}, y = {y}: the member's period {P} rounds; (3p) on 4,000 rounds: {p3(Ws, P)};"
        f" R3 {r3(Ws, [y] * 4000, dial3)[0]}")
Wf, seed = fair_side(seed, [257] * 4000)
say(f"  a fair stand-in draw at 257 a round, read with the period {PS[3000]} carried: {p3(Wf, PS[3000])}")

# ================================================================ B. R4 with the new (e)
SAVED = sys.argv
sys.argv = [SAVED[0], str(HERE.joinpath("nl", "src")), "40000", "unused"]
PO = HERE.joinpath("pair_order.py")
po = {"__file__": str(PO), "__name__": "pair_order_defs"}
exec(compile(PO.read_text(encoding="utf-8").split('out.append(f"R4 on records')[0], str(PO), "exec"), po)
sys.argv = SAVED
born, turn, click, HALF, SAME, PAIRS = (po[k] for k in ("born", "turn", "click", "HALF", "SAME", "PAIRS"))
chi2x2, order_z2 = po["chi2x2"], po["order_z2"]
DT = po["space"]["D"]
B2 = 2000 * 2000


def pair_step(alice, bob, pair, turned):
    turn(alice), turn(bob)
    if turned:
        turn(pair)
    a = 2 * click(HALF, alice, 0)
    b = 1 + 2 * click(HALF, bob, 0)
    sa = 2 * click(HALF, pair, 0) - 1
    same = click(SAME[abs(b - a)], pair, 1)
    return a, b, sa, sa * (2 * same - 1)


def rec_one(turned):
    alice, bob, pair = born(1), born(2), born(3)
    lines = []
    for t in range(PAIRS):
        a, b, sa, sb = pair_step(alice, bob, pair, turned)
        lines += [(t, "A", a, sa, 0), (t, "B", b, sb, 0)]
    return lines


def rec_two_firsts():
    alice, bob, hands = born(1), born(2), (born(3), born(4))
    lines, ev = [], 0
    for t in range(carry(PAIRS, 2, 0)[0]):
        for h, pair in enumerate(hands):
            a, b, sa, sb = pair_step(alice, bob, pair, False)
            lines += [(ev, "A", a, sa, h), (ev, "B", b, sb, h)]
            ev += 1
    return lines


def rec_parity():
    alice, bob, pair = born(1), born(2), born(3)
    lines, count = [], 0
    for t in range(PAIRS):
        turn(alice), turn(bob)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        count += click(HALF, pair, 0)
        sa = 1 - 2 * carry(count, 2, 0)[1]
        same = click(SAME[abs(b - a)], pair, 1)
        lines += [(t, "A", a, sa, 0), (t, "B", b, sa * (2 * same - 1), 0)]
    return lines


def rec_period4():
    alice, bob, pair = born(1), born(2), born(3)
    lines = []
    for t in range(PAIRS):
        turn(alice), turn(bob)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        sa = 1 - 2 * carry(carry(t, 4, 0)[1], 2, 0)[0]
        same = click(SAME[abs(b - a)], pair, 1)
        lines += [(t, "A", a, sa, 0), (t, "B", b, sa * (2 * same - 1), 0)]
    return lines


def rec_echo():
    """A's outcome its own previous setting (no draw at A); the hand turned, so B draws by the hand's share."""
    alice, bob, pair = born(1), born(2), born(3)
    lines, prev = [], 0
    for t in range(PAIRS):
        turn(alice), turn(bob), turn(pair)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        sa = 1 if prev == 0 else -1
        click(HALF, pair, 0)
        same = click(SAME[abs(b - a)], pair, 1)
        lines += [(t, "A", a, sa, 0), (t, "B", b, sa * (2 * same - 1), 0)]
        prev = a
    return lines


def rec_local():
    """Each place draws its outcome from its own turned teeth alone (a member local to its place, a shared birth)."""
    alice, bob, ta, tb = born(1), born(2), born(5), born(6)
    lines = []
    for t in range(PAIRS):
        turn(alice), turn(bob), turn(ta), turn(tb)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        lines += [(t, "A", a, 2 * click(HALF, ta, 0) - 1, 0), (t, "B", b, 2 * click(HALF, tb, 0) - 1, 0)]
    return lines


def order_e(xs, cut):
    """(e) on one source's outcomes at one place in one half: lag-1 and R2's past ladder, gated on power."""
    n = len(xs)
    plus = sum(1 for v in xs if v > 0)
    if plus == 0 or plus == n:
        return ("NOT SHOWN", "the outcomes do not vary")
    maj, mnr = max(plus, n - plus), min(plus, n - plus)
    if th(maj ** 7 * mnr ** 2, n ** 8) < M2 or mnr * mnr < FIVE * n:
        return ("NOT READ", "below the power gate")
    r1, z = order_z2(xs)
    amb = [ambiguous(xs, L) for L in (1, 2, 4, 8)]
    ok = z <= cut and all(v >= AMBIG for v in amb)
    return ("SHOWN" if ok else "NOT SHOWN", r1, z, amb)


def r4f(lines):
    joined = {}
    for t, place, setting, outcome, src in lines:
        joined.setdefault(t, {})[place] = (setting, outcome, src)
    trials = [(t, v["A"], v["B"]) for t, v in sorted(joined.items()) if set(v) == {"A", "B"}]
    sources = sorted({A[2] for _, A, _ in trials})
    nt = 2 * (5 + 2 + 4 + 1 + 1 + 2 * len(sources))
    cut = CUTS[nt]
    idx_a, idx_b = {2: 0, 0: 1}, {1: 0, 3: 1}
    # R3 at each place, on its +1 landings in the pair events' order, against its passing (HALF over D, a board field)
    r3v = {}
    for place, k in (("A", 1), ("B", 2)):
        q = [1 if (A if k == 1 else Bb)[1] > 0 else 0 for _, A, Bb in trials]
        r3v[place] = r3(q, [HALF] * len(q), DT)
    gate = r3v["A"][0] == "SHOWN" and r3v["B"][0] == "SHOWN"
    H, _ = carry(len(trials), 2, 0)
    halves = []
    for half in (trials[:H], trials[H:H + H]):
        cnt, num = {}, {}
        for _, A, Bb in half:
            kk = (idx_a[A[0]], idx_b[Bb[0]])
            cnt[kk] = cnt.get(kk, 0) + 1
            num[kk] = num.get(kk, 0) + A[1] * Bb[1]
        E = {kk: th(num[kk], cnt[kk]) for kk in cnt}
        S = E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)]
        S_lo = S - 1
        var = sum(carry(UNIT * UNIT - E[kk] * E[kk], cnt[kk], 0)[0] for kk in cnt)
        m2, _ = carry(cut * var, UNIT, 0)
        reach = not (m2 < B2 and (B2 - m2) * (B2 - m2) > 4 * B2 * m2)  # 2,000 + m reaches the hand's bound
        va = "NOT READ" if reach else ("SHOWN" if S_lo > 2000 and (S_lo - 2000) * (S_lo - 2000) > m2 else "NOT SHOWN")
        Lq = S_lo * S_lo + m2 - 2 * B2
        past = S_lo > 0 and S_lo * S_lo > m2 and Lq > 0 and Lq * Lq > 4 * S_lo * S_lo * m2
        zc = []
        for me in (1, 2):
            mine, farx = (idx_a, idx_b) if me == 1 else (idx_b, idx_a)
            for s_me in (0, 1):
                n0 = n1 = p0 = p1 = 0
                for _, A, Bb in half:
                    own, other = (A, Bb) if me == 1 else (Bb, A)
                    if mine[own[0]] != s_me:
                        continue
                    plus = 1 if own[1] > 0 else 0
                    if farx[other[0]] == 0:
                        n0, p0 = n0 + 1, p0 + plus
                    else:
                        n1, p1 = n1 + 1, p1 + plus
                n, P = n0 + n1, p0 + p1
                den = n0 * n1 * P * (n - P)
                zc.append(None if den == 0 else carry(UNIT * (p0 * n1 - p1 * n0) ** 2 * n, den, 0)[0])
        vc = ("NOT READ" if not gate else
              ("SHOWN" if all(z is not None and z <= cut for z in zc) else "NOT SHOWN"))
        sa_set = [idx_a[A[0]] for _, A, _ in half]
        sb_set = [idx_b[Bb[0]] for _, _, Bb in half]
        a_out = [1 if A[1] > 0 else 0 for _, A, _ in half]
        b_out = [1 if Bb[1] > 0 else 0 for _, _, Bb in half]
        mi = []
        for x, yv in ((sa_set, sb_set), (sa_set[1:], a_out[:-1]), (sa_set[1:], b_out[:-1]), (sb_set[1:], a_out[:-1]),
                      (sb_set[1:], b_out[:-1]), (sa_set[:-1], a_out[1:]), (sb_set[:-1], b_out[1:])):
            c4 = [0, 0, 0, 0]
            for u, v in zip(x, yv):
                c4[u + u + v] += 1
            mi.append(chi2x2(*c4))
        v2 = "SHOWN" if all(z is not None and z <= cut for z in mi[:5]) else "NOT SHOWN"
        vown = "SHOWN" if all(z is not None and z <= cut for z in mi[5:]) else "NOT SHOWN"
        ev = []
        for s in sources:
            for k in (1, 2):
                xs = [(A if k == 1 else Bb)[1] for _, A, Bb in half if A[2] == s]
                ev.append(order_e(xs, cut))
        ve = both([e[0] for e in ev])
        halves.append({"(a)": va, "limit": "NOT SHOWN" if past else "SHOWN", "(c)": vc, "2 x 2": v2,
                       "own past settings": vown, "(e)": ve, "S": S, "own z^2": mi[5:], "e": ev})
    parts = {k: both([h[k] for h in halves]) for k in ("(a)", "limit", "(c)", "2 x 2", "own past settings", "(e)")}
    parts["(b)"] = parts["(d)"] = "NOT READ"
    click_parts = both([parts[k] for k in ("(a)", "limit", "(c)", "2 x 2", "own past settings", "(e)")])
    return nt, cut, r3v, parts, click_parts, both(list(parts.values())), halves


say(f"B. R4 with the new (e), on records of {PAIRS} pair events (20,000 a half); each landing names its pair event and its"
    f" pair source; each place's passing, HALF over D = {DT}, carried as a board field:")
for label, lines in (("the third click (the hand turned)", rec_one(True)),
                     ("the first click (the hand unturned, no draw)", rec_one(False)),
                     ("two first clicks interleaved (two sources, no draw)", rec_two_firsts()),
                     ("the parity first click (no draw)", rec_parity()),
                     ("a fixed order of period four at A (no draw)", rec_period4()),
                     ("A's outcome its own previous setting (no draw at A)", rec_echo()),
                     ("a draw at each place alone (a member local to its place)", rec_local())):
    nt, cut, r3v, parts, cp, r4v, halves = r4f(lines)
    say(f"  {label}: N_T {nt}, CUT_FW {cut}; R3 at A {r3v['A']}, at B {r3v['B']}; parts {parts}; the click"
        f" parts {cp}; R4 {r4v}")
    for h, hh in zip(("first half", "second half"), halves):
        es = [(e[0], e[1], e[2], e[3]) if len(e) == 4 else e for e in hh["e"]]
        say(f"    {h}: S {hh['S']}; own past settings z^2 {hh['own z^2']}; (e) per source and place (verdict, lag-1"
            f" per mille, z^2, R2's ladder at 1, 2, 4, 8): {es}")

# ================================================================ C. the seed test's (ii), its no in THIRD7's twin


def member_board(rounds, turned, hidden):
    """A stand-in board of two Node-clocks: 0, the stand-in triangle under THIRD7's form (decode3e's form 2) with one
    hidden unit in the triangle's twin; 1, a lone edge (two clocks). Records in the run tool's format."""
    dial = 3 * D
    born, _ = carry(dial - 1, 2, 0)
    k, kT, eT = [born, born, born], born, born + hidden
    k1, _ = carry(D - 1, 2, 0)
    lines, sides, places, passing, teeth = [], [], {}, [], []
    for r in range(rounds):
        x = [-230, -410, 77]
        y = sum(c * v for c, v in zip(CYC, x))
        passing.append((x, y))
        before = list(k)
        qe = []
        for e in range(3):
            c, k[e] = carry(3 * x[e] - CYC[e] * y, dial, k[e])
            qe.append(c)
        if turned:
            eT = cen(eT - born + 3 * (kT - born), dial, born) + born
            kT = cen(kT - born + 3 * (eT - born), dial, born) + born
        n, kT = carry(y, dial, kT)
        if turned:
            kT = cen(kT - born + 3 * (eT - born), dial, born) + born
            eT = cen(eT - born + 3 * (kT - born), dial, born) + born
        qe = [v + c * n for v, c in zip(qe, CYC)]
        teeth.append((before, list(k)))
        if any(qe):
            places[(r, 0)] = qe
            for e, v in enumerate(qe):
                if v:
                    sides.append((r, 0, e, v))
            for i in (2, 3, 4):
                if clock_sum(qe, i):
                    lines.append((r, 0, i, clock_sum(qe, i)))
        c1, k1 = carry(x[0], D, k1)
        if c1:
            places[(r, 1)] = [c1, 0, 0]
            sides.append((r, 1, 0, c1))
            lines += [(r, 1, 2, c1), (r, 1, 3, -c1)]
    return {"header": {"hidden": [0, "twin"] if hidden else None}, "lines": lines, "sides": sides}, places, passing, \
        teeth, dial


def seed_ii_f(a, b):
    ha, hb = a["header"]["hidden"], b["header"]["hidden"]
    if ha is not None and hb is not None and ha != hb:
        return "NOT READ: the two headers name different units"
    return seed_ii(a, b)[0]


say("C. The seed test's (ii), 'the clicks depend on the unit, at its clock only', on a stand-in board of two Node-clocks"
    " (0: a triangle under THIRD7's form; 1: a lone edge), 2,000 rounds, one hidden unit in the triangle's twin:")
for turned, label in ((True, "the twin turned (THIRD7's form)"), (False, "the twin never turned (the structural no)")):
    a, pa, pas, tee, dial = member_board(2000, turned, 0)
    b, pb, _, teb, _ = member_board(2000, turned, 1)
    v = seed_ii_f(a, b)
    worst, rf, idle, against = checks_b_c(pb, pas, teb, dial, 2000)
    books = "SHOWN" if rf is None and worst < 2000 else "NOT SHOWN"
    apart = len(set(a["sides"]) ^ set(b["sides"]))
    lines_apart = len(set(a["lines"]) ^ set(b["lines"]))
    say(f"  {label}: (ii) {v}; sides apart {apart}, lines apart {lines_apart}; the books (L2 every round, L3 within"
        f" its teeth: {worst} thousandths of a dial against 2,000) {books}; accepted"
        f" {v == 'SHOWN' and books == 'SHOWN'}")
b2 = json.loads(json.dumps(b))
b2["header"]["hidden"] = [1, "twin"]
say(f"  its no, the two headers naming different units: {seed_ii_f(b2, b if b['header']['hidden'] else a)}")
recs = {nm: json.loads(HERE.joinpath("st2run_1", nm).read_text(encoding="utf-8"))
        for nm in ("click_200_0_laid.json", "click_200_0_hidden01.json", "click_200_1_laid.json",
                   "click_200_1_hidden01.json")}
for turned, label in ((1, "stage 1's turn"), (0, "the first click")):
    a, b = recs[f"click_200_{turned}_laid.json"], recs[f"click_200_{turned}_hidden01.json"]
    v = seed_ii_f(a, b)
    rec_b = a
    dial_b, rounds = rec_b["header"]["dial"], rec_b["header"]["rounds"]
    sides_at = {}
    for t, x, e, c in rec_b["sides"]:
        if x == 0:
            sides_at.setdefault(t, [0, 0, 0])[e] += c
    tot, swp, worst = {2: 0, 3: 0, 4: 0}, {2: 0, 3: 0, 4: 0}, 0
    for t in range(rounds):
        qe = sides_at.get(t, [0, 0, 0])
        xx = rec_b["passing"][t][0]
        for i in (2, 3, 4):
            tot[i] += clock_sum(qe, i)
            swp[i] += sum((v_ if aa == i else (-v_ if bb == i else 0)) for (aa, bb), v_ in zip(EDGES, xx))
            worst = max(worst, abs(dial_b * tot[i] - swp[i]))
    books = "SHOWN" if worst < 2 * dial_b else "NOT SHOWN"
    say(f"  the frozen board records, {label}: (ii) {v}; L3 at Node-clock 0 {th(worst, dial_b)} thousandths of a dial"
        f" against 2,000: {books}; accepted as a third click's form {v == 'SHOWN' and books == 'SHOWN'}")

# ================================================================ D. the three kinds at ed6a1f225


def kinds_read_f(rec):
    """Each place by its structure; a place with an edge on two triangles reads NOT READ, named."""
    keep, refused = {}, []
    for key, ls in rec.items():
        clocks = sorted(set(ls) | {u for _, (q, s) in ls.items() for u in s})
        edges = {tuple(sorted((t, u))) for t, (q, s) in ls.items() for u in s}
        tri = [(i, j, k) for i in clocks for j in clocks for k in clocks if i < j < k and (i, j) in edges and
               (i, k) in edges and (j, k) in edges]
        on = {e: sum(1 for (i, j, k) in tri if e in ((i, j), (i, k), (j, k))) for e in edges}
        if any(v >= 2 for v in on.values()):
            refused.append(key)
        else:
            keep[key] = ls
    count, verdict, circ = kinds_read(keep)
    return refused, count, verdict


def place_lines(edge_q):
    ls = {}
    for (a, b), v in edge_q.items():
        ls.setdefault(a, {})[b] = v
        ls.setdefault(b, {})[a] = -v
    return {t: (sum(s.values()), s) for t, s in ls.items()}


places, passing, teeth, dial, Ws = triangle(2, 400, 200)
rec = lines_of(places)
rec[(5, 7)] = place_lines({(0, 1): 1, (0, 2): 0, (1, 2): -1, (1, 3): 1, (2, 3): 0})
rec[(6, 8)] = place_lines({(0, 1): 1, (0, 2): 0, (0, 3): 0, (1, 2): -1, (1, 3): 0, (2, 3): 1})
refused, count, verdict = kinds_read_f(rec)
say(f"D. The three kinds, a place with an edge on two triangles NOT READ: the stand-in triangle's record with two such"
    f" places added (two triangles sharing an edge; four clocks pairwise joined): NOT READ at {refused}; the rest"
    f" {count}, {verdict}")
say(f"  the frozen records hold one triangle a Node-clock, so no place there is refused: the run tool's structure is"
    f" one triangle (edges {list(EDGES)}) at each Node-clock")
for R in (400, 4000):
    places, passing, teeth, dial, Ws = triangle(2, R, R)
    mins = cq_eq = cq_one = worst = run = run_worst = 0
    for r in range(R):
        qe = places.get((r, 0), [0, 0, 0])
        mins += g["whole_circulations"](qe)[0]
        cq = sum(c * v for c, v in zip(CYC, qe))
        cq_eq += int(cq == 3 * Ws[r])
        cq_one += int(abs(cq - 3 * Ws[r]) <= 1)
        worst = max(worst, abs(cq - 3 * Ws[r]))
        run += cq - 3 * Ws[r]
        run_worst = max(run_worst, abs(run))
    say(f"  W from the record, {R} rounds of the stand-in triangle (never idle): the tooth lands {sum(Ws)}; the record"
        f" alone by the least circulation reads {mins} (a lower count); by c . q, c . q = 3 W in {cq_eq} of {R} rounds"
        f" and within one of 3 W in {cq_one},"
        f" |c . q - 3 W| at most {worst} a round, the running |SUM c . q - 3 SUM W| at most {run_worst} (DERIVED: at"
        f" most 2)")
places, passing, teeth, dial, Ws = triangle(2, 400, 200)


def lone_exact(places, passing, rounds):
    k, _ = carry(D - 1, 2, 0)
    for r in range(rounds):
        c, k = carry(passing[r][0][0], D, k)
        if places.get((r, 1), [0, 0, 0])[0] != c:
            return f"NOT SHOWN at round {r}"
    return "SHOWN"


forged = dict(places)
r0 = next(r for r in range(400) if (r, 1) in forged and (r + 1, 1) not in forged)
forged[(r0 + 1, 1)] = forged.pop((r0, 1))
say(f"  the lone edge recomputed exactly from its passing and the birth: the record {lone_exact(places, passing, 400)};"
    f" one landing moved a round later (round {r0} to {r0 + 1}): exact {lone_exact(forged, passing, 400)}; the old"
    f" within-a-dial check {g['lone_edge'](forged, passing, 400)} thousandths of a dial (passes, under 1,000)")



def guard(rec):
    """Writer E's guard (sides.paired), as a stand-in: every side's mate opposite, every line its sides' sum; a record
    that fails is malformed and refused at read with its cause, never a NOT SHOWN."""
    for key, ls in sorted(rec.items()):
        for t, (q, sd) in ls.items():
            if q != sum(sd.values()):
                return f"REFUSED at read: the line of clock {t} at {key} is off its sides' sum"
            for u, v in sd.items():
                if ls.get(u, (0, {}))[1].get(t) != -v:
                    return f"REFUSED at read: the side {t} to {u} at {key} has no opposite mate"
    return "read"


def met(rec):
    """Meetings from what passes (A4's shadow.met): a side at q 0 is no meeting; 'three clocks meet' where three clocks
    are pairwise joined by edges that pass a quantum in that round at that place."""
    two = three = 0
    for key, ls in rec.items():
        edges = {tuple(sorted((t, u))) for t, (q, sd) in ls.items() for u, v in sd.items() if v}
        clocks = sorted({c for e in edges for c in e})
        tri = any((i, j) in edges and (i, k) in edges and (j, k) in edges for i in clocks for j in clocks for k in clocks
                  if i < j < k)
        three += int(tri)
        two += int(bool(edges) and not tri)
    return two, three


places, passing, teeth, dial, Ws = triangle(2, 400, 200)
rec = lines_of(places)
say(f"D2. Meetings from what passes, the stand-in triangle's 400 rounds: the guard {guard(rec)}; places with a meeting"
    f" and no three clocks meeting, and places where three clocks meet: {met(rec)}; places of the triangle's structure"
    f" (a board check) with any passing: {sum(1 for (r, x) in rec if x == 0)}")
bad = lines_of(places)
k0 = next(k for k in sorted(bad) if k[1] == 1)
bad[k0][2] = (bad[k0][2][0] + 1, bad[k0][2][1])
say(f"  a line one off at a two-clock place: {guard(bad)}")
bad = lines_of(places)
k1 = next(k for k in sorted(bad) if k[1] == 0 and any(places[k]))
sd = dict(bad[k1][2][1])
sd[3] += 1
bad[k1][2] = (sum(sd.values()), sd)
say(f"  a broken mate (clock 2's side to 3 one up, its line kept its sides' sum): {guard(bad)}")
for nm in ("click_200_0_laid.json", "click_200_1_laid.json"):
    at = {}
    for t, x, e, c in recs[nm]["sides"]:
        if c:
            at.setdefault((t, x), set()).add(e)
    say(f"  the frozen board record {nm}: places with a passing {len(at)}; places where three clocks meet (all three"
        f" edges pass) {sum(1 for v in at.values() if len(v) == 3)}")

# ================================================================ E. each clock's own count, and D4
say("E. Each clock's own count: its own lines in the record's order (the Boss's ruling on FACE2); D4, no round read as a"
    " duration:")
for nm in ("click_200_0_laid.json", "click_200_1_laid.json"):
    rec_b = recs[nm]
    per = {}
    for t, x, tr, v in rec_b["lines"]:
        per.setdefault((x, tr), []).append(t)
    differ = sum(1 for ts in per.values() if len(ts) > 1 and len(ts) - 1 != ts[-1] - ts[0])
    at0 = {tr: (len(ts) - 1, ts[-1] - ts[0]) for (x, tr), ts in sorted(per.items()) if x == 0}
    say(f"  {nm}: clocks with lines {len(per)}; clocks whose own count between their first and last lines differs from"
        f" the rounds between them {differ}; at Node-clock 0 (clock: own count, rounds between) {at0}")
READINGS = {"(3b)": ["rounds (a board check)"], "(3d)": ["rounds (a board check)"], "(3e)": ["rounds (a board check)"],
            "R2": ["the round standing in for the clock's own count"], "C-a": ["own count"], "C-c": ["own count"],
            "C-a mutant": ["round difference"], "C-a face mutant": ["face difference"]}


def d4(name):
    bad = [i for i in READINGS[name] if i in ("round difference", "face difference")]
    return f"refused by D4: reads a {bad[0]} as a duration" if bad else "allowed"


say("  D4 on the decoder's readings: " + "; ".join(f"{k} {d4(k)}" for k in READINGS))
for nm in ("click_200_0_laid.json",):
    across = sum(1 for ln in recs[nm]["lines"] if len(ln) > 4)
    say(f"  rule L on the frozen board records: across sides {across}: no Mesh meeting, so light's lines NOT SHOWN and"
        f" C-a to C-e NOT READ there")



def one_key(header):
    """One key per record (KEY3's physicist, m5): a card whose key is off the header's dial is refused at read, named."""
    off = [c for c in header.get("cards", []) if c["key"] != header["dial"]]
    if off:
        return f"REFUSED at read: the card of train {off[0]['train']} has key {off[0]['key']} off the header's dial"
    return "read"


for nm in ("click_200_0_laid.json", "click_200_1_laid.json"):
    hd = recs[nm]["header"]
    say(f"  one key per record, {nm}: {one_key(hd)} (one dial {hd['dial']}, no card); the dial is 3 times the world's"
        f" key {KEY} read from its file: {hd['dial'] == 3 * KEY}")
hd = {"dial": 3 * KEY, "cards": [{"train": 0, "key": 3 * KEY}, {"train": 1, "key": 3 * KEY}]}
say(f"  a stand-in header with two cards at the dial: {one_key(hd)}; with train 1's card two above it:"
    f" {one_key(dict(hd, cards=[hd['cards'][0], {'train': 1, 'key': 3 * KEY + 2}]))}")

# ================================================================ F. the conversions' checks on hand-built counts


def own_count_at(lines_of_clock, r):
    return sum(1 for t in lines_of_clock if t < r)


def ca(A_rounds, give, take, B_rounds, b1, b2):
    t1, t2 = own_count_at(A_rounds, give), own_count_at(A_rounds, take)
    hold = own_count_at(B_rounds, b2) - own_count_at(B_rounds, b1)
    return t1 + t2, t2 - t1 - hold


pattern = [r for r in range(60) if carry(r, 3, 0)[1] != 2]
A_l, B_l = list(pattern), list(pattern)
ab = ca(A_l, 9, 21, B_l, 15, 16)
ba = ca(B_l, 9, 21, A_l, 15, 16)
say(f"F. C-a on hand-built counts (two clocks of one kind at rest, lines 2 of every 3 rounds; a test of the check's"
    f" logic): 2t, 2r from A to B {ab}, from B to A {ba}: one 2r within one count {abs(ab[1] - ba[1]) <= 1}; the"
    f" rounds give 2r {21 - 9 - 1} where the own count gives {ab[1]} (D4 bites)")
ba_f = ca(B_l, 9, 24, A_l, 15, 16)
say(f"  its no, the return leg forged three rounds longer: 2r {ab[1]} against {ba_f[1]}: one 2r"
    f" {abs(ab[1] - ba_f[1]) <= 1}")


def k_of(em, rc):
    return (rc[1] - rc[0], em[1] - em[0])


kab, kba = k_of((0, 10), (0, 20)), k_of((0, 10), (0, 20))
kbc, kac = k_of((0, 10), (0, 15)), k_of((0, 10), (0, 30))
say(f"  C-c on hand-built counts: k_AB {kab}, k_BA {kba}: reciprocal {kab[0] * kba[1] == kab[1] * kba[0]}; k_BC {kbc},"
    f" k_AC {kac}: k_AC = k_AB k_BC {kac[0] * kab[1] * kbc[1] == kac[1] * kab[0] * kbc[0]}; its no, k_AC forged to"
    f" (31, 10): {31 * kab[1] * kbc[1] == 10 * kab[0] * kbc[0]}")

kab2, kba2, kbc2, kca2 = (12, 10), (10, 12), (15, 12), (10, 15)
close = kab2[0] * kbc2[0] * kca2[0] == kab2[1] * kbc2[1] * kca2[1]
recip = kab2[0] * kba2[0] == kab2[1] * kba2[1]
say(f"  C-d on hand-built counts (three clocks at rest): k_AB {kab2}, k_BA {kba2}: k_AB k_BA = 1 {recip}; k_BC {kbc2},"
    f" k_CA {kca2}: the closure k_AB k_BC k_CA = 1 {close}; A deeper than B (k_AB above one) {kab2[0] > kab2[1]}; its no,"
    f" k_CA forged to (11, 15): {kab2[0] * kbc2[0] * 11 == kab2[1] * kbc2[1] * 15}")
HERE.joinpath(OUTNAME).write_text("\n".join(out) + "\n", encoding="utf-8")
