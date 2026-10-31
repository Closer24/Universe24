"""ALG3: an equilateral triangle of three alike clocks, and the order of the steps (a toy of whole numbers, never src).

Args: <tree> <rounds> <lays>
Three clocks, one gear each (count now a, before b, edge tooth r), teeth W constant, pairwise joined by three equal
quartic couplings f x_i^2 x_j^2 and each held by its own spring g x_i^2. The step is the engine's gear (step.gear, the
dial 2W from both slots), with the push read two ways:
  - all at once: every clock's push read at the round's counts, then every gear moves (the leapfrog's order);
  - one clock after another: clock 0 moves, then clock 1 reads clock 0's new count, then clock 2 (a family order).
Read, over the six relabellings of the three clocks: does the step commute with each (step(s o g) = step(s) o g)? And
each step's books: the place's residual SUM D (VARY4's) for the step all at once; for the step one clock after another,
each clock's own move against its own staggered energy 2 (f S_i + g) a b, S_i the others' squares as it reads them.
Whole numbers only; Rule3's carry the one division."""
import sys
from itertools import permutations
from pathlib import Path

tree, rounds, nlays = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(tree.joinpath("src")))
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

W, f, g, senses = 200, 1, 3, 2  # the curvature 2 f SUM + 2 g stays below 4 W on the lays below (|x| <= 7)


def push(a, i):
    S = sum(a[j] * a[j] for j in range(3) if j != i)
    return -2 * f * a[i] * S - 2 * g * a[i]


def gear(a, b, r, i, pu):
    a1, b1, r1 = step.gear(a, b, r, 2 * W, 2 * W, pu, senses)
    return a1, b1, r1


def together(s):
    a, b, r = s
    pu = [push(a, i) for i in range(3)]
    moved = [gear(a[i], b[i], r[i], i, pu[i]) for i in range(3)]
    return [m[0] for m in moved], [m[1] for m in moved], [m[2] for m in moved]


def in_turn(s, books=None):
    a, b, r = [list(x) for x in s]
    for i in range(3):
        pu = push(a, i)
        S = sum(a[j] * a[j] for j in range(3) if j != i)
        a1, b1, r1 = gear(a[i], b[i], r[i], i, pu)
        if books is not None:
            work = pu * (a1 - b[i])
            e_before = 2 * (f * S + g) * a[i] * b[i]
            e_after = 2 * (f * S + g) * a1 * b1
            books["sub-step moves whose work != -(the change of its own staggered energy)"] += int(work != -(e_after - e_before))
            books["sub-steps"] += 1
        a[i], b[i], r[i] = a1, b1, r1
    return a, b, r


def relabel(s, p):
    return tuple([x[p[k]] for k in range(3)] for x in s)


def D_place(s0, s1):
    """VARY4's SUM D_i over the place's terms for one round from s0 (a, b) to s1 (a+): T_i(x; y) = J_i(y) x_i."""
    a, b = s0[0], s0[1]
    a1 = s1[0]

    def T(x, y):
        return sum(push(y, i) * x[i] for i in range(3))
    return (T(a1, a) - T(a, a1)) + (T(a, b) - T(b, a))


lays = []
for n in range(nlays):
    _, u = carry(7919 * (n + 1), 13, 0)
    _, v = carry(104729 * (n + 1), 11, 0)
    _, w = carry(1299709 * (n + 1), 9, 0)
    lays.append(([u - 6, v - 5, w - 4], [u - 6, v - 5, w - 4], [0, 0, 0]))
lays.append(([5, 5, 5], [5, 5, 5], [0, 0, 0]))  # a lay every relabelling fixes
lays.append(([7, 3, 3], [7, 3, 3], [0, 0, 0]))  # a lay one transposition fixes
for name, stepper in (("all at once", together), ("one clock after another", in_turn)):
    commuting = {p: 0 for p in permutations(range(3))}
    for s0 in lays:
        for p in commuting:
            s, t = s0, relabel(s0, p)
            ok = True
            for _ in range(rounds):
                s, t = stepper(s), stepper(t)
                if relabel(s, p) != t:
                    ok = False
                    break
            commuting[p] += int(ok)
    print("STEP", name, ": lays where the step commutes with the relabelling, of", len(lays), ":",
          {"".join(str(k) for k in p): c for p, c in commuting.items()})
books = {"sub-step moves whose work != -(the change of its own staggered energy)": 0, "sub-steps": 0}
peakD, nzD = 0, 0
for s0 in lays:
    s = s0
    total = 0
    for _ in range(rounds):
        s1 = together(s)
        total += D_place(s, s1)
        peakD, nzD = max(peakD, abs(total)), nzD + int(total != 0)
        s = s1
    s = s0
    for _ in range(rounds):
        s = in_turn(s, books)
biggest = 0
for s0 in lays:
    s = s0
    for _ in range(rounds):
        s = together(s)
        biggest = max(biggest, max(abs(v) for v in s[0]))
print("BOUND: the largest count on any lay over the run, all at once:", biggest)
print("BOOKS: all at once, the place's running SUM D: largest", peakD, "; not 0 at", nzD, "of", rounds * len(lays),
      "lay-rounds. One clock after another:", books)
# the triangle's circulating passing y = P01 + P12 - P02, each edge passing the difference of its own coupling's works
# on its two clocks, P_ij = W_i(ij) - W_j(ij), W_i(ij) = (-2 f a_i a_j^2)(a+_i - b_i): read on a generic lay and on the
# two lays a relabelling fixes (every relabelling the first, the transposition (1 2) the second)
for s0 in lays:
    s = s0
    ys = []
    for _ in range(rounds):
        s1 = together(s)
        a, b, a1 = s[0], s[1], s1[0]

        def Wk(i, j):
            return (-2 * f * a[i] * a[j] * a[j]) * (a1[i] - b[i])
        P01, P12, P02 = Wk(0, 1) - Wk(1, 0), Wk(1, 2) - Wk(2, 1), Wk(0, 2) - Wk(2, 0)
        ys.append(P01 + P12 - P02)
        s = s1
    print("LAY", s0[0], ": the circulating passing y = P01 + P12 - P02 not 0 in", sum(1 for y in ys if y), "of",
          rounds, "rounds; largest", max(abs(y) for y in ys))
print("END")
