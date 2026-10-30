"""Clock: the floor's pump on a slow hand (the G2 readers' finding on N2's p-form and term 13): a gear whose tooth is
counted from 0 answers a sub-notch negative momentum with a whole notch (p div W = -1 for -W < p < 0), and the strides'
squares then wind the 00 slot without bound. Measured on the readers' own one-site replica
(g2_phys/a_source_and_energy_lib.tick1) beside the same hand, clock and source on the edge form, the tooth counted from
the dial's middle (edge_lib.split).
Algebra: whole numbers and Rule3's carry. The edge's source is read at the in-dial: the floor part D_in (v^2 + q1^2)
with q1 the kicked stride split at the now dial (the p-form's sigma_a at the now teeth), the exact part
(p_in^2 + p_kicked^2) div (4 D_in); on a standing clock both equal the replica's 2 w (sb^2 + sa^2) and
2 (p^2 + pa^2) div w.
Board: one Node-clock: the hand on its spring, its 00 slot (teeth at rest), its ii slot; REST 3000, G 210, T_d 1000, as
the readers' check F.
Clicks: n/a.

Run: <t24b>/.venv/bin/python -I probe_pump.py > probe_pump.txt
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.joinpath("g2_phys")))

from a_source_and_energy_lib import tick1  # noqa: E402  (the readers' replica, unchanged)
from edge_lib import split  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402

REST, G, TD = 3000, 210, 1000
W0 = REST
D0 = 2 * W0  # the edge's dial on a standing clock, in half-teeth: half a notch of momentum
HALF_W, _ = carry(W0, 2, 0)


def div(num, den):
    """The whole quotient by Rule3's carry, for a report's mean."""
    q, _ = carry(num, den, 0)
    return int(q)


def marks_round(t, every):
    """1 where the round t is a multiple of every, by one carry."""
    _, rest = carry(t, every, 0)
    return rest == 0


def lay_edge(m0, d=D0):
    """A hand carrying the momentum m0 (in tooth units) on the edge: 4 m0 half-teeth split at 2 D into (v, s)."""
    v, s = split(4 * m0, 2 * d)
    return v, s


def permille(num, den):
    q, _ = carry(1000 * num, den, 0)
    return int(q)


# ------------------------------------------------------------------ A. one gear at rest, one push


def section_a():
    print("A. One gear at rest (stride 0), one push k, W = 3000: the stride it answers with")
    rows = {
        "act as built, tooth 0": lambda k: carry(k, W0, 0)[0],
        "act as built, tooth born at W div 2 (law (i))": lambda k: carry(k, W0, HALF_W)[0],
        "edge, tooth 0 (the middle)": lambda k: split(4 * k, 2 * D0)[0],
    }
    ks = range(-W0, W0 + 1)
    for name, f in rows.items():
        counts = {}
        for k in ks:
            q = int(f(k))
            counts[q] = counts.get(q, 0) + 1
        neg = [k for k in ks if int(f(k)) < 0]
        pos = [k for k in ks if int(f(k)) > 0]
        print(f"   {name}: strides {dict(sorted(counts.items()))} over k in [-3000, 3000];"
              f" a backward notch for k in [{min(neg) if neg else '-'}, {max(neg) if neg else '-'}],"
              f" a forward notch for k in [{min(pos) if pos else '-'}, {max(pos) if pos else '-'}]")
    print("   (the edge: no notch for |k| <= W / 2 = 1500, the tie at |k| = 1500 taken even, 0; one notch beyond, both signs alike)")
    print()


# ------------------------------------------------------------------ B. a free sub-notch momentum


def section_b():
    print("B. A free gear (no force) carrying a momentum m for 100 rounds: the notches it moves")
    for m in (-1, 1, -1499, 1499, -1500, 1500, -1501, 1501, -3000, 3000):
        # the act as built: W v + r = m, r in [0, W)
        v, r = carry(m, W0, 0)
        a = 0
        for _ in range(100):
            q, r = carry(W0 * v, W0, r)
            v = q
            a += q
        built = a
        # the p-form (the readers' replica of the hand alone): a+ = a + p div W, p kept
        ap = 0
        for _ in range(100):
            ap += carry(m, W0, 0)[0]
        # the edge: (v, s) the split of 4 m at 2 D, N = 2 D v + s each round
        v, s = lay_edge(m)
        ae = 0
        for _ in range(100):
            q, s = split(2 * D0 * v + s, 2 * D0)
            v = q
            ae += q
        print(f"   m = {m:6d} ({permille(abs(m), W0):4d} permille of a notch): the act as built moves {built:5d} notches, the p-form {ap:5d}, the edge {ae:5d}")
    print()


# ------------------------------------------------------------------ C. the slow hand on its spring, the clock standing


def hand_p(m0, rounds):
    """The p-form hand alone on a standing clock: p kept, a+ = a + (p - G a) div W; the floor and exact sources summed."""
    a, p = 0, m0
    strides, floor_sum, exact_sum, p_sum, sub = 0, 0, 0, 0, 0
    for _ in range(rounds):
        sb = carry(p, W0, 0)[0]
        pa = p - G * a
        sa = carry(pa, W0, 0)[0]
        floor_sum += 2 * W0 * (sb * sb + sa * sa)
        exact_sum += carry(2 * (p * p + pa * pa), W0, 0)[0]
        if (sb == -1 and -W0 < p < 0) or (sa == -1 and -W0 < pa < 0):
            sub += 2 * W0 * ((sb == -1 and -W0 < p < 0) + (sa == -1 and -W0 < pa < 0))
        p = pa
        a += sa
        strides += sa
        p_sum += p
    return strides, floor_sum, exact_sum, sub, p_sum


def hand_edge(m0, rounds):
    """The edge hand alone on a standing clock: (a, b, s), push -G a, the dial 2 W; the floor source D (v^2 + q1^2) with
    q1 the kicked stride at the dial, the exact (p_in^2 + p_kicked^2) div (4 D)."""
    v, s = lay_edge(m0)
    a, b = 0, -v
    strides, floor_sum, exact_sum, below_half, below_one = 0, 0, 0, 0, 0
    m_sum = 0
    for _ in range(rounds):
        v = a - b
        p_in = 2 * D0 * v + s
        n = p_in + 4 * (-G * a)
        q1, _ = split(n, 2 * D0)
        floor_sum += D0 * (v * v + q1 * q1)
        exact_sum += carry(p_in * p_in + n * n, 4 * D0, 0)[0]
        if abs(p_in) < D0:
            below_half += D0 * (v * v)  # 0 by construction: |p_in| < D gives v = 0
        if abs(p_in) < 2 * D0:
            below_one += D0 * (v * v)
        q, s = split(n, 2 * D0)
        a, b = a + q, a
        strides += q
        m_sum += 2 * D0 * q + s
    return strides, floor_sum, exact_sum, below_half, below_one, m_sum


def section_c():
    rounds = 12000
    print(f"C. The slow hand on its spring (G = 210), the clock standing at W = 3000, no 00 push, {rounds} rounds: laid with the")
    print("   momentum m0; the strides summed (a drift if not 0), the floor source SUM 2 W (sb^2 + sa^2) against the exact SUM 2 p^2 / W,")
    print("   the share of the floor source from a -1 stride at -W < p < 0 (the p-form) or from strides below half a notch and below one")
    print("   notch (the edge), and the mean momentum (the hand's rest), in tooth units")
    for m0 in (-1, 1, -300, -1499, -1500, -3000, 30000):
        sp, fp, ep, subp, psum = hand_p(m0, rounds)
        se, fe, ee, bh, bo, msum = hand_edge(m0, rounds)
        print(f"   m0 = {m0:6d}: p-form: strides sum {sp:7d}, floor {fp:14d}, exact {ep:14d}, floor/exact {permille(fp, ep) if ep else 0:6d} permille,"
              f" from -1 at -W < p < 0: {permille(subp, fp) if fp else 0:4d} permille, mean p {div(psum, rounds):6d};")
        print(f"               edge:   strides sum {se:7d}, floor {fe:14d}, exact {ee:14d}, floor/exact {permille(fe, ee) if ee else 0:6d} permille,"
              f" from below half a notch: {permille(bh, fe) if fe else 0:4d}, below one notch: {permille(bo, fe) if fe else 0:4d} permille, mean momentum {div(msum, 4 * rounds):6d}")
    print()


# ------------------------------------------------------------------ D. the readers' check F on the edge


def tick1_edge(x, exact=False):
    """The readers' one-site replica on the edge form: the hand (a, b, s), the 00 gear (c, cb, s00) at the standing dial
    4 REST, the ii gear (i, ib, sii) at the hand's dials; the drives as theirs (T_d on the metric rows, the hand's kick
    -G a direct). The source read at the in-dial (the docstring); the 00 gear's split first gives W(a+) to the others."""
    a, b, s, c, cb, s00, rd00, i, ib, sii, rdii = x
    wa, wb = REST + c, REST + cb
    d_in = wa + wb
    v = a - b
    p_in = 2 * d_in * v + s
    n = p_in + 4 * (-G * a)
    q1, _ = split(n, 2 * d_in)
    floor_part = d_in * (v * v + q1 * q1)
    exact_part, _ = carry(p_in * p_in + n * n, 4 * d_in, 0)
    j00 = -2 * G * a * a + (exact_part if exact else floor_part)
    jii = 2 * G * a * a
    q00, rd00n = carry(j00, TD, rd00)
    qii, rdiin = carry(jii, TD, rdii)
    # the 00 gear at its standing dial 2 REST (half-teeth 4 REST)
    v00, s00n = split(2 * (2 * REST) * (c - cb) + 4 * q00 + s00, 4 * REST)
    cn = c + v00
    d_out = wa + REST + cn
    q, sn = split(n, 2 * d_out)
    vii, siin = split(2 * d_in * (i - ib) + 4 * qii + sii, 2 * d_out)
    sub_half = int(abs(p_in) < d_in)  # the hand's momentum below half a notch: its stride in is 0
    return (a + q, a, sn, cn, c, s00n, rd00n, i + vii, i, siin, rdiin), (j00, floor_part - exact_part, v, q, wa, sub_half)


