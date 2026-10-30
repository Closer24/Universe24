"""Born's rule for position on the fair draw, carried along the Meshes; and one quantum at two detectors (Grangier).

usage: python3 -I p3_born_position.py <tensor24 worktree>/src
(A) A hand spread over n Node-clocks on a ring, its parts' sizes rho(x) = N(psi(x)) from Gaussian integers. The click
    is a tournament of two-part split clicks, each at one Mesh: the two parts' sizes meet there, the fair draw at the
    Mesh's Node-clock picks a side with odds by the sizes, the winner keeps the whole winding of both, and the loser's
    wind travels to it along the Meshes, one Mesh per tick. Two schedules: (A1) a fixed tree by position; (A2) each
    part merges with the neighbouring part of the larger size (the rank count of the sizes, ties by the lower size
    first), a schedule the 24 leave alike. Exact distributions by recursion over every draw's full turn (each merge's
    side drawn sigma times in L over its turn), against rho(x) / SUM rho.
(B) The same tournament driven by the dial's own draws on stage 7a's act (p2's board, the fine teeth in pitch units,
    d = (c + V) mod L at the merging Node-clock), one quantum starting at each beat, its k-th round of merges read at
    the k-th beat after: the clicks' positions against Born.
(C) One quantum at two detectors: the split gives the whole winding to one; coincidences, and g2 = <n_A n_B> /
    (<n_A> <n_B>), exact over the full turn, for one quantum and for two quanta each with its own draw.
"""
import importlib.util
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("p2", os.path.join(HERE, "p2_fair_draw_engine.py"))
sys.argv = [sys.argv[0], sys.argv[1]]
p2 = importlib.util.module_from_spec(spec)
_print = print
import builtins  # noqa: E402

builtins.print = lambda *a, **k: None  # p2 prints its own tables on import; silence them here
spec.loader.exec_module(p2)
builtins.print = _print


def norm(z):
    return z[0] * z[0] + z[1] * z[1]


PSI = [(3, 1), (2, -2), (0, 1), (1, 4), (-2, 0), (5, 1), (1, 1), (0, -3)]  # a hand's Gaussian parts on 8 Node-clocks
RHO = [norm(z) for z in PSI]
N = len(RHO)
TOTAL = sum(RHO)
print(f"the hand: psi {PSI}, rho {RHO}, SUM rho {TOTAL}")


def merge_prob(sa, sb):
    return Fraction(sa, sa + sb)  # the fair draw over its full turn: side a exactly sa times in sa + sb


def tree_schedule():
    """(A1): regions [i, i + 2^k) merge pairwise by position; the winner's Node-clock holds both."""
    dist = {}

    def rec(parts, p, ticks):
        # parts: list of (holder Node-clock, size, first, last) in ring order
        if len(parts) == 1:
            holder = parts[0][0]
            dist[holder] = dist.get(holder, 0) + p
            rec.ticks = max(rec.ticks, ticks)
            return
        pairs = [(parts[i], parts[i + 1]) for i in range(0, len(parts) - 1, 2)]
        rest = [parts[-1]] if len(parts) % 2 else []
        # each pair's two outcomes; the loser's wind travels from its holder to the winner's: |holder distance| ticks
        def branch(k, acc, prob, travel):
            if k == len(pairs):
                rec(acc + rest, prob, ticks + travel)
                return
            (ha, sa, fa, la), (hb, sb, fb, lb) = pairs[k]
            gap = abs(hb - ha)
            branch(k + 1, acc + [(ha, sa + sb, fa, lb)], prob * merge_prob(sa, sb), max(travel, gap))
            branch(k + 1, acc + [(hb, sa + sb, fa, lb)], prob * merge_prob(sb, sa), max(travel, gap))

        branch(0, [], p, 0)

    rec.ticks = 0
    rec([(x, RHO[x], x, x) for x in range(N)], Fraction(1), 0)
    return dist, rec.ticks


def matching_schedule():
    """(A2): each part points to its larger neighbouring part (ring order of the parts; ties to the lower holder's
    side by the rank count of (size, holder)); two parts pointing at each other merge, the others wait."""
    dist = {}

    def rec(parts, p, depth):
        if len(parts) == 1:
            dist[parts[0][0]] = dist.get(parts[0][0], 0) + p
            rec.depth = max(rec.depth, depth)
            return
        m = len(parts)
        key = [(sz, -h) for h, sz in parts]
        point = []
        for i in range(m):
            left, right = (i - 1) % m, (i + 1) % m
            point.append(left if key[left] > key[right] else right)
        merged, used = [], set()
        for i in range(m):
            j = point[i]
            if point[j] == i and i < j and i not in used and j not in used:
                merged.append((i, j))
                used |= {i, j}
        if not merged:  # a ring of parts pointing round in one sense: the largest merges with the one it points to
            i = max(range(m), key=lambda t: key[t])
            merged, used = [(min(i, point[i]), max(i, point[i]))], {i, point[i]}

        def branch(k, acc, prob):
            if k == len(merged):
                order = sorted(acc + [(parts[t][0], parts[t][1], t) for t in range(m) if t not in used], key=lambda e: e[2])
                rec([(h, s) for h, s, _ in order], prob, depth + 1)
                return
            i, j = merged[k]
            (ha, sa), (hb, sb) = parts[i], parts[j]
            branch(k + 1, acc + [(ha, sa + sb, i)], prob * merge_prob(sa, sb))
            branch(k + 1, acc + [(hb, sa + sb, i)], prob * merge_prob(sb, sa))

        branch(0, [], p)

    rec.depth = 0
    rec([(x, RHO[x]) for x in range(N)], Fraction(1), 0)
    return dist, rec.depth


