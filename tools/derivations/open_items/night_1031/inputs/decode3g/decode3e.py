"""DECODE3e's measurements of its changed rules. Whole numbers; every division is Rule3's carry; no random module.

Stand-in single, one-way sides (named stand-ins, the dial D = 1,000, so a round's chance is its passing over the dial,
p_r = x_r / D, in thousandths):
- carried sides: Rule3's carry with the tooth kept, x_r a round, 20 phases of the tooth (no choice);
- fair draws: a 64-bit carry sequence's top 32 bits, landing with chance x_r / D (a stand-in draw);
- each at a steady passing or at a moving one (swing: 50 up to 300 and back within each half, the HALF physicist's;
  wide: 300 up to 700 over the first half and back over the second, DECODE3c's; step: 100 then 250 within each half).
The rules read (DECODE3e):
- (3b) against the board's passing: at the window ladder's top w, a window is read where its expected landings
  X_k / D and misses (w D - X_k) / D are both at least five (Pearson's rule on both cells); per window
  z_k = (D C_k - X_k)^2 / V_k with V_k = SUM x_r (D - x_r); Z = SUM z_k; Var Z = SUM (2 + W4_k / V_k^2),
  W4_k = SUM x_r (D - x_r) (D^2 - 6 x_r (D - x_r)); z^2 = (Z - K)^2 / Var Z against CUT; NOT READ below K_MIN windows
  read, and NOT READ where the carried bound B = SUM D^2 / V_k (rounded up) does not itself read past CUT;
- (3d) against the board's passing: L = the half's rounds over its expected landings (whole part); the gaps from each
  landing at least 2 L rounds before the half's end fall in three cells (at most L, L to 2 L, above 2 L), each gap's
  cell chances from the passing (the products of 1 - p_r); NOT READ below K_MIN gaps or where a cell expects fewer
  than five; NOT SHOWN where the half's gaps take two values or fewer; else Pearson's three-cell sum against 5,991;
- R2 gated on (3b) in that form, and E2 = n (n - 1) / H at least M2 = 2,996;
- beside them, DECODE3d's (3b) (the steady reference) and DECODE3b's (3d) (one point), as frozen.
Then: R4's power condition on (a), root-free; the seed test's click part of (ii) on the run tool's board records
(st2run_1/, pairs_gen.py); and the three kinds of event with the checks (b) and (c), on a stand-in triangle and on the
board records. argv: the output name."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

UNIT, CUT, CUT2, FIVE, KMIN, AMBIG, M2 = 1000, 3841, 5991, 5, 20, 2, 2996
PASTS = (1, 2, 4, 8)
MUL, ADD, MOD, HI = 6364136223846793005, 1442695040888963407, 18446744073709551616, 4294967296
D = 1000
out = []
say = out.append


def th(num, den):
    return None if den == 0 else carry(UNIT * num, den, 0)[0]


def up(num, den):
    return carry(num + den - 1, den, 0)[0]


# ---------------------------------------------------------------- the stand-in sides and their passings

def lcg(s):
    _, s = carry(s * MUL + ADD, MOD, 0)
    hi, _ = carry(s, HI, 0)
    _, u = carry(hi, UNIT, 0)
    return u, s


def fair_side(seed, xs):
    qs, s = [], seed
    for x in xs:
        u, s = lcg(s)
        c, _ = carry(u + x, UNIT, 0)
        qs.append(c)
    return qs, s


def carried_side(xs, tooth):
    qs, k = [], tooth
    for x in xs:
        c, k = carry(x, D, k)
        qs.append(c)
    return qs


def steady(p, H):
    return [p] * (H + H)


def swing(H):
    half, _ = carry(H, 2, 0)
    one = []
    for r in range(H):
        u = r if r < half else H - r
        v, _ = carry(250 * u, half, 0)
        one.append(50 + v)
    return one + one


def wide(H):
    xs = [300 + carry(400 * r, H, 0)[0] for r in range(H)]
    return xs + [700 - carry(400 * r, H, 0)[0] for r in range(H)]


def step(H):
    half, _ = carry(H, 2, 0)
    one = [100] * half + [250] * (H - half)
    return one + one


# ---------------------------------------------------------------- (3b)

def ladder_top(H, kmin):
    w = 1
    while True:
        k2, _ = carry(H, w + w, 0)
        if k2 < kmin:
            return w
        w = w + w


def b3_given_half(q, x, dial, kmin):
    """(3b) against the board's passing on one half: (verdict, z^2, windows read, Z / K in thousandths)."""
    H = len(q)
    if any(v < 0 or v > dial for v in x):
        return ("NOT READ", None, 0, None)
    w = ladder_top(H, kmin)
    K, _ = carry(H, w, 0)
    if K < kmin:
        return ("NOT READ", None, 0, None)
    Z = V = B = Kr = 0
    for j in range(K):
        xs, qs = x[j * w:j * w + w], q[j * w:j * w + w]
        X = sum(xs)
        Vk = sum(v * (dial - v) for v in xs)
        if X < FIVE * dial or w * dial - X < FIVE * dial or Vk == 0:
            continue
        W4 = sum(v * (dial - v) * (dial * dial - 6 * v * (dial - v)) for v in xs)
        C = sum(qs)
        Z += carry(UNIT * (dial * C - X) * (dial * C - X), Vk, 0)[0]
        V += 2 * UNIT + carry(UNIT * W4, Vk * Vk, 0)[0]
        B += up(UNIT * dial * dial, Vk)
        Kr += 1
    if Kr < kmin:
        return ("NOT READ", None, Kr, None)
    if B >= UNIT * Kr or carry((UNIT * Kr - B) * (UNIT * Kr - B), V, 0)[0] <= CUT:
        return ("NOT READ", None, Kr, None)
    z2, _ = carry((Z - UNIT * Kr) * (Z - UNIT * Kr), V, 0)
    return ("SHOWN" if z2 <= CUT else "NOT SHOWN", z2, Kr, carry(Z, Kr, 0)[0])