def section_d():
    print("D. The readers' check F: a hand on its spring winding its own 00 slot (term 5 in energy units through T_d = 1000),")
    print("   12,000 rounds, one Node-clock; W at rounds 0, 2000, ..., 12000; the readers' replica (the p-form) beside the edge form")
    for exact in (False, True):
        print(f"   The source {'exact, 2 p^2 / W' if exact else 'the strides squared (the floor part), 2 W sigma^2'}:")
        for p0 in (-1, -300, -3000, 30000):
            # the p-form, theirs
            x = (0, p0, 0, 0, 0, 0, 0, 0)
            marks, push, sub_push = [], 0, 0
            for t in range(12001):
                if marks_round(t, 2000):
                    marks.append(REST + x[2])
                if t < 12000:
                    a5, p5, c00 = x[0], x[1], x[2]
                    w = REST + c00
                    sb = carry(p5, w, 0)[0]
                    pa = p5 - G * a5
                    sa = carry(pa, w, 0)[0]
                    x, (j00, _, _, _, _) = tick1(x, exact)
                    push += j00
                    if (sb == -1 and -w < p5 < 0) or (sa == -1 and -w < pa < 0):
                        sub_push += j00
            e0 = div(p0 * p0, REST)
            print(f"     p0 = {p0:6d} (2E0 = {e0:6d}): p-form W = {marks}; the 00 push summed {push}, of it from rounds with a -1 stride at -W < p < 0: {permille(sub_push, push) if push else 0} permille")
            # the edge
            v, s = lay_edge(p0)
            y = (0, -v, s, 0, 0, 0, 0, 0, 0, 0, 0)
            marks_e, push_e, sub_e, strides = [], 0, 0, 0
            for t in range(12001):
                if marks_round(t, 2000):
                    marks_e.append(REST + y[3])
                if t < 12000:
                    y, (j00, _, vin, q, wa, sub_half) = tick1_edge(y, exact)
                    push_e += j00
                    strides += q
                    if sub_half:
                        sub_e += j00
            print(f"                              edge   W = {marks_e}; the 00 push summed {push_e}, of it from rounds with the hand below half a notch: {permille(sub_e, push_e) if push_e else 0} permille; the hand's strides summed {strides}")
    print("   (2E0 = p0^2 / W, the hand's energy at the lay, in the probe's doubled units; a push of 2E0 through T_d winds W by about 2E0 / (T_d REST) notches)")
    print()


def main():
    print("The floor's pump on a slow hand, and the tooth on the edge (whole numbers; REST 3000, G 210, T_d 1000)")
    print()
    section_a()
    section_b()
    section_c()
    section_d()


if __name__ == "__main__":
    main()
