"""The pair world's two ends, path (C) (the owner's word of 08:2x UTC through #2187 6541185833), and its controls, in
whole numbers and Rule3's carry. A hand born at a source and carried by the board's act to two wings; each wing reads
only its own copy of the hand and its own setting, drawn by its own late-chooser teeth; the settings are the
triangle's own, 0 and 60 degrees at wing A, 30 and 90 at wing B. Every group of teeth is born apart and turned apart
(pairwhole.py's turn) on the click world's key D, so nothing is chosen for an outcome. The hand's copy is read on the
dial H as the place of its tooth, H (tooth) div D: the turn on the dial H alone repeats every 76,056 rounds, too short
for a free hand.
  (X)  exact, over the hand's H values: under the sign rule every hand value gives CHSH +2 or -2 (Bell's count), so
       any measure of the hand that does not read the settings gives at most 2; the exact readings of the sign rule,
       the member rule and the timelike rule over an even hand; and two seeds' laws with nothing picked, each read
       exactly: the end at the middle (each member's end tooth at its dial's middle, the time mirror of the birth at
       the middle) and one birth with one death (the two wings' member teeth born as one tooth and ending as one);
  (B)  forward from a free start, two local rules at each wing: the sign of the hand within 90 degrees of the
       setting, and the member's landing on its own tooth at the share 1 - 2 d / H of the hand's distance d from
       the setting;
  (C0) the same world laid from a free end: each wing's end (its copy of the hand, its chooser's teeth, its member's
       tooth) laid apart, kept where the two copies, run back, meet in one birth; each member's landing is read back
       from its end tooth, and its start tooth recovered and run forward again to the same end tooth and the same
       landing (the run back exact) at every kept pair. The choosers and members turn at each kept end: they are apart
       from the copies, so the keeping reads none of them;
  (T)  the timelike case: wing A's setting and landing carried on to wing B, inside its cone, and B's own member
       landing at Malus's share for the two settings (pairwhole's rule). Refused under the owner's 11:47 and 11:52
       laws (a click writes nothing on the board; the connection comes from the start and the end), and kept only as
       a control of what the law forbids.
Each sampled reading is CHSH per mille, each wing's +1 share under the far setting (no signal), and the order of each
wing's landings (its landing times the landing one and two pairs later, per mille), twice.

Usage: python3 -I twoends.py <src> [pairs, 200000 unless given; the free end keeps a quarter of them] [runs, 2 unless
given, each from its own births]
"""
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

PAIRS = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
KEEP, _ = carry(PAIRS, 4, 0)
RUNS = int(sys.argv[3]) if len(sys.argv) > 3 else 2
D = 50811429  # the click world's key: every group's dial
H = 97  # the hand's dial, odd
N = 4
C, _ = carry(D - 1, 2, 0)
HALF = C
SAME = {1: carry(3 * D, 4, 0)[0], 3: 0}  # Malus's share of equal landings 30 and 90 degrees apart (pairwhole's rule)
SETS = {(0, 1): 1, (0, 3): -1, (2, 1): 1, (2, 3): 1}


def cen(v):
    _, r = carry(v + C, D, 0)
    return r - C


def turn(u):
    for i in range(1, N):
        u[i] = cen(u[i] + u[i - 1])
    u[0] = cen(u[0] + u[N - 1])


def born(times):
    u = [0] * N
    for _ in range(times):
        u[0] = cen(u[0] + 1)
        turn(u)
    return u


def click(x, u):
    q, r = carry(u[0] + C + x, D, 0)
    u[0] = r - C
    return q


def copy(u):  # the hand's copy on the dial H: the place of its tooth
    lam, _ = carry(H * (u[0] + C), D, 0)
    return lam


def place(units):  # a setting in units of 30 degrees, on the hand's dial
    p, _ = carry(units * H, 12, 0)
    return p


def dist(lam, units):
    _, r = carry(lam - place(units), H, 0)
    far, _ = carry(r, carry(H + 1, 2, 0)[0], 0)
    return r + far * (H - 2 * r)


def sign_rule(lam, units):  # +1 within 90 degrees of the setting
    q, _ = carry(4 * dist(lam, units), H, 0)
    return 1 - 2 * q


def share(lam, units):  # the member's teeth of +1 landings, D (1 - 2 d / H), by one carry
    g, _ = carry(D * (H - 2 * dist(lam, units)), H, 0)
    return g


def member_rule(lam, units, member):
    return 2 * click(share(lam, units), member) - 1


def read_back(g, end):  # the landing read back from the end tooth; the start tooth; forward again to the same end
    q, _ = carry(g - 1 - (end + C) + D, D, 0)
    start = [cen(end - g)]
    again = click(g, start)
    return 2 * q - 1, again == q and start[0] == end


def chsh(rec):
    num, cnt = {}, {}
    for a, b, sa, sb in rec:
        num[(a, b)] = num.get((a, b), 0) + sa * sb
        cnt[(a, b)] = cnt.get((a, b), 0) + 1
    total = 0
    for ab, sg in SETS.items():
        e, _ = carry(1000 * num[ab], cnt[ab], 0)
        total += sg * e
    return total


def signal(rec):
    out = []
    for far in (1, 3):
        sel = [r for r in rec if r[1] == far]
        out.append(carry(1000 * sum(1 for r in sel if r[2] == 1), len(sel), 0)[0])
    for far in (0, 2):
        sel = [r for r in rec if r[0] == far]
        out.append(carry(1000 * sum(1 for r in sel if r[3] == 1), len(sel), 0)[0])
    return out


