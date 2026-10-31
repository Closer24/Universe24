"""DECODE3h's measurements of its changed rules. Whole numbers; every division Rule3's carry; no random module.

It executes decode3e.py's and pair_order.py's frozen definitions, lifts named functions from decode3f.py and
decode3g.py (copies here), reads every cut from the readings file readings3h.json (written once by cuts3h.py, checked in
G, never computed at read time), and reads:
A. R3 on single, one-way sides: (3b) against the chi-square on K degrees, two tails, per K from the readings file, the
   carried bound's gate at the lower cut; (3d), (3e) as DECODE3g. The rate on 1,000 right records a case; carried
   families. The bench reading of THIRD7's member on a moving W, with (3p) beside R3, never appended.
B. R2 per clock and per side, in its own count, gated from the clock's own counts: the exact exchangeable chances that
   rung 1 lacks a context (no "11", no "00", no "10", no "01"), plus the higher rungs' first-order bounds, summed
   against 1/20; the passing-given chance beside it, a board check. The transfer recursion checked against the closed
   forms for every N up to 16.
C. R4 on pair records written as meetings on both sides, the bearing meeting included, in lines and sides alone; the
   guard's mates; the 2 x 2 tests at lags 1, 2, 4 and 8 on each place's own settings and outcomes; a ladder's share
   spent once; the free-lay control (the member born at the middle) and a local act at S = 2 exactly. The rate.
D. D4 as a static check, with the mutant as its no.
G. The readings file checked.
argv: the output name."""

import ast
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTNAME = sys.argv[1] if len(sys.argv) > 1 else "decode3h.txt"
ETEXT = HERE.joinpath("decode3e.py").read_text(encoding="utf-8")
FTEXT = HERE.joinpath("decode3f.py").read_text(encoding="utf-8")
GTEXT = HERE.joinpath("decode3g.py").read_text(encoding="utf-8")
SRC = HERE.joinpath("decode3e.py")
exec(compile(ETEXT.split("# ---- the stand-in cases")[0], str(SRC), "exec"), globals())


def lift(text, name):
    head = text.index("\ndef " + name + "(") + 1
    body = text[head:].split("\n")
    keep = [body[0]]
    for ln in body[1:]:
        if ln and not ln.startswith((" ", "#")):
            break
        keep.append(ln)
    return "\n".join(keep) + "\n"


exec(compile("".join(lift(ETEXT, n) for n in ("cen", "circulation")), "decode3e.py", "exec"), globals())
RD = json.loads(HERE.joinpath("readings3h.json").read_text(encoding="utf-8"))
B3 = {int(k): v for k, v in RD["B3"].items()}
C2, C4, KMIN, EMIN2, FIVE, AMBIG = (RD[k] for k in ("C2", "C4", "K_MIN", "E_MIN_TWO", "FIVE", "AMBIG"))
CUT_FW = {int(k): v for k, v in RD["CUT_FW"].items()}
UNIT = 1000
SC = 10 ** 30
exec(compile("".join(lift(GTEXT, n) for n in ("worst", "halves", "d3_half", "e3_half", "p3", "exp_neg_up",
                                              "ladder_gate", "two_sides")), "decode3g.py", "exec"), globals())
out = []
say = out.append


def tally(d, v):
    d[v] = d.get(v, 0) + 1


# ================================================================ A. R3 on sides; the member on the bench

def b3_half(q, x, dial):
    """(3b) against the passing: Z, the floored sum of the windows' z_k, against the chi-square on K degrees, two
    tails at 5/12 per cent each, the cuts per K from the readings file; read only where the carried bound B is at most
    the lower cut (then every carried side, Z < B, reads NOT SHOWN)."""
    Hh = len(q)
    if any(v < 0 or v > dial for v in x):
        return ("NOT READ", "a passing outside one quantum")
    w = ladder_top(Hh, KMIN)
    K, _ = carry(Hh, w, 0)
    if K < KMIN:
        return ("NOT READ", "the ladder")
    Z = B = Kr = 0
    for j in range(K):
        xs, qs = x[j * w:j * w + w], q[j * w:j * w + w]
        X = sum(xs)
        Vk = sum(v * (dial - v) for v in xs)
        if X < FIVE * dial or w * dial - X < FIVE * dial or Vk == 0:
            continue
        C = sum(qs)
        Z += carry(UNIT * (dial * C - X) * (dial * C - X), Vk, 0)[0]
        B += up(UNIT * dial * dial, Vk)
        Kr += 1
    if Kr < KMIN or Kr not in B3:
        return ("NOT READ", "the cells")
    lo, hi = B3[Kr]
    if B > lo:
        return ("NOT READ", "the carried bound's gate")
    return ("NOT SHOWN" if Z < lo or Z > hi else "SHOWN", Z, Kr)


