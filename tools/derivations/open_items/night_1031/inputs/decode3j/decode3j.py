"""DECODE3j's measurements of its changed rules. Whole numbers; every division Rule3's carry; no random module; run
under python3 -I -B. It executes decode3e.py's and pair_order.py's frozen definitions, lifts named functions from
decode3f.py to decode3i.py (copies here), reads every cut from readings3j.json (written once by cuts3j.py), and reads:
B. R2 per clock on its own lines, both ways (the lines and the reversed lines); its failing rows where it reads.
C. R4 with two new ladders: the two-sided joint (the last L and the next L settings and outcomes with the present
   setting, L = 1, 2 and 4) and the joint of both places both ways (per place, the L events before and after, each
   with its own setting, own outcome and the far setting, with the present own and far settings; L = 1 and 2);
   N_T = 2 (21 + 12 S); "refusing only" per record, from its own gates; the laws from both ends and through the far
   place; the gates' lengths; the rates. The pair parse by the joining meeting before, after or both.
D. D4 in the whitelist form; the sizes as estimates with their helpers.
argv: the output name."""

import ast
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTNAME = sys.argv[1] if len(sys.argv) > 1 else "decode3j.txt"
TEXTS = {n: HERE.joinpath(n + ".py").read_text(encoding="utf-8") for n in ("decode3e", "decode3f", "decode3g",
                                                                            "decode3h", "decode3i")}
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
RD = json.loads(HERE.joinpath("readings3j.json").read_text(encoding="utf-8"))
FIVE, AMBIG = RD["FIVE"], RD["AMBIG"]
CUT_FW = {int(k): v for k, v in RD["CUT_FW"].items()}
LAGSUM = {int(k): {int(d): c for d, c in v.items()} for k, v in RD["LAGSUM"].items()}
UNIT, SC = 1000, 10 ** 30
lift_all("decode3g", ("worst", "halves", "exp_neg_up", "ladder_gate", "two_sides"))
lift_all("decode3h", ("comb", "rung1_chance", "ladder_once", "order_e", "joint_past", "to_lines", "mates", "own",
                      "ca_own", "ca_rounds"))
lift_all("decode3i", ("r2_lines", "own_lines", "lag_sum", "ahead", "back", "ca_neg", "ca_sum", "size"))
OWN_SET = [L for L in range(-8, 9) if L != 0]
OWN_OUT = list(range(1, 9))
out = []
say = out.append
seed = 27182


def tally(d, v):
    d[v] = d.get(v, 0) + 1


KEY = json.loads(HERE.joinpath("nl", "examples", "tensor24-click", "universe.json").read_text(encoding="utf-8"))[
    "chosen"]["key"]
DIAL3 = 9 * KEY

# ================================================================ B. R2 per clock, both ways


def r2_both(seq_halves):
    """R2 per clock read on the clock's own lines and on the reversed lines, the same function: SHOWN only where both
    read SHOWN; one precedence."""
    v1, _ = r2_lines(seq_halves)
    v2, _ = r2_lines([s[::-1] for s in seq_halves])
    return worst([v1, v2])


def refractory(seq):
    """A double (1) never follows a double: each 1 right after a 1 is set to 0 (a test record, never an act)."""
    outs, last = [], 0
    for v in seq:
        v = 0 if (v and last) else v
        outs.append(v)
        last = v
    return outs


say("B. R2 per clock on its own lines and on the reversed lines (both ways); 200 fair draws a case, halves of 2,000:")
rows, rows_f, rows_ref = {}, {}, {}
for _ in range(200):
    q1, q2 = two_sides(steady(175, 2000), steady(175, 2000), True)
    sh = own_lines(q1, q2)
    tally(rows, r2_both(sh))
    tally(rows_f, r2_lines(sh)[0])
    tally(rows_ref, r2_both([refractory(s) for s in sh]))
