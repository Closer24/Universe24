"""OPEN 3, the twin hand's axis step: the 24 turn the twin train's frame, and its amplitude rows take a sign alone.

usage: python3 -I twin_frame.py <tensor24 src>

A twin hand is held as four integer rows, the quaternion A = a0 + a1 i + a2 j + a3 k (its two hands up and down), in
the frame of its train, one primitive integer quaternion q; the spinor on the board is q A / |q|. A turn g of the 24
lifts to an integer quaternion u (R(u) = g, R(u) v = u v conj(u) / N(u)); the image of a world turns the frame,
u q = c e q' with c the content and e the sign that puts q' in its canonical sign, and leaves every amplitude row as
it is but for the sign e. The act on the twin rows is the 7a gear with the drive: the pull through the Meshes and the
spring (frame-free), and a T1 field b coupled by the left product with the frame-relative field conj(q) b q, whose
norm N(q) is the drive's teeth. Its image is the same act by p18's common factor on the drive alone. Integers only,
the engine's own carry, home and flip.
"""

import itertools
import math
import random
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry, flip, home  # noqa: E402

# ---------- quaternions on Python integers ----------


def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (
        a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
        a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
        a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
        a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
    )


def qconj(q):
    return (q[0], -q[1], -q[2], -q[3])


def qnorm(q):
    return sum(x * x for x in q)


def rot_num(u, v):
    """u v conj(u) for a vector v, the integer numerator of R(u) v (R(u) v = this / N(u))."""
    w = qmul(qmul(u, (0,) + tuple(v)), qconj(u))
    assert w[0] == 0
    return w[1:]


def matvec(g, v):
    return tuple(sum(g[i][j] * v[j] for j in range(3)) for i in range(3))


def det3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def the_24():
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for i in range(3):
                m[i][perm[i]] = signs[i]
            if det3(m) == 1:
                out.append(tuple(tuple(r) for r in m))
    return out


def lift(g):
    """The primitive integer quaternion u with R(u) = g, of least norm, one of its two signs."""
    best = None
    for u in itertools.product(range(-1, 2), repeat=4):
        if u == (0, 0, 0, 0):
            continue
        n = qnorm(u)
        ok = all(
            tuple(x for x in rot_num(u, e)) == tuple(n * y for y in matvec(g, e))
            for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        )
        if ok and (best is None or n < qnorm(best)):
            best = u
    return best


def content(q):
    c = 0
    for x in q:
        c = math.gcd(c, abs(x))
    return c


def canonical(q):
    """q = e q' with e the sign of q's first coordinate that is not 0, so that q' has that coordinate above 0."""
    for x in q:
        if x != 0:
            e = 1 if x > 0 else -1
            return e, tuple(e * y for y in q)
    raise ValueError


# ---------- the board, the twin train and the act ----------

N3 = 3
SITES = [(x, y, z) for x in range(N3) for y in range(N3) for z in range(N3)]
INDEX = {s: i for i, s in enumerate(SITES)}
STEPS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
NB = [[INDEX[tuple((s[k] + d[k]) % N3 for k in range(3))] for d in STEPS] for s in SITES]


def teeth_of(lay):
    """The drive's teeth: its unit times the frame's norm N(q) (the mutant: the unit alone)."""
    return lay[5] * qnorm(lay[7]) if lay[9] else lay[5]


def tick(lay, st):
    """One round on the twin train: the gear's carry on the pull, the spring and the drive of the field's coupling."""
    w, sv, grip, dsp, mu, td0, tk, q, field, _ = lay
    a, b, r, go, rd = st
    teeth = teeth_of(lay)
    qc = qconj(q)
    na, nb_, nr, nrd = [], [], [], []
    for i in range(len(SITES)):
        force = [grip * sum(a[j][k] - a[i][k] for j in NB[i]) - dsp * a[i][k] for k in range(4)]
        bq = qmul(qmul(qc, (0,) + field[i]), q)
        jv = qmul(bq, a[i])
        out = [carry(mu * jv[k], teeth, rd[i][k]) for k in range(4)]
        qd = [o[0] for o in out]
        push = [sv * (force[k] + tk * qd[k]) for k in range(4)]
        p = [w * (a[i][k] - b[i][k]) + (r[i][k] - home(w, go[i][k])) for k in range(4)]
        gq = [carry(p[k] + push[k], w, home(w, go[i][k])) for k in range(4)]
        na.append(tuple(a[i][k] + gq[k][0] for k in range(4)))
        nb_.append(tuple(a[i]))
        nr.append(tuple(gq[k][1] for k in range(4)))
        nrd.append(tuple(o[1] for o in out))
    return (na, nb_, nr, [tuple(x) for x in go], nrd)


