"""DECODE3i's measurements of its changed rules. Whole numbers; every division Rule3's carry; no random module; run
under python3 -I -B so that no run writes into the tree.

It executes decode3e.py's and pair_order.py's frozen definitions, lifts named functions from decode3f.py, decode3g.py
and decode3h.py (copies here), reads every cut from readings3i.json (written once by cuts3i.py), and reads:
B. R2 per clock on the clock's own lines (Q10): the ladder and the own-count gate on the q of each of its clicks.
C. R4 reading the order both ways: per place and half, three lag sums (own settings at lags -8 to -1 and 1 to 8, on 16
   degrees; own outcomes at lags 1 to 8, on 8; the far place's settings at lags -8 to 8 but 0, on 16), each cut at the
   chi-square on its degrees from the readings file; a joint future (the joint past on the reversed record); no R3
   beside (c), and no passing in the record; N_T = 2 (21 + 8 S). The forms from the past and from the future; where
   the summed gate opens; the rate on 1,000 right records at 3,000 events a half.
D. D4 over every arithmetic node: a conversion's record fields reach its arithmetic only through own(); its no, three
   mutants. The settled items' sizes, counted in this probe's own functions.
argv: the output name."""

import ast
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTNAME = sys.argv[1] if len(sys.argv) > 1 else "decode3i.txt"
TEXTS = {n: HERE.joinpath(n + ".py").read_text(encoding="utf-8") for n in ("decode3e", "decode3f", "decode3g",
                                                                            "decode3h")}
exec(compile(TEXTS["decode3e"].split("# ---- the stand-in cases")[0], str(HERE.joinpath("decode3e.py")), "exec"),
     globals())


def lift(text, name):
    head = text.index("\ndef " + name + "(") + 1
    body = text[head:].split("\n")
    keep = [body[0]]
    for ln in body[1:]:
        if ln and not ln.startswith((" ", "#")):
            break
        keep.append(ln)
    return "\n".join(keep) + "\n"


def lift_all(src, names):
    exec(compile("".join(lift(TEXTS[src], n) for n in names), src + ".py", "exec"), globals())


lift_all("decode3e", ("cen", "circulation"))
RD = json.loads(HERE.joinpath("readings3i.json").read_text(encoding="utf-8"))
FIVE, AMBIG = RD["FIVE"], RD["AMBIG"]
CUT_FW = {int(k): v for k, v in RD["CUT_FW"].items()}
LAGSUM = {int(k): {int(d): c for d, c in v.items()} for k, v in RD["LAGSUM"].items()}
UNIT, SC = 1000, 10 ** 30
lift_all("decode3g", ("worst", "halves", "exp_neg_up", "ladder_gate", "two_sides"))
lift_all("decode3h", ("comb", "rung1_chance", "ladder_once", "order_e", "joint_past", "to_lines", "mates",
                      "from_lines", "own", "ca_own", "ca_rounds"))
out = []
say = out.append
seed = 27182


def tally(d, v):
    d[v] = d.get(v, 0) + 1


KEY = json.loads(HERE.joinpath("nl", "examples", "tensor24-click", "universe.json").read_text(encoding="utf-8"))[
    "chosen"]["key"]
DIAL3 = 9 * KEY

# ================================================================ B. R2 per clock on its own lines (Q10)


def r2_lines(seq_halves, share_den=20):
    """R2 per clock: in each half, the clock's own lines' q at its clicks, two values in the stand-ins (0, 1); the
    ladder at 1, 2, 4, 8, behind the own-count gate (rung 1 exact, the higher rungs' bounds), summed against 1/20."""
    res, why = [], []
    for seq in seq_halves:
        N, n = len(seq), sum(seq)
        if n == 0 or n == N:
            res.append("NOT READ")
            why.append("one value in this half")
            continue
        r1, tot = rung1_chance(N, n)
        total = carry(SC * r1, tot, 0)[0] + 1
        for L in (2, 4, 8):
            total += ladder_gate(([n, N - n], [1]), (n, N - n), N, L, share_den, L + 1)[1]
        if total * share_den > SC:
            res.append("NOT READ")
            why.append("the gate")
            continue
        res.append("SHOWN" if all(ambiguous(seq, L) >= AMBIG for L in (1, 2, 4, 8)) else "NOT SHOWN")
        why.append("read")
    return worst(res), why