periodic = [[1 if carry(i, 10, 0)[1] == 9 else 0 for i in range(640)] for _ in range(2)]
say(f"  steady 175 and 175: R2 per clock one way {rows_f}, both ways {rows}; the same draws made refractory (a double"
    f" never after a double) {rows_ref}; a double exactly every tenth click (640 clicks, 64 doubles a half)"
    f" {r2_both(periodic)}")
for name, x1, x2 in (("side 1 steady 300, side 2 steady 30", steady(300, 2000), steady(30, 2000)),
                     ("one side passing, side 2 never", steady(175, 2000), [0] * 4000)):
    rr = {}
    for _ in range(200):
        q1, q2 = two_sides(x1, x2, True)
        tally(rr, r2_both(own_lines(q1, q2)))
    say(f"  {name}: R2 per clock both ways {rr}")

# ================================================================ C. R4 with the two new ladders
SAVED = sys.argv
sys.argv = [SAVED[0], str(HERE.joinpath("nl", "src")), "40000", "unused"]
PO = HERE.joinpath("pair_order.py")
po = {"__file__": str(PO), "__name__": "pair_order_defs"}
exec(compile(PO.read_text(encoding="utf-8").split('out.append(f"R4 on records')[0], str(PO), "exec"), po)
sys.argv = SAVED
exec(compile("".join(lift(TEXTS["decode3f"], n) for n in ("pair_step", "rec_one", "rec_two_firsts")), "decode3f.py",
             "exec"), po)
born, turn, click, HALF, SAME, PAIRS, chi2x2, order_z2 = (po[k] for k in ("born", "turn", "click", "HALF", "SAME",
                                                                          "PAIRS", "chi2x2", "order_z2"))
DT = po["space"]["D"]
B2 = 2000 * 2000
lift_all("decode3h", ("rec_member_middle", "rec_at_two"))
lift_all("decode3i", ("rec_by_settings",))


def rec_by_far(rule):
    """A test record: A's outcome a rule on the far place's (B's) setting sequence; B's outcome as the toy's."""
    alice, bob, pair = born(1), born(2), born(3)
    A, Bs = [], []
    for t in range(PAIRS + 8):
        turn(alice), turn(bob)
        A.append(2 * click(HALF, alice, 0))
        Bs.append(1 + 2 * click(HALF, bob, 0))
    lines = []
    for t in range(PAIRS):
        a, b = A[t + 4], Bs[t + 4]
        sa = rule(Bs, t + 4)
        click(HALF, pair, 0)
        same = click(SAME[abs(b - a)], pair, 1)
        lines += [(t, "A", a, sa, 0), (t, "B", b, sa * (2 * same - 1), 0)]
    return lines


def gate_sum(sym, pres, plus, minus, n, rungs, share_den):
    """A ladder's share spent once: its rungs' first-order bounds summed (rungs: (symbols in the context, qexp))."""
    total = 0
    for nsym, qexp in rungs:
        total += ladder_gate((sym, pres), (plus, minus), n, nsym, share_den, qexp)[1]
    return total * share_den <= SC, total


def joint_two_sided(sets, xs, share_den):
    """The two-sided joint ladder: the last L and the next L settings and outcomes, with the present setting,
    L = 1, 2 and 4, AMBIG 2, behind the summed gate (qexp 4L + 2)."""
    n = len(xs)
    plus = sum(1 for v in xs if v > 0)
    s0 = sum(1 for s in sets if s == sets[0])
    if plus == 0 or plus == n or s0 == n:
        return ("NOT SHOWN", "the outcomes or settings do not vary")
    sym = [s * o for s in (s0, n - s0) for o in (plus, n - plus)]
    ok, _ = gate_sum(sym, [s0, n - s0], plus, n - plus, n, [(L + L, 4 * L + 2) for L in (1, 2, 4)], share_den)
    if not ok:
        return ("NOT READ", "the ladder's gate")
    amb = []
    for L in (1, 2, 4):
        nexts = {}
        for i in range(L, n - L):
            ctx = (tuple(zip(sets[i - L:i], xs[i - L:i])), tuple(zip(sets[i + 1:i + 1 + L], xs[i + 1:i + 1 + L])),
                   sets[i])
            nexts.setdefault(ctx, set()).add(xs[i])
        amb.append(sum(1 for v in nexts.values() if len(v) >= 2))
    return ("SHOWN" if all(v >= AMBIG for v in amb) else "NOT SHOWN", amb)