def r3(q, x, dial):
    """R3 on a single, one-way side: (3b), then (3d) and (3e) where (3b) is SHOWN (they give no verdict of their own)."""
    hb = [b3_half(a, b, dial) for a, b in zip(halves(q), halves(x))]
    vb = worst([h[0] for h in hb])
    if vb != "SHOWN":
        return vb, {"3b": vb}
    hd = [d3_half(a, b, dial) for a, b in zip(halves(q), halves(x))]
    he = [e3_half(a, b, dial) for a, b in zip(halves(q), halves(x))]
    parts = {"3b": vb, "3d": worst([h[0] for h in hd]), "3e": worst([h[0] for h in he]),
             "two values": sum(1 for h in hd if h[1] == "two values")}
    return worst([parts["3d"], parts["3e"]]), parts


def bench_w(Ws, ys, dial, P):
    """The member's bench reading (Big Pic's, not the decoder's): R3's verdict on W, with (3p) printed beside it."""
    v, parts = r3(Ws, ys, dial)
    return v, parts, (p3(Ws, P) if len(set(ys)) == 1 else ("NOT READ", "no steady stretch"))


say("A. R3 on single, one-way sides; (3b) against the chi-square on K degrees, two tails per K (readings file):")
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
    say(f"  right records, {name}, 1,000 fair draws: R3 {dict(sorted(rows.items()))}; first refused by {by}; halves"
        f" NOT SHOWN by the two values {tv}")
for name, xs in (("steady 300", steady(300, 2000)), ("steady 175", steady(175, 2000)), ("steady 190", steady(190, 1000)),
                 ("steady 313, halves of 480", steady(313, 480)), ("the swing", swing(2000)), ("the step", step(2000))):
    rows = {}
    for ph in range(0, 1000, 50):
        tally(rows, r3(carried_side(xs, ph), xs, D)[0])
    say(f"  carried, {name}, 20 phases: R3 {dict(sorted(rows.items()))}")
fam3 = {}
for hi_ in (200, 250, 300):
    for mid in (90, 110):
        for lo_ in (30, 40, 50):
            for lh in (30, 60, 100):
                for lm in (30, 60, 100):
                    for ll in (30, 60, 100):
                        one = []
                        while len(one) < 2000:
                            one += [hi_] * lh + [mid] * lm + [lo_] * ll
                        xs = one[:2000] + one[:2000]
                        for ph in (0, 600):
                            tally(fam3, r3(carried_side(xs, ph), xs, D)[0])
say(f"  carried, the HALF mathematician's three-level family (972 records): R3 {dict(sorted(fam3.items()))}")
KEY = json.loads(HERE.joinpath("nl", "examples", "tensor24-click", "universe.json").read_text(encoding="utf-8"))[
    "chosen"]["key"]
DIAL3 = 9 * KEY
ys = [carry((80 + carry(40 * (v - 50), 250, 0)[0]) * DIAL3, UNIT, 0)[0] for v in swing(8000)]
for j in range(3):
    v, parts, vp = bench_w(circulation(ys, DIAL3, True, j), ys, DIAL3, 1585440)
    say(f"  the bench (Big Pic's): THIRD7's member, y swinging from 80 to 120 thousandths of 3D, halves of 8,000, lay {j}:"
        f" R3 {v}, parts {parts}; (3p) beside it {vp}")

# ================================================================ B. R2 per clock and per side, gated from its own counts