def own_lines(q1, q2):
    """The clock's own lines: at each of its clicks (a round where a side passes) the line's q, here q1 + q2 in
    {1, 2}, written 0 or 1."""
    return [[a + b - 1 for a, b in zip(h1, h2) if a or b] for h1, h2 in zip(halves(q1), halves(q2))]


say("B. R2 per clock, on the clock's own lines' q at its clicks (Q10), gated from its own counts; 200 fair draws a case,"
    " halves of 2,000:")
for name, x1, x2 in (("steady 175 and 175", steady(175, 2000), steady(175, 2000)),
                     ("side 1 alternating 350 and 0, side 2 steady 175",
                      [350 if carry(r, 2, 0)[1] == 0 else 0 for r in range(4000)], steady(175, 2000)),
                     ("side 1 the swing, side 2 steady 100", swing(2000), steady(100, 2000)),
                     ("side 1 steady 8, side 2 steady 300", steady(8, 2000), steady(300, 2000)),
                     ("side 1 steady 300, side 2 steady 30", steady(300, 2000), steady(30, 2000)),
                     ("side 1 steady 300, side 2 steady 8", steady(300, 2000), steady(8, 2000)),
                     ("both 175, side 2 at 0 in the second half", steady(175, 2000), [175] * 2000 + [0] * 2000),
                     ("one side passing, side 2 never", steady(175, 2000), [0] * 4000)):
    rows = {}
    for _ in range(200):
        q1, q2 = two_sides(x1, x2, True)
        tally(rows, r2_lines(own_lines(q1, q2))[0])
    cq1, cq2 = two_sides(x1, x2, False)
    say(f"  {name}: R2 per clock {rows}; carried {r2_lines(own_lines(cq1, cq2))[0]}")

# ================================================================ C. R4, the order both ways
SAVED = sys.argv
sys.argv = [SAVED[0], str(HERE.joinpath("nl", "src")), "40000", "unused"]
PO = HERE.joinpath("pair_order.py")
po = {"__file__": str(PO), "__name__": "pair_order_defs"}
exec(compile(PO.read_text(encoding="utf-8").split('out.append(f"R4 on records')[0], str(PO), "exec"), po)
sys.argv = SAVED
exec(compile("".join(lift(TEXTS["decode3f"], n) for n in ("pair_step", "rec_one", "rec_two_firsts", "rec_parity",
                                                          "rec_period4", "rec_echo")), "decode3f.py", "exec"), po)
born, turn, click, HALF, SAME, PAIRS, chi2x2, order_z2 = (po[k] for k in ("born", "turn", "click", "HALF", "SAME",
                                                                          "PAIRS", "chi2x2", "order_z2"))
DT = po["space"]["D"]
B2 = 2000 * 2000
lift_all("decode3g", ("rec_two_back", "rec_parity_two"))
lift_all("decode3h", ("rec_two_back_flipped", "rec_member_middle", "rec_at_two"))


def rec_by_settings(rule, flip=0):
    """A test record: the settings drawn first by each place's own turned teeth; A's outcome a rule on its own setting
    sequence (ahead or back), flipped with a stand-in draw `flip` per 1,000; B's outcome as the toy's (the unturned
    hand's share). Never an act."""
    global seed
    alice, bob, pair = born(1), born(2), born(3)
    A, Bs = [], []
    for t in range(PAIRS + 8):
        turn(alice), turn(bob)
        A.append(2 * click(HALF, alice, 0))
        Bs.append(1 + 2 * click(HALF, bob, 0))
    lines = []
    for t in range(PAIRS):
        a, b = A[t + 4], Bs[t + 4]
        sa = rule(A, t + 4)
        if flip:
            u, seed = lcg(seed)
            if u < flip:
                sa = -sa
        click(HALF, pair, 0)
        same = click(SAME[abs(b - a)], pair, 1)
        lines += [(t, "A", a, sa, 0), (t, "B", b, sa * (2 * same - 1), 0)]
    return lines