def joint_places(own_s, own_o, far_s, share_den):
    """The joint of both places both ways, per place: the L events before and after, each its own setting, its own
    outcome and the far setting, with the present own and far settings; L = 1 and 2; the summed gate (qexp 6L + 3)."""
    n = len(own_o)
    plus = sum(1 for v in own_o if v > 0)
    s0 = sum(1 for v in own_s if v == own_s[0])
    f0 = sum(1 for v in far_s if v == far_s[0])
    if plus == 0 or plus == n or s0 == n or f0 == n:
        return ("NOT SHOWN", "the outcomes or settings do not vary")
    sym = [s * o * f for s in (s0, n - s0) for o in (plus, n - plus) for f in (f0, n - f0)]
    pres = [s * f for s in (s0, n - s0) for f in (f0, n - f0)]
    ok, _ = gate_sum(sym, pres, plus, n - plus, n, [(L + L, 6 * L + 3) for L in (1, 2)], share_den)
    if not ok:
        return ("NOT READ", "the ladder's gate")
    amb = []
    for L in (1, 2):
        nexts = {}
        for i in range(L, n - L):
            ev = lambda j: (own_s[j], own_o[j], far_s[j])  # noqa: E731
            ctx = (tuple(ev(j) for j in range(i - L, i)), tuple(ev(j) for j in range(i + 1, i + 1 + L)), own_s[i],
                   far_s[i])
            nexts.setdefault(ctx, set()).add(own_o[i])
        amb.append(sum(1 for v in nexts.values() if len(v) >= 2))
    return ("SHOWN" if all(v >= AMBIG for v in amb) else "NOT SHOWN", amb)


def r4j(trials):
    """R4 under (C), per half; the order read both ways, both sides at once and both places at once;
    N_T = 2 (21 + 12 S); one precedence; "refusing only" where a ladder's gate does not open on the record's counts."""
    sources = sorted({A[2] for _, A, _ in trials})
    nt = 2 * (21 + 12 * len(sources))
    cut, c16, c8 = CUT_FW[nt], LAGSUM[nt][16], LAGSUM[nt][8]
    share_den = 20 * nt
    idx_a, idx_b = {2: 0, 0: 1}, {1: 0, 3: 1}
    hv, refusing_only = [], False
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
        ladders = {"(e)": [], "the joint past": [], "the joint future": [], "the two-sided joint": [],
                   "the joint of both places": []}
        for s in sources:
            for k in (1, 2):
                sub = [((A, Bb) if k == 1 else (Bb, A)) for _, A, Bb in half if A[2] == s]
                own_s = [(idx_a if k == 1 else idx_b)[v[0][0]] for v in sub]
                far_s = [(idx_b if k == 1 else idx_a)[v[1][0]] for v in sub]
                xs = [v[0][1] for v in sub]
                own_o = [1 if v > 0 else 0 for v in xs]
                ladders["(e)"].append(order_e(xs, cut, share_den))
                ladders["the joint past"].append(joint_past(own_s, xs, share_den))
                ladders["the joint future"].append(joint_past(own_s[::-1], xs[::-1], share_den))
                ladders["the two-sided joint"].append(joint_two_sided(own_s, xs, share_den))
                ladders["the joint of both places"].append(joint_places(own_s, own_o, far_s, share_den))
        refusing_only = refusing_only or any(r[0] == "NOT READ" and "gate" in str(r[1]) for v in ladders.values()
                                             for r in v)
        gate_c = worst([r[0] for v in ladders.values() for r in v]) == "SHOWN"
        zc = []
        for me in (1, 2):
            mine, farx = (idx_a, idx_b) if me == 1 else (idx_b, idx_a)
            for s_me in (0, 1):
                n0 = n1 = p0 = p1 = 0
                for _, A, Bb in half:
                    own_, other = (A, Bb) if me == 1 else (Bb, A)
                    if mine[own_[0]] != s_me:
                        continue
                    pl = 1 if own_[1] > 0 else 0
                    if farx[other[0]] == 0:
                        n0, p0 = n0 + 1, p0 + pl
                    else:
                        n1, p1 = n1 + 1, p1 + pl
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
        row = {"(a)": va, "the limit": "NOT SHOWN" if past else "SHOWN", "the curve": worst(curve), "(c)": vc,
               "2 x 2": "SHOWN" if all(z is not None and z <= cut for z in mi) else "NOT SHOWN", "the lag sums": vs,
               "S": S, "ladders": {k: [r[:2] for r in v] for k, v in ladders.items()},
               "largest sum": max(((z, k) for k, (z, c) in sums.items() if z is not None), default=(None, None))}
        row.update({k: worst([r[0] for r in v]) for k, v in ladders.items()})
        hv.append(row)
    keys = ("(a)", "the limit", "the curve", "(c)", "2 x 2", "the lag sums", "(e)", "the joint past",
            "the joint future", "the two-sided joint", "the joint of both places")
    parts = {k: worst([h[k] for h in hv]) for k in keys}
    click_parts = worst(list(parts.values()))
    return nt, parts, click_parts, refusing_only, hv


