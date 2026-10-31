"""GEN5 probe: Big Pic's turning frame (#2187 6538128481 item 5) on HALF2's 24-gear train, in whole numbers.

Whole numbers only; Rule3's carry the one division (every exact division checked to remainder 0); no root, no
float, no order in the act's parts; the probe's loops and tests are the prober's. Reuses probe_half2, probe_gen3 and
probe_gen4 (their prints silenced). The turn is Cayley's, t = 1/4: c = 13/19, s = 8/19, c^2 + 3 s^2 = 1.
Part A: the toy plane (the axes' x + y + z = 0, one hand): W whole, J = 2 W + I, J^2 = -3; the turn by three carried
        shears with their teeth, undone by the same shears at -t: exact on 20,000 whole points.
Part B: the toy plane's turn laid on the 8-gear train on the three axes, R_axes x I_8: which of the 24 keep it.
Part C: the turn in the 24's own plane on the 24-gear train, T = (38 Pi_2 + 26 Pi_c + 96 Q) / 456: orthogonal, kept by
        the 24, reversed by the r2 lifts; it parts 2' from 2'' (tr(T^k B)), and so does the round spring-then-turn.
Part D: the obstruction to carried shears kept by the 24: the 24's orbit of a vector of the 2' + 2'' part spans a
        Q-invariant space (no shear line); the uniform turn's determinant over the plane's complex structure.
Part E: the power road R^sigma: the bits of its numerators as sigma grows.
"""

import contextlib
import io

import numpy as np

with contextlib.redirect_stdout(io.StringIO()):
    import probe_gen3 as g3
    import probe_gen4 as g4
from probe_half2 import carry, draw, rotation, UNITS

WHOLE, CH = g3.WHOLE, g3.CH
P, Qd = 1, 4  # t = P / Qd
DEN = Qd * Qd + 3 * P * P  # 19


def shear(alpha, beta, num, den, tooth):
    """alpha += carry(num beta, den, tooth): one Rule3 carry, its tooth kept."""
    q, kept = carry(num * beta, den, tooth)
    return alpha + q, kept


def turn_toy(state, sign):
    """The turn in the basis (u, J u) of one plane: S_x(-3t) S_y(2t / (1 + 3t^2)) S_x(-3t), at t or -t (sign)."""
    al, be, r1, r2, r3 = state
    al, r1 = shear(al, be, sign * (-3) * P, Qd, r1)
    be, r2 = shear(be, al, sign * 2 * P * Qd, DEN, r2)
    al, r3 = shear(al, be, sign * (-3) * P, Qd, r3)
    return al, be, r1, r2, r3


def back_toy(state):
    """The run back: the same three shears at -t, in the reverse order (the same, the product being a palindrome),
    each tooth handed back by the carry's sign law (carry(-n, d, r') = (-q, r))."""
    al, be, r1, r2, r3 = state
    al, r3 = shear(al, be, 3 * P, Qd, r3)
    be, r2 = shear(be, al, -2 * P * Qd, DEN, r2)
    al, r1 = shear(al, be, 3 * P, Qd, r1)
    return al, be, r1, r2, r3


