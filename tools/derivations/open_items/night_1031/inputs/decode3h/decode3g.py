"""DECODE3g's measurements of its changed rules. Whole numbers; every division Rule3's carry; no random module.

It executes the frozen definitions of decode3e.py and pair_order.py, lifts named functions from decode3f.py (copies in
this folder), takes every cut from READINGS (computed once by cuts3g.py, checked in section G, never at read time), and
reads:
A. R3 at one family-wise level of 5 per cent (the union bound): (3b) with the carried bound's gate at the (3b) cut and
   K_MIN 20; (3d) with its two-values rule only where every cell expects ten; (3e); (3p) on a steady stretch of W.
   The rate at which a right record reads NOT SHOWN, 1,000 right records a case, steady and moving; carried families.
B. R2 per clock in its own count: the gate (the passing-given exact chance of no landing twice in a row, by the
   transfer recursion, at most 1/20, a board check); the ladder on the clock's own clicks.
C. R4 under the owner's road (C): pair records in click form (each setting a line of its own clock, each pair named by
   the meeting that bore it); the pair's curve, both bounds, no signal gated on a click reading (R3 beside), the order
   reading per source, the joint past by R2's ladder, the free-lay control; the seeds' law NOT READ by name. Then the
   rate on 1,000 right pair records.
D. The conversions' checks carrying the counts' grain (the interval rule), on the HALF physicist's configurations;
   C-e on hand-built numbers; C-a's premise; D4's no by computation; one key per record through D = (kappa div
   senses) K.
G. The cited cuts checked: True at C, False at C - 1.
argv: the output name."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTNAME = sys.argv[1] if len(sys.argv) > 1 else "decode3g.txt"
SRC = HERE.joinpath("decode3e.py")
TEXT = SRC.read_text(encoding="utf-8")
FTEXT = HERE.joinpath("decode3f.py").read_text(encoding="utf-8")
g = {"__file__": str(SRC), "__name__": "decode3e_defs"}
exec(compile(TEXT.split("# ---- the stand-in cases")[0], str(SRC), "exec"), g)


def lift(text, name):
    head = text.index("\ndef " + name + "(") + 1
    body = text[head:].split("\n")
    keep = [body[0]]
    for ln in body[1:]:
        if ln and not ln.startswith((" ", "#")):
            break
        keep.append(ln)
    return "\n".join(keep) + "\n"


exec(compile("".join(lift(TEXT, n) for n in ("cen", "circulation")), str(SRC), "exec"), g)
carry, th, up, D = g["carry"], g["th"], g["up"], g["D"]
ladder_top, fair_side, carried_side, steady, swing, step, ambiguous, lcg = (g[k] for k in (
    "ladder_top", "fair_side", "carried_side", "steady", "swing", "step", "ambiguous", "lcg"))
circulation, cen = g["circulation"], g["cen"]

READINGS = {"C1": 6961, "C2": 9575, "C4": 13696, "K_MIN": 20, "E_MIN_TWO": 10, "FIVE": 5, "AMBIG": 2, "M2": 2996,
            "CUT_FW": {46: 10674, 58: 11103}, "R2_GATE": 20}
C1, C2, C4, KMIN, EMIN2, FIVE, AMBIG = (READINGS[k] for k in ("C1", "C2", "C4", "K_MIN", "E_MIN_TWO", "FIVE", "AMBIG"))
UNIT = 1000
out = []
say = out.append


def tally(d, v):
    d[v] = d.get(v, 0) + 1


def worst(names):
    """One precedence at every level: NOT SHOWN first, then NOT READ, then SHOWN."""
    if "NOT SHOWN" in names:
        return "NOT SHOWN"
    if "NOT READ" in names:
        return "NOT READ"
    return "SHOWN"


def halves(seq):
    H, _ = carry(len(seq), 2, 0)
    return seq[:H], seq[H:H + H]


# ================================================================ A. R3 at one family-wise level

def b3_half(q, x, dial):
    """decode3e's (3b), passing-given, with the carried bound's gate and the verdict both at C1, K_MIN 20."""
    Hh = len(q)
    if any(v < 0 or v > dial for v in x):
        return ("NOT READ", "a passing outside one quantum")
    w = ladder_top(Hh, KMIN)
    K, _ = carry(Hh, w, 0)
    if K < KMIN:
        return ("NOT READ", "the ladder")
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
    if Kr < KMIN:
        return ("NOT READ", "the cells")
    if B >= UNIT * Kr or carry((UNIT * Kr - B) * (UNIT * Kr - B), V, 0)[0] <= C1:
        return ("NOT READ", "the carried bound's gate")
    z2, _ = carry((Z - UNIT * Kr) * (Z - UNIT * Kr), V, 0)
    return ("SHOWN" if z2 <= C1 else "NOT SHOWN", z2)


def d3_half(q, x, dial):
    """decode3e's (3d) against the passing, at C2; the two-values NOT SHOWN only where every cell expects ten."""
    Hh = len(q)
    if any(v < 0 or v > dial for v in x):
        return ("NOT READ", "a passing outside one quantum")
    X = sum(x)
    if X == 0:
        return ("NOT READ", "no passing")
    L, _ = carry(Hh * dial, X, 0)
    if L + L > Hh - 1:
        return ("NOT READ", "the passing too slow")
    lands = [t for t, c in enumerate(q) if c]
    gaps = [b - a for a, b in zip(lands, lands[1:])]
    if len(gaps) < KMIN:
        return ("NOT READ", "fewer than K_MIN gaps")
    Q, DL = dial ** (L + L), dial ** L
    O, N = [0, 0, 0], [0, 0, 0]
    for i, t in enumerate(lands):
        if t + L + L > Hh - 1:
            break
        gp = lands[i + 1] - t if i + 1 < len(lands) else L + L + 1
        O[0 if gp <= L else (1 if gp <= L + L else 2)] += 1
        sL = 1
        for j in range(1, L + 1):
            sL *= dial - x[t + j]
        s2L = sL
        for j in range(L + 1, L + L + 1):
            s2L *= dial - x[t + j]
        N[0] += Q - sL * DL
        N[1] += sL * DL - s2L
        N[2] += s2L
    if any(Nc < FIVE * Q for Nc in N):
        return ("NOT READ", "a cell expects fewer than five")
    if len(set(gaps)) <= 2 and all(Nc >= EMIN2 * Q for Nc in N):
        return ("NOT SHOWN", "two values")
    X2 = sum(carry(UNIT * (O[c] * Q - N[c]) * (O[c] * Q - N[c]), Q * N[c], 0)[0] for c in range(3))
    return ("SHOWN" if X2 <= C2 else "NOT SHOWN", X2)