def both(halves):
    names = [h[0] for h in halves]
    if "NOT READ" in names:
        return "NOT READ"
    return "SHOWN" if names == ["SHOWN", "SHOWN"] else "NOT SHOWN"


def b3_given(q, x, dial, kmin):
    if x is None:
        return "NOT READ", []
    H, _ = carry(len(q), 2, 0)
    hv = [b3_given_half(q[:H], x[:H], dial, kmin), b3_given_half(q[H:H + H], x[H:H + H], dial, kmin)]
    return both(hv), hv


def b3_old(q, kmin):
    """DECODE3d's (3b) as frozen: the steady reference F0 = 1,000 - p, the rule of five on landings only."""
    H, _ = carry(len(q), 2, 0)
    res = []
    for half in (q[:H], q[H:H + H]):
        w = ladder_top(len(half), kmin)
        K, _ = carry(len(half), w, 0)
        counts = [sum(half[j * w:j * w + w]) for j in range(K)]
        s1, s2 = sum(counts), sum(c * c for c in counts)
        if K < kmin or UNIT * s1 < FIVE * UNIT * K:
            res.append(("NOT READ",))
            continue
        F, F0 = th(K * s2 - s1 * s1, K * s1), UNIT - th(s1, K * w)
        z2, _ = carry(UNIT * (F - F0) * (F - F0) * (K - 1), 2 * F0 * F0, 0)
        res.append(("SHOWN" if z2 <= CUT else "NOT SHOWN",))
    return both(res)


# ---------------------------------------------------------------- (3d)

def d3_given_half(q, x, dial, kmin):
    """(3d) against the board's passing on one half: (verdict, reason or X^2, L, gaps read)."""
    H = len(q)
    if any(v < 0 or v > dial for v in x):
        return ("NOT READ", "a passing outside one quantum", None, 0)
    X = sum(x)
    if X == 0:
        return ("NOT READ", "no passing", None, 0)
    L, _ = carry(H * dial, X, 0)
    if L + L > H - 1:
        return ("NOT READ", "the passing too slow for the half", L, 0)
    lands = [t for t, c in enumerate(q) if c]
    gaps = [b - a for a, b in zip(lands, lands[1:])]
    if len(gaps) < kmin:
        return ("NOT READ", "fewer than K_MIN gaps", L, len(gaps))
    Q = dial ** (L + L)
    DL = dial ** L
    O, N, n = [0, 0, 0], [0, 0, 0], 0
    for i, t in enumerate(lands):
        if t + L + L > H - 1:
            break
        g = lands[i + 1] - t if i + 1 < len(lands) else L + L + 1
        O[0 if g <= L else (1 if g <= L + L else 2)] += 1
        sL = 1
        for j in range(1, L + 1):
            sL *= dial - x[t + j]
        s2L = sL
        for j in range(L + 1, L + L + 1):
            s2L *= dial - x[t + j]
        N[0] += Q - sL * DL
        N[1] += sL * DL - s2L
        N[2] += s2L
        n += 1
    if any(Nc < FIVE * Q for Nc in N):
        return ("NOT READ", "a cell expects fewer than five", L, n)
    if len(set(gaps)) <= 2:
        return ("NOT SHOWN", "gaps take two values or fewer", L, n)
    X2 = sum(carry(UNIT * (O[c] * Q - N[c]) * (O[c] * Q - N[c]), Q * N[c], 0)[0] for c in range(3))
    return ("SHOWN" if X2 <= CUT2 else "NOT SHOWN", X2, L, n)


def d3_given(q, x, dial, kmin):
    if x is None:
        return "NOT READ", []
    H, _ = carry(len(q), 2, 0)
    hv = [d3_given_half(q[:H], x[:H], dial, kmin), d3_given_half(q[H:H + H], x[H:H + H], dial, kmin)]
    return both(hv), hv