def untick(lay, st):
    """The round run back from its now: the sources read on the rebuilt start, the drive undone, the gear undone."""
    w, sv, grip, dsp, mu, td0, tk, q, field, _ = lay
    a1, b1, r1, go, rd1 = st
    a = b1
    teeth = teeth_of(lay)
    qc = qconj(q)
    pa, pb, pr, prd = [], [], [], []
    for i in range(len(SITES)):
        force = [grip * sum(a[j][k] - a[i][k] for j in NB[i]) - dsp * a[i][k] for k in range(4)]
        bq = qmul(qmul(qc, (0,) + field[i]), q)
        jv = qmul(bq, a[i])
        back = [carry(rd1[i][k] - mu * jv[k], teeth, 0) for k in range(4)]
        qd = [-x[0] for x in back]
        rd0 = [x[1] for x in back]
        push = [sv * (force[k] + tk * qd[k]) for k in range(4)]
        qq = [a1[i][k] - b1[i][k] for k in range(4)]
        pp = [qq[k] * w + r1[i][k] - home(w, go[i][k]) - push[k] for k in range(4)]
        dd = [carry(pp[k], w, home(w, go[i][k])) for k in range(4)]
        pa.append(tuple(a[i]))
        pb.append(tuple(a[i][k] - dd[k][0] for k in range(4)))
        pr.append(tuple(dd[k][1] for k in range(4)))
        prd.append(tuple(rd0))
    return (pa, pb, pr, [tuple(x) for x in go], prd)


def image(lay, st, g, u, sign_kept=True, frame_turned=True):
    """The world turned by g with the lift u: the sites and the field by g, the frame by u, the rows by the sign e.

    The frame's image is e u q, e the sign that puts it in its canonical sign; the frame is kept unnormalized, so its
    norm is N(u) N(q) and the drive's teeth scale by L = N(u), p18's common factor on the drive alone."""
    w, sv, grip, dsp, mu, td0, tk, q, field, scaled = lay
    a, b, r, go, rd = st
    e, q2 = canonical(qmul(u, q) if frame_turned else q)
    if not sign_kept:
        e = 1  # the mutant: the frame put in its canonical sign, the sign not handed to the rows
    lay2 = (w, sv, grip, dsp, mu, td0, tk, q2, None, scaled)
    teeth2 = teeth_of(lay2)
    big = teeth2 // teeth_of(lay)
    assert big * teeth_of(lay) == teeth2
    n = len(SITES)
    na, nb_, nr, ngo, nrd, nf = [None] * n, [None] * n, [None] * n, [None] * n, [None] * n, [None] * n
    for i, s in enumerate(SITES):
        j = INDEX[tuple(x % N3 for x in matvec(g, s))]
        na[j] = tuple(e * x for x in a[i])
        nb_[j] = tuple(e * x for x in b[i])
        nr[j] = tuple(x if e == 1 else flip(x, w) for x in r[i])
        ngo[j] = tuple(x if e == 1 else 1 - x for x in go[i])
        mapped = [big * x for x in rd[i]]
        nrd[j] = tuple(x if e == 1 else flip(x, teeth2) for x in mapped)
        nf[j] = matvec(g, field[i])
    lay2 = (w, sv, grip, dsp, mu, td0, tk, q2, nf, scaled)
    return lay2, (na, nb_, nr, ngo, nrd), e, big