say(f"C. R4 with the two-sided joint and the joint of both places both ways, on pair records written as meetings on both"
    f" sides, {PAIRS} pair events (20,000 a half); every record's settings from each place's own turned teeth:")
forms = [("the toy's third click (a format and reading test)", po["rec_one"](True)),
         ("the first click", po["rec_one"](False)), ("two first clicks interleaved", po["rec_two_firsts"]()),
         ("two ahead", rec_by_settings(ahead(2))),
         ("parity of the next two settings", rec_by_settings(lambda A, t: 1 if A[t + 1] == A[t + 2] else -1)),
         ("one back and one ahead (the physicist's; the mathematician's row 1)",
          rec_by_settings(lambda A, t: 1 if A[t - 1] == A[t + 1] else -1)),
         ("two back and two ahead (the physicist's)", rec_by_settings(lambda A, t: 1 if A[t - 2] == A[t + 2] else -1)),
         ("four back and four ahead (the mathematician's row 2)",
          rec_by_settings(lambda A, t: 1 if A[t - 4] == A[t + 4] else -1)),
         ("the parity of B's two previous settings (the mathematician's row 3)",
          rec_by_far(lambda B, t: 1 if B[t - 1] == B[t - 2] else -1)),
         ("the parity of B's setting one before and one after (the mathematician's row 4)",
          rec_by_far(lambda B, t: 1 if B[t - 1] == B[t + 1] else -1)),
         ("one back and one ahead, flipped 100 per 1,000 (the reach)",
          rec_by_settings(lambda A, t: 1 if A[t - 1] == A[t + 1] else -1, 100)),
         ("the free-lay control: the member born at the middle", rec_member_middle()),
         ("a local act at the bound, S = 2 exactly", rec_at_two())]
lift_all("decode3h", ("from_lines",))
for label, lines in forms:
    rec = to_lines(lines)
    trials = from_lines(rec)
    nt, parts, cp, ro, hv = r4j(trials)
    short = {k: v for k, v in parts.items() if v != "SHOWN"}
    lad = hv[0]["ladders"]
    say(f"  {label}: mates {mates(rec)}; pairs {len(trials)}; N_T {nt}; S {[h['S'] for h in hv]}; parts not SHOWN"
        f" {short}; the click parts {cp}; refusing only {ro}")
    say(f"    first half, at A: the two-sided joint {lad['the two-sided joint'][0]}; the joint of both places"
        f" {lad['the joint of both places'][0]}; the largest lag sum {hv[0]['largest sum']}")