def d3_old(q, kmin):
    """DECODE3b's (3d) as frozen: one point of the gap law, the gaps above L = the mean gap's whole part."""
    H, _ = carry(len(q), 2, 0)
    res = []
    for half in (q[:H], q[H:H + H]):
        lands = [t for t, c in enumerate(half) if c]
        gaps = [b - a for a, b in zip(lands, lands[1:])]
        n, G = len(gaps), sum(gaps)
        if n < kmin:
            res.append(("NOT READ",))
            continue
        L, _ = carry(G, n, 0)
        A = sum(1 for g in gaps if g > L)
        EA, _ = carry(UNIT * n * (G - n) ** L, G ** L, 0)
        den = EA * (UNIT * n - EA)
        if den == 0:
            res.append(("NOT READ",))
            continue
        z2 = th((UNIT * A - EA) * (UNIT * A - EA) * n, den)
        res.append(("SHOWN" if z2 <= CUT else "NOT SHOWN",))
    return both(res)


# ---------------------------------------------------------------- R2, gated

def ambiguous(seq, length):
    nexts = {}
    for i in range(length, len(seq)):
        nexts.setdefault(tuple(seq[i - length:i]), set()).add(seq[i])
    return sum(1 for v in nexts.values() if len(v) >= 2)


def r2(q, b3v):
    if b3v != "SHOWN":
        return "NOT READ"
    H, _ = carry(len(q), 2, 0)
    halves = (q[:H], q[H:H + H])
    for h in halves:
        n = sum(h)
        if th(n * (n - 1), len(h)) < M2:
            return "NOT READ"
    ok = all(ambiguous(h, L) >= AMBIG for h in halves for L in PASTS)
    return "SHOWN" if ok else "NOT SHOWN"


# ---------------------------------------------------------------- the stand-in cases

def tally(d, v):
    d[v] = d.get(v, 0) + 1


def read_group(name, group, carried):
    """group: a list of (q, x). Prints the verdict counts of every rule, and for carried sides the least z^2."""
    rows = {k: {} for k in ("3b given 15", "3b given 20", "3b given 30", "3b DECODE3d", "3d given",
                             "3d DECODE3b", "R2 gated on 3b given", "R2 gated on 3b DECODE3d")}
    least_b, least_d, most_zk, two_values = None, None, None, 0
    for q, x in group:
        for kmin in (15, 20, 30):
            v, hv = b3_given(q, x, D, kmin)
            tally(rows[f"3b given {kmin}"], v)
            if kmin == 20:
                b20 = v
                for h in hv:
                    if h[1] is not None:
                        least_b = h[1] if least_b is None else min(least_b, h[1])
                        most_zk = h[3] if most_zk is None else max(most_zk, h[3])
        old = b3_old(q, 20)
        tally(rows["3b DECODE3d"], old)
        v, hv = d3_given(q, x, D, KMIN)
        tally(rows["3d given"], v)
        for h in hv:
            if h[0] != "NOT READ" and isinstance(h[1], int):
                least_d = h[1] if least_d is None else min(least_d, h[1])
            two_values += int(h[1] == "gaps take two values or fewer")
        tally(rows["3d DECODE3b"], d3_old(q, KMIN))
        tally(rows["R2 gated on 3b given"], r2(q, b20))
        tally(rows["R2 gated on 3b DECODE3d"], r2(q, old))
    say(f"  {name}:")
    for k, d in rows.items():
        say(f"    {k}: {dict(sorted(d.items()))}")
    if carried:
        say(f"    carried: least (3b) z^2 among halves read at K_MIN 20 {least_b}; largest Z / K there {most_zk}"
            f" thousandths; (3d) halves NOT SHOWN by two values or fewer {two_values}; least (3d) X^2 among the rest"
            f" read {least_d}")


def carried_group(xs):
    return [(carried_side(xs, ph), xs) for ph in range(0, 1000, 50)]


seed = 27182
fair_cache = {}


def fair_group(xs, n):
    global seed
    group = []
    for _ in range(n):
        q, seed = fair_side(seed, xs)
        group.append((q, xs))
    return group


# ---- the stand-in cases
say("1. (3b), (3d) and R2 against the board's passing, on the stand-ins (verdict counts; DECODE3d's (3b) and DECODE3b's"
    " (3d) beside them)")
say(" carried steady sides, 20 phases each:")
for p, H in ((950, 200), (950, 400), (900, 200), (900, 400), (800, 200), (800, 400), (40, 100), (40, 1000), (70, 100),
             (70, 1000), (70, 3000), (100, 100), (100, 1000), (190, 100), (190, 1000), (175, 2000), (190, 2000),
             (250, 2000), (300, 2000), (400, 2000)):
    read_group(f"carried steady, {p} a round, halves of {H}", carried_group(steady(p, H)), True)
say(" carried moving sides, 20 phases each:")
for nm, xs in (("swing 50 to 300 and back within each half, halves of 2,000", swing(2000)),
               ("wide 300 to 700 and back, halves of 100", wide(100)),
               ("wide 300 to 700 and back, halves of 1,000", wide(1000)),
               ("step 100 then 250 within each half, halves of 2,000", step(2000))):
    read_group(f"carried moving, {nm}", carried_group(xs), True)
