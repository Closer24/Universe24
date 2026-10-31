"""SPLIT2's probe: the weights from the law, read on Big Pic's toys (origin/bigpic-3clicks 18561a673,
tools/derivations/open_items/derive/bigpic/three_clicks/turnteeth.py and threeclicks.py, copied unchanged into
split/bp3/). Each toy's definitions are run as written up to its own main loop (its turn, unturn, step and back; its dial
D, the click world's key 50,811,429; its passing's divisor 1,250), and nothing of its main loop runs. The toys' own
carries are Python's divmod at a positive dial, which is Rule3's carry (carry.py: u // d, u % d).

This probe's own arithmetic is whole numbers alone, every division Rule3's carry (tensor24.algebra.carry.carry from
node-live's src, exported into split/nl/). No float, true division, root, round, math, random, sine or cosine. The
lay of the teeth is a STAND-IN: a whole-number carry sequence (the 64-bit linear congruential constants named below),
standing in for a lay that varies below the clicks; the squares 16, 9, 4 and 1 are the toys' stand-in squares.

(a) equal squares: two takers of square 16 each, over stand-in lays, turned and carried; z^2 of the takes against the
    binomial's half, in thousandths; and the toy's 9 : 16 split against 9/25;
(b) the swap of the two takers: their giver edges' teeth exchanged, the takers' edge's tooth complemented (its
    orientation reversed), their passings exchanged; the swapped run against the original run with its takers swapped,
    round by round; and the turn's matrix T against P T P, P the swap;
(c) counting equal whole parts on threeclicks.py's n-taker turn: two takers of squares 4 and 1 against five takers of
    square 1, the first four counted together;
(d) the square as a count: the classes of the Gaussian integers modulo a two-row hand's own a + b i, counted;
(e) the 24 do not pick the square: the sum of absolute rows is as invariant under the 24 as the sum of squares."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import kinds as K  # noqa: E402
from tensor24.runner import files as F  # noqa: E402

out = []
say = out.append


def toy(name: str, cut: str, argv: list[str]) -> dict:
    """A toy's definitions, run as written up to its main loop (the line beginning `cut`), with argv as given."""
    text = HERE.joinpath("bp3", name).read_text(encoding="utf-8")
    head = text.split(cut)[0]
    keep = sys.argv
    sys.argv = [name, *argv]
    space: dict = {}
    exec(compile(head, name, "exec"), space)  # noqa: S102
    sys.argv = keep
    return space


T = toy("turnteeth.py", "rng = random.Random(31)", ["50811429", "1", "1", "1250"])
D, c, k = T["D"], T["c"], T["k"]

# the stand-in lay: a 64-bit linear congruential sequence by Rule3's carry (a stand-in, named so)
MUL, ADD = 6364136223846793005, 1442695040888963407
MOD = 18446744073709551616


def lay_teeth(seed: int, n: int) -> tuple[list[int], int]:
    """n teeth in [-c, c] from the stand-in sequence, and the sequence's next state."""
    teeth = []
    s = seed
    for _ in range(n):
        _, s = carry(s * MUL + ADD, MOD, 0)
        _, t = carry(s, D, 0)
        teeth.append(t - c)
    return teeth, s


def thousandths(num: int, den: int) -> int:
    q, _ = carry(1000 * num, den, 0)
    return q


def z2_half(ta: int, tb: int) -> int:
    """z^2 of ta against the binomial's half of ta + tb, in thousandths: (ta - tb)^2 / (ta + tb)."""
    return thousandths((ta - tb) * (ta - tb), ta + tb)


def z2_share(t: int, n: int, m: int, mm: int) -> int:
    """z^2 of t takes of n against the share m / mm, in thousandths: (mm t - m n)^2 / (n m (mm - m))."""
    return thousandths((mm * t - m * n) * (mm * t - m * n), n * m * (mm - m))


def run(u: list[int], xa: int, xb: int, rounds: int, turned: int) -> tuple[list[tuple[int, int]], list[int]]:
    seq = []
    for _ in range(rounds):
        u, qa, qb = T["step"](u, xa, xb, turned)
        seq.append((qa, qb))
    return seq, u


LAYS, ROUNDS = 20, 100000
say(f"turnteeth.py: dial D {D}, birth c {c}, k = D div 1250 = {k}; {LAYS} stand-in lays of {ROUNDS} rounds each")

# (a) equal squares
for turned in (1, 0):
    sa = sb = past = zsum = 0
    rows = []
    seed = 12345
    for lay in range(LAYS):
        u0, seed = lay_teeth(seed, 3)
        seq, _ = run(list(u0), 16 * k, 16 * k, ROUNDS, turned)
        ta = sum(q for q, _ in seq)
        tb = sum(q for _, q in seq)
        z = z2_half(ta, tb)
        zsum += z
        past += int(z > 3841)
        sa, sb = sa + ta, sb + tb
        rows.append(f"{ta}:{tb}")
    word = "turned" if turned else "carried (no turn)"
    say(f"(a) squares 16 and 16, {word}: takes per lay {' '.join(rows)}")
    say(f"    pooled {sa} : {sb}, z^2 {z2_half(sa, sb)} thousandths against the binomial's half; the sum of the {LAYS}"
        f" lays' z^2 {zsum} thousandths (chance's mean {LAYS} 000); lays past 3,841: {past} (chance 1 of 20)")