def e3_half(q, x, dial):
    """(3e): the landing rates given the last two outcomes against the passing, four degrees, at C4."""
    if any(v not in (0, 1) for v in q) or any(v < 0 or v > dial for v in x):
        return ("NOT READ", "not a single, one-way side")
    O, X, V, N = [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]
    for r in range(2, len(q)):
        c = q[r - 2] + q[r - 2] + q[r - 1]
        O[c] += q[r]
        X[c] += x[r]
        V[c] += x[r] * (dial - x[r])
        N[c] += 1
    for c in range(4):
        if X[c] < FIVE * dial or N[c] * dial - X[c] < FIVE * dial or V[c] == 0:
            return ("NOT READ", "a past expects fewer than five")
    X2 = sum(carry(UNIT * (dial * O[c] - X[c]) * (dial * O[c] - X[c]), V[c], 0)[0] for c in range(4))
    return ("SHOWN" if X2 <= C4 else "NOT SHOWN", X2)


def p3(Ws, P):
    if P is None:
        return ("NOT READ", "no period carried")
    if len(Ws) < P + P:
        return ("BEYOND", "the period beyond the record")
    return ("NOT SHOWN", "repeats") if Ws[P:P + P] == Ws[:P] else ("SHOWN", "no repetition")


def r3(q, x, dial, w_period=None, is_w=False):
    """R3 = (3b), then (3d) and (3e) where (3b) is SHOWN; on W at a steady stretch, (3p) beside them."""
    if x is None:
        return "NOT READ", {"3b": "NOT READ"}
    hb = [b3_half(a, b, dial) for a, b in zip(halves(q), halves(x))]
    vb = worst([h[0] for h in hb])
    if vb != "SHOWN":
        return vb, {"3b": vb, "3b why": [h[1] for h in hb]}
    hd = [d3_half(a, b, dial) for a, b in zip(halves(q), halves(x))]
    he = [e3_half(a, b, dial) for a, b in zip(halves(q), halves(x))]
    parts = {"3b": vb, "3d": worst([h[0] for h in hd]), "3e": worst([h[0] for h in he]),
             "two values": sum(1 for h in hd if h[1] == "two values"), "3e X^2": [h[1] for h in he]}
    names = [parts["3d"], parts["3e"]]
    if is_w:
        steady_w = len(set(x)) == 1
        vp = p3(q, w_period) if steady_w else ("NOT READ", "no steady stretch")
        parts["3p"] = vp
        if vp[0] in ("NOT SHOWN", "NOT READ"):
            names.append(vp[0])
    return worst(names), parts


say("A. R3 at one family-wise level (C1 6,961, C2 9,575, C4 13,696; the carried bound's gate at C1; K_MIN 20; the two"
    " values only where every cell expects ten):")
seed = 27182


def fairs(xs, n):
    global seed
    grp = []
    for _ in range(n):
        q, seed = fair_side(seed, xs)
        grp.append(q)
    return grp


for name, xs in (("steady 175, halves of 2,000", steady(175, 2000)), ("steady 300, halves of 2,000", steady(300, 2000)),
                 ("the swing, halves of 2,000", swing(2000)), ("the step, halves of 2,000", step(2000))):
    rows, by, tv = {}, {}, 0
    for q in fairs(xs, 1000):
        v, parts = r3(q, xs, D)
        tally(rows, v)
        if v == "NOT SHOWN":
            tally(by, "(3b)" if parts["3b"] == "NOT SHOWN" else ("(3d)" if parts.get("3d") == "NOT SHOWN" else "(3e)"))
        tv += parts.get("two values", 0)
    say(f"  right records, {name}, 1,000 fair draws: R3 {dict(sorted(rows.items()))}; NOT SHOWN first by {by};"
        f" halves NOT SHOWN by the two values {tv}")