def opening(sym_of, pres_of, rungs, nt, ns, nsrc=1):
    for n in ns:
        m, _ = carry(n, nsrc, 0)
        sym, pres, plus = sym_of(m), pres_of(m), carry(m, 2, 0)[0]
        if gate_sum(sym, pres, plus, m - plus, m, rungs, 20 * nt)[0]:
            return n
    return None


def fair_sym(m):
    h, _ = carry(m, 2, 0)
    return [h * h, h * (m - h), (m - h) * h, (m - h) * (m - h)]


def skew_sym(m):
    s0, _ = carry(7 * m, 10, 0)
    h, _ = carry(m, 2, 0)
    return [s * o for s in (s0, m - s0) for o in (h, m - h)]


def fair_pres(m):
    h, _ = carry(m, 2, 0)
    return [h, m - h]


def skew_pres(m):
    s0, _ = carry(7 * m, 10, 0)
    return [s0, m - s0]


NS = list(range(500, 6001, 100))
TS = [(L + L, 4 * L + 2) for L in (1, 2, 4)]
say("  the summed gates first open at (pair events a half, steps of 100): the joint past and future, one source fair"
    f" (N_T 66) {opening(fair_sym, fair_pres, [(L, L + L + 2) for L in (1, 2, 4, 8)], 66, NS)}; the two-sided joint"
    f" {opening(fair_sym, fair_pres, TS, 66, NS)}; two sources fair (N_T 90, each source half the events)"
    f" {opening(fair_sym, fair_pres, [(L, L + L + 2) for L in (1, 2, 4, 8)], 90, NS, 2)}; one source with settings 700"
    f" and 300 (N_T 66) {opening(skew_sym, skew_pres, [(L, L + L + 2) for L in (1, 2, 4, 8)], 66, NS)}")
lift_all("decode3h", ("right_pairs",))


def right_pairs_skew(n_ev):
    """A right pair record of the pattern with each place's settings 700 and 300 per 1,000 (a stand-in draw)."""
    global seed
    lines = []
    for t in range(n_ev):
        u1, seed = lcg(seed)
        u2, seed = lcg(seed)
        u3, seed = lcg(seed)
        u4, seed = lcg(seed)
        a = 0 if u1 < 700 else 2
        b = 1 if u2 < 700 else 3
        sa = 1 if u3 < 500 else -1
        same = 1 if u4 * DT < UNIT * SAME[abs(b - a)] else 0
        lines.append((t, (a, sa, 0), (b, sa * (2 * same - 1), 0)))
    return lines


for label, maker, n_ev, count in (("fair settings, 3,000 a half", right_pairs, 6000, 1000),
                                  ("settings 700 and 300, 1,300 a half", right_pairs_skew, 2600, 200),
                                  ("fair settings, 1,300 a half", right_pairs, 2600, 200)):
    rows, by, ro_n = {}, {}, 0
    for _ in range(count):
        nt, parts, cp, ro, hv = r4j(maker(n_ev))
        tally(rows, cp)
        ro_n += int(ro)
        for k, v in parts.items():
            if v == "NOT SHOWN":
                tally(by, k)
    say(f"  the rate, {count} right pair records of the pattern, {label}: the click parts {rows}; refusing only on"
        f" {ro_n}; NOT SHOWN by part {by}")


