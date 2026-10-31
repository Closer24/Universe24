"""DECODE3g: C-a's check within the counts' grain, on hand-built counts (a test of the check's logic, never a world).
Two clocks of one kind at rest, lines at 2 of every 3 rounds (as DECODE3f section F). Each own count is the true
count within one, so 2r = t2 - t1 - h (two differences of counts) is within two of its true value, and two right
readings of one 2r differ by at most four. The no is forged past that bound: the return leg 3 rounds longer (inside the
grain: it must read SHOWN, the grain cannot tell it) and 9 rounds longer (past it). Whole numbers. argv: the output."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

A_l = [r for r in range(80) if carry(r, 3, 0)[1] != 2]
B_l = list(A_l)


def own(ls, r):
    return sum(1 for t in ls if t < r)


def two_r(X, give, take, Y, b1, b2):
    return own(X, take) - own(X, give) - (own(Y, b2) - own(Y, b1))


ab = two_r(A_l, 9, 21, B_l, 15, 16)
out = [f"C-a: 2r from A to B {ab}; from B to A {two_r(B_l, 9, 21, A_l, 15, 16)}; one 2r within four:"
       f" {abs(ab - two_r(B_l, 9, 21, A_l, 15, 16)) <= 4}"]
for extra in (3, 9):
    ba = two_r(B_l, 9, 21 + extra, A_l, 15, 16)
    out.append(f"  the return leg forged {extra} rounds longer: 2r {ab} against {ba}: one 2r within four"
               f" {abs(ab - ba) <= 4}")
HERE.joinpath(sys.argv[1]).write_text("\n".join(out) + "\n", encoding="utf-8")