born = {x: Fraction(RHO[x], TOTAL) for x in range(N)}
d1, ticks = tree_schedule()
d2, depth = matching_schedule()
print(f"(A1) the tree by position: P(x) = rho(x) / SUM rho at every Node-clock: {d1 == born}; "
      f"the loser's wind travels at most {ticks} Meshes in all, one Mesh per tick")
print(f"(A2) the larger-neighbour matching: P(x) = rho(x) / SUM rho at every Node-clock: {d2 == born}; rounds {depth}")
print(f"     P = {[str(d1[x]) for x in range(N)]}")

# (B) the dial's own draws on 7a's act drive the tournament (A1), one quantum per beat
nb, records = p2.run(11, True, ticks=3000, pitch=True)
counts = [0] * N
quanta = 0
for t in range(50, len(records) - 3):
    holders = [(x, RHO[x]) for x in range(N)]
    level = 0
    while len(holders) > 1:
        c, v = records[t + level]  # each round of merges at a later beat, after the losers' wind has travelled
        level += 1
        nxt = []
        for i in range(0, len(holders) - 1, 2):
            (ha, sa), (hb, sb) = holders[i], holders[i + 1]
            L = sa + sb
            d = (int(c[ha]) + int(v[ha])) % L  # the draw at the merging Node-clock: its dial and its digits
            nxt.append((ha, L) if d < sa else (hb, L))  # the rank count: side a where d < sigma_a
        if len(holders) % 2:
            nxt.append(holders[-1])
        holders = nxt
    counts[holders[0][0]] += 1
    quanta += 1
chi = sum((k - quanta * RHO[x] / TOTAL) ** 2 / (quanta * RHO[x] / TOTAL) for x, k in enumerate(counts))
print(f"(B) on 7a's act, {quanta} quanta, one per beat, each tournament drawn by the merging Node-clocks' own dials:")
print(f"    clicks per Node-clock {counts}; Born's expectation {[round(quanta * r / TOTAL, 1) for r in RHO]}; "
      f"chi-square {chi:.1f} on {N - 1}")

# (C) one quantum at two detectors (equal arms), and two quanta each with its own draw
L = 2
one = {"A": 0, "B": 0, "AB": 0}
for d in range(L):  # the full turn of the one draw
    one["A" if d < 1 else "B"] += 1
nA, nB, nAB = Fraction(one["A"], L), Fraction(one["B"], L), Fraction(0)  # the whole winding goes to one: never both
g2_one = nAB / (nA * nB)
pairs = [(d1_, d2_) for d1_ in range(L) for d2_ in range(L)]  # two quanta, two independent full turns
EnA = sum(Fraction((d1_ < 1) + (d2_ < 1), len(pairs)) for d1_, d2_ in pairs)
EnB = sum(Fraction((d1_ >= 1) + (d2_ >= 1), len(pairs)) for d1_, d2_ in pairs)
EnAB = sum(Fraction(((d1_ < 1) + (d2_ < 1)) * ((d1_ >= 1) + (d2_ >= 1)), len(pairs)) for d1_, d2_ in pairs)
print(f"(C) one quantum at two detectors: P(A) {nA}, P(B) {nB}, both {nAB}: g2 = {g2_one} (Grangier's anticorrelation)")
print(f"    two quanta, each with its own full turn: <n_A> {EnA}, <n_B> {EnB}, <n_A n_B> {EnAB}: g2 = {EnAB / (EnA * EnB)} "
      f"(1 - 1/n at n = 2)")
# the same on 7a's act: one quantum per beat at two Node-clocks one Mesh apart, the draw at the first
hits = {"A": 0, "B": 0, "AB": 0}
for c, v in records[50:]:
    d = (int(c[0]) + int(v[0])) % 2
    hits["A" if d < 1 else "B"] += 1
q = len(records) - 50
print(f"    on 7a's act, {q} single quanta: A {hits['A']}, B {hits['B']}, both {hits['AB']}: g2 = 0")