sa = sb = 0
seed = 777
for lay in range(LAYS):
    u0, seed = lay_teeth(seed, 3)
    seq, _ = run(list(u0), 9 * k, 16 * k, ROUNDS, 1)
    sa += sum(q for q, _ in seq)
    sb += sum(q for _, q in seq)
say(f"(a) the toy's squares 9 and 16, turned: pooled {sa} : {sb}, the first's share {thousandths(sa, sa + sb)} thousandths"
    f" against 9/25 = 360; z^2 {z2_share(sa, sa + sb, 9, 25)} thousandths")


# (b) the swap
def swap(u: list[int]) -> list[int]:
    ga, ab, gb = u
    return [gb, -ab, ga]


def matrix(f) -> list[list[int]]:
    cols = [f([1 if i == j else 0 for i in range(3)]) for j in range(3)]
    return [[cols[j][i] for j in range(3)] for i in range(3)]


Tm = matrix(T["turn"])
Pm = matrix(swap)
PTP = matrix(lambda v: swap(T["turn"](swap(v))))
Ti = matrix(T["unturn"])
say(f"(b) the turn's matrix T on (giver-a, a-b, giver-b): {Tm}; the swap P: {Pm}")
say(f"    P T P = {PTP}; equal to T: {PTP == Tm}; equal to T's inverse {Ti}: {PTP == Ti}")
LB, RB = 10, 50000
for squares in ((16, 16), (9, 16)):
    for turned in (1, 0):
        same = 0
        firsts = []
        totals_ok = 0
        seed = 4242
        tot = [0, 0, 0, 0]
        for lay in range(LB):
            u0, seed = lay_teeth(seed, 3)
            xa, xb = squares[0] * k, squares[1] * k
            seq, _ = run(list(u0), xa, xb, RB, turned)
            sw, _ = run(swap(list(u0)), xb, xa, RB, turned)
            match = [int(p == (q[1], q[0])) for p, q in zip(sw, seq)]
            same += sum(match)
            first = next((i + 1 for i, m in enumerate(match) if m == 0), 0)
            firsts.append(first)
            ta, tb = sum(q for q, _ in seq), sum(q for _, q in seq)
            sa_, sb_ = sum(q for q, _ in sw), sum(q for _, q in sw)
            totals_ok += int((sa_, sb_) == (tb, ta))
            tot = [tot[0] + ta, tot[1] + tb, tot[2] + sa_, tot[3] + sb_]
        word = "turned" if turned else "carried (no turn)"
        shown = " ".join(str(f) for f in firsts)
        say(f"(b) squares {squares[0]} and {squares[1]}, {word}: the swapped run equals the original run swapped at"
            f" {same} of {LB * RB} rounds ({LB} lays of {RB}); first round apart per lay (0: never): {shown};"
            f" totals swapped exactly in {totals_ok} of {LB} lays; pooled original {tot[0]} : {tot[1]}, swapped {tot[2]} : {tot[3]}")

# (c) counting equal whole parts, on threeclicks.py's n-taker turn
C3 = toy("threeclicks.py", "squares = {1:", [])


def many(squares: list[int], lays: int, rounds: int, seed: int) -> list[int]:
    n = len(squares)
    xs = [s * k for s in squares]
    tot = [0] * n
    for _ in range(lays):
        ug, seed = lay_teeth(seed, n)
        tt, seed = lay_teeth(seed, len(C3["edges"](n)))
        ut = dict(zip(C3["edges"](n), tt))
        for _ in range(rounds):
            qs = C3["step"](ug, ut, xs, n)
            tot = [a + b for a, b in zip(tot, qs)]
    return tot


L3, R3 = 10, 50000
two = many([4, 1], L3, R3, 99)
five = many([1, 1, 1, 1, 1], L3, R3, 99)
n2, n5 = sum(two), sum(five)
group = sum(five[:4])
say(f"(c) threeclicks.py's turn, {L3} stand-in lays of {R3} rounds: squares 4 and 1: {two[0]} : {two[1]}, the first's"
    f" share {thousandths(two[0], n2)} thousandths against 4/5 = 800, z^2 {z2_share(two[0], n2, 4, 5)} thousandths")
say(f"    five takers of square 1: {five}; the first four together {group} of {n5}, share {thousandths(group, n5)}"
    f" thousandths against 800, z^2 {z2_share(group, n5, 4, 5)}; each alone against 1/5:"
    f" {[z2_share(t, n5, 1, 5) for t in five]} thousandths")