def ahead(L):
    return lambda A, t: 1 if A[t + L] == 0 else -1


def back(L):
    return lambda A, t: 1 if A[t - L] == 0 else -1


def lag_sum(xs, ys, lags):
    """The sum of the lag 2 x 2 z^2 of an outcome sequence ys against a sequence xs at the given lags (a positive lag:
    xs L events before; a negative one: |L| events after). None where a table is degenerate."""
    total = 0
    for L in lags:
        if L > 0:
            pa, pb = xs[:-L], ys[L:]
        else:
            pa, pb = xs[-L:], ys[:L]
        c4 = [0, 0, 0, 0]
        for u, v in zip(pa, pb):
            c4[u + u + v] += 1
        z = chi2x2(*c4)
        if z is None:
            return None
        total += z
    return total


OWN_SET = [L for L in range(-8, 9) if L != 0]
OWN_OUT = list(range(1, 9))


def r4i(trials):
    """R4 under (C), per half, the order read both ways; N_T = 2 (21 + 8 S); precedence NOT SHOWN first."""
    sources = sorted({A[2] for _, A, _ in trials})
    nt = 2 * (21 + 8 * len(sources))
    cut, c16, c8 = CUT_FW[nt], LAGSUM[nt][16], LAGSUM[nt][8]
    share_den = 20 * nt
    idx_a, idx_b = {2: 0, 0: 1}, {1: 0, 3: 1}
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
        var = sum(carry(UNIT * UNIT - E[(idx_a[a], idx_b[b])] ** 2, cnt[(a, b)], 0)[0] for (a, b) in cnt)
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
        ev, jp, jf = [], [], []
        for s in sources:
            for k in (1, 2):
                sub = [(A if k == 1 else Bb) for _, A, Bb in half if A[2] == s]
                sets, xs = [v[0] for v in sub], [v[1] for v in sub]
                ev.append(order_e(xs, cut, share_den))
                jp.append(joint_past(sets, xs, share_den))
                jf.append(joint_past(sets[::-1], xs[::-1], share_den))
        gate_c = worst([e[0] for e in ev] + [j[0] for j in jp] + [j[0] for j in jf]) == "SHOWN"
        zc = []
        for me in (1, 2):
            mine, farx = (idx_a, idx_b) if me == 1 else (idx_b, idx_a)
            for s_me in (0, 1):
                n0 = n1 = p0 = p1 = 0
                for _, A, Bb in half:
                    own_, other = (A, Bb) if me == 1 else (Bb, A)
                    if mine[own_[0]] != s_me:
                        continue
                    plus = 1 if own_[1] > 0 else 0
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
        for x_, y_ in ((sa, sb), (sa[1:], ao[:-1]), (sa[1:], bo[:-1]), (sb[1:], ao[:-1]), (sb[1:], bo[:-1])):
            c4 = [0, 0, 0, 0]
            for u, v in zip(x_, y_):
                c4[u + u + v] += 1
            mi.append(chi2x2(*c4))
        sums = {"A own settings": (lag_sum(sa, ao, OWN_SET), c16), "B own settings": (lag_sum(sb, bo, OWN_SET), c16),
                "A own outcomes": (lag_sum(ao, ao, OWN_OUT), c8), "B own outcomes": (lag_sum(bo, bo, OWN_OUT), c8),
                "A far settings": (lag_sum(sb, ao, OWN_SET), c16), "B far settings": (lag_sum(sa, bo, OWN_SET), c16)}
        vs = worst(["NOT READ" if z is None else ("SHOWN" if z <= c else "NOT SHOWN") for z, c in sums.values()])
        hv.append({"(a)": va, "the limit": "NOT SHOWN" if past else "SHOWN", "the curve": worst(curve), "(c)": vc,
                   "2 x 2": "SHOWN" if all(z is not None and z <= cut for z in mi) else "NOT SHOWN",
                   "the lag sums": vs, "(e)": worst([e[0] for e in ev]), "the joint past": worst([j[0] for j in jp]),
                   "the joint future": worst([j[0] for j in jf]), "S": S, "sums": {k: z for k, (z, c) in sums.items()},
                   "jp": [j[:2] for j in jp], "jf": [j[:2] for j in jf]})
    parts = {k: worst([h[k] for h in hv]) for k in ("(a)", "the limit", "the curve", "(c)", "2 x 2", "the lag sums",
                                                    "(e)", "the joint past", "the joint future")}
    click_parts = worst(list(parts.values()))
    parts.update({"(b) under (C)": "NOT READ: no seeds' law exists", "(d), the board's cone": "NOT READ: no cone",
                  "the per-clock causal order": "NOT READ: no chain of meetings between the places"})
    return nt, (cut, c16, c8), parts, click_parts, worst([v if not v.startswith("NOT READ") else "NOT READ"
                                                          for v in parts.values()]), hv