def part_a():
    print("PART A: the toy plane x + y + z = 0 (one hand on the three axes)")
    w = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=object)  # placeholder, replaced by w's own turn below
    r = rotation(UNITS[g3.OMEGA])
    w = np.array(r, dtype=object)
    basis = np.array([[1, -1, 0], [0, 1, -1]], dtype=object).T  # the plane's whole lattice
    j = 2 * w + np.eye(3, dtype=object)
    on_plane = j.dot(j.dot(basis))
    print(f"  W is w's turn, whole: {w.tolist()}; J = 2 W + I: J J = -3 on the plane: {(on_plane == -3 * basis).all()}")
    vals, _ = draw(3, 2 * 20000 + 3 * 20000, 10 ** 6)
    exact = 0
    for n in range(20000):
        al, be = vals[2 * n], vals[2 * n + 1]
        t1, _ = carry(vals[40000 + 3 * n], Qd, 0)
        _, r1 = carry(vals[40000 + 3 * n], Qd, 0)
        _, r2 = carry(vals[40000 + 3 * n + 1], DEN, 0)
        _, r3 = carry(vals[40000 + 3 * n + 2], Qd, 0)
        start = (al, be, r1, r2, r3)
        exact += back_toy(turn_toy(start, 1)) == start
    print(f"  three carried shears, teeth kept, undone by the same shears at -t: {exact} of 20000 exact")
    # the shears' product without rounding is the Cayley turn: S_x S_y S_x = [[c, -3 s], [s, c]] (times DEN)
    sx = np.array([[Qd, -3 * P], [0, Qd]], dtype=object)  # x Qd
    sy = np.array([[DEN, 0], [2 * P * Qd, DEN]], dtype=object)  # x DEN
    prod = sx.dot(sy).dot(sx)  # x Qd^2 DEN
    target = np.array([[Qd * Qd - 3 * P * P, -3 * 2 * P * Qd], [2 * P * Qd, Qd * Qd - 3 * P * P]], dtype=object)
    print(f"  the shears' product = Qd^2 x [[c, -3 s], [s, c]] x DEN: {(prod == Qd * Qd * target).all()} "
          f"(c = {Qd * Qd - 3 * P * P}/{DEN}, s = {2 * P * Qd}/{DEN})")
    return w


def part_b(w):
    print("PART B: the toy plane's turn laid on the 8-gear train on the three axes (R_axes x I_8)")
    ones = np.ones((3, 3), dtype=object)
    eye = np.eye(3, dtype=object)
    c_num, s_num = Qd * Qd - 3 * P * P, 2 * P * Qd  # 13, 8 over 19
    r57 = DEN * ones + c_num * (3 * eye - ones) + 3 * s_num * (2 * w + eye - ones)  # 3 DEN R_axes
    print(f"  R_axes whole over {3 * DEN}: orthogonal {(r57.dot(r57.T) == (3 * DEN) ** 2 * eye).all()}; "
          f"commutes with W {(r57.dot(w) == w.dot(r57)).all()}")
    g8, _ = g3.trains()
    big = np.kron(r57, np.eye(8, dtype=object))
    g8x = g3.tensor_axes(g8)
    kept = [g for g in WHOLE if (g8x[g].dot(big) == big.dot(g8x[g])).all()]
    print(f"  kept by {len(kept)} of the 24 whole units (the lifts of w's three turns); the 24 keep it: {len(kept) == 24}")
    turns = sorted({tuple(np.array(rotation(UNITS[g]), dtype=object).flat) for g in kept})
    print(f"  the turns that keep it: {len(turns)} (the identity and w's two)")