say(" fair draws at a steady chance:")
for p, H, n in ((175, 2000, 200), (190, 1000, 200), (190, 100, 200), (300, 2000, 100), (950, 200, 100),
                (800, 400, 100), (70, 600, 100), (70, 1400, 100), (70, 2560, 100)):
    read_group(f"fair, {p} a round, halves of {H}, {n} draws", fair_group(steady(p, H), n), False)
say(" fair draws whose chance follows a moving passing:")
for nm, xs, n in (("swing 50 to 300 and back within each half, halves of 2,000", swing(2000), 200),
                  ("wide 300 to 700 and back, halves of 1,000", wide(1000), 200),
                  ("step 100 then 250 within each half, halves of 2,000", step(2000), 100)):
    read_group(f"fair moving, {nm}, {n} draws", fair_group(xs, n), False)
say(" a record that does not carry the passing: (3b) " + b3_given([0, 1] * 400, None, D, 20)[0] + ", (3d) "
    + d3_given([0, 1] * 400, None, D, 20)[0])

# ---------------------------------------------------------------- R4's power condition on (a), root-free

say("2. R4: the power condition on the local bound (a), root-free. With m^2 = CUT_FW x Var S / 1,000 (millionths), (a)"
    " is NOT READ where b^2 <= m^2 or (b^2 - m^2)^2 <= 4 b^2 m^2, b = 2,000 the local bound: where 2,000 + m does not"
    " reach the hand's bound, whose square is 2 b^2. The least trials per setting pair and half at which (a) is read:")
B2 = 2000 * 2000
for cut_fw, label in ((8948, "CUT_FW about 8,948 (N_T = 18)"), (9140, "CUT_FW about 9,140 (N_T = 20)")):
    row = []
    for E in (0, 500):
        n = 2
        while True:
            var = 4 * carry(UNIT * UNIT - E * E, n, 0)[0]
            m2, _ = carry(cut_fw * var, UNIT, 0)
            if m2 < B2 and (B2 - m2) * (B2 - m2) > 4 * B2 * m2:
                break
            n += 1
        row.append(f"|E_ab| {E}: {n}")
    say(f"  {label}: " + "; ".join(row))

# ---------------------------------------------------------------- the seed test's click part of (ii)

RUN = HERE.joinpath("st2run_1")


def load(name):
    return json.loads(RUN.joinpath(name).read_text(encoding="utf-8"))


def by_place(rec):
    places = {}
    for t, x, tr, v in rec["lines"]:
        places.setdefault((t, x), [[], []])[0].append((tr, v))
    for t, x, e, c in rec["sides"]:
        places.setdefault((t, x), [[], []])[1].append((e, c))
    return {k: (sorted(a), sorted(b)) for k, (a, b) in places.items()}


def seed_ii(a, b):
    """The click part of the seed test's (ii): two records from lays one hidden unit apart, compared on the click
    world's content (each place's lines and sides), with the hidden unit's Node-clock read from the header."""
    xs = a["header"]["hidden"] or b["header"]["hidden"]
    if xs is None:
        return "NOT READ: no hidden unit named", None, None, None
    site = xs[0]
    pa, pb = by_place(a), by_place(b)
    apart = sorted(k for k in set(pa) | set(pb) if pa.get(k) != pb.get(k))
    if not apart:
        return "NOT SHOWN: the clicks do not differ", None, [], 0
    r_star = apart[0][0]
    sites = sorted({x for _, x in apart})
    elsewhere = [k for k in apart if k[1] != site]
    if elsewhere:
        return f"NOT SHOWN: apart at Node-clock {elsewhere[0][1]}, round {elsewhere[0][0]}", r_star, sites, len(apart)
    return "SHOWN", r_star, sites, len(apart)


say("3. The seed test's click part of (ii), on the run tool's board records (Big Pic's stage 1 act, the click world, 200"
    " rounds; one hidden unit in edge 1's tooth at Node-clock 0):")
recs = {nm: load(nm) for nm in ("click_200_0_laid.json", "click_200_0_hidden01.json", "click_200_1_laid.json",
                                 "click_200_1_hidden01.json")}
for turned, label in ((1, "third click (turned)"), (0, "first click (carried)")):
    a, b = recs[f"click_200_{turned}_laid.json"], recs[f"click_200_{turned}_hidden01.json"]
    v, r_star, sites, n = seed_ii(a, b)
    same_passing = a["passing"] == b["passing"]
    lines_apart = len(set(map(tuple, a["lines"])) ^ set(map(tuple, b["lines"])))
    say(f"  {label}: {v}; first round apart {r_star}; Node-clocks apart {sites}; places apart {n}, click lines apart"
        f" {lines_apart}. (The run tool's: the board's passing alike every round in the two runs: {same_passing})")