for name, xs in (("steady 300", steady(300, 2000)), ("steady 175", steady(175, 2000)), ("steady 190", steady(190, 1000)),
                 ("steady 313, halves of 480", steady(313, 480)), ("the swing", swing(2000)), ("the step", step(2000))):
    rows = {}
    for ph in range(0, 1000, 50):
        tally(rows, r3(carried_side(xs, ph), xs, D)[0])
    say(f"  carried, {name}, 20 phases: R3 {dict(sorted(rows.items()))}")
fam3 = {}
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
                            tally(fam3, r3(carried_side(xs, ph), xs, D)[0])
say(f"  carried, the HALF mathematician's three-level family (972 records): R3 {dict(sorted(fam3.items()))}")
KEY = json.loads(HERE.joinpath("nl", "examples", "tensor24-click", "universe.json").read_text(encoding="utf-8"))[
    "chosen"]["key"]
DIAL3 = 9 * KEY
P_CLICK = 1585440  # the round's order at 3D = 9 x the click world's key where 3 does not divide y (THIRD7's readers)
y = carry(100 * DIAL3, UNIT, 0)[0]
ys = [y] * 800000
for turned, j in ((True, 0), (True, 1), (False, 0)):
    Ws = circulation(ys, DIAL3, turned, j)
    v, parts = r3(Ws, ys, DIAL3, P_CLICK, True)
    say(f"  W at the click world's dial, y = 100 thousandths of 3D, 800,000 rounds, {'turned lay ' + str(j) if turned else 'carried'},"
        f" the period {P_CLICK} carried: R3 {v}, parts {parts}")
q, seed = fair_side(seed, [100] * 800000)
v, parts = r3(q, [100] * 800000, D)
say(f"  a fair draw at 100 a round, 800,000 rounds: R3 {v}, parts {parts}")

# ================================================================ B. R2 per clock in its own count


def two_sides(x1, x2, fair):
    global seed
    if fair:
        q1, seed = fair_side(seed, x1)
        q2, seed = fair_side(seed, x2)
    else:
        q1, q2 = carried_side(x1, 0), carried_side(x2, 500)
    return q1, q2


def no_pair_chance_ok(x1, x2):
    """The gate, a board check: the exact chance, from the two sides' passings alone, that a half holds no two of the
    clock's own clicks in a row with side 1 landing, by the transfer recursion over its rounds (states: no click yet,
    the last click with side 1, the last click without it), in whole numbers over D^(2H); read where it is at most 1/20."""
    e, a, b = 1, 0, 0
    for v1, v2 in zip(x1, x2):
        n0, m1, m2 = (D - v1) * (D - v2), v1 * D, (D - v1) * v2
        e, a, b = e * n0, (e + b) * m1 + a * n0, (e + a + b) * m2 + b * n0
    return READINGS["R2_GATE"] * (e + a + b) <= D ** (2 * len(x1)), th(e + a + b, D ** (2 * len(x1)))


def r2_own(q1, q2, x1, x2, gates):
    """R2 for side 1 of a clock with two sides, in the clock's own count: at each of its clicks (a round where a side
    lands), whether side 1 lands; the ladder at 1, 2, 4, 8, AMBIG 2, in both halves; the gate first."""
    if sum(1 for v in x2 if v) == 0:
        return "NOT READ: one side, its own count is its landings", None
    res, chances = [], []
    for (h1, h2), (ok, ch) in zip(zip(halves(q1), halves(q2)), gates):
        chances.append(ch)
        if not ok:
            res.append("NOT READ")
            continue
        seq = [a for a, b in zip(h1, h2) if a or b]
        res.append("SHOWN" if all(ambiguous(seq, L) >= AMBIG for L in (1, 2, 4, 8)) else "NOT SHOWN")
    return worst(res), chances


say("B. R2 per clock in its own count (the gate a board check: the exact chance of no landing twice in a row in the"
    " clock's own clicks, at most 1/20):")
alt = lambda hi, lo: [hi if carry(r, 2, 0)[1] == 0 else lo for r in range(2000)] * 2  # noqa: E731
for name, x1, x2 in (("steady 175 and 175", steady(175, 2000), steady(175, 2000)),
                     ("side 1 alternating 350 and 0, side 2 steady 175", alt(350, 0), steady(175, 2000)),
                     ("side 1 alternating 350 and 0, side 2 alternating 0 and 350", alt(350, 0), alt(0, 350)),
                     ("side 1 the swing, side 2 steady 100", swing(2000), steady(100, 2000)),
                     ("one side: alternating 350 and 0 (the mathematician's B1), side 2 never passing", alt(350, 0),
                      [0] * 4000)):
    for fair in (True, False):
        rows, ch = {}, None
        gates = [no_pair_chance_ok(y1, y2) for y1, y2 in zip(halves(x1), halves(x2))]
        for _ in range(200 if fair else 1):
            q1, q2 = two_sides(x1, x2, fair)
            v, ch = r2_own(q1, q2, x1, x2, gates)
            tally(rows, v)
        say(f"  {name}, {'200 fair draws' if fair else 'carried'}: R2 {dict(sorted(rows.items()))}; the gate's chance"
            f" of no pair a half {ch} thousandths")