def to_lines_joined(lines, mode):
    """The pair record with the joining meeting at another round (format: a test's): pair event t's outcomes and
    settings at round 3t + 1; the bearing meeting at 3t (mode "before"), the tie at 3t + 2 ("after"), or both."""
    rec = []
    by_t = {}
    for t, place, setting, outcome, src in lines:
        by_t.setdefault(t, {})[place] = (setting, outcome, src)
    for t in sorted(by_t):
        v = by_t[t]
        src = v["A"][2]
        r0 = 3 * t + 1
        joins = {"before": [r0 - 1], "after": [r0 + 1], "both": [r0 - 1, r0 + 1]}[mode]
        for rj in joins:
            rec.append({"round": rj, "site": 9, "train": 3 + src, "q": -2, "sides": [],
                        "across": [[2, 0, -1], [2, 1, -1]]})
            for site in (0, 1):
                rec.append({"round": rj, "site": site, "train": 2, "q": 1, "sides": [], "across": [[3 + src, 9, 1]]})
        for place, site in (("A", 0), ("B", 1)):
            setting, outcome, _ = v[place]
            rec.append({"round": r0, "site": site, "train": 1, "q": -1, "sides": [[10 + setting, -1]], "across": []})
            rec.append({"round": r0, "site": site, "train": 10 + setting, "q": 1, "sides": [[1, 1]], "across": []})
            rec.append({"round": r0, "site": site, "train": 2, "q": outcome, "sides": [[30, outcome]], "across": []})
            rec.append({"round": r0, "site": site, "train": 30, "q": -outcome, "sides": [[2, -outcome]], "across": []})
    return sorted(rec, key=lambda ln: (ln["round"], ln["site"], ln["train"]))


def from_lines_joined(rec):
    """The pair parse at any round: in each outcome clock's own lines, an outcome is joined by the meeting next before
    it (a bearing) if one stands since its last outcome, else by the meeting next after it (a tie); the two places'
    outcomes joined by one meeting form a pair; each place's setting is its setting clock's partner in the outcome's
    round."""
    setting_at = {}
    for ln in rec:
        if ln["site"] in (0, 1) and ln["train"] == 1:
            setting_at[(ln["round"], ln["site"])] = ln["sides"][0][0] - 10
    joined = {}
    for site, place in ((0, "A"), (1, "B")):
        pending, waiting = None, []
        for ln in (x for x in rec if x["site"] == site and x["train"] == 2):
            if ln["across"]:
                u, p, _ = ln["across"][0]
                mid = (ln["round"], p, u)
                if waiting:
                    for w in waiting:
                        joined.setdefault(mid, {})[place] = w
                    waiting = []
                else:
                    pending = mid
            else:
                o = (setting_at[(ln["round"], site)], ln["sides"][0][1])
                if pending is not None:
                    joined.setdefault(pending, {})[place] = o
                    pending = None
                else:
                    waiting.append(o)
    return [(mid[0], (v["A"][0], v["A"][1], mid[2]), (v["B"][0], v["B"][1], mid[2]))
            for mid, v in sorted(joined.items()) if set(v) == {"A", "B"}]


toy = po["rec_one"](True)
for mode in ("before", "after", "both"):
    rec = to_lines_joined(toy, mode)
    trials = from_lines_joined(rec)
    nt, parts, cp, ro, hv = r4j(trials)
    say(f"  the pair parse by the joining meeting, {mode}: mates {mates(rec)}; {len(rec)} lines; pairs read back"
        f" {len(trials)}; the toy's click parts {cp}")

# ================================================================ D. D4 in the whitelist form; the sizes
BIG = 10 ** 6


def ca_keyword(A_lines, give, take, B_lines, b1, b2):
    return own(A_lines, r=take) - own(A_lines, r=give) - (own(B_lines, r=b2) - own(B_lines, r=b1))


def ca_range(A_lines, give, take, B_lines, b1, b2):
    return own(range(BIG), take) - own(range(BIG), give) - (own(range(BIG), b2) - own(range(BIG), b1))


def ca_locals(A_lines, give, take, B_lines, b1, b2):
    v = locals()
    return (v["take"] - v["give"]) - (v["b2"] - v["b1"])


def ca_star(*f):
    return (f[2] - f[1]) - (f[5] - f[4])


def ca_kwonly(*, A_lines, give, take, B_lines, b1, b2):
    return (take - give) - (b2 - b1)