say(f"C. R4 reading the order both ways, on pair records written as meetings on both sides, {PAIRS} pair events (20,000"
    f" a half); the settings from each place's own turned teeth in every record:")
forms = [("the toy's third click (a format and reading test)", po["rec_one"](True)),
         ("the first click", po["rec_one"](False)), ("two first clicks interleaved", po["rec_two_firsts"]()),
         ("the parity first click", po["rec_parity"]()), ("a fixed order of period four", po["rec_period4"]()),
         ("A's outcome its own previous setting", po["rec_echo"]()), ("two back", rec_two_back()),
         ("parity of two", rec_parity_two()), ("two back, flipped 100 per 1,000", rec_two_back_flipped(100)),
         ("two back, flipped 200 per 1,000", rec_two_back_flipped(200)),
         ("two ahead (both readers')", rec_by_settings(ahead(2))), ("four ahead (the mathematician's)",
                                                                  rec_by_settings(ahead(4))),
         ("parity of the next two settings (the physicist's)",
          rec_by_settings(lambda A, t: 1 if A[t + 1] == A[t + 2] else -1)),
         ("two ahead, flipped 100 per 1,000 (the mathematician's)", rec_by_settings(ahead(2), 100)),
         ("three back, flipped 100 per 1,000 (the mathematician's)", rec_by_settings(back(3), 100)),
         ("the free-lay control: the member born at the middle", rec_member_middle()),
         ("a local act at the bound, S = 2 exactly", rec_at_two())]
for label, lines in forms:
    rec = to_lines(lines)
    g_ = mates(rec)
    trials = from_lines(rec)
    nt, cuts, parts, cp, r4v, hv = r4i(trials)
    short = {k: v for k, v in parts.items() if v != "SHOWN" and not v.startswith("NOT READ: no")}
    say(f"  {label}: mates {g_}; pairs read back {len(trials)}; N_T {nt}, cuts (CUT_FW, 16, 8) {cuts}; S"
        f" {[h['S'] for h in hv]}; parts not SHOWN {short}; the click parts {cp}; R4 {r4v}")
    say(f"    the lag sums, first half {hv[0]['sums']}; the joint future per half {[h['jf'] for h in hv]}")

n_open = None
for n in range(2000, 3001, 100):
    h_, _ = carry(n, 2, 0)
    sym = [h_ * h_, h_ * (n - h_), (n - h_) * h_, (n - h_) * (n - h_)]
    total = sum(ladder_gate((sym, [h_, n - h_]), (h_, n - h_), n, L, 20 * 58, L + L + 2)[1] for L in (1, 2, 4, 8))
    if n_open is None and total * 20 * 58 <= SC:
        n_open = n