x1, x2 = steady(8, 2000), steady(300, 2000)
gates = [no_pair_chance_ok(y1, y2) for y1, y2 in zip(halves(x1), halves(x2))]
rows, raw = {}, {}
for _ in range(200):
    q1, q2 = two_sides(x1, x2, True)
    tally(rows, r2_own(q1, q2, x1, x2, gates)[0])
    seq_h = [[a for a, b in zip(h1, h2) if a or b] for h1, h2 in zip(halves(q1), halves(q2))]
    tally(raw, worst(["SHOWN" if all(ambiguous(sq, L) >= AMBIG for L in (1, 2, 4, 8)) else "NOT SHOWN"
                      for sq in seq_h]))
say(f"  the gate's no: side 1 steady 8, side 2 steady 300, 200 fair draws: the gate's chance of no pair a half"
    f" {[gt[1] for gt in gates]} thousandths: R2 {rows}; the ladder read without its gate {raw}")

# ================================================================ C. R4 under the owner's road (C)
SAVED = sys.argv
sys.argv = [SAVED[0], str(HERE.joinpath("nl", "src")), "40000", "unused"]
PO = HERE.joinpath("pair_order.py")
po = {"__file__": str(PO), "__name__": "pair_order_defs"}
exec(compile(PO.read_text(encoding="utf-8").split('out.append(f"R4 on records')[0], str(PO), "exec"), po)
sys.argv = SAVED
exec(compile("".join(lift(FTEXT, n) for n in ("pair_step", "rec_one", "rec_two_firsts", "rec_parity", "rec_period4",
                                              "rec_echo", "rec_local")), "decode3f.py", "exec"), po)
born, turn, click, HALF, SAME, PAIRS, chi2x2, order_z2 = (po[k] for k in ("born", "turn", "click", "HALF", "SAME",
                                                                          "PAIRS", "chi2x2", "order_z2"))
DT = po["space"]["D"]
B2 = 2000 * 2000
SC = 10 ** 30


def rec_two_back():
    alice, bob, pair = born(1), born(2), born(3)
    lines, p1, p2 = [], 0, 0
    for t in range(PAIRS):
        turn(alice), turn(bob)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        sa = 1 if p2 == 0 else -1
        click(HALF, pair, 0)
        same = click(SAME[abs(b - a)], pair, 1)
        lines += [(t, "A", a, sa, 0), (t, "B", b, sa * (2 * same - 1), 0)]
        p2, p1 = p1, a
    return lines


def rec_parity_two():
    alice, bob, pair = born(1), born(2), born(3)
    lines, p1, p2 = [], 0, 0
    for t in range(PAIRS):
        turn(alice), turn(bob)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        sa = 1 if p1 == p2 else -1
        click(HALF, pair, 0)
        same = click(SAME[abs(b - a)], pair, 1)
        lines += [(t, "A", a, sa, 0), (t, "B", b, sa * (2 * same - 1), 0)]
        p2, p1 = p1, a
    return lines


def rec_free_lay(j):
    """The free-lay control: each place's outcome a function of its own setting and its own teeth, both places' teeth
    born from one shared lay j (a shared past laid freely); no read across places."""
    alice, bob, ta, tb = born(1), born(2), born(7 + j), born(7 + j)
    lines = []
    for t in range(PAIRS):
        turn(alice), turn(bob), turn(ta), turn(tb)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        lines += [(t, "A", a, 2 * click(HALF if a == 0 else SAME[1], ta, 0) - 1, 0),
                  (t, "B", b, 2 * click(HALF if b == 1 else SAME[1], tb, 0) - 1, 0)]
    return lines


def to_clicks(lines):
    """The pair record in click form: the bearing meeting (round t, the source place 9, the source clock, its partner);
    each place's setting a line of its own setting clock (train 1) passing one quantum to partner 10 + setting; its
    outcome a line of its own outcome clock (train 2) passing the outcome's sign; both naming the bearing meeting."""
    rec, meets = [], {}
    for t, place, setting, outcome, src in lines:
        site = 0 if place == "A" else 1
        meets[t] = [t, 9, 3 + src, 20 + src]
        rec.append({"round": t, "site": site, "train": 1, "q": 1, "sides": [[10 + setting, 1]], "pair": t})
        rec.append({"round": t, "site": site, "train": 2, "q": outcome, "sides": [[30, outcome]], "pair": t})
    return rec, meets


def from_clicks(rec, meets):
    """Read back from click lines alone: settings, outcomes and sources joined by the meeting that bore each pair."""
    got = {}
    for ln in rec:
        place = "A" if ln["site"] == 0 else "B"
        slot = got.setdefault(ln["pair"], {}).setdefault(place, [None, None])
        if ln["train"] == 1:
            slot[0] = ln["sides"][0][0] - 10
        else:
            slot[1] = ln["q"]
    trials = []
    for pid in sorted(got):
        v = got[pid]
        if set(v) == {"A", "B"} and None not in v["A"] + v["B"]:
            trials.append((pid, (v["A"][0], v["A"][1], meets[pid][2]), (v["B"][0], v["B"][1], meets[pid][2])))
    return trials


def exp_neg_up(X, Y):
    """An upper bound on e^(-X / Y), scaled by SC: 1 / SUM_(k <= 12) (X / Y)^k / k!, rounded up."""
    num, f = 0, 1
    for k in range(13):
        num += carry(479001600 * X ** k * Y ** (12 - k), f, 0)[0]
        f *= k + 1
    den = 479001600 * Y ** 12
    return carry(SC * den + num - 1, num, 0)[0]


