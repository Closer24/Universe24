"""GEN4 probe: the count of rates on HALF2's 24-gear train, and 2' = 2'' at every rate, in whole numbers.

Whole numbers only; Rule3's carry the one division (Bareiss's exact divisions checked to remainder 0); Z[w] as exact
pairs; no root, no order. Reuses probe_half2 and probe_gen3 (imported with probe_gen3's own prints silenced).
Part A: distinct rates of a real symmetric spring = the Krylov rank (the minimal polynomial's degree), on the train,
        on its 2 part and on its 2' + 2'' part: a spring kept by all 48 (drawn), by the 24 whole units alone (drawn),
        and R(h) + R(h^-1), h = (1 + i) / r2 (right multiplication on the units mod sign, whole, kept by all 48).
Part B: 2' and 2'' have the same rates with multiplicity iff tr(C^k B) = 0 for every k, where SUM conj(chi_2'(g)) L(g)
        = A + B w; the no: C + Q, a term odd in Q.
Part C: the act's own steps under R(h) + R(h^-1): the leak out of a laid part in counts (Pi / 12 by the carry), at two
        amplitudes and two round counts; and where W divides every push.
"""

import contextlib
import io

import numpy as np

with contextlib.redirect_stdout(io.StringIO()):
    import probe_gen3 as g3
from probe_half2 import E, INDEX, M1, MUL, UNITS, act_round, carry, draw, induced, qmul

WHOLE, CH = g3.WHOLE, g3.CH


def bareiss_rank(rows):
    """The rank of a whole matrix by fraction-free elimination; every division exact (remainder checked 0)."""
    m = [list(r) for r in rows]
    nr, nc = len(m), len(m[0])
    rank, prev, col = 0, 1, 0
    while rank < nr and col < nc:
        pivot = next((r for r in range(rank, nr) if m[r][col] != 0), None)
        if pivot is None:
            col += 1
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        for r in range(rank + 1, nr):
            for c in range(col + 1, nc):
                num = m[rank][col] * m[r][c] - m[r][col] * m[rank][c]
                q, rem = carry(num, prev, 0)
                assert rem == 0
                m[r][c] = q
            m[r][col] = 0
        prev = m[rank][col]
        rank += 1
        col += 1
    return rank


def krylov(c, v):
    vecs, x = [], v
    for _ in range(len(v) + 1):
        vecs.append([int(t) for t in x])
        x = c.dot(x)
    return bareiss_rank(vecs)


def right_h(g24_reps_unit):
    """R(h) on the 24-gear train: e_[u] -> sign e_[u h], h = (1 + i) / r2 (doubled: r2 (1 + i))."""
    h = INDEX[((0, 1), (0, 1), (0, 0), (0, 0))]
    reps, where = g24_reps_unit
    n = len(reps)
    r = np.zeros((n, n), dtype=object)
    for col, u in enumerate(reps):
        uh = MUL[u][h]
        row, s = where[uh]
        r[row][col] = s
    return r


def train24():
    """The 24-gear train with its representatives: the first of each pair +-u in the units' order."""
    reps, seen, where = [], set(), {}
    for u in range(48):
        if u not in seen:
            seen.add(u)
            seen.add(MUL[M1][u])
            reps.append(u)
    for at, u in enumerate(reps):
        where[u] = (at, 1)
        where[MUL[M1][u]] = (at, -1)
    mats = []
    for g in range(48):
        m = np.zeros((24, 24), dtype=object)
        for col, u in enumerate(reps):
            row, s = where[MUL[g][u]]
            m[row][col] = s
        mats.append(m)
    return mats, (reps, where)


def springs(mats):
    n = len(mats[0])
    out = {}
    for name, group, seed in (("kept by all 48, draw 17", range(48), 17), ("kept by all 48, draw 29", range(48), 29),
                              ("kept by the 24 alone, draw 17", WHOLE, 17)):
        vals, _ = draw(seed, n * n, 3)
        m = np.array(vals, dtype=object).reshape(n, n)
        m = m + m.T
        out[name] = sum(mats[g].dot(m).dot(mats[g].T) for g in group)
    return out


def b_part(mats):
    n = len(mats[0])
    a = np.zeros((n, n), dtype=object)
    b = np.zeros((n, n), dtype=object)
    for g in WHOLE:
        p, q = g3.wconj(CH["2'"][g])
        a = a + p * mats[g]
        b = b + q * mats[g]
    return a, b