say(f"  the summed joint ladder gate (N_T 58, one source, fair marginals) first opens at {n_open} pair events a half,"
    f" in steps of 100 from 2,000")
lift_all("decode3h", ("right_pairs",))
rows, by = {}, {}
for _ in range(1000):
    nt, cuts, parts, cp, r4v, hv = r4i(right_pairs(6000))
    tally(rows, cp)
    for k, v in parts.items():
        if v == "NOT SHOWN":
            tally(by, k)
say(f"  the rate: 1,000 right pair records of the pattern (a stand-in draw, 3,000 events a half, its settings fair at"
    f" each place, read on the trials): the click parts {rows}; NOT SHOWN by part {by}")

# ================================================================ D. D4 over every arithmetic node; the sizes


def ca_neg(A_lines, give, take, B_lines, b1, b2):
    return take + -give + -b2 + b1


def ca_sum(A_lines, give, take, B_lines, b1, b2):
    return sum((take, -give, -b2, b1))


def d4_static(fn_name):
    """D4, a static check of a conversion's code: every record field it takes (each parameter) reaches its arithmetic
    only as an argument of own(), never in any other node."""
    tree = ast.parse(lift(Path(__file__).read_text(encoding="utf-8") if fn_name in ("ca_neg", "ca_sum")
                          else TEXTS["decode3h"], fn_name))
    fn = tree.body[0]
    params = {a.arg for a in fn.args.args}
    parents = {}
    for node in ast.walk(fn):
        for ch in ast.iter_child_nodes(node):
            parents[ch] = node
    for node in ast.walk(fn):
        if isinstance(node, ast.Name) and node.id in params:
            par = parents.get(node)
            if not (isinstance(par, ast.Call) and getattr(par.func, "id", "") == "own" and node in par.args):
                return f"refused: the field {node.id} reaches a {type(par).__name__} node"
    return "allowed"


say(f"D. D4 over every arithmetic node: C-a on own counts {d4_static('ca_own')}; its no, the mutants: on rounds"
    f" {d4_static('ca_rounds')}; negated {d4_static('ca_neg')}; summed {d4_static('ca_sum')}")


def size(src, name):
    """A function's lines, blank, comment and docstring lines left out."""
    code = lift(src, name)
    fn = ast.parse(code).body[0]
    skip = set()
    if fn.body and isinstance(fn.body[0], ast.Expr) and isinstance(getattr(fn.body[0], "value", None), ast.Constant):
        skip = set(range(fn.body[0].lineno, fn.body[0].end_lineno + 1))
    return sum(1 for i, ln in enumerate(code.split("\n"), 1) if ln.strip() and not ln.strip().startswith("#")
               and i not in skip)


ME = Path(__file__).read_text(encoding="utf-8")
items = (("one precedence", (("decode3g", "worst"), ("decode3g", "halves"))),
         ("one key per record", (("decode3g", "one_key"),)),
         ("D4, a test of the decoder's code", (("me", "d4_static"),)),
         ("R2 per clock (with its gate)", (("me", "r2_lines"), ("decode3h", "comb"), ("decode3h", "rung1_chance"),
                                           ("decode3g", "ladder_gate"), ("decode3g", "exp_neg_up"))),
         ("R4's click parts", (("me", "r4i"), ("me", "lag_sum"), ("decode3h", "order_e"), ("decode3h", "joint_past"),
                               ("decode3h", "ladder_once"))),
         ("R4's record parse and mates", (("decode3h", "from_lines"), ("decode3h", "mates"))))
say("  the settled items' sizes in this probe's functions (lines, blank, comment and docstring lines left out): " +
    "; ".join(f"{nm} {sum(size(ME if s == 'me' else TEXTS[s], f) for s, f in fs)}" for nm, fs in items))
HERE.joinpath(OUTNAME).write_text("\n".join(out) + "\n", encoding="utf-8")