def ladder_gate(counts_ctx, n_out, n, L, share_den, qexp):
    """The ladder's power gate at one rung, a first-order chance bound that fewer than AMBIG contexts are followed by
    both outcomes: the least of (U) the two likeliest contexts' misses and (P) e^(-E) (1 + 3 E), E a lower bound on
    the ambiguous contexts expected; read where the bound is at most 1 / share_den. counts_ctx: per symbol of the past
    alphabet, its count in the half (the alphabet's symbols independent); the present setting's counts beside."""
    sym, pres = counts_ctx
    m = n - L
    plus, minus = n_out
    comps = [((), 1, 1)]
    for _ in range(L):
        nxt = {}
        for c, mult, pr in comps:
            for i, s in enumerate(sym):
                key = tuple(sorted(c + (i,)))
                if key in nxt:
                    nxt[key] = (nxt[key][0] + mult, pr * s)
                else:
                    nxt[key] = (mult, pr * s)
        comps = [(k, v[0], v[1]) for k, v in nxt.items()]
    comps = [(k, mult, pr * ps, ) for k, mult, pr in comps for ps in pres]
    Qd = n ** qexp
    E = 0
    best = []
    for k, mult, pr in comps:
        A, Bq = m * pr * plus, m * pr * minus
        E += carry(SC * mult * A * Bq, (Qd + A) * (Qd + Bq), 0)[0]
        best.append((pr, mult))
    best.sort(reverse=True)
    two = [best[0][0]] * min(2, best[0][1]) + ([best[1][0]] if best[0][1] < 2 else [])
    bound_u = sum(exp_neg_up(m * pr * plus, Qd) + exp_neg_up(m * pr * minus, Qd) for pr in two[:2])
    bound_p = carry((SC + 3 * E) * exp_neg_up(E, SC), SC, 0)[0] + 1
    bound = min(bound_u, bound_p)
    return bound * share_den <= SC, bound


def order_e(xs, sets, cut, share_den):
    """(e) at one place for one source in one half: lag-1, and R2's ladder on the outcomes alone, behind its gate."""
    n = len(xs)
    plus = sum(1 for v in xs if v > 0)
    if plus == 0 or plus == n:
        return ("NOT SHOWN", "the outcomes do not vary")
    if min(plus, n - plus) ** 2 < FIVE * n:
        return ("NOT READ", "lag-1's cells")
    r1, z = order_z2(xs)
    for L in (1, 2, 4, 8):
        ok, _ = ladder_gate(([plus, n - plus], [1]), (plus, n - plus), n, L, share_den, L + 1)
        if not ok:
            return ("NOT READ", f"the ladder's gate at {L}")
    amb = [ambiguous(xs, L) for L in (1, 2, 4, 8)]
    return ("SHOWN" if z <= cut and all(v >= AMBIG for v in amb) else "NOT SHOWN", r1, z, amb)


def joint_past(sets, xs, share_den):
    """The place's whole joint past: its last L settings and outcomes, with its present setting, by R2's ladder."""
    n = len(xs)
    plus = sum(1 for v in xs if v > 0)
    s0 = sum(1 for s in sets if s == sets[0])
    if plus == 0 or plus == n or s0 == n:
        return ("NOT SHOWN", "the outcomes or settings do not vary")
    sym = [s * o for s in (s0, n - s0) for o in (plus, n - plus)]
    amb = []
    for L in (1, 2, 4, 8):
        ok, _ = ladder_gate((sym, [s0, n - s0]), (plus, n - plus), n, L, share_den, L + L + 2)
        if not ok:
            return ("NOT READ", f"the gate at {L}", amb)
        nexts = {}
        for i in range(L, n):
            ctx = (tuple(zip(sets[i - L:i], xs[i - L:i])), sets[i])
            nexts.setdefault(ctx, set()).add(xs[i])
        amb.append(sum(1 for v in nexts.values() if len(v) >= 2))
    return ("SHOWN" if all(v >= AMBIG for v in amb) else "NOT SHOWN", amb)