mill = lambda num, den: carry(1000000 * num, den, 0)[0]  # noqa: E731
say(f"    the takes per round per unit of square: two takers {mill(n2, 5 * L3 * R3)}, five takers"
    f" {mill(n5, 5 * L3 * R3)} millionths of a take (k / D = {mill(k, D)} millionths)")


# (d) the square as a count of equal whole parts: classes of Z[i] modulo a + b i
def classes(a: int, b: int) -> tuple[int, int]:
    n = a * a + b * b
    inside = 0
    for x in range(n):
        for y in range(n):
            _, r1 = carry(x * a + y * b, n, 0)
            _, r2 = carry(y * a - x * b, n, 0)
            inside += int(r1 == 0 and r2 == 0)
    q, r = carry(n * n, inside, 0)
    return q, r


for a, b in ((1, 1), (2, 1), (1, 2), (2, 2), (3, 2), (4, 3), (5, 0)):
    q, r = classes(a, b)
    say(f"(d) the hand ({a}, {b}): its square {a * a + b * b}; classes of Z[i] modulo {a} + {b} i: {q} (remainder {r})")
for n in (2, 3, 5):
    say(f"(d) one row of count {n}: classes of Z modulo {n}: {n}, against its square {n * n}")

# (d') the whole quaternions: a hand q of four rows (one scalar, three along the Spokes) with its vector part not 0
# satisfies q q = t q - n, t = 2 Re q and n = N(q), by Hamilton's product; so Z[q] = Z + Z q, and multiplying by q on
# the basis (1, q) is [[0, -n], [1, t]], of determinant n: the classes of the hand's own ring modulo the hand number n.
def ham(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


hold_ok = coeff_ok = tried = 0
seed = 2024
for _ in range(1000):
    rows, seed = lay_teeth(seed, 4)
    q = tuple(carry(r, 41, 0)[1] - 20 for r in rows)  # a stand-in hand, each row within [-20, 20]
    at = next((i for i in (1, 2, 3) if q[i] != 0), 0)
    if at == 0:
        continue
    tried += 1
    t2, n = 2 * q[0], sum(x * x for x in q)
    qq = ham(q, q)
    hold_ok += int(qq == tuple(t2 * x - (n if i == 0 else 0) for i, x in enumerate(q)))
    # q q's coefficients on (1, q), found from Hamilton's product alone: beta from a vector row by Rule3's carry (its
    # remainder 0 where q q lies in Z + Z q), alpha from the scalar row; the ideal q Z[q] is spanned by q 1 = (0, 1) and
    # q q = (alpha, beta), so its index in Z[q] is |alpha|, the determinant of [[0, alpha], [1, beta]]
    beta, left = carry(qq[at], q[at], 0)
    alpha = qq[0] - beta * q[0]
    rest = [qq[i] - beta * q[i] for i in (1, 2, 3)]
    coeff_ok += int(left == 0 and rest == [0, 0, 0] and beta == t2 and -alpha == n)
say(f"(d') {tried} stand-in whole quaternion hands with a vector part, rows within [-20, 20]: q q = t q - n by Hamilton's"
    f" product at {hold_ok}; q q's coefficients on (1, q) read from the product, beta = t and alpha = -n, at {coeff_ok}:"
    f" the index of q Z[q] in Z[q], |alpha|, is the square n")
three = [n for n in range(1, 65) if not any(a * a + b * b + c * c == n for a in range(9) for b in range(9) for c in range(9))]
four = [n for n in range(1, 65) if not any(a * a + b * b + c * c + d * d == n for a in range(9) for b in range(9) for c in range(9) for d in range(9))]
say(f"(d') squares 1 to 64 that no three-row hand holds (Legendre: 4^a (8 b + 7)): {three}; that no four-row hand holds (Lagrange): {four}")

# (e) the 24 and the measure
spokes = F.star(3)
matrices, weight = K.turns(spokes)
kept = [m for m, w in zip(matrices, weight) if int(w) == 1]
vectors = [(3, 0, 0), (2, 2, 1), (1, 2, 2), (3, 4, 0)]
l1_ok = sq_ok = 0
for m in kept:
    for v in vectors:
        w = [sum(int(m[i][j]) * v[j] for j in range(3)) for i in range(3)]
        l1_ok += int(sum(abs(x) for x in w) == sum(abs(x) for x in v))
        sq_ok += int(sum(x * x for x in w) == sum(x * x for x in v))
say(f"(e) the 24 turns ({len(kept)} of {len(matrices)} candidates), {len(vectors)} T1 hands: the sum of squares kept at"
    f" {sq_ok} of {len(kept) * len(vectors)}, the sum of absolute rows kept at {l1_ok} of {len(kept) * len(vectors)};"
    f" (3, 0, 0) and (2, 2, 1): squares 9 and 9, absolute sums 3 and 5")

target = HERE.joinpath(sys.argv[1] if len(sys.argv) > 1 else "split2_probe.txt")
target.write_text("\n".join(out) + "\n", encoding="utf-8")