def comb(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(k):
        r = carry(r * (n - i), i + 1, 0)[0]
    return r


def rung1_chance(N, n):
    """The exact exchangeable chance, given N clicks and n with the side, that rung 1 lacks one of its contexts: no
    "11" plus no "00" plus no "10" plus no "01" (closed forms of the transfer recursion), over C(N, n)."""
    tot = comb(N, n)
    if n == 0 or n == N:
        return tot, tot
    return comb(N - n + 1, n) + comb(n + 1, N - n) + 2, tot


def recursion_count(N, n, banned):
    """The transfer recursion on the clock's own counts: strings of N clicks with n of the side, avoiding a pair."""
    f = {(0, 0, None): 1}
    for _ in range(N):
        g = {}
        for (length, ones, last), c in f.items():
            for b in (0, 1):
                if last is not None and (last, b) == banned:
                    continue
                key = (length + 1, ones + b, b)
                g[key] = g.get(key, 0) + c
        f = g
    return sum(c for (length, ones, last), c in f.items() if ones == n)


bad = 0
for N in range(2, 17):
    for n in range(0, N + 1):
        bad += int(recursion_count(N, n, (1, 1)) != comb(N - n + 1, n))
        bad += int(recursion_count(N, n, (0, 0)) != comb(n + 1, N - n))
say(f"B. R2: the transfer recursion on own counts against its closed forms, every N from 2 to 16 and every n: {bad}"
    f" disagreements")


def r2_side(clicks_halves, share_den=20):
    """R2 for one side, from the clock's own clicks alone, per half: the side's 0/1 at each click; the gate summed."""
    res, why = [], []
    for seq, n_sides in clicks_halves:
        N, n = len(seq), sum(seq)
        if n_sides < 2:
            res.append("NOT READ")
            why.append("one side in this half: its own count is its landings")
            continue
        r1, tot = rung1_chance(N, n)
        total = carry(SC * r1, tot, 0)[0] + 1
        for L in (2, 4, 8):
            total += ladder_gate(([n, N - n], [1]), (n, N - n), N, L, share_den, L + 1)[1]
        if total * share_den > SC:
            res.append("NOT READ")
            why.append(f"the gate, {carry(1000 * total, SC, 0)[0]} thousandths")
            continue
        res.append("SHOWN" if all(ambiguous(seq, L) >= AMBIG for L in (1, 2, 4, 8)) else "NOT SHOWN")
        why.append("read")
    return worst(res), why


def board_chances(x1, x2):
    """Beside it, a board check: the passing-given exact chances of no "11" and of no "00" (side 1), by the recursion."""
    e, a, b = 1, 0, 0
    e0, a0, b0 = 1, 0, 0
    for v1, v2 in zip(x1, x2):
        n0, m1, m2 = (D - v1) * (D - v2), v1 * D, (D - v1) * v2
        e, a, b = e * n0, (e + b) * m1 + a * n0, (e + a + b) * m2 + b * n0
        e0, a0, b0 = e0 * n0, (e0 + a0 + b0) * m1 + a0 * n0, (e0 + a0) * m2 + b0 * n0
    den = D ** (2 * len(x1))
    return th(e + a + b, den), th(e0 + a0 + b0, den)


def r2_clock(q1, q2):
    """R2 for every side of a two-sided clock: the clock's clicks are the rounds where a side passes."""
    verdicts = []
    for s in (0, 1):
        hv = []
        for h1, h2 in zip(halves(q1), halves(q2)):
            seq = [(a if s == 0 else b) for a, b in zip(h1, h2) if a or b]
            sides = int(any(h1)) + int(any(h2))
            hv.append((seq, sides))
        verdicts.append(r2_side(hv))
    return verdicts


cases = (("steady 175 and 175", steady(175, 2000), steady(175, 2000)),
         ("side 1 alternating 350 and 0, side 2 steady 175", [350 if carry(r, 2, 0)[1] == 0 else 0 for r in range(4000)],
          steady(175, 2000)),
         ("side 1 the swing, side 2 steady 100", swing(2000), steady(100, 2000)),
         ("side 1 steady 8, side 2 steady 300 (DECODE3g's gate's no)", steady(8, 2000), steady(300, 2000)),
         ("side 1 steady 300, side 2 steady 30 (the HALF mathematician's)", steady(300, 2000), steady(30, 2000)),
         ("side 1 steady 300, side 2 steady 8 (the HALF mathematician's)", steady(300, 2000), steady(8, 2000)),
         ("both 175, side 2 at 0 in the second half (the HALF mathematician's)", steady(175, 2000),
          [175] * 2000 + [0] * 2000),
         ("one side, alternating 350 and 0, side 2 never passing", [350 if carry(r, 2, 0)[1] == 0 else 0
                                                                     for r in range(4000)], [0] * 4000))
for name, x1, x2 in cases:
    rows = [{}, {}]
    for _ in range(200):
        q1, q2 = two_sides(x1, x2, True)
        for s, (v, why) in enumerate(r2_clock(q1, q2)):
            tally(rows[s], v)
    cq1, cq2 = two_sides(x1, x2, False)
    cv = [v for v, _ in r2_clock(cq1, cq2)]
    bc = [board_chances(y1, y2) for y1, y2 in zip(halves(x1), halves(x2))]
    say(f"  {name}, 200 fair draws: R2 side 1 {rows[0]}, side 2 {rows[1]}; carried: sides 1 and 2 {cv}; beside it, the"
        f" board check's chances of no 11 and no 00 for side 1, per half {bc} thousandths")

# ================================================================ C. R4 on pair records as meetings on both sides
SAVED = sys.argv
sys.argv = [SAVED[0], str(HERE.joinpath("nl", "src")), "40000", "unused"]
PO = HERE.joinpath("pair_order.py")
po = {"__file__": str(PO), "__name__": "pair_order_defs"}
exec(compile(PO.read_text(encoding="utf-8").split('out.append(f"R4 on records')[0], str(PO), "exec"), po)
sys.argv = SAVED
exec(compile("".join(lift(FTEXT, n) for n in ("pair_step", "rec_one", "rec_two_firsts", "rec_parity", "rec_period4",
                                              "rec_echo")), "decode3f.py", "exec"), po)
born, turn, click, HALF, SAME, PAIRS, chi2x2, order_z2 = (po[k] for k in ("born", "turn", "click", "HALF", "SAME",
                                                                          "PAIRS", "chi2x2", "order_z2"))
DT = po["space"]["D"]
B2 = 2000 * 2000
exec(compile("".join(lift(GTEXT, n) for n in ("rec_two_back", "rec_parity_two")), "decode3g.py", "exec"), globals())


def rec_two_back_flipped(per_mille):
    """The HALF mathematician's B2 form: "two back" with A's outcome flipped at each event with a stand-in draw before
    B's outcome is made from it, so the hand's share stands (S as the toy's)."""
    global seed
    alice, bob, pair = born(1), born(2), born(3)
    lines, p1, p2 = [], 0, 0
    for t in range(PAIRS):
        turn(alice), turn(bob)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        sa = 1 if p2 == 0 else -1
        u, seed = lcg(seed)
        if u < per_mille:
            sa = -sa
        click(HALF, pair, 0)
        same = click(SAME[abs(b - a)], pair, 1)
        lines += [(t, "A", a, sa, 0), (t, "B", b, sa * (2 * same - 1), 0)]
        p2, p1 = p1, a
    return lines


def rec_member_middle():
    """The free-lay control, as ruled: the member born at the middle at each place (THIRD7's form at the click world's
    dial, y half of 3D), local to its place; each place's setting (its own turned teeth) chooses which reading of the
    place's own record is its outcome: index 0 the landing this round, index 1 whether it changed since the last."""
    alice, bob = born(1), born(2)
    W = circulation([carry(DIAL3, 2, 0)[0]] * (PAIRS + 1), DIAL3, True, 0)
    lines = []
    for t in range(PAIRS):
        turn(alice), turn(bob)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        r0, r1 = 2 * W[t + 1] - 1, 1 if W[t + 1] != W[t] else -1
        lines += [(t, "A", a, r0 if a == 2 else r1, 0), (t, "B", b, r0 if b == 1 else r1, 0)]
    return lines


def rec_at_two():
    """A local act at the bound: both places' outcome the same shared reading h_t, whatever the setting: S = 2."""
    alice, bob, hh = born(1), born(2), born(11)
    lines = []
    for t in range(PAIRS):
        turn(alice), turn(bob), turn(hh)
        a = 2 * click(HALF, alice, 0)
        b = 1 + 2 * click(HALF, bob, 0)
        h = 2 * click(HALF, hh, 0) - 1
        lines += [(t, "A", a, h, 0), (t, "B", b, h, 0)]
    return lines


def to_lines(lines):
    """The pair record in lines and sides alone, every meeting on both sides (format: a test's).
    Per pair event t, at the source place 9 the bearing meeting: the source clock (train 3 + src) gives one quantum to
    each place's outcome clock across (its across sides), and each outcome clock takes it there (the mirror). At each
    place, the setting meeting: the setting clock (train 1) gives one quantum to the setting's partner (train 10 +
    setting), which takes it. The outcome's sign is the outcome clock's own-place meeting with partner train 30."""
    rec = []
    by_t = {}
    for t, place, setting, outcome, src in lines:
        by_t.setdefault(t, {})[place] = (setting, outcome, src)
    for t in sorted(by_t):
        v = by_t[t]
        src = v["A"][2]
        rec.append({"round": t, "site": 9, "train": 3 + src, "q": -2, "sides": [],
                    "across": [[2, 0, -1], [2, 1, -1]]})
        for place, site in (("A", 0), ("B", 1)):
            setting, outcome, _ = v[place]
            rec.append({"round": t, "site": site, "train": 1, "q": -1, "sides": [[10 + setting, -1]], "across": []})
            rec.append({"round": t, "site": site, "train": 10 + setting, "q": 1, "sides": [[1, 1]], "across": []})
            rec.append({"round": t, "site": site, "train": 2, "q": 1 + outcome, "sides": [[30, outcome]],
                        "across": [[3 + src, 9, 1]]})
            rec.append({"round": t, "site": site, "train": 30, "q": -outcome, "sides": [[2, -outcome]], "across": []})
    return rec


def mates(rec):
    """The guard's mates (E's sides.paired, as a stand-in): every side and every across side has its mirror."""
    at = {(ln["round"], ln["site"], ln["train"]): ln for ln in rec}
    for ln in rec:
        for u, q in ln["sides"]:
            m = at.get((ln["round"], ln["site"], u))
            if m is None or [ln["train"], -q] not in m["sides"]:
                return f"REFUSED: the side {ln['train']} to {u} at {ln['round']}, {ln['site']} has no mate"
        for u, p, q in ln["across"]:
            m = at.get((ln["round"], p, u))
            if m is None or [ln["train"], ln["site"], -q] not in m["across"]:
                return f"REFUSED: the across side at {ln['round']}, {ln['site']} has no mate"
    return "read"


def from_lines(rec):
    """Read back from lines and sides alone: a pair is the bearing meeting an outcome's across side names (its round,
    its place and its clock); each place's setting is its setting clock's partner in that round."""
    got = {}
    for ln in rec:
        place = {0: "A", 1: "B"}.get(ln["site"])
        if place is None:
            continue
        if ln["train"] == 1:
            got.setdefault(ln["round"], {}).setdefault(place, [None, None, None])[0] = ln["sides"][0][0] - 10
        elif ln["train"] == 2:
            u, p, _ = ln["across"][0]
            slot = got.setdefault(ln["round"], {}).setdefault(place, [None, None, None])
            slot[1], slot[2] = ln["sides"][0][1], (ln["round"], p, u)
    trials = []
    for t in sorted(got):
        v = got[t]
        if set(v) == {"A", "B"} and None not in v["A"] + v["B"] and v["A"][2] == v["B"][2]:
            trials.append((t, (v["A"][0], v["A"][1], v["A"][2][2]), (v["B"][0], v["B"][1], v["B"][2][2])))
    return trials


def ladder_once(xs_alph, n_out, n, share_den, qexp_of, read):
    """A ladder's share spent once: the four rungs' bounds summed against the share."""
    total = SC * 0
    for L in (1, 2, 4, 8):
        total += ladder_gate(xs_alph, n_out, n, L, share_den, qexp_of(L))[1]
    if total * share_den > SC:
        return ("NOT READ", f"the ladder's gate, {carry(1000000 * total, SC, 0)[0]} per million")
    return read()


def order_e(xs, cut, share_den):
    n = len(xs)
    plus = sum(1 for v in xs if v > 0)
    if plus == 0 or plus == n:
        return ("NOT SHOWN", "the outcomes do not vary")
    if min(plus, n - plus) ** 2 < FIVE * n:
        return ("NOT READ", "lag-1's cells")
    r1, z = order_z2(xs)

    def read():
        amb = [ambiguous(xs, L) for L in (1, 2, 4, 8)]
        return ("SHOWN" if z <= cut and all(v >= AMBIG for v in amb) else "NOT SHOWN", r1, z, amb)
    return ladder_once(([plus, n - plus], [1]), (plus, n - plus), n, share_den, lambda L: L + 1, read)


def joint_past(sets, xs, share_den):
    n = len(xs)
    plus = sum(1 for v in xs if v > 0)
    s0 = sum(1 for s in sets if s == sets[0])
    if plus == 0 or plus == n or s0 == n:
        return ("NOT SHOWN", "the outcomes or settings do not vary")
    sym = [s * o for s in (s0, n - s0) for o in (plus, n - plus)]

    def read():
        amb = []
        for L in (1, 2, 4, 8):
            nexts = {}
            for i in range(L, n):
                ctx = (tuple(zip(sets[i - L:i], xs[i - L:i])), sets[i])
                nexts.setdefault(ctx, set()).add(xs[i])
            amb.append(sum(1 for v in nexts.values() if len(v) >= 2))
        return ("SHOWN" if all(v >= AMBIG for v in amb) else "NOT SHOWN", amb)
    return ladder_once((sym, [s0, n - s0]), (plus, n - plus), n, share_den, lambda L: L + L + 2, read)


def r4h(trials):
    """R4 under (C), per half; N_T = 2 (29 + 6 S); precedence NOT SHOWN first."""
    sources = sorted({A[2] for _, A, _ in trials})
    nt = 2 * (29 + 6 * len(sources))
    cut = CUT_FW[nt]
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
        ev, jp = [], []
        for s in sources:
            for k in (1, 2):
                sub = [(A if k == 1 else Bb) for _, A, Bb in half if A[2] == s]
                ev.append(order_e([v[1] for v in sub], cut, share_den))
                jp.append(joint_past([v[0] for v in sub], [v[1] for v in sub], share_den))
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
        for x_, y_ in ((sa, sb), (sa[1:], ao[:-1]), (sa[1:], bo[:-1]), (sb[1:], ao[:-1]), (sb[1:], bo[:-1])):
            c4 = [0, 0, 0, 0]
            for u, v in zip(x_, y_):
                c4[u + u + v] += 1
            mi.append(chi2x2(*c4))
        lags = {}
        for L in (1, 2, 4, 8):
            for nm, x_, y_ in (("A setting", sa[:-L], ao[L:]), ("B setting", sb[:-L], bo[L:]),
                               ("A outcome", ao[:-L], ao[L:]), ("B outcome", bo[:-L], bo[L:])):
                if L == 1 and nm.endswith("outcome"):
                    continue
                c4 = [0, 0, 0, 0]
                for u, v in zip(x_, y_):
                    c4[u + u + v] += 1
                lags[f"{nm} {L} back"] = chi2x2(*c4)
        hv.append({"(a)": va, "the limit": "NOT SHOWN" if past else "SHOWN", "the curve": worst(curve), "(c)": vc,
                   "2 x 2": "SHOWN" if all(z is not None and z <= cut for z in mi) else "NOT SHOWN",
                   "own past at lags 1, 2, 4, 8": "SHOWN" if all(z is not None and z <= cut for z in lags.values())
                   else "NOT SHOWN", "(e)": worst([e[0] for e in ev]), "the joint past": worst([j[0] for j in jp]),
                   "S": S, "lags": lags, "jp": jp})
    parts = {k: worst([h[k] for h in hv]) for k in ("(a)", "the limit", "the curve", "(c)", "2 x 2",
                                                    "own past at lags 1, 2, 4, 8", "(e)", "the joint past")}
    click_parts = worst(list(parts.values()))
    parts.update({"(b) under (C)": "NOT READ: no seeds' law exists", "(d), the board's cone": "NOT READ: no cone",
                  "the per-clock causal order": "NOT READ: no chain of meetings between the places"})
    return nt, cut, r3v, parts, click_parts, worst([v if not v.startswith("NOT READ") else "NOT READ"
                                                    for v in parts.values()]), hv


say(f"C. R4 under (C) on pair records written as meetings on both sides, {PAIRS} pair events (20,000 a half); the"
    f" settings from each place's own turned teeth (the toy's alice and bob) in every record:")
forms = [("the toy's third click (a format and reading test; its hand reads both settings, no lawful act)",
          po["rec_one"](True)), ("the first click", po["rec_one"](False)),
         ("two first clicks interleaved", po["rec_two_firsts"]()), ("the parity first click", po["rec_parity"]()),
         ("a fixed order of period four", po["rec_period4"]()), ("A's outcome its own previous setting",
                                                                 po["rec_echo"]()),
         ("two back", rec_two_back()), ("parity of two", rec_parity_two()),
         ("two back, flipped 100 per 1,000 (the HALF mathematician's B2)", rec_two_back_flipped(100)),
         ("two back, flipped 200 per 1,000", rec_two_back_flipped(200)),
         ("the free-lay control: the member born at the middle at each place", rec_member_middle()),
         ("a local act at the bound, S = 2 exactly", rec_at_two())]
for label, lines in forms:
    rec = to_lines(lines)
    g_ = mates(rec)
    trials = from_lines(rec)
    nt, cut, r3v, parts, cp, r4v, hv = r4h(trials)
    short = {k: v for k, v in parts.items() if v != "SHOWN"}
    say(f"  {label}: the guard's mates {g_}; {len(rec)} lines, {len(trials)} pairs read back; N_T {nt}, CUT_FW {cut};"
        f" R3 beside {r3v}; S {[h['S'] for h in hv]}; parts not SHOWN {short}; the click parts {cp}; R4 {r4v}")
    worst_lag = max((z, k) for h in hv for k, z in h["lags"].items() if z is not None)
    say(f"    the largest lag z^2 {worst_lag}; the joint past per half {[[j[:2] for j in h['jp']] for h in hv]}")


def right_pairs(n_ev):
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
        lines.append((t, (a, sa, 0), (b, sa * (2 * same - 1), 0)))
    return lines


rows, by = {}, {}
for _ in range(1000):
    nt, cut, r3v, parts, cp, r4v, hv = r4h(right_pairs(4000))
    tally(rows, cp)
    for k, v in parts.items():
        if v == "NOT SHOWN":
            tally(by, k)
say(f"  the rate: 1,000 right pair records of the pattern (a stand-in draw, 2,000 events a half, its settings fair at"
    f" each place; read on the trials, the format tested above): the click parts {rows}; NOT SHOWN by part {by}")

# ================================================================ D. D4 as a static check


def ca_own(A_lines, give, take, B_lines, b1, b2):
    return own(A_lines, take) - own(A_lines, give) - (own(B_lines, b2) - own(B_lines, b1))


def ca_rounds(A_lines, give, take, B_lines, b1, b2):
    return (take - give) - (b2 - b1)


def own(ls, r):
    return sum(1 for t in ls if t < r)


def d4_static(fn_name):
    """D4, a static check of a reading's code: every difference it takes is a difference of own counts (calls of
    own()), never of a round or a face field."""
    tree = ast.parse(lift(Path(__file__).read_text(encoding="utf-8"), fn_name))
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
            for side in (node.left, node.right):
                ok = (isinstance(side, ast.Call) and getattr(side.func, "id", "") == "own") or (
                    isinstance(side, ast.BinOp) and isinstance(side.op, ast.Sub))
                if not ok:
                    return f"refused: a difference of {ast.dump(side)[:40]}... (a round or face field)"
    return "allowed"


say(f"D. D4, a static check: C-a on own counts {d4_static('ca_own')}; its no, the mutant C-a on rounds"
    f" {d4_static('ca_rounds')}")

# ================================================================ G. the readings file, checked
exec(compile("".join(lift(HERE.joinpath("cuts3h.py").read_text(encoding="utf-8"), n) for n in (
    "atan_inv", "exp_half", "poisson_part", "odd_u", "cdf_le", "cdf_ge", "one_ok")), "cuts3h.py", "exec"), globals())
SC = 10 ** 90
TERMS = 320
PI = 16 * atan_inv(5) - 4 * atan_inv(239)
chk = []
for K in (20, 21, 30, 39):
    lo, hi = B3[K]
    chk.append(f"K {K}: hi {hi} upper tail within at C {cdf_ge(hi, K, 239, 240)}, at C - 1 {cdf_ge(hi - 1, K, 239, 240)};"
               f" lo {lo} lower tail within at lo + K {cdf_le(lo + K, K, 1, 240)}, at lo + K + 1"
               f" {cdf_le(lo + K + 1, K, 1, 240)}")
for nt in (70, 82):
    chk.append(f"CUT_FW {nt} {CUT_FW[nt]}: at C {one_ok(CUT_FW[nt], nt)}, at C - 1 {one_ok(CUT_FW[nt] - 1, nt)}")
say("G. The readings file, checked: " + "; ".join(chk))
HERE.joinpath(OUTNAME).write_text("\n".join(out) + "\n", encoding="utf-8")