def r4c(trials):
    """R4 under the owner's road (C), per half; the parts printed apart; precedence NOT SHOWN first."""
    sources = sorted({A[2] for _, A, _ in trials})
    nt = 2 * (17 + 6 * len(sources))
    cut = READINGS["CUT_FW"][nt]
    share_den = 20 * nt
    idx_a, idx_b = {2: 0, 0: 1}, {1: 0, 3: 1}
    r3v = {}
    for place, k in (("A", 1), ("B", 2)):
        qq = [1 if (A if k == 1 else Bb)[1] > 0 else 0 for _, A, Bb in trials]
        r3v[place] = r3(qq, [HALF] * len(qq), DT)[0]
    hv = []
    for half in halves(trials):
        cnt, num = {}, {}
        for _, A, Bb in half:
            kk = (A[0], Bb[0])
            cnt[kk] = cnt.get(kk, 0) + 1
            num[kk] = num.get(kk, 0) + A[1] * Bb[1]
        E = {(idx_a[a], idx_b[b]): th(num[(a, b)], cnt[(a, b)]) for (a, b) in cnt}
        S = E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)]
        S_lo = S - 1
        var = sum(carry(UNIT * UNIT - E[kk] * E[kk], cnt[(a, b)], 0)[0]
                  for (a, b) in cnt for kk in [(idx_a[a], idx_b[b])])
        m2, _ = carry(cut * var, UNIT, 0)
        reach = not (m2 < B2 and (B2 - m2) * (B2 - m2) > 4 * B2 * m2)
        va = "NOT READ" if reach else ("SHOWN" if S_lo > 2000 and (S_lo - 2000) ** 2 > m2 else "NOT SHOWN")
        Lq = S_lo * S_lo + m2 - 2 * B2
        past = S_lo > 0 and S_lo * S_lo > m2 and Lq > 0 and Lq * Lq > 4 * S_lo * S_lo * m2
        curve = []
        for (a, b), n_ in sorted(cnt.items()):
            e = 2 * SAME[abs(b - a)] - DT
            if DT * DT == e * e:
                curve.append("SHOWN" if num[(a, b)] * DT == n_ * e else "NOT SHOWN")
            else:
                z = carry(UNIT * (num[(a, b)] * DT - n_ * e) ** 2, n_ * (DT * DT - e * e), 0)[0]
                curve.append("SHOWN" if z <= cut else "NOT SHOWN")
        ev, jp = [], []
        for s in sources:
            for k in (1, 2):
                sub = [(A if k == 1 else Bb) for _, A, Bb in half if A[2] == s]
                xs = [v[1] for v in sub]
                sets = [v[0] for v in sub]
                ev.append(order_e(xs, sets, cut, share_den))
                jp.append(joint_past(sets, xs, share_den))
        gate_c = worst([e[0] for e in ev] + [j[0] for j in jp]) == "SHOWN"
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
                nn, P = n0 + n1, p0 + p1
                den = n0 * n1 * P * (nn - P)
                zc.append(None if den == 0 else carry(UNIT * (p0 * n1 - p1 * n0) ** 2 * nn, den, 0)[0])
        vc = "NOT READ" if not gate_c else ("SHOWN" if all(z is not None and z <= cut for z in zc) else "NOT SHOWN")
        sa = [idx_a[A[0]] for _, A, _ in half]
        sb = [idx_b[Bb[0]] for _, _, Bb in half]
        ao = [1 if A[1] > 0 else 0 for _, A, _ in half]
        bo = [1 if Bb[1] > 0 else 0 for _, _, Bb in half]
        mi = []
        for x_, y_ in ((sa, sb), (sa[1:], ao[:-1]), (sa[1:], bo[:-1]), (sb[1:], ao[:-1]), (sb[1:], bo[:-1]),
                       (sa[:-1], ao[1:]), (sb[:-1], bo[1:])):
            c4 = [0, 0, 0, 0]
            for u, v in zip(x_, y_):
                c4[u + u + v] += 1
            mi.append(chi2x2(*c4))
        hv.append({"(a)": va, "the limit": "NOT SHOWN" if past else "SHOWN", "the curve": worst(curve),
                   "(c)": vc, "2 x 2": "SHOWN" if all(z is not None and z <= cut for z in mi[:5]) else "NOT SHOWN",
                   "own past settings": "SHOWN" if all(z is not None and z <= cut for z in mi[5:]) else "NOT SHOWN",
                   "(e)": worst([e[0] for e in ev]), "the joint past": worst([j[0] for j in jp]), "S": S,
                   "jp": jp, "ev": ev})
    parts = {k: worst([h[k] for h in hv]) for k in ("(a)", "the limit", "the curve", "(c)", "2 x 2",
                                                    "own past settings", "(e)", "the joint past")}
    click_parts = worst(list(parts.values()))
    parts.update({"(b) under (C), the settings' dependence on the hand the seeds' law's alone":
                  "NOT READ: no seeds' law exists", "(d), the board's cone (D8)": "NOT READ: no cone on the record",
                  "the click world's causal order (chains of meetings that share a clock)":
                  "NOT READ: the record names no chain of meetings between the places"})
    return nt, cut, r3v, parts, click_parts, worst([v if not v.startswith("NOT READ") else "NOT READ"
                                                    for v in parts.values()]), hv


say(f"C. R4 under the owner's road (C), on pair records in click form, {PAIRS} pair events (20,000 a half):")
forms = [("the toy's third click (its hand reads both settings: a test of the reading, no lawful act)",
          po["rec_one"](True)), ("the first click", po["rec_one"](False)), ("two first clicks interleaved", po["rec_two_firsts"]()),
         ("the parity first click", po["rec_parity"]()), ("a fixed order of period four", po["rec_period4"]()),
         ("A's outcome its own previous setting", po["rec_echo"]()), ("two back (the HALF physicist's)",
                                                                      rec_two_back()),
         ("parity of two (the HALF physicist's)", rec_parity_two())]
forms += [(f"the free-lay control, lay {j} (local, a shared lay)", rec_free_lay(j)) for j in range(3)]
FROM = {True: "each place's own turned teeth (the toy's alice and bob, born 1 and 2)"}
for label, lines in forms:
    rec, meets = to_clicks(lines)
    nt, cut, r3v, parts, cp, r4v, hv = r4c(from_clicks(rec, meets))
    short = {k: v for k, v in parts.items() if v != "SHOWN"}
    say(f"  {label}: the settings from {FROM[True]}; N_T {nt}, CUT_FW {cut}; R3 beside {r3v}; S"
        f" {[h['S'] for h in hv]}; parts not SHOWN {short};"
        f" the click parts {cp}; R4 {r4v}")
    say(f"    the joint past per half {[h['jp'] for h in hv]}; (e) per half {[[e[:2] for e in h['ev']] for h in hv]}")
    if label.startswith("the toy's"):
        say(f"    the record: {len(rec)} click lines and {len(meets)} bearing meetings, read back from the lines alone")