def d4_whitelist(src, fn_name):
    """D4, a static check in the whitelist form, over every parameter kind. A conversion may hold only: own() calls
    whose first argument is a lines parameter (a name ending in _lines) and whose second, positional or r=, is a
    round parameter; arithmetic and constants over them; its return. Every other name, call or parameter kind
    (*args, **kwargs) is refused."""
    fn = ast.parse(lift(src, fn_name)).body[0]
    a = fn.args
    if a.vararg or a.kwarg:
        return "refused: a *args or **kwargs parameter"
    params = [p.arg for p in a.posonlyargs + a.args + a.kwonlyargs]
    lines_p = {p for p in params if p.endswith("_lines")}
    round_p = set(params) - lines_p
    allowed_ids = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Call):
            if getattr(node.func, "id", None) != "own":
                return f"refused: a call of {ast.dump(node.func)[:30]}"
            args = list(node.args) + [k.value for k in node.keywords]
            names = [k.arg for k in node.keywords]
            if len(args) != 2 or any(nm not in (None, "r") for nm in names):
                return "refused: own() takes a lines and a round"
            first, second = args
            if not (isinstance(first, ast.Name) and first.id in lines_p):
                return "refused: own()'s first argument is no lines parameter"
            if not (isinstance(second, ast.Name) and second.id in round_p):
                return "refused: own()'s second argument is no round parameter"
            allowed_ids.update({id(node.func), id(first), id(second)})
    for node in ast.walk(fn):
        if isinstance(node, ast.Name) and id(node) not in allowed_ids:
            return f"refused: the name {node.id} outside own()"
        if not isinstance(node, (ast.FunctionDef, ast.arguments, ast.arg, ast.Return, ast.Call, ast.Name, ast.Load,
                                 ast.BinOp, ast.UnaryOp, ast.Sub, ast.Add, ast.USub, ast.keyword, ast.Constant)):
            return f"refused: a {type(node).__name__} node"
    return "allowed"


ME = Path(__file__).read_text(encoding="utf-8")
res = [(nm, d4_whitelist(TEXTS["decode3h"] if nm in ("ca_own", "ca_rounds") else
                         (TEXTS["decode3i"] if nm in ("ca_neg", "ca_sum") else ME), nm))
       for nm in ("ca_own", "ca_keyword", "ca_rounds", "ca_neg", "ca_sum", "ca_range", "ca_locals", "ca_star",
                  "ca_kwonly")]
say("D. D4 in the whitelist form: " + "; ".join(f"{nm} {v}" for nm, v in res))
items = (("one precedence", (("decode3g", "worst"), ("decode3g", "halves"))),
         ("one key per record", (("decode3g", "one_key"),)),
         ("D4, a test of the decoder's code", (("me", "d4_whitelist"),)),
         ("R2 per clock, both ways, with its gate and helpers",
          (("me", "r2_both"), ("decode3i", "r2_lines"), ("decode3h", "comb"), ("decode3h", "rung1_chance"),
           ("decode3g", "ladder_gate"), ("decode3g", "exp_neg_up"), ("decode3e", "ambiguous"))),
         ("R4's click parts, with their helpers",
          (("me", "r4j"), ("decode3i", "lag_sum"), ("decode3h", "order_e"), ("decode3h", "joint_past"),
           ("me", "joint_two_sided"), ("me", "joint_places"), ("me", "gate_sum"), ("decode3h", "ladder_once"),
           ("decode3g", "ladder_gate"), ("decode3g", "exp_neg_up"), ("decode3e", "ambiguous"), ("decode3e", "th"),
           ("decode3g", "worst"))),
         ("R4's record parse at any round and the mates", (("me", "from_lines_joined"), ("decode3h", "mates"))))
say("  the sizes, estimates of the build (lines, blank, comment and docstring lines left out), helpers counted: " +
    "; ".join(f"{nm} {sum(size(ME if s == 'me' else TEXTS[s], f) for s, f in fs)}" for nm, fs in items) +
    f"; with pair_order's chi2x2 and order_z2 beside R4: {size(PO.read_text(encoding='utf-8'), 'chi2x2')} and"
    f" {size(PO.read_text(encoding='utf-8'), 'order_z2')}")
HERE.joinpath(OUTNAME).write_text("\n".join(out) + "\n", encoding="utf-8")