mut = json.loads(json.dumps(recs["click_200_1_hidden01.json"]))
at = next(i for i, ln in enumerate(mut["lines"]) if ln[1] == 5)
mut["lines"][at][3] += 1
v, r_star, sites, n = seed_ii(recs["click_200_1_laid.json"], mut)
say(f"  its no, the third click's pair with one line at Node-clock 5 one off (round {mut['lines'][at][0]}): {v}")
mut2 = json.loads(json.dumps(recs["click_200_1_laid.json"]))
mut2["header"]["hidden"] = [0, 1]
v, _, _, _ = seed_ii(recs["click_200_1_laid.json"], mut2)
say(f"  its no, a record against itself (no unit apart): {v}")

# ---------------------------------------------------------------- the three kinds of event, (a) to (c)

EDGES = ((2, 3), (2, 4), (3, 4))
CYC = (1, -1, 1)


def clock_sum(qe, i):
    """A clock's line from the edges' quotients, the edge's first clock taking +q and its second -q (stage 1's sense)."""
    s = 0
    for (a, b), v in zip(EDGES, qe):
        s += v if i == a else (-v if i == b else 0)
    return s


def whole_circulations(qe):
    best = 0
    for s in (1, -1):
        w = min(s * c * v for c, v in zip(CYC, qe))
        best = max(best, w)
    return best, (0 if best == 0 else (1 if min(c * v for c, v in zip(CYC, qe)) > 0 else -1))


def cen(v, dial, born):
    _, r = carry(v + born, dial, 0)
    return r - born


def triangle(form, rounds, idle_from, x34=None, turned=True):
    """A stand-in triangle (clocks 2, 3, 4; edges (2,3), (2,4), (3,4)) and a two-clock site (edge (2,3) alone), on the
    stand-in board's passing: clock 2 gives 230 and 410 a round to 3 and 4 (thousandths of a quantum), and the takers
    pass 77 between them (or x34(r)), so y = c . x = 257; from idle_from on 3 passes 180 to 4 and y = 0 (idle).
    form 1: the first click (each edge carries its passing at the dial D, its own tooth);
    form 2: one circulation (Big Pic's PICTURE.md section 7, his mode 11): each edge carries 3 x_e - c_e y at the
            dial 3 D, unturned; the triangle's own tooth carries y at 3 D, turned with its twin by the palindrome at
            K = 3 about the birth (eta += 3 tau, tau += 3 eta; the carries; tau += 3 eta, eta += 3 tau), or carried
            (turned False, the no); each quantum it lands books c on the three edges in one round;
    form 3: the booked wrap: as form 2, but each landing booked on its own edge a round apart ((2,3), then (3,4), then
            (2,4)), the form the owner's word refuses;
    form 0: stage 1's turn: the three edge teeth turned between carries (DECODE3's third click), each at the dial D.
    Returns the places (round, site) -> {edge: q}, the board's passing per round, the edge teeth per round, the dial."""
    dial = D if form in (0, 1) else 3 * D
    born, _ = carry(dial - 1, 2, 0)
    k = [born, born, born]
    kT = eT = born
    k1, _ = carry(D - 1, 2, 0)  # the lone edge's own birth, on its own dial D
    Ws = []
    late = {}
    places, passing, teeth = {}, [], []
    for r in range(rounds):
        x = [-230, -410, 77 if x34 is None else x34(r)] if r < idle_from else [-230, -410, -180]
        y = sum(c * v for c, v in zip(CYC, x))
        passing.append((x, y))
        before = list(k)
        if form == 0:
            ga, ab, gb = 0, 2, 1
            a_, b_, c_ = k[ga] - born, k[ab] - born, k[gb] - born
            b_ = cen(b_ + a_, dial, born)
            c_ = cen(c_ - b_, dial, born)
            a_ = cen(a_ - c_, dial, born)
            k[ga], k[ab], k[gb] = a_ + born, b_ + born, c_ + born
        qe = []
        for e in range(3):
            fed = x[e] if form in (0, 1) else 3 * x[e] - CYC[e] * y
            c, k[e] = carry(fed, dial, k[e])
            qe.append(c)
        if form in (2, 3):
            if turned:
                eT = cen(eT - born + 3 * (kT - born), dial, born) + born
                kT = cen(kT - born + 3 * (eT - born), dial, born) + born
            n, kT = carry(y, dial, kT)
            if turned:
                kT = cen(kT - born + 3 * (eT - born), dial, born) + born
                eT = cen(eT - born + 3 * (kT - born), dial, born) + born
            Ws.append(n)
            if form == 2:
                qe = [v + c * n for v, c in zip(qe, CYC)]
            else:
                for e, lag in ((0, 0), (2, 1), (1, 2)):
                    late[(r + lag, e)] = late.get((r + lag, e), 0) + CYC[e] * n
                qe = [v + late.pop((r, e), 0) for e, v in enumerate(qe)]
        teeth.append((before, list(k)))
        if any(qe):
            places[(r, 0)] = qe
        c1, k1 = carry(x[0], D, k1)
        if c1:
            places[(r, 1)] = [c1, 0, 0]
    return places, passing, teeth, dial, Ws