def right_pairs(n_ev):
    """A right pair record of the pair's pattern (a stand-in draw): settings fair at each place; A's outcome fair;
    B's outcome alike with the curve's share at the two settings (the record of the pattern, never an act)."""
    global seed
    lines = []
    for t in range(n_ev):
        u1, seed = lcg(seed)
        u2, seed = lcg(seed)
        u3, seed = lcg(seed)
        u4, seed = lcg(seed)
        a = 0 if u1 < 500 else 2
        b = 1 if u2 < 500 else 3
        sa = 1 if u3 < 500 else -1
        same = 1 if u4 * DT < UNIT * SAME[abs(b - a)] else 0
        lines += [(t, "A", a, sa, 0), (t, "B", b, sa * (2 * same - 1), 0)]
    return lines


rows, by = {}, {}
for _ in range(1000):
    rec, meets = to_clicks(right_pairs(4000))
    nt, cut, r3v, parts, cp, r4v, hv = r4c(from_clicks(rec, meets))
    tally(rows, cp)
    for k, v in parts.items():
        if v == "NOT SHOWN":
            tally(by, k)
say(f"  the rate: 1,000 right pair records of the pattern (4,000 events, 2,000 a half; the settings from the stand-in"
    f" draw, fair at each place): the click parts {rows};"
    f" NOT SHOWN by part {by}")

# ================================================================ D. the conversions with the grain; D4; the key


def lines_at(num, den, shift, rounds):
    ls, tooth = [], shift
    for r in range(rounds):
        c, tooth = carry(num, den, tooth)
        if c:
            ls.append(r)
    return ls


def own(ls, r):
    return sum(1 for t in ls if t < r)


def meets_iv(left, right):
    """The grain's interval rule: each own count within one of its true value, so a product of counts lies in
    [PRODUCT max(x - 1, 0), PRODUCT (x + 1)]; an identity between two products is SHOWN where the intervals meet."""
    lo_l = hi_l = lo_r = hi_r = 1
    for x in left:
        lo_l, hi_l = lo_l * max(x - 1, 0), hi_l * (x + 1)
    for x in right:
        lo_r, hi_r = lo_r * max(x - 1, 0), hi_r * (x + 1)
    return lo_l <= hi_r and lo_r <= hi_l


R = 800
for label, ra, rb, truth in (("one depth (both 2 of every 3 rounds)", (2, 3), (2, 3), 0),
                             ("two depths (A 2 of every 3, B 3 of every 4)", (2, 3), (3, 4), 1)):
    for span in (10, 30, 300):
        n = recip_no = close_no = deep_wrong = deep_read = forged_close_shown = 0
        for s in range(3):
            A_l, B_l = lines_at(ra[0], ra[1], 0, R), lines_at(rb[0], rb[1], s, R)
            for d in range(1, 6):
                for e1 in range(30):
                    f1 = carry(e1 * 7 + s, 30, 0)[1]
                    e2, f2 = e1 + span, f1 + span
                    p, q_ = own(B_l, e2 + d) - own(B_l, e1 + d), own(A_l, e2) - own(A_l, e1)
                    pp, qq = own(A_l, f2 + d) - own(A_l, f1 + d), own(B_l, f2) - own(B_l, f1)
                    n += 1
                    recip_no += int(not meets_iv([p, qq], [q_, pp]))
                    close_no += int(not meets_iv([p, pp], [q_, qq]))
                    if p >= q_ + 2 or q_ >= p + 2:
                        deep_read += 1
                        deep_wrong += int(truth == 0 or q_ >= p + 2)
                    forged_close_shown += int(meets_iv([p + q_ + 3, pp], [q_, qq]))
        say(f"D. {label}, span {span}: right configurations {n}; C-c's k_AB = k_BA within the grain NOT SHOWN"
            f" {recip_no}; C-d's closure k_AB k_BA = 1 within the grain NOT SHOWN {close_no}; 'deeper' read past the"
            f" grain {deep_read}, wrongly {deep_wrong}; its no, p forged to p + q + 3: still SHOWN {forged_close_shown}")


def ce(two_ra, m, two_rf, nf, two_rb, lb, gr):
    lo_f, hi_f = (two_rf - gr) ** 2 * m * m, (two_rf + gr) ** 2 * m * m
    lo_a, hi_a = 2 * nf * nf * (two_ra - gr) ** 2, 2 * nf * nf * (two_ra + gr) ** 2
    lo_b, hi_b = (two_rb - gr) ** 2 * m * m, (two_rb + gr) ** 2 * m * m
    lo_a3, hi_a3 = 3 * lb * lb * (two_ra - gr) ** 2, 3 * lb * lb * (two_ra + gr) ** 2
    return (lo_f <= hi_a and lo_a <= hi_f) and (lo_b <= hi_a3 and lo_a3 <= hi_b)