def part_c():
    print("PART C: the turn in the 24's own plane on the 24-gear train")
    mats, reps = g4.train24()
    pc_chi = {g: g3.wadd(CH["2'"][g], CH["2''"][g]) for g in WHOLE}
    p2 = g3.projector(mats, CH["2"])
    pc = g3.projector(mats, pc_chi)
    cls = g3.classes()
    q = sum(mats[g] for g in cls[g3.OMEGA]) - sum(mats[g] for g in cls[g3.O2])
    c_num, s_num = Qd * Qd - 3 * P * P, 2 * P * Qd
    # T = Pi_2 / 12 + c Pi_c / 12 + (s / 2) Q, over 12 x 2 x DEN = 456
    d = 12 * 2 * DEN
    nt = 2 * DEN * p2 + 2 * c_num * pc + 12 * s_num * q
    eye = np.eye(24, dtype=object)
    print(f"  T whole over {d}: orthogonal {(nt.dot(nt.T) == d * d * eye).all()}; kept by the 24 "
          f"{all((m.dot(nt) == nt.dot(m)).all() for m in (mats[g] for g in WHOLE))}; each r2 lift turns it back "
          f"{all((mats[g].dot(nt).dot(mats[g].T) == nt.T).all() for g in range(48) if g not in WHOLE)}; "
          f"identity on 2: {(nt.dot(p2) == d * p2).all()}")
    _, b = g4.b_part(mats)
    x, tr = eye.copy(), []
    for _ in range(9):
        tr.append(sum((x * b.T).sum(axis=1)))
        x = x.dot(nt)
    print(f"  tr((456 T)^k B), k = 0 .. 8: {tr}: the turn parts 2' from 2'' (nonzero from k = 1)")
    r = g4.right_h(reps)
    rr = r + r.T
    top = np.concatenate((nt.dot(rr), -nt), axis=1)
    bottom = np.concatenate((nt, 0 * nt), axis=1)
    m = np.concatenate((top, bottom), axis=0)  # x 456: the round (a, b) -> T (rr a - b), T a)
    bb = np.zeros((48, 48), dtype=object)
    bb[:24, :24] = b
    bb[24:, 24:] = b
    x, tr = np.eye(48, dtype=object), []
    for _ in range(9):
        tr.append(sum((x * bb.T).sum(axis=1)))
        x = x.dot(m)
    plain = np.concatenate((np.concatenate((rr, -eye), axis=1), np.concatenate((eye, 0 * eye), axis=1)), axis=0)
    x, tr0 = np.eye(48, dtype=object), []
    for _ in range(9):
        tr0.append(sum((x * bb.T).sum(axis=1)))
        x = x.dot(plain)
    first = next((k for k, t in enumerate(tr) if t != 0), None)
    print(f"  the round spring-then-turn (rr a - b, then T on both slots): tr(M^k (B + B)), k = 0 .. 8, first not 0 at "
          f"k = {first} ({tr[first] if first is not None else 0}): parted {first is not None}; the round with no turn: "
          f"all 0 {all(t == 0 for t in tr0)}: parted {any(t != 0 for t in tr0)}")
    return mats, pc, q


def part_d(mats, pc, q):
    print("PART D: the obstruction to carried shears kept by the 24")
    vals, _ = draw(77, 24, 9)
    v = pc.dot(np.array(vals, dtype=object))
    orbit = [[int(t) for t in mats[g].dot(v)] for g in WHOLE]
    with_q = orbit + [[int(t) for t in q.dot(mats[g].dot(v))] for g in WHOLE]
    r1, r2 = g4.bareiss_rank(orbit), g4.bareiss_rank(with_q)
    print(f"  the 24's orbit of a vector of 2' + 2'' spans rank {r1}; with Q applied, rank {r2}: the orbit's span is "
          f"Q-invariant: {r1 == r2}")
    print("  (Q is a sum of L(g), so every space the 24 keep is Q-invariant: a complex subspace, never one line of a pair (u, J u))")
    print("  and a shear kept by the 24 commutes with Q: the uniform turn would need such shears")
    # the uniform turn's determinant over Q's complex structure, on one copy space: (c + i r3 s)^m, m = 4 copies
    c_num, s_num = Qd * Qd - 3 * P * P, 2 * P * Qd
    re, im = 1, 0  # (re + im r(-3)) / DEN^k
    for _ in range(4):
        re, im = re * c_num - 3 * im * s_num, re * s_num + im * c_num
    print(f"  (c + s r(-3))^4 x DEN^4 = {re} + {im} r(-3), against DEN^4 = {DEN ** 4}: the uniform turn's complex "
          f"determinant on the 4 copies is 1: {(re, im) == (DEN ** 4, 0)}")


def part_e():
    print("PART E: the power road R^sigma (the toy plane, R over DEN)")
    r = np.array([[Qd * Qd - 3 * P * P, -3 * 2 * P * Qd], [2 * P * Qd, Qd * Qd - 3 * P * P]], dtype=object)
    x = np.eye(2, dtype=object)
    marks = {1, 10, 100, 1000}
    for sig in range(1, 1001):
        x = x.dot(r)
        if sig in marks:
            bits = max(int(abs(t)).bit_length() for t in x.flat)
            print(f"  sigma = {sig}: R^sigma = N / {DEN}^{sig}, its largest numerator {bits} bits; the act's width 128")


def main():
    w = part_a()
    part_b(w)
    mats, pc, q = part_c()
    part_d(mats, pc, q)
    part_e()


if __name__ == "__main__":
    main()