def main():
    mats, reps = train24()
    assert all((m.dot(m.T) == np.eye(24, dtype=object)).all() for m in mats)
    pc_chi = {g: g3.wadd(CH["2'"][g], CH["2''"][g]) for g in WHOLE}
    p2 = g3.projector(mats, CH["2"])
    pc = g3.projector(mats, pc_chi)
    cls = g3.classes()
    q = sum(mats[g] for g in cls[g3.OMEGA]) - sum(mats[g] for g in cls[g3.O2])
    r = right_h(reps)
    rr = r + r.T
    all_springs = springs(mats)
    all_springs["R(h) + R(h^-1)"] = rr
    print("PART A: distinct rates (the Krylov rank of a drawn start) on the 24-gear train")
    print(f"  R(h): a signed permutation {((r * r).sum(axis=0) == 1).all()}; kept by all 48 "
          f"{all((m.dot(r) == r.dot(m)).all() for m in mats)}; R(h) + R(h^-1) symmetric {(rr.T == rr).all()}")
    vals, _ = draw(5, 24, 50)
    v = np.array(vals, dtype=object)
    for name, c in all_springs.items():
        keeps48 = all((m.dot(c) == c.dot(m)).all() for m in mats)
        keeps24 = all((mats[g].dot(c) == c.dot(mats[g])).all() for g in WHOLE)
        print(f"  {name}: symmetric {(c.T == c).all()}, kept by the 24 {keeps24}, by all 48 {keeps48}; commutes with Q "
              f"{(c.dot(q) == q.dot(c)).all()}; rates on the train {krylov(c, v)}, on 2 {krylov(c, p2.dot(v))}, "
              f"on 2' + 2'' {krylov(c, pc.dot(v))}")
    print("PART B: 2' and 2'' at every rate: tr(C^k B) for k = 0 .. 24, B the w part of SUM conj(chi_2'(g)) L(g)")
    a, b = b_part(mats)
    print(f"  A + B w checks: A, B whole; tr A = {sum(a[k][k] for k in range(24))}, tr B = {sum(b[k][k] for k in range(24))}")
    for name, c in list(all_springs.items()) + [("the no: R(h) + R(h^-1) + Q (odd in Q)", rr + q)]:
        x = np.eye(24, dtype=object)
        traces = []
        for _ in range(25):
            traces.append(sum((x * b.T).sum(axis=1)))
            x = x.dot(c)
        zero = all(t == 0 for t in traces)
        first = next((k for k, t in enumerate(traces) if t != 0), None)
        print(f"  {name}: tr(C^k B) = 0 for every k: {zero}" + ("" if zero else f" (first k = {first}, value {traces[first]})"))
    print("PART C: the act's own steps under R(h) + R(h^-1) (kept by all 48), the leak in counts")
    for w, exact, size, rounds in ((5, True, 1000, 12), (1000000, False, 1000, 400), (3, False, 1000, 100),
                                   (3, False, 1000, 400), (3, False, 10000, 400), (5, False, 1000, 400),
                                   (6, False, 1000, 400), (6, False, 10000, 400)):
        couple = (w * rr - 2 * w * np.eye(24, dtype=object)) if exact else (rr - 2 * w * np.eye(24, dtype=object))
        for part_name, proj, other in (("2", p2, pc), ("2' + 2''", pc, p2)):
            vals, _ = draw(41 + size + rounds, 48, size)
            a0 = proj.dot(np.array(vals[:24], dtype=object))
            b0 = proj.dot(np.array(vals[24:], dtype=object))
            state, worst, own, moved, raw = (a0, b0, 0 * a0), 0, 0, 0, 0
            for _ in range(rounds):
                new = act_round(state, w, couple)
                moved += int((new[0] != -state[1]).sum())  # a count the spring moved: a+ != -b
                state = new
                leak, _ = carry(other.dot(state[0]), 12, 0)
                mine, _ = carry(proj.dot(state[0]), 12, 0)
                worst = max(worst, max(abs(t) for t in leak))
                raw = max(raw, max(abs(t) for t in other.dot(state[0])))
                own = max(own, max(abs(t) for t in mine))
            tag = "W divides every push" if exact else "the carry rounds"
            print(f"  W = {w} ({tag}), amplitude {size}, {rounds} rounds, laid in {part_name}: counts the spring moved {moved}; "
                  f"the other part's largest entry x12 {raw} (in counts {worst}), its own part's largest count {own}")


if __name__ == "__main__":
    main()