say(f"  C-e within the grain (hand-built numbers, a test of the check's logic): an isotropic reading (2r_a 200 over 100"
    f" Meshes; 2r_f 198 to (70, 70, 0); 2r_b 208 to (60, 60, 60)), grain 2: {ce(200, 100, 198, 70, 208, 60, 2)};"
    f" its no, 2r_f forged to 210: {ce(200, 100, 210, 70, 208, 60, 2)}")
A_l = [r for r in range(60) if carry(r, 3, 0)[1] != 2]
B_l = list(A_l)
kab = (own(B_l, 16) - own(B_l, 4), own(A_l, 15) - own(A_l, 3))
kba = (own(A_l, 16) - own(A_l, 4), own(B_l, 15) - own(B_l, 3))
rest = meets_iv([kab[0], kba[1]], [kab[1], kba[0]]) and meets_iv([kab[0], kba[0]], [kab[1], kba[1]])
t1, t2, hold = own(A_l, 9), own(A_l, 21), own(B_l, 16) - own(B_l, 15)
two_r = t2 - t1 - hold
say(f"  C-a's premise in the click world: k_AB {kab}, k_BA {kba}: k = 1 both ways within the grain (rest) {rest}; so"
    f" 2r = t2 - t1 - h = {two_r} (A's own counts {t1}, {t2}; B's hold {hold})")


def ca_own(A_lines, give, take, B_lines, b1, b2):
    return own(A_lines, take) - own(A_lines, give) - (own(B_lines, b2) - own(B_lines, b1))


def ca_rounds(A_lines, give, take, B_lines, b1, b2):
    return (take - give) - (b2 - b1)


def d4(reading):
    """D4, a code check by computation: on a probe record where own counts and rounds differ, a conversion's value
    must be the own-count value the decoder computes; a reading that takes rounds gives another number and is refused."""
    want = ca_own(A_l, 9, 21, B_l, 15, 16)
    got = reading(A_l, 9, 21, B_l, 15, 16)
    return "allowed" if got == want else f"refused by D4: it reads {got} where the clocks' own counts give {want}"


say(f"  D4 by computation: C-a on own counts {d4(ca_own)}; a mutant C-a on rounds {d4(ca_rounds)}")


def one_key(header):
    for c in header.get("cards", []):
        K = 2 * c["middle"] + 1
        if header["dial"] != carry(c["kappa"], c["senses"], 0)[0] * K:
            return f"REFUSED at read: train {c['train']}'s card gives D = (kappa div senses) K off the header's dial"
    return "read"


mid = carry(KEY - 1, 2, 0)[0]
hd = {"dial": 3 * KEY, "cards": [{"train": t, "middle": mid, "kappa": 6, "senses": 2} for t in (0, 1, 2)]}
bad = json.loads(json.dumps(hd))
bad["cards"][1]["middle"] += 1
say(f"  one key per record through D = (kappa div senses) K, K = 2 middle + 1 (a stand-in header, kappa div senses = 3"
    f" as the click world's dial is 3 K): three cards at middle {mid}: {one_key(hd)}; train 1's middle one up:"
    f" {one_key(bad)}")
for nm in ("click_200_0_laid.json",):
    hdr = json.loads(HERE.joinpath("st2run_1", nm).read_text(encoding="utf-8"))["header"]
    say(f"  the frozen board record {nm}: its header's fields {sorted(hdr)}: no card and no across field (stage 1's"
        f" format); its dial {hdr['dial']} = 3 x the file's key {KEY}: {hdr['dial'] == 3 * KEY}")

# ================================================================ G. the cited cuts, checked (never used at read time)
CS = 10 ** 80


def atan_inv(x):
    total, k, power, sign = 0, 0, x, 1
    while True:
        t, _ = carry(CS, (k + k + 1) * power, 0)
        if t == 0:
            return total
        total += sign * t
        sign, k, power = -sign, k + 1, power * x * x


PI = 16 * atan_inv(5) - 4 * atan_inv(239)


def one_ok(c, n):
    T, fact, sign = 0, 1, 1
    for k in range(200):
        t, _ = carry(CS * c ** k, 2000 ** k * fact * (k + k + 1), 0)
        T += sign * t
        sign, fact = -sign, fact * (k + 1)
    return 2 * c * T * T * (20 * n) ** 2 >= 1000 * PI * CS * (20 * n - 1) ** 2


def exp_half(c):
    total, fact = 0, 1
    for k in range(200):
        total += carry(CS * c ** k, 2000 ** k * fact, 0)[0]
        fact *= k + 1
    return total


checks = [("C1", C1, lambda c: one_ok(c, 6)), ("C2", C2, lambda c: exp_half(c) >= 120 * CS),
          ("C4", C4, lambda c: 2000 * exp_half(c) >= 120 * CS * (2000 + c))]
checks += [(f"CUT_FW {nt}", c, (lambda c, nt=nt: one_ok(c, nt))) for nt, c in READINGS["CUT_FW"].items()]
say("G. The readings file's cuts, checked (the least whole thousandth whose tail is at most its level): " + "; ".join(
    f"{nm} {c}: at C {ok(c)}, at C - 1 {ok(c - 1)}" for nm, c, ok in checks))
HERE.joinpath(OUTNAME).write_text("\n".join(out) + "\n", encoding="utf-8")