def order(rec):  # each wing's landing times its landing one and two pairs later, per mille: A's lags 1, 2, then B's
    out = []
    for w in (2, 3):
        for lag in (1, 2):
            n = len(rec) - lag
            out.append(carry(1000 * sum(rec[t][w] * rec[t + lag][w] for t in range(n)), n, 0)[0])
    return out


# (X) exact, over the hand's H values
per_hand = {}
sign_sum = 0
for lam in range(H):
    s = sum(sg * sign_rule(lam, a) * sign_rule(lam, b) for (a, b), sg in SETS.items())
    per_hand[s] = per_hand.get(s, 0) + 1
    sign_sum += s
member_num = sum(sg * (2 * share(lam, a) - D) * (2 * share(lam, b) - D)
                 for (a, b), sg in SETS.items() for lam in range(H))
print(f"(X) exact, over the hand's {H} values:", flush=True)
print(f"  the sign rule's CHSH at each hand value (CHSH: hand values): {sorted(per_hand.items())};"
      f" any measure of the hand that does not read the settings averages these, at most 2", flush=True)
print(f"  over an even hand: the sign rule {carry(1000 * sign_sum, H, 0)[0]} per mille, the member rule"
      f" {carry(1000 * member_num, H * D * D, 0)[0]}, the timelike rule"
      f" {carry(1000 * (3 * (2 * SAME[1] - D) + D), D, 0)[0]}",
      flush=True)

# the end at the middle: each member's landing read back from an end tooth at the middle (0 about the middle)
middle = sum(1 for lam in range(H) for u in range(4) if read_back(share(lam, u), 0)[0] == sign_rule(lam, u))
print(f"  the end at the middle: the landing read back is the sign rule at {middle} of {4 * H} (hand value, setting);"
      f" so it reads at most 2, and {carry(1000 * sign_sum, H, 0)[0]} per mille over an even hand", flush=True)
# one birth and one death: one start tooth m for both members and one end tooth, m + g_A = m + g_B on the dial,
# so a pair is kept only where the two shares are equal, and then the two landings are one landing
kept_one = {ab: [lam for lam in range(H) if share(lam, ab[0]) == share(lam, ab[1])] for ab in SETS}
a_share = {ab: [carry(1000 * share(lam, ab[0]), D, 0)[0] for lam in kept_one[ab]] for ab in SETS}
print(f"  one birth and one death: the hand values kept per setting pair {kept_one}, each pair's two landings one"
      f" landing, so CHSH {1000 * sum(SETS.values())} per mille; A's +1 share in per mille under B's settings 1 and 3"
      f" at A's setting 0: {a_share[(0, 1)]} and {a_share[(0, 3)]}, a signal", flush=True)

for run in range(1, RUNS + 1):
    base = 20 * run
    hand, cho_a, cho_b, mem_a, mem_b, t_a, t_b = (born(base + k) for k in range(1, 8))
    rec_sign, rec_member, rec_t = [], [], []
    for _ in range(PAIRS):
        for u in (hand, cho_a, cho_b, mem_a, mem_b, t_a, t_b):
            turn(u)
        a = 2 * click(HALF, cho_a)
        b = 1 + 2 * click(HALF, cho_b)
        lam = copy(hand)
        rec_sign.append((a, b, sign_rule(lam, a), sign_rule(lam, b)))
        rec_member.append((a, b, member_rule(lam, a, mem_a), member_rule(lam, b, mem_b)))
        sa = 2 * click(HALF, t_a) - 1
        sb = sa * (2 * click(SAME[abs(b - a)], t_b) - 1)
        rec_t.append((a, b, sa, sb))
    # (C0) the free end: each wing's end laid apart; kept where the two copies, run back, meet in one birth
    end_a, end_b, cho_ea, cho_eb, mem_ea, mem_eb = (born(base + k) for k in range(8, 14))
    rec_es, rec_em, kept, tried, exact = [], [], [0] * H, 0, 0
    while len(rec_es) < KEEP:
        tried += 1
        turn(end_a)
        turn(end_b)
        la, lb = copy(end_a), copy(end_b)
        if la == lb:
            kept[la] += 1
            for u in (cho_ea, cho_eb, mem_ea, mem_eb):
                turn(u)
            a = 2 * click(HALF, cho_ea)
            b = 1 + 2 * click(HALF, cho_eb)
            rec_es.append((a, b, sign_rule(la, a), sign_rule(la, b)))
            xa, ok_a = read_back(share(la, a), mem_ea[0])
            xb, ok_b = read_back(share(la, b), mem_eb[0])
            exact += 1 if ok_a and ok_b else 0
            rec_em.append((a, b, xa, xb))
    print(f"run {run}, {PAIRS} pairs forward, {KEEP} kept at the free end:", flush=True)
    print(f"  (B) the sign rule, forward: CHSH {chsh(rec_sign)} per mille; the +1 shares under the far setting"
          f" {signal(rec_sign)}; the order {order(rec_sign)}", flush=True)
    print(f"  (B) the member's landing, forward: CHSH {chsh(rec_member)} per mille; {signal(rec_member)};"
          f" the order {order(rec_member)}",
          flush=True)
    print(f"  (C0) the free end ({KEEP} kept of {tried} laid; each hand value kept {min(kept)} to {max(kept)} times):",
          flush=True)
    print(f"       the sign rule: CHSH {chsh(rec_es)} per mille; {signal(rec_es)}; the order {order(rec_es)}",
          flush=True)
    print(f"       the member's landing read back from its end tooth: CHSH {chsh(rec_em)} per mille; {signal(rec_em)};"
          f" the order {order(rec_em)}; the run back exact at {exact} of {KEEP}", flush=True)
    print(f"  (T) the timelike case, A's landing carried to B: CHSH {chsh(rec_t)} per mille; {signal(rec_t)};"
          f" the order {order(rec_t)}",
          flush=True)