def world(rng, q, scaled=True):
    w = rng.randrange(5000, 9000)
    lay = (
        w,  # W = W+
        rng.randrange(1, 4),  # s
        rng.randrange(1, w // 40),  # the grip per Mesh
        rng.randrange(0, w // 30),  # the spring D
        rng.randrange(1, 9),  # the field's strength mu
        rng.randrange(2, 30),  # the drive's teeth per unit of the frame's norm
        rng.randrange(1, 5),  # T_k
        q,
        [tuple(rng.randrange(-6, 7) for _ in range(3)) for _ in SITES],
        scaled,
    )
    teeth = teeth_of(lay)
    a = [tuple(rng.randrange(-400, 401) for _ in range(4)) for _ in SITES]
    b = [tuple(x + rng.randrange(-30, 31) for x in v) for v in a]
    r = [tuple(rng.randrange(0, w) for _ in range(4)) for _ in SITES]
    go = [tuple(rng.randrange(0, 2) for _ in range(4)) for _ in SITES]
    rd = [tuple(rng.randrange(0, teeth) for _ in range(4)) for _ in SITES]
    return lay, (a, b, r, go, rd)


def run(st, lay, ticks):
    for _ in range(ticks):
        st = tick(lay, st)
    return st


def same(x, y):
    return all(list(map(tuple, p)) == list(map(tuple, q)) for p, q in zip(x, y))


def kind_of(g, u):
    n = qnorm(u)
    tr = g[0][0] + g[1][1] + g[2][2]
    return {3: "identity", -1: "half turn (axis)" if n == 1 else "half turn (edge)", 1: "quarter turn", 0: "third turn"}[tr]


def hopf(a):
    """The twin's axis in its frame, A i conj(A): a pure quaternion of norm N(A) (S . S = rho rho)."""
    s = qmul(qmul(a, (0, 1, 0, 0)), qconj(a))
    assert s[0] == 0
    return s[1:]


def main():
    rng = random.Random(20261029)
    group = the_24()
    lifts = [(g, lift(g)) for g in group]
    print(f"the 24 as signed permutation matrices of determinant 1: {len(group)}")
    classes = {}
    for g, u in lifts:
        classes.setdefault((kind_of(g, u), qnorm(u)), []).append(u)
    for (kind, n), members in sorted(classes.items(), key=lambda t: (t[0][1], t[0][0])):
        print(f"  {kind:17s}: {len(members):2d} turns, lift norm {n}, e.g. u = {members[0]}")
    # the lifts close under the product up to a positive scale and a sign (the 48)
    signs = {1: 0, -1: 0}
    for (g, u), (h, v) in itertools.product(lifts, lifts):
        gh = tuple(tuple(sum(g[i][k] * h[k][j] for k in range(3)) for j in range(3)) for i in range(3))
        w_ = dict(lifts)[gh]
        uv = qmul(u, v)
        c = content(uv)
        ratio = [x // c for x in uv]
        e = 1 if tuple(ratio) == tuple(w_) else (-1 if tuple(-x for x in ratio) == tuple(w_) else 0)
        assert e != 0
        signs[e] += 1
    print(f"the lifts' product u_g u_h = (content) (+-1) u_gh at all 576 pairs: +1 at {signs[1]}, -1 at {signs[-1]} (the double cover's sign)")

    frames = [(1, 0, 0, 0), (2, 1, 0, 1), (3, -1, 2, 1), (1, 1, 1, 1)]
    worlds, ticks = 12, 6
    tally = {}
    back_ok = back_n = 0
    hopf_ok = hopf_n = 0
    tt_ok = tt_n = 0
    for wi in range(worlds):
        q = frames[wi % len(frames)]
        lay, st = world(rng, q)
        after = run(st, lay, ticks)
        back = after
        for _ in range(ticks):
            back = untick(lay, back)
        back_n += 1
        back_ok += same(back, st)
        for g, u0 in lifts:
            for u in (u0, tuple(-x for x in u0)):
                lay2, st2, e, big = image(lay, st, g, u)
                lay3, after_img, _, _ = image(lay, after, g, u)
                ok = same(run(st2, lay2, ticks), after_img)
                key = kind_of(g, u0)
                t = tally.setdefault(key, [0, 0, set(), set()])
                t[0] += ok
                t[1] += 1
                t[2].add(e)
                t[3].add(big)
                # the axis on the board turns by g exactly, the density stays
                for i, s in enumerate(SITES):
                    j = INDEX[tuple(x % N3 for x in matvec(g, s))]
                    sf, sf2 = hopf(st[0][i]), hopf(st2[0][j])
                    board = rot_num(q, sf)
                    board2 = rot_num(lay2[7], sf2)
                    lhs = tuple(x * qnorm(q) for x in board2)
                    rhs = tuple(x * qnorm(lay2[7]) for x in matvec(g, board))
                    hopf_n += 1
                    hopf_ok += lhs == rhs and qnorm(st[0][i]) == qnorm(st2[0][j])
        # T on the twin rows: A -> A j, T T = -1
        for v in st[0]:
            tv = qmul(v, (0, 0, 1, 0))
            ttv = qmul(tv, (0, 0, 1, 0))
            tt_n += 1
            tt_ok += ttv == tuple(-x for x in v)
    print(f"\nthe images test: {worlds} worlds of 27 Node-clocks, {ticks} rounds, every turn with both lifts (48):")
    for key, (ok, n, es, bigs) in tally.items():
        print(f"  {key:17s}: {ok} of {n} equal bit for bit; signs e seen {sorted(es)}; the drive's factor L seen {sorted(bigs)}")
    print(f"the run back: {back_ok} of {back_n} worlds return bit for bit after {ticks} rounds")
    print(f"the axis on the board, M(q) S / N(q), turns by g and the density stays: {hopf_ok} of {hopf_n}")
    print(f"T on the twin rows (right product by j): T T = -1 at {tt_ok} of {tt_n} hands; it commutes with every image, the image being a sign")

    # the full turn: four quarter turns about one axis bring the frame back to a positive multiple, the rows' sign -1
    zq = next(u for g, u in lifts if kind_of(g, u) == "quarter turn" and g[2][2] == 1)
    for q in frames:
        f, sign = q, 1
        signs_seen = []
        for turn in range(8):
            e, f = canonical(qmul(zq, f))
            sign *= e
            signs_seen.append(sign)
            if turn == 3:
                four = (f, sign)
        mult = four[0][0] // q[0] if q[0] else None
        print(
            f"the full turn on the frame {q}: after 4 quarter turns about z the frame is {four[0]} = {mult} q and the rows' sign is {four[1]};"
            f" after 8, {f} with the sign {sign}"
        )
    # mutants
    print("\nmutants:")
    for name, kw, scaled in (
        ("the field turned and the frame left unturned", {"frame_turned": False}, True),
        ("the drive's teeth not scaled by the frame's norm", {}, False),
        ("the frame put in its sign and the sign not handed to the rows (a symmetry, not a mutant: the act is odd)", {"sign_kept": False}, True),
    ):
        bad = {}
        for wi in range(4):
            q = frames[wi % len(frames)]
            lay, st = world(rng, q, scaled)
            after = run(st, lay, ticks)
            for g, u0 in lifts:
                for u in (u0, tuple(-x for x in u0)):
                    lay2, st2, e, big = image(lay, st, g, u, **kw)
                    lay3, after_img, _, _ = image(lay, after, g, u, **kw)
                    ok = same(run(st2, lay2, ticks), after_img)
                    b = bad.setdefault(kind_of(g, u0), [0, 0])
                    b[0] += not ok
                    b[1] += 1
        print(f"  {name}: parts at " + ", ".join(f"{k} {v[0]} of {v[1]}" for k, v in bad.items()))
    # the departure: the amplitudes turned in the board's frame, the 4 rows by the lift's left product
    print("  the departure (the rows turned by the lift, the frame kept): the lift's left product on the 4 rows is")
    for (kind, n), members in sorted(classes.items(), key=lambda t: (t[0][1], t[0][0])):
        u = members[0]
        cols = [qmul(u, e) for e in ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))]
        signed_perm = all(sum(1 for x in col if x != 0) == 1 and all(abs(x) in (0, 1) for x in col) for col in cols)
        print(f"    {kind:17s}: {'a signed permutation, so the carries keep it' if signed_perm else f'no signed permutation (each column of norm {n}), so the rows scale by the root of {n} and no carry keeps it'}")


if __name__ == "__main__":
    main()
