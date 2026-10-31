"""DECODE3j's reading of the far outcome's reach (the Boss's ruling of 11:2x UTC, the HALF mathematician's Q4).
It executes decode3j.py's head and section C's definitions unchanged (r4j and its helpers, to_lines, mates, and
decode3h's from_lines), and bellend.py's definitions (the copy here, bigpic-3clicks 2a839f25f as frozen, its own sum
fac767ec...), each with Rule3's carry from nl/src.
The records are the HALF mathematician's (bp_bell_math/p_record.py's rec_end, copied unchanged): the toy's frame,
40,000 pair events, settings from each place's own turned teeth, the click world's dial D, and bellend's end law on its
own direction, across and share.
- E1: the A end every pair event; E2: the end by the pair's own tooth at HALF / D (about 1 : 1);
- E3: a late hand: the A end, and B reads the hand the previous pair event's end left;
- E4: the late hand at 1 pair event in 10 (the pair's tooth 1 at D div 10);
- the toy's third click, beside them, as a format and reading test.
Each is read by R4 in DECODE3j's form (r4j, N_T 66) and, beside it, by a named candidate that no rule holds: the
far-outcome lag sum, A's outcome against B's outcome at lags -8 to 8 but 0 (lag_sum, sixteen 2 x 2 z^2), against the
16-degree cut at N_T 66 from readings3j.json, per half. The candidate is counted in no N_T and enters no verdict.
Test records, never an act. Whole numbers; Rule3's carry the one division. argv: the output name."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = sys.argv[1]
P = HERE.joinpath("decode3j.py")
TEXT = P.read_text(encoding="utf-8")
B_MARK = "# ================================================================ B. R2 per clock, both ways"
C_MARK = "# ================================================================ C. R4 with the two new ladders"
C_END = 'say(f"C. R4 with the two-sided joint'
ns = {"__file__": str(P), "__name__": "decode3j_defs"}
sys.argv = [str(P), "unused.txt"]
exec(compile(TEXT.split(B_MARK)[0], str(P), "exec"), ns)
exec(compile(TEXT.split(C_MARK)[1].split(C_END)[0], str(P), "exec"), ns)
ns["lift_all"]("decode3h", ("from_lines",))
BE = HERE.joinpath("bellend.py")
sys.argv = [str(BE), str(HERE.joinpath("nl", "src"))]
bn = {"__name__": "bellend_defs"}
exec(compile(BE.read_text(encoding="utf-8").split("for w_a, w_b in WEIGHTS:")[0], str(BE), "exec"), bn)
sys.argv = [str(HERE.joinpath("far3j.py")), OUT]
direction, across, share = bn["direction"], bn["across"], bn["share"]
carry, halves, r4j, to_lines, mates, from_lines = (ns[k] for k in ("carry", "halves", "r4j", "to_lines", "mates",
                                                                    "from_lines"))
born, turn, click, HALF, PAIRS, DT = ns["born"], ns["turn"], ns["click"], ns["HALF"], ns["PAIRS"], ns["DT"]
lag_sum, OWN_SET, LAGSUM, CUT_FW, order_e = (ns[k] for k in ("lag_sum", "OWN_SET", "LAGSUM", "CUT_FW",
                                                             "order_e"))
TENTH, _ = carry(DT, 10, 0)
out = []


def rec_end(end_rule, late_rule):
    alice, bob, pair = born(1), born(2), born(3)
    lines, prev = [], None
    for t in range(PAIRS):
        turn(alice), turn(bob), turn(pair)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        va, vb = direction(a), direction(b)
        if end_rule(pair):
            oa = 2 * click(HALF, alice, 1) - 1
            h = va if oa == 1 else across(va)
            use = prev if (prev is not None and late_rule(pair)) else h
            n, d = share(use, vb)
            ob = 2 * click(carry(n * DT, d, 0)[0], bob, 1) - 1
            prev = h
        else:
            ob = 2 * click(HALF, bob, 1) - 1
            h = vb if ob == 1 else across(vb)
            n, d = share(h, va)
            oa = 2 * click(carry(n * DT, d, 0)[0], alice, 1) - 1
        lines += [(t, "A", a, oa, 0), (t, "B", b, ob, 0)]
    return lines


def read(label, lines):
    rec = to_lines(lines)
    g_ = mates(rec)
    trials = from_lines(rec)
    nt, parts, cp, ro, hv = r4j(trials)
    c16, cut, share_den = LAGSUM[nt][16], CUT_FW[nt], 20 * nt
    short = {k: v for k, v in parts.items() if v != "SHOWN"}
    fo, ez = [], []
    for half in halves(trials):
        ao = [1 if A[1] > 0 else 0 for _, A, _ in half]
        bo = [1 if Bb[1] > 0 else 0 for _, _, Bb in half]
        fo.append(lag_sum(ao, bo, OWN_SET))
        ez.append([order_e([A[1] for _, A, _ in half], cut, share_den)[:3],
                   order_e([Bb[1] for _, _, Bb in half], cut, share_den)[:3]])
    cand = "SHOWN" if all(z <= c16 for z in fo) else "NOT SHOWN"
    lad = {k: [[r[0] for r in h["ladders"][k]] for h in hv] for k in hv[0]["ladders"]}
    out.append(f"  {label}: mates {g_}; pairs {len(trials)}; N_T {nt}; S {[h['S'] for h in hv]}; parts not SHOWN"
               f" {short}; the click parts {cp}; refusing only {ro}")
    out.append(f"    the largest of the six lag sums per half {[h['largest sum'] for h in hv]}")
    out.append(f"    the ladders' verdicts per half, at A then B: {lad}")
    out.append(f"    (e) per half, at A then B (verdict, lag-1 count, z against CUT_FW {cut}): {ez}")
    out.append(f"    the candidate, the far-outcome lag sum per half {fo}, against the cut {c16}: {cand}")


out.append(f"The far outcome's reach: bellend's end law written as records, {PAIRS} pair events (20,000 a half), the dial"
           f" {DT}; R4 in DECODE3j's form, and the far-outcome lag sum beside it as a candidate:")
read("E1, the A end every pair event", rec_end(lambda u: 1, lambda u: 0))
read("E2, the end by the pair's own tooth (about 1 : 1)", rec_end(lambda u: click(HALF, u, 0), lambda u: 0))
read("E3, a late hand: B reads the previous pair event's hand", rec_end(lambda u: 1, lambda u: 1))
read("E4, the late hand at 1 pair event in 10", rec_end(lambda u: 1, lambda u: click(TENTH, u, 1)))
read("the toy's third click (a format and reading test)", ns["po"]["rec_one"](True))
HERE.joinpath(OUT).write_text("\n".join(out) + "\n", encoding="utf-8")