def lines_of(places):
    """The record in schema 1.4's shape: each place's lines, every side of a clock listed (zeros included)."""
    rec = {}
    for (r, x), qe in places.items():
        on = [(a, b) for (a, b), v in zip(EDGES, qe)] if x == 0 else [EDGES[0]]
        ls = {}
        for (a, b), v in zip(EDGES, qe):
            if (a, b) in on:
                ls.setdefault(a, {})[b] = v
                ls.setdefault(b, {})[a] = -v
        rec[(r, x)] = {t: (sum(s.values()), s) for t, s in ls.items()}
    return rec


def kinds_read(rec):
    """(a), from the record alone: each place by its structure and sides; the books per kind."""
    count = {"first": 0, "split": 0, "third": 0}
    fail = {"first": None, "split": None, "third": None}
    circ = {1: 0, -1: 0}
    for (r, x), ls in sorted(rec.items()):
        clocks = set(ls) | {u for _, (q, s) in ls.items() for u in s}
        edges = {tuple(sorted((t, u))) for t, (q, s) in ls.items() for u in s}
        ok = all(q == sum(s.values()) for q, s in ls.values()) and all(
            ls.get(u, (0, {}))[1].get(t) is not None and ls[u][1][t] + v == 0
            for t, (q, s) in ls.items() for u, v in s.items())
        if len(clocks) == 2 and len(edges) == 1:
            count["first"] += 1
            fail["first"] = fail["first"] or (None if ok else (r, x))
        elif len(clocks) == 3 and len(edges) == 3:
            qe = [ls[a][1][b] for a, b in EDGES]
            shared = any(len([v for v in s.values() if v > 0]) == 2 or len([v for v in s.values() if v < 0]) == 2
                         for q, s in ls.values())
            w, sense = whole_circulations(qe)
            count["split"] += int(shared)
            count["third"] += int(w > 0)
            if w:
                circ[sense] += w
            for kind in ("split", "third"):
                fail[kind] = fail[kind] or (None if ok else (r, x))
    verdict = {kd: ("NOT READ: none" if count[kd] == 0 else ("SHOWN" if fail[kd] is None else f"NOT SHOWN at {fail[kd]}"))
               for kd in count}
    return count, verdict, circ


def checks_b_c(places, passing, teeth, dial, rounds):
    """(b) never seen alone, and (c) an idle triangle lands no circulation: checks against the board's passing."""
    worst, first_round_fail = 0, None
    total = {2: 0, 3: 0, 4: 0}
    swept = {2: 0, 3: 0, 4: 0}
    idle_circ, against = 0, 0
    for r in range(rounds):
        x, y = passing[r]
        qe = places.get((r, 0), [0, 0, 0])
        before, after = teeth[r]
        prev = teeth[r - 1][1] if r else before
        for i in (2, 3, 4):
            qi = clock_sum(qe, i)
            fed = sum((dial * v if (a == i) else (-dial * v if b == i else 0)) for (a, b), v in zip(EDGES, x))
            fed, _ = carry(fed, D, 0)
            total[i] += qi
            swept[i] += fed
            worst = max(worst, abs(dial * total[i] - swept[i]))
            dk = sum(((after[e] - prev[e]) if a == i else (-(after[e] - prev[e]) if b == i else 0))
                     for e, (a, b) in enumerate(EDGES))
            if first_round_fail is None and dial * qi + dk != fed:
                first_round_fail = (r, i)
        w, sense = whole_circulations(qe)
        if w and y == 0:
            idle_circ += 1
        if w and y * sense < 0:
            against += 1
    return th(worst, dial), first_round_fail, idle_circ, against


say("4. The three kinds of event (a), and the checks (b) and (c), on a stand-in triangle and a two-clock site, 400"
    " rounds, the triangle idle from round 200 (to be checked against Big Pic's text):")
for form, label in ((1, "the first click"), (2, "one circulation (THIRD7's form)"), (3, "the booked wrap"),
                    (0, "stage 1's turn")):
    places, passing, teeth, dial, _ = triangle(form, 400, 200)
    count, verdict, circ = kinds_read(lines_of(places))
    worst, rf, idle_circ, against = checks_b_c(places, passing, teeth, dial, 400)
    say(f"  {label}: (a) events {count}, verdicts {verdict}, whole circulations by sense {circ}; (b) the largest"
        f" departure of a clock's booked total from its passing {worst} thousandths of a dial (its two edge teeth hold"
        f" under 2,000), the first round where a clock's line is not its passing's own carry {rf}; (c) whole"
        f" circulations at an idle round {idle_circ}, against y {against}")
places, passing, teeth, dial, _ = triangle(1, 400, 200)
rec = lines_of(places)
first2 = next(k for k in sorted(rec) if k[1] == 1)
rec[first2][2] = (rec[first2][2][0] + 1, rec[first2][2][1])
say(f"  its no for (a)'s books, the first click with one line at a two-clock place one off: {kinds_read(rec)[1]}")
places, passing, teeth, dial, _ = triangle(2, 400, 200)
rec = lines_of(places)
tri = next(k for k in sorted(rec) if k[1] == 0 and any(v != 0 for v in places[k]))
s = dict(rec[tri][2][1])
s[3], s[4] = s[3] + 1, s[4] - 1
rec[tri][2] = (rec[tri][2][0], s)
say(f"  its no for (a)'s books, one circulation with one quantum moved between clock 2's sides (its sum kept):"
    f" {kinds_read(rec)[1]}")



