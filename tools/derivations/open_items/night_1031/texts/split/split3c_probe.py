"""SPLIT3's third probe, the hostile physicist's B3 read again (scratchpad/split2_phys/fano.py's split): each taker's
Fano factor and the two takers' co-movement, on Big Pic's triangle (bp3/turnteeth.py's step, run as written up to its
main loop), the THIRD palindrome (toy6/mirror6.py's shears), the swap-symmetric palindrome split per taker and the
coupled one (split3b_probe.py's).
(a) over the 20 stand-in lays of 100,000 rounds at 16 k and 16 k, the lays SPLIT2 (a) and SPLIT3 (3) used: var over lays
    over the mean (fano.py's measure), the covariance, and r^2 = cov^2 / (var a var b) with cov's sign, no root;
(b) within one record: one stand-in lay, 2,000,000 rounds, 200 blocks of 10,000: each taker's Fano factor over the blocks,
    read twice (blocks 1 to 100 and 101 to 200), and the two takers' r^2 with its sign.
Whole numbers; the probe's divisions Rule3's carry; the lay a STAND-IN (a 64-bit carry sequence). argv: the output name."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

out = []
say = out.append
D = 50811429
c, _ = carry(D - 1, 2, 0)
k, _ = carry(D, 1250, 0)
MUL, ADD, MOD = 6364136223846793005, 1442695040888963407, 18446744073709551616
keep = sys.argv
T3: dict = {}
text = HERE.joinpath("bp3", "turnteeth.py").read_text(encoding="utf-8").split("rng = random.Random(31)")[0]
sys.argv = ["turnteeth.py", "50811429", "1", "1", "1250"]
exec(compile(text, "turnteeth.py", "exec"), T3)  # noqa: S102
sys.argv = keep


def cen(v):
    _, r = carry(v + c, D, 0)
    return r - c


def lay(seed, n):
    teeth, s = [], seed
    for _ in range(n):
        _, s = carry(s * MUL + ADD, MOD, 0)
        _, t = carry(s, D, 0)
        teeth.append(t - c)
    return teeth, s


def th(num, den):
    return carry(1000 * num, den, 0)[0]


def tcarry(u, i, x):
    q, r = carry(u[i] + c + x, D, 0)
    u[i] = r - c
    return q


def pal(shears):
    def step(u, x1, x2):
        u = list(u)
        for i, j, sg in shears:
            u[i] = cen(u[i] + sg * u[j])
        q1 = tcarry(u, 0, x1)
        q2 = tcarry(u, 1, x2)
        for i, j, sg in reversed(shears):
            u[i] = cen(u[i] + sg * u[j])
        return u, q1, q2
    return step


def tri(u, x1, x2):
    return T3["step"](u, x1, x2, 1)


THIRD = [(2, 0, 1), (0, 2, -1), (3, 1, 1), (1, 2, 1), (0, 3, 1)]
SPLIT = [(2, 0, 1), (3, 1, 1), (0, 2, 1), (1, 3, 1)]
JOIN = [(2, 0, 1), (3, 1, 1), (0, 2, -1), (1, 3, -1), (2, 0, -1), (3, 1, -1), (0, 3, 1), (1, 2, 1)]
FORMS = (("Big Pic's triangle", tri, 3), ("the THIRD palindrome", pal(THIRD), 4),
         ("the symmetric palindrome split per taker", pal(SPLIT), 4), ("the coupled symmetric palindrome", pal(JOIN), 4))


def split(A, B):
    """fano.py's measures: n^2 var a, n^2 var b, n^2 cov, the sums."""
    n, sa, sb = len(A), sum(A), sum(B)
    va = n * sum(a * a for a in A) - sa * sa
    vb = n * sum(b * b for b in B) - sb * sb
    cv = n * sum(a * b for a, b in zip(A, B)) - sa * sb
    return n, sa, sb, va, vb, cv


def words(A, B):
    n, sa, sb, va, vb, cv = split(A, B)
    sign = "+" if cv > 0 else ("-" if cv < 0 else "0")
    r2 = th(cv * cv, va * vb) if va * vb else 0
    return (f"Fano a {th(va, n * sa)} and b {th(vb, n * sb)} thousandths (independent takes about 1,000); cov {sign},"
            f" r^2 {r2} thousandths; var(a - b) {th(va + vb - 2 * cv, n * n)} against independent takes'"
            f" {th(sa + sb, n)}")


for name, step, teeth in FORMS:
    A, B = [], []
    seed = 12345
    for _ in range(20):
        u, seed = lay(seed, teeth)
        ta = tb = 0
        for _ in range(100000):
            u, q1, q2 = step(u, 16 * k, 16 * k)
            ta, tb = ta + q1, tb + q2
        A.append(ta)
        B.append(tb)
    say(f"(a) {name}, 20 lays of 100,000 at 16 k and 16 k: {words(A, B)}")
    u, _ = lay(4711, teeth)
    A, B = [], []
    for _ in range(200):
        ta = tb = 0
        for _ in range(10000):
            u, q1, q2 = step(u, 16 * k, 16 * k)
            ta, tb = ta + q1, tb + q2
        A.append(ta)
        B.append(tb)
    say(f"(b) {name}, one record of 2,000,000 rounds in 200 blocks of 10,000: all blocks: {words(A, B)}")
    say(f"    blocks 1 to 100: {words(A[:100], B[:100])}")
    say(f"    blocks 101 to 200: {words(A[100:], B[100:])}")

HERE.joinpath(sys.argv[1] if len(sys.argv) > 1 else "split3c_probe.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