def lone_edge(places, passing, rounds):
    """The first click's check against the board's passing: the lone edge's booked net within one dial of its passing."""
    worst = Q = X = 0
    for r in range(rounds):
        Q += places.get((r, 1), [0, 0, 0])[0]
        X += passing[r][0][0]
        worst = max(worst, abs(D * Q - X))
    return th(worst, D)


places, passing, teeth, dial, _ = triangle(2, 400, 200)
say(f"  the first click's check on the lone edge (one circulation's record): its booked net within"
    f" {lone_edge(places, passing, 400)} thousandths of a dial of its passing (one dial: 1,000)")
forged = dict(places)
idle = next(r for r in range(200, 400) if (r, 0) not in forged)
forged[(idle, 0)] = list(CYC)
v = kinds_read(lines_of(forged))[1]
c = checks_b_c(forged, passing, teeth, dial, 400)
say(f"  its no for (c), one whole circulation forged at idle round {idle}, both ends booked: (a) {v}; (c) whole"
    f" circulations at an idle round {c[2]}")
forged = dict(places)
quiet = next(r for r in range(200) if (r, 0) not in forged)
forged[(quiet, 0)] = [-v for v in CYC]
v = kinds_read(lines_of(forged))[1]
c = checks_b_c(forged, passing, teeth, dial, 400)
say(f"  its no for (c), one whole circulation forged against y at round {quiet}: (a) {v}; (c) against y {c[3]}")
forged = dict(places)
r1 = next(r for r in range(400) if (r, 1) not in forged)
forged[(r1, 1)] = [1, 0, 0]
say(f"  its no for the lone edge, one quantum forged on it at round {r1}, both ends booked: (a)"
    f" {kinds_read(lines_of(forged))[1]['first']}; its booked net within {lone_edge(forged, passing, 400)} thousandths"
    f" of a dial")

say("4b. The third click's draw, read on its circulation's landings W (the triangle's own, not a side), against its"
    " circulating passing y over the dial 3 D: (3b), (3d) and R2 as in section 1 with x_r -> y_r, D -> 3 D; one"
    " circulation, 4,000 rounds (halves of 2,000), the triangle never idle:")


def x34_swing(r):
    _, s = carry(r, 2000, 0)
    u = s if s < 1000 else 2000 - s
    return carry(154 * u, 1000, 0)[0]


for x34, nm in ((None, "y steady at 257"), (x34_swing, "y swinging from 180 to 334 and back within each half")):
    for turned, label in ((True, "turned (the palindrome, the choice)"), (False, "carried (no turn: the no)")):
        _, passing, _, dial, Ws = triangle(2, 4000, 4000, x34, turned)
        ys = [y for _, y in passing]
        v3b, _ = b3_given(Ws, ys, dial, KMIN)
        v3d, _ = d3_given(Ws, ys, dial, KMIN)
        say(f"  {nm}, {label}: landings {sum(Ws)} against the passing's {th(sum(ys), dial)} thousandths;"
            f" (3b) {v3b}; (3d) {v3d}; R2 {r2(Ws, v3b)}")



def circulation(ys, dial3, turned, hidden=0):
    """The triangle's own tooth and twin alone (PICTURE.md section 7): W_r = carry(y_r, 3 D, tau), the palindrome at
    K = 3 about the birth before and after the carry where turned."""
    born, _ = carry(dial3 - 1, 2, 0)
    tau, eta = born, born + hidden
    Ws = []
    for y in ys:
        if turned:
            eta = cen(eta - born + 3 * (tau - born), dial3, born) + born
            tau = cen(tau - born + 3 * (eta - born), dial3, born) + born
        n, tau = carry(y, dial3, tau)
        if turned:
            tau = cen(tau - born + 3 * (eta - born), dial3, born) + born
            eta = cen(eta - born + 3 * (tau - born), dial3, born) + born
        Ws.append(n)
    return Ws


KEY = json.loads(HERE.joinpath("nl", "examples", "tensor24-click", "universe.json").read_text(encoding="utf-8"))[
    "chosen"]["key"]  # the click world's key, read from its universe file
DIAL3 = 9 * KEY  # the triangle's dial 3 D, D = 3 K the edge dial
say(f"  at the click world's own dial 3 D = {DIAL3} (9 times its key), the triangle's tooth alone, halves of 2,000:")
for nm, shape in (("p steady at 86 thousandths", [86] * 4000),
                  ("p swinging from 60 to 111 thousandths and back within each half", swing(2000))):
    if shape[0] != 86:
        shape = [60 + carry(51 * (v - 50), 250, 0)[0] for v in shape]
    ys = [carry(v * DIAL3, UNIT, 0)[0] for v in shape]
    for turned, label in ((True, "turned, 20 lays (the twin at the birth and 1 to 19 hidden units above it)"),
                          (False, "carried (the no), its one lay")):
        rows = {"3b": {}, "3d": {}, "R2": {}}
        landed = []
        for j in range(20 if turned else 1):
            Ws = circulation(ys, DIAL3, turned, j)
            v3b, _ = b3_given(Ws, ys, DIAL3, KMIN)
            tally(rows["3b"], v3b)
            tally(rows["3d"], d3_given(Ws, ys, DIAL3, KMIN)[0])
            tally(rows["R2"], r2(Ws, v3b))
            landed.append(sum(Ws))
        say(f"    {nm}, {label}: landings {min(landed)} to {max(landed)} against the passing's"
            f" {th(sum(ys), DIAL3)} thousandths; (3b) {rows['3b']}; (3d) {rows['3d']}; R2 {rows['R2']}")
say("  (the stand-in dial 3 D = 3,000 above is the small dial's no: the turn's orbit there is short, and memory shows)")

say("5. The three kinds of event on the run tool's board records (stage 1's format: one c per edge, no zero sides),"
    " Node-clock 0, with (b)'s booked totals against the board's passing (edgeclick's flows):")
for turned, label in ((0, "first click"), (1, "third click (stage 1's turn)")):
    rec_b = recs[f"click_200_{turned}_laid.json"]
    dial_b = rec_b["header"]["dial"]
    rounds = rec_b["header"]["rounds"]
    sides_at = {}
    for t, x, e, c in rec_b["sides"]:
        if x == 0:
            sides_at.setdefault(t, [0, 0, 0])[e] += c
    lines_at = {}
    for t, x, tr, v in rec_b["lines"]:
        if x == 0:
            lines_at.setdefault(t, {})[tr] = v
    kinds_b = {"one edge": 0, "two edges": 0, "three edges": 0, "a clock sharing a passing": 0, "whole circulations": 0}
    off = 0
    for t, qe in sides_at.items():
        on = sum(1 for v in qe if v)
        kinds_b[["", "one edge", "two edges", "three edges"][on]] += 1
        kinds_b["whole circulations"] += whole_circulations(qe)[0]
        for i in (2, 3, 4):
            off += int(lines_at.get(t, {}).get(i, 0) != clock_sum(qe, i))
        signs = [[v for (a, b), v in zip(EDGES, qe) if a == i] + [-v for (a, b), v in zip(EDGES, qe) if b == i]
                 for i in (2, 3, 4)]
        kinds_b["a clock sharing a passing"] += int(any(len([v for v in sg if v > 0]) == 2 or
                                                        len([v for v in sg if v < 0]) == 2 for sg in signs))
    worst = 0
    tot, swp = {2: 0, 3: 0, 4: 0}, {2: 0, 3: 0, 4: 0}
    for t in range(rounds):
        qe = sides_at.get(t, [0, 0, 0])
        x = rec_b["passing"][t][0]
        for i in (2, 3, 4):
            tot[i] += clock_sum(qe, i)
            swp[i] += sum((v if a == i else (-v if b == i else 0)) for (a, b), v in zip(EDGES, x))
            worst = max(worst, abs(dial_b * tot[i] - swp[i]))
    say(f"  {label}: places by the edges carrying {kinds_b}; lines off their sides' sum {off}; (b) the largest"
        f" departure of a clock's booked total from its passing {th(worst, dial_b)} thousandths of a dial (its two"
        f" edge teeth hold under 2,000)")
    slow = [(sides_at.get(t, [0, 0, 0])[2]) for t in range(rounds)]
    net = sum(slow)
    sign = 1 if net >= 0 else -1
    qs = [sign * v for v in slow]
    xs_b = [sign * rec_b["passing"][t][0][2] for t in range(rounds)]
    v3b, hv3b = b3_given(qs, xs_b, dial_b, KMIN)
    v3d, hv3d = d3_given(qs, xs_b, dial_b, KMIN)
    say(f"    the slow edge (3, 4) at Node-clock 0, against the board's passing: (3b) {v3b}"
        f" {[h[0] for h in hv3b]}, windows read {[h[2] for h in hv3b]}; (3d) {v3d} {[h[:2] for h in hv3d]};"
        f" its landings by half {sum(qs[:100])}, {sum(qs[100:])}, the first at round"
        f" {next(t for t, v in enumerate(qs) if v)}")
    on = next(t for t, v in enumerate(xs_b) if v)
    say(f"    its passing (the board's, a board field): 0 until round {on - 1}, then in thousandths of a quantum a round"
        f" {[(t, th(xs_b[t], dial_b)) for t in (on, 80, 100, 120, 150, 199)]}; over the record"
        f" {th(sum(xs_b), rounds * dial_b)}, over rounds {on} to {rounds - 1} {th(sum(xs_b[on:]), (rounds - on) * dial_b)}")

HERE.joinpath(sys.argv[1] if len(sys.argv) > 1 else "decode3e.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
